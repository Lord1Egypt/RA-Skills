#!/usr/bin/env python3
import json
import os
from datetime import datetime

def get_workspace_root():
    return os.environ.get(
        "WORKSPACE_ROOT",
        os.path.expanduser("~/.openclaw/workspace")
    )

MEMORY_DIR = os.path.join(get_workspace_root(), "memory", "clawguard")
REPORTS_PATH = os.path.join(MEMORY_DIR, "reports.json")

def ensure_storage():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(REPORTS_PATH):
        with open(REPORTS_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "metadata": {
                    "version": "1.0.0",
                    "created_at": datetime.utcnow().isoformat(),
                    "last_updated": datetime.utcnow().isoformat()
                },
                "reports": {}
            }, f, indent=2, ensure_ascii=False)

def load_reports():
    ensure_storage()
    with open(REPORTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_report(report):
    data = load_reports()
    data["reports"][report["report_id"]] = report
    data["metadata"]["last_updated"] = datetime.utcnow().isoformat()
    with open(REPORTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
