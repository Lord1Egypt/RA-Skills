import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 budget=int(r['maxChars']);need(budget>0,'maxChars must be positive');docs=r['documents'];need(len({x['id'] for x in docs})==len(docs),'Duplicate document ID');parts=[];selected=[];omitted=[];used=0
 for x in sorted(docs,key=lambda x:(-int(x.get('priority',0)),x['id'])):
  text='## '+x['id']+'\n'+x['text'].strip()+'\n';n=len(text)+(1 if parts else 0)
  if used+n<=budget:parts.append(text);selected.append(x['id']);used+=n
  else:omitted.append(x['id'])
 c.emit('context.md','\n'.join(parts));return {'selected':selected,'omitted':omitted,'characters':used,'tokenCountEstimated':False,'sourceTextsChanged':False}
