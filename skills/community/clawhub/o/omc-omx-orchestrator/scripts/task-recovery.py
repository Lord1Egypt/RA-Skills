#!/usr/bin/env python3
from __future__ import annotations
"""
OMC/OMX Task Recovery & Status Tool.

Scans tasks directory to recover state after agent restart.
Can also be used to list/query tasks.

Usage:
    # Recovery: reconcile running tasks with actual process state
    python3 task-recovery.py recover

    # List all tasks
    python3 task-recovery.py list

    # Show one task detail
    python3 task-recovery.py show <task-id>

    # Clean up old completed/failed tasks (>7 days)
    python3 task-recovery.py cleanup [--days 7]
"""

import json
import os
import signal
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

TASKS_DIR = (
    Path(os.environ["HERMES_HOME"]) / "tasks"
    if os.environ.get("HERMES_HOME")
    else Path(os.environ["OPENCLAW_HOME"]) / "workspace" / "tasks"
    if os.environ.get("OPENCLAW_HOME")
    else Path.home() / ".openclaw" / "workspace" / "tasks"
)


def _task_dirs():
    """Yield all task directories containing task.json."""
    if not TASKS_DIR.exists():
        return
    for d in sorted(TASKS_DIR.iterdir()):
        task_json = d / "task.json"
        if d.is_dir() and task_json.exists():
            yield d, task_json


def _read_task(task_json_path: Path) -> "dict | None":
    try:
        return json.loads(task_json_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_task(task_json_path: Path, data: dict):
    """Atomic write to avoid corruption."""
    tmp = task_json_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.rename(task_json_path)


def _is_pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def recover():
    """Reconcile running tasks with actual process state."""
    updated = 0
    for task_dir, task_json in _task_dirs():
        task = _read_task(task_json)
        if not task or task.get("status") != "running":
            continue

        task_id = task["id"]
        pid = task.get("pid")
        exit_code_file = task_dir / "exit_code"

        # Check 1: exit_code file exists → process completed while agent was down
        if exit_code_file.exists():
            try:
                ec = int(exit_code_file.read_text().strip())
            except ValueError:
                ec = -1
            task["status"] = "completed" if ec == 0 else "failed"
            task["exit_code"] = ec
            task["completed_at"] = datetime.now().isoformat()
            _write_task(task_json, task)
            updated += 1
            print(f"  ✅ {task_id}: completed (exit_code={ec})")
            continue

        # Check 2: PID still alive → still running (detached)
        if pid and _is_pid_alive(pid):
            task["detached"] = True
            _write_task(task_json, task)
            print(f"  🔄 {task_id}: still running (pid={pid}, detached)")
            continue

        # Check 3: PID dead, no exit_code → interrupted/failed
        task["status"] = "failed"
        task["exit_code"] = -1
        task["completed_at"] = datetime.now().isoformat()
        task["failure_reason"] = "Agent restarted; process died without exit_code"
        _write_task(task_json, task)
        updated += 1
        print(f"  ❌ {task_id}: failed (process died, no exit_code)")

    print(f"\nRecovery done: {updated} tasks updated")
    return updated


def list_tasks(status_filter: str = None):
    """List all tasks, optionally filtered by status."""
    tasks = []
    for task_dir, task_json in _task_dirs():
        task = _read_task(task_json)
        if task:
            if status_filter and task.get("status") != status_filter:
                continue
            # Quick summary
            desc = task.get("description", "")[:50]
            engine = task.get("engine", "?")
            status = task.get("status", "?")
            started = task.get("started_at", "")[:16]
            tid = task.get("id", "?")
            ec = task.get("exit_code", "")
            ec_str = f" (exit={ec})" if ec is not None else ""
            tasks.append(f"  {status:10} {engine:4} {started}  {tid}{ec_str}")
            tasks.append(f"             {desc}")

    if not tasks:
        print("No tasks found.")
    else:
        print(f"{'STATUS':10} {'ENG':4} {'STARTED':16}  TASK ID")
        print("-" * 80)
        print("\n".join(tasks))


def show_task(task_id: str):
    """Show full detail for one task."""
    for task_dir, task_json in _task_dirs():
        task = _read_task(task_json)
        if task and (task.get("id") == task_id or task_dir.name == task_id):
            print(json.dumps(task, indent=2, ensure_ascii=False))
            # Show spec.md if exists
            spec_file = task_dir / "spec.md"
            if spec_file.exists():
                content = spec_file.read_text(encoding="utf-8")
                print(f"\n--- spec.md ---")
                print(content[:1000] if len(content) > 1000 else content)
            # Show result file if exists
            result_file = task_dir / task.get("result_file", "result.txt")
            if result_file.exists():
                content = result_file.read_text(encoding="utf-8")
                print(f"\n--- {result_file.name} (last 500 chars) ---")
                print(content[-500:] if len(content) > 500 else content)
            return
    print(f"Task not found: {task_id}")


def cleanup(days: int = 7):
    """Remove completed/failed tasks older than N days."""
    cutoff = time.time() - (days * 86400)
    removed = 0
    for task_dir, task_json in _task_dirs():
        task = _read_task(task_json)
        if not task:
            continue
        status = task.get("status")
        if status not in ("completed", "failed"):
            continue
        # Use completed_at or started_at for age check
        ts_str = task.get("completed_at") or task.get("started_at") or ""
        if not ts_str:
            continue
        try:
            ts = datetime.fromisoformat(ts_str).timestamp()
        except ValueError:
            continue
        if ts < cutoff:
            import shutil
            shutil.rmtree(task_dir)
            removed += 1
            print(f"  Removed: {task_dir.name} ({status})")
    print(f"Cleanup done: {removed} tasks removed (>{days} days)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "recover":
        recover()
    elif cmd == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: task-recovery.py show <task-id>")
            sys.exit(1)
        show_task(sys.argv[2])
    elif cmd == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "--days" else (
            int(sys.argv[3]) if len(sys.argv) > 3 else 7
        )
        cleanup(days)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
