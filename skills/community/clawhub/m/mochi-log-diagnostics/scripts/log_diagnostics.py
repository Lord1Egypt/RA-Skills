import collections,gzip
from core import *
ACCESS=re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "([A-Z]+) (.*?) HTTP/[^\"]+" (\d{3}) (\d+|-)\s*(?:"([^\"]*)" "([^\"]*)")?')
def scrub(text):
 text=re.sub(r'(?i)\b(authorization|password|token|api[_-]?key|secret)\s*[:=]\s*[^\s,;]+',r'\1=[REDACTED]',text)
 text=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}','[EMAIL]',text);return text[:300]
def parsed(line):
 if line.lstrip().startswith('{'):
  v=json.loads(line);require(isinstance(v,dict),'Log entry must be an object')
  status=v.get('status',v.get('statusCode'))
  if status is not None:require(str(status).isdigit() and 100<=int(status)<=599,'Invalid status code');status=int(status)
  return {'time':str(v.get('timestamp',v.get('time',''))),'status':status,'level':str(v.get('level','')).lower(),'path':str(v.get('path',v.get('url',''))).split('?')[0],'message':scrub(str(v.get('message',v.get('msg','')))),'ip':str(v.get('ip',v.get('remote_addr',''))),'ua':str(v.get('userAgent',v.get('user_agent',''))),'bytes':v.get('bytes',0)}
 m=ACCESS.match(line)
 if m:
  ip,time,method,path,status,size,ref,ua=m.groups();time=dt.datetime.strptime(time,'%d/%b/%Y:%H:%M:%S %z').isoformat()
  return {'ip':ip,'time':time,'method':method,'path':path.split('?')[0],'status':int(status),'level':'','message':'','ua':ua or '', 'bytes':0 if size=='-' else int(size)}
 m=re.match(r'^\[?(\d{4}-\d\d-\d\d[T ][\d:.+-]+Z?)\]?\s+\[?(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\]?\s*[: -]?(.*)',line,re.I)
 require(m is not None,'Unrecognized log format');return {'time':m[1],'level':m[2].lower(),'message':scrub(m[3]),'path':'','status':None,'ip':'','ua':'','bytes':0}
def handle(s,r):
 require(r.get('action')=='analyze','Action: analyze');files=r.get('files');require(isinstance(files,list) and 1<=len(files)<=20,'Provide 1..20 log files')
 for key in ('dateFrom','dateTo'):
  if r.get(key):dt.date.fromisoformat(r[key])
 status=collections.Counter();levels=collections.Counter();routes=collections.Counter();hours=collections.Counter();visitors=set();errors=collections.Counter();invalid=[];invalid_count=0;selected=0;excluded=0;total=0;byte_total=0;error_count=0
 statuses=r.get('statuses');require(statuses is None or isinstance(statuses,list) and all(isinstance(n,int) and 100<=n<=599 for n in statuses),'Invalid status filter')
 for name in files:
  p=local(s.root,name,'file');raw=readbytes(p,32*1024*1024)
  if p.suffix=='.gz':
   with gzip.GzipFile(fileobj=io.BytesIO(raw)) as f:raw=f.read(32*1024*1024+1)
   require(len(raw)<=32*1024*1024,'Decompressed log too large')
  for number,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
   if not line.strip():continue
   total+=1;require(total<=200000,'Too many log lines')
   try:v=parsed(line)
   except (ValueError,TypeError,KeyError):
    invalid_count+=1
    if len(invalid)<100:invalid.append({'file':name,'line':number,'reason':'unrecognized or malformed entry'})
    continue
   bot=bool(re.search(r'bot|crawler|spider|slurp|headless',v['ua'],re.I))
   if bot and not r.get('includeBots',False):excluded+=1;continue
   if statuses is not None and v['status'] not in statuses:continue
   if r.get('pathContains') and r['pathContains'] not in v['path']:continue
   day=v['time'][:10]
   if r.get('dateFrom') and day<r['dateFrom'] or r.get('dateTo') and day>r['dateTo']:continue
   selected+=1;status[str(v['status']) if v['status'] is not None else 'none']+=1;levels[v['level'] or 'none']+=1
   if v['path']:routes[v['path'][:250]]+=1
   hours[v['time'][:13] or 'unknown']+=1
   if v['ip']:visitors.add(sha(v['ip'].encode())[:16])
   try:byte_total+=max(0,int(v['bytes']))
   except (ValueError,TypeError):pass
   if v['level'] in ('error','fatal','critical') or isinstance(v['status'],int) and v['status']>=500:
    error_count+=1;signature=re.sub(r'\b(?:\d+|[a-f0-9]{16,})\b','{value}',v['message'] or v['path']);errors[signature or 'HTTP server error']+=1
 data={'inputLines':total,'selectedLines':selected,'excludedBotLines':excluded,'botDetection':'user-agent heuristic','invalidLines':invalid_count,'invalidLineSample':invalid,'uniqueIPCount':len(visitors),'bytes':byte_total,'statusCounts':dict(status),'levelCounts':dict(levels),'hourBuckets':dict(sorted(hours.items())),'topRoutes':[{'path':k,'count':n} for k,n in routes.most_common(100)],'errors':error_count,'topErrorSignatures':[{'signature':k,'count':n} for k,n in errors.most_common(50)]}
 return s.report(data,'Log diagnostics',(['path','count'],data['topRoutes']))
