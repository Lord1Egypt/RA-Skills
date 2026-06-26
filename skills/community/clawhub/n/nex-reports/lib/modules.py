"""
Nex Reports - Module Implementations
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import json
import subprocess
from datetime import datetime
from imaplib import IMAP4_SSL
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import IMAP_HOST, IMAP_PORT, IMAP_USER, IMAP_PASS


def module_email(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check unread emails via IMAP.
    Returns: {"title": str, "content": str, "status": "ok/warning/error", "items": list}
    """
    try:
        host = config.get("imap_host", IMAP_HOST)
        user = config.get("imap_user", IMAP_USER)
        password = config.get("imap_pass", IMAP_PASS)
        port = config.get("imap_port", IMAP_PORT)
        limit = config.get("unread_limit", 5)

        if not user or not password:
            return {
                "title": "Email",
                "content": "IMAP credentials not configured",
                "status": "error",
                "items": [],
            }

        conn = IMAP4_SSL(host, port)
        conn.login(user, password)
        conn.select("INBOX")

        status, messages = conn.search(None, "UNSEEN")
        unread_ids = messages[0].split()
        unread_count = len(unread_ids)

        items = []
        for msg_id in unread_ids[-limit:]:
            status, msg_data = conn.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
            msg_text = msg_data[0][1].decode("utf-8", errors="ignore")

            subject = "Unknown"
            sender = "Unknown"

            for line in msg_text.split("\n"):
                if line.startswith("Subject:"):
                    subject = line.replace("Subject:", "").strip()
                elif line.startswith("From:"):
                    sender = line.replace("From:", "").strip()

            items.append(f"{sender}: {subject}")

        conn.close()

        content = f"Unread: {unread_count}"
        status_level = "warning" if unread_count > 10 else "ok"

        return {
            "title": "Email",
            "content": content,
            "status": status_level,
            "items": items,
        }

    except Exception as e:
        return {
            "title": "Email",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_calendar(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse ICS calendar file for events.
    """
    try:
        ics_path = config.get("ics_path")
        show_days = config.get("show_days", 7)

        if not ics_path:
            return {
                "title": "Calendar",
                "content": "ICS path not configured",
                "status": "error",
                "items": [],
            }

        ics_file = Path(ics_path)
        if not ics_file.exists():
            return {
                "title": "Calendar",
                "content": f"Calendar file not found: {ics_path}",
                "status": "error",
                "items": [],
            }

        items = []
        content = f"Events (next {show_days} days)"

        # Basic ICS parsing - extract lines with SUMMARY and DTSTART
        with open(ics_file, "r") as f:
            lines = f.readlines()

        current_event = {}
        for line in lines:
            line = line.strip()
            if line.startswith("SUMMARY:"):
                current_event["summary"] = line.replace("SUMMARY:", "").strip()
            elif line.startswith("DTSTART"):
                # Extract date/time
                parts = line.split(":")
                if len(parts) > 1:
                    current_event["dtstart"] = parts[1]
                if "summary" in current_event:
                    items.append(f"{current_event.get('dtstart', 'TBD')}: {current_event['summary']}")
                    current_event = {}

        return {
            "title": "Calendar",
            "content": content,
            "status": "ok",
            "items": items[:10],
        }

    except Exception as e:
        return {
            "title": "Calendar",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_tasks(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read JSON taskboard file.
    """
    try:
        taskboard_path = config.get("taskboard_path")

        if not taskboard_path:
            return {
                "title": "Tasks",
                "content": "Taskboard path not configured",
                "status": "error",
                "items": [],
            }

        taskboard_file = Path(taskboard_path)
        if not taskboard_file.exists():
            return {
                "title": "Tasks",
                "content": f"Taskboard file not found: {taskboard_path}",
                "status": "error",
                "items": [],
            }

        with open(taskboard_file, "r") as f:
            tasks = json.load(f)

        items = []
        open_count = 0

        if isinstance(tasks, list):
            for task in tasks:
                if isinstance(task, dict):
                    status = task.get("status", "open")
                    if status == "open":
                        open_count += 1
                        title = task.get("title", "Untitled")
                        due = task.get("due", "No due date")
                        items.append(f"{title} (due: {due})")
        elif isinstance(tasks, dict):
            for task_id, task in tasks.items():
                if isinstance(task, dict):
                    status = task.get("status", "open")
                    if status == "open":
                        open_count += 1
                        title = task.get("title", task_id)
                        due = task.get("due", "No due date")
                        items.append(f"{title} (due: {due})")

        return {
            "title": "Tasks",
            "content": f"Open tasks: {open_count}",
            "status": "warning" if open_count > 5 else "ok",
            "items": items[:10],
        }

    except Exception as e:
        return {
            "title": "Tasks",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_health(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run `nex-healthcheck check` subprocess.
    """
    try:
        result = subprocess.run(
            ["nex-healthcheck", "check"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return {
                "title": "Health Check",
                "content": "Errors detected",
                "status": "error",
                "items": result.stderr.split("\n")[:5],
            }

        items = result.stdout.split("\n")
        return {
            "title": "Health Check",
            "content": "All systems operational",
            "status": "ok",
            "items": [line for line in items if line.strip()][:5],
        }

    except subprocess.TimeoutExpired:
        return {
            "title": "Health Check",
            "content": "Timeout",
            "status": "error",
            "items": [],
        }
    except FileNotFoundError:
        return {
            "title": "Health Check",
            "content": "nex-healthcheck not found",
            "status": "error",
            "items": [],
        }
    except Exception as e:
        return {
            "title": "Health Check",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_crm(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run `nex-crm pipeline` subprocess.
    """
    try:
        result = subprocess.run(
            ["nex-crm", "pipeline"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return {
                "title": "CRM Pipeline",
                "content": "Pipeline retrieval failed",
                "status": "warning",
                "items": [],
            }

        items = result.stdout.split("\n")
        return {
            "title": "CRM Pipeline",
            "content": "Pipeline status",
            "status": "ok",
            "items": [line for line in items if line.strip()][:5],
        }

    except subprocess.TimeoutExpired:
        return {
            "title": "CRM Pipeline",
            "content": "Timeout",
            "status": "error",
            "items": [],
        }
    except FileNotFoundError:
        return {
            "title": "CRM Pipeline",
            "content": "nex-crm not found",
            "status": "error",
            "items": [],
        }
    except Exception as e:
        return {
            "title": "CRM Pipeline",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_expenses(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run `nex-expenses summary monthly` subprocess.
    """
    try:
        result = subprocess.run(
            ["nex-expenses", "summary", "monthly"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return {
                "title": "Expenses",
                "content": "Summary failed",
                "status": "warning",
                "items": [],
            }

        items = result.stdout.split("\n")
        return {
            "title": "Expenses",
            "content": "Monthly summary",
            "status": "ok",
            "items": [line for line in items if line.strip()][:5],
        }

    except subprocess.TimeoutExpired:
        return {
            "title": "Expenses",
            "content": "Timeout",
            "status": "error",
            "items": [],
        }
    except FileNotFoundError:
        return {
            "title": "Expenses",
            "content": "nex-expenses not found",
            "status": "error",
            "items": [],
        }
    except Exception as e:
        return {
            "title": "Expenses",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_deliverables(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run `nex-deliverables overdue` subprocess.
    """
    try:
        result = subprocess.run(
            ["nex-deliverables", "overdue"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        items = result.stdout.split("\n") if result.stdout else []
        status = "warning" if result.returncode != 0 or items else "ok"

        return {
            "title": "Deliverables",
            "content": "Overdue items",
            "status": status,
            "items": [line for line in items if line.strip()][:5],
        }

    except subprocess.TimeoutExpired:
        return {
            "title": "Deliverables",
            "content": "Timeout",
            "status": "error",
            "items": [],
        }
    except FileNotFoundError:
        return {
            "title": "Deliverables",
            "content": "nex-deliverables not found",
            "status": "error",
            "items": [],
        }
    except Exception as e:
        return {
            "title": "Deliverables",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_domains(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run `nex-domains expiring` subprocess.
    """
    try:
        result = subprocess.run(
            ["nex-domains", "expiring"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        items = result.stdout.split("\n") if result.stdout else []
        status = "warning" if result.returncode != 0 or items else "ok"

        return {
            "title": "Domains",
            "content": "Expiring domains",
            "status": status,
            "items": [line for line in items if line.strip()][:5],
        }

    except subprocess.TimeoutExpired:
        return {
            "title": "Domains",
            "content": "Timeout",
            "status": "error",
            "items": [],
        }
    except FileNotFoundError:
        return {
            "title": "Domains",
            "content": "nex-domains not found",
            "status": "error",
            "items": [],
        }
    except Exception as e:
        return {
            "title": "Domains",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_vault(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run `nex-vault alerts` subprocess.
    """
    try:
        result = subprocess.run(
            ["nex-vault", "alerts"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        items = result.stdout.split("\n") if result.stdout else []
        status = "warning" if result.returncode != 0 or items else "ok"

        return {
            "title": "Vault",
            "content": "Security alerts",
            "status": status,
            "items": [line for line in items if line.strip()][:5],
        }

    except subprocess.TimeoutExpired:
        return {
            "title": "Vault",
            "content": "Timeout",
            "status": "error",
            "items": [],
        }
    except FileNotFoundError:
        return {
            "title": "Vault",
            "content": "nex-vault not found",
            "status": "error",
            "items": [],
        }
    except Exception as e:
        return {
            "title": "Vault",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def module_custom(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run arbitrary shell command.
    """
    try:
        command = config.get("command")

        if not command:
            return {
                "title": "Custom Command",
                "content": "No command specified",
                "status": "error",
                "items": [],
            }

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )

        items = result.stdout.split("\n") if result.stdout else []
        status = "error" if result.returncode != 0 else "ok"

        return {
            "title": "Custom Command",
            "content": command,
            "status": status,
            "items": [line for line in items if line.strip()][:5],
        }

    except subprocess.TimeoutExpired:
        return {
            "title": "Custom Command",
            "content": "Timeout",
            "status": "error",
            "items": [],
        }
    except Exception as e:
        return {
            "title": "Custom Command",
            "content": f"Error: {str(e)}",
            "status": "error",
            "items": [],
        }


def run_module(module_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatcher for running modules.
    """
    module_map = {
        "EMAIL": module_email,
        "CALENDAR": module_calendar,
        "TASKS": module_tasks,
        "HEALTH": module_health,
        "CRM": module_crm,
        "EXPENSES": module_expenses,
        "DELIVERABLES": module_deliverables,
        "DOMAINS": module_domains,
        "VAULT": module_vault,
        "CUSTOM": module_custom,
    }

    if module_type not in module_map:
        return {
            "title": module_type,
            "content": f"Unknown module: {module_type}",
            "status": "error",
            "items": [],
        }

    return module_map[module_type](config)
