
"""
Personal Assistant Skill — Report Generator (Sprint 3)

月报和半年报生成。纯数据聚合 + Markdown 模板填充，不调用 LLM。
时间范围使用 SQLite date() 函数筛选。
"""

from __future__ import annotations
from datetime import date
from calendar import monthrange
from pathlib import Path

from .db import Database
from .task_manager import TaskManager
from .progress import ProgressTracker
from .okr import OKRManager

# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------

REPORTS_DIR = Path.home() / ".hermes" / "reports"

# ---------------------------------------------------------------------------
# ReportGenerator
# ---------------------------------------------------------------------------

class ReportGenerator:
    """Generate monthly and semi-annual work reports."""

    def __init__(
        self,
        db: Database,
        task_manager: TaskManager,
        progress_tracker: ProgressTracker,
        okr_manager: OKRManager,
    ):
        self.db = db
        self.tm = task_manager
        self.pt = progress_tracker
        self.okr = okr_manager

    # ===================================================================
    # Public API
    # ===================================================================

    def monthly(
        self,
        year: int = None,
        month: int = None,
        output_path: str = None,
    ) -> str:
        """Generate a monthly work report. Defaults to the current month.

        Args:
            year:  Report year (default: current year).
            month: Report month 1–12 (default: current month).
            output_path: Destination path for the Markdown report.
                         Defaults to ``~/.hermes/reports/YYYY-MM-月报.md``.

        Returns:
            Absolute path to the generated report file.
        """
        if year is None:
            year = date.today().year
        if month is None:
            month = date.today().month

        data = self._query_monthly_tasks(year, month)
        okr_data = self._query_okr_progress()
        next_month_tasks = self._query_next_month_tasks(year, month)

        report = self._format_monthly_report(
            year, month, data, okr_data, next_month_tasks
        )

        return self._write_report(output_path, f"{year}-{month:02d}-月报.md", report)

    def semiannual(
        self,
        year: int = None,
        half: int = None,
        output_path: str = None,
    ) -> str:
        """Generate a semi-annual report.

        Args:
            year: Report year (default: current year).
            half: 1 = 上半年 (Jan–Jun), 2 = 下半年 (Jul–Dec).
                  Default: inferred from current month.
            output_path: Destination path for the Markdown report.
                         Defaults to ``~/.hermes/reports/YYYY-半年报.md``.

        Returns:
            Absolute path to the generated report file.
        """
        if year is None:
            year = date.today().year
        if half is None:
            current_month = date.today().month
            half = 1 if current_month <= 6 else 2

        if half == 1:
            months = range(1, 7)
            half_label = "上半年"
        elif half == 2:
            months = range(7, 13)
            half_label = "下半年"
        else:
            raise ValueError(f"half must be 1 or 2, got {half!r}")

        # Collect data for each month
        all_monthly_data: list[tuple[int, dict]] = []
        monthly_trend: list[dict] = []

        for m in months:
            data = self._query_monthly_tasks(year, m)
            all_monthly_data.append((m, data))
            monthly_trend.append({
                "month": m,
                "completed": data["completed_count"],
                "in_progress": data["active_tasks_count"],
                "total_hours": data["total_hours"],
            })

        # Aggregate totals
        total_completed = sum(d["completed_count"] for _, d in all_monthly_data)
        total_hours = sum(d["total_hours"] for _, d in all_monthly_data)
        total_new = sum(d["new_count"] for _, d in all_monthly_data)

        okr_data = self._query_okr_progress()

        report = self._format_semiannual_report(
            year=year,
            half_label=half_label,
            total_completed=total_completed,
            total_hours=total_hours,
            total_new=total_new,
            all_monthly_data=all_monthly_data,
            monthly_trend=monthly_trend,
            okr_data=okr_data,
        )

        return self._write_report(output_path, f"{year}-{half_label}-半年报.md", report)

    # ===================================================================
    # Internal — Write
    # ===================================================================

    def _write_report(
        self,
        output_path: str | None,
        default_filename: str,
        content: str,
    ) -> str:
        """Write report content to disk and return the absolute path."""
        if output_path is not None:
            dest = Path(output_path).expanduser().resolve()
        else:
            dest = (REPORTS_DIR / default_filename).resolve()

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        return str(dest)

    # ===================================================================
    # Internal — Query
    # ===================================================================

    def _query_monthly_tasks(self, year: int, month: int) -> dict:
        """Query all task data for a given month.

        Returns a dict with keys:
            completed, completed_count, active_tasks, active_tasks_count,
            new_tasks, new_count, total_hours, category_stats
        """
        _, last_day = monthrange(year, month)
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day:02d}"

        # --- Completed tasks in this month ---
        # Use date(updated_at) as a proxy for completion date.
        completed = self.db.fetch_all(
            """SELECT * FROM tasks
               WHERE status = 'done'
                 AND date(updated_at) >= ?
                 AND date(updated_at) <= ?
               ORDER BY updated_at DESC""",
            (start_date, end_date),
        )

        # --- Active tasks (not done, not cancelled) ---
        active_tasks = self.db.fetch_all(
            """SELECT * FROM tasks
               WHERE status NOT IN ('done', 'cancelled')
               ORDER BY priority ASC""",
        )

        # --- New tasks created in this month ---
        new_tasks = self.db.fetch_all(
            """SELECT * FROM tasks
               WHERE date(created_at) >= ?
                 AND date(created_at) <= ?
               ORDER BY created_at DESC""",
            (start_date, end_date),
        )

        # --- Total hours from progress_logs in this month ---
        hours_row = self.db.fetch_one(
            """SELECT COALESCE(SUM(hours_spent), 0) AS total
               FROM progress_logs
               WHERE date(logged_at) >= ? AND date(logged_at) <= ?""",
            (start_date, end_date),
        )
        total_hours = round(float(hours_row["total"]), 1) if hours_row else 0.0

        # --- Category stats ---
        cat_stats: dict[str, dict] = {}

        # Seed all categories from both completed and active tasks
        for t in completed + active_tasks:
            cat = t.get("category") or "(未分类)"
            cat_stats.setdefault(cat, {"completed": 0, "hours": 0.0})

        # Count completed per category
        for t in completed:
            cat = t.get("category") or "(未分类)"
            cat_stats[cat]["completed"] += 1

        # Hours per category (from progress_logs joined on tasks)
        cat_hours = self.db.fetch_all(
            """SELECT t.category, COALESCE(SUM(pl.hours_spent), 0) AS total_hours
               FROM progress_logs pl
               JOIN tasks t ON pl.task_id = t.id
               WHERE date(pl.logged_at) >= ? AND date(pl.logged_at) <= ?
               GROUP BY t.category""",
            (start_date, end_date),
        )
        for row in cat_hours:
            cat = row["category"] or "(未分类)"
            if cat in cat_stats:
                cat_stats[cat]["hours"] = round(float(row["total_hours"]), 1)

        # --- Average completion days for tasks completed this month ---
        avg_days_row = self.db.fetch_one(
            """SELECT AVG(JULIANDAY(updated_at) - JULIANDAY(created_at)) AS avg_days
               FROM tasks
               WHERE status = 'done'
                 AND date(updated_at) >= ?
                 AND date(updated_at) <= ?""",
            (start_date, end_date),
        )
        avg_completion_days = round(float(avg_days_row["avg_days"]), 1) if avg_days_row and avg_days_row["avg_days"] else None

        return {
            "completed": completed,
            "completed_count": len(completed),
            "active_tasks": active_tasks,
            "active_tasks_count": len(active_tasks),
            "new_tasks": new_tasks,
            "new_count": len(new_tasks),
            "total_hours": total_hours,
            "category_stats": cat_stats,
            "avg_completion_days": avg_completion_days,
        }

    def _query_next_month_tasks(self, year: int, month: int) -> list[dict]:
        """Return tasks with deadlines falling in the *next* calendar month."""
        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1

        _, last_day = monthrange(next_year, next_month)
        start = f"{next_year}-{next_month:02d}-01"
        end = f"{next_year}-{next_month:02d}-{last_day:02d}"

        return self.db.fetch_all(
            """SELECT * FROM tasks
               WHERE status NOT IN ('done', 'cancelled')
                 AND deadline IS NOT NULL
                 AND date(deadline) >= ? AND date(deadline) <= ?
               ORDER BY deadline ASC""",
            (start, end),
        )

    def _query_okr_progress(self) -> list[dict]:
        """Query OKR progress summary from OKRManager."""
        summary = self.okr.progress_summary()
        return summary.get("objectives", [])

    # ===================================================================
    # Internal — Format (monthly)
    # ===================================================================

    def _format_monthly_report(
        self,
        year: int,
        month: int,
        data: dict,
        okr_data: list[dict],
        next_month_tasks: list[dict],
    ) -> str:
        lines: list[str] = []

        # -- Title --
        lines.append(f"# 月度工作报告 — {year}年{month}月")
        lines.append("")

        # -- Overview --
        lines.append("## 📊 概览")
        lines.append(f"- 完成任务: {data['completed_count']} 项")
        lines.append(f"- 活跃任务: {data['active_tasks_count']} 项")
        lines.append(f"- 总投入时间: {data['total_hours']} 小时")
        lines.append(f"- 新增任务: {data['new_count']} 项")
        if data.get("avg_completion_days") is not None:
            lines.append(f"- 平均任务完成天数: {data['avg_completion_days']} 天")
        lines.append("")

        # -- Completed --
        lines.append("## ✅ 本月完成")
        if data["completed"]:
            lines.append("| 任务 | 分类 | 优先级 | 完成日期 | 投入时间 |")
            lines.append("| --- | --- | --- | --- | --- |")
            for t in data["completed"]:
                cat = t.get("category") or "-"
                pri = f"P{t['priority']}" if t.get("priority") else "-"
                done_date = (t.get("updated_at") or "")[:10]
                hours = t.get("actual_hours") or 0
                lines.append(
                    f"| {t['title']} | {cat} | {pri} | {done_date} | {hours}h |"
                )
        else:
            lines.append("本月无完成任务。")
        lines.append("")

        # -- Active tasks --
        lines.append("## 🔄 活跃任务")
        if data["active_tasks"]:
            lines.append("| 任务 | 分类 | 优先级 | 进度 | 截止日期 |")
            lines.append("| --- | --- | --- | --- | --- |")
            for t in data["active_tasks"]:
                cat = t.get("category") or "-"
                pri = f"P{t['priority']}" if t.get("priority") else "-"
                prog = f"{t.get('progress') or 0}%"
                dl = (t.get("deadline") or "")[:10] if t.get("deadline") else "-"
                lines.append(
                    f"| {t['title']} | {cat} | {pri} | {prog} | {dl} |"
                )
        else:
            lines.append("暂无活跃任务。")
        lines.append("")

        # -- Category stats --
        lines.append("## 📈 分类统计")
        lines.append("| 分类 | 完成数 | 投入时间 |")
        lines.append("| --- | --- | --- |")
        for cat in sorted(data["category_stats"]):
            stats = data["category_stats"][cat]
            lines.append(f"| {cat} | {stats['completed']} | {stats['hours']}h |")
        lines.append("")

        # -- OKR progress --
        lines.append("## 🎯 OKR 进展")
        if okr_data:
            lines.append("| Objective | 进度 | 关联任务 |")
            lines.append("| --- | --- | --- |")
            for obj in okr_data:
                title = obj["title"]
                progress = f"{obj['progress']}%"
                linked = sum(
                    kr.get("linked_task_count", 0)
                    for kr in obj.get("key_results", [])
                )
                lines.append(f"| {title} | {progress} | {linked} |")
        else:
            lines.append("暂无 OKR 数据。")
        lines.append("")

        # -- Key outputs --
        lines.append("## 💡 关键产出")
        if data["completed"]:
            for t in data["completed"]:
                milestones = self.pt.list_milestones(t["id"])
                if milestones:
                    done_ms = [m for m in milestones if m["status"] == "completed"]
                    lines.append(
                        f"- **{t['title']}** — {len(done_ms)}/{len(milestones)} 里程碑完成"
                    )
                else:
                    lines.append(f"- **{t['title']}**")
        else:
            lines.append("本月无关键产出。")
        lines.append("")

        # -- Next month --
        lines.append("## 📅 下月展望")
        if next_month_tasks:
            for t in next_month_tasks:
                dl = (t.get("deadline") or "")[:10]
                lines.append(
                    f"- **{t['title']}** 📅 {dl} `{t.get('category') or '-'}`"
                )
        else:
            lines.append("下月暂无到期任务。")

        return "\n".join(lines)

    # ===================================================================
    # Internal — Format (semi-annual)
    # ===================================================================

    def _format_semiannual_report(
        self,
        year: int,
        half_label: str,
        total_completed: int,
        total_hours: float,
        total_new: int,
        all_monthly_data: list[tuple[int, dict]],
        monthly_trend: list[dict],
        okr_data: list[dict],
    ) -> str:
        lines: list[str] = []

        # -- Title --
        lines.append(f"# 半年度工作报告 — {year}年{half_label}")
        lines.append("")

        # -- Overview --
        lines.append("## 📊 概览")
        lines.append(f"- 完成任务: {total_completed} 项")
        lines.append(f"- 总投入时间: {total_hours} 小时")
        lines.append(f"- 新增任务: {total_new} 项")
        lines.append("")

        # -- Monthly trend --
        lines.append("## 📈 月度趋势")
        lines.append("| 月份 | 完成数 | 进行中 | 投入时间 |")
        lines.append("| --- | --- | --- | --- |")
        for item in monthly_trend:
            m = item["month"]
            lines.append(
                f"| {m}月 | {item['completed']} | {item['in_progress']} | "
                f"{item['total_hours']}h |"
            )
        lines.append("")

        # -- Trend bars (text-based) --
        if monthly_trend:
            max_completed = max(item["completed"] for item in monthly_trend)
            bar_width = max(max_completed, 1)
            for item in monthly_trend:
                m = item["month"]
                cnt = item["completed"]
                bar = "█" * cnt if cnt > 0 else ""
                lines.append(f"- {m}月: {bar} {cnt}项")
            lines.append("")

            # Trend description
            completed_counts = [item["completed"] for item in monthly_trend]
            if len(completed_counts) >= 2:
                if all(completed_counts[i] <= completed_counts[i+1] for i in range(len(completed_counts)-1)):
                    lines.append("> 📈 趋势：任务完成数逐月上升")
                elif all(completed_counts[i] >= completed_counts[i+1] for i in range(len(completed_counts)-1)):
                    lines.append("> 📉 趋势：任务完成数逐月下降")
                elif completed_counts[-1] > completed_counts[0]:
                    lines.append("> 📊 趋势：整体呈上升态势，中间有波动")
                elif completed_counts[-1] < completed_counts[0]:
                    lines.append("> 📊 趋势：整体呈下降态势，中间有波动")
                else:
                    lines.append("> 📊 趋势：任务完成数整体持平")
            lines.append("")

        # -- Per-month detail --
        for m, data in all_monthly_data:
            lines.append(f"## {m}月")
            lines.append(
                f"完成 {data['completed_count']} 项，"
                f"新增 {data['new_count']} 项，"
                f"投入 {data['total_hours']}h"
            )
            if data["completed"]:
                lines.append("")
                lines.append("**完成的任务：**")
                for t in data["completed"][:5]:
                    lines.append(f"- {t['title']}")
                if data["completed_count"] > 5:
                    lines.append(f"- ...及其他 {data['completed_count'] - 5} 项")
            lines.append("")

        # -- Aggregated category stats --
        all_cats: dict[str, dict] = {}
        for _, data in all_monthly_data:
            for cat, stats in data["category_stats"].items():
                all_cats.setdefault(cat, {"completed": 0, "hours": 0.0})
                all_cats[cat]["completed"] += stats["completed"]
                all_cats[cat]["hours"] += stats["hours"]

        lines.append("## 📊 分类统计")
        lines.append("| 分类 | 完成数 | 投入时间 |")
        lines.append("| --- | --- | --- |")
        for cat in sorted(all_cats):
            stats = all_cats[cat]
            lines.append(f"| {cat} | {stats['completed']} | {stats['hours']}h |")
        lines.append("")

        # -- OKR progress --
        lines.append("## 🎯 OKR 进展")
        if okr_data:
            lines.append("| Objective | 进度 | 关联任务 |")
            lines.append("| --- | --- | --- |")
            for obj in okr_data:
                title = obj["title"]
                progress = f"{obj['progress']}%"
                linked = sum(
                    kr.get("linked_task_count", 0)
                    for kr in obj.get("key_results", [])
                )
                lines.append(f"| {title} | {progress} | {linked} |")
        else:
            lines.append("暂无 OKR 数据。")

        return "\n".join(lines)

    # ===================================================================
    # Generic format entry point (for extensibility)
    # ===================================================================

    def _format_report(self, data: dict) -> str:
        """Assemble a Markdown report from pre-computed data dict.

        This is a generic entry point primarily intended for extensibility.
        The *data* dict should include at minimum ``year`` and ``month``,
        plus the same keys returned by ``_query_monthly_tasks``, ``okr``,
        and ``next_month``.
        """
        return self._format_monthly_report(
            year=data.get("year", date.today().year),
            month=data.get("month", date.today().month),
            data=data,
            okr_data=data.get("okr", []),
            next_month_tasks=data.get("next_month", []),
        )
