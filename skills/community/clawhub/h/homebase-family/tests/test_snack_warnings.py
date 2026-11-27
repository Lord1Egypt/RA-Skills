"""
test_snack_warnings.py — SnackManager's two schedule warnings, and the rule
that neither of them is ever returned as a snack.

Written after the September 2026 reminder was found being generated and thrown
away on every run of its own window. `should_warn_about_missing_schedule()`
returns two different warnings:

  - the current month has no schedule at all;
  - it is the last week of the month and next month's photo hasn't arrived.

The caller gated both on `if not snack_text`. That guard is dead weight for the
first (a snack for today is itself proof the month is loaded) and fatal to the
second, whose entire window is normal school days with snacks. So the reminder
could only surface on a day this month's snack was missing, which is the one
kind of day it isn't about.

The other half is labelling: `format_for_briefing()` used to return a warning
in place of snack text, which lands it in the briefing's `snack` field and gets
pasted verbatim under a "School Snacks Today" heading.

August 2026 is the reference month throughout — 31 days, so the last-week
window opens on the 25th, and the 26th is a Wednesday.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from features.school.snack_manager import SnackManager


AUGUST_SNACK_DAYS = ["2026-08-21", "2026-08-24", "2026-08-25",
                     "2026-08-26", "2026-08-27", "2026-08-28"]


def _frozen(y, m, d):
    """Freeze datetime.now() inside snack_manager only.

    A subclass rather than a MagicMock so strptime/replace keep working —
    is_school_closed() parses date strings through the same name.
    """
    fixed = datetime(y, m, d, 6, 5)

    class _FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed

    return patch("features.school.snack_manager.datetime", _FrozenDatetime)


def _manager(tmp_path, days=AUGUST_SNACK_DAYS, september=False):
    """A SnackManager whose schedule holds `days`, optionally plus September."""
    schedule = {
        d: {"morning": "1/2 c Goldfish", "afternoon": "1/2 c strawberries",
            "school_closed": False, "updated_at": "2026-08-01T00:00:00"}
        for d in days
    }
    if september:
        schedule["2026-09-01"] = {"morning": "Crackers", "afternoon": "Apple",
                                  "school_closed": False,
                                  "updated_at": "2026-08-01T00:00:00"}
    household = tmp_path / "household"
    household.mkdir(exist_ok=True)
    (household / "snack_schedule.json").write_text(json.dumps(schedule))
    return SnackManager(str(tmp_path))


class TestNextMonthReminder:
    """The regression: it must fire on an ordinary school day."""

    def test_fires_on_a_normal_school_day_that_has_a_snack(self, tmp_path):
        # Wednesday Aug 26. August loaded, today has a snack, September empty.
        # This is the exact live state on the day the bug was found.
        m = _manager(tmp_path)
        with _frozen(2026, 8, 26):
            assert m.get_today_snack()          # a snack exists today
            warning = m.should_warn_about_missing_schedule()
        assert warning is not None
        assert "September" in warning

    def test_silent_once_september_arrives(self, tmp_path):
        m = _manager(tmp_path, september=True)
        with _frozen(2026, 8, 26):
            assert m.should_warn_about_missing_schedule() is None

    def test_silent_before_the_window_opens(self, tmp_path):
        # Aug 24. Window is day >= 31 - 6 == 25, so the 24th is too early.
        m = _manager(tmp_path)
        with _frozen(2026, 8, 24):
            assert m.should_warn_about_missing_schedule() is None

    def test_fires_on_the_first_day_of_the_window(self, tmp_path):
        m = _manager(tmp_path)
        with _frozen(2026, 8, 25):
            warning = m.should_warn_about_missing_schedule()
        assert warning is not None
        assert "September" in warning

    def test_silent_at_the_weekend(self, tmp_path):
        # Saturday Aug 29 — inside the window, but nobody is at school.
        m = _manager(tmp_path)
        with _frozen(2026, 8, 29):
            assert m.should_warn_about_missing_schedule() is None

    def test_fires_on_a_day_with_no_snack_entry(self, tmp_path):
        # Monday Aug 31 has no row at all. Before the fix this was the only
        # day of the window that surfaced anything, and it surfaced it as a
        # snack. It must still warn, and must not claim to be a snack.
        m = _manager(tmp_path)
        with _frozen(2026, 8, 31):
            warning = m.should_warn_about_missing_schedule()
            assert m.format_for_briefing() is None
        assert warning is not None
        assert "September" in warning


class TestMonthEndArithmetic:
    """The 31st must not raise.

    `replace(month=m + 1)` without `day=1` is a ValueError on the 31st of any
    month whose successor is shorter. That is five days a year, all of them
    inside the last-week window — so the crash sat on exactly the days the
    reminder is for. Found by the Aug 31 case below, which is a Monday.
    """

    SHORT_SUCCESSOR_31STS = [
        (2026, 1, 31),   # → February
        (2026, 3, 31),   # → April
        (2026, 5, 31),   # → June
        (2026, 8, 31),   # → September
        (2026, 10, 31),  # → November
    ]

    def test_every_31st_is_survivable(self, tmp_path):
        m = _manager(tmp_path, days=[])
        for y, mo, d in self.SHORT_SUCCESSOR_31STS:
            with _frozen(y, mo, d):
                m.is_next_month_loaded()
                m.should_warn_about_missing_schedule()
                m.format_for_briefing()

    def test_december_rolls_into_january(self, tmp_path):
        m = _manager(tmp_path, days=["2026-12-31"])
        with _frozen(2026, 12, 31):
            assert m.is_next_month_loaded() is False
            assert "January" in m.should_warn_about_missing_schedule()

    def test_next_month_detection_is_correct_on_the_31st(self, tmp_path):
        # Aug 31 with September present: the reminder must go quiet, which
        # only happens if the prefix was built from September and not from
        # a wrapped-around date.
        m = _manager(tmp_path, days=["2026-08-31"], september=True)
        with _frozen(2026, 8, 31):
            assert m.is_next_month_loaded() is True
            assert m.should_warn_about_missing_schedule() is None


class TestCurrentMonthWarning:
    """The louder warning, and the reason its old guard was redundant."""

    def test_fires_when_nothing_is_loaded(self, tmp_path):
        m = _manager(tmp_path, days=[])
        with _frozen(2026, 8, 26):
            warning = m.should_warn_about_missing_schedule()
        assert warning is not None
        assert "August" in warning

    def test_cannot_fire_while_a_snack_exists(self, tmp_path):
        # The property the removed `if not snack_text` guard was relying on:
        # today's snack is itself the key that makes the month "loaded", so
        # this branch is already unreachable whenever there is a snack.
        m = _manager(tmp_path)
        with _frozen(2026, 8, 26):
            assert m.get_today_snack()
            assert m.is_current_month_loaded()
            assert "August" not in (m.should_warn_about_missing_schedule() or "")

    def test_the_two_warnings_are_mutually_exclusive(self, tmp_path):
        # Nothing loaded at all, deep in the last week: the current-month
        # warning wins and the next-month one never gets a look in.
        m = _manager(tmp_path, days=[])
        with _frozen(2026, 8, 26):
            warning = m.should_warn_about_missing_schedule()
        assert "August" in warning
        assert "September" not in warning

    def test_silent_at_the_weekend(self, tmp_path):
        m = _manager(tmp_path, days=[])
        with _frozen(2026, 8, 29):
            assert m.should_warn_about_missing_schedule() is None


class TestFormatForBriefingNeverWarns:
    """A warning in the `snack` field gets pasted under a snack heading."""

    def test_returns_none_when_no_snack_today(self, tmp_path):
        m = _manager(tmp_path, days=[])
        with _frozen(2026, 8, 26):
            assert m.format_for_briefing() is None

    def test_returns_none_when_the_entry_is_empty(self, tmp_path):
        # A row exists but carries neither morning nor afternoon.
        household = tmp_path / "household"
        household.mkdir(exist_ok=True)
        (household / "snack_schedule.json").write_text(json.dumps({
            "2026-08-26": {"morning": "", "afternoon": "",
                           "school_closed": False,
                           "updated_at": "2026-08-01T00:00:00"},
        }))
        m = SnackManager(str(tmp_path))
        with _frozen(2026, 8, 26):
            assert m.format_for_briefing() is None

    def test_still_returns_the_snack_block_when_there_is_one(self, tmp_path):
        m = _manager(tmp_path)
        with _frozen(2026, 8, 26):
            text = m.format_for_briefing()
        assert text is not None
        assert text.startswith("🍎 *School Snacks Today*")
        assert "Goldfish" in text
        assert "📸" not in text
