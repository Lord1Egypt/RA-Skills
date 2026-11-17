#!/usr/bin/env python3
"""Drop a safe queue task for the local army."""
from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import ollama_daemon as od

HERE = Path(__file__).resolve().parent
TASKS = HERE / "ollama_command_center" / "tasks"
QUEUE = HERE / "ollama_queue"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", required=True, choices=sorted(od.SAFE_ROLES))
    ap.add_argument("--prompt", default="Say ready.")
    ap.add_argument("--id", default="")
    args = ap.parse_args()
    tid = args.id or f"task-{uuid.uuid4().hex[:10]}"
    body = {
        "id": tid,
        "role": args.role,
        "payload": {"prompt": args.prompt},
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    TASKS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    text = json.dumps(body, indent=2) + "\n"
    (TASKS / f"{tid}.task.json").write_text(text, encoding="utf-8")
    (QUEUE / f"{tid}.task.json").write_text(text, encoding="utf-8")
    print(json.dumps({"ok": True, "id": tid, "role": args.role, "path": str(TASKS / f"{tid}.task.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
