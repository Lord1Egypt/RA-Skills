import collections,time
from html.parser import HTMLParser
from urllib.parse import urldefrag,urlunsplit
from core import *

class Page(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.links=[];self.ids=set();self.title=[];self.intitle=False;self.h1=0;self.images=0;self.missingAlt=0;self.canonical=[];self.description=[];self.robots=[];self.base=None
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if attrs.get('id'):self.ids.add(attrs['id'])
  if tag=='a':
   if attrs.get('name'):self.ids.add(attrs['name'])
   if attrs.get('href'):self.links.append(attrs['href'])
  if tag=='title':self.intitle=True
  if tag=='h1':self.h1+=1
  if tag=='img':self.images+=1;self.missingAlt+=int('alt' not in attrs)
  if tag=='base' and attrs.get('href'):self.base=attrs['href']
  if tag=='link' and 'canonical' in attrs.get('rel','').lower().split():self.canonical.append(attrs.get('href',''))
  if tag=='meta' and attrs.get('name','').lower()=='description':self.description.append(attrs.get('content',''))
  if tag=='meta' and attrs.get('name','').lower()=='robots':self.robots.append(attrs.get('content',''))
 def handle_endtag(self,tag):
  if tag=='title':self.intitle=False
 def handle_data(self,data):
  if self.intitle:self.title.append(data)
def clean(url):
 p=urlsplit(urldefrag(url)[0]);return urlunsplit((p.scheme,p.netloc,p.path or '/',p.query,''))
def handle(s,r):
 require(r.get('action')=='crawl','Action: crawl');root=clean(r['url']);u=urlsplit(root);origin=(u.scheme,u.netloc);maximum=limit(r.get('maxPages',20),1,60);private=r.get('allowPrivateHosts',[])
 require(u.scheme=='https' or u.hostname in private,'Start with HTTPS');queue=collections.deque([root]);seen=set();pages=[];edges=[];ids={};titles=collections.defaultdict(list);request_count=0
 while queue and len(seen)<maximum:
  url=queue.popleft()
  if url in seen:continue
  seen.add(url);started=time.monotonic();row={'url':url,'status':None,'errorType':None};parser=None
  try:
   response=safe_request(url,private_hosts=private,redirects=3);request_count+=1;row.update(status=response['status'],finalUrl=response['url'],milliseconds=round((time.monotonic()-started)*1000,2))
   if 'text/html' in response['headers'].get('content-type','').lower():
    parser=Page();parser.feed(response['body'].decode('utf-8','replace'));title=''.join(parser.title).strip();titles[title].append(url);ids[url]=parser.ids
    row.update(title=title,h1Count=parser.h1,images=parser.images,missingAlt=parser.missingAlt,canonical=parser.canonical,description=parser.description,robots=parser.robots)
    base=urljoin(response['url'],parser.base) if parser.base else response['url']
    for href in parser.links[:2000]:
     target=urljoin(base,href);parts=urlsplit(target)
     if parts.scheme not in ('https','http'):continue
     target_base=clean(target);internal=(parts.scheme,parts.netloc)==origin;edges.append({'source':url,'target':target_base,'fragment':parts.fragment,'internal':internal})
     if internal and target_base not in seen and len(queue)<3000:queue.append(target_base)
  except Exception as e:row['errorType']=type(e).__name__
  pages.append(row)
 index={x['url']:x for x in pages};broken=[];fragments=[]
 for edge in edges:
  target=index.get(edge['target'])
  if target and (target['errorType'] or target['status'] is not None and target['status']>=400):broken.append(edge|{'status':target['status'],'errorType':target['errorType']})
  if edge['fragment'] and edge['target'] in ids and edge['fragment'] not in ids[edge['target']]:fragments.append(edge)
 external=sorted({e['target'] for e in edges if not e['internal']});external_checks=[]
 if r.get('checkExternal'):
  for url in external[:limit(r.get('maxExternal',10),1,20)]:
   try:rr=safe_request(url,method='HEAD',private_hosts=private,redirects=2);external_checks.append({'url':url,'status':rr['status']});request_count+=1
   except Exception as e:external_checks.append({'url':url,'errorType':type(e).__name__})
 data={'root':root,'pages':pages,'visited':len(pages),'maximumPages':maximum,'limitReached':bool(queue),'brokenInternalLinks':broken,'missingFragments':fragments,'duplicateTitles':[{'title':k,'pages':v} for k,v in titles.items() if k and len(v)>1],'pagesMissingTitle':[x['url'] for x in pages if x.get('title')==''],'externalLinks':external,'externalChecks':external_checks,'uncheckedInternalLinks':len({e['target'] for e in edges if e['internal'] and e['target'] not in index}),'requestCount':request_count,'javascriptRendered':False}
 return s.report(data,'Website link and content audit',(['url','status','title','h1Count','missingAlt','milliseconds','errorType'],pages))
