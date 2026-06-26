#!/usr/bin/env python3
"""Normalize Fitbit daily raw bundle into Wellness-like fields.

Usage:
  python3 scripts/fitbit_normalize_daily.py raw.json --out fitbit_day.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any, Dict, Optional


def safe_get(d: Any, *keys):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = json.load(open(args.raw, "r", encoding="utf-8"))
    date = raw.get("requested_date")
    tz = raw.get("requested_tz")

    ep = raw.get("endpoints") or {}
    act = (ep.get("activity") or {}).get("data")
    slp = (ep.get("sleep") or {}).get("data")

    steps = safe_get(act, "summary", "steps")
    dist = None
    # Fitbit distance is in summary.distances list; pick "total" or first.
    distances = safe_get(act, "summary", "distances")
    if isinstance(distances, list) and distances:
        for x in distances:
            if isinstance(x, dict) and x.get("activity") == "total":
                dist = x.get("distance")
                break
        if dist is None and isinstance(distances[0], dict):
            dist = distances[0].get("distance")

    sleep_minutes = None
    sleep_score = None
    # Sleep response often contains a list of sleeps.
    sleeps = safe_get(slp, "sleep")
    if isinstance(sleeps, list) and sleeps:
        s0 = sleeps[0] if isinstance(sleeps[0], dict) else None
        if isinstance(s0, dict):
            sleep_minutes = s0.get("minutesAsleep")
            # score may be in s0['sleepScore']['overallScore'] depending on API.
            ss = s0.get("sleepScore")
            if isinstance(ss, dict):
                sleep_score = ss.get("overallScore") or ss.get("score")

    out: Dict[str, Any] = {
        "date": date,
        "timezone": tz,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "sleep": {
            "duration_minutes": sleep_minutes,
            "score": sleep_score,
            "source": "fitbit",
        },
        "activity": {
            "steps": steps,
            "distance_km": dist,
            "source": "fitbit",
        },
        "sources_present": ["fitbit"],
        "source": {"raw_files": [args.raw]},
    }

    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=2, sort_keys=True)
    open(args.out, "a", encoding="utf-8").write("\n")


if __name__ == "__main__":
    main()
