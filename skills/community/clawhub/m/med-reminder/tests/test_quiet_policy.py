"""
schedule.quiet_policy for interval meds (#11).

'shift' (the default) holds an interval dose that lands in quiet hours
until quiet end; 'ignore' reminds on time. Shifting moves only the
announcement: the occurrence key, close instant and next_due anchor stay
on the nominal chain instant. Quiet hours are 22:00–07:00 (make_state).
"""
from datetime import timedelta

import pytest

import tick
from tests.conftest import TZ, local_dt, make_med, make_tick_env, utc

NEXT = timedelta(days=1)


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def interval_med(hours, start_hhmm, policy=None):
    med = make_med(frequency="interval", interval_hours=hours)
    h, m = map(int, start_hhmm.split(":"))
    med["active_since_utc"] = utc(local_dt(h, m)).isoformat()
    if policy is not None:
        med["schedule"]["quiet_policy"] = policy
    return med


def key(local):
    return utc(local).strftime("%Y-%m-%dT%H:%M:%SZ")


def stage_keys(env, stage):
    return [e["occurrence_key"] for e in env.events("send_intent")
            if e["stage"] == stage]


def test_default_policy_is_shift():
    assert tick.quiet_policy(make_med(frequency="interval", interval_hours=8)) == "shift"


# 12h med anchored 11:00 → the 23:00 dose lands in quiet hours

def test_shift_holds_a_quiet_dose_until_quiet_end(env):
    env.write(meds=[interval_med(12, "11:00", "shift")])
    env.run(local_dt(11, 5))
    env.run(local_dt(23, 5))
    assert stage_keys(env, "reminder") == [key(local_dt(11, 0))]
    env.run(local_dt(6, 55) + NEXT)
    assert stage_keys(env, "reminder") == [key(local_dt(11, 0))]
    env.run(local_dt(7, 5) + NEXT)
    # announced at quiet end, still keyed by the nominal 23:00 instant
    assert stage_keys(env, "reminder") == [key(local_dt(11, 0)), key(local_dt(23, 0))]


def test_default_shifts_like_explicit_shift(env):
    env.write(meds=[interval_med(12, "11:00")])
    env.run(local_dt(11, 5))
    env.run(local_dt(23, 5))
    assert key(local_dt(23, 0)) not in stage_keys(env, "reminder")
    env.run(local_dt(7, 5) + NEXT)
    assert key(local_dt(23, 0)) in stage_keys(env, "reminder")


def test_ignore_reminds_on_time_inside_quiet_hours(env):
    env.write(meds=[interval_med(12, "11:00", "ignore")])
    env.run(local_dt(11, 5))
    env.run(local_dt(23, 5))
    assert stage_keys(env, "reminder") == [key(local_dt(11, 0)), key(local_dt(23, 0))]
    env.run(local_dt(7, 5) + NEXT)
    assert stage_keys(env, "reminder").count(key(local_dt(23, 0))) == 1


def test_shift_nudges_count_from_quiet_end(env):
    env.write(meds=[interval_med(12, "11:00", "shift")])
    env.run(local_dt(11, 5))
    env.run(local_dt(23, 5))
    env.run(local_dt(7, 5) + NEXT)
    env.run(local_dt(7, 25) + NEXT)
    nudges = [e for e in env.events("send_intent")
              if tick.is_nudge(e["stage"]) and e["occurrence_key"] == key(local_dt(23, 0))]
    assert nudges == []
    env.run(local_dt(7, 35) + NEXT)          # quiet end 07:00 + 30 min
    nudges = [e for e in env.events("send_intent")
              if tick.is_nudge(e["stage"]) and e["occurrence_key"] == key(local_dt(23, 0))]
    assert len(nudges) == 1


def test_shift_keeps_close_instant_and_anchor_on_the_chain(env):
    env.write(meds=[interval_med(12, "11:00", "shift")])
    env.run(local_dt(11, 5))
    env.run(local_dt(23, 5))
    env.run(local_dt(7, 5) + NEXT)
    # the anchor never moved to quiet end
    assert env.med_state()["next_due"] == utc(local_dt(11, 0)).isoformat()
    env.run(local_dt(10, 55) + NEXT)
    assert key(local_dt(23, 0)) not in [e["occurrence_key"] for e in env.events("missed")]
    env.run(local_dt(11, 5) + NEXT)          # next chain dose closes the held one
    assert key(local_dt(23, 0)) in [e["occurrence_key"] for e in env.events("missed")]
    assert stage_keys(env, "reminder")[-1] == key(local_dt(11, 0) + NEXT)


# 6h med anchored 18:00 → 00:00 and 06:00 both land in one quiet window

def test_shift_announces_only_the_latest_held_dose(env):
    env.write(meds=[interval_med(6, "18:00", "shift")])
    t = local_dt(18, 5)
    while t <= local_dt(7, 30) + NEXT:       # tick every 5 min through the night
        env.run(t)
        t += timedelta(minutes=5)
    assert stage_keys(env, "reminder") == [key(local_dt(18, 0)), key(local_dt(6, 0) + NEXT)]
    missed = [e["occurrence_key"] for e in env.events("missed")]
    assert key(local_dt(0, 0) + NEXT) in missed      # closed at 06:00, silently
    assert not any("While your computer was off" in m for m in env.sent())
    # the held dose shows in the overnight summary instead
    assert any("(12:00am) wasn't logged" in m for m in env.sent())


def test_ignore_reminds_every_dose_in_the_window(env):
    env.write(meds=[interval_med(6, "18:00", "ignore")])
    for t in (local_dt(18, 5), local_dt(0, 5) + NEXT, local_dt(6, 5) + NEXT):
        env.run(t)
    assert stage_keys(env, "reminder") == [
        key(local_dt(18, 0)), key(local_dt(0, 0) + NEXT), key(local_dt(6, 0) + NEXT)]


# anchor initialization (issue §3.3) follows the policy too

def test_init_anchor_shifts_to_quiet_end_under_shift(env):
    env.write(meds=[interval_med(8, "23:00", "shift")])
    env.run(local_dt(23, 5))
    assert env.med_state()["next_due"] == utc(local_dt(7, 0) + NEXT).isoformat()


def test_init_anchor_stays_put_under_ignore(env):
    env.write(meds=[interval_med(8, "23:00", "ignore")])
    env.run(local_dt(23, 5))
    assert env.med_state()["next_due"] == utc(local_dt(23, 0)).isoformat()
    assert stage_keys(env, "reminder") == [key(local_dt(23, 0))]


def test_shift_does_not_touch_scheduled_time_meds():
    med = make_med(frequency="once_daily", times=["23:00"])
    quiet = {"start": "22:00", "end": "07:00"}
    T = utc(local_dt(23, 0))
    assert tick.fire_instant(med, T, quiet, TZ) == T
