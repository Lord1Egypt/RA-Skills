#!/usr/bin/env python3
"""完成窗口"""
import json
import os
import sys
from datetime import datetime

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
INDEX_FILE = os.path.join(TASKS_DIR, "tasks.json")

def complete_task(task_id, status="已完成"):
    """标记窗口完成"""
    if not os.path.exists(INDEX_FILE):
        return False, "暂无窗口"
    
    with open(INDEX_FILE, "r") as f:
        tasks = json.load(f)
    
    if task_id not in tasks:
        return False, f"窗口 {task_id} 不存在"
    
    # 更新索引
    tasks[task_id]["status"] = status
    tasks[task_id]["completed"] = datetime.now().isoformat()
    
    with open(INDEX_FILE, "w") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    # 更新 meta.json
    task_dir = os.path.join(TASKS_DIR, tasks[task_id].get("dir", ""))
    meta_file = os.path.join(task_dir, "meta.json")
    if os.path.exists(meta_file):
        with open(meta_file, "r") as f:
            meta = json.load(f)
        meta["status"] = status
        meta["completed"] = datetime.now().isoformat()
        with open(meta_file, "w") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    
    return True, f"窗口 {task_id} 已标记为 {status}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: complete.py <窗口ID>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    success, msg = complete_task(task_id)
    if success:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")
