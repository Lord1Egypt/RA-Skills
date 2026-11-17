"""Official public feeds + frozen shadow decisions, in an isolated process.

Every outbound request is GET or a public WebSocket subscription/heartbeat.
No credentials, signing, order SDK, private stream, or live-order endpoint.
"""
import asyncio
from collections import deque, Counter
import contextlib
import hashlib
import json
import math
try:
    import msvcrt
except ImportError:
    msvcrt = None  # Paper runtime supplies its own portable process lock.
import os
from pathlib import Path
import queue
import time
import uuid
import orjson
import psutil
import websockets
from pm_predict.market_data.public_models import normalize_market, website_reference, PublicBook
from pm_predict.market_data.candles import TradeBars
from pm_predict.market_data.reference_clock import ReferenceClock
from pm_predict.strategy.indicators import Volatility
from pm_predict.runtime.live_archive import LiveArchive
from pm_predict.runtime.live_shadow import LiveShadow
from pm_predict.runtime.paper_session import load_session
from pm_predict.runtime.public_http import PublicHTTP
from pm_predict.runtime.live_health import input_health
from pm_predict.runtime.capture_policy import validate_plan, deadline_reached
from pm_predict.runtime.worker import percentiles


def wall_ms():return time.time_ns()//1_000_000


class LiveCollector:
    def __init__(self,root,output,stop):
        self.root=Path(root);self.output=output;self.stop=stop
        self.plan=json.loads((self.root/'config/live_capture.json').read_text('utf8'))
        validate_plan(self.plan)
        self.run_id=uuid.uuid4().hex;self.started=time.monotonic();self.start_ms=wall_ms()
        self.archive=LiveArchive(self.root/'data/live/frames',self.run_id,
            self.plan['max_capture_bytes'],self.plan['minimum_free_bytes'])
        thresholds_path=self.root/self.plan['threshold_file']
        if hashlib.sha256(thresholds_path.read_bytes()).hexdigest()!=self.plan['threshold_sha256']:
            raise ValueError('frozen threshold hash mismatch')
        self.events=deque(maxlen=80);self.counts=Counter();self.latencies={}
        self.timings=deque(maxlen=8192);self.early=deque(maxlen=8192);self.curve=deque(maxlen=900)
        self.by_handler={};self.closed_trade_bars=deque(maxlen=14)
        self.performance=deque(maxlen=240);self.last_perf=0;self.last_ui=0
        self.feeds={n:{'connected':False,'messages':0,'connections':0,'disconnects':0,
                      'last_receive_ms':None,'last_source_ms':None,'last_error':None} for n in ('binance','pm','metadata')}
        self.market=None;self.ptb=None;self.price=None;self.sigma=None;self.clock=None
        self.reference_clock=ReferenceClock()
        self.books={};self.token_sides={};self.tradebars=TradeBars();self.last_trade=None
        self.shadow=LiveShadow(json.loads(thresholds_path.read_text('utf8')),self.event)
        self.error=None;self.status='STARTING';self.last_publish=0;self.last_status=0
        self.last_clock_wall=wall_ms();self.last_clock_mono=time.monotonic()
        self.process=psutil.Process();self.process.cpu_percent()

    def event(self,kind,payload):
        if kind in ('SIGNAL_LOCKED','PAPER_GATE','FROZEN_ENGINE') and getattr(getattr(self,'shadow',None),'session',None):
            payload={**payload,'paper_session_id':self.shadow.session['id']}
        self.archive.add(kind,payload)
        self.events.append({'time_ms':wall_ms(),'event':kind,**payload})
        self.counts[kind]+=1

    def utc_ms(self):
        return self.reference_clock.now(time.perf_counter_ns()) or wall_ms()

    def seen(self,name,received,source_ms=None):
        f=self.feeds[name];f['messages']+=1;f['last_receive_ms']=received;f['last_source_ms']=source_ms
        if source_ms is not None:
            delay=self.utc_ms()-source_ms
            values=self.latencies.setdefault(name,deque(maxlen=8192));values.append(delay*1_000_000)
            if delay<0:self.counts[name+'_future_timestamp']+=1
            elif delay>2000:self.counts[name+'_over_2s']+=1

    async def get(self,url,params=None,html=False,lane='market'):
        begin=wall_ms();r=await self.http.get(lane,url,params=params);received=(wall_ms(),time.perf_counter_ns())
        r.raise_for_status()
        payload=r.text if html else r.json()
        self.archive.add('HTTP_RESPONSE',{'url':str(r.url),'status':r.status_code,'request_ms':begin,
            'server_date':r.headers.get('date'),'payload':payload},received=received)
        return payload,received[0]

    async def clock_loop(self):
        while True:
            try:
                samples=[]
                for _ in range(3):
                    before=wall_ms();m0=time.perf_counter_ns()
                    data,after=await self.get('https://api.binance.com/api/v3/time',lane='clock')
                    rtt=(time.perf_counter_ns()-m0)/1e6
                    if abs((after-before)-rtt)>50:raise ValueError('wall-clock step during sample')
                    samples.append({'at_ms':after,'offset_ms':data['serverTime']-(before+after)/2,
                                    'uncertainty_ms':rtt/2,'rtt_ms':rtt,'sample_mono_ns':time.perf_counter_ns()})
                best=min(samples,key=lambda x:x['rtt_ms'])
                self.reference_clock.update(best,best['sample_mono_ns'])
                self.clock=self.reference_clock.public(time.perf_counter_ns());self.event('CLOCK',self.clock)
            except Exception as ex:self.event('CLOCK_ERROR',{'reason':f'{type(ex).__name__}: {ex}'})
            await asyncio.sleep(60)

    async def candle_bootstrap(self,start):
        rows,_=await self.get('https://api.binance.com/api/v3/klines',
            {'symbol':'BTCUSDT','interval':'15m','endTime':start*1000-1,'limit':14},lane='candles')
        bars=[{'start':x[0]//1000,'high':float(x[2]),'low':float(x[3]),'close':float(x[4])} for x in rows]
        if any(x[6]>=start*1000 for x in rows):raise ValueError('unclosed bootstrap candle')
        reference={b['start']:b for b in bars}
        for b in self.closed_trade_bars:
            if b.start in reference:
                result=reference[b.start]
                if any(abs(getattr(b,k)-result[k])>.0000001 for k in ('high','low','close')):
                    self.event('CANDLE_MISMATCH',{'trade':vars(b),'rest':result})
                    raise ValueError('contiguous trade candle differs from official REST; do not lock this signal')
        if self.closed_trade_bars:self.event('CANDLE_CHECK',{'checked':sum(b.start in reference for b in self.closed_trade_bars),'pass':True})
        self.shadow.lock(start,bars);self.shadow.bars=bars

    async def volatility_loop(self):
        while True:
            try:
                if not self.reference_clock.anchor:
                    await asyncio.sleep(.1);continue
                boundary=self.utc_ms()//60000*60
                rows,_=await self.get('https://api.binance.com/api/v3/klines',
                    {'symbol':'BTCUSDT','interval':'1m','endTime':boundary*1000-1,'limit':61},lane='volatility')
                v=Volatility()
                for x in rows:
                    if x[6]>=boundary*1000:raise ValueError('unclosed volatility candle')
                    v.push(x[0]//1000,float(x[4]))
                if v.last[0] != boundary-60:raise ValueError('minute bootstrap stale')
                self.sigma=v.sigma();self.sigma_until=(boundary+61)*1000
            except Exception as ex:
                self.sigma=None;self.event('VOLATILITY_ERROR',{'reason':f'{type(ex).__name__}: {ex}'})
            await asyncio.sleep(max(1,61-self.utc_ms()/1000%60))

    async def discovery(self):
        while True:
            if not self.reference_clock.anchor:
                await asyncio.sleep(.1);continue
            start=self.utc_ms()//900000*900
            try:
                rows,received=await self.get('https://gamma-api.polymarket.com/markets',{'slug':f'btc-updown-15m-{start}'})
                if not rows:raise ValueError('current BTC 15m market missing')
                market=normalize_market(rows[0],start)
                if not self.market or self.market['start']!=start:
                    if self.market:self.event('WINDOW_FINISHED',{'market':self.market,'paper':self.shadow.public()})
                    self.market=market;self.ptb=None;self.books={};self.token_sides={v:k for k,v in market['tokens'].items()}
                    self.event('MARKET_SELECTED',market)
                else:self.market=market
                if self.shadow.current!=start:await self.candle_bootstrap(start)
                if not self.ptb:
                    html,received=await self.get(f'https://polymarket.com/event/{market["slug"]}',html=True)
                    ptb=await asyncio.to_thread(website_reference,html,start)
                    ptb.update(observed_ms=self.utc_ms(),host_observed_ms=received,url=f'https://polymarket.com/event/{market["slug"]}')
                    if self.market['start']==start:
                        self.ptb=ptb;self.event('OFFICIAL_PTB',ptb)
                self.feeds['metadata']['connected']=True;self.feeds['metadata']['last_error']=None
                self.seen('metadata',received)
            except Exception as ex:
                self.feeds['metadata'].update(connected=False,last_error=f'{type(ex).__name__}: {ex}')
                self.event('METADATA_ERROR',{'reason':f'{type(ex).__name__}: {ex}'})
            await asyncio.sleep(10 if not self.ptb else min(30,901-self.utc_ms()/1000%900))

    async def settlements(self):
        # Only windows captured by this run. A close-price proxy is never a settlement label.
        pending={};seen_start=None
        while True:
            if self.market and self.market['start']!=seen_start:
                if seen_start is not None:pending[seen_start]=0
                seen_start=self.market['start']
            for start in list(pending):
                try:
                    rows,_=await self.get('https://gamma-api.polymarket.com/markets',{'slug':f'btc-updown-15m-{start}'},lane='settlement')
                    if not rows:raise ValueError('official settlement market missing; remains unknown')
                    m=rows[0];prices=m.get('outcomePrices');prices=json.loads(prices) if isinstance(prices,str) else prices
                    if m.get('closed') and m.get('umaResolutionStatus')=='resolved' and prices in (['1','0'],['0','1']):
                        self.event('OFFICIAL_SETTLEMENT',{'start':start,'winner':'Up' if prices[0]=='1' else 'Down',
                            'source':'Gamma closed + resolved + one-hot outcomePrices','actual_pnl':None})
                        del pending[start]
                    else:
                        pending[start]+=1
                        if pending[start]>=60:
                            self.event('SETTLEMENT_UNKNOWN',{'start':start,'reason':'not officially resolved within 60 polls'});del pending[start]
                except Exception as ex:self.event('SETTLEMENT_ERROR',{'start':start,'reason':f'{type(ex).__name__}: {ex}'})
            await asyncio.sleep(60)

    async def binance(self):
        retry=1
        while True:
            epoch=uuid.uuid4().hex;frame=0;f=self.feeds['binance']
            self.event('CONNECT_ATTEMPT',{'feed':'binance','connection':epoch})
            try:
                async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@trade',
                    open_timeout=12,ping_interval=20,ping_timeout=20,max_queue=64) as ws:
                    f.update(connected=True,last_error=None);f['connections']+=1;retry=1
                    self.event('CONNECTED',{'feed':'binance','connection':epoch})
                    while True:
                        raw=await asyncio.wait_for(ws.recv(),20);received=(wall_ms(),time.perf_counter_ns());frame+=1
                        self.archive.add('BINANCE_FRAME',raw,epoch,frame,received)
                        t0=time.perf_counter_ns();d=orjson.loads(raw)
                        if d.get('e')!='trade' or d.get('s')!='BTCUSDT':raise ValueError('unexpected raw trade schema')
                        tid,stamp,p=int(d['t']),int(d['T']),float(d['p'])
                        if not math.isfinite(p) or p<=0:raise ValueError('invalid trade price')
                        duplicate=self.last_trade is not None and tid==self.last_trade['id']
                        if duplicate:
                            if (stamp,p)!=(self.last_trade['source_ms'],float(self.last_trade['price'])):raise ValueError('conflicting trade duplicate')
                            self.counts['binance_duplicates']+=1;continue
                        if self.last_trade and (tid!=self.last_trade['id']+1 or stamp<self.last_trade['source_ms']):
                            self.event('BINANCE_SEQUENCE_GAP',{'previous':self.last_trade,'next_id':tid,'next_ms':stamp,'unknown':True})
                            self.shadow.disconnect(self.utc_ms(),'币安逐笔缺口；本窗口停止执行，后续窗口用官方已收盘 K 线重建')
                            self.tradebars=TradeBars()
                        self.last_trade={'id':tid,'source_ms':stamp,'price':d['p'],'quantity':d['q'],'receive_ms':received[0]}
                        closed=self.tradebars.push(tid,stamp,p)
                        if closed:
                            self.closed_trade_bars.append(closed);self.event('TRADE_BAR_CLOSED',vars(closed))
                        self.price=dict(self.last_trade);self.seen('binance',received[0],stamp)
                        self.decide(received[1])
                        self.measure(t0,'binance')
            except Exception as ex:
                f.update(connected=False,last_error=f'{type(ex).__name__}: {ex}');f['disconnects']+=1
                self.event('DISCONNECTED',{'feed':'binance','connection':epoch,'last':f['last_receive_ms'],'reason':f['last_error']})
                self.shadow.disconnect(self.utc_ms(),'币安连接断开，缺口未知')
                await asyncio.sleep(retry);retry=min(30,retry*2)

    def pm_event(self,d,received,epoch):
        kind=d.get('event_type');stamp=d.get('timestamp');now=self.utc_ms()
        self.seen('pm',received[0],int(stamp) if stamp else None)
        if kind=='book':
            side=self.token_sides.get(d.get('asset_id'))
            if side:
                b=self.books.get(side) or PublicBook();b.snapshot(d,now,epoch);self.books[side]=b
        elif kind=='price_change':
            for change in d['price_changes']:
                side=self.token_sides.get(change.get('asset_id'))
                if side:
                    b=self.books.get(side)
                    if not b:raise ValueError('PM delta arrived before snapshot')
                    b.delta(change,stamp,now,epoch)
        elif kind=='tick_size_change':
            self.shadow.disconnect(now,'官方最小价格步长变化，本窗口停止执行')
            self.event('TICK_CHANGE',d)
        elif kind in ('last_trade_price','market_resolved'):
            self.counts[kind]+=1
            # Trades are evidence of other participants, not receipts for shadow orders.

    async def pm(self):
        retry=1
        while True:
            if not self.market:await asyncio.sleep(.2);continue
            start=self.market['start'];epoch=uuid.uuid4().hex;f=self.feeds['pm'];frame=0
            self.books={};self.event('CONNECT_ATTEMPT',{'feed':'pm','connection':epoch,'start':start})
            try:
                async with websockets.connect('wss://ws-subscriptions-clob.polymarket.com/ws/market',
                    open_timeout=12,ping_interval=None,max_queue=64) as ws:
                    sub={'type':'market','assets_ids':list(self.market['tokens'].values()),'custom_feature_enabled':True}
                    await ws.send(orjson.dumps(sub).decode());self.archive.add('PM_SUBSCRIBE',sub,epoch)
                    f.update(connected=True,last_error=None);f['connections']+=1;retry=1
                    self.event('CONNECTED',{'feed':'pm','connection':epoch});ping=time.monotonic();pong=ping
                    while self.market and self.market['start']==start:
                        if time.monotonic()-ping>=10:
                            await ws.send('PING');ping=time.monotonic();self.archive.add('PM_PING',{},epoch)
                        if time.monotonic()-pong>25:raise TimeoutError('PM PONG timeout')
                        try:raw=await asyncio.wait_for(ws.recv(),1)
                        except asyncio.TimeoutError:continue
                        received=(wall_ms(),time.perf_counter_ns());frame+=1
                        self.archive.add('PM_FRAME',raw,epoch,frame,received)
                        if raw=='PONG':pong=time.monotonic();continue
                        t0=time.perf_counter_ns();data=orjson.loads(raw)
                        for d in data if isinstance(data,list) else [data]:self.pm_event(d,received,epoch)
                        self.decide(received[1])
                        self.measure(t0,'pm')
                    self.event('PLANNED_MARKET_SWITCH',{'feed':'pm','start':start,'connection':epoch})
            except Exception as ex:
                f['disconnects']+=1;f['last_error']=f'{type(ex).__name__}: {ex}'
                self.event('DISCONNECTED',{'feed':'pm','connection':epoch,'last':f['last_receive_ms'],'reason':f['last_error']})
                self.shadow.disconnect(self.utc_ms(),'PM 断线或盘口解析异常；重连后必须重新取得全量快照')
                await asyncio.sleep(retry);retry=min(30,retry*2)
            finally:
                f['connected']=False
                for b in self.books.values():b.valid=False

    def measure(self,t0,kind='decision'):
        elapsed=time.perf_counter_ns()-t0;self.timings.append(elapsed)
        self.by_handler.setdefault(kind,deque(maxlen=8192)).append(elapsed)
        if len(self.early)<8192:self.early.append(elapsed)

    def decide(self,received_mono=None):
        if not self.market or self.shadow.current!=self.market['start']:return
        t0=time.perf_counter_ns();now=self.utc_ms()
        self.clock=self.reference_clock.public(time.perf_counter_ns())
        self.shadow.step(self.market,self.ptb,self.books,self.price,
            self.sigma if now<getattr(self,'sigma_until',0) else None,self.clock,now)
        self.measure(t0,'decision')
        if received_mono is not None:
            self.by_handler.setdefault('receive_to_decision',deque(maxlen=8192)).append(time.perf_counter_ns()-received_mono)

    def public(self):
        now=self.utc_ms();host_now=wall_ms()
        clock=self.reference_clock.public(time.perf_counter_ns())
        sigma=self.sigma if now<getattr(self,'sigma_until',0) else None
        return {'status':self.status,'run_id':self.run_id,'source':'OFFICIAL_PUBLIC_LIVE',
            'now_ms':now,'host_now_ms':host_now,'started_ms':self.start_ms,'deadline_ms':self.plan['deadline_ms'],'pid':os.getpid(),
            'uptime_seconds':round(time.monotonic()-self.started,1),'market':self.market,'ptb':self.ptb,
            'price':self.price,'sigma':sigma,'clock':clock,
            'health':input_health(now,self.market,self.ptb,self.price,sigma,clock,self.books,self.shadow.signal),
            'http':self.http.public() if hasattr(self,'http') else {},
            'feeds':{k:{**v,'receive_age_ms':host_now-v['last_receive_ms'] if v['last_receive_ms'] else None} for k,v in self.feeds.items()},
            'books':{k:v.public(now) for k,v in self.books.items()},'paper':self.shadow.public(),
            'events':list(self.events),'counts':dict(self.counts),'storage':self.archive.status(),
            'performance':list(self.performance),'curve':list(self.curve),
            'handling':percentiles(self.timings),'early_handling':percentiles(self.early),
            'handler_breakdown':{k:percentiles(v) for k,v in self.by_handler.items()},
            'receive_lag':{k:percentiles(v) for k,v in self.latencies.items()},
            'error':self.error,'limitations':['Maker 队列位置、实际成交、订单往返延迟未知',
                'PM 盘口无全局源序号，接收序号不能证明上游连续',
                '待击败价来自官方网页公开查询，非已认证 PolyBolt 直连',
                '双边成本只作条件估算；未知成交不得计入收益'],
            'recovery_blocked':bool(self.shadow.recovery_reason)}

    async def monitor(self):
        while not self.stop.is_set():
            now=wall_ms();mono=time.monotonic()
            if self.archive.error:raise RuntimeError(self.archive.error)
            if deadline_reached(self.plan,now):
                self.status='COMPLETED';self.event('SOAK_DEADLINE',{'deadline_ms':self.plan['deadline_ms']});return
            jump=(now-self.last_clock_wall)/1000-(mono-self.last_clock_mono)
            self.last_clock_wall,self.last_clock_mono=now,mono
            if abs(jump)>.05:
                self.clock=None;self.reference_clock.anchor=None
                self.shadow.disconnect(max(now,self.shadow.engine.now),'系统时钟变化，停止本窗口执行')
                self.event('CLOCK_JUMP',{'seconds':jump})
            self.decide()
            if mono-self.last_ui>=1:
                if self.price:
                    point={'time':self.utc_ms()//1000,'value':float(self.price['price'])}
                    if self.curve and point['time']<=self.curve[-1]['time']:self.curve[-1]=point
                    else:self.curve.append(point)
                self.last_ui=mono
            if mono-self.last_perf>=60:
                self.last_perf=mono
                sample={'at_ms':now,'rss_mb':round(self.process.memory_info().rss/2**20,2),
                    'cpu_percent':self.process.cpu_percent(),'queue_pending':self.archive.queue.qsize(),
                    'handling':percentiles(self.timings),'records':self.archive.count,
                    'handler_breakdown':{k:percentiles(v) for k,v in self.by_handler.items()},
                    'objects':{'books':len(self.books),'windows':len(self.shadow.engine.windows),
                               'orders':len(self.shadow.engine.orders),'curve':len(self.curve),'events':len(self.events)}}
                self.performance.append(sample);self.event('PERFORMANCE',sample)
            if mono-self.last_publish>=.5:
                self.last_publish=mono;snapshot=self.public()
                try:self.output.put_nowait(snapshot)
                except queue.Full:pass # UI-only coalescing; raw audit is never silently dropped.
                if mono-self.last_status>=2:
                    self.last_status=mono
                    await asyncio.to_thread(self.write_status,snapshot)
            await asyncio.sleep(.1)
        self.status='STOPPED'

    def write_status(self,data):
        directory=self.root/'data/live';directory.mkdir(exist_ok=True,parents=True)
        path=directory/'status.json';tmp=directory/f'status.{self.run_id}.tmp'
        tmp.write_bytes(orjson.dumps(data,default=str))
        for _ in range(10):
            try:tmp.replace(path);return
            except PermissionError:time.sleep(.02)
        raise RuntimeError('status write blocked repeatedly')

    async def run(self):
        old=self.root/'data/live/status.json'
        previous_raw=old.read_bytes() if old.exists() else None
        previous=json.loads(previous_raw) if previous_raw else None
        self.shadow.session,self.shadow.archived_sessions,new_session=load_session(self.root,previous_raw)
        if previous and not new_session and (previous.get('paper',{}).get('orders') or previous.get('recovery_blocked')):
            self.shadow.recovery_reason='重启前存在未确认的影子意图；保留原预算，停止新增意图，等待离线对账'
            self.shadow.previous_account=previous.get('paper',{}).get('account')
            self.shadow.previous_orders=previous.get('paper',{}).get('orders',[])
        self.event('PROCESS_START',{'run_id':self.run_id,'plan':self.plan,
            'previous_run':previous.get('run_id') if previous else None,
            'unknown_gap_from_ms':previous.get('host_now_ms',previous.get('now_ms')) if previous else None,
            'gap_clock_domain':'raw host clock; any clock step makes elapsed gap uncertain'})
        if new_session:
            self.event('PAPER_SESSION_STARTED',{'session':self.shadow.session,
                'archived_sessions':self.shadow.archived_sessions,'fills_created':False,
                'historical_reserves_released':False})
            # Persist the epoch before processing any new market event. If this
            # fails, the consumed marker prevents silently starting it again.
            self.write_status(self.public())
        self.status='RUNNING'
        async with PublicHTTP(self.event) as self.http:
            tasks=[asyncio.create_task(f()) for f in (self.clock_loop,self.discovery,self.volatility_loop,self.binance,self.pm,self.settlements)]
            try:await self.monitor()
            except Exception as ex:
                self.status='ERROR';self.error=f'{type(ex).__name__}: {ex}'
            finally:
                for t in tasks:t.cancel()
                await asyncio.gather(*tasks,return_exceptions=True)
                with contextlib.suppress(Exception):self.event('PROCESS_STOP',{'status':self.status,'error':self.error})
                await asyncio.to_thread(self.archive.close)
                snapshot=self.public();self.write_status(snapshot)
                with contextlib.suppress(queue.Full):self.output.put_nowait(snapshot)


def live_main(root,output,stop):
    directory=Path(root)/'data/live';directory.mkdir(parents=True,exist_ok=True)
    with (directory/'collector.lock').open('a+b') as lock:
        lock.seek(0)
        if not lock.read(1):lock.write(b'0');lock.flush()
        lock.seek(0)
        try:msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        except OSError:
            output.put({'status':'ERROR','error':'another live collector holds the lock'});return
        try:asyncio.run(LiveCollector(root,output,stop).run())
        except Exception as ex:output.put({'status':'ERROR','error':f'{type(ex).__name__}: {ex}'})
