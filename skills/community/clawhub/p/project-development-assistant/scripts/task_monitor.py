#!/usr/bin/env python3
"""
项目健康监控 - 被动静默版

设计原则：只写文件，不主动推送消息。供 OpenClaw cron 调用，
结果写入文件供下次会话时读取，不打扰用户。

用法:
    python task_monitor.py              # 运行检查（静默）
    python task_monitor.py --show       # 显示检查结果
"""

import os
import sys
import json
import glob
import re
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
BRIEFINGS_DIR = os.path.join(SKILL_DIR, "briefings")
MONITOR_LOG = os.path.join(BRIEFINGS_DIR, "monitor_log.json")

def scan_projects():
    """扫描项目"""
    projects = []
    workspace = os.path.expanduser("~/.openclaw/workspace")
    for item in os.listdir(workspace) if os.path.exists(workspace) else []:
        p = os.path.join(workspace, item)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "logs")):
            projects.append({"name": item, "path": p})
    for drive in ['E:', 'D:', 'F:']:
        base = os.path.join(drive, 'Projects')
        for item in os.listdir(base) if os.path.exists(base) else []:
            p = os.path.join(base, item)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, "logs")):
                projects.append({"name": item, "path": p})
    return projects

INTERRUPT_KEYWORDS = [
    "exec failed", "error:", "exception", "crashed", "aborted",
    "timeout", "killed", "SIGKILL", "SIGTERM",
    "Command exited with code 1", "Process exited with code 1",
    "out of memory", "segmentation fault",
]

def get_latest_entries(logs_dir, count=5):
    import glob
    files = glob.glob(os.path.join(logs_dir, "devlog_*.md"))
    if not files:
        return []
    latest = max(files, key=os.path.getmtime)
    with open(latest, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    entries = []
    for line in lines[3:]:
        m = re.match(r'## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] (.+)', line)
        if m:
            entries.append({"ts": m.group(1), "cat": m.group(2), "msg": m.group(3),
                            "dt": datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S')})
    return entries[-count:]

def check_project(proj):
    """检查单个项目，返回结果"""
    logs_dir = os.path.join(proj["path"], "logs")
    entries = get_latest_entries(logs_dir)
    if not entries:
        return None

    latest = entries[-1]
    issues = [e['msg'][:60] for e in entries[-5:]
              if e['cat'] in ('ERROR', 'WARNING')]

    interrupted = any(
        any(kw.lower() in e['msg'].lower() for kw in INTERRUPT_KEYWORDS)
        for e in entries[-3:]
    )

    age = datetime.now() - latest['dt']
    stale = age > timedelta(hours=4)

    status = "normal"
    if interrupted: status = "interrupted"
    elif stale: status = "stale"
    elif issues: status = "has_issues"

    return {
        "name": proj["name"],
        "path": proj["path"],
        "status": status,
        "last_ts": latest['ts'],
        "last_msg": latest['msg'][:60],
        "issues": issues[:2],
        "interrupted": interrupted,
        "stale": stale,
        "age_hours": round(age.total_seconds() / 3600, 1),
    }

def write_monitor_log(results):
    """写入监控日志"""
    os.makedirs(BRIEFINGS_DIR, exist_ok=True)
    log = {
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(results),
        "interrupted": [r for r in results if r and r['status'] == 'interrupted'],
        "stale": [r for r in results if r and r['status'] == 'stale'],
        "has_issues": [r for r in results if r and r['status'] == 'has_issues'],
        "normal": [r for r in results if r and r['status'] == 'normal'],
        "all": results,
    }
    with open(MONITOR_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    return log

def main():
    show = '--show' in sys.argv or '-v' in sys.argv

    projects = scan_projects()
    results = []
    for proj in projects:
        r = check_project(proj)
        if r:
            results.append(r)

    log = write_monitor_log(results)

    if show:
        print(f"📊 健康检查 | {datetime.now().strftime('%H:%M:%S')} | {len(projects)} 个项目")
        for r in results:
            icon = {"normal":"[OK]","interrupted":"[>]","stale":"⏳","has_issues":"[!]"}.get(r['status'],"[-]")
            print(f"  {icon} {r['name']} | {r['status']} | {r['last_ts']}")
        print()
        print(f"需关注：[>] {len(log['interrupted'])} | ⏳ {len(log['stale'])} | [!] {len(log['has_issues'])}")
    else:
        print(f"[OK] 检查完成：{len(projects)} 个项目，{len(log['interrupted'])} 需恢复")

if __name__ == '__main__':
    main()
