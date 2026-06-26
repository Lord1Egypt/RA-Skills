#!/usr/bin/env python3
"""Fetch Withings daily data bundle (measurements + sleep summary where available).

This script focuses on personal-user-accessible endpoints.

Env:
- WITHINGS_CLIENT_ID
- WITHINGS_CLIENT_SECRET
Optional:
- WITHINGS_TZ (default: Asia/Shanghai)

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
from typing import Any, Dict, Tuple

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from withings_token import get_access_token


API_BASE = "https://wbsapi.withings.net"


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


def api_post(action: str, params: Dict[str, str], access_token: str) -> Any:
    url = API_BASE + action
    body = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            time.sleep(5)
            return api_post(action, params, access_token)
        raise RuntimeError(f"HTTP {e.code} POST {url}: {raw}") from e


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="today|yesterday|YYYY-MM-DD")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tz", default=os.environ.get("WITHINGS_TZ", "Asia/Shanghai"))
    args = ap.parse_args()

    day = resolve_date(args.date, args.tz)
    start, end = day_range_epoch_utc(day, args.tz)

    client_id = must_env("WITHINGS_CLIENT_ID")
    client_secret = must_env("WITHINGS_CLIENT_SECRET")
    access_token = get_access_token(client_id=client_id, client_secret=client_secret)

    # Measure API (v1) - getmeas (for weight/body fat/BP/heart rate etc.)
    meas = api_post(
        "/measure",
        {
            "action": "getmeas",
            "startdate": str(start),
            "enddate": str(end),
            "category": "1",  # real measurements
        },
        access_token,
    )

    # Sleep v2 summary (best-effort)
    sleep_summary = None
    try:
        sleep_summary = api_post(
            "/v2/sleep",
            {
                "action": "getsummary",
                "startdate": str(start),
                "enddate": str(end),
            },
            access_token,
        )
    except Exception:
        sleep_summary = None

    bundle = {
        "requested_date": day,
        "requested_tz": args.tz,
        "range_utc_epoch": {"start": start, "end": end},
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "api_base": API_BASE,
        "measure": meas,
        "sleep_summary": sleep_summary,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
