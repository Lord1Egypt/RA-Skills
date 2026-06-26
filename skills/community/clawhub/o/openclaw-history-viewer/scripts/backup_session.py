#!/usr/bin/env python3
"""
OpenClaw Session Backup Hook
备份当前会话到 ~/.openclaw/workspace/history/

用法:
    python3 backup_session.py [session_id]
    
如果未提供 session_id，会自动从 sessions.json 获取当前会话
"""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
SESSIONS_FILE = SESSIONS_DIR / "sessions.json"
BACKUP_DIR = Path.home() / ".openclaw" / "workspace" / "history"


def backup_current_session(session_id=None):
    """备份当前会话到 history 目录"""
    
    # 确保备份目录存在
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # 如果没有提供 session_id，从 sessions.json 获取
    if not session_id:
        if not SESSIONS_FILE.exists():
            print("❌ sessions.json 不存在")
            return False
        
        try:
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                sessions_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ 读取 sessions.json 失败：{e}")
            return False
        
        # 获取第一个会话的 ID
        for key, session in sessions_data.items():
            session_id = session.get("sessionId")
            if session_id:
                break
        
        if not session_id:
            print("❌ 未找到会话 ID")
            return False
    
    # 构建会话文件路径
    session_file = SESSIONS_DIR / f"{session_id}.jsonl"
    
    if not session_file.exists():
        print(f"❌ 会话文件不存在：{session_file}")
        return False
    
    # 构建备份文件路径
    backup_file = BACKUP_DIR / f"{session_id}.jsonl"
    
    # 如果备份文件已存在，添加时间戳
    if backup_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"{session_id}_{timestamp}.jsonl"
    
    try:
        # 复制文件
        shutil.copy2(session_file, backup_file)
        
        # 获取文件大小和行数
        file_size = backup_file.stat().st_size
        with open(backup_file, "r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)
        
        print(f"✅ 会话已备份")
        print(f"   Session ID: {session_id}")
        print(f"   备份文件：{backup_file}")
        print(f"   文件大小：{file_size:,} bytes")
        print(f"   消息数：{line_count}")
        
        # 创建/更新备份索引
        update_backup_index(session_id, backup_file, line_count, file_size)
        
        return True
        
    except Exception as e:
        print(f"❌ 备份失败：{e}")
        return False


def update_backup_index(session_id, backup_file, message_count, file_size):
    """更新备份索引文件"""
    index_file = BACKUP_DIR / "backup_index.json"
    
    # 加载现有索引
    if index_file.exists():
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                index = json.load(f)
        except json.JSONDecodeError:
            index = {"backups": {}}
    else:
        index = {"backups": {}}
    
    # 更新索引
    if session_id not in index["backups"]:
        index["backups"][session_id] = {
            "files": [],
            "total_backups": 0,
            "last_backup": None
        }
    
    backup_entry = {
        "file": str(backup_file),
        "filename": backup_file.name,
        "timestamp": datetime.now().isoformat(),
        "message_count": message_count,
        "file_size": file_size
    }
    
    index["backups"][session_id]["files"].append(backup_entry)
    index["backups"][session_id]["total_backups"] = len(index["backups"][session_id]["files"])
    index["backups"][session_id]["last_backup"] = backup_entry["timestamp"]
    
    # 保存索引
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    session_id = sys.argv[1] if len(sys.argv) > 1 else None
    success = backup_current_session(session_id)
    sys.exit(0 if success else 1)
