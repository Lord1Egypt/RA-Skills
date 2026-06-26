#!/usr/bin/env python3
"""显示/切换当前窗口"""
import json
import os
import sys
from datetime import datetime

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
CURRENT_FILE = os.path.join(TASKS_DIR, "current.json")

def get_current():
    """获取当前窗口"""
    if not os.path.exists(CURRENT_FILE):
        return None
    
    with open(CURRENT_FILE, "r") as f:
        return json.load(f)

def set_current(task_id):
    """设置当前窗口"""
    os.makedirs(TASKS_DIR, exist_ok=True)
    
    index_file = os.path.join(TASKS_DIR, "tasks.json")
    if not os.path.exists(index_file):
        return False, "窗口不存在"
    
    with open(index_file, "r") as f:
        tasks = json.load(f)
    
    if task_id not in tasks:
        return False, f"窗口 {task_id} 不存在"
    
    task_info = tasks[task_id]
    current = {
        "task_id": task_id,
        "name": task_info.get("name", ""),
        "dir": task_info.get("dir", ""),
        "switched": datetime.now().isoformat()
    }
    
    with open(CURRENT_FILE, "w") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    
    return True, task_id

def show_current():
    """显示当前窗口"""
    current = get_current()
    if not current:
        return "🌙 当前在临时窗口（无窗口）"
    
    task_id = current.get("task_id", "")
    name = current.get("name", "")
    switched = current.get("switched", "")
    
    if switched:
        try:
            dt = datetime.fromisoformat(switched)
            switched = dt.strftime("%m-%d %H:%M")
        except:
            pass
    
    return f"📌 当前窗口：{task_id}（{name}）\n切换时间：{switched}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 切换窗口
        task_id = sys.argv[1]
        success, msg = set_current(task_id)
        if success:
            print(f"🔄 已切换到窗口 {msg}")
        else:
            print(f"❌ {msg}")
    else:
        # 显示当前
        print(show_current())
