#!/usr/bin/env python3
"""
Live Task Pulse — CLI for real-time task tracking.

Usage:
  task_pulse.py create <name> <step1> [step2] ...   → prints taskId
  task_pulse.py next <taskId> [message]              → advance step
  task_pulse.py heartbeat <taskId> [message]         → update current step
  task_pulse.py done <taskId> [result]               → mark complete
  task_pulse.py error <taskId> <error_msg>           → mark failed
  task_pulse.py status [taskId]                      → query status
  task_pulse.py cleanup [--days N]                   → remove old completed tasks
"""

import json, sys, os, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

TASK_DIR = Path(os.environ.get(
    "TASK_PULSE_DIR",
    os.path.expanduser("~/.openclaw/workspace/tasks")
))
TZ = timezone(timedelta(hours=int(os.environ.get("TASK_PULSE_TZ", "8"))))
STALL_SECONDS = int(os.environ.get("TASK_PULSE_STALL", "180"))
CLEANUP_DAYS = 7


def now_iso():
    return datetime.now(TZ).isoformat()


def now_ts():
    return datetime.now(TZ)


def parse_iso(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def task_path(task_id):
    return TASK_DIR / f"{task_id}.json"


def find_task(task_id):
    """Find task file by exact match or prefix."""
    p = task_path(task_id)
    if p.exists():
        return p
    for f in sorted(TASK_DIR.glob("*.json")):
        if f.stem.startswith(task_id):
            return f
    return None


def load_task(task_id):
    p = find_task(task_id)
    if not p:
        print(f"Error: task '{task_id}' not found", file=sys.stderr)
        sys.exit(1)
    with open(p) as f:
        return json.load(f), p


def save_task(data, path):
    data["updatedAt"] = now_iso()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def safe_filename(name):
    return re.sub(r'[^\w\-]', '-', name).strip('-')[:60]


def progress_bar(done, total, width=10):
    filled = int(width * done / total) if total else 0
    return '█' * filled + '░' * (width - filled)


def format_duration(seconds):
    if seconds < 60:
        return f"{int(seconds)}s"
    if seconds < 3600:
        return f"{int(seconds // 60)}m{int(seconds % 60)}s"
    return f"{int(seconds // 3600)}h{int((seconds % 3600) // 60)}m"


# ─── Commands ───────────────────────────────────────────────

def cmd_create(args):
    if len(args) < 2:
        print("Usage: create <taskName> <step1> [step2] ...", file=sys.stderr)
        sys.exit(1)

    name, step_names = args[0], args[1:]
    ts = datetime.now(TZ).strftime("%Y%m%d-%H%M%S")
    task_id = f"{safe_filename(name)}-{ts}"

    steps = [{"name": s, "status": "pending"} for s in step_names]
    if steps:
        steps[0]["status"] = "running"
        steps[0]["startedAt"] = now_iso()

    task = {
        "taskId": task_id,
        "taskName": name,
        "status": "running",
        "startedAt": now_iso(),
        "updatedAt": now_iso(),
        "finishedAt": None,
        "steps": steps,
        "error": None,
        "result": None,
    }

    save_task(task, task_path(task_id))
    # Machine-readable output for scripting
    print(task_id)


def cmd_next(args):
    if not args:
        print("Usage: next <taskId> [message]", file=sys.stderr)
        sys.exit(1)

    task, path = load_task(args[0])
    msg = " ".join(args[1:]) if len(args) > 1 else None
    steps = task.get("steps", [])

    advanced = False
    for i, s in enumerate(steps):
        if s["status"] == "running":
            s["status"] = "done"
            s["finishedAt"] = now_iso()
            if msg:
                s["message"] = msg
            if i + 1 < len(steps):
                steps[i + 1]["status"] = "running"
                steps[i + 1]["startedAt"] = now_iso()
            advanced = True
            break

    if not advanced:
        print("Warning: no running step to advance", file=sys.stderr)

    save_task(task, path)

    done = sum(1 for s in steps if s["status"] == "done")
    total = len(steps)
    current = next((s["name"] for s in steps if s["status"] == "running"), "—")
    bar = progress_bar(done, total)
    print(f"[{done}/{total}] {bar} → {current}")


def cmd_heartbeat(args):
    if not args:
        print("Usage: heartbeat <taskId> [message]", file=sys.stderr)
        sys.exit(1)

    task, path = load_task(args[0])
    msg = " ".join(args[1:]) if len(args) > 1 else None

    if msg:
        for s in task.get("steps", []):
            if s["status"] == "running":
                s["message"] = msg
                break

    save_task(task, path)
    print("💓 ok")


def cmd_done(args):
    if not args:
        print("Usage: done <taskId> [result]", file=sys.stderr)
        sys.exit(1)

    task, path = load_task(args[0])
    result = " ".join(args[1:]) if len(args) > 1 else None

    task["status"] = "done"
    task["finishedAt"] = now_iso()
    if result:
        task["result"] = result

    for s in task.get("steps", []):
        if s["status"] == "running":
            s["status"] = "done"
            s["finishedAt"] = now_iso()

    save_task(task, path)

    started = parse_iso(task.get("startedAt", ""))
    duration = ""
    if started:
        duration = f" ({format_duration((now_ts() - started).total_seconds())})"
    print(f"✅ 完成{duration}")


def cmd_error(args):
    if len(args) < 2:
        print("Usage: error <taskId> <error_message>", file=sys.stderr)
        sys.exit(1)

    task, path = load_task(args[0])
    error_msg = " ".join(args[1:])

    task["status"] = "error"
    task["finishedAt"] = now_iso()
    task["error"] = error_msg

    for s in task.get("steps", []):
        if s["status"] == "running":
            s["status"] = "error"
            s["message"] = error_msg
            break

    save_task(task, path)
    print(f"❌ {error_msg}")


def cmd_status(args):
    task_id = args[0] if args else None

    if task_id:
        task, _ = load_task(task_id)
        print(json.dumps(task, ensure_ascii=False, indent=2))
        return

    if not TASK_DIR.exists():
        print("📭 没有任务")
        return

    files = sorted(TASK_DIR.glob("*.json"))
    if not files:
        print("📭 没有任务")
        return

    now = now_ts()
    counts = {"running": 0, "done": 0, "error": 0, "stalled": 0}

    for f in files:
        try:
            with open(f) as fh:
                t = json.load(fh)
        except Exception:
            continue

        status = t.get("status", "?")
        name = t.get("taskName", "?")
        steps = t.get("steps", [])
        done_steps = sum(1 for s in steps if s["status"] == "done")
        total = len(steps)
        current = next((s["name"] for s in steps if s["status"] == "running"), "—")
        current_msg = next(
            (s.get("message", "") for s in steps if s["status"] == "running"), ""
        )

        # Stall detection
        stalled = False
        updated = parse_iso(t.get("updatedAt", ""))
        if status == "running" and updated:
            elapsed = (now - updated).total_seconds()
            stalled = elapsed > STALL_SECONDS

        # Duration
        started = parse_iso(t.get("startedAt", ""))
        duration = ""
        if started:
            end = parse_iso(t.get("finishedAt", "")) or now
            duration = format_duration((end - started).total_seconds())

        # Icon
        if stalled:
            icon, label = "⚠️", "STALLED"
            counts["stalled"] += 1
        else:
            icons = {"running": ("🔄", "执行中"), "done": ("✅", "完成"), "error": ("❌", "失败")}
            icon, label = icons.get(status, ("❓", status))
            counts[status] = counts.get(status, 0) + 1

        bar = progress_bar(done_steps, total)
        print(f"{icon} {name} [{done_steps}/{total}] {bar} {label} ({duration})")
        if status == "running" or stalled:
            print(f"   当前: {current}", end="")
            if current_msg:
                print(f" — {current_msg}", end="")
            print()
        if status == "error" and t.get("error"):
            print(f"   错误: {t['error']}")

    print(f"\n📊 🔄{counts['running']} ⚠️{counts['stalled']} ✅{counts['done']} ❌{counts['error']}")


def cmd_cleanup(args):
    days = CLEANUP_DAYS
    for i, a in enumerate(args):
        if a == "--days" and i + 1 < len(args):
            days = int(args[i + 1])

    if not TASK_DIR.exists():
        return

    now = now_ts()
    cutoff = now - timedelta(days=days)
    cleaned = 0

    for f in TASK_DIR.glob("*.json"):
        try:
            with open(f) as fh:
                t = json.load(fh)
        except Exception:
            continue

        if t.get("status") not in ("done", "error"):
            continue

        finished = parse_iso(t.get("finishedAt") or t.get("updatedAt", ""))
        if finished and finished < cutoff:
            f.unlink()
            cleaned += 1

    print(f"🧹 清理 {cleaned} 个过期任务（>{days}天）")


# ─── Main ───────────────────────────────────────────────────

COMMANDS = {
    "create": cmd_create,
    "next": cmd_next,
    "heartbeat": cmd_heartbeat,
    "done": cmd_done,
    "error": cmd_error,
    "status": cmd_status,
    "cleanup": cmd_cleanup,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])
