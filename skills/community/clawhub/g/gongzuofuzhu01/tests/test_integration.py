"""
Integration tests for Personal Assistant skill — end-to-end workflows.

Tests cover:
- Full workflow: add task → check today → log progress → reminder → complete
- Recurring workflow: add recurring → generate instances → verify
- OKR sync to report: sync OKR → link tasks → generate report with OKR progress
- Reminder dedup: multiple reminders do not duplicate
- Soft delete: cancelled tasks still appear in reports/stats
"""

import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

# Ensure the parent (personal-assistant) is on sys.path
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.task_manager import TaskManager
from scripts.progress import ProgressTracker
from scripts.recurring import RecurringManager
from scripts.reminder import ReminderEngine
from scripts.okr import OKRManager
from scripts.report import ReportGenerator
from scripts.advisor import Advisor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db():
    """Fresh temporary database with schema initialised."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()

    database = Database(db_path=tmp.name)
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
def pt(db, tm):
    """ProgressTracker wired to temp db."""
    return ProgressTracker(db, tm)


@pytest.fixture
def rm(db, tm):
    """RecurringManager wired to temp db."""
    return RecurringManager(db, tm)


@pytest.fixture
def engine(db, tm):
    """ReminderEngine wired to temp db."""
    return ReminderEngine(db, tm)


@pytest.fixture
def okr(db):
    """OKRManager wired to temp db."""
    return OKRManager(db)


@pytest.fixture
def report(db, tm, pt, okr):
    """ReportGenerator wired to temp db."""
    return ReportGenerator(db, tm, pt, okr)


@pytest.fixture
def advisor(db, tm, okr):
    """Advisor wired to temp db."""
    return Advisor(db, tm, okr)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _days_from_now(days: int) -> str:
    dt = datetime.now() + timedelta(days=days)
    return dt.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()


def _hours_from_now(hours: int) -> str:
    """Return an ISO datetime string *hours* from now, clamped to today."""
    dt = datetime.now() + timedelta(hours=hours)
    # Ensure the deadline is today by using today's date + the computed time
    today = date.today()
    dt = datetime.combine(today, dt.time())
    return dt.isoformat()


# ---------------------------------------------------------------------------
# 1. Full workflow: add → today → progress → reminder → complete
# ---------------------------------------------------------------------------


class TestFullWorkflow:
    """End-to-end: add task → check today → log progress → remind → complete."""

    def test_add_to_remind_to_complete(self, tm, pt, engine):
        """Full lifecycle of a task from creation to completion with reminders."""
        # 1) Add a task
        tid = tm.add(
            title="Write integration tests",
            description="Ensure all modules work together",
            category="开发",
            priority=2,
            deadline=_hours_from_now(5),
            estimated_hours=3.0,
        )
        assert tid > 0

        # 2) Verify task appears in today's list
        today_tasks = tm.today()
        today_ids = {t["id"] for t in today_tasks}
        assert tid in today_ids

        # 3) Log progress
        log_id = pt.log(tid, "Started writing tests", hours_spent=1.0, new_progress=30)
        assert log_id > 0

        task = tm.get(tid)
        assert task["progress"] == 30
        assert task["actual_hours"] == 1.0

        # 4) Get tasks for reminder
        reminder_tasks = engine.get_tasks_for_reminder("morning")
        reminder_ids = {t["id"] for t in reminder_tasks}
        assert tid in reminder_ids

        # 5) Format and log the reminder
        msg = engine.format_reminder(reminder_tasks, "morning")
        assert "Write integration tests" in msg

        engine.log_reminder([tid], "morning", msg)

        # 6) Same task should NOT appear in same reminder type today (dedup)
        reminder_tasks_2 = engine.get_tasks_for_reminder("morning")
        reminder_ids_2 = {t["id"] for t in reminder_tasks_2}
        assert tid not in reminder_ids_2, "Task should be deduped after reminder"

        # 7) Complete the task
        pt.log(tid, "All tests pass", hours_spent=2.0, new_progress=100)
        tm.set_status(tid, "done")

        task = tm.get(tid)
        assert task["status"] == "done"
        assert task["progress"] == 100
        assert task["actual_hours"] == 3.0

        # 8) Done task should not appear in today
        today_after = tm.today()
        today_after_ids = {t["id"] for t in today_after}
        assert tid not in today_after_ids

    def test_multiple_tasks_workflow(self, tm, pt, engine):
        """Multiple tasks through the full workflow simultaneously."""
        # Add tasks
        t1 = tm.add("Task Alpha", priority=1, deadline=_hours_from_now(3))
        t2 = tm.add("Task Beta", priority=3, deadline=_hours_from_now(8))  # same-day deadline
        t3 = tm.add("Task Gamma", priority=5)

        # t1 & t2 (today deadline) + t3 (no deadline) should be in today
        today = tm.today()
        today_ids = {t["id"] for t in today}
        assert t1 in today_ids
        assert t2 in today_ids
        assert t3 in today_ids

        # Log progress on t1
        pt.log(t1, "Alpha started", hours_spent=0.5, new_progress=50)
        pt.log(t2, "Beta started", hours_spent=0.5, new_progress=20)

        # Reminder should include all three
        tasks = engine.get_tasks_for_reminder("morning")
        assert len(tasks) == 3

        # Sort by urgency: t1 should be first (deadline within 24h)
        sorted_tasks = engine.sort_by_urgency(tasks)
        assert sorted_tasks[0]["id"] == t1


# ---------------------------------------------------------------------------
# 2. Recurring workflow: add template → generate → verify instance
# ---------------------------------------------------------------------------


class TestRecurringWorkflow:
    """Recurring task: template → instance → verification."""

    def test_recurring_generates_instance(self, rm):
        """Add a recurring template and generate task instance."""
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()

        rid = rm.add(
            template_title="Daily standup",
            recurrence_type="daily",
            first_date=yesterday,
            template_desc="Morning team sync",
            category="会议",
            priority=2,
            estimated_hours=0.5,
        )

        # Generate instances
        new_ids = rm.generate_instances()
        assert len(new_ids) == 1

        # Verify instance was created
        task = rm.task_manager.get(new_ids[0])
        assert task["title"] == "Daily standup"
        assert task["description"] == "Morning team sync"
        assert task["source_type"] == "recurring"
        assert task["recurring_id"] == rid
        assert task["deadline"] == f"{yesterday}T18:00:00"

        # next_run_date should be advanced
        tmpl = rm.get(rid)
        assert tmpl["next_run_date"] == today.isoformat()

    def test_recurring_weekly_generates_multiple(self, rm):
        """Weekly recurring tasks generate correctly."""
        today = date.today()
        days_ago_10 = (today - timedelta(days=10)).isoformat()

        rid = rm.add("Weekly review", "weekly", days_ago_10, priority=3)

        # First run: generates for days_ago_10, advances to days_ago_10 + 7
        ids_1 = rm.generate_instances()
        assert len(ids_1) == 1

        schedule_date_1 = (today - timedelta(days=10)).isoformat()
        task_1 = rm.task_manager.get(ids_1[0])
        assert task_1["deadline"] == f"{schedule_date_1}T18:00:00"

        # next should be days_ago_10 + 7
        expected_next = (date.today() - timedelta(days=3)).isoformat()
        tmpl = rm.get(rid)
        assert tmpl["next_run_date"] == expected_next

        # Second run: if next is still <= today, generates again
        ids_2 = rm.generate_instances()
        assert len(ids_2) == 1

    def test_recurring_disabled_template_skipped(self, rm):
        """Disabled templates should not generate instances."""
        today = date.today()
        yesterday = (today - timedelta(days=1)).isoformat()

        rid = rm.add("Should not generate", "daily", yesterday)
        rm.toggle(rid, False)

        new_ids = rm.generate_instances()
        assert new_ids == []


# ---------------------------------------------------------------------------
# 3. OKR sync → link tasks → report contains OKR progress
# ---------------------------------------------------------------------------


class TestOkrSyncToReport:
    """OKR data appears in monthly reports."""

    def test_okr_progress_in_monthly(self, tm, okr, report):
        """Monthly report includes OKR progress."""
        oid = okr.add_objective("提升产品稳定性", "减少生产事故")
        kr1 = okr.add_key_result(oid, "减少 P0 事故 50%")
        okr.add_key_result(oid, "平均恢复时间 < 30 分钟")
        okr.update_progress(kr1, 60)

        tm.add("Review incident response plan", priority=1)
        
        import tempfile, os
        fd, out = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        path = report.monthly(output_path=out)
        content = Path(path).read_text(encoding="utf-8")
        assert "提升产品稳定性" in content
        assert "OKR" in content
        os.unlink(path)

    def test_monthly_report_with_okr(self, tm, okr, report):
        """Monthly report markdown includes OKR section."""
        oid = okr.add_objective("Q3 目标", "本季度目标")
        okr.add_key_result(oid, "KR A")
        tm.add("Task 1", priority=2)

        import tempfile, os
        fd, out = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        path = report.monthly(output_path=out)
        content = Path(path).read_text(encoding="utf-8")
        assert "Q3 目标" in content
        os.unlink(path)


# ---------------------------------------------------------------------------
# 4. Reminder dedup — no duplicate pushes
# ---------------------------------------------------------------------------


class TestReminderDedup:
    """Multiple reminder triggers should not produce duplicates."""

    def test_log_reminder_twice_no_duplicate(self, tm, engine):
        """Calling log_reminder twice with the same task → only one record."""
        tid = tm.add("Dedup test", priority=1)
        engine.log_reminder([tid], "morning")
        engine.log_reminder([tid], "morning")  # Second call

        history = engine.history()
        assert len(history) == 1
        assert history[0]["task_id"] == tid

    def test_multiple_types_no_cross_dedup(self, tm, engine):
        """Different reminder types are tracked independently."""
        tid = tm.add("Cross type test", priority=1)
        engine.log_reminder([tid], "morning")
        engine.log_reminder([tid], "afternoon")
        engine.log_reminder([tid], "evening")

        history = engine.history()
        assert len(history) == 3

        types = {h["reminder_type"] for h in history}
        assert types == {"morning", "afternoon", "evening"}

    def test_get_tasks_filters_already_reminded(self, tm, engine):
        """get_tasks_for_reminder excludes tasks already reminded today."""
        t1 = tm.add("Already reminded", priority=1)
        t2 = tm.add("Not reminded", priority=2)

        engine.log_reminder([t1], "morning")

        tasks = engine.get_tasks_for_reminder("morning")
        task_ids = {t["id"] for t in tasks}
        assert t1 not in task_ids
        assert t2 in task_ids

    def test_same_task_reminded_next_day(self, tm, engine):
        """A task reminded yesterday should be includable today."""
        tid = tm.add("Daily task", priority=1)
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) "
            "VALUES (?, 'morning', ?)",
            (tid, yesterday),
        )

        tasks = engine.get_tasks_for_reminder("morning")
        task_ids = {t["id"] for t in tasks}
        assert tid in task_ids, "Yesterday's reminder should not block today"


# ---------------------------------------------------------------------------
# 5. Soft delete — cancelled tasks preserved for reports
# ---------------------------------------------------------------------------


class TestSoftDeletePreservesData:
    """Soft-deleted (cancelled) tasks should still appear in stats and reports."""

    def test_soft_delete_keeps_row(self, tm):
        """Soft delete sets status to cancelled, row still exists."""
        tid = tm.add("Soft delete me", priority=2)
        tm.delete(tid)  # soft delete

        task = tm.get(tid)
        assert task is not None
        assert task["status"] == "cancelled"

    def test_soft_deleted_in_stats(self, tm, report):
        """Cancelled tasks appear in task stats."""
        tm.add("Active task", priority=1)
        tid = tm.add("Cancelled task", priority=3)
        tm.delete(tid)  # soft delete

        stats = tm.stats()
        assert "cancelled" in stats["by_status"]
        assert stats["by_status"]["cancelled"] == 1
        assert stats["by_status"]["todo"] == 1

    def test_cancelled_not_in_today(self, tm):
        """Cancelled tasks should NOT appear in today()."""
        tid = tm.add("Cancelled", priority=1)
        tm.delete(tid)

        today = tm.today()
        today_ids = {t["id"] for t in today}
        assert tid not in today_ids

    def test_cancelled_not_in_reminder(self, tm, engine):
        """Cancelled tasks should NOT appear in reminders."""
        tid = tm.add("Cancelled for reminder", priority=1)
        tm.delete(tid)

        tasks = engine.get_tasks_for_reminder("morning")
        task_ids = {t["id"] for t in tasks}
        assert tid not in task_ids

    def test_hard_delete_removes_from_stats(self, tm, report):
        """Hard delete actually removes the row (not in stats at all)."""
        tid = tm.add("Hard delete me", priority=2)
        tm.delete(tid, hard=True)

        task = tm.get(tid)
        assert task is None

        stats = tm.stats()
        total = sum(stats["by_status"].values())
        assert total == 0

    def test_advisor_ignores_cancelled(self, tm, advisor):
        """Advisor recommendations should not include cancelled tasks."""
        tm.add("Active P1", priority=1)
        tid = tm.add("Cancelled P1", priority=1)
        tm.delete(tid)  # soft delete

        recs = advisor.recommend_next(limit=5)
        rec_ids = {r["id"] for r in recs}
        assert tid not in rec_ids
        assert len(recs) >= 1  # at least the active one


# ---------------------------------------------------------------------------
# 6. Cross-module integration: Advisor + Report + OKR
# ---------------------------------------------------------------------------


class TestCrossModuleIntegration:
    """Integration across multiple modules: advisor recommendations with OKR context."""

    def test_advisor_recommends_okr_linked_tasks(self, tm, okr, advisor):
        """OKR-linked tasks get higher recommendation scores."""
        # Create OKR
        oid = okr.add_objective("O1")
        kr1 = okr.add_key_result(oid, "KR1")

        # Regular task (no OKR link)
        tm.add("Regular task", priority=1)

        # OKR-linked task
        t2 = tm.add("OKR-linked task", priority=3)
        okr.link_task(kr1, t2)

        recs = advisor.recommend_next(limit=3)
        # Regular P1 should be recommended (high priority)
        # But OKR-linked task should also be present
        rec_titles = {r["title"] for r in recs}
        assert "Regular task" in rec_titles
        assert "OKR-linked task" in rec_titles

    def test_workload_analysis_reflects_state(self, tm, advisor):
        """Workload analysis changes as tasks are added and completed."""
        # Empty → light
        analysis = advisor.workload_analysis()
        assert analysis["active_tasks"] == 0
        assert analysis["status"] == "light"

        # Add a few tasks
        tm.add("T1", priority=2)
        tm.add("T2", priority=3)
        tm.add("T3", priority=4)
        tm.add("T4", priority=5)

        analysis = advisor.workload_analysis()
        assert analysis["active_tasks"] == 4
        assert analysis["status"] == "moderate"

    def test_full_monthly_report(self, tm, pt, okr, report):
        """Monthly report integrates data from all modules."""
        t1 = tm.add("Task 1", priority=1, estimated_hours=3)
        tm.add("Task 2", priority=2, estimated_hours=2)
        pt.log(t1, "Working on it", hours_spent=1.5, new_progress=50)
        oid = okr.add_objective("O1")
        okr.add_key_result(oid, "KR1")

        import tempfile, os
        fd, out = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        path = report.monthly(output_path=out)
        content = Path(path).read_text(encoding="utf-8")
        assert "Task 1" in content
        assert "O1" in content
        os.unlink(path)


# ---------------------------------------------------------------------------
# 7. Report generation edge cases
# ---------------------------------------------------------------------------


class TestReportEdgeCases:
    """Report generation handles edge cases gracefully."""

    def test_monthly_empty_db(self, report):
        """Empty database should not crash monthly report generation."""
        import tempfile, os
        fd, out = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        path = report.monthly(output_path=out)
        content = Path(path).read_text(encoding="utf-8")
        assert len(content) > 0
        os.unlink(path)

    def test_semiannual_empty_db(self, report):
        """Empty database should not crash semiannual report generation."""
        import tempfile, os
        fd, out = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        path = report.semiannual(output_path=out)
        content = Path(path).read_text(encoding="utf-8")
        assert len(content) > 0
        os.unlink(path)

    def test_stats_empty_db(self, tm):
        """Task stats return zeros when no data."""
        stats = tm.stats()
        # Empty database: by_status is empty dict
        assert stats["by_status"] == {}

    def test_report_with_only_cancelled(self, tm, report):
        """Report handles case where all tasks are cancelled."""
        tid = tm.add("Only task", priority=2)
        tm.delete(tid)  # soft delete → cancelled

        import tempfile, os
        fd, out = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        path = report.monthly(output_path=out)
        content = Path(path).read_text(encoding="utf-8")
        assert len(content) > 0
        os.unlink(path)


# ---------------------------------------------------------------------------
# 8. Advisor edge cases
# ---------------------------------------------------------------------------


class TestAdvisorEdgeCases:
    """Advisor handles edge cases correctly."""

    def test_recommend_empty(self, advisor):
        """Recommend with no tasks returns empty list."""
        recs = advisor.recommend_next()
        assert recs == []

    def test_suggest_priority_urgent(self, advisor):
        """Urgent keywords produce high priority."""
        result = advisor.suggest_priority("Fix critical crash bug", "开发")
        assert result["priority"] == 1
        assert "crash" in result["reason"]

    def test_suggest_priority_default(self, advisor):
        """Non-urgent titles default to priority 3."""
        result = advisor.suggest_priority("Update README", "文档")
        assert result["priority"] == 3

    def test_workload_overloaded(self, tm, advisor):
        """Heavy workload detection."""
        for i in range(15):
            tm.add(f"Task {i}", priority=3)
        analysis = advisor.workload_analysis()
        assert analysis["status"] == "overloaded"
        assert analysis["active_tasks"] == 15

    def test_suggest_priority_with_category(self, advisor):
        """Category-based suggestions work."""
        result = advisor.suggest_priority("General task", "urgent")
        assert result["priority"] == 1
        assert "urgent" in result["reason"].lower()
