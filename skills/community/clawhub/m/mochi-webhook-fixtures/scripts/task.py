import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 events=r['events'];seen=set();out=[];duplicates=[]
 for x in events:
  event=x['id'];need(event and 'payload' in x,'Each event needs an ID and payload')
  if event in seen:duplicates.append(event);continue
  seen.add(event);out.append({'id':event,'payload':x['payload']})
 c.emit('fixtures.jsonl',''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out));return {'uniqueEvents':len(out),'duplicateIds':duplicates,'replayedOverNetwork':False}
