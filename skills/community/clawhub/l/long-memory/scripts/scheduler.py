#!/usr/bin/env python3
"""定时任务调度器：管理蒸馏/备份/清理等定时任务"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read, safe_write, safe_read_json, safe_write_json

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
SCHEDULE_FILE = ".schedule.json"
LOG_FILE = ".scheduler.log.jsonl"


def load_schedule(memory_dir: Path) -> list[dict]:
    fp = memory_dir / SCHEDULE_FILE
    if fp.exists():
        return safe_read_json(fp)
    # 默认任务
    return [
        {
            "id": "weekly-distill",
            "name": "周蒸馏",
            "command": "distill_week.py",
            "args": [],
            "schedule": "weekly",
            "enabled": True,
            "last_run": None,
            "last_status": None,
        },
        {
            "id": "daily-summary",
            "name": "每日摘要",
            "command": "generate_summary.py",
            "args": [],
            "schedule": "daily",
            "enabled": True,
            "last_run": None,
            "last_status": None,
        },
        {
            "id": "daily-backup",
            "name": "每日备份",
            "command": "auto_backup.py",
            "args": [],
            "schedule": "daily",
            "enabled": False,
            "last_run": None,
            "last_status": None,
        },
        {
            "id": "monthly-clean",
            "name": "月度清理",
            "command": "clean_old.py",
            "args": ["--days", "90", "--execute"],
            "schedule": "monthly",
            "enabled": False,
            "last_run": None,
            "last_status": None,
        },
        {
            "id": "weekly-integrity",
            "name": "周完整性检查",
            "command": "integrity_check.py",
            "args": [],
            "schedule": "weekly",
            "enabled": True,
            "last_run": None,
            "last_status": None,
        },
    ]


def save_schedule(memory_dir: Path, schedule: list[dict]):
    safe_write_json(memory_dir / SCHEDULE_FILE, schedule)


def should_run(task: dict) -> bool:
    """判断任务是否应该运行"""
    if not task.get("enabled", False):
        return False

    last_run = task.get("last_run")
    if not last_run:
        return True

    last = datetime.fromisoformat(last_run)
    now = datetime.now()
    schedule = task.get("schedule", "daily")

    if schedule == "daily":
        return last.date() < now.date()
    elif schedule == "weekly":
        return (now - last).days >= 7
    elif schedule == "monthly":
        return (now - last).days >= 30
    elif schedule == "hourly":
        return (now - last).seconds >= 3600
    return False


def run_task(task: dict, memory_dir: Path) -> dict:
    """执行单个任务"""
    scripts_dir = Path(__file__).parent
    script = scripts_dir / task["command"]
    
    if not script.exists():
        return {"status": "error", "message": f"脚本不存在: {task['command']}"}

    args = [sys.executable, str(script)] + task.get("args", [])
    args.append("--memory-dir")
    args.append(str(memory_dir))

    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=60)
        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout[:500],
            "stderr": result.stderr[:200],
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "执行超时"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def run_due_tasks(memory_dir: Path, force: bool = False):
    """运行所有到期任务"""
    schedule = load_schedule(memory_dir)
    results = []

    for task in schedule:
        if force or should_run(task):
            print(f"🔄 运行: {task['name']}...")
            result = run_task(task, memory_dir)
            task["last_run"] = datetime.now().isoformat()
            task["last_status"] = result["status"]
            
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"   {status_icon} {task['name']}")
            if result.get("stdout"):
                for line in result["stdout"].split("\n")[:3]:
                    if line.strip():
                        print(f"   {line}")
            
            results.append({"task": task["name"], **result})

    save_schedule(memory_dir, schedule)
    
    # 记录日志
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
    }
    log_path = memory_dir / LOG_FILE
    safe_write(log_path, json.dumps(log_entry, ensure_ascii=False) + "\n", append=True)

    return results


def print_schedule(schedule: list[dict]):
    print("=" * 60)
    print("⏰ 定时任务调度器")
    print("=" * 60)

    for task in schedule:
        enabled = "🟢" if task.get("enabled") else "⚫"
        schedule_icons = {"daily": "📅", "weekly": "📆", "monthly": "🗓️", "hourly": "⏰"}
        s_icon = schedule_icons.get(task.get("schedule", ""), "❓")
        
        last_run = task.get("last_run", "从未")
        if last_run and last_run != "从未":
            last_run = last_run[:16].replace("T", " ")
        
        last_status = ""
        if task.get("last_status"):
            last_status = " ✅" if task["last_status"] == "success" else " ❌"

        print(f"\n  {enabled} {task['name']} {s_icon} {task.get('schedule', '?')}")
        print(f"     脚本: {task['command']}")
        print(f"     上次: {last_run}{last_status}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="定时任务调度器")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--run", action="store_true", help="运行到期任务")
    p.add_argument("--force", "-f", action="store_true", help="强制运行所有任务")
    p.add_argument("--list", "-l", action="store_true", help="列出任务")
    p.add_argument("--enable", type=str, help="启用任务（按ID）")
    p.add_argument("--disable", type=str, help="禁用任务（按ID）")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.enable or args.disable:
        schedule = load_schedule(md)
        task_id = args.enable or args.disable
        enabled = bool(args.enable)
        for task in schedule:
            if task["id"] == task_id:
                task["enabled"] = enabled
                print(f"{'✅ 启用' if enabled else '⚫ 禁用'}: {task['name']}")
                break
        save_schedule(md, schedule)

    elif args.run or args.force:
        results = run_due_tasks(md, args.force)
        success = sum(1 for r in results if r["status"] == "success")
        print(f"\n📊 完成: {success}/{len(results)} 个任务成功")

    elif args.list:
        schedule = load_schedule(md)
        print_schedule(schedule)

    else:
        # 默认列出
        schedule = load_schedule(md)
        print_schedule(schedule)
        due = [t for t in schedule if should_run(t)]
        if due:
            print(f"\n🔔 {len(due)} 个任务待运行（使用 --run 执行）")
