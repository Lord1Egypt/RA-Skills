#!/usr/bin/env python3
"""
Apple Health Sync — query.py
Query stored health data from SQLite for OpenClaw AI responses.

Usage:
    python3 query.py --status
    python3 query.py --type stepCount --period today
    python3 query.py --type heartRate --period week
    python3 query.py --summary --period today
    python3 query.py --summary --period week
    python3 query.py --summary --period month
    python3 query.py --list-types
"""

import sys
import json
import sqlite3
import argparse
from datetime import datetime, timedelta, timezone, date
from pathlib import Path

DB_PATH = Path.home() / ".apple-health-sync" / "health.db"

PERIOD_LABELS = {
    "today": "今天",
    "yesterday": "昨天",
    "week": "本周",
    "month": "本月",
    "all": "全部",
}

# Friendly Chinese name + unit for each type
TYPE_META = {
    "stepCount":                   ("步数",        "步"),
    "heartRate":                   ("心率",        "bpm"),
    "heartRateVariabilitySDNN":    ("HRV",         "ms"),
    "oxygenSaturation":            ("血氧",        "%"),
    "activeEnergyBurned":          ("活动能量",    "千卡"),
    "basalEnergyBurned":           ("静息能量",    "千卡"),
    "bodyMass":                    ("体重",        "kg"),
    "bodyMassIndex":               ("BMI",         ""),
    "bodyFatPercentage":           ("体脂率",      "%"),
    "height":                      ("身高",        "cm"),
    "distanceWalkingRunning":      ("步行距离",    "km"),
    "distanceCycling":             ("骑行距离",    "km"),
    "flightsClimbed":              ("爬楼",        "层"),
    "bloodPressureSystolic":       ("收缩压",      "mmHg"),
    "bloodPressureDiastolic":      ("舒张压",      "mmHg"),
    "bloodGlucose":                ("血糖",        "mg/dL"),
    "bodyTemperature":             ("体温",        "°C"),
    "respiratoryRate":             ("呼吸率",      "次/分"),
    "vo2Max":                      ("最大摄氧量",  "ml/kg·min"),
    "appleExerciseTime":           ("锻炼时间",    "分钟"),
    "appleStandTime":              ("站立时间",    "分钟"),
    "walkingSpeed":                ("步行速度",    "km/h"),
    "runningSpeed":                ("跑步速度",    "km/h"),
    "dietaryEnergyConsumed":       ("饮食能量",    "千卡"),
    "dietaryWater":                ("饮水量",      "ml"),
    "sleepAnalysis":               ("睡眠",        ""),
    "mindfulSession":              ("正念",        "分钟"),
    "workout":                     ("运动记录",    ""),
    "environmentalAudioExposure":  ("环境噪音",    "dB"),
    "headphoneAudioExposure":      ("耳机音量",    "dB"),
    "appleSleepingWristTemperature": ("睡眠手腕温度", "°C"),
    "highHeartRateEvent":          ("心率过高",    ""),
    "lowHeartRateEvent":           ("心率过低",    ""),
    "irregularHeartRhythmEvent":   ("心律不规则",  ""),
}

# Types that are SUMMED (not averaged) over a period
SUM_TYPES = {
    "stepCount", "activeEnergyBurned", "basalEnergyBurned",
    "flightsClimbed", "distanceWalkingRunning", "distanceCycling",
    "distanceSwimming", "dietaryEnergyConsumed", "dietaryWater",
    "appleExerciseTime", "appleStandTime",
}


def get_date_range(period: str) -> tuple[str, str]:
    today = date.today()
    if period == "today":
        start = today
        end = today
    elif period == "yesterday":
        start = today - timedelta(days=1)
        end = today - timedelta(days=1)
    elif period == "week":
        start = today - timedelta(days=today.weekday())  # Monday
        end = today
    elif period == "month":
        start = today.replace(day=1)
        end = today
    else:  # all
        return "1970-01-01", "2999-12-31"

    return start.isoformat(), end.isoformat()


def open_db() -> sqlite3.Connection | None:
    if not DB_PATH.exists():
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def cmd_status(conn: sqlite3.Connection):
    total = conn.execute("SELECT COUNT(*) FROM health_samples").fetchone()[0]
    types = conn.execute(
        "SELECT COUNT(DISTINCT type) FROM health_samples"
    ).fetchone()[0]
    last = conn.execute(
        "SELECT MAX(received_at) FROM sync_log"
    ).fetchone()[0]
    oldest = conn.execute(
        "SELECT MIN(sample_date) FROM health_samples"
    ).fetchone()[0]
    newest = conn.execute(
        "SELECT MAX(sample_date) FROM health_samples"
    ).fetchone()[0]

    print(json.dumps({
        "status": "ok",
        "total_samples": total,
        "type_count": types,
        "last_sync": last,
        "data_from": oldest,
        "data_to": newest,
        "db_path": str(DB_PATH),
    }, ensure_ascii=False, indent=2))


def cmd_list_types(conn: sqlite3.Connection):
    rows = conn.execute("""
        SELECT type, type_name, COUNT(*) as cnt,
               MIN(sample_date) as first_date,
               MAX(sample_date) as last_date
        FROM health_samples
        GROUP BY type
        ORDER BY cnt DESC
    """).fetchall()

    result = []
    for row in rows:
        meta = TYPE_META.get(row["type"], (row["type_name"] or row["type"], ""))
        result.append({
            "type": row["type"],
            "name": meta[0],
            "count": row["cnt"],
            "from": row["first_date"],
            "to": row["last_date"],
        })

    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_query_type(conn: sqlite3.Connection, type_id: str, period: str):
    start, end = get_date_range(period)
    meta = TYPE_META.get(type_id, (type_id, ""))
    name, unit = meta

    rows = conn.execute("""
        SELECT sample_date, value, value_str, unit
        FROM health_samples
        WHERE type = ? AND date(sample_date) BETWEEN ? AND ?
        ORDER BY sample_date ASC
    """, (type_id, start, end)).fetchall()

    if not rows:
        print(json.dumps({
            "type": type_id,
            "name": name,
            "period": period,
            "period_label": PERIOD_LABELS.get(period, period),
            "count": 0,
            "data": [],
            "message": f"{PERIOD_LABELS.get(period, period)}没有{name}数据",
        }, ensure_ascii=False, indent=2))
        return

    values = [r["value"] for r in rows if r["value"] is not None]

    stats = {}
    if values:
        if type_id in SUM_TYPES:
            stats["total"] = round(sum(values), 2)
        else:
            stats["avg"] = round(sum(values) / len(values), 2)
            stats["min"] = round(min(values), 2)
            stats["max"] = round(max(values), 2)
            stats["latest"] = round(values[-1], 2)

    samples = [
        {"time": r["sample_date"], "value": r["value"], "display": r["value_str"]}
        for r in rows[-20:]  # last 20 samples max
    ]

    print(json.dumps({
        "type": type_id,
        "name": name,
        "unit": unit,
        "period": period,
        "period_label": PERIOD_LABELS.get(period, period),
        "count": len(rows),
        "stats": stats,
        "samples": samples,
    }, ensure_ascii=False, indent=2))


def cmd_summary(conn: sqlite3.Connection, period: str):
    start, end = get_date_range(period)
    period_label = PERIOD_LABELS.get(period, period)

    # Key metrics to include in summary
    summary_types = [
        "stepCount", "activeEnergyBurned", "heartRate",
        "heartRateVariabilitySDNN", "oxygenSaturation",
        "bodyMass", "sleepAnalysis", "appleExerciseTime",
        "distanceWalkingRunning", "respiratoryRate",
        "bloodPressureSystolic", "bloodGlucose",
    ]

    result = {
        "period": period,
        "period_label": period_label,
        "from": start,
        "to": end,
        "metrics": {},
    }

    for type_id in summary_types:
        rows = conn.execute("""
            SELECT value, value_str
            FROM health_samples
            WHERE type = ? AND date(sample_date) BETWEEN ? AND ?
        """, (type_id, start, end)).fetchall()

        if not rows:
            continue

        meta = TYPE_META.get(type_id, (type_id, ""))
        name, unit = meta
        values = [r["value"] for r in rows if r["value"] is not None]

        if not values:
            continue

        if type_id in SUM_TYPES:
            metric_val = round(sum(values), 1)
            label = f"{metric_val} {unit}".strip()
        else:
            metric_val = round(sum(values) / len(values), 1)
            label = f"{metric_val} {unit}（均值）".strip()

        result["metrics"][type_id] = {
            "name": name,
            "unit": unit,
            "value": metric_val,
            "display": label,
            "samples": len(values),
        }

    # Also check recent sync
    last_sync = conn.execute(
        "SELECT MAX(received_at) FROM sync_log"
    ).fetchone()[0]
    result["last_sync"] = last_sync

    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Query Apple Health data")
    parser.add_argument("--status", action="store_true", help="Show DB status")
    parser.add_argument("--list-types", action="store_true", help="List all available data types")
    parser.add_argument("--type", help="HealthKit type identifier (e.g. stepCount)")
    parser.add_argument("--period", default="today",
                        choices=["today", "yesterday", "week", "month", "all"],
                        help="Time period")
    parser.add_argument("--summary", action="store_true", help="Generate multi-metric summary")
    args = parser.parse_args()

    conn = open_db()
    if conn is None:
        print(json.dumps({
            "error": "数据库不存在",
            "message": "还没有收到任何健康数据。请确认 iOS App 已配置并连接到 OpenClaw。",
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.status:
        cmd_status(conn)
    elif args.list_types:
        cmd_list_types(conn)
    elif args.summary:
        cmd_summary(conn, args.period)
    elif args.type:
        cmd_query_type(conn, args.type, args.period)
    else:
        # Default: show today's summary
        cmd_summary(conn, "today")

    conn.close()


if __name__ == "__main__":
    main()
