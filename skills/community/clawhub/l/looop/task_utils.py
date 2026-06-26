"""Task Management Utility Functions"""
import json
import os
from datetime import datetime
from typing import Optional

# Task status constants
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETED = "completed"
STATUS_BLOCKED = "blocked"
STATUS_NEEDS_MANUAL = "needs_manual"


def init_looop_dir(src_dir: str) -> None:
    """Initialize src/.looop directory"""
    looop_dir = os.path.join(src_dir, ".looop")
    os.makedirs(looop_dir, exist_ok=True)


def load_tasks(tasks_file: str) -> dict:
    """Load task list from file"""
    if not os.path.exists(tasks_file):
        return {
            "project": "",
            "created_at": "",
            "docs_dir": "",
            "src_dir": "",
            "requirements_docs": [],
            "tasks": []
        }
    with open(tasks_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(data: dict, tasks_file: str) -> None:
    """Save task list to file"""
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_next_task(data: dict) -> Optional[dict]:
    """Intelligently select the next task to execute

    Selection logic:
    1. Filter tasks with pending status (exclude needs_manual)
    2. Exclude tasks with incomplete dependencies
    3. Sort by priority and select highest priority
    """
    pending_tasks = [t for t in data["tasks"]
                     if t["status"] == STATUS_PENDING]
    if not pending_tasks:
        return None

    completed_ids = {t["id"] for t in data["tasks"]
                     if t["status"] == STATUS_COMPLETED}
    eligible = []
    for task in pending_tasks:
        deps = task.get("dependencies", [])
        if all(d in completed_ids for d in deps):
            eligible.append(task)

    if not eligible:
        return None

    priority_order = {"high": 0, "medium": 1, "low": 2}
    eligible.sort(key=lambda t: priority_order.get(t.get("priority", "medium"), 1))
    return eligible[0]


def update_task_status(data: dict, task_id: int, status: str,
                       result: Optional[str] = None, issues: Optional[list] = None,
                       tasks_file: Optional[str] = None) -> None:
    """Update task status"""
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = status
            if result:
                task["result"] = result
            if issues:
                task["issues"] = issues
            if status == "completed":
                task["completed_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            break
    if tasks_file:
        save_tasks(data, tasks_file)


def get_task_summary(data: dict) -> dict:
    """Get task statistics"""
    total = len(data["tasks"])
    completed = sum(1 for t in data["tasks"] if t["status"] == STATUS_COMPLETED)
    pending = sum(1 for t in data["tasks"] if t["status"] == STATUS_PENDING)
    in_progress = sum(1 for t in data["tasks"] if t["status"] == STATUS_IN_PROGRESS)
    blocked = sum(1 for t in data["tasks"] if t["status"] == STATUS_BLOCKED)
    needs_manual = sum(1 for t in data["tasks"] if t["status"] == STATUS_NEEDS_MANUAL)
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress,
        "blocked": blocked,
        "needs_manual": needs_manual
    }


def mark_task_manual(data: dict, task_id: int, reason: Optional[str] = None,
                     tasks_file: Optional[str] = None) -> bool:
    """Mark task as needing manual intervention"""
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = STATUS_NEEDS_MANUAL
            if reason:
                task["manual_reason"] = reason
            if tasks_file:
                save_tasks(data, tasks_file)
            return True
    return False
