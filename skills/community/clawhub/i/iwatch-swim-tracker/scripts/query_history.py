#!/usr/bin/env python3
"""查询游泳训练历史数据，用于趋势分析和周对比。

用法:
  query_history.py                  # 默认查最近 14 天
  query_history.py --days 30        # 查最近 30 天
  query_history.py --weeks 4        # 按周汇总最近 4 周
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "swim_data"


def load_sessions(start_date: datetime, end_date: datetime) -> list[dict]:
    """加载指定日期范围内的所有训练记录。"""
    sessions = []
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        year = current.strftime("%Y")
        month = current.strftime("%m")
        file_path = DATA_DIR / year / month / f"{date_str}.json"
        if file_path.exists():
            data = json.loads(file_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                sessions.extend(data)
            else:
                sessions.append(data)
        current += timedelta(days=1)
    return sessions


def compute_stats(sessions: list[dict]) -> dict:
    """计算一组训练的统计指标。"""
    if not sessions:
        return {
            "count": 0,
            "total_distance": 0,
            "avg_distance": 0,
            "avg_pace_seconds": 0,
            "avg_heart_rate": 0,
            "total_calories": 0,
            "total_duration_seconds": 0,
        }

    total_distance = sum(s.get("total_distance", 0) for s in sessions)
    paces = [s["avg_pace_seconds"] for s in sessions if s.get("avg_pace_seconds")]
    hrs = [s["avg_heart_rate"] for s in sessions if s.get("avg_heart_rate")]
    cals = sum(s.get("calories", 0) for s in sessions)
    durations = sum(s.get("duration_seconds", 0) for s in sessions)

    return {
        "count": len(sessions),
        "total_distance": total_distance,
        "avg_distance": round(total_distance / len(sessions)),
        "avg_pace_seconds": round(sum(paces) / len(paces)) if paces else 0,
        "avg_heart_rate": round(sum(hrs) / len(hrs)) if hrs else 0,
        "total_calories": cals,
        "total_duration_seconds": durations,
    }


def week_range(ref_date: datetime, weeks_ago: int) -> tuple[datetime, datetime]:
    """返回 ref_date 所在周往前 weeks_ago 周的周一到周日。"""
    # 找到 ref_date 所在周的周一
    monday = ref_date - timedelta(days=ref_date.weekday())
    target_monday = monday - timedelta(weeks=weeks_ago)
    target_sunday = target_monday + timedelta(days=6)
    return target_monday, target_sunday


def weekly_comparison(ref_date: datetime, num_weeks: int = 4) -> list[dict]:
    """生成最近 N 周的周度统计。"""
    weeks = []
    for i in range(num_weeks):
        start, end = week_range(ref_date, i)
        sessions = load_sessions(start, end)
        stats = compute_stats(sessions)
        stats["week_start"] = start.strftime("%Y-%m-%d")
        stats["week_end"] = end.strftime("%Y-%m-%d")
        stats["label"] = "本周" if i == 0 else f"{i}周前"
        weeks.append(stats)
    return weeks


def trend_analysis(ref_date: datetime, days: int = 14) -> dict:
    """最近 N 天的趋势分析。"""
    start = ref_date - timedelta(days=days - 1)
    sessions = load_sessions(start, ref_date)

    if len(sessions) < 2:
        return {
            "sessions": [summarize(s) for s in sessions],
            "trend": "insufficient_data",
        }

    # 按日期排序
    sessions.sort(key=lambda s: (s.get("date", ""), s.get("time_range", "")))

    # 前半 vs 后半对比
    mid = len(sessions) // 2
    first_half = compute_stats(sessions[:mid])
    second_half = compute_stats(sessions[mid:])

    def delta(key):
        a, b = first_half[key], second_half[key]
        if a == 0:
            return 0
        return round((b - a) / a * 100, 1)

    return {
        "period_days": days,
        "total_sessions": len(sessions),
        "sessions": [summarize(s) for s in sessions],
        "overall": compute_stats(sessions),
        "trend": {
            "distance_change_pct": delta("avg_distance"),
            "pace_change_pct": delta("avg_pace_seconds"),
            "heart_rate_change_pct": delta("avg_heart_rate"),
            "note": "负值表示下降/更快（配速负值=进步）",
        },
    }


def summarize(session: dict) -> dict:
    """提取单次训练的摘要字段。"""
    return {
        "date": session.get("date"),
        "time_range": session.get("time_range"),
        "total_distance": session.get("total_distance"),
        "duration": session.get("duration"),
        "avg_pace": session.get("avg_pace"),
        "avg_pace_seconds": session.get("avg_pace_seconds"),
        "avg_heart_rate": session.get("avg_heart_rate"),
        "calories": session.get("calories"),
        "strokes": session.get("strokes"),
    }


def main():
    parser = argparse.ArgumentParser(description="查询游泳训练历史")
    parser.add_argument("--days", type=int, default=14, help="查询最近 N 天（默认 14）")
    parser.add_argument("--weeks", type=int, default=4, help="周对比的周数（默认 4）")
    parser.add_argument("--date", type=str, default=None, help="参考日期 YYYY-MM-DD（默认今天）")
    args = parser.parse_args()

    ref_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.now()

    result = {
        "ref_date": ref_date.strftime("%Y-%m-%d"),
        "trend": trend_analysis(ref_date, args.days),
        "weekly": weekly_comparison(ref_date, args.weeks),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
