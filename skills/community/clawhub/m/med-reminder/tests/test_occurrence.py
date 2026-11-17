"""
occurrence.py — UTC Occurrence helpers (issue #1 PR 1).

All comparisons and offsets run in UTC; local time only feeds keys and
display. DST rules: nonexistent wall time normalizes forward, ambiguous
wall time takes the first instance (fold=0).
"""
from datetime import date, datetime, timedelta, timezone

from occurrence import (
    Occurrence,
    at_local,
    at_utc,
    covered_occurrence,
    for_instant,
    most_recent_past,
    occurrences_between,
)
from tests.conftest import local_dt, TZ

UTC = timezone.utc


# ── at_local: key, UTC instant, display ───────────────────────────────────────

def test_at_local_key_and_utc():
    occ = at_local(date(2026, 4, 21), "08:00", TZ, index=0)
    assert occ.key == "2026-04-21T08:00#0"
    assert occ.utc == datetime(2026, 4, 21, 15, 0, tzinfo=UTC)   # 08:00 PDT
    assert occ.local_display == "Tue Apr 21 8:00am PDT"


def test_at_local_index_distinguishes_doses():
    a = at_local(date(2026, 4, 21), "08:00", TZ, index=0)
    b = at_local(date(2026, 4, 21), "20:00", TZ, index=1)
    assert a.key.endswith("#0") and b.key.endswith("#1")
    assert a.utc < b.utc


def test_at_local_dont_compare_non_utc():
    # .utc is the only field for math; .local exists for display only
    occ = at_local(date(2026, 4, 21), "08:00", TZ)
    assert occ.local.tzinfo is TZ          # display side
    assert occ.utc.tzinfo is UTC           # math side


# ── DST: spring forward / fall back ───────────────────────────────────────────

def test_nonexistent_wall_time_normalizes_forward():
    # 02:30 does not exist on 2027-03-14 in LA (spring forward) — issue AC 10
    occ = at_local(date(2027, 3, 14), "02:30", TZ)
    assert occ.utc == datetime(2027, 3, 14, 10, 30, tzinfo=UTC)  # 03:30 PDT
    assert occ.local.hour == 3


def test_ambiguous_wall_time_takes_first_instance():
    # 01:30 occurs twice on 2026-11-01 in LA (fall back) — issue AC 9
    occ = at_local(date(2026, 11, 1), "01:30", TZ)
    assert occ.utc == datetime(2026, 11, 1, 8, 30, tzinfo=UTC)   # PDT, fold=0
    assert occ.local.strftime("%Z") == "PDT"


def test_offsets_in_utc_survive_fold_day():
    # +30 absolute minutes from the first 01:30 lands at 09:00Z = 01:00 PST
    occ = at_local(date(2026, 11, 1), "01:30", TZ)
    nudged = occ.utc + timedelta(minutes=30)
    assert nudged == datetime(2026, 11, 1, 9, 0, tzinfo=UTC)
    assert nudged.astimezone(TZ).strftime("%Z %H:%M") == "PST 01:00"


# ── at_utc: interval keys are the UTC instant ─────────────────────────────────

def test_at_utc_key_is_utc_instant():
    occ = at_utc(datetime(2026, 11, 1, 8, 30, tzinfo=UTC), TZ)
    assert occ.key == "2026-11-01T08:30:00Z"
    assert occ.local_display.endswith("1:30am PDT")


def test_at_utc_no_fallback_collision():
    # Both 01:30 PDT (08:30Z) and 01:30 PST (09:30Z) get distinct keys
    a = at_utc(datetime(2026, 11, 1, 8, 30, tzinfo=UTC), TZ)
    b = at_utc(datetime(2026, 11, 1, 9, 30, tzinfo=UTC), TZ)
    assert a.key != b.key


# ── occurrences_between ───────────────────────────────────────────────────────

def test_occurrences_between_daily_window():
    sched = {"frequency": "twice_daily", "times": ["08:00", "20:00"]}
    lo = local_dt(0, 0)           # Tue 2026-04-21 00:00 PDT
    hi = local_dt(0, 0) + timedelta(days=1) + timedelta(hours=8)  # Wed 08:00 PDT
    occs = occurrences_between(sched, lo, hi, TZ)
    assert [o.key for o in occs] == [
        "2026-04-21T08:00#0", "2026-04-21T20:00#1",
        "2026-04-22T08:00#0",
    ]
    assert [o.utc for o in occs] == sorted(o.utc for o in occs)


def test_occurrences_between_exclusive_lo_inclusive_hi():
    sched = {"frequency": "once_daily", "times": ["08:00"]}
    occ = at_local(date(2026, 4, 21), "08:00", TZ)
    # hi is included, lo is not
    assert occurrences_between(sched, occ.utc - timedelta(seconds=1), occ.utc, TZ) == [occ]
    assert occurrences_between(sched, occ.utc, occ.utc + timedelta(hours=1), TZ) == []
    assert occurrences_between(sched, occ.utc - timedelta(days=1), occ.utc - timedelta(microseconds=1), TZ) == []


def test_occurrences_between_weekly_only_on_day():
    # Monday med; window Wed 2026-04-22 → Sat 2026-04-25 holds no Monday
    sched = {"frequency": "weekly", "times": ["09:00"], "day_of_week": "mon"}
    lo, hi = local_dt(0, 0, day=22), local_dt(0, 0, day=25)
    assert occurrences_between(sched, lo, hi, TZ) == []
    # Window extended to Mon 2026-04-27 10:00 catches that Monday's 09:00
    hi = local_dt(10, 0, day=27)
    occs = occurrences_between(sched, lo, hi, TZ)
    assert [o.key for o in occs] == ["2026-04-27T09:00#0"]


def test_occurrences_between_interval_is_empty():
    sched = {"frequency": "interval", "interval_hours": 8}
    assert occurrences_between(sched, local_dt(0, 0), local_dt(0, 0) + timedelta(days=1), TZ) == []


# ── most_recent_past ─────────────────────────────────────────────────────────

def test_most_recent_past_same_day_and_yesterday():
    sched = {"frequency": "once_daily", "times": ["08:00"]}
    assert most_recent_past(sched, local_dt(12, 0), TZ).key == "2026-04-21T08:00#0"
    assert most_recent_past(sched, local_dt(7, 0), TZ).key == "2026-04-20T08:00#0"


def test_most_recent_past_twice_daily_picks_latest():
    sched = {"frequency": "twice_daily", "times": ["08:00", "20:00"]}
    assert most_recent_past(sched, local_dt(12, 0), TZ).key == "2026-04-21T08:00#0"
    assert most_recent_past(sched, local_dt(21, 0), TZ).key == "2026-04-21T20:00#1"


def test_most_recent_past_none_for_interval():
    assert most_recent_past({"frequency": "interval", "interval_hours": 8}, local_dt(12, 0), TZ) is None


# ── covered_occurrence: pre-tick rules (migration parity) ─────────────────────

def test_covered_early_confirm_credits_upcoming():
    sched = {"frequency": "twice_daily", "times": ["08:00", "20:00"]}
    occ = covered_occurrence(sched, local_dt(7, 32), TZ)
    assert occ.key == "2026-04-21T08:00#0"


def test_covered_midday_credits_morning():
    sched = {"frequency": "twice_daily", "times": ["08:00", "20:00"]}
    assert covered_occurrence(sched, local_dt(12, 0), TZ).key == "2026-04-21T08:00#0"


def test_covered_none_for_interval_and_as_needed():
    assert covered_occurrence({"frequency": "interval", "interval_hours": 6}, local_dt(12, 0), TZ) is None
    assert covered_occurrence({"frequency": "as_needed"}, local_dt(12, 0), TZ) is None


# ── for_instant (confirmed_dose anchor) ───────────────────────────────────────

def test_for_instant_matches_wall_time_key():
    sched = {"frequency": "twice_daily", "times": ["08:00", "20:00"]}
    occ = for_instant(sched, local_dt(8, 0), TZ)
    assert occ.key == "2026-04-21T08:00#0"


def test_for_instant_falls_back_to_utc_key():
    sched = {"frequency": "once_daily", "times": ["08:00"]}
    occ = for_instant(sched, local_dt(11, 17), TZ)   # not a scheduled wall time
    assert occ.key == occ.utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_for_instant_interval_uses_utc_key():
    sched = {"frequency": "interval", "interval_hours": 8}
    occ = for_instant(sched, local_dt(8, 0), TZ)
    assert occ.key == "2026-04-21T15:00:00Z"
