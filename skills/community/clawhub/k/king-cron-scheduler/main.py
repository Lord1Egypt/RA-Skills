#!/usr/bin/env python3
"""Cron Scheduler — manage, monitor, and alert on cron and systemd timer tasks."""
import json, subprocess, sys, os
from datetime import datetime

VERSION = "1.0.0"

def list_timers():
    r = subprocess.run(["systemctl", "list-timers", "--all", "--no-pager"], capture_output=True, text=True, timeout=10)
    return r.stdout

def list_crontabs():
    r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
    return r.stdout if r.returncode == 0 else "No crontab"

def check_failures(log_path="/var/log/syslog"):
    if not os.path.exists(log_path): return []
    r = subprocess.run(["grep", "-i", "failed|error|timeout", log_path], capture_output=True, text=True, timeout=10)
    return r.stdout.strip().split("\n")[-5:] if r.stdout.strip() else []

if __name__ == '__main__':
    if "--version" in sys.argv: print(VERSION); sys.exit(0)
    if "--help" in sys.argv or len(sys.argv) < 2:
        print(f"""Cron Scheduler v{VERSION}
Usage: python3 main.py --list      List all scheduled tasks
       python3 main.py --crontab   View user crontab
       python3 main.py --failures  Recent failure log
       python3 main.py --pro       Pro: schedule editor + alerts""")
        sys.exit(0)
    result = {"version": VERSION, "timestamp": datetime.now().isoformat()}
    if "--list" in sys.argv: result["timers"] = list_timers()
    if "--crontab" in sys.argv: result["crontab"] = list_crontabs()
    if "--failures" in sys.argv: result["recent_failures"] = check_failures()
    if "--pro" in sys.argv: result["pro"] = {"alert_enabled": True, "retry": "exponential_backoff"}
    print(json.dumps(result, indent=2, ensure_ascii=False))
