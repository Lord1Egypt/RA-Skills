import difflib
from core import *

def inventory(s,directory):
 base=local(s.root,directory,'dir');rows=[];total=0
 for p in walkfiles(s.root,directory,5000):
  raw=readbytes(p,64*1024*1024);total+=len(raw);require(total<=256*1024*1024,'Directory exceeds 256 MiB');rows.append({'path':p.relative_to(base).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
 return {'directory':directory,'files':rows,'totalBytes':total}
def changes(left,right):
 l={x['path']:x for x in left};r={x['path']:x for x in right};return {'added':sorted(r.keys()-l.keys()),'removed':sorted(l.keys()-r.keys()),'changed':sorted(k for k in l.keys()&r.keys() if l[k]['sha256']!=r[k]['sha256']),'unchanged':sum(l[k]['sha256']==r[k]['sha256'] for k in l.keys()&r.keys())}
def jsondiff(a,b,path='',out=None):
 out=[] if out is None else out
 if len(out)>=1000:return out
 if type(a)!=type(b):out.append({'path':path or '/','kind':'type','left':a,'right':b})
 elif isinstance(a,dict):
  for key in sorted(a.keys()|b.keys()):
   p=path+'/'+str(key).replace('~','~0').replace('/','~1')
   if key not in a:out.append({'path':p,'kind':'added','right':b[key]})
   elif key not in b:out.append({'path':p,'kind':'removed','left':a[key]})
   else:jsondiff(a[key],b[key],p,out)
   if len(out)>=1000:break
 elif isinstance(a,list):
  for n in range(max(len(a),len(b))):
   p=path+'/'+str(n)
   if n>=len(a):out.append({'path':p,'kind':'added','right':b[n]})
   elif n>=len(b):out.append({'path':p,'kind':'removed','left':a[n]})
   else:jsondiff(a[n],b[n],p,out)
   if len(out)>=1000:break
 elif a!=b:out.append({'path':path or '/','kind':'value','left':a,'right':b})
 return out
def handle(s,r):
 a=r.get('action')
 if a=='manifest':return s.report(inventory(s,r['directory']),'Delivery file manifest')
 if a=='verify':
  baseline=readjson(local(s.root,r['manifest'],'file'));baseline=baseline.get('report',baseline);require(isinstance(baseline.get('files'),list),'Manifest requires files');current=inventory(s,r['directory']);delta=changes(baseline['files'],current['files']);return s.report({'verified':not any(delta[k] for k in ('added','removed','changed')),'differences':delta},'Delivery verification')
 if a=='directories':
  l=inventory(s,r['left']);rr=inventory(s,r['right']);return s.report({'left':r['left'],'right':r['right'],**changes(l['files'],rr['files'])},'Directory comparison')
 if a=='text':
  left=textfile(s.root,r['left'],4*1024*1024);right=textfile(s.root,r['right'],4*1024*1024);l=left.splitlines();rr=right.splitlines();require(len(l)<=10000 and len(rr)<=10000,'Text comparison supports at most 10000 lines per file')
  if r.get('ignoreWhitespace'):l=[' '.join(x.split()) for x in l];rr=[' '.join(x.split()) for x in rr]
  diff='\n'.join(difflib.unified_diff(l,rr,fromfile=r['left'],tofile=r['right'],n=3,lineterm=''));require(len(diff)<=2*1024*1024,'Diff output too large')
  result=s.report({'equal':l==rr,'left':r['left'],'right':r['right'],'leftLines':len(l),'rightLines':len(rr),'unifiedDiff':diff,'ignoreWhitespace':bool(r.get('ignoreWhitespace'))},'Text comparison');p=local(s.root,result['directory'])/'changes.diff';write_new(p,diff.encode());result['files'].append(s.rel(p));return result
 if a=='json':
  left=readjson(local(s.root,r['left'],'file'));right=readjson(local(s.root,r['right'],'file'));d=jsondiff(left,right);return s.report({'equal':left==right,'differences':d,'limitedAt':1000 if len(d)>=1000 else None},'JSON structural comparison')
 if a=='csv':
  lf,left=csv_rows(local(s.root,r['left'],'file'));rf,right=csv_rows(local(s.root,r['right'],'file'));keys=r.get('keys');require(isinstance(keys,list) and keys and all(k in lf and k in rf for k in keys),'Provide matching key columns')
  def indexed(rows):
   values={};duplicates=[]
   for row in rows:
    key=tuple(row[k] for k in keys)
    if key in values:duplicates.append(list(key))
    else:values[key]=row
   return values,duplicates
  l,ld=indexed(left);rr,rd=indexed(right);blocked={tuple(x) for x in ld+rd};changed=[]
  for key in sorted(l.keys()&rr.keys()-blocked):
   if l[key]!=rr[key]:changed.append({'key':list(key),'fields':{k:{'left':l[key].get(k),'right':rr[key].get(k)} for k in sorted(set(lf+rf)) if l[key].get(k)!=rr[key].get(k)}})
  return s.report({'keyColumns':keys,'leftHeaders':lf,'rightHeaders':rf,'leftDuplicateKeys':ld,'rightDuplicateKeys':rd,'addedKeys':[list(k) for k in sorted(rr.keys()-l.keys())],'removedKeys':[list(k) for k in sorted(l.keys()-rr.keys())],'changedRows':changed[:1000],'changedRowCount':len(changed),'equal':lf==rf and not ld and not rd and l==rr},'CSV keyed comparison')
 raise ValueError('Actions: text, json, csv, directories, manifest, verify')
