#!/usr/bin/env python3
"""
NextLink - Unified CLI for Exchange on-premises operations.

Commands:
  mail      - Email operations (read, send, reply, etc.)
  calendar  - Calendar operations (events, meetings)
  tasks     - Task operations (create, list, update)
  analytics - Email analytics and statistics
  sync      - Task sync and reminders (bidirectional sync with Exchange)

Usage:
  nexlink mail connect
  nexlink mail read --limit 10
  nexlink calendar today
  nexlink tasks list --overdue
  nexlink sync sync
  nexlink sync reminders --hours 24
"""

import argparse
import os
import sys

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import add_json_argument


def main():
    """Main entry point for NextLink CLI."""
    parser = argparse.ArgumentParser(
        prog="nexlink",
        description="Email, Calendar, and Tasks for Exchange on-premises (2016/2019).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s mail connect
  %(prog)s mail read --limit 10 --unread
  %(prog)s mail send --to user@example.com --subject "Hello" --body "Message"
  %(prog)s calendar today
  %(prog)s calendar create --subject "Meeting" --start "2024-01-15 14:00"
  %(prog)s tasks list --overdue
  %(prog)s tasks create --subject "Task" --due "+7d" --priority high
  %(prog)s sync sync
  %(prog)s sync reminders --hours 24
        """,
    )

    subparsers = parser.add_subparsers(dest="module", help="Module to use")
    add_json_argument(parser)

    # Mail subparser
    mail_parser = subparsers.add_parser("mail", help="Email operations")
    add_json_argument(mail_parser)
    mail_sub = mail_parser.add_subparsers(dest="command", help="Mail command")

    try:
        from mail import add_parser as add_mail_parser

        add_mail_parser(mail_sub)
    except ImportError as e:
        print(f"Warning: Could not load mail module: {e}", file=sys.stderr)

    # Calendar subparser
    cal_parser = subparsers.add_parser("calendar", help="Calendar operations")
    add_json_argument(cal_parser)
    cal_sub = cal_parser.add_subparsers(dest="command", help="Calendar command")

    try:
        from cal import add_parser as add_cal_parser

        add_cal_parser(cal_sub)
    except ImportError as e:
        print(f"Warning: Could not load calendar module: {e}", file=sys.stderr)

    # Tasks subparser
    tasks_parser = subparsers.add_parser("tasks", help="Task operations")
    add_json_argument(tasks_parser)
    tasks_sub = tasks_parser.add_subparsers(dest="command", help="Tasks command")

    try:
        from tasks import add_parser as add_tasks_parser

        add_tasks_parser(tasks_sub)
    except ImportError as e:
        print(f"Warning: Could not load tasks module: {e}", file=sys.stderr)

    # Sync subparser
    sync_parser = subparsers.add_parser("sync", help="Task sync and reminders")
    add_json_argument(sync_parser)
    sync_sub = sync_parser.add_subparsers(dest="command", help="Sync command")

    try:
        from sync import add_parser as add_sync_parser

        add_sync_parser(sync_sub)
    except ImportError as e:
        print(f"Warning: Could not load sync module: {e}", file=sys.stderr)

    # Analytics subparser
    analytics_parser = subparsers.add_parser("analytics", help="Email analytics and statistics")
    add_json_argument(analytics_parser)
    analytics_sub = analytics_parser.add_subparsers(dest="command", help="Analytics command")

    try:
        from analytics import add_parser as add_analytics_parser

        add_analytics_parser(analytics_sub)
    except ImportError as e:
        print(f"Warning: Could not load analytics module: {e}", file=sys.stderr)

    args = parser.parse_args()

    # If no module specified, show help
    if not args.module:
        parser.print_help()
        sys.exit(0)

    # If module specified but no command, show module help
    if hasattr(args, "func"):
        args.func(args)
    else:
        # Show help for the module
        if args.module == "mail":
            mail_parser.print_help()
        elif args.module == "calendar":
            cal_parser.print_help()
        elif args.module == "tasks":
            tasks_parser.print_help()
        elif args.module == "sync":
            sync_parser.print_help()
        elif args.module == "analytics":
            analytics_parser.print_help()
        else:
            parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
