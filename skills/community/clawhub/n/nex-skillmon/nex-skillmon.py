#!/usr/bin/env python3
# Nex SkillMon - Skill Health & Cost Monitor
# MIT-0 License - Copyright 2026 Nex AI

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from lib.config import DATA_DIR, LOG_PATH, CURRENCY, CURRENCY_SYMBOL
from lib.storage import get_storage
from lib.cost_tracker import CostTracker
from lib.scanner import Scanner

# Setup logging
LOG_PATH.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH / "nex-skillmon.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

FOOTER = "[Nex SkillMon by Nex AI | nex-ai.be]"


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    symbol = CURRENCY_SYMBOL.get(CURRENCY, CURRENCY)
    return f"{symbol}{amount:.2f}"


def format_timestamp(ts: str) -> str:
    """Format timestamp as human-readable."""
    if not ts:
        return "Never"

    dt = datetime.fromisoformat(ts)
    now = datetime.now()
    delta = now - dt

    if delta.days == 0:
        if delta.seconds < 60:
            return "Just now"
        elif delta.seconds < 3600:
            return f"{delta.seconds // 60} minutes ago"
        else:
            return f"{delta.seconds // 3600} hours ago"
    elif delta.days == 1:
        return "1 day ago"
    elif delta.days < 30:
        return f"{delta.days} days ago"
    else:
        return f"{delta.days // 30} months ago"


def cmd_scan(args):
    """Scan installed skills."""
    print("\nScanning installed skills...\n")
    scanner = Scanner()
    skills = scanner.scan_installed_skills()

    if not skills:
        print("No skills found.")
        return

    storage = get_storage()
    for skill in skills:
        skill_id = storage.save_skill(skill)
        print(f"  ✓ {skill['name']} v{skill.get('version', '?')} ({skill_id})")

    print(f"\nFound {len(skills)} skill(s).")
    print(FOOTER)


def cmd_list(args):
    """List skills."""
    storage = get_storage()

    status = args.status or None
    flags = args.flagged
    stale = args.stale

    skills = storage.list_skills(status=status, stale=stale, flagged=flags)

    if not skills:
        print("No skills found.")
        return

    print(f"\n{'ID':<4} {'Name':<25} {'Version':<10} {'Status':<12} {'Triggers':<10}")
    print("-" * 70)

    for skill in skills:
        skill_id = skill["id"]
        name = skill["name"][:25]
        version = skill.get("version", "?")[:10]
        status = skill.get("status", "?")[:12]
        triggers = skill.get("trigger_count", 0)

        print(f"{skill_id:<4} {name:<25} {version:<10} {status:<12} {triggers:<10}")

    print(f"\nTotal: {len(skills)} skill(s)")
    print(FOOTER)


def cmd_show(args):
    """Show skill details."""
    storage = get_storage()
    skill = storage.get_skill_by_name(args.skill)

    if not skill:
        print(f"Skill not found: {args.skill}")
        return

    print(f"\n{'Skill:':<20} {skill['name']}")
    print(f"{'ID:':<20} {skill['id']}")
    print(f"{'Version:':<20} {skill.get('version', 'unknown')}")
    print(f"{'Status:':<20} {skill.get('status', 'active')}")
    print(f"{'Author:':<20} {skill.get('author', '?')}")
    print(f"{'Homepage:':<20} {skill.get('homepage', '?')}")
    print(f"{'Description:':<20} {skill.get('description', '?')[:50]}...")
    print(f"\n{'Installed:':<20} {skill.get('install_date', '?')}")
    print(f"{'Last Updated:':<20} {skill.get('last_updated', '?')}")
    print(f"{'Last Triggered:':<20} {format_timestamp(skill.get('last_triggered'))}")
    print(f"{'Trigger Count:':<20} {skill.get('trigger_count', 0)}")
    print(f"{'Path:':<20} {skill.get('skill_path', '?')}")

    # Usage stats
    usage_logs = storage.get_skill_usage(skill["id"])
    if usage_logs:
        total_cost = sum(log.get("estimated_cost", 0) for log in usage_logs)
        avg_duration = sum(log.get("duration_ms", 0) for log in usage_logs) / len(
            usage_logs
        )
        success_count = sum(1 for log in usage_logs if log["success"])

        print(f"\n{'Total Cost:':<20} {format_currency(total_cost)}")
        print(f"{'Total Triggers:':<20} {len(usage_logs)}")
        print(f"{'Success Rate:':<20} {success_count / len(usage_logs) * 100:.1f}%")
        print(f"{'Avg Duration:':<20} {avg_duration:.0f}ms")

    # Health score
    health_score = storage.get_skill_health_score(skill["id"])
    print(f"{'Health Score:':<20} {health_score}/100")

    print(FOOTER)


def cmd_health(args):
    """Show health dashboard."""
    storage = get_storage()
    skills = storage.list_skills()
    cost_tracker = CostTracker()

    if not skills:
        print("No skills found.")
        return

    print("\nSkill Health Dashboard")
    print("-" * 90)
    print(
        f"{'Score':<7} {'Skill':<20} {'Triggers':<10} {'Cost/mo':<10} {'Last Used':<15} {'Status':<10}"
    )
    print("-" * 90)

    active = 0
    stale = 0
    flagged = 0

    for skill in skills:
        health = storage.get_skill_health_score(skill["id"])
        name = skill["name"][:20]

        # Determine status
        status = skill.get("status", "active")
        if status == "flagged":
            status = "FLAGGED"
            flagged += 1
        elif status == "active":
            # Check if stale
            if skill.get("last_triggered"):
                last_triggered = datetime.fromisoformat(skill["last_triggered"])
                days_unused = (datetime.now() - last_triggered).days
                if days_unused > 30:
                    status = "STALE"
                    stale += 1
                else:
                    status = "OK"
                    active += 1
            else:
                status = "STALE"
                stale += 1
        elif status == "disabled":
            status = "DISABLED"

        triggers = skill.get("trigger_count", 0)
        last_used = format_timestamp(skill.get("last_triggered"))

        # Get cost
        usage_logs = storage.get_skill_usage(skill["id"])
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_logs = [
            log for log in usage_logs
            if datetime.fromisoformat(log["triggered_at"]) >= month_start
        ]
        month_cost = sum(log.get("estimated_cost", 0) for log in month_logs)

        cost_str = format_currency(month_cost)

        print(
            f"{health:<7} {name:<20} {triggers:<10} {cost_str:<10} {last_used:<15} {status:<10}"
        )

    print("-" * 90)

    # Summary
    total_cost = sum(
        log.get("estimated_cost", 0)
        for skill in skills
        for log in storage.get_skill_usage(skill["id"])
    )

    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_logs = []
    for skill in skills:
        logs = storage.get_skill_usage(skill["id"])
        for log in logs:
            if datetime.fromisoformat(log["triggered_at"]) >= month_start:
                month_logs.append(log)

    month_cost = sum(log.get("estimated_cost", 0) for log in month_logs)

    budget_str = ""
    budget = storage.get_config("monthly_budget")
    if budget:
        budget_decimal = Decimal(budget)
        budget_str = f" | Budget: {format_currency(float(budget_decimal))}"
        if month_cost < float(budget_decimal):
            usage_pct = (month_cost / float(budget_decimal)) * 100
            budget_str += f" ({usage_pct:.0f}% used)"
        else:
            overage = month_cost - float(budget_decimal)
            budget_str += f" (EXCEEDED by {format_currency(overage)})"

    print(
        f"Total skills: {len(skills)} | Active: {active} | Stale: {stale} | Flagged: {flagged}"
    )
    print(f"This month: {format_currency(month_cost)}{budget_str}")
    print(FOOTER)


def cmd_check(args):
    """Run health checks."""
    print("\nRunning health checks...\n")
    scanner = Scanner()

    if args.skill:
        storage = get_storage()
        skill = storage.get_skill_by_name(args.skill)
        if not skill:
            print(f"Skill not found: {args.skill}")
            return
        skill_list = [skill]
    else:
        skill_list = scanner.scan_installed_skills()

    for skill in skill_list:
        print(f"Checking {skill['name']}...")

        # Check updates
        updates = scanner.check_for_updates(
            skill["name"], skill.get("version", "unknown")
        )
        if updates["update_available"]:
            print(f"  ! Update available: {updates['latest_version']}")

        # Check security
        security = scanner.check_security_flags(skill["name"])
        if security["flagged"]:
            print(f"  ✗ FLAGGED: {security['reason']}")

        # Check integrity
        integrity = scanner.verify_file_integrity(
            skill["skill_path"], skill.get("file_hash")
        )
        if not integrity["integrity_ok"]:
            print(f"  ✗ INTEGRITY CHANGED")

        print(f"  ✓ Check complete\n")

    print(FOOTER)


def cmd_security(args):
    """Security scan."""
    storage = get_storage()
    alerts = storage.get_security_alerts(unacknowledged=False)

    if not alerts:
        print("No security alerts.")
        return

    print(f"\n{'ID':<4} {'Skill':<20} {'Type':<20} {'Severity':<10} {'Date':<20}")
    print("-" * 80)

    for alert in alerts:
        alert_id = alert["id"]
        skill_name = alert.get("skill_name", "?")[:20]
        check_type = alert.get("check_type", "?")[:20]
        severity = alert.get("severity", "?")[:10]
        checked_at = alert.get("checked_at", "?")[:20]

        ack = " [ACK]" if alert["acknowledged"] else ""

        print(f"{alert_id:<4} {skill_name:<20} {check_type:<20} {severity:<10} {checked_at:<20}{ack}")

    print(f"\nTotal alerts: {len(alerts)}")
    print(FOOTER)


def cmd_cost(args):
    """Cost overview."""
    tracker = CostTracker()

    period = args.period or "monthly"
    if period == "monthly":
        since = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        today = datetime.now()
        since = today - timedelta(days=today.weekday())
    else:
        since = None

    aggregated = tracker.aggregate_costs(since=since)

    print(tracker.generate_cost_report(period))
    print(FOOTER)


def cmd_stale(args):
    """Show stale skills."""
    storage = get_storage()
    stale_skills = storage.get_stale_skills(days=30)

    if not stale_skills:
        print("No stale skills (all skills used in last 30 days).")
        return

    print(f"\n{'Name':<25} {'Last Used':<20} {'Days Unused':<15}")
    print("-" * 60)

    for skill in stale_skills:
        name = skill["name"][:25]
        last_used = format_timestamp(skill.get("last_triggered"))

        if skill.get("last_triggered"):
            last_triggered = datetime.fromisoformat(skill["last_triggered"])
            days_unused = (datetime.now() - last_triggered).days
        else:
            days_unused = 999

        print(f"{name:<25} {last_used:<20} {days_unused:<15}")

    print(f"\nTotal stale skills: {len(stale_skills)}")
    print(FOOTER)


def cmd_usage(args):
    """Usage statistics."""
    storage = get_storage()

    if args.skill:
        skill = storage.get_skill_by_name(args.skill)
        if not skill:
            print(f"Skill not found: {args.skill}")
            return
        skills = [skill]
    else:
        skills = storage.list_skills()

    print(f"\n{'Skill':<25} {'Triggers':<10} {'Tokens':<15} {'Cost':<12} {'Avg Duration':<15}")
    print("-" * 77)

    for skill in skills:
        usage_logs = storage.get_skill_usage(skill["id"])

        triggers = len(usage_logs)
        tokens = sum(log.get("tokens_used", 0) for log in usage_logs)
        cost = sum(log.get("estimated_cost", 0) for log in usage_logs)
        avg_duration = (
            sum(log.get("duration_ms", 0) for log in usage_logs) / triggers
            if triggers > 0
            else 0
        )

        name = skill["name"][:25]
        cost_str = format_currency(cost)

        print(
            f"{name:<25} {triggers:<10} {tokens:<15} {cost_str:<12} {avg_duration:.0f}ms"
        )

    print(FOOTER)


def cmd_updates(args):
    """Check for updates."""
    print("\nChecking for updates...\n")
    scanner = Scanner()
    skills = scanner.scan_installed_skills()

    updates_found = 0
    for skill in skills:
        result = scanner.check_for_updates(
            skill["name"], skill.get("version", "unknown")
        )
        if result["update_available"]:
            print(
                f"  {skill['name']}: {result['current_version']} → {result['latest_version']}"
            )
            updates_found += 1

    if updates_found == 0:
        print("  All skills are up-to-date.")
    else:
        print(f"\n{updates_found} update(s) available.")

    print(FOOTER)


def cmd_alerts(args):
    """Show alerts."""
    storage = get_storage()
    unack_only = not args.all
    alerts = storage.get_security_alerts(unacknowledged=unack_only)

    if not alerts:
        print("No security alerts." if unack_only else "No alerts.")
        return

    print(f"\n{'ID':<4} {'Skill':<20} {'Type':<20} {'Severity':<10} {'Details':<30}")
    print("-" * 90)

    for alert in alerts:
        alert_id = alert["id"]
        skill_name = alert.get("skill_name", "?")[:20]
        check_type = alert.get("check_type", "?")[:20]
        severity = alert.get("severity", "?")[:10]
        details = str(alert.get("details", ""))[:30]

        print(f"{alert_id:<4} {skill_name:<20} {check_type:<20} {severity:<10} {details:<30}")

    print(f"\nTotal: {len(alerts)} alert(s)")
    print(FOOTER)


def cmd_acknowledge(args):
    """Acknowledge an alert."""
    storage = get_storage()
    storage.acknowledge_alert(args.alert_id)
    print(f"Alert {args.alert_id} acknowledged.")
    print(FOOTER)


def cmd_budget(args):
    """Budget management."""
    storage = get_storage()

    if args.set:
        storage.set_config("monthly_budget", str(args.set))
        print(f"Monthly budget set to {format_currency(float(args.set))}")
    else:
        budget = storage.get_config("monthly_budget")
        if budget:
            tracker = CostTracker()
            alert = tracker.get_budget_alert(Decimal(budget))
            print(f"\nMonthly Budget: {format_currency(float(budget))}")
            print(f"Current Spend:  {format_currency(alert['current_cost'])}")
            print(f"Remaining:      {format_currency(alert['remaining'])}")
            print(f"Usage:          {alert['percent_of_budget']:.1f}%")
            if alert.get("exceeded"):
                print(f"EXCEEDED by:    {format_currency(alert['overage'])}")
        else:
            print("No budget set. Use --set to set a budget.")

    print(FOOTER)


def cmd_export(args):
    """Export report."""
    storage = get_storage()
    report = storage.export_report(period=args.period or "monthly", format=args.format or "json")

    if args.format == "json":
        # Convert non-serializable types
        def serialize(obj):
            if isinstance(obj, (datetime, Decimal)):
                return str(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        output = json.dumps(report, indent=2, default=serialize)
    else:
        # Markdown format
        output = f"# Nex SkillMon Report\n\n"
        output += f"**Period:** {report['period']}\n"
        output += f"**Generated:** {report['generated_at']}\n\n"

        output += f"## Skills ({len(report['skills'])})\n\n"
        output += "| Name | Version | Status | Triggers |\n"
        output += "|------|---------|--------|----------|\n"
        for skill in report["skills"]:
            output += f"| {skill['name']} | {skill.get('version', '?')} | {skill.get('status', '?')} | {skill.get('trigger_count', 0)} |\n"

        output += f"\n## Security Alerts ({len(report['security_alerts'])})\n\n"
        if report["security_alerts"]:
            output += "| Skill | Type | Severity |\n"
            output += "|-------|------|----------|\n"
            for alert in report["security_alerts"]:
                output += f"| {alert.get('skill_name', '?')} | {alert.get('check_type', '?')} | {alert.get('severity', '?')} |\n"

    print(output)
    print(FOOTER)


def cmd_config(args):
    """Configuration management."""
    storage = get_storage()

    if args.set and args.value:
        storage.set_config(args.set, args.value)
        print(f"Config {args.set} = {args.value}")
    else:
        print("\nConfiguration:")
        print(f"  SKILLS_BASE_DIR={storage.get_config('SKILLS_BASE_DIR', 'default')}")
        print(f"  monthly_budget={storage.get_config('monthly_budget', 'not set')}")
        print(f"  CURRENCY={CURRENCY}")

    print(FOOTER)


def main():
    """Main entry point."""
    # Ensure database is initialized
    storage = get_storage()
    storage.init_db()

    parser = argparse.ArgumentParser(
        description="Nex SkillMon - Skill Health & Cost Monitor",
        epilog=FOOTER,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # scan
    subparsers.add_parser("scan", help="Scan installed skills")

    # list
    list_parser = subparsers.add_parser("list", help="List skills")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--stale", action="store_true", help="Show stale skills only")
    list_parser.add_argument("--flagged", action="store_true", help="Show flagged skills only")

    # show
    show_parser = subparsers.add_parser("show", help="Show skill details")
    show_parser.add_argument("skill", help="Skill name")

    # health
    subparsers.add_parser("health", help="Health dashboard")

    # check
    check_parser = subparsers.add_parser("check", help="Run health checks")
    check_parser.add_argument("--skill", help="Specific skill to check")

    # security
    subparsers.add_parser("security", help="Security scan")

    # cost
    cost_parser = subparsers.add_parser("cost", help="Cost overview")
    cost_parser.add_argument("--period", choices=["daily", "weekly", "monthly"], help="Time period")

    # stale
    subparsers.add_parser("stale", help="Show stale skills")

    # usage
    usage_parser = subparsers.add_parser("usage", help="Usage statistics")
    usage_parser.add_argument("--skill", help="Specific skill")

    # updates
    subparsers.add_parser("updates", help="Check for updates")

    # alerts
    alerts_parser = subparsers.add_parser("alerts", help="Show alerts")
    alerts_parser.add_argument("--all", action="store_true", help="Show all alerts (not just unacknowledged)")

    # acknowledge
    ack_parser = subparsers.add_parser("acknowledge", help="Acknowledge alert")
    ack_parser.add_argument("alert_id", type=int, help="Alert ID")

    # budget
    budget_parser = subparsers.add_parser("budget", help="Budget management")
    budget_parser.add_argument("--set", type=float, help="Set monthly budget")

    # export
    export_parser = subparsers.add_parser("export", help="Export report")
    export_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    export_parser.add_argument("--period", default="monthly")

    # config
    config_parser = subparsers.add_parser("config", help="Configuration")
    config_parser.add_argument("--set", help="Config key")
    config_parser.add_argument("--value", help="Config value")

    args = parser.parse_args()

    # Route commands
    commands = {
        "scan": cmd_scan,
        "list": cmd_list,
        "show": cmd_show,
        "health": cmd_health,
        "check": cmd_check,
        "security": cmd_security,
        "cost": cmd_cost,
        "stale": cmd_stale,
        "usage": cmd_usage,
        "updates": cmd_updates,
        "alerts": cmd_alerts,
        "acknowledge": cmd_acknowledge,
        "budget": cmd_budget,
        "export": cmd_export,
        "config": cmd_config,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
