#!/usr/bin/env python3
"""Minimal HTTP server for the OpenCron dashboard.

Serves the dashboard at / and live cron data at /cron-data.
Reads jobs.json on each request so data is always fresh.

Usage:
    python3 skills/opencron/serve.py [--port 8787]
"""

import argparse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

JOBS_PATH = Path.home() / ".openclaw/cron/jobs.json"
DASHBOARD_PATH = Path(__file__).parent / "cron_dashboard.html"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/cron-data":
            self._serve_json()
        elif self.path in ("/", "/index.html"):
            self._serve_html()
        else:
            self.send_error(404)

    def _serve_json(self):
        try:
            data = json.loads(JOBS_PATH.read_text())
        except Exception as e:
            data = {"error": str(e), "jobs": []}
        payload = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _serve_html(self):
        html = DASHBOARD_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, fmt, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="OpenCron dashboard server")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    server = HTTPServer(("0.0.0.0", args.port), Handler)
    print(f"OpenCron: http://0.0.0.0:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
