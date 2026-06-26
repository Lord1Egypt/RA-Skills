"""
Tests for the Personal Assistant database layer (Sprint 0).

Uses pytest + temporary databases via tempfile.
"""

import os
import tempfile
import json
from pathlib import Path

import pytest

# Add the scripts directory to the import path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from db import Database


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_db():
    """Create a Database instance backed by a temporary file; init schema."""
    fd, path = tempfile.mkstemp(suffix=".db", prefix="pa_test_")
    os.close(fd)
    db = Database(db_path=path)
    db.init_db()
    yield db
    # Cleanup
    db.close()
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture
def tmp_db_with_task(tmp_db):
    """Database with one pre-inserted task."""
    task_id = tmp_db.insert("tasks", {
        "title": "Test Task",
        "description": "A test task",
        "category": "dev",
        "status": "todo",
        "priority": 3,
        "deadline": "2026-12-31T18:00:00",
    })
    return tmp_db, task_id


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

# --- 1. Schema & Init ------------------------------------------------------

def test_init_db_creates_all_tables(tmp_db):
    """Verify all 6 tables exist after init_db()."""
    expected_tables = {
        "tasks", "milestones", "progress_logs",
        "recurring_tasks", "okr_items", "reminder_log",
    }

    tables = tmp_db.fetch_all(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    table_names = {r["name"] for r in tables}

    assert expected_tables.issubset(table_names), \
        f"Missing tables: {expected_tables - table_names}"


def test_init_db_creates_indexes(tmp_db):
    """Verify key indexes are created."""
    indexes = tmp_db.fetch_all(
        "SELECT name FROM sqlite_master WHERE type='index'"
    )
    index_names = {r["name"] for r in indexes}

    expected_indexes = {
        "idx_tasks_status", "idx_tasks_deadline", "idx_tasks_priority",
        "idx_tasks_category", "idx_tasks_parent", "idx_tasks_okr",
        "idx_milestones_task",
        "idx_progress_logs_task", "idx_progress_logs_date",
        "idx_okr_status", "idx_okr_parent", "idx_okr_source",
    }
    assert expected_indexes.issubset(index_names), \
        f"Missing indexes: {expected_indexes - index_names}"


def test_wal_mode_enabled(tmp_db):
    """Verify WAL journal mode is active."""
    row = tmp_db.fetch_one("PRAGMA journal_mode")
    assert row is not None
    assert row["journal_mode"].lower() == "wal"


def test_foreign_keys_enabled(tmp_db):
    """Verify foreign_keys PRAGMA is ON."""
    row = tmp_db.fetch_one("PRAGMA foreign_keys")
    assert row is not None
    assert row["foreign_keys"] == 1


# --- 2. CRUD Operations ----------------------------------------------------

def test_insert_and_fetch(tmp_db):
    """Insert a task then fetch it back; verify all fields."""
    task_id = tmp_db.insert("tasks", {
        "title": "Finish Q2 Report",
        "description": "Write the quarterly summary",
        "category": "docs",
        "status": "todo",
        "priority": 2,
        "deadline": "2026-06-30T18:00:00",
        "estimated_hours": 8.0,
    })
    assert task_id == 1

    task = tmp_db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
    assert task is not None
    assert task["title"] == "Finish Q2 Report"
    assert task["status"] == "todo"
    assert task["priority"] == 2
    assert task["estimated_hours"] == 8.0
    assert task["progress"] == 0
    assert task["source_type"] == "manual"
    assert task["created_at"] is not None


def test_insert_multiple_and_fetch_all(tmp_db):
    """Insert multiple rows and verify fetch_all returns all of them."""
    tmp_db.insert("tasks", {"title": "Task 1", "status": "todo", "priority": 1})
    tmp_db.insert("tasks", {"title": "Task 2", "status": "in_progress", "priority": 3})
    tmp_db.insert("tasks", {"title": "Task 3", "status": "done", "priority": 5})

    rows = tmp_db.fetch_all("SELECT * FROM tasks ORDER BY id")
    assert len(rows) == 3
    assert rows[0]["title"] == "Task 1"
    assert rows[1]["title"] == "Task 2"
    assert rows[2]["title"] == "Task 3"


def test_update(tmp_db_with_task):
    """Update task fields and verify changes persisted."""
    tmp_db, task_id = tmp_db_with_task

    tmp_db.update(
        "tasks",
        {"status": "in_progress", "progress": 50, "progress_note": "Half done"},
        "id = ?",
        (task_id,),
    )

    task = tmp_db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
    assert task["status"] == "in_progress"
    assert task["progress"] == 50
    assert task["progress_note"] == "Half done"


def test_delete(tmp_db_with_task):
    """Delete a task and verify it's gone."""
    tmp_db, task_id = tmp_db_with_task

    tmp_db.delete("tasks", "id = ?", (task_id,))
    task = tmp_db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
    assert task is None


def test_delete_nonexistent(tmp_db):
    """Deleting a non-existent row should not raise."""
    tmp_db.delete("tasks", "id = ?", (999,))
    # Should not raise


# --- 3. Foreign Key Cascade ------------------------------------------------

def test_foreign_key_cascade_milestones(tmp_db_with_task):
    """Deleting a task cascades to its milestones."""
    tmp_db, task_id = tmp_db_with_task

    # Add milestones
    m1 = tmp_db.insert("milestones", {"task_id": task_id, "title": "M1"})
    m2 = tmp_db.insert("milestones", {"task_id": task_id, "title": "M2"})

    # Verify they exist
    assert tmp_db.fetch_one("SELECT * FROM milestones WHERE id = ?", (m1,)) is not None

    # Delete the task
    tmp_db.delete("tasks", "id = ?", (task_id,))

    # Milestones should be cascade-deleted
    assert tmp_db.fetch_one("SELECT * FROM milestones WHERE id = ?", (m1,)) is None
    assert tmp_db.fetch_one("SELECT * FROM milestones WHERE id = ?", (m2,)) is None


def test_foreign_key_cascade_progress_logs(tmp_db_with_task):
    """Deleting a task cascades to its progress_logs."""
    tmp_db, task_id = tmp_db_with_task

    # Add progress log
    log_id = tmp_db.insert("progress_logs", {
        "task_id": task_id,
        "content": "Started working",
        "progress_before": 0,
        "progress_after": 25,
        "hours_spent": 2.0,
    })

    assert tmp_db.fetch_one("SELECT * FROM progress_logs WHERE id = ?", (log_id,)) is not None

    # Delete the task
    tmp_db.delete("tasks", "id = ?", (task_id,))

    # Progress log should be cascade-deleted
    assert tmp_db.fetch_one("SELECT * FROM progress_logs WHERE id = ?", (log_id,)) is None


def test_foreign_key_reminder_log_cascade(tmp_db_with_task):
    """Deleting a task cascades to its reminder_log entries."""
    tmp_db, task_id = tmp_db_with_task

    # Insert a reminder_log entry
    tmp_db.execute(
        "INSERT INTO reminder_log (task_id, reminder_type, reminder_date, message) VALUES (?, 'morning', '2026-05-26', 'test')",
        (task_id,)
    )

    row = tmp_db.fetch_one("SELECT id FROM reminder_log WHERE task_id = ?", (task_id,))
    assert row is not None

    tmp_db.delete("tasks", "id = ?", (task_id,))

    # Should be cascade-deleted
    row = tmp_db.fetch_one("SELECT id FROM reminder_log WHERE task_id = ?", (task_id,))
    assert row is None


def test_foreign_key_set_null_parent_task(tmp_db):
    """Deleting a parent task sets child's parent_task_id to NULL."""
    parent_id = tmp_db.insert("tasks", {"title": "Parent", "status": "todo", "priority": 3})
    child_id = tmp_db.insert("tasks", {
        "title": "Child",
        "status": "todo",
        "priority": 3,
        "parent_task_id": parent_id,
    })

    tmp_db.delete("tasks", "id = ?", (parent_id,))

    child = tmp_db.fetch_one("SELECT * FROM tasks WHERE id = ?", (child_id,))
    assert child is not None
    assert child["parent_task_id"] is None


# --- 4. CHECK Constraints --------------------------------------------------

def test_check_constraints_invalid_status(tmp_db):
    """Insert with invalid status should raise IntegrityError."""
    with pytest.raises(Exception):  # sqlite3.IntegrityError
        tmp_db.insert("tasks", {
            "title": "Bad Task",
            "status": "invalid_status",
            "priority": 3,
        })


def test_check_constraints_invalid_priority(tmp_db):
    """Insert with out-of-range priority should raise IntegrityError."""
    with pytest.raises(Exception):
        tmp_db.insert("tasks", {
            "title": "Bad Priority",
            "status": "todo",
            "priority": 10,
        })


def test_check_constraints_invalid_source_type(tmp_db):
    """Insert with invalid source_type should raise IntegrityError."""
    with pytest.raises(Exception):
        tmp_db.insert("tasks", {
            "title": "Bad Source",
            "status": "todo",
            "priority": 3,
            "source_type": "unknown_source",
        })


def test_check_constraints_invalid_progress(tmp_db):
    """Insert with progress out of 0-100 should raise IntegrityError."""
    with pytest.raises(Exception):
        tmp_db.insert("tasks", {
            "title": "Bad Progress",
            "status": "todo",
            "priority": 3,
            "progress": 150,
        })


def test_check_constraints_okr_items(tmp_db):
    """Insert invalid obj_type into okr_items should raise."""
    with pytest.raises(Exception):
        tmp_db.insert("okr_items", {
            "title": "Bad OKR",
            "obj_type": "invalid_type",
        })


def test_check_constraints_reminder_log(tmp_db_with_task):
    """Insert invalid reminder_type should raise."""
    tmp_db, task_id = tmp_db_with_task
    with pytest.raises(Exception):
        tmp_db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'midnight', '2026-05-26')",
            (task_id,)
        )


# --- 5. UNIQUE Constraint (reminder_log) -----------------------------------

def test_reminder_log_unique_constraint(tmp_db_with_task):
    """Duplicate (task_id, reminder_type, reminder_date) should raise."""
    tmp_db, task_id = tmp_db_with_task

    tmp_db.execute(
        "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', '2026-05-26')",
        (task_id,)
    )

    with pytest.raises(Exception):
        tmp_db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', '2026-05-26')",
            (task_id,)
        )


# --- 6. Export / Import Roundtrip -----------------------------------------

def test_export_import_roundtrip(tmp_db):
    """Export data, re-init from blank, import, verify data preserved."""
    # Insert some data
    t1 = tmp_db.insert("tasks", {"title": "Alpha", "status": "todo", "priority": 1})
    t2 = tmp_db.insert("tasks", {"title": "Beta", "status": "done", "priority": 4})
    tmp_db.insert("milestones", {"task_id": t1, "title": "Milestone A"})
    tmp_db.insert("progress_logs", {
        "task_id": t1, "content": "Log entry", "progress_before": 0, "progress_after": 50,
    })

    # Export
    export_path = tmp_db.db_path.parent / "export_dump.sql"
    tmp_db.export(str(export_path))

    assert export_path.exists()
    dump_content = export_path.read_text(encoding="utf-8")
    assert "Alpha" in dump_content
    assert "Beta" in dump_content
    assert "Milestone A" in dump_content
    assert "Log entry" in dump_content

    # Create a brand new database
    fd, new_path = tempfile.mkstemp(suffix=".db", prefix="pa_import_")
    os.close(fd)
    new_db = Database(db_path=new_path)
    new_db.init_db()

    # Import the dump
    new_db.import_(str(export_path))

    # Verify data
    tasks = new_db.fetch_all("SELECT * FROM tasks ORDER BY id")
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Alpha"
    assert tasks[1]["title"] == "Beta"

    milestones = new_db.fetch_all("SELECT * FROM milestones")
    assert len(milestones) == 1
    assert milestones[0]["title"] == "Milestone A"

    logs = new_db.fetch_all("SELECT * FROM progress_logs")
    assert len(logs) == 1
    assert logs[0]["content"] == "Log entry"

    # Cleanup
    new_db.close()
    try:
        os.unlink(new_path)
    except OSError:
        pass
    try:
        os.unlink(str(export_path))
    except OSError:
        pass


# --- 7. Stats --------------------------------------------------------------

def test_stats(tmp_db_with_task):
    """stats() returns correct row counts and db size."""
    tmp_db, task_id = tmp_db_with_task

    stats = tmp_db.stats()
    assert "tables" in stats
    assert "db_size_bytes" in stats
    assert "db_path" in stats

    # At least the tasks table should have 1 row
    assert stats["tables"]["tasks"] == 1

    # Other tables should be 0
    for t in ["milestones", "progress_logs", "recurring_tasks", "okr_items", "reminder_log"]:
        assert stats["tables"][t] == 0, f"Table {t} should be empty"

    assert stats["db_size_bytes"] > 0
    assert str(tmp_db.db_path) in stats["db_path"]


def test_stats_empty_db(tmp_db):
    """stats() on an empty database shows zero rows."""
    stats = tmp_db.stats()
    for count in stats["tables"].values():
        assert count == 0


# --- 8. Cleanup ------------------------------------------------------------

def test_cleanup_removes_old_reminder_logs(tmp_db_with_task):
    """cleanup() removes reminder_log entries older than 30 days."""
    tmp_db, task_id = tmp_db_with_task

    # Insert an old reminder (40 days ago)
    tmp_db.execute(
        "INSERT INTO reminder_log (task_id, reminder_type, reminder_date, sent_at) "
        "VALUES (?, 'morning', date('now', 'localtime', '-40 days'), datetime('now', 'localtime', '-40 days'))",
        (task_id,)
    )
    # Insert a recent reminder (5 days ago)
    tmp_db.execute(
        "INSERT INTO reminder_log (task_id, reminder_type, reminder_date, sent_at) "
        "VALUES (?, 'afternoon', date('now', 'localtime', '-5 days'), datetime('now', 'localtime', '-5 days'))",
        (task_id,)
    )

    # Verify both exist
    all_logs = tmp_db.fetch_all("SELECT * FROM reminder_log ORDER BY id")
    assert len(all_logs) == 2

    tmp_db.cleanup()

    remaining = tmp_db.fetch_all("SELECT * FROM reminder_log ORDER BY id")
    assert len(remaining) == 1
    assert remaining[0]["reminder_type"] == "afternoon"


# --- 9. Edge Cases ---------------------------------------------------------

def test_init_db_idempotent(tmp_db):
    """Calling init_db() multiple times should not raise errors."""
    tmp_db.init_db()
    tmp_db.init_db()  # Second call should be safe
    test_init_db_creates_all_tables(tmp_db)  # Tables still exist


def test_insert_empty_data(tmp_db):
    """Insert with only defaults should work for nullable columns."""
    # Only provide required fields
    task_id = tmp_db.insert("tasks", {"title": "Minimal Task"})
    task = tmp_db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
    assert task["status"] == "todo"
    assert task["priority"] == 3
    assert task["progress"] == 0
    assert task["source_type"] == "manual"


def test_db_path_expanduser():
    """Database path with ~ should be expanded properly."""
    db = Database(db_path="~/test_expanded.db")
    assert str(db.db_path) == os.path.expanduser("~/test_expanded.db")
    # Don't actually create a file; just verify expansion


def test_auto_create_parent_dir(tmp_path):
    """init_db() should create parent directories if they don't exist."""
    nested = tmp_path / "deep" / "nested" / "test.db"
    db = Database(db_path=str(nested))
    db.init_db()

    assert nested.exists()
    test_init_db_creates_all_tables(db)

    db.close()
