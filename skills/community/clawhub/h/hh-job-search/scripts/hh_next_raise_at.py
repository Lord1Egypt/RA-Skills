#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from hh_browser_cli import BrowserCli, BrowserCliError
from job_search_probe import read_resume_cards_js

HH_RESUMES_URL = "https://hh.ru/applicant/resumes"
TIME_RE = re.compile(r"Поднять в (\d{1,2}):(\d{2})")


def compute_next_iso(status_lines: list[str], tz_name: str, now: datetime | None = None) -> str | None:
    tz = ZoneInfo(tz_name)
    now = now or datetime.now(tz)
    candidates: list[datetime] = []
    for line in status_lines:
        m = TIME_RE.search(line or "")
        if not m:
            continue
        hour = int(m.group(1))
        minute = int(m.group(2))
        dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if dt <= now:
            dt += timedelta(days=1)
        dt += timedelta(minutes=5)
        candidates.append(dt)
    if not candidates:
        return None
    return min(candidates).isoformat()


def main() -> int:
    ap = argparse.ArgumentParser(description='Compute next HH resume raise time from current cooldowns')
    ap.add_argument('--profile', default='chrome-relay')
    ap.add_argument('--tz', default='Asia/Krasnoyarsk')
    args = ap.parse_args()

    browser = BrowserCli(profile=args.profile)
    result = {"ok": True}
    try:
        browser.ensure_ready()
        target_id = browser.current_target()
        browser.navigate_js(HH_RESUMES_URL, target_id)
        browser.wait_time(2200, target_id)
        cards = browser.evaluate(read_resume_cards_js(None), target_id, retries=2).result or []
        lines = [c.get('statusLine') or '' for c in cards]
        next_at = compute_next_iso(lines, args.tz)
        result.update({"resumes": cards, "nextAt": next_at})
    except BrowserCliError as e:
        result = {"ok": False, "error": str(e), "nextAt": None}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
