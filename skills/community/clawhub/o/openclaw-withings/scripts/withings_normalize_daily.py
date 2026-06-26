#!/usr/bin/env python3
"""Normalize Withings raw bundle into a daily summary for the Wellness hub.

Maps common Withings measure type IDs.

Usage:
  python3 scripts/withings_normalize_daily.py raw.json --out withings_day.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


# Withings measure type IDs (common)
# Source: Withings docs (Measure - Getmeas)
TYPE_WEIGHT = 1
TYPE_FAT_RATIO = 6
TYPE_FAT_MASS = 8
TYPE_DIASTOLIC = 9
TYPE_SYSTOLIC = 10
TYPE_HEART_PULSE = 11


def meas_value(m: Dict[str, Any]) -> Optional[float]:
    try:
        v = float(m.get("value"))
        u = int(m.get("unit"))
        return v * (10 ** u)
    except Exception:
        return None


def pick_latest(measuregrps: List[Dict[str, Any]], type_id: int) -> Optional[Tuple[int, float]]:
    best = None
    for g in measuregrps:
        if not isinstance(g, dict):
            continue
        ts = g.get("date")
        try:
            ts_i = int(ts)
        except Exception:
            continue
        measures = g.get("measures")
        if not isinstance(measures, list):
            continue
        for m in measures:
            if not isinstance(m, dict):
                continue
            if m.get("type") != type_id:
                continue
            val = meas_value(m)
            if val is None:
                continue
            if best is None or ts_i > best[0]:
                best = (ts_i, val)
    return best


def normalize_sleep_minutes(sleep_summary: Any) -> Dict[str, Any]:
    # Keep best-effort; Withings sleep summary shapes may evolve.
    if not isinstance(sleep_summary, dict):
        return {"duration_minutes": None, "score": None}
    body = sleep_summary.get("body")
    if not isinstance(body, dict):
        return {"duration_minutes": None, "score": None}

    # Try a few common keys
    series = body.get("series")
    if isinstance(series, list) and series:
        # pick first item
        s0 = series[0] if isinstance(series[0], dict) else None
        if isinstance(s0, dict):
            dur = s0.get("data", {}).get("total_sleep_time") if isinstance(s0.get("data"), dict) else None
            try:
                if dur is not None:
                    return {"duration_minutes": int(round(float(dur) / 60.0)), "score": None}
            except Exception:
                pass

    return {"duration_minutes": None, "score": None}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = json.load(open(args.raw, "r", encoding="utf-8"))
    date = raw.get("requested_date")
    tz = raw.get("requested_tz")

    meas = raw.get("measure")
    mg = []
    if isinstance(meas, dict):
        body = meas.get("body")
        if isinstance(body, dict) and isinstance(body.get("measuregrps"), list):
            mg = body.get("measuregrps")

    latest_weight = pick_latest(mg, TYPE_WEIGHT)
    latest_fat_ratio = pick_latest(mg, TYPE_FAT_RATIO)
    latest_sys = pick_latest(mg, TYPE_SYSTOLIC)
    latest_dia = pick_latest(mg, TYPE_DIASTOLIC)
    latest_hr = pick_latest(mg, TYPE_HEART_PULSE)

    sleep = normalize_sleep_minutes(raw.get("sleep_summary"))

    out: Dict[str, Any] = {
        "date": date,
        "timezone": tz,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "sleep": {
            "duration_minutes": sleep.get("duration_minutes"),
            "score": sleep.get("score"),
            "source": "withings",
        },
        "body": {
            "weight_kg": latest_weight[1] if latest_weight else None,
            "body_fat_percent": (latest_fat_ratio[1] * 100.0) if latest_fat_ratio else None,
            "source": "withings",
        },
        "vitals": {
            "bp_systolic": int(round(latest_sys[1])) if latest_sys else None,
            "bp_diastolic": int(round(latest_dia[1])) if latest_dia else None,
            "resting_hr_bpm": int(round(latest_hr[1])) if latest_hr else None,
            "source": "withings",
        },
        "sources_present": ["withings"],
        "source": {"raw_files": [args.raw]},
    }

    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=2, sort_keys=True)
    open(args.out, "a", encoding="utf-8").write("\n")


if __name__ == "__main__":
    main()
