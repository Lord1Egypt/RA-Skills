"""English + Chinese time-token parser for diary entries.

Lifted and trimmed from the original CEO-secretary log_event.py, with all MCP
and DiaryAnalyzer dependencies removed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Tuple

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

DEFAULT_TIMEZONE = "America/Denver"

TIME_TOKEN = r"(?:[01]?\d|2[0-3])(?::[0-5]\d)?\s*(?:a\.??m\.??|p\.??m\.??|am|pm)?"
CN_HOUR_TOKEN = r"(?:十[一二三四五六七八九]?|[一二三四五六七八九两]|\d{1,2})"
CN_START_TOKEN = rf"(?:(?:凌晨|早上|上午|中午|下午|晚上)\s*)?{CN_HOUR_TOKEN}(?:点|點)(?:半|[0-5]?\d分?)?"

RANGE_RE = re.compile(
    rf"\bfrom\s+(?P<start>{TIME_TOKEN})\s+(?:to|until|till|through|-|–|—)\s+(?P<end>{TIME_TOKEN}|now)\b",
    re.IGNORECASE,
)
BETWEEN_RE = re.compile(
    rf"\bbetween\s+(?P<start>{TIME_TOKEN})\s+and\s+(?P<end>{TIME_TOKEN}|now)\b",
    re.IGNORECASE,
)
END_ONLY_RE = re.compile(
    rf"\b(?:to|till|til|until|through)\s+(?P<end>{TIME_TOKEN}|now)\b",
    re.IGNORECASE,
)
START_ONLY_RE = re.compile(
    rf"\b(?:at|from|starting(?:\s+at)?|start(?:ing)?(?:\s+at)?)\s+(?P<start>{TIME_TOKEN})\b",
    re.IGNORECASE,
)
LEADING_RANGE_RE = re.compile(
    rf"^(?P<start>{TIME_TOKEN})\s*(?:-|–|—|to)\s*(?P<end>{TIME_TOKEN}|now)\b",
    re.IGNORECASE,
)
TIME_CLEANUP_RE = re.compile(
    rf"\b(?:from\s+{TIME_TOKEN}\s+(?:to|until|till|through|-|–|—)\s+(?:{TIME_TOKEN}|now)|"
    rf"between\s+{TIME_TOKEN}\s+and\s+(?:{TIME_TOKEN}|now)|"
    rf"(?:to|till|til|until|through)\s+(?:{TIME_TOKEN}|now)|"
    rf"(?:at|from|starting(?:\s+at)?|start(?:ing)?(?:\s+at)?)\s+{TIME_TOKEN})\b",
    re.IGNORECASE,
)
CHINESE_START_ONLY_RE = re.compile(rf"^(?P<start>{CN_START_TOKEN})(?P<title>.*)$")


class TimeParseError(ValueError):
    pass


@dataclass
class ResolvedRange:
    start: datetime
    end: datetime
    mode: str          # both_explicit | start_only | end_only | none_explicit
    cleaned_title: str


def now_in(tz: str) -> datetime:
    if ZoneInfo is None:
        return datetime.now()
    return datetime.now(ZoneInfo(tz))


def _normalize_ampm(token: str) -> str:
    return re.sub(r"\s+", "", token.strip().lower().replace(".", ""))


def _parse_chinese_hour(token: str) -> int:
    token = token.strip()
    if token.isdigit():
        return int(token)
    mapping = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6,
               "七": 7, "八": 8, "九": 9, "两": 2}
    if token == "十":
        return 10
    if token.startswith("十"):
        return 10 + mapping[token[1]]
    if token.endswith("十"):
        return mapping[token[0]] * 10
    if "十" in token:
        left, right = token.split("十", 1)
        return mapping[left] * 10 + mapping[right]
    if token in mapping:
        return mapping[token]
    raise TimeParseError(f"Unsupported Chinese hour token: {token}")


def parse_time_token(token: str, anchor: datetime) -> datetime:
    normalized = _normalize_ampm(token)
    if normalized == "now":
        return anchor

    m = re.fullmatch(r"(?P<hour>[01]?\d|2[0-3])(?::(?P<minute>[0-5]\d))?(?P<ampm>am|pm)?", normalized)
    if m:
        hour = int(m.group("hour"))
        minute = int(m.group("minute") or 0)
        ampm = m.group("ampm")
        if ampm == "am":
            hour = 0 if hour == 12 else hour
        elif ampm == "pm":
            hour = 12 if hour == 12 else hour + 12
        return anchor.replace(hour=hour, minute=minute, second=0, microsecond=0)

    cm = re.fullmatch(
        rf"(?P<period>凌晨|早上|上午|中午|下午|晚上)?(?P<hour>{CN_HOUR_TOKEN})(?:点|點)(?P<minute>半|[0-5]?\d分?)?",
        token.strip(),
    )
    if not cm:
        raise TimeParseError(f"Unsupported time token: {token}")

    hour = _parse_chinese_hour(cm.group("hour"))
    minute_token = cm.group("minute")
    minute = 30 if minute_token == "半" else int((minute_token or "0").replace("分", ""))
    period = cm.group("period")

    if period in ("凌晨", "早上", "上午"):
        hour = 0 if hour == 12 else hour
    elif period == "中午":
        if hour < 11:
            hour += 12
    elif period in ("下午", "晚上"):
        if hour < 12:
            hour += 12
    return anchor.replace(hour=hour, minute=minute, second=0, microsecond=0)


def adjust_relative_day(candidate: datetime, reference: datetime) -> datetime:
    delta = candidate - reference
    if delta > timedelta(hours=12):
        return candidate - timedelta(days=1)
    if delta < timedelta(hours=-12):
        return candidate + timedelta(days=1)
    return candidate


def strip_time_phrases(title: str) -> str:
    cleaned = LEADING_RANGE_RE.sub("", title).strip()
    cleaned = RANGE_RE.sub("", cleaned)
    cleaned = BETWEEN_RE.sub("", cleaned)
    cleaned = END_ONLY_RE.sub("", cleaned)
    cleaned = START_ONLY_RE.sub("", cleaned)
    cm = CHINESE_START_ONLY_RE.match(cleaned)
    if cm:
        cleaned = cm.group("title").strip()
    cleaned = TIME_CLEANUP_RE.sub("", cleaned)
    cleaned = re.sub(r"^[,，;；:\-–—\s]+", "", cleaned)
    cleaned = re.sub(r"[,，;；:\-–—\s]+$", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or title.strip()


def extract_time_hints(message: str) -> Tuple[Optional[str], Optional[str]]:
    for pattern in (RANGE_RE, BETWEEN_RE, LEADING_RANGE_RE):
        m = pattern.search(message)
        if m:
            return m.group("start"), m.group("end")
    end_match = END_ONLY_RE.search(message)
    start_match = START_ONLY_RE.search(message)
    if end_match and start_match:
        return start_match.group("start"), end_match.group("end")
    if end_match:
        return None, end_match.group("end")
    if start_match:
        return start_match.group("start"), None
    cm = CHINESE_START_ONLY_RE.match(message.strip())
    if cm:
        return cm.group("start"), None
    return None, None


def resolve_range(
    raw_title: str,
    timezone: str = DEFAULT_TIMEZONE,
    explicit_start: Optional[str] = None,
    explicit_end: Optional[str] = None,
    last_event_end: Optional[datetime] = None,
    now: Optional[datetime] = None,
) -> ResolvedRange:
    """Resolve a diary entry's start/end from natural language or explicit args.

    `last_event_end` is required when the message has end-only or no time hints;
    callers fetch it from the diary calendar before invoking this.
    """
    now = (now or now_in(timezone)).replace(second=0, microsecond=0)
    cleaned = strip_time_phrases(raw_title)

    start_hint = explicit_start
    end_hint = explicit_end
    if not (start_hint or end_hint):
        start_hint, end_hint = extract_time_hints(raw_title)

    if start_hint and end_hint:
        start_dt = parse_time_token(start_hint, now)
        end_dt = parse_time_token(end_hint, start_dt)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        mode = "both_explicit"
    elif start_hint:
        start_dt = adjust_relative_day(parse_time_token(start_hint, now), now)
        end_dt = now
        mode = "start_only"
    elif end_hint:
        if last_event_end is None:
            raise TimeParseError("End-only patterns require last_event_end")
        start_dt = last_event_end
        end_dt = parse_time_token(end_hint, start_dt)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        mode = "end_only"
    else:
        if last_event_end is None:
            raise TimeParseError("Untimed entries require last_event_end")
        start_dt = last_event_end
        end_dt = now
        mode = "none_explicit"

    if end_dt <= start_dt:
        raise TimeParseError(f"Resolved range has zero/negative duration: {start_dt} -> {end_dt}")
    return ResolvedRange(start=start_dt, end=end_dt, mode=mode, cleaned_title=cleaned)
