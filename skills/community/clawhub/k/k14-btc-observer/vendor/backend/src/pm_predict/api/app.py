"""Loopback-only control plane. The browser cannot call arbitrary engine events."""
import asyncio
from contextlib import asynccontextmanager
import json
import mimetypes
import queue
import time
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
import orjson
from pm_predict.runtime.manager import RuntimeManager
from pm_predict.runtime.worker import describe_cases
from pm_predict.runtime.storage import history, load_run

ROOT = Path(__file__).resolve().parents[4]
# Windows registry associations can otherwise serve .js as text/plain, breaking ES modules.
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/css', '.css')


class Command(BaseModel):
    model_config = ConfigDict(extra='forbid')
    action: Literal['start','pause','resume','stop']
    scenario: str | None = None
    delay_ms: int = Field(default=180, ge=0, le=1000)


def same_origin(origin, host):
    if origin is None:
        return True
    u = urlparse(origin)
    return u.scheme in ('http','https') and u.netloc == host


def create_app(root=ROOT):
    @asynccontextmanager
    async def lifespan(app):
        app.state.runtime = RuntimeManager(root)
        await app.state.runtime.start()
        yield
        await app.state.runtime.close()

    app = FastAPI(title='PM Predict · Paper Console', version='0.1.0', lifespan=lifespan)

    @app.middleware('http')
    async def local_control(request: Request, call_next):
        host = request.headers.get('host','').split(':')[0]
        if host not in ('127.0.0.1','localhost','testserver'):
            return Response('Invalid host', status_code=400)
        if request.method not in ('GET','HEAD','OPTIONS') and not same_origin(request.headers.get('origin'), request.headers.get('host')):
            return Response('Cross-origin control denied', status_code=403)
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'no-store' if request.url.path.startswith('/api') else 'no-cache'
        return response

    @app.get('/api/state')
    async def state(request: Request):
        return Response(orjson.dumps(request.app.state.runtime.public(), default=str), media_type='application/json')

    @app.get('/api/config')
    async def config():
        th = json.loads((Path(root)/'config/thresholds_2026-10.json').read_text('utf-8'))
        bench = Path(root)/'reports/benchmark.json'
        return {'mode': 'OFFLINE_PAPER', 'data_source': 'SYNTHETIC', 'thresholds': th,
                'cases': describe_cases(), 'benchmark': json.loads(bench.read_text('utf-8')) if bench.exists() else None,
                'limits': {'capital':60,'shares':5,'entry_seconds':120,'no_buy_last_seconds':60,
                           'max_price':.50,'entry_cap':.48,'pair_cap':.95,'daily_risk':6,'total_risk':20}}

    @app.get('/api/live')
    async def live(request: Request):
        return Response(orjson.dumps(request.app.state.runtime.live_public(),default=str),media_type='application/json')

    @app.post('/api/live/stop')
    async def live_stop(request: Request):
        request.app.state.runtime.live_stop.set()
        return {'stopping':True,'note':'flush public audit and stop; no orders exist at exchange'}

    @app.post('/api/control')
    async def control(c: Command, request: Request):
        try:
            run_id = request.app.state.runtime.command(c.action, c.scenario, c.delay_ms)
        except (ValueError, queue.Full) as ex:
            # Control failure never falls through to an execution adapter.
            raise HTTPException(409, str(ex)) from ex
        return {'accepted': True, 'run_id': run_id}

    @app.get('/api/runs')
    async def runs(request: Request):
        return await asyncio.to_thread(history, request.app.state.runtime.db_path)

    @app.get('/api/runs/{run_id}')
    async def run(run_id: str, request: Request):
        row = await asyncio.to_thread(load_run, request.app.state.runtime.db_path, run_id)
        if row is None:
            raise HTTPException(404, 'Run not found')
        return row

    @app.websocket('/ws')
    async def websocket(ws: WebSocket):
        if not same_origin(ws.headers.get('origin'), ws.headers.get('host')):
            await ws.close(code=1008); return
        await ws.accept()
        last = -1
        last_sent = 0
        try:
            while True:
                runtime = ws.app.state.runtime
                if runtime.version != last or time.monotonic() - last_sent >= 2:
                    last = runtime.version
                    await asyncio.wait_for(ws.send_text(orjson.dumps(runtime.public(), default=str).decode()), timeout=2)
                    last_sent = time.monotonic()
                # UI transport only. The engine is independently event-driven.
                await asyncio.sleep(.25)
        except (WebSocketDisconnect, asyncio.TimeoutError, RuntimeError):
            return

    dist = Path(root)/'frontend/dist'
    if (dist/'assets').exists():
        app.mount('/assets', StaticFiles(directory=dist/'assets'), name='assets')

    @app.get('/')
    async def index():
        if not (dist/'index.html').exists():
            raise HTTPException(503, 'Frontend not built. Run npm run build in frontend.')
        return FileResponse(dist/'index.html')

    return app


app = create_app()
