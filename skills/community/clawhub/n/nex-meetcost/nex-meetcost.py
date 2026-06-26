#!/usr/bin/env python3
"""
Nex MeetCost - Meeting cost calculator.
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sys
import os
import json
import argparse
import datetime as dt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.storage import (
    init_db, calculate_cost, save_meeting, get_meeting,
    list_meetings, get_stats, export_meetings,
)
from lib.config import (
    MEETING_TYPES, DEFAULT_RATES, CURRENCY_SYMBOL,
    SEPARATOR, SUBSEPARATOR, EXPORT_DIR,
)

FOOTER = "[MeetCost by Nex AI | nex-ai.be]"


# --- Helpers ---

def _fmt_money(amount):
    return f"{CURRENCY_SYMBOL}{amount:,.2f}"


def _fmt_duration(minutes):
    h = int(minutes // 60)
    m = int(minutes % 60)
    if h > 0 and m > 0:
        return f"{h}h {m}m"
    if h > 0:
        return f"{h}h"
    return f"{m}m"


def _fmt_date(iso_str):
    if not iso_str:
        return "N/A"
    try:
        return dt.date.fromisoformat(iso_str[:10]).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return iso_str


def _parse_attendees(raw):
    """Parse attendees from 'name:role:rate,name:role,name' format."""
    result = []
    for part in raw.split(','):
        parts = part.strip().split(':')
        entry = {'name': parts[0].strip()}
        if len(parts) > 1 and parts[1].strip():
            entry['role'] = parts[1].strip()
        if len(parts) > 2 and parts[2].strip():
            try:
                entry['rate'] = float(parts[2].strip())
            except ValueError:
                pass
        result.append(entry)
    return result


# --- Commands ---

def cmd_calc(args):
    init_db()

    attendee_list = _parse_attendees(args.attendees)
    total, details = calculate_cost(args.duration, attendee_list)

    print(f"\n{SEPARATOR}")
    print(f"MEETING COST: {args.title or 'Quick calculation'}")
    print(f"{SEPARATOR}\n")

    print(f"Duration: {_fmt_duration(args.duration)}")
    print(f"Attendees: {len(details)}\n")

    for d in details:
        print(f"  {d['name']:<20} {d['role']:<12} {_fmt_money(d['rate'])}/h  = {_fmt_money(d['cost'])}")

    print(f"\n{SUBSEPARATOR}")
    print(f"TOTAL COST: {_fmt_money(total)}")

    if args.recurring:
        weekly = total * args.recurring
        monthly = weekly * 4.33
        yearly = weekly * 52
        print(f"\nRecurring {args.recurring}x/week:")
        print(f"  Weekly:  {_fmt_money(weekly)}")
        print(f"  Monthly: {_fmt_money(monthly)}")
        print(f"  Yearly:  {_fmt_money(yearly)}")

    print(f"\n{FOOTER}")

    if args.save:
        meeting_id, _, _ = save_meeting(
            title=args.title or "Untitled meeting",
            duration_minutes=args.duration,
            attendee_list=attendee_list,
            meeting_type=args.type,
            notes=args.notes,
            recurring=args.recurring is not None and args.recurring > 0,
            recurrence_weekly=args.recurring or 0,
        )
        print(f"Saved as meeting #{meeting_id}")


def cmd_log(args):
    init_db()

    attendee_list = _parse_attendees(args.attendees)

    meeting_id, total_cost, details = save_meeting(
        title=args.title,
        duration_minutes=args.duration,
        attendee_list=attendee_list,
        meeting_type=args.type,
        meeting_date=args.date,
        notes=args.notes,
        recurring=args.recurring is not None and args.recurring > 0,
        recurrence_weekly=args.recurring or 0,
    )

    print(f"\nMeeting logged (ID: {meeting_id})")
    print(f"  Title: {args.title}")
    print(f"  Duration: {_fmt_duration(args.duration)}")
    print(f"  Attendees: {len(details)}")
    print(f"  Total cost: {_fmt_money(total_cost)}")

    if args.recurring:
        monthly = total_cost * args.recurring * 4.33
        print(f"  Recurring: {args.recurring}x/week ({_fmt_money(monthly)}/month)")

    print(FOOTER)


def cmd_show(args):
    init_db()

    meeting = get_meeting(args.id)
    if not meeting:
        print(f"Meeting {args.id} not found.")
        print(FOOTER)
        return

    print(f"\n{SEPARATOR}")
    print(f"MEETING #{meeting['id']}: {meeting['title']}")
    print(f"{SEPARATOR}\n")

    print(f"Type: {meeting['meeting_type']}")
    print(f"Date: {_fmt_date(meeting['meeting_date'])}")
    print(f"Duration: {_fmt_duration(meeting['duration_minutes'])}")
    print(f"Total cost: {_fmt_money(meeting['total_cost'])}")

    if meeting['recurring']:
        weekly = meeting['total_cost'] * meeting['recurrence_weekly']
        monthly = weekly * 4.33
        print(f"Recurring: {meeting['recurrence_weekly']}x/week ({_fmt_money(monthly)}/month)")

    if meeting['attendee_details']:
        print(f"\nAttendees:")
        for a in meeting['attendee_details']:
            cost = (meeting['duration_minutes'] / 60.0) * (a['hourly_rate'] or 0)
            print(f"  {a['name']:<20} {a['role']:<12} {_fmt_money(a['hourly_rate'] or 0)}/h  = {_fmt_money(cost)}")

    if meeting['notes']:
        print(f"\nNotes: {meeting['notes']}")

    print(f"\n{FOOTER}")


def cmd_list(args):
    init_db()

    meetings = list_meetings(
        meeting_type=args.type,
        date_from=args.date_from,
        date_to=args.date_to,
        limit=args.limit or 50,
    )

    if not meetings:
        print("No meetings logged.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Date':<12} {'Duration':<10} {'Cost':<12} {'Title':<25} {'Type':<10}")
    print("-" * 74)

    total_cost = 0
    for m in meetings:
        title = m['title'][:24]
        date = _fmt_date(m['meeting_date'])
        dur = _fmt_duration(m['duration_minutes'])
        cost = _fmt_money(m['total_cost'])
        total_cost += m['total_cost']
        print(f"{m['id']:<5} {date:<12} {dur:<10} {cost:<12} {title:<25} {m['meeting_type']:<10}")

    print(f"\nTotal: {len(meetings)} meetings | {_fmt_money(total_cost)}")
    print(FOOTER)


def cmd_rates(args):
    print(f"\nDefault hourly rates:\n")
    for role, rate in sorted(DEFAULT_RATES.items()):
        print(f"  {role:<16} {_fmt_money(rate)}/h")
    print(f"\nOverride per attendee: name:role:rate")
    print(FOOTER)


def cmd_stats(args):
    init_db()

    stats = get_stats(date_from=args.date_from, date_to=args.date_to)

    print(f"\n{SEPARATOR}")
    print(f"MEETCOST STATISTICS")
    print(f"{SEPARATOR}\n")

    print(f"Total meetings: {stats['total_meetings']}")
    print(f"Total time in meetings: {_fmt_duration(stats['total_minutes'])} ({stats['total_hours']}h)")
    print(f"Total cost: {_fmt_money(stats['total_cost'])}")
    print(f"Average cost per meeting: {_fmt_money(stats['avg_cost'])}")

    if stats['monthly_recurring'] > 0:
        print(f"Monthly recurring cost: {_fmt_money(stats['monthly_recurring'])}")
        print(f"Yearly recurring cost: {_fmt_money(stats['monthly_recurring'] * 12)}")

    if stats['by_type']:
        print(f"\nBy Meeting Type:")
        for mtype, data in stats['by_type'].items():
            print(f"  {mtype:<16} {data['count']} meetings  {_fmt_duration(data['minutes']):<10} {_fmt_money(data['cost'])}")

    if stats['by_month']:
        print(f"\nCost per Month:")
        for month, data in stats['by_month'].items():
            bar = '#' * max(1, int(data['cost'] / 50))
            print(f"  {month} {bar} {_fmt_money(data['cost'])} ({data['count']})")

    print(f"\n{FOOTER}")


def cmd_export(args):
    init_db()

    data = export_meetings(format_type=args.format)
    if not data:
        print("No meetings to export.")
        return

    output_file = args.output or f"meetcost_export.{args.format}"
    output_path = EXPORT_DIR / output_file

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(data)

    print(f"Exported to {output_path}")
    print(FOOTER)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Nex MeetCost - Meeting cost calculator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # CALC
    p = subparsers.add_parser('calc', help='Calculate meeting cost (optional save)')
    p.add_argument('duration', type=float, help='Duration in minutes')
    p.add_argument('--attendees', '-a', required=True, help='Attendees: name:role:rate,name:role')
    p.add_argument('--title', '-t', help='Meeting title')
    p.add_argument('--type', default='other', choices=MEETING_TYPES, help='Meeting type')
    p.add_argument('--recurring', type=int, help='Times per week (for projection)')
    p.add_argument('--notes', help='Notes')
    p.add_argument('--save', action='store_true', help='Save to database')
    p.set_defaults(func=cmd_calc)

    # LOG
    p = subparsers.add_parser('log', help='Log a meeting with cost')
    p.add_argument('title', help='Meeting title')
    p.add_argument('duration', type=float, help='Duration in minutes')
    p.add_argument('--attendees', '-a', required=True, help='Attendees: name:role:rate,name:role')
    p.add_argument('--type', default='other', choices=MEETING_TYPES, help='Meeting type')
    p.add_argument('--date', help='Meeting date (YYYY-MM-DD)')
    p.add_argument('--recurring', type=int, help='Times per week')
    p.add_argument('--notes', help='Notes')
    p.set_defaults(func=cmd_log)

    # SHOW
    p = subparsers.add_parser('show', help='Show meeting details')
    p.add_argument('id', type=int, help='Meeting ID')
    p.set_defaults(func=cmd_show)

    # LIST
    p = subparsers.add_parser('list', help='List meetings')
    p.add_argument('--type', choices=MEETING_TYPES, help='Filter by type')
    p.add_argument('--date-from', help='From date (YYYY-MM-DD)')
    p.add_argument('--date-to', help='To date (YYYY-MM-DD)')
    p.add_argument('--limit', type=int, default=50, help='Max results')
    p.set_defaults(func=cmd_list)

    # RATES
    p = subparsers.add_parser('rates', help='Show default hourly rates')
    p.set_defaults(func=cmd_rates)

    # STATS
    p = subparsers.add_parser('stats', help='Show statistics')
    p.add_argument('--date-from', help='From date')
    p.add_argument('--date-to', help='To date')
    p.set_defaults(func=cmd_stats)

    # EXPORT
    p = subparsers.add_parser('export', help='Export meetings')
    p.add_argument('format', choices=['json', 'csv'], help='Export format')
    p.add_argument('--output', help='Output filename')
    p.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
