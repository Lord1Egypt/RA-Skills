#!/usr/bin/env python3
"""CLI for Moodle student sync workflows."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any

try:
    from .digest import generate_daily_digest
    from .moodle_client import MoodleAPIError, MoodleClient
    from .study_planner import generate_study_plan
except ImportError:
    from digest import generate_daily_digest
    from moodle_client import MoodleAPIError, MoodleClient
    from study_planner import generate_study_plan


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _get_client(rate_limit_seconds: float, timeout_seconds: float) -> MoodleClient:
    return MoodleClient.from_env(
        rate_limit_seconds=rate_limit_seconds,
        timeout_seconds=timeout_seconds,
    )


def _is_active_course(course: dict[str, Any], now_ts: int) -> bool:
    if not isinstance(course, dict):
        return False
    enddate = course.get("enddate")
    if not isinstance(enddate, int):
        return True
    return enddate == 0 or enddate > now_ts


def build_sync_snapshot(
    client: MoodleClient,
    include_contents: bool = False,
    max_courses_for_contents: int = 5,
) -> dict[str, Any]:
    site_info = client.get_site_info()
    user_id = client.resolve_user_id()
    courses = client.get_courses(user_id)
    calendar = client.get_upcoming()
    grade_overview = client.get_grade_overview(user_id)
    notifications = client.get_notifications(limit=10)

    now_ts = int(datetime.now(tz=timezone.utc).timestamp())
    active_courses = [c for c in courses if _is_active_course(c, now_ts)]

    contents_by_course: dict[str, Any] = {}
    if include_contents:
        for course in active_courses[:max_courses_for_contents]:
            course_id = course.get("id")
            if not isinstance(course_id, int):
                continue
            contents_by_course[str(course_id)] = client.get_course_contents(course_id)

    return {
        "generated_at": _now_iso(),
        "site_info": site_info,
        "user_id": user_id,
        "courses": courses,
        "active_courses": active_courses,
        "calendar": calendar,
        "grade_overview": grade_overview,
        "notifications": notifications,
        "course_contents": contents_by_course,
    }


def _write_output(payload: str, output_path: str | None) -> None:
    if output_path:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(payload)
        print(f"Wrote output to {output_path}", file=sys.stderr)
        return
    sys.stdout.write(payload)
    if not payload.endswith("\n"):
        sys.stdout.write("\n")


def cmd_sync(args: argparse.Namespace) -> int:
    client = _get_client(args.rate_limit, args.timeout)
    snapshot = build_sync_snapshot(
        client,
        include_contents=args.include_contents,
        max_courses_for_contents=args.max_courses,
    )
    _write_output(json.dumps(snapshot, indent=2, ensure_ascii=False), args.output)
    return 0


def cmd_deadlines(args: argparse.Namespace) -> int:
    client = _get_client(args.rate_limit, args.timeout)
    snapshot = build_sync_snapshot(client, include_contents=False)
    events = snapshot.get("calendar", {}).get("events", [])
    if not isinstance(events, list):
        events = []
    payload = {
        "generated_at": snapshot["generated_at"],
        "count": min(len(events), args.limit),
        "events": events[: args.limit],
    }
    _write_output(json.dumps(payload, indent=2, ensure_ascii=False), args.output)
    return 0


def cmd_grades(args: argparse.Namespace) -> int:
    client = _get_client(args.rate_limit, args.timeout)
    user_id = client.resolve_user_id()
    grades = client.get_grade_overview(user_id)
    payload = {
        "generated_at": _now_iso(),
        "user_id": user_id,
        "grades": grades,
    }
    _write_output(json.dumps(payload, indent=2, ensure_ascii=False), args.output)
    return 0


def cmd_digest(args: argparse.Namespace) -> int:
    client = _get_client(args.rate_limit, args.timeout)
    snapshot = build_sync_snapshot(client, include_contents=False)
    digest = generate_daily_digest(snapshot, limit=args.limit)
    _write_output(digest, args.output)
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    client = _get_client(args.rate_limit, args.timeout)
    snapshot = build_sync_snapshot(client, include_contents=False)
    plan = generate_study_plan(
        snapshot,
        days=args.days,
        grade_threshold=args.grade_threshold,
    )
    _write_output(plan, args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Moodle Student Sync CLI")
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=15.0,
        help="Seconds to sleep after each API call.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP request timeout in seconds.",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. Defaults to stdout.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Perform full sync snapshot.")
    sync_parser.add_argument(
        "--include-contents",
        action="store_true",
        help="Fetch per-course section/module contents for active courses.",
    )
    sync_parser.add_argument(
        "--max-courses",
        type=int,
        default=5,
        help="Maximum active courses to fetch contents for when include-contents is enabled.",
    )
    sync_parser.set_defaults(func=cmd_sync)

    deadlines_parser = subparsers.add_parser("deadlines", help="Show upcoming deadlines/events.")
    deadlines_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of events to include.",
    )
    deadlines_parser.set_defaults(func=cmd_deadlines)

    grades_parser = subparsers.add_parser("grades", help="Show grade overview.")
    grades_parser.set_defaults(func=cmd_grades)

    digest_parser = subparsers.add_parser("digest", help="Generate daily markdown digest.")
    digest_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of events/notifications in digest sections.",
    )
    digest_parser.set_defaults(func=cmd_digest)

    plan_parser = subparsers.add_parser("plan", help="Generate study plan markdown.")
    plan_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Planning horizon in days.",
    )
    plan_parser.add_argument(
        "--grade-threshold",
        type=float,
        default=70.0,
        help="Courses below this raw grade are flagged for recovery.",
    )
    plan_parser.set_defaults(func=cmd_plan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except MoodleAPIError as exc:
        print(f"Moodle API error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

