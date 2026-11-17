import collections,csv,datetime as dt,email.parser,email.policy,html,io,itertools,json,re,statistics,textwrap,urllib.parse,xml.etree.ElementTree as ET
from runtime import need,instant,decimal,table,safezip

def handle(r,c):
 cases=r['cases'];need(cases and len({x['id'] for x in cases})==len(cases),'Case IDs must be unique and nonempty');results=[]
 for x in cases:
  actual=x['actual'];checks=[t in actual for t in x.get('mustContain',[])]+[t not in actual for t in x.get('mustNotContain',[])]
  if 'exact' in x:checks.append(actual==x['exact'])
  need(checks,'Each case needs an expectation');results.append({'id':x['id'],'passed':all(checks),'checks':len(checks)})
 return {'cases':results,'passed':sum(x['passed'] for x in results),'total':len(results),'modelWasCalled':False,'semanticQualityScored':False}
