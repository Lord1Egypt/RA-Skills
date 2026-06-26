#!/usr/bin/env python3
"""Create a Proof Loop task artifact skeleton."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize .agent/tasks/<TASK_ID>/ proof artifacts")
    parser.add_argument("task_id", help="Task id, e.g. ui-language-fix")
    parser.add_argument("--title", default=None, help="Human title for the task statement")
    parser.add_argument("--root", default=".", help="Repository root to create artifacts in")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing task directory")
    return parser.parse_args()


def validate_task_id(task_id: str) -> None:
    if not TASK_ID_RE.match(task_id):
        raise SystemExit(
            "Invalid task id. Use 1-80 letters, numbers, dots, underscores, or hyphens; no slashes."
        )
    if task_id in {".", ".."} or task_id.startswith("."):
        raise SystemExit("Invalid task id. Do not use hidden or parent-directory names.")


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    validate_task_id(args.task_id)

    root = Path(args.root).resolve()
    task_dir = root / ".agent" / "tasks" / args.task_id
    if task_dir.exists() and any(task_dir.iterdir()) and not args.force:
        raise SystemExit(f"Task directory already exists: {task_dir}")
    task_dir.mkdir(parents=True, exist_ok=True)

    title = args.title or args.task_id.replace("-", " ").title()
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    write(
        task_dir / "spec.md",
        f"""# Task: {args.task_id}\n\n## Task Statement\n\n{title}\n\n## Acceptance Criteria\n\n**AC1:** [specific, testable condition]\n- Verify: [command, browser check, API call, or manual check]\n\n**AC2:** [specific, testable condition]\n- Verify: [command, browser check, API call, or manual check]\n\n## Constraints\n\n- [what must not break]\n\n## Non-Goals\n\n- [what is explicitly out of scope]\n\n## Verification Approach\n\n[how a fresh verifier should check each AC]\n""",
        args.force,
    )

    verdict = {
        "task_id": args.task_id,
        "phase": "spec-freeze",
        "agent": "unassigned",
        "timestamp": timestamp,
        "overall": "UNKNOWN",
        "criteria": [
            {"id": "AC1", "status": "UNKNOWN", "note": "Not verified yet."},
            {"id": "AC2", "status": "UNKNOWN", "note": "Not verified yet."},
        ],
    }
    write(task_dir / "verdict.json", json.dumps(verdict, indent=2) + "\n", args.force)
    write(task_dir / "problems.md", "# Problems - {0}\n\nNo verifier pass has run yet.\n".format(args.task_id), args.force)
    write(
        task_dir / "evidence.md",
        f"""# Evidence - {args.task_id}\n\n## Build Summary\n\n[what changed and why]\n\n## Checks Run\n\n- [ ] [command or check]\n\n## Notes\n\n[anything the verifier needs to know]\n""",
        args.force,
    )

    print(f"PROOF_LOOP_TASK_CREATED {task_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
