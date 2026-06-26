#!/usr/bin/env python3
"""
Microsoft Graph calendar operations for OpenClaw msgraph skill.

NOTE: Named cal.py (not calendar.py) to avoid Python stdlib conflict.

Usage:
  python cal.py list [--days N] [--calendar NAME]
  python cal.py get <event_id>
  python cal.py create --subject "..." --start "YYYY-MM-DDTHH:MM" --end "YYYY-MM-DDTHH:MM"
                       [--tz "America/New_York"] [--location "..."] [--body "..."]
                       [--attendees "email1,email2"]
  python cal.py delete <event_id> [--confirm]
  python cal.py calendars
"""

import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import auth
import graph_api
import utils

DEFAULT_TZ = "America/New_York"


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_list(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--days", type=int, default=7, help="Number of days to list")
    parser.add_argument("--calendar", default=None, help="Calendar ID")
    parsed = parser.parse_args(args)

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=parsed.days)
    start_str = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    path = f"/me/calendars/{parsed.calendar}/calendarView" if parsed.calendar else "/me/calendarView"
    params = {
        "startDateTime": start_str,
        "endDateTime": end_str,
        "$top": "50",
        "$orderby": "start/dateTime",
        "$select": "id,subject,start,end,location,isAllDay,organizer,attendees,bodyPreview,isCancelled,onlineMeetingUrl",
    }
    result = graph_api.graph_get(path, params)
    events = result.get("value", [])

    if not events:
        print(f"No events in the next {parsed.days} days.")
        return

    print(f"\n{'─'*80}")
    print(f"  CALENDAR — next {parsed.days} days ({len(events)} events)")
    print(f"{'─'*80}\n")
    for ev in events:
        if ev.get("isCancelled"):
            continue
        start = ev.get("start", {})
        end_ = ev.get("end", {})
        loc = ev.get("location", {}).get("displayName", "")
        organizer = ev.get("organizer", {}).get("emailAddress", {})
        attendees = ev.get("attendees", [])
        attendee_list = [a["emailAddress"]["address"] for a in attendees[:5]]
        online = "🔗 " if ev.get("onlineMeetingUrl") else ""

        print(f"  {online}{ev.get('subject', '(no subject)')}")
        if ev.get("isAllDay"):
            print(f"  📅 All day · {start.get('dateTime', '')[:10]}")
        else:
            print(f"  🕐 {utils.format_datetime(start.get('dateTime', ''))}")
            print(f"     → {utils.format_datetime(end_.get('dateTime', ''))}")
        if loc:
            print(f"  📍 {loc}")
        if attendees:
            print(f"  👥 {', '.join(attendee_list)}{' +more' if len(attendees) > 5 else ''}")
        print(f"  ID: {ev['id']}")
        print()

def cmd_get(args):
    if not args:
        print("Usage: python cal.py get <event_id>")
        sys.exit(1)
    event_id = args[0]
    params = {"$select": "id,subject,start,end,location,body,organizer,attendees,isAllDay,onlineMeetingUrl,isCancelled,webLink"}
    ev = graph_api.graph_get(f"/me/events/{event_id}", params)

    start = ev.get("start", {})
    end_ = ev.get("end", {})
    body = ev.get("body", {}).get("content", "")
    body_type = ev.get("body", {}).get("contentType", "")
    organizer = ev.get("organizer", {}).get("emailAddress", {})
    attendees = ev.get("attendees", [])

    print(f"\nSubject:   {ev.get('subject', '(no subject)')}")
    print(f"Start:     {utils.format_datetime(start.get('dateTime', ''))} ({start.get('timeZone', '')})")
    print(f"End:       {utils.format_datetime(end_.get('dateTime', ''))} ({end_.get('timeZone', '')})")
    print(f"Location:  {ev.get('location', {}).get('displayName', '(none)')}")
    print(f"Organizer: {organizer.get('name', '')} <{organizer.get('address', '')}>")
    if attendees:
        print("Attendees:")
        for a in attendees:
            ea = a["emailAddress"]
            status = a.get("status", {}).get("response", "none")
            print(f"  - {ea.get('name', '')} <{ea.get('address', '')}> [{status}]")
    if ev.get("onlineMeetingUrl"):
        print(f"Meeting:   {ev['onlineMeetingUrl']}")
    print(f"{'─'*80}")
    if body_type == "html":
        body = utils.strip_html(body)
    if body.strip():
        print(body[:2000])

def cmd_create(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--start", required=True, help="YYYY-MM-DDTHH:MM")
    parser.add_argument("--end", required=True, help="YYYY-MM-DDTHH:MM")
    parser.add_argument("--tz", default=DEFAULT_TZ)
    parser.add_argument("--location", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--attendees", default="", help="Comma-separated emails")
    parser.add_argument("--all-day", action="store_true")
    parser.add_argument("--calendar", default=None, help="Calendar ID")
    parsed = parser.parse_args(args)

    event = {
        "subject": parsed.subject,
        "start": utils.parse_local_datetime(parsed.start, parsed.tz),
        "end": utils.parse_local_datetime(parsed.end, parsed.tz),
        "isAllDay": parsed.all_day,
    }
    if parsed.location:
        event["location"] = {"displayName": parsed.location}
    if parsed.body:
        event["body"] = {"contentType": "text", "content": parsed.body}
    if parsed.attendees:
        emails = [e.strip() for e in parsed.attendees.split(",") if e.strip()]
        event["attendees"] = [
            {"emailAddress": {"address": e}, "type": "required"} for e in emails
        ]

    path = f"/me/calendars/{parsed.calendar}/events" if parsed.calendar else "/me/events"
    result = graph_api.graph_post(path, event)
    print(f"✓ Event created: {result.get('subject', '?')}")
    print(f"  ID:    {result.get('id', '?')}")
    print(f"  Start: {utils.format_datetime(result.get('start', {}).get('dateTime', ''))}")
    print(f"  End:   {utils.format_datetime(result.get('end', {}).get('dateTime', ''))}")
    if result.get("webLink"):
        print(f"  Link:  {result['webLink']}")

def cmd_delete(args):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("event_id", help="Event ID to delete")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation prompt")
    parsed = parser.parse_args(args)

    if not parsed.confirm:
        answer = input(f"Delete event {parsed.event_id[:48]}...? [y/N] ")
        if answer.lower() != "y":
            print("Cancelled.")
            return

    graph_api.graph_delete(f"/me/events/{parsed.event_id}")
    print(f"✓ Event deleted.")

def cmd_calendars(args):
    result = graph_api.graph_get("/me/calendars", {
        "$select": "id,name,isDefaultCalendar,canEdit,color",
        "$top": "50",
    })
    cals = result.get("value", [])
    print(f"\n  CALENDARS ({len(cals)})\n")
    for c in cals:
        default = " [default]" if c.get("isDefaultCalendar") else ""
        edit = " (read-only)" if not c.get("canEdit") else ""
        print(f"  {c['name']}{default}{edit}")
        print(f"  ID: {c['id']}")
        print()


# ── Entry point ───────────────────────────────────────────────────────────────

COMMANDS = {
    "list": cmd_list,
    "get": cmd_get,
    "create": cmd_create,
    "delete": cmd_delete,
    "calendars": cmd_calendars,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Usage: python cal.py <command> [args]")
        print("Commands:", ", ".join(COMMANDS.keys()))
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])
