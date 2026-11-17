"""
DST tests for the tick engine (issue #1 §3.3, AC 9-10, 13).

2026-11-01 (America/Los_Angeles): fall back — 01:30 exists twice
(01:30 PDT = 08:30Z, then 01:30 PST = 09:30Z).
2027-03-14: spring forward — 02:30 doesn't exist; it normalizes to
03:30 PDT = 10:30Z. Offsets are absolute (UTC) time.

Quiet hours are parked in the daytime for these tests so muting never
interferes — the ACs under test are about time math, not quiet hours.
"""
import pytest

import event_store
from occurrence import at_local
from tests.conftest import local_dt, make_med, make_tick_env

import datetime as dtmod
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Los_Angeles")
DAYTIME_QUIET = ("13:00", "14:00")   # never covers a dose or nudge here


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def write_env(env, med):
    # quiet parked in the daytime and digest at 23:59 (not yet due at any
    # tick these tests run) so neither can pollute the assertions
    env.write(meds=[med], quiet_start=DAYTIME_QUIET[0], quiet_end=DAYTIME_QUIET[1],
              digest_time="23:59")


def nov(hour, minute=0, day=1):
    return dtmod.datetime(2026, 11, day, hour, minute, tzinfo=TZ)


def mar(hour, minute=0):
    return dtmod.datetime(2027, 3, 14, hour, minute, tzinfo=TZ)


# ── AC 9: fall back (2026-11-01) ──────────────────────────────────────────────

def test_ac9_ambiguous_130_dose_reminds_once_at_first_instance(env):
    write_env(env, make_med(frequency="once_daily", times=["01:30"]))
    env.run(nov(0, 30))                    # warm tick, before the fold
    env.run(nov(1, 35))                    # first tick ≥ 01:30 PDT (08:30Z)
    assert env.sent_count("Reminder") == 1
    env.run(nov(1, 40))                    # second pass: 01:40 PST — same key
    assert env.sent_count("Reminder") == 1
    keys = [e["occurrence_key"] for e in env.events("send_intent")]
    assert keys == ["2026-11-01T01:30#0"]


def test_ac9_nudge_is_absolute_plus_30_from_first_instance(env):
    write_env(env, make_med(frequency="once_daily", times=["01:30"]))
    env.run(nov(0, 30))
    env.run(nov(1, 35))                    # reminder at 01:30 PDT
    # nudge due 01:30 PDT + 30 absolute = 09:00Z = 01:00 PST; the tick at
    # 01:05 PST (fold=1) is past it even though the wall clock went back
    env.run(dtmod.datetime(2026, 11, 1, 1, 5, tzinfo=TZ).replace(fold=1))
    assert env.sent_count("Late:") == 1


def test_ac9_800_dose_fires_at_800_pst(env):
    write_env(env, make_med(frequency="once_daily", times=["08:00"]))
    env.run(nov(7, 0))
    env.run(nov(8, 5))                     # 08:00 PST = 16:00Z
    assert env.sent_count("Reminder") == 1
    intent = env.events("send_intent")[0]
    assert intent["occurrence_utc"] == "2026-11-01T16:00:00+00:00"


# ── AC 10: spring forward (2027-03-14) ────────────────────────────────────────

def test_ac10_nonexistent_230_fires_at_first_tick_past_330(env):
    write_env(env, make_med(frequency="once_daily", times=["02:30"]))
    env.run(mar(1, 0))
    env.run(mar(2, 0))                     # 02:00 PST — dose time doesn't exist yet
    assert env.sent_count("Reminder") == 0
    env.run(mar(3, 35))                    # first tick ≥ 03:30 PDT (10:30Z)
    assert env.sent_count("Reminder") == 1
    intent = env.events("send_intent")[0]
    assert intent["occurrence_utc"] == "2027-03-14T10:30:00+00:00"


def test_ac10_800_dose_fires_at_800_pdt(env):
    write_env(env, make_med(frequency="once_daily", times=["08:00"]))
    env.run(mar(7, 0))
    env.run(mar(8, 5))                     # 08:00 PDT = 15:00Z
    assert env.sent_count("Reminder") == 1
    assert env.events("send_intent")[0]["occurrence_utc"] == "2027-03-14T15:00:00+00:00"


# ── AC 13: interval keys across the fall-back hour ────────────────────────────

def test_ac13_one_hour_interval_across_fallback_no_key_collision(env):
    med = make_med(frequency="interval", interval_hours=1)
    # anchor 00:30 PDT = 07:30Z: chain 07:30Z, 08:30Z (01:30 PDT),
    # 09:30Z (01:30 PST), 10:30Z … distinct UTC keys, no collision
    med["active_since_utc"] = "2026-11-01T07:30:00+00:00"
    write_env(env, med)
    env.run(dtmod.datetime(2026, 10, 31, 23, 0, tzinfo=TZ))   # warm, before DST
    env.run(dtmod.datetime(2026, 11, 1, 1, 35, tzinfo=TZ))                  # 01:35 PDT
    env.run(dtmod.datetime(2026, 11, 1, 1, 35, tzinfo=TZ).replace(fold=1))  # 01:35 PST
    # both 01:30 wall times got their own reminder under distinct UTC keys
    reminders = [e["occurrence_key"] for e in env.events("send_intent")
                 if e["stage"] == "reminder"]
    assert reminders == ["2026-11-01T08:30:00Z", "2026-11-01T09:30:00Z"]


# ── Weekly midnight wrap (AC 11; the weekly-day logic itself is in
#    test_weekly.py) ───────────────────────────────────────────────────────────

def test_weekly_sun_2330_nudge_lands_monday_midnight(env):
    med = make_med(frequency="weekly", times=["23:30"], day_of_week="sun")
    write_env(env, med)
    sun = dtmod.datetime(2026, 4, 19, 23, 0, tzinfo=TZ)       # Sun Apr 19
    env.run(sun)
    env.run(dtmod.datetime(2026, 4, 19, 23, 35, tzinfo=TZ))   # reminder
    env.run(dtmod.datetime(2026, 4, 20, 0, 5, tzinfo=TZ))     # Mon 00:05
    assert env.sent_count("Late:") == 1                       # nudge due Mon 00:00
    env.run(dtmod.datetime(2026, 4, 20, 1, 5, tzinfo=TZ))     # Mon 01:05
    assert env.events("missed") == []                         # still open (#11)
    assert env.sent_count("Late:") == 2                       # 01:00 slot (quiet is daytime here)
    # a weekly dose closes at CLOSE_CAP (25h), not a week later
    env.run(dtmod.datetime(2026, 4, 21, 0, 35, tzinfo=TZ))    # Tue 00:35
    assert len(env.events("missed")) == 1


def test_weekly_wrong_day_never_reminds(env):
    med = make_med(frequency="weekly", times=["09:00"], day_of_week="mon")
    write_env(env, med)
    env.run(dtmod.datetime(2026, 4, 20, 8, 55, tzinfo=TZ))    # Monday warm tick
    # Monday's dose was taken — Tuesday must produce nothing at all
    env.seed([event_store.new_event(
        "med-001", "taken", dtmod.datetime(2026, 4, 20, 9, 10, tzinfo=TZ),
        occurrence=at_local(dtmod.date(2026, 4, 20), "09:00", TZ, 0))])
    env.run(dtmod.datetime(2026, 4, 21, 9, 5, tzinfo=TZ))     # Tuesday
    assert env.sent() == []
    assert env.events("missed") == []
