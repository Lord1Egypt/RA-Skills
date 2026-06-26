"""
Tests for reminder.py — ReminderEngine: filtering, sorting, dedup,
message formatting, logging, history, and stats.

Uses pytest + tempfile for fully isolated tests.
"""

import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

# Set up import path — needs the skill root so `from scripts.db import ...` works
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.task_manager import TaskManager
from scripts.reminder import ReminderEngine


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db():
    """Fresh temporary database with schema initialised."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()

    database = Database(db_path=tmp.name)
    # Ensure SCHEMA_FILE is correct
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
    """TaskManager wired to the fresh database."""
    return TaskManager(db)


@pytest.fixture
def engine(db, tm):
    """ReminderEngine wired to fresh db + task_manager."""
    return ReminderEngine(db, tm)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _days_from_now(days: int) -> str:
    """Return ISO datetime string for N days from now at noon."""
    dt = datetime.now() + timedelta(days=days)
    return dt.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()


def _hours_from_now(hours: int) -> str:
    """Return ISO datetime string for N hours from now."""
    dt = datetime.now() + timedelta(hours=hours)
    return dt.isoformat()


# ---------------------------------------------------------------------------
# 1. get_tasks_for_reminder — 筛选
# ---------------------------------------------------------------------------

class TestGetTasksFiltering:
    def test_only_todo_and_in_progress(self, tm, engine):
        """只返回 todo 和 in_progress，不包含 done/cancelled/blocked。"""
        tm.add("Todo task", priority=3)
        tid_ip = tm.add("In progress task", priority=2)
        tm.set_status(tid_ip, "in_progress")
        tid_done = tm.add("Done task", priority=1)
        tm.set_status(tid_done, "done")
        tid_cancelled = tm.add("Cancelled task", priority=4)
        tm.set_status(tid_cancelled, "cancelled")
        tid_blocked = tm.add("Blocked task", priority=5)
        tm.set_status(tid_blocked, "blocked")

        tasks = engine.get_tasks_for_reminder("morning")

        assert len(tasks) == 2
        titles = {t["title"] for t in tasks}
        assert titles == {"Todo task", "In progress task"}

    def test_empty_result(self, engine):
        """空数据库返回空列表。"""
        assert engine.get_tasks_for_reminder("morning") == []


# ---------------------------------------------------------------------------
# 2. get_tasks_for_reminder — 排序
# ---------------------------------------------------------------------------

class TestGetTasksSorting:
    def test_sort_by_priority_asc(self, tm, engine):
        """按 priority ASC 排序（1 最优先在前）。"""
        tm.add("P5 task", priority=5)
        tm.add("P1 task", priority=1)
        tm.add("P3 task", priority=3)

        tasks = engine.get_tasks_for_reminder("morning")
        priorities = [t["priority"] for t in tasks]
        assert priorities == [1, 3, 5]

    def test_sort_priority_then_deadline(self, tm, engine):
        """同 priority 时按 deadline ASC，NULL deadline 排最后。"""
        tm.add("Distant", priority=1, deadline=_days_from_now(30))
        tm.add("No deadline", priority=1)
        tm.add("Urgent", priority=1, deadline=_days_from_now(1))

        tasks = engine.get_tasks_for_reminder("morning")

        assert tasks[0]["title"] == "Urgent"  # earliest deadline
        assert tasks[1]["title"] == "Distant"  # later deadline
        assert tasks[2]["title"] == "No deadline"  # NULL last


# ---------------------------------------------------------------------------
# 3. get_tasks_for_reminder — 去重
# ---------------------------------------------------------------------------

class TestGetTasksDedup:
    def test_excludes_already_reminded(self, tm, engine):
        """排除当天该类型已提醒的任务。"""
        tid = tm.add("Already reminded today", priority=1)
        tm.add("Not yet reminded", priority=2)

        # 模拟今天已经为该任务发送过 morning 提醒
        today = date.today().isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', ?)",
            (tid, today),
        )

        tasks = engine.get_tasks_for_reminder("morning")
        titles = {t["title"] for t in tasks}
        assert "Already reminded today" not in titles
        assert "Not yet reminded" in titles

    def test_different_type_not_excluded(self, tm, engine):
        """不同提醒类型互相不影响去重。"""
        tid = tm.add("Only morning reminded", priority=1)
        today = date.today().isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', ?)",
            (tid, today),
        )

        # afternoon 时该任务仍应出现
        tasks = engine.get_tasks_for_reminder("afternoon")
        titles = {t["title"] for t in tasks}
        assert "Only morning reminded" in titles

    def test_past_days_not_excluded(self, tm, engine):
        """昨天提醒过的任务今天仍应出现。"""
        tid = tm.add("Reminded yesterday", priority=1)
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', ?)",
            (tid, yesterday),
        )

        tasks = engine.get_tasks_for_reminder("morning")
        titles = {t["title"] for t in tasks}
        assert "Reminded yesterday" in titles


# ---------------------------------------------------------------------------
# 4. sort_by_urgency
# ---------------------------------------------------------------------------

class TestSortByUrgency:
    def test_24h_deadline_first(self, engine):
        """24h 内 deadline 排第一档。"""
        tasks = [
            {"id": 1, "title": "Normal", "priority": 5, "deadline": _days_from_now(7)},
            {"id": 2, "title": "Urgent", "priority": 5, "deadline": _hours_from_now(2)},
            {"id": 3, "title": "P1", "priority": 1, "deadline": _days_from_now(7)},
        ]
        sorted_tasks = engine.sort_by_urgency(tasks)
        assert sorted_tasks[0]["title"] == "Urgent"

    def test_3day_deadline_before_low_priority(self, engine):
        """3 天内 deadline 排在 priority 1-2 之前。"""
        tasks = [
            {"id": 1, "title": "P1 No DL", "priority": 1},
            {"id": 2, "title": "3day DL P5", "priority": 5, "deadline": _hours_from_now(50)},
        ]
        sorted_tasks = engine.sort_by_urgency(tasks)
        assert sorted_tasks[0]["title"] == "3day DL P5"

    def test_priority_1_2_before_other(self, engine):
        """priority 1-2 排在 priority 3+ 前面（无 deadline）。"""
        tasks = [
            {"id": 1, "title": "P4", "priority": 4},
            {"id": 2, "title": "P2", "priority": 2},
            {"id": 3, "title": "P3", "priority": 3},
            {"id": 4, "title": "P1", "priority": 1},
        ]
        sorted_tasks = engine.sort_by_urgency(tasks)
        # P1, P2 should come before P3, P4
        assert sorted_tasks[0]["priority"] == 1
        assert sorted_tasks[1]["priority"] == 2
        assert sorted_tasks[2]["priority"] == 3
        assert sorted_tasks[3]["priority"] == 4

    def test_null_deadline_not_urgent(self, engine):
        """NULL deadline 不算紧急。"""
        tasks = [
            {"id": 1, "title": "No DL P1", "priority": 1},
            {"id": 2, "title": "No DL P5", "priority": 5},
        ]
        sorted_tasks = engine.sort_by_urgency(tasks)
        # P1 排在 P5 前面
        assert sorted_tasks[0]["priority"] == 1

    def test_empty_list(self, engine):
        """空列表直接返回空。"""
        assert engine.sort_by_urgency([]) == []


# ---------------------------------------------------------------------------
# 5. format_reminder
# ---------------------------------------------------------------------------

class TestFormatReminder:
    def test_three_sections(self, engine):
        """三段式：紧急 / 重要 / 常规。"""
        tasks = [
            {"id": 1, "title": "Urgent task", "priority": 1, "deadline": _hours_from_now(2), "status": "todo", "category": "bug"},
            {"id": 2, "title": "Important P2", "priority": 2, "status": "in_progress"},
            {"id": 3, "title": "Routine task", "priority": 4, "deadline": _days_from_now(30)},
        ]
        msg = engine.format_reminder(tasks, "morning")

        assert "🔴 紧急" in msg
        assert "🟡 重要" in msg
        assert "🟢 常规" in msg
        assert "Urgent task" in msg
        assert "Important P2" in msg
        assert "Routine task" in msg
        assert "共 3 项待办" in msg

    def test_empty_tasks(self, engine):
        """空任务返回友好提示。"""
        msg = engine.format_reminder([], "morning")
        assert "暂无待办" in msg
        assert "✅" in msg

    def test_morning_greeting(self, engine):
        """早上提醒包含早上问候语。"""
        tasks = [{"id": 1, "title": "T1", "priority": 1}]
        msg = engine.format_reminder(tasks, "morning")
        assert "早上好" in msg

    def test_afternoon_greeting(self, engine):
        """下午提醒包含下午问候语。"""
        tasks = [{"id": 1, "title": "T1", "priority": 1}]
        msg = engine.format_reminder(tasks, "afternoon")
        assert "下午好" in msg

    def test_evening_greeting(self, engine):
        """晚间提醒包含晚间问候语。"""
        tasks = [{"id": 1, "title": "T1", "priority": 1}]
        msg = engine.format_reminder(tasks, "evening")
        assert "晚间回顾" in msg

    def test_in_progress_marked(self, engine):
        """in_progress 状态在消息中标记。"""
        tasks = [{"id": 1, "title": "Ongoing", "priority": 2, "status": "in_progress"}]
        msg = engine.format_reminder(tasks, "morning")
        assert "▶️" in msg

    def test_only_one_section(self, engine):
        """只有常规任务时只显示一个段落。"""
        tasks = [
            {"id": 1, "title": "Normal task", "priority": 4, "deadline": _days_from_now(30)},
        ]
        msg = engine.format_reminder(tasks, "morning")
        assert "🔴 紧急" not in msg
        assert "🟡 重要" not in msg
        assert "🟢 常规" in msg


# ---------------------------------------------------------------------------
# 6. log_reminder
# ---------------------------------------------------------------------------

class TestLogReminder:
    def test_log_and_verify(self, tm, engine):
        """记录提醒后能查到。"""
        tid = tm.add("Task A", priority=1)
        engine.log_reminder([tid], "morning")

        history = engine.history()
        assert len(history) == 1
        assert history[0]["task_id"] == tid
        assert history[0]["reminder_type"] == "morning"

    def test_log_multiple_tasks(self, tm, engine):
        """批量记录多个任务。"""
        t1 = tm.add("T1", priority=1)
        t2 = tm.add("T2", priority=2)
        t3 = tm.add("T3", priority=3)

        engine.log_reminder([t1, t2, t3], "afternoon")

        history = engine.history()
        assert len(history) == 3

    def test_log_duplicate_ignored(self, tm, engine):
        """同一天同一类型重复记录不报错（INSERT OR IGNORE）。"""
        tid = tm.add("Task A", priority=1)
        engine.log_reminder([tid], "morning")
        engine.log_reminder([tid], "morning")  # 不应抛异常

        history = engine.history()
        assert len(history) == 1  # 只有一条记录


# ---------------------------------------------------------------------------
# 7. was_reminded_today
# ---------------------------------------------------------------------------

class TestWasRemindedToday:
    def test_was_reminded_true(self, tm, engine):
        """记录后 was_reminded_today 返回 True。"""
        tid = tm.add("Task", priority=1)
        engine.log_reminder([tid], "morning")
        assert engine.was_reminded_today(tid, "morning") is True

    def test_was_reminded_false(self, tm, engine):
        """未记录返回 False。"""
        tid = tm.add("Task", priority=1)
        assert engine.was_reminded_today(tid, "morning") is False

    def test_was_reminded_different_type(self, tm, engine):
        """不同类型不互相影响。"""
        tid = tm.add("Task", priority=1)
        engine.log_reminder([tid], "morning")
        assert engine.was_reminded_today(tid, "afternoon") is False


# ---------------------------------------------------------------------------
# 8. history
# ---------------------------------------------------------------------------

class TestHistory:
    def test_history_default_7_days(self, tm, engine):
        """默认返回最近 7 天。"""
        tid = tm.add("Task", priority=1)
        today = date.today().isoformat()

        # 插入 6 天前的记录
        six_days_ago = (date.today() - timedelta(days=6)).isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', ?)",
            (tid, six_days_ago),
        )
        engine.log_reminder([tid], "afternoon")

        history = engine.history()  # default 7 days
        assert len(history) == 2

    def test_history_old_excluded(self, tm, engine):
        """超过指定天数的记录不返回。"""
        tid = tm.add("Task", priority=1)
        eight_days_ago = (date.today() - timedelta(days=8)).isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', ?)",
            (tid, eight_days_ago),
        )

        history = engine.history(days=7)
        assert len(history) == 0  # 8 天前的记录超出 7 天

    def test_history_desc_order(self, tm, engine):
        """历史记录按日期降序排列。"""
        t1 = tm.add("T1", priority=1)
        t2 = tm.add("T2", priority=2)

        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', ?)",
            (t1, yesterday),
        )
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'afternoon', ?)",
            (t2, today),
        )

        history = engine.history(days=30)
        assert history[0]["reminder_date"] == today
        assert history[1]["reminder_date"] == yesterday


# ---------------------------------------------------------------------------
# 9. stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_basic(self, tm, engine):
        """基本统计：总数、按类型分布。"""
        t1 = tm.add("T1", priority=1)
        t2 = tm.add("T2", priority=2)

        engine.log_reminder([t1], "morning")
        engine.log_reminder([t2], "morning")
        engine.log_reminder([t1], "afternoon")
        engine.log_reminder([t2], "evening")

        s = engine.stats(days=30)

        assert s["total_reminders"] == 4
        assert s["by_type"]["morning"] == 2
        assert s["by_type"]["afternoon"] == 1
        assert s["by_type"]["evening"] == 1
        assert s["unique_tasks_reminded"] == 2
        assert s["days"] == 30
        assert s["avg_per_day"] > 0

    def test_stats_empty(self, engine):
        """空数据库统计返回 0。"""
        s = engine.stats(days=30)
        assert s["total_reminders"] == 0
        assert s["by_type"] == {"morning": 0, "afternoon": 0, "evening": 0, "deadline_alert": 0, "manual": 0}
        assert s["unique_tasks_reminded"] == 0
        assert s["avg_per_day"] == 0.0

    def test_stats_respects_days(self, tm, engine):
        """stats 只统计指定天数。"""
        tid = tm.add("Task", priority=1)
        forty_days_ago = (date.today() - timedelta(days=40)).isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'morning', ?)",
            (tid, forty_days_ago),
        )

        s = engine.stats(days=30)
        assert s["total_reminders"] == 0  # 40 天前超出 30 天


# ---------------------------------------------------------------------------
# 10. get_tasks_for_reminder — deadline_alert 类型
# ---------------------------------------------------------------------------

class TestGetTasksDeadlineAlert:
    def test_only_24h_deadline_tasks(self, tm, engine):
        """deadline_alert 只返回 24h 内截止的任务。"""
        tm.add("Urgent 2h", priority=3, deadline=_hours_from_now(2))
        tm.add("Not urgent 3d", priority=1, deadline=_days_from_now(3))
        tm.add("No deadline", priority=1)

        tasks = engine.get_tasks_for_reminder("deadline_alert")

        titles = {t["title"] for t in tasks}
        assert "Urgent 2h" in titles
        assert "Not urgent 3d" not in titles
        assert "No deadline" not in titles

    def test_deadline_alert_no_dedup(self, tm, engine):
        """deadline_alert 不受去重限制，即使今天已提醒过仍然返回。"""
        tid = tm.add("Already reminded", priority=1, deadline=_hours_from_now(2))
        today = date.today().isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'deadline_alert', ?)",
            (tid, today),
        )

        tasks = engine.get_tasks_for_reminder("deadline_alert")
        titles = {t["title"] for t in tasks}
        assert "Already reminded" in titles

    def test_deadline_alert_empty_when_no_urgent(self, tm, engine):
        """没有 24h 内截止的任务时返回空列表。"""
        tm.add("Distant", priority=1, deadline=_days_from_now(5))
        tm.add("No deadline", priority=2)

        tasks = engine.get_tasks_for_reminder("deadline_alert")
        assert tasks == []


# ---------------------------------------------------------------------------
# 11. get_tasks_for_reminder — manual 类型
# ---------------------------------------------------------------------------

class TestGetTasksManual:
    def test_manual_returns_all_active(self, tm, engine):
        """manual 类型返回所有 todo/in_progress 任务。"""
        tm.add("Todo", priority=1)
        tid_ip = tm.add("In progress", priority=2)
        tm.set_status(tid_ip, "in_progress")
        tid_done = tm.add("Done", priority=1)
        tm.set_status(tid_done, "done")

        tasks = engine.get_tasks_for_reminder("manual")

        titles = {t["title"] for t in tasks}
        assert len(tasks) == 2
        assert titles == {"Todo", "In progress"}

    def test_manual_no_dedup(self, tm, engine):
        """manual 类型不受去重限制。"""
        tid = tm.add("Already reminded", priority=1)
        today = date.today().isoformat()
        engine.db.execute(
            "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'manual', ?)",
            (tid, today),
        )

        tasks = engine.get_tasks_for_reminder("manual")
        titles = {t["title"] for t in tasks}
        assert "Already reminded" in titles


# ---------------------------------------------------------------------------
# 12. reminder_type CHECK 约束验证
# ---------------------------------------------------------------------------

class TestReminderTypesCheck:
    def test_all_five_types_insertable(self, tm, engine):
        """验证 5 种提醒类型都可以成功插入。"""
        tid = tm.add("Test task", priority=1)
        today = date.today().isoformat()

        for rtype in ("morning", "afternoon", "evening", "deadline_alert", "manual"):
            engine.db.execute(
                "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, ?, ?)",
                (tid, rtype, today),
            )

        # 应该有 5 条记录（不同日期/类型的组合不会冲突）
        history = engine.history(days=365)
        # 同一天同一任务的5种类型，UNIQUE 约束是 (task_id, reminder_type, reminder_date)
        assert len(history) == 5

    def test_invalid_type_rejected(self, tm, engine):
        """非法类型应被数据库拒绝。"""
        tid = tm.add("Test", priority=1)
        today = date.today().isoformat()

        import sqlite3
        with pytest.raises(sqlite3.IntegrityError):
            engine.db.execute(
                "INSERT INTO reminder_log (task_id, reminder_type, reminder_date) VALUES (?, 'invalid_type', ?)",
                (tid, today),
            )
