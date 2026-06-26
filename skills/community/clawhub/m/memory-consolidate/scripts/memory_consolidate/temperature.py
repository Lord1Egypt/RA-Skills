"""Temperature, decay, reinforcement, and priority scoring."""

from __future__ import annotations

import datetime as dt
import math
import re
from typing import Any, Dict, List, Tuple

from .core import parse_iso_utc, normalize_for_match, char_ngrams, is_reference_match


def count_recent_references(content: str, corpus: List[str]) -> int:
    target = normalize_for_match(content)
    if len(target) < 12:
        return 0
    count = 0
    for line in corpus:
        if is_reference_match(target, line):
            count += 1
    return count


def infer_priority_score(item: Dict[str, Any]) -> float:
    explicit = str(item.get("priority") or "").strip().lower()
    mapping = {
        "core": 1.0,
        "high": 1.0,
        "important": 0.5,
        "medium": 0.5,
        "low": 0.0,
        "reference": 0.0,
        "🔴": 1.0,
        "🟡": 0.5,
        "⚪": 0.0,
    }
    if explicit in mapping:
        return float(mapping[explicit])

    event_type = str(item.get("event_type") or "")
    if event_type in {"decision", "progress"}:
        return 1.0
    if event_type in {"solution", "issue", "artifact"}:
        return 0.5

    imp = float(item.get("importance") or 0.5)
    if imp >= 0.85:
        return 1.0
    if imp >= 0.7:
        return 0.5
    return 0.0


def compute_temperature(item: Dict[str, Any], now: dt.datetime, corpus: List[str], cfg: Dict[str, Any]) -> Dict[str, Any]:
    created_at = item.get("created_at") or item.get("updated_at")
    try:
        created_dt = dt.datetime.fromisoformat(str(created_at).replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except Exception:
        created_dt = now

    # Fall back to source filename date if created_at looks newer than source
    sources = item.get("sources") or []
    if not sources and item.get("source"):
        sources = [item["source"]]
    for s in sources:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", str(s))
        if m:
            try:
                src_dt = dt.datetime.fromisoformat(m.group(1) + "T00:00:00+00:00")
                if src_dt < created_dt:
                    created_dt = src_dt
                    item["created_at"] = m.group(1) + "T00:00:00Z"
            except Exception:
                pass
            break

    age_days = max(0.0, (now - created_dt).total_seconds() / 86400.0)
    age_lambda = float(cfg.get("age_lambda", 0.03))
    age_score = math.exp(-age_lambda * age_days)

    refs = count_recent_references(str(item.get("content") or ""), corpus)
    ref_cap = max(1, int(cfg.get("ref_cap", 3)))
    ref_score = min(1.0, refs / ref_cap)

    pri_score = infer_priority_score(item)

    w_age = float(cfg.get("w_age", 0.5))
    w_ref = float(cfg.get("w_ref", 0.3))
    w_pri = float(cfg.get("w_pri", 0.2))

    temp = (w_age * age_score) + (w_ref * ref_score) + (w_pri * pri_score)
    temp = float(min(1.0, max(0.0, temp)))

    hot_threshold = float(cfg.get("hot_threshold", 0.7))
    warm_threshold = float(cfg.get("warm_threshold", 0.3))
    if temp > hot_threshold:
        bucket = "hot"
    elif temp > warm_threshold:
        bucket = "warm"
    else:
        bucket = "cold"

    item["age_days"] = round(age_days, 2)
    item["recent_refs"] = refs
    item["priority_score"] = pri_score
    item["temperature"] = round(temp, 4)
    item["temperature_bucket"] = bucket
    item["weight"] = temp
    return item


def apply_temperature(rows: List[Dict[str, Any]], now: dt.datetime, corpus: List[str], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [compute_temperature(r, now, corpus, cfg) for r in rows]


def apply_decay(item: Dict[str, Any], rate: float, now: dt.datetime) -> Dict[str, Any]:
    updated_at = item.get("updated_at") or item.get("created_at")
    try:
        t = dt.datetime.fromisoformat(str(updated_at).replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except Exception:
        t = now
    days = max(0.0, (now - t).total_seconds() / 86400.0)
    importance = float(item.get("importance") or 0.5)
    actual_rate = rate * (1.0 - min(1.0, importance) * 0.5)
    w0 = float(item.get("weight") or 1.0)
    w = w0 * math.exp(-actual_rate * days)
    item["weight"] = float(max(0.0, w))
    return item


def apply_usage_reinforcement(
    rows: List[Dict[str, Any]],
    now: dt.datetime,
    cfg: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], int]:
    if not bool(cfg.get("enabled", True)):
        return rows, 0

    cooldown_hours = float(cfg.get("cooldown_hours", 18))
    boost_per_ref = float(cfg.get("boost_per_ref", 0.03))
    max_boost = float(cfg.get("max_boost", 0.12))
    now_iso = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    reinforced = 0
    out: List[Dict[str, Any]] = []

    for row in rows:
        refs = int(row.get("recent_refs") or 0)
        if refs <= 0:
            out.append(row)
            continue

        last_reinforced = parse_iso_utc(row.get("last_reinforced_at"), fallback=dt.datetime.fromtimestamp(0, tz=dt.timezone.utc))
        hours_since = (now - last_reinforced).total_seconds() / 3600.0
        if hours_since < cooldown_hours:
            out.append(row)
            continue

        bonus = min(max_boost, refs * boost_per_ref)
        row["temperature"] = round(min(1.0, float(row.get("temperature") or row.get("weight") or 0.0) + bonus), 4)
        row["weight"] = float(row["temperature"])
        row["confidence"] = round(min(1.0, float(row.get("confidence") or 0.0) + bonus * 0.45), 4)
        row["importance"] = round(min(1.0, float(row.get("importance") or 0.5) + min(0.12, bonus * 0.6)), 4)
        row["usage_hits"] = int(row.get("usage_hits") or 0) + refs
        row["last_reinforced_at"] = now_iso
        row["updated_at"] = now_iso
        row["last_seen_at"] = now_iso

        reinforced += 1
        out.append(row)

    return out, reinforced
