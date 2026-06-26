#!/usr/bin/env python3
"""Deploy the OpenCron dashboard to the OpenClaw canvas directory.

Copies cron_dashboard.html and writes live cron-data.json from jobs.json.

Usage:
    python3 skills/opencron/update_canvas.py
"""

import json
import urllib.request
from pathlib import Path

JOBS_PATH = Path.home() / ".openclaw/cron/jobs.json"
CANVAS_DIR = Path.home() / ".openclaw/canvas"
CANVAS_HTML = CANVAS_DIR / "cron.html"
CANVAS_JSON = CANVAS_DIR / "cron-data.json"
DASHBOARD_URL = "https://raw.githubusercontent.com/firstfloris/opencron/master/cron-dashboard.html"


def main():
    CANVAS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        data = json.loads(JOBS_PATH.read_text())
    except Exception as e:
        data = {"error": str(e), "jobs": []}

    print(f"Fetching dashboard from {DASHBOARD_URL}...")
    req = urllib.request.urlopen(DASHBOARD_URL)
    CANVAS_HTML.write_bytes(req.read())
    CANVAS_JSON.write_text(json.dumps(data))
    print(f"Deployed {CANVAS_HTML} + {CANVAS_JSON}")


if __name__ == "__main__":
    main()
