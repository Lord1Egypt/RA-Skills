"""
Whisper proxy: rewrites model=default -> model=Systran/faster-whisper-base
Listens on :8001, forwards to http://localhost:8000
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, urllib.error, re, sys

UPSTREAM = 'http://localhost:8000'
CORRECT_MODEL = b'Systran/faster-whisper-base'


class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silent

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        # Rewrite model field in multipart form: name="model"\r\n\r\n<value>
        if b'name="model"' in body:
            body = re.sub(
                rb'(name="model"\r\n\r\n)[^\r\n\-]+',
                lambda m: m.group(1) + CORRECT_MODEL,
                body,
            )

        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in ('host', 'content-length')}
        headers['Content-Length'] = str(len(body))

        req = urllib.request.Request(
            UPSTREAM + self.path, data=body,
            headers=headers, method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in ('transfer-encoding',):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(data)

    def do_GET(self):
        req = urllib.request.Request(UPSTREAM + self.path)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in ('transfer-encoding',):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(data)
        except Exception:
            self.send_response(502)
            self.end_headers()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    server = HTTPServer(('0.0.0.0', port), ProxyHandler)
    print(f'Whisper proxy on :{port} -> {UPSTREAM}', flush=True)
    server.serve_forever()
