#!/usr/bin/env python3
"""
Nex HealthCheck - Multi-Service Health Dashboard
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add lib to path
LIB_DIR = Path(__file__).parent / "lib"
sys.path.insert(0, str(LIB_DIR))

from config import CheckType, StatusLevel, DATA_DIR, DEFAULT_CHECK_INTERVAL
from storage import (
    init_db, save_service, get_service, list_services, delete_service,
    save_check_result, get_latest_results, get_service_history,
    get_incidents, resolve_incident, get_uptime_stats, get_dashboard_summary,
    search_services
)
from checkers import run_check, run_all_checks
from alerter import send_telegram_alert, format_dashboard_message, format_incident_alert, format_status_emoji

FOOTER = "[Nex HealthCheck by Nex AI | nex-ai.be]"


def cmd_check(args):
    """Run health checks."""
    # Get services to check
    if args.service:
        services = [s for s in list_services() if s["name"] == args.service]
        if not services:
            print(f"Service not found: {args.service}")
            return 1
    elif args.group:
        services = list_services(group_name=args.group)
    elif args.tag:
        services = list_services(tag=args.tag)
    else:
        services = list_services(enabled_only=True)

    if not services:
        print("No services to check")
        return 0

    # Run checks
    print("Health Dashboard")
    print("---")

    results_by_group = {}
    for service in services:
        result = run_check(service)
        save_check_result(service["id"], result.get("status"), result.get("response_time_ms"), result.get("message"), result.get("details"))

        group = service.get("group_name") or "General"
        if group not in results_by_group:
            results_by_group[group] = []
        results_by_group[group].append((service, result))

    # Print grouped results
    for group in sorted(results_by_group.keys()):
        print(f"\n[{group}]")
        for service, result in results_by_group[group]:
            emoji = format_status_emoji(result.get("status"))
            name = service["name"]
            message = result.get("message", "No details")
            response = f" {result.get('response_time_ms')}ms" if result.get("response_time_ms") else ""
            print(f"  {emoji} {name:30} {message}{response}")

    # Summary
    summary = get_dashboard_summary()
    total = summary.get("total_services", 0)
    healthy = summary.get("healthy_services", 0)
    print(f"\n---")
    print(f"All systems operational. {healthy}/{total} healthy.")
    print(f"\n{FOOTER}")

    return 0


def cmd_add(args):
    """Add a service to monitor."""
    if not args.name or not args.type or not args.target:
        print("Error: --name, --type, and --target are required")
        return 1

    # Validate check type
    try:
        check_type = CheckType[args.type.upper().replace("-", "_")]
    except KeyError:
        valid = ", ".join([t.value for t in CheckType])
        print(f"Invalid check type. Valid types: {valid}")
        return 1

    service_id = save_service(
        name=args.name,
        check_type=check_type.value,
        target=args.target,
        expected_status=args.expected,
        port=args.port,
        enabled=True,
        check_interval=args.interval or DEFAULT_CHECK_INTERVAL,
        tags=args.tag,
        group_name=args.group,
        notes=args.notes
    )

    print(f"Service '{args.name}' added (ID: {service_id})")
    print(FOOTER)
    return 0


def cmd_list(args):
    """List all monitored services."""
    services = list_services()

    if not services:
        print("No services configured")
        print(FOOTER)
        return 0

    print("Monitored Services")
    print("---")

    by_group = {}
    for s in services:
        group = s.get("group_name") or "General"
        if group not in by_group:
            by_group[group] = []
        by_group[group].append(s)

    for group in sorted(by_group.keys()):
        print(f"\n[{group}]")
        for s in by_group[group]:
            enabled = "✓" if s.get("enabled") else "✗"
            print(f"  {enabled} {s['name']:30} [{s['check_type']}] {s['target']}")
            if s.get("notes"):
                print(f"    Notes: {s['notes']}")

    print(f"\n{FOOTER}")
    return 0


def cmd_remove(args):
    """Remove a service."""
    services = [s for s in list_services() if s["name"] == args.name]
    if not services:
        print(f"Service not found: {args.name}")
        return 1

    service = services[0]
    delete_service(service["id"])
    print(f"Service '{args.name}' removed")
    print(FOOTER)
    return 0


def cmd_status(args):
    """Quick status using last cached results."""
    results = get_latest_results(limit=100)

    if not results:
        print("No check results yet. Run 'nex-healthcheck check' first.")
        print(FOOTER)
        return 0

    # Group by service
    by_service = {}
    for r in results:
        service_id = r.get("service_id")
        if service_id not in by_service:
            by_service[service_id] = r

    print("Status (Last Check)")
    print("---")

    for result in by_service.values():
        emoji = format_status_emoji(result.get("status"))
        name = result.get("name", "Unknown")
        message = result.get("message", "")
        checked = result.get("checked_at", "?")
        print(f"  {emoji} {name:30} {message}")
        print(f"     Last checked: {checked}")

    print(f"\n{FOOTER}")
    return 0


def cmd_history(args):
    """Show check history for a service."""
    services = [s for s in list_services() if s["name"] == args.name]
    if not services:
        print(f"Service not found: {args.name}")
        return 1

    service = services[0]
    days = int(args.days or 7)
    history = get_service_history(service["id"], days=days)

    if not history:
        print(f"No history for '{args.name}' in last {days} days")
        print(FOOTER)
        return 0

    print(f"Check History - {args.name}")
    print(f"(Last {days} days)")
    print("---")

    for h in sorted(history, key=lambda x: x.get("date", "")):
        date = h.get("date", "?")
        uptime = h.get("uptime_pct", 0)
        avg_response = h.get("avg_response_ms", 0)
        total = h.get("checks_total", 0)
        failed = h.get("checks_failed", 0)
        print(f"  {date}: {uptime:.1f}% uptime, {avg_response}ms avg, {total-failed}/{total} successful")

    print(f"\n{FOOTER}")
    return 0


def cmd_incidents(args):
    """Show incidents."""
    active_only = not args.all
    incidents = get_incidents(active_only=active_only)

    if not incidents:
        print("No incidents" + (" (showing all)" if args.all else " (showing active only)"))
        print(FOOTER)
        return 0

    print("Incidents" + (" (All)" if args.all else " (Active)"))
    print("---")

    for inc in incidents:
        service_name = inc.get("name", "Unknown")
        status = inc.get("status", "?")
        started = inc.get("started_at", "?")
        resolved = inc.get("resolved_at", "?")
        duration = inc.get("duration_seconds", 0)

        if resolved:
            duration_str = f" ({int(duration/60)}m duration)"
        else:
            duration_str = " (ongoing)"

        print(f"  [{status}] {service_name}")
        print(f"    Started: {started}{duration_str}")
        if resolved:
            print(f"    Resolved: {resolved}")

    print(f"\n{FOOTER}")
    return 0


def cmd_uptime(args):
    """Show uptime statistics."""
    services = list_services()

    if not services:
        print("No services configured")
        return 0

    days = int(args.days or 30)

    print(f"Uptime Statistics (Last {days} days)")
    print("---")

    for service in services:
        stats = get_uptime_stats(service["id"], days=days)
        total = stats.get("total_checks", 0)
        failed = stats.get("failed_checks", 0)
        uptime = stats.get("avg_uptime", 100)
        avg_response = stats.get("avg_response_ms", 0)

        print(f"  {service['name']}")
        print(f"    Uptime: {uptime:.1f}%")
        print(f"    Checks: {total-failed}/{total} successful")
        print(f"    Avg Response: {avg_response}ms")

    print(f"\n{FOOTER}")
    return 0


def cmd_dashboard(args):
    """Full dashboard view."""
    services = list_services(enabled_only=True)
    results = get_latest_results(limit=200)

    if not services:
        print("No services configured")
        print(FOOTER)
        return 0

    # Match latest result for each service
    by_service = {}
    for r in results:
        service_id = r.get("service_id")
        if service_id not in by_service:
            by_service[service_id] = r

    print("Health Dashboard")
    print("---")

    by_group = {}
    for service in services:
        group = service.get("group_name") or "General"
        if group not in by_group:
            by_group[group] = []
        by_group[group].append(service)

    all_ok = 0
    all_total = 0

    for group in sorted(by_group.keys()):
        print(f"\n[{group}]")
        for service in by_group[group]:
            result = by_service.get(service["id"], {})
            status = result.get("status", StatusLevel.UNKNOWN.value)
            emoji = format_status_emoji(status)
            message = result.get("message", "No recent check")
            response = f" {result.get('response_time_ms')}ms" if result.get("response_time_ms") else ""

            print(f"  {emoji} {service['name']:30} {message}{response}")

            all_total += 1
            if status == StatusLevel.OK.value:
                all_ok += 1

    print(f"\n---")
    print(f"All systems operational. {all_ok}/{all_total} healthy.")
    print(f"\n{FOOTER}")

    return 0


def cmd_notify(args):
    """Send current dashboard via Telegram."""
    services = list_services(enabled_only=True)
    results = get_latest_results(limit=200)

    if not services:
        print("No services configured")
        return 1

    # Match latest result
    by_service = {}
    for r in results:
        service_id = r.get("service_id")
        if service_id not in by_service:
            by_service[service_id] = r

    # Build message
    message = "🏥 *Health Dashboard*\n"
    message += "─" * 40 + "\n\n"

    by_group = {}
    for service in services:
        group = service.get("group_name") or "General"
        if group not in by_group:
            by_group[group] = []
        by_group[group].append(service)

    for group in sorted(by_group.keys()):
        message += f"*[{group}]*\n"
        for service in by_group[group]:
            result = by_service.get(service["id"], {})
            emoji = format_status_emoji(result.get("status", StatusLevel.UNKNOWN.value))
            msg = result.get("message", "No check")
            message += f"  {emoji} {service['name']}: {msg}\n"

    message += "─" * 40 + "\n"

    if send_telegram_alert(message):
        print("Dashboard sent via Telegram")
    else:
        print("Failed to send Telegram alert. Check HEALTHCHECK_TELEGRAM_TOKEN and HEALTHCHECK_TELEGRAM_CHAT env vars")
        return 1

    print(FOOTER)
    return 0


def cmd_config(args):
    """Set configuration."""
    if args.set_token:
        os.environ["HEALTHCHECK_TELEGRAM_TOKEN"] = args.set_token
        print("Telegram bot token set")
    if args.set_chat:
        os.environ["HEALTHCHECK_TELEGRAM_CHAT"] = args.set_chat
        print("Telegram chat ID set")

    print(f"Token: {os.environ.get('HEALTHCHECK_TELEGRAM_TOKEN', '(not set)')[:20]}...")
    print(f"Chat: {os.environ.get('HEALTHCHECK_TELEGRAM_CHAT', '(not set)')}")
    print(FOOTER)
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="nex-healthcheck",
        description="Multi-Service Health Dashboard"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # check
    p = subparsers.add_parser("check", help="Run health checks")
    p.add_argument("--service", help="Check specific service")
    p.add_argument("--group", help="Check specific group")
    p.add_argument("--tag", help="Check services with tag")
    p.set_defaults(func=cmd_check)

    # add
    p = subparsers.add_parser("add", help="Add service to monitor")
    p.add_argument("--name", required=True, help="Service name")
    p.add_argument("--type", required=True, help="Check type (http, tcp, dns, ssl_cert, docker, systemd, ssh_cmd, ping, disk)")
    p.add_argument("--target", required=True, help="Target URL/host/container/path")
    p.add_argument("--port", type=int, help="Port (for TCP)")
    p.add_argument("--expected", help="Expected status/output")
    p.add_argument("--interval", type=int, help="Check interval in seconds")
    p.add_argument("--group", help="Service group")
    p.add_argument("--tag", help="Tags (comma-separated)")
    p.add_argument("--notes", help="Notes")
    p.add_argument("--ssh-host", help="SSH host for remote checks (user@host)")
    p.set_defaults(func=cmd_add)

    # list
    p = subparsers.add_parser("list", help="List services")
    p.set_defaults(func=cmd_list)

    # remove
    p = subparsers.add_parser("remove", help="Remove service")
    p.add_argument("--name", required=True, help="Service name")
    p.set_defaults(func=cmd_remove)

    # status
    p = subparsers.add_parser("status", help="Quick status")
    p.set_defaults(func=cmd_status)

    # history
    p = subparsers.add_parser("history", help="Check history")
    p.add_argument("--name", required=True, help="Service name")
    p.add_argument("--days", help="Number of days (default: 7)")
    p.set_defaults(func=cmd_history)

    # incidents
    p = subparsers.add_parser("incidents", help="Show incidents")
    p.add_argument("--all", action="store_true", help="Show all (not just active)")
    p.set_defaults(func=cmd_incidents)

    # uptime
    p = subparsers.add_parser("uptime", help="Uptime statistics")
    p.add_argument("--days", help="Number of days (default: 30)")
    p.set_defaults(func=cmd_uptime)

    # dashboard
    p = subparsers.add_parser("dashboard", help="Full dashboard")
    p.set_defaults(func=cmd_dashboard)

    # notify
    p = subparsers.add_parser("notify", help="Send dashboard via Telegram")
    p.set_defaults(func=cmd_notify)

    # config
    p = subparsers.add_parser("config", help="Set configuration")
    p.add_argument("--set-token", help="Set Telegram bot token")
    p.add_argument("--set-chat", help="Set Telegram chat ID")
    p.set_defaults(func=cmd_config)

    args = parser.parse_args()

    # Initialize database
    init_db()

    # Run command
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
