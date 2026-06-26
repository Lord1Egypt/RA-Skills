#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


WEEK_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAY_ZH = {
    "Mon": "周一",
    "Tue": "周二",
    "Wed": "周三",
    "Thu": "周四",
    "Fri": "周五",
    "Sat": "周六",
    "Sun": "周日",
}
TYPE_ZH = {
    "hydration": "饮水",
    "mobility": "站立活动",
    "sleep": "睡眠",
    "workout": "运动",
    "supplement": "保健品",
    "general": "提醒",
}


def parse_hhmm(value: str) -> int:
    hour, minute = value.split(":")
    return int(hour) * 60 + int(minute)


def to_hhmm(minutes: int) -> str:
    minutes = minutes % (24 * 60)
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def in_quiet_window(t: int, quiet_start: int, quiet_end: int) -> bool:
    if quiet_start == quiet_end:
        return False
    if quiet_start < quiet_end:
        return quiet_start <= t < quiet_end
    return t >= quiet_start or t < quiet_end


def expand_interval(start: int, end: int, every: int, offset: int = 0) -> list[int]:
    if every <= 0:
        return []
    times: list[int] = []
    current = start + offset
    while current <= end:
        if current >= start:
            times.append(current)
        current += every
    return times


def resolve_profile_days(config: dict[str, Any]) -> dict[str, list[str]]:
    profiles = config.get("profiles", {})
    if not isinstance(profiles, dict):
        return {"default": WEEK_ORDER}
    resolved: dict[str, list[str]] = {}
    for profile, content in profiles.items():
        if isinstance(content, dict) and isinstance(content.get("days"), list):
            days = [d for d in content["days"] if d in WEEK_ORDER]
            if days:
                resolved[profile] = days
    return resolved or {"default": WEEK_ORDER}


def expand_rules(config: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    quiet = config.get("quiet_hours", {})
    quiet_start = parse_hhmm(str(quiet.get("start", "23:59")))
    quiet_end = parse_hhmm(str(quiet.get("end", "00:00")))

    profile_days = resolve_profile_days(config)
    rules = config.get("rules", [])
    if not isinstance(rules, list):
        rules = []

    day_items: dict[str, list[dict[str, str]]] = {day: [] for day in WEEK_ORDER}

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        mode = str(rule.get("mode", "")).strip().lower()
        profile = str(rule.get("profile", "default"))
        days = profile_days.get(profile, WEEK_ORDER)
        r_type = str(rule.get("type", "general"))
        message = str(rule.get("message", "提醒"))
        rule_id = str(rule.get("id", f"{r_type}-rule"))

        times: list[int] = []
        if mode == "fixed":
            raw_times = rule.get("times", [])
            if isinstance(raw_times, list):
                for t in raw_times:
                    try:
                        times.append(parse_hhmm(str(t)))
                    except Exception:
                        pass
        elif mode == "interval":
            try:
                start = parse_hhmm(str(rule["window_start"]))
                end = parse_hhmm(str(rule["window_end"]))
                every = int(rule["every_minutes"])
                offset = int(rule.get("offset_minutes", 0))
            except Exception:
                continue
            if end < start:
                # Split across midnight
                times = expand_interval(start, 24 * 60 - 1, every, offset) + expand_interval(0, end, every, 0)
            else:
                times = expand_interval(start, end, every, offset)
        else:
            continue

        for day in days:
            for t in sorted(set(times)):
                if in_quiet_window(t, quiet_start, quiet_end):
                    continue
                day_items[day].append(
                    {
                        "time": to_hhmm(t),
                        "type": r_type,
                        "message": message,
                        "rule_id": rule_id,
                    }
                )

    for day in WEEK_ORDER:
        day_items[day].sort(key=lambda x: x["time"])
    return day_items


def build_markdown(config: dict[str, Any], day_items: dict[str, list[dict[str, str]]]) -> str:
    tz = str(config.get("timezone", "本地时区"))
    lines: list[str] = [
        "# 复杂提醒时间表",
        "",
        f"- 时区: {tz}",
        "",
        "## 每周时间表",
    ]

    type_counts = defaultdict(int)
    for day in WEEK_ORDER:
        items = day_items.get(day, [])
        lines.append("")
        lines.append(f"### {WEEKDAY_ZH.get(day, day)}")
        if not items:
            lines.append("- （无提醒）")
            continue
        for item in items:
            tzh = TYPE_ZH.get(item["type"], item["type"])
            lines.append(f"- {item['time']} | {tzh} | {item['message']} ({item['rule_id']})")
            type_counts[tzh] += 1

    lines.extend(["", "## 每周提醒统计"])
    if not type_counts:
        lines.append("- 未生成提醒")
    else:
        for key in sorted(type_counts.keys()):
            lines.append(f"- {key}: {type_counts[key]}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reminder timetable markdown from complex schedule JSON.")
    parser.add_argument("--input", required=True, help="Input schedule JSON file")
    parser.add_argument("--output", help="Output markdown file (default: stdout)")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    day_items = expand_rules(data)
    output = build_markdown(data, day_items)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
