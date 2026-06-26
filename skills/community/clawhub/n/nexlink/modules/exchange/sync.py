"""
Task synchronization between OpenClaw and Exchange Server.
Provides bidirectional sync, reminders, and calendar integration.
"""

import argparse
import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any
from pathlib import Path

# Add scripts directory to path for imports FIRST
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from exchangelib.items import Task, CalendarItem
    from exchangelib.properties import Mailbox

    HAS_EXCHANGELIB = True
except ImportError:
    HAS_EXCHANGELIB = False

from config import get_connection_config
from connection import get_account, check_dependencies
from utils import out, die, format_datetime, task_to_dict, add_json_argument, confirm_or_die, add_yes_argument
from logger import get_logger

# Sync state file location
SYNC_STATE_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
SYNC_STATE_FILE = SYNC_STATE_DIR / "task-sync-state.json"

_logger = get_logger()


def get_sync_state() -> Dict[str, Any]:
    """Load sync state from file."""
    if SYNC_STATE_FILE.exists():
        try:
            with open(SYNC_STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            _logger.warning(f"Could not load sync state: {e}")
    return {
        "last_sync": None,
        "tasks": {},  # Exchange ID -> {changekey, subject, due_date, status, local_id}
        "local_tasks": {},  # local_id -> Exchange ID
    }


def save_sync_state(state: Dict[str, Any]) -> None:
    """Save sync state to file with restrictive permissions."""
    SYNC_STATE_DIR.mkdir(parents=True, exist_ok=True)
    SYNC_STATE_DIR.chmod(0o700)
    with open(SYNC_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)
    SYNC_STATE_FILE.chmod(0o600)


def cmd_sync(args: argparse.Namespace) -> None:
    """
    Synchronize tasks between Exchange and local state.

    Bidirectional sync:
    - New tasks in Exchange -> added to local state
    - Changed tasks -> updated locally
    - Completed tasks -> marked as completed locally

    Local changes can be pushed back to Exchange.
    """
    confirm_or_die("Sync tasks with Exchange", getattr(args, 'yes', False))
    check_dependencies()
    account = get_account()

    _logger.info("Starting task sync")
    start_time = datetime.now()

    # Load current state
    state = get_sync_state()

    # Fetch all tasks from Exchange
    _logger.debug("Fetching tasks from Exchange")
    exchange_tasks = list(account.tasks.all().order_by("due_date"))

    # Build index of current Exchange tasks
    exchange_ids = {t.id for t in exchange_tasks}

    # Track changes
    new_count = 0
    updated_count = 0
    deleted_count = 0

    # Process each Exchange task
    for task in exchange_tasks:
        task_dict = task_to_dict(task)
        task_id = task.id

        if task_id not in state["tasks"]:
            # New task in Exchange
            state["tasks"][task_id] = task_dict
            new_count += 1
            _logger.debug(f"New task: {task.subject}")
        else:
            # Check if changed
            existing = state["tasks"][task_id]
            if existing.get("changekey") != task.changekey:
                # Task was updated
                state["tasks"][task_id] = task_dict
                updated_count += 1
                _logger.debug(f"Updated task: {task.subject}")

    # Check for deleted tasks (in local state but not in Exchange)
    for task_id in list(state["tasks"].keys()):
        if task_id not in exchange_ids:
            del state["tasks"][task_id]
            deleted_count += 1
            _logger.debug(f"Deleted task: {task_id}")

    # Update last sync time
    state["last_sync"] = datetime.now().isoformat()

    # Save state
    save_sync_state(state)

    duration = (datetime.now() - start_time).total_seconds() * 1000

    _logger.info(
        "Sync completed",
        {
            "new": new_count,
            "updated": updated_count,
            "deleted": deleted_count,
            "total": len(state["tasks"]),
            "duration_ms": int(duration),
        },
    )

    out(
        {
            "ok": True,
            "message": "Sync completed",
            "stats": {
                "new": new_count,
                "updated": updated_count,
                "deleted": deleted_count,
                "total_tasks": len(state["tasks"]),
            },
            "last_sync": state["last_sync"],
            "tasks": [t for t in state["tasks"].values()][: args.limit],
        }
    )


def cmd_reminders(args: argparse.Namespace) -> None:
    """
    Send email reminders for overdue or upcoming tasks.

    Checks for:
    - Overdue tasks (due_date < now AND status != Completed)
    - Upcoming tasks (due_date within N hours)

    Sends one consolidated email with all relevant tasks.
    """
    check_dependencies()
    account = get_account()

    _logger.info("Checking for task reminders")

    # Fetch incomplete tasks
    now = datetime.now()

    # Get all tasks (filter client-side)
    all_tasks = list(account.tasks.all())

    overdue_tasks = []
    upcoming_tasks = []

    for task in all_tasks:
        if str(task.status) == "Completed":
            continue

        if not task.due_date:
            continue

        # Convert EWSDate to datetime for comparison
        task_due = datetime(task.due_date.year, task.due_date.month, task.due_date.day)

        if task_due < now:
            # Overdue
            days_overdue = (now - task_due).days
            overdue_tasks.append(
                {
                    "subject": task.subject,
                    "due_date": format_datetime(task.due_date),
                    "days_overdue": days_overdue,
                    "importance": str(task.importance),
                }
            )
        elif args.hours and task_due <= now + timedelta(hours=args.hours):
            # Upcoming within N hours
            hours_until = int((task_due - now).total_seconds() / 3600)
            upcoming_tasks.append(
                {
                    "subject": task.subject,
                    "due_date": format_datetime(task.due_date),
                    "hours_until": hours_until,
                    "importance": str(task.importance),
                }
            )

    # Build email body
    if not overdue_tasks and not upcoming_tasks:
        _logger.info("No overdue or upcoming tasks")
        out(
            {
                "ok": True,
                "message": "No overdue or upcoming tasks",
                "overdue": 0,
                "upcoming": 0,
            }
        )
        return

    # Compose email
    from exchangelib import Message, HTMLBody

    body_parts = []

    if overdue_tasks:
        body_parts.append("<h2>⚠️ Overdue Tasks</h2>")
        body_parts.append("<ul>")
        for task in overdue_tasks:
            body_parts.append(
                f"<li><b>{task['subject']}</b> - {task['days_overdue']} days overdue (due: {task['due_date']})</li>"
            )
        body_parts.append("</ul>")

    if upcoming_tasks:
        body_parts.append("<h2>📅 Upcoming Tasks</h2>")
        body_parts.append("<ul>")
        for task in upcoming_tasks:
            body_parts.append(
                f"<li><b>{task['subject']}</b> - due in {task['hours_until']} hours ({task['due_date']})</li>"
            )
        body_parts.append("</ul>")

    body_html = "".join(body_parts)

    # Determine recipient: explicit --to > OWNER_EMAIL config > Exchange account address
    conn_config = get_connection_config()
    to_addr = args.to or conn_config.get("owner_email") or account.primary_smtp_address

    if args.dry_run:
        _logger.info(
            "Dry run - would send email",
            {
                "to": to_addr,
                "overdue": len(overdue_tasks),
                "upcoming": len(upcoming_tasks),
            },
        )
        out(
            {
                "ok": True,
                "message": "Dry run - no email sent",
                "would_send_to": to_addr,
                "overdue": overdue_tasks,
                "upcoming": upcoming_tasks,
            }
        )
        return

    # Send email
    try:
        message = Message(
            account=account,
            subject=f"Task Reminder: {len(overdue_tasks)} overdue, {len(upcoming_tasks)} upcoming",
            body=HTMLBody(body_html),
            to_recipients=[Mailbox(email_address=to_addr)],
        )
        message.send()

        _logger.info(
            "Reminder email sent",
            {
                "to": to_addr,
                "overdue": len(overdue_tasks),
                "upcoming": len(upcoming_tasks),
            },
        )

        out(
            {
                "ok": True,
                "message": "Reminder email sent",
                "to": to_addr,
                "overdue": len(overdue_tasks),
                "upcoming": len(upcoming_tasks),
            }
        )
    except Exception as e:
        _logger.error(f"Failed to send reminder: {e}")
        die(f"Failed to send reminder email: {e}")


def cmd_link_calendar(args: argparse.Namespace) -> None:
    """
    Create a calendar event from a task.

    Useful for tasks that need specific time slots or reminders.
    """
    confirm_or_die(f"Create calendar event from task {args.id}", getattr(args, 'yes', False))
    check_dependencies()
    account = get_account()

    # Get the task
    try:
        task = account.tasks.get(id=args.id)
    except Exception:
        die(f"Task not found: {args.id}")

    if not task.due_date:
        die("Task has no due date. Use 'tasks update --id ... --due YYYY-MM-DD' first.")

    # Parse time from args or default to 09:00
    start_time = args.time or "09:00"

    try:
        hour, minute = map(int, start_time.split(":"))
    except ValueError:
        die(f"Invalid time format: {args.time}. Use HH:MM format.")

    # Create datetime from due_date
    task_date = task.due_date
    start_dt = datetime(task_date.year, task_date.month, task_date.day, hour, minute)
    end_dt = start_dt + timedelta(minutes=args.duration)

    # Set timezone from account
    start_dt = start_dt.replace(tzinfo=account.default_timezone)
    end_dt = end_dt.replace(tzinfo=account.default_timezone)

    # Create event
    event = CalendarItem(
        account=account,
        folder=account.calendar,
        subject=f"📌 {task.subject}",
        body=task.body if task.body else "",
        start=start_dt,
        end=end_dt,
        reminder_is_set=True,
        reminder_minutes_before_start=args.reminder,
    )

    try:
        if args.invite:
            from exchangelib.items import SEND_ONLY_TO_ALL

            event.save(send_meeting_invitations=SEND_ONLY_TO_ALL)
        else:
            event.save()

        _logger.info(
            "Calendar event created",
            {
                "subject": task.subject,
                "start": format_datetime(start_dt),
                "end": format_datetime(end_dt),
            },
        )

        out(
            {
                "ok": True,
                "message": "Calendar event created from task",
                "task": {
                    "id": task.id,
                    "subject": task.subject,
                },
                "event": {
                    "id": event.id,
                    "subject": event.subject,
                    "start": format_datetime(event.start),
                    "end": format_datetime(event.end),
                },
            }
        )
    except Exception as e:
        _logger.error(f"Failed to create calendar event: {e}")
        die(f"Failed to create calendar event: {e}")


def cmd_status(args: argparse.Namespace) -> None:
    """Show sync status and statistics."""
    state = get_sync_state()
    account = get_account()

    # Get counts from Exchange
    total_tasks = account.tasks.total_count

    # Count by status — fetch only needed fields to reduce payload
    status_only_tasks = list(account.tasks.all().only('status', 'due_date'))
    status_counts = {}
    for task in status_only_tasks:
        status = str(task.status)
        status_counts[status] = status_counts.get(status, 0) + 1

    # Count overdue
    now = datetime.now()
    overdue = sum(
        1
        for t in status_only_tasks
        if t.due_date
        and datetime(t.due_date.year, t.due_date.month, t.due_date.day) < now
        and str(t.status) != "Completed"
    )

    out(
        {
            "ok": True,
            "exchange": {
                "total": total_tasks,
                "by_status": status_counts,
                "overdue": overdue,
            },
            "sync": {
                "last_sync": state.get("last_sync"),
                "tracked_tasks": len(state.get("tasks", {})),
            },
            "account": account.primary_smtp_address,
        }
    )


def add_parser(subparsers: argparse.ArgumentParser) -> None:
    """Add sync commands to the CLI parser."""

    # sync
    p_sync = subparsers.add_parser("sync", help="Synchronize tasks with Exchange")
    p_sync.add_argument(
        "--limit", "-n", type=int, default=50, help="Maximum tasks to return"
    )
    p_sync.set_defaults(func=cmd_sync)
    add_json_argument(p_sync)
    add_yes_argument(p_sync)

    # reminders
    p_reminders = subparsers.add_parser(
        "reminders", help="Send email reminders for tasks"
    )
    p_reminders.add_argument("--to", "-t", help="Recipient email (default: self)")
    p_reminders.add_argument(
        "--hours", type=int, default=24, help="Hours ahead for upcoming tasks"
    )
    p_reminders.add_argument(
        "--dry-run", action="store_true", help="Show what would be sent"
    )
    p_reminders.set_defaults(func=cmd_reminders)
    add_json_argument(p_reminders)

    # link-calendar
    p_link = subparsers.add_parser(
        "link-calendar", help="Create calendar event from task"
    )
    p_link.add_argument("--id", "-i", required=True, help="Task ID")
    p_link.add_argument("--time", "-t", help="Start time (HH:MM, default 09:00)")
    p_link.add_argument(
        "--duration", "-d", type=int, default=60, help="Duration in minutes"
    )
    p_link.add_argument(
        "--reminder", "-r", type=int, default=30, help="Reminder minutes before"
    )
    p_link.add_argument("--invite", action="store_true", help="Send invite to self")
    p_link.set_defaults(func=cmd_link_calendar)
    add_json_argument(p_link)
    add_yes_argument(p_link)

    # status
    p_status = subparsers.add_parser("status", help="Show sync status and statistics")
    p_status.set_defaults(func=cmd_status)
    add_json_argument(p_status)


def main() -> None:
    """Main entry point for standalone execution."""
    add_json_argument(parser)
    parser = argparse.ArgumentParser(
        prog="sync.py",
        description="Task sync and reminder operations",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    subparsers.required = True

    add_parser(subparsers)

    args = parser.parse_args()

    # Load configuration
    from config import get_config

    get_config()

    # Execute command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
