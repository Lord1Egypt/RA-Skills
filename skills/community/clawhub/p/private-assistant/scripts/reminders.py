#!/usr/bin/env python3
"""Reminder helpers for the private-assistant Hermes skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, time as dt_time, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from records import RecordStore, _as_datetime, now_local  # noqa: E402


def _print(payload: dict, *, exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def _prompt_for_reminder(memo: dict, reminder_at: str) -> str:
    title = memo.get("title") or "未命名提醒"
    content = memo.get("content") or title
    kind = memo.get("kind") or "note"
    return (
        "This cron job was created by the private-assistant skill.\n"
        "Send exactly one short reminder message with no process details, no headers, and no extra metadata.\n"
        f"Memo ID: {memo.get('id')}\n"
        f"Memo kind: {kind}\n"
        f"Reminder time: {reminder_at}\n"
        f"Title: {title}\n"
        f"Content: {content}\n"
        "Preferred style: concise, single message, user-facing, Chinese if the source note is Chinese."
    )


_CHINESE_DIGITS = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}


def _normalize_time_text(value: str) -> str:
    text = str(value or "").strip().lower()
    text = text.translate(
        str.maketrans(
            {
                "：": ":",
                "，": ",",
                "。": ".",
                "／": "/",
                "－": "-",
                "—": "-",
                "～": "~",
            }
        )
    )
    return " ".join(text.split())


def _parse_number_token(token: str) -> int:
    text = _normalize_time_text(token).replace("个", "")
    if not text:
        raise ValueError("Missing numeric token")
    if text.isdigit():
        return int(text)
    if text == "半":
        return 30
    if "十" in text:
        left, _, right = text.partition("十")
        tens = 1 if not left else _CHINESE_DIGITS[left]
        units = 0
        if right:
            if right.isdigit():
                units = int(right)
            else:
                units = int("".join(str(_CHINESE_DIGITS[ch]) for ch in right))
        return tens * 10 + units
    if all(ch in _CHINESE_DIGITS for ch in text):
        return int("".join(str(_CHINESE_DIGITS[ch]) for ch in text))
    raise ValueError(f"Unsupported numeric token: {token}")


def _parse_relative_time(text: str, current: datetime) -> datetime | None:
    normalized = _normalize_time_text(text)
    future_markers = ("后", "之后", "以后", "later", "from now")
    has_future_marker = any(marker in normalized for marker in future_markers) or re.search(
        r"\bin\s+\d", normalized, re.IGNORECASE
    )
    if not has_future_marker:
        return None

    total = timedelta(0)
    matched = False

    if re.search(r"(半个?小时|half an hour|half-hour)", normalized, re.IGNORECASE):
        total += timedelta(minutes=30)
        matched = True

    patterns = (
        (r"(?P<value>\d+|[零〇一二两三四五六七八九十]+)\s*(?:天|日|days?|d)", "days"),
        (r"(?P<value>\d+|[零〇一二两三四五六七八九十]+)\s*(?:个)?(?:小时|钟头|hours?|hrs?|hr|h)", "hours"),
        (r"(?P<value>\d+|[零〇一二两三四五六七八九十]+)\s*(?:个)?(?:分钟|分(?:钟)?|minutes?|mins?|min|m)", "minutes"),
    )
    for pattern, unit in patterns:
        for match in re.finditer(pattern, normalized, re.IGNORECASE):
            value = _parse_number_token(match.group("value"))
            matched = True
            if unit == "days":
                total += timedelta(days=value)
            elif unit == "hours":
                total += timedelta(hours=value)
            else:
                total += timedelta(minutes=value)

    if not matched or total <= timedelta(0):
        return None
    return current + total


def _detect_day_context(text: str) -> tuple[int | None, bool, str | None]:
    normalized = _normalize_time_text(text)
    specific_tokens = (
        ("day after tomorrow morning", 2, "morning"),
        ("day after tomorrow evening", 2, "evening"),
        ("tomorrow morning", 1, "morning"),
        ("tomorrow evening", 1, "evening"),
        ("today morning", 0, "morning"),
        ("tonight", 0, "evening"),
        ("后天早上", 2, "morning"),
        ("后天晚上", 2, "evening"),
        ("明天早上", 1, "morning"),
        ("明天晚上", 1, "evening"),
        ("明早", 1, "morning"),
        ("明晚", 1, "evening"),
        ("今天早上", 0, "morning"),
        ("今天晚上", 0, "evening"),
        ("今早", 0, "morning"),
        ("今晚", 0, "evening"),
    )
    for token, day_offset, daypart in specific_tokens:
        if token in normalized:
            return day_offset, True, daypart

    explicit_day_tokens = (
        ("day after tomorrow", 2),
        ("tomorrow", 1),
        ("today", 0),
        ("后天", 2),
        ("明天", 1),
        ("今天", 0),
        ("今日", 0),
    )
    for token, day_offset in explicit_day_tokens:
        if token in normalized:
            return day_offset, True, None

    generic_dayparts = (
        ("凌晨", "midnight"),
        ("早上", "morning"),
        ("早晨", "morning"),
        ("上午", "morning"),
        ("中午", "noon"),
        ("下午", "afternoon"),
        ("晚上", "evening"),
        ("晚间", "evening"),
        ("夜里", "evening"),
        ("morning", "morning"),
        ("noon", "noon"),
        ("afternoon", "afternoon"),
        ("evening", "evening"),
    )
    for token, daypart in generic_dayparts:
        if token in normalized:
            return None, False, daypart

    return None, False, None


def _apply_daypart(hour: int, daypart: str | None, ampm: str | None = None) -> int:
    if ampm:
        marker = ampm.lower()
        if marker == "am":
            return 0 if hour == 12 else hour
        if marker == "pm" and hour < 12:
            return hour + 12
        return hour

    if daypart in {"afternoon", "evening"} and 1 <= hour < 12:
        return hour + 12
    if daypart == "noon" and 1 <= hour < 11:
        return hour + 12
    if daypart == "midnight" and hour == 12:
        return 0
    return hour


def _parse_clock_time(text: str, daypart: str | None) -> tuple[int, int] | None:
    normalized = _normalize_time_text(text)

    match = re.search(
        r"\b(?P<hour>\d{1,2})(?::(?P<minute>\d{1,2}))?\s*(?P<ampm>am|pm)\b",
        normalized,
        re.IGNORECASE,
    )
    if match:
        hour = int(match.group("hour"))
        minute = int(match.group("minute") or 0)
        return _apply_daypart(hour, daypart, match.group("ampm")), minute

    match = re.search(r"\b(?P<hour>\d{1,2}):(?P<minute>\d{1,2})\b", normalized)
    if match:
        hour = _apply_daypart(int(match.group("hour")), daypart)
        minute = int(match.group("minute"))
        return hour, minute

    match = re.search(
        r"(?P<hour>[\d零〇一二两三四五六七八九十]+)\s*点(?:钟)?(?:(?P<suffix>半|一刻|三刻)|(?P<minute>[\d零〇一二两三四五六七八九十]+)\s*分?)?",
        normalized,
    )
    if match:
        hour = _apply_daypart(_parse_number_token(match.group("hour")), daypart)
        if match.group("suffix") == "半":
            minute = 30
        elif match.group("suffix") == "一刻":
            minute = 15
        elif match.group("suffix") == "三刻":
            minute = 45
        else:
            minute = _parse_number_token(match.group("minute")) if match.group("minute") else 0
        return hour, minute

    return None


def _parse_natural_reminder_time(text: str, current: datetime) -> datetime | None:
    relative = _parse_relative_time(text, current)
    if relative is not None:
        return relative

    day_offset, explicit_day, daypart = _detect_day_context(text)
    clock = _parse_clock_time(text, daypart)
    if clock is None:
        return None

    hour, minute = clock
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Parsed reminder time is out of range: {hour:02d}:{minute:02d}")

    target_date = current.date() if day_offset is None else (current + timedelta(days=day_offset)).date()
    candidate = datetime.combine(target_date, dt_time(hour=hour, minute=minute), tzinfo=current.tzinfo)
    if explicit_day:
        if candidate <= current:
            raise ValueError(
                "Parsed reminder time is already in the past for the requested day phrase. "
                f"Got {candidate.isoformat()}, current time is {current.isoformat()}."
            )
        return candidate

    if candidate <= current:
        candidate += timedelta(days=1)
    return candidate


def _resolve_reminder_time(reminder_at: str, current: datetime | None = None) -> datetime:
    active_now = current or now_local()
    try:
        parsed = _as_datetime(reminder_at)
    except ValueError:
        parsed = None
    if parsed is None:
        parsed = _parse_natural_reminder_time(reminder_at, active_now)
    if parsed is None:
        raise ValueError(
            "Could not parse reminder time. Use an absolute datetime like "
            "'2026-04-16 20:00' or a natural phrase like '1分钟后', '今晚9点', or '明早8点'."
        )
    return parsed


class ReminderManager:
    def __init__(self, store: RecordStore | None = None):
        self.store = store or RecordStore()

    def create_payload(self, memo_id: str | None = None, *, use_last: bool = False, reminder_at: str) -> dict:
        memo = self.store.get_memo(memo_id, use_last=use_last)
        current = now_local()
        when = _resolve_reminder_time(reminder_at, current=current)
        if when <= current:
            raise ValueError(
                "reminder_at must be in the future. "
                f"Got {when.isoformat()}, current time is {current.isoformat()}."
            )
        reminder_iso = when.isoformat()
        title = memo.get("title") or memo.get("content") or "私人助手提醒"
        return {
            "memo_id": memo["id"],
            "schedule": reminder_iso,
            "name": f"Reminder: {title[:40]}",
            "prompt": _prompt_for_reminder(memo, reminder_iso),
            "reminder_at": reminder_iso,
        }

    def link(self, memo_id: str | None = None, *, use_last: bool = False, cron_job_id: str, reminder_at: str) -> dict:
        return self.store.update_memo(
            memo_id,
            use_last=use_last,
            cron_job_id=cron_job_id,
            reminder_at=reminder_at,
        )

    def unlink(
        self,
        memo_id: str | None = None,
        *,
        use_last: bool = False,
        cron_job_id: str | None = None,
    ) -> dict:
        target = None
        if memo_id or use_last:
            target = self.store.get_memo(memo_id, use_last=use_last, reminders_only=bool(use_last and not memo_id))
        elif cron_job_id:
            result = self.store.list_memos(reminders_only=True, limit=0)
            for memo in result["memos"]:
                if memo.get("cron_job_id") == cron_job_id:
                    target = memo
                    break
        if target is None:
            raise ValueError("Reminder target not found.")
        return self.store.update_memo(
            str(target["id"]),
            cron_job_id="",
            reminder_at="",
        )

    def get(self, memo_id: str | None = None, *, use_last: bool = False) -> dict:
        if memo_id or use_last:
            return self.store.get_memo(memo_id, use_last=use_last, reminders_only=bool(use_last and not memo_id))
        result = self.store.list_memos(reminders_only=True, upcoming_only=True, limit=1)
        if not result["memos"]:
            raise ValueError("No reminder records found.")
        return result["memos"][0]

    def list(self, *, limit: int = 20, upcoming_only: bool = True) -> dict:
        result = self.store.list_memos(
            reminders_only=True,
            upcoming_only=upcoming_only,
            limit=limit,
        )
        reminders = sorted(
            result["memos"],
            key=lambda memo: memo.get("reminder_at") or datetime.max.isoformat(),
        )
        return {
            "count": len(reminders),
            "reminders": reminders,
            "skipped_corrupt_lines": result["skipped_corrupt_lines"],
            "generated_at": now_local().isoformat(),
        }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Private assistant reminder CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    create_payload = sub.add_parser("create-payload")
    create_payload.add_argument("--memo-id")
    create_payload.add_argument("--last", action="store_true")
    create_payload.add_argument("--reminder-at", required=True)

    link = sub.add_parser("link")
    link.add_argument("--memo-id")
    link.add_argument("--last", action="store_true")
    link.add_argument("--cron-job-id", required=True)
    link.add_argument("--reminder-at", required=True)

    unlink = sub.add_parser("unlink")
    unlink.add_argument("--memo-id")
    unlink.add_argument("--last", action="store_true")
    unlink.add_argument("--cron-job-id")

    get_cmd = sub.add_parser("get")
    get_cmd.add_argument("--memo-id")
    get_cmd.add_argument("--last", action="store_true")

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--limit", type=int, default=20)
    list_cmd.add_argument("--all", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)
    manager = ReminderManager()
    try:
        if args.command == "create-payload":
            payload = manager.create_payload(args.memo_id, use_last=args.last, reminder_at=args.reminder_at)
            _print({"success": True, **payload})

        if args.command == "link":
            record = manager.link(
                args.memo_id,
                use_last=args.last,
                cron_job_id=args.cron_job_id,
                reminder_at=args.reminder_at,
            )
            _print({"success": True, "record": record})

        if args.command == "unlink":
            record = manager.unlink(args.memo_id, use_last=args.last, cron_job_id=args.cron_job_id)
            _print({"success": True, "record": record})

        if args.command == "get":
            record = manager.get(args.memo_id, use_last=args.last)
            _print({"success": True, "record": record})

        if args.command == "list":
            result = manager.list(limit=args.limit, upcoming_only=not args.all)
            _print({"success": True, **result})

        _print({"success": False, "error": f"Unhandled command: {args.command}"}, exit_code=1)
    except Exception as exc:
        _print({"success": False, "error": str(exc)}, exit_code=1)


if __name__ == "__main__":
    main()
