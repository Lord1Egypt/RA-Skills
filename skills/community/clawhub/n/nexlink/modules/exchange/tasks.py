"""
Task operations for Exchange Mailbox skill.
Supports creating, listing, updating, and deleting tasks.
Tasks can be assigned to self or to other users.
"""

import argparse
import sys
import os
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any

# Add scripts directory to path for imports FIRST
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from exchangelib.items import Task

    HAS_EXCHANGELIB = True
except ImportError:
    HAS_EXCHANGELIB = False

from connection import get_account
from utils import out, die, parse_datetime, format_datetime, task_to_dict, add_json_argument, confirm_or_die, add_yes_argument

# Task status mapping
STATUS_MAP = {
    "not_started": "NotStarted",
    "in_progress": "InProgress",
    "completed": "Completed",
    "waiting": "WaitingOnOthers",
    "deferred": "Deferred",
}

STATUS_REVERSE = {v: k for k, v in STATUS_MAP.items()}


def get_error_response(error: Exception, action: str, task_id: str = None, mailbox: str = None) -> Dict[str, Any]:
    """Generate informative error response with alternatives.
    
    Args:
        error: The exception that occurred
        action: The action that failed (trash, update, complete)
        task_id: Task ID if available
        mailbox: Target mailbox if delegate access
    
    Returns:
        Dict with error, cause, and alternatives
    """
    error_str = str(error)
    
    # Permission denied errors
    if "cannot be deleted" in error_str.lower() or "delete" in error_str.lower():
        return {
            "ok": False,
            "error": f"Task-urile pot fi șterse doar manual din Outlook.",
            "cause": f"Asistentul are permisiuni de Editor (poate crea/edita/completa), dar nu poate șterge task-urile. Aceasta e o limitare intenționată - task-urile se păstrează până le ștergi tu.",
            "alternatives": [
                {
                    "action": "complete",
                    "description": "Marchează task-ul ca finalizat (recomandat)",
                    "command": f"tasks complete --mailbox {mailbox} --id {task_id}" if mailbox else f"tasks complete --id {task_id}"
                },
                {
                    "action": "manual_delete",
                    "description": "Șterge manual din Outlook sau OWA"
                }
            ]
        }
    
    # Change key mismatch (concurrent modification)
    if "change key" in error_str.lower():
        return {
            "ok": False,
            "error": "Task-ul a fost modificat de altcineva. Reîncarcă și încearcă din nou.",
            "cause": "Exchange detectează o versiune mai nouă a task-ului (race condition).",
            "alternatives": [
                {
                    "action": "refresh",
                    "description": "Reîncarcă task-ul și aplică modificarea din nou",
                    "command": f"tasks list --mailbox {mailbox}" if mailbox else "tasks list"
                }
            ]
        }
    
    # Not found or invalid ID
    if "not found" in error_str.lower() or "malformed" in error_str.lower():
        return {
            "ok": False,
            "error": f"Task-ul nu a fost găsit.",
            "cause": f"Task ID {task_id} nu există sau este invalid.",
            "alternatives": [
                {
                    "action": "list",
                    "description": "Listează task-urile disponibile",
                    "command": f"tasks list --mailbox {mailbox}" if mailbox else "tasks list"
                }
            ]
        }
    
    # Generic error
    return {
        "ok": False,
        "error": f"Operațiunea '{action}' a eșuat: {error_str}",
        "cause": "Eroare necunoscută. Verifică log-urile pentru detalii.",
        "alternatives": []
    }


def cmd_connect(args: argparse.Namespace) -> None:
    """Test connection to Exchange and show task folder info."""
    from connection import test_connection

    result = test_connection()
    out({"ok": True, "message": "Connected successfully", **result})


def cmd_list(args: argparse.Namespace) -> None:
    """List tasks from the tasks folder.
    
    Use --mailbox to list tasks from another user's mailbox via delegate access.
    Without --mailbox, lists tasks from the service account's mailbox.
    """
    # Determine which account to use
    if getattr(args, 'mailbox', None):
        from connection import get_account_for
        try:
            account = get_account_for(args.mailbox)
        except Exception as e:
            die(f"Failed to access mailbox {args.mailbox}: {e}")
    else:
        account = get_account()

    # Build query
    query = account.tasks.all()

    # Note: EWS doesn't support filtering on status field for tasks
    # We'll filter client-side instead

    # Order by due date
    query = query.order_by("due_date")

    # Limit
    limit = args.limit or 20
    items = list(query[: limit * 2])  # Fetch more to account for filtering

    # Filter by status (client-side)
    if args.status:
        status_value = STATUS_MAP.get(args.status.lower())
        items = [t for t in items if str(t.status) == status_value]

    # Filter by completion
    if args.completed_only:
        items = [t for t in items if str(t.status) == "Completed"]
    elif not args.include_completed:
        # Default: exclude completed
        items = [t for t in items if str(t.status) != "Completed"]

    # Filter by overdue
    if args.overdue:
        now = datetime.now()
        items = [
            t
            for t in items
            if t.due_date and t.due_date < now and str(t.status) != "Completed"
        ]

    # Apply limit after filtering
    items = items[:limit]

    tasks = []
    for item in items:
        tasks.append(task_to_dict(item))

    out({
        "ok": True, 
        "count": len(tasks), 
        "mailbox": account.primary_smtp_address,
        "tasks": tasks
    })


def cmd_get(args: argparse.Namespace) -> None:
    """Get details of a specific task.
    
    Use --mailbox to get a task from another user's mailbox via delegate access.
    """
    # Determine which account to use
    if getattr(args, 'mailbox', None):
        from connection import get_account_for
        try:
            account = get_account_for(args.mailbox)
        except Exception as e:
            die(f"Failed to access mailbox {args.mailbox}: {e}")
    else:
        account = get_account()

    try:
        task = account.tasks.get(id=args.id)
        out({"ok": True, "mailbox": account.primary_smtp_address, "task": task_to_dict(task, detailed=True)})
    except Exception as e:
        die(f"Task not found: {args.id} ({e})")


def cmd_create(args: argparse.Namespace) -> None:
    """Create a new task in the account's Tasks folder.
    
    Use --assign-to to create a task directly in another user's mailbox.
    This requires delegate permissions on the target mailbox.
    """
    confirm_or_die(f"Create task \"{args.subject}\"", getattr(args, 'yes', False))

    # Determine which account to use
    if args.assign_to:
        from connection import get_account_for
        try:
            account = get_account_for(args.assign_to)
        except Exception as e:
            die(f"Failed to access mailbox {args.assign_to}: {e}")
    else:
        account = get_account()

    # Parse dates - EWS requires EWSDate for tasks (not EWSDateTime)
    from exchangelib import EWSDate

    if args.start:
        start_dt = parse_datetime(args.start)
        if start_dt:
            start_date = EWSDate(start_dt.year, start_dt.month, start_dt.day)
    else:
        start_date = None

    if args.due:
        due_dt = parse_datetime(args.due)
        if due_dt:
            due_date = EWSDate(due_dt.year, due_dt.month, due_dt.day)
    else:
        due_date = None

    # Create task object
    task = Task(
        account=account,
        folder=account.tasks,
        subject=args.subject,
        body=args.body or "",
    )

    # Set dates
    if start_date:
        task.start_date = start_date
    if due_date:
        task.due_date = due_date

    # Set priority
    if args.priority:
        priority_map = {"low": "Low", "normal": "Normal", "high": "High"}
        task.importance = priority_map.get(args.priority.lower(), "Normal")

    # Save
    try:
        task.save()
    except Exception as e:
        die(f"Failed to create task: {e}")

    out(
        {
            "ok": True,
            "message": f"Task created{' in ' + args.assign_to if args.assign_to else ''}",
            "task": task_to_dict(task),
            "mailbox": account.primary_smtp_address if args.assign_to else None
        }
    )


def cmd_assign(args: argparse.Namespace) -> None:
    """Assign a task to another user via delegate access.
    
    Creates the task directly in the target user's Exchange mailbox.
    Requires the service account to have delegate permissions on the target mailbox.
    """
    from connection import get_account_for
    from exchangelib import EWSDate

    try:
        account = get_account_for(args.to)
    except Exception as e:
        die(f"Failed to access mailbox {args.to}: {e}")

    # Parse dates
    if args.start:
        start_dt = parse_datetime(args.start)
        if start_dt:
            start_date = EWSDate(start_dt.year, start_dt.month, start_dt.day)
    else:
        start_date = None

    if args.due:
        due_dt = parse_datetime(args.due)
        if due_dt:
            due_date = EWSDate(due_dt.year, due_dt.month, due_dt.day)
    else:
        due_date = None

    # Create task in target user's mailbox
    task = Task(
        account=account,
        folder=account.tasks,
        subject=args.subject,
        body=args.body or "",
    )

    if start_date:
        task.start_date = start_date
    if due_date:
        task.due_date = due_date

    if args.priority:
        priority_map = {"low": "Low", "normal": "Normal", "high": "High"}
        task.importance = priority_map.get(args.priority.lower(), "Normal")

    try:
        task.save()
    except Exception as e:
        die(f"Failed to assign task to {args.to}: {e}")

    out(
        {
            "ok": True,
            "message": f"Task assigned to {args.to}",
            "task": task_to_dict(task),
            "assigned_to": args.to
        }
    )


def cmd_update(args: argparse.Namespace) -> None:
    """Update an existing task.
    
    Use --mailbox to update a task in another user's mailbox via delegate access.
    """
    # Determine which account to use
    if getattr(args, 'mailbox', None):
        from connection import get_account_for
        try:
            account = get_account_for(args.mailbox)
        except Exception as e:
            die(f"Failed to access mailbox {args.mailbox}: {e}")
    else:
        account = get_account()

    try:
        task = account.tasks.get(id=args.id)
    except Exception as e:
        error_resp = get_error_response(e, "get", args.id, getattr(args, 'mailbox', None))
        die(error_resp)

    # Update fields
    updated = []

    if args.subject:
        task.subject = args.subject
        updated.append("subject")

    if args.body:
        task.body = args.body
        updated.append("body")

    if args.due:
        task.due_date = parse_datetime(args.due)
        updated.append("due_date")

    if args.start:
        task.start_date = parse_datetime(args.start)
        updated.append("start_date")

    if args.priority:
        priority_map = {"low": "Low", "normal": "Normal", "high": "High"}
        task.importance = priority_map.get(args.priority.lower(), "Normal")
        updated.append("importance")

    if args.status:
        task.status = STATUS_MAP.get(args.status.lower(), args.status)
        updated.append("status")

        # If completed, set completion
        if args.status.lower() == "completed":
            task.percent_complete = Decimal("100")
            # complete_date is read-only - Exchange sets it automatically

    if args.percent:
        task.percent_complete = min(100, max(0, args.percent))
        updated.append("percent_complete")

        # Auto-update status based on percent
        if task.percent_complete == 100:
            task.status = "Completed"
            task.percent_complete = Decimal("100")
            # complete_date is read-only - Exchange sets it automatically
        elif task.percent_complete > 0:
            task.status = "InProgress"

    if not updated:
        die(
            "No fields to update. Use --subject, --body, --due, --start, --priority, --status, or --percent"
        )

    try:
        task.save(update_fields=updated)
    except Exception as e:
        error_resp = get_error_response(e, "update", args.id, getattr(args, 'mailbox', None))
        die(error_resp)

    out(
        {
            "ok": True,
            "message": "Task updated successfully",
            "mailbox": account.primary_smtp_address,
            "updated_fields": updated,
            "task": task_to_dict(task),
        }
    )


def cmd_complete(args: argparse.Namespace) -> None:
    """Mark a task as completed.
    
    Use --mailbox to complete a task in another user's mailbox via delegate access.
    """
    confirm_or_die(f"Mark task {args.id} as completed", getattr(args, 'yes', False))

    # Determine which account to use
    if getattr(args, 'mailbox', None):
        from connection import get_account_for
        try:
            account = get_account_for(args.mailbox)
        except Exception as e:
            die(f"Failed to access mailbox {args.mailbox}: {e}")
    else:
        account = get_account()

    try:
        task = account.tasks.get(id=args.id)
    except Exception as e:
        error_resp = get_error_response(e, "get", args.id, getattr(args, 'mailbox', None))
        die(error_resp)

    task.status = "Completed"
    task.percent_complete = Decimal("100")
    # complete_date is read-only - Exchange sets it automatically

    try:
        task.save(update_fields=["status", "percent_complete"])
    except Exception as e:
        error_resp = get_error_response(e, "complete", args.id, getattr(args, 'mailbox', None))
        die(error_resp)

    out({"ok": True, "message": "Task marked as completed", "mailbox": account.primary_smtp_address, "task": task_to_dict(task)})


def cmd_trash(args: argparse.Namespace) -> None:
    """Move a task to the Deleted Items folder.
    
    Use --mailbox to trash a task in another user's mailbox via delegate access.
    This is safer than hard delete as the task can be recovered from Deleted Items.
    """
    confirm_or_die(f"Move task {args.id} to trash", getattr(args, 'yes', False))

    # Determine which account to use
    if getattr(args, 'mailbox', None):
        from connection import get_account_for
        try:
            account = get_account_for(args.mailbox)
        except Exception as e:
            die(f"Failed to access mailbox {args.mailbox}: {e}")
    else:
        account = get_account()

    try:
        task = account.tasks.get(id=args.id)
    except Exception as e:
        error_resp = get_error_response(e, "get", args.id, getattr(args, 'mailbox', None))
        die(error_resp)

    task_info = task_to_dict(task)

    try:
        task.move_to_trash()
    except Exception as e:
        error_resp = get_error_response(e, "trash", args.id, getattr(args, 'mailbox', None))
        die(error_resp)

    out({"ok": True, "message": "Task moved to Deleted Items", "mailbox": account.primary_smtp_address, "task": task_info})


def add_parser(subparsers: argparse.ArgumentParser) -> None:
    """Add task commands to the CLI parser."""

    # connect
    p_connect = subparsers.add_parser("connect", help="Test connection to Exchange")
    p_connect.set_defaults(func=cmd_connect)
    add_json_argument(p_connect)

    # list
    p_list = subparsers.add_parser("list", help="List tasks")
    p_list.add_argument(
        "--limit", "-n", type=int, default=20, help="Maximum number of tasks to return"
    )
    p_list.add_argument(
        "--status",
        choices=["not_started", "in_progress", "completed", "waiting", "deferred"],
        help="Filter by status",
    )
    p_list.add_argument(
        "--completed",
        action="store_true",
        dest="completed_only",
        help="Show only completed tasks",
    )
    p_list.add_argument(
        "--all",
        "-a",
        action="store_true",
        dest="include_completed",
        help="Include completed tasks",
    )
    p_list.add_argument(
        "--overdue", action="store_true", help="Show only overdue tasks"
    )
    p_list.add_argument(
        "--mailbox", "-m",
        help="Target mailbox (email address). Use to access tasks via delegate permissions."
    )
    p_list.set_defaults(func=cmd_list)
    add_json_argument(p_list)

    # get
    p_get = subparsers.add_parser("get", help="Get task details")
    p_get.add_argument("--id", "-i", required=True, help="Task ID")
    p_get.add_argument(
        "--mailbox", "-m",
        help="Target mailbox (email address). Use to access tasks via delegate permissions."
    )
    p_get.set_defaults(func=cmd_get)
    add_json_argument(p_get)

    # create
    p_create = subparsers.add_parser("create", help="Create a new task")
    p_create.add_argument("--subject", "-s", required=True, help="Task subject")
    p_create.add_argument("--body", "-b", help="Task body/description")
    p_create.add_argument("--due", "-d", help="Due date (YYYY-MM-DD or +Nd for N days)")
    p_create.add_argument("--start", help="Start date (YYYY-MM-DD)")
    p_create.add_argument(
        "--priority",
        "-p",
        choices=["low", "normal", "high"],
        default="normal",
        help="Task priority",
    )
    p_create.add_argument(
        "--assign-to",
        help="Assign task to another user (email address). Requires delegate permissions.",
    )
    p_create.set_defaults(func=cmd_create)
    add_json_argument(p_create)
    add_yes_argument(p_create)

    # assign
    p_assign = subparsers.add_parser(
        "assign",
        help="Assign a task to another user via delegate access",
        description="Create a task directly in another user's Exchange mailbox. Requires the service account to have delegate permissions on the target mailbox.",
    )
    p_assign.add_argument(
        "--to",
        "-t",
        required=True,
        help="Target user email address (must have delegate access)",
    )
    p_assign.add_argument("--subject", "-s", required=True, help="Task subject")
    p_assign.add_argument("--body", "-b", help="Task body/description")
    p_assign.add_argument("--due", "-d", help="Due date (YYYY-MM-DD or +Nd for N days)")
    p_assign.add_argument("--start", help="Start date (YYYY-MM-DD)")
    p_assign.add_argument(
        "--priority",
        "-p",
        choices=["low", "normal", "high"],
        default="normal",
        help="Task priority",
    )
    p_assign.set_defaults(func=cmd_assign)
    add_json_argument(p_assign)

    # update
    p_update = subparsers.add_parser("update", help="Update a task")
    p_update.add_argument("--id", "-i", required=True, help="Task ID")
    p_update.add_argument("--subject", "-s", help="New subject")
    p_update.add_argument("--body", "-b", help="New body")
    p_update.add_argument("--due", "-d", help="New due date")
    p_update.add_argument("--start", help="New start date")
    p_update.add_argument(
        "--priority", "-p", choices=["low", "normal", "high"], help="New priority"
    )
    p_update.add_argument(
        "--status",
        choices=["not_started", "in_progress", "completed", "waiting", "deferred"],
        help="New status",
    )
    p_update.add_argument("--percent", type=int, help="Completion percentage (0-100)")
    p_update.add_argument(
        "--mailbox", "-m",
        help="Target mailbox (email address). Use to access tasks via delegate permissions."
    )
    p_update.set_defaults(func=cmd_update)
    add_json_argument(p_update)

    # complete
    p_complete = subparsers.add_parser("complete", help="Mark task as completed")
    p_complete.add_argument("--id", "-i", required=True, help="Task ID")
    p_complete.add_argument(
        "--mailbox", "-m",
        help="Target mailbox (email address). Use to access tasks via delegate permissions."
    )
    p_complete.set_defaults(func=cmd_complete)
    add_json_argument(p_complete)
    add_yes_argument(p_complete)

    # trash
    p_trash = subparsers.add_parser("trash", help="Move task to Deleted Items folder")
    p_trash.add_argument("--id", "-i", required=True, help="Task ID")
    p_trash.add_argument(
        "--mailbox", "-m",
        help="Target mailbox (email address). Use to access tasks via delegate permissions."
    )
    p_trash.set_defaults(func=cmd_trash)
    add_json_argument(p_trash)
    add_yes_argument(p_trash)


def main() -> None:
    """Main entry point for standalone execution."""
    add_json_argument(parser)
    parser = argparse.ArgumentParser(
        prog="tasks.py",
        description="Task operations for Exchange Mailbox",
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
