#!/usr/bin/env python3
"""
情緒溫度計模組
分析 EMOJI-JOURNAL.md 的情緒趨勢
"""

import os
import re
from datetime import datetime, timedelta

def read_emoji_journal():
    """讀取 EMOJI-JOURNAL.md"""
    workspace = os.path.expanduser("~/.openclaw/workspace-frontdesk")
    journal_path = os.path.join(workspace, "EMOJI-JOURNAL.md")
    
    if not os.path.exists(journal_path):
        return None
    
    with open(journal_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return content

def parse_emojis(content):
    """解析情緒 emoji"""
    # 匹配 emoji 符號
    emoji_pattern = re.compile(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+")
    
    emojis = emoji_pattern.findall(content)
    return emojis

def emoji_to_score(emoji):
    """將 emoji 轉換為情緒分數 (0~1)"""
    # 正面情緒
    positive = ["😊", "😄", "😁", "🥰", "😍", "🤩", "😎", "👍", "✨", "💡", "🔥", "💪", "🎉"]
    # 負面情緒
    negative = ["😢", "😭", "😞", "😔", "😟", "😕", "🙁", "☹️", "👎", "💔", "😭", "😫"]
    # 中性
    neutral = ["😐", "😶", "🤔", "👀", "🙂", "🙃"]
    
    if emoji in positive:
        return 0.8
    elif emoji in negative:
        return 0.2
    elif emoji in neutral:
        return 0.5
    else:
        return 0.5

def analyze_emotion_trend():
    """分析情緒趨勢"""
    content = read_emoji_journal()
    
    if not content:
        return {
            "today_score": 0.5,
            "yesterday_score": 0.5,
            "trend": "→",
            "message": "EMOJI-JOURNAL.md 不存在"
        }
    
    # 解析 emoji
    emojis = parse_emojis(content)
    
    if not emojis:
        return {
            "today_score": 0.5,
            "yesterday_score": 0.5,
            "trend": "→",
            "message": "未找到情緒記錄"
        }
    
    # 計算今日情緒分數（取最近 10 個 emoji 的平均）
    recent_emojis = emojis[-10:] if len(emojis) >= 10 else emojis
    today_score = sum(emoji_to_score(e) for e in recent_emojis) / len(recent_emojis)
    
    # 計算昨日情緒分數（取前 10 個 emoji 的平均）
    if len(emojis) >= 20:
        yesterday_emojis = emojis[-20:-10]
        yesterday_score = sum(emoji_to_score(e) for e in yesterday_emojis) / len(yesterday_emojis)
    else:
        yesterday_score = today_score
    
    # 判斷趨勢
    diff = today_score - yesterday_score
    if diff > 0.05:
        trend = "↗"
    elif diff < -0.05:
        trend = "↘"
    else:
        trend = "→"
    
    return {
        "today_score": round(today_score, 2),
        "yesterday_score": round(yesterday_score, 2),
        "trend": trend,
        "recent_emojis": recent_emojis[-5:] if len(recent_emojis) >= 5 else recent_emojis
    }

if __name__ == "__main__":
    import json
    print(json.dumps(analyze_emotion_trend(), indent=2, ensure_ascii=False))
