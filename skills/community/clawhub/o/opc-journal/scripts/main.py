"""OPC Journal - CLI-style single skill entry point.

Usage:
    /opc-journal <command> [options]

Commands:
    init        Initialize journal
    record      Record an entry
    search      Search entries
    export      Export journal
    analyze     Analyze patterns from memory
    milestones  Detect milestones
    insights    Generate insights
    task        Create async task (legacy)
    batch-task  Create multiple async tasks at once
    status      Show journal status
    delete      Delete a journal entry
    archive     Archive journal data
    update-meta Update journal metadata
    help        Show this help
"""
import sys
import json
import argparse
from typing import List, Dict, Any

# Ensure skill root is on path
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.commands import init, record, search, export, analyze, milestones, insights, task, status, update_meta, delete, archive, batch_task


COMMANDS = {
    "init": init,
    "record": record,
    "search": search,
    "export": export,
    "analyze": analyze,
    "milestones": milestones,
    "insights": insights,
    "task": task,
    "batch-task": batch_task,
    "status": status,
    "update-meta": update_meta,
    "delete": delete,
    "archive": archive,
}


class _NoExitParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def _build_parser() -> _NoExitParser:
    parser = _NoExitParser(
        prog="opc-journal",
        description="OPC Journal - One Person Company growth journal"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p = subparsers.add_parser("init", help="Initialize journal")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--day", type=int, default=1)
    p.add_argument("--goals", nargs="*", default=[])
    p.add_argument("--preferences", type=json.loads, default={})
    p.add_argument("--language", default="", help="Force language (zh/en). Auto-detected if omitted.")

    # record
    p = subparsers.add_parser("record", help="Record a journal entry")
    p.add_argument("content", nargs="?", help="Entry content")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--day", type=int, default=1)
    p.add_argument("--metadata", type=json.loads, default={})

    # search
    p = subparsers.add_parser("search", help="Search journal entries")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--query", default="")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--case-sensitive", action="store_true", default=False)

    # export
    p = subparsers.add_parser("export", help="Export journal")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--format", default="markdown")
    p.add_argument("--time-range", default="all")
    p.add_argument("--output-path", default="")

    # analyze
    p = subparsers.add_parser("analyze", help="Analyze patterns")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--dimension", default="general")

    # milestones
    p = subparsers.add_parser("milestones", help="Detect milestones")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--content", default="")
    p.add_argument("--day", type=int, default=1)

    # insights
    p = subparsers.add_parser("insights", help="Generate insights")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--day", type=int, default=1)
    p.add_argument("--days-back", type=int, default=7)

    # task
    p = subparsers.add_parser("task", help="Create async task")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--type", default="research")
    p.add_argument("--description", default="")
    p.add_argument("--timeout-hours", type=int, default=8)

    # batch-task
    p = subparsers.add_parser("batch-task", help="Create multiple async tasks at once")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--type", default="research")
    p.add_argument("--descriptions", nargs="+", required=True, help="List of task descriptions")
    p.add_argument("--timeout-hours", type=int, default=8)

    # status
    p = subparsers.add_parser("status", help="Show journal status")
    p.add_argument("--customer-id", default="OPC-001")

    # delete
    p = subparsers.add_parser("delete", help="Delete a journal entry by entry_id")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--entry-id", required=True, help="Entry ID to delete")
    p.add_argument("--force", action="store_true", help="Confirm destructive deletion")

    # archive
    p = subparsers.add_parser("archive", help="Archive journal data")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--clear", action="store_true", help="Clear memory files after archiving")
    p.add_argument("--force", action="store_true", help="Confirm destructive clear")

    # update-meta
    p = subparsers.add_parser("update-meta", help="Update journal metadata")
    p.add_argument("--customer-id", default="OPC-001")
    p.add_argument("--language", default="", help="Switch language (zh/en)")
    p.add_argument("--goals", nargs="*", default=None)
    p.add_argument("--preferences", type=json.loads, default=None)

    # help
    subparsers.add_parser("help", help="Show help")

    return parser


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = _build_parser()
    if not argv:
        parser.print_help()
        raise SystemExit(0)
    return parser.parse_args(argv)


def main(context: dict = None) -> dict:
    """Main entry point. Accepts OpenClaw context dict or runs as CLI."""
    if context is None:
        argv = sys.argv[1:]
        customer_id = "OPC-001"
    else:
        input_data = context.get("input", {})
        if isinstance(input_data, dict):
            argv = input_data.get("argv", [])
            text = input_data.get("text", "")
            if text and not argv:
                argv = text.split()
            customer_id = context.get("customer_id", "OPC-001")
        else:
            argv = str(input_data).split()
            customer_id = context.get("customer_id", "OPC-001")

    try:
        args = parse_args(argv)
    except ValueError as e:
        return {
            "status": "error",
            "result": None,
            "message": str(e)
        }
    except SystemExit:
        return {
            "status": "success",
            "result": {"help_displayed": True},
            "message": "Help displayed"
        }

    cmd_name = args.command
    if not cmd_name or cmd_name == "help":
        parser = _build_parser()
        parser.print_help()
        return {
            "status": "success",
            "result": {"help_displayed": True},
            "message": "Help displayed"
        }

    module = COMMANDS.get(cmd_name)
    if not module:
        return {
            "status": "error",
            "result": None,
            "message": f"Unknown command: {cmd_name}"
        }

    # Build args dict from namespace
    args_dict = {k: v for k, v in vars(args).items() if k != "command"}
    # Override customer_id from context if explicit in context but not argv
    if context and "customer_id" in context and not any(a.startswith("--customer-id") for a in argv):
        args_dict["customer_id"] = context["customer_id"]

    return module.run(args_dict.get("customer_id", customer_id), args_dict)


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, ensure_ascii=False))
