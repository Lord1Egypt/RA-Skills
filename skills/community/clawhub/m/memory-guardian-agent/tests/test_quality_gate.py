"""Tests for quality_gate — quality gate state machine and checks."""

import pytest

from quality_gate import (
    get_l2_config,
    load_normalized_meta,
    get_gate_state,
    save_gate_state,
    transition_state,
    check_layer,
    check_all_layers,
    compute_intervention_level,
    record_result,
    record_degraded_write,
    end_correction,
    check_l2_timeout,
    check_l1_audit_expired,
    get_l1_pending_count,
    enqueue_l1_pending,
    get_anomaly_mode,
    evaluate_quiet_degradation_state,
    check_inbox_backlog,
    check_routing_health,
    check_conflict_rate,
    run_health_checks,
    INTERVENTION_L0_SILENT,
    INTERVENTION_L1_NOTIFY,
    INTERVENTION_L2_PAUSE,
    INTERVENTION_L3_MANUAL,
    STATE_NORMAL,
    STATE_WARNING,
    STATE_CRITICAL,
    STATE_RECOVERING,
    WARNING_ANOMALY_N,
    RECOVERY_SWITCH_M,
    END_CORRECTION_THRESHOLD,
)


def _make_state(**overrides):
    defaults = {
        "state": "NORMAL",
        "anomaly_count": 0,
        "total_writes": 0,
        "total_failures": 0,
        "failure_rate": 0.0,
        "consecutive_clean": 0,
        "consecutive_failures": 0,
        "total_checks": 0,
        "history": [],
        "check_history": [],
        "warning_entered_at": None,
        "critical_entered_at": None,
        "recovering_entered_at": None,
    }
    defaults.update(overrides)
    return defaults


def _make_gate():
    return _make_state()


class TestGetGateState:
    def test_default_state(self):
        state = get_gate_state({"version": "0.4.2", "memories": []})
        assert state["state"] == "NORMAL"

    def test_existing_state(self):
        meta = {"version": "0.4.2", "memories": [],
                "quality_gate_state": {"state": "WARNING"}}
        state = get_gate_state(meta)
        assert state["state"] == "WARNING"


class TestTransitionState:
    def test_clean_stays_normal(self):
        state = _make_state()
        new_state, changed, info = transition_state(state, "clean")
        assert new_state["state"] == "NORMAL"

    def test_anomaly_normal_to_warning(self):
        state = _make_state()
        for _ in range(WARNING_ANOMALY_N):
            state, _, _ = transition_state(state, "anomaly")
        assert state["state"] == "WARNING"

    def test_anomaly_stays_normal_below_threshold(self):
        state = _make_state()
        for _ in range(WARNING_ANOMALY_N - 1):
            state, _, _ = transition_state(state, "anomaly")
        assert state["state"] == "NORMAL"

    def test_clean_warning_to_normal(self):
        # Need anomaly_count to drop to 0
        state = _make_state(state="WARNING", anomaly_count=1, consecutive_clean=0)
        new_state, changed, info = transition_state(state, "clean")
        assert new_state["state"] == "NORMAL"
        assert changed is True

    def test_clean_critical_stays_critical(self):
        state = _make_state(state="CRITICAL", anomaly_count=5)
        new_state, changed, info = transition_state(state, "clean")
        assert new_state["state"] == "CRITICAL"

    def test_clean_recovering_to_normal(self):
        state = _make_state(state="RECOVERING", consecutive_clean=RECOVERY_SWITCH_M)
        new_state, changed, info = transition_state(state, "clean")
        assert new_state["state"] == "NORMAL"

    def test_force_normal(self):
        state = _make_state(state="CRITICAL")
        new_state, changed, info = transition_state(state, "force_normal")
        assert new_state["state"] == "NORMAL"
        assert changed is True


class TestCheckLayer:
    def test_returns_tuple(self):
        result = check_layer("test", "security", {}, _make_gate())
        assert isinstance(result, tuple)
        assert len(result) == 3  # (passed, name, critical)

    def test_security_layer_passes(self):
        passed, name, critical = check_layer("normal content", "security", {}, _make_gate())
        assert passed is True

    def test_unknown_layer_passes(self):
        passed, name, critical = check_layer("test", "nonexistent", {}, _make_gate())
        assert passed is True


class TestCheckAllLayers:
    def test_all_pass(self):
        all_passed, results, _ = check_all_layers(
            "This is a normal content string for quality check",
            {"version": "0.4.2", "memories": []}
        )
        assert all_passed is True

    def test_empty_content(self):
        all_passed, results, _ = check_all_layers(
            "",
            {"version": "0.4.2", "memories": []}
        )
        assert isinstance(all_passed, bool)


class TestComputeInterventionLevel:
    def test_normal_state_l0(self):
        level, _, _ = compute_intervention_level(_make_state(), "ingest")
        assert level == INTERVENTION_L0_SILENT

    def test_warning_state_l1(self):
        level, _, _ = compute_intervention_level(_make_state(state="WARNING"), "ingest")
        assert level == INTERVENTION_L1_NOTIFY

    def test_critical_state_l2(self):
        level, _, _ = compute_intervention_level(_make_state(state="CRITICAL"), "ingest")
        assert level == INTERVENTION_L2_PAUSE


class TestGetL2Config:
    def test_default(self):
        meta = {"version": "0.4.2"}
        config = get_l2_config(meta)
        assert isinstance(config, dict)
        assert "queue_cap" in config
        assert config["queue_cap"] > 0


# ─── Helper: create a minimal meta.json in tmp_path/memory/ ───

def _setup_meta(tmp_path, **meta_overrides):
    """Create memory/meta.json in tmp_path with defaults + overrides."""
    import json
    from mg_utils import save_meta
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    meta_path = memory_dir / "meta.json"
    meta = {"version": "0.4.2", "memories": []}
    meta.update(meta_overrides)
    save_meta(str(meta_path), meta)
    return str(meta_path), meta


class TestLoadNormalizedMeta:
    def test_load_basic(self, tmp_path):
        meta_path, _ = _setup_meta(tmp_path)
        meta = load_normalized_meta(meta_path)
        assert "version" in meta
        assert "memories" in meta

    def test_persist_changes(self, tmp_path):
        meta_path, _ = _setup_meta(tmp_path)
        # normalize may add defaults; persist=True should save
        meta = load_normalized_meta(meta_path, persist=True)
        # Reload and verify
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        assert reloaded is not None


class TestSaveGateState:
    def test_save_and_reload(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        state = get_gate_state(meta)
        state["anomaly_count"] = 5
        state["total_writes"] = 10
        save_gate_state(meta_path, meta, state)
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        qgs = reloaded.get("quality_gate_state", {})
        assert qgs["anomaly_count"] == 5
        assert qgs["total_writes"] == 10

    def test_preserves_unknown_fields(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        meta["quality_gate_state"] = {"state": "NORMAL", "custom_field": "keep_me"}
        state = get_gate_state(meta)
        save_gate_state(meta_path, meta, state)
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        assert reloaded["quality_gate_state"].get("custom_field") == "keep_me"

    def test_none_values_skip(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        meta["quality_gate_state"] = {"state": "NORMAL", "anomaly_count": 3}
        state = get_gate_state(meta)
        state["anomaly_count"] = None
        save_gate_state(meta_path, meta, state)
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        assert reloaded["quality_gate_state"]["anomaly_count"] == 3


class TestTransitionStateExtended:
    def test_anomaly_during_recovering(self):
        state = _make_state(state="RECOVERING", consecutive_clean=3)
        state, changed, info = transition_state(state, "anomaly")
        assert state["state"] == STATE_WARNING
        assert changed is True
        assert state["anomaly_count"] == 1  # reset counter

    def test_anomaly_in_warning_with_high_failure_rate(self):
        state = _make_state(state="WARNING", anomaly_count=5,
                            total_writes=1, total_failures=10)
        # failure_rate should be high enough to trigger CRITICAL
        state["failure_rate"] = 0.5
        state["state_entered_at"] = _now_iso()  # recent, so time condition not met
        # But anomaly trigger doesn't directly check failure_rate in WARNING;
        # _should_upgrade_to_critical does
        state, changed, info = transition_state(state, "anomaly")
        # With failure_rate 0.5 > 0.2, should upgrade
        assert state["state"] == STATE_CRITICAL
        assert changed is True

    def test_recovering_not_enough_clean(self):
        state = _make_state(state="RECOVERING", consecutive_clean=RECOVERY_SWITCH_M - 2)
        state, changed, info = transition_state(state, "clean")
        assert state["state"] == STATE_RECOVERING
        assert changed is False

    def test_clean_reduces_anomaly_count(self):
        state = _make_state(anomaly_count=2)
        state, _, _ = transition_state(state, "clean")
        assert state["anomaly_count"] == 1

    def test_force_normal_resets_counters(self):
        state = _make_state(state="CRITICAL", anomaly_count=10,
                            total_failures=20, failure_rate=0.8)
        state, changed, info = transition_state(state, "force_normal")
        assert state["anomaly_count"] == 0
        assert state["failure_rate"] == 0.0
        assert state["state"] == STATE_NORMAL

    def test_auto_check_upgrades_warning_to_critical(self):
        state = _make_state(state="WARNING", anomaly_count=3,
                            total_writes=1, total_failures=10)
        state["failure_rate"] = 0.5
        state, changed, info = transition_state(state, "auto_check")
        assert state["state"] == STATE_CRITICAL
        assert changed is True

    def test_history_records_transitions(self):
        state = _make_state()
        transition_state(state, "anomaly")
        transition_state(state, "anomaly")
        transition_state(state, "anomaly")
        # Now in WARNING
        assert state["state"] == STATE_WARNING
        assert len(state["history"]) >= 1
        assert state["history"][-1]["from"] == STATE_NORMAL
        assert state["history"][-1]["to"] == STATE_WARNING

    def test_clean_in_warning_resolves_anomaly_count_zero(self):
        state = _make_state(state="WARNING", anomaly_count=1, consecutive_clean=0)
        state, changed, info = transition_state(state, "clean")
        assert state["state"] == STATE_NORMAL
        assert changed is True


class TestCheckLayerExtended:
    def test_critical_blocks_all(self):
        gate = _make_state(state="CRITICAL")
        for layer in ["security", "dedup", "ingest", "decay"]:
            passed, reason, critical = check_layer("anything", layer, {}, gate)
            assert passed is False
            assert "critical:blocked" in reason

    def test_warning_skips_dedup(self):
        gate = _make_state(state="WARNING")
        passed, reason, bypass = check_layer("content", "dedup", {}, gate)
        assert passed is True
        assert bypass is True
        assert "skipped_warning" in reason

    def test_recovering_relaxes_dedup(self):
        gate = _make_state(state="RECOVERING")
        passed, reason, bypass = check_layer("content", "dedup", {}, gate)
        assert passed is True
        assert bypass is True

    def test_security_with_critical_rule(self):
        gate = _make_state()
        meta = {"security_rules": [{
            "id": "test-block", "severity": "critical",
            "pattern": r"forbidden_word", "description": "blocks forbidden",
        }]}
        passed, reason, _ = check_layer("this has forbidden_word", "security", meta, gate)
        assert passed is False

    def test_ingest_short_content_blocked(self):
        gate = _make_state()
        passed, reason, _ = check_layer("short", "ingest", {}, gate)
        assert passed is False
        assert "too_short" in reason

    def test_decay_always_passes(self):
        gate = _make_state()
        passed, reason, _ = check_layer("anything", "decay", {}, gate)
        assert passed is True

    def test_security_regex_error_fallback(self):
        gate = _make_state()
        meta = {"security_rules": [{
            "id": "bad-regex", "severity": "critical",
            "pattern": r"[invalid(", "description": "bad regex",
        }]}
        # Malformed regex should be skipped (not caught by literal fallback)
        passed, reason, _ = check_layer("[invalid(", "security", meta, gate)
        assert passed is True


class TestCheckAllLayersExtended:
    def test_critical_blocks_overall(self):
        gate = _make_state(state="CRITICAL")
        all_passed, results, degraded = check_all_layers("content", {}, gate)
        assert all_passed is False
        assert degraded is False  # critical is not degraded, it's blocked

    def test_warning_is_degraded(self):
        gate = _make_state(state="WARNING")
        all_passed, results, degraded = check_all_layers("a normal content string", {}, gate)
        assert degraded is True

    def test_recovering_is_degraded(self):
        gate = _make_state(state="RECOVERING")
        all_passed, results, degraded = check_all_layers("a normal content string", {}, gate)
        assert degraded is True

    def test_results_include_intervention_level(self):
        all_passed, results, _ = check_all_layers("content", {})
        assert "intervention_level" in results
        assert "notification_needed" in results


class TestRecordResult:
    def test_record_pass(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        gate = get_gate_state(meta)
        record_result(meta_path, meta, True, gate)
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        history = reloaded.get("quality_gate_state", {}).get("check_history", [])
        assert len(history) == 1
        assert history[0]["passed"] is True

    def test_record_fail(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        gate = get_gate_state(meta)
        record_result(meta_path, meta, False, gate)
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        history = reloaded.get("quality_gate_state", {}).get("check_history", [])
        assert len(history) == 1
        assert history[0]["passed"] is False

    def test_history_bounded(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        gate = get_gate_state(meta)
        # Add more than 100 entries
        for _ in range(120):
            record_result(meta_path, meta, True, gate)
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        history = reloaded.get("quality_gate_state", {}).get("check_history", [])
        assert len(history) <= 100


class TestRecordDegradedWrite:
    def test_warning_records_skipped_layers(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        gate = get_gate_state(meta)
        gate["state"] = STATE_WARNING
        record_degraded_write(meta_path, meta, "test content", gate)
        assert len(gate["degraded_writes"]) == 1
        entry = gate["degraded_writes"][0]
        assert "dedup" in entry["layers_skipped"]
        assert "ingest" in entry["layers_skipped"]

    def test_recovering_records_dedup_skipped(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        gate = get_gate_state(meta)
        gate["state"] = STATE_RECOVERING
        record_degraded_write(meta_path, meta, "test content", gate)
        entry = gate["degraded_writes"][0]
        assert "dedup" in entry["layers_skipped"]
        assert "ingest" not in entry["layers_skipped"]

    def test_content_preview_truncated(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        gate = get_gate_state(meta)
        gate["state"] = STATE_WARNING
        long_content = "x" * 200
        record_degraded_write(meta_path, meta, long_content, gate)
        entry = gate["degraded_writes"][0]
        assert len(entry["content_preview"]) <= 100


class TestEndCorrection:
    def test_flags_low_decay_memories(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path, memories=[
            {"id": "m1", "status": "active", "decay_score": 0.1, "content": "low decay"},
            {"id": "m2", "status": "active", "decay_score": 0.9, "content": "high decay"},
            {"id": "m3", "status": "archived", "decay_score": 0.05, "content": "archived"},
        ])
        flagged = end_correction(meta_path, meta)
        assert "m1" in flagged
        assert "m2" not in flagged
        assert "m3" not in flagged  # archived, not active

    def test_no_low_decay(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path, memories=[
            {"id": "m1", "status": "active", "decay_score": 0.8, "content": "ok"},
        ])
        flagged = end_correction(meta_path, meta)
        assert flagged == []

    def test_sets_quality_gate_fields(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path, memories=[
            {"id": "m1", "status": "active", "decay_score": 0.1, "content": "low"},
        ])
        end_correction(meta_path, meta)
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        mem = reloaded["memories"][0]
        assert "quality_gate" in mem
        assert mem["quality_gate"]["gate_mode"] == "anomaly_correction"


class TestComputeInterventionLevelExtended:
    def test_normal_delete_l0(self):
        level, _, _ = compute_intervention_level(_make_state(), "delete")
        assert level == INTERVENTION_L0_SILENT

    def test_l3_high_anomaly_delete(self):
        level, notify, block = compute_intervention_level(
            _make_state(anomaly_count=10), "delete")
        assert level == INTERVENTION_L3_MANUAL
        assert notify is True
        assert block is True

    def test_l3_not_in_critical(self):
        # In CRITICAL state, destructive actions (delete/modify) still trigger L3
        # because human confirmation is needed even more urgently when the system
        # is in a degraded state. Only ingest falls through to L2 queueing.
        level, _, _ = compute_intervention_level(
            _make_state(state="CRITICAL", anomaly_count=20), "delete")
        assert level == INTERVENTION_L3_MANUAL

    def test_l2_for_ingest_in_critical(self):
        # In CRITICAL, non-destructive actions (ingest) still go to L2 queue
        level, _, _ = compute_intervention_level(
            _make_state(state="CRITICAL", anomaly_count=20), "ingest")
        assert level == INTERVENTION_L2_PAUSE

    def test_warning_modify_l1(self):
        level, notify, block = compute_intervention_level(
            _make_state(state="WARNING"), "modify")
        assert level == INTERVENTION_L1_NOTIFY
        assert notify is True
        assert block is False

    def test_recovering_ingest_l1(self):
        level, _, _ = compute_intervention_level(
            _make_state(state="RECOVERING"), "ingest")
        assert level == INTERVENTION_L1_NOTIFY

    def test_anomaly_count_3_triggers_l1(self):
        # anomaly_count >= 3 but state=NORMAL → only for delete/modify, not ingest
        level, _, _ = compute_intervention_level(
            _make_state(anomaly_count=3), "delete")
        assert level == INTERVENTION_L1_NOTIFY

    def test_configurable_l3_threshold(self):
        meta = {"decay_config": {"l3_anomaly_threshold": 20}}
        level, _, _ = compute_intervention_level(
            _make_state(anomaly_count=10), "delete", meta)
        # 10 < 20, so not L3
        assert level != INTERVENTION_L3_MANUAL


class TestCheckL2Timeout:
    def test_no_l2_entry(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        result = check_l2_timeout(meta_path)
        assert result["timed_out"] is False

    def test_recent_entry_no_timeout(self, tmp_path):
        from datetime import datetime, timedelta, timezone
        from mg_utils import save_meta
        meta_path, meta = _setup_meta(tmp_path)
        now = datetime.now(timezone(timedelta(hours=8)))
        meta["quality_gate_state"] = {"state": STATE_CRITICAL, "l2_entered_at": now.isoformat()}
        save_meta(meta_path, meta)
        result = check_l2_timeout(meta_path)
        assert result["timed_out"] is False

    def test_old_entry_timeout(self, tmp_path):
        from datetime import datetime, timedelta, timezone
        from mg_utils import save_meta
        meta_path, meta = _setup_meta(tmp_path)
        CST = timezone(timedelta(hours=8))
        old = datetime.now(CST) - timedelta(minutes=60)
        meta["quality_gate_state"] = {
            "state": STATE_CRITICAL,
            "l2_entered_at": old.isoformat(),
            "l2_write_queue": [],
        }
        save_meta(meta_path, meta)
        result = check_l2_timeout(meta_path)
        assert result["timed_out"] is True


class TestCheckL1AuditExpired:
    def test_no_pending(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        result = check_l1_audit_expired(meta_path)
        assert result["expired"] == 0

    def test_active_entry_not_expired(self, tmp_path):
        from mg_utils import save_meta
        from datetime import datetime, timedelta, timezone
        CST = timezone(timedelta(hours=8))
        now = datetime.now(CST)
        future = (now + timedelta(minutes=30)).isoformat()
        meta_path, meta = _setup_meta(tmp_path)
        meta["l1_pending"] = [{
            "id": "l1_test", "status": "executed",
            "audit_until": future, "reviewed": False,
        }]
        save_meta(meta_path, meta)
        result = check_l1_audit_expired(meta_path)
        assert result["expired"] == 0

    def test_expired_entry_resolved(self, tmp_path):
        from mg_utils import save_meta
        from datetime import datetime, timedelta, timezone
        CST = timezone(timedelta(hours=8))
        now = datetime.now(CST)
        past = (now - timedelta(minutes=60)).isoformat()
        meta_path, meta = _setup_meta(tmp_path)
        meta["l1_pending"] = [{
            "id": "l1_old", "status": "executed",
            "audit_until": past, "reviewed": False,
        }]
        save_meta(meta_path, meta)
        result = check_l1_audit_expired(meta_path)
        assert result["expired"] == 1


class TestGetL1PendingCount:
    def test_empty(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        result = get_l1_pending_count(meta_path)
        assert result["active"] == 0
        assert result["total"] == 0

    def test_with_active_entries(self, tmp_path):
        from mg_utils import save_meta
        meta_path, meta = _setup_meta(tmp_path)
        meta["l1_pending"] = [
            {"id": "l1_1", "status": "executed"},
            {"id": "l1_2", "status": "executed"},
            {"id": "l1_3", "status": "audit_expired"},
        ]
        save_meta(meta_path, meta)
        result = get_l1_pending_count(meta_path)
        assert result["active"] == 2
        assert result["total"] == 3


class TestEnqueueL1Pending:
    def test_basic_enqueue(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        entry = enqueue_l1_pending(meta_path, {"action": "ingest", "fields": {"content": "test"}},
                                   reason="test enqueue")
        assert entry["status"] == "executed"
        assert entry["action"] == "ingest"
        assert entry["audit_until"] is not None

    def test_persists_to_meta(self, tmp_path):
        meta_path, meta = _setup_meta(tmp_path)
        enqueue_l1_pending(meta_path, {"action": "delete", "fields": {}}, reason="test")
        from mg_utils import load_meta
        reloaded = load_meta(meta_path)
        assert len(reloaded.get("l1_pending", [])) == 1


class TestGetAnomalyMode:
    def test_default_mode(self):
        mode_info = get_anomaly_mode({"version": "0.4.2"})
        assert mode_info["mode"] == "normal_decay"
        assert "config" in mode_info

    def test_config_structure(self):
        mode_info = get_anomaly_mode({"version": "0.4.2"})
        cfg = mode_info["config"]
        assert "failure_rate_threshold" in cfg
        assert "failure_count_threshold" in cfg
        assert "recovery_consecutive_clean" in cfg
        assert "auto_heal_hours" in cfg


class TestEvaluateQuietDegradationState:
    def test_no_samples(self):
        result = evaluate_quiet_degradation_state({"version": "0.4.2", "quality_gate_state": {}})
        # Should return a dict with status info
        assert isinstance(result, dict)

    def test_with_samples(self):
        from datetime import datetime, timedelta, timezone
        CST = timezone(timedelta(hours=8))
        now = datetime.now(CST)
        samples = []
        for i in range(10):
            samples.append({
                "timestamp": (now - timedelta(days=i)).isoformat(),
                "archived_count": 2,
                "total_count": 10,
                "rate": 0.2,
            })
        result = evaluate_quiet_degradation_state({
            "version": "0.4.2",
            "quality_gate_state": {"archive_rate_history": samples},
        })
        assert isinstance(result, dict)


class TestCheckInboxBacklog:
    def test_empty_memories(self):
        result = check_inbox_backlog({"memories": []})
        assert result["status"] == "healthy"
        assert result["inbox_count"] == 0

    def test_inbox_entries(self):
        result = check_inbox_backlog({"memories": [
            {"id": "m1", "status": "_inbox"},
            {"id": "m2", "status": "_inbox"},
            {"id": "m3", "status": "active"},
        ]})
        assert result["inbox_count"] == 2

    def test_critical_backlog(self):
        memories = [{"id": f"m{i}", "status": "_inbox"} for i in range(35)]
        result = check_inbox_backlog({"memories": memories})
        assert result["status"] == "critical"

    def test_warning_backlog(self):
        memories = [{"id": f"m{i}", "status": "_inbox"} for i in range(15)]
        result = check_inbox_backlog({"memories": memories})
        assert result["status"] == "warning"

    def test_overdue_needs_review(self):
        from datetime import datetime, timedelta, timezone
        CST = timezone(timedelta(hours=8))
        old = (datetime.now(CST) - timedelta(days=10)).isoformat()
        result = check_inbox_backlog({"memories": [
            {"id": "m1", "status": "active", "needs_review": True,
             "needs_review_since": old, "needs_review_timeout": 7},
        ]})
        assert result["overdue_count"] == 1


class TestCheckRoutingHealth:
    def test_no_routing_data(self):
        result = check_routing_health({"routing_log": []})
        assert result["status"] == "healthy"
        assert result["total_routes"] == 0

    def test_balanced_routing(self):
        routing_log = [
            {"selected": [("cat_a", 0.9)]},
            {"selected": [("cat_b", 0.8)]},
            {"selected": [("cat_a", 0.7)]},
            {"selected": [("cat_c", 0.6)]},
        ]
        result = check_routing_health({"routing_log": routing_log})
        assert result["status"] == "healthy"
        assert result["concentration_ratio"] < 0.8

    def test_concentrated_routing(self):
        routing_log = [{"selected": [("cat_a", 0.9)]} for _ in range(20)]
        result = check_routing_health({"routing_log": routing_log})
        assert result["status"] == "warning"
        assert len(result["alerts"]) > 0


class TestCheckConflictRate:
    def test_no_conflicts(self):
        result = check_conflict_rate({"conflict_log": [], "quality_gate_state": {}})
        assert result["status"] == "healthy"
        assert result["conflict_rate"] == 0.0

    def test_with_recent_conflicts(self):
        from datetime import datetime, timedelta, timezone
        CST = timezone(timedelta(hours=8))
        now = datetime.now(CST)
        conflict_log = [{"timestamp": now.isoformat()} for _ in range(5)]
        gate = {"write_counters": {"total_writes_24h": 100}}
        result = check_conflict_rate({"conflict_log": conflict_log, "quality_gate_state": gate})
        assert result["total_conflicts_24h"] == 5
        assert result["conflict_rate"] == 0.05

    def test_critical_conflict_rate(self):
        from datetime import datetime, timedelta, timezone
        CST = timezone(timedelta(hours=8))
        now = datetime.now(CST)
        conflict_log = [{"timestamp": now.isoformat()} for _ in range(10)]
        gate = {"write_counters": {"total_writes_24h": 100}}
        result = check_conflict_rate({"conflict_log": conflict_log, "quality_gate_state": gate})
        assert result["status"] == "critical"


class TestRunHealthChecks:
    def test_all_healthy(self):
        result = run_health_checks({"memories": [], "routing_log": [], "conflict_log": []})
        assert result["overall_status"] == "healthy"
        assert "inbox" in result
        assert "routing" in result
        assert "conflicts" in result

    def test_overall_is_worst(self):
        result = run_health_checks({
            "memories": [{"id": f"m{i}", "status": "_inbox"} for i in range(35)],
            "routing_log": [],
            "conflict_log": [],
        })
        assert result["overall_status"] == "critical"

    def test_alert_count(self):
        result = run_health_checks({"memories": [], "routing_log": [], "conflict_log": []})
        # info alerts should be filtered out
        assert isinstance(result["alert_count"], int)

    def test_checked_at_present(self):
        result = run_health_checks({"memories": [], "routing_log": [], "conflict_log": []})
        assert "checked_at" in result
        assert result["checked_at"] is not None


def _now_iso():
    """Helper to get current ISO timestamp."""
    from datetime import datetime, timezone, timedelta
    return datetime.now(timezone(timedelta(hours=8))).isoformat()
