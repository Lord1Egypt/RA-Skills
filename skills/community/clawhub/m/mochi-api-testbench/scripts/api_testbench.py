import time
from core import *

def pointer(value,path):
 require(isinstance(path,str) and (not path or path.startswith('/')),'JSON pointer must be empty or start with /')
 for part in path.split('/')[1:]:
  part=part.replace('~1','/').replace('~0','~')
  value=value[int(part)] if isinstance(value,list) else value[part]
 return value
def validate(r):
 cases=r.get('cases');require(isinstance(cases,list) and 1<=len(cases)<=25,'Provide 1..25 test cases');seen=set()
 for case in cases:
  require(isinstance(case,dict),'Each case must be an object');key=ident(case['id']);require(key not in seen,'Duplicate test case ID');seen.add(key)
  u=urlsplit(case['url']);require(u.hostname and not u.username and not u.password and not u.fragment,'Invalid URL');method=case.get('method','GET').upper();require(method in ('GET','HEAD','OPTIONS','POST','PUT','PATCH','DELETE'),'Invalid method')
  require(method in ('GET','HEAD','OPTIONS') or r.get('allowMutations') is True,'Write requests need allowMutations:true and user authorization')
  require(isinstance(case.get('headers',{}),dict) and isinstance(case.get('headerEnv',{}),dict),'Headers must be objects')
  for env in case.get('headerEnv',{}).values():require(isinstance(env,str) and re.fullmatch('[A-Za-z_][A-Za-z0-9_]*',env),'Invalid environment variable name')
  checks=case.get('assert',{});require(isinstance(checks,dict),'Assertions must be an object');require(set(checks)<=set(('status','jsonEquals','jsonExists','bodyContains','headers','maxMilliseconds')),'Unknown assertion')
  require(checks,'Each case needs assertions')
 return cases
def handle(s,r):
 a=r.get('action');require(a in ('validate','run','compare'),'Actions: validate, run, compare')
 if a=='compare':
  before=readjson(local(s.root,r['before'],'file'));after=readjson(local(s.root,r['after'],'file'));left={x['id']:x for x in before['cases']};right={x['id']:x for x in after['cases']};rows=[]
  for key in sorted(left.keys()&right.keys()):rows.append({'id':key,'beforePassed':left[key]['passed'],'afterPassed':right[key]['passed'],'beforeMs':left[key]['milliseconds'],'afterMs':right[key]['milliseconds'],'regression':left[key]['passed'] and not right[key]['passed']})
  return s.report({'cases':rows,'added':sorted(right.keys()-left.keys()),'removed':sorted(left.keys()-right.keys())},'API regression comparison')
 cases=validate(r)
 if a=='validate':return {'valid':True,'cases':len(cases),'networkRequests':0}
 private=r.get('allowPrivateHosts',[]);require(isinstance(private,list) and all(isinstance(x,str) for x in private),'Private host allowlist must be a list');rows=[];prepared=[]
 for case in cases:
  headers=dict(case.get('headers',{}));secret_values=[]
  for name,env in case.get('headerEnv',{}).items():
   value=os.environ.get(env);require(value,'Required header environment variable is empty');headers[name]=value;secret_values.append(value)
  if case.get('bearerEnv'):
   value=os.environ.get(case['bearerEnv']);require(value,'Bearer environment variable is empty');headers['Authorization']='Bearer '+value;secret_values.append(value)
  body=None
  if 'json' in case:body=jsonbytes(case['json']);headers.setdefault('Content-Type','application/json')
  elif 'body' in case:require(isinstance(case['body'],str),'Body must be text');body=case['body'].encode()
  require(body is None or len(body)<=1024*1024,'Request body too large');prepared.append((case,headers,secret_values,body))
 for case,headers,secret_values,body in prepared:
  start=time.monotonic();checks=[];error=None;status=None
  try:
   response=safe_request(case['url'],case.get('method','GET').upper(),headers,body,private_hosts=private);status=response['status'];text=response['body'].decode('utf-8','replace');rule=case['assert'];parsed=None
   if 'status' in rule:checks.append({'check':'status','passed':status in rule['status'] if isinstance(rule['status'],list) else status==rule['status']})
   if 'headers' in rule:
    for name,value in rule['headers'].items():checks.append({'check':'header:'+name,'passed':response['headers'].get(name.lower())==str(value)})
   if rule.get('jsonEquals') or rule.get('jsonExists'):
    try:parsed=json.loads(text)
    except ValueError:checks.append({'check':'jsonParse','passed':False})
   for path,value in rule.get('jsonEquals',{}).items():
    try:ok=pointer(parsed,path)==value
    except (KeyError,TypeError,ValueError,IndexError):ok=False
    checks.append({'check':'jsonEquals:'+path,'passed':ok})
   for path in rule.get('jsonExists',[]):
    try:pointer(parsed,path);ok=True
    except (KeyError,TypeError,ValueError,IndexError):ok=False
    checks.append({'check':'jsonExists:'+path,'passed':ok})
   for n,value in enumerate(rule.get('bodyContains',[])):checks.append({'check':'bodyContains#'+str(n+1),'passed':str(value) in text})
  except Exception as e:error=type(e).__name__
  elapsed=round((time.monotonic()-start)*1000,2)
  if 'maxMilliseconds' in case['assert']:checks.append({'check':'maxMilliseconds','passed':elapsed<=float(case['assert']['maxMilliseconds'])})
  u=urlsplit(case['url']);url=u.scheme+'://'+u.netloc+u.path
  for secret in secret_values:url=url.replace(secret,'[REDACTED]')
  rows.append({'id':case['id'],'urlWithoutQuery':url,'method':case.get('method','GET').upper(),'status':status,'milliseconds':elapsed,'checks':checks,'errorType':error,'passed':not error and bool(checks) and all(x['passed'] for x in checks)})
 data={'createdAt':now(),'cases':rows,'passed':all(x['passed'] for x in rows),'casesAttempted':len(rows),'responseBodiesSaved':False,'credentialsSaved':False}
 return s.report(data,'API test results',(['id','method','urlWithoutQuery','status','milliseconds','passed','errorType'],rows))
