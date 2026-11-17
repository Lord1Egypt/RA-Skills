"""
Cases 11-15: compute_next_due() — next scheduled dose after a given time.
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dispatch import compute_next_due
from tests.conftest import make_med, local_dt, TZ


def next_due(med, after):
    return compute_next_due(med, after, TZ)


def at_time(dt, hh, mm=0):
    """Return a datetime on the same calendar date at a different time."""
    return dt.replace(hour=hh, minute=mm, second=0, microsecond=0)


# ── Case 11: once_daily, last_taken before today's dose time ──────────────────

def test_case_11_once_daily_before_dose_time():
    """Taken at 06:00, dose is 08:00 → next_due = today 08:00."""
    med  = make_med(frequency="once_daily", times=["08:00"])
    after = local_dt(6, 0)    # 06:00, before dose time
    result = next_due(med, after)
    expected = at_time(after, 8, 0)
    assert result == expected, f"Expected {expected}, got {result}"


# ── Case 12: once_daily, last_taken after today's dose time ───────────────────

def test_case_12_once_daily_after_dose_time():
    """Taken at 09:00, dose is 08:00 → next_due = tomorrow 08:00."""
    med   = make_med(frequency="once_daily", times=["08:00"])
    after = local_dt(9, 0)   # 09:00, past dose time
    result = next_due(med, after)
    expected = at_time(after + timedelta(days=1), 8, 0)
    assert result == expected, f"Expected {expected}, got {result}"


# ── Case 13: twice_daily, taken between dose 1 and dose 2 ────────────────────

def test_case_13_twice_daily_between_doses():
    """Taken at 10:00, doses at 08:00 and 20:00 → next_due = today 20:00."""
    med   = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    after = local_dt(10, 0)  # between 08:00 and 20:00
    result = next_due(med, after)
    expected = at_time(after, 20, 0)
    assert result == expected, f"Expected {expected}, got {result}"


def test_case_13b_twice_daily_after_both_doses():
    """Taken at 21:00, both doses past → next_due = tomorrow 08:00 (first dose)."""
    med   = make_med(frequency="twice_daily", times=["08:00", "20:00"])
    after = local_dt(21, 0)  # after both doses
    result = next_due(med, after)
    expected = at_time(after + timedelta(days=1), 8, 0)
    assert result == expected, f"Expected {expected}, got {result}"


# ── Case 14: interval — exact N hours forward ─────────────────────────────────

def test_case_14_interval_adds_hours_exactly():
    """interval_hours=6 → next_due = after + 6 hours, to the second."""
    med   = make_med(frequency="interval", interval_hours=6)
    after = local_dt(8, 0)
    result = next_due(med, after)
    expected = after + timedelta(hours=6)
    assert result == expected, f"Expected {expected}, got {result}"


def test_case_14b_interval_24h():
    med   = make_med(frequency="interval", interval_hours=24)
    after = local_dt(14, 30)
    result = next_due(med, after)
    assert result == after + timedelta(hours=24)


# ── Case 15: weekly — at least 6 days out, same time of day ──────────────────

def test_case_15_weekly_at_least_six_days_out():
    """Weekly med: next_due must be ≥6 days after `after`, at dose time."""
    med   = make_med(frequency="weekly", times=["08:00"])
    after = local_dt(9, 0)   # just after the dose time
    result = next_due(med, after)

    assert result is not None
    delta_days = (result - after).total_seconds() / 86400
    assert delta_days >= 6, f"Expected ≥6 days out, got {delta_days:.2f}"
    assert result.hour == 8 and result.minute == 0, \
        f"Expected dose time 08:00, got {result.strftime('%H:%M')}"


# ── Case: as_needed returns None ──────────────────────────────────────────────

def test_as_needed_returns_none():
    med   = make_med(frequency="as_needed")
    after = local_dt(12, 0)
    assert next_due(med, after) is None
