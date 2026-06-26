#!/usr/bin/env python3
"""
Ézekiel Holistic Memory System — Cron Manager
Sets up automatic maintenance for all memory layers
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path.home() / ".openclaw" / "skills" / "holistic-memory-system" / "scripts"
CRON_MARKER = Path.home() / ".openclaw" / "cron" / "holistic-memory-jobs.json"

def create_cron_jobs():
    """Create OpenClaw cron jobs for memory maintenance"""
    
    jobs = [
        {
            "name": "L6 Gravity Decay (Daily)",
            "description": "Apply semantic gravity decay to L6 nebula nodes — nodes older than 180 days sink",
            "schedule": {"kind": "cron", "expr": "0 4 * * *", "tz": "America/Toronto"},
            "payload": {
                "kind": "systemEvent",
                "text": "__ezekiel_nebula_decay__"
            },
            "sessionTarget": "isolated",
            "enabled": True
        },
        {
            "name": "L5 Crystallization Check (Every 6h)",
            "description": "Check for brillant nodes and crystallize to L5 Obsidian notes",
            "schedule": {"kind": "cron", "expr": "0 */6 * * *", "tz": "America/Toronto"},
            "payload": {
                "kind": "systemEvent",
                "text": "__ezekiel_crystallize__"
            },
            "sessionTarget": "isolated",
            "enabled": True
        },
        {
            "name": "Memory Health Check (Daily)",
            "description": "Run full health check on all memory layers",
            "schedule": {"kind": "cron", "expr": "0 7 * * *", "tz": "America/Toronto"},
            "payload": {
                "kind": "systemEvent",
                "text": "__ezekiel_health_check__"
            },
            "sessionTarget": "isolated",
            "enabled": True
        },
        {
            "name": "L3 Log Rotation Check (Weekly)",
            "description": "Ensure JSONL logs are being written, check rotation",
            "schedule": {"kind": "cron", "expr": "0 8 * * 0", "tz": "America/Toronto"},
            "payload": {
                "kind": "systemEvent",
                "text": "__ezekiel_log_check__"
            },
            "sessionTarget": "isolated",
            "enabled": True
        }
    ]
    
    with open(CRON_MARKER, "w") as f:
        json.dump({"version": 1, "jobs": jobs, "created": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    
    return len(jobs)

def install_system_crons():
    """Install system crons for script-based maintenance"""
    cron_commands = [
        "# Ézekiel Holistic Memory Maintenance",
        "# Gravity decay - daily at 4am",
        "0 4 * * * python3 /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_nebula.py decay >> ~/.openclaw/logs/nebula-decay.log 2>&1",
        "# Health check - daily at 7am",
        "0 7 * * * python3 /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_health_check.py >> ~/.openclaw/logs/health-check.log 2>&1",
        "# Crystallization check - every 6 hours",
        "0 */6 * * * python3 /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_crystallizer.py status >> ~/.openclaw/logs/crystallization.log 2>&1",
        "# Startup initializer - boot",
        "@reboot /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_memory_startup.sh >> ~/.openclaw/logs/startup.log 2>&1"
    ]
    
    crontab_current = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    crontab_new = crontab_current
    
    for cmd in cron_commands:
        if cmd.startswith("#"):
            crontab_new += cmd + "\n"
        elif cmd not in crontab_new:
            crontab_new += cmd + "\n"
    
    subprocess.run(["crontab", "-"], input=crontab_new, text=True)
    return True

def handle_memory_event(event: str):
    """Handle memory system events triggered by cron/system"""
    if event == "__ezekiel_nebula_decay__":
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "ezekiel_nebula.py"), "decay"],
            capture_output=True, text=True
        )
        return {"event": event, "result": result.stdout.strip() or "decay applied"}
    
    elif event == "__ezekiel_crystallize__":
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "ezekiel_crystallizer.py"), "crystallize"],
            capture_output=True, text=True
        )
        return {"event": event, "result": result.stdout.strip() or "crystallization complete"}
    
    elif event == "__ezekiel_health_check__":
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "ezekiel_health_check.py")],
            capture_output=True, text=True
        )
        return {"event": event, "result": "health check completed"}
    
    elif event == "__ezekiel_log_check__":
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "ezekiel_log.py"), "query"],
            capture_output=True, text=True
        )
        return {"event": event, "result": "log check completed"}
    
    return {"event": event, "result": "unknown event"}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "install":
            count = create_cron_jobs()
            install_system_crons()
            print(f"✅ Installed {count} cron jobs + system crontab entries")
        
        elif sys.argv[1] == "handle" and len(sys.argv) > 2:
            result = handle_memory_event(sys.argv[2])
            print(json.dumps(result, indent=2))
        
        elif sys.argv[1] == "list":
            if CRON_MARKER.exists():
                with open(CRON_MARKER, "r") as f:
                    data = json.load(f)
                print(f"Cron jobs defined: {len(data['jobs'])}")
                for job in data["jobs"]:
                    print(f"  - {job['name']}: {job['schedule']['expr']}")
            else:
                print("No cron jobs defined yet. Run 'install' first.")
    
    else:
        print("Usage: python3 ezekiel_cron_manager.py [install|handle|list]")
        print("  install - Set up all cron jobs")
        print("  handle <event> - Handle a memory event")
        print("  list - List defined cron jobs")