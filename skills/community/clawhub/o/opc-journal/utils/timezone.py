"""Timezone utilities for opc-journal."""
from datetime import datetime
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE = "Asia/Shanghai"


def now_tz(tz_name: str = DEFAULT_TIMEZONE) -> datetime:
    """Return timezone-aware current time."""
    return datetime.now(ZoneInfo(tz_name))


def iso_now(tz_name: str = DEFAULT_TIMEZONE) -> str:
    """Return ISO-formatted timezone-aware current time."""
    return now_tz(tz_name).isoformat()


def parse_iso_with_tz(iso_string: str, tz_name: str = DEFAULT_TIMEZONE) -> datetime:
    """Parse ISO string, adding timezone if naive."""
    if iso_string.endswith("Z"):
        iso_string = iso_string[:-1] + "+00:00"
    dt = datetime.fromisoformat(iso_string)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(tz_name))
    return dt
