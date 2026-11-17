"""
Send lease tests (issue #1 §3.6, AC 23-25): at-least-once delivery with
a 5-minute lease, retries after unknown outcomes prefixed "(repeat …)",
backoff on known failures until the missed deadline, the SENDER_DOWN
marker, and plain (never prefixed) messages once sends recover (#21).
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

import event_store
import tick
from occurrence import at_local
from tests.conftest import local_dt, make_med, make_tick_env, TZ, utc

import datetime as dtmod

TUE = dtmod.date(2026, 4, 21)
REPO = Path(__file__).resolve().parent.parent


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def once_daily():
    return make_med(med_id="med-001", frequency="once_daily", times=["08:00"])


def intent_for(env, stage="reminder"):
    return [e for e in env.events("send_intent") if e["stage"] == stage]


# ── Lease basics ───────────────────────────────────────────────────────────────

def test_intent_lease_written_under_transact_before_sending(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    intents = intent_for(env)
    assert len(intents) == 1
    assert intents[0]["attempt"] == 1
    lease = event_store and __import__("clock").parse_instant(intents[0]["lease_until_utc"])
    assert lease == utc(local_dt(8, 10))     # now + 5 min
    assert env.sent_count("Reminder") == 1


def test_unexpired_lease_is_not_retried(env):
    # an in-flight send (lease active, no sent yet) must not be re-sent
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    env.sent_file.write_text("", encoding="utf-8")   # hide it from the count
    env.run(local_dt(8, 6))                 # 1 min later: lease still held
    assert env.sent() == []


# ── AC 23: crash between send and record → exactly one more, prefixed ────────

def seed_crashed_intent(env):
    """
    Reproduce a kill -9 between the send and its `sent` record: an intent
    with an EXPIRED lease and no sent/send_failed after it (strip the
    `sent` lines — exactly the state a dead process leaves behind).
    """
    import safe_write as sw
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    assert env.sent_count("Reminder") == 1
    hist = sw.history_file()
    kept = [json.dumps(e, ensure_ascii=False) for e in env.events()
            if e["event"] != "sent"]
    hist.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")


def test_ac23_expired_lease_unknown_outcome_retries_once_with_prefix(env):
    seed_crashed_intent(env)
    env.sent_file.write_text("", encoding="utf-8")
    env.run(local_dt(8, 11))                # lease expired, outcome unknown
    msgs = env.sent()
    assert len(msgs) == 1
    assert msgs[0].startswith("(repeat — ignore if you already got this)")
    intents = intent_for(env)
    assert [i["attempt"] for i in intents] == [1, 2]
    # the retry recorded `sent` → a third tick does nothing
    env.run(local_dt(8, 17))
    assert len(env.sent()) == 1


def test_ac23_real_process_killed_between_send_and_record(tmp_path):
    """
    The real thing: dispatch.py tick in a subprocess whose sender DELIVERS
    and then hangs (FAKE_SEND_TRIP) — kill -9 the tree while the tick is
    blocked in the send, before the record phase. The next tick (fresh
    process, 6 min later, lease expired) sends exactly one repeat.
    """
    from tests.conftest import make_state

    sf = tmp_path / "meds-state.json"
    sf.write_text(json.dumps(make_state(
        digest_time="23:59",
        meds=[make_med(med_id="med-001", frequency="once_daily", times=["08:00"])])),
        encoding="utf-8")
    out = tmp_path / "sent.txt"
    trip_flag = tmp_path / "trip-on"

    env_vars = dict(os.environ)
    env_vars.update({
        "MEDS_TEST": "1",
        "MEDS_SEND_CMD": f'"{sys.executable}" "{REPO / "tests" / "fake_sender.py"}"',
        "FAKE_SEND_OUT": str(out),
        "FAKE_SEND_SLEEP": str(tmp_path / "sleep-absent"),
        "FAKE_SEND_FAIL": str(tmp_path / "fail-absent"),
        "FAKE_SEND_TRIP": str(tmp_path / "trip-absent"),
    })

    def run_tick(fake_now):
        env_vars["MEDS_FAKE_NOW"] = fake_now
        return subprocess.run(
            [sys.executable, str(REPO / "dispatch.py"), "--state", str(sf), "tick"],
            capture_output=True, text=True, timeout=90,
            cwd=str(REPO), env=env_vars)

    # seed the watermark with an earlier, uneventful tick
    assert run_tick("2026-04-21T07:00:00-07:00").returncode == 0

    # this tick delivers, then blocks in the sender for 30s
    trip_flag.write_text("30", encoding="utf-8")
    env_vars["FAKE_SEND_TRIP"] = str(trip_flag)
    env_vars["MEDS_FAKE_NOW"] = "2026-04-21T08:05:00-07:00"
    p = subprocess.Popen(
        [sys.executable, str(REPO / "dispatch.py"), "--state", str(sf), "tick"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        cwd=str(REPO), env=env_vars)
    try:
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if out.exists() and "Reminder" in out.read_text(encoding="utf-8"):
                break
            time.sleep(0.02)
        else:
            pytest.fail("sender never delivered the reminder")
        kill_tree(p)                        # kill -9 between send and record
    finally:
        trip_flag.unlink(missing_ok=True)
        env_vars["FAKE_SEND_TRIP"] = str(tmp_path / "trip-absent")

    msgs = [m for m in out.read_text(encoding="utf-8").split("\n---\n") if m]
    assert len(msgs) == 1                   # delivered exactly once

    # next tick, 6 minutes later in a fresh process: one repeat send
    r = run_tick("2026-04-21T08:11:00-07:00")
    assert r.returncode == 0, r.stderr
    msgs = [m for m in out.read_text(encoding="utf-8").split("\n---\n") if m]
    assert len(msgs) == 2
    assert msgs[1].startswith("(repeat — ignore if you already got this)")

    # and it settled: another tick sends nothing more
    run_tick("2026-04-21T08:20:00-07:00")
    msgs = [m for m in out.read_text(encoding="utf-8").split("\n---\n") if m]
    assert len(msgs) == 2


def kill_tree(p):
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)],
                       capture_output=True)
    else:
        import signal
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)


# ── AC 24: hung sender → timeout, send_failed, retried next tick ──────────────

def test_ac24_hung_sender_times_out_and_is_retried(env, monkeypatch):
    monkeypatch.setattr(tick, "SEND_TIMEOUT", 1)
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.sleep_sends(8)                      # far beyond the 1s timeout
    env.run(local_dt(8, 5))
    assert env.sent() == []                 # nothing delivered
    failed = env.events("send_failed")
    assert len(failed) == 1 and failed[0]["stage"] == "reminder"
    assert "timed out" in failed[0]["error"]
    assert (env.state_file.parent / "SENDER_DOWN").exists()

    # healed; the 5-minute backoff has elapsed at 08:11 → retry succeeds
    env.wake_sends()
    env.run(local_dt(8, 11))
    assert env.sent_count("Reminder") == 1
    assert env.events("sent")[-1]["stage"] == "reminder"


def test_ac24_failed_retry_respects_backoff(env, monkeypatch):
    monkeypatch.setattr(tick, "SEND_TIMEOUT", 1)
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.sleep_sends(8)
    env.run(local_dt(8, 5))                 # attempt 1 fails
    env.wake_sends()
    env.run(local_dt(8, 8))                 # 3 min later: still backing off
    assert env.sent() == []
    env.run(local_dt(8, 11))                # 6 min later: retried
    assert env.sent_count("Reminder") == 1


def test_tick_lock_prevents_overlap(env):
    import safe_write as sw
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    with sw.file_lock(timeout=1, _path=tick.tick_lock_file()):
        assert env.run(local_dt(8, 5)) == 0  # exits silently, no work done
    assert env.sent() == []
    env.run(local_dt(8, 6))                 # lock free again → works
    assert env.sent_count("Reminder") == 1


# ── AC 25: outage window → SENDER_DOWN marker, cleared on recovery ────────────

def test_ac25_sender_down_marker_cleared_on_recovery(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.fail_sends()
    env.run(local_dt(8, 5))                 # reminder attempt 1 fails, marker
    marker = env.state_file.parent / "SENDER_DOWN"
    assert marker.exists()
    assert "since_utc" in json.loads(marker.read_text(encoding="utf-8"))

    env.run(local_dt(8, 11))                # reminder attempt 2 (backoff done)
    env.run(local_dt(8, 22))                # attempt 3
    env.run(local_dt(8, 43))                # nudge (due 08:30) fires and fails
                                            # too — escalation continues, and
                                            # the reminder retry is superseded
    stages = sorted(e["stage"] for e in env.events("send_failed"))
    assert stages == ["nudge", "reminder", "reminder", "reminder"]
    assert marker.exists()

    env.heal_sends()
    env.run(local_dt(9, 25))                # first success after the outage
    msgs = env.sent()
    assert len(msgs) == 1                   # nudge supersedes the reminder retry
    # #21: never prefixed with an outage note — the highest due stage's
    # message goes out as itself
    assert msgs[0].startswith("Late: Metformin")
    assert not marker.exists()              # marker cleared on success


def test_ac25_retries_stop_after_the_missed_deadline(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.fail_sends()
    env.run(local_dt(8, 5))
    env.run(local_dt(8, 11))
    env.run(local_dt(8, 22))
    # long after the occurrence's missed deadline (the next dose, 08:00
    # tomorrow — #11): today's reminder and nudge retries are dropped
    env.run(local_dt(13, 0) + timedelta(days=1))
    assert env.sent() == []
    assert len(env.events("missed")) == 1
    today = "2026-04-21T08:00#0"
    intents = [e for e in env.events("send_intent")
               if e["occurrence_key"] == today
               and (e["stage"] == "reminder" or e["stage"].startswith("nudge"))]
    assert all(int(e.get("attempt") or 1) <= 3 for e in intents), \
        "no stage retries past the missed deadline"
    assert (env.state_file.parent / "SENDER_DOWN").exists()
