#!/usr/bin/env python3
"""
Task Planner with reminders, recurring tasks, and document export (Markdown calendar).
Data stored in ~/.openclaw_tasks.json
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re

DATA_FILE = Path.home() / ".openclaw_tasks.json"

def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"next_id": 1, "tasks": []}

def save_tasks(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_deadline(date_str, time_str=None):
    now = datetime.now()
    full_str = f"{date_str} {time_str}" if time_str else date_str
    if "今天" in full_str:
        base_date = now.date()
    elif "明天" in full_str:
        base_date = now.date() + timedelta(days=1)
    elif "后天" in full_str:
        base_date = now.date() + timedelta(days=2)
    else:
        match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', full_str)
        if not match:
            match = re.search(r'(\d{1,2})月(\d{1,2})日', full_str)
            if match:
                month, day = int(match.group(1)), int(match.group(2))
                year = now.year
                if month < now.month or (month == now.month and day < now.day):
                    year += 1
                base_date = datetime(year, month, day).date()
            else:
                base_date = now.date()
        else:
            base_date = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3))).date()
    time_match = re.search(r'(\d{1,2})[:：](\d{1,2})', full_str)
    if time_match:
        hour, minute = int(time_match.group(1)), int(time_match.group(2))
    else:
        hour, minute = 20, 0
    result = datetime(base_date.year, base_date.month, base_date.day, hour, minute)
    if result < now and ("今天" not in full_str and "明天" not in full_str and "后天" not in full_str):
        result += timedelta(days=1)
    return result.isoformat()

def parse_recurrence(recurrence_str):
    if not recurrence_str:
        return None
    recurrence = {}
    text = recurrence_str.lower()
    if "每天" in text:
        recurrence["type"] = "daily"
        recurrence["interval"] = 1
    elif "每周" in text:
        recurrence["type"] = "weekly"
        recurrence["interval"] = 1
        match = re.search(r'每(\d+)周', text)
        if match:
            recurrence["interval"] = int(match.group(1))
    elif "每月" in text:
        recurrence["type"] = "monthly"
        recurrence["interval"] = 1
    elif "每年" in text:
        recurrence["type"] = "yearly"
        recurrence["interval"] = 1
    else:
        return None
    end = {}
    match_count = re.search(r'重复(\d+)次', text)
    if match_count:
        end["after_count"] = int(match_count.group(1))
    match_until = re.search(r'直到(\d{4}-\d{1,2}-\d{1,2})', text)
    if match_until:
        end["until_date"] = match_until.group(1)
    if end:
        recurrence["end"] = end
    return recurrence

def add_task(title, deadline_str, remind_before_minutes, priority, category, extra_json, recurrence_json=None):
    data = load_tasks()
    deadline = parse_deadline(deadline_str)
    remind_before = int(remind_before_minutes)
    priority = priority.lower() if priority in ["low","medium","high"] else "medium"
    category = category.lower() if category in ["work","life","other"] else "other"
    extra = {}
    if extra_json:
        try:
            extra = json.loads(extra_json)
        except:
            extra = {"raw": extra_json}
    recurrence = None
    if recurrence_json:
        try:
            recurrence = json.loads(recurrence_json)
        except:
            recurrence = parse_recurrence(recurrence_json)
    task = {
        "id": data["next_id"],
        "title": title,
        "deadline": deadline,
        "remind_before_minutes": remind_before,
        "reminder_sent": False,
        "priority": priority,
        "category": category,
        "extra": extra,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    if recurrence:
        task["recurrence"] = recurrence
    data["tasks"].append(task)
    data["next_id"] += 1
    save_tasks(data)
    return {"success": True, "task": task}

def update_task(task_id, title=None, deadline_str=None, remind_before_minutes=None,
                priority=None, category=None, extra_json=None, recurrence_json=None):
    data = load_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if deadline_str is not None:
                task["deadline"] = parse_deadline(deadline_str)
                task["reminder_sent"] = False
            if remind_before_minutes is not None:
                task["remind_before_minutes"] = int(remind_before_minutes)
                task["reminder_sent"] = False
            if priority is not None:
                task["priority"] = priority.lower() if priority in ["low","medium","high"] else "medium"
            if category is not None:
                task["category"] = category.lower() if category in ["work","life","other"] else "other"
            if extra_json is not None:
                try:
                    new_extra = json.loads(extra_json)
                    if isinstance(new_extra, dict):
                        task["extra"].update(new_extra)
                    else:
                        task["extra"] = {"raw": extra_json}
                except:
                    task["extra"] = {"raw": extra_json}
            if recurrence_json is not None:
                try:
                    task["recurrence"] = json.loads(recurrence_json)
                except:
                    task["recurrence"] = parse_recurrence(recurrence_json)
            save_tasks(data)
            return {"success": True, "task": task}
    return {"success": False, "error": f"Task with id {task_id} not found"}

def complete_task(task_id):
    data = load_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            if task["status"] == "pending":
                task["status"] = "done"
                save_tasks(data)
                if "recurrence" in task:
                    next_task = generate_next_recurring(task)
                    if next_task:
                        data = load_tasks()
                        next_task["id"] = data["next_id"]
                        data["tasks"].append(next_task)
                        data["next_id"] += 1
                        save_tasks(data)
                return {"success": True, "task": task}
            else:
                return {"success": False, "error": "Task already completed"}
    return {"success": False, "error": "Task not found"}

def generate_next_recurring(task):
    rec = task["recurrence"]
    rec_type = rec["type"]
    interval = rec.get("interval", 1)
    end = rec.get("end")
    current_dt = datetime.fromisoformat(task["deadline"])
    if rec_type == "daily":
        delta = timedelta(days=interval)
    elif rec_type == "weekly":
        delta = timedelta(weeks=interval)
    elif rec_type == "monthly":
        year = current_dt.year
        month = current_dt.month + interval
        while month > 12:
            month -= 12
            year += 1
        day = current_dt.day
        next_month_last_day = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        if day > next_month_last_day.day:
            day = next_month_last_day.day
        next_dt = datetime(year, month, day, current_dt.hour, current_dt.minute)
        delta = next_dt - current_dt
    elif rec_type == "yearly":
        next_dt = current_dt.replace(year=current_dt.year + interval)
        delta = next_dt - current_dt
    else:
        return None
    next_deadline = current_dt + delta
    if end and "until_date" in end:
        until = datetime.fromisoformat(end["until_date"])
        if next_deadline > until:
            return None
    new_task = {
        "id": None,
        "title": task["title"],
        "deadline": next_deadline.isoformat(),
        "remind_before_minutes": task["remind_before_minutes"],
        "reminder_sent": False,
        "priority": task["priority"],
        "category": task["category"],
        "extra": task["extra"].copy(),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "recurrence": rec,
        "recurrence_parent_id": task["id"]
    }
    return new_task

def list_tasks(status=None):
    data = load_tasks()
    tasks = data["tasks"]
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    return {"tasks": tasks}

def summary(date_filter):
    data = load_tasks()
    today = datetime.now().date()
    if date_filter == "today":
        target_date = today
    elif date_filter == "tomorrow":
        target_date = today + timedelta(days=1)
    elif date_filter == "week":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        tasks = [t for t in data["tasks"] if start <= datetime.fromisoformat(t["deadline"]).date() <= end]
        return {"filter": "week", "tasks": tasks}
    else:
        target_date = datetime.fromisoformat(date_filter).date()
    tasks = [t for t in data["tasks"] if datetime.fromisoformat(t["deadline"]).date() == target_date]
    return {"filter": target_date.isoformat(), "tasks": tasks}

def delete_task(task_id):
    data = load_tasks()
    original_len = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    if len(data["tasks"]) < original_len:
        save_tasks(data)
        return {"success": True}
    return {"success": False, "error": "Task not found"}

def check_reminders():
    data = load_tasks()
    now = datetime.now()
    reminded_tasks = []
    for task in data["tasks"]:
        if task["status"] != "pending":
            continue
        if task.get("reminder_sent", False):
            continue
        deadline = datetime.fromisoformat(task["deadline"])
        remind_time = deadline - timedelta(minutes=task["remind_before_minutes"])
        if now >= remind_time:
            task["reminder_sent"] = True
            reminded_tasks.append(task)
    if reminded_tasks:
        save_tasks(data)
    return {"reminders": reminded_tasks}

def export_doc(date_range="week"):
    """导出日历文档（Markdown 格式），按天分组。"""
    data = load_tasks()
    now = datetime.now()
    if date_range == "week":
        start_date = now.date() - timedelta(days=now.weekday())
        end_date = start_date + timedelta(days=6)
        title = f"每周日历 ({start_date} 至 {end_date})"
    elif date_range == "month":
        start_date = now.date().replace(day=1)
        next_month = start_date + timedelta(days=32)
        end_date = next_month.replace(day=1) - timedelta(days=1)
        title = f"每月日历 ({start_date.year}年{start_date.month}月)"
    else:
        start_date = now.date()
        end_date = start_date
        title = f"单日日历 ({start_date})"

    tasks_in_range = []
    for task in data["tasks"]:
        if task["status"] != "pending":
            continue
        dt = datetime.fromisoformat(task["deadline"]).date()
        if start_date <= dt <= end_date:
            tasks_in_range.append(task)

    tasks_by_date = {}
    for task in tasks_in_range:
        dt = datetime.fromisoformat(task["deadline"]).date()
        tasks_by_date.setdefault(dt, []).append(task)

    md_lines = [f"# {title}\n", f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
    for dt in sorted(tasks_by_date.keys()):
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
        md_lines.append(f"## {dt} ({weekday})\n")
        md_lines.append("| 时间 | 任务 | 提醒 | 优先级 | 分类 | 备注 |")
        md_lines.append("|------|------|------|--------|------|------|")
        for task in tasks_by_date[dt]:
            deadline_time = datetime.fromisoformat(task["deadline"]).strftime("%H:%M")
            remind_min = task["remind_before_minutes"]
            remind_str = f"提前{remind_min}分钟" if remind_min else "无"
            priority_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(task["priority"], "⚪")
            category_icon = {"work": "💼", "life": "🏠", "other": "📌"}.get(task["category"], "📌")
            extra_str = ""
            if task.get("extra"):
                extra_items = []
                if "cinema" in task["extra"]:
                    extra_items.append(f"影院:{task['extra']['cinema']}")
                if "seat" in task["extra"]:
                    extra_items.append(f"座位:{task['extra']['seat']}")
                if "movie" in task["extra"]:
                    extra_items.append(f"电影:{task['extra']['movie']}")
                extra_str = ", ".join(extra_items)
            md_lines.append(f"| {deadline_time} | {task['title']} | {remind_str} | {priority_icon} {task['priority']} | {category_icon} {task['category']} | {extra_str} |")
        md_lines.append("")
    if not tasks_in_range:
        md_lines.append("该时间段内没有未完成的任务。")

    doc_path = Path.home() / "openclaw_calendar.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))
    
    return {"success": True, "file_path": str(doc_path), "range": date_range, "task_count": len(tasks_in_range)}

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--deadline", required=True)
    add_parser.add_argument("--remind-before", type=int, required=True)
    add_parser.add_argument("--priority", default="medium")
    add_parser.add_argument("--category", default="other")
    add_parser.add_argument("--extra", default="{}")
    add_parser.add_argument("--recurrence", default=None)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--title")
    update_parser.add_argument("--deadline")
    update_parser.add_argument("--remind-before", type=int)
    update_parser.add_argument("--priority")
    update_parser.add_argument("--category")
    update_parser.add_argument("--extra")
    update_parser.add_argument("--recurrence")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=["pending", "done"], default=None)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--date", required=True, choices=["today", "tomorrow", "week"])

    complete_parser = subparsers.add_parser("complete")
    complete_parser.add_argument("--id", type=int, required=True)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    remind_parser = subparsers.add_parser("remind")

    export_doc_parser = subparsers.add_parser("export_doc")
    export_doc_parser.add_argument("--range", choices=["week", "month"], default="week")

    args = parser.parse_args()

    if args.command == "add":
        result = add_task(args.title, args.deadline, args.remind_before,
                          args.priority, args.category, args.extra, args.recurrence)
    elif args.command == "update":
        result = update_task(args.id, args.title, args.deadline, args.remind_before,
                             args.priority, args.category, args.extra, args.recurrence)
    elif args.command == "list":
        result = list_tasks(args.status)
    elif args.command == "summary":
        result = summary(args.date)
    elif args.command == "complete":
        result = complete_task(args.id)
    elif args.command == "delete":
        result = delete_task(args.id)
    elif args.command == "remind":
        result = check_reminders()
    elif args.command == "export_doc":
        result = export_doc(args.range)
    else:
        result = {"success": False, "error": "Unknown command"}

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
