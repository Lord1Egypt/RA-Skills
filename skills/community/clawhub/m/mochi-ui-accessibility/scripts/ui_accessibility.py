from helpers import *
from html.parser import HTMLParser

class Audit(HTMLParser):
 def __init__(self):super().__init__();self.lang=False;self.ids={};self.labels=set();self.inputs=[];self.issues=[];self.heading=0;self.stack=[];self.buttons=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='html':self.lang=bool(d.get('lang'))
  if d.get('id'):
   if d['id'] in self.ids:self.issues.append({'rule':'duplicate-id','id':d['id']})
   self.ids[d['id']]=t
  if t=='label' and d.get('for'):self.labels.add(d['for'])
  if t=='img' and 'alt' not in d:self.issues.append({'rule':'missing-image-alt','line':self.getpos()[0]})
  if t in ('input','select','textarea') and d.get('type') not in ('hidden','submit','button','reset'):
   self.inputs.append((d,any(x=='label' for x in self.stack),self.getpos()[0]))
  if re.fullmatch(r'h[1-6]',t):
   level=int(t[1]);
   if self.heading and level>self.heading+1:self.issues.append({'rule':'heading-level-skip','line':self.getpos()[0]})
   self.heading=level
  if t=='button':self.buttons.append({'name':d.get('aria-label',''),'labelledby':d.get('aria-labelledby',''),'text':'','line':self.getpos()[0],'open':True})
  if t not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.stack.append(t)
 def handle_data(self,data):
  for b in self.buttons:
   if b['open']:b['text']+=data
 def handle_endtag(self,t):
  if t=='button':
   for b in reversed(self.buttons):
    if b['open']:b['open']=False;break
  if t in self.stack:
   i=len(self.stack)-1-self.stack[::-1].index(t);self.stack=self.stack[:i]
 def finish(self):
  if not self.lang:self.issues.append({'rule':'missing-document-language'})
  for d,nested,line in self.inputs:
   refs=d.get('aria-labelledby','').split()
   if not (nested or d.get('id') in self.labels or d.get('aria-label') or refs and all(k in self.ids for k in refs)):self.issues.append({'rule':'input-without-label','line':line})
  for b in self.buttons:
   if not (b['name'].strip() or b['text'].strip() or b['labelledby'] and all(k in self.ids for k in b['labelledby'].split())):self.issues.append({'rule':'empty-button','line':b['line']})
  return self.issues

def contrast(a,b):
 def lum(c):
  require(isinstance(c,str) and re.fullmatch(r'#[0-9a-fA-F]{6}',c),'Colours must be #RRGGBB');v=[int(c[i:i+2],16)/255 for i in (1,3,5)];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return sum(x*w for x,w in zip(v,[.2126,.7152,.0722]))
 x,y=sorted([lum(a),lum(b)]);return round((y+.05)/(x+.05),3)

def handle(s,r):
 require(r.get('action')=='audit','Action: audit');p=Audit();p.feed(textfile(s.root,r['file']));issues=p.finish();ratios=[]
 for x in objects({'pairs':r.get('contrast',[])},'pairs',100):
  ratio=contrast(x['foreground'],x['background']);ratios.append({'foreground':x['foreground'],'background':x['background'],'ratio':ratio,'normalTextAA':ratio>=4.5,'largeTextAA':ratio>=3})
 return s.report({'issues':issues,'contrast':ratios,'scope':'Static HTML and explicit opaque colour pairs only; inspect keyboard, focus, rendered states and assistive technology separately.'})
