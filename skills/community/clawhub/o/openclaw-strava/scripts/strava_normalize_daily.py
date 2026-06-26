#!/usr/bin/env python3
"""Normalize Strava raw activities bundle into a simple daily summary.

Keeps a stable contract for the Wellness hub.

Usage:
  python3 scripts/strava_normalize_daily.py raw.json --out strava_day.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any, Dict, List, Optional


def activity_type(a: Dict[str, Any]) -> str:
    t = a.get("type")
    if isinstance(t, str) and t:
        return t.lower()
    return "workout"


def to_minutes(seconds: Any) -> Optional[int]:
    try:
        if seconds is None:
            return None
        return int(round(float(seconds) / 60.0))
    except Exception:
        return None


def to_km(meters: Any) -> Optional[float]:
    try:
        if meters is None:
            return None
        return float(meters) / 1000.0
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", help="raw bundle from strava_fetch_activities.py")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = json.load(open(args.raw, "r", encoding="utf-8"))
    date = raw.get("requested_date")
    tz = raw.get("requested_tz")
    acts = raw.get("activities")

    workouts: List[Dict[str, Any]] = []
    if isinstance(acts, list):
        for a in acts:
            if not isinstance(a, dict):
                continue
            workouts.append(
                {
                    "start": a.get("start_date"),
                    "end": None,
                    "type": activity_type(a),
                    "duration_minutes": to_minutes(a.get("elapsed_time")),
                    "distance_km": to_km(a.get("distance")),
                    "calories_kcal": a.get("calories"),
                    "avg_hr_bpm": a.get("average_heartrate"),
                    "max_hr_bpm": a.get("max_heartrate"),
                    "source": "strava",
                }
            )

    out: Dict[str, Any] = {
        "date": date,
        "timezone": tz,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "training": {
            "workouts": workouts,
            "source": "strava",
        },
        "sources_present": ["strava"],
        "source": {"raw_files": [args.raw]},
    }

    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=2, sort_keys=True)
    open(args.out, "a", encoding="utf-8").write("\n")


if __name__ == "__main__":
    main()
