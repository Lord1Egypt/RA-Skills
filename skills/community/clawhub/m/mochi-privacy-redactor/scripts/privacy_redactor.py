from core import *
PATTERNS={
 'email':re.compile(r'(?i)(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])'),
 'phone':re.compile(r'(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)'),
 'identity':re.compile(r'(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx](?!\w)'),
 'ipv4':re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])'),
 'token':re.compile(r'(?i)\b(?:sk-[A-Za-z0-9_-]{16,}|mlk_[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|Bearer\s+[A-Za-z0-9._~+/-]{16,}=*)')}
SENSITIVE=re.compile(r'(?i)^(?:password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|authorization|client[_-]?secret|private[_-]?key)$')
def handle(s,r):
 a=r.get('action');require(a in ('scan','redact'),'Actions: scan, redact');files=r.get('files');require(isinstance(files,list) and 1<=len(files)<=100,'Provide 1..100 files')
 kinds=r.get('patterns',list(PATTERNS));require(isinstance(kinds,list) and all(k in PATTERNS for k in kinds),'Unknown pattern category')
 rules=r.get('literals',[]);require(isinstance(rules,list) and len(rules)<=50 and all(isinstance(x,str) and 2<=len(x)<=1000 for x in rules),'Literal rules must contain 2..1000 characters')
 out=s.exports() if a=='redact' else None;results=[]
 def process(text,counts):
  for kind in kinds:
   def replace(m):
    if kind=='ipv4':
     try:ipaddress.ip_address(m[0])
     except ValueError:return m[0]
    counts[kind]=counts.get(kind,0)+1;return '['+kind.upper()+']'
   text=PATTERNS[kind].sub(replace,text)
  # Config-style secret fields in text files, without including values in reports.
  text,n=re.subn(r'(?im)(\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*[:=]\s*)(?:"[^"\r\n]*"|\S+)',r'\1[SECRET]',text);counts['secretField']=counts.get('secretField',0)+n
  for literal in sorted(rules,key=len,reverse=True):
   n=text.count(literal);text=text.replace(literal,'[CUSTOM]');counts['custom']=counts.get('custom',0)+n
  return text
 def recursive(v,counts,depth=0):
  require(depth<=50,'JSON nesting too deep')
  if isinstance(v,dict):
   out={}
   for k,x in v.items():
    if SENSITIVE.fullmatch(k):counts['secretField']=counts.get('secretField',0)+1;out[k]='[SECRET]'
    else:out[k]=recursive(x,counts,depth+1)
   return out
  if isinstance(v,list):return [recursive(x,counts,depth+1) for x in v]
  return process(v,counts) if isinstance(v,str) else v
 for index,name in enumerate(files):
  p=local(s.root,name,'file');require(p.suffix.lower() in ('.txt','.md','.csv','.json','.log','.html'),'Supported: text, Markdown, CSV, JSON, log, HTML');raw=readbytes(p,8*1024*1024);text=raw.decode('utf-8-sig');counts={}
  if p.suffix.lower()=='.json':value=recursive(json.loads(text),counts);result=jsonbytes(value)
  elif p.suffix.lower()=='.csv':
   fields,rows=csv_rows(p);newfields=[process(k,counts) for k in fields];require(len(newfields)==len(set(newfields)),'Redaction would create duplicate CSV headers')
   result=csvbytes(newfields,[dict(zip(newfields,[process(row[k],counts) for k in fields])) for row in rows])
  else:result=process(text,counts).encode('utf-8')
  item={'source':name,'sourceSha256':sha(raw),'matches':{k:v for k,v in counts.items() if v},'output':None}
  if out:
   dest=out/(str(index+1).zfill(3)+'-'+p.name);write_new(dest,result);item['output']=s.rel(dest);item['outputSha256']=sha(result)
  results.append(item)
 data={'mode':a,'files':results,'originalsModified':False,'detection':'configured pattern and field matching; review selected output before sharing'}
 if out:
  newjson(out/'report.json',data);write_new(out/'report.html',htmlreport('Privacy redaction report',data));return {'report':data,'directory':s.rel(out)}
 return s.report(data,'Privacy scan report')
