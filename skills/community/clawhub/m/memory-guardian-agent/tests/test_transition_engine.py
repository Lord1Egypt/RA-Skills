"""Tests for mg_state.transition_engine — anomaly mode state transitions."""

import pytest
from mg_state.transition_engine import (
    ANOMALY_MODE_NORMAL,
    ANOMALY_MODE_ANOMALY,
    ANOMALY_MODE_ERROR_RECOVERY,
    update_anomaly_mode_state,
    auto_heal_anomaly_mode,
)


def _make_meta(mode=ANOMALY_MODE_NORMAL):
    return {"anomaly_mode": mode}


def _make_gate(state="NORMAL", consecutive_clean=0):
    return {"state": state, "consecutive_clean": consecutive_clean}


class TestUpdateAnomalyModeState:
    def test_stays_normal_when_healthy(self):
        meta = _make_meta()
        gate = _make_gate()
        result = update_anomaly_mode_state(meta, gate, passed=True, trigger=None)
        assert result["mode"] == ANOMALY_MODE_NORMAL
        assert "anomaly_mode_reason" not in meta

    def test_transitions_to_anomaly_on_trigger(self):
        meta = _make_meta()
        meta["anomaly_count"] = 2  # Need ≥2 consecutive anomalies (Bug 4 fix)
        gate = _make_gate()
        # Simulate 6 failures out of 10 to satisfy failure thresholds
        meta["quality_gate_state"] = {
            "check_history": [{"passed": False}] * 6 + [{"passed": True}] * 4
        }
        result = update_anomaly_mode_state(meta, gate, passed=False, trigger="anomaly")
        assert result["mode"] == ANOMALY_MODE_ANOMALY
        assert meta["anomaly_mode_entered_at"] is not None
        assert meta["anomaly_mode_reason"] != ""

    def test_transitions_to_anomaly_on_high_failure_rate(self):
        meta = _make_meta()
        meta["anomaly_count"] = 2  # Need ≥2 consecutive anomalies (Bug 4 fix)
        gate = _make_gate()
        # Simulate 6 failures out of 10
        meta["quality_gate_state"] = {
            "check_history": [{"passed": False}] * 6 + [{"passed": True}] * 4
        }
        result = update_anomaly_mode_state(meta, gate, passed=False, trigger=None)
        assert result["mode"] == ANOMALY_MODE_ANOMALY

    def test_transitions_to_anomaly_on_5_failures(self):
        meta = _make_meta()
        meta["anomaly_count"] = 2  # Need ≥2 consecutive anomalies (Bug 4 fix)
        gate = _make_gate()
        meta["quality_gate_state"] = {
            "check_history": [{"passed": False}] * 5 + [{"passed": True}] * 5
        }
        result = update_anomaly_mode_state(meta, gate, passed=False, trigger=None)
        assert result["mode"] == ANOMALY_MODE_ANOMALY

    def test_anomaly_to_error_recovery_on_critical(self):
        meta = _make_meta(ANOMALY_MODE_ANOMALY)
        meta["anomaly_mode_entered_at"] = "2026-01-01T00:00:00+08:00"
        meta["anomaly_mode_reason"] = "test"
        gate = _make_gate(state="CRITICAL")
        result = update_anomaly_mode_state(meta, gate, passed=False, trigger=None)
        assert result["mode"] == ANOMALY_MODE_ERROR_RECOVERY
        assert result["reason"] == "CRITICAL state entered"

    def test_anomaly_to_normal_after_recovery(self):
        meta = _make_meta(ANOMALY_MODE_ANOMALY)
        meta["anomaly_mode_entered_at"] = "2026-01-01T00:00:00+08:00"
        meta["anomaly_mode_reason"] = "test"
        gate = _make_gate(state="NORMAL", consecutive_clean=5)
        result = update_anomaly_mode_state(meta, gate, passed=True, trigger=None)
        assert result["mode"] == ANOMALY_MODE_NORMAL
        assert "anomaly_mode_entered_at" not in meta
        assert "anomaly_mode_reason" not in meta

    def test_anomaly_stays_without_enough_clean(self):
        meta = _make_meta(ANOMALY_MODE_ANOMALY)
        meta["anomaly_mode_entered_at"] = "2026-01-01T00:00:00+08:00"
        gate = _make_gate(state="NORMAL", consecutive_clean=3)
        result = update_anomaly_mode_state(meta, gate, passed=True, trigger=None)
        assert result["mode"] == ANOMALY_MODE_ANOMALY

    def test_error_recovery_to_normal(self):
        meta = _make_meta(ANOMALY_MODE_ERROR_RECOVERY)
        meta["anomaly_mode_entered_at"] = "2026-01-01T00:00:00+08:00"
        gate = _make_gate(state="NORMAL", consecutive_clean=5)
        result = update_anomaly_mode_state(meta, gate, passed=True, trigger=None)
        assert result["mode"] == ANOMALY_MODE_NORMAL


class TestAutoHealAnomalyMode:
    def test_no_heal_when_normal(self):
        meta = _make_meta(ANOMALY_MODE_NORMAL)
        result = auto_heal_anomaly_mode(meta)
        assert result["healed"] is False

    def test_no_heal_when_too_recent(self):
        from datetime import datetime, timedelta
        from mg_utils import CST
        meta = _make_meta(ANOMALY_MODE_ANOMALY)
        meta["anomaly_mode_entered_at"] = (datetime.now(CST) - timedelta(hours=24)).isoformat()
        result = auto_heal_anomaly_mode(meta, auto_heal_hours=168)
        assert result["healed"] is False

    def test_heal_when_stale_and_clean(self):
        from datetime import datetime, timedelta
        from mg_utils import CST
        meta = _make_meta(ANOMALY_MODE_ANOMALY)
        meta["anomaly_mode_entered_at"] = (datetime.now(CST) - timedelta(hours=200)).isoformat()
        meta["quality_gate_state"] = {
            "check_history": [{"passed": True}] * 5
        }
        result = auto_heal_anomaly_mode(meta)
        assert result["healed"] is True
        assert result["mode"] == ANOMALY_MODE_NORMAL
        assert "anomaly_mode_entered_at" not in meta

    def test_no_heal_when_stale_but_dirty(self):
        from datetime import datetime, timedelta
        from mg_utils import CST
        meta = _make_meta(ANOMALY_MODE_ANOMALY)
        meta["anomaly_mode_entered_at"] = (datetime.now(CST) - timedelta(hours=200)).isoformat()
        meta["quality_gate_state"] = {
            "check_history": [{"passed": True}, {"passed": False}]
        }
        result = auto_heal_anomaly_mode(meta)
        assert result["healed"] is False
