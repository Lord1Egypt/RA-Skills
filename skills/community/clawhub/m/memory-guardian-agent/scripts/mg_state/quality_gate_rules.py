"""Rule helpers for quality gate degradation detection."""

from __future__ import annotations

from datetime import datetime, timedelta
from statistics import median

from mg_utils import CST


DEFAULT_QUIET_DEGRADATION_CONFIG = {
    "min_sample": 5,
    "relative_baseline_factor": 1.5,
    "baseline_window_days": 30,
    "seed_stale_days": 14,
}


def evaluate_quiet_degradation(samples, config=None, now=None, seed_last_updated_ts=None):
    """Evaluate quiet degradation using a relative baseline and minimum sample gate."""
    merged = dict(DEFAULT_QUIET_DEGRADATION_CONFIG)
    if config:
        merged.update(config)

    current_time = now or datetime.now(CST)
    current_window_days = merged["baseline_window_days"]
    baseline_cutoff = current_time - timedelta(days=current_window_days)

    def _parse_timestamp(entry):
        value = entry.get("timestamp")
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value)

    parsed = []
    for sample in samples:
        try:
            parsed.append((_parse_timestamp(sample), float(sample["archive_rate"])))
        except (KeyError, TypeError, ValueError):
            continue

    baseline_values = [value for ts, value in parsed if ts < baseline_cutoff]
    current_values = [value for ts, value in parsed if ts >= baseline_cutoff]
    if not baseline_values:
        baseline_values = [value for _, value in parsed]
    if not current_values:
        current_values = [value for _, value in parsed]

    sample_count = len(parsed)
    baseline_value = median(baseline_values) if baseline_values else 0.0
    current_value = median(current_values) if current_values else 0.0
    relative_floor = baseline_value / max(merged["relative_baseline_factor"], 1.0)

    seed_stale = False
    if seed_last_updated_ts:
        try:
            seed_updated = datetime.fromisoformat(seed_last_updated_ts)
            seed_stale = (current_time - seed_updated).days >= merged["seed_stale_days"]
        except (TypeError, ValueError):
            seed_stale = False

    degraded = (
        sample_count >= merged["min_sample"]
        and baseline_value > 0
        and current_value < relative_floor
    )

    return {
        "degraded": degraded,
        "sample_count": sample_count,
        "baseline_value": round(baseline_value, 4),
        "current_value": round(current_value, 4),
        "relative_floor": round(relative_floor, 4),
        "seed_stale": seed_stale,
        "config": merged,
    }
