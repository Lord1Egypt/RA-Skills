# 模块说明：
# - skill 内部共享的时间解析和学期节律特征工具。
# - 支撑时间判断和检索打标。

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Dict


WEEKDAY_MAP = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

WEEKDAY_HINTS = {
    "星期一": "Monday",
    "星期二": "Tuesday",
    "星期三": "Wednesday",
    "星期四": "Thursday",
    "星期五": "Friday",
    "星期六": "Saturday",
    "星期日": "Sunday",
    "星期天": "Sunday",
    "周一": "Monday",
    "周二": "Tuesday",
    "周三": "Wednesday",
    "周四": "Thursday",
    "周五": "Friday",
    "周六": "Saturday",
    "周日": "Sunday",
    "周天": "Sunday",
}

SPRING_FESTIVAL_RANGES = {
    2024: (date(2024, 2, 10), date(2024, 2, 17)),
    2025: (date(2025, 1, 28), date(2025, 2, 4)),
    2026: (date(2026, 2, 17), date(2026, 2, 24)),
    2027: (date(2027, 2, 6), date(2027, 2, 13)),
}

WINTER_VACATION_RANGES = {
    2024: (date(2024, 1, 15), date(2024, 2, 25)),
    2025: (date(2025, 1, 15), date(2025, 2, 25)),
    2026: (date(2026, 1, 15), date(2026, 2, 25)),
    2027: (date(2027, 1, 15), date(2027, 2, 25)),
}

SUMMER_VACATION_RANGES = {
    2024: (date(2024, 7, 1), date(2024, 8, 31)),
    2025: (date(2025, 7, 1), date(2025, 8, 31)),
    2026: (date(2026, 7, 1), date(2026, 8, 31)),
    2027: (date(2027, 7, 1), date(2027, 8, 31)),
}

FULLWIDTH_COLON = "\uff1a"
WEEKDAY_PATTERN = re.compile(
    "|".join(sorted((re.escape(token) for token in WEEKDAY_HINTS), key=len, reverse=True))
)


def normalize_timestamp_text(text: str) -> str:
    normalized = (text or "").strip().replace(FULLWIDTH_COLON, ":")
    normalized = normalized.replace("T", " ")
    normalized = WEEKDAY_PATTERN.sub(" ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def infer_weekday(text: str, dt: datetime) -> str:
    for token, label in WEEKDAY_HINTS.items():
        if token in text:
            return label
    return WEEKDAY_MAP[dt.weekday()]


def infer_time_bucket(hour: int) -> str:
    if 0 <= hour < 6:
        return "late_night"
    if 6 <= hour < 9:
        return "early_morning"
    if 9 <= hour < 12:
        return "morning"
    if 12 <= hour < 14:
        return "noon"
    if 14 <= hour < 18:
        return "afternoon"
    if 18 <= hour < 22:
        return "evening"
    return "late_night"


def parse_timestamp(text: str) -> datetime:
    normalized = normalize_timestamp_text(text)
    patterns = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
    ]
    for pattern in patterns:
        try:
            return datetime.strptime(normalized, pattern)
        except ValueError:
            continue
    raise ValueError(
        "Unable to parse timestamp. Expected formats like '2026-03-18 周三 08:59' or '2026-03-18 23:40:00'."
    )


def _date_in_range(day: date, ranges: Dict[int, tuple[date, date]]) -> bool:
    current_range = ranges.get(day.year)
    if current_range is None:
        return False
    start, end = current_range
    return start <= day <= end


def infer_holiday_label(day: date) -> str:
    if _date_in_range(day, SPRING_FESTIVAL_RANGES):
        return "spring_festival"
    if day.month == 5 and 1 <= day.day <= 5:
        return "labor_day"
    if day.month == 10 and 1 <= day.day <= 7:
        return "national_day"
    if _date_in_range(day, WINTER_VACATION_RANGES):
        return "winter_vacation"
    if _date_in_range(day, SUMMER_VACATION_RANGES):
        return "summer_vacation"
    return "none"


def infer_school_holiday_hint(holiday_label: str) -> bool:
    return holiday_label in {
        "spring_festival",
        "labor_day",
        "national_day",
        "winter_vacation",
        "summer_vacation",
    }


def build_time_feature_payload(timestamp_text: str, timezone: str = "Asia/Shanghai") -> Dict[str, object]:
    dt = parse_timestamp(timestamp_text)
    weekday = infer_weekday(timestamp_text, dt)
    holiday_label = infer_holiday_label(dt.date())
    return {
        "local_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": timezone,
        "weekday": weekday,
        "is_weekend": weekday in {"Saturday", "Sunday"},
        "is_late_night": dt.hour < 6 or dt.hour >= 22,
        "time_bucket": infer_time_bucket(dt.hour),
        "holiday_label": holiday_label,
        "school_holiday_hint": infer_school_holiday_hint(holiday_label),
    }
