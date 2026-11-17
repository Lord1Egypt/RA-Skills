"""Local supervisor. API clients receive coalesced snapshots, never engine ownership."""
import asyncio
import contextlib
import multiprocessing as mp
import os
from pathlib import Path
import queue
import time
import uuid
from .worker import worker_main, describe_cases
from .storage import writer_main
from .live import live_main
import json


def idle():
    return {'status': 'idle', 'mode': 'OFFLINE_PAPER', 'source': 'SYNTHETIC', 'run_id': None,
            'scenario': None, 'progress': {'done': 0, 'total': 0}, 'account': {
                'cash': '60', 'reserved': '0', 'realized_synthetic_pnl': '0',
                'actual_strategy_profit': 'UNKNOWN', 'actual_fill_probability': 'UNKNOWN',
                'exchange_order_latency': 'NOT_MEASURED'},
            'orders': [], 'fills': [], 'windows': [], 'events': [], 'intents': [], 'curve': [],
            'latency': {'samples': 0, 'p50_us': None, 'p95_us': None, 'p99_us': None}}


class RuntimeManager:
    def __init__(self, root):
        self.root = Path(root)
        self.db_path = str(self.root/'data/paper.sqlite3')
        ctx = mp.get_context('spawn')
        self.commands, self.output = ctx.Queue(32), ctx.Queue(512)
        self.audit, self.writer_ack = ctx.Queue(1024), ctx.Queue(8)
        self.worker = ctx.Process(target=worker_main, args=(self.commands,self.output), daemon=True, name='pm-engine')
        self.writer = ctx.Process(target=writer_main, args=(self.audit,self.writer_ack,self.db_path), daemon=True, name='pm-audit')
        self.latest, self.storage = idle(), {'persisted_events': 0, 'last_commit_ms': None}
        self.version = 0
        self.error = None
        self.pending_command = None
        self.task = None
        self.closing = False
        self.live_queue=ctx.Queue(4);self.live_stop=ctx.Event();self.live=None
        self.live_latest={'status':'DISABLED','source':'OFFICIAL_PUBLIC_LIVE'}
        plan=self.root/'config/live_capture.json'
        if plan.exists() and json.loads(plan.read_text('utf8')).get('enabled'):
            self.live=ctx.Process(target=live_main,args=(str(self.root),self.live_queue,self.live_stop),daemon=True,name='pm-public-feeds')

    async def start(self):
        self.writer.start(); self.worker.start()
        if self.live:self.live.start()
        self.task = asyncio.create_task(self._pump())

    def public(self):
        return {**self.latest, 'version': self.version, 'runtime': {
            'api_pid': os.getpid(), 'worker_pid': self.worker.pid, 'writer_pid': self.writer.pid,
            'worker_alive': self.worker.is_alive(), 'writer_alive': self.writer.is_alive(),
            'storage': self.storage, 'error': self.error, 'pending_command': self.pending_command,
            'web_snapshot_interval_ms': 250, 'db': 'SQLite WAL / 独立写入进程'}}

    def command(self, action, scenario=None, delay_ms=180):
        if self.error or not self.worker.is_alive() or not self.writer.is_alive():
            raise ValueError('运行进程异常，请先检查日志')
        if self.pending_command:
            raise ValueError('上一条控制指令尚未确认')
        status = self.latest['status']
        allowed = {'start': status not in ('running','paused'), 'pause': status == 'running',
                   'resume': status == 'paused', 'stop': status in ('running','paused')}
        if not allowed.get(action):
            raise ValueError('当前状态不接受此操作')
        cmd = {'action': action}
        if action == 'start':
            if scenario not in {x['id'] for x in describe_cases()}:
                raise ValueError('未知演示用例')
            cmd.update(scenario=scenario, delay_ms=delay_ms, run_id=str(uuid.uuid4()))
        self.commands.put_nowait(cmd)
        self.pending_command = action
        self.version += 1
        return cmd.get('run_id')

    def _drain(self):
        while True:
            try:self.live_latest=self.live_queue.get_nowait();self.version+=1
            except queue.Empty:break
        for _ in range(256):
            try:
                message = self.output.get_nowait()
            except queue.Empty:
                break
            kind = message['kind']
            if kind == 'snapshot':
                self.latest = message['payload']
                self.pending_command = None
            elif kind in ('runtime_error','command_rejected'):
                self.error = message['reason']; self.pending_command = None
                self.latest['status'] = 'error'
            if kind in ('run_started','event','snapshot','runtime_error'):
                try:
                    self.audit.put_nowait(message)
                except queue.Full:
                    self.error = '审计队列满，停止演示；未持久化尾部状态未知'
                    self.commands.put_nowait({'action': 'stop'})
            self.version += 1
        while True:
            try:
                self.storage = self.writer_ack.get_nowait()
            except queue.Empty:
                break

    async def _pump(self):
        while not self.closing:
            self._drain()
            if not self.worker.is_alive() or not self.writer.is_alive():
                self.error = '计算或审计进程退出，禁止启动新回放'
                self.latest['status'] = 'error'
                self.version += 1
                if self.worker.is_alive():
                    with contextlib.suppress(queue.Full):
                        self.commands.put_nowait({'action': 'stop'})
            await asyncio.sleep(.02)

    async def close(self):
        self.live_stop.set()
        if self.live:
            await asyncio.to_thread(self.live.join,15)
            if self.live.is_alive():
                self.live.terminate();await asyncio.to_thread(self.live.join,2)
        with contextlib.suppress(queue.Full):
            self.commands.put_nowait({'action': 'shutdown'})
        await asyncio.to_thread(self.worker.join, 3)
        self.closing = True
        if self.task:
            await self.task
        self._drain()
        self.audit.put(None, timeout=1)
        await asyncio.to_thread(self.writer.join, 3)
        for p in (self.worker, self.writer):
            if p.is_alive():
                p.terminate(); await asyncio.to_thread(p.join, 1)
        for q in (self.commands,self.output,self.audit,self.writer_ack):
            q.close(); q.cancel_join_thread()
        self.live_queue.close();self.live_queue.cancel_join_thread()

    def live_public(self):
        state=dict(self.live_latest)
        state['process_alive']=bool(self.live and self.live.is_alive())
        host_ms=state.get('host_now_ms')
        state['snapshot_age_ms']=int(time.time()*1000)-host_ms if host_ms else None
        if state.get('status')=='RUNNING' and host_ms and state['snapshot_age_ms']>10000:
            state.update(status='ERROR',error='live status stale for more than 10s; new decisions unverified')
        if self.live and not self.live.is_alive() and state.get('status') not in ('COMPLETED','STOPPED','ERROR'):
            state.update(status='ERROR',error='live process exited; unpersisted tail and outage UNKNOWN')
        return state
