#!/usr/bin/env python3
"""Fetch Oura v2 daily data (sleep, readiness, activity) for a local day.

Auth: Personal Access Token (OURA_ACCESS_TOKEN).

No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


API_BASE = "https://api.ouraring.com/v2"


def must_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(2)
    return v


def _tzinfo(tz_name: str):
    if ZoneInfo is None:
        return None
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return None


def resolve_date(s: str, tz_name: str) -> str:
    s = s.strip().lower()
    tz = _tzinfo(tz_name)
    now = datetime.now(tz) if tz else datetime.now()
    if s == "today":
        return now.strftime("%Y-%m-%d")
    if s == "yesterday":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    datetime.strptime(s, "%Y-%m-%d")
    return s


def day_range(date_yyyy_mm_dd: str) -> Tuple[str, str]:
    # Oura v2 endpoints commonly accept start_date/end_date as YYYY-MM-DD.
    # end_date is typically inclusive; to be safe, we query [date, date].
    return date_yyyy_mm_dd, date_yyyy_mm_dd


def http_get_json(url: str, token: str) -> Any:
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} GET {url}: {raw}") from e


def fetch_collection(path: str, token: str, start_date: str, end_date: str) -> Any:
    params = {"start_date": start_date, "end_date": end_date}
    url = API_BASE + path + "?" + urllib.parse.urlencode(params)
    return {"url": url, "data": http_get_json(url, token)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="today|yesterday|YYYY-MM-DD")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tz", default=os.environ.get("OURA_TZ", "Asia/Shanghai"))
    args = ap.parse_args()

    token = must_env("OURA_ACCESS_TOKEN")
    day = resolve_date(args.date, args.tz)
    start_date, end_date = day_range(day)

    bundle: Dict[str, Any] = {
        "requested_date": day,
        "requested_tz": args.tz,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "api_base": API_BASE,
        "endpoints": {
            "sleep": fetch_collection("/usercollection/sleep", token, start_date, end_date),
            "readiness": fetch_collection("/usercollection/readiness", token, start_date, end_date),
            "activity": fetch_collection("/usercollection/daily_activity", token, start_date, end_date),
        },
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
