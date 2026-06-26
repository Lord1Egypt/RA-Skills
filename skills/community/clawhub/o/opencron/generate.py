#!/usr/bin/env python3
"""Generate a standalone OpenCron HTML with embedded cron data.

Bakes jobs.json into the template so it works without a server.

Usage:
    python3 skills/opencron/generate.py                    # stdout
    python3 skills/opencron/generate.py -o dashboard.html  # file
"""

import argparse
import json
import sys
from pathlib import Path

JOBS_PATH = Path.home() / ".openclaw/cron/jobs.json"
TEMPLATE_PATH = Path(__file__).parent / "cron_dashboard.html"


def generate_html():
    try:
        data = json.loads(JOBS_PATH.read_text())
    except Exception as e:
        data = {"error": str(e), "jobs": []}

    html = TEMPLATE_PATH.read_text()
    # Inject data as window.__CRON_DATA__ for offline use
    inject = f"<script>window.__CRON_DATA__ = {json.dumps(data)};</script>"
    html = html.replace("</head>", f"{inject}\n</head>")
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate standalone OpenCron HTML")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    html = generate_html()
    if args.output:
        Path(args.output).write_text(html)
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(html)


if __name__ == "__main__":
    main()
