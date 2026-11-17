"""
Cases 21-25: safe_write.py — atomic write, validation, locking.

Tests the Python module directly (no bash subprocess).
"""
import json
import os
import sys
import tempfile
import time
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import safe_write as sw


def _state(n_meds=1):
    meds = []
    for i in range(n_meds):
        meds.append({
            "id": f"med-{str(i+1).zfill(3)}",
            "name": "Metformin", "type": "pill",
            "dose": "500", "unit": "mg", "paused": False,
            "schedule": {"frequency": "once_daily", "times": ["08:00"],
                         "interval_hours": None, "with_food": False, "notes": ""},
            "escalation": {"late_threshold_minutes": 30, "missed_threshold_minutes": 90,
                           "late_message": "Late: {name}", "missed_message": "Missed: {name}"},
            "state": {"status": "pending", "last_taken": None, "last_reminded": None,
                      "next_due": None, "missed_count": 0, "history": []},
        })
    return {"version": "1", "global": {
        "timezone": "America/Los_Angeles",
        "quiet_hours": {"start": "22:00", "end": "07:00"},
        "paused": False, "digest_time": "08:00", "delivery_channel": "whatsapp",
    }, "meds": meds}


def with_paths(tmp_path, fn):
    """Run fn with sw paths pointed at tmp_path (derived paths follow STATE_FILE)."""
    orig_state = sw.STATE_FILE
    orig_log   = sw.LOG_FILE
    try:
        sw.STATE_FILE = tmp_path / "meds-state.json"
        sw.LOG_FILE   = tmp_path / "safe-write.log"
        fn(tmp_path)
    finally:
        sw.STATE_FILE = orig_state
        sw.LOG_FILE   = orig_log


# ── Case 21: valid state → success, backup created, file updated ──────────────

def test_case_21_valid_write_and_backup(tmp_path):
    def run(d):
        sw.STATE_FILE.write_text(json.dumps(_state(0)), encoding="utf-8")
        original = sw.STATE_FILE.read_text()
        new = json.dumps(_state(1), indent=2)
        sw.safe_write(new)
        assert sw.STATE_FILE.read_text() == new
        assert sw.backup_file().exists()
        assert sw.backup_file().read_text() == original
    with_paths(tmp_path, run)


# ── Case 22: invalid JSON → ValueError, file unchanged ───────────────────────

def test_case_22_invalid_json_rejected(tmp_path):
    def run(d):
        original = json.dumps(_state(0))
        sw.STATE_FILE.write_text(original, encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid JSON"):
            sw.safe_write("{ not valid json }")
        assert sw.STATE_FILE.read_text() == original
    with_paths(tmp_path, run)


# ── Case 23: lock held by another holder → RuntimeError ──────────────────────

def test_case_23_lock_held_raises(tmp_path, monkeypatch):
    def run(d):
        sw.STATE_FILE.write_text(json.dumps(_state(0)), encoding="utf-8")
        monkeypatch.setattr(sw, "LOCK_WAIT", 0.3)
        held, release = threading.Event(), threading.Event()

        def hold():
            with sw.file_lock():
                held.set()
                release.wait(2)

        t = threading.Thread(target=hold)
        t.start()
        try:
            assert held.wait(1), "holder never acquired the lock"
            with pytest.raises(RuntimeError, match="Could not acquire lock"):
                sw.safe_write(_state(1))
        finally:
            release.set()
            t.join(3)
    with_paths(tmp_path, run)


# ── Case 24: first install (no existing file) → write, no backup ─────────────

def test_case_24_first_install(tmp_path):
    def run(d):
        assert not sw.STATE_FILE.exists()
        sw.safe_write(_state(1))
        assert sw.STATE_FILE.exists()
        assert not sw.backup_file().exists()
    with_paths(tmp_path, run)


# ── Case 25: structurally invalid state → ValueError ─────────────────────────

def test_case_25_invalid_structure_rejected(tmp_path):
    def run(d):
        original = json.dumps(_state(0))
        sw.STATE_FILE.write_text(original, encoding="utf-8")
        bad = {"version": "1", "global": {}, "meds": "not-an-array"}
        with pytest.raises(ValueError):
            sw.safe_write(bad)
        assert sw.STATE_FILE.read_text() == original
    with_paths(tmp_path, run)


# ── Backup rotation: two generations survive consecutive writes ───────────────

def test_backup_rotation_keeps_two_generations(tmp_path):
    def run(d):
        sw.safe_write(_state(1))                     # gen 1 on disk
        first = sw.STATE_FILE.read_text(encoding="utf-8")
        sw.safe_write(_state(2))                     # gen 1 → .bak
        second = sw.STATE_FILE.read_text(encoding="utf-8")
        sw.safe_write(_state(3))                     # .bak → .bak.old, gen 2 → .bak
        assert sw.STATE_FILE.read_text(encoding="utf-8") != second
        assert sw.backup_file().read_text(encoding="utf-8") == second
        assert sw.backup_old_file().read_text(encoding="utf-8") == first
    with_paths(tmp_path, run)


# ── Regression: as_needed without times must be accepted ─────────────────────

def test_as_needed_without_times_accepted(tmp_path):
    def run(d):
        state = _state(0)
        state["meds"] = [{
            "id": "med-001", "name": "Ibuprofen", "type": "pill",
            "dose": "400", "unit": "mg", "paused": False,
            "schedule": {"frequency": "as_needed", "interval_hours": None,
                         "with_food": False, "notes": ""},
            "escalation": {"late_threshold_minutes": 30, "missed_threshold_minutes": 90,
                           "late_message": "x", "missed_message": "y"},
            "state": {"status": "pending", "last_taken": None, "last_reminded": None,
                      "next_due": None, "missed_count": 0, "history": []},
        }]
        sw.safe_write(state)  # must not raise
        assert sw.STATE_FILE.exists()
    with_paths(tmp_path, run)


# ── Validate: duplicate med IDs rejected ────────────────────────────────────

def test_duplicate_med_id_rejected():
    state = _state(1)
    state["meds"].append(state["meds"][0].copy())  # duplicate med-001
    with pytest.raises(ValueError, match="duplicate id"):
        sw.validate(state)


# ── Validate: late >= missed rejected ────────────────────────────────────────

def test_late_threshold_no_longer_ordered_against_missed():
    # #11: late_threshold_minutes is the nudge cadence; missed is retired
    state = _state(1)
    state["meds"][0]["escalation"]["late_threshold_minutes"]   = 90
    state["meds"][0]["escalation"]["missed_threshold_minutes"] = 30
    sw.validate(state)


# ── day_of_week: single string or canonical list (PR 7) ─────────────────────

def _weekly_state(day):
    state = _state(1)
    state["meds"][0]["schedule"] = {
        "frequency": "weekly", "times": ["09:00"], "interval_hours": None,
        "day_of_week": day, "with_food": False, "notes": ""}
    return state


def test_day_of_week_canonical_list_accepted():
    sw.validate(_weekly_state(["tue", "sat"]))
    sw.validate(_weekly_state(["mon", "tue", "wed", "thu", "fri"]))


def test_day_of_week_single_string_still_accepted():
    sw.validate(_weekly_state("mon"))


def test_day_of_week_empty_list_rejected():
    with pytest.raises(ValueError, match="empty list"):
        sw.validate(_weekly_state([]))


def test_day_of_week_unknown_day_in_list_rejected():
    with pytest.raises(ValueError, match="unknown day"):
        sw.validate(_weekly_state(["tue", "funday"]))


def test_day_of_week_unknown_string_rejected():
    with pytest.raises(ValueError, match="must be one of"):
        sw.validate(_weekly_state("funday"))


def test_day_of_week_duplicates_rejected():
    with pytest.raises(ValueError, match="duplicate day"):
        sw.validate(_weekly_state(["tue", "sat", "tue"]))


def test_day_of_week_unsorted_rejected():
    with pytest.raises(ValueError, match="sorted mon..sun"):
        sw.validate(_weekly_state(["sat", "tue"]))


def test_day_of_week_non_string_non_list_rejected():
    with pytest.raises(ValueError, match="day string, a list of days"):
        sw.validate(_weekly_state(3))


def test_weekly_without_day_of_week_still_rejected():
    with pytest.raises(ValueError, match="required for weekly"):
        sw.validate(_weekly_state(None))
