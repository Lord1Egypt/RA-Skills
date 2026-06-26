"""Morning report generator — overnight execution summary."""

from __future__ import annotations
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from .models import PlanStatus
    from .queue import get_plan, list_plans
    from .git_manager import get_branch_commits, get_diff_stats
except ImportError:  # Allow direct execution via executor.py from scripts/
    from models import PlanStatus
    from queue import get_plan, list_plans
    from git_manager import get_branch_commits, get_diff_stats

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"

REPORTS_DIR = _DATA_DIR / "reports"
WORKSPACE = _WORKSPACE


class MorningReporter:
    """Generate morning reports for overnight execution."""

    def generate_report(self, date: Optional[str] = None) -> str:
        """Generate a morning report. date defaults to today."""
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # Load all plans
        index = list_plans()
        plans = []
        for entry in index:
            plan = get_plan(entry["id"])
            if plan and plan.status in (
                PlanStatus.COMPLETED,
                PlanStatus.FAILED,
                PlanStatus.SKIPPED,
            ):
                plans.append(plan)

        if not plans:
            report = f"# 🌅 Night Shift Report — {date}\n\nNo plans were executed.\n"
            self._save_report(report, date)
            return report

        # Categorize
        completed = [p for p in plans if p.status == PlanStatus.COMPLETED]
        failed = [p for p in plans if p.status == PlanStatus.FAILED]
        skipped = [p for p in plans if p.status == PlanStatus.SKIPPED]

        # Aggregate stats
        total_commits = sum(len(get_branch_commits(p.id)) for p in completed)
        total_time = sum(p.execution.total_duration_seconds for p in plans)
        total_api_calls = sum(p.execution.total_api_calls for p in plans)

        # Build report
        lines = [
            f"# 🌅 Night Shift Report — {date}",
            "",
            "## Summary",
            f"- **Plans executed:** {len(plans)}",
            f"- **Succeeded:** {len(completed)} ✅",
            f"- **Failed:** {len(failed)} ❌",
            f"- **Skipped:** {len(skipped)} ⏭️",
            f"- **Total time:** {_format_duration(total_time)}",
            f"- **API calls:** {total_api_calls}",
            f"- **Commits:** {total_commits}",
            "",
        ]

        # Completed plans
        if completed:
            lines.append("## Completed Plans ✅\n")
            for p in completed:
                commits = get_branch_commits(p.id)
                diff = get_diff_stats(p.id)
                lines.append(f"### Plan #{p.id}: {p.title}")
                lines.append(f"- **Branch:** `night-shift/{p.id}`")
                lines.append(
                    f"- **Phases:** {sum(1 for ph in p.phases if ph.status.value == 'passed')}/{len(p.phases)} passed"
                )
                lines.append(
                    f"- **Time:** {_format_duration(p.execution.total_duration_seconds)}"
                )
                lines.append(f"- **API calls:** {p.execution.total_api_calls}")
                if commits:
                    lines.append("- **Commits:**")
                    for c in commits:
                        lines.append(f"  - `{c['hash']}` {c['message']}")
                if diff:
                    lines.append(f"- **Changes:** {diff}")
                lines.append("- **Status:** Ready to merge ⬅️ review & merge")
                lines.append("")

        # Failed plans
        if failed:
            lines.append("## Failed Plans ❌\n")
            for p in failed:
                # Find failed phase
                failed_phase = next(
                    (ph for ph in p.phases if ph.status.value == "failed"), None
                )
                fail_info = ""
                if failed_phase:
                    fail_info = f"- **Failed at:** Phase {failed_phase.id}/{len(p.phases)} ({failed_phase.title})\n"
                    if failed_phase.attempts:
                        fail_info += f"- **Attempts:** {failed_phase.attempts}\n"

                # Get failure log
                if p.execution.failure_log:
                    last_failure = p.execution.failure_log[-1]
                    fail_info += f"- **Error:** `{last_failure.get('error_type', 'unknown')}` — {last_failure.get('details', 'N/A')[:200]}\n"

                fail_info += (
                    f"- **Partial work:** Branch preserved at `night-shift/{p.id}`\n"
                )
                fail_info += "- **Status:** Needs manual intervention\n"

                lines.append(f"### Plan #{p.id}: {p.title}")
                lines.append(fail_info)
                lines.append("")

        # Skipped plans
        if skipped:
            lines.append("## Skipped Plans ⏭️\n")
            for p in skipped:
                lines.append(f"### Plan #{p.id}: {p.title}")
                lines.append("- **Reason:** Budget/time exceeded")
                lines.append("- **Status:** Re-queued for next night")
                lines.append("")

        # Recommendations
        if failed:
            lines.append("## Recommendations\n")
            lines.append(
                "1. Review failed plan branches manually before next night shift"
            )
            lines.append("2. Consider adjusting phase prompts for failed phases")
            lines.append("3. Use `/plan retry #<id>` to re-queue failed plans")

        report = "\n".join(lines)
        self._save_report(report, date)
        return report

    def get_latest_report(self) -> Optional[str]:
        """Get the most recent report."""
        if not REPORTS_DIR.exists():
            return None
        reports = sorted(REPORTS_DIR.glob("*.md"))
        if not reports:
            return None
        return reports[-1].read_text()

    def _save_report(self, report: str, date: str):
        path = REPORTS_DIR / f"{date}.md"
        path.write_text(report)


def _format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"
