#!/usr/bin/env python3
"""保存工作摘要到窗口"""
import json
import os
import sys
from datetime import datetime

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
CURRENT_FILE = os.path.join(TASKS_DIR, "current.json")

def get_current_window():
    """获取当前窗口"""
    if not os.path.exists(CURRENT_FILE):
        return None
    with open(CURRENT_FILE, "r") as f:
        return json.load(f)

def save_summary(summary_text):
    """保存工作摘要"""
    current = get_current_window()
    if not current:
        return False, "当前不在任何窗口中，请先切换到窗口"
    
    task_id = current.get("task_id", "")
    name = current.get("name", "")
    
    if not task_id:
        return False, "当前不在任何窗口中"
    
    # 获取窗口目录
    task_dir = os.path.join(TASKS_DIR, current.get("dir", ""))
    if not os.path.exists(task_dir):
        return False, f"窗口目录不存在: {task_dir}"
    
    # 保存到 summary.md
    summary_file = os.path.join(task_dir, "summary.md")
    
    content = []
    content.append("# 工作摘要")
    content.append("")
    content.append(f"## {datetime.now().strftime('%Y-%m-%d')}")
    content.append("")
    content.append(summary_text)
    content.append("")
    content.append(f"\n*最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    with open(summary_file, "w") as f:
        f.write("\n".join(content))
    
    # 同时更新 meta.json
    meta_file = os.path.join(task_dir, "meta.json")
    if os.path.exists(meta_file):
        with open(meta_file, "r") as f:
            meta = json.load(f)
        meta["summary"] = summary_text
        meta["updated"] = datetime.now().isoformat()
        with open(meta_file, "w") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    
    return True, task_id

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: save_summary.py <摘要内容>")
        sys.exit(1)
    
    summary = sys.argv[1]
    success, msg = save_summary(summary)
    if success:
        print(f"✅ 已保存工作摘要到窗口 {msg}")
    else:
        print(f"❌ {msg}")
