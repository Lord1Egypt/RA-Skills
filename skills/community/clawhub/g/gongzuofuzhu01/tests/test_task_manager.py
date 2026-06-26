"""
Tests for task_manager.py — TaskManager CRUD, queries, sort, and stats.

Uses a temporary SQLite database via pytest fixtures so no side effects occur.
"""

import tempfile
import sys
from pathlib import Path

import pytest

# Ensure the *parent* (personal-assistant) is on sys.path so that
# `from scripts.db import Database` and relative imports inside
# `task_manager` resolve correctly.
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.task_manager import TaskManager


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db():
    """Create a fresh in-memory-like database inside a temp file."""
    # Use a real file so multiple connections (via `with self.get_conn()`)
    # see the same data — in-memory :memory: connections each get their own
    # empty DB in the WAL-connection-per-call model.
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


# ---------------------------------------------------------------------------
# CRUD — Add
# ---------------------------------------------------------------------------


class TestAdd:
    def test_add_task(self, tm):
        tid = tm.add("Buy milk")
        assert isinstance(tid, int)
        assert tid > 0

    def test_add_task_with_all_fields(self, tm):
        tid = tm.add(
            title="Design API",
            description="RESTful endpoints for task service",
            category="开发",
            priority=1,
            deadline="2026-06-15T18:00:00",
            start_time="2026-06-01T09:00:00",
            estimated_hours=8.0,
            extra='{"tags":["urgent"]}',
            progress_note="Just started",
        )
        task = tm.get(tid)
        assert task["title"] == "Design API"
        assert task["description"] == "RESTful endpoints for task service"
        assert task["category"] == "开发"
        assert task["priority"] == 1
        assert task["deadline"] == "2026-06-15T18:00:00"
        assert task["start_time"] == "2026-06-01T09:00:00"
        assert task["estimated_hours"] == 8.0
        assert task["extra"] == '{"tags":["urgent"]}'
        assert task["status"] == "todo"  # default


# ---------------------------------------------------------------------------
# CRUD — Get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_task(self, tm):
        tid = tm.add("Write docs")
        task = tm.get(tid)
        assert task is not None
        assert task["title"] == "Write docs"

    def test_get_nonexistent(self, tm):
        assert tm.get(99999) is None


# ---------------------------------------------------------------------------
# CRUD — Update
# ---------------------------------------------------------------------------


class TestUpdate:
    def test_update_task(self, tm):
        tid = tm.add("Old title", priority=3, category="杂务")
        tm.update(tid, title="New title", priority=2)
        task = tm.get(tid)
        assert task["title"] == "New title"
        assert task["priority"] == 2
        assert task["category"] == "杂务"  # unchanged

    def test_update_unknown_field_ignored(self, tm):
        tid = tm.add("Test")
        # Should not crash — unknown kwargs are silently ignored
        tm.update(tid, title="Still works", bogus_field=42)
        assert tm.get(tid)["title"] == "Still works"

    def test_update_no_fields_raises(self, tm):
        tid = tm.add("Test")
        with pytest.raises(ValueError, match="At least one field"):
            tm.update(tid)


# ---------------------------------------------------------------------------
# CRUD — Set status
# ---------------------------------------------------------------------------


class TestSetStatus:
    @pytest.mark.parametrize("status", ["todo", "in_progress", "blocked", "done", "cancelled"])
    def test_set_status(self, tm, status):
        tid = tm.add("Task")
        tm.set_status(tid, status)
        assert tm.get(tid)["status"] == status

    def test_set_status_invalid(self, tm):
        tid = tm.add("Task")
        with pytest.raises(ValueError, match="Invalid status"):
            tm.set_status(tid, "nonexistent")

    def test_set_status_whitespace_and_case(self, tm):
        tid = tm.add("Task")
        tm.set_status(tid, "  IN_PROGRESS  ")
        assert tm.get(tid)["status"] == "in_progress"


# ---------------------------------------------------------------------------
# CRUD — Delete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_soft_delete(self, tm):
        tid = tm.add("Soft task")
        tm.delete(tid)
        task = tm.get(tid)
        assert task is not None  # row still exists
        assert task["status"] == "cancelled"

    def test_hard_delete(self, tm):
        tid = tm.add("Hard task")
        tm.delete(tid, hard=True)
        assert tm.get(tid) is None


# ---------------------------------------------------------------------------
# List — basic
# ---------------------------------------------------------------------------


class TestListBasic:
    def test_list_all(self, tm):
        tm.add("A")
        tm.add("B")
        tm.add("C")
        results = tm.list()
        assert len(results) == 3

    def test_list_empty(self, tm):
        assert tm.list() == []


# ---------------------------------------------------------------------------
# List — filters
# ---------------------------------------------------------------------------


class TestListFilters:
    def test_list_filter_by_status_single(self, tm):
        tm.add("Todo task")
        tid = tm.add("Done task")
        tm.set_status(tid, "done")
        results = tm.list(status="todo")
        assert len(results) == 1
        assert results[0]["status"] == "todo"

    def test_list_filter_by_status_multiple(self, tm):
        tm.add("A")
        tid = tm.add("B")
        tm.set_status(tid, "done")
        tid2 = tm.add("C")
        tm.set_status(tid2, "cancelled")
        results = tm.list(status=["done", "cancelled"])
        assert len(results) == 2

    def test_list_filter_by_category(self, tm):
        tm.add("A", category="开发")
        tm.add("B", category="会议")
        results = tm.list(category="开发")
        assert len(results) == 1
        assert results[0]["category"] == "开发"

    def test_list_filter_by_priority_range(self, tm):
        tm.add("P1", priority=1)
        tm.add("P3", priority=3)
        tm.add("P5", priority=5)
        results = tm.list(priority_min=2, priority_max=4)
        assert len(results) == 1
        assert results[0]["priority"] == 3

    def test_list_filter_by_deadline_range(self, tm):
        tm.add("Early", deadline="2026-01-01T00:00:00")
        tm.add("Mid", deadline="2026-06-15T00:00:00")
        tm.add("Late", deadline="2026-12-31T00:00:00")
        results = tm.list(
            deadline_after="2026-03-01T00:00:00",
            deadline_before="2026-09-01T00:00:00",
        )
        assert len(results) == 1
        assert results[0]["title"] == "Mid"

    def test_list_search(self, tm):
        tm.add("Write API docs", description="Document the REST API")
        tm.add("Fix login bug", description="Urgent bug in auth flow")
        tm.add("Buy groceries")
        results = tm.list(search="api")
        assert len(results) == 1
        assert results[0]["title"] == "Write API docs"

    def test_list_limit_offset(self, tm):
        for i in range(5):
            tm.add(f"Task {i}")
        results = tm.list(limit=2, offset=2)
        assert len(results) == 2


# ---------------------------------------------------------------------------
# List — ordering
# ---------------------------------------------------------------------------


class TestListOrdering:
    def test_list_order_by_priority_asc(self, tm):
        tm.add("Low", priority=5)
        tm.add("High", priority=1)
        tm.add("Mid", priority=3)
        results = tm.list(order_by="priority")
        assert results[0]["priority"] == 1
        assert results[1]["priority"] == 3
        assert results[2]["priority"] == 5

    def test_list_order_by_deadline_desc(self, tm):
        tm.add("Early", deadline="2026-01-01T00:00:00")
        tm.add("Mid", deadline="2026-06-15T00:00:00")
        tm.add("Late", deadline="2026-12-31T00:00:00")
        results = tm.list(order_by="deadline")
        assert results[0]["deadline"] == "2026-12-31T00:00:00"
        assert results[1]["deadline"] == "2026-06-15T00:00:00"
        assert results[2]["deadline"] == "2026-01-01T00:00:00"

    def test_list_order_by_created_at(self, tm):
        import time

        tm.add("First")
        time.sleep(1.1)  # ensure timestamps differ
        tm.add("Second")
        results = tm.list(order_by="created_at")
        # Most recent first (DESC)
        assert results[0]["title"] == "Second"
        assert results[1]["title"] == "First"


# ---------------------------------------------------------------------------
# today / upcoming / overdue
# ---------------------------------------------------------------------------


class TestToday:
    def test_today(self, tm):
        tm.add("No deadline")
        tm.add("Past deadline", deadline="2020-01-01T00:00:00")
        tm.add("Future deadline", deadline="2099-01-01T00:00:00")
        results = tm.today()
        # Past deadline AND no-deadline should show; future should not
        assert len(results) == 2
        titles = {r["title"] for r in results}
        assert "No deadline" in titles
        assert "Past deadline" in titles

    def test_today_excludes_done(self, tm):
        tid = tm.add("Done task")
        tm.set_status(tid, "done")
        results = tm.today()
        assert all(r["title"] != "Done task" for r in results)

    def test_today_excludes_cancelled(self, tm):
        tid = tm.add("Cancelled task")
        tm.set_status(tid, "cancelled")
        results = tm.today()
        assert all(r["title"] != "Cancelled task" for r in results)


class TestUpcoming:
    def test_upcoming(self, tm):
        tm.add("Past", deadline="2020-01-01T00:00:00")
        tm.add("Far future", deadline="2099-01-01T00:00:00")
        # Add a task with a deadline in the future (depends on today's date)
        # Just verify the method runs and returns something sane
        results = tm.upcoming(days=365 * 100)  # big enough window
        assert len(results) >= 1  # at least Far future


class TestOverdue:
    def test_overdue(self, tm):
        tm.add("Past task", deadline="2020-01-01T00:00:00")
        tm.add("Future task", deadline="2099-01-01T00:00:00")
        tm.add("No deadline")
        results = tm.overdue()
        assert len(results) == 1
        assert results[0]["title"] == "Past task"

    def test_overdue_excludes_done(self, tm):
        tid = tm.add("Past but done", deadline="2020-01-01T00:00:00")
        tm.set_status(tid, "done")
        assert tm.overdue() == []


# ---------------------------------------------------------------------------
# by_okr / search
# ---------------------------------------------------------------------------


class TestByOkr:
    def test_by_okr(self, tm):
        # Create OKR items first (FK constraint)
        tm.db.insert("okr_items", {"id": 1, "title": "OKR 1", "obj_type": "objective"})
        tm.db.insert("okr_items", {"id": 2, "title": "OKR 2", "obj_type": "objective"})
        tm.add("OKR task 1", okr_id=1)
        tm.add("OKR task 2", okr_id=1)
        tm.add("Other task", okr_id=2)
        results = tm.by_okr(1)
        assert len(results) == 2
        assert all(r["okr_id"] == 1 for r in results)

    def test_by_okr_empty(self, tm):
        assert tm.by_okr(999) == []


class TestSearch:
    def test_search(self, tm):
        tm.add("Write API documentation", description="Cover all endpoints")
        tm.add("Fix login bug", description="Auth flow broken")
        tm.add("Buy groceries")
        results = tm.search("api")
        assert len(results) == 1
        assert "API" in results[0]["title"]

    def test_search_no_results(self, tm):
        tm.add("Task A")
        assert tm.search("zzz_nonexistent_zzz") == []


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_stats(self, tm):
        tm.add("A", category="开发", priority=1)
        tid = tm.add("B", category="开发", priority=2)
        tm.set_status(tid, "done")
        tm.add("C", category="会议", priority=3)

        s = tm.stats()
        assert s["by_status"] == {"todo": 2, "done": 1}
        assert s["by_priority"] == {"1": 1, "2": 1, "3": 1}
        assert s["by_category"] == {"开发": 2, "会议": 1}

    def test_stats_empty(self, tm):
        s = tm.stats()
        assert s["by_status"] == {}
        assert s["by_priority"] == {}
        assert s["by_category"] == {}
