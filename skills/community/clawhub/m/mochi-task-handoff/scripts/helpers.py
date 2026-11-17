from core import *
import math

def text(v, maximum=12000, empty=False):
 require(isinstance(v,str) and (empty or v.strip()) and len(v)<=maximum,'Invalid text field')
 require(not any(ord(c)<32 and c not in '\t\n\r' for c in v),'Control character in text')
 return v

def objects(r,key,maximum=1000):
 v=r.get(key);require(isinstance(v,list) and len(v)<=maximum and all(isinstance(x,dict) for x in v),'Expected a bounded list of objects: '+key);return v

def strings(v,maximum=100):
 require(isinstance(v,list) and len(v)<=maximum,'Expected a bounded list of strings');return [text(x) for x in v]

def public_url(v):
 text(v,4096);p=urlsplit(v);require(p.scheme=='https' and p.hostname and not p.username and not p.password,'Expected public HTTPS URL')
 require(p.hostname not in ('localhost','localhost.localdomain') and not p.hostname.endswith('.local'),'Private URL not supported')
 try: addr=ipaddress.ip_address(p.hostname)
 except ValueError: return v
 require(addr.is_global,'Private or reserved IP not supported');return v

def rows_file(s,r):
 v=readjson(local(s.root,r['file'],'file'));require(isinstance(v,list) and len(v)<=10000 and all(isinstance(x,dict) for x in v),'Expected JSON array of objects');return v

def date(v):
 text(v,50);d=dt.datetime.fromisoformat(v.replace('Z','+00:00'));require(d.tzinfo is not None,'Timestamp requires timezone');return d

def file_report(s,data,filename,content):
 result=s.report(data);directory=local(s.root,result['directory'],'dir');write_new(directory/filename,content)
 result['files'].append(s.rel(directory/filename));return result
