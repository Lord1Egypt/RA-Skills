
"""
Personal Assistant Skill — Recurring Task Manager (Sprint 2)

周期任务管理 + 实例自动生成。
RecurringManager sits on top of Database + TaskManager.
"""

from __future__ import annotations
from datetime import date, datetime, timedelta
from calendar import monthrange

from .db import Database
from .task_manager import TaskManager

# ---------------------------------------------------------------------------
# Valid recurrence types
# ---------------------------------------------------------------------------

VALID_RECURRENCE_TYPES = frozenset({"daily", "weekly", "biweekly", "monthly", "custom"})

# ---------------------------------------------------------------------------
# RecurringManager
# ---------------------------------------------------------------------------

class RecurringManager:
    """Manage recurring task templates and auto-generate task instances."""

    def __init__(self, db: Database, task_manager: TaskManager):
        self.db = db
        self.task_manager = task_manager

    # ===================================================================
    # CRUD
    # ===================================================================

    def add(
        self,
        template_title: str,
        recurrence_type: str,
        first_date: str,
        **kwargs,
    ) -> int:
        """Add a recurring task template and return its ``id``.

        Args:
            template_title: Title template for generated tasks.
            recurrence_type: daily / weekly / biweekly / monthly / custom.
            first_date: YYYY-MM-DD — the first date a task should be generated for.
                        Also used as the initial ``next_run_date``.
            **kwargs: Optional — template_desc, category, priority,
                      estimated_hours, recurrence_rule, advance_days, extra.

        Returns:
            The id of the newly created recurring task template.

        Raises:
            ValueError: if recurrence_type is not valid.
        """
        recurrence_type = recurrence_type.strip().lower()
        if recurrence_type not in VALID_RECURRENCE_TYPES:
            raise ValueError(
                f"Invalid recurrence_type '{recurrence_type}'. "
                f"Must be one of: {', '.join(sorted(VALID_RECURRENCE_TYPES))}"
            )

        allowed = {
            "template_desc",
            "category",
            "priority",
            "estimated_hours",
            "recurrence_rule",
            "advance_days",
            "extra",
        }
        data: dict = {
            "template_title": template_title,
            "recurrence_type": recurrence_type,
            "next_run_date": first_date,
        }
        for k, v in kwargs.items():
            if k in allowed and v is not None:
                data[k] = v

        return self.db.insert("recurring_tasks", data)

    def get(self, recurring_id: int) -> dict | None:
        """Return a single recurring task template dict, or *None* if not found."""
        return self.db.fetch_one(
            "SELECT * FROM recurring_tasks WHERE id = ?", (recurring_id,)
        )

    def list(self, enabled_only: bool = False) -> list[dict]:
        """List recurring task templates.

        Args:
            enabled_only: If True, return only enabled (enabled=1) templates.

        Returns:
            List of recurring task template dicts.
        """
        if enabled_only:
            sql = "SELECT * FROM recurring_tasks WHERE enabled = 1 ORDER BY id"
        else:
            sql = "SELECT * FROM recurring_tasks ORDER BY id"
        return self.db.fetch_all(sql)

    def toggle(self, recurring_id: int, enabled: bool) -> None:
        """Enable or disable a recurring task template."""
        self.db.execute(
            "UPDATE recurring_tasks "
            "SET enabled = ?, updated_at = datetime('now', 'localtime') "
            "WHERE id = ?",
            (1 if enabled else 0, recurring_id),
        )

    def delete(self, recurring_id: int) -> None:
        """Delete a recurring task template.

        Does **not** affect task instances that have already been generated.
        Existing tasks keep their ``recurring_id`` reference, but since the
        FK uses ``ON DELETE SET NULL``, the column will be nullified by SQLite.
        """
        self.db.delete("recurring_tasks", "id = ?", (recurring_id,))

    # ===================================================================
    # Instance generation
    # ===================================================================

    def generate_instances(self) -> list[int]:
        """Scan enabled recurring templates and generate task instances.

        For each enabled template whose ``next_run_date`` is <= today,
        create a task via TaskManager.add() and advance the template's
        ``next_run_date`` to the next occurrence.

        Generated tasks have:
          - source_type = 'recurring'
          - recurring_id = the template id
          - deadline = next_run_date T 18:00:00

        Returns:
            List of newly created task IDs (may be empty).
        """
        today_str = date.today().isoformat()
        templates = self.db.fetch_all(
            "SELECT * FROM recurring_tasks "
            "WHERE enabled = 1 AND next_run_date <= ? "
            "ORDER BY id",
            (today_str,),
        )

        new_task_ids: list[int] = []

        for tmpl in templates:
            # Generate the task instance
            next_date = tmpl["next_run_date"]
            deadline = f"{next_date}T18:00:00"

            task_id = self.task_manager.add(
                title=tmpl["template_title"],
                description=tmpl["template_desc"] or None,
                category=tmpl["category"] or None,
                priority=tmpl["priority"],
                deadline=deadline,
                estimated_hours=tmpl["estimated_hours"] or None,
                source_type="recurring",
                recurring_id=tmpl["id"],
                extra=tmpl["extra"] or None,
            )
            new_task_ids.append(task_id)

            # Advance next_run_date
            new_next = self.calc_next_date(
                current_date=next_date,
                recurrence_type=tmpl["recurrence_type"],
                recurrence_rule=tmpl["recurrence_rule"],
            )

            self.db.execute(
                "UPDATE recurring_tasks "
                "SET next_run_date = ?, last_run_date = ?, "
                "updated_at = datetime('now', 'localtime') "
                "WHERE id = ?",
                (new_next, next_date, tmpl["id"]),
            )

        return new_task_ids

    # ===================================================================
    # Date arithmetic
    # ===================================================================

    @staticmethod
    def calc_next_date(
        current_date: str,
        recurrence_type: str,
        recurrence_rule: str | None = None,
    ) -> str:
        """Calculate the next occurrence date from *current_date*.

        Args:
            current_date: YYYY-MM-DD string.
            recurrence_type: daily / weekly / biweekly / monthly / custom.
            recurrence_rule: Optional custom rule (e.g., JSON with ``interval``
                             and ``unit``). Only used when type is 'custom'.

        Returns:
            The next date as a YYYY-MM-DD string.

        Raises:
            ValueError: if recurrence_type is invalid or custom rule is malformed.
            NotImplementedError: if recurrence_type is 'custom' and no rule is provided.

        === Month-end boundary handling ===
        When the current date is the last day of the month, the next monthly
        occurrence snaps to the last day of the target month.  Examples:

        - Jan 31 → Feb 28 (or 29 in leap years)
        - Feb 28 → Mar 31 (if Feb 28 is the last calendar day of Feb)
        - Mar 31 → Apr 30
        """
        dt = datetime.strptime(current_date, "%Y-%m-%d").date()
        rtype = recurrence_type.strip().lower()

        if rtype == "daily":
            return (dt + timedelta(days=1)).isoformat()

        elif rtype == "weekly":
            return (dt + timedelta(days=7)).isoformat()

        elif rtype == "biweekly":
            return (dt + timedelta(days=14)).isoformat()

        elif rtype == "monthly":
            # Determine whether current_date is the last day of its month
            _, last_day_of_current = monthrange(dt.year, dt.month)
            is_month_end = dt.day == last_day_of_current

            # Advance to the next month
            if dt.month == 12:
                target_year = dt.year + 1
                target_month = 1
            else:
                target_year = dt.year
                target_month = dt.month + 1

            if is_month_end:
                # Snap to last day of target month
                _, last_day_of_target = monthrange(target_year, target_month)
                day = last_day_of_target
            else:
                # Try the same day-of-month, clamp if out of range
                _, last_day_of_target = monthrange(target_year, target_month)
                day = min(dt.day, last_day_of_target)

            return date(target_year, target_month, day).isoformat()

        elif rtype == "custom":
            if recurrence_rule is None:
                raise NotImplementedError(
                    "Custom recurrence requires a recurrence_rule."
                )
            return RecurringManager._calc_custom(dt, recurrence_rule)

        else:
            raise ValueError(f"Unknown recurrence_type: {recurrence_type!r}")

    # ===================================================================
    # Custom recurrence helper
    # ===================================================================

    @staticmethod
    def _calc_custom(dt: date, rule: str) -> str:
        """Parse a JSON recurrence_rule and compute the next date.

        Supported rule shapes::

            {"interval": N, "unit": "days"|"weeks"|"months"}

        ``interval`` is a positive integer (defaults to 1).
        ``unit`` defaults to ``"days"``.
        """
        import json

        try:
            rule_obj: dict = json.loads(rule)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in recurrence_rule: {exc}") from exc

        interval = int(rule_obj.get("interval", 1))
        unit = rule_obj.get("unit", "days").lower()

        if interval < 1:
            raise ValueError("interval must be >= 1")

        if unit == "days":
            return (dt + timedelta(days=interval)).isoformat()
        elif unit == "weeks":
            return (dt + timedelta(weeks=interval)).isoformat()
        elif unit == "months":
            # Same month-end logic as the monthly branch
            target_year = dt.year + (dt.month + interval - 1) // 12
            target_month = (dt.month + interval - 1) % 12 + 1

            _, last_day_current = monthrange(dt.year, dt.month)
            is_month_end = dt.day == last_day_current

            if is_month_end:
                _, last_day_target = monthrange(target_year, target_month)
                day = last_day_target
            else:
                _, last_day_target = monthrange(target_year, target_month)
                day = min(dt.day, last_day_target)

            return date(target_year, target_month, day).isoformat()
        else:
            raise ValueError(f"Unsupported custom recurrence unit: {unit!r}")
