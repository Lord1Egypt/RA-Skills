#!/usr/bin/env python3
"""Study plan generator from Moodle sync snapshots."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


def _safe_dt(timestamp: Any) -> datetime | None:
    if timestamp is None:
        return None
    try:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def _upcoming_deadlines(sync_data: dict[str, Any], days: int) -> list[dict[str, Any]]:
    now = datetime.now(tz=timezone.utc)
    end = now + timedelta(days=days)
    calendar = sync_data.get("calendar", {})
    events = calendar.get("events", []) if isinstance(calendar, dict) else []
    if not isinstance(events, list):
        return []

    output: list[dict[str, Any]] = []
    for event in events:
        if not isinstance(event, dict):
            continue
        dt = _safe_dt(event.get("timesort") or event.get("timestart"))
        if not dt:
            continue
        if dt < now or dt > end:
            continue
        output.append(
            {
                "title": event.get("name", "Untitled event"),
                "course": event.get("course", {}).get("fullname")
                if isinstance(event.get("course"), dict)
                else "Unknown course",
                "due": dt,
            }
        )
    output.sort(key=lambda item: item["due"])
    return output


def _low_grade_courses(sync_data: dict[str, Any], threshold: float) -> list[dict[str, Any]]:
    grades = sync_data.get("grade_overview", [])
    if not isinstance(grades, list):
        return []

    output: list[dict[str, Any]] = []
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
            score = float(raw)
        except (TypeError, ValueError):
            continue
        if score < threshold:
            output.append(
                {
                    "course": item.get("fullname", "Unknown course"),
                    "score": score,
                    "display": grade.get("grade", ""),
                }
            )
    output.sort(key=lambda item: item["score"])
    return output


def generate_study_plan(sync_data: dict[str, Any], days: int = 7, grade_threshold: float = 70.0) -> str:
    now = datetime.now(tz=timezone.utc)
    deadlines = _upcoming_deadlines(sync_data, days=days)
    low_grades = _low_grade_courses(sync_data, threshold=grade_threshold)

    lines: list[str] = []
    lines.append("# Study Plan")
    lines.append("")
    lines.append(f"Plan window: {now.strftime('%Y-%m-%d')} to {(now + timedelta(days=days)).strftime('%Y-%m-%d')}")
    lines.append("")

    lines.append("## Priority Tasks")
    if deadlines:
        for item in deadlines[:10]:
            due_text = item["due"].strftime("%Y-%m-%d %H:%M UTC")
            lines.append(f"- Deadline prep: {item['title']} ({item['course']}) due {due_text}")
    else:
        lines.append("- No deadlines in the selected window.")

    lines.append("")
    lines.append("## Grade Recovery Focus")
    if low_grades:
        for item in low_grades[:5]:
            display = f" ({item['display']})" if item["display"] else ""
            lines.append(f"- {item['course']}: {item['score']:.2f}{display}")
    else:
        lines.append("- No courses under threshold.")

    lines.append("")
    lines.append("## Daily Routine")
    lines.append("- Day 1-2: Review upcoming deadlines and gather required materials.")
    lines.append("- Day 3-4: Complete highest-impact assignments first.")
    lines.append("- Day 5-6: Practice weak course topics and recheck gradebook.")
    lines.append("- Day 7: Submit remaining work and verify Moodle notifications.")
    lines.append("")

    lines.append("## Checkpoint")
    if deadlines:
        lines.append(f"- Earliest deadline: {deadlines[0]['title']} on {deadlines[0]['due'].strftime('%Y-%m-%d')}")
    else:
        lines.append("- No immediate deadlines detected.")
    lines.append("- Refresh this plan after each major submission.")
    lines.append("")

    return "\n".join(lines)

