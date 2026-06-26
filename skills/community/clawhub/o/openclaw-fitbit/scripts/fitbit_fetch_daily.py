#!/usr/bin/env python3
"""Fetch Fitbit daily summaries (activity + sleep) for a local day.

Endpoints (typical):
- GET /1/user/-/activities/date/<date>.json
- GET /1.2/user/-/sleep/date/<date>.json

No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta
from typing import Any, Dict

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from fitbit_token import get_access_token


API_BASE = "https://api.fitbit.com"


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


def http_get_json(url: str, access_token: str) -> Any:
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="today|yesterday|YYYY-MM-DD")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tz", default=os.environ.get("FITBIT_TZ", "Asia/Shanghai"))
    args = ap.parse_args()

    day = resolve_date(args.date, args.tz)

    client_id = must_env("FITBIT_CLIENT_ID")
    client_secret = must_env("FITBIT_CLIENT_SECRET")
    access_token = get_access_token(client_id=client_id, client_secret=client_secret)

    act_url = f"{API_BASE}/1/user/-/activities/date/{day}.json"
    sleep_url = f"{API_BASE}/1.2/user/-/sleep/date/{day}.json"

    bundle: Dict[str, Any] = {
        "requested_date": day,
        "requested_tz": args.tz,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "api_base": API_BASE,
        "endpoints": {
            "activity": {"url": act_url, "data": http_get_json(act_url, access_token)},
            "sleep": {"url": sleep_url, "data": http_get_json(sleep_url, access_token)},
        },
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
