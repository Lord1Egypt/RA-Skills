#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

MEMORY_TEMPLATE = """# MEMORY.md\n\n## Identity\n\n- Assistant name:\n- User preferred form of address:\n\n## Communication Preferences\n\n- \n\n## Tool / Workflow Preferences\n\n- \n\n## Active Projects\n\n- \n\n## Recurring Tasks / Cron\n\n- \n"""

INBOX_TEMPLATE = """# inbox\n\n> New facts, preferences, decisions, todos, and project state go here first.\n> The hourly cron job compresses pending items into `memory/YYYY-MM-DD-raw.md`.\n\n## pending\n"""

SYSTEM_MEMORY_PIPELINE_TEMPLATE = """# Memory pipeline\n\nThis workspace uses a curated memory workflow:\n\nconversation -> memory/inbox.md -> memory/YYYY-MM-DD-raw.md -> memory/YYYY-MM-DD.md -> MEMORY.md\n\nDefault mode:\n- concise / curated memory\n- store preferences, decisions, todos, project state, lessons learned\n- avoid full transcript dumping unless explicitly requested\n"""


def ensure_dir(path: Path, created: list[str]) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        created.append(f"dir  {path}")


def ensure_file(path: Path, content: str, created: list[str], skipped: list[str]) -> None:
    if path.exists():
        skipped.append(f"keep {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(f"file {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Markdown memory pipeline structure.")
    parser.add_argument("--workspace", default=".", help="Workspace root (default: current directory)")
    parser.add_argument("--force-system-note", action="store_true", help="Create memory/system/memory-pipeline.md even if optional")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    memory_dir = workspace / "memory"

    created: list[str] = []
    skipped: list[str] = []

    ensure_dir(memory_dir, created)
    ensure_dir(memory_dir / "projects", created)
    ensure_dir(memory_dir / "system", created)
    ensure_dir(memory_dir / "groups", created)
    ensure_dir(memory_dir / "logs", created)

    ensure_file(workspace / "MEMORY.md", MEMORY_TEMPLATE, created, skipped)
    ensure_file(memory_dir / "inbox.md", INBOX_TEMPLATE, created, skipped)

    if args.force_system_note:
        ensure_file(memory_dir / "system" / "memory-pipeline.md", SYSTEM_MEMORY_PIPELINE_TEMPLATE, created, skipped)

    print(f"workspace: {workspace}")
    print()
    if created:
        print("created:")
        for item in created:
            print(f"  - {item}")
    else:
        print("created:\n  - nothing")

    print()
    if skipped:
        print("kept existing:")
        for item in skipped:
            print(f"  - {item}")
    else:
        print("kept existing:\n  - nothing")

    print()
    print("next steps:")
    print("  1. Define memory capture rules")
    print("  2. Install hourly, daily, and weekly cron jobs")
    print("  3. Run verify_memory_pipeline.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
