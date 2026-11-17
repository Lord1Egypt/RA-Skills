from core import *

def date(value):
 if value:dt.date.fromisoformat(value)
 return value or ''
def cycle(tasks):
 visiting=set();done=set()
 def visit(key):
  require(key not in visiting,'Dependency cycle detected')
  if key in done:return
  visiting.add(key)
  for d in tasks[key].get('dependencies',[]):require(d in tasks,'Dependency task not found');visit(d)
  visiting.remove(key);done.add(key)
 for key in tasks:visit(key)
def handle(s,r):
 a=r.get('action')
 if a=='project.upsert':
  key=ident(r['id']);require(isinstance(r.get('name'),str) and r['name'].strip(),'Project name required')
  value={'id':key,'name':r['name'].strip(),'due':date(r.get('due')),'updatedAt':now()};return s.put('project',key,value)
 if a=='task.upsert':
  key=ident(r['id']);old=s.get('task',key,{})
  v={**old,**{k:r[k] for k in ('project','title','status','owner','due','dependencies','estimateHours','milestone') if k in r},'id':key}
  require(s.get('project',v.get('project','')) is not None,'Project not found');require(isinstance(v.get('title'),str) and v['title'].strip(),'Task title required')
  v.setdefault('status','todo');require(v['status'] in ('todo','doing','done','cancelled'),'Unknown status');v['due']=date(v.get('due'));v.setdefault('owner','');v.setdefault('dependencies',[])
  require(isinstance(v['dependencies'],list) and len(v['dependencies'])<=100,'Invalid dependency list');v['dependencies']=[ident(x) for x in v['dependencies']]
  hours=v.setdefault('estimateHours',0);require(isinstance(hours,(int,float)) and not isinstance(hours,bool) and 0<=hours<=10000,'Invalid estimate')
  tasks={t['id']:t for t in s.all('task') if t['project']==v['project']};tasks[key]=v;cycle(tasks)
  for task in tasks.values():
   if task['status']=='done':require(all(tasks[d]['status']=='done' for d in task['dependencies']),'Completed tasks must retain completed dependencies; reopen dependent tasks first')
  for other in s.all('task'):
   if key in other.get('dependencies',[]):require(other['project']==v['project'],'Moving a depended-on task across projects is not allowed')
  v['updatedAt']=now();return s.put('task',key,v)
 if a=='task.remove':
  key=ident(r['id']);require(s.get('task',key) is not None,'Task not found');require(not any(key in t.get('dependencies',[]) for t in s.all('task')),'Other tasks depend on this task');s.delete('task',key);return {'removed':key}
 if a in ('list','report'):
  tasks=s.all('task');projects=s.all('project')
  if r.get('project'):tasks=[t for t in tasks if t['project']==r['project']];projects=[p for p in projects if p['id']==r['project']]
  today=date(r.get('today')) or dt.date.today().isoformat();alltasks={t['id']:t for t in s.all('task')};work={}
  for t in tasks:
   t['blockedBy']=[d for d in t['dependencies'] if alltasks.get(d,{}).get('status')!='done'];t['overdue']=bool(t['due'] and t['due']<today and t['status'] not in ('done','cancelled'))
   if t['status'] not in ('done','cancelled'):work[t['owner']]=work.get(t['owner'],0)+t['estimateHours']
  data={'projects':projects,'tasks':tasks,'remainingHoursByOwner':work,'counts':{k:sum(t['status']==k for t in tasks) for k in ('todo','doing','done','cancelled')}}
  if a=='list':return data
  result=s.report(data,'Project board',(['id','project','title','status','owner','due','estimateHours','overdue'],tasks));out=local(s.root,result['directory'])
  def esc(x):return str(x).replace('\\','\\\\').replace(';','\\;').replace(',','\\,').replace('\r','').replace('\n','\\n')
  lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//MochiLab//Project Board//EN']
  for t in tasks:
   if t['due'] and t['status'] not in ('done','cancelled'):
    day=t['due'].replace('-','');end=(dt.date.fromisoformat(t['due'])+dt.timedelta(days=1)).strftime('%Y%m%d');lines+=['BEGIN:VEVENT','UID:'+t['id']+'-'+t['project']+'@mochilab.bz','DTSTAMP:'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'DTSTART;VALUE=DATE:'+day,'DTEND;VALUE=DATE:'+end,'SUMMARY:'+esc(t['title']),'END:VEVENT']
  lines+=['END:VCALENDAR'];write_new(out/'deadlines.ics',icalbytes(lines));result['files'].append(s.rel(out/'deadlines.ics'));return result
 raise ValueError('Actions: project.upsert, task.upsert, task.remove, list, report')
