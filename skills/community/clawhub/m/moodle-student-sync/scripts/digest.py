#!/usr/bin/env python3
"""Daily digest generator for Moodle sync data."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _to_dt(timestamp: Any) -> datetime | None:
    if timestamp is None:
        return None
    try:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def _extract_events(sync_data: dict[str, Any]) -> list[dict[str, Any]]:
    calendar = sync_data.get("calendar", {})
    events = calendar.get("events", []) if isinstance(calendar, dict) else []
    if not isinstance(events, list):
        return []
    normalized: list[dict[str, Any]] = []
    for raw in events:
        if not isinstance(raw, dict):
            continue
        dt = _to_dt(raw.get("timesort") or raw.get("timestart"))
        normalized.append(
            {
                "name": raw.get("name", "Untitled event"),
                "description": raw.get("description", ""),
                "course": raw.get("course", {}).get("fullname")
                if isinstance(raw.get("course"), dict)
                else None,
                "dt": dt,
                "timestamp": raw.get("timesort") or raw.get("timestart"),
            }
        )
    normalized.sort(key=lambda item: item["timestamp"] or 0)
    return normalized


def _extract_low_grades(sync_data: dict[str, Any], threshold: float = 70.0) -> list[dict[str, Any]]:
    grades = sync_data.get("grade_overview", [])
    if not isinstance(grades, list):
        return []
    flagged: list[dict[str, Any]] = []
    for item in grades:
        if not isinstance(item, dict):
            continue
        grade = item.get("grade")
        if not isinstance(grade, dict):
            continue
        raw = grade.get("rawgrade")
        if raw is None:
            continue
        try:
            raw_num = float(raw)
        except (TypeError, ValueError):
            continue
        if raw_num < threshold:
            flagged.append(
                {
                    "course": item.get("fullname", "Unknown course"),
                    "rawgrade": raw_num,
                    "display_grade": grade.get("grade", ""),
                }
            )
    flagged.sort(key=lambda item: item["rawgrade"])
    return flagged


def generate_daily_digest(sync_data: dict[str, Any], limit: int = 10) -> str:
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    events = _extract_events(sync_data)[:limit]
    low_grades = _extract_low_grades(sync_data)
    notifications = sync_data.get("notifications", {}).get("notifications", [])
    if not isinstance(notifications, list):
        notifications = []

    lines: list[str] = []
    lines.append("# Daily Moodle Digest")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("## Upcoming Deadlines")
    if not events:
        lines.append("- No upcoming events found.")
    else:
        for event in events:
            when = event["dt"].strftime("%Y-%m-%d %H:%M UTC") if event["dt"] else "Unknown time"
            course = f" ({event['course']})" if event["course"] else ""
            lines.append(f"- {when}: {event['name']}{course}")

    lines.append("")
    lines.append("## Grade Watch")
    if not low_grades:
        lines.append("- No low grades detected below threshold.")
    else:
        for grade in low_grades[:10]:
            display = f" ({grade['display_grade']})" if grade["display_grade"] else ""
            lines.append(f"- {grade['course']}: {grade['rawgrade']:.2f}{display}")

    lines.append("")
    lines.append("## Recent Notifications")
    if not notifications:
        lines.append("- No recent notifications.")
    else:
        for note in notifications[:10]:
            if not isinstance(note, dict):
                continue
            subject = note.get("subject", "No subject")
            text = note.get("text", "").strip().replace("\n", " ")
            preview = text[:140] + ("..." if len(text) > 140 else "")
            lines.append(f"- {subject}: {preview}")

    lines.append("")
    lines.append("## Suggested Next Action")
    if events:
        lines.append(f"- Prioritize: {events[0]['name']}")
    elif low_grades:
        lines.append(f"- Review lowest course: {low_grades[0]['course']}")
    else:
        lines.append("- Do a light review session and check Moodle announcements.")

    return "\n".join(lines) + "\n"

