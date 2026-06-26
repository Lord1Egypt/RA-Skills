#!/usr/bin/env python3
"""Generate per-subject cron templates for reminders/assessment/curation."""

from __future__ import annotations
import argparse
import json
from pathlib import Path

TEMPLATES = {
    "light": {
        "morning": "30 7 * * 1-5",
        "evening": "0 20 * * 1-5",
        "curation": "0 10 * * 3",
        "weekly": "0 7 * * 1",
    },
    "standard": {
        "morning": "30 7 * * *",
        "evening": "0 20 * * *",
        "curation": "0 10 * * 3,6",
        "weekly": "0 7 * * 1",
    },
    "intensive": {
        "morning": "0 6 * * *",
        "evening": "30 21 * * *",
        "curation": "0 10 * * 2,4,6",
        "weekly": "0 7 * * 1",
    },
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--template", default="standard", choices=sorted(TEMPLATES.keys()))
    ap.add_argument("--workspace", default=str(Path.home() / ".openclaw" / "workspace"))
    ap.add_argument("--out", help="Optional output json path")
    args = ap.parse_args()

    t = TEMPLATES[args.template]
    w = Path(args.workspace)
    scripts = w / "skills" / "learning-coach" / "scripts"

    jobs = [
        {"name": f"{args.subject}:daily-morning", "cron": t["morning"], "cmd": f"python3 {scripts}/weekly_report.py --data-root {w}/data"},
        {"name": f"{args.subject}:daily-evening", "cron": t["evening"], "cmd": f"python3 {scripts}/weekly_report.py --data-root {w}/data"},
        {"name": f"{args.subject}:curation", "cron": t["curation"], "cmd": f"python3 {scripts}/weekly_report.py --data-root {w}/data"},
        {"name": f"{args.subject}:weekly", "cron": t["weekly"], "cmd": f"python3 {scripts}/weekly_report.py --data-root {w}/data"},
    ]

    payload = {"subject": args.subject, "template": args.template, "jobs": jobs}
    out = Path(args.out) if args.out else Path("/tmp") / f"learning-coach-{args.subject.replace(' ','-')}-cron.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
