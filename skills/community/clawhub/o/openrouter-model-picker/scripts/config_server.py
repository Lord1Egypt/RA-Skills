#!/usr/bin/env python3
"""
HTTP server for model picker config updates + data serving.
- GET  /data   → return current picker data (fetch_models output)
- POST /apply  → write config (explicitly remove unselected models)
- GET  /health → health check (idle timer resets on every request)
- CORS-enabled, loopback-only.

Lifecycle:
  --port PORT         Listen port (default 18790)
  --idle SECONDS      Idle time before auto-shutdown (default 300)
                      0 = never auto-shutdown

After a successful POST /apply, the server shuts down within 5 seconds.
If no request comes in for --idle seconds, the server also shuts down.
"""
import json
import os
import subprocess
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 18790
IDLE_TIMEOUT = 600  # seconds (10 min), 0 = never

# Parse args: python3 config_server.py [--port N] [--idle N]
args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] in ('--port', '-p') and i + 1 < len(args):
        PORT = int(args[i + 1]); i += 2
    elif args[i] in ('--idle', '-t') and i + 1 < len(args):
        IDLE_TIMEOUT = int(args[i + 1]); i += 2
    else:
        i += 1


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Shared state ────────────────────────────────────────────────────────────
_last_activity = time.time()
_shutdown_flag = False

def activity():
    global _last_activity
    _last_activity = time.time()

def request_shutdown():
    global _shutdown_flag
    _shutdown_flag = True

# ── Helpers ─────────────────────────────────────────────────────────────────
def to_config_id(mid):
    if not mid: return mid
    return mid if mid.startswith('openrouter/') else 'openrouter/' + mid

def get_picker_data():
    script = os.path.join(SCRIPT_DIR, "fetch_models.py")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        return {"error": result.stderr}
    return json.loads(result.stdout)

def get_current_models():
    try:
        r = subprocess.run(
            ["openclaw", "config", "get", "agents.defaults.models"],
            capture_output=True, text=True, timeout=10
        )
        return set(json.loads(r.stdout).keys())
    except Exception:
        return set()

# ── Handler ─────────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        activity()
        if self.path == '/data':
            data = get_picker_data()
            self._json(200, data)
        elif self.path == '/health':
            elapsed = time.time() - _last_activity
            self._json(200, {"status": "ok", "idle_seconds": round(elapsed, 1)})

        else:
            self.send_error(404)

    def do_POST(self):
        activity()
        if self.path != '/apply':
            self.send_error(404)
            return

        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))

        primary = to_config_id(body.get('primary', ''))
        enabled = [to_config_id(e) for e in body.get('enabled', []) if e]
        fallbacks = [to_config_id(f) for f in body.get('fallbacks', []) if f]

        models_dict = {mid: {} for mid in enabled}
        current_ids = get_current_models()
        to_remove = current_ids - set(enabled)
        for rid in to_remove:
            models_dict[rid] = None

        patch = {
            "agents": {
                "defaults": {
                    "model": {"primary": primary, "fallbacks": fallbacks},
                    "models": models_dict
                }
            }
        }

        result = subprocess.run(
            ['openclaw', 'config', 'patch', '--stdin'],
            input=json.dumps(patch), capture_output=True, text=True
        )
        validate = subprocess.run(
            ['openclaw', 'config', 'validate'],
            capture_output=True, text=True
        )

        ok = result.returncode == 0
        if ok:
            # Signal to the assistant that apply succeeded
            try:
                with open('/tmp/picker-applied', 'w') as f:
                    f.write('1')
            except Exception:
                pass

        resp = {
            "success": ok,
            "primary": primary,
            "enabled_count": len(enabled),
            "removed_count": len(to_remove),
            "patch_output": result.stdout.strip(),
            "validate": validate.stdout.strip(),
            "hot_reloaded": ok
        }
        if not ok:
            resp["error"] = result.stderr.strip()

        self._json(200 if ok else 500, resp)

        if ok:
            # Schedule shutdown after successful apply (grace period allows
            # the response to be fully sent before the socket closes)
            request_shutdown()

    def do_OPTIONS(self):
        activity()
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        pass  # we use our own logging below

# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), Handler)
    server.timeout = 5  # poll interval for idle/shutdown checks

    timeout_str = f"{IDLE_TIMEOUT}s" if IDLE_TIMEOUT > 0 else "never"
    print(f"[config-server] http://127.0.0.1:{PORT} | idle-timeout: {timeout_str} | pid={os.getpid()}", flush=True)

    shutdown_reason = ""
    try:
        while not _shutdown_flag:
            server.handle_request()  # blocks up to timeout=5s, then returns
            if _shutdown_flag:
                shutdown_reason = "after-apply"
                break
            elapsed = time.time() - _last_activity
            if IDLE_TIMEOUT > 0 and elapsed > IDLE_TIMEOUT:
                shutdown_reason = f"idle-{elapsed:.0f}s"
                break
    except KeyboardInterrupt:
        shutdown_reason = "interrupt"

    server.server_close()
    print(f"[config-server] Stopped ({shutdown_reason})", flush=True)