#!/usr/bin/env python3
"""
tz_offset.py — 从时区名获取 UTC 偏移量 / Get UTC offset from timezone name.

Usage:
    python3 tz_offset.py Asia/Shanghai
    python3 tz_offset.py America/New_York
    python3 tz_offset.py Europe/London

Output (stdout):
    {"timezone": "Asia/Shanghai", "offset_hours": 8, "offset_str": "+08:00"}

Errors:
    If timezone is not found or invalid, exits with code 1 and prints error to stderr.
    JSON is always on stdout for reliable parsing.

Requires Python 3.9+ (zoneinfo is stdlib since 3.9).
On some platforms (especially Windows), the 'tzdata' package may be needed.
"""

import json
import sys
from datetime import datetime, timezone, timedelta

try:
    from zoneinfo import ZoneInfo, available_timezones
except ImportError:
    # Python < 3.9 fallback
    print(json.dumps({"error": "zoneinfo not available. Python 3.9+ required."}))
    sys.exit(1)


def get_offset(timezone_name: str) -> dict:
    """Calculate UTC offset for a given timezone name."""
    try:
        tz = ZoneInfo(timezone_name)
    except (KeyError, TypeError):
        return {"error": f"Unknown timezone: {timezone_name}"}

    now = datetime.now(tz)
    utc_offset = now.utcoffset()
    if utc_offset is None:
        return {"error": f"Cannot determine offset for {timezone_name}"}

    total_seconds = int(utc_offset.total_seconds())
    offset_hours = total_seconds / 3600

    # Format as +/-HH:MM
    sign = "+" if total_seconds >= 0 else "-"
    abs_seconds = abs(total_seconds)
    hours = abs_seconds // 3600
    minutes = (abs_seconds % 3600) // 60
    offset_str = f"{sign}{hours:02d}:{minutes:02d}"

    return {
        "timezone": timezone_name,
        "offset_hours": offset_hours,
        "offset_str": offset_str,
    }


def suggest_timezone() -> list:
    """Try to detect system timezone and return likely candidates."""
    import subprocess
    import os

    candidates = []

    # macOS
    try:
        result = subprocess.run(
            ["systemsetup", "-gettimezone"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            tz = result.stdout.strip().replace("Time Zone: ", "")
            if tz:
                candidates.append(tz)
    except Exception:
        pass

    # Linux (timedatectl)
    try:
        result = subprocess.run(
            ["timedatectl", "show", "--value", "-p", "Timezone"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            tz = result.stdout.strip()
            if tz:
                candidates.append(tz)
    except Exception:
        pass

    # /etc/localtime (macOS/Linux)
    try:
        if os.path.exists("/etc/localtime"):
            link = os.readlink("/etc/localtime")
            # Extract like "Asia/Shanghai" from ".../usr/share/zoneinfo/Asia/Shanghai"
            parts = link.split("/usr/share/zoneinfo/")
            if len(parts) > 1:
                candidates.append(parts[-1])
    except Exception:
        pass

    # /etc/timezone (Linux)
    try:
        with open("/etc/timezone") as f:
            tz = f.read().strip()
            if tz:
                candidates.append(tz)
    except Exception:
        pass

    return candidates


if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = get_offset(sys.argv[1])
        if "error" in result:
            print(json.dumps(result))
            sys.exit(1)
        print(json.dumps(result))
    else:
        # No arg: print system-suggested timezone(s) + help
        detected = suggest_timezone()
        info = {
            "usage": "python3 tz_offset.py <timezone_name>",
            "examples": ["Asia/Shanghai", "America/New_York", "Europe/London"],
            "detected_timezones": detected,
            "all_timezones_count": len(available_timezones()),
        }
        print(json.dumps(info, indent=2))
