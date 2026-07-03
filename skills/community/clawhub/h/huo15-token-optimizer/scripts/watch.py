#!/usr/bin/env python3
"""huo15-token-optimizer watch — 持续监控 token 消耗，超阈值告警"""
import os, json, sys, time
from datetime import datetime

WORKSPACE_BASE = os.path.expanduser("~/.openclaw")
ALERT_FILE = os.path.join(WORKSPACE_BASE, "workspace", "memory", "token-alert.md")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def check_once(config):
    alerts = []
    thresholds = config["thresholds"]
    
    for d in os.listdir(WORKSPACE_BASE):
        if not d.startswith("workspace"):
            continue
        ws_path = os.path.join(WORKSPACE_BASE, d)
        if not os.path.isdir(ws_path):
            continue
        
        ws_name = d.replace("workspace-", "").replace("workspace.", "")
        
        # Check AGENTS.md
        agents = os.path.join(ws_path, "AGENTS.md")
        if os.path.exists(agents):
            size = os.path.getsize(agents)
            if size > thresholds["watch_agents_max_kb"] * 1024:
                alerts.append(f"[{ws_name}] AGENTS.md {size/1024:.0f}KB > {thresholds['watch_agents_max_kb']}KB")
        
        # Check DREAMS.md
        dreams = os.path.join(ws_path, "DREAMS.md")
        if os.path.exists(dreams):
            size = os.path.getsize(dreams)
            if size > thresholds["watch_dreams_max_kb"] * 1024:
                alerts.append(f"[{ws_name}] DREAMS.md {size/1024:.0f}KB > {thresholds['watch_dreams_max_kb']}KB")
    
    if alerts:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [f"## {now} Token 告警"] + [f"- {a}" for a in alerts] + [""]
        with open(ALERT_FILE, "a") as f:
            f.write("\n".join(lines) + "\n")
        
        print(f"[{now}] ALERT: {len(alerts)} 项超阈值")
        for a in alerts:
            print(f"  {a}")
        return True
    return False

def watch():
    config = load_config()
    print("辉火 Token 监控已启动 (Ctrl+C 停止)")
    print(f"阈值: AGENTS > {config['thresholds']['watch_agents_max_kb']}KB | DREAMS > {config['thresholds']['watch_dreams_max_kb']}KB")
    
    try:
        while True:
            check_once(config)
            time.sleep(3600)  # Check every hour
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        check_once(load_config())
    else:
        watch()
