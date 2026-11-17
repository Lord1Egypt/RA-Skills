"""
Escalation stage boundaries (issue #1 §3.4) — the tier table the old
resolver tested, now expressed against the tick engine.

For an 08:00 dose with late=30 / missed=90 (digest and quiet hours
parked away so only stage timing decides):
  < 08:00        nothing
  08:00–08:30    reminder
  08:30–09:30    nudge
  ≥ 09:30        missed
Boundaries are inclusive at the threshold instant.
"""
import datetime as dtmod

import pytest

from tests.conftest import local_dt, make_med, make_tick_env


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def med(med_id="med-001"):
    return make_med(med_id=med_id, frequency="once_daily", times=["08:00"])


def stages(env):
    return sorted({e["stage"] for e in env.events("send_intent")})


def test_before_dose_nothing(env):
    env.write(meds=[med()], quiet_start="13:00", quiet_end="14:00", digest_time="23:59")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 59))
    assert env.sent() == [] and env.events() == []


def test_at_dose_time_reminder(env):
    env.write(meds=[med()], quiet_start="13:00", quiet_end="14:00", digest_time="23:59")
    env.run(local_dt(7, 0))
    env.run(local_dt(8, 0))                 # exactly T
    assert env.sent_count("Reminder") == 1


def test_within_grace_reminder_only(env):
    env.write(meds=[med()], quiet_start="13:00", quiet_end="14:00", digest_time="23:59")
    env.run(local_dt(7, 0))
    env.run(local_dt(8, 29))                # 1 min before the late threshold
    assert env.sent_count("Reminder") == 1
    assert env.sent_count("Late:") == 0


def test_exact_late_threshold_nudge(env):
    env.write(meds=[med()], quiet_start="13:00", quiet_end="14:00", digest_time="23:59")
    env.run(local_dt(7, 0))
    env.run(local_dt(8, 30))                # exactly T+late
    assert env.sent_count("Late:") == 1


def test_late_window_nudge(env):
    env.write(meds=[med()], quiet_start="13:00", quiet_end="14:00", digest_time="23:59")
    env.run(local_dt(7, 0))
    env.run(local_dt(9, 29))                # machine off since 07:00
    # only the highest due stage acted: the latest nudge slot (09:00, i.e.
    # T+60) — no reminder, no burst of the skipped 08:30 slot (#11)
    assert stages(env) == ["nudge-60"]


def test_exact_next_dose_closes_missed(env):
    env.write(meds=[med()], quiet_start="13:00", quiet_end="14:00", digest_time="23:59")
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 59) + dtmod.timedelta(days=1))   # 1 min before the next dose
    assert env.events("missed") == []
    env.run(local_dt(8, 0) + dtmod.timedelta(days=1))    # exactly the next dose
    assert len(env.events("missed")) == 1
    assert env.sent_count("Missed:") == 0   # fresh close is silent (#11)


def test_paused_med_no_stages(env):
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"], paused=True)],
              quiet_start="13:00", quiet_end="14:00", digest_time="23:59")
    env.run(local_dt(7, 0))
    env.run(local_dt(9, 30))
    assert env.sent() == [] and env.events() == []


def test_quiet_hours_do_not_block_reminder(env):
    env.write(meds=[med()])                 # default quiet 22:00–07:00
    env.run(local_dt(7, 0))
    env.run(local_dt(8, 5))
    assert env.sent_count("Reminder") == 1
