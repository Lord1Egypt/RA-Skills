#!/usr/bin/env python3
"""
Nex Timetrack - Billable time logger for freelancers and agencies.
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sys
import os
import json
import argparse
import datetime as dt
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.storage import (
    init_db, start_timer, stop_timer, get_active_timer, cancel_timer,
    save_entry, get_entry, list_entries, update_entry, delete_entry,
    search_entries, save_client, get_client, find_client_by_name,
    list_clients, save_project, get_project, find_project_by_name,
    list_projects, get_summary, get_stats, export_entries,
)
from lib.config import (
    CATEGORIES, DEFAULT_RATE, CURRENCY_SYMBOL,
    ROUND_TO_MINUTES, SEPARATOR, SUBSEPARATOR, EXPORT_DIR,
)

FOOTER = "[Timetrack by Nex AI | nex-ai.be]"


# --- Helpers ---

def _fmt_duration(minutes):
    if not minutes:
        return "0m"
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


def _fmt_time(iso_str):
    if not iso_str:
        return ""
    try:
        return dt.datetime.fromisoformat(iso_str).strftime("%H:%M")
    except (ValueError, TypeError):
        return ""


def _fmt_money(amount):
    return f"{CURRENCY_SYMBOL}{amount:,.2f}"


def _parse_duration(raw):
    raw = raw.strip().lower()
    if 'h' in raw and 'm' in raw:
        parts = raw.replace('m', '').split('h')
        return float(parts[0]) * 60 + float(parts[1])
    if raw.endswith('h'):
        return float(raw[:-1]) * 60
    if raw.endswith('m'):
        return float(raw[:-1])
    return float(raw) * 60


def _resolve_client(name):
    if not name:
        return None
    clients = find_client_by_name(name)
    if clients:
        return clients[0]['id']
    return None


def _resolve_project(name):
    if not name:
        return None
    projects = find_project_by_name(name)
    if projects:
        return projects[0]['id']
    return None


# --- Commands ---

def cmd_start(args):
    init_db()

    client_id = _resolve_client(args.client)
    project_id = _resolve_project(args.project)
    billable = not args.non_billable
    tags = args.tags

    started, existing = start_timer(
        description=args.description,
        project_id=project_id,
        client_id=client_id,
        category=args.category,
        billable=billable,
        tags=tags,
    )

    if existing:
        elapsed = dt.datetime.now() - dt.datetime.fromisoformat(existing['started_at'])
        mins = elapsed.total_seconds() / 60.0
        print(f"Timer already running: {existing['description']} ({_fmt_duration(mins)})")
        print(f"Stop it first: nex-timetrack stop")
    else:
        print(f"Timer started: {args.description}")
        print(f"  Started: {_fmt_time(started)}")
        if args.client:
            print(f"  Client: {args.client}")
        if args.project:
            print(f"  Project: {args.project}")
        print(f"  Category: {args.category}")
        print(f"  Billable: {'yes' if billable else 'no'}")
    print(FOOTER)


def cmd_stop(args):
    init_db()

    result = stop_timer(notes=args.notes)
    if not result:
        print("No active timer.")
        print(FOOTER)
        return

    print(f"Timer stopped (Entry #{result['entry_id']})")
    print(f"  Task: {result['description']}")
    print(f"  Duration: {_fmt_duration(result['duration_minutes'])}")
    print(f"  From: {_fmt_time(result['started_at'])} to {_fmt_time(result['ended_at'])}")
    print(FOOTER)


def cmd_status(args):
    init_db()

    timer = get_active_timer()
    if not timer:
        print("No active timer.")
        print(FOOTER)
        return

    print(f"Active timer: {timer['description']}")
    print(f"  Running: {_fmt_duration(timer['elapsed_minutes'])}")
    print(f"  Started: {_fmt_time(timer['started_at'])}")
    print(f"  Category: {timer['category']}")
    print(f"  Billable: {'yes' if timer['billable'] else 'no'}")
    print(FOOTER)


def cmd_cancel(args):
    init_db()

    timer = cancel_timer()
    if not timer:
        print("No active timer.")
    else:
        print(f"Timer cancelled: {timer['description']}")
        print("No entry saved.")
    print(FOOTER)


def cmd_log(args):
    init_db()

    duration = _parse_duration(args.duration)
    client_id = _resolve_client(args.client)
    project_id = _resolve_project(args.project)
    billable = not args.non_billable

    entry_id = save_entry(
        description=args.description,
        duration_minutes=duration,
        project_id=project_id,
        client_id=client_id,
        category=args.category,
        billable=billable,
        tags=args.tags,
        notes=args.notes,
        entry_date=args.date,
        rate=args.rate,
    )

    print(f"Entry logged (ID: {entry_id})")
    print(f"  Task: {args.description}")
    print(f"  Duration: {_fmt_duration(duration)}")
    if args.client:
        print(f"  Client: {args.client}")
    if args.project:
        print(f"  Project: {args.project}")
    print(f"  Billable: {'yes' if billable else 'no'}")
    print(FOOTER)


def cmd_show(args):
    init_db()

    entry = get_entry(args.id)
    if not entry:
        print(f"Entry {args.id} not found.")
        print(FOOTER)
        return

    print(f"\n{SEPARATOR}")
    print(f"ENTRY #{entry['id']}: {entry['description']}")
    print(f"{SEPARATOR}\n")

    print(f"Date: {_fmt_date(entry['started_at'])}")
    if entry['started_at'] and entry['ended_at']:
        print(f"Time: {_fmt_time(entry['started_at'])} - {_fmt_time(entry['ended_at'])}")
    print(f"Duration: {_fmt_duration(entry['duration_minutes'])}")
    print(f"Category: {entry['category']}")
    print(f"Billable: {'yes' if entry['billable'] else 'no'}")

    if entry['client_name']:
        print(f"Client: {entry['client_name']}")
    if entry['project_name']:
        print(f"Project: {entry['project_name']}")
    if entry['rate']:
        amount = (entry['duration_minutes'] / 60.0) * entry['rate']
        print(f"Rate: {_fmt_money(entry['rate'])}/h = {_fmt_money(amount)}")
    if entry['tags']:
        print(f"Tags: {entry['tags']}")
    if entry['notes']:
        print(f"Notes: {entry['notes']}")

    print(f"\n{FOOTER}")


def cmd_list(args):
    init_db()

    client_id = _resolve_client(args.client) if args.client else None
    project_id = _resolve_project(args.project) if args.project else None
    billable = None
    if args.billable:
        billable = True
    elif args.non_billable:
        billable = False

    entries = list_entries(
        project_id=project_id,
        client_id=client_id,
        category=args.category,
        billable=billable,
        date_from=args.date_from,
        date_to=args.date_to,
        limit=args.limit or 50,
    )

    if not entries:
        print("No entries found.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Date':<12} {'Duration':<10} {'Description':<30} {'Client':<16} {'Bill':<5}")
    print("-" * 78)

    total_mins = 0
    for e in entries:
        desc = e['description'][:29]
        client = (e['client_name'] or "")[:15]
        date = _fmt_date(e['started_at'])
        dur = _fmt_duration(e['duration_minutes'])
        bill = "yes" if e['billable'] else "no"
        total_mins += e['duration_minutes'] or 0
        print(f"{e['id']:<5} {date:<12} {dur:<10} {desc:<30} {client:<16} {bill:<5}")

    print(f"\nTotal: {len(entries)} entries | {_fmt_duration(total_mins)}")
    print(FOOTER)


def cmd_edit(args):
    init_db()

    updates = {}
    if args.description:
        updates['description'] = args.description
    if args.duration:
        updates['duration_minutes'] = _parse_duration(args.duration)
    if args.category:
        updates['category'] = args.category
    if args.notes:
        updates['notes'] = args.notes
    if args.tags:
        updates['tags'] = args.tags
    if args.rate is not None:
        updates['rate'] = args.rate
    if args.billable:
        updates['billable'] = True
    elif args.non_billable:
        updates['billable'] = False
    if args.client:
        cid = _resolve_client(args.client)
        if cid:
            updates['client_id'] = cid
    if args.project:
        pid = _resolve_project(args.project)
        if pid:
            updates['project_id'] = pid

    if not updates:
        print("No updates specified.")
        return

    success = update_entry(args.id, **updates)
    if success:
        print(f"Entry #{args.id} updated.")
        for k, v in updates.items():
            print(f"  {k}: {v}")
    else:
        print(f"Entry {args.id} not found.")
    print(FOOTER)


def cmd_delete(args):
    init_db()

    entry = get_entry(args.id)
    if not entry:
        print(f"Entry {args.id} not found.")
        print(FOOTER)
        return

    if not args.confirm:
        print(f"Delete entry #{args.id}: {entry['description']} ({_fmt_duration(entry['duration_minutes'])})?")
        print(f"Run again with --confirm to delete.")
        print(FOOTER)
        return

    delete_entry(args.id)
    print(f"Entry #{args.id} deleted.")
    print(FOOTER)


def cmd_search(args):
    init_db()

    results = search_entries(args.query)
    if not results:
        print(f"No entries matching '{args.query}'")
        print(FOOTER)
        return

    print(f"\nSearch: '{args.query}' ({len(results)} found)\n")
    for e in results:
        print(f"  [{e['id']}] {e['description']}")
        print(f"       {_fmt_date(e['started_at'])} | {_fmt_duration(e['duration_minutes'])}", end="")
        if e['client_name']:
            print(f" | {e['client_name']}", end="")
        print()

    print(f"\n{FOOTER}")


def cmd_client_add(args):
    init_db()

    cid = save_client(
        name=args.name,
        rate=args.rate,
        contact_email=args.email,
        notes=args.notes,
    )

    print(f"Client added (ID: {cid})")
    print(f"  Name: {args.name}")
    if args.rate:
        print(f"  Rate: {_fmt_money(args.rate)}/h")
    if args.email:
        print(f"  Email: {args.email}")
    print(FOOTER)


def cmd_clients(args):
    init_db()

    clients = list_clients()
    if not clients:
        print("No clients.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Name':<25} {'Rate':<12} {'Email':<30}")
    print("-" * 72)

    for c in clients:
        rate = _fmt_money(c['rate']) + "/h" if c['rate'] else "-"
        email = (c['contact_email'] or "")[:29]
        print(f"{c['id']:<5} {c['name'][:24]:<25} {rate:<12} {email:<30}")

    print(f"\nTotal: {len(clients)} clients")
    print(FOOTER)


def cmd_project_add(args):
    init_db()

    client_id = _resolve_client(args.client) if args.client else None

    pid = save_project(
        name=args.name,
        client_id=client_id,
        rate=args.rate,
        budget_hours=args.budget,
        notes=args.notes,
    )

    print(f"Project added (ID: {pid})")
    print(f"  Name: {args.name}")
    if args.client:
        print(f"  Client: {args.client}")
    if args.rate:
        print(f"  Rate: {_fmt_money(args.rate)}/h")
    if args.budget:
        print(f"  Budget: {args.budget}h")
    print(FOOTER)


def cmd_projects(args):
    init_db()

    projects = list_projects(active_only=not args.all)
    if not projects:
        print("No projects.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Project':<25} {'Client':<20} {'Rate':<12} {'Budget':<8}")
    print("-" * 70)

    for p in projects:
        client = (p['client_name'] or "")[:19]
        rate = _fmt_money(p['rate']) + "/h" if p['rate'] else "-"
        budget = f"{p['budget_hours']}h" if p['budget_hours'] else "-"
        print(f"{p['id']:<5} {p['name'][:24]:<25} {client:<20} {rate:<12} {budget:<8}")

    print(f"\nTotal: {len(projects)} projects")
    print(FOOTER)


def cmd_summary(args):
    init_db()

    client_id = _resolve_client(args.client) if args.client else None
    project_id = _resolve_project(args.project) if args.project else None

    summary = get_summary(
        client_id=client_id,
        project_id=project_id,
        date_from=args.date_from,
        date_to=args.date_to,
        billable_only=args.billable,
        round_up=args.round_up,
    )

    print(f"\n{SEPARATOR}")
    print(f"TIME SUMMARY")
    if args.date_from or args.date_to:
        period = f"{args.date_from or '...'} to {args.date_to or '...'}"
        print(f"Period: {period}")
    print(f"{SEPARATOR}\n")

    print(f"Total entries: {summary['total_entries']}")
    print(f"Total time: {_fmt_duration(summary['total_minutes'])} ({summary['total_hours']}h)")
    print(f"Billable time: {_fmt_duration(summary['billable_minutes'])} ({summary['billable_hours']}h)")
    print(f"Total billable: {_fmt_money(summary['total_amount'])}")

    if args.round_up:
        print(f"  (rounded up to {ROUND_TO_MINUTES}min blocks)")

    if summary['by_client']:
        print(f"\nBy Client:")
        for name, data in summary['by_client'].items():
            print(f"  {name:<25} {_fmt_duration(data['minutes']):<10} {_fmt_money(data['amount'])}")

    if summary['by_project']:
        print(f"\nBy Project:")
        for name, data in summary['by_project'].items():
            print(f"  {name:<25} {_fmt_duration(data['minutes']):<10} {_fmt_money(data['amount'])}")

    if summary['by_category']:
        print(f"\nBy Category:")
        for cat, mins in summary['by_category'].items():
            print(f"  {cat:<20} {_fmt_duration(mins)}")

    print(f"\n{FOOTER}")


def cmd_stats(args):
    init_db()

    stats = get_stats()

    print(f"\n{SEPARATOR}")
    print(f"TIMETRACK STATISTICS")
    print(f"{SEPARATOR}\n")

    print(f"Total entries: {stats['total_entries']}")
    print(f"Total clients: {stats['total_clients']}")
    print(f"Active projects: {stats['total_projects']}")
    print(f"Total time: {_fmt_duration(stats['total_minutes'])} ({stats['total_hours']}h)")
    print(f"Billable time: {_fmt_duration(stats['billable_minutes'])} ({stats['billable_hours']}h)")
    print(f"Total revenue: {_fmt_money(stats['total_revenue'])}")

    if stats['total_minutes'] > 0:
        ratio = (stats['billable_minutes'] / stats['total_minutes']) * 100
        print(f"Billable ratio: {ratio:.0f}%")

    if stats['by_category']:
        print(f"\nTime by Category:")
        for cat, mins in stats['by_category'].items():
            bar = '#' * max(1, int(mins / 30))
            print(f"  {cat:<16} {bar} {_fmt_duration(mins)}")

    if stats['top_clients']:
        print(f"\nTop Clients:")
        for name, mins in stats['top_clients'].items():
            print(f"  {name:<25} {_fmt_duration(mins)}")

    if stats['by_month']:
        print(f"\nTime per Month:")
        for month, mins in stats['by_month'].items():
            bar = '#' * max(1, int(mins / 60))
            print(f"  {month} {bar} {_fmt_duration(mins)}")

    print(f"\n{FOOTER}")


def cmd_export(args):
    init_db()

    client_id = _resolve_client(args.client) if args.client else None
    project_id = _resolve_project(args.project) if args.project else None

    data = export_entries(
        format_type=args.format,
        client_id=client_id,
        project_id=project_id,
        date_from=args.date_from,
        date_to=args.date_to,
    )

    if not data:
        print("No entries to export.")
        return

    output_file = args.output or f"timetrack_export.{args.format}"
    output_path = EXPORT_DIR / output_file

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(data)

    print(f"Exported to {output_path}")
    print(FOOTER)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Nex Timetrack - Billable time logger.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # START
    p = subparsers.add_parser('start', help='Start a timer')
    p.add_argument('description', help='What you are working on')
    p.add_argument('--client', help='Client name')
    p.add_argument('--project', help='Project name')
    p.add_argument('--category', default='other', choices=CATEGORIES, help='Activity category')
    p.add_argument('--tags', help='Comma-separated tags')
    p.add_argument('--non-billable', action='store_true', help='Mark as non-billable')
    p.set_defaults(func=cmd_start)

    # STOP
    p = subparsers.add_parser('stop', help='Stop the active timer')
    p.add_argument('--notes', help='Notes about the work done')
    p.set_defaults(func=cmd_stop)

    # STATUS
    p = subparsers.add_parser('status', help='Show active timer')
    p.set_defaults(func=cmd_status)

    # CANCEL
    p = subparsers.add_parser('cancel', help='Cancel active timer without saving')
    p.set_defaults(func=cmd_cancel)

    # LOG
    p = subparsers.add_parser('log', help='Log time manually')
    p.add_argument('description', help='What you worked on')
    p.add_argument('duration', help='Duration (e.g., 2h, 90m, 1h30m)')
    p.add_argument('--client', help='Client name')
    p.add_argument('--project', help='Project name')
    p.add_argument('--category', default='other', choices=CATEGORIES, help='Activity category')
    p.add_argument('--tags', help='Comma-separated tags')
    p.add_argument('--notes', help='Additional notes')
    p.add_argument('--date', help='Date (YYYY-MM-DD, default: today)')
    p.add_argument('--rate', type=float, help='Override hourly rate')
    p.add_argument('--non-billable', action='store_true', help='Mark as non-billable')
    p.set_defaults(func=cmd_log)

    # SHOW
    p = subparsers.add_parser('show', help='Show entry details')
    p.add_argument('id', type=int, help='Entry ID')
    p.set_defaults(func=cmd_show)

    # LIST
    p = subparsers.add_parser('list', help='List time entries')
    p.add_argument('--client', help='Filter by client')
    p.add_argument('--project', help='Filter by project')
    p.add_argument('--category', choices=CATEGORIES, help='Filter by category')
    p.add_argument('--billable', action='store_true', help='Only billable')
    p.add_argument('--non-billable', action='store_true', help='Only non-billable')
    p.add_argument('--date-from', help='From date (YYYY-MM-DD)')
    p.add_argument('--date-to', help='To date (YYYY-MM-DD)')
    p.add_argument('--limit', type=int, default=50, help='Max results')
    p.set_defaults(func=cmd_list)

    # EDIT
    p = subparsers.add_parser('edit', help='Edit an entry')
    p.add_argument('id', type=int, help='Entry ID')
    p.add_argument('--description', help='New description')
    p.add_argument('--duration', help='New duration')
    p.add_argument('--category', choices=CATEGORIES, help='New category')
    p.add_argument('--client', help='New client')
    p.add_argument('--project', help='New project')
    p.add_argument('--notes', help='New notes')
    p.add_argument('--tags', help='New tags')
    p.add_argument('--rate', type=float, help='New rate')
    p.add_argument('--billable', action='store_true', help='Mark billable')
    p.add_argument('--non-billable', action='store_true', help='Mark non-billable')
    p.set_defaults(func=cmd_edit)

    # DELETE
    p = subparsers.add_parser('delete', help='Delete an entry')
    p.add_argument('id', type=int, help='Entry ID')
    p.add_argument('--confirm', action='store_true', help='Confirm deletion')
    p.set_defaults(func=cmd_delete)

    # SEARCH
    p = subparsers.add_parser('search', help='Search entries')
    p.add_argument('query', help='Search query')
    p.set_defaults(func=cmd_search)

    # CLIENT ADD
    p = subparsers.add_parser('client-add', help='Add a client')
    p.add_argument('name', help='Client name')
    p.add_argument('--rate', type=float, help='Default hourly rate')
    p.add_argument('--email', help='Contact email')
    p.add_argument('--notes', help='Notes')
    p.set_defaults(func=cmd_client_add)

    # CLIENTS
    p = subparsers.add_parser('clients', help='List clients')
    p.set_defaults(func=cmd_clients)

    # PROJECT ADD
    p = subparsers.add_parser('project-add', help='Add a project')
    p.add_argument('name', help='Project name')
    p.add_argument('--client', help='Client name')
    p.add_argument('--rate', type=float, help='Project hourly rate')
    p.add_argument('--budget', type=float, help='Budget in hours')
    p.add_argument('--notes', help='Notes')
    p.set_defaults(func=cmd_project_add)

    # PROJECTS
    p = subparsers.add_parser('projects', help='List projects')
    p.add_argument('--all', action='store_true', help='Include inactive projects')
    p.set_defaults(func=cmd_projects)

    # SUMMARY
    p = subparsers.add_parser('summary', help='Billing summary')
    p.add_argument('--client', help='Filter by client')
    p.add_argument('--project', help='Filter by project')
    p.add_argument('--date-from', help='From date (YYYY-MM-DD)')
    p.add_argument('--date-to', help='To date (YYYY-MM-DD)')
    p.add_argument('--billable', action='store_true', help='Only billable entries')
    p.add_argument('--round-up', action='store_true', help=f'Round to {ROUND_TO_MINUTES}min blocks')
    p.set_defaults(func=cmd_summary)

    # STATS
    p = subparsers.add_parser('stats', help='Show statistics')
    p.set_defaults(func=cmd_stats)

    # EXPORT
    p = subparsers.add_parser('export', help='Export entries')
    p.add_argument('format', choices=['json', 'csv'], help='Export format')
    p.add_argument('--client', help='Filter by client')
    p.add_argument('--project', help='Filter by project')
    p.add_argument('--date-from', help='From date')
    p.add_argument('--date-to', help='To date')
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
