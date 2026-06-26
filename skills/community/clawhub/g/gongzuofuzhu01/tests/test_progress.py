"""
Tests for progress.py — ProgressTracker: progress logging and milestone management.

Uses a temporary SQLite database via pytest fixtures so no side effects occur.
"""

import tempfile
import sys
from pathlib import Path

import pytest

# Ensure the *parent* (personal-assistant) is on sys.path so that
# `from scripts.db import Database` and relative imports inside
# `progress` resolve correctly.
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.task_manager import TaskManager
from scripts.progress import ProgressTracker


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db():
    """Create a fresh SQLite database inside a temp file."""
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
    # Clean up
    try:
        Path(tmp.name).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture
def tm(db):
    """TaskManager wired to a fresh database."""
    return TaskManager(db)


@pytest.fixture
def pt(db, tm):
    """ProgressTracker wired to a fresh database + TaskManager."""
    return ProgressTracker(db, tm)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _add_task(tm, title="Test task", **kwargs):
    return tm.add(title, **kwargs)


# ---------------------------------------------------------------------------
# log()
# ---------------------------------------------------------------------------


class TestLog:
    def test_log_basic(self, pt, tm):
        """log() creates a progress_log entry and returns a valid id."""
        tid = _add_task(tm, "Basic task")
        log_id = pt.log(tid, "Started working on it")
        assert isinstance(log_id, int)
        assert log_id > 0

    def test_log_content_persisted(self, pt, tm, db):
        """log() stores content, progress_before, progress_after, and hours_spent."""
        tid = _add_task(tm, "Write tests")
        pt.log(tid, "Wrote unit tests", hours_spent=2.5)

        row = db.fetch_one(
            "SELECT * FROM progress_logs WHERE task_id = ?", (tid,)
        )
        assert row is not None
        assert row["content"] == "Wrote unit tests"
        assert row["progress_before"] == 0  # default task progress
        assert row["progress_after"] == 0
        assert row["hours_spent"] == 2.5

    def test_log_captures_progress_before(self, pt, tm):
        """log() reads the task's current progress as progress_before."""
        tid = _add_task(tm, "Halfway task")
        tm.update(tid, progress=50)

        pt.log(tid, "Still working", new_progress=70)
        logs = pt.history(tid)
        assert logs[0]["progress_before"] == 50
        assert logs[0]["progress_after"] == 70

    def test_log_nonexistent_task_raises(self, pt):
        """log() raises ValueError for a non-existent task."""
        with pytest.raises(ValueError, match="not found"):
            pt.log(99999, "Ghost task")

    def test_log_accumulates_hours_without_progress_change(self, pt, tm):
        """hours_spent is added to actual_hours even when new_progress is None."""
        tid = _add_task(tm, "Time tracking task")
        pt.log(tid, "First session", hours_spent=1.0)
        pt.log(tid, "Second session", hours_spent=2.0)

        task = tm.get(tid)
        assert task["actual_hours"] == 3.0


# ---------------------------------------------------------------------------
# log() — syncs task.progress
# ---------------------------------------------------------------------------


class TestLogUpdatesTask:
    def test_log_updates_task_progress(self, pt, tm):
        """When new_progress is given, task.progress is updated."""
        tid = _add_task(tm, "Progress sync")
        pt.log(tid, "Made progress", new_progress=30)
        task = tm.get(tid)
        assert task["progress"] == 30

    def test_log_updates_actual_hours_with_progress(self, pt, tm):
        """actual_hours accumulates when new_progress is set."""
        tid = _add_task(tm, "Hours+progress", estimated_hours=10)
        pt.log(tid, "First day", hours_spent=3, new_progress=40)
        pt.log(tid, "Second day", hours_spent=4, new_progress=80)

        task = tm.get(tid)
        assert task["actual_hours"] == 7.0
        assert task["progress"] == 80


# ---------------------------------------------------------------------------
# history()
# ---------------------------------------------------------------------------


class TestHistory:
    def test_history_returns_all(self, pt, tm):
        """history() returns all logs for a task, newest first."""
        tid = _add_task(tm, "History task")
        pt.log(tid, "Entry 1")
        pt.log(tid, "Entry 2")
        pt.log(tid, "Entry 3")

        entries = pt.history(tid)
        assert len(entries) == 3
        # newest first
        assert entries[0]["content"] == "Entry 3"
        assert entries[2]["content"] == "Entry 1"

    def test_history_respects_limit(self, pt, tm):
        """history() respects the limit parameter."""
        tid = _add_task(tm, "Limit test")
        for i in range(25):
            pt.log(tid, f"Log {i}")

        entries = pt.history(tid, limit=5)
        assert len(entries) == 5

    def test_history_empty(self, pt, tm):
        """history() returns empty list for task with no logs."""
        tid = _add_task(tm, "No logs")
        assert pt.history(tid) == []


# ---------------------------------------------------------------------------
# timeline()
# ---------------------------------------------------------------------------


class TestTimeline:
    def test_timeline_date_range(self, pt, tm):
        """timeline() filters by start_date and end_date."""
        tid = _add_task(tm, "Timeline task")

        # Logs each have an auto-generated logged_at timestamp.
        pt.log(tid, "Today's work")

        # With a wide range, the entry should appear.
        results = pt.timeline(start_date="2000-01-01", end_date="2099-12-31")
        assert len(results) >= 1
        assert results[0]["content"] == "Today's work"

    def test_timeline_excludes_out_of_range(self, pt, tm):
        """timeline() excludes logs outside the date range."""
        tid = _add_task(tm, "Date range task")
        pt.log(tid, "Recent")

        # A past-only range should exclude today's entry
        results = pt.timeline(
            start_date="2000-01-01", end_date="2000-12-31"
        )
        assert results == []

    def test_timeline_no_filters(self, pt, tm):
        """timeline() with no arguments returns all logs chronologically."""
        tid = _add_task(tm, "All logs")
        pt.log(tid, "First")
        pt.log(tid, "Second")

        results = pt.timeline()
        assert len(results) == 2
        # chronological: first, then second
        assert results[0]["content"] == "First"
        assert results[1]["content"] == "Second"


# ---------------------------------------------------------------------------
# add_milestone()
# ---------------------------------------------------------------------------


class TestAddMilestone:
    def test_add_milestone_basic(self, pt, tm):
        """add_milestone() creates a milestone and returns its id."""
        tid = _add_task(tm, "Milestone task")
        mid = pt.add_milestone(tid, "Design complete")
        assert isinstance(mid, int)
        assert mid > 0

    def test_add_milestone_with_due_date(self, pt, tm, db):
        """add_milestone() stores due_date when provided."""
        tid = _add_task(tm, "Dated milestone")
        pt.add_milestone(tid, "API ready", due_date="2026-06-15T18:00:00")

        row = db.fetch_one(
            "SELECT * FROM milestones WHERE task_id = ?", (tid,)
        )
        assert row["due_date"] == "2026-06-15T18:00:00"
        assert row["status"] == "pending"


# ---------------------------------------------------------------------------
# complete_milestone()
# ---------------------------------------------------------------------------


class TestCompleteMilestone:
    def test_complete_milestone(self, pt, tm, db):
        """complete_milestone() sets status='completed' and a timestamp."""
        tid = _add_task(tm, "Finish milestone")
        mid = pt.add_milestone(tid, "Done")

        pt.complete_milestone(mid)

        row = db.fetch_one("SELECT * FROM milestones WHERE id = ?", (mid,))
        assert row["status"] == "completed"
        assert row["completed_at"] is not None


# ---------------------------------------------------------------------------
# list_milestones()
# ---------------------------------------------------------------------------


class TestListMilestones:
    def test_list_milestones_order(self, pt, tm):
        """list_milestones() returns milestones sorted by sort_order."""
        tid = _add_task(tm, "Ordered task")
        pt.add_milestone(tid, "Third", sort_order=3)
        pt.add_milestone(tid, "First", sort_order=1)
        pt.add_milestone(tid, "Second", sort_order=2)

        milestones = pt.list_milestones(tid)
        assert len(milestones) == 3
        assert milestones[0]["title"] == "First"
        assert milestones[1]["title"] == "Second"
        assert milestones[2]["title"] == "Third"

    def test_list_milestones_empty(self, pt, tm):
        """list_milestones() returns empty list for task with no milestones."""
        tid = _add_task(tm, "No milestones")
        assert pt.list_milestones(tid) == []


# ---------------------------------------------------------------------------
# milestone_progress()
# ---------------------------------------------------------------------------


class TestMilestoneProgress:
    def test_milestone_progress_all_pending(self, pt, tm):
        """milestone_progress() reports 0% when none completed."""
        tid = _add_task(tm, "All pending")
        pt.add_milestone(tid, "A")
        pt.add_milestone(tid, "B")
        pt.add_milestone(tid, "C")

        mp = pt.milestone_progress(tid)
        assert mp == {"total": 3, "completed": 0, "percent": 0}

    def test_milestone_progress_mixed(self, pt, tm):
        """milestone_progress() calculates correct percent for mixed states."""
        tid = _add_task(tm, "Mixed")
        pt.add_milestone(tid, "A")
        m2 = pt.add_milestone(tid, "B")
        pt.add_milestone(tid, "C")

        pt.complete_milestone(m2)

        mp = pt.milestone_progress(tid)
        assert mp["total"] == 3
        assert mp["completed"] == 1
        assert mp["percent"] == 33  # 1/3 * 100 = 33.33 → 33

    def test_milestone_progress_empty(self, pt, tm):
        """milestone_progress() returns zeros when no milestones exist."""
        tid = _add_task(tm, "Empty milestones")
        mp = pt.milestone_progress(tid)
        assert mp == {"total": 0, "completed": 0, "percent": 0}

    def test_milestone_progress_fully_completed(self, pt, tm):
        """milestone_progress() reports 100% when all completed."""
        tid = _add_task(tm, "All done")
        for title in ("A", "B"):
            mid = pt.add_milestone(tid, title)
            pt.complete_milestone(mid)

        mp = pt.milestone_progress(tid)
        assert mp == {"total": 2, "completed": 2, "percent": 100}
