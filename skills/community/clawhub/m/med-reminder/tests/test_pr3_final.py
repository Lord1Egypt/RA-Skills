"""
PR 3 end-to-end tests (issue #1 §5 + §7): the pieces from separate units
working together, still with every OS interaction faked.

- migrate → doctor agree: after a legacy crontab migrates, doctor's
  scheduler + heartbeat checks pass on the same artifacts; before the
  heartbeat exists (or once stale), doctor FAILs (AC 35).
- Windows: the same loop through folder enumeration (AC 34).
- Redaction runs through a real tick: a failing sender whose stderr
  names the med leaves only the med id in dispatch.log, and the
  send_failed/SENDER_DOWN path doctor reports is produced by the tick
  itself (AC 36 + §5 delivery checks).
"""
import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import doctor
from tests.conftest import load_setup_tasks, make_med, make_tick_env
from tests.test_scheduler_migration import FakeOs, FOREIGN, legacy_block

setup_tasks = load_setup_tasks()
NOW = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    sf = tmp_path / "meds-state.json"
    sf.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(setup_tasks, "STATE_FILE", sf)
    monkeypatch.setattr(setup_tasks, "SCRIPT_DIR", tmp_path)
    monkeypatch.setattr(setup_tasks, "LEGACY_REGISTRY_FILE",
                        tmp_path / ".registered-tasks.json")
    return sf


def migrate_on(state_file, fake, platform_name="linux", scheduler="cron"):
    old = sys.platform
    sys.platform = platform_name
    try:
        return setup_tasks.migrate(setup_tasks.state_hash(state_file), state_file,
                                   5, scheduler, run=fake)
    finally:
        sys.platform = old


def doctor_checks(monkeypatch, state_file, fake, platform_name, now=NOW):
    """Run doctor's scheduler + heartbeat checks against the faked OS."""
    monkeypatch.setattr(doctor, "STATE_FILE", state_file)
    monkeypatch.setattr(doctor, "_run", fake)
    monkeypatch.setattr(sys, "platform", platform_name)
    doctor.results.clear()
    doctor.check_scheduler()
    doctor.check_heartbeat(doctor.tick_minutes_for_state(), now=now)
    return doctor.results


def failures(results):
    return [msg for level, msg in results if level == "fail"]


# ── migration and doctor agree (AC 35) ─────────────────────────────────────────

def test_after_migration_doctor_is_healthy(sandbox, monkeypatch):
    flag = str(Path(sandbox).resolve())
    fake = FakeOs(crontab=FOREIGN + legacy_block(flag))
    assert migrate_on(sandbox, fake) == 0

    # no heartbeat yet → the tick has never run → doctor FAILs
    results = doctor_checks(monkeypatch, sandbox, fake, "linux")
    assert any("never run" in m for m in failures(results))

    # the tick runs: heartbeat appears, fresh → no failures at all
    (sandbox.parent / "tick-heartbeat.json").write_text(json.dumps({
        "started_utc": NOW.isoformat(), "ended_utc": NOW.isoformat(),
        "watermark_utc": NOW.isoformat(), "errors": 0}), encoding="utf-8")
    results = doctor_checks(monkeypatch, sandbox, fake, "linux")
    assert not failures(results)


def test_stale_heartbeat_after_registration_fails_doctor(sandbox, monkeypatch):
    fake = FakeOs(crontab=[])
    assert migrate_on(sandbox, fake) == 0
    (sandbox.parent / "tick-heartbeat.json").write_text(json.dumps({
        "started_utc": (NOW - timedelta(hours=2)).isoformat(),
        "ended_utc": (NOW - timedelta(hours=2)).isoformat(),
        "watermark_utc": (NOW - timedelta(hours=2)).isoformat(),
        "errors": 0}), encoding="utf-8")
    results = doctor_checks(monkeypatch, sandbox, fake, "linux")
    assert any("stale" in m for m in failures(results))


def test_two_states_doctor_reads_only_its_own_tick(sandbox, tmp_path, monkeypatch):
    other = tmp_path / "meds-state-b.json"
    other.write_text("{}", encoding="utf-8")
    fake = FakeOs(crontab=[])
    assert migrate_on(sandbox, fake) == 0        # A registered
    # doctor on B (never migrated): B's hash has no block → FAIL
    results = doctor_checks(monkeypatch, other, fake, "linux")
    assert any("tick block missing" in m for m in failures(results))


# ── Windows: enumeration migration + doctor (AC 34) ────────────────────────────

def test_windows_migration_then_doctor_clean(sandbox, monkeypatch):
    fake = FakeOs(tasks={
        "\\MedReminder\\fire_med-001_0": True,
        "\\MedReminder\\miss_med-001_0": True,
        "\\MedReminder\\digest": True,
    })
    assert migrate_on(sandbox, fake, platform_name="win32") == 0
    results = doctor_checks(monkeypatch, sandbox, fake, "win32")
    # heartbeat still missing → that's the only failure; no legacy failure
    fails = failures(results)
    assert len(fails) == 1 and "never run" in fails[0]


# ── redaction through a real tick (AC 36 + §5 delivery reporting) ─────────────

@pytest.fixture
def fresh_root():
    root = logging.getLogger()
    saved = root.handlers[:]
    root.handlers.clear()
    yield root
    for h in root.handlers[:]:
        root.removeHandler(h)
        h.close()
    root.handlers.extend(saved)


def test_tick_send_failure_redacts_and_doctor_reports(tmp_path, monkeypatch,
                                                      fresh_root):
    import dispatch
    import tick
    from clock import FakeClock
    from tests.conftest import make_state

    env = make_tick_env(tmp_path, monkeypatch)
    state = make_state(meds=[make_med(name="Metformin", times=["08:00"])])
    # watermark at 14:00Z so the 08:00 PDT (15:00Z) occurrence is enumerated
    state["tick"] = {"watermark_utc": "2026-04-21T14:00:00+00:00"}
    env.state_file.write_text(json.dumps(state), encoding="utf-8")

    monkeypatch.setenv("MEDS_LOG_REDACT", "1")
    logfile = tmp_path / "dispatch.log"
    monkeypatch.setattr(dispatch, "LOG_FILE", logfile)
    fresh_root.handlers.clear()
    dispatch.setup_logging(False)

    # failing sender whose stderr names the med — exactly what AC 36 bans
    sender = f'"{sys.executable}" -c "import sys; ' \
             f"sys.stderr.write('Metformin sender blew up'); sys.exit(1)\""
    monkeypatch.setattr(dispatch, "SEND_CMD", sender)

    # 08:00 America/Los_Angeles = 15:00Z; tick at 15:05 → reminder send fails
    tick.run_tick(dry_run=False,
                  clock=FakeClock(datetime(2026, 4, 21, 15, 5, tzinfo=timezone.utc)),
                  tick_minutes=5)

    log_text = logfile.read_text(encoding="utf-8")
    assert "Metformin" not in log_text
    assert "med-001" in log_text
    assert (tmp_path / "SENDER_DOWN").exists()
    assert env.events("send_failed")

    monkeypatch.setattr(doctor, "STATE_FILE", env.state_file)
    doctor.results.clear()
    doctor.check_delivery()
    assert any(level == "fail" and "SENDER_DOWN" in msg
               for level, msg in doctor.results)
    assert any("send(s) failed" in m and "med-001" in m
               for level, m in doctor.results if level == "warn")
