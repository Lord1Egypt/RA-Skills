"""
safe_write locks, transact, version token, CLI sha, file modes
(issue #1 PR 1, testing-plan row 2).
"""
import hashlib
import io
import json
import os
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

import event_store
import safe_write as sw
from clock import FakeClock
from tests.conftest import iso, local_dt, make_med, make_state

UTC = timezone.utc
NOW = local_dt(10, 0).astimezone(UTC)


@pytest.fixture
def state_file(tmp_path, monkeypatch):
    """Point safe_write's derived paths at tmp_path via STATE_FILE/LOG_FILE."""
    sf = tmp_path / "meds-state.json"
    monkeypatch.setattr(sw, "STATE_FILE", sf)
    monkeypatch.setattr(sw, "LOG_FILE", tmp_path / "safe-write.log")
    return sf


def write_initial(sf, meds=None):
    sf.write_text(json.dumps(make_state(meds=meds if meds is not None else [])),
                  encoding="utf-8")


# ── OS file lock ──────────────────────────────────────────────────────────────

def test_file_lock_acquire_and_release(state_file):
    with sw.file_lock(timeout=1):
        assert sw.lock_file().exists()
    # released → immediately re-acquirable
    with sw.file_lock(timeout=1):
        pass


def test_file_lock_held_raises_after_timeout(state_file, monkeypatch):
    monkeypatch.setattr(sw, "LOCK_WAIT", 0.3)
    held, release = threading.Event(), threading.Event()

    def hold():
        with sw.file_lock():
            held.set()
            release.wait(2)

    t = threading.Thread(target=hold)
    t.start()
    try:
        assert held.wait(1)
        with pytest.raises(RuntimeError, match="Could not acquire lock"):
            with sw.file_lock():
                pass
    finally:
        release.set()
        t.join(3)


def test_file_lock_released_when_body_raises(state_file):
    with pytest.raises(ValueError, match="boom"):
        with sw.file_lock(timeout=1):
            raise ValueError("boom")
    with sw.file_lock(timeout=1):   # lock was freed by the exception path
        pass


def test_file_lock_clears_stale_mkdir_lock(state_file):
    # a leftover pre-PR1 lock *directory* is stale by construction
    sw.lock_file().mkdir()
    with sw.file_lock(timeout=1):
        assert sw.lock_file().is_file()


def test_file_lock_blocks_second_holder_same_process(state_file):
    # flock/LockFile conflicts apply across handles even in one process
    with sw.file_lock(timeout=0.2):
        with pytest.raises(RuntimeError):
            with sw.file_lock(timeout=0.2):
                pass


# ── transact ──────────────────────────────────────────────────────────────────

def taken_event(med_id="med-001", eid="evt-taken-1"):
    from occurrence import at_local
    import datetime as dtmod
    occ = at_local(dtmod.date(2026, 4, 21), "08:00", local_dt(12, 0).tzinfo, index=0)
    return event_store.new_event(
        med_id, "taken", NOW, occurrence=occ,
        id=eid, dose_prescribed="500mg")


def test_transact_commits_state_events_and_mirror(state_file):
    med = make_med(med_id="med-001", history=[
        {"timestamp": iso(local_dt(8, 14)), "event": "taken", "dose_prescribed": "500mg"}])
    write_initial(state_file, meds=[med])

    def fn(state_copy, history_view):
        state_copy["global"]["paused"] = True
        return state_copy, [taken_event()]

    result = sw.transact(fn, clock=FakeClock(NOW))

    assert result["global"]["paused"] is True
    assert result["tick"]["watermark_utc"] == NOW.isoformat()   # migration ran
    on_disk = json.loads(state_file.read_text(encoding="utf-8"))
    assert on_disk["global"]["paused"] is True
    assert on_disk["tick"]["watermark_utc"] == NOW.isoformat()

    events = event_store.load_events(sw.history_file())
    kinds = {(e["event"], e.get("id")) for e in events}
    assert ("taken", "evt-taken-1") in kinds                     # fn's event
    assert any(e["id"].startswith("mig-") for e in events)       # migration events

    # rollback mirror: the new taken event appears once; migration entries
    # (already in state.history) are not duplicated
    hist = on_disk["meds"][0]["state"]["history"]
    assert len([e for e in hist if e["event"] == "taken"]) == 2  # original + mirror


def test_transact_fn_gets_a_copy_and_history_view(state_file):
    write_initial(state_file)
    seen = {}

    def fn(state_copy, history_view):
        seen["state"] = state_copy
        seen["history"] = history_view
        seen["mutated_view"] = list(history_view)
        return state_copy, []

    sw.transact(fn, clock=FakeClock(NOW))
    # mutating the copies after the fact cannot change what was committed
    seen["state"]["global"]["paused"] = True
    seen["mutated_view"].append({"bogus": True})
    on_disk = json.loads(state_file.read_text(encoding="utf-8"))
    assert on_disk["global"]["paused"] is False
    assert event_store.load_events(sw.history_file()) == []


def test_transact_forced_retry_duplicates_nothing(state_file):
    med = make_med(med_id="med-001")
    write_initial(state_file, meds=[med])

    def fn(state_copy, history_view):
        state_copy["global"]["paused"] = True
        return state_copy, [taken_event()]

    sw.transact(fn, clock=FakeClock(NOW))
    sw.transact(fn, clock=FakeClock(NOW))    # forced retry (same ids)

    lines = sw.history_file().read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1                   # one event line, not two


def test_transact_stale_token_rejected(state_file):
    write_initial(state_file)
    token = sw.state_token(state_file)
    # someone else commits between our read and our write
    state = json.loads(state_file.read_text(encoding="utf-8"))
    state["global"]["paused"] = True
    state_file.write_text(json.dumps(state), encoding="utf-8")

    def fn(state_copy, history_view):
        return state_copy, []

    with pytest.raises(RuntimeError, match="Stale version token"):
        sw.transact(fn, clock=FakeClock(NOW), expected_token=token)
    assert json.loads(state_file.read_text(encoding="utf-8"))["global"]["paused"] is True


def test_transact_fresh_token_accepted(state_file):
    write_initial(state_file)
    token = sw.state_token(state_file)

    def fn(state_copy, history_view):
        return state_copy, []

    sw.transact(fn, clock=FakeClock(NOW), expected_token=token)


def test_transact_fn_error_writes_nothing(state_file):
    med = make_med(med_id="med-001")
    write_initial(state_file, meds=[med])
    before = state_file.read_text(encoding="utf-8")

    def fn(state_copy, history_view):
        raise ValueError("pure fn failed")

    with pytest.raises(ValueError, match="pure fn failed"):
        sw.transact(fn, clock=FakeClock(NOW))
    assert state_file.read_text(encoding="utf-8") == before
    assert not sw.history_file().exists()


def test_transact_missing_state_file_raises(state_file):
    with pytest.raises(FileNotFoundError):
        sw.transact(lambda s, h: (s, []), clock=FakeClock(NOW))


# ── version token ─────────────────────────────────────────────────────────────

def test_state_token_matches_file(state_file):
    write_initial(state_file)
    mtime_ns, digest = sw.state_token(state_file)
    assert mtime_ns == state_file.stat().st_mtime_ns
    assert digest == hashlib.sha256(state_file.read_bytes()).hexdigest()


def test_state_token_absent_when_no_file(state_file):
    assert sw.state_token(state_file) == (0, "absent")


def test_load_state_returns_state_and_token(state_file):
    write_initial(state_file)
    state, (mtime_ns, digest) = sw.load_state()
    assert state["version"] == "1"
    assert digest == hashlib.sha256(state_file.read_bytes()).hexdigest()


# ── CLI: --expected-sha256 required and enforced ──────────────────────────────

def run_cli(monkeypatch, argv, payload):
    monkeypatch.setattr(sys, "argv", ["safe_write.py"] + argv)
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))
    sw.main()


def test_cli_requires_expected_sha256(state_file, monkeypatch):
    write_initial(state_file)
    with pytest.raises(SystemExit) as e:
        run_cli(monkeypatch, [], '{"version": "1"}')
    assert e.value.code == 2                # argparse usage error


def test_cli_stale_sha_rejected(state_file, monkeypatch, capsys):
    write_initial(state_file)
    stale = sw.state_token(state_file)[1]
    state_file.write_text(json.dumps(make_state(paused=True)), encoding="utf-8")

    payload = json.dumps(make_state())
    with pytest.raises(SystemExit) as e:
        run_cli(monkeypatch, ["--expected-sha256", stale], payload)
    assert e.value.code == 1
    assert "Stale write token" in capsys.readouterr().err
    assert json.loads(state_file.read_text(encoding="utf-8"))["global"]["paused"] is True


def test_cli_fresh_sha_writes(state_file, monkeypatch):
    write_initial(state_file)
    sha = sw.state_token(state_file)[1]
    payload = json.dumps(make_state(paused=True))
    run_cli(monkeypatch, ["--expected-sha256", sha], payload)
    assert json.loads(state_file.read_text(encoding="utf-8"))["global"]["paused"] is True


def test_cli_absent_token_allows_new_file(state_file, monkeypatch):
    assert not state_file.exists()
    run_cli(monkeypatch, ["--expected-sha256", "absent"], json.dumps(make_state()))
    assert state_file.exists()


def test_cli_absent_token_rejected_when_file_exists(state_file, monkeypatch):
    write_initial(state_file)
    payload = json.dumps(make_state(paused=True))
    with pytest.raises(SystemExit) as e:
        run_cli(monkeypatch, ["--expected-sha256", "absent"], payload)
    assert e.value.code == 1
    assert json.loads(state_file.read_text(encoding="utf-8"))["global"]["paused"] is False


# ── Windows os.replace retry ──────────────────────────────────────────────────

def test_windows_replace_permission_error_retried(state_file, monkeypatch):
    write_initial(state_file)
    real_replace = os.replace
    calls = {"n": 0}

    def flaky_replace(src, dst):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise PermissionError(f"fake AV hold #{calls['n']}")
        return real_replace(src, dst)

    monkeypatch.setattr(sw.os, "replace", flaky_replace)
    monkeypatch.setattr(sw.time, "sleep", lambda s: None)
    sw.safe_write(make_state(paused=True))
    assert calls["n"] == 3                   # 2 failures, then success
    assert json.loads(state_file.read_text(encoding="utf-8"))["global"]["paused"] is True


# ── File modes (POSIX only — Windows chmod is a documented no-op) ─────────────

@pytest.mark.skipif(sys.platform == "win32", reason="POSIX-only: 0600 modes (issue AC 37)")
class TestPosixFileModes:
    def test_written_files_are_private(self, state_file):
        sw.apply_process_umask()
        med = make_med(med_id="med-001")
        write_initial(state_file, meds=[med])

        def fn(state_copy, history_view):
            return state_copy, [taken_event()]

        sw.transact(fn, clock=FakeClock(NOW))
        for p in (state_file, sw.history_file(), sw.tmp_file()):
            if p.exists():
                assert (p.stat().st_mode & 0o777) == 0o600, p
        # backups too
        sw.safe_write(make_state())
        assert (sw.backup_file().stat().st_mode & 0o777) == 0o600

    def test_secure_private_files_fixes_existing(self, state_file):
        write_initial(state_file)
        state_file.chmod(0o644)
        sw.secure_private_files()
        assert (state_file.stat().st_mode & 0o777) == 0o600
