"""
Integration tests (issue #1 PR 2): a simulated day of 5-minute ticks
(AC 7, 14, 16) and a confirm racing a live tick (AC 31).
"""
import json
import threading
from datetime import timedelta

import pytest

import event_store
import safe_write as sw
import tick
from clock import FakeClock
from occurrence import at_local, at_utc
from reply import handle_confirm
from tests.conftest import local_dt, make_med, make_tick_env, TZ, utc

import datetime as dtmod

TUE = dtmod.date(2026, 4, 21)


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def seed_taken(env, med_id, hhmm, day=TUE, index=0, at=None):
    """Scripted confirm: taken event for a wall-time occurrence."""
    occ = at_local(day, hhmm, TZ, index)
    taken_at = at if at is not None else occ.utc + timedelta(minutes=10)
    env.seed([event_store.new_event(
        med_id, "taken", taken_at, occurrence=occ,
        taken_at_utc=taken_at.astimezone(dtmod.timezone.utc).isoformat())])


# ── Simulated day: 288 five-minute ticks over Tue Apr 21 2026 ─────────────────

def test_simulated_day_of_5_minute_ticks(env):
    """
    Two meds, a full day of ticks at the real cadence, scripted confirms
    and a machine-off window. Every scheduled contact happens exactly
    once; unresolved doses are nudged on the 30-min cadence until quiet
    hours mute them, and the off-window's dose is picked up by its nudge
    when the machine wakes (AC 7, 16; #11).
    """
    m1 = make_med(med_id="med-001", name="Metformin",
                  frequency="twice_daily", times=["08:00", "20:00"])
    m2 = make_med(med_id="med-002", name="Theophylline",
                  frequency="interval", interval_hours=6)
    m2["state"]["next_due"] = utc(local_dt(6, 0)).isoformat()
    # 06:00 is inside quiet hours: 'ignore' keeps it reminded on time
    # (the 'shift' default is covered in test_quiet_policy.py)
    m2["schedule"]["quiet_policy"] = "ignore"
    env.write(meds=[m1, m2], digest_time="07:30")

    # interval occurrences keyed by UTC instant: 06:00, 12:00, 18:00 local
    occ_0600 = at_utc(utc(local_dt(6, 0)), TZ)
    occ_1200 = at_utc(utc(local_dt(12, 0)), TZ)
    scripted = {   # (hour, minute) → taken event to seed before that tick
        (8, 10): ("med-001", at_local(TUE, "08:00", TZ, 0)),
        (6, 10): ("med-002", occ_0600),
        (12, 10): ("med-002", occ_1200),
    }
    off_lo, off_hi = local_dt(17, 55), local_dt(20, 0)

    now = local_dt(0, 0)
    for _ in range(288):                     # 00:00 → 23:55, every 5 min
        script = scripted.get((now.hour, now.minute))
        if script:
            med_id, occ = script
            env.seed([event_store.new_event(
                med_id, "taken", now, occurrence=occ,
                taken_at_utc=utc(now).isoformat())])
        if not (off_lo <= now < off_hi):     # machine "on"
            env.run(now)
        now += timedelta(minutes=5)

    msgs = env.sent()

    # med-001: morning reminded + taken (no escalation); evening reminded
    # (never confirmed) → nudges 20:30, 21:00, 21:30 and 22:00 (first 30 min
    # of quiet hours), then muted; it stays open until tomorrow's 08:00
    assert len([m for m in msgs if "Metformin" in m and "Reminder" in m]) == 2
    assert len([m for m in msgs if "Late: Metformin" in m]) == 4
    assert not any("Missed:" in m for m in msgs)

    # med-002 (6h from 06:00): 06:00 and 12:00 reminded and taken; the
    # 18:00 dose fell inside the off window → still open when the machine
    # woke at 20:00, so its nudge (slot 20:00) is the first contact, then
    # 20:30 … 22:00; it closes at the next dose (00:00), after the loop
    assert len([m for m in msgs if "Theophylline" in m and "Reminder" in m]) == 2
    assert len([m for m in msgs if "Late: Theophylline" in m]) == 5
    assert not any("wasn't logged" in m for m in msgs)

    # digest exactly once
    assert len([m for m in msgs if "Meds for" in m]) == 1

    # every intent got exactly one delivered send; no stage fired twice
    intents, sents = env.events("send_intent"), env.events("sent")
    assert len(intents) == len(sents)
    assert len({e["id"] for e in intents}) == len(intents)
    seen = set()
    for e in intents:
        k = (e["med_id"], e["occurrence_key"], e["stage"])
        assert k not in seen, k
        seen.add(k)

    # state valid; both evening doses still open, so the watermark trails
    # the oldest of them (18:00) and nothing is logged missed yet
    json.loads(env.state_file.read_text(encoding="utf-8"))
    assert env.heartbeat()["watermark_utc"] == \
        utc(local_dt(18, 0) - timedelta(seconds=1)).isoformat()
    assert env.events("missed") == []


# ── AC 31: a confirm racing a tick is not lost ────────────────────────────────

def test_confirm_waits_for_the_state_lock_and_commits(env):
    """A tick (or any writer) holding the lock delays — not loses — a confirm."""
    import dispatch
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])])
    env.run(local_dt(7, 55))
    released = threading.Event()
    held = threading.Event()

    def hold():
        with sw.file_lock(timeout=5):
            held.set()
            released.wait(5)

    t = threading.Thread(target=hold)
    t.start()
    try:
        assert held.wait(2)
        handle_confirm("med-001", None, dry_run=False,
                       clock=FakeClock(local_dt(8, 14)))
    finally:
        released.set()
        t.join(5)
    taken = env.events("taken")
    assert len(taken) == 1 and taken[0]["occurrence_key"] == "2026-04-21T08:00#0"


def test_confirm_racing_a_live_tick_both_land(env):
    """
    A tick is mid-send (slow sender) while the user confirms. The tick's
    send does not clobber the confirm: both commit, the state file stays
    valid, and the occurrence ends taken.
    """
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])])
    env.run(local_dt(7, 55))
    env.sleep_sends(1.5)                   # slow but under the 60s timeout

    done = threading.Event()
    errors = []

    def run_the_tick():
        try:
            env.run(local_dt(8, 5))         # reminder send takes ~1.5s
        except Exception as e:              # pragma: no cover
            errors.append(e)
        finally:
            done.set()

    t = threading.Thread(target=run_the_tick)
    t.start()
    import time as _time
    _time.sleep(0.4)                        # tick is now blocked in the sender
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 6)))
    assert done.wait(10)
    t.join(10)
    assert errors == []

    # both effects landed: the reminder was sent AND the dose is taken
    assert env.sent_count("Reminder") == 1
    taken = env.events("taken")
    assert len(taken) == 1 and taken[0]["occurrence_key"] == "2026-04-21T08:00#0"
    # state file intact and parseable
    st = json.loads(env.state_file.read_text(encoding="utf-8"))
    assert st["meds"][0]["state"]["status"] == "confirmed"
