import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 now=instant(r['asOf']);groups=collections.defaultdict(list);expired=[]
 for x in r['facts']:
  need(x.get('source') and x.get('key'),'Every fact needs a key and source')
  if x.get('expiresAt') and instant(x['expiresAt'])<=now:expired.append(x['key']);continue
  groups[x['key']].append(x)
 conflicts={k:[{'value':x['value'],'source':x['source']} for x in xs] for k,xs in groups.items() if len({json.dumps(x['value'],sort_keys=True) for x in xs})>1}
 return {'currentFacts':{k:xs[-1]['value'] for k,xs in groups.items() if k not in conflicts},'conflicts':conflicts,'expiredKeys':expired,'memoryFilesModified':False}
