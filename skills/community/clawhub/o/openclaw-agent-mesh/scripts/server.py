#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = pathlib.Path(__file__).resolve().parent
MESH = ROOT / 'mesh.py'


def run_mesh(args, state_dir: str):
    env = os.environ.copy()
    env['OPENCLAW_AGENT_MESH_DIR'] = state_dir
    res = subprocess.run([sys.executable, str(MESH)] + args, env=env, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr


class Handler(BaseHTTPRequestHandler):
    state_dir = ''

    def _send(self, code: int, obj: dict):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/agent-mesh/discovery':
            rc, out, err = run_mesh(['discovery'], self.state_dir)
            if rc == 0:
                self._send(200, json.loads(out))
            else:
                self._send(500, {'ok': False, 'error': err or out})
            return
        self._send(404, {'ok': False, 'error': 'not_found'})

    def do_POST(self):
        length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode('utf-8') or '{}')
        except Exception:
            self._send(400, {'ok': False, 'error': 'invalid_json'})
            return

        tmp = pathlib.Path(self.state_dir) / 'tmp'
        tmp.mkdir(parents=True, exist_ok=True)

        if self.path == '/agent-mesh/contact-request':
            p = tmp / 'incoming-contact.json'
            p.write_text(json.dumps(payload))
            rc, out, err = run_mesh(['receive-contact', str(p)], self.state_dir)
            if rc == 0:
                self._send(200, {'ok': True, 'result': json.loads(out)})
            else:
                self._send(400, {'ok': False, 'error': err or out})
            return

        if self.path == '/agent-mesh/message':
            p = tmp / 'incoming-message.json'
            p.write_text(json.dumps(payload))
            rc, out, err = run_mesh(['receive-message', str(p)], self.state_dir)
            if rc == 0:
                self._send(200, {'ok': True, 'result': json.loads(out)})
            else:
                self._send(400, {'ok': False, 'error': err or out})
            return

        self._send(404, {'ok': False, 'error': 'not_found'})


def main():
    ap = argparse.ArgumentParser(description='OpenClaw Agent Mesh V1 server')
    ap.add_argument('--host', default='0.0.0.0')
    ap.add_argument('--port', type=int, default=8787)
    ap.add_argument('--state-dir', default=os.path.expanduser('~/.openclaw/agent-mesh'))
    args = ap.parse_args()

    Handler.state_dir = args.state_dir
    httpd = HTTPServer((args.host, args.port), Handler)
    print(json.dumps({'ok': True, 'host': args.host, 'port': args.port, 'state_dir': args.state_dir}))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
