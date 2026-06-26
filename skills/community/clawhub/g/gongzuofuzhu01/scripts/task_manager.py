
"""
Personal Assistant Skill — Task Manager Layer (Sprint 1)

Task CRUD + query + sort operations on top of db.py.
Uses parameterised queries throughout for SQL injection prevention.
All times stored as localtime (UTC+8 / Beijing time via SQLite datetime('now','localtime')).
"""

from __future__ import annotations
from .db import Database

# ---------------------------------------------------------------------------
# Valid statuses and sensible defaults
# ---------------------------------------------------------------------------

VALID_STATUSES = frozenset({"todo", "in_progress", "blocked", "done", "cancelled"})
VALID_ORDER_BY = frozenset({"priority", "deadline", "created_at", "updated_at"})

# ---------------------------------------------------------------------------
# TaskManager
# ---------------------------------------------------------------------------

class TaskManager:
    """High-level task operations backed by a Database instance."""

    def __init__(self, db: Database):
        self.db = db

    # ===================================================================
    # CRUD
    # ===================================================================

    def add(self, title: str, **kwargs) -> int:
        """Add a task and return its ``task_id``.

        Accepted kwargs (all optional):
            description, category, priority (1-5), deadline, start_time,
            estimated_hours, parent_task_id, okr_id, source_type, extra,
            progress_note.

        Auto-generates ``display_id`` in YYYYMMDD-NNN format.
        """
        allowed = {
            "description",
            "category",
            "priority",
            "deadline",
            "start_time",
            "estimated_hours",
            "parent_task_id",
            "okr_id",
            "source_type",
            "recurring_id",
            "extra",
            "progress_note",
        }
        data = {"title": title}
        for k, v in kwargs.items():
            if k in allowed and v is not None:
                data[k] = v

        # 生成 display_id: YYYYMMDD-NNN
        today = self.db.fetch_one(
            "SELECT date('now', 'localtime') AS d", ()
        )["d"].replace("-", "")
        row = self.db.fetch_one(
            "SELECT MAX(display_id) AS mx FROM tasks WHERE display_id LIKE ?",
            (f"{today}-%",),
        )
        if row and row["mx"]:
            seq = int(row["mx"].split("-")[1]) + 1
        else:
            seq = 1
        data["display_id"] = f"{today}-{seq:03d}"

        return self.db.insert("tasks", data)

    def get(self, task_id: int) -> dict | None:
        """Return a single task dict, or *None* if not found."""
        return self.db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))

    def update(self, task_id: int, **kwargs) -> None:
        """Update one or more task fields. ``updated_at`` is refreshed automatically.

        Raises:
            ValueError: if no fields were provided.
        """
        if not kwargs:
            raise ValueError("At least one field must be provided for update.")

        kwargs["updated_at"] = None  # placeholder; replaced below

        allowed = {
            "title",
            "description",
            "category",
            "status",
            "priority",
            "deadline",
            "start_time",
            "estimated_hours",
            "actual_hours",
            "progress",
            "progress_note",
            "parent_task_id",
            "okr_id",
            "source_type",
            "recurring_id",
            "extra",
        }

        data = {}
        for k, v in kwargs.items():
            if k in allowed and v is not None:
                data[k] = v

        if not data:
            raise ValueError("No valid fields to update.")

        # Set updated_at via SQL so it uses SQLite's localtime
        set_clause = ", ".join(f"{col} = ?" for col in data.keys())
        set_clause += ", updated_at = datetime('now', 'localtime')"
        values = list(data.values()) + [task_id]

        sql = f"UPDATE tasks SET {set_clause} WHERE id = ?"
        self.db.execute(sql, values)

    def set_status(self, task_id: int, status: str) -> None:
        """Set the status of a task.

        Valid values: todo / in_progress / blocked / done / cancelled.
        """
        status = status.strip().lower()
        if status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )
        self.update(task_id, status=status)

    def delete(self, task_id: int, hard: bool = False) -> None:
        """Delete a task.

        - ``hard=False`` (default): soft delete — sets status to 'cancelled'.
        - ``hard=True``: physical deletion from the database.
        """
        if hard:
            self.db.delete("tasks", "id = ?", (task_id,))
        else:
            self.update(task_id, status="cancelled")

    # ===================================================================
    # Queries
    # ===================================================================

    def list(
        self,
        status=None,
        category=None,
        priority_min=None,
        priority_max=None,
        deadline_before=None,
        deadline_after=None,
        search=None,
        limit=50,
        offset=0,
        order_by="priority",
    ) -> list[dict]:
        """Flexible task query with filters and ordering.

        ``order_by``: priority / deadline / created_at / updated_at
        (default: ``priority`` ASC).

        ``search`` performs a LIKE match on both title and description.
        """
        conditions: list[str] = []
        params: list = []

        if status is not None:
            if isinstance(status, (list, tuple, set)):
                placeholders = ", ".join("?" for _ in status)
                conditions.append(f"status IN ({placeholders})")
                params.extend(status)
            else:
                conditions.append("status = ?")
                params.append(status)

        if category is not None:
            conditions.append("category = ?")
            params.append(category)

        if priority_min is not None:
            conditions.append("priority >= ?")
            params.append(priority_min)

        if priority_max is not None:
            conditions.append("priority <= ?")
            params.append(priority_max)

        if deadline_before is not None:
            conditions.append("deadline IS NOT NULL AND deadline <= ?")
            params.append(deadline_before)

        if deadline_after is not None:
            conditions.append("deadline IS NOT NULL AND deadline >= ?")
            params.append(deadline_after)

        if search is not None:
            conditions.append("(title LIKE ? OR description LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like])

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        # Ordering
        order_col = order_by if order_by in VALID_ORDER_BY else "priority"
        direction = "ASC" if order_col == "priority" else "DESC"
        nulls = ""
        if order_col == "deadline":
            order_col = f"CASE WHEN {order_col} IS NULL THEN 1 ELSE 0 END, {order_col}"

        sql = (
            f"SELECT * FROM tasks {where} "
            f"ORDER BY {order_col} {direction} {nulls} "
            f"LIMIT ? OFFSET ?"
        )
        params.extend([limit, offset])

        return self.db.fetch_all(sql, params)

    def today(self) -> list[dict]:
        """Tasks due today (or earlier, or un-deadlined), excluding done/cancelled.

        Uses SQLite ``date()`` so only the date portion is compared.
        """
        sql = """
            SELECT * FROM tasks
            WHERE status NOT IN ('done', 'cancelled')
              AND (deadline IS NULL OR date(deadline) <= date('now', 'localtime'))
            ORDER BY priority ASC
        """
        return self.db.fetch_all(sql)

    def upcoming(self, days: int = 7) -> list[dict]:
        """Tasks due within the next *N* days that are not done/cancelled."""
        sql = """
            SELECT * FROM tasks
            WHERE status NOT IN ('done', 'cancelled')
              AND deadline IS NOT NULL
              AND date(deadline) BETWEEN date('now', 'localtime')
                                    AND date('now', 'localtime', ?)
            ORDER BY deadline ASC
        """
        return self.db.fetch_all(sql, (f"+{days} days",))

    def overdue(self) -> list[dict]:
        """Tasks whose deadline has passed and that are not done/cancelled."""
        sql = """
            SELECT * FROM tasks
            WHERE status NOT IN ('done', 'cancelled')
              AND deadline IS NOT NULL
              AND date(deadline) < date('now', 'localtime')
            ORDER BY deadline ASC
        """
        return self.db.fetch_all(sql)

    def by_okr(self, okr_id: int) -> list[dict]:
        """All tasks linked to a given OKR item."""
        return self.db.fetch_all(
            "SELECT * FROM tasks WHERE okr_id = ? ORDER BY priority ASC",
            (okr_id,),
        )

    def search(self, keyword: str) -> list[dict]:
        """Full-text search on title and description."""
        return self.list(search=keyword, limit=50, order_by="updated_at")

    # ===================================================================
    # Stats
    # ===================================================================

    def stats(self) -> dict:
        """Aggregated counts grouped by status, priority, and category."""
        by_status = self.db.fetch_all(
            "SELECT status, COUNT(*) AS cnt FROM tasks GROUP BY status"
        )
        by_priority = self.db.fetch_all(
            "SELECT priority, COUNT(*) AS cnt FROM tasks GROUP BY priority"
        )
        by_category = self.db.fetch_all(
            "SELECT category, COUNT(*) AS cnt FROM tasks GROUP BY category ORDER BY cnt DESC"
        )

        return {
            "by_status": {r["status"]: r["cnt"] for r in by_status} if by_status else {},
            "by_priority": {str(r["priority"]): r["cnt"] for r in by_priority} if by_priority else {},
            "by_category": {r["category"] if r["category"] else "(uncategorised)": r["cnt"] for r in by_category} if by_category else {},
        }
