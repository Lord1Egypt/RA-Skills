#!/usr/bin/env python3
"""Resolve conservative Chinese relative due dates against the meeting date."""

from __future__ import annotations

import argparse
import calendar
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any


WEEKDAYS = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6}


def _valid_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def resolve_due(expression: str | None, base: date | None) -> tuple[str | None, str]:
    """Return ISO date and a short machine-readable reason."""

    if not expression:
        return None, "missing_expression"
    if base is None:
        return None, "missing_meeting_date"

    text = re.sub(r"\s+", "", expression)

    iso_match = re.search(r"(?<!\d)(20\d{2})-(\d{1,2})-(\d{1,2})(?!\d)", text)
    if iso_match:
        parsed = _valid_date(*(int(part) for part in iso_match.groups()))
        return (parsed.isoformat(), "absolute_iso") if parsed else (None, "invalid_absolute_date")

    full_cn = re.search(r"(20\d{2})年(\d{1,2})月(\d{1,2})[日号]", text)
    if full_cn:
        parsed = _valid_date(*(int(part) for part in full_cn.groups()))
        return (parsed.isoformat(), "absolute_chinese") if parsed else (None, "invalid_absolute_date")

    short_cn = re.search(r"(?<!\d)(\d{1,2})月(\d{1,2})[日号]", text)
    if short_cn:
        month, day_number = (int(part) for part in short_cn.groups())
        parsed = _valid_date(base.year, month, day_number)
        if parsed and parsed >= base:
            return parsed.isoformat(), "absolute_month_day"
        return None, "ambiguous_past_month_day"

    if "后天" in text:
        return (base + timedelta(days=2)).isoformat(), "relative_day"
    if "明天" in text or "明日" in text:
        return (base + timedelta(days=1)).isoformat(), "relative_day"
    if "今天" in text or "今日" in text:
        return base.isoformat(), "relative_day"

    weekday_match = re.search(
        r"(?P<prefix>下下周|下下星期|下周|下星期|本周|本星期|这周|这星期|周|星期)"
        r"(?P<weekday>[一二三四五六日天])",
        text,
    )
    if weekday_match:
        target = WEEKDAYS[weekday_match.group("weekday")]
        prefix = weekday_match.group("prefix")
        monday = base - timedelta(days=base.weekday())
        if prefix in {"下下周", "下下星期"}:
            result = monday + timedelta(days=14 + target)
        elif prefix in {"下周", "下星期"}:
            result = monday + timedelta(days=7 + target)
        elif prefix in {"本周", "本星期", "这周", "这星期"}:
            result = monday + timedelta(days=target)
            if result < base:
                return None, "weekday_already_passed"
        else:
            delta = (target - base.weekday()) % 7
            result = base + timedelta(days=delta)
        return result.isoformat(), "relative_weekday"

    if "下月底" in text or "下月末" in text:
        month = 1 if base.month == 12 else base.month + 1
        year = base.year + 1 if base.month == 12 else base.year
        return date(year, month, calendar.monthrange(year, month)[1]).isoformat(), "relative_month_end"
    if "月底" in text or "月末" in text:
        return date(base.year, base.month, calendar.monthrange(base.year, base.month)[1]).isoformat(), "relative_month_end"

    return None, "unresolved_expression"


def normalize_receipt(data: dict[str, Any], override_base: date | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    meeting_date = override_base
    if meeting_date is None:
        raw_date = data.get("meeting", {}).get("date")
        if raw_date:
            try:
                meeting_date = date.fromisoformat(raw_date)
            except ValueError:
                meeting_date = None

    report: list[dict[str, Any]] = []
    for commitment in data.get("commitments", []):
        original = commitment.get("due_original")
        existing = commitment.get("due_resolved")
        if existing:
            report.append({"id": commitment.get("id"), "original": original, "resolved": existing, "reason": "kept_existing"})
            continue
        resolved, reason = resolve_due(original, meeting_date)
        if resolved:
            commitment["due_resolved"] = resolved
        report.append({"id": commitment.get("id"), "original": original, "resolved": resolved, "reason": reason})
    return data, report


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize conservative Chinese due-date expressions in a receipt.")
    parser.add_argument("input", help="Receipt JSON path")
    parser.add_argument("--output", help="Write normalized JSON here; stdout when omitted")
    parser.add_argument("--base-date", help="Override meeting date with YYYY-MM-DD")
    parser.add_argument("--report", help="Write date-resolution report JSON here")
    args = parser.parse_args()

    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        override = date.fromisoformat(args.base_date) if args.base_date else None
        normalized, report = normalize_receipt(data, override)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"date normalization error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    output = json.dumps(normalized, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    report_doc = {
        "meeting_date": (override or normalized.get("meeting", {}).get("date")),
        "resolved": sum(1 for item in report if item["resolved"]),
        "unresolved": sum(1 for item in report if not item["resolved"]),
        "items": report,
    }
    if args.report:
        Path(args.report).write_text(json.dumps(report_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
