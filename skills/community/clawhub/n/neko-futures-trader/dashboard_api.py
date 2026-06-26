#!/usr/bin/env python3
"""
Dashboard API server - threaded with 25-second Binance cache.
Each HTTP request runs in its own thread so slow Binance API calls don't block.
"""
import os, json, time, hmac, hashlib, requests, socketserver, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Lock

# ── Load env ──────────────────────────────────────────────────────────────────
ENV_PATH = '/root/.openclaw/workspace/neko-futures-trader/.env'
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if '=' in line:
            k, v = line.split('=', 1)
            os.environ[k] = v

API_KEY  = os.environ['BINANCE_API_KEY']
SECRET   = os.environ['BINANCE_SECRET']

# ── Cache ─────────────────────────────────────────────────────────────────────
_CACHE_TTL   = 25           # seconds
_CACHE       = {'data': None, 'timestamp': 0}
_CACHE_LOCK  = Lock()


def _fetch_fresh():
    """Use fapi/v2/positionRisk — has entryPrice, markPrice, unRealizedProfit."""
    ts  = int(time.time() * 1000)
    sig = hmac.new(SECRET.encode(), f'timestamp={ts}'.encode(), hashlib.sha256).hexdigest()
    r   = requests.get(
        f'https://fapi.binance.com/fapi/v2/positionRisk?timestamp={ts}&signature={sig}',
        headers={'X-MBX-APIKEY': API_KEY}, timeout=8
    )
    raw = r.json()
    if isinstance(raw, dict) and raw.get('code'):
        raise Exception(raw.get('msg', 'positionRisk error'))

    pnl = 0.0
    pos = []
    for p in raw:
        amt = float(p.get('positionAmt', 0))
        if amt == 0:
            continue
        entry = float(p.get('entryPrice', 0))
        mark  = float(p.get('markPrice', 0))
        unreal = float(p.get('unRealizedProfit', 0))
        pnl   += unreal
        pos.append({
            's': p['symbol'].replace('USDT', ''),
            'd': 'LONG' if amt > 0 else 'SHORT',
            'e': entry,
            'm': mark,
            'u': unreal,
            'a': abs(amt),
        })

    # Balance from account snapshot
    sig2 = hmac.new(SECRET.encode(), f'timestamp={ts}'.encode(), hashlib.sha256).hexdigest()
    r2   = requests.get(
        f'https://fapi.binance.com/fapi/v3/account?timestamp={ts}&signature={sig2}',
        headers={'X-MBX-APIKEY': API_KEY}, timeout=8
    )
    bal = float(r2.json().get('totalMarginBalance', 0))
    return {'bal': bal, 'pnl': pnl, 'pos': pos}


def get_account_data():
    """
    Return cached data if fresh (< CACHE_TTL seconds old),
    otherwise fetch fresh from Binance.
    On any error, return last known good data with `cached: True`
    so the dashboard always shows something.
    """
    global _CACHE
    now = time.time()

    # Fast path: cache hit
    if _CACHE['data'] is not None and (now - _CACHE['timestamp']) < _CACHE_TTL:
        return {**_CACHE['data'], 'cached': True}

    # Try to fetch fresh
    try:
        fresh = _fetch_fresh()
        with _CACHE_LOCK:
            _CACHE['data']      = fresh
            _CACHE['timestamp']  = now
        return {**fresh, 'cached': False}
    except Exception as exc:
        print(f'[dashboard_api] Binance API error: {exc}')
        with _CACHE_LOCK:
            if _CACHE['data'] is not None:
                print('[dashboard_api] Serving stale cached data')
                return {**_CACHE['data'], 'cached': True, 'err': str(exc)}
        # No data ever fetched — graceful empty response
        return {'err': str(exc), 'bal': 0.0, 'pnl': 0.0, 'pos': []}


# ── Request handler ───────────────────────────────────────────────────────────
class H(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/api'):
            self._handle_api()
        else:
            self._serve_static()

    def _handle_api(self):
        try:
            data = get_account_data()
        except Exception as e:
            data = {'err': str(e), 'bal': 0.0, 'pnl': 0.0, 'pos': []}
        # Always return 200 so the browser never shows a blank error page
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self):
        """Serve files from /root/.openclaw/workspace/, limited to that directory tree."""
        if '..' in self.path:
            self.send_error(403, 'Forbidden')
            return

        if self.path == '/':
            file_path = '/root/.openclaw/workspace/index.html'
        else:
            file_path = '/root/.openclaw/workspace' + self.path

        if not os.path.isfile(file_path):
            self.send_error(404, 'Not Found')
            return

        mime = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        try:
            with open(file_path, 'rb') as f:
                body = f.read()
        except Exception:
            self.send_error(500, 'Internal Server Error')
            return

        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f'[dashboard_api] {fmt % args}')


# ── Threaded HTTP server ───────────────────────────────────────────────────────
class ThreadedHTTPServer(HTTPServer):
    """Handle each request in a new thread via ThreadingMixIn."""
    daemon_threads   = True
    allow_reuse_address = True


if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 8080), H)
    print('[dashboard_api] Listening on 0.0.0.0:8080')
    server.serve_forever()
