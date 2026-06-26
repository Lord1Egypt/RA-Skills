#!/usr/bin/env python3
"""Self-check for a bootstrapped project. Run manually or via cron for health monitoring."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "projects" / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from project_routing_loader import load_project_routing


def main() -> None:
    project_key = Path(__file__).resolve().parent.parent.name
    project_root = Path(__file__).resolve().parents[2] / "projects" / project_key

    print(f"=== Self-Check: {project_key} ===")
    issues = []
    warnings = []

    # 1. Check latest_run_summary.json exists and is fresh
    summary_path = project_root / "logs" / "latest_run_summary.json"
    if not summary_path.exists():
        issues.append(f"latest_run_summary.json missing — pipeline may never have run")
    else:
        try:
            data = json.loads(summary_path.read_text(encoding="utf-8"))
            run_date_str = data.get("runDate", "")
            # Check freshness (within 48 hours)
            try:
                from dateutil import parser as dateutil
                run_date = dateutil.parse(run_date_str)
                now = datetime.now(timezone.utc)
                age = (now - run_date.replace(tzinfo=timezone.utc)).total_seconds()
                if age > 48 * 3600:
                    warnings.append(f"latest_run_summary.json is {age/3600:.0f}h old (> 48h)")
            except Exception:
                pass
            if data.get("status") == "error":
                issues.append(f"Latest run status is 'error': {data.get('failures', [])}")
        except Exception as e:
            issues.append(f"latest_run_summary.json unreadable: {e}")

    # 2. Check routing config
    try:
        route = load_project_routing(
            project_key=project_key,
            default_routing_group=f"{project_key}-group",
            default_chat_id="",
            default_target=project_key,
        )
        if not route.get("chatId"):
            issues.append("chatId not configured in routing")
        report_thread = route.get("reportThreadId") or route.get("threadId")
        if not report_thread:
            warnings.append("reportThreadId not set — reports may go to wrong thread")
    except Exception as e:
        issues.append(f"Routing config error: {e}")

    # 3. Check required directories
    for subdir in ["data/rewrite_queue", "data/rewrite_results", "logs"]:
        if not (project_root / subdir).exists():
            warnings.append(f"Directory missing: {subdir}")

    # 4. Check scripts are executable
    scripts_dir = project_root / "scripts"
    for script in ["run_pipeline.sh", "pipeline_reporter.py", "write_run_summary.py"]:
        path = scripts_dir / script
        if not path.exists():
            issues.append(f"Script missing: {script}")

    # 5. Summary
    if issues:
        print(f"\n❌ Issues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if not issues and not warnings:
        print(f"\n✅ All checks passed")

    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
