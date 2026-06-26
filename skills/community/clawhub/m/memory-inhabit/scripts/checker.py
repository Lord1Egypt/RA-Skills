#!/usr/bin/env python3
"""
Memory-Inhabit Proactive Checker — 判断是否该发主动消息

用法：
  python3 checker.py check     检查是否该发消息（返回 should_send + 消息内容）
  python3 checker.py mark      标记已发送
  python3 checker.py stats     查看今日统计
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

STATE_FILE = Path(__file__).parent.parent / ".mi_state.json"
STATS_FILE = Path(__file__).parent.parent / ".mi_stats.json"


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def load_stats():
    if STATS_FILE.exists():
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"today": None, "count": 0, "last_sent": None}


def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def is_quiet_hours(quiet_range):
    """检查是否在免打扰时段"""
    if not quiet_range or len(quiet_range) < 2:
        return False
    
    now = datetime.now()
    current_minutes = now.hour * 60 + now.minute
    
    start_h, start_m = map(int, quiet_range[0].split(":"))
    end_h, end_m = map(int, quiet_range[1].split(":"))
    start_minutes = start_h * 60 + start_m
    end_minutes = end_h * 60 + end_m
    
    # 跨夜的情况（如 23:00 - 09:00）
    if start_minutes > end_minutes:
        return current_minutes >= start_minutes or current_minutes < end_minutes
    else:
        return start_minutes <= current_minutes < end_minutes


def check():
    """检查是否应该发送主动消息"""
    state = load_state()
    if not state:
        print(json.dumps({"should_send": False, "reason": "no_persona_loaded"}))
        return
    
    if state.get("mode") != "companion":
        print(json.dumps({"should_send": False, "reason": "not_companion_mode"}))
        return
    
    proactive = state.get("proactive_config", {})
    
    # 检查免打扰
    quiet_hours = proactive.get("quiet_hours", [])
    if is_quiet_hours(quiet_hours):
        print(json.dumps({"should_send": False, "reason": "quiet_hours"}))
        return
    
    # 检查频率限制
    freq = proactive.get("frequency", {})
    daily_max = freq.get("daily_max", 3)
    min_interval_hours = freq.get("min_interval_hours", 4)
    
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 重置今日计数
    if stats.get("today") != today:
        stats = {"today": today, "count": 0, "last_sent": None}
    
    # 检查每日上限
    if stats["count"] >= daily_max:
        print(json.dumps({"should_send": False, "reason": "daily_max_reached", "count": stats["count"]}))
        return
    
    # 检查最小间隔
    if stats.get("last_sent"):
        last = datetime.fromisoformat(stats["last_sent"])
        elapsed = (datetime.now() - last).total_seconds() / 3600
        if elapsed < min_interval_hours:
            print(json.dumps({
                "should_send": False, 
                "reason": "min_interval_not_met",
                "elapsed_hours": round(elapsed, 1),
                "required_hours": min_interval_hours
            }))
            return
    
    # 可以发送
    templates = proactive.get("templates", {})
    voice_config = proactive.get("voice", {})
    
    print(json.dumps({
        "should_send": True,
        "today_count": stats["count"],
        "daily_max": daily_max,
        "voice_enabled": voice_config.get("enabled", False),
        "voice_probability": voice_config.get("probability", 0.3),
        "voice_name": voice_config.get("voice_name", "xiaoxiao"),
        "templates": templates,
    }, ensure_ascii=False))


def mark_sent():
    """标记已发送"""
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if stats.get("today") != today:
        stats = {"today": today, "count": 0, "last_sent": None}
    
    stats["count"] = stats.get("count", 0) + 1
    stats["last_sent"] = datetime.now().isoformat()
    
    save_stats(stats)
    print(json.dumps({"marked": True, "today_count": stats["count"]}, ensure_ascii=False))


def show_stats():
    """查看今日统计"""
    state = load_state()
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if stats.get("today") != today:
        stats = {"today": today, "count": 0, "last_sent": None}
    
    result = {
        "mode": state.get("mode") if state else "none",
        "persona": state.get("profile_name") if state else "none",
        "today": today,
        "sent_count": stats["count"],
        "last_sent": stats.get("last_sent"),
        "quiet_hours": state.get("proactive_config", {}).get("quiet_hours", []) if state else [],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("用法: python3 checker.py [check|mark|stats]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "check":
        check()
    elif cmd == "mark":
        mark_sent()
    elif cmd == "stats":
        show_stats()
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
