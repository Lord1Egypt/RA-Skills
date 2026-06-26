#!/usr/bin/env python3
"""Create a Google Calendar event from Gmail content via Maton."""

from __future__ import annotations

import argparse
import base64
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"

FIELD_ALIASES = {
    "summary": ["Title", "Summary", "标题", "主题"],
    "date": ["Date", "日期"],
    "start": ["Start", "Start Time", "开始", "开始时间"],
    "end": ["End", "End Time", "结束", "结束时间"],
    "timezone": ["Time Zone", "Timezone", "时区"],
    "location": ["Location", "地点"],
    "description": ["Description", "Details", "描述", "详情"],
}

RELATIVE_DAY_OFFSETS = {
    "day after tomorrow": 2,
    "tomorrow": 1,
    "today": 0,
    "后天": 2,
    "明天": 1,
    "今天": 0,
}

WEEKDAY_MAP = {
    "周一": 0,
    "星期一": 0,
    "monday": 0,
    "mon": 0,
    "周二": 1,
    "星期二": 1,
    "tuesday": 1,
    "tue": 1,
    "周三": 2,
    "星期三": 2,
    "wednesday": 2,
    "wed": 2,
    "周四": 3,
    "星期四": 3,
    "thursday": 3,
    "thu": 3,
    "周五": 4,
    "星期五": 4,
    "friday": 4,
    "fri": 4,
    "周六": 5,
    "星期六": 5,
    "saturday": 5,
    "sat": 5,
    "周日": 6,
    "周天": 6,
    "星期日": 6,
    "星期天": 6,
    "sunday": 6,
    "sun": 6,
}

ABSOLUTE_DATE_PATTERNS = [
    re.compile(r"(?P<year>\d{4})[/-](?P<month>\d{1,2})[/-](?P<day>\d{1,2})"),
    re.compile(r"(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日?"),
    re.compile(r"(?P<month>\d{1,2})月(?P<day>\d{1,2})日"),
    re.compile(r"(?P<month>\d{1,2})/(?P<day>\d{1,2})(?:/(?P<year>\d{2,4}))?"),
]

TIME_TOKEN_PATTERN = re.compile(
    r"""
    (?P<prefix>上午|下午|晚上|中午|早上|凌晨)?
    \s*
    (?P<hour>\d{1,2})
    (?:
        :
        (?P<minute_colon>\d{1,2})
      |
        [点时]
        (?:
            (?P<minute_cn>\d{1,2})?
            (?:分)?
          |
            (?P<half>半)
        )?
    )?
    \s*
    (?P<suffix>am|pm)?
    """,
    re.IGNORECASE | re.VERBOSE,
)

TIME_RANGE_PATTERN = re.compile(
    r"""
    (?P<start>
        (?:上午|下午|晚上|中午|早上|凌晨)?\s*\d{1,2}(?::\d{1,2})?\s*(?:am|pm)?
      |
        (?:上午|下午|晚上|中午|早上|凌晨)?\s*\d{1,2}[点时](?:\d{1,2}分?|半)?\s*(?:am|pm)?
    )
    \s*
    (?:-|–|—|~|至|到|to)
    \s*
    (?P<end>
        (?:上午|下午|晚上|中午|早上|凌晨)?\s*\d{1,2}(?::\d{1,2})?\s*(?:am|pm)?
      |
        (?:上午|下午|晚上|中午|早上|凌晨)?\s*\d{1,2}[点时](?:\d{1,2}分?|半)?\s*(?:am|pm)?
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

TIMEZONE_PATTERN = re.compile(
    r"\b(?:[A-Z][A-Za-z_+-]*)/(?:[A-Z][A-Za-z_+-]*)(?:/(?:[A-Z][A-Za-z_+-]*))?\b"
)
MEETING_URL_PATTERN = re.compile(
    r"https?://\S*(?:zoom\.us|meet\.google\.com|teams\.microsoft\.com|voovmeeting\.com|v\.qq\.com)\S*",
    re.IGNORECASE,
)
FREE_TEXT_LOCATION_PATTERN = re.compile(
    r"(?:在|via|on)\s+(Zoom|Google Meet|Meet|Teams|Tencent Meeting|Voov|腾讯会议|飞书会议|会议室[^\s，。]*)",
    re.IGNORECASE,
)


class MatonClient:
    def __init__(self, api_key: str, mail_connection: str | None, calendar_connection: str | None):
        self.api_key = api_key
        self.mail_connection = mail_connection
        self.calendar_connection = calendar_connection

    def request_json(
        self,
        url: str,
        *,
        method: str = "GET",
        payload: dict[str, Any] | None = None,
        connection_id: str | None = None,
    ) -> dict[str, Any]:
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=data, method=method)
        request.add_header("Authorization", f"Bearer {self.api_key}")
        if payload is not None:
            request.add_header("Content-Type", "application/json")
        if connection_id:
            request.add_header("Maton-Connection", connection_id)

        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            if not body:
                return {}
            return json.loads(body)

    def find_message_id(self, query: str) -> str:
        encoded_query = urllib.parse.quote(query)
        url = (
            "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages"
            f"?q={encoded_query}&maxResults=1"
        )
        data = self.request_json(url, connection_id=self.mail_connection)
        messages = data.get("messages", [])
        if not messages:
            raise RuntimeError(f"No Gmail messages matched query: {query}")
        return messages[0]["id"]

    def get_message(self, message_id: str) -> dict[str, Any]:
        url = (
            "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/"
            f"{message_id}?format=full"
        )
        return self.request_json(url, connection_id=self.mail_connection)

    def create_event(self, calendar_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        calendar_id = urllib.parse.quote(calendar_id, safe="")
        url = (
            "https://gateway.maton.ai/google-calendar/calendar/v3/calendars/"
            f"{calendar_id}/events"
        )
        return self.request_json(
            url,
            method="POST",
            payload=payload,
            connection_id=self.calendar_connection,
        )


def load_api_key() -> str:
    if "MATON_API_KEY" in os_environ():
        return os_environ()["MATON_API_KEY"]
    if not ENV_PATH.exists():
        raise RuntimeError(f"Missing .env file: {ENV_PATH}")
    values: dict[str, str] = {}
    for raw_line in ENV_PATH.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    api_key = values.get("MATON_API_KEY")
    if not api_key:
        raise RuntimeError(f"MATON_API_KEY is missing in {ENV_PATH}")
    return api_key


def os_environ() -> dict[str, str]:
    import os

    return os.environ


def get_header(message: dict[str, Any], name: str) -> str | None:
    payload = message.get("payload", {})
    for header in payload.get("headers", []):
        if header.get("name", "").lower() == name.lower():
            return header.get("value")
    return None


def decode_gmail_body(payload: dict[str, Any]) -> str:
    data = payload.get("body", {}).get("data")
    if data:
        return decode_base64url(data)
    for part in payload.get("parts", []) or []:
        mime_type = part.get("mimeType", "")
        if mime_type.startswith("text/plain"):
            part_data = part.get("body", {}).get("data")
            if part_data:
                return decode_base64url(part_data)
        nested = decode_gmail_body(part)
        if nested:
            return nested
    return ""


def decode_base64url(value: str) -> str:
    padding = "=" * (-len(value) % 4)
    raw = base64.urlsafe_b64decode((value + padding).encode("ascii"))
    return raw.decode("utf-8", errors="replace")


def extract_structured_fields(text: str, subject: str | None) -> dict[str, str]:
    extracted: dict[str, str] = {}
    for key, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            match = re.search(rf"^{re.escape(alias)}\s*[:：]\s*(.+)$", text, flags=re.MULTILINE)
            if match:
                extracted[key] = match.group(1).strip()
                break

    if "date" not in extracted and "start" in extracted:
        maybe_date = try_extract_date_prefix(extracted["start"])
        if maybe_date:
            extracted["date"] = maybe_date

    return extracted


def extract_fields(text: str, subject: str | None, *, allow_free_text: bool) -> tuple[dict[str, str], str]:
    structured = extract_structured_fields(text, subject)
    if not allow_free_text:
        if "start" not in structured:
            raise RuntimeError("Structured-only mode requires Start/开始时间 in the message body.")
        return structured, "structured"

    free_text = extract_free_text_fields(text, subject)
    merged = dict(free_text)
    merged.update(structured)
    if "summary" not in merged and subject:
        merged["summary"] = subject

    if "start" not in merged:
        raise RuntimeError(
            "Missing start time. Add Start/开始时间 fields or include a free-text schedule such as "
            "'2026年4月25日下午3点到4点' or 'tomorrow 3pm-4pm'."
        )

    if structured and free_text:
        mode = "mixed"
    elif structured:
        mode = "structured"
    else:
        mode = "free_text"
    return merged, mode


def try_extract_date_prefix(value: str) -> str | None:
    match = re.match(r"^(\d{4}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2})", value)
    if not match:
        return None
    return match.group(1).replace("/", "-")


def extract_free_text_fields(text: str, subject: str | None) -> dict[str, str]:
    combined = "\n".join(part for part in [subject or "", text] if part).strip()
    if not combined:
        return {}

    extracted: dict[str, str] = {}
    today = datetime.now().date()

    date_value = find_date_in_text(combined, today)
    if date_value:
        extracted["date"] = date_value

    time_range = find_time_range_in_text(combined)
    if time_range:
        extracted["start"] = time_range["start"]
        if time_range.get("end"):
            extracted["end"] = time_range["end"]

    timezone_name = find_timezone_in_text(combined)
    if timezone_name:
        extracted["timezone"] = timezone_name

    location = find_location_in_text(combined)
    if location:
        extracted["location"] = location

    if subject:
        extracted["summary"] = subject.strip()
    if text.strip():
        extracted["description"] = text.strip()
    return extracted


def find_date_in_text(text: str, today: date) -> str | None:
    for pattern in ABSOLUTE_DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        year = match.groupdict().get("year")
        normalized_year = today.year if not year else int(year)
        if normalized_year < 100:
            normalized_year += 2000
        month = int(match.group("month"))
        day_value = int(match.group("day"))
        return date(normalized_year, month, day_value).isoformat()

    lowered = text.lower()
    for label, offset in RELATIVE_DAY_OFFSETS.items():
        if label.isascii():
            if re.search(rf"\b{re.escape(label)}\b", lowered):
                return (today + timedelta(days=offset)).isoformat()
        elif label in text:
            return (today + timedelta(days=offset)).isoformat()

    chinese_weekday = re.search(r"(下周)?(周[一二三四五六日天]|星期[一二三四五六日天])", text)
    if chinese_weekday:
        return resolve_weekday(
            today,
            chinese_weekday.group(2),
            force_next_week=bool(chinese_weekday.group(1)),
        ).isoformat()

    english_weekday = re.search(
        r"\b(next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)\b",
        lowered,
    )
    if english_weekday:
        return resolve_weekday(
            today,
            english_weekday.group(2),
            force_next_week=bool(english_weekday.group(1)),
        ).isoformat()

    return None


def resolve_weekday(today: date, token: str, *, force_next_week: bool) -> date:
    target = WEEKDAY_MAP[token.lower()]
    if force_next_week:
        current_week_monday = today - timedelta(days=today.weekday())
        next_week_monday = current_week_monday + timedelta(days=7)
        return next_week_monday + timedelta(days=target)
    days_ahead = (target - today.weekday()) % 7
    return today + timedelta(days=days_ahead)


def find_time_range_in_text(text: str) -> dict[str, str] | None:
    match = TIME_RANGE_PATTERN.search(text)
    if match:
        start_info = parse_time_fragment(match.group("start"))
        end_info = parse_time_fragment(match.group("end"))
        if start_info and end_info:
            propagate_meridiem(start_info, end_info)
            return {
                "start": time_info_to_string(start_info),
                "end": time_info_to_string(end_info),
            }

    time_infos = []
    for candidate in TIME_TOKEN_PATTERN.finditer(text):
        info = parse_time_fragment(candidate.group(0))
        if info:
            time_infos.append(info)
    if not time_infos:
        return None

    result: dict[str, str] = {}
    if len(time_infos) > 1:
        propagate_meridiem(time_infos[0], time_infos[1])
        result["end"] = time_info_to_string(time_infos[1])
    result["start"] = time_info_to_string(time_infos[0])
    return result


def parse_time_fragment(value: str) -> dict[str, Any] | None:
    cleaned = value.strip().rstrip(".,，。；;")
    match = TIME_TOKEN_PATTERN.fullmatch(cleaned)
    if not match:
        return None

    minute = 0
    if match.group("minute_colon"):
        minute = int(match.group("minute_colon"))
    elif match.group("minute_cn"):
        minute = int(match.group("minute_cn"))
    elif match.group("half"):
        minute = 30

    return {
        "hour": int(match.group("hour")),
        "minute": minute,
        "meridiem": (match.group("suffix") or match.group("prefix") or "").strip().lower() or None,
    }


def propagate_meridiem(first: dict[str, Any], second: dict[str, Any]) -> None:
    if first.get("meridiem") and not second.get("meridiem"):
        second["meridiem"] = first["meridiem"]
    elif second.get("meridiem") and not first.get("meridiem"):
        first["meridiem"] = second["meridiem"]


def time_info_to_string(info: dict[str, Any]) -> str:
    hour = int(info["hour"])
    minute = int(info["minute"])
    meridiem = info.get("meridiem")

    if meridiem in {"pm", "下午", "晚上"} and 1 <= hour < 12:
        hour += 12
    elif meridiem in {"am", "上午", "早上", "凌晨"} and hour == 12:
        hour = 0
    elif meridiem == "中午":
        if hour == 0:
            hour = 12
        elif 1 <= hour < 11:
            hour += 12

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise RuntimeError(f"Unsupported time fragment: {info}")
    return f"{hour:02d}:{minute:02d}:00"


def find_timezone_in_text(text: str) -> str | None:
    match = TIMEZONE_PATTERN.search(text)
    if match:
        return match.group(0)
    if "北京时间" in text or "中国时间" in text:
        return "Asia/Shanghai"
    if re.search(r"\bCST\b", text):
        return "Asia/Shanghai"
    return None


def find_location_in_text(text: str) -> str | None:
    url_match = MEETING_URL_PATTERN.search(text)
    if url_match:
        return url_match.group(0)
    inline_match = FREE_TEXT_LOCATION_PATTERN.search(text)
    if inline_match:
        return inline_match.group(1)
    return None


def build_event_payload(
    fields: dict[str, str],
    *,
    default_timezone: str,
    default_duration_minutes: int,
    message_id: str,
    subject: str | None,
) -> dict[str, Any]:
    timezone_name = fields.get("timezone", default_timezone)
    start_value = normalize_datetime(fields["start"], fields.get("date"))

    if "end" in fields:
        end_value = normalize_datetime(fields["end"], fields.get("date"))
    else:
        start_dt = datetime.fromisoformat(start_value)
        end_value = (start_dt + timedelta(minutes=default_duration_minutes)).isoformat()

    description = fields.get("description", "").strip()
    source_subject = subject or fields.get("summary", "(No subject)")
    trailer = f"Imported from Gmail message {message_id} ({source_subject})."
    full_description = description if description else trailer
    if description:
        full_description = f"{description}\n\n{trailer}"

    event: dict[str, Any] = {
        "summary": fields.get("summary", source_subject),
        "description": full_description,
        "start": {"dateTime": start_value, "timeZone": timezone_name},
        "end": {"dateTime": end_value, "timeZone": timezone_name},
    }
    if "location" in fields:
        event["location"] = fields["location"]
    return event


def normalize_datetime(value: str, date_text: str | None) -> str:
    cleaned = value.strip()
    if "T" in cleaned or re.match(r"^\d{4}-\d{2}-\d{2} ", cleaned):
        return datetime.fromisoformat(cleaned.replace("Z", "+00:00")).isoformat()

    date_value = date_text
    time_value = cleaned

    if not date_value:
        pieces = re.match(r"^(\d{4}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2})[ T](.+)$", cleaned)
        if pieces:
            date_value = pieces.group(1)
            time_value = pieces.group(2)

    if not date_value:
        raise RuntimeError(
            "Missing event date. Expected Date/日期 or a recognizable free-text date in the message."
        )

    normalized_date = parse_date(date_value).strftime("%Y-%m-%d")
    normalized_time = parse_time(time_value)
    return datetime.fromisoformat(f"{normalized_date}T{normalized_time}").isoformat()


def parse_date(value: str) -> datetime:
    detected = find_date_in_text(value.strip(), datetime.now().date())
    if detected:
        return datetime.strptime(detected, "%Y-%m-%d")
    raise RuntimeError(f"Unsupported date format: {value}")


def parse_time(value: str) -> str:
    cleaned = value.strip()
    for fmt in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(cleaned, fmt).strftime("%H:%M:%S")
        except ValueError:
            continue
    info = parse_time_fragment(cleaned)
    if info:
        return time_info_to_string(info)
    raise RuntimeError(f"Unsupported time format: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read a Gmail message through Maton and create a Google Calendar event."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--message-id", help="Specific Gmail message ID to import")
    source.add_argument("--query", help="Gmail search query used to find the newest message")
    parser.add_argument("--calendar-id", default="primary", help="Google Calendar ID (default: primary)")
    parser.add_argument(
        "--timezone",
        default="Asia/Shanghai",
        help="Fallback timezone when the email body does not provide one",
    )
    parser.add_argument(
        "--default-duration-minutes",
        type=int,
        default=30,
        help="Duration used when the email provides a start time but no end time",
    )
    parser.add_argument("--mail-connection", help="Optional Maton connection ID for Gmail")
    parser.add_argument("--calendar-connection", help="Optional Maton connection ID for Google Calendar")
    parser.add_argument("--dry-run", action="store_true", help="Parse the message without creating an event")
    parser.add_argument(
        "--structured-only",
        action="store_true",
        help="Disable free-text fallback and require explicit Title/Date/Start/End style fields",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = load_api_key()
    client = MatonClient(api_key, args.mail_connection, args.calendar_connection)

    message_id = args.message_id or client.find_message_id(args.query)
    message = client.get_message(message_id)
    subject = get_header(message, "Subject")
    body = decode_gmail_body(message.get("payload", {}))
    if not body.strip():
        raise RuntimeError("Could not extract a plain-text body from the Gmail message.")

    fields, parsing_mode = extract_fields(body, subject, allow_free_text=not args.structured_only)
    event_payload = build_event_payload(
        fields,
        default_timezone=args.timezone,
        default_duration_minutes=args.default_duration_minutes,
        message_id=message_id,
        subject=subject,
    )

    result: dict[str, Any] = {
        "message_id": message_id,
        "subject": subject,
        "parsing_mode": parsing_mode,
        "extracted_fields": fields,
        "event_payload": event_payload,
    }

    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    created_event = client.create_event(args.calendar_id, event_payload)
    result["created_event"] = {
        "id": created_event.get("id"),
        "status": created_event.get("status"),
        "htmlLink": created_event.get("htmlLink"),
        "summary": created_event.get("summary"),
        "start": created_event.get("start"),
        "end": created_event.get("end"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - CLI surface
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
