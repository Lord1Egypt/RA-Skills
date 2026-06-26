#!/usr/bin/env python3
"""
Calendar operations for Exchange.
Commands: list, get, create, update, delete, respond, availability.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connection import get_account
from utils import out, die, add_json_argument, confirm_or_die

from logger import get_logger

_logger = get_logger()


def parse_datetime(s: str) -> datetime:
    """Parse datetime string in various formats."""
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(
        f"Cannot parse datetime: {s}. Use format: YYYY-MM-DD HH:MM or YYYY-MM-DD"
    )


def event_to_dict(item) -> dict:
    """Serialize a CalendarItem to dict."""
    # Required attendees
    required = []
    if item.required_attendees:
        for a in item.required_attendees:
            required.append(
                {
                    "email": (
                        a.mailbox.email_address if hasattr(a, "mailbox") else str(a)
                    ),
                    "name": (
                        a.mailbox.name
                        if hasattr(a, "mailbox") and hasattr(a.mailbox, "name")
                        else None
                    ),
                    "response": getattr(a, "response_type", None),
                }
            )

    # Optional attendees
    optional = []
    if item.optional_attendees:
        for a in item.optional_attendees:
            optional.append(
                {
                    "email": (
                        a.mailbox.email_address if hasattr(a, "mailbox") else str(a)
                    ),
                    "name": (
                        a.mailbox.name
                        if hasattr(a, "mailbox") and hasattr(a.mailbox, "name")
                        else None
                    ),
                }
            )

    # Location
    location = None
    if item.location:
        location = item.location

    # Is all day event
    is_all_day = getattr(item, "is_all_day", False)

    return {
        "id": item.id,
        "subject": item.subject or "(no subject)",
        "body": item.text_body or item.body or "",
        "location": location,
        "start": str(item.start) if item.start else None,
        "end": str(item.end) if item.end else None,
        "is_all_day": is_all_day,
        "organizer": item.organizer.email_address if item.organizer else None,
        "organizer_name": (
            item.organizer.name
            if item.organizer and hasattr(item.organizer, "name")
            else None
        ),
        "required_attendees": required,
        "optional_attendees": optional,
        "is_recurring": getattr(item, "is_recurring", False),
        "reminder": getattr(item, "reminder_minutes_before_start", None),
    }


# ── Commands ────────────────────────────────────────────────────────────────


def cmd_connect(_args):
    """Test calendar connection."""
    account = get_account()
    out(
        {
            "ok": True,
            "email": str(account.primary_smtp_address),
            "calendar_total": account.calendar.total_count,
        }
    )


def cmd_list(args):
    """List calendar events in a date range."""
    from exchangelib import UTC_NOW

    account = get_account()
    calendar = account.calendar

    # Use UTC_NOW (returns EWSDateTime with timezone)
    now = UTC_NOW()

    # Parse start date
    if args.start:
        start_dt = parse_datetime(args.start)
        start_ews = now.replace(
            year=start_dt.year,
            month=start_dt.month,
            day=start_dt.day,
            hour=start_dt.hour if hasattr(start_dt, "hour") else 0,
            minute=start_dt.minute if hasattr(start_dt, "minute") else 0,
            second=start_dt.second if hasattr(start_dt, "second") else 0,
            microsecond=0,
        )
    else:
        start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_ews = start_dt

    # Parse end date
    if args.end:
        end_dt = parse_datetime(args.end)
        end_ews = now.replace(
            year=end_dt.year,
            month=end_dt.month,
            day=end_dt.day,
            hour=end_dt.hour if hasattr(end_dt, "hour") else 0,
            minute=end_dt.minute if hasattr(end_dt, "minute") else 0,
            second=end_dt.second if hasattr(end_dt, "second") else 0,
            microsecond=0,
        )
    else:
        end_ews = start_ews + timedelta(days=args.days)

    # Query
    try:
        items = calendar.filter(
            start__lt=end_ews,
            end__gt=start_ews,
        ).order_by("start")
    except Exception as e:
        die(f"Failed to query calendar: {e}")

    events = []
    for item in items[: args.limit]:
        try:
            events.append(event_to_dict(item))
        except Exception:
            # Skip problematic events
            continue

    out(
        {
            "ok": True,
            "count": len(events),
            "start": str(start_ews),
            "end": str(end_ews),
            "events": events,
        }
    )


def cmd_get(args):
    """Get event details by ID."""
    account = get_account()

    try:
        item = account.calendar.get(id=args.id)
    except Exception as e:
        die(f"Event not found: {e}")

    out({"ok": True, "event": event_to_dict(item)})


def cmd_create(args):
    """Create a new calendar event."""
    confirm_or_die(f"Create calendar event \"{args.subject}\" at {args.start}")

    from exchangelib import EWSDateTime
    from exchangelib.items import CalendarItem
    from exchangelib.properties import Attendee, Mailbox

    account = get_account()
    calendar = account.calendar

    # Parse dates
    start_dt = parse_datetime(args.start)
    end_dt = parse_datetime(args.end) if args.end else None

    if not end_dt:
        if args.duration:
            end_dt = start_dt + timedelta(minutes=args.duration)
        else:
            end_dt = start_dt + timedelta(hours=1)

    # Convert to EWSDateTime (timezone-aware required)
    from exchangelib import UTC

    # Use UTC timezone
    start_ews = EWSDateTime(
        start_dt.year,
        start_dt.month,
        start_dt.day,
        start_dt.hour,
        start_dt.minute,
        start_dt.second,
        tzinfo=UTC,
    )
    end_ews = EWSDateTime(
        end_dt.year,
        end_dt.month,
        end_dt.day,
        end_dt.hour,
        end_dt.minute,
        end_dt.second,
        tzinfo=UTC,
    )

    # Build attendees
    required_attendees = None
    if args.to:
        to_list = [a.strip() for a in args.to.split(",")]
        required_attendees = [
            Attendee(mailbox=Mailbox(email_address=email), response_type="Unknown")
            for email in to_list
        ]

    optional_attendees = None
    if getattr(args, "cc", None):
        cc_list = [a.strip() for a in args.cc.split(",")]
        optional_attendees = [
            Attendee(mailbox=Mailbox(email_address=email), response_type="Unknown")
            for email in cc_list
        ]

    # Create event
    kwargs = {
        "account": account,
        "folder": calendar,
        "subject": args.subject,
        "body": args.body or "",
        "start": start_ews,
        "end": end_ews,
        "location": args.location or "",
        "required_attendees": required_attendees,
        "optional_attendees": optional_attendees,
    }

    if args.all_day:
        kwargs["is_all_day"] = True

    if args.reminder:
        kwargs["reminder_minutes_before_start"] = args.reminder

    try:
        from exchangelib.items import SEND_TO_ALL_AND_SAVE_COPY

        item = CalendarItem(**kwargs)
        # Send meeting invitations to all attendees
        if required_attendees or optional_attendees:
            item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)
        else:
            item.save()
    except Exception as e:
        die(f"Failed to create event: {e}")

    out(
        {
            "ok": True,
            "message": "Event created",
            "id": item.id,
            "subject": args.subject,
            "start": str(start_dt),
            "end": str(end_dt),
        }
    )


def cmd_update(args):
    """Update an existing calendar event."""
    account = get_account()

    try:
        item = account.calendar.get(id=args.id)
    except Exception as e:
        die(f"Event not found: {e}")

    update_fields = []

    if args.subject:
        item.subject = args.subject
        update_fields.append("subject")

    if args.body is not None:
        item.body = args.body
        update_fields.append("body")

    if args.location:
        item.location = args.location
        update_fields.append("location")

    if args.start:
        from exchangelib import EWSDateTime

        start_dt = parse_datetime(args.start)
        item.start = EWSDateTime.from_datetime(start_dt, tzinfo=None)
        update_fields.append("start")

    if args.end:
        from exchangelib import EWSDateTime

        end_dt = parse_datetime(args.end)
        item.end = EWSDateTime.from_datetime(end_dt, tzinfo=None)
        update_fields.append("end")

    if not update_fields:
        die("No fields to update")

    try:
        item.save(update_fields=update_fields)
    except Exception as e:
        die(f"Failed to update event: {e}")

    out(
        {
            "ok": True,
            "message": "Event updated",
            "id": args.id,
            "updated_fields": update_fields,
        }
    )


def cmd_delete(args):
    """Delete a calendar event."""
    confirm_or_die(f"Delete calendar event {args.id}")

    account = get_account()

    try:
        item = account.calendar.get(id=args.id)
    except Exception as e:
        die(f"Event not found: {e}")

    subject = item.subject
    item.delete()

    out({"ok": True, "message": "Event deleted", "id": args.id, "subject": subject})


def cmd_respond(args):
    """Accept, decline, or tentatively accept a meeting request."""
    confirm_or_die(f"{args.response.capitalize()} meeting {args.id}")

    account = get_account()

    try:
        item = account.calendar.get(id=args.id)
    except Exception as e:
        die(f"Event not found: {e}")

    response_type = args.response.lower()

    if response_type == "accept":
        item.accept(args.body or "")
        msg = "Meeting accepted"
    elif response_type == "decline":
        item.decline(args.body or "")
        msg = "Meeting declined"
    elif response_type in ("tentative", "maybe"):
        item.tentatively_accept(args.body or "")
        msg = "Tentatively accepted"
    else:
        die(f"Invalid response type: {response_type}. Use: accept, decline, tentative")

    out({"ok": True, "message": msg, "id": args.id})


def cmd_availability(args):
    """Check free/busy status for an email address."""
    # Note: GetUserAvailability API is complex and requires specific timezone setup.
    # For now, this returns a helpful message suggesting to check calendar directly.

    start_dt = parse_datetime(args.start)
    if args.end:
        end_dt = parse_datetime(args.end)
    else:
        end_dt = start_dt + timedelta(hours=24)

    out(
        {
            "ok": True,
            "email": args.email,
            "start": str(start_dt),
            "end": str(end_dt),
            "message": "Free/busy API requires complex timezone setup. Use 'cal.py list --email ADDR --days N' to check calendar events directly.",
            "tip": "For your own calendar, use 'cal.py list' or 'cal.py today'. For others, ask them to share their calendar.",
        }
    )


# ── CLI ───────────────────────────────────────────────────────────────────────
def cmd_today(args):
    """List today's events."""
    today = datetime.now().strftime("%Y-%m-%d")
    list_args = argparse.Namespace(start=today, end=None, days=1, limit=args.limit or 20)
    return cmd_list(list_args)


def cmd_week(args):
    """List this week's events."""
    now = datetime.now()
    start_of_week = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
    end_of_week = (now + timedelta(days=7 - now.weekday())).strftime("%Y-%m-%d")
    list_args = argparse.Namespace(start=start_of_week, end=end_of_week, days=7, limit=args.limit or 50)
    return cmd_list(list_args)

def main():
    add_json_argument(parser)
    parser = argparse.ArgumentParser(
        prog="cal.py",
        description="Exchange calendar operations",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # connect
    p_connect = sub.add_parser("connect", help="Test calendar connection")
    p_connect.set_defaults(func=cmd_connect)
    add_json_argument(p_connect)

    # list
    p_list = sub.add_parser("list", help="List events in date range")
    p_list.add_argument("--start", "-s", help="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)")
    p_list.add_argument("--end", "-e", help="End date")
    p_list.add_argument("--days", "-d", type=int, default=7, help="Days to show (default 7)")
    p_list.add_argument("--limit", "-n", type=int, default=50, help="Max events")
    p_list.set_defaults(func=cmd_list)
    add_json_argument(p_list)

    # today
    p_today = sub.add_parser("today", help="List today's events")
    p_today.add_argument("--limit", "-n", type=int, default=20, help="Max events")
    p_today.set_defaults(func=cmd_today)
    add_json_argument(p_today)

    # week
    p_week = sub.add_parser("week", help="List this week's events")
    p_week.add_argument("--limit", "-n", type=int, default=50, help="Max events")
    p_week.set_defaults(func=cmd_week)
    add_json_argument(p_week)

    # get
    p_get = sub.add_parser("get", help="Get event details")
    p_get.add_argument("--id", "-i", required=True, help="Event ID")
    p_get.set_defaults(func=cmd_get)
    add_json_argument(p_get)

    # create
    p_create = sub.add_parser("create", help="Create event")
    p_create.add_argument("--subject", "-s", required=True, help="Event subject")
    p_create.add_argument("--start", required=True, help="Start date/time (YYYY-MM-DD HH:MM)")
    p_create.add_argument("--end", help="End date/time (YYYY-MM-DD HH:MM)")
    p_create.add_argument("--duration", type=int, default=60, help="Duration in minutes")
    p_create.add_argument("--location", "-l", help="Location")
    p_create.add_argument("--body", "-b", help="Body/description")
    p_create.add_argument("--to", "-t", help="Attendees (comma-separated emails)")
    p_create.add_argument("--all-day", action="store_true", help="All-day event")
    p_create.add_argument("--reminder", type=int, help="Reminder minutes before")
    p_create.set_defaults(func=cmd_create)
    add_json_argument(p_create)

    # update
    p_update = sub.add_parser("update", help="Update event")
    p_update.add_argument("--id", "-i", required=True, help="Event ID")
    p_update.add_argument("--subject", "-s", help="New subject")
    p_update.add_argument("--location", "-l", help="New location")
    p_update.add_argument("--start", help="New start date/time")
    p_update.add_argument("--end", help="New end date/time")
    p_update.add_argument("--body", "-b", help="New body")
    p_update.set_defaults(func=cmd_update)
    add_json_argument(p_update)

    # delete
    p_delete = sub.add_parser("delete", help="Delete event")
    p_delete.add_argument("--id", "-i", required=True, help="Event ID")
    p_delete.set_defaults(func=cmd_delete)
    add_json_argument(p_delete)

    # respond
    p_respond = sub.add_parser("respond", help="Respond to meeting")
    p_respond.add_argument("--id", "-i", required=True, help="Event ID")
    p_respond.add_argument("--response", "-r", required=True, choices=["accept", "decline", "tentative"], help="Response")
    p_respond.add_argument("--body", "-b", help="Response message")
    p_respond.set_defaults(func=cmd_respond)
    add_json_argument(p_respond)
    add_yes_argument(p_respond)

    # availability
    p_avail = sub.add_parser("availability", help="Check availability")
    p_avail.add_argument("--email", "-e", required=True, help="Email address")
    p_avail.add_argument("--start", "-s", required=True, help="Start date")
    p_avail.add_argument("--end", help="End date")
    p_avail.set_defaults(func=cmd_availability)
    add_json_argument(p_avail)

    args = parser.parse_args()

    dispatch = {
        "connect": cmd_connect,
        "list": cmd_list,
        "today": cmd_today,
        "week": cmd_week,
        "get": cmd_get,
        "create": cmd_create,
        "update": cmd_update,
        "delete": cmd_delete,
        "respond": cmd_respond,
        "availability": cmd_availability,
    }

    try:
        dispatch[args.cmd](args)
    except SystemExit:
        raise
    except Exception as e:
        die(str(e))


def add_parser(subparsers):
    """Add calendar commands to CLI parser."""
    # connect
    p_connect = subparsers.add_parser("connect", help="Test calendar connection")
    p_connect.set_defaults(func=cmd_connect)
    add_json_argument(p_connect)

    # list
    p_list = subparsers.add_parser("list", help="List events in date range")
    p_list.add_argument("--start", "-s", help="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)")
    p_list.add_argument("--end", "-e", help="End date")
    p_list.add_argument("--days", "-d", type=int, default=7, help="Days to show (default 7)")
    p_list.add_argument("--limit", "-n", type=int, default=50, help="Max events")
    p_list.set_defaults(func=cmd_list)
    add_json_argument(p_list)

    # today
    p_today = subparsers.add_parser("today", help="List today's events")
    p_today.add_argument("--limit", "-n", type=int, default=20, help="Max events")
    p_today.set_defaults(func=cmd_today)
    add_json_argument(p_today)

    # week
    p_week = subparsers.add_parser("week", help="List this week's events")
    p_week.add_argument("--limit", "-n", type=int, default=50, help="Max events")
    p_week.set_defaults(func=cmd_week)
    add_json_argument(p_week)

    # get
    p_get = subparsers.add_parser("get", help="Get event details")
    p_get.add_argument("--id", "-i", required=True, help="Event ID")
    p_get.set_defaults(func=cmd_get)
    add_json_argument(p_get)

    # create
    p_create = subparsers.add_parser("create", help="Create event")
    p_create.add_argument("--subject", "-s", required=True, help="Event subject")
    p_create.add_argument("--start", required=True, help="Start date/time (YYYY-MM-DD HH:MM)")
    p_create.add_argument("--end", help="End date/time (YYYY-MM-DD HH:MM)")
    p_create.add_argument("--duration", type=int, default=60, help="Duration in minutes")
    p_create.add_argument("--location", "-l", help="Location")
    p_create.add_argument("--body", "-b", help="Body/description")
    p_create.add_argument("--to", "-t", help="Attendees (comma-separated emails)")
    p_create.add_argument("--all-day", action="store_true", help="All-day event")
    p_create.add_argument("--reminder", type=int, help="Reminder minutes before")
    p_create.set_defaults(func=cmd_create)
    add_json_argument(p_create)

    # update
    p_update = subparsers.add_parser("update", help="Update event")
    p_update.add_argument("--id", "-i", required=True, help="Event ID")
    p_update.add_argument("--subject", "-s", help="New subject")
    p_update.add_argument("--location", "-l", help="New location")
    p_update.add_argument("--start", help="New start date/time")
    p_update.add_argument("--end", help="New end date/time")
    p_update.add_argument("--body", "-b", help="New body")
    p_update.set_defaults(func=cmd_update)
    add_json_argument(p_update)

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete event")
    p_delete.add_argument("--id", "-i", required=True, help="Event ID")
    p_delete.set_defaults(func=cmd_delete)
    add_json_argument(p_delete)

    # respond
    p_respond = subparsers.add_parser("respond", help="Respond to meeting")
    p_respond.add_argument("--id", "-i", required=True, help="Event ID")
    p_respond.add_argument("--response", "-r", required=True, choices=["accept", "decline", "tentative"], help="Response")
    p_respond.add_argument("--body", "-b", help="Response message")
    p_respond.set_defaults(func=cmd_respond)
    add_json_argument(p_respond)
    add_yes_argument(p_respond)

    # availability
    p_avail = subparsers.add_parser("availability", help="Check availability")
    p_avail.add_argument("--email", "-e", required=True, help="Email address")
    p_avail.add_argument("--start", "-s", required=True, help="Start date")
    p_avail.add_argument("--end", help="End date")
    p_avail.set_defaults(func=cmd_availability)
    add_json_argument(p_avail)


if __name__ == "__main__":
    main()