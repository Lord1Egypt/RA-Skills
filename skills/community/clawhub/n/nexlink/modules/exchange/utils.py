"""
Utility functions for Exchange Mailbox skill.
Common functions used across all modules.
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import List, Optional, Dict, Any

# Try to import exchangelib for type hints
try:
    from exchangelib.items import Task
    HAS_EXCHANGELIB = True
except ImportError:
    HAS_EXCHANGELIB = False
    Task = None  # type: ignore

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logger import get_logger

def add_json_argument(parser: argparse.ArgumentParser) -> None:
    """Add --json flag for machine-readable JSON output."""
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output results in JSON format",
    )


def add_yes_argument(parser: argparse.ArgumentParser) -> None:
    """Add --yes flag for per-command confirmation bypass."""
    parser.add_argument(
        "--yes",
        action="store_true",
        default=False,
        help="Skip confirmation for this single command (use only in tightly scoped automation)",
    )


_logger = get_logger()


def out(data: Dict[str, Any]) -> None:
    """Output JSON to stdout and exit successfully."""
    print(json.dumps(data, indent=2, default=str))
    sys.exit(0)


def confirm_or_die(action_desc: str, auto_approved: bool = False) -> None:
    """Prompt for confirmation before a destructive operation.

    Exits with code 2 on non-confirmation. When auto_approved is True (e.g.,
    via the per-command --yes flag), the prompt is skipped for this single
    invocation only. There is no session-wide or environment bypass.

    Args:
        action_desc: Human-readable description of what's about to happen.
        auto_approved: If True, skip confirmation (from per-command --yes).
    """
    if auto_approved:
        return

    if not sys.stdin.isatty():
        die({
            "ok": False,
            "error": (
                f"Confirmation required: {action_desc}. "
                "Re-run with --yes to confirm this single operation."
            ),
        })

    try:
        answer = input(f"⚠️  {action_desc} [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("", file=sys.stderr)
        sys.exit(2)

    if answer not in ("y", "yes"):
        print("Aborted.", file=sys.stderr)
        sys.exit(2)


def die(message) -> None:
    """Output error JSON to stdout and exit with error code.
    
    Args:
        message: String error message or dict with error details
    """
    if isinstance(message, dict):
        print(json.dumps(message, indent=2, default=str))
    else:
        print(json.dumps({"ok": False, "error": message}, indent=2))
    sys.exit(1)


def parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Parse date string in various formats."""
    if not date_str:
        return None
    
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime for JSON output."""
    if dt is None:
        return None
    
    return dt.isoformat()


def mask_email(email: str) -> str:
    """Mask email for logging (show first char and domain)."""
    if not email or "@" not in email:
        return "***"
    local, domain = email.split("@", 1)
    return f"{local[0]}***@{domain}"


def parse_recipients(recipient_str: Optional[str]) -> List[str]:
    """Parse comma-separated recipient string into list."""
    if not recipient_str:
        return []
    return [addr.strip() for addr in recipient_str.split(",") if addr.strip()]


def task_to_dict(task: Task, detailed: bool = False) -> Dict[str, Any]:
    """
    Convert Task object to dictionary.
    
    Args:
        task: exchangelib Task object
        detailed: If True, include extended fields (body, owner, etc.)
    
    Returns:
        Dictionary representation of the task
    """
    if not HAS_EXCHANGELIB or task is None:
        return {}
    
    # Status mapping (same as in tasks.py)
    STATUS_REVERSE = {v: k for k, v in {
        "NotStarted": 1,
        "InProgress": 2,
        "Completed": 3,
        "WaitingOnOthers": 4,
        "Deferred": 5,
    }.items()}
    
    result = {
        "id": task.id,
        "subject": task.subject or "",
        "status": STATUS_REVERSE.get(str(task.status), str(task.status)),
        "percent_complete": task.percent_complete or 0,
        "due_date": format_datetime(task.due_date),
        "start_date": format_datetime(task.start_date),
    }
    
    if detailed:
        result.update(
            {
                "body": task.body if task.body else None,
                "owner": task.owner,
                "delegation_state": (
                    str(task.delegation_state) if task.delegation_state else None
                ),
                "complete_date": format_datetime(task.complete_date),
                "importance": str(task.importance) if task.importance else None,
                "changekey": task.changekey,
                "datetime_created": format_datetime(task.datetime_created),
                "datetime_received": format_datetime(task.datetime_received),
            }
        )
    
    return result