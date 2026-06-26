"""Task storage with file locking for persistence."""
import fcntl
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from utils.storage import build_customer_dir


def _get_tasks_path(customer_id: str) -> str:
    """Get path to tasks JSON file."""
    return os.path.expanduser(Path(build_customer_dir(customer_id)) / "tasks.json")


def read_tasks(customer_id: str) -> List[Dict[str, Any]]:
    """Read all tasks for a customer with file locking."""
    path = _get_tasks_path(customer_id)
    
    if not os.path.exists(path):
        return []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            # Acquire shared lock for reading
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except (json.JSONDecodeError, Exception):
        return []


def write_tasks(customer_id: str, tasks: List[Dict[str, Any]]) -> bool:
    """Write tasks with exclusive file locking."""
    path = _get_tasks_path(customer_id)
    
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            # Acquire exclusive lock for writing
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        return True
    except Exception:
        return False


def add_task(customer_id: str, task: Dict[str, Any]) -> bool:
    """Add a single task to storage."""
    tasks = read_tasks(customer_id)
    tasks.append(task)
    return write_tasks(customer_id, tasks)


def add_tasks(customer_id: str, new_tasks: List[Dict[str, Any]]) -> bool:
    """Add multiple tasks to storage."""
    tasks = read_tasks(customer_id)
    tasks.extend(new_tasks)
    return write_tasks(customer_id, tasks)


def get_task(customer_id: str, task_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific task by ID."""
    tasks = read_tasks(customer_id)
    for task in tasks:
        if task.get("task_id") == task_id:
            return task
    return None


def update_task(customer_id: str, task_id: str, updates: Dict[str, Any]) -> bool:
    """Update a specific task."""
    tasks = read_tasks(customer_id)
    for task in tasks:
        if task.get("task_id") == task_id:
            task.update(updates)
            return write_tasks(customer_id, tasks)
    return False


def delete_task(customer_id: str, task_id: str) -> bool:
    """Delete a specific task."""
    tasks = read_tasks(customer_id)
    original_len = len(tasks)
    tasks = [t for t in tasks if t.get("task_id") != task_id]
    if len(tasks) == original_len:
        return False
    return write_tasks(customer_id, tasks)


def list_tasks(customer_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List tasks, optionally filtered by status."""
    tasks = read_tasks(customer_id)
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    return tasks
