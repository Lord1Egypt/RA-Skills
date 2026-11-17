"""Read-only loopback sidecar; leaves the public collector and paper ledger alone."""
import asyncio
from collections import deque
from contextlib import asynccontextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx
import orjson

from pm_predict.strategy.exit_routes import evaluate_snapshot

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'reports/exit_watch'


def encoded(value):
    return orjson.dumps(value, default=str, option=orjson.OPT_SORT_KEYS)


def atomic_json(path, value):
    tmp = path.with_suffix(f'.{os.getpid()}.tmp')
    tmp.write_bytes(encoded(value))
    for i in range(5):
        try:
            tmp.replace(path)
            return
        except PermissionError:
            time.sleep(.02 * (i + 1))
    raise OSError('cannot persist exit-watch status')


class Journal:
    def __init__(self):
        self.run = uuid.uuid4().hex
        self.index = 0
        self.seq = 0
        self.previous = None
        self.previous_segment = None
        self.fp = None
        self.open()

    def open(self):
        self.path = OUT / f'{self.run}_{self.index:04d}.jsonl'
        self.fp = self.path.open('xb')
        self.digest = hashlib.sha256()
        self.size = 0

    def append(self, row):
        if self.size >= 16 * 1024 * 1024:
            self.close()
            self.index += 1
            self.open()
        self.seq += 1
        payload = encoded({**row, 'record': self.seq, 'previous_sha256': self.previous})
        self.fp.write(payload + b'\n')
        self.fp.flush()
        self.digest.update(payload + b'\n')
        self.size += len(payload) + 1
        self.previous = hashlib.sha256(payload).hexdigest()

    def close(self):
        if self.fp is None:
            return
        self.fp.flush()
        os.fsync(self.fp.fileno())
        self.fp.close()
        self.fp = None
        digest = self.digest.hexdigest()
        atomic_json(self.path.with_suffix('.seal.json'), {
            'sha256': digest, 'file': self.path.name, 'last_record': self.seq,
            'last_record_sha256': self.previous, 'previous_segment_sha256': self.previous_segment})
        self.previous_segment = digest


async def observe(app, plan):
    checks = 0
    timings = deque(maxlen=1024)
    journal = Journal()
    last_state = None
    last_log = 0.
    last_source = None
    last_source_mono = 0.
    try:
        async with httpx.AsyncClient(trust_env=False, timeout=2) as client:
            while True:
                begin = time.perf_counter()
                host_ms = time.time_ns() // 1_000_000
                if (OUT / 'STOP').exists():
                    raise RuntimeError('用户停止退出观察器')
                if shutil.disk_usage(ROOT).free < plan['minimum_free_bytes']:
                    raise RuntimeError('空闲磁盘低于 5 GiB，退出观察器停止写入')
                if hashlib.sha256((ROOT / 'config/exit_watch.json').read_bytes()).hexdigest() != app.state.plan_hash:
                    raise RuntimeError('封存配置改变；禁止运行中自动采用新参数')
                capture = json.loads((ROOT / 'config/live_capture.json').read_text('utf-8'))
                try:
                    if not capture.get('enabled'):
                        raise ValueError('主采集已被用户禁用')
                    response = await client.get(plan['source'])
                    response.raise_for_status()
                    s = response.json()
                    receive = time.perf_counter()
                    source = (s.get('run_id'), s.get('now_ms'))
                    if source != last_source:
                        last_source, last_source_mono = source, receive
                    source_age = max(s.get('snapshot_age_ms', 0), (receive - last_source_mono) * 1000)
                    source_age += (receive - begin) * 1000
                    calc = time.perf_counter_ns()
                    result = evaluate_snapshot(s, plan, source_age_ms=source_age)
                    timings.append((time.perf_counter_ns() - calc) / 1000)
                    result['input_fingerprint'] = {
                        'trade_id': (s.get('price') or {}).get('id'),
                        'book_source_ms': {k: v.get('source_ms') for k, v in s.get('books', {}).items()},
                        'book_local_seq': {k: v.get('local_sequence') for k, v in s.get('books', {}).items()},
                        'raw_records': s.get('storage', {}).get('received')}
                    result['source_snapshot_age_ms'] = source_age
                except (httpx.HTTPError, ValueError, TypeError) as ex:
                    result = {'state': 'INPUT_UNKNOWN', 'message': '输入不可用，停止路线建议并持续检查恢复。',
                              'issues': [str(ex)], 'routes': None, 'execution_allowed': False}
                checks += 1
                ordered = sorted(timings)
                result.update(host_ms=time.time_ns() // 1_000_000, pid=os.getpid(), checks=checks,
                              version=plan['version'], plan_sha256=app.state.plan_hash,
                              mode=plan['mode'], poll_seconds=plan['poll_seconds'],
                              calculation_p95_us=ordered[int(.95 * (len(ordered) - 1))] if ordered else None,
                              actual_orders_sent=0, actual_profit=None)
                app.state.latest = result
                # Keep decision transitions plus periodic source snapshots. The main
                # collector retains raw events. Do not pretend 1s polling is lossless.
                routes = result.get('routes') or {}
                state = (result['state'], result.get('market'), result.get('order_id'),
                         routes.get('recommendation'), tuple(result.get('issues', [])),
                         routes.get('wait', {}).get('risk_deadline_reached'))
                if state != last_state or time.monotonic() - last_log >= 15:
                    await asyncio.to_thread(journal.append, {'host_ms': result['host_ms'], 'type': 'OBSERVATION', 'snapshot': result})
                    last_state, last_log = state, time.monotonic()
                await asyncio.to_thread(atomic_json, OUT / 'status.json', result)
                await asyncio.sleep(max(.05, plan['poll_seconds'] - (time.perf_counter() - begin)))
    except asyncio.CancelledError:
        app.state.latest = {**app.state.latest, 'state': 'STOPPED', 'message': '退出观察器已停止', 'host_ms': time.time_ns() // 1_000_000}
        raise
    except Exception as ex:
        app.state.latest = {**app.state.latest, 'state': 'ERROR', 'routes': None,
                            'message': str(ex), 'host_ms': time.time_ns() // 1_000_000}
    finally:
        await asyncio.to_thread(journal.close)
        await asyncio.to_thread(atomic_json, OUT / 'status.json', app.state.latest)


@asynccontextmanager
async def lifespan(app):
    OUT.mkdir(parents=True, exist_ok=True)
    data = (ROOT / 'config/exit_watch.json').read_bytes()
    plan = json.loads(data)
    if not plan['enabled'] or plan['source'] != 'http://127.0.0.1:8765/api/live' or plan['order_submission'] != 'NONE':
        raise ValueError('exit observer must remain local, public-data-only and enabled')
    app.state.plan_hash = hashlib.sha256(data).hexdigest()
    app.state.latest = {'state': 'STARTING', 'message': '退出路线观察器启动中', 'routes': None}
    task = asyncio.create_task(observe(app, plan))
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)


@app.middleware('http')
async def read_only(request: Request, call_next):
    if request.headers.get('host', '').split(':')[0] not in ('localhost', '127.0.0.1', 'testserver'):
        return Response(status_code=400)
    if request.method not in ('GET', 'HEAD', 'OPTIONS'):
        return Response(status_code=405)
    response = Response(status_code=204) if request.method == 'OPTIONS' else await call_next(request)
    if request.headers.get('origin') in ('http://127.0.0.1:8765', 'http://localhost:8765'):
        response.headers['Access-Control-Allow-Origin'] = request.headers['origin']
        response.headers['Vary'] = 'Origin'
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.get('/status')
async def status(request: Request):
    return Response(encoded(request.app.state.latest), media_type='application/json')
