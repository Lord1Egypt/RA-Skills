#!/usr/bin/env python3
"""
MBTI Guru - 会话管理模块
支持测试进度保存和恢复
"""

import os
import json
import time
from datetime import datetime
from typing import Optional, Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sessions")

def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)

def save_session(chat_id: int, version: int, current_index: int, answers: List[tuple], questions_total: int) -> str:
    """
    保存测试进度
    
    Args:
        chat_id: 用户ID
        version: 测试版本(70/93/144/200)
        current_index: 当前题目索引(从1开始)
        answers: 已完成的答案 [(question_id, choice), ...]
        questions_total: 总题数
    
    Returns:
        session_id: 会话ID，用于恢复
    """
    ensure_data_dir()
    
    timestamp = int(time.time())
    session_id = f"{chat_id}_{timestamp}"
    
    session_data = {
        "session_id": session_id,
        "chat_id": chat_id,
        "version": version,
        "current_index": current_index,
        "answers": answers,
        "questions_total": questions_total,
        "timestamp": timestamp,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    return session_id

def load_session(session_id: str) -> Optional[Dict]:
    """
    加载会话数据
    
    Args:
        session_id: 会话ID
    
    Returns:
        session数据或None
    """
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_incomplete_session(chat_id: int) -> Optional[Dict]:
    """
    获取用户未完成的会话
    
    Args:
        chat_id: 用户ID
    
    Returns:
        最新的未完成会话或None
    """
    ensure_data_dir()
    
    sessions = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json') and filename.startswith(str(chat_id)):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                session = json.load(f)
                sessions.append(session)
    
    if not sessions:
        return None
    
    # 返回最新的未完成会话
    sessions.sort(key=lambda x: x['timestamp'], reverse=True)
    latest = sessions[0]
    
    # 检查是否真的未完成
    if latest['current_index'] < latest['questions_total']:
        return latest
    
    return None

def delete_session(session_id: str) -> bool:
    """
    删除会话
    
    Args:
        session_id: 会话ID
    
    Returns:
        是否删除成功
    """
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def list_user_sessions(chat_id: int, include_complete: bool = False) -> List[Dict]:
    """
    列出用户的所有会话
    
    Args:
        chat_id: 用户ID
        include_complete: 是否包含已完成的
    
    Returns:
        会话列表
    """
    ensure_data_dir()
    
    sessions = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json') and filename.startswith(str(chat_id)):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                session = json.load(f)
                if include_complete or session['current_index'] < session['questions_total']:
                    sessions.append(session)
    
    sessions.sort(key=lambda x: x['timestamp'], reverse=True)
    return sessions
