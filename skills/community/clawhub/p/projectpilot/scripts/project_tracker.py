#!/usr/bin/env python3
"""
ProjectPilot — lightweight project/task tracker for OpenClaw agents.
Stores data as JSON in the workspace. No dependencies beyond stdlib.

Usage:
  python3 project_tracker.py <command> [args]

Commands:
  init <project>                    Create a new project
  add <project> <task> [--priority H|M|L] [--due YYYY-MM-DD] [--assignee name]
  list <project> [--status todo|doing|done] [--priority H|M|L]
  update <project> <task_id> [--status todo|doing|done] [--priority H|M|L] [--due YYYY-MM-DD]
  done <project> <task_id>          Mark task as done
  delete <project> <task_id>        Remove a task
  summary <project>                 Print project summary with stats
  projects                          List all projects
  overdue <project>                 Show overdue tasks
  burndown <project>                Show completion progress
"""

import json
import sys
import os
import re
from datetime import datetime, date
from pathlib import Path
from uuid import uuid4

DATA_DIR = Path(os.environ.get("PROJECTPILOT_DATA", Path.home() / ".openclaw/workspace/data/projects"))

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_name(name):
    """Sanitize project name to prevent path traversal. Only allow safe characters."""
    # Strip leading/trailing whitespace and path separators
    name = name.strip().strip("/\\")
    # Only allow alphanumeric, hyphens, underscores, and dots
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '-', name)
    # Collapse multiple separators
    sanitized = re.sub(r'[-.]{2,}', '-', sanitized)
    # Reject empty or hidden names
    if not sanitized or sanitized.startswith('.'):
        print("Error: Invalid project name. Use only letters, numbers, hyphens, and underscores.")
        sys.exit(1)
    return sanitized

def project_path(name):
    """Return safe path for project data. Validates name stays within DATA_DIR."""
    name = sanitize_name(name)
    p = (DATA_DIR / f"{name}.json").resolve()
    # Ensure resolved path is still inside DATA_DIR (path traversal guard)
    if not str(p).startswith(str(DATA_DIR.resolve())):
        print("Error: Invalid project name.")
        sys.exit(1)
    return p

def load_project(name):
    p = project_path(name)
    if not p.exists():
        print(f"Error: Project '{name}' not found. Create it with: init {name}")
        sys.exit(1)
    return json.loads(p.read_text())

def save_project(name, data):
    ensure_data_dir()
    project_path(name).write_text(json.dumps(data, indent=2, default=str))

def new_task_id():
    return uuid4().hex[:6]

def cmd_init(name):
    if project_path(name).exists():
        print(f"Project '{name}' already exists.")
        sys.exit(1)
    data = {
        "name": name,
        "created": datetime.now().isoformat(),
        "tasks": []
    }
    save_project(name, data)
    print(f"✅ Project '{name}' created.")

def cmd_add(name, task_text, priority="M", due=None, assignee=None):
    data = load_project(name)
    task = {
        "id": new_task_id(),
        "task": task_text,
        "status": "todo",
        "priority": priority.upper(),
        "due": due,
        "assignee": assignee,
        "created": datetime.now().isoformat(),
        "completed": None
    }
    data["tasks"].append(task)
    save_project(name, data)
    print(f"✅ Added [{task['id']}] {task_text} (priority: {priority}, due: {due or 'none'})")

def cmd_list(name, status_filter=None, priority_filter=None):
    data = load_project(name)
    tasks = data["tasks"]
    if status_filter:
        tasks = [t for t in tasks if t["status"] == status_filter]
    if priority_filter:
        tasks = [t for t in tasks if t["priority"] == priority_filter.upper()]
    if not tasks:
        print("No tasks found.")
        return
    priority_order = {"H": 0, "M": 1, "L": 2}
    tasks.sort(key=lambda t: (priority_order.get(t["priority"], 1), t.get("due") or "9999"))
    status_icon = {"todo": "⬜", "doing": "🔄", "done": "✅"}
    print(f"\n📋 {name} — {len(tasks)} task(s)\n")
    for t in tasks:
        icon = status_icon.get(t["status"], "❓")
        due_str = f" | due: {t['due']}" if t.get("due") else ""
        assignee = f" | @{t['assignee']}" if t.get("assignee") else ""
        print(f"  {icon} [{t['id']}] [{t['priority']}] {t['task']}{due_str}{assignee}")
    print()

def cmd_update(name, task_id, **kwargs):
    data = load_project(name)
    for t in data["tasks"]:
        if t["id"] == task_id:
            for k, v in kwargs.items():
                if v is not None:
                    t[k] = v
            if kwargs.get("status") == "done":
                t["completed"] = datetime.now().isoformat()
            save_project(name, data)
            print(f"✅ Updated [{task_id}]: {kwargs}")
            return
    print(f"Error: Task [{task_id}] not found.")
    sys.exit(1)

def cmd_done(name, task_id):
    cmd_update(name, task_id, status="done", completed=datetime.now().isoformat())

def cmd_delete(name, task_id):
    data = load_project(name)
    before = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    if len(data["tasks"]) == before:
        print(f"Error: Task [{task_id}] not found.")
        sys.exit(1)
    save_project(name, data)
    print(f"🗑️ Deleted [{task_id}].")

def cmd_summary(name):
    data = load_project(name)
    tasks = data["tasks"]
    total = len(tasks)
    todo = len([t for t in tasks if t["status"] == "todo"])
    doing = len([t for t in tasks if t["status"] == "doing"])
    done = len([t for t in tasks if t["status"] == "done"])
    high = len([t for t in tasks if t["priority"] == "H" and t["status"] != "done"])
    today = date.today().isoformat()
    overdue = len([t for t in tasks if t.get("due") and t["due"] < today and t["status"] != "done"])
    pct = round(done / total * 100) if total else 0

    print(f"\n📊 Project: {name}")
    print(f"   Created: {data.get('created', 'unknown')[:10]}")
    print(f"   Total tasks: {total}")
    print(f"   ⬜ Todo: {todo} | 🔄 Doing: {doing} | ✅ Done: {done}")
    print(f"   🔴 High priority (open): {high}")
    print(f"   ⚠️  Overdue: {overdue}")
    print(f"   Progress: {pct}% {'█' * (pct // 5)}{'░' * (20 - pct // 5)}")
    print()

def cmd_projects():
    ensure_data_dir()
    projects = sorted(DATA_DIR.glob("*.json"))
    if not projects:
        print("No projects found.")
        return
    print("\n📁 Projects:\n")
    for p in projects:
        data = json.loads(p.read_text())
        total = len(data["tasks"])
        done = len([t for t in data["tasks"] if t["status"] == "done"])
        print(f"  • {p.stem} ({done}/{total} done)")
    print()

def cmd_overdue(name):
    data = load_project(name)
    today = date.today().isoformat()
    overdue = [t for t in data["tasks"] if t.get("due") and t["due"] < today and t["status"] != "done"]
    if not overdue:
        print("No overdue tasks. 🎉")
        return
    print(f"\n⚠️  Overdue tasks in {name}:\n")
    for t in overdue:
        print(f"  🔴 [{t['id']}] [{t['priority']}] {t['task']} (due: {t['due']})")
    print()

def cmd_burndown(name):
    data = load_project(name)
    tasks = data["tasks"]
    total = len(tasks)
    if not total:
        print("No tasks to show.")
        return
    done = len([t for t in tasks if t["status"] == "done"])
    remaining = total - done
    bar_len = 30
    filled = int(done / total * bar_len)
    print(f"\n🔥 Burndown: {name}")
    print(f"   [{'█' * filled}{'░' * (bar_len - filled)}] {done}/{total} ({round(done/total*100)}%)")
    print(f"   Remaining: {remaining} tasks\n")

# --- CLI ---
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "projects":
        cmd_projects()
    elif cmd == "init" and len(sys.argv) >= 3:
        cmd_init(sys.argv[2])
    elif cmd == "add" and len(sys.argv) >= 4:
        name = sys.argv[2]
        task = sys.argv[3]
        kwargs = {}
        args = sys.argv[4:]
        i = 0
        while i < len(args):
            if args[i] == "--priority" and i + 1 < len(args):
                kwargs["priority"] = args[i + 1]; i += 2
            elif args[i] == "--due" and i + 1 < len(args):
                kwargs["due"] = args[i + 1]; i += 2
            elif args[i] == "--assignee" and i + 1 < len(args):
                kwargs["assignee"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_add(name, task, **kwargs)
    elif cmd == "list" and len(sys.argv) >= 3:
        name = sys.argv[2]
        kwargs = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--status" and i + 1 < len(args):
                kwargs["status_filter"] = args[i + 1]; i += 2
            elif args[i] == "--priority" and i + 1 < len(args):
                kwargs["priority_filter"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_list(name, **kwargs)
    elif cmd == "update" and len(sys.argv) >= 4:
        name = sys.argv[2]
        task_id = sys.argv[3]
        kwargs = {}
        args = sys.argv[4:]
        i = 0
        while i < len(args):
            if args[i] == "--status" and i + 1 < len(args):
                kwargs["status"] = args[i + 1]; i += 2
            elif args[i] == "--priority" and i + 1 < len(args):
                kwargs["priority"] = args[i + 1]; i += 2
            elif args[i] == "--due" and i + 1 < len(args):
                kwargs["due"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_update(name, task_id, **kwargs)
    elif cmd == "done" and len(sys.argv) >= 4:
        cmd_done(sys.argv[2], sys.argv[3])
    elif cmd == "delete" and len(sys.argv) >= 4:
        cmd_delete(sys.argv[2], sys.argv[3])
    elif cmd == "summary" and len(sys.argv) >= 3:
        cmd_summary(sys.argv[2])
    elif cmd == "overdue" and len(sys.argv) >= 3:
        cmd_overdue(sys.argv[2])
    elif cmd == "burndown" and len(sys.argv) >= 3:
        cmd_burndown(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
