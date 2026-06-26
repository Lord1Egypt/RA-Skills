#!/usr/bin/env python3
"""归档任务窗口"""
import json
import os
import sys

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
INDEX_FILE = os.path.join(TASKS_DIR, "tasks.json")
ARCHIVED_FILE = os.path.join(TASKS_DIR, "archived.json")

def load_tasks():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(INDEX_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def load_archived():
    if os.path.exists(ARCHIVED_FILE):
        with open(ARCHIVED_FILE, "r") as f:
            return json.load(f)
    return {}

def save_archived(archived):
    with open(ARCHIVED_FILE, "w") as f:
        json.dump(archived, f, indent=2)

def archive_task(task_id):
    tasks = load_tasks()
    
    if task_id not in tasks:
        print(f"❌ 任务 {task_id} 不存在")
        return False
    
    task = tasks.pop(task_id)
    task["archived_at"] = datetime.now().isoformat()
    
    archived = load_archived()
    archived[task_id] = task
    save_tasks(tasks)
    save_archived(archived)
    
    print(f"✅ 任务 {task_id} 已归档")
    return True

from datetime import datetime

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 archive.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    archive_task(task_id)
