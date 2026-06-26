from datetime import datetime, timedelta, timezone

# 简化映射：固定 UTC 偏移（bug：忽略了 DST）
_FIXED_OFFSETS = {
    "UTC": 0,
    "America/New_York": -5,  # EST，但 EDT 是 -4
    "Asia/Shanghai": 8,
}


def local_to_utc(naive_dt: datetime, tz_name: str) -> datetime:
    off = _FIXED_OFFSETS[tz_name]
    return (naive_dt - timedelta(hours=off)).replace(tzinfo=timezone.utc)


def utc_to_local(utc_dt: datetime, tz_name: str) -> datetime:
    off = _FIXED_OFFSETS[tz_name]
    return (utc_dt.astimezone(timezone.utc) + timedelta(hours=off)).replace(tzinfo=None)
