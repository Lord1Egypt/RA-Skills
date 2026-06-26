#!/usr/bin/env python3
"""
proactive-ops-monitor — token tracking, alerts, health dashboard
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.cwd()
MEMORY_DIR = WORKSPACE / "memory"
WAL_FILE = MEMORY_DIR / "wal.jsonl"
BUFFER_FILE = MEMORY_DIR / "working-buffer.md"
ALERTS_FILE = MEMORY_DIR / "ops-alerts.jsonl"
CONFIG_FILE = WORKSPACE / "proactive-ops-config.json"

def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except:
            pass
    return {
        "alerts": {"token_warning": 70, "token_critical": 85, "buffer_warning_size_kb": 5000},
        "suggestions": {"enabled": True, "max_per_turn": 1, "include_open_loops": True, "include_context_gaps": True},
        "dashboard": {"show_suggestions": True, "show_alerts": True}
    }

def estimate_tokens(text: str) -> int:
    return len(text) // 4

def get_token_utilization():
    # Rough estimate: count recent conversation (assume 120k context)
    # For demo, we'll read buffer if exists
    if BUFFER_FILE.exists():
        content = BUFFER_FILE.read_text()
        tokens = estimate_tokens(content[-20000:])  # last 20k chars
        # Assume buffer represents ~60% of recent context; double to estimate total
        estimated_total = tokens * 2
        utilization = min(100, int((estimated_total / 120000) * 100))
        return {"tokens_est": estimated_total, "utilization_percent": utilization}
    return {"tokens_est": 0, "utilization_percent": 0}

def get_memory_health():
    wal_count = sum(1 for _ in open(WAL_FILE)) if WAL_FILE.exists() else 0
    wal_size = WAL_FILE.stat().st_size if WAL_FILE.exists() else 0
    buf_size = BUFFER_FILE.stat().st_size if BUFFER_FILE.exists() else 0
    daily_count = len(list(MEMORY_DIR.glob("*.md")))
    token_stats = get_token_utilization()
    status = "healthy"
    if token_stats["utilization_percent"] >= 85:
        status = "critical"
    elif token_stats["utilization_percent"] >= 70:
        status = "warning"
    return {
        "wal": {"entries": wal_count, "size_bytes": wal_size},
        "buffer": {"size_bytes": buf_size},
        "daily_logs": daily_count,
        "token_utilization": token_stats["utilization_percent"],
        "status": status
    }

def check_alerts():
    cfg = load_config()
    health = get_memory_health()
    alerts = []
    if health["token_utilization"] >= cfg["alerts"]["token_critical"]:
        alerts.append({"level": "critical", "metric": "token_utilization", "value": health["token_utilization"], "message": "Token usage critical. Wrap up immediately."})
    elif health["token_utilization"] >= cfg["alerts"]["token_warning"]:
        alerts.append({"level": "warning", "metric": "token_utilization", "value": health["token_utilization"], "message": "Token usage elevated. Consider /wrap_up."})
    # Log alerts to file
    if alerts and ALERTS_FILE.exists():
        for a in alerts:
            a["timestamp"] = datetime.utcnow().isoformat() + "Z"
            with open(ALERTS_FILE, "a") as f:
                f.write(json.dumps(a) + "\n")
    return alerts

def generate_suggestions(limit=3):
    cfg = load_config()
    suggestions = []
    # Check open loops in WAL (category=draft, decision, correction)
    if WAL_FILE.exists():
        open_loops = []
        with open(WAL_FILE) as f:
            for line in f.readlines()[-100:]:
                try:
                    entry = json.loads(line)
                    if entry["category"] in ("draft", "decision", "correction"):
                        open_loops.append(entry["content"])
                except:
                    continue
        for i, loop in enumerate(open_loops[:limit]):
            suggestions.append({"type": "open_loop", "content": loop, "priority": "high"})
    # Check token utilization suggestion
    health = get_memory_health()
    if health["token_utilization"] > 80:
        suggestions.append({"type": "ops", "content": "Token utilization high — run /wrap_up to preserve context", "priority": "high"})
    return suggestions[:limit]

def health_dashboard(format="text"):
    health = get_memory_health()
    alerts = check_alerts()
    suggestions = generate_suggestions() if load_config()["dashboard"]["show_suggestions"] else []
    if format == "json":
        out = {"health": health, "alerts": alerts, "suggestions": suggestions}
        print(json.dumps(out, indent=2))
        return
    # Text format
    lines = [
        "🛡️  OpenClaw Ops Dashboard",
        "=" * 40,
        f"Token Utilization:     {health['token_utilization']}%",
        f"Memory Layers:",
        f"  • WAL entries:       {health['wal']['entries']} ({health['wal']['size_bytes']} bytes)",
        f"  • Working buffer:    {health['buffer']['size_bytes']} bytes",
        f"  • Daily logs:        {health['daily_logs']}",
        f"Status:               {'✅ Healthy' if health['status']=='healthy' else '⚠️ Warning' if health['status']=='warning' else '🚨 Critical'}",
        "",
    ]
    if alerts and load_config()["dashboard"]["show_alerts"]:
        lines.append("Alerts:")
        for a in alerts:
            lines.append(f"  • {a['level'].upper()}: {a['message']}")
        lines.append("")
    if suggestions:
        lines.append("Suggestions:")
        for i, s in enumerate(suggestions, 1):
            lines.append(f"  {i}. [{s['type']}] {s['content']}")
    print("\n".join(lines))

def main():
    if len(sys.argv) < 2:
        print("Usage: run.py [health_dashboard|token_utilization|suggest_next|alert_config] [json_input]")
        sys.exit(1)

    action = sys.argv[1]
    input_data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    if action == "health_dashboard":
        health_dashboard(format=input_data.get("format", "text"))
    elif action == "token_utilization":
        print(json.dumps(get_token_utilization()))
    elif action == "suggest_next":
        suggestions = generate_suggestions(limit=input_data.get("limit", 3))
        print(json.dumps(suggestions, indent=2))
    elif action == "alert_config":
        # Update config file
        cfg = load_config()
        # Merge
        if "alerts" in input_data:
            cfg["alerts"].update(input_data["alerts"])
        if "suggestions" in input_data:
            cfg["suggestions"].update(input_data["suggestions"])
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
        print(json.dumps({"status": "ok", "config_file": str(CONFIG_FILE)}))
    else:
        print(json.dumps({"error": f"unknown action: {action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()