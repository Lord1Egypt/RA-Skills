from helpers import *
from collections import Counter

def handle(s,r):
 require(r.get('action')=='triage','Action: triage');items=rows_file(s,r);at=date(r['asOf']);rows=[];numbers=set();seen=Counter();repository=None
 limit(r.get('staleDays',30),1,3650)
 for x in items:
  number=limit(x['number'],1,10**9);require(number not in numbers,'Duplicate issue number');numbers.add(number);title=text(x['title'],2000);updated=date(x['updatedAt']);require(updated<=at,'asOf precedes issue timestamp');u=public_url(x['url']);require(urlsplit(u).hostname=='github.com','Expected github.com issue URL')
  match=re.fullmatch(r'/([^/]+)/([^/]+)/(issues|pull)/(\d+)/?',urlsplit(u).path);require(match and int(match[4])==number,'Issue URL must match its number');repo=match[1]+'/'+match[2]
  require(repository is None or repository==repo,'Export one repository per request');repository=repo
  state=x.get('state','OPEN').upper();require(state in ('OPEN','CLOSED','MERGED'),'Unknown state');age=(at-updated).total_seconds()/86400;assignees=x.get('assignees',[]);labels=x.get('labels',[]);require(isinstance(assignees,list) and isinstance(labels,list),'Invalid assignees/labels');names=[text(v['name'],100) if isinstance(v,dict) else text(v,100) for v in labels]
  seen.update(names);rows.append({'number':number,'title':title,'url':u,'state':state,'daysSinceUpdate':int(age),'unassigned':not assignees,'labels':names,'needsTriage':state=='OPEN' and (not assignees or age>=r.get('staleDays',30))})
 limit(r.get('staleDays',30),1,3650);duplicates=[]
 require(len(rows)<=2000,'Too many issues for pairwise review')
 tokens=[set(re.findall(r'[\w\u3400-\u9fff]+',x['title'].casefold())) for x in rows]
 # Bound comparisons to 250k; large repositories should export a narrower query.
 require(len(rows)*(len(rows)-1)//2<=250000,'Narrow the issue export before similarity analysis')
 for i,a in enumerate(rows):
  for j in range(i+1,len(rows)):
   union=tokens[i]|tokens[j];score=len(tokens[i]&tokens[j])/len(union) if union else 0
   if score>=.8:duplicates.append({'numbers':[a['number'],rows[j]['number']],'titleTokenSimilarity':round(score,3)})
 return s.report({'asOf':at.isoformat(),'issues':rows,'possibleDuplicates':duplicates,'labelCounts':dict(seen),'remoteChanges':False,'note':'Triage hints only; similar titles are not proof of duplicate issues.'},table=(['number','title','state','daysSinceUpdate','unassigned','needsTriage'],rows))
