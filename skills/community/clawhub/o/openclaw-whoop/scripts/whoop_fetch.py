#!/usr/bin/env python3
"""Fetch WHOOP data for a given day (with date filtering + pagination).

This script fetches WHOOP v2 collections using `start`, `end`, and `nextToken`
query params (per OpenAPI), and writes a raw bundle.

Downstream normalization converts the raw bundle into a stable daily schema.

Requires env:
- WHOOP_CLIENT_ID
- WHOOP_CLIENT_SECRET

Optional env:
- WHOOP_TOKEN_PATH
- WHOOP_TZ (default: Asia/Shanghai)

Usage:
  python3 scripts/whoop_fetch.py --date today|yesterday|YYYY-MM-DD --out /tmp/whoop_raw.json

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
from typing import Any, Dict, Optional, Tuple

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from whoop_token import get_access_token


API_BASE = "https://api.prod.whoop.com/developer"


def must_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        print(f"Missing env var: {name}", file=sys.stderr)
        sys.exit(2)
    return v


def http_get_json(url: str, access_token: str) -> Any:
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        # Basic 429 handling
        if e.code == 429:
            ra = e.headers.get("Retry-After")
            if ra:
                try:
                    time.sleep(int(ra))
                    return http_get_json(url, access_token)
                except Exception:
                    pass
        raise RuntimeError(f"HTTP {e.code} GET {url}: {raw}") from e


def resolve_date(s: str, tz_name: str) -> str:
    s = s.strip().lower()
    tz = _tzinfo(tz_name)
    now = datetime.now(tz)
    if s == "today":
        return now.strftime("%Y-%m-%d")
    if s == "yesterday":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    # assume YYYY-MM-DD
    datetime.strptime(s, "%Y-%m-%d")
    return s


def _tzinfo(tz_name: str):
    if ZoneInfo is None:
        return timezone.utc
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return timezone.utc


def day_range_utc(date_yyyy_mm_dd: str, tz_name: str) -> Tuple[str, str]:
    """Return (start,end) in UTC ISO-8601 with Z, covering the local day."""
    tz = _tzinfo(tz_name)
    d = datetime.strptime(date_yyyy_mm_dd, "%Y-%m-%d")
    start_local = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=tz)
    end_local = datetime(d.year, d.month, d.day, 23, 59, 59, tzinfo=tz)
    start_utc = start_local.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    end_utc = end_local.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return start_utc, end_utc


def url_with_params(path: str, params: Optional[Dict[str, str]] = None) -> str:
    url = API_BASE.rstrip("/") + "/" + path.lstrip("/")
    if params:
        # Keep None out of the query string.
        params2 = {k: v for k, v in params.items() if v is not None}
        return url + "?" + urllib.parse.urlencode(params2)
    return url


def fetch_collection(
    *,
    path: str,
    access_token: str,
    start: str,
    end: str,
    limit: int,
    max_pages: int,
) -> Dict[str, Any]:
    """Fetch a paginated WHOOP collection endpoint using nextToken."""
    records = []
    next_token = None
    pages = 0
    last_url = None

    while True:
        pages += 1
        if pages > max_pages:
            break

        params = {
            "limit": str(limit),
            "start": start,
            "end": end,
        }
        if next_token:
            params["nextToken"] = next_token

        url = url_with_params(path, params)
        last_url = url
        data = http_get_json(url, access_token)

        # Common response patterns: {records:[], nextToken:"..."}
        if isinstance(data, dict):
            recs = data.get("records") or data.get("data") or data.get("items") or []
            if isinstance(recs, list):
                records.extend([r for r in recs if isinstance(r, dict)])
            next_token = data.get("nextToken") or data.get("next_token")
        elif isinstance(data, list):
            records.extend([r for r in data if isinstance(r, dict)])
            next_token = None
        else:
            next_token = None

        if not next_token:
            break

    return {
        "url": last_url,
        "pages": pages,
        "start": start,
        "end": end,
        "limit": limit,
        "records": records,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="today|yesterday|YYYY-MM-DD")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tz", default=os.environ.get("WHOOP_TZ", "Asia/Shanghai"))
    ap.add_argument("--limit", type=int, default=50, help="page size for collection endpoints")
    ap.add_argument("--max-pages", type=int, default=10, help="safety cap for pagination")
    args = ap.parse_args()

    day = resolve_date(args.date, args.tz)
    start, end = day_range_utc(day, args.tz)

    client_id = must_env("WHOOP_CLIENT_ID")
    client_secret = must_env("WHOOP_CLIENT_SECRET")

    access_token = get_access_token(client_id=client_id, client_secret=client_secret)

    bundle: Dict[str, Any] = {
        "requested_date": day,
        "requested_tz": args.tz,
        "range_utc": {"start": start, "end": end},
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "api_base": API_BASE,
        "endpoints": {},
    }

    # Non-collection endpoints
    bundle["endpoints"]["profile_basic"] = {
        "url": url_with_params("/v2/user/profile/basic"),
        "data": http_get_json(url_with_params("/v2/user/profile/basic"), access_token),
    }
    bundle["endpoints"]["body_measurement"] = {
        "url": url_with_params("/v2/user/measurement/body"),
        "data": http_get_json(url_with_params("/v2/user/measurement/body"), access_token),
    }

    # Collections with date filtering + pagination
    collections = {
        "recovery": "/v2/recovery",
        "sleep": "/v2/activity/sleep",
        "cycle": "/v2/cycle",
        "workout": "/v2/activity/workout",
    }

    for key, path in collections.items():
        bundle["endpoints"][key] = fetch_collection(
            path=path,
            access_token=access_token,
            start=start,
            end=end,
            limit=args.limit,
            max_pages=args.max_pages,
        )

    out_path = args.out
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
