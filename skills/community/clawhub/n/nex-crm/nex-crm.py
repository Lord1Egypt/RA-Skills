#!/usr/bin/env python3
"""
Nex CRM - CLI Tool
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Chat-native CRM for one-person agencies and freelancers.
Prospect tracking, pipeline management, conversation memory, conversational activity logging.
Built by Nex AI (nex-ai.be)
"""
import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from decimal import Decimal

# Add lib directory to Python path
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SKILL_DIR, "lib")
sys.path.insert(0, LIB_DIR)

from lib import config
from lib.storage import (
    init_db, db_conn, add_prospect, get_prospect, list_prospects,
    update_prospect_stage, log_activity, get_activities, get_follow_ups,
    set_follow_up, search_prospects, get_pipeline_stats, export_prospects,
    get_stale_prospects, interact_with_prospect, set_reminder, get_reminders
)
from lib.nl_parser import parse_activity_input, parse_prospect_input

FOOTER = "[Nex CRM by Nex AI | nex-ai.be]"


def _print_footer():
    print("\n%s" % FOOTER)


def _format_currency(value):
    """Format value as EUR currency."""
    if value is None or value == 0:
        return "-"
    if isinstance(value, str):
        value = Decimal(value)
    elif not isinstance(value, Decimal):
        value = Decimal(str(value))
    return f"€{value:.0f}/mo"


def _format_date(date_str):
    """Format date string for display."""
    if not date_str:
        return "Never"
    try:
        dt_obj = dt.datetime.fromisoformat(date_str)
        return dt_obj.strftime("%d %b %Y")
    except:
        return date_str


def _check_db():
    """Check if the database exists."""
    if not config.DB_PATH.exists():
        print(
            "CRM database not found at %s.\n"
            "Run 'bash setup.sh' to initialize." % config.DB_PATH,
            file=sys.stderr,
        )
        sys.exit(1)


def cmd_add(args):
    """Add a new prospect."""
    _check_db()

    prospect_data = {}

    # Parse natural language input or use structured flags
    if args.natural:
        prospect_data = parse_prospect_input(args.natural)
    else:
        # Use structured input
        prospect_data = {
            "company": args.company,
            "contact_name": args.contact,
            "email": args.email,
            "phone": args.phone,
            "source": args.source or "other",
            "priority": args.priority or "cold",
            "value": args.value or 0,
        }

    # Validate required fields
    if not prospect_data.get("company"):
        print("Error: Company name is required.", file=sys.stderr)
        sys.exit(1)

    prospect_id = add_prospect(prospect_data)
    print(f"Prospect added: {prospect_data.get('company')} (ID: {prospect_id})")
    _print_footer()


def cmd_show(args):
    """Show prospect details."""
    _check_db()

    # Find prospect by name or ID
    identifier = args.identifier
    prospect = None

    try:
        pid = int(identifier)
        prospect = get_prospect(pid)
    except ValueError:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id FROM prospects WHERE company = ? LIMIT 1", (identifier,))
        row = cur.fetchone()
        if row:
            prospect = get_prospect(row[0])
        conn.close()

    if not prospect:
        print(f"Prospect not found: {identifier}", file=sys.stderr)
        sys.exit(1)

    if args.output == "json":
        print(json.dumps(prospect, indent=2, default=str))
    else:
        # Human-readable output
        print(f"\n{prospect['company']}")
        print("=" * 60)
        print(f"ID:            {prospect['id']}")
        print(f"Contact:       {prospect.get('contact_name', 'N/A')}")
        print(f"Email:         {prospect.get('email', 'N/A')}")
        print(f"Phone:         {prospect.get('phone', 'N/A')}")
        print(f"Stage:         {config.PIPELINE_STAGE_LABELS.get(prospect['stage'], prospect['stage'])}")
        print(f"Priority:      {prospect.get('priority', 'cold').upper()}")
        print(f"Value:         {_format_currency(prospect.get('value', 0))}")
        print(f"Source:        {prospect.get('source', 'unknown')}")
        print(f"Created:       {_format_date(prospect.get('created_at'))}")
        print(f"Last contact:  {_format_date(prospect.get('last_contact'))}")
        print(f"Next follow-up: {_format_date(prospect.get('next_follow_up'))}")

        # Recent activities
        activities = get_activities(prospect['id'], limit=5)
        if activities:
            print("\nRecent Activities:")
            print("-" * 60)
            for activity in activities:
                activity_date = _format_date(activity['timestamp'])
                activity_type = activity.get('type', 'note').upper()
                summary = activity.get('summary', '')[:50]
                print(f"  {activity_date} [{activity_type}] {summary}")

    _print_footer()


def cmd_list(args):
    """List prospects with filtering."""
    _check_db()

    filters = {}
    if args.stage:
        filters['stage'] = args.stage
    if args.priority:
        filters['priority'] = args.priority
    if args.source:
        filters['source'] = args.source
    if args.stale:
        filters['stale'] = True

    prospects = list_prospects(filters)

    if args.output == "json":
        print(json.dumps(prospects, indent=2, default=str))
    else:
        if not prospects:
            print("No prospects found.")
        else:
            print(f"\nProspects ({len(prospects)})")
            print("=" * 80)
            print(f"{'ID':<5} {'Company':<25} {'Stage':<18} {'Priority':<8} {'Value':<12}")
            print("-" * 80)
            for p in prospects:
                stage_label = config.PIPELINE_STAGE_LABELS.get(p['stage'], p['stage'])[:17]
                value_str = _format_currency(p.get('value', 0))
                print(f"{p['id']:<5} {p['company']:<25} {stage_label:<18} {p.get('priority', 'cold'):<8} {value_str:<12}")

    _print_footer()


def cmd_stage(args):
    """Update prospect stage in pipeline."""
    _check_db()

    # Find prospect
    identifier = args.prospect
    prospect = None

    try:
        pid = int(identifier)
        prospect = get_prospect(pid)
    except ValueError:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id FROM prospects WHERE company = ? LIMIT 1", (identifier,))
        row = cur.fetchone()
        if row:
            prospect = get_prospect(row[0])
        conn.close()

    if not prospect:
        print(f"Prospect not found: {identifier}", file=sys.stderr)
        sys.exit(1)

    # Validate stage
    if args.stage not in config.PIPELINE_STAGES:
        print(f"Invalid stage. Valid stages: {', '.join(config.PIPELINE_STAGES)}", file=sys.stderr)
        sys.exit(1)

    reason = args.reason or ""
    update_prospect_stage(prospect['id'], args.stage, reason)

    stage_label = config.PIPELINE_STAGE_LABELS.get(args.stage, args.stage)
    print(f"{prospect['company']} moved to {stage_label}")
    if reason:
        print(f"Reason: {reason}")

    _print_footer()


def cmd_log(args):
    """Log activity for a prospect."""
    _check_db()

    prospect = None
    activity_data = {}

    # Natural language parsing
    if args.text and not args.prospect:
        activity_data, prospect_name = parse_activity_input(args.text)
        if prospect_name:
            conn = db_conn()
            cur = conn.cursor()
            cur.execute("SELECT id FROM prospects WHERE company = ? LIMIT 1", (prospect_name,))
            row = cur.fetchone()
            if row:
                prospect = get_prospect(row[0])
            conn.close()
    else:
        # Structured input
        identifier = args.prospect
        try:
            pid = int(identifier)
            prospect = get_prospect(pid)
        except ValueError:
            conn = db_conn()
            cur = conn.cursor()
            cur.execute("SELECT id FROM prospects WHERE company = ? LIMIT 1", (identifier,))
            row = cur.fetchone()
            if row:
                prospect = get_prospect(row[0])
            conn.close()

        activity_data = {
            "type": args.type or "note",
            "summary": args.summary or "",
        }

    if not prospect:
        print(f"Prospect not found: {args.prospect or 'in text'}", file=sys.stderr)
        sys.exit(1)

    log_activity(prospect['id'], activity_data)
    print(f"Activity logged for {prospect['company']}")

    _print_footer()


def cmd_follow_up(args):
    """Manage follow-ups."""
    _check_db()

    if args.prospect:
        # Set follow-up for specific prospect
        identifier = args.prospect
        prospect = None

        try:
            pid = int(identifier)
            prospect = get_prospect(pid)
        except ValueError:
            conn = db_conn()
            cur = conn.cursor()
            cur.execute("SELECT id FROM prospects WHERE company = ? LIMIT 1", (identifier,))
            row = cur.fetchone()
            if row:
                prospect = get_prospect(row[0])
            conn.close()

        if not prospect:
            print(f"Prospect not found: {identifier}", file=sys.stderr)
            sys.exit(1)

        follow_up_date = args.date
        if args.in_days:
            follow_up_date = (dt.datetime.now() + dt.timedelta(days=args.in_days)).isoformat()

        set_follow_up(prospect['id'], follow_up_date)
        print(f"Follow-up set for {prospect['company']} on {_format_date(follow_up_date)}")
    else:
        # Show all due follow-ups
        follow_ups = get_follow_ups()

        if not follow_ups:
            print("No follow-ups due.")
        else:
            print(f"\nDue Follow-ups ({len(follow_ups)})")
            print("=" * 80)
            print(f"{'Company':<25} {'Date':<15} {'Days':<6} {'Stage':<18}")
            print("-" * 80)

            today = dt.datetime.now().date()
            for fu in follow_ups:
                try:
                    fu_date = dt.datetime.fromisoformat(fu['date']).date()
                    days_ago = (today - fu_date).days
                    days_str = f"{days_ago}d ago" if days_ago > 0 else "Today"
                except:
                    days_str = "?"

                stage_label = config.PIPELINE_STAGE_LABELS.get(fu['stage'], fu['stage'])[:17]
                print(f"{fu['company']:<25} {_format_date(fu['date']):<15} {days_str:<6} {stage_label:<18}")

    _print_footer()


def cmd_search(args):
    """Search prospects by text."""
    _check_db()

    results = search_prospects(args.query)

    if not results:
        print(f"No prospects found matching '{args.query}'")
    else:
        print(f"\nSearch results for '{args.query}' ({len(results)})")
        print("=" * 80)
        for p in results:
            print(f"  {p['id']:>3}: {p['company']:<25} [{p['stage']}] {p.get('contact_name', 'N/A')}")

    _print_footer()


def cmd_pipeline(args):
    """Show pipeline overview."""
    _check_db()

    stats = get_pipeline_stats()

    print("\nPipeline Overview")
    print("=" * 80)

    total_value = 0
    won_value = 0
    total_count = 0

    for stage in config.PIPELINE_STAGES:
        stage_data = stats.get(stage, {'count': 0, 'value': 0})
        count = stage_data['count']
        value = stage_data['value'] or 0

        if count == 0:
            continue

        total_count += count
        total_value += value
        if stage == 'won':
            won_value = value

        # ASCII bar chart
        bar_length = max(1, count // 2)
        bar = '█' * bar_length
        value_str = _format_currency(value) if value > 0 else "-"
        stage_label = config.PIPELINE_STAGE_LABELS.get(stage, stage)

        print(f"{stage_label:<20} |{bar:<30}| {count:>3}  {value_str}")

    print("-" * 80)
    total_value_str = _format_currency(total_value)
    won_value_str = _format_currency(won_value)
    win_rate = int((won_value / total_value * 100)) if total_value > 0 else 0
    print(f"Total pipeline: {total_value_str} | Won: {won_value_str} | Win rate: {win_rate}%")

    _print_footer()


def cmd_stats(args):
    """Show statistics."""
    _check_db()

    conn = db_conn()
    cur = conn.cursor()

    # Basic stats
    cur.execute("SELECT COUNT(*) FROM prospects WHERE stage != 'lost'")
    active_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prospects WHERE stage = 'won'")
    won_count = cur.fetchone()[0]

    cur.execute("SELECT SUM(value) FROM prospects WHERE stage = 'won'")
    won_value = cur.fetchone()[0] or 0

    cur.execute("SELECT AVG(value) FROM prospects WHERE stage != 'lost' AND value > 0")
    avg_deal = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(DISTINCT source) FROM prospects")
    source_count = cur.fetchone()[0]

    conn.close()

    print("\nCRM Statistics")
    print("=" * 60)
    print(f"Active prospects:  {active_count}")
    print(f"Won deals:         {won_count}")
    print(f"Total revenue:     {_format_currency(won_value)}")
    print(f"Avg deal size:     {_format_currency(avg_deal)}")
    print(f"Lead sources:      {source_count}")

    _print_footer()


def cmd_export(args):
    """Export prospects."""
    _check_db()

    config.EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    prospects = list_prospects({})

    if args.format == "json":
        output_file = config.EXPORT_DIR / f"prospects-{dt.datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, "w") as f:
            json.dump(prospects, f, indent=2, default=str)
        print(f"Exported to {output_file}")

    elif args.format == "csv":
        import csv
        output_file = config.EXPORT_DIR / f"prospects-{dt.datetime.now().strftime('%Y%m%d')}.csv"
        if prospects:
            with open(output_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=prospects[0].keys())
                writer.writeheader()
                writer.writerows(prospects)
            print(f"Exported to {output_file}")
        else:
            print("No prospects to export.")

    _print_footer()


def cmd_interact(args):
    """Store an interaction/conversation."""
    _check_db()

    identifier = args.prospect
    prospect = None

    try:
        pid = int(identifier)
        prospect = get_prospect(pid)
    except ValueError:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id FROM prospects WHERE company = ? LIMIT 1", (identifier,))
        row = cur.fetchone()
        if row:
            prospect = get_prospect(row[0])
        conn.close()

    if not prospect:
        print(f"Prospect not found: {identifier}", file=sys.stderr)
        sys.exit(1)

    interact_with_prospect(prospect['id'], args.channel, args.message, args.direction)
    print(f"Interaction logged for {prospect['company']}")

    _print_footer()


def cmd_remind(args):
    """Set a reminder."""
    _check_db()

    identifier = args.prospect
    prospect = None

    try:
        pid = int(identifier)
        prospect = get_prospect(pid)
    except ValueError:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id FROM prospects WHERE company = ? LIMIT 1", (identifier,))
        row = cur.fetchone()
        if row:
            prospect = get_prospect(row[0])
        conn.close()

    if not prospect:
        print(f"Prospect not found: {identifier}", file=sys.stderr)
        sys.exit(1)

    set_reminder(prospect['id'], args.date, args.message)
    print(f"Reminder set for {prospect['company']} on {_format_date(args.date)}")

    _print_footer()


def cmd_config(args):
    """Show configuration."""
    _check_db()

    print("\nNex CRM Configuration")
    print("=" * 60)
    print(f"Data directory: {config.DATA_DIR}")
    print(f"Database:       {config.DB_PATH}")
    print(f"Export dir:     {config.EXPORT_DIR}")
    print(f"\nPipeline stages: {', '.join(config.PIPELINE_STAGES)}")
    print(f"Lead sources:    {', '.join(config.LEAD_SOURCES)}")
    print(f"Activity types:  {', '.join(config.ACTIVITY_TYPES)}")
    print(f"Priority levels: {', '.join(config.PRIORITY_LEVELS)}")
    print(f"\nRetainer tiers:")
    for tier, price in config.RETAINER_TIERS.items():
        print(f"  {tier:<15} EUR {price}/month")

    _print_footer()


def main():
    parser = argparse.ArgumentParser(
        prog="nex-crm",
        description="Chat-native CRM for agencies and freelancers",
        epilog=FOOTER
    )

    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add prospect")
    add_parser.add_argument("natural", nargs="?", help="Natural language input")
    add_parser.add_argument("--company", help="Company name")
    add_parser.add_argument("--contact", help="Contact name")
    add_parser.add_argument("--email", help="Email")
    add_parser.add_argument("--phone", help="Phone")
    add_parser.add_argument("--source", help="Lead source (scrape, referral, inbound, outreach, event, website, other)")
    add_parser.add_argument("--priority", help="Priority (hot, warm, cold)")
    add_parser.add_argument("--value", type=int, help="Monthly value in EUR")
    add_parser.set_defaults(func=cmd_add)

    # Show command
    show_parser = subparsers.add_parser("show", help="Show prospect details")
    show_parser.add_argument("identifier", help="Prospect name or ID")
    show_parser.add_argument("--output", choices=["text", "json"], default="text")
    show_parser.set_defaults(func=cmd_show)

    # List command
    list_parser = subparsers.add_parser("list", help="List prospects")
    list_parser.add_argument("--stage", help="Filter by stage")
    list_parser.add_argument("--priority", help="Filter by priority")
    list_parser.add_argument("--source", help="Filter by source")
    list_parser.add_argument("--stale", action="store_true", help="Show stale prospects (>14 days)")
    list_parser.add_argument("--output", choices=["text", "json"], default="text")
    list_parser.set_defaults(func=cmd_list)

    # Stage command
    stage_parser = subparsers.add_parser("stage", help="Update stage")
    stage_parser.add_argument("prospect", help="Prospect name or ID")
    stage_parser.add_argument("stage", help="New stage")
    stage_parser.add_argument("--reason", help="Reason for stage change")
    stage_parser.set_defaults(func=cmd_stage)

    # Log command
    log_parser = subparsers.add_parser("log", help="Log activity")
    log_parser.add_argument("text", nargs="?", help="Natural language activity description")
    log_parser.add_argument("--prospect", help="Prospect name or ID")
    log_parser.add_argument("--type", help="Activity type (call, email, meeting, demo, note, follow_up, proposal, invoice)")
    log_parser.add_argument("--summary", help="Activity summary")
    log_parser.set_defaults(func=cmd_log)

    # Follow-up command
    followup_parser = subparsers.add_parser("follow-up", help="Manage follow-ups")
    followup_parser.add_argument("prospect", nargs="?", help="Prospect name or ID")
    followup_parser.add_argument("--date", help="Follow-up date (ISO format)")
    followup_parser.add_argument("--in", dest="in_days", type=int, help="Days from now")
    followup_parser.set_defaults(func=cmd_follow_up)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search prospects")
    search_parser.add_argument("query", help="Search query")
    search_parser.set_defaults(func=cmd_search)

    # Pipeline command
    pipeline_parser = subparsers.add_parser("pipeline", help="Show pipeline overview")
    pipeline_parser.set_defaults(func=cmd_pipeline)

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument("--since", help="Since date (ISO format)")
    stats_parser.set_defaults(func=cmd_stats)

    # Export command
    export_parser = subparsers.add_parser("export", help="Export prospects")
    export_parser.add_argument("format", choices=["csv", "json"], help="Export format")
    export_parser.set_defaults(func=cmd_export)

    # Interact command
    interact_parser = subparsers.add_parser("interact", help="Store interaction")
    interact_parser.add_argument("prospect", help="Prospect name or ID")
    interact_parser.add_argument("--channel", default="note", help="Channel (telegram, whatsapp, email, call, note)")
    interact_parser.add_argument("--message", required=True, help="Message/interaction text")
    interact_parser.add_argument("--direction", choices=["inbound", "outbound"], default="outbound")
    interact_parser.set_defaults(func=cmd_interact)

    # Remind command
    remind_parser = subparsers.add_parser("remind", help="Set reminder")
    remind_parser.add_argument("prospect", help="Prospect name or ID")
    remind_parser.add_argument("--date", required=True, help="Reminder date (ISO format)")
    remind_parser.add_argument("--message", help="Reminder message")
    remind_parser.set_defaults(func=cmd_remind)

    # Config command
    config_parser = subparsers.add_parser("config", help="Show configuration")
    config_parser.set_defaults(func=cmd_config)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
