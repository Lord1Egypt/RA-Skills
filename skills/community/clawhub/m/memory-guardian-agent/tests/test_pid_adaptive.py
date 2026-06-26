"""Tests for pid_adaptive — PID controller for adaptive thresholds."""

import pytest

from pid_adaptive import PIDController, get_pid_state, get_or_create_controller


class TestPIDController:
    def test_compute_output(self):
        pid = PIDController(kp=0.1, ki=0.01, kd=0.05)
        result = pid.compute(1.0)
        assert isinstance(result, dict)
        assert result["output"] > 0

    def test_integral_accumulation(self):
        pid = PIDController(kp=0.0, ki=0.1, kd=0.0)
        pid.compute(1.0)
        result = pid.compute(1.0)
        assert result["output"] > 0

    def test_zero_error_zero_output(self):
        pid = PIDController(kp=0.1, ki=0.0, kd=0.0)
        result = pid.compute(0.0)
        assert result["output"] == 0.0

    def test_negative_error(self):
        pid = PIDController(kp=0.1, ki=0.0, kd=0.0)
        result = pid.compute(-1.0)
        assert result["output"] < 0

    def test_has_p_i_d_terms(self):
        pid = PIDController(kp=0.1, ki=0.01, kd=0.05)
        result = pid.compute(1.0)
        assert "p_term" in result
        assert "i_term" in result
        assert "d_term" in result

    def test_reset(self):
        pid = PIDController(kp=0.1, ki=0.1, kd=0.0)
        pid.compute(1.0)
        pid.compute(1.0)
        pid.reset()
        result = pid.compute(1.0)
        # After reset, integral should start fresh
        assert result["i_term"] < 0.2  # Much smaller than accumulated


class TestGetOrCreateController:
    def test_creates_new(self):
        pid_state = {"controllers": {}}
        ctrl = get_or_create_controller(pid_state, "test_group", kp=0.1)
        assert ctrl is not None
        assert "test_group" in pid_state["controllers"]

    def test_reuses_existing(self):
        pid_state = {"controllers": {}}
        ctrl1 = get_or_create_controller(pid_state, "test_group", kp=0.1)
        ctrl2 = get_or_create_controller(pid_state, "test_group", kp=0.1)
        # Controller state is persisted in pid_state
        assert "test_group" in pid_state["controllers"]


class TestGetPidState:
    def test_default(self):
        meta = {"version": "0.4.2"}
        state = get_pid_state(meta)
        assert isinstance(state, dict)
        assert "controllers" in state


# ─── New tests for uncovered functions ───────────────────────

from pid_adaptive import compute_error_signal, save_pid_state, update_thresholds


class TestComputeErrorSignal:
    def test_returns_dict(self):
        meta = {"memories": [], "l3_confirmations": [], "quality_gate_state": {}}
        result = compute_error_signal(meta)
        assert isinstance(result, dict)
        assert "error" in result
        assert "components" in result

    def test_with_l3_data(self):
        meta = {
            "memories": [],
            "l3_confirmations": [
                {"status": "confirmed"},
                {"status": "confirmed"},
                {"status": "degraded"},
                {"status": "pending"},
            ],
            "quality_gate_state": {"state": "NORMAL"},
        }
        result = compute_error_signal(meta)
        assert result["components"]["l3_coverage"]["rate"] == 0.75  # 3/4

    def test_critical_gate_state(self):
        meta = {
            "memories": [],
            "l3_confirmations": [],
            "quality_gate_state": {"state": "CRITICAL"},
        }
        result = compute_error_signal(meta)
        assert result["components"]["gate_factor"]["factor"] == 0.3


class TestSavePidState:
    def test_saves_state(self, tmp_path):
        import json
        meta = {"version": "0.4.2", "memories": []}
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        pid_state = get_pid_state(meta)
        pid_state["scene_thresholds"]["test"] = 0.7
        save_pid_state(p, meta, pid_state)
        with open(p) as f:
            saved = json.load(f)
        assert saved["pid_state"]["scene_thresholds"]["test"] == 0.7
        assert saved["pid_state"]["last_update"] is not None

    def test_updates_last_update(self, tmp_path):
        import json
        meta = {"version": "0.4.2", "memories": []}
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        pid_state = get_pid_state(meta)
        assert pid_state["last_update"] is None
        save_pid_state(p, meta, pid_state)
        with open(p) as f:
            saved = json.load(f)
        assert saved["pid_state"]["last_update"] is not None


class TestUpdateThresholds:
    def test_updates_active_memories(self, tmp_path):
        import json
        meta = {
            "version": "0.4.2",
            "memories": [
                {"id": "m1", "memory_type": "absorb", "status": "active"},
            ],
            "l3_confirmations": [],
            "quality_gate_state": {"state": "NORMAL"},
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        result = update_thresholds(p)
        assert result["status"] in ("updated", "no_change", "skipped")
        assert "error" in result

    def test_dry_run_no_save(self, tmp_path):
        import json
        meta = {
            "version": "0.4.2",
            "memories": [],
            "l3_confirmations": [],
            "quality_gate_state": {},
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        result = update_thresholds(p, dry_run=True)
        assert result["dry_run"] is True
        # meta.json should not have pid_state written
        with open(p) as f:
            saved = json.load(f)
        assert "pid_state" not in saved
