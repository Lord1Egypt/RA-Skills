"""Isolated, recoverable public GET clients. No order or authentication support.

Each periodic job owns a lane. A broken pool is discarded after a transport
failure; other jobs retain their connections. Retrying is left to the existing
job schedule, so a reset does not duplicate a request or change its frequency.
"""
import asyncio
import time
import httpx


LANES = ('clock', 'market', 'candles', 'volatility', 'settlement')


class PublicHTTP:
    def __init__(self, emit, factory=None, request_seconds=15, close_seconds=2):
        self.emit = emit
        self.factory = factory or (lambda lane: httpx.AsyncClient(
            timeout=15, follow_redirects=True,
            limits=httpx.Limits(max_connections=2, max_keepalive_connections=2)))
        self.request_seconds = request_seconds
        self.close_seconds = close_seconds
        self.clients = {}
        self.locks = {lane: asyncio.Lock() for lane in LANES}
        self.state = {lane: {'requests': 0, 'failures': 0, 'resets': 0,
                            'last_success_ms': None, 'last_error': None} for lane in LANES}

    async def _discard(self, lane):
        client = self.clients.pop(lane, None)
        if client is not None:
            try:
                async with asyncio.timeout(self.close_seconds):
                    await client.aclose()
            except Exception as ex:
                self.emit('HTTP_CLOSE_ERROR', {'lane': lane, 'reason': f'{type(ex).__name__}: {ex}'})

    async def get(self, lane, url, params=None):
        if lane not in self.locks:
            raise ValueError('unknown public HTTP lane')
        async with self.locks[lane]:
            state = self.state[lane]
            if lane not in self.clients:
                self.clients[lane] = self.factory(lane)
            begin = time.perf_counter_ns()
            state['requests'] += 1
            self.emit('HTTP_REQUEST', {'lane': lane, 'url': url, 'params': params,
                                      'request_host_ms': time.time_ns() // 1_000_000})
            try:
                async with asyncio.timeout(self.request_seconds):
                    response = await self.clients[lane].get(url, params=params)
                    response.raise_for_status()
            except asyncio.CancelledError:
                # The collector closes all clients after cancelling its jobs.
                raise
            except Exception as ex:
                reason = f'{type(ex).__name__}: {ex}'
                state['failures'] += 1
                state['last_error'] = reason
                self.emit('HTTP_ERROR', {'lane': lane, 'url': url, 'reason': reason,
                    'elapsed_ms': (time.perf_counter_ns() - begin) / 1e6})
                if isinstance(ex, (httpx.TransportError, TimeoutError)):
                    state['resets'] += 1
                    await self._discard(lane)
                    self.emit('HTTP_POOL_RESET', {'lane': lane, 'reason': reason,
                                                 'retry': 'next scheduled poll only'})
                raise
            state['last_success_ms'] = time.time_ns() // 1_000_000
            state['last_error'] = None
            return response

    def public(self):
        return {lane: dict(value) for lane, value in self.state.items()}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await asyncio.gather(*(self._discard(lane) for lane in list(self.clients)))
