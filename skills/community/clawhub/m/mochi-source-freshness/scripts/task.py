import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 now=instant(r['asOf']);limit=int(r.get('maxAgeDays',30));need(limit>=0,'maxAgeDays must be nonnegative');rows=[]
 for x in r['sources']:
  date=x.get('updatedAt') or x.get('publishedAt');age=(now-instant(date)).total_seconds()/86400 if date else None
  rows.append({'id':x['id'],'url':x['url'],'ageDays':round(age,2) if age is not None else None,'state':'unknown-date' if age is None else 'future-date' if age<0 else 'stale' if age>limit else 'within-window','eventDate':x.get('eventDate')})
 return {'sources':rows,'staleCount':sum(x['state']=='stale' for x in rows),'truthVerified':False}
