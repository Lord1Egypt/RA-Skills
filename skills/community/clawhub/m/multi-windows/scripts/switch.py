#!/usr/bin/env python3
"""
窗口切换脚本 - 改进版
功能：
1. 切换窗口时自动保存当前 session 对话历史
2. 切换到新窗口时加载该窗口的历史上下文
3. 保持窗口间上下文隔离
"""
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
CURRENT_FILE = os.path.join(TASKS_DIR, "current.json")
INDEX_FILE = os.path.join(TASKS_DIR, "tasks.json")
SESSIONS_DIR = os.path.expanduser("~/.openclaw/agents/main/sessions")

def get_task_dir(task_id, name=""):
    """获取任务目录"""
    task_dir = os.path.join(TASKS_DIR, f"{task_id}{name.replace('/', '-')}")
    return task_dir

def get_meta(task_id, name=""):
    """获取窗口 meta.json"""
    task_dir = get_task_dir(task_id, name)
    meta_path = os.path.join(task_dir, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            return json.load(f)
    return None

def update_meta(task_id, name="", updates=None):
    """更新窗口 meta.json"""
    if updates is None:
        updates = {}
    task_dir = get_task_dir(task_id, name)
    os.makedirs(task_dir, exist_ok=True)
    meta_path = os.path.join(task_dir, "meta.json")
    
    meta = get_meta(task_id, name) or {"task_id": task_id, "name": name}
    meta.update(updates)
    meta["updated"] = datetime.now().isoformat()
    
    with open(meta_path, "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return meta

def get_current():
    """获取当前窗口"""
    if not os.path.exists(CURRENT_FILE):
        return None
    with open(CURRENT_FILE, "r") as f:
        return json.load(f)

def get_latest_session_path():
    """获取最新活跃的 session jsonl 文件"""
    if not os.path.exists(SESSIONS_DIR):
        return None
    
    sessions = []
    for f in os.listdir(SESSIONS_DIR):
        if f.endswith(".jsonl") and not f.endswith(".deleted") and not f.endswith(".reset"):
            path = os.path.join(SESSIONS_DIR, f)
            mtime = os.path.getmtime(path)
            sessions.append((mtime, path))
    
    if not sessions:
        return None
    
    # 返回最新的 session
    sessions.sort(reverse=True)
    return sessions[0][1]

def save_current_session_to_window(current):
    """保存当前 session 的对话历史到当前窗口目录"""
    if not current:
        return
    
    task_id = current.get("task_id", "")
    name = current.get("name", "")
    
    if not task_id:
        return
    
    task_dir = get_task_dir(task_id, name)
    output_dir = os.path.join(task_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取最新 session
    session_path = get_latest_session_path()
    if session_path:
        dest_path = os.path.join(output_dir, "transcript.jsonl")
        shutil.copy2(session_path, dest_path)
        print(f"💾 已保存当前对话到: {task_id}")
    else:
        print(f"⚠️ 未找到当前 session 文件")

def load_window_context(task_id, name=""):
    """加载窗口的历史对话上下文"""
    task_dir = get_task_dir(task_id, name)
    transcript_path = os.path.join(task_dir, "output", "transcript.jsonl")
    
    if not os.path.exists(transcript_path):
        return None
    
    # 读取并解析对话（只取 user 和 assistant 消息）
    messages = []
    try:
        with open(transcript_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    # 提取消息内容
                    if entry.get("type") == "message":
                        msg = entry.get("message", {})
                        role = msg.get("role")
                        content_list = msg.get("content", [])
                        if role in ["user", "assistant"] and content_list:
                            text = ""
                            for c in content_list:
                                if c.get("type") == "text":
                                    text += c.get("text", "")
                            if text:
                                messages.append(f"**{role}**: {text[:200]}")
                except:
                    pass
    except Exception as e:
        return None
    
    return messages[-10:] if len(messages) > 10 else messages  # 最近10条

def set_current(task_id, name=""):
    """设置当前窗口"""
    os.makedirs(TASKS_DIR, exist_ok=True)
    
    # 先保存当前窗口的上下文
    current = get_current()
    if current:
        save_current_session_to_window(current)
    
    # 检查窗口是否存在
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            tasks = json.load(f)
        if task_id in tasks:
            task_info = tasks[task_id]
            name = task_info.get("name", "")
    
    current = {
        "task_id": task_id,
        "name": name,
        "dir": f"{task_id}{name.replace('/', '-')}",
        "switched": datetime.now().isoformat()
    }
    
    with open(CURRENT_FILE, "w") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    
    return current

def switch_to(task_id):
    """切换到指定窗口"""
    # 获取窗口信息
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            tasks = json.load(f)
        if task_id in tasks:
            task_name = tasks[task_id].get("name", "")
    
    # 执行切换（自动保存当前和加载新窗口）
    set_current(task_id, task_name)
    
    # 加载新窗口的历史
    history = load_window_context(task_id, task_name)
    
    return task_id, task_name, history

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
        tid, name, history = switch_to(task_id)
        
        print(f"🔄 **已切换到窗口 {tid}（{name}）**\n")
        
        if history:
            print("📜 **历史对话：**\n")
            for msg in history:
                print(msg)
                print()
        else:
            print("（暂无历史对话）")
    else:
        current = get_current()
        if current:
            print(f"📌 当前窗口: {current.get('task_id')} ({current.get('name')})")
        else:
            print("🌙 当前在临时窗口")
