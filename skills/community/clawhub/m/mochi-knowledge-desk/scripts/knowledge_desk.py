import collections,math,re
from html.parser import HTMLParser
from core import *

class Plain(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def tokens(text):
 text=text.lower();english=re.findall(r'[a-z0-9_]{2,}',text);chinese=[]
 for block in re.findall(r'[\u3400-\u9fff]+',text):chinese.extend([block] if len(block)==1 else [block[n:n+2] for n in range(len(block)-1)])
 return english+chinese
def handle(s,r):
 action=r.get('action');docs=s.all('document')
 if action=='index':
  files=r.get('files');prefix=None
  if files is None:
   prefix=r.get('directory');require(prefix,'Provide files or directory');files=[s.rel(x) for x in walkfiles(s.root,prefix,2000) if x.suffix.lower() in ('.txt','.md','.html','.htm','.csv','.json')]
  require(isinstance(files,list) and len(files)<=2000 and all(isinstance(x,str) for x in files),'Invalid file list')
  require(isinstance(r.get('tags',[]),list) and len(r.get('tags',[]))<=20 and all(isinstance(x,str) and len(x)<=80 for x in r.get('tags',[])),'Invalid tag list')
  changed=[];unchanged=[];skipped=[];totalbytes=0
  for name in sorted(set(files)):
   p=local(s.root,name,'file');require(p.suffix.lower() in ('.txt','.md','.html','.htm','.csv','.json'),'Unsupported document type')
   raw=readbytes(p,8*1024*1024);totalbytes+=len(raw);require(totalbytes<=32*1024*1024,'Index batch exceeds 32 MiB');key=sha(name.encode())[:32];old=s.get('document',key);digest=sha(raw)
   if old and old['sha256']==digest and old.get('tags',[])==r.get('tags',[]):unchanged.append(name);continue
   text=raw.decode('utf-8-sig')
   if p.suffix.lower() in ('.html','.htm'):
    parser=Plain();parser.feed(text);text='\n'.join(parser.parts)
   paragraphs=[text[n:n+1500] for n in range(0,len(text),1500)];require(len(paragraphs)<=6000,'Document has too many chunks')
   chunks=[{'number':n+1,'text':s1,'counts':dict(collections.Counter(tokens(s1)))} for n,s1 in enumerate(paragraphs)]
   s.put('document',key,{'id':key,'path':name,'sha256':digest,'indexedAt':now(),'tags':r.get('tags',[]),'chunks':chunks});changed.append(name)
  pruned=[]
  if prefix and r.get('prune') is True:
   prefix=Path(prefix).as_posix().rstrip('/')+'/'
   for d in docs:
    if d['path'].startswith(prefix) and d['path'] not in files:s.delete('document',d['id']);pruned.append(d['path'])
  return {'indexed':changed,'unchanged':unchanged,'pruned':pruned,'documentCount':len(s.all('document'))}
 if action=='list':return [{'id':d['id'],'path':d['path'],'sha256':d['sha256'],'chunks':len(d['chunks']),'tags':d['tags']} for d in docs]
 if action=='remove':
  key=ident(r['id']);require(s.get('document',key) is not None,'Document ID not found');s.delete('document',key);return {'removedFromIndex':key,'sourceDeleted':False}
 if action=='search':
  query=r.get('query','').strip();require(query and len(query)<=300,'Provide a query of 1..300 characters');wanted=set(tokens(query));require(wanted,'Query needs words or Chinese characters')
  if r.get('tag'):docs=[d for d in docs if r['tag'] in d['tags']]
  chunks=[(d,c) for d in docs for c in d['chunks']];df={t:sum(t in c['counts'] for d,c in chunks) for t in wanted};hits=[]
  for d,c in chunks:
   score=sum((1+math.log(c['counts'][t]))*math.log(1+(len(chunks)+1)/(df[t]+1)) for t in wanted if t in c['counts'])
   phrase=query.lower() in c['text'].lower()
   if not score and not phrase:continue
   score=(score+(5 if phrase else 0))/math.sqrt(max(1,len(c['text'])/300))
   at=c['text'].lower().find(query.lower());at=max(0,at-100) if at>=0 else 0
   p=local(s.root,d['path']);fresh=p.is_file() and sha(readbytes(p,8*1024*1024))==d['sha256']
   hits.append({'source':d['path'],'chunk':c['number'],'citation':d['path']+'#chunk-'+str(c['number']),'score':round(score,4),'snippet':c['text'][at:at+600],'sourceSha256':d['sha256'],'indexCurrent':fresh})
  hits.sort(key=lambda x:(-x['score'],x['source'],x['chunk']));return s.report({'query':query,'totalHits':len(hits),'matches':hits[:limit(r.get('limit',10),1,50)],'indexedDocuments':len(docs)},'Knowledge search')
 if action=='export':return s.report({'documents':handle(s,{'action':'list'})},'Knowledge index')
 raise ValueError('Actions: index, search, list, remove, export')
