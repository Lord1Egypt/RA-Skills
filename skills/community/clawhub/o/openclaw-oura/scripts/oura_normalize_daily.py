#!/usr/bin/env python3
"""Normalize Oura raw bundle into Wellness-like daily fields.

Best-effort mapping: pick first record matching requested_date.

Usage:
  python3 scripts/oura_normalize_daily.py raw.json --out oura_day.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any, Dict, Optional


def pick_record(data: Any, requested_date: str) -> Optional[Dict[str, Any]]:
    if not isinstance(data, dict):
        return None
    recs = data.get("data")
    if not isinstance(recs, list):
        return None
    for r in recs:
        if isinstance(r, dict) and (r.get("day") == requested_date or r.get("summary_date") == requested_date):
            return r
    for r in recs:
        if isinstance(r, dict):
            return r
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = json.load(open(args.raw, "r", encoding="utf-8"))
    date = raw.get("requested_date")
    tz = raw.get("requested_tz")

    ep = raw.get("endpoints") or {}
    sleep = pick_record(((ep.get("sleep") or {}).get("data")), date)
    readiness = pick_record(((ep.get("readiness") or {}).get("data")), date)
    activity = pick_record(((ep.get("activity") or {}).get("data")), date)

    out: Dict[str, Any] = {
        "date": date,
        "timezone": tz,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "sleep": {
            "duration_minutes": (sleep or {}).get("total_sleep_duration") if sleep else None,
            "efficiency": (sleep or {}).get("efficiency") if sleep else None,
            "score": (sleep or {}).get("score") if sleep else None,
            "source": "oura",
        },
        "recovery": {
            "score": (readiness or {}).get("score") if readiness else None,
            "source": "oura",
        },
        "activity": {
            "steps": (activity or {}).get("steps") if activity else None,
            "active_calories_kcal": (activity or {}).get("active_calories") if activity else None,
            "source": "oura",
        },
        "sources_present": ["oura"],
        "source": {"raw_files": [args.raw]},
    }

    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=2, sort_keys=True)
    open(args.out, "a", encoding="utf-8").write("\n")


if __name__ == "__main__":
    main()
