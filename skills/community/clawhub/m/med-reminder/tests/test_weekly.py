"""
Weekly-med tests — the time helpers (most_recent_weekly_time,
compute_next_due, fmt_days). The tick-side weekly behavior (day filter,
Sunday-23:30 offsets landing Monday) lives in tests/test_dst.py and
tests/test_tick.py; the multi-day tick/digest/reply integration is in
tests/test_multi_day.py.

Fixture date 2026-04-21 is a Tuesday; Monday is 2026-04-20;
the surrounding week runs Sat Apr 18 – Sun Apr 26.
"""
from datetime import timedelta

from dispatch import compute_next_due, fmt_days, most_recent_weekly_time
from occurrence import day_indexes, occurrences_between
from tests.conftest import local_dt, make_med, TZ


def monday(hour=9, minute=0):
    """Monday 2026-04-20 at HH:MM."""
    return local_dt(hour, minute, year=2026, month=4, day=20)


def tuesday(hour=12):
    return local_dt(hour, 0, year=2026, month=4, day=21)


# ── most_recent_weekly_time ────────────────────────────────────────────────────

def test_most_recent_weekly_same_day():
    # Tuesday 12:00, dose Tuesdays 09:00 → today 09:00
    assert most_recent_weekly_time("tue", "09:00", TZ, tuesday(12)) == tuesday(9)


def test_most_recent_weekly_earlier_day():
    # Tuesday 12:00, dose Mondays 09:00 → yesterday 09:00
    assert most_recent_weekly_time("mon", "09:00", TZ, tuesday(12)) == monday(9)


def test_most_recent_weekly_before_time_same_day():
    # Tuesday 07:00, dose Tuesdays 09:00 → last week's Tuesday 09:00
    expected = local_dt(9, 0, year=2026, month=4, day=14)  # Tue Apr 14 09:00
    assert most_recent_weekly_time("tue", "09:00", TZ, local_dt(7, 0, year=2026, month=4, day=21)) \
        == expected


# ── compute_next_due respects the day ──────────────────────────────────────────

def test_next_due_from_off_day_is_next_weeks_dose_day():
    med = make_med(frequency="weekly", times=["09:00"], day_of_week="mon")
    nd = compute_next_due(med, tuesday(12), TZ)
    assert nd == monday(9) + timedelta(days=7)


def test_next_due_on_dose_day_after_time_is_next_week():
    med = make_med(frequency="weekly", times=["09:00"], day_of_week="mon")
    nd = compute_next_due(med, monday(10), TZ)   # Monday 10:00, dose was 09:00
    assert nd == monday(9) + timedelta(days=7)


# ── Multi-day weekly schedules (PR 7) ─────────────────────────────────────────

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri"]


def test_day_indexes_both_forms():
    assert day_indexes("tue") == (1,)
    assert day_indexes(["mon", "fri"]) == (0, 4)
    assert day_indexes(None) == ()
    assert day_indexes([]) == ()


def test_fmt_days():
    assert fmt_days("tue") == "Tue"
    assert fmt_days(["tue"]) == "Tue"
    assert fmt_days(["tue", "sat"]) == "Tue+Sat"          # non-consecutive
    assert fmt_days(WEEKDAYS) == "Mon–Fri"                # 5-day run
    assert fmt_days(["mon", "tue", "wed", "sat"]) == "Mon–Wed+Sat"
    assert fmt_days(["mon", "tue"]) == "Mon+Tue"          # runs of 2 stay open
    assert fmt_days(None) == ""
    assert fmt_days([]) == ""


def test_multi_day_enumeration_only_listed_days():
    # Tue+Sat med over Sat Apr 18 – Tue Apr 21: fires Sat and Tue, never Sun/Mon
    sched = make_med(frequency="weekly", times=["09:00"],
                     day_of_week=["tue", "sat"])["schedule"]
    occs = occurrences_between(sched, local_dt(0, 0, day=18), local_dt(23, 59, day=21), TZ)
    assert [o.key for o in occs] == ["2026-04-18T09:00#0", "2026-04-21T09:00#0"]


def test_mon_fri_has_zero_weekend_occurrences():
    sched = make_med(frequency="weekly", times=["08:00"], day_of_week=WEEKDAYS)["schedule"]
    occs = occurrences_between(sched, local_dt(0, 0, day=17), local_dt(23, 59, day=27), TZ)
    days = {o.local.strftime("%a") for o in occs}
    assert days == {"Mon", "Tue", "Wed", "Thu", "Fri"}
    assert len(occs) == 7                     # every weekday in the window, once


def test_next_due_multi_day_picks_soonest_day():
    med = make_med(frequency="weekly", times=["09:00"], day_of_week=WEEKDAYS)
    # Wednesday 10:00 — Wednesday's 09:00 dose already went → Thursday 09:00
    assert compute_next_due(med, local_dt(10, 0, day=22), TZ) \
        == local_dt(9, 0, day=23)
    # Friday 10:00 — the workweek's last dose went → next Monday 09:00
    assert compute_next_due(med, local_dt(10, 0, day=17), TZ) \
        == local_dt(9, 0, day=20)


def test_next_due_tue_sat_skips_to_saturday():
    med = make_med(frequency="weekly", times=["09:00"], day_of_week=["tue", "sat"])
    # Wednesday 12:00 → next dose is Saturday 09:00
    assert compute_next_due(med, local_dt(12, 0, day=22), TZ) \
        == local_dt(9, 0, day=25)


def test_single_string_still_enumerates_like_array():
    # The legacy form and its array twin must enumerate identically.
    legacy = make_med(frequency="weekly", times=["09:00"], day_of_week="tue")["schedule"]
    array = make_med(frequency="weekly", times=["09:00"], day_of_week=["tue"])["schedule"]
    window = (local_dt(0, 0, day=17), local_dt(23, 59, day=26))
    assert [o.key for o in occurrences_between(legacy, *window, TZ)] \
        == [o.key for o in occurrences_between(array, *window, TZ)]
