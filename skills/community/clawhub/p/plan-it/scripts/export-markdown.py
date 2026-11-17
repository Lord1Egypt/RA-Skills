#!/usr/bin/env python3
"""export-markdown.py — flatten plan.html embedded JSON to clean Markdown.

Mitigates the "I want to hand-edit" critique sometimes raised about HTML outputs:
plan-it round-trips between HTML and Markdown via this script.

Output: task_plan.md, findings.md, progress.md (planning-with-files compatible).

Usage:
  python scripts/export-markdown.py                # writes task_plan.md + findings.md + progress.md
  python scripts/export-markdown.py --stdout       # print combined to stdout
  python scripts/export-markdown.py --single       # single combined plan.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DATA_BLOCK_RE = re.compile(
    r'<script\s+type="application/json"\s+id="plan-data"\s*>\s*(\{.*?\})\s*</script>',
    re.DOTALL,
)


def _resolve_plan_path() -> Path | None:
    plan_id = (Path(".planning") / ".active_plan")
    if plan_id.is_file():
        slug = plan_id.read_text(encoding="utf-8").strip()
        if slug:
            cand = Path(".planning") / slug / "plan.html"
            if cand.is_file():
                return cand
    if Path("plan.html").is_file():
        return Path("plan.html")
    return None


def _extract(plan_path: Path) -> dict | None:
    try:
        text = plan_path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = DATA_BLOCK_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def render_task_plan(plan: dict) -> str:
    out: list[str] = []
    title = plan.get("plan_title", "Plan")
    out.append(f"# Task Plan: {title}")
    out.append("")
    goal = plan.get("goal", "")
    if goal:
        out.append("## Goal")
        out.append(goal)
        out.append("")
    out.append(f"## Current Phase")
    out.append(f"Phase {plan.get('current_phase', 1)}")
    out.append("")
    out.append("## Phases")
    out.append("")
    for ph in plan.get("phases", []):
        out.append(f"### Phase {ph.get('id')}: {ph.get('title', '')}")
        for it in ph.get("items", []):
            mark = "[x]" if it.get("done") else "[ ]"
            owner = it.get("owner")
            line = f"- {mark} {it.get('text', '')}"
            if owner:
                line += f" (@{owner})"
            out.append(line)
        out.append(f"- **Status:** {ph.get('status', 'pending')}")
        if ph.get("milestones"):
            out.append("- **Milestones:**")
            for m in ph["milestones"]:
                out.append(f"  - {m}")
        out.append("")
    decisions = plan.get("decisions", [])
    if decisions:
        out.append("## Decisions Made")
        out.append("| Decision | Rationale |")
        out.append("|---|---|")
        for d in decisions:
            out.append(f"| {d.get('decision', '')} | {d.get('rationale', '')} |")
        out.append("")
    errors = plan.get("errors", [])
    if errors:
        out.append("## Errors Encountered")
        out.append("| Timestamp | Error | Attempt | Resolution |")
        out.append("|---|---|---|---|")
        for e in errors:
            out.append(
                f"| {e.get('ts', '')} | {e.get('error', '')} | {e.get('attempt', '')} | {e.get('resolution', '')} |"
            )
        out.append("")
    return "\n".join(out)


def render_findings(plan: dict) -> str:
    out = ["# Findings"]
    for f in plan.get("findings", []):
        topic = f.get("topic", "(untitled)")
        body = f.get("body", "")
        out.append("")
        out.append(f"## {topic}")
        out.append(body)
    return "\n".join(out)


def render_progress(plan: dict) -> str:
    out = ["# Progress Log"]
    for p in plan.get("progress_log", []):
        ts = p.get("ts", "")
        phase = p.get("phase", "")
        action = p.get("action", "")
        files = p.get("files", []) or []
        out.append("")
        out.append(f"- {ts} (phase {phase}): {action}")
        if files:
            out.append("  - files: " + ", ".join(files))
    return "\n".join(out)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--single", action="store_true", help="single plan.md instead of three files")
    args = parser.parse_args(argv)

    plan_path = _resolve_plan_path()
    if plan_path is None:
        print("[export] no plan.html found", file=sys.stderr)
        return 1
    plan = _extract(plan_path)
    if plan is None:
        print("[export] plan-data JSON could not be parsed from plan.html", file=sys.stderr)
        return 2

    task_plan = render_task_plan(plan)
    findings = render_findings(plan)
    progress = render_progress(plan)

    if args.stdout or args.single:
        combined = "\n\n".join([task_plan, findings, progress])
        if args.stdout:
            print(combined)
        if args.single:
            Path("plan.md").write_text(combined + "\n", encoding="utf-8")
            print("[export] wrote plan.md")
        return 0

    Path("task_plan.md").write_text(task_plan + "\n", encoding="utf-8")
    Path("findings.md").write_text(findings + "\n", encoding="utf-8")
    Path("progress.md").write_text(progress + "\n", encoding="utf-8")
    print("[export] wrote task_plan.md, findings.md, progress.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
