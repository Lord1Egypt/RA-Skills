"""
Personal Assistant Skill — Advisor Module (Sprint 2)

Workload analysis + intelligent suggestions built on Database, TaskManager,
and OKRManager.  All analysis is rule-based; no LLM calls are made here.
The ``get_context_for_llm()`` method aggregates results into a structured
text representation that an upstream LLM (e.g. Hermes Agent with a pro model)
can use to generate natural-language advice.
"""

from __future__ import annotations
import json
from datetime import date, datetime, timedelta

from .db import Database
from .okr import OKRManager
from .task_manager import TaskManager

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HIGH_PRIORITY_THRESHOLD = 2  # priorities 1-2 are "high"
DELEGATABLE_CATEGORIES = frozenset({  # categories that suggest delegatability
    "会议", "meeting", "文档", "documentation", "测试", "testing",
    "运维", "ops", "review", "审查",
})
PERSONAL_CATEGORIES = frozenset({"个人", "personal", "生活", "health", "健康"})

# ---------------------------------------------------------------------------
# Advisor
# ---------------------------------------------------------------------------

class Advisor:
    """Workload analysis and intelligent task/OKR suggestions."""

    def __init__(self, db: Database, task_manager: 'TaskManager', okr_manager: 'OKRManager'):
        self.db = db
        self.tm = task_manager
        self.okr = okr_manager

    # ===================================================================
    # 1. Workload analysis
    # ===================================================================

    def analyze_workload(self) -> dict:
        """Analyse current workload and return structured data.

        Returns a dict with counts, hour estimates, busy categories,
        untethered OKRs, and simple rule-based suggestions.
        """
        # --- Active tasks (exclude done & cancelled) ------------------------
        raw_active = self.tm.list(
            status=["todo", "in_progress", "blocked"],
            limit=500,
            order_by="priority",
        )
        active_tasks = len(raw_active)

        # --- Overdue tasks --------------------------------------------------
        raw_overdue = self.tm.overdue()
        overdue_tasks = len(raw_overdue)

        # --- High priority (1-2) -------------------------------------------
        high_priority_tasks = sum(
            1 for t in raw_active
            if (t.get("priority") or 5) <= HIGH_PRIORITY_THRESHOLD
        )

        # --- Today & this week ----------------------------------------------
        today = date.today()
        today_str = today.isoformat()
        week_end = today + timedelta(days=7)
        week_end_str = week_end.isoformat()

        today_tasks = sum(
            1 for t in raw_active
            if t.get("deadline") and t["deadline"][:10] <= today_str
        )
        # Also include tasks without a deadline (they can be done anytime)
        today_tasks += sum(1 for t in raw_active if not t.get("deadline"))

        this_week_tasks = sum(
            1 for t in raw_active
            if t.get("deadline") and today_str <= t["deadline"][:10] <= week_end_str
        ) + today_tasks  # today_tasks already includes those due ≤today

        # --- Estimated hours remaining --------------------------------------
        estimated_hours_remaining = sum(
            t.get("estimated_hours", 0) or 0 for t in raw_active
        )

        # --- Busy categories ------------------------------------------------
        cat_count: dict[str, int] = {}
        for t in raw_active:
            cat = (t.get("category") or "").strip()
            if cat:
                cat_count[cat] = cat_count.get(cat, 0) + 1
        # Top 5 categories by count
        busy_categories = sorted(cat_count, key=cat_count.get, reverse=True)[:5]

        # --- OKRs with no linked tasks --------------------------------------
        okr_with_no_tasks = self._find_okrs_with_no_tasks()

        # --- Rule-based suggestions -----------------------------------------
        suggestions: list[str] = []

        # Suggestion 1: delegation candidates
        delegatable = [
            t for t in raw_active
            if (t.get("category") or "").strip() in DELEGATABLE_CATEGORIES
               and (t.get("category") or "").strip() not in PERSONAL_CATEGORIES
        ]
        if delegatable:
            titles = [t["title"] for t in delegatable[:3]]
            suggestions.append(
                f"建议将任务 {', '.join(repr(t) for t in titles)} 考虑委派或并行处理"
            )

        # Suggestion 2: high priority cluster on same day
        high_prio_with_deadline = [
            t for t in raw_active
            if (t.get("priority") or 5) <= HIGH_PRIORITY_THRESHOLD and t.get("deadline")
        ]
        deadline_groups: dict[str, list[dict]] = {}
        for t in high_prio_with_deadline:
            d = t["deadline"][:10]
            deadline_groups.setdefault(d, []).append(t)
        for d, tasks in deadline_groups.items():
            if len(tasks) >= 3:
                suggestions.append(
                    f"{len(tasks)}项高优任务集中在{d}，建议提前分散安排"
                )

        # Suggestion 3: too many active tasks
        if active_tasks > 10:
            suggestions.append(
                f"当前活跃任务{active_tasks}项较多，建议将低优先级或无截止日期的任务延后"
            )

        # Suggestion 4: overdue attention
        if overdue_tasks:
            suggestions.append(
                f"有{overdue_tasks}项任务已逾期，建议优先处理或重新评估截止日期"
            )

        # Suggestion 5: no high priority work
        if high_priority_tasks == 0 and active_tasks > 3:
            suggestions.append("当前没有高优先级任务，建议确认是否有遗漏的重要事项")

        return {
            "active_tasks": active_tasks,
            "overdue_tasks": overdue_tasks,
            "high_priority_tasks": high_priority_tasks,
            "today_tasks": today_tasks,
            "this_week_tasks": this_week_tasks,
            "estimated_hours_remaining": round(estimated_hours_remaining, 1),
            "busy_categories": busy_categories,
            "okr_with_no_tasks": okr_with_no_tasks,
            "suggestions": suggestions,
        }

    # ===================================================================
    # 2. Delegation suggestions
    # ===================================================================

    def suggest_delegation(self) -> list[dict]:
        """Analyse tasks for delegation or parallel-processing candidates.

        Rules:
        - Non-personal categories (会议/文档/测试/运维/review) are delegatable.
        - Low-priority tasks (4-5) without a deadline can be postponed.
        - Tasks already in "个人" / "personal" category are excluded.

        Returns a list of dicts, each with ``task_id``, ``title``, ``reason``,
        and ``suggested_action`` (``"delegate"`` or ``"postpone"``).
        """
        suggestions: list[dict] = []

        # --- Delegation candidates ------------------------------------------
        raw_active = self.tm.list(
            status=["todo", "in_progress", "blocked"],
            limit=500,
            order_by="priority",
        )

        for t in raw_active:
            cat = (t.get("category") or "").strip()
            task_id = t["id"]
            title = t["title"]
            priority = t.get("priority") or 5
            has_deadline = bool(t.get("deadline"))

            # Delegation: matching category + not personal
            if cat in DELEGATABLE_CATEGORIES and cat not in PERSONAL_CATEGORIES:
                suggestions.append({
                    "task_id": task_id,
                    "title": title,
                    "category": cat,
                    "reason": f"分类 '{cat}' 可考虑委派给团队成员",
                    "suggested_action": "delegate",
                })

            # Postpone: low priority + no deadline + not already flagged
            elif priority >= 4 and not has_deadline:
                suggestions.append({
                    "task_id": task_id,
                    "title": title,
                    "category": cat,
                    "reason": f"低优先级(p{priority})且无截止日期，可延后处理",
                    "suggested_action": "postpone",
                })

        return suggestions

    # ===================================================================
    # 3. Schedule suggestions
    # ===================================================================

    def suggest_schedule(self) -> str:
        """Generate a Markdown daily/weekly schedule suggestion.

        Sorts active tasks by priority and estimated time, flags
        same-day high-priority conflicts, and suggests time allocation.
        """
        raw_active = self.tm.list(
            status=["todo", "in_progress", "blocked"],
            limit=500,
            order_by="priority",
        )

        today = date.today()
        today_str = today.isoformat()

        # Partition: high priority (1-2), medium (3), low (4-5)
        high = [t for t in raw_active if (t.get("priority") or 5) <= 2]
        medium = [t for t in raw_active if (t.get("priority") or 5) == 3]
        low = [t for t in raw_active if (t.get("priority") or 5) >= 4]

        lines: list[str] = []
        lines.append(f"## 📅 日程建议 — {today_str}")
        lines.append("")

        # --- Key warnings ---------------------------------------------------
        # Conflict detection
        deadline_groups: dict[str, list[dict]] = {}
        for t in raw_active:
            if t.get("deadline") and (t.get("priority") or 5) <= 2:
                d = t["deadline"][:10]
                deadline_groups.setdefault(d, []).append(t)

        for d, tasks in deadline_groups.items():
            if len(tasks) >= 3:
                lines.append(f"⚠️ **冲突警告**: {len(tasks)}项高优任务截止于 **{d}**")
                for t in tasks:
                    lines.append(f"  - {t['title']} (p{t.get('priority', '?')})")
                lines.append("")

        # --- High priority --------------------------------------------------
        lines.append("### 🔴 高优先级 (今日优先)")
        lines.append("")
        if high:
            total_high_hours = sum(t.get("estimated_hours", 0) or 0 for t in high)
            for t in high:
                hours = t.get("estimated_hours") or 0
                deadline = t["deadline"][:10] if t.get("deadline") else "无截止"
                status_icon = {"todo": "⬜", "in_progress": "🔄", "blocked": "🚫"}.get(
                    t.get("status", "todo"), "⬜"
                )
                lines.append(
                    f"- {status_icon} **{t['title']}** "
                    f"`p{t.get('priority','?')}` `{hours}h` 📅 {deadline}"
                )
            lines.append(f"\n> 预计总耗时: **{total_high_hours}h**")
        else:
            lines.append("> 无高优先级任务")
        lines.append("")

        # --- Medium priority ------------------------------------------------
        lines.append("### 🟡 中优先级")
        lines.append("")
        if medium:
            total_med_hours = sum(t.get("estimated_hours", 0) or 0 for t in medium)
            for t in medium:
                hours = t.get("estimated_hours") or 0
                deadline = t["deadline"][:10] if t.get("deadline") else "无截止"
                lines.append(
                    f"- {t['title']} `{hours}h` 📅 {deadline}"
                )
            lines.append(f"\n> 预计总耗时: **{total_med_hours}h**")
        else:
            lines.append("> 无中优先级任务")
        lines.append("")

        # --- Low priority ---------------------------------------------------
        lines.append("### 🟢 低优先级 / 可延后")
        lines.append("")
        if low:
            for t in low:
                hours = t.get("estimated_hours") or 0
                deadline = t["deadline"][:10] if t.get("deadline") else "无截止"
                lines.append(
                    f"- {t['title']} `{hours}h` 📅 {deadline}"
                )
        else:
            lines.append("> 无低优先级任务")
        lines.append("")

        # --- Summary stats --------------------------------------------------
        total_hours = sum(t.get("estimated_hours", 0) or 0 for t in raw_active)
        lines.append("---")
        lines.append(f"**总计**: {len(raw_active)} 项活跃任务, "
                     f"预计总耗时 **{total_hours}h**")

        return "\n".join(lines)

    # ===================================================================
    # 4. OKR health check
    # ===================================================================

    def okr_health_check(self) -> dict:
        """Check the health of all active OKRs.

        Returns a dict with:
        - ``progress_behind``: KRs whose progress lags behind elapsed time
        - ``no_tasks``: active OKRs with zero linked tasks
        - ``expiring_soon``: OKRs whose end_date is within 7 days
        """
        today = date.today()
        progress_behind: list[dict] = []
        no_tasks: list[dict] = []
        expiring_soon: list[dict] = []

        # All active key results (the measuring point for progress)
        active_krs = self.db.fetch_all(
            "SELECT * FROM okr_items WHERE obj_type = 'key_result' AND status = 'active'"
        )

        for kr in active_krs:
            kr_id = kr["id"]
            kr_title = kr["title"]
            kr_progress = kr.get("progress", 0) or 0

            # --- Progress-behind check --------------------------------------
            start = kr.get("start_date")
            end = kr.get("end_date")

            if start and end:
                try:
                    start_dt = datetime.strptime(start, "%Y-%m-%d").date()
                    end_dt = datetime.strptime(end, "%Y-%m-%d").date()
                    total_days = (end_dt - start_dt).days
                    elapsed_days = (today - start_dt).days
                except (ValueError, TypeError):
                    total_days = 0
                    elapsed_days = 0

                # Also inherit from parent Objective if KR lacks dates
            else:
                # Try parent Objective's dates
                parent = self.db.fetch_one(
                    "SELECT start_date, end_date FROM okr_items WHERE id = ?",
                    (kr.get("parent_id"),),
                )
                if parent:
                    try:
                        start_dt = datetime.strptime(parent["start_date"], "%Y-%m-%d").date() if parent.get("start_date") else None
                        end_dt = datetime.strptime(parent["end_date"], "%Y-%m-%d").date() if parent.get("end_date") else None
                        if start_dt and end_dt:
                            total_days = (end_dt - start_dt).days
                            elapsed_days = (today - start_dt).days
                        else:
                            total_days = 0
                            elapsed_days = 0
                    except (ValueError, TypeError):
                        total_days = 0
                        elapsed_days = 0
                else:
                    total_days = 0
                    elapsed_days = 0

            if total_days > 0 and elapsed_days >= 7:
                expected_progress = min(int((elapsed_days / total_days) * 100), 100)
                if kr_progress < expected_progress * 0.7:  # 30% lag threshold
                    progress_behind.append({
                        "okr_id": kr_id,
                        "title": kr_title,
                        "current_progress": kr_progress,
                        "expected_progress": expected_progress,
                        "gap": expected_progress - kr_progress,
                    })

            # --- Tasks-linked check -----------------------------------------
            linked = self.db.fetch_all(
                "SELECT COUNT(*) AS cnt FROM tasks "
                "WHERE okr_id = ? AND status NOT IN ('done', 'cancelled')",
                (kr_id,),
            )
            linked_count = linked[0]["cnt"] if linked else 0
            if linked_count == 0:
                # Get parent Objective title for context
                obj_title = ""
                parent_id = kr.get("parent_id")
                if parent_id:
                    parent_row = self.db.fetch_one(
                        "SELECT title FROM okr_items WHERE id = ?", (parent_id,)
                    )
                    if parent_row:
                        obj_title = parent_row["title"]

                no_tasks.append({
                    "okr_id": kr_id,
                    "title": kr_title,
                    "objective_title": obj_title,
                    "obj_type": "key_result",
                })

            # --- Expiring soon ----------------------------------------------
            end_date_str = kr.get("end_date")
            if not end_date_str:
                # Try parent
                if kr.get("parent_id"):
                    parent = self.db.fetch_one(
                        "SELECT end_date FROM okr_items WHERE id = ?",
                        (kr["parent_id"],),
                    )
                    if parent:
                        end_date_str = parent.get("end_date")

            if end_date_str:
                try:
                    end_dt = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                    days_left = (end_dt - today).days
                    if 0 <= days_left <= 7:
                        expiring_soon.append({
                            "okr_id": kr_id,
                            "title": kr_title,
                            "end_date": end_date_str,
                            "days_left": days_left,
                            "progress": kr_progress,
                        })
                except (ValueError, TypeError):
                    pass

        # Also check active Objectives with no tasks at all
        active_objs = self.db.fetch_all(
            "SELECT * FROM okr_items WHERE obj_type = 'objective' AND status = 'active'"
        )
        for obj in active_objs:
            linked = self.db.fetch_all(
                "SELECT COUNT(*) AS cnt FROM tasks "
                "WHERE okr_id = ? AND status NOT IN ('done', 'cancelled')",
                (obj["id"],),
            )
            # Also check KRs under this objective
            krs = self.db.fetch_all(
                "SELECT id FROM okr_items WHERE parent_id = ? AND obj_type = 'key_result'",
                (obj["id"],),
            )
            total_task_count = linked[0]["cnt"] if linked else 0
            for kr in krs:
                kr_linked = self.db.fetch_all(
                    "SELECT COUNT(*) AS cnt FROM tasks "
                    "WHERE okr_id = ? AND status NOT IN ('done', 'cancelled')",
                    (kr["id"],),
                )
                total_task_count += kr_linked[0]["cnt"] if kr_linked else 0

            if total_task_count == 0:
                no_tasks.append({
                    "okr_id": obj["id"],
                    "title": obj["title"],
                    "objective_title": obj["title"],
                    "obj_type": "objective",
                })

        return {
            "progress_behind": progress_behind,
            "no_tasks": no_tasks,
            "expiring_soon": expiring_soon,
        }

    # ===================================================================
    # 5. LLM context aggregator
    # ===================================================================

    def get_context_for_llm(self) -> str:
        """Aggregate all analysis results into a structured text for an LLM.

        The upstream Hermes Agent (pro model) uses this context to
        generate natural-language advice and scheduling recommendations.
        """
        workload = self.analyze_workload()
        delegation = self.suggest_delegation()
        okr_health = self.okr_health_check()

        parts: list[str] = []

        # --- Header ---------------------------------------------------------
        parts.append("=" * 60)
        parts.append("PERSONAL ASSISTANT — WORKLOAD CONTEXT")
        parts.append(f"Generated: {datetime.now().isoformat()}")
        parts.append("=" * 60)
        parts.append("")

        # --- Workload summary -----------------------------------------------
        parts.append("## 工作负载总览")
        parts.append(f"- 活跃任务: {workload['active_tasks']}")
        parts.append(f"- 逾期任务: {workload['overdue_tasks']}")
        parts.append(f"- 高优先级: {workload['high_priority_tasks']}")
        parts.append(f"- 今日任务: {workload['today_tasks']}")
        parts.append(f"- 本周任务: {workload['this_week_tasks']}")
        parts.append(f"- 剩余预估工时: {workload['estimated_hours_remaining']}h")
        parts.append(f"- 繁忙分类: {', '.join(workload['busy_categories']) if workload['busy_categories'] else '无'}")
        parts.append("")

        # --- OKRs without tasks ---------------------------------------------
        if workload["okr_with_no_tasks"]:
            parts.append("## 无关联任务的 OKR")
            for okr_title in workload["okr_with_no_tasks"]:
                parts.append(f"- {okr_title}")
            parts.append("")

        # --- Rule-based suggestions -----------------------------------------
        if workload["suggestions"]:
            parts.append("## 系统建议 (规则引擎)")
            for i, s in enumerate(workload["suggestions"], 1):
                parts.append(f"{i}. {s}")
            parts.append("")

        # --- Delegation candidates ------------------------------------------
        if delegation:
            parts.append("## 委派 / 延后建议")
            delegate_items = [d for d in delegation if d["suggested_action"] == "delegate"]
            postpone_items = [d for d in delegation if d["suggested_action"] == "postpone"]
            if delegate_items:
                parts.append("### 可委派")
                for d in delegate_items:
                    parts.append(f"- [{d['task_id']}] {d['title']} — {d['reason']}")
            if postpone_items:
                parts.append("### 可延后")
                for d in postpone_items:
                    parts.append(f"- [{d['task_id']}] {d['title']} — {d['reason']}")
            parts.append("")

        # --- OKR health -----------------------------------------------------
        parts.append("## OKR 健康检查")
        if okr_health["progress_behind"]:
            parts.append("### 进度落后")
            for kr in okr_health["progress_behind"]:
                parts.append(
                    f"- **{kr['title']}**: 当前 {kr['current_progress']}%, "
                    f"预期 {kr['expected_progress']}%, 差距 {kr['gap']}%"
                )
        else:
            parts.append("### 进度落后: 无")

        if okr_health["no_tasks"]:
            parts.append("### 无关联任务")
            for item in okr_health["no_tasks"]:
                parts.append(f"- [{item['obj_type']}] {item['title']}")
        else:
            parts.append("### 无关联任务: 无")

        if okr_health["expiring_soon"]:
            parts.append("### 即将到期 (≤7天)")
            for kr in okr_health["expiring_soon"]:
                parts.append(
                    f"- **{kr['title']}**: {kr['days_left']}天, "
                    f"进度 {kr['progress']}%"
                )
        else:
            parts.append("### 即将到期: 无")
        parts.append("")

        # --- Footer ---------------------------------------------------------
        parts.append("=" * 60)
        parts.append("END OF CONTEXT — Please generate natural-language advice.")
        parts.append("=" * 60)

        return "\n".join(parts)

    # ===================================================================
    # Helpers
    # ===================================================================

    def _find_okrs_with_no_tasks(self) -> list[str]:
        """Return titles of active OKR items that have zero linked active tasks.

        Checks key_results first (more actionable), then objectives
        that have no tasks anywhere in their subtree.
        """
        titles: list[str] = []

        # Check active key_results
        active_krs = self.db.fetch_all(
            "SELECT id, title FROM okr_items "
            "WHERE obj_type = 'key_result' AND status = 'active'"
        )
        for kr in active_krs:
            linked = self.db.fetch_all(
                "SELECT COUNT(*) AS cnt FROM tasks "
                "WHERE okr_id = ? AND status NOT IN ('done', 'cancelled')",
                (kr["id"],),
            )
            if linked and linked[0]["cnt"] == 0:
                titles.append(kr["title"])

        # Check active objectives (only those with KRs that all have 0 tasks)
        active_objs = self.db.fetch_all(
            "SELECT id, title FROM okr_items "
            "WHERE obj_type = 'objective' AND status = 'active'"
        )
        for obj in active_objs:
            # Get all KRs under this objective
            krs = self.db.fetch_all(
                "SELECT id FROM okr_items WHERE parent_id = ? AND obj_type = 'key_result'",
                (obj["id"],),
            )
            if not krs:
                # No KRs at all — check direct task links on the objective
                linked = self.db.fetch_all(
                    "SELECT COUNT(*) AS cnt FROM tasks "
                    "WHERE okr_id = ? AND status NOT IN ('done', 'cancelled')",
                    (obj["id"],),
                )
                if linked and linked[0]["cnt"] == 0:
                    titles.append(obj["title"])
            else:
                # Check if ALL KRs have zero tasks
                all_empty = True
                for kr in krs:
                    linked = self.db.fetch_all(
                        "SELECT COUNT(*) AS cnt FROM tasks "
                        "WHERE okr_id = ? AND status NOT IN ('done', 'cancelled')",
                        (kr["id"],),
                    )
                    if linked and linked[0]["cnt"] > 0:
                        all_empty = False
                        break
                if all_empty:
                    titles.append(obj["title"])

        return titles

    # ===================================================================
    # Integration-test compatibility aliases
    # ===================================================================

    # Priority suggestion keywords (order matters: more specific first)
    _URGENT_KEYWORDS = (
        "crash", "critical", "outage", "incident", "broken",
        "security", "production", "bug", "fix", "urgent", "紧急",
    )
    _LOW_PRIORITY_KEYWORDS = frozenset({
        "polish", "refactor", "nice to have", "optional",
        "documentation", "readme", "update readme", "整理", "笔记",
    })

    def suggest_priority(self, title: str, category: str = "") -> dict:
        """Suggest a priority (1-5) for a new task based on title keywords.

        Returns a dict with ``priority`` and ``reason``.
        """
        title_lower = title.lower()
        cat_lower = (category or "").lower()

        # Category-based: "urgent" category → p1
        if "urgent" in cat_lower:
            return {"priority": 1, "reason": "category 'urgent' implies high urgency"}

        # Keyword-based: urgent terms → p1
        for kw in self._URGENT_KEYWORDS:
            if kw in title_lower:
                return {"priority": 1, "reason": f"keyword '{kw}' indicates urgency"}

        # Low-priority keywords → p3 (default)
        for kw in self._LOW_PRIORITY_KEYWORDS:
            if kw in title_lower:
                return {"priority": 3, "reason": "standard priority, no urgency indicators"}

        return {"priority": 3, "reason": "standard priority, no urgency indicators"}

    def recommend_next(self, limit: int = 5) -> list[dict]:
        """Recommend the next tasks to work on.

        Returns a sorted list of task dicts (id, title, priority, etc.)
        that the user should tackle next.
        """
        # Get active tasks sorted by priority
        raw_active = self.tm.list(
            status=["todo", "in_progress"],
            limit=200,
            order_by="priority",
        )

        # Boost OKR-linked tasks: move them ahead of same-priority non-OKR tasks
        okr_tasks: list[dict] = []
        non_okr_tasks: list[dict] = []
        for t in raw_active:
            if t.get("okr_id"):
                okr_tasks.append(t)
            else:
                non_okr_tasks.append(t)

        # Interleave: OKR tasks first, then non-OKR, both sorted by priority
        result = okr_tasks + non_okr_tasks
        return result[:limit]

    def workload_analysis(self) -> dict:
        """Alias for ``analyze_workload`` with an added ``status`` field.

        The ``status`` field indicates workload level:
        - ``"light"``: 0–3 active tasks
        - ``"moderate"``: 4–10 active tasks
        - ``"overloaded"``: >10 active tasks
        """
        result = self.analyze_workload()
        n = result["active_tasks"]
        if n <= 3:
            result["status"] = "light"
        elif n <= 10:
            result["status"] = "moderate"
        else:
            result["status"] = "overloaded"
        return result
