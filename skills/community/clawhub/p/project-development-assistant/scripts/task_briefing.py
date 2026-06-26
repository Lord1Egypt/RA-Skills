#!/usr/bin/env python3
"""
项目任务简报生成器 - 简洁版

设计原则：结构化输出，聊天只回一行摘要。

用法:
    python task_briefing.py -a generate        # 生成所有简报（静默）
    python task_briefing.py -a generate --show  # 显示摘要
    python task_briefing.py -a status -p <项目名>  # 查看单个状态
    python task_briefing.py -a check-resume      # 检查需要恢复的任务
"""

import os
import sys
import json
import glob
import re
from datetime import datetime, timedelta

BRIEFINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "briefings")

STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETED = "completed"
STATUS_BLOCKED = "blocked"

INTERRUPT_KEYWORDS = [
    "exec failed", "error:", "exception", "crashed", "aborted",
    "timeout", "killed", "SIGKILL", "SIGTERM",
    "Command exited with code 1", "Process exited with code 1",
    "Connection refused", "Connection reset", "broken pipe",
    "out of memory", "segmentation fault",
]

COMPLETION_KEYWORDS = [
    "success", "completed", "已完成", "任务完成",
    "编译成功", "build succeeded", "Done!",
]

def scan_projects(base_path):
    """扫描项目，查找有 logs/ 目录的项目"""
    projects = []
    if not os.path.exists(base_path):
        return projects
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if not os.path.isdir(item_path):
            continue
        logs_dir = os.path.join(item_path, "logs")
        if os.path.exists(logs_dir):
            projects.append({"name": item, "path": item_path, "logs_dir": logs_dir})
    return projects

def get_all_projects():
    """扫描所有可能的项目目录"""
    projects = []

    # workspace
    workspace = os.path.expanduser("~/.openclaw/workspace")
    projects.extend(scan_projects(workspace))

    # USB E: 盘
    for drive in ['E:', 'D:', 'F:']:
        base = os.path.join(drive, 'Projects')
        if os.path.exists(base):
            projects.extend(scan_projects(base))
        # 直接扫驱动器根目录下的项目
        if os.path.exists(drive):
            for item in os.listdir(drive):
                item_path = os.path.join(drive, item)
                if os.path.isdir(item_path):
                    logs_dir = os.path.join(item_path, "logs")
                    if os.path.exists(logs_dir):
                        projects.append({"name": item, "path": item_path, "logs_dir": logs_dir})

    # 去重
    seen = set()
    unique = []
    for p in projects:
        if p['path'] not in seen:
            seen.add(p['path'])
            unique.append(p)
    return unique

def get_latest_log(logs_dir):
    pattern = os.path.join(logs_dir, "devlog_*.md")
    files = glob.glob(pattern)
    if not files:
        return None, []
    latest = max(files, key=os.path.getmtime)
    with open(latest, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # 跳过 header（前3行）
    entries = []
    for line in lines[3:]:
        m = re.match(r'## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] (.+)', line)
        if m:
            entries.append({"ts": m.group(1), "cat": m.group(2), "msg": m.group(3),
                            "dt": datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S')})
    return latest, entries

def analyze(entries):
    if not entries:
        return STATUS_PENDING, None, None, []
    latest = entries[-1]
    status = STATUS_IN_PROGRESS
    current = None
    issues = []
    for e in reversed(entries[-8:]):
        msg = e['msg'].lower()
        if any(kw in msg for kw in COMPLETION_KEYWORDS):
            status = STATUS_COMPLETED
            break
        if e['cat'] in ('ERROR', 'WARNING'):
            issues.append(e['msg'][:80])
        if e['cat'] == 'PROGRESS' and not current:
            current = e['msg']
    if latest:
        age = datetime.now() - latest['dt']
        if age > timedelta(hours=2) and status == STATUS_IN_PROGRESS:
            issues.append(f"[!] {age.seconds//3600}h 无更新")
    return status, current, latest['ts'], issues[:3]

def check_interrupt(entries):
    for e in entries[-5:]:
        for kw in INTERRUPT_KEYWORDS:
            if kw.lower() in e['msg'].lower():
                return True, e['msg'][:60]
    return False, None

def generate_one(proj):
    path, name, logs_dir = proj['path'], proj['name'], proj['logs_dir']
    _, entries = get_latest_log(logs_dir)
    status, current, last_ts, issues = analyze(entries)
    interrupted, intr_msg = check_interrupt(entries)

    return {
        "project_name": name,
        "project_path": path,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "current_task": current,
        "last_update": last_ts,
        "open_issues": issues,
        "is_interrupted": interrupted,
        "interruption_msg": intr_msg,
        "needs_resume": interrupted and status == STATUS_IN_PROGRESS,
    }

def save_briefing(b):
    os.makedirs(BRIEFINGS_DIR, exist_ok=True)
    safe = re.sub(r'[^\w\u4e00-\u9fff-]', '_', b["project_name"])
    safe = re.sub(r'_+', '_', safe).strip('_')
    path = os.path.join(BRIEFINGS_DIR, f"{safe}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(b, f, ensure_ascii=False, indent=2)
    return path

def main():
    import argparse
    parser = argparse.ArgumentParser(description='项目简报工具')
    parser.add_argument('--action', '-a',
                        choices=['generate', 'list', 'status', 'check-resume'],
                        default='generate')
    parser.add_argument('--project', '-p', help='项目名（部分匹配）')
    parser.add_argument('--show', action='store_true', help='显示摘要')
    args = parser.parse_args()

    if args.action == 'generate':
        projects = get_all_projects()
        results = []
        for proj in projects:
            b = generate_one(proj)
            save_briefing(b)
            results.append(b)

        needs_resume = [b for b in results if b['needs_resume']]

        if args.show:
            for b in results:
                icon = {"pending":"⏳","in_progress":"[>]","completed":"[OK]","blocked":"🚫"}.get(b['status'],"[-]")
                print(f"{icon} {b['project_name']} | {b['status']}")
                if b['current_task']:
                    print(f"   → {b['current_task'][:60]}")
                if b['is_interrupted']:
                    print(f"   [!] {b['interruption_msg'][:60]}")
                if b['open_issues']:
                    print(f"   问题：{b['open_issues'][0][:60]}")
                print()

        print(f"[OK] 已生成 {len(results)} 个简报，{len(needs_resume)} 个需恢复")

    elif args.action == 'status':
        if not args.project:
            print("[X] 需要 --project")
            sys.exit(1)
        projects = get_all_projects()
        proj = next((p for p in projects if args.project.lower() in p['name'].lower() or args.project in p['path']), None)
        if not proj:
            print(f"[X] 未找到项目：{args.project}")
            sys.exit(1)
        b = generate_one(proj)
        icon = {"pending":"⏳","in_progress":"[>]","completed":"[OK]","blocked":"🚫"}.get(b['status'],"[-]")
        print(f"{icon} {b['project_name']} | {b['status']}")
        if b['current_task']: print(f"   当前：{b['current_task'][:80]}")
        if b['open_issues']: print(f"   问题：{b['open_issues'][0]}")
        if b['is_interrupted']: print(f"   [!] {b['interruption_msg']}")
        print(f"   最后更新：{b['last_update']}")

    elif args.action == 'list':
        projects = get_all_projects()
        print(f"[=] 共 {len(projects)} 个项目：")
        for p in projects:
            b = generate_one(p)
            icon = {"pending":"⏳","in_progress":"[>]","completed":"[OK]","blocked":"🚫"}.get(b['status'],"[-]")
            print(f"  {icon} {p['name']} | {b['status']}")

    elif args.action == 'check-resume':
        projects = get_all_projects()
        needs = []
        for proj in projects:
            b = generate_one(proj)
            if b['needs_resume']:
                save_briefing(b)
                needs.append(b)
        if needs:
            for b in needs:
                print(f"[>] {b['project_name']}: {b['current_task'] or 'N/A'}")
            print(f"\n[!] {len(needs)} 个任务需恢复，简报已保存")
        else:
            print("[OK] 没有需恢复的任务")

if __name__ == '__main__':
    main()
