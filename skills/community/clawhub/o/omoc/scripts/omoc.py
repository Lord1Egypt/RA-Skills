#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,re,uuid
from datetime import datetime,timezone,timedelta
from pathlib import Path
from typing import Any
SAFE=re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$'); STATUSES={'pending','blocked','in_progress','completed','failed'}; TERMINAL={'completed','failed'}
def now(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def pt(v):
    if not v: return None
    try: return datetime.fromisoformat(v.replace('Z','+00:00'))
    except Exception: return None
def root(): return Path(os.environ.get('OMOC_ROOT','.omoc'))
def ensure(p): p.mkdir(parents=True,exist_ok=True)
def rj(p,d=None):
    p=Path(p)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else d
def wj(p,o):
    p=Path(p); ensure(p.parent); t=p.with_suffix(p.suffix+f'.{os.getpid()}.{uuid.uuid4().hex}.tmp'); t.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); t.replace(p)
def aj(p,o): ensure(Path(p).parent); open(p,'a',encoding='utf-8').write(json.dumps(o,ensure_ascii=False)+'\n')
def safe(v,l):
    if not SAFE.match(v): raise SystemExit(f'invalid {l}: {v}')
def slug(s,fb='omoc'):
    x=re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:30]
    return x if x and SAFE.match(x) else fb
def td(team): safe(team,'team'); return root()/'teams'/team
def tp(team,tid):
    if not re.match(r'^\d{1,20}$',str(tid)): raise SystemExit(f'invalid task id: {tid}')
    return td(team)/'tasks'/f'{tid}.json'
def cfg(team):
    c=rj(td(team)/'config.json')
    if not c: raise SystemExit(f'team not found: {team}')
    return c
def task(team,tid):
    t=rj(tp(team,tid))
    if not t: raise SystemExit(f'task not found: {tid}')
    return t
def ev(team,typ,**kw): aj(td(team)/'events.jsonl',{'event_id':uuid.uuid4().hex,'type':typ,'team':team,'created_at':now(),**kw})
def create_task(team,subject,description='',role=None,owner=None,depends_on='',coordination='lightweight',verifier_required=False):
    c=cfg(team); tid=str(c.get('next_task_id',1)); c['next_task_id']=int(tid)+1
    t={'id':tid,'subject':subject,'description':description or '','status':'pending','role':role,'owner':owner,'depends_on':[x for x in (depends_on or '').split(',') if x],'version':1,'created_at':now(),'coordination':{'mode':coordination},'verifier_required':bool(verifier_required)}
    wj(tp(team,tid),t); wj(td(team)/'config.json',c); ev(team,'task_created',worker='leader',task_id=tid,reason=subject); return t
def tasks(team):
    p=td(team)/'tasks'; return [rj(x) for x in sorted(p.glob('*.json'),key=lambda q:int(q.stem))] if p.exists() else []
def summary(team):
    c=cfg(team); ts=tasks(team); counts={s:sum(1 for t in ts if t.get('status')==s) for s in STATUSES}; ver=any((t.get('role')=='verifier' or t.get('verifier_required')) and t.get('status')=='completed' for t in ts); term=counts['pending']==counts['in_progress']==counts['blocked']==0
    s={'team':team,'task':c.get('task'),'goal_id':c.get('goal_id'),'counts':counts,'terminal':term,'verifier_done':ver,'tasks':ts,'loop':c.get('loop',{})}; wj(td(team)/'summary.json',s); return s

def cmd_compose_init(a):
    o={'schema':'omoc.workflow.v1','objective':a.objective,'modes':[x.strip() for x in a.modes.split(',') if x.strip()],'status':'active','created_at':now(),'active':{'goal_id':None,'team':None,'ralph_loop':None},'memory_policy':{'compact_after_events':50,'max_worker_context_chars':12000}}
    wj(root()/'workflow.json',o); print(json.dumps(o,indent=2))
def events(n=None):
    p=root()/'memory'/'events.jsonl'
    if not p.exists(): return []
    lines=p.read_text(encoding='utf-8').splitlines(); lines=lines[-n:] if n else lines; out=[]
    for line in lines:
        try: out.append(json.loads(line))
        except Exception: pass
    return out
def cmd_memory_add(a):
    rec={'event_id':uuid.uuid4().hex,'kind':a.kind,'text':a.text,'source':a.source,'created_at':now()}; aj(root()/'memory'/'events.jsonl',rec); print(json.dumps({'ok':True,'event':rec},indent=2))
def cmd_memory_compact(a):
    es=events(a.max_events); ensure(root()/'memory'/'summaries'); sp=root()/'memory'/'summaries'/f"summary-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.md"; lines=['# OMOC Memory Summary','',f'Created: {now()}',f'Events summarized: {len(es)}','']
    for e in es[-a.max_events:]: lines.append(f"- [{e.get('kind','note')}] {e.get('text','')[:500]}")
    sp.write_text('\n'.join(lines),encoding='utf-8'); idx={'latest_summary':str(sp),'event_count':len(events()),'compacted_at':now(),'max_events':a.max_events}; wj(root()/'memory'/'index.json',idx); print(json.dumps({'ok':True,'summary':str(sp),'index':idx},indent=2))
def cmd_memory_status(a): print(json.dumps({'index':rj(root()/'memory'/'index.json',{}),'recent_events':events(10)},indent=2))
def cmd_team_init(a):
    name=a.name or slug(a.task,'team'); safe(name,'team'); ws=[w.strip() for w in (a.workers or 'worker-1,verifier').split(',') if w.strip()]; wob=[]
    for i,w in enumerate(ws,1):
        wn=w if SAFE.match(w) else f'worker-{i}'; wob.append({'name':wn,'index':i,'role':'verifier' if 'verif' in wn else 'worker','assigned_tasks':[],'state':'idle'})
    c={'schema':'omoc.team.v1','name':name,'task':a.task,'goal_id':a.goal_id,'worker_count':len(wob),'workers':wob,'next_task_id':1,'created_at':now(),'status':'running','leader':a.leader or 'leader','loop':{'status':'idle','lease':{}}}
    ensure(td(name)/'tasks'); ensure(td(name)/'mailbox'); wj(td(name)/'config.json',c)
    for w in wob: wj(td(name)/'mailbox'/f"{w['name']}.json",{'worker':w['name'],'messages':[]})
    ev(name,'team_initialized',worker='leader',reason=a.task); print(json.dumps({'ok':True,'team':name,'workers':wob},indent=2))
def cmd_team_add_task(a): print(json.dumps({'ok':True,'task':create_task(a.team,a.subject,a.description,a.role,a.owner,a.depends_on,a.coordination,a.verifier_required)},indent=2))
def deps_ready(team,t):
    miss=[]
    for d in t.get('depends_on') or []:
        dt=rj(tp(team,d))
        if not dt or dt.get('status')!='completed': miss.append(d)
    return not miss,miss
def cmd_team_claim(a):
    c=cfg(a.team)
    if a.worker not in [w['name'] for w in c.get('workers',[])]: raise SystemExit(f'worker_not_found: {a.worker}')
    t=task(a.team,a.task_id); ok,miss=deps_ready(a.team,t)
    if not ok: print(json.dumps({'ok':False,'error':'blocked_dependency','dependencies':miss},indent=2)); return
    if t.get('status') in TERMINAL: print(json.dumps({'ok':False,'error':'already_terminal'},indent=2)); return
    claim=t.get('claim') or {}; exp=pt(claim.get('leased_until'))
    if t.get('status')=='in_progress' and exp and exp>datetime.now(timezone.utc): print(json.dumps({'ok':False,'error':'claim_conflict','lease':claim},indent=2)); return
    token=uuid.uuid4().hex; until=(datetime.now(timezone.utc)+timedelta(seconds=a.ttl_seconds)).isoformat().replace('+00:00','Z'); t.update({'status':'in_progress','owner':a.worker,'version':int(t.get('version',1))+1,'claim':{'owner':a.worker,'token':token,'leased_until':until}}); wj(tp(a.team,a.task_id),t); ev(a.team,'task_claimed',worker=a.worker,task_id=a.task_id); print(json.dumps({'ok':True,'task':t,'claimToken':token},indent=2))
def finish(a,status):
    t=task(a.team,a.task_id); cl=t.get('claim') or {}
    if cl.get('token')!=a.claim_token: print(json.dumps({'ok':False,'error':'claim_conflict'},indent=2)); return
    exp=pt(cl.get('leased_until'))
    if exp and exp<=datetime.now(timezone.utc): print(json.dumps({'ok':False,'error':'lease_expired'},indent=2)); return
    t.update({'status':status,'completed_at':now(),'version':int(t.get('version',1))+1}); t.pop('claim',None)
    if status=='completed': t['result']=a.result or ''
    else: t['error']=a.error or a.result or 'failed'
    wj(tp(a.team,a.task_id),t); ev(a.team,'task_completed' if status=='completed' else 'task_failed',worker=t.get('owner','unknown'),task_id=a.task_id,reason=t.get('result') or t.get('error')); print(json.dumps({'ok':True,'task':t},indent=2))
def cmd_team_status(a): print(json.dumps(summary(a.team),indent=2))
def cmd_team_gate(a):
    s=summary(a.team); c=s['counts']
    if c['failed']>0: g={'decision':'blocked','reason':'failed_tasks_present'}
    elif c['in_progress']>0: g={'decision':'wait','reason':'workers_active'}
    elif c['pending']>0 or c['blocked']>0: g={'decision':'continue','reason':'work_remaining'}
    elif not s['verifier_done']: g={'decision':'needs_verifier','reason':'terminal_without_verifier_evidence'}
    else: g={'decision':'checkpoint_goal','reason':'team_terminal_and_verified','goal_id':a.goal_id or s.get('goal_id')}
    ev(a.team,'team_gate',worker='leader',reason=g['decision']); print(json.dumps({'ok':True,'summary':s,'gate':g},indent=2))
def cmd_team_loop(a):
    c=cfg(a.team); loop=c.setdefault('loop',{'status':'idle','lease':{}}); lease=loop.get('lease') or {}; exp=pt(lease.get('expires_at'))
    if loop.get('status')=='running' and exp and exp>datetime.now(timezone.utc): print(json.dumps({'ok':False,'error':'already_running','lease':lease},indent=2)); return
    owner=a.owner or uuid.uuid4().hex; loop['status']='running'; loop['lease']={'owner':owner,'acquired_at':now(),'expires_at':(datetime.now(timezone.utc)+timedelta(seconds=a.ttl_seconds)).isoformat().replace('+00:00','Z'),'heartbeat_at':now()}; wj(td(a.team)/'config.json',c)
    s=summary(a.team); cts=s['counts']; created=None
    if cts['pending']==0 and cts['in_progress']==0 and cts['blocked']==0 and not s['verifier_done']:
        created=create_task(a.team,'Verifier gate',f"Verify team {a.team} against goal {a.goal_id or s.get('goal_id')}",'verifier',None,','.join(t['id'] for t in s['tasks'] if t.get('status')=='completed'),'coordinated',True)
    s2=summary(a.team); c=cfg(a.team); c['loop']={'status':'idle','lease':{},'last_loop_at':now()}; wj(td(a.team)/'config.json',c); ev(a.team,'team_loop',worker='leader',reason='advanced'); print(json.dumps({'ok':True,'owner':owner,'created_task':created,'summary':s2,'next':'run team gate; schedule next loop if not checkpointable'},indent=2))
def cmd_team_send(a):
    cfg(a.team); p=td(a.team)/'mailbox'/f'{a.to}.json'; mb=rj(p,{'worker':a.to,'messages':[]}); msg={'message_id':uuid.uuid4().hex,'from_worker':a.from_worker,'to_worker':a.to,'body':a.body,'created_at':now()}; mb.setdefault('messages',[]).append(msg); wj(p,mb); ev(a.team,'message_received',worker=a.to,message_id=msg['message_id'],reason=a.body[:200]); print(json.dumps({'ok':True,'message':msg},indent=2))
def cmd_team_mailbox(a): print(json.dumps(rj(td(a.team)/'mailbox'/f'{a.worker}.json',{'worker':a.worker,'messages':[]}),indent=2))
def gp(): return root()/'goals'/'goals.json'
def lp(): return root()/'goals'/'ledger.jsonl'
def goals():
    s=rj(gp())
    if not s: raise SystemExit('goals not initialized')
    return s
def cmd_goal_init(a):
    ensure(root()/'goals'); brief=a.brief or Path(a.brief_file).read_text(encoding='utf-8'); (root()/'goals'/'brief.md').write_text(brief,encoding='utf-8'); lines=[x.strip() for x in brief.splitlines() if x.strip()] or [brief]
    gs=[{'id':f'G{i:03d}','title':line[:80],'objective':line,'status':'pending','created_at':now(),'evidence':[]} for i,line in enumerate(lines[:20],1)]; st={'schema':'omoc.goals.v1','aggregate_status':'active','activeGoalId':gs[0]['id'],'created_at':now(),'goals':gs,'final_gate':None}; wj(gp(),st); aj(lp(),{'event':'goals_initialized','created_at':now(),'goal_count':len(gs)}); print(json.dumps(st,indent=2))
def cmd_goal_next(a):
    s=goals(); nxt=next((g for g in s['goals'] if g.get('status') in {'pending','failed','blocked'}),None)
    if nxt: s['activeGoalId']=nxt['id']; wj(gp(),s)
    print(json.dumps({'ok':True,'next':nxt},indent=2))
def cmd_goal_checkpoint(a):
    s=goals(); g=next((x for x in s['goals'] if x['id']==a.goal_id),None)
    if not g: raise SystemExit(f'goal not found: {a.goal_id}')
    g['status']=a.status; g.setdefault('evidence',[]).append({'at':now(),'evidence':a.evidence})
    if a.status=='complete': g['completed_at']=now()
    if all(x.get('status')=='complete' for x in s['goals']): s['aggregate_status']='ready_for_final_gate'
    wj(gp(),s); aj(lp(),{'event':'checkpoint','goal_id':a.goal_id,'status':a.status,'evidence':a.evidence,'created_at':now()}); print(json.dumps({'ok':True,'goal':g,'aggregate_status':s['aggregate_status']},indent=2))
def cmd_goal_status(a): print(json.dumps(goals(),indent=2))
def rd(loop): safe(loop,'loop_id'); return root()/'ralph'/loop
def rs(loop):
    s=rj(rd(loop)/'state.json')
    if not s: raise SystemExit(f'ralph loop not found: {loop}')
    return s
def wr(loop,s): wj(rd(loop)/'state.json',s)
def cmd_ralph_init(a):
    s={'schema':'omoc.ralph.v1','loop_id':a.loop_id,'objective':a.objective,'status':'idle','iteration':0,'max_iterations':a.max_iterations,'lease':{'owner':None,'acquired_at':None,'expires_at':None,'heartbeat_at':None},'evidence':[],'risks':[],'completion_audit':None,'created_at':now()}; wr(a.loop_id,s); print(json.dumps(s,indent=2))
def cmd_ralph_acquire(a):
    s=rs(a.loop_id); le=s.get('lease') or {}; exp=pt(le.get('expires_at'))
    if s.get('status')=='running' and exp and exp>datetime.now(timezone.utc): print(json.dumps({'ok':False,'error':'already_running','lease':le},indent=2)); return
    stale=s.get('status')=='running'; s['status']='running'; s['iteration']=int(s.get('iteration',0))+1; s['lease']={'owner':a.owner,'acquired_at':now(),'expires_at':(datetime.now(timezone.utc)+timedelta(seconds=a.ttl_seconds)).isoformat().replace('+00:00','Z'),'heartbeat_at':now(),'stale_recovery':stale}; wr(a.loop_id,s); print(json.dumps({'ok':True,'state':s},indent=2))
def cmd_ralph_heartbeat(a):
    s=rs(a.loop_id)
    if (s.get('lease') or {}).get('owner')!=a.owner: print(json.dumps({'ok':False,'error':'lease_owner_mismatch'},indent=2)); return
    s['lease']['heartbeat_at']=now(); wr(a.loop_id,s); print(json.dumps({'ok':True,'lease':s['lease']},indent=2))
def cmd_ralph_release(a):
    s=rs(a.loop_id)
    if (s.get('lease') or {}).get('owner')!=a.owner: print(json.dumps({'ok':False,'error':'lease_owner_mismatch'},indent=2)); return
    s['status']=a.status
    if a.evidence: s.setdefault('evidence',[]).append({'at':now(),'evidence':a.evidence})
    s['lease']={'owner':None,'acquired_at':None,'expires_at':None,'heartbeat_at':None}; wr(a.loop_id,s); print(json.dumps({'ok':True,'state':s},indent=2))
def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='area',required=True)
    comp=sub.add_parser('compose'); cs=comp.add_subparsers(dest='cmd',required=True); a=cs.add_parser('init'); a.add_argument('--objective',required=True); a.add_argument('--modes',default='goal,ralplan,team,ralph'); a.set_defaults(func=cmd_compose_init)
    mem=sub.add_parser('memory'); ms=mem.add_subparsers(dest='cmd',required=True); a=ms.add_parser('add'); a.add_argument('--kind',default='note'); a.add_argument('--text',required=True); a.add_argument('--source',default='leader'); a.set_defaults(func=cmd_memory_add); a=ms.add_parser('compact'); a.add_argument('--max-events',type=int,default=50); a.set_defaults(func=cmd_memory_compact); a=ms.add_parser('status'); a.set_defaults(func=cmd_memory_status)
    team=sub.add_parser('team'); ts=team.add_subparsers(dest='cmd',required=True)
    a=ts.add_parser('init'); a.add_argument('--name'); a.add_argument('--task',required=True); a.add_argument('--workers'); a.add_argument('--leader'); a.add_argument('--goal-id'); a.set_defaults(func=cmd_team_init)
    a=ts.add_parser('add-task'); a.add_argument('--team',required=True); a.add_argument('--subject',required=True); a.add_argument('--description'); a.add_argument('--role'); a.add_argument('--owner'); a.add_argument('--depends-on'); a.add_argument('--coordination',choices=['lightweight','coordinated'],default='lightweight'); a.add_argument('--verifier-required',action='store_true'); a.set_defaults(func=cmd_team_add_task)
    a=ts.add_parser('claim'); a.add_argument('--team',required=True); a.add_argument('--task-id',required=True); a.add_argument('--worker',required=True); a.add_argument('--ttl-seconds',type=int,default=900); a.set_defaults(func=cmd_team_claim)
    a=ts.add_parser('complete'); a.add_argument('--team',required=True); a.add_argument('--task-id',required=True); a.add_argument('--claim-token',required=True); a.add_argument('--result'); a.set_defaults(func=lambda x: finish(x,'completed'))
    a=ts.add_parser('fail'); a.add_argument('--team',required=True); a.add_argument('--task-id',required=True); a.add_argument('--claim-token',required=True); a.add_argument('--error'); a.add_argument('--result'); a.set_defaults(func=lambda x: finish(x,'failed'))
    a=ts.add_parser('status'); a.add_argument('--team',required=True); a.set_defaults(func=cmd_team_status)
    a=ts.add_parser('gate'); a.add_argument('--team',required=True); a.add_argument('--goal-id'); a.set_defaults(func=cmd_team_gate)
    a=ts.add_parser('loop'); a.add_argument('--team',required=True); a.add_argument('--goal-id'); a.add_argument('--owner'); a.add_argument('--ttl-seconds',type=int,default=900); a.set_defaults(func=cmd_team_loop)
    a=ts.add_parser('send'); a.add_argument('--team',required=True); a.add_argument('--from',dest='from_worker',required=True); a.add_argument('--to',required=True); a.add_argument('--body',required=True); a.set_defaults(func=cmd_team_send)
    a=ts.add_parser('mailbox'); a.add_argument('--team',required=True); a.add_argument('--worker',required=True); a.set_defaults(func=cmd_team_mailbox)
    goal=sub.add_parser('goal'); gs=goal.add_subparsers(dest='cmd',required=True); a=gs.add_parser('init'); a.add_argument('--brief'); a.add_argument('--brief-file'); a.set_defaults(func=cmd_goal_init); a=gs.add_parser('next'); a.set_defaults(func=cmd_goal_next); a=gs.add_parser('checkpoint'); a.add_argument('--goal-id',required=True); a.add_argument('--status',choices=['complete','failed','blocked'],required=True); a.add_argument('--evidence',required=True); a.set_defaults(func=cmd_goal_checkpoint); a=gs.add_parser('status'); a.set_defaults(func=cmd_goal_status)
    r=sub.add_parser('ralph'); rsb=r.add_subparsers(dest='cmd',required=True); a=rsb.add_parser('init'); a.add_argument('--loop-id',required=True); a.add_argument('--objective',required=True); a.add_argument('--max-iterations',type=int,default=10); a.set_defaults(func=cmd_ralph_init); a=rsb.add_parser('acquire'); a.add_argument('--loop-id',required=True); a.add_argument('--owner',required=True); a.add_argument('--ttl-seconds',type=int,default=900); a.set_defaults(func=cmd_ralph_acquire); a=rsb.add_parser('heartbeat'); a.add_argument('--loop-id',required=True); a.add_argument('--owner',required=True); a.set_defaults(func=cmd_ralph_heartbeat); a=rsb.add_parser('release'); a.add_argument('--loop-id',required=True); a.add_argument('--owner',required=True); a.add_argument('--status',choices=['idle','blocked','complete','failed'],default='idle'); a.add_argument('--evidence'); a.set_defaults(func=cmd_ralph_release)
    args=p.parse_args(); args.func(args)
if __name__=='__main__': main()
