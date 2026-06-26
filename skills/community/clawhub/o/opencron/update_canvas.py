#!/usr/bin/env python3
"""Deploy the OpenCron dashboard with embedded data.

Fetches the dashboard HTML from GitHub, reads job data and run history
from disk, injects them inline, and writes to the gateway's static UI
directory so it's served at /cron.html on the same port as OpenClaw.

Usage:
    python3 skills/opencron/update_canvas.py
"""

import json
import urllib.request
from pathlib import Path

JOBS_PATH = Path.home() / ".openclaw/cron/jobs.json"
RUNS_DIR = Path.home() / ".openclaw/cron/runs"
CANVAS_DIR = Path.home() / ".openclaw/canvas"
UI_DIR = Path("/app/dist/control-ui")
CACHE_DIR = Path(__file__).parent / ".cache"
DASHBOARD_CACHE = CACHE_DIR / "cron-dashboard.html"
DASHBOARD_URL = "https://raw.githubusercontent.com/firstfloris/opencron/master/cron-dashboard.html"


def fetch_template():
    """Download dashboard HTML from GitHub and cache locally."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    data = urllib.request.urlopen(DASHBOARD_URL).read()
    DASHBOARD_CACHE.write_bytes(data)
    return data.decode("utf-8")


def get_template():
    """Get cached template or fetch from GitHub."""
    if DASHBOARD_CACHE.exists():
        return DASHBOARD_CACHE.read_text("utf-8")
    return fetch_template()


def read_jobs():
    try:
        return json.loads(JOBS_PATH.read_text())
    except Exception:
        return {"jobs": []}


def read_runs(jobs):
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


def build_page(template=None):
    """Build complete HTML with embedded data."""
    if template is None:
        template = get_template()
    jobs = read_jobs()
    runs = read_runs(jobs)

    inject = (
        "<script>"
        "window.__OPENCRON_DATA=" + json.dumps(jobs) + ";"
        "window.__OPENCRON_RUNS=" + json.dumps(runs) + ";"
        "</script>"
    )
    return template.replace("</head>", inject + "</head>")


def deploy(html):
    """Write HTML to gateway UI dir and canvas dir."""
    if UI_DIR.exists():
        (UI_DIR / "cron.html").write_text(html, encoding="utf-8")

    CANVAS_DIR.mkdir(parents=True, exist_ok=True)
    (CANVAS_DIR / "cron.html").write_text(html, encoding="utf-8")
    (CANVAS_DIR / "cron-data.json").write_text(json.dumps(read_jobs()))


def main():
    import sys
    sync = "--sync" in sys.argv

    if sync:
        # Quick refresh: re-read data, use cached template
        deploy(build_page())
    else:
        # Full deploy: fetch latest HTML from GitHub
        print(f"Fetching dashboard from {DASHBOARD_URL}...")
        template = fetch_template()
        deploy(build_page(template))
        print(f"Dashboard deployed to /cron.html")


if __name__ == "__main__":
    main()
