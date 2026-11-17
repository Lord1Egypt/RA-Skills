"""Portable full-strategy paper runtime + strictly virtual Simmer mirror."""
import argparse,asyncio,copy,json,os,signal,sqlite3,sys,threading,time
import httpx
from pathlib import Path
from types import SimpleNamespace
import bootstrap
from bootstrap import ROOT
from common import atomic_json,jsonable,redact
from paper_engine import PaperEngine
from simmer_paper import SimmerPaper,smoke

class State:
    def __init__(self,root):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.lock=open(self.root/'process.lock','a+b');self.lock.seek(0);self.lock.write(b'0');self.lock.flush();self.lock.seek(0)
        if os.name=='nt':
            import msvcrt
            try:msvcrt.locking(self.lock.fileno(),msvcrt.LK_NBLCK,1)
            except OSError:raise RuntimeError('paper runtime already running in this state directory')
        else:
            import fcntl
            fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.db=sqlite3.connect(self.root/'paper.sqlite')
        self.db.execute('pragma journal_mode=WAL');self.db.execute('pragma synchronous=FULL')
        self.db.execute('create table if not exists checkpoint (id integer primary key, body text)')
        self.db.execute('create table if not exists events (id text primary key, body text)')
        self.db.execute('create table if not exists mirror_outbox (id text primary key, body text, status text, error text)')
        self.db.execute("update mirror_outbox set status='UNKNOWN' where status='SENDING'")
        self.db.commit()
    def load(self):
        r=self.db.execute('select body from checkpoint where id=1').fetchone();return json.loads(r[0]) if r else None
    def save(self,engine,events):
        with self.db:
            for event in events:
                body=json.dumps(jsonable(event),ensure_ascii=False)
                self.db.execute('insert into events values (?,?)',(event['id'],body))
                if event['kind']=='FILL':self.db.execute('insert into mirror_outbox values (?,?,?,?)',(event['id'],body,'NEW',None))
            self.db.execute('insert or replace into checkpoint values (1,?)',(json.dumps(engine.checkpoint()),))
    def close(self):self.db.close();self.lock.close()

async def run(args):
    state=State(args.state_dir);stop=threading.Event();queue=asyncio.Queue(maxsize=1)
    engine=PaperEngine(json.loads((ROOT/'thresholds.json').read_text('utf8')),state.load())
    client=SimmerPaper(args.state_dir) if os.environ.get('SIMMER_API_KEY') else None
    def on_snapshot(s):
        if queue.full():queue.get_nowait()
        queue.put_nowait(s)
    from public_feed import make_feed
    cfg=SimpleNamespace(source_root=str(ROOT/'vendor'),source_sha256=json.loads((ROOT/'source-pins.json').read_text('utf8')),decision_interval_ms=100)
    feed=make_feed(cfg,Path(args.state_dir)/'feed',on_snapshot,stop)
    def halt(*unused):stop.set()
    for sig in (signal.SIGINT,signal.SIGTERM):signal.signal(sig,halt)
    start=time.monotonic();last=None;last_received=None;last_report=0;last_status=0;last_resolution=0;error=None
    mirror_task=None;status_task=None;resolution_task=None
    async def resolutions():
        proofs=[]
        async with httpx.AsyncClient(timeout=15,follow_redirects=False) as http:
            for market,e in engine.sessions.items():
                if not e.exit or e.exit.settled or not (e.exit.own or e.exit.other) or e.now_ms<e.start_ms+900000:continue
                response=await http.get('https://gamma-api.polymarket.com/markets',params={'slug':market})
                response.raise_for_status();rows=response.json()
                if not rows:continue
                row=rows[0];outcomes=row.get('outcomes');prices=row.get('outcomePrices')
                outcomes=json.loads(outcomes) if isinstance(outcomes,str) else outcomes
                prices=json.loads(prices) if isinstance(prices,str) else prices
                if row.get('slug')==market and row.get('closed') is True and row.get('umaResolutionStatus')=='resolved' and set(outcomes or [])=={'Up','Down'} and prices in (['1','0'],['0','1']):
                    proofs.append((market,outcomes[prices.index('1')],{'official':True,'source':'Gamma closed/resolved + exact outcomes + one-hot outcomePrices','condition_id':row.get('conditionId')}))
        return proofs
    task=asyncio.create_task(feed.run())
    async def mirror_one(row):
        rid,body=row
        state.db.execute("update mirror_outbox set status='SENDING' where id=?",(rid,));state.db.commit()
        try:
            await client.mirror(json.loads(body))
            state.db.execute("update mirror_outbox set status='COMPLETE' where id=?",(rid,))
        except Exception as ex:
            # Preserve the original event; no repeating a possibly accepted POST.
            state.db.execute("update mirror_outbox set status='UNKNOWN',error=? where id=?",(type(ex).__name__+': '+str(redact(str(ex)))[:250],rid))
        state.db.commit()
    try:
        while not stop.is_set() and time.monotonic()-start<args.seconds and not (Path(args.state_dir)/'STOP').exists():
            if task.done():await task;raise RuntimeError('public feed ended unexpectedly')
            try:s=await asyncio.wait_for(queue.get(),timeout=.5)
            except asyncio.TimeoutError:s=None
            if s:
                last=s;last_received=time.monotonic();events=engine.step(s);state.save(engine,events)
            elif last and time.monotonic()-last_received>2:
                stale=copy.deepcopy(last);stale['now_ms']=last['now_ms']+int((time.monotonic()-last_received)*1000)
                events=engine.step(stale,timer=True);state.save(engine,events)
            if resolution_task and resolution_task.done():
                try:
                    for market,winner,proof in await resolution_task:
                        events=engine.settle(market,winner,engine.sessions[market].now_ms,proof);state.save(engine,events)
                except httpx.HTTPError:pass
                resolution_task=None
            if resolution_task is None and time.monotonic()-last_resolution>=60:
                last_resolution=time.monotonic();resolution_task=asyncio.create_task(resolutions())
            if client:
                if mirror_task and mirror_task.done():await mirror_task;mirror_task=None
                if mirror_task is None:
                    blocked=state.db.execute("select 1 from mirror_outbox where status='UNKNOWN' limit 1").fetchone()
                    row=None if blocked else state.db.execute("select id,body from mirror_outbox where status='NEW' order by rowid limit 1").fetchone()
                    if row:mirror_task=asyncio.create_task(mirror_one(row))
                if status_task and status_task.done():
                    try:await status_task
                    except Exception as ex:client.last_error=type(ex).__name__
                    status_task=None
                if status_task is None and time.monotonic()-last_status>=60:
                    last_status=time.monotonic();status_task=asyncio.create_task(client.status())
            if time.monotonic()-last_report>=2:
                last_report=time.monotonic();status=feed.public()
                report={**engine.report(),'process_status':'RUNNING','pid':os.getpid(),'runtime_host':'local' if os.name=='nt' else 'current-host','uptime_seconds':round(time.monotonic()-start,1),'updated_ms':status['now_ms'],'feed_health':status['health'],'market':status['market'],'signal':status['paper']['signal'],'feed_counts':status['counts'],'simmer_connected':client is not None,'simmer_last_error':client.last_error if client else None,'mirror_outbox':dict(state.db.execute('select status,count(*) from mirror_outbox group by status'))}
                atomic_json(Path(args.state_dir)/'report.json',report)
        return engine.report()
    except Exception as ex:error=type(ex).__name__+': '+str(ex);raise
    finally:
        stop.set();await asyncio.gather(task,return_exceptions=True)
        for pending in (mirror_task,status_task,resolution_task):
            if pending:
                try:await asyncio.wait_for(pending,35)
                except Exception:pass
        # Local-model orders can be cancelled deterministically at shutdown.
        if last:
            end=copy.deepcopy(last);end['now_ms']=max(last['now_ms'],max((e.now_ms for e in engine.sessions.values()),default=0))+1
            events=engine.step(end,timer=True);state.save(engine,events)
        atomic_json(Path(args.state_dir)/'report.json',{**engine.report(),'process_status':'ERROR' if error else 'STOPPED','error':error,'pid':os.getpid(),'cloud_execution_verified':False})
        if client:await client.close()
        state.close()

async def main(args):
    if args.action=='smoke':return await smoke(args.state_dir)
    if args.action=='status':
        client=SimmerPaper(args.state_dir)
        try:
            r=await client.status();return {'virtual_portfolio':r['virtual_portfolio'],'real_money_orders':0,'receipt_file':str(Path(args.state_dir)/'simmer-status.json')}
        finally:await client.close()
    return await run(args)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Full K14 paper strategy. No real trading mode exists.')
    parser.add_argument('--action',choices=['run','status','smoke'],default='run')
    parser.add_argument('--seconds',type=int,default=int(os.environ.get('K14_RUN_SECONDS','1800')))
    parser.add_argument('--state-dir',default=os.environ.get('K14_STATE_DIR',str(ROOT/'state')))
    args=parser.parse_args()
    if not 10<=args.seconds<=86400:parser.error('seconds must be 10..86400')
    try:print(json.dumps(jsonable(asyncio.run(main(args))),ensure_ascii=False))
    except Exception as ex:print(json.dumps({'error':type(ex).__name__,'message':redact(str(ex))},ensure_ascii=False));sys.exit(1)
