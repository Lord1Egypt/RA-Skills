#!/usr/bin/env python3
"""Fetch Strava athlete activities for a day (UTC-filtered) and write raw JSON.

Uses:
- GET https://www.strava.com/api/v3/athlete/activities?after=...&before=...&page=...&per_page=...

Env:
- STRAVA_CLIENT_ID
- STRAVA_CLIENT_SECRET
Optional:
- STRAVA_TZ (default: Asia/Shanghai)

No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from strava_token import get_access_token


API_BASE = "https://www.strava.com/api/v3"


def must_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(2)
    return v


def _tzinfo(tz_name: str):
    if ZoneInfo is None:
        return timezone.utc
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return timezone.utc


def resolve_date(s: str, tz_name: str) -> str:
    s = s.strip().lower()
    tz = _tzinfo(tz_name)
    now = datetime.now(tz)
    if s == "today":
        return now.strftime("%Y-%m-%d")
    if s == "yesterday":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    datetime.strptime(s, "%Y-%m-%d")
    return s


def day_range_epoch_utc(date_yyyy_mm_dd: str, tz_name: str) -> Tuple[int, int]:
    tz = _tzinfo(tz_name)
    d = datetime.strptime(date_yyyy_mm_dd, "%Y-%m-%d")
    start_local = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=tz)
    end_local = datetime(d.year, d.month, d.day, 23, 59, 59, tzinfo=tz)
    start_utc = int(start_local.astimezone(timezone.utc).timestamp())
    end_utc = int(end_local.astimezone(timezone.utc).timestamp())
    return start_utc, end_utc


def http_get_json(url: str, access_token: str) -> Any:
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            time.sleep(5)
            return http_get_json(url, access_token)
        raise RuntimeError(f"HTTP {e.code} GET {url}: {raw}") from e


def fetch_activities(*, access_token: str, after: int, before: int, per_page: int, max_pages: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    page = 1
    while page <= max_pages:
        params = {
            "after": str(after),
            "before": str(before),
            "page": str(page),
            "per_page": str(per_page),
        }
        url = API_BASE + "/athlete/activities?" + urllib.parse.urlencode(params)
        data = http_get_json(url, access_token)
        if not isinstance(data, list) or not data:
            break
        out.extend([x for x in data if isinstance(x, dict)])
        if len(data) < per_page:
            break
        page += 1
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="today|yesterday|YYYY-MM-DD")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tz", default=os.environ.get("STRAVA_TZ", "Asia/Shanghai"))
    ap.add_argument("--per-page", type=int, default=50)
    ap.add_argument("--max-pages", type=int, default=10)
    args = ap.parse_args()

    day = resolve_date(args.date, args.tz)
    after, before = day_range_epoch_utc(day, args.tz)

    client_id = must_env("STRAVA_CLIENT_ID")
    client_secret = must_env("STRAVA_CLIENT_SECRET")

    access_token = get_access_token(client_id=client_id, client_secret=client_secret)
    acts = fetch_activities(
        access_token=access_token,
        after=after,
        before=before,
        per_page=args.per_page,
        max_pages=args.max_pages,
    )

    bundle = {
        "requested_date": day,
        "requested_tz": args.tz,
        "range_utc_epoch": {"after": after, "before": before},
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "api_base": API_BASE,
        "activities": acts,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
