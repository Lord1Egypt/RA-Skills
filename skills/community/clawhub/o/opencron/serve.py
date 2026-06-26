#!/usr/bin/env python3
"""Standalone HTTP server for the OpenCron dashboard.

Reads job data and run history from disk, injects it into the HTML,
and serves a complete page — no client-side fetch needed, no auth.

The agent starts this on the bridge port (18790) which is already
exposed by every OpenClaw container.

Usage:
    python3 skills/opencron/serve.py [--port 18790]
"""

import argparse
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

JOBS_PATH = Path.home() / ".openclaw/cron/jobs.json"
RUNS_DIR = Path.home() / ".openclaw/cron/runs"
CACHE_DIR = Path(__file__).parent / ".cache"
DASHBOARD_CACHE = CACHE_DIR / "cron-dashboard.html"
DASHBOARD_URL = "https://raw.githubusercontent.com/firstfloris/opencron/master/cron-dashboard.html"


def fetch_dashboard():
    """Download dashboard HTML from GitHub and cache locally."""
    CACHE_DIR.mkdir(exist_ok=True)
    data = urllib.request.urlopen(DASHBOARD_URL).read()
    DASHBOARD_CACHE.write_bytes(data)
    return data.decode("utf-8")


def get_template():
    """Get dashboard HTML, fetching from GitHub if not cached."""
    if DASHBOARD_CACHE.exists():
        return DASHBOARD_CACHE.read_text("utf-8")
    return fetch_dashboard()


def read_jobs():
    """Read jobs.json from disk."""
    try:
        return json.loads(JOBS_PATH.read_text())
    except Exception:
        return {"jobs": []}


def read_runs(jobs):
    """Read all run history JSONL files into a dict keyed by job id."""
    runs = {}
    for job in jobs.get("jobs", []):
        job_id = job.get("id", "")
        run_file = RUNS_DIR / f"{job_id}.jsonl"
        if run_file.exists():
            entries = []
            for line in run_file.read_text().strip().split("\n"):
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
            runs[job_id] = entries
        else:
            runs[job_id] = []
    return runs


def render_page():
    """Build complete HTML with job data and run history embedded."""
    template = get_template()
    jobs = read_jobs()
    runs = read_runs(jobs)

    inject = (
        "<script>"
        "window.__OPENCRON_DATA=" + json.dumps(jobs) + ";"
        "window.__OPENCRON_RUNS=" + json.dumps(runs) + ";"
        "</script>"
    )

    # Inject before the closing </head> tag
    return template.replace("</head>", inject + "</head>")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html", "/cron.html"):
            self._serve_html()
        else:
            self.send_error(404)

    def _serve_html(self):
        html = render_page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, fmt, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="OpenCron dashboard server")
    parser.add_argument("--port", type=int, default=18790)
    args = parser.parse_args()

    # Pre-fetch dashboard template
    get_template()

    server = HTTPServer(("0.0.0.0", args.port), Handler)
    print(f"OpenCron dashboard: http://0.0.0.0:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
