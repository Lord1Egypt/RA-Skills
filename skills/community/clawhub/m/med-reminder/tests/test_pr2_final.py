"""
Final PR 2 coverage: the legacy-wrapper contract, --tick-minutes,
AC 26 (a dose inside quiet hours loads/ticks/confirms) and AC 29's
skipped-shown-separarily digest line.
"""
from datetime import timedelta
from unittest.mock import patch

import pytest

import dispatch
import event_store
import tick
from clock import FakeClock
from occurrence import at_local
from reply import handle_confirm
from tests.conftest import local_dt, make_med, make_tick_env, TZ, utc

import datetime as dtmod

TUE = dtmod.date(2026, 4, 21)


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


# ── Legacy subcommands are tick-only wrappers (issue §3.10) ──────────────────

@pytest.mark.parametrize("call", [
    lambda dr: dispatch.handle_fire("med-001", 0, dr),
    lambda dr: dispatch.handle_check("med-001", 0, dr),
    lambda dr: dispatch.handle_miss("med-001", 0, dr),
    lambda dr: dispatch.handle_digest(dr),
    lambda dr: dispatch.handle_reset_deferred(dr),
])
def test_legacy_subcommands_only_call_tick(call):
    ran = []
    with patch.object(tick, "run_tick", side_effect=lambda **kw: (ran.append(kw), 0)[1]):
        call(False)
    assert ran and "clock" in ran[0]          # no logic of their own


def test_cli_parses_tick_minutes():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tick-minutes", type=int, default=5)
    assert parser.parse_args(["--tick-minutes", "1"]).tick_minutes == 1


def test_tick_minutes_1_runs(env):
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["08:00"])])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 2), tick_minutes=1)
    assert env.sent_count("Reminder") == 1


# ── AC 26: a dose inside quiet hours still loads, ticks and confirms ─────────

def test_ac26_dose_inside_quiet_hours_loads_ticks_and_confirms(env):
    # 23:30 dose with quiet 22:00–07:00: validate() must not reject the
    # state, the tick must run (reminder is quiet-exempt), and a confirm
    # must credit the dose (edit-time rejection is PR 4's add/edit check)
    env.write(meds=[make_med(med_id="med-001", frequency="once_daily",
                             times=["23:30"])])
    env.run(local_dt(23, 25))
    env.run(local_dt(23, 35))
    assert env.sent_count("Reminder") == 1

    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(23, 44)))
    taken = env.events("taken")
    assert len(taken) == 1 and taken[0]["occurrence_key"] == "2026-04-21T23:30#0"
    # and the tick stays quiet afterwards — no nudge, no missed
    env.run(local_dt(23, 55))
    assert env.events("missed") == []
    assert env.sent_count("Late:") == 0


# ── AC 29: skipped shown separately in the digest ────────────────────────────

def test_digest_shows_skipped_separately(env):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med], digest_time="07:30")
    evs = []
    for days_ago, event in ((1, "taken"), (2, "taken"), (3, "skipped"), (6, "taken")):
        day = TUE - dtmod.timedelta(days=days_ago)
        at = local_dt(8, 10) - dtmod.timedelta(days=days_ago)
        evs.append(event_store.new_event(
            "med-001", event, at, occurrence=at_local(day, "08:00", TZ, 0),
            taken_at_utc=utc(at).isoformat() if event == "taken" else None))
    env.seed(evs)
    env.run(local_dt(7, 0))
    env.run(local_dt(7, 32))
    msg = [m for m in env.sent() if "Meds for" in m][0]
    assert "Last 7 days: 3/3 doses taken, 1 skipped" in msg
