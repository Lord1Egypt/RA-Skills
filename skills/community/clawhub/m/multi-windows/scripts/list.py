#!/usr/bin/env python3
"""列出所有任务"""
import json
import os
from datetime import datetime

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
INDEX_FILE = os.path.join(TASKS_DIR, "tasks.json")

def list_tasks():
    if not os.path.exists(INDEX_FILE):
        return "暂无任务"
    
    with open(INDEX_FILE, "r") as f:
        tasks = json.load(f)
    
    if not tasks:
        return "暂无任务"
    
    # 按创建时间排序
    sorted_tasks = sorted(tasks.items(), key=lambda x: x[1].get("created", ""), reverse=True)
    
    lines = ["📋 窗口列表：", "", "| ID | 名称 | 状态 | 创建时间 |", "|---|---|---|---|"]
    for task_id, info in sorted_tasks:
        created = info.get("created", "")
        if created:
            try:
                dt = datetime.fromisoformat(created)
                created = dt.strftime("%m-%d %H:%M")
            except:
                pass
        lines.append(f"| {task_id} | {info.get('name', '-')} | {info.get('status', '-')} | {created} |")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(list_tasks())
