#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import time
from google.appengine.ext import db
template_dir=os.path.join(os.path.dirname(__file__),'templates')

jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
          autoescape=True)



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t= jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def render_front(self, title="", bloge=""):
        posts=db.GqlQuery("SELECT * FROM Bloge ORDER BY created DESC LIMIT 5")
        self.render("front.html",title=title, bloge=bloge,  posts=posts)

    def get(self):
        self.render_front()


class NewPost(Handler):

    def get(self):
        self.render("newpost.html")

    def post(self):
        title=self.request.get("title")
        bloge=self.request.get("bloge")

        if title and bloge:
            blogpost=Bloge(title=title, bloge=bloge)
            blogpost.put()
            time.sleep(0.25)

            self.redirect('/blog'+str(blogpost.key().id()))
        else:
            error="Please enter a title and post!"
            self.render_front(title, bloge, error)

class ViewPostHandler(Handler):
    def get(self, id):
        posts=blogpost.get_by_id(int(id))
        self.render("front.html", posts=posts)

class Bloge(db.Model):
    title=db.StringProperty(required=True)
    bloge=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)





app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', MainPage),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
