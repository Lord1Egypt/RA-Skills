#!/usr/bin/env python3
"""
保存当前对话为新窗口
功能：
1. 获取当前 session 的对话历史
2. 创建新窗口
3. 保存对话到窗口的 output/context.md
4. 切换到新窗口
"""
import json
import os
import sys
import uuid
from datetime import datetime

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
INDEX_FILE = os.path.join(TASKS_DIR, "tasks.json")
CURRENT_FILE = os.path.join(TASKS_DIR, "current.json")

def get_current_session_key():
    """获取当前 session key"""
    # 从 current.json 获取当前 session 信息
    if os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, "r") as f:
            current = json.load(f)
            return current.get("session_key")
    return None

def get_next_id():
    """生成下一个窗口ID：MMDD-N"""
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

def create_window(name):
    """创建新窗口"""
    os.makedirs(TASKS_DIR, exist_ok=True)
    
    window_id = get_next_id()
    window_dir = os.path.join(TASKS_DIR, window_id + name.replace("/", "-"))
    os.makedirs(window_dir, exist_ok=True)
    os.makedirs(os.path.join(window_dir, "input"), exist_ok=True)
    os.makedirs(os.path.join(window_dir, "output"), exist_ok=True)
    
    session_key = f"window:{window_id}:{uuid.uuid4().hex[:8]}"
    
    meta = {
        "id": window_id,
        "name": name,
        "status": "进行中",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "session_key": session_key,
        "source": "从对话保存"
    }
    
    with open(os.path.join(window_dir, "meta.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    # 更新索引
    tasks = {}
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            tasks = json.load(f)
    
    tasks[window_id] = {
        "name": name,
        "dir": window_id + name.replace("/", "-"),
        "status": "进行中",
        "created": meta["created"],
        "session_key": session_key
    }
    
    with open(INDEX_FILE, "w") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    return window_id, window_dir, session_key

def save_context_to_window(window_id, window_dir, context_content):
    """保存对话上下文到窗口"""
    context_file = os.path.join(window_dir, "output", "context.md")
    
    content = []
    content.append(f"# 窗口上下文 - {window_id}")
    content.append(f"\n保存时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"来源：从临时对话保存")
    content.append("\n---\n")
    content.append(context_content)
    
    with open(context_file, "w") as f:
        f.write("\n".join(content))
    
    return context_file

def switch_to_window(window_id, name):
    """切换到新窗口"""
    current = {
        "task_id": window_id,
        "name": name,
        "dir": window_id + name.replace("/", "-"),
        "switched": datetime.now().isoformat(),
        "session_key": f"window:{window_id}:{uuid.uuid4().hex[:8]}"
    }
    
    with open(CURRENT_FILE, "w") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    
    return True

if __name__ == "__main__":
    # 模拟获取对话内容（实际使用时由 agent 传入）
    context = sys.argv[1] if len(sys.argv) > 1 else "未命名对话"
    name = sys.argv[2] if len(sys.argv) > 2 else "从对话保存"
    
    # 创建窗口
    window_id, window_dir, session_key = create_window(name)
    
    # 保存上下文
    context_file = save_context_to_window(window_id, window_dir, context)
    
    # 切换到新窗口
    switch_to_window(window_id, name)
    
    print(f"✅ 已创建窗口 {window_id}（{name}）")
    print(f"📁 目录: {window_dir}")
    print(f"💾 已保存对话上下文到: {context_file}")
    print(f"🔄 已自动切换到新窗口")
