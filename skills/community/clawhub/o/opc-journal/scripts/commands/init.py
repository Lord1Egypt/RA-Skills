"""Journal command: initialize."""
import json

from utils.storage import build_customer_dir, build_memory_path, write_memory_file
from utils.timezone import now_tz
from scripts.commands._meta import detect_language, write_meta


def run(customer_id: str, args: dict) -> dict:
    """Initialize journal for customer."""
    day = args.get("day", 1)
    goals = args.get("goals", [])
    preferences = args.get("preferences", {})

    if not preferences:
        preferences = {
            "communication_style": "friendly_professional",
            "timezone": "Asia/Shanghai",
        }

    language = args.get("language") or detect_language(goals + list(preferences.values()))
    today_str = now_tz().strftime("%d-%m-%y")

    # Minimal charter without hardcoded motivational text or bilingual blocks.
    goals_text = json.dumps(goals, ensure_ascii=False) if goals else "[]"
    prefs_text = json.dumps(preferences, ensure_ascii=False)

    content = f"""---
type: charter
date: {today_str}
day: {day}
customer_id: {customer_id}
version: 2.5.1
language: {language}
---

# OPC Journal Charter — Day {day}

**Customer**: {customer_id}
**Version**: 2.5.1
**Language**: {language}

## Goals
{goals_text}

## Preferences
{prefs_text}
"""

    memory_path = build_memory_path(customer_id)
    write_result = write_memory_file(memory_path, content)

    meta = {
        "customer_id": customer_id,
        "started_day": day,
        "started_at": now_tz().isoformat(),
        "version": "2.5.2",
        "goals": goals,
        "preferences": preferences,
        "language": language,
        "total_entries": 0,
    }
    write_meta(customer_id, meta)

    if write_result["success"]:
        return {
            "status": "success",
            "result": {
                "customer_id": customer_id,
                "initialized": True,
                "day": day,
                "goals_count": len(goals),
                "memory_path": memory_path,
                "language": language,
            },
            "message": f"Journal initialized for {customer_id}",
        }

    return {
        "status": "error",
        "result": None,
        "message": f"Failed to write memory: {write_result.get('error')}",
    }
