#!/usr/bin/env python3
"""
习惯养成教练 — 工具脚本
功能: track, review, plan

用法:
    python3 habit_coach_tool.py track [args]    # 习惯打卡
    python3 habit_coach_tool.py review [args]    # 进度回顾
    python3 habit_coach_tool.py plan [args]    # 制定计划
"""

import sys, json, os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
REF_URLS = ["https://jamesclear.com/atomic-habits", "https://github.com/hesamsheikh/awesome-openclaw-usecases", "https://www.reddit.com/r/productivity/comments/ai_habit_tracker/"]

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_data():
    data_file = os.path.join(DATA_DIR, "habit_coach_data.json")
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "created": datetime.now().isoformat(), "tool": "habit-coach"}

def save_data(data):
    ensure_data_dir()
    data_file = os.path.join(DATA_DIR, "habit_coach_data.json")
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def track(args):
    """习惯打卡"""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "track",
        "input": " ".join(args) if args else "",
        "status": "completed"
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "track",
        "message": "track完成",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3]
    }


def review(args):
    """进度回顾"""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "review",
        "input": " ".join(args) if args else "",
        "status": "completed"
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "review",
        "message": "review完成",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3]
    }


def plan(args):
    """制定计划"""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "plan",
        "input": " ".join(args) if args else "",
        "status": "completed"
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "plan",
        "message": "plan完成",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3]
    }


def main():
    cmds = ["track", "review", "plan"]
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(json.dumps({
            "error": f"用法: habit_coach_tool.py <{','.join(cmds)}> [args]",
            "available_commands": {"track": "习惯打卡", "review": "进度回顾", "plan": "制定计划"},
            "tool": "habit-coach",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    result = globals()[cmd](args)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

if __name__ == "__main__":
    main()
