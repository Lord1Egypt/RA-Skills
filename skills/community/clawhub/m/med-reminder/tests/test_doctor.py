"""
Doctor checks (issue #1 §5): heartbeat freshness (3x the tick interval),
quiet-hours FAILs (dose time and muted T+late; AC 26 + AC 28's head
exemption), the SENDER_DOWN marker, and outstanding send_failed events.

OS interactions go through doctor's _run seam (covered in
test_scheduler_migration.py); everything here runs against tmp_path files.
"""
import json
from datetime import datetime, timedelta, timezone

import pytest

import doctor
import event_store
import safe_write
from tests.conftest import make_med, make_state

NOW = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def env(tmp_path, monkeypatch):
    """A doctor pointed at a tmp state dir (state, heartbeat, history)."""
    sf = tmp_path / "meds-state.json"
    monkeypatch.setattr(doctor, "STATE_FILE", sf)
    monkeypatch.setattr(safe_write, "STATE_FILE", sf)

    def write_state(meds=None, **kw):
        sf.write_text(json.dumps(make_state(meds=meds if meds is not None else [], **kw)),
                      encoding="utf-8")

    def write_heartbeat(age_minutes):
        ended = NOW - timedelta(minutes=age_minutes)
        (tmp_path / "tick-heartbeat.json").write_text(json.dumps({
            "started_utc": ended.isoformat(),
            "ended_utc": ended.isoformat(),
            "watermark_utc": ended.isoformat(),
            "errors": 0,
        }), encoding="utf-8")

    from types import SimpleNamespace

    write_state()
    return SimpleNamespace(
        state_file=sf,
        write_state=write_state,
        write_heartbeat=write_heartbeat,
        history_file=tmp_path / "history.jsonl",
        seed=lambda events: event_store.append_events(
            tmp_path / "history.jsonl", events),
    )


def checked(fn, *a, **kw):
    doctor.results.clear()
    fn(*a, **kw)
    return doctor.results


def failures(results):
    return [msg for level, msg in results if level == "fail"]


def warnings(results):
    return [msg for level, msg in results if level == "warn"]


# ── heartbeat freshness (issue #1 §5) ──────────────────────────────────────────

def test_missing_heartbeat_fails(env):
    res = checked(doctor.check_heartbeat, 5, now=NOW)
    assert any("never run" in m for m in failures(res))


def test_stale_heartbeat_fails(env):
    env.write_heartbeat(age_minutes=20)          # 3 x 5 = 15 min limit
    res = checked(doctor.check_heartbeat, 5, now=NOW)
    assert any("stale" in m for m in failures(res))


def test_fresh_heartbeat_ok(env):
    env.write_heartbeat(age_minutes=4)
    res = checked(doctor.check_heartbeat, 5, now=NOW)
    assert not failures(res)
    assert any("fresh" in msg for level, msg in res if level == "ok")


def test_boundary_exactly_three_intervals_is_ok(env):
    env.write_heartbeat(age_minutes=15)          # == 3 x 5: only OLDER fails
    res = checked(doctor.check_heartbeat, 5, now=NOW)
    assert not failures(res)


def test_interval_scales_the_limit(env):
    env.write_heartbeat(age_minutes=20)
    assert failures(checked(doctor.check_heartbeat, 1, now=NOW))    # limit 3
    assert not failures(checked(doctor.check_heartbeat, 10, now=NOW))  # limit 30


def test_unreadable_heartbeat_fails(env):
    (env.state_file.parent / "tick-heartbeat.json").write_text("{not json",
                                                               encoding="utf-8")
    res = checked(doctor.check_heartbeat, 5, now=NOW)
    assert failures(res)


# ── quiet hours (issue #1 §5, AC 26/28) ────────────────────────────────────────

def test_dose_inside_quiet_hours_fails_and_state_still_valid(env):
    # AC 26: the state loads (validate passes) but doctor FAILs on it
    env.write_state(meds=[make_med(times=["23:30"])])
    safe_write.validate(json.loads(env.state_file.read_text(encoding="utf-8")))
    res = checked(doctor.check_quiet_hours,
                  json.loads(env.state_file.read_text(encoding="utf-8")))
    assert any("inside quiet hours" in m for m in failures(res))


def test_late_nudge_in_muted_quiet_fails(env):
    # 21:00 + 90m = 22:30 = start+30m: the head is start <= t < start+30
    # (exclusive end), so 22:30 is already muted
    env.write_state(meds=[make_med(times=["21:00"], late_threshold=90)])
    state = json.loads(env.state_file.read_text(encoding="utf-8"))
    res = checked(doctor.check_quiet_hours, state)
    assert any("muted" in m for m in failures(res))


def test_late_nudge_in_quiet_head_is_ok(env):
    # AC 28: 21:30 + 30m = 22:00 — first 30 min of quiet hours, still sends
    env.write_state(meds=[make_med(times=["21:30"], late_threshold=30)])
    state = json.loads(env.state_file.read_text(encoding="utf-8"))
    res = checked(doctor.check_quiet_hours, state)
    assert not failures(res)


def test_healthy_schedule_ok(env):
    env.write_state(meds=[make_med(times=["08:00", "20:00"])])
    state = json.loads(env.state_file.read_text(encoding="utf-8"))
    res = checked(doctor.check_quiet_hours, state)
    assert not failures(res)
    assert any("no dose or late nudge" in msg for level, msg in res if level == "ok")


def test_interval_meds_skipped(env):
    env.write_state(meds=[make_med(frequency="interval", interval_hours=8)])
    state = json.loads(env.state_file.read_text(encoding="utf-8"))
    assert not failures(checked(doctor.check_quiet_hours, state))


def test_midnight_wrap_nudge_detected(env):
    # 23:30 + 60m = 00:30 — inside the 22:00-07:00 window, past its head
    env.write_state(meds=[make_med(times=["23:30"], late_threshold=60)])
    state = json.loads(env.state_file.read_text(encoding="utf-8"))
    res = checked(doctor.check_quiet_hours, state)
    assert any("00:30" in m for m in failures(res))


# ── SENDER_DOWN + send_failed (issue #1 §5) ───────────────────────────────────

def test_sender_down_marker_fails(env):
    (env.state_file.parent / "SENDER_DOWN").write_text(
        json.dumps({"since_utc": (NOW - timedelta(hours=1)).isoformat()}),
        encoding="utf-8")
    res = checked(doctor.check_delivery)
    assert any("SENDER_DOWN" in m for m in failures(res))


def test_no_marker_ok(env):
    assert not failures(checked(doctor.check_delivery))


def send_failed_event(ts, stage="reminder", key="2026-10-18T08:00#0", attempt=1):
    return event_store.new_event(
        "med-001", "send_failed", ts,
        occurrence_key=key, occurrence_utc=ts.isoformat(), stage=stage,
        attempt=attempt, error="sender exited 1")


def sent_event(ts, stage="reminder", key="2026-10-18T08:00#0"):
    return event_store.new_event(
        "med-001", "sent", ts, occurrence_key=key,
        occurrence_utc=ts.isoformat(), stage=stage)


def test_outstanding_send_failed_warned(env):
    env.seed([send_failed_event(NOW - timedelta(minutes=10))])
    res = checked(doctor.check_delivery)
    assert any("send(s) failed" in m and "med-001" in m for m in warnings(res))


def test_send_failed_cleared_by_later_sent(env):
    env.seed([
        send_failed_event(NOW - timedelta(minutes=20)),
        sent_event(NOW - timedelta(minutes=10)),
    ])
    res = checked(doctor.check_delivery)
    assert not warnings(res)


def test_retry_then_fail_again_still_outstanding(env):
    env.seed([
        send_failed_event(NOW - timedelta(minutes=30), attempt=1),
        send_failed_event(NOW - timedelta(minutes=10), attempt=2),
    ])
    res = checked(doctor.check_delivery)
    assert any("send(s) failed" in m for m in warnings(res))
