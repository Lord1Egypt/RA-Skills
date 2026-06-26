"""Tests for mg_state.quality_gate_rules — quiet degradation evaluation."""

import pytest
from datetime import datetime, timedelta
from mg_state.quality_gate_rules import evaluate_quiet_degradation, DEFAULT_QUIET_DEGRADATION_CONFIG
from mg_utils import CST


def _sample(archive_rate, days_ago, timestamp=None):
    if timestamp is None:
        ts = (datetime.now(CST) - timedelta(days=days_ago)).isoformat()
    else:
        ts = timestamp
    return {"archive_rate": archive_rate, "timestamp": ts}


class TestEvaluateQuietDegradation:
    def test_empty_samples(self):
        result = evaluate_quiet_degradation([])
        assert result["degraded"] is False
        assert result["sample_count"] == 0

    def test_below_min_sample(self):
        samples = [_sample(0.5, 1) for _ in range(3)]
        result = evaluate_quiet_degradation(samples)
        assert result["degraded"] is False
        assert result["sample_count"] == 3

    def test_no_degradation_when_stable(self):
        # Baseline and current both around 0.5
        samples = [_sample(0.5, d) for d in [35, 30, 25, 20, 15, 5, 3, 1]]
        result = evaluate_quiet_degradation(samples)
        assert result["degraded"] is False

    def test_degradation_detected(self):
        # High baseline, low current
        samples = [_sample(0.8, d) for d in [35, 30, 25]] + [_sample(0.1, d) for d in [5, 3, 1]]
        result = evaluate_quiet_degradation(samples)
        assert result["degraded"] is True
        assert result["baseline_value"] > result["current_value"]

    def test_custom_config(self):
        samples = [_sample(0.5, d) for d in [1, 2, 3]]
        result = evaluate_quiet_degradation(samples, config={"min_sample": 2})
        assert result["sample_count"] == 3
        # min_sample=2 so degraded check should run (but not trigger since stable)

    def test_seed_stale_detection(self):
        from datetime import datetime, timedelta
        old_ts = (datetime.now(CST) - timedelta(days=20)).isoformat()
        samples = [_sample(0.5, 1)]
        result = evaluate_quiet_degradation(samples, seed_last_updated_ts=old_ts)
        assert result["seed_stale"] is True

    def test_seed_not_stale(self):
        from datetime import datetime
        recent_ts = datetime.now(CST).isoformat()
        samples = [_sample(0.5, 1)]
        result = evaluate_quiet_degradation(samples, seed_last_updated_ts=recent_ts)
        assert result["seed_stale"] is False

    def test_invalid_samples_skipped(self):
        samples = [
            {"archive_rate": "not_a_number", "timestamp": "2026-01-01"},
            {"archive_rate": 0.5},  # missing timestamp
            _sample(0.5, 1),
        ]
        result = evaluate_quiet_degradation(samples)
        assert result["sample_count"] == 1

    def test_datetime_timestamp_objects(self):
        samples = [
            {"archive_rate": 0.5, "timestamp": datetime.now(CST) - timedelta(days=1)},
        ]
        result = evaluate_quiet_degradation(samples)
        assert result["sample_count"] == 1

    def test_zero_baseline_never_degraded(self):
        samples = [_sample(0.0, d) for d in [30, 20, 10, 5, 1]]
        result = evaluate_quiet_degradation(samples)
        assert result["degraded"] is False
