"""Reuse reviewed official public feeds in a separate process directory.

The callback is invoked on data events, not by polling the old UI/old intents.
The existing collector and historical paper ledger are never opened for writes.
"""
import asyncio
from collections import Counter,deque
import contextlib
import json
from pathlib import Path
import queue
import sys
import time
from types import SimpleNamespace
from common import atomic_json

def load_core(config):
    root=Path(config.source_root).resolve()
    if not (root/'backend/src/pm_predict/strategy/trial_session.py').exists():raise ValueError('reviewed TrialSession core missing')
    sys.dont_write_bytecode=True
    sys.path.insert(0,str(root/'backend/src'))
    if config.source_sha256:
        import hashlib
        for f,expected in config.source_sha256.items():
            if hashlib.sha256((root/f).read_bytes()).hexdigest()!=expected:raise ValueError('reviewed source changed: '+f)

def make_feed(config,root,callback,stop):
    load_core(config)
    from pm_predict.runtime.live import LiveCollector
    from pm_predict.runtime.public_http import PublicHTTP
    from pm_predict.strategy.indicators import Bar,k14,signal,fair_up
    from pm_predict.runtime.worker import percentiles
    source=Path(config.source_root);root=Path(root)
    (root/'config').mkdir(parents=True,exist_ok=True)
    plan=json.loads((source/'config/live_capture.json').read_text('utf-8'))
    # Own bounded archive, never the source collector's directory/epoch.
    plan['max_capture_bytes']=2*1024**3
    atomic_json(root/'config/live_capture.json',plan)
    th=plan['threshold_file'];target=root/th;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes((source/th).read_bytes())

    class SignalOnly:
        def __init__(self,thresholds):
            self.thresholds=thresholds;self.current=None;self.signal=None;self.bars=[]
            self.blocked_window=None;self.block_reason=None;self.recovery_reason=None
            self.engine=SimpleNamespace(now=0,windows={},orders={});self.session=None
        def lock(self,start,bars):
            if self.thresholds.get('provisional') is not False:raise ValueError('provisional thresholds are not executable')
            value=k14([Bar(**x) for x in bars],start)
            self.current=start;self.bars=bars
            self.signal={'start':start,'k14':value,'side':signal(value,self.thresholds,start),'fair_up':None}
        def disconnect(self,now,reason):
            self.engine.now=max(self.engine.now,now);self.blocked_window=self.current;self.block_reason=reason
        def public(self):return {'signal':self.signal,'thresholds':self.thresholds,'orders':[]}

    class EventFeed(LiveCollector):
        def __init__(self):
            super().__init__(root,queue.Queue(maxsize=1),stop)
            self.shadow=SignalOnly(json.loads((root/th).read_text('utf-8')))
            self.last_emit_mono=0
        def decide(self,received_mono=None):
            if not self.market or self.shadow.current!=self.market['start']:return
            t=time.monotonic()
            if t-self.last_emit_mono<config.decision_interval_ms/1000:return
            self.last_emit_mono=t
            began=time.perf_counter_ns();s=self.public();s['process_alive']=True
            if self.shadow.blocked_window==self.shadow.current:
                s['health']={'status':'DEGRADED','reasons':[self.shadow.block_reason]}
            if s['price'] and s['ptb'] and s['sigma'] is not None:
                s['paper']['signal']['fair_up']=fair_up(float(s['price']['price']),s['ptb']['value'],s['sigma'],900-(s['now_ms']/1000-self.market['start']))
            s['source_received_monotonic_ns']=time.perf_counter_ns()
            callback(s)
            self.measure(began,'executor_snapshot')
        def monitor_local(self):
            wall=time.time_ns()//1000000;mono=time.monotonic()
            jump=(wall-self.last_clock_wall)/1000-(mono-self.last_clock_mono)
            self.last_clock_wall,self.last_clock_mono=wall,mono
            if abs(jump)>.05:
                self.clock=None;self.reference_clock.anchor=None
                self.shadow.disconnect(self.utc_ms(),'host clock jumped; current window blocked')
                self.event('CLOCK_JUMP',{'seconds':jump})
            if mono-self.last_perf>=60:
                self.last_perf=mono
                sample={'at_ms':self.utc_ms(),'rss_mb':round(self.process.memory_info().rss/2**20,2),
                    'cpu_percent':self.process.cpu_percent(),'queue_pending':self.archive.queue.qsize(),
                    'handler_breakdown':{k:percentiles(v) for k,v in self.by_handler.items()},
                    'records':self.archive.count,'mode':'independent public feed; no trade execution timing'}
                self.performance.append(sample);self.event('PERFORMANCE',sample)
        async def run(self):
            self.status='RUNNING'
            async with PublicHTTP(self.event) as self.http:
                tasks=[asyncio.create_task(f()) for f in (self.clock_loop,self.discovery,self.volatility_loop,self.binance,self.pm,self.settlements)]
                try:
                    while not stop.is_set():
                        if self.archive.error:raise RuntimeError(self.archive.error)
                        for task in tasks:
                            if task.done():
                                await task
                                raise RuntimeError('public feed background task unexpectedly stopped')
                        self.monitor_local();self.decide();await asyncio.sleep(.05)
                finally:
                    for task in tasks:task.cancel()
                    await asyncio.gather(*tasks,return_exceptions=True)
                    self.status='STOPPED'
                    await asyncio.to_thread(self.archive.close)
    return EventFeed()
