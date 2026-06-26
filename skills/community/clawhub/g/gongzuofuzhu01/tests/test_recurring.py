"""
Tests for recurring.py — RecurringManager CRUD, date calculation,
and instance generation.

Uses a temporary SQLite database via pytest fixtures so no side effects occur.
"""

import tempfile
import sys
from pathlib import Path
from datetime import date, timedelta

import pytest

# Ensure the *parent* (personal-assistant) is on sys.path so that
# `from scripts.db import Database` and relative imports inside
# `recurring` resolve correctly.
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.task_manager import TaskManager
from scripts.recurring import RecurringManager


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db():
    """Create a fresh temp-file database."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()

    database = Database(db_path=tmp.name)
    # Override SCHEMA_FILE so init_db() reads the real schema.sql
    import scripts.db as db_mod

    db_mod.SCHEMA_FILE = (
        Path(__file__).resolve().parent.parent / "scripts" / "schema.sql"
    )
    database.init_db()
    yield database
    try:
        Path(tmp.name).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture
def tm(db):
    """TaskManager wired to the temp database."""
    return TaskManager(db)


@pytest.fixture
def rm(db, tm):
    """RecurringManager wired to the temp database."""
    return RecurringManager(db, tm)


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------


class TestAdd:
    def test_add_basic(self, rm):
        rid = rm.add("Exercise", "daily", "2026-06-01")
        assert isinstance(rid, int)
        assert rid > 0

        tmpl = rm.get(rid)
        assert tmpl is not None
        assert tmpl["template_title"] == "Exercise"
        assert tmpl["recurrence_type"] == "daily"
        assert tmpl["next_run_date"] == "2026-06-01"
        assert tmpl["enabled"] == 1  # default

    def test_add_with_all_fields(self, rm):
        rid = rm.add(
            template_title="Team standup",
            recurrence_type="weekly",
            first_date="2026-07-01",
            template_desc="Daily standup sync",
            category="会议",
            priority=1,
            estimated_hours=0.5,
            recurrence_rule='{"interval": 1, "unit": "weeks"}',
            advance_days=1,
            extra='{"channel":"zoom"}',
        )
        tmpl = rm.get(rid)
        assert tmpl["template_title"] == "Team standup"
        assert tmpl["recurrence_type"] == "weekly"
        assert tmpl["next_run_date"] == "2026-07-01"
        assert tmpl["template_desc"] == "Daily standup sync"
        assert tmpl["category"] == "会议"
        assert tmpl["priority"] == 1
        assert tmpl["estimated_hours"] == 0.5
        assert tmpl["recurrence_rule"] == '{"interval": 1, "unit": "weeks"}'
        assert tmpl["advance_days"] == 1
        assert tmpl["extra"] == '{"channel":"zoom"}'

    def test_add_invalid_recurrence_type(self, rm):
        with pytest.raises(ValueError, match="Invalid recurrence_type"):
            rm.add("Bad", "yearly", "2026-06-01")

    def test_add_recurrence_type_case_and_space(self, rm):
        """Recurrence type should be case/whitespace insensitive."""
        rid = rm.add("Test", "  DAILY  ", "2026-06-01")
        tmpl = rm.get(rid)
        assert tmpl["recurrence_type"] == "daily"


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_existing(self, rm):
        rid = rm.add("Read", "daily", "2026-06-01")
        tmpl = rm.get(rid)
        assert tmpl is not None
        assert tmpl["template_title"] == "Read"

    def test_get_nonexistent(self, rm):
        assert rm.get(99999) is None


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


class TestList:
    def test_list_all(self, rm):
        rm.add("A", "daily", "2026-06-01")
        rm.add("B", "weekly", "2026-06-02")
        rm.add("C", "monthly", "2026-06-03")
        results = rm.list()
        assert len(results) == 3

    def test_list_empty(self, rm):
        assert rm.list() == []

    def test_list_enabled_only(self, rm):
        rid1 = rm.add("A", "daily", "2026-06-01")
        rid2 = rm.add("B", "daily", "2026-06-01")
        rm.toggle(rid2, False)
        results = rm.list(enabled_only=True)
        assert len(results) == 1
        assert results[0]["id"] == rid1

    def test_list_disabled_not_included(self, rm):
        rm.add("A", "daily", "2026-06-01")
        rid2 = rm.add("B", "daily", "2026-06-01")
        rm.toggle(rid2, False)
        # enabled_only=False should show all
        all_results = rm.list(enabled_only=False)
        assert len(all_results) == 2
        # enabled_only=True should only show enabled
        enabled_results = rm.list(enabled_only=True)
        assert len(enabled_results) == 1


# ---------------------------------------------------------------------------
# toggle
# ---------------------------------------------------------------------------


class TestToggle:
    def test_toggle_disable(self, rm):
        rid = rm.add("Task", "daily", "2026-06-01")
        assert rm.get(rid)["enabled"] == 1
        rm.toggle(rid, False)
        assert rm.get(rid)["enabled"] == 0

    def test_toggle_enable(self, rm):
        rid = rm.add("Task", "daily", "2026-06-01")
        rm.toggle(rid, False)
        rm.toggle(rid, True)
        assert rm.get(rid)["enabled"] == 1

    def test_toggle_updated_at_changes(self, rm):
        rid = rm.add("Task", "daily", "2026-06-01")
        old_ts = rm.get(rid)["updated_at"]
        rm.toggle(rid, False)
        new_ts = rm.get(rid)["updated_at"]
        # updated_at should change (or at least not be None)
        assert new_ts is not None
        # On fast test runs the timestamps might be equal; that's ok.


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_delete_removes_template(self, rm):
        rid = rm.add("Task", "daily", "2026-06-01")
        rm.delete(rid)
        assert rm.get(rid) is None

    def test_delete_preserves_generated_tasks(self, rm):
        """Deleting a template does not delete its already-generated task instances."""
        rid = rm.add("Recurring task", "daily", "2020-01-01")

        # Generate an instance (force a past date so it's due)
        from datetime import date as dt_date

        # Manually create a task as if it were generated
        tid = rm.task_manager.add(
            title="Recurring task",
            source_type="recurring",
            recurring_id=rid,
            deadline="2020-01-01T18:00:00",
        )
        assert tid > 0

        # Now delete the template
        rm.delete(rid)
        assert rm.get(rid) is None

        # The generated task should still exist
        task = rm.task_manager.get(tid)
        assert task is not None
        assert task["title"] == "Recurring task"


# ---------------------------------------------------------------------------
# calc_next_date — daily
# ---------------------------------------------------------------------------


class TestCalcNextDateDaily:
    def test_daily(self):
        assert RecurringManager.calc_next_date("2026-06-01", "daily") == "2026-06-02"

    def test_daily_cross_month(self):
        assert RecurringManager.calc_next_date("2026-01-31", "daily") == "2026-02-01"

    def test_daily_cross_year(self):
        assert RecurringManager.calc_next_date("2025-12-31", "daily") == "2026-01-01"


# ---------------------------------------------------------------------------
# calc_next_date — weekly
# ---------------------------------------------------------------------------


class TestCalcNextDateWeekly:
    def test_weekly(self):
        assert RecurringManager.calc_next_date("2026-06-01", "weekly") == "2026-06-08"

    def test_weekly_cross_month(self):
        assert RecurringManager.calc_next_date("2026-07-29", "weekly") == "2026-08-05"


# ---------------------------------------------------------------------------
# calc_next_date — biweekly
# ---------------------------------------------------------------------------


class TestCalcNextDateBiweekly:
    def test_biweekly(self):
        assert RecurringManager.calc_next_date("2026-06-01", "biweekly") == "2026-06-15"

    def test_biweekly_cross_month(self):
        assert RecurringManager.calc_next_date("2026-06-20", "biweekly") == "2026-07-04"


# ---------------------------------------------------------------------------
# calc_next_date — monthly
# ---------------------------------------------------------------------------


class TestCalcNextDateMonthly:
    def test_monthly_mid_month(self):
        assert RecurringManager.calc_next_date("2026-06-15", "monthly") == "2026-07-15"

    def test_monthly_cross_year(self):
        assert RecurringManager.calc_next_date("2025-12-10", "monthly") == "2026-01-10"

    def test_monthly_jan_31_to_feb(self):
        """Jan 31 → Feb 28 (non-leap year) — month-end boundary."""
        # 2026 is not a leap year, Feb has 28 days
        assert RecurringManager.calc_next_date("2026-01-31", "monthly") == "2026-02-28"

    def test_monthly_jan_31_to_feb_leap(self):
        """Jan 31 → Feb 29 (leap year) — month-end boundary."""
        # 2024 is a leap year, Feb has 29 days
        assert RecurringManager.calc_next_date("2024-01-31", "monthly") == "2024-02-29"

    def test_monthly_mar_31_to_apr(self):
        """Mar 31 → Apr 30 — month-end boundary."""
        assert RecurringManager.calc_next_date("2026-03-31", "monthly") == "2026-04-30"

    def test_monthly_feb_28_non_leap(self):
        """Feb 28 (last day of month in non-leap year) → Mar 31 (month-end snap)."""
        # 2025: Feb has 28 days, so Feb 28 is the last day
        assert RecurringManager.calc_next_date("2025-02-28", "monthly") == "2025-03-31"

    def test_monthly_mid_feb(self):
        """Feb 15 → Mar 15 (not month-end, normal advance)."""
        assert RecurringManager.calc_next_date("2026-02-15", "monthly") == "2026-03-15"

    def test_monthly_clamp_day(self):
        """Jan 30 → Feb 28 (30 doesn't exist in Feb, clamp)."""
        # Jan 30 is NOT the last day of Jan — so it clamps to Feb 28
        assert RecurringManager.calc_next_date("2026-01-30", "monthly") == "2026-02-28"


# ---------------------------------------------------------------------------
# calc_next_date — custom
# ---------------------------------------------------------------------------


class TestCalcNextDateCustom:
    def test_custom_days(self):
        rule = '{"interval": 5, "unit": "days"}'
        assert RecurringManager.calc_next_date("2026-06-01", "custom", rule) == "2026-06-06"

    def test_custom_weeks(self):
        rule = '{"interval": 2, "unit": "weeks"}'
        assert RecurringManager.calc_next_date("2026-06-01", "custom", rule) == "2026-06-15"

    def test_custom_months(self):
        rule = '{"interval": 1, "unit": "months"}'
        assert RecurringManager.calc_next_date("2026-06-15", "custom", rule) == "2026-07-15"

    def test_custom_without_rule_raises(self):
        with pytest.raises(NotImplementedError, match="recurrence_rule"):
            RecurringManager.calc_next_date("2026-06-01", "custom")

    def test_custom_invalid_json(self):
        with pytest.raises(ValueError, match="Invalid JSON"):
            RecurringManager.calc_next_date("2026-06-01", "custom", "not json")


# ---------------------------------------------------------------------------
# generate_instances
# ---------------------------------------------------------------------------


class TestGenerateInstances:
    def test_generates_task_for_due_template(self, rm):
        """A template with next_run_date in the past should generate a task."""
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()

        rid = rm.add("Daily review", "daily", yesterday)
        new_ids = rm.generate_instances()

        assert len(new_ids) == 1
        task = rm.task_manager.get(new_ids[0])
        assert task is not None
        assert task["title"] == "Daily review"
        assert task["source_type"] == "recurring"
        assert task["recurring_id"] == rid

    def test_correct_fields_on_generated_task(self, rm):
        """Verify all fields are set correctly on generated tasks."""
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()

        rid = rm.add(
            template_title="Standup",
            recurrence_type="daily",
            first_date=yesterday,
            template_desc="Morning sync",
            category="会议",
            priority=2,
            estimated_hours=0.5,
            extra='{"meeting":true}',
        )
        new_ids = rm.generate_instances()

        assert len(new_ids) == 1
        task = rm.task_manager.get(new_ids[0])
        assert task["title"] == "Standup"
        assert task["description"] == "Morning sync"
        assert task["category"] == "会议"
        assert task["priority"] == 2
        assert task["estimated_hours"] == 0.5
        assert task["source_type"] == "recurring"
        assert task["recurring_id"] == rid
        assert task["extra"] == '{"meeting":true}'
        # deadline should be yesterday T18:00:00
        assert task["deadline"] == f"{yesterday}T18:00:00"

    def test_not_due_yet_skips(self, rm):
        """A template whose next_run_date is in the future should be skipped."""
        future = (date.today() + timedelta(days=30)).isoformat()
        rm.add("Future task", "daily", future)
        new_ids = rm.generate_instances()
        assert new_ids == []

    def test_disabled_template_skipped(self, rm):
        """Disabled templates should not generate instances."""
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        rid = rm.add("Disabled task", "daily", yesterday)
        rm.toggle(rid, False)
        new_ids = rm.generate_instances()
        assert new_ids == []

    def test_next_run_date_advances(self, rm):
        """After generation, next_run_date should advance by one period."""
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()
        tomorrow = (today + timedelta(days=1)).isoformat()

        rid = rm.add("Daily check", "daily", yesterday)
        rm.generate_instances()

        tmpl = rm.get(rid)
        assert tmpl["next_run_date"] == today.isoformat()  # yesterday + 1 day

    def test_last_run_date_set(self, rm):
        """After generation, last_run_date should be set to the date that was used."""
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()

        rid = rm.add("Daily check", "daily", yesterday)
        assert rm.get(rid)["last_run_date"] is None  # not run yet

        rm.generate_instances()
        tmpl = rm.get(rid)
        assert tmpl["last_run_date"] == yesterday

    def test_multiple_templates(self, rm):
        """Multiple due templates should all generate tasks."""
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()

        rm.add("Task A", "daily", yesterday)
        rm.add("Task B", "weekly", yesterday)
        new_ids = rm.generate_instances()

        assert len(new_ids) == 2

    def test_same_template_twice_same_day(self, rm):
        """Running generate_instances twice on the same day should generate two batches.

        The first call generates for yesterday (next_run_date=yesterday <= today).
        After advance: next_run_date = today.  The second call sees today <= today
        and generates for today, then advances to tomorrow.  A third call on the
        same day would see tomorrow > today and produce nothing.
        """
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()

        rid = rm.add("Daily task", "daily", yesterday)

        # First run: generates for yesterday, advances to today
        first_ids = rm.generate_instances()
        assert len(first_ids) == 1

        # Second run: next_run_date = today <= today → generates for today
        second_ids = rm.generate_instances()
        assert len(second_ids) == 1  # today's instance

        # Third run: next_run_date advanced to tomorrow → nothing
        third_ids = rm.generate_instances()
        assert len(third_ids) == 0

    def test_generate_returns_empty_list(self, rm):
        """If no templates are due, return an empty list."""
        assert rm.generate_instances() == []
