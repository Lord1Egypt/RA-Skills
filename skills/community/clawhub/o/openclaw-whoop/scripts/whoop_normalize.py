#!/usr/bin/env python3
"""Normalize raw WHOOP bundle into a stable daily summary schema.

Heuristic: pick the first item in each collection whose date best matches the
requested date. Keep it conservative; downstream prompts should rely on this
schema rather than WHOOP's raw shapes.

Usage:
  python3 scripts/whoop_normalize.py raw.json --out whoop.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


def parse_iso(dt: str) -> Optional[datetime]:
    if not dt or not isinstance(dt, str):
        return None
    # Accept trailing Z
    s = dt.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def whoop_time_bounds(obj: Dict[str, Any]) -> Optional[tuple[Optional[datetime], Optional[datetime]]]:
    """Return (start,end) datetimes when available.

    Based on WHOOP v2 schemas:
    - Sleep/Cycle/WorkoutV2 expose `start` and `end`.
    - Recovery exposes `created_at`/`updated_at` (no start/end).
    """
    if not isinstance(obj, dict):
        return None

    start = parse_iso(obj.get("start"))
    end = parse_iso(obj.get("end"))

    if start or end:
        return start, end

    created = parse_iso(obj.get("created_at"))
    updated = parse_iso(obj.get("updated_at"))
    if created or updated:
        return created, updated

    return None


def in_range(dt: Optional[datetime], start: Optional[datetime], end: Optional[datetime]) -> bool:
    if dt is None or start is None or end is None:
        return False
    return start <= dt <= end


def overlaps_range(
    start_end: Optional[tuple[Optional[datetime], Optional[datetime]]],
    range_start: Optional[datetime],
    range_end: Optional[datetime],
) -> bool:
    if not start_end or range_start is None or range_end is None:
        return False
    s, e = start_end
    if s and e:
        return not (e < range_start or s > range_end)
    if s:
        return range_start <= s <= range_end
    if e:
        return range_start <= e <= range_end
    return False


def pick_best_for_range(items: Any, range_start: Optional[datetime], range_end: Optional[datetime]) -> Optional[Dict[str, Any]]:
    if not isinstance(items, list) or not items:
        return None

    # Prefer overlap with the requested UTC day-range.
    for it in items:
        if isinstance(it, dict) and overlaps_range(whoop_time_bounds(it), range_start, range_end):
            return it

    # Fallback: first dict item.
    for it in items:
        if isinstance(it, dict):
            return it
    return None


def get_collection(data: Any) -> Any:
    # Common patterns in APIs: {"records": [...]}, {"data": [...]}, or direct list
    if isinstance(data, dict):
        for k in ("records", "data", "items"):
            if k in data and isinstance(data[k], list):
                return data[k]
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", help="path to raw bundle JSON")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tz", default=None, help="IANA timezone label (stored only; no conversion here)")
    args = ap.parse_args()

    raw = json.load(open(args.raw, "r", encoding="utf-8"))
    requested_date = raw.get("requested_date")
    tz = args.tz or raw.get("requested_tz") or "Asia/Shanghai"

    endpoints = raw.get("endpoints", {})

    prof = endpoints.get("profile_basic", {}).get("data") or {}
    meas = endpoints.get("body_measurement", {}).get("data") or {}

    # whoop_fetch stores collections as {records:[...]} in endpoints.<key>.records
    rec_items = endpoints.get("recovery", {}).get("records")
    slp_items = endpoints.get("sleep", {}).get("records")
    cyc_items = endpoints.get("cycle", {}).get("records")
    wko_items = endpoints.get("workout", {}).get("records")

    # Backward compatibility if a raw bundle came from an older script version:
    if rec_items is None:
        rec_items = get_collection(endpoints.get("recovery", {}).get("data"))
    if slp_items is None:
        slp_items = get_collection(endpoints.get("sleep", {}).get("data"))
    if cyc_items is None:
        cyc_items = get_collection(endpoints.get("cycle", {}).get("data"))
    if wko_items is None:
        wko_items = get_collection(endpoints.get("workout", {}).get("data"))

    # Parse the requested UTC range (produced by whoop_fetch.py)
    rng = raw.get("range_utc") or {}
    range_start = parse_iso(rng.get("start")) if isinstance(rng, dict) else None
    range_end = parse_iso(rng.get("end")) if isinstance(rng, dict) else None

    best_rec = pick_best_for_range(rec_items, range_start, range_end)
    best_slp = pick_best_for_range(slp_items, range_start, range_end)
    best_cyc = pick_best_for_range(cyc_items, range_start, range_end)

    # Workout: summarize for the requested range.
    wkos = [w for w in wko_items if isinstance(w, dict)] if isinstance(wko_items, list) else []
    wkos_for_range = [w for w in wkos if overlaps_range(whoop_time_bounds(w), range_start, range_end)]

    def workout_strain(workout: Dict[str, Any]) -> Optional[float]:
        # WorkoutV2.score is an object; strain is typically nested.
        sc = workout.get("score")
        if isinstance(sc, dict):
            for k in ("strain", "activity_strain"):
                if k in sc:
                    try:
                        return float(sc.get(k))
                    except Exception:
                        return None
        for k in ("strain", "activity_strain"):
            if k in workout:
                try:
                    return float(workout.get(k))
                except Exception:
                    return None
        return None

    top_strain = None
    for w in (wkos_for_range or wkos):
        s = workout_strain(w)
        if s is None:
            continue
        top_strain = s if top_strain is None else max(top_strain, s)

    out: Dict[str, Any] = {
        "date": requested_date,
        "timezone": tz,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "profile": {
            "name": prof.get("name") or prof.get("full_name"),
            "email": prof.get("email"),
        },
        "recovery": {
            "score": (best_rec or {}).get("score"),
            "hrv_ms": (best_rec or {}).get("hrv_ms") or (best_rec or {}).get("hrv"),
            "rhr_bpm": (best_rec or {}).get("resting_heart_rate") or (best_rec or {}).get("rhr"),
        },
        "sleep": {
            "duration_minutes": (best_slp or {}).get("duration") or (best_slp or {}).get("duration_minutes"),
            "performance_percent": (best_slp or {}).get("performance") or (best_slp or {}).get("performance_percent"),
        },
        "cycle": {
            "strain": (best_cyc or {}).get("strain"),
            "avg_hr_bpm": (best_cyc or {}).get("average_heart_rate") or (best_cyc or {}).get("avg_heart_rate"),
        },
        "workout": {
            "count": len(wkos_for_range) if (range_start and range_end) else len(wkos),
            "top_strain": top_strain,
        },
        "source": {
            "whoop": {
                "api_base": raw.get("api_base"),
                "raw_files": [args.raw],
            }
        },
    }

    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=2, sort_keys=True)
    open(args.out, "a", encoding="utf-8").write("\n")


if __name__ == "__main__":
    main()
