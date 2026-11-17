#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
from datetime import date

from count_working_days import count_working_days


def test_simple_range():
    assert count_working_days(date(2026, 7, 1), date(2026, 7, 2)) == 1


# DISCRIMINATING: off-by-one / range-boundary coverage
# A buggy off-by-one impl typically drops 1 day for discriminating cases.

def test_single_day_range_different_dates():
    # exactly 1 calendar day boundary: one weekday, should count 1
    assert count_working_days(date(2026, 7, 1), date(2026, 7, 2)) == 1


def test_full_week_monday_to_sunday():
    assert count_working_days(date(2026, 7, 6), date(2026, 7, 13)) == 5


def test_weekend_only_sunday_range():
    start = date(2026, 7, 5)  # Sunday
    end = date(2026, 7, 6)    # Monday
    assert count_working_days(start, end) == 1


def test_month_boundary_eom_to_next_day():
    assert count_working_days(date(2026, 6, 30), date(2026, 7, 1)) == 1


def test_long_span_2_weeks():
    assert count_working_days(date(2026, 7, 6), date(2026, 7, 20)) == 10


def test_friday_to_monday_includes_friday():
    assert count_working_days(date(2026, 7, 10), date(2026, 7, 13)) == 1


# Non-discriminating sanity checks

def test_same_start_and_end():
    assert count_working_days(date(2026, 7, 6), date(2026, 7, 6)) == 0


def test_start_after_end():
    assert count_working_days(date(2026, 7, 10), date(2026, 7, 6)) == 0


def test_weekend_no_weekdays():
    assert count_working_days(date(2026, 7, 4), date(2026, 7, 6)) == 0
