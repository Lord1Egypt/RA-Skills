"""
#11 escalation rework: nudges repeat every late_threshold_minutes until the
dose is taken, skipped, snoozed ("pause N"), or closed as missed when the
med's next dose arrives (at most occurrence.CLOSE_CAP after it was due).
"""
import datetime as dtmod
import json

import pytest

import event_store
import occurrence
from clock import FakeClock
from occurrence import at_local
from reply import handle_confirm, handle_skip, handle_snooze
from tests.conftest import TZ, local_dt, make_med, make_tick_env, utc

TUE = dtmod.date(2026, 4, 21)


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def day(n, h, m=0):
    return local_dt(h, m) + dtmod.timedelta(days=n)


def tick_every_5(env, start, end):
    t = start
    while t <= end:
        env.run(t)
        t += dtmod.timedelta(minutes=5)


def nudge_stages(env):
    return [e["stage"] for e in env.events("send_intent")
            if e["stage"].startswith("nudge")]


# ── close_instant ─────────────────────────────────────────────────────────────

def test_close_at_next_daily_dose():
    sched = {"frequency": "once_daily", "times": ["08:00"]}
    T = at_local(TUE, "08:00", TZ).utc
    assert occurrence.close_instant(sched, T, TZ) == utc(day(1, 8))


def test_close_at_next_dose_same_day():
    sched = {"frequency": "twice_daily", "times": ["08:00", "20:00"]}
    T = at_local(TUE, "08:00", TZ).utc
    assert occurrence.close_instant(sched, T, TZ) == utc(local_dt(20))


def test_weekly_dose_closes_at_the_cap_not_next_week():
    sched = {"frequency": "weekly", "times": ["08:00"], "day_of_week": "tue"}
    T = at_local(TUE, "08:00", TZ).utc
    assert occurrence.close_instant(sched, T, TZ) == T + occurrence.CLOSE_CAP


def test_interval_closes_at_next_interval_dose():
    sched = {"frequency": "interval", "interval_hours": 6}
    T = utc(local_dt(8))
    assert occurrence.close_instant(sched, T, TZ) == T + dtmod.timedelta(hours=6)


def test_daily_dose_across_dst_fall_back_closes_at_next_dose():
    # Nov 1 2026 is a 25h day in Los Angeles — the cap must not cut it short
    sched = {"frequency": "once_daily", "times": ["08:00"]}
    T = at_local(dtmod.date(2026, 10, 31), "08:00", TZ).utc
    nxt = at_local(dtmod.date(2026, 11, 1), "08:00", TZ).utc
    assert nxt - T == dtmod.timedelta(hours=25)
    assert occurrence.close_instant(sched, T, TZ) == nxt


# ── cadence ───────────────────────────────────────────────────────────────────

def test_nudges_repeat_every_30_minutes(env):
    env.write(meds=[make_med(times=["08:00"])])
    tick_every_5(env, local_dt(7, 55), local_dt(10, 5))
    assert env.sent_count("Reminder") == 1
    assert env.sent_count("Late:") == 4               # 08:30 09:00 09:30 10:00
    assert nudge_stages(env) == ["nudge", "nudge-60", "nudge-90", "nudge-120"]


def test_custom_interval(env):
    env.write(meds=[make_med(times=["08:00"], late_threshold=45)])
    tick_every_5(env, local_dt(7, 55), local_dt(10, 5))
    assert nudge_stages(env) == ["nudge", "nudge-90"]   # 08:45, 09:30


def test_missed_threshold_is_ignored(env):
    env.write(meds=[make_med(times=["08:00"], missed_threshold=60)])
    tick_every_5(env, local_dt(7, 55), local_dt(10, 5))
    assert env.events("missed") == []
    assert env.sent_count("Late:") == 4


def test_no_burst_after_the_machine_sleeps(env):
    env.write(meds=[make_med(times=["08:00"])])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    env.run(local_dt(11, 10))                         # slept 08:05–11:10
    assert env.sent_count("Late:") == 1               # only the 11:00 slot
    assert nudge_stages(env) == ["nudge-180"]


def test_each_slot_sends_once_across_ticks(env):
    env.write(meds=[make_med(times=["08:00"])])
    env.run(local_dt(7, 55))
    for m in (31, 35, 40, 45, 50, 55):
        env.run(local_dt(8, m))
    assert env.sent_count("Late:") == 1


# ── the four exits ────────────────────────────────────────────────────────────

def test_taken_stops_the_nudges(env):
    env.write(meds=[make_med(times=["08:00"])])
    tick_every_5(env, local_dt(7, 55), local_dt(9, 5))
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(9, 10)))
    tick_every_5(env, local_dt(9, 15), local_dt(12, 0))
    assert env.sent_count("Late:") == 2               # 08:30, 09:00
    env.run(day(1, 8, 5))
    assert env.events("missed") == []


def test_partial_dose_counts_as_taken(env, capsys):
    env.write(meds=[make_med(times=["08:00"])])
    tick_every_5(env, local_dt(7, 55), local_dt(8, 35))
    handle_confirm("med-001", "250mg", dry_run=False, clock=FakeClock(local_dt(8, 40)))
    tick_every_5(env, local_dt(8, 45), local_dt(11, 0))
    assert env.sent_count("Late:") == 1
    assert env.events("taken")[0]["dose_taken"] == "250mg"


def test_skip_stops_the_nudges(env):
    env.write(meds=[make_med(times=["08:00"])])
    tick_every_5(env, local_dt(7, 55), local_dt(8, 35))
    handle_skip("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 40)))
    tick_every_5(env, local_dt(8, 45), local_dt(12, 0))
    assert env.sent_count("Late:") == 1
    env.run(day(1, 8, 5))
    assert env.events("missed") == []                 # skipped is never missed


def test_pause_silences_then_restarts_the_cadence(env):
    env.write(meds=[make_med(times=["08:00"])])
    tick_every_5(env, local_dt(7, 55), local_dt(8, 35))     # reminder + 08:30 nudge
    handle_snooze("med-001", 90, dry_run=False, clock=FakeClock(local_dt(8, 40)))
    tick_every_5(env, local_dt(8, 45), local_dt(10, 5))
    assert env.sent_count("Late:") == 1               # silent 08:40–10:10
    tick_every_5(env, local_dt(10, 10), local_dt(11, 15))
    assert env.sent_count("snoozed") == 1             # wake at 10:10
    assert env.sent_count("Late:") == 3               # 10:40, 11:10


def test_next_dose_closes_silently_and_reminds(env):
    env.write(meds=[make_med(frequency="twice_daily", times=["08:00", "14:00"])])
    tick_every_5(env, local_dt(7, 55), local_dt(14, 0))
    missed = env.events("missed")
    assert [m["occurrence_key"] for m in missed] == ["2026-04-21T08:00#0"]
    assert env.sent_count("Missed:") == 0
    assert env.sent_count("Reminder") == 2
    # the 08:00 dose's last nudge was 13:30 — nothing for it at/after 14:00
    assert env.sent_count("Late:") == 11              # 08:30 … 13:30


def test_interval_med_closes_at_the_next_interval_dose(env):
    med = make_med(frequency="interval", interval_hours=4)
    med["active_since_utc"] = utc(local_dt(8)).isoformat()
    env.write(meds=[med])
    tick_every_5(env, local_dt(8, 0), local_dt(12, 5))
    assert [m["occurrence_key"] for m in env.events("missed")] == [
        "2026-04-21T15:00:00Z"]
    assert env.sent_count("Reminder") == 2


# ── storage ───────────────────────────────────────────────────────────────────

def test_repeat_nudge_stage_validates():
    occ = at_local(TUE, "08:00", TZ)
    event_store.new_event("med-001", "send_intent", utc(local_dt(9)),
                          occurrence=occ, stage="nudge-60")
    with pytest.raises(ValueError):
        event_store.new_event("med-001", "send_intent", utc(local_dt(9)),
                              occurrence=occ, stage="nudge-x")


def test_repeat_nudge_mirrors_as_legacy_late_nudge():
    occ = at_local(TUE, "08:00", TZ)
    e = event_store.new_event("med-001", "sent", utc(local_dt(9)),
                              occurrence=occ, stage="nudge-60")
    assert event_store.mirror_entry(e)["event"] == "late_nudge_sent"


def test_stale_nudge_retry_dropped_after_its_slot(env):
    env.write(meds=[make_med(times=["08:00"])])
    tick_every_5(env, local_dt(7, 55), local_dt(8, 25))
    env.fail_sends()
    env.run(local_dt(8, 30))                          # 08:30 nudge fails
    env.heal_sends()
    env.run(local_dt(9, 5))                           # 09:00 slot is due
    late = [m for m in env.sent() if "Late:" in m]
    assert len(late) == 1                             # the 09:00 nudge only
    assert not late[0].startswith("(repeat")
