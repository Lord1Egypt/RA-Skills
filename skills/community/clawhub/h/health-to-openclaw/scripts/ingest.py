#!/usr/bin/env python3
"""
Apple Health Sync — ingest.py
Parses incoming health data messages from the iOS app and stores them in SQLite.

Usage:
    echo "message text" | python3 ingest.py
    python3 ingest.py < message.txt
    python3 ingest.py "full message text"
"""

import sys
import re
import sqlite3
import os
from datetime import datetime, timezone
from pathlib import Path

DB_DIR = Path.home() / ".apple-health-sync"
DB_PATH = DB_DIR / "health.db"


def init_db(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS health_samples (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            type        TEXT NOT NULL,
            type_name   TEXT,
            sample_date TEXT NOT NULL,
            value       REAL,
            value_str   TEXT,
            unit        TEXT,
            received_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sync_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at TEXT NOT NULL,
            type        TEXT NOT NULL,
            type_name   TEXT,
            count       INTEGER NOT NULL,
            raw_message TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_type_date ON health_samples(type, sample_date);
        CREATE INDEX IF NOT EXISTS idx_date ON health_samples(sample_date);
    """)
    conn.commit()


def parse_message(text: str) -> dict | None:
    """Parse a health data message from the iOS app."""
    if "🍎 Apple Health 数据更新" not in text and "Apple Health" not in text:
        return None

    lines = text.strip().split("\n")
    result = {
        "type": None,
        "type_name": None,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "samples": [],
    }

    # Parse header
    for line in lines:
        if line.startswith("类型："):
            result["type_name"] = line.replace("类型：", "").strip()
        elif line.startswith("时间："):
            pass  # iOS timestamp, not used directly

    # Infer type identifier from Chinese name
    result["type"] = name_to_identifier(result["type_name"] or "")

    # Parse sample lines (start with "• ")
    separator_seen = False
    for line in lines:
        if line.strip() == "---":
            separator_seen = True
            continue
        if not separator_seen:
            continue
        if not line.startswith("•"):
            continue

        # Format: "• MM-DD HH:mm: VALUE UNIT"  or  "• MM-DD HH:mm（DURATION）: DESC"
        line = line.lstrip("• ").strip()
        sample = parse_sample_line(line)
        if sample:
            result["samples"].append(sample)

    return result if result["samples"] else None


def parse_sample_line(line: str) -> dict | None:
    """Parse a single data line like '05-08 10:30: 8,432 步' """
    # Match: "MM-DD HH:mm: VALUE UNIT" or "MM-DD HH:mm（DURATION）: description"
    m = re.match(
        r"(\d{2}-\d{2}\s+\d{2}:\d{2})(?:（[^）]*）)?:\s*(.+)",
        line
    )
    if not m:
        return None

    date_str = m.group(1).strip()
    value_str = m.group(2).strip()

    # Add year (current year)
    year = datetime.now().year
    try:
        sample_date = datetime.strptime(f"{year}-{date_str}", "%Y-%m-%d %H:%M").isoformat()
    except ValueError:
        sample_date = datetime.now().isoformat()

    # Try to extract numeric value and unit
    numeric_m = re.match(r"^([\d,\.]+)\s*(.*)$", value_str)
    if numeric_m:
        num_str = numeric_m.group(1).replace(",", "")
        unit = numeric_m.group(2).strip()
        try:
            value = float(num_str)
        except ValueError:
            value = None
    else:
        value = None
        unit = ""

    return {
        "sample_date": sample_date,
        "value": value,
        "value_str": value_str,
        "unit": unit,
    }


def name_to_identifier(name: str) -> str:
    """Convert Chinese type name to HealthKit identifier."""
    mapping = {
        "步数": "stepCount",
        "心率": "heartRate",
        "心率变异性（HRV）": "heartRateVariabilitySDNN",
        "HRV": "heartRateVariabilitySDNN",
        "血氧饱和度": "oxygenSaturation",
        "活动能量": "activeEnergyBurned",
        "静息能量": "basalEnergyBurned",
        "体重": "bodyMass",
        "BMI": "bodyMassIndex",
        "体脂率": "bodyFatPercentage",
        "身高": "height",
        "步行/跑步距离": "distanceWalkingRunning",
        "骑行距离": "distanceCycling",
        "游泳距离": "distanceSwimming",
        "爬楼层数": "flightsClimbed",
        "收缩压": "bloodPressureSystolic",
        "舒张压": "bloodPressureDiastolic",
        "血糖": "bloodGlucose",
        "体温": "bodyTemperature",
        "基础体温": "basalBodyTemperature",
        "呼吸率": "respiratoryRate",
        "最大摄氧量": "vo2Max",
        "锻炼时间": "appleExerciseTime",
        "站立时间": "appleStandTime",
        "步行速度": "walkingSpeed",
        "跑步速度": "runningSpeed",
        "饮食能量": "dietaryEnergyConsumed",
        "饮水量": "dietaryWater",
        "睡眠分析": "sleepAnalysis",
        "正念冥想": "mindfulSession",
        "运动记录": "workout",
        "心率过高事件": "highHeartRateEvent",
        "心率过低事件": "lowHeartRateEvent",
        "心律不规则": "irregularHeartRhythmEvent",
        "环境噪音": "environmentalAudioExposure",
        "耳机音量": "headphoneAudioExposure",
        "睡眠手腕温度": "appleSleepingWristTemperature",
    }
    # Exact match first
    if name in mapping:
        return mapping[name]
    # Partial match
    for k, v in mapping.items():
        if k in name or name in k:
            return v
    # Fallback: return the name itself
    return name or "unknown"


def ingest(conn: sqlite3.Connection, parsed: dict) -> int:
    """Insert samples into DB, return count inserted."""
    type_id = parsed["type"]
    type_name = parsed["type_name"]
    received_at = parsed["received_at"]
    inserted = 0

    for s in parsed["samples"]:
        # Idempotency: skip if exact same (type, date, value_str) already exists
        existing = conn.execute(
            "SELECT id FROM health_samples WHERE type=? AND sample_date=? AND value_str=?",
            (type_id, s["sample_date"], s["value_str"])
        ).fetchone()
        if existing:
            continue

        conn.execute(
            """INSERT INTO health_samples
               (type, type_name, sample_date, value, value_str, unit, received_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (type_id, type_name, s["sample_date"], s["value"], s["value_str"], s["unit"], received_at)
        )
        inserted += 1

    # Log the sync event
    conn.execute(
        """INSERT INTO sync_log (received_at, type, type_name, count, raw_message)
           VALUES (?, ?, ?, ?, ?)""",
        (received_at, type_id, type_name, len(parsed["samples"]), None)
    )

    conn.commit()
    return inserted


def main():
    # Read message from stdin or argv
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("ERROR: No input provided", file=sys.stderr)
        sys.exit(1)

    # Init DB
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    # Parse
    parsed = parse_message(text)
    if not parsed:
        print("SKIP: Not a health data message or no samples found")
        sys.exit(0)

    # Ingest
    count = ingest(conn, parsed)
    conn.close()

    # Output for the AI to read
    print(f"OK: {count} new samples stored | type={parsed['type']} | name={parsed['type_name']}")


if __name__ == "__main__":
    main()
