
"""
Personal Assistant Skill — Progress Tracker Layer (Sprint 2)

Progress logging and milestone management on top of db.py and task_manager.py.
All times stored as localtime (UTC+8 / Beijing time via SQLite datetime('now','localtime')).
"""

from __future__ import annotations
from .db import Database
from .task_manager import TaskManager

class ProgressTracker:
    """Progress logging and milestone management backed by a Database + TaskManager."""

    def __init__(self, db: Database, task_manager: TaskManager):
        self.db = db
        self.tm = task_manager

    # ===================================================================
    # Progress logging
    # ===================================================================

    def log(
        self,
        task_id: int,
        content: str,
        hours_spent: float = 0,
        new_progress: int = None,
    ) -> int:
        """Record a progress log entry.

        Automatically captures ``progress_before`` from the current task state.
        If *new_progress* is not ``None``, the task's ``progress`` column is
        updated accordingly and both ``actual_hours`` is incremented.

        Returns the new ``log_id``.
        """
        # Read current task state
        task = self.tm.get(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")

        progress_before = task.get("progress") or 0
        progress_after = (
            new_progress if new_progress is not None else progress_before
        )

        # Insert the log row
        log_id = self.db.insert(
            "progress_logs",
            {
                "task_id": task_id,
                "content": content,
                "progress_before": progress_before,
                "progress_after": progress_after,
                "hours_spent": hours_spent,
            },
        )

        # Sync task.progress if requested
        if new_progress is not None:
            update_kwargs: dict = {"progress": new_progress}
            # Accumulate actual_hours
            current_actual = task.get("actual_hours") or 0
            update_kwargs["actual_hours"] = current_actual + hours_spent
            self.tm.update(task_id, **update_kwargs)
        else:
            # Still accumulate hours even if progress didn't change
            if hours_spent > 0:
                current_actual = task.get("actual_hours") or 0
                self.tm.update(task_id, actual_hours=current_actual + hours_spent)

        return log_id

    def history(self, task_id: int, limit: int = 20) -> list[dict]:
        """Return progress logs for *task_id*, newest first.

        Args:
            task_id: The task to query.
            limit: Max number of entries to return.
        """
        return self.db.fetch_all(
            "SELECT * FROM progress_logs WHERE task_id = ? "
            "ORDER BY logged_at DESC, id DESC LIMIT ?",
            (task_id, limit),
        )

    def timeline(
        self, start_date: str = None, end_date: str = None
    ) -> list[dict]:
        """Return all progress logs within a date range, chronological order.

        Dates are compared against the date portion of ``logged_at``
        (i.e. ``date(logged_at)``).  Format: ``YYYY-MM-DD``.

        Args:
            start_date: Inclusive lower bound (e.g. ``"2026-05-01"``).
            end_date:   Inclusive upper bound (e.g. ``"2026-05-31"``).
        """
        conditions: list[str] = []
        params: list = []

        if start_date is not None:
            conditions.append("date(logged_at) >= ?")
            params.append(start_date)
        if end_date is not None:
            conditions.append("date(logged_at) <= ?")
            params.append(end_date)

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = (
            f"SELECT * FROM progress_logs {where} ORDER BY logged_at ASC"
        )
        return self.db.fetch_all(sql, params)

    # ===================================================================
    # Milestones
    # ===================================================================

    def add_milestone(
        self,
        task_id: int,
        title: str,
        due_date: str = None,
        sort_order: int = 0,
    ) -> int:
        """Create a milestone for a task. Returns the new milestone id."""
        data: dict = {
            "task_id": task_id,
            "title": title,
            "sort_order": sort_order,
        }
        if due_date is not None:
            data["due_date"] = due_date
        return self.db.insert("milestones", data)

    def complete_milestone(self, milestone_id: int) -> None:
        """Mark a milestone as completed with the current timestamp."""
        self.db.update(
            "milestones",
            {
                "status": "completed",
                "completed_at": None,  # placeholder; replaced by SQL below
            },
            "id = ?",
            (milestone_id,),
        )
        # Set completed_at via SQL so it uses SQLite's localtime
        self.db.execute(
            "UPDATE milestones SET completed_at = datetime('now', 'localtime') "
            "WHERE id = ?",
            (milestone_id,),
        )

    def list_milestones(self, task_id: int) -> list[dict]:
        """Return all milestones for *task_id*, ordered by ``sort_order``."""
        return self.db.fetch_all(
            "SELECT * FROM milestones WHERE task_id = ? ORDER BY sort_order ASC",
            (task_id,),
        )

    def milestone_progress(self, task_id: int) -> dict:
        """Return ``{total, completed, percent}`` for a task's milestones.

        *percent* is rounded to the nearest integer (0-100).  Returns 0 %
        when there are zero milestones.
        """
        rows = self.db.fetch_all(
            "SELECT status FROM milestones WHERE task_id = ?",
            (task_id,),
        )
        total = len(rows)
        completed = sum(1 for r in rows if r["status"] == "completed")
        percent = round(completed / total * 100) if total > 0 else 0
        return {"total": total, "completed": completed, "percent": percent}
