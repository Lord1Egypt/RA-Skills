#!/usr/bin/env python3
"""
OpenCode 主 Session 管理和监控工具
用于管理多个主session并自动监控进度
"""

import json
import sys
from datetime import datetime

# 主session配置存储
MAIN_SESSIONS_FILE = "/root/.openclaw/workspace/opencode-sessions.json"

def load_main_sessions():
    """加载主session列表"""
    try:
        with open(MAIN_SESSIONS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_main_sessions(sessions):
    """保存主session列表"""
    with open(MAIN_SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

def add_main_session(short_name, endpoint, session_id, task):
    """添加主session"""
    sessions = load_main_sessions()
    sessions[short_name] = {
        "endpoint": endpoint,
        "session_id": session_id,
        "task": task,
        "created_at": datetime.now().isoformat(),
        "monitoring": False
    }
    save_main_sessions(sessions)
    print(f"✅ 已添加主session: {short_name}")

def list_main_sessions():
    """列出所有主session"""
    sessions = load_main_sessions()
    if not sessions:
        print("暂无主session")
        return
    
    print("\n📋 主 Session 列表:")
    print("-" * 80)
    for short_name, info in sessions.items():
        status = "🔄 监控中" if info.get("monitoring") else "⏸️ 未监控"
        print(f"\n{short_name}:")
        print(f"  Endpoint: {info['endpoint']}")
        print(f"  Session: {info['session_id']}")
        print(f"  Task: {info['task']}")
        print(f"  Status: {status}")

def mark_monitoring(short_name, monitoring=True):
    """标记session监控状态"""
    sessions = load_main_sessions()
    if short_name in sessions:
        sessions[short_name]["monitoring"] = monitoring
        save_main_sessions(sessions)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 main_session_manager.py add <短名> <endpoint> <session_id> <任务>")
        print("  python3 main_session_manager.py list")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add" and len(sys.argv) == 6:
        add_main_session(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "list":
        list_main_sessions()
    else:
        print("未知命令")
