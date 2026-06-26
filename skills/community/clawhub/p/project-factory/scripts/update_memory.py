#!/usr/bin/env python3
"""Generate or update the project's memory log entry for today.

Run after each pipeline execution to scaffold today's memory entry.
Human fills in the "learnings" section.

Usage:
    python3 scripts/update_memory.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = ROOT / "memory"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ENTRY_PATH = MEMORY_DIR / f"{TODAY}.md"


def load_latest_summary(project_dir: Path) -> dict | None:
    summary_path = project_dir / "logs" / "latest_run_summary.json"
    if summary_path.exists():
        try:
            return json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def build_memory_entry(project_key: str, project_name: str, summary: dict | None) -> str:
    status = summary.get("status", "unknown") if summary else "unknown"
    run_date = summary.get("runDate", TODAY) if summary else TODAY
    run_id = summary.get("runId", "N/A") if summary else "N/A"

    issues = []
    if summary:
        issues = summary.get("failures", []) + summary.get("warnings", [])

    lines = [
        f"# {TODAY} — {project_name}",
        "",
        f"**Project**: {project_key}",
        f"**Run Date**: {run_date}",
        f"**Status**: {status}",
        f"**Run ID**: {run_id}",
        "",
    ]

    if summary:
        # Summarize key metrics
        for section in ["trend", "content", "tasks"]:
            if section in summary:
                lines.append(f"**{section.capitalize()}**: {summary[section]}")
        lines.append("")

    lines += [
        "## Today's Summary",
        "",
        "<!-- Human: describe what happened today, key decisions, errors encountered -->",
        "",
        "## Learnings",
        "",
        "<!-- Human: what did we learn? what should be remembered for next time? -->",
        "",
        "## Issues to Track",
        ""
    ]

    if issues:
        for issue in issues:
            lines.append(f"- [ ] {issue}")
        lines.append("")
    else:
        lines.append("<!-- No issues to track today -->")
        lines.append("")

    lines += [
        "## Next Steps",
        "",
        "<!-- Human: what needs to be done next? -->",
        "",
        "---",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
    ]

    return "\n".join(lines)


def main() -> None:
    project_key = Path(__file__).resolve().parent.parent.name
    project_dir = Path(__file__).resolve().parents[2] / "projects" / project_key
    project_name = project_key  # fallback

    # Try to get project name from PROJECT.md
    pm = project_dir / "PROJECT.md"
    if pm.exists():
        for line in pm.read_text(encoding="utf-8").splitlines():
            if line.startswith("# Project:"):
                project_name = line.replace("# Project:", "").strip()
                break

    MEMORY_DIR.mkdir(exist_ok=True)

    if ENTRY_PATH.exists():
        print(f"[update_memory] {ENTRY_PATH} already exists — not overwriting")
        print(f"  Run date: {TODAY}")
        sys.exit(0)

    summary = load_latest_summary(project_dir)
    entry = build_memory_entry(project_key, project_name, summary)
    ENTRY_PATH.write_text(entry, encoding="utf-8")
    print(f"[update_memory] Created {ENTRY_PATH}")
    print(f"  Project: {project_key}")
    print(f"  Status: {summary.get('status') if summary else 'N/A'}")
    print(f"\n  Open the file and fill in the ## Learnings section.")


if __name__ == "__main__":
    main()
