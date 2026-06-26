"""
schemas.py — L3 data structures and validation

Responsibilities:
- Date format validation
- Error type definitions
- Version number constants
- Timezone detection
"""

import re
import os
from datetime import datetime, date

CURRENT_VERSION = "v1.3.1"
def get_client_timezone() -> str:
    """
    Get the client's timezone.
    First checks AINEWS_CLIENT_TIMEZONE environment variable.
    Falls back to local system timezone.
    """
    # Check env var first
    env_tz = os.getenv("AINEWS_CLIENT_TIMEZONE")
    if env_tz:
        return env_tz

    # Try to get local timezone
    try:
        import zoneinfo
        local_tz = zoneinfo.ZoneInfo("localtime")
        return str(local_tz.key) if hasattr(local_tz, 'key') else str(local_tz)
    except (ImportError, Exception):
        try:
            import tzlocal
            return str(tzlocal.get_localzone())
        except (ImportError, Exception):
            # Fall back to Asia/Shanghai as default
            return "Asia/Shanghai"


def get_local_today() -> str:
    """
    Get today's date in the client's local timezone (YYYY-MM-DD).
    """
    tz_name = get_client_timezone()
    try:
        import zoneinfo
        tz = zoneinfo.ZoneInfo(tz_name)
        now = datetime.now(tz)
        return now.date().isoformat()
    except (ImportError, Exception):
        # Fall back to system local date
        return date.today().isoformat()


class L3Error(Exception):
    pass


class VersionError(L3Error):
    pass


class NetworkError(L3Error):
    pass


class CacheError(L3Error):
    pass


def validate_date(date_str: str) -> str | None:
    """Validate date format YYYY-MM-DD, return error message or None"""
    if not date_str:
        return None
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return f"Invalid date format, must be YYYY-MM-DD, got: {date_str}"
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return f"Invalid date: {date_str}"
    return None


def get_today() -> str:
    """Get today's date in YYYY-MM-DD format"""
    return date.today().isoformat()
