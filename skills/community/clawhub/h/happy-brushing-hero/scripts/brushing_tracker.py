#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📅 刷牙俠打卡紀錄 — 每日刷牙記錄、星級評價、連續天數、週報表

資料檔：~/.bookshelf-plus/kids/brushing_log.json

星級評價（刷牙俠標準）：
    刷夠 2 分鐘  = ⭐⭐⭐⭐⭐
    刷夠 90 秒   = ⭐⭐⭐⭐
    刷夠 60 秒   = ⭐⭐⭐

用法：
    python3 brushing_tracker.py --report    # 本週報表
    python3 brushing_tracker.py --streak    # 連續刷牙天數
    python3 brushing_tracker.py --stars     # 星級標準
"""

import datetime as dt
import json
import os
import sys

DATA_DIR = os.path.expanduser("~/.bookshelf-plus/kids")
LOG_FILE = os.path.join(DATA_DIR, "brushing_log.json")


def _ensure():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_log():
    """讀取全部刷牙記錄（list[dict]）。"""
    _ensure()
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_log(records):
    _ensure()
    tmp = LOG_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    os.replace(tmp, LOG_FILE)


def rate_duration(seconds):
    """依秒數給刷牙俠星級（1-5 星）。"""
    if seconds >= 120:
        return 5
    if seconds >= 90:
        return 4
    if seconds >= 60:
        return 3
    if seconds >= 30:
        return 2
    return 1


def auto_session(now=None):
    now = now or dt.datetime.now()
    return "上午" if now.hour < 12 else "下午"


def record_brushing(who="寶貝", duration=120, session=None, now=None):
    """寫入一筆刷牙記錄，回傳記錄（含 streak）。"""
    now = now or dt.datetime.now()
    session = session or auto_session(now)
    records = load_log()
    rec = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "who": who,
        "duration": int(duration),
        "session": session,
        "stars": rate_duration(duration),
    }
    records.append(rec)
    save_log(records)
    rec["streak"] = get_streak(records, date=rec["date"])
    return rec


def records_on(records, date_str):
    return [r for r in records if r.get("date") == date_str]


def brushed_today(records=None, session=None, date_str=None):
    """今天（或指定日期）是否刷過；session 指定時只看該時段。"""
    records = records if records is not None else load_log()
    date_str = date_str or dt.date.today().isoformat()
    day = records_on(records, date_str)
    if session:
        return any(r.get("session") == session for r in day)
    return len(day) > 0


def today_count(records=None):
    """今天刷了幾次。"""
    records = records if records is not None else load_log()
    return len(records_on(records, dt.date.today().isoformat()))


def get_streak(records=None, date=None):
    """連續刷牙天數：從 date（預設今天）往前數連續有刷的天數。
    今天還沒刷時從昨天起算，不因今天未刷而歸零。"""
    records = records if records is not None else load_log()
    if date is None:
        date = dt.date.today()
    elif isinstance(date, str):
        date = dt.date.fromisoformat(date)
    days = {r.get("date") for r in records if r.get("date")}
    streak = 0
    d = date
    if d.isoformat() not in days:
        d -= dt.timedelta(days=1)
    while d.isoformat() in days:
        streak += 1
        d -= dt.timedelta(days=1)
    return streak


def weekly_report(records=None, date=None):
    """本週報表：刷了幾次、有刷的日子、全勤天數（一天刷 2 次以上）、最佳星級。"""
    records = records if records is not None else load_log()
    if date is None:
        date = dt.date.today()
    elif isinstance(date, str):
        date = dt.date.fromisoformat(date)
    monday = date - dt.timedelta(days=date.weekday())
    week_records = []
    for i in range(7):
        d = (monday + dt.timedelta(days=i)).isoformat()
        week_records.extend(records_on(records, d))
    day_counts = {}
    for r in week_records:
        day_counts[r["date"]] = day_counts.get(r["date"], 0) + 1
    best_stars = max([r.get("stars", 1) for r in week_records], default=0)
    return {
        "week_start": monday.isoformat(),
        "week_end": (monday + dt.timedelta(days=6)).isoformat(),
        "total_brushes": len(week_records),
        "active_days": len(day_counts),
        "full_attendance_days": sum(1 for c in day_counts.values() if c >= 2),
        "best_stars": best_stars,
        "days": sorted(day_counts.items()),
    }


def report_text(report, who="寶貝"):
    """把週報表變成好讀（且適合同樂）的文字。"""
    stars = "⭐" * report["best_stars"] if report["best_stars"] else "—"
    return (
        f"📊 {who} 本週刷牙報表（{report['week_start']} ~ {report['week_end']}）：\n"
        f"這週刷了 {report['total_brushes']} 次，有刷的日子 {report['active_days']} 天，"
        f"早晚都刷的全勤天數 {report['full_attendance_days']} 天，最佳星級 {stars}！\n"
        f"{who} 好棒！我們下週繼續加油！💪"
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--report" in args:
        print(report_text(weekly_report()))
    elif "--streak" in args:
        print(f"🎉 已連續刷牙 {get_streak()} 天！繼續保持！")
    elif "--stars" in args:
        print("刷牙俠星級評價：")
        print("刷夠 2 分鐘 = ⭐⭐⭐⭐⭐")
        print("刷夠 90 秒  = ⭐⭐⭐⭐")
        print("刷夠 60 秒  = ⭐⭐⭐")
    else:
        print(__doc__.strip())
