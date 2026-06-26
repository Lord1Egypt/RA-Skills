import os, json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

host = os.environ.get("HOST") or "0.0.0.0"
env_ports = ["PORT","HTTP_PORT","WEB_PORT","APP_PORT","SERVER_PORT","LISTEN_PORT","UVICORN_PORT","CLAWHUB_PORT"]
port = None
for k in env_ports:
    v = os.environ.get(k)
    if v and v.isdigit():
        port = int(v)
        break
if port is None:
    port = 8080

class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path in ["/", "/health"]:
            self._send(200, {"status":"ok","project":"MuskInsider"})
        elif self.path == "/invoke":
            self._send(200, {
                "title": "Elon 今日决策内参 (Bare)",
                "mood_index": "Bullish",
                "highlights": ["Bare server active"],
                "notice": "支付 0.01U 获取完整深度分析",
                "api_status": "bare"
            })
        else:
            self._send(404, {"error":"not found"})
    def do_POST(self):
        if self.path == "/invoke":
            self._send(200, {
                "charge_id": "musk_order_001",
                "payment_url": "https://pay.skillpay.me/order/sample",
                "message": "请扫码支付 0.01U 获取马斯克今日内参"
            })
        else:
            self._send(404, {"error":"not found"})

def run_on(p):
    try:
        HTTPServer((host, p), H).serve_forever()
    except Exception:
        pass

if __name__ == "__main__":
    ports = [port] if port else []
    for candidate in [8080, 8000, 3000, 80]:
        if candidate not in ports:
            ports.append(candidate)
    started = False
    for p in ports:
        try:
            t = threading.Thread(target=run_on, args=(p,), daemon=True)
            t.start()
            started = True
        except Exception:
            continue
    if started:
        threading.Event().wait()
    else:
        pass
