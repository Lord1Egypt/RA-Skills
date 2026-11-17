from helpers import *
from collections import defaultdict

def handle(s,r):
 require(r.get('action')=='map','Action: map');base=local(s.root,r['directory'],'dir');paths=[p for p in walkfiles(s.root,r['directory'],2000) if p.suffix.lower()=='.md'];notes={p.relative_to(base).as_posix():p for p in paths};stems=defaultdict(list);heads={};links=[];missing=[];incoming=defaultdict(int)
 for n,p in notes.items():
  stems[p.stem.casefold()].append(n);content=re.sub(r'```.*?```','',textfile(s.root,s.rel(p)),flags=re.S);heads[n]={x.strip().casefold() for x in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',content,re.M)}
 for n,p in notes.items():
  content=re.sub(r'```.*?```','',textfile(s.root,s.rel(p)),flags=re.S)
  for raw in re.findall(r'!?\[\[([^\]]+)\]\]',content):
   target=raw.split('|',1)[0];part,sep,anchor=target.partition('#');candidates=[]
   if not part:candidates=[n]
   else:
    require(not part.startswith(('/', '\\')) and '..' not in Path(part.replace('\\','/')).parts,'Wiki link escapes vault')
    part=part.replace('\\','/');part=part if part.lower().endswith('.md') else part+'.md'
    relative=(Path(n).parent/part).as_posix()
    if relative in notes:candidates=[relative]
    elif part in notes:candidates=[part]
    elif '/' not in part:candidates=stems[Path(part).stem.casefold()]
   valid=len(candidates)==1;to=candidates[0] if valid else None
   if valid and anchor and anchor.casefold() not in heads[to]:missing.append({'from':n,'target':target,'reason':'heading-not-found'})
   elif not valid:missing.append({'from':n,'target':target,'reason':'ambiguous' if candidates else 'note-not-found'})
   if valid:incoming[to]+=1;links.append({'from':n,'to':to,'anchor':anchor})
 return s.report({'notes':sorted(notes),'links':links,'brokenLinks':missing,'orphans':[n for n in notes if not incoming[n]],'backlinks':{n:[e['from'] for e in links if e['to']==n] for n in notes},'scope':'Markdown wikilinks and heading names; no block IDs, plugins or note modifications.'})
