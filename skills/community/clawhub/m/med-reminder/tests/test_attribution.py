"""
Attribution tests (issue #1 §4, PR 2 — testing-plan row 3, AC 1-6).

Nearest-in-time candidates, the ambiguous zone, --dose pinning,
--taken-at resolution, and schedule-derived min-gap defaults.
"""
from datetime import timedelta

import pytest

import attribution
import event_store
from attribution import (
    EARLY_WINDOW,
    attribute,
    find_candidates,
    last_taken_before,
    min_gap,
    nearest_dose_occurrence,
    resolve_taken_at,
    unresolved_or_missed,
)
from occurrence import at_local, at_utc
from tests.conftest import local_dt, make_med, TZ

import datetime as dtmod

TUE = dtmod.date(2026, 4, 21)   # fixture week: Tue Apr 21 2026
MON = dtmod.date(2026, 4, 20)


def occ_daily(hhmm, day=TUE, index=0):
    return at_local(day, hhmm, TZ, index)


def taken(med_id, occ, at, taken_at=None):
    return event_store.new_event(
        med_id, "taken", at, occurrence=occ,
        taken_at_utc=(taken_at or at).isoformat())


def missed(med_id, occ, at):
    return event_store.new_event(med_id, "missed", at, occurrence=occ)


# ── AC 1: midday confirm credits the morning dose, evening still fires ────────

def test_ac1_midday_confirm_credits_morning_dose():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    kind, occ = attribute(med, [], local_dt(14, 30), TZ)
    assert kind == "credit" and occ.key == occ_daily("08:00").key
    # and the 20:00 reminder still fires: it is the future candidate, unresolved
    past, future = find_candidates(med, [], local_dt(14, 30), TZ)
    assert future.key == occ_daily("20:00", index=1).key


def test_ontime_confirm_credits_that_dose():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    kind, occ = attribute(med, [], local_dt(8, 14), TZ)
    assert kind == "credit" and occ.key == occ_daily("08:00").key


def test_early_confirm_within_window_credits_upcoming_dose():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    kind, occ = attribute(med, [], local_dt(18, 45), TZ)   # 75 min before 20:00
    assert kind == "credit" and occ.key == occ_daily("20:00", index=1).key


def test_early_confirm_outside_window_credits_past_dose():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    kind, occ = attribute(med, [], local_dt(16, 0), TZ)    # 4h before 20:00
    assert kind == "credit" and occ.key == occ_daily("08:00").key


# ── AC 3: the ambiguous zone exits 4 / writes nothing ─────────────────────────

def test_ac3_confirm_in_ambiguous_zone_is_ambiguous():
    # gap 90 min < 2×90-min window: between the early window start (08:30)
    # and the midpoint (08:45) both candidates are plausible
    med = make_med(frequency="twice_daily", times=["08:00", "09:30"])
    kind, payload = attribute(med, [], local_dt(8, 40), TZ)
    assert kind == "ambiguous"
    past, future = payload
    assert past.key == occ_daily("08:00").key
    assert future.key == occ_daily("09:30", index=1).key


def test_before_early_window_is_not_ambiguous():
    # long gap: midpoint 14:00, window opens 18:30 — 15:00 is a late morning dose
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    assert attribute(med, [], local_dt(15, 0), TZ)[0] == "credit"


def test_at_midpoint_is_not_ambiguous():
    # exactly equidistant with the future in window → nearer-or-equal future
    med = make_med(frequency="twice_daily", times=["08:00", "09:30"])
    kind, occ = attribute(med, [], local_dt(8, 45), TZ)
    assert kind == "credit" and occ.key == occ_daily("09:30", index=1).key


# ── AC 2: a missed occurrence is still creditable (taken late) ────────────────

def test_ac2_confirm_after_missed_credits_the_missed_dose():
    med = make_med(frequency="twice_daily", times=["08:00", "13:00"])
    events = [missed("med-001", occ_daily("08:00"), local_dt(9, 30))]
    kind, occ = attribute(med, events, local_dt(10, 0), TZ)
    assert kind == "credit" and occ.key == occ_daily("08:00").key


def test_resolved_taken_occurrence_is_not_a_candidate():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    events = [taken("med-001", occ_daily("08:00"), local_dt(8, 14))]
    kind, occ = attribute(med, events, local_dt(12, 0), TZ)
    # 08:00 resolved; 20:00 outside the early window → nothing to credit yet…
    # yesterday 20:00 is unresolved though — walking back finds it
    assert kind == "credit" and occ.key == occ_daily("20:00", MON, index=1).key


def test_skipped_occurrence_is_not_a_candidate():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    ev = event_store.new_event("med-001", "skipped", local_dt(8, 0),
                               occurrence=occ_daily("08:00"))
    _, future = find_candidates(med, [ev], local_dt(10, 0), TZ)
    assert future.key == occ_daily("20:00", index=1).key
    assert not unresolved_or_missed([ev], "med-001", occ_daily("08:00").key)


# ── AC 4: --dose pins an occurrence ────────────────────────────────────────────

def test_ac4_dose_pin_credits_evening_dose():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    occ = nearest_dose_occurrence(med, "20:00", local_dt(14, 30), TZ)
    assert occ.key == occ_daily("20:00", index=1).key


def test_ac4_dose_pin_rejects_unscheduled_time():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    with pytest.raises(ValueError, match="not a scheduled time"):
        nearest_dose_occurrence(med, "09:00", local_dt(14, 30), TZ)


def test_dose_pin_picks_nearest_instance():
    med = make_med(frequency="once_daily", times=["08:00"])
    # at 02:00 the nearest 08:00 instance is today's (6h ahead vs 18h back)
    occ = nearest_dose_occurrence(med, "08:00", local_dt(2, 0), TZ)
    assert occ.key == occ_daily("08:00").key
    # at 23:00 it is today's already-passed one (9h back vs 9h+16h ahead)... no:
    # 08:00 today is 15h back, 08:00 tomorrow is 9h ahead → tomorrow wins
    occ = nearest_dose_occurrence(med, "08:00", local_dt(23, 0), TZ)
    assert occ.key == occ_daily("08:00", TUE + dtmod.timedelta(days=1)).key


def test_dose_pin_weekly_only_on_day_of_week():
    med = make_med(frequency="weekly", times=["09:00"], day_of_week="mon")
    # Tue Apr 21 → nearest Monday 09:00 is yesterday's
    occ = nearest_dose_occurrence(med, "09:00", local_dt(12, 0), TZ)
    assert occ.key == at_local(MON, "09:00", TZ, 0).key


# ── AC 5: --taken-at resolves to the most recent past wall time ────────────────

def test_ac5_taken_at_before_midnight_records_yesterday():
    got = resolve_taken_at("23:00", TZ, local_dt(0, 30))   # Wed 00:30
    assert got == local_dt(23, 0) - timedelta(days=1)
    assert got.astimezone(TZ).hour == 23


def test_taken_at_same_day():
    assert resolve_taken_at("08:00", TZ, local_dt(12, 0)) == local_dt(8, 0)


def test_taken_at_today_instance_future_uses_yesterday():
    # at noon, today's 20:00 hasn't happened — yesterday's 20:00 (16h back) is used
    got = resolve_taken_at("20:00", TZ, local_dt(12, 0))
    assert got == local_dt(20, 0) - timedelta(days=1)


def test_taken_at_dst_fall_back_takes_first_instance():
    # 2026-11-01 in America/Los_Angeles: 01:30 exists twice (PDT then PST).
    # After the second pass, the FIRST instance (01:30 PDT, fold=0) wins.
    now = dtmod.datetime(2026, 11, 1, 2, 30, tzinfo=TZ)   # 02:30 PST
    got = resolve_taken_at("01:30", TZ, now)
    first = dtmod.datetime(2026, 11, 1, 1, 30, tzinfo=TZ)  # fold=0 → PDT
    # NB compare in UTC: CPython 3.14 inter-zone == on fold-ambiguous
    # wall times returns False even for the same instant
    assert got == first.astimezone(dtmod.timezone.utc)
    assert first.utcoffset() == timedelta(hours=-7)


def test_taken_at_dst_unambiguous_normal_day():
    now = dtmod.datetime(2026, 4, 21, 12, 0, tzinfo=TZ)
    assert resolve_taken_at("09:15", TZ, now) == dtmod.datetime(2026, 4, 21, 9, 15, tzinfo=TZ)


# ── Interval and as_needed meds ────────────────────────────────────────────────

def test_interval_candidates_walk_the_anchor_chain():
    import datetime as dt
    med = make_med(frequency="interval", interval_hours=8,
                   next_due=dt.datetime(2026, 4, 20, 8, 0, tzinfo=TZ).isoformat())
    taken_at = local_dt(10, 0)   # local chain: 04-20 08:00, 16:00, 04-21 00:00, 08:00
    past, future = find_candidates(med, [], taken_at, TZ)
    # 04-21 08:00 PDT = 15:00Z is the most recent past occurrence
    assert past.local.hour == 8 and past.utc == dt.datetime(2026, 4, 21, 15, 0, tzinfo=dt.timezone.utc)
    assert future.local.hour == 16 and future.utc == dt.datetime(2026, 4, 21, 23, 0, tzinfo=dt.timezone.utc)


def test_interval_no_anchor_yields_no_candidates():
    med = make_med(frequency="interval", interval_hours=8, next_due=None)
    assert find_candidates(med, [], local_dt(12, 0), TZ) == (None, None)


def test_as_needed_has_no_candidates():
    med = make_med(frequency="as_needed")
    kind, payload = attribute(med, [], local_dt(12, 0), TZ)
    assert (kind, payload) == ("unattributed", None)


def test_active_since_bounds_the_walk():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    med["active_since_utc"] = local_dt(12, 0).isoformat()
    # confirm at 14:30: today 08:00 predates active_since → yesterday 20:00
    # is also before it → nothing creditable, 20:00 today is the future
    past, future = find_candidates(med, [], local_dt(14, 30), TZ)
    assert past is None
    assert future.key == occ_daily("20:00", index=1).key


# ── min-gap defaults (issue §4) ────────────────────────────────────────────────

def test_min_gap_once_daily_12h():
    assert min_gap(make_med(frequency="once_daily", times=["08:00"])) == timedelta(hours=12)


def test_min_gap_twice_daily_08_20_6h():
    assert min_gap(make_med(frequency="twice_daily", times=["08:00", "20:00"])) == timedelta(hours=6)


def test_min_gap_twice_daily_08_13_half_shortest():
    assert min_gap(make_med(frequency="twice_daily", times=["08:00", "13:00"])) == \
        timedelta(hours=2.5)


def test_min_gap_interval_half_interval():
    assert min_gap(make_med(frequency="interval", interval_hours=8)) == timedelta(hours=4)


def test_min_gap_weekly_from_its_days():
    # one day a week → half of 7 days (#25; was a flat 24h)
    assert min_gap(make_med(frequency="weekly", times=["09:00"], day_of_week="mon")) == \
        timedelta(hours=84)


def test_min_gap_as_needed_4h():
    assert min_gap(make_med(frequency="as_needed")) == timedelta(hours=4)


def test_min_gap_override_field_wins():
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    med["min_gap_hours"] = 3
    assert min_gap(med) == timedelta(hours=3)


# ── duplicate lookup ───────────────────────────────────────────────────────────

def test_last_taken_before_uses_taken_at_not_ts():
    occ = occ_daily("08:00")
    # event recorded later in the day but taken_at at 08:05
    ev = taken("med-001", occ, at=local_dt(11, 0), taken_at=local_dt(8, 5))
    got = last_taken_before([ev], "med-001", local_dt(14, 0))
    assert got is ev
    assert last_taken_before([ev], "med-001", local_dt(8, 5)) is None   # strict


def test_last_taken_before_scoped_to_med():
    other = taken("med-002", occ_daily("08:00"), local_dt(8, 5))
    assert last_taken_before([other], "med-001", local_dt(14, 0)) is None
