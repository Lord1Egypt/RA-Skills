#!/usr/bin/env python3
"""创建新任务"""
import json
import os
import sys
from datetime import datetime

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
INDEX_FILE = os.path.join(TASKS_DIR, "tasks.json")

def get_next_id():
    """生成下一个任务ID：MMDD-N"""
    today = datetime.now().strftime("%m%d")
    
    if not os.path.exists(INDEX_FILE):
        return f"{today}-1"
    
    with open(INDEX_FILE, "r") as f:
        tasks = json.load(f)
    
    # 找今天最大的序号
    max_num = 0
    for task_id in tasks.keys():
        if task_id.startswith(today):
            try:
                num = int(task_id.split("-")[1])
                max_num = max(max_num, num)
            except:
                pass
    
    return f"{today}-{max_num + 1}"

def create_task(name):
    """创建新任务"""
    os.makedirs(TASKS_DIR, exist_ok=True)
    
    task_id = get_next_id()
    task_dir = os.path.join(TASKS_DIR, task_id + name.replace("/", "-"))
    os.makedirs(task_dir, exist_ok=True)
    os.makedirs(os.path.join(task_dir, "input"), exist_ok=True)
    os.makedirs(os.path.join(task_dir, "output"), exist_ok=True)
    
    meta = {
        "id": task_id,
        "name": name,
        "status": "进行中",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    
    with open(os.path.join(task_dir, "meta.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    # 更新索引
    tasks = {}
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            tasks = json.load(f)
    
    tasks[task_id] = {
        "name": name,
        "dir": task_id + name.replace("/", "-"),
        "status": "进行中",
        "created": meta["created"]
    }
    
    with open(INDEX_FILE, "w") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    return task_id, task_dir

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "未命名任务"
    task_id, task_dir = create_task(name)
    print(f"✅ 已创建窗口 {task_id}（{name}）")
    print(f"📁 目录: {task_dir}")
