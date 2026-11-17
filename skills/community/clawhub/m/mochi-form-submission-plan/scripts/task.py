import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 fields=r['fields'];need(isinstance(fields,list),'fields must be a list');names=[x['name'] for x in fields];need(len(names)==len(set(names)),'Duplicate field name');values=r.get('values',{});missing=[x['name'] for x in fields if x.get('required') and ((x.get('type')=='checkbox' and values.get(x['name']) is not True) or not str(values.get(x['name'],'')).strip())]
 unknown=sorted(set(values)-set(names));sensitive=[x['name'] for x in fields if x.get('sensitive') or x.get('type') in ['password','file']]
 return {'readyForReview':not missing and not unknown,'missing':missing,'unknown':unknown,'sensitiveFields':sensitive,'fieldNamesToFill':[n for n in names if n in values],'submissionPerformed':False,'finalAction':r.get('finalAction','submit')}
