"""
Personal Assistant Skill — Reminder Engine (Sprint 2)

提醒引擎：筛选待办任务、按紧急度排序、生成 Markdown 提醒消息、去重日志。
"""

from __future__ import annotations
from datetime import date, datetime, timedelta

from .db import Database

# ---------------------------------------------------------------------------
# ReminderEngine
# ---------------------------------------------------------------------------

class ReminderEngine:
    """提醒引擎：筛选、排序、格式化、日志、统计。"""

    def __init__(self, db: Database, task_manager: 'TaskManager'):
        self.db = db
        self.task_manager = task_manager

    # ===================================================================
    # 任务筛选
    # ===================================================================

    def get_tasks_for_reminder(self, reminder_type: str = "morning") -> list[dict]:
        """筛选 todo / in_progress 任务，按 priority→deadline 排序。

        - morning / afternoon / evening：排除今天该时段已经提醒过的任务（去重）。
        - deadline_alert：只筛选即将到期（24h 内）的任务，不受去重限制。
        - manual：返回全部 todo / in_progress 任务，不受去重限制。
        """
        today = date.today().isoformat()

        # 获取所有活跃任务
        tasks = self.task_manager.list(
            status=["todo", "in_progress"],
            order_by="priority",
            limit=10000,
        )

        # 进一步按 deadline 做二次排序（priority ASC 已在 SQL 层完成，
        # 但 NULL deadline 需要放到最后）
        tasks = self._sort_by_priority_then_deadline(tasks)

        # deadline_alert：只保留 24h 内截止的任务
        if reminder_type == "deadline_alert":
            now = datetime.now()
            tasks = [t for t in tasks if _is_deadline_within(t.get("deadline"), now, hours=24)]

        # manual 和 deadline_alert 不做去重
        if reminder_type in ("deadline_alert", "manual"):
            return tasks

        # 排除今天已提醒的任务
        reminded_ids = self._get_reminded_task_ids(today, reminder_type)

        return [t for t in tasks if t["id"] not in reminded_ids]

    def _get_reminded_task_ids(self, reminder_date: str, reminder_type: str) -> set[int]:
        """返回指定日期和类型已提醒过的 task_id 集合。"""
        rows = self.db.fetch_all(
            "SELECT task_id FROM reminder_log WHERE reminder_date = ? AND reminder_type = ?",
            (reminder_date, reminder_type),
        )
        return {r["task_id"] for r in rows}

    def _sort_by_priority_then_deadline(self, tasks: list[dict]) -> list[dict]:
        """先按 priority ASC，再按 deadline ASC（NULL deadline 排最后）。"""
        return sorted(
            tasks,
            key=lambda t: (
                t.get("priority", 5),
                _deadline_sort_key(t.get("deadline")),
            ),
        )

    # ===================================================================
    # 紧急度排序
    # ===================================================================

    def sort_by_urgency(self, tasks: list[dict]) -> list[dict]:
        """纯规则排序：24h 内 deadline > 3 天内 deadline > priority 1-2 > 其他。

        同一档次内按 deadline ASC, priority ASC。
        """
        now = datetime.now()

        def urgency_key(task: dict) -> tuple[int, str, int]:
            """返回 (urgency_tier, deadline_sort, priority)。urgency_tier 越小越紧急。"""
            priority = task.get("priority", 5)

            # 0 — 24h 内到期
            if _is_deadline_within(task.get("deadline"), now, hours=24):
                return (0, _deadline_sort_key(task.get("deadline")), priority)

            # 1 — 3 天内到期
            if _is_deadline_within(task.get("deadline"), now, hours=72):
                return (1, _deadline_sort_key(task.get("deadline")), priority)

            # 2 — priority 1-2
            if priority <= 2:
                return (2, _deadline_sort_key(task.get("deadline")), priority)

            # 3 — 其他
            return (3, _deadline_sort_key(task.get("deadline")), priority)

        return sorted(tasks, key=urgency_key)

    # ===================================================================
    # 消息生成
    # ===================================================================

    def format_reminder(self, tasks: list[dict], reminder_type: str = "morning") -> str:
        """生成 Markdown 提醒消息。

        三段式结构：🔴 紧急 → 🟡 重要 → 🟢 常规。
        """
        if not tasks:
            return self._empty_reminder(reminder_type)

        # 按紧急度分组
        urgent: list[dict] = []
        important: list[dict] = []
        normal: list[dict] = []

        now = datetime.now()

        for t in tasks:
            if _is_deadline_within(t.get("deadline"), now, hours=24):
                urgent.append(t)
            elif _is_deadline_within(t.get("deadline"), now, hours=72) or t.get("priority", 5) <= 2:
                important.append(t)
            else:
                normal.append(t)

        # 构建消息
        greeting = _greeting_for(reminder_type)
        lines = [greeting, ""]

        if urgent:
            lines.append("### 🔴 紧急")
            for t in urgent:
                lines.append(f"- {_task_line(t)}")

        if important:
            if urgent:
                lines.append("")
            lines.append("### 🟡 重要")
            for t in important:
                lines.append(f"- {_task_line(t)}")

        if normal:
            if urgent or important:
                lines.append("")
            lines.append("### 🟢 常规")
            for t in normal:
                lines.append(f"- {_task_line(t)}")

        lines.append("")
        lines.append(f"*共 {len(tasks)} 项待办*")

        return "\n".join(lines)

    def _empty_reminder(self, reminder_type: str) -> str:
        """生成空任务提醒消息。"""
        greeting = _greeting_for(reminder_type)
        return f"{greeting}\n\n✅ 暂无待办任务，享受当下！"

    # ===================================================================
    # 日志
    # ===================================================================

    def log_reminder(self, task_ids: list[int], reminder_type: str, message: str = ""):
        """批量记录提醒日志。

        使用 INSERT OR IGNORE 处理 UNIQUE 冲突，同一任务同一天同类型只记录一次。
        """
        today = date.today().isoformat()
        for tid in task_ids:
            self.db.execute(
                "INSERT OR IGNORE INTO reminder_log (task_id, reminder_type, reminder_date, message) "
                "VALUES (?, ?, ?, ?)",
                (tid, reminder_type, today, message),
            )

    def was_reminded_today(self, task_id: int, reminder_type: str) -> bool:
        """检查某任务今天是否已在该时段提醒过。"""
        today = date.today().isoformat()
        row = self.db.fetch_one(
            "SELECT id FROM reminder_log WHERE task_id = ? AND reminder_type = ? AND reminder_date = ?",
            (task_id, reminder_type, today),
        )
        return row is not None

    # ===================================================================
    # 历史 & 统计
    # ===================================================================

    def history(self, days: int = 7) -> list[dict]:
        """返回最近 N 天的提醒历史。"""
        since = (date.today() - timedelta(days=days - 1)).isoformat()
        return self.db.fetch_all(
            "SELECT * FROM reminder_log WHERE reminder_date >= ? ORDER BY reminder_date DESC, sent_at DESC",
            (since,),
        )

    def stats(self, days: int = 30) -> dict:
        """返回提醒统计。

        Returns:
            {
                "total_reminders": int,
                "by_type": {"morning": N, "afternoon": N, "evening": N},
                "unique_tasks_reminded": int,
                "days": int,
                "avg_per_day": float,
            }
        """
        since = (date.today() - timedelta(days=days - 1)).isoformat()

        # 按类型统计
        by_type_rows = self.db.fetch_all(
            "SELECT reminder_type, COUNT(*) AS cnt FROM reminder_log "
            "WHERE reminder_date >= ? GROUP BY reminder_type",
            (since,),
        )
        by_type = {}
        total = 0
        for r in by_type_rows:
            by_type[r["reminder_type"]] = r["cnt"]
            total += r["cnt"]
        # 确保所有类型都有默认值
        for t in ("morning", "afternoon", "evening", "deadline_alert", "manual"):
            by_type.setdefault(t, 0)

        # 去重任务数
        unique_row = self.db.fetch_one(
            "SELECT COUNT(DISTINCT task_id) AS cnt FROM reminder_log WHERE reminder_date >= ?",
            (since,),
        )
        unique_tasks = unique_row["cnt"] if unique_row else 0

        # 活跃天数
        active_days_row = self.db.fetch_one(
            "SELECT COUNT(DISTINCT reminder_date) AS cnt FROM reminder_log WHERE reminder_date >= ?",
            (since,),
        )
        active_days = active_days_row["cnt"] if active_days_row else 0

        return {
            "total_reminders": total,
            "by_type": by_type,
            "unique_tasks_reminded": unique_tasks,
            "days": days,
            "avg_per_day": round(total / max(days, 1), 2),
        }

# =========================================================================
# 辅助函数
# =========================================================================

def _deadline_sort_key(deadline_str: str | None) -> str:
    """Deadline 排序键：NULL 排最后。"""
    if deadline_str is None:
        return "z"  # 排序在最后
    return deadline_str

def _is_deadline_within(
    deadline_str: str | None, now: datetime, hours: int
) -> bool:
    """判断 deadline 是否在指定小时数内到期。"""
    if deadline_str is None:
        return False
    try:
        dl = datetime.strptime(deadline_str.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        # 回退：尝试仅日期格式
        try:
            dl = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            return False
    delta = dl - now
    return timedelta(0) <= delta < timedelta(hours=hours)

def _task_line(task: dict) -> str:
    """单条任务 Markdown 行。"""
    title = task.get("title", "(无标题)")
    category = task.get("category", "")
    status = task.get("status", "")
    deadline = task.get("deadline")
    priority = task.get("priority", 3)

    # display_id 前置
    did = task.get('display_id') or f"N{task.get('id', 0):03d}"
    parts = [did, title]

    if category:
        parts.append(f"`{category}`")

    # 优先级标记
    if priority == 1:
        parts.append("🔴P1")
    elif priority == 2:
        parts.append("🟠P2")

    # 进行中标记
    if status == "in_progress":
        parts.append("▶️")

    # 截止日期（短格式）
    if deadline:
        try:
            dl_date = deadline[:10]  # "2026-06-15"
            parts.append(f"📅{dl_date}")
        except (IndexError, TypeError):
            pass

    return " ".join(parts)

def _greeting_for(reminder_type: str) -> str:
    """根据提醒类型返回问候语。"""
    greetings = {
        "morning": "🌅 **早上好！今日待办**",
        "afternoon": "☀️ **下午好！当前进度**",
        "evening": "🌙 **晚间回顾**",
        "deadline_alert": "⏰ **截止时间提醒**",
        "manual": "📋 **任务清单**",
    }
    return greetings.get(reminder_type, "📋 **任务提醒**")
