#!/usr/bin/env python3
"""Print a structured local business snapshot with dates rolled to today."""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DATA_PATH = Path(__file__).resolve().parents[1] / "assets" / "get_data.md"
MAX_DATA_BYTES = 1024 * 1024
CURRENT_DATE_TOKEN = "{{CURRENT_DATE}}"
IFT_SOURCE_MARKER = "Источник данных: get_data API (ИФТ)."
MOCK_ANCHOR_DATE = date(2026, 7, 16)
IFT_ANCHOR_DATE = date(2026, 7, 15)
try:
    BUSINESS_TIME_ZONE = ZoneInfo("Asia/Novosibirsk")
except ZoneInfoNotFoundError:
    BUSINESS_TIME_ZONE = timezone(timedelta(hours=7), "Asia/Novosibirsk")
MONTHS = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)
MONTH_NUMBER = {name: index for index, name in enumerate(MONTHS, start=1)}
MONTH_PATTERN = "|".join(MONTHS)
DATE_PATTERN = re.compile(
    rf"(?<!\d)(?:"
    rf"(?P<range_start>\d{{1,2}})[–-](?P<range_end>\d{{1,2}})\s+"
    rf"(?P<range_month>{MONTH_PATTERN})"
    rf"(?:\s+(?P<range_year>\d{{4}})\s+года)?"
    rf"|"
    rf"(?P<day>\d{{1,2}})\s+(?P<month>{MONTH_PATTERN})"
    rf"(?:\s+(?P<year>\d{{4}})\s+года)?"
    rf")(?!\w)"
)
SECTION_PATTERN = re.compile(r"(?=^## )", re.MULTILINE)
SECTION_HEADER_PATTERN = re.compile(
    r"^##[ \t]+(?P<title>\S(?:[^\r\n]*\S)?)[ \t]*$",
    re.MULTILINE,
)
SOURCE_DECLARATION_PATTERN = re.compile(
    r"^Источник данных:[^\r\n]+$",
    re.MULTILINE,
)
IFT_SOURCE_LINE_PATTERN = re.compile(
    rf"^{re.escape(IFT_SOURCE_MARKER)}[ \t]*$",
    re.MULTILINE,
)
STRUCTURAL_SECTION_TITLES = frozenset({"Происхождение данных"})
SOURCE_IDS = ("ift", "mock")


class SnapshotUnavailable(RuntimeError):
    """The required local snapshot cannot be used safely."""


def _format_date(value: date, include_year: bool) -> str:
    rendered = f"{value.day} {MONTHS[value.month - 1]}"
    if include_year:
        rendered += f" {value.year} года"
    return rendered


def _format_range(start: date, end: date, include_year: bool) -> str:
    if start.year == end.year and start.month == end.month:
        rendered = f"{start.day}–{end.day} {MONTHS[start.month - 1]}"
        if include_year:
            rendered += f" {start.year} года"
        return rendered

    if start.year == end.year:
        rendered = f"{start.day} {MONTHS[start.month - 1]}–" f"{end.day} {MONTHS[end.month - 1]}"
        if include_year:
            rendered += f" {start.year} года"
        return rendered

    return (
        f"{start.day} {MONTHS[start.month - 1]} {start.year} года–" f"{end.day} {MONTHS[end.month - 1]} {end.year} года"
    )


def _roll_section_dates(section: str, anchor: date, target: date) -> str:
    offset = target - anchor

    def replace(match: re.Match[str]) -> str:
        range_start = match.group("range_start")
        if range_start is not None:
            year_text = match.group("range_year")
            year = int(year_text) if year_text else anchor.year
            month = MONTH_NUMBER[match.group("range_month")]
            start = date(year, month, int(range_start)) + offset
            end = date(year, month, int(match.group("range_end"))) + offset
            return _format_range(start, end, include_year=year_text is not None)

        year_text = match.group("year")
        year = int(year_text) if year_text else anchor.year
        value = date(
            year,
            MONTH_NUMBER[match.group("month")],
            int(match.group("day")),
        )
        return _format_date(value + offset, include_year=year_text is not None)

    return DATE_PATTERN.sub(replace, section)


def roll_dates(value: str, target: date) -> str:
    sections = SECTION_PATTERN.split(value)
    sections[0] = sections[0].replace(
        CURRENT_DATE_TOKEN,
        _format_date(target, include_year=True),
    )

    for index in range(1, len(sections)):
        anchor = IFT_ANCHOR_DATE if IFT_SOURCE_MARKER in sections[index] else MOCK_ANCHOR_DATE
        sections[index] = _roll_section_dates(sections[index], anchor, target)

    return "".join(sections)


def _business_today() -> date:
    return datetime.now(BUSINESS_TIME_ZONE).date()


def _validate_document_preamble(value: str) -> None:
    first_line = value.splitlines()[0] if value else ""
    if not first_line.startswith("# ") or first_line.startswith("## "):
        raise SnapshotUnavailable("snapshot_unavailable")
    if value.count(CURRENT_DATE_TOKEN) != 1:
        raise SnapshotUnavailable("snapshot_unavailable")


def _extract_sections(value: str) -> list[dict[str, str]]:
    headers = list(SECTION_HEADER_PATTERN.finditer(value))
    declared_headers = sum(1 for line in value.splitlines() if re.match(r"^##(?:[ \t]|$)", line))
    if not headers or len(headers) != declared_headers:
        raise SnapshotUnavailable("snapshot_unavailable")

    sections: list[dict[str, str]] = []
    seen_topics: set[str] = set()
    for index, header in enumerate(headers):
        topic = header.group("title").strip()
        if topic in seen_topics:
            raise SnapshotUnavailable("snapshot_unavailable")
        seen_topics.add(topic)

        end = headers[index + 1].start() if index + 1 < len(headers) else len(value)
        facts = value[header.end() : end].strip()
        if topic in STRUCTURAL_SECTION_TITLES:
            continue

        declarations = SOURCE_DECLARATION_PATTERN.findall(facts)
        if any(item.strip() != IFT_SOURCE_MARKER for item in declarations):
            raise SnapshotUnavailable("snapshot_unavailable")

        source = "ift" if declarations else "mock"
        if declarations:
            facts = IFT_SOURCE_LINE_PATTERN.sub("", facts).strip()
        if not facts:
            continue

        sections.append(
            {
                "topic": topic,
                "source": source,
                "facts": facts,
            }
        )

    return sections


def load_data(path: Path = DATA_PATH, *, today: date | None = None) -> str:
    try:
        if not path.is_file() or path.stat().st_size > MAX_DATA_BYTES:
            raise OSError
        value = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise SnapshotUnavailable("snapshot_unavailable") from exc
    if not value:
        raise SnapshotUnavailable("snapshot_unavailable")

    _validate_document_preamble(value)
    target = today or _business_today()
    try:
        return roll_dates(value, target)
    except ValueError as exc:
        raise SnapshotUnavailable("snapshot_unavailable") from exc


def build_snapshot(
    path: Path = DATA_PATH,
    *,
    today: date | None = None,
) -> dict[str, object]:
    target = today or _business_today()
    sections = _extract_sections(load_data(path, today=target))
    available_sources = {item["source"] for item in sections}
    if not available_sources:
        raise SnapshotUnavailable("snapshot_unavailable")

    skipped_sources = [
        {
            "id": source,
            "critical": False,
            "reason": "not_available",
        }
        for source in SOURCE_IDS
        if source not in available_sources
    ]
    return {
        "ok": True,
        "completeness": "full" if not skipped_sources else "partial",
        "as_of": target.isoformat(),
        "sections": sections,
        "skipped_sources": skipped_sources,
    }


def _render(value: dict[str, object]) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def main() -> int:
    target = _business_today()
    try:
        result = build_snapshot(today=target)
    except SnapshotUnavailable:
        result = {
            "ok": False,
            "reason": "snapshot_unavailable",
            "completeness": "none",
            "as_of": target.isoformat(),
            "sections": [],
            "skipped_sources": [],
        }
        print(_render(result))
        return 0

    print(_render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
