"""时间工具：可配置时区 + 时间戳/日期辅助。

Python >=3.9 用标准库 zoneinfo；3.8 回退到固定偏移（仅覆盖常见时区）。
"""

from datetime import datetime, timedelta, timezone

# 常见时区的 UTC 偏移（小时）。Python 3.8 无 zoneinfo 时用作回退。
_FALLBACK_OFFSETS = {
    "UTC": 0,
    "Etc/UTC": 0,
    "Asia/Shanghai": 8,
    "Asia/Hong_Kong": 8,
    "Asia/Singapore": 8,
    "Asia/Tokyo": 9,
    "America/New_York": -5,
    "America/Los_Angeles": -8,
    "Europe/London": 0,
}


def get_tz(name="Asia/Shanghai"):
    """返回给定时区名的 tzinfo 对象。"""
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+
        return ZoneInfo(name)
    except Exception:
        offset = _FALLBACK_OFFSETS.get(name, 8)
        return timezone(timedelta(hours=offset))


def now(tz="Asia/Shanghai"):
    return datetime.now(get_tz(tz))


def now_iso(tz="Asia/Shanghai"):
    return now(tz).isoformat()


def today_str(tz="Asia/Shanghai"):
    return now(tz).strftime("%Y-%m-%d")
