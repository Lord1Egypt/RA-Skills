#!/usr/bin/env python3
"""
Nex Reports - Scheduled Report Generator
Meta-skill that chains other skills and compiles results into formatted reports.
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from lib.config import (
    REPORT_FOOTER,
    REPORT_MODULES,
    SCHEDULE_PRESETS,
    OUTPUT_FORMATS,
    OUTPUT_TARGETS,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
)
from lib.storage import get_db
from lib.modules import run_module
from lib.formatter import format_report
from lib.notifier import save_report


def cmd_create(args):
    """Create a new report config."""
    db = get_db()

    # Parse modules
    if not args.modules:
        print("Error: --modules required")
        return False

    modules_list = []
    for module_spec in args.modules.split(","):
        module_spec = module_spec.strip().upper()
        if module_spec not in REPORT_MODULES:
            print(f"Error: Unknown module: {module_spec}")
            return False
        modules_list.append({"type": module_spec})

    # Validate schedule
    schedule = args.schedule
    if schedule.upper() in SCHEDULE_PRESETS:
        schedule = SCHEDULE_PRESETS[schedule.upper()]

    # Validate output format
    if args.output.upper() not in [f.upper() for f in OUTPUT_FORMATS.values()]:
        print(f"Error: Invalid output format: {args.output}")
        return False

    # Save config
    config_id = db.save_config(
        name=args.name,
        schedule=schedule,
        modules=modules_list,
        output_format=args.output.lower(),
        output_target=args.output_target.lower(),
        enabled=True,
    )

    if config_id:
        print(f"Report config created: {args.name} (ID: {config_id})")
        return True
    else:
        print(f"Error: Report config '{args.name}' already exists or database error")
        return False


def cmd_run(args):
    """Run a report or all reports."""
    db = get_db()

    if args.all:
        configs = db.list_configs()
        if not configs:
            print("No report configs found")
            return True

        results = []
        for config in configs:
            result = _run_report(config)
            results.append(result)

        success_count = sum(1 for r in results if r)
        print(f"Ran {success_count}/{len(configs)} reports")
        return all(results)
    else:
        if not args.name:
            print("Error: --name required or use --all")
            return False

        config = db.get_config(args.name)
        if not config:
            print(f"Error: Report config not found: {args.name}")
            return False

        return _run_report(config)


def _run_report(config: dict) -> bool:
    """Internal function to run a single report."""
    db = get_db()

    print(f"\nRunning report: {config['name']}")
    started_at = datetime.utcnow().isoformat()

    module_results = []
    errors = {}

    for module_config in config["modules"]:
        module_type = module_config.get("type")
        print(f"  Running module: {module_type}")

        try:
            result = run_module(module_type, module_config)
            module_results.append(result)
        except Exception as e:
            print(f"    Error: {e}")
            errors[module_type] = str(e)

    # Format report
    title = f"{config['name']} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    formatted = format_report(title, module_results, config["output_format"])

    # Save/send report
    output_path = save_report(
        formatted,
        config["output_format"],
        config["name"],
        config["output_target"],
        TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID,
    )

    # Save run record
    status = "partial" if errors else "success"
    db.save_run(
        config["id"],
        started_at,
        status,
        module_results,
        errors if errors else None,
        output_path,
    )

    print(f"  Status: {status}")
    if output_path:
        print(f"  Output: {output_path}")

    return True


def cmd_list(args):
    """List all report configs."""
    db = get_db()
    configs = db.list_configs()

    if not configs:
        print("No report configs found")
        return True

    print(f"\n{'Name':<30} {'Schedule':<20} {'Modules':<30} {'Target':<10}")
    print("-" * 90)

    for config in configs:
        modules = ", ".join(m.get("type", "?") for m in config["modules"])
        last_run = config.get("last_run", "Never")
        if last_run and len(last_run) > 19:
            last_run = last_run[:16]

        print(
            f"{config['name']:<30} {config['schedule']:<20} {modules:<30} {config['output_target']:<10}"
        )

    print()
    return True


def cmd_show(args):
    """Show report config and last run."""
    db = get_db()
    config = db.get_config(args.name)

    if not config:
        print(f"Error: Report config not found: {args.name}")
        return False

    print(f"\nReport: {config['name']}")
    print(f"  Schedule: {config['schedule']}")
    print(f"  Modules: {', '.join(m.get('type', '?') for m in config['modules'])}")
    print(f"  Output Format: {config['output_format']}")
    print(f"  Output Target: {config['output_target']}")
    print(f"  Enabled: {config['enabled']}")
    print(f"  Created: {config['created_at']}")
    if config.get("last_run"):
        print(f"  Last Run: {config['last_run']}")

    # Show last run
    latest = db.get_latest_run(args.name)
    if latest:
        print(f"\n  Latest Run:")
        print(f"    Started: {latest['started_at']}")
        print(f"    Status: {latest['status']}")
        if latest.get("output_path"):
            print(f"    Output: {latest['output_path']}")
        if latest.get("errors"):
            print(f"    Errors: {json.dumps(latest['errors'], indent=6)}")

    print()
    return True


def cmd_edit(args):
    """Edit report config."""
    db = get_db()
    config = db.get_config(args.name)

    if not config:
        print(f"Error: Report config not found: {args.name}")
        return False

    updated = False

    if args.schedule:
        schedule = args.schedule
        if schedule.upper() in SCHEDULE_PRESETS:
            schedule = SCHEDULE_PRESETS[schedule.upper()]
        config["schedule"] = schedule
        updated = True

    if args.modules:
        modules_list = []
        for module_spec in args.modules.split(","):
            module_spec = module_spec.strip().upper()
            if module_spec not in REPORT_MODULES:
                print(f"Error: Unknown module: {module_spec}")
                return False
            modules_list.append({"type": module_spec})
        config["modules"] = modules_list
        updated = True

    if args.output:
        config["output_format"] = args.output.lower()
        updated = True

    if args.output_target:
        config["output_target"] = args.output_target.lower()
        updated = True

    if updated:
        db.update_config(
            args.name,
            schedule=config.get("schedule"),
            modules=config.get("modules"),
            output_format=config.get("output_format"),
            output_target=config.get("output_target"),
        )
        print(f"Report config updated: {args.name}")
        return True
    else:
        print("No changes specified")
        return False


def cmd_delete(args):
    """Delete report config."""
    db = get_db()

    if db.delete_config(args.name):
        print(f"Report config deleted: {args.name}")
        return True
    else:
        print(f"Error: Report config not found: {args.name}")
        return False


def cmd_history(args):
    """Show run history for a report."""
    db = get_db()
    config = db.get_config(args.name)

    if not config:
        print(f"Error: Report config not found: {args.name}")
        return False

    limit = args.limit or 10
    runs = db.get_runs(args.name, limit=limit)

    if not runs:
        print(f"No runs found for: {args.name}")
        return True

    print(f"\nRun History: {args.name}")
    print(f"{'Started':<20} {'Status':<10} {'Output':<50}")
    print("-" * 80)

    for run in runs:
        started = run["started_at"][:16] if run["started_at"] else "?"
        output = Path(run["output_path"]).name if run["output_path"] else "-"
        print(f"{started:<20} {run['status']:<10} {output:<50}")

    print()
    return True


def cmd_modules(args):
    """List available modules."""
    print("\nAvailable Modules:")
    print("-" * 60)

    for module_key, module_info in REPORT_MODULES.items():
        print(f"\n{module_key}")
        print(f"  Name: {module_info['name']}")
        print(f"  Description: {module_info['description']}")
        if module_info.get("config_keys"):
            print(f"  Config: {', '.join(module_info['config_keys'])}")

    print("\nSchedule Presets:")
    print("-" * 60)
    for preset, cron in SCHEDULE_PRESETS.items():
        print(f"  {preset}: {cron}")

    print()
    return True


def cmd_test(args):
    """Test a single module."""
    if args.module.upper() not in REPORT_MODULES:
        print(f"Error: Unknown module: {args.module}")
        return False

    print(f"Testing module: {args.module}")

    try:
        result = run_module(args.module.upper(), args.config or {})
        print(f"  Title: {result.get('title')}")
        print(f"  Status: {result.get('status')}")
        print(f"  Content: {result.get('content')}")

        items = result.get("items", [])
        if items:
            print(f"  Items ({len(items)}):")
            for item in items[:5]:
                print(f"    - {item}")

        print()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def cmd_config(args):
    """Set configuration."""
    print("Configuration commands not yet implemented")
    print("Use environment variables instead:")
    print("  IMAP_HOST, IMAP_USER, IMAP_PASS, IMAP_PORT")
    print("  TELEGRAM_TOKEN, TELEGRAM_CHAT_ID")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Nex Reports - Scheduled Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  nex-reports create "Monday Morning" --schedule "0 8 * * 1" --modules health,crm,deliverables --output markdown
  nex-reports run "Monday Morning"
  nex-reports run --all
  nex-reports list
  nex-reports show "Monday Morning"
  nex-reports edit "Monday Morning" --modules health,crm,expenses
  nex-reports delete "Monday Morning"
  nex-reports history "Monday Morning"
  nex-reports modules
  nex-reports test health

{REPORT_FOOTER}
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # create command
    create_parser = subparsers.add_parser("create", help="Create report config")
    create_parser.add_argument("name", help="Report name")
    create_parser.add_argument("--schedule", required=True, help="Cron expression or preset")
    create_parser.add_argument("--modules", required=True, help="Comma-separated module names")
    create_parser.add_argument(
        "--output", default="markdown", help="Output format: telegram, markdown, html, json"
    )
    create_parser.add_argument(
        "--output-target", default="file", help="Output target: file, telegram, both"
    )

    # run command
    run_parser = subparsers.add_parser("run", help="Run report(s)")
    run_parser.add_argument("name", nargs="?", help="Report name")
    run_parser.add_argument("--all", action="store_true", help="Run all enabled reports")

    # list command
    subparsers.add_parser("list", help="List reports")

    # show command
    show_parser = subparsers.add_parser("show", help="Show report config and last run")
    show_parser.add_argument("name", help="Report name")

    # edit command
    edit_parser = subparsers.add_parser("edit", help="Edit report config")
    edit_parser.add_argument("name", help="Report name")
    edit_parser.add_argument("--schedule", help="New schedule")
    edit_parser.add_argument("--modules", help="New modules (comma-separated)")
    edit_parser.add_argument("--output", help="New output format")
    edit_parser.add_argument("--output-target", help="New output target")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete report config")
    delete_parser.add_argument("name", help="Report name")

    # history command
    history_parser = subparsers.add_parser("history", help="Show run history")
    history_parser.add_argument("name", help="Report name")
    history_parser.add_argument("--limit", type=int, help="Number of runs to show")

    # modules command
    subparsers.add_parser("modules", help="List available modules")

    # test command
    test_parser = subparsers.add_parser("test", help="Test module")
    test_parser.add_argument("module", help="Module name")
    test_parser.add_argument("--config", help="JSON config for module")

    # config command
    subparsers.add_parser("config", help="Set configuration")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Dispatch to command
    cmd_map = {
        "create": cmd_create,
        "run": cmd_run,
        "list": cmd_list,
        "show": cmd_show,
        "edit": cmd_edit,
        "delete": cmd_delete,
        "history": cmd_history,
        "modules": cmd_modules,
        "test": cmd_test,
        "config": cmd_config,
    }

    cmd_func = cmd_map.get(args.command)
    if cmd_func:
        result = cmd_func(args)
        return 0 if result else 1
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
