"""
Holiday / Workday utility for Personal Assistant.

Reads scripts/holidays.json to determine if a given date is:
  - a public holiday (休息日)
  - a makeup workday (调休上班日)
  - a regular workday
"""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path

_HOLIDAYS_FILE = Path(__file__).resolve().parent / "holidays.json"


def _load_holidays() -> dict:
    with open(_HOLIDAYS_FILE) as f:
        return json.load(f)


def _date_range(start: str, end: str) -> set[str]:
    """Generate all date strings between start and end (inclusive)."""
    s = datetime.strptime(start, "%Y-%m-%d").date()
    e = datetime.strptime(end, "%Y-%m-%d").date()
    result = set()
    d = s
    while d <= e:
        result.add(d.isoformat())
        d += timedelta(days=1)
    return result


def is_workday(d: date | str = None) -> bool:
    """Check if a date is a workday.

    Returns True if:
      - Mon-Fri and NOT a public holiday
      - Sat/Sun that IS a makeup workday (调休)
    """
    if d is None:
        d = date.today()
    if isinstance(d, str):
        d = datetime.strptime(d, "%Y-%m-%d").date()

    ds = d.isoformat()
    data = _load_holidays()

    # Find the year data
    year_str = str(d.year)
    if year_str not in data:
        # No holiday data for this year → use simple Mon-Fri rule
        return d.weekday() < 5

    year_data = data[year_str]

    # Check makeup workdays first (周末调休上班)
    if ds in year_data.get("makeup_workdays", []):
        return True

    # Check holidays
    for holiday in year_data.get("holidays", []):
        if ds in _date_range(holiday["start"], holiday["end"]):
            return False

    # Regular weekday
    return d.weekday() < 5


def next_workday(d: date = None) -> date:
    """Return the next workday starting from d (inclusive if d is workday)."""
    if d is None:
        d = date.today()
    while not is_workday(d):
        d += timedelta(days=1)
    return d


def is_weekend(d: date = None) -> bool:
    """True if Saturday or Sunday (regardless of makeup days)."""
    if d is None:
        d = date.today()
    if isinstance(d, str):
        d = datetime.strptime(d, "%Y-%m-%d").date()
    return d.weekday() >= 5


def is_last_day_of_month(d: date = None) -> bool:
    """True if d is the last calendar day of its month."""
    if d is None:
        d = date.today()
    if isinstance(d, str):
        d = datetime.strptime(d, "%Y-%m-%d").date()
    next_day = d + timedelta(days=1)
    return next_day.month != d.month


def is_last_day_of_quarter(d: date = None) -> bool:
    """True if d is the last calendar day of its quarter."""
    if d is None:
        d = date.today()
    if isinstance(d, str):
        d = datetime.strptime(d, "%Y-%m-%d").date()
    quarter_last = {3: 31, 6: 30, 9: 30, 12: 31}
    return d.month in quarter_last and d.day == quarter_last[d.month]


def get_biweekly_meeting_dates(start_date: str) -> list[str]:
    """Get biweekly Monday meeting dates starting from start_date.
    
    Returns dates as iso strings.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    dates = []
    d = start
    end_of_year = date(start.year, 12, 31)
    while d <= end_of_year:
        dates.append(d.isoformat())
        d += timedelta(days=14)
    return dates


def today_str() -> str:
    """Return today's date as YYYY-MM-DD."""
    return date.today().isoformat()
