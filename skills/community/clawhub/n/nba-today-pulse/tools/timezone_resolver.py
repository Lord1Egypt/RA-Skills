#!/usr/bin/env python3
"""Timezone parsing and resolution for NBA_TR."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

try:
    from .nba_common import NBAReportError
except ImportError:  # pragma: no cover - script execution path
    from nba_common import NBAReportError

ENV_TZ_KEYS = (
    "OPENCLAW_USER_TIMEZONE",
    "OPENCLAW_TIMEZONE",
    "USER_TIMEZONE",
    "TZ",
)

CITY_TIMEZONE_MAP = {
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "hong kong": "Asia/Hong_Kong",
    "singapore": "Asia/Singapore",
    "tokyo": "Asia/Tokyo",
    "seoul": "Asia/Seoul",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "san francisco": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "denver": "America/Denver",
    "phoenix": "America/Phoenix",
    "toronto": "America/Toronto",
    "vancouver": "America/Vancouver",
    "北京": "Asia/Shanghai",
    "上海": "Asia/Shanghai",
    "香港": "Asia/Hong_Kong",
    "新加坡": "Asia/Singapore",
    "东京": "Asia/Tokyo",
    "首尔": "Asia/Seoul",
    "伦敦": "Europe/London",
    "巴黎": "Europe/Paris",
    "柏林": "Europe/Berlin",
    "纽约": "America/New_York",
    "洛杉矶": "America/Los_Angeles",
    "旧金山": "America/Los_Angeles",
    "芝加哥": "America/Chicago",
    "丹佛": "America/Denver",
    "菲尼克斯": "America/Phoenix",
    "多伦多": "America/Toronto",
    "温哥华": "America/Vancouver",
}

IANA_PATTERN = re.compile(r"\b(?:[A-Za-z_]+/[A-Za-z_]+(?:/[A-Za-z_]+)?)\b")
OFFSET_PATTERN = re.compile(r"(?<!\d)\b(?:UTC|GMT)?\s*([+-]\d{1,2})(?::?(\d{2}))?\b", re.IGNORECASE)


@dataclass(frozen=True)
class ResolvedTimezone:
    name: str
    tzinfo: timezone | ZoneInfo
    source: str


def _fixed_offset_timezone(hours_text: str, minutes_text: str | None) -> ResolvedTimezone | None:
    sign = -1 if hours_text.startswith("-") else 1
    hours = abs(int(hours_text))
    minutes = int(minutes_text or "0")
    if hours > 14 or minutes > 59:
        return None
    delta = timedelta(hours=hours, minutes=minutes) * sign
    name = f"UTC{hours_text}{':' + minutes_text if minutes_text else ':00'}"
    return ResolvedTimezone(name=name, tzinfo=timezone(delta, name=name), source="offset")


def _resolve_iana(name: str, source: str) -> ResolvedTimezone | None:
    try:
        zone = ZoneInfo(name)
    except ZoneInfoNotFoundError:
        return None
    return ResolvedTimezone(name=name, tzinfo=zone, source=source)


def canonical_timezone_name(resolved: ResolvedTimezone | None) -> str | None:
    """Return the canonical long-term timezone name when one exists.

    Region-based IANA timezones are the only preferred canonical storage form.
    Fixed UTC offsets remain valid for the current request, but should not
    displace an existing IANA timezone preference.
    """

    if resolved and isinstance(resolved.tzinfo, ZoneInfo):
        return resolved.name
    return None


def canonicalize_timezone_input(text: str | None) -> str | None:
    """Normalize user-facing timezone input to canonical IANA when possible."""

    return canonical_timezone_name(extract_timezone_hint(text))


def extract_timezone_hint(text: str | None) -> ResolvedTimezone | None:
    raw_text = (text or "").strip()
    if not raw_text:
        return None

    iana_match = IANA_PATTERN.search(raw_text)
    if iana_match:
        resolved = _resolve_iana(iana_match.group(0), "command")
        if resolved:
            return resolved

    offset_match = OFFSET_PATTERN.search(raw_text)
    if offset_match:
        resolved = _fixed_offset_timezone(offset_match.group(1), offset_match.group(2))
        if resolved:
            return ResolvedTimezone(name=resolved.name, tzinfo=resolved.tzinfo, source="command")

    lowered = raw_text.lower()
    for alias, zone_name in sorted(CITY_TIMEZONE_MAP.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in raw_text or alias in lowered:
            resolved = _resolve_iana(zone_name, "command")
            if resolved:
                return resolved
    return None


def resolve_timezone(explicit_tz: str | None = None, command_text: str | None = None) -> ResolvedTimezone:
    if explicit_tz:
        explicit = extract_timezone_hint(explicit_tz)
        if explicit:
            return ResolvedTimezone(name=explicit.name, tzinfo=explicit.tzinfo, source="explicit")
        raise NBAReportError(
            "无法识别时区，请传入 IANA 时区（如 Asia/Shanghai）或带 UTC 偏移的时区（如 UTC+08:00）。",
            kind="invalid_timezone",
        )

    inferred = extract_timezone_hint(command_text)
    if inferred:
        return inferred

    for env_key in ENV_TZ_KEYS:
        value = os.environ.get(env_key, "").strip()
        if not value:
            continue
        resolved = extract_timezone_hint(value)
        if resolved:
            return ResolvedTimezone(name=resolved.name, tzinfo=resolved.tzinfo, source=f"env:{env_key}")

    raise NBAReportError(
        "无法确定请求方时区。请提供 IANA 时区（如 Asia/Shanghai、America/Los_Angeles）或城市（如 上海、New York）。",
        kind="missing_timezone",
    )
