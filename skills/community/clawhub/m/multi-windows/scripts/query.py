#!/usr/bin/env python3
"""查询历史窗口"""
import json
import os
import re
import sys
from datetime import datetime, timedelta

TASKS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/tasks")
INDEX_FILE = os.path.join(TASKS_DIR, "tasks.json")

def parse_period(period_str):
    """解析时间段"""
    now = datetime.now()
    period_str = period_str.strip().lower()
    
    if "今天" in period_str:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif "昨天" in period_str:
        start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif "上周" in period_str:
        # 获取本周一
        today = now.date()
        start_of_week = today - timedelta(days=today.weekday())
        start = datetime.combine(start_of_week - timedelta(days=7), datetime.min.time())
        end = datetime.combine(start_of_week, datetime.min.time())
    elif "上周" in period_str or "last week" in period_str:
        start = now - timedelta(days=7)
        end = now
    elif "月" in period_str:
        # 解析 MMDD 格式
        match = re.search(r"(\d{2})(\d{2})", period_str)
        if match:
            month, day = int(match.group(1)), int(match.group(2))
            year = now.year
            start = datetime(year, month, day)
            end = start + timedelta(days=1)
            return start, end
    else:
        # 默认为今天
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    
    return start, end

def query_tasks(period_str="今天"):
    if not os.path.exists(INDEX_FILE):
        return "暂无窗口记录"
    
    with open(INDEX_FILE, "r") as f:
        tasks = json.load(f)
    
    start, end = parse_period(period_str)
    
    results = []
    for task_id, info in tasks.items():
        created = info.get("created", "")
        if created:
            try:
                dt = datetime.fromisoformat(created)
                if start <= dt <= end:
                    results.append((task_id, info, dt))
            except:
                pass
    
    if not results:
        return f"查询 \"{period_str}\" 期间没有窗口记录"
    
    # 按时间倒序
    results.sort(key=lambda x: x[2], reverse=True)
    
    lines = [f"📋 {period_str} 窗口列表：", "", "| ID | 名称 | 状态 |", "|---|---|---|"]
    for task_id, info, dt in results:
        lines.append(f"| {task_id} | {info.get('name', '-')} | {info.get('status', '-')} |")
    
    return "\n".join(lines)

if __name__ == "__main__":
    period = sys.argv[1] if len(sys.argv) > 1 else "今天"
    print(query_tasks(period))
