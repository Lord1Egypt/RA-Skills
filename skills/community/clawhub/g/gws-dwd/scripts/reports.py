#!/usr/bin/env python3
"""Admin SDK Reports API — audit logs, login activity, usage reports."""

import argparse
import json
import sys
from typing import Optional

from auth import get_service


def login_activity(
    user_key: str = "all",
    max_results: int = 25,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    event_name: Optional[str] = None,
) -> dict:
    """Get login activity report.

    Args:
        user_key: Email address or 'all' for everyone.
        max_results: Max activities to return.
        start_time: ISO 8601 start time (optional).
        end_time: ISO 8601 end time (optional).
        event_name: Filter by event (login_success, login_failure, logout, etc).

    Returns:
        Dict with login activities.
    """
    service = get_service("reports")
    kwargs = {
        "userKey": user_key,
        "applicationName": "login",
        "maxResults": max_results,
    }
    if start_time:
        kwargs["startTime"] = start_time
    if end_time:
        kwargs["endTime"] = end_time
    if event_name:
        kwargs["eventName"] = event_name

    results = service.activities().list(**kwargs).execute()
    activities = results.get("items", [])

    return {
        "report": "login",
        "user_key": user_key,
        "total": len(activities),
        "activities": [_parse_activity(a) for a in activities],
    }


def admin_activity(
    max_results: int = 25,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    event_name: Optional[str] = None,
) -> dict:
    """Get admin console activity report.

    Args:
        max_results: Max activities to return.
        start_time: ISO 8601 start time.
        end_time: ISO 8601 end time.
        event_name: Filter by event name.

    Returns:
        Dict with admin activities.
    """
    service = get_service("reports")
    kwargs = {
        "userKey": "all",
        "applicationName": "admin",
        "maxResults": max_results,
    }
    if start_time:
        kwargs["startTime"] = start_time
    if end_time:
        kwargs["endTime"] = end_time
    if event_name:
        kwargs["eventName"] = event_name

    results = service.activities().list(**kwargs).execute()
    activities = results.get("items", [])

    return {
        "report": "admin",
        "total": len(activities),
        "activities": [_parse_activity(a) for a in activities],
    }


def drive_activity(
    user_key: str = "all",
    max_results: int = 25,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    event_name: Optional[str] = None,
) -> dict:
    """Get Google Drive activity report.

    Args:
        user_key: Email address or 'all'.
        max_results: Max activities to return.
        start_time: ISO 8601 start time.
        end_time: ISO 8601 end time.
        event_name: Filter by event (view, edit, create, download, etc).

    Returns:
        Dict with Drive activities.
    """
    service = get_service("reports")
    kwargs = {
        "userKey": user_key,
        "applicationName": "drive",
        "maxResults": max_results,
    }
    if start_time:
        kwargs["startTime"] = start_time
    if end_time:
        kwargs["endTime"] = end_time
    if event_name:
        kwargs["eventName"] = event_name

    results = service.activities().list(**kwargs).execute()
    activities = results.get("items", [])

    return {
        "report": "drive",
        "user_key": user_key,
        "total": len(activities),
        "activities": [_parse_activity(a) for a in activities],
    }


def token_activity(
    user_key: str = "all",
    max_results: int = 25,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> dict:
    """Get OAuth token activity — third-party app access grants/revocations.

    Args:
        user_key: Email address or 'all'.
        max_results: Max activities to return.
        start_time: ISO 8601 start time.
        end_time: ISO 8601 end time.

    Returns:
        Dict with token activities.
    """
    service = get_service("reports")
    kwargs = {
        "userKey": user_key,
        "applicationName": "token",
        "maxResults": max_results,
    }
    if start_time:
        kwargs["startTime"] = start_time
    if end_time:
        kwargs["endTime"] = end_time

    results = service.activities().list(**kwargs).execute()
    activities = results.get("items", [])

    return {
        "report": "token",
        "user_key": user_key,
        "total": len(activities),
        "activities": [_parse_activity(a) for a in activities],
    }


def gmail_activity(
    user_key: str = "all",
    max_results: int = 25,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> dict:
    """Get Gmail activity logs (messages sent, received, etc).

    Note: This reports on email activity metadata, not content.

    Args:
        user_key: Email address or 'all'.
        max_results: Max activities to return.
        start_time: ISO 8601 start time.
        end_time: ISO 8601 end time.

    Returns:
        Dict with Gmail activities.
    """
    service = get_service("reports")
    kwargs = {
        "userKey": user_key,
        "applicationName": "gmail",
        "maxResults": max_results,
    }
    if start_time:
        kwargs["startTime"] = start_time
    if end_time:
        kwargs["endTime"] = end_time

    results = service.activities().list(**kwargs).execute()
    activities = results.get("items", [])

    return {
        "report": "gmail",
        "user_key": user_key,
        "total": len(activities),
        "activities": [_parse_activity(a) for a in activities],
    }


def _parse_activity(activity: dict) -> dict:
    """Parse a raw activity into a clean dict."""
    actor = activity.get("actor", {})
    events = activity.get("events", [])

    parsed_events = []
    for event in events:
        params = {}
        for p in event.get("parameters", []):
            name = p.get("name", "")
            value = p.get("value") or p.get("intValue") or p.get("boolValue") or p.get("multiValue", "")
            params[name] = value
        parsed_events.append({
            "type": event.get("type", ""),
            "name": event.get("name", ""),
            "parameters": params,
        })

    return {
        "time": activity.get("id", {}).get("time", ""),
        "actor_email": actor.get("email", ""),
        "actor_name": actor.get("profileId", ""),
        "ip_address": activity.get("ipAddress", ""),
        "events": parsed_events,
    }


def main():
    parser = argparse.ArgumentParser(description="GWS Reports API")
    sub = parser.add_subparsers(dest="command", required=True)

    # login
    p_login = sub.add_parser("login", help="Login activity")
    p_login.add_argument("--user", default="all")
    p_login.add_argument("--max", type=int, default=25)
    p_login.add_argument("--start", help="ISO 8601 start time")
    p_login.add_argument("--end", help="ISO 8601 end time")
    p_login.add_argument("--event", help="Event name filter")

    # admin
    p_admin = sub.add_parser("admin", help="Admin activity")
    p_admin.add_argument("--max", type=int, default=25)
    p_admin.add_argument("--start")
    p_admin.add_argument("--end")
    p_admin.add_argument("--event")

    # drive
    p_drive = sub.add_parser("drive", help="Drive activity")
    p_drive.add_argument("--user", default="all")
    p_drive.add_argument("--max", type=int, default=25)
    p_drive.add_argument("--start")
    p_drive.add_argument("--end")
    p_drive.add_argument("--event")

    # token
    p_token = sub.add_parser("token", help="OAuth token activity")
    p_token.add_argument("--user", default="all")
    p_token.add_argument("--max", type=int, default=25)
    p_token.add_argument("--start")
    p_token.add_argument("--end")

    # gmail
    p_gmail = sub.add_parser("gmail", help="Gmail activity")
    p_gmail.add_argument("--user", default="all")
    p_gmail.add_argument("--max", type=int, default=25)
    p_gmail.add_argument("--start")
    p_gmail.add_argument("--end")

    args = parser.parse_args()

    try:
        if args.command == "login":
            result = login_activity(args.user, args.max, args.start, args.end, getattr(args, "event", None))
        elif args.command == "admin":
            result = admin_activity(args.max, args.start, args.end, getattr(args, "event", None))
        elif args.command == "drive":
            result = drive_activity(args.user, args.max, args.start, args.end, getattr(args, "event", None))
        elif args.command == "token":
            result = token_activity(args.user, args.max, args.start, args.end)
        elif args.command == "gmail":
            result = gmail_activity(args.user, args.max, args.start, args.end)
        else:
            result = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
