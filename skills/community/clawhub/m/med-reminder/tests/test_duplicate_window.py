"""
#25: the duplicate-dose window misfired across days for multi-day weekly
meds — a next-day confirm was refused (exit 3) and the next dose's nudge
carried a dateless "You logged X at 8:45pm" caution citing yesterday.

- min_gap for weekly meds comes from the actual day/time spacing
  (Mon–Fri 19:00 → 12h), not a flat 24h.
- A confirm crediting the next scheduled dose after the last logged one is
  never a duplicate; a second log of the same dose, or a back-fill of an
  older missed dose minutes after a newer one, still is.
- Every caution / refusal names the day ("yesterday at 8:45pm").
"""
import datetime as dtmod
from datetime import timedelta

import pytest

import event_store
from attribution import min_gap
from clock import FakeClock
from occurrence import at_local
from reply import EXIT_DUPLICATE, handle_confirm
from tests.conftest import TZ, local_dt, make_med, make_tick_env, utc

TUE = dtmod.date(2026, 4, 21)       # a Tuesday
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri"]


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def weekday_med(**kw):
    return make_med(name="Ipamorelin", frequency="weekly", times=["19:00"],
                    day_of_week=WEEKDAYS, **kw)


def taken(med_id, day, hhmm_occ, taken_local):
    occ = at_local(day, hhmm_occ, TZ)
    return event_store.new_event(med_id, "taken", utc(taken_local), occurrence=occ,
                                 taken_at_utc=utc(taken_local).isoformat())


# ── min_gap from the real schedule ────────────────────────────────────────────

@pytest.mark.parametrize("days,times,hours", [
    (WEEKDAYS, ["19:00"], 12),                 # weekday doses are a day apart
    (["tue", "sat"], ["09:00"], 36),           # Tue→Sat 4d, Sat→Tue 3d → 1.5d
    (["mon"], ["09:00"], 84),                  # once a week → 3.5d
    ("mon", ["09:00"], 84),                    # legacy single-day string
    (["mon"], ["08:00", "20:00"], 6),          # two doses that day
])
def test_weekly_min_gap_follows_the_schedule(days, times, hours):
    med = make_med(frequency="weekly", times=times, day_of_week=days)
    assert min_gap(med) == timedelta(hours=hours)


def test_min_gap_override_still_wins_for_weekly():
    med = weekday_med(); med["min_gap_hours"] = 2
    assert min_gap(med) == timedelta(hours=2)


# ── confirm (defect 1) ────────────────────────────────────────────────────────

def test_next_day_confirm_is_not_a_duplicate(env, capsys):
    # the dogfood case: Mon 20:45 logged, Tue 20:22 confirm (22.6h later)
    env.write(meds=[weekday_med()])
    mon = TUE - timedelta(days=1)
    env.seed([taken("med-001", mon, "19:00", local_dt(20, 45) - timedelta(days=1))])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(20, 22)))
    out = capsys.readouterr().out
    assert "Logged as your 7:00pm dose." in out
    assert len(env.events("taken")) == 2


def test_progression_wins_even_inside_a_long_gap(env, capsys):
    # Tue+Sat med: Sat's dose logged late on Mon, Tue's dose on Tue morning —
    # 14h apart, inside the 36h gap, but it's simply the next scheduled dose
    med = make_med(frequency="weekly", times=["08:00"], day_of_week=["tue", "sat"])
    env.write(meds=[med])
    sat = TUE - timedelta(days=3)
    env.seed([taken("med-001", sat, "08:00", local_dt(18, 0) - timedelta(days=1))])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    assert "Logged as your 8:00am dose." in capsys.readouterr().out


def test_same_dose_twice_minutes_apart_is_refused(env, capsys):
    env.write(meds=[weekday_med()])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(19, 5)))
    capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(19, 10)))
    assert e.value.code == EXIT_DUPLICATE
    out = capsys.readouterr().out
    assert "Already logged Ipamorelin today at 7:05pm" in out
    assert "--force" in out
    assert len(env.events("taken")) == 1


def test_backfilling_an_older_dose_right_after_a_newer_one_is_refused(env):
    # 08:00 missed, 12:00 taken at 12:05 — a second "took" at 12:10 would
    # credit the missed 08:00: minutes after a dose, that's a double log
    env.write(meds=[make_med(frequency="twice_daily", times=["08:00", "12:00"])])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(12, 5)))
    with pytest.raises(SystemExit) as e:
        handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(12, 10)))
    assert e.value.code == EXIT_DUPLICATE


def test_pinning_an_already_taken_dose_is_refused(env, capsys):
    # a 1h gap keeps the time rule out of it: only "this dose is already
    # logged" can refuse the 12:00 --dose 08:00 confirm
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    med["min_gap_hours"] = 1
    env.write(meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(12, 0)),
                       dose_pin="08:00")
    assert e.value.code == EXIT_DUPLICATE
    assert ("Already logged Metformin today at 8:05am. "
            "That's your 8:00am dose — it's already logged.") in capsys.readouterr().out


def test_confirm_all_logs_the_next_day_dose(env, capsys):
    env.write(meds=[weekday_med()])
    mon = TUE - timedelta(days=1)
    env.seed([taken("med-001", mon, "19:00", local_dt(20, 45) - timedelta(days=1))])
    from reply import handle_confirm_all
    handle_confirm_all(None, dry_run=False, clock=FakeClock(local_dt(20, 22)))
    assert "Confirmed: Ipamorelin." in capsys.readouterr().out


# ── nudge caution (defect 2) ──────────────────────────────────────────────────

def test_next_day_reminder_and_nudge_carry_no_caution(env):
    env.write(meds=[weekday_med()])
    mon = TUE - timedelta(days=1)
    env.seed([taken("med-001", mon, "19:00", local_dt(20, 45) - timedelta(days=1))])
    env.run(local_dt(18, 55))
    env.run(local_dt(19, 5))
    env.run(local_dt(19, 35))
    assert env.sent_count("Reminder: Ipamorelin") == 1
    assert env.sent_count("Late:") == 1
    assert env.sent_count("You logged") == 0


def test_caution_names_yesterday(env):
    # once daily 07:00: yesterday's dose logged at 23:30 is 7.5h before today's
    # (inside the 12h gap) — a real caution, and it must say which day
    env.write(meds=[make_med(times=["07:00"])])
    env.seed([taken("med-001", TUE - timedelta(days=1), "07:00",
                    local_dt(23, 30) - timedelta(days=1))])
    env.run(local_dt(6, 55))
    env.run(local_dt(7, 5))
    assert "You logged Metformin yesterday at 11:30pm." in env.sent()[0]


def test_caution_names_today(env):
    env.write(meds=[make_med(times=["08:00"])])
    env.run(local_dt(7, 0))
    env.seed([event_store.new_event("med-001", "taken", utc(local_dt(2, 30)),
                                    taken_at_utc=utc(local_dt(2, 30)).isoformat())])
    env.run(local_dt(8, 5))
    assert "You logged Metformin today at 2:30am." in env.sent()[0]
