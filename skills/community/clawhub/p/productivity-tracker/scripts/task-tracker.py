#!/usr/bin/env python3
"""
Task Tracker - 任务管理与时间追踪工具
"""

import json
import os
import sys
import time
import threading
from datetime import datetime, date
from pathlib import Path

DATA_DIR = Path.home() / ".task-tracker"
TASKS_FILE = DATA_DIR / "tasks.json"
HABITS_FILE = DATA_DIR / "habits.json"
STATS_FILE = DATA_DIR / "stats.json"

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for f in [TASKS_FILE, HABITS_FILE, STATS_FILE]:
        if not f.exists():
            f.write_text("{}")

def load_json(path):
    """加载 JSON 文件"""
    try:
        return json.loads(path.read_text())
    except:
        return {}

def save_json(path, data):
    """保存 JSON 文件"""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def add_task(title):
    """添加新任务"""
    tasks = load_json(TASKS_FILE)
    task_id = max([int(k) for k in tasks.keys()] + [0]) + 1
    tasks[str(task_id)] = {
        "title": title,
        "completed": False,
        "created": datetime.now().isoformat(),
        "time_spent": 0
    }
    save_json(TASKS_FILE, tasks)
    print(f"{GREEN}✓ 任务已添加: {title}{RESET}")
    return task_id

def list_tasks():
    """列出所有任务"""
    tasks = load_json(TASKS_FILE)
    if not tasks:
        print(f"{YELLOW}暂无任务{RESET}")
        return
    
    print(f"\n{BOLD}📋 任务列表:{RESET}")
    print("-" * 50)
    pending = []
    completed = []
    
    for tid, task in tasks.items():
        if task["completed"]:
            completed.append((tid, task))
        else:
            pending.append((tid, task))
    
    for tid, task in pending:
        print(f"  [{BLUE}{tid}{RESET}] ⭕ {task['title']}")
    
    if completed:
        print()
        for tid, task in completed:
            print(f"  [{BLUE}{tid}{RESET}] ✅ {task['title']} (已完成)")
    print("-" * 50)

def complete_task(task_id):
    """标记任务完成"""
    tasks = load_json(TASKS_FILE)
    tid = str(task_id)
    if tid not in tasks:
        print(f"{RED}任务不存在{RESET}")
        return
    
    tasks[tid]["completed"] = True
    tasks[tid]["completed_at"] = datetime.now().isoformat()
    save_json(TASKS_FILE, tasks)
    print(f"{GREEN}✓ 任务已完成: {tasks[tid]['title']}{RESET}")

def delete_task(task_id):
    """删除任务"""
    tasks = load_json(TASKS_FILE)
    tid = str(task_id)
    if tid not in tasks:
        print(f"{RED}任务不存在{RESET}")
        return
    
    title = tasks[tid]["title"]
    del tasks[tid]
    save_json(TASKS_FILE, tasks)
    print(f"{GREEN}✓ 任务已删除: {title}{RESET}")

def pomodoro(duration=25):
    """番茄钟"""
    print(f"\n{BOLD}🍅 番茄钟 - {duration} 分钟{RESET}")
    print("按 Ctrl+C 停止\n")
    
    def countdown(mins):
        remaining = mins * 60
        while remaining > 0:
            m, s = divmod(remaining, 60)
            print(f"\r  {m:02d}:{s:02d} ", end="", flush=True)
            time.sleep(1)
            remaining -= 1
    
    try:
        countdown(duration)
        print(f"\n{GREEN}🎉 时间到！休息一下吧{RESET}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}番茄钟已停止{RESET}")

def add_habit(name):
    """添加习惯"""
    habits = load_json(HABITS_FILE)
    if name in habits:
        print(f"{YELLOW}习惯已存在: {name}{RESET}")
        return
    
    habits[name] = {
        "created": date.today().isoformat(),
        "streak": 0,
        "last_check": None
    }
    save_json(HABITS_FILE, habits)
    print(f"{GREEN}✓ 习惯已添加: {name}{RESET}")

def check_habit(name):
    """打卡习惯"""
    habits = load_json(HABITS_FILE)
    if name not in habits:
        print(f"{RED}习惯不存在: {name}{RESET}")
        return
    
    today = date.today().isoformat()
    habit = habits[name]
    
    if habit.get("last_check") == today:
        print(f"{YELLOW}今日已打卡: {name}{RESET}")
        return
    
    # 更新连续天数
    yesterday = (date.today() - __import__('datetime').timedelta(days=1)).isoformat()
    if habit.get("last_check") == yesterday:
        habit["streak"] += 1
    else:
        habit["streak"] = 1
    
    habit["last_check"] = today
    save_json(HABITS_FILE, habits)
    print(f"{GREEN}✓ 打卡成功！连续 {habit['streak']} 天: {name}{RESET}")

def list_habits():
    """列出习惯"""
    habits = load_json(HABITS_FILE)
    if not habits:
        print(f"{YELLOW}暂无习惯{RESET}")
        return
    
    print(f"\n{BOLD}🎯 习惯列表:{RESET}")
    print("-" * 50)
    today = date.today().isoformat()
    
    for name, habit in habits.items():
        checked = "✅" if habit.get("last_check") == today else "⭕"
        print(f"  {checked} {name} (连续 {habit.get('streak', 0)} 天)")
    print("-" * 50)

def daily_stats():
    """每日统计"""
    tasks = load_json(TASKS_FILE)
    habits = load_json(HABITS_FILE)
    
    today = date.today().isoformat()
    today_completed = [t for t in tasks.values() if t.get("completed_at", "").startswith(today)]
    
    print(f"\n{BOLD}📊 今日统计 ({today}):{RESET}")
    print("-" * 50)
    print(f"  完成任务: {len(today_completed)} / {len([t for t in tasks.values() if not t['completed']])}")
    
    today_habits = [h for h in habits.values() if h.get("last_check") == today]
    print(f"  习惯打卡: {len(today_habits)} / {len(habits)}")
    
    total_time = sum(t.get("time_spent", 0) for t in tasks.values())
    if total_time > 0:
        print(f"  总耗时: {total_time // 60} 小时 {total_time % 60} 分钟")
    print("-" * 50)

def main():
    ensure_data_dir()
    
    if len(sys.argv) < 2:
        print(f"""
{BOLD}Task Tracker - 任务管理与时间追踪{RESET}

{BLUE}使用方法:{RESET}
  task-tracker add <任务名称>      - 添加任务
  task-tracker list                - 列出任务
  task-tracker complete <id>       - 完成任务
  task-tracker delete <id>         - 删除任务
  task-tracker pomodoro [分钟]    - 开始番茄钟
  task-tracker habit add <名称>    - 添加习惯
  task-tracker habit check <名称> - 打卡习惯
  task-tracker habit list          - 列出习惯
  task-tracker stats               - 今日统计
  task-tracker help                - 显示帮助
""")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "complete" and len(sys.argv) > 2:
        complete_task(sys.argv[2])
    elif cmd == "delete" and len(sys.argv) > 2:
        delete_task(sys.argv[2])
    elif cmd == "pomodoro":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 25
        pomodoro(duration)
    elif cmd == "habit":
        if len(sys.argv) < 3:
            print("使用: task-tracker habit <add|check|list> [名称]")
            return
        subcmd = sys.argv[2].lower()
        if subcmd == "add" and len(sys.argv) > 3:
            add_habit(" ".join(sys.argv[3:]))
        elif subcmd == "check" and len(sys.argv) > 3:
            check_habit(" ".join(sys.argv[3:]))
        elif subcmd == "list":
            list_habits()
        else:
            print("使用: task-tracker habit <add|check|list> [名称]")
    elif cmd == "stats":
        daily_stats()
    elif cmd == "help":
        main()
    else:
        print(f"{RED}未知命令: {cmd}{RESET}")
        main()

if __name__ == "__main__":
    main()
