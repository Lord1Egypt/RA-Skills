#!/usr/bin/env python3
"""追踪已推送的主题，避免短期重复"""

import json
import sys
import re
from pathlib import Path
from typing import List, Optional

HISTORY_FILE = Path("/root/.openclaw/workspace/memory/hourly-knowledge-history.json")
CONFIG_FILE = Path("/root/.openclaw/workspace/skills/hourly-knowledge/config.json")
MAX_HISTORY = 10


def load_history() -> List[str]:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []


def save_history(topics: List[str]) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(topics[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)


def load_config() -> dict:
    with open(CONFIG_FILE) as f:
        return json.load(f)


def get_recent_topics() -> List[str]:
    """获取最近推送的主题列表"""
    return load_history()


def add_topic(topic: str) -> None:
    """添加新主题到历史记录"""
    topics = load_history()
    topics.append(topic)
    save_history(topics)


def get_blocklist() -> List[str]:
    """获取需要避开的主题关键词"""
    return load_history()


def is_topic_blocked(topic: str, blocklist: List[str]) -> bool:
    """检查主题是否在 blocklist 中"""
    topic_lower = topic.lower()
    for blocked in blocklist:
        if blocked.lower() in topic_lower or topic_lower in blocked.lower():
            return True
    return False


def suggest_category() -> str:
    """随机选择一个分类"""
    categories = ["人文", "历史", "科技", "自然", "生活", "地理", "艺术"]
    import random
    return random.choice(categories)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "get"

    if cmd == "get":
        topics = get_recent_topics()
        print(json.dumps(topics, ensure_ascii=False, indent=2))
    elif cmd == "add" and len(sys.argv) > 2:
        add_topic(sys.argv[2])
        print(f"Added: {sys.argv[2]}")
    elif cmd == "blocklist":
        blocklist = get_blocklist()
        print(json.dumps(blocklist, ensure_ascii=False, indent=2))
    elif cmd == "config":
        print(json.dumps(load_config(), ensure_ascii=False, indent=2))
    else:
        print("Usage: track_topics.py [get|add <topic>|blocklist|config]")
