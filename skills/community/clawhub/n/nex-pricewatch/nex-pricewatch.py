#!/usr/bin/env python3
"""
Nex PriceWatch - Competitive Price Monitor for SMEs/Agencies
Track competitor and supplier pricing with automatic alerts
Copyright 2026 Nex AI (Kevin Blancaflor)
MIT-0 License
"""

import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

from lib.config import DATA_DIR, CHECK_INTERVAL_HOURS
from lib.storage import (
    init_db, save_target, get_target, list_targets, update_target,
    delete_target, get_price_history, get_price_stats, get_all_changes,
    search_targets, export_history, get_target_by_id
)
from lib.scraper import scrape_price, check_all_targets
from lib.alerter import detect_changes, format_price_alert, format_price_dashboard, send_alerts

FOOTER = "[Nex PriceWatch by Nex AI | nex-ai.be]"


def cmd_add(args):
    """Add a new price target."""
    print(f"Adding price target: {args.name}")

    if not args.url or not args.selector or not args.selector_type:
        print("ERROR: --url, --selector, and --selector-type are required", file=sys.stderr)
        return False

    try:
        target_id = save_target(
            name=args.name,
            url=args.url,
            selector_type=args.selector_type,
            selector=args.selector,
            competitor_name=args.competitor,
            type_=args.type,
            currency=args.currency,
            check_interval_hours=args.interval,
            tags=args.tags,
            notes=args.notes
        )
        print(f"✓ Target added with ID {target_id}")
        print(f"  Name: {args.name}")
        print(f"  URL: {args.url}")
        print(f"  Type: {args.type}")
        print(f"  Selector: {args.selector}")
        print()
        print(FOOTER)
        return True
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return False


def cmd_check(args):
    """Check prices for targets."""
    targets = list_targets(enabled_only=True)

    if not targets:
        print("No targets configured. Add targets with: nex-pricewatch add ...", file=sys.stderr)
        return False

    # Filter by name if specified
    if args.name:
        targets = [t for t in targets if args.name.lower() in t['name'].lower()]
        if not targets:
            print(f"No targets matching: {args.name}", file=sys.stderr)
            return False

    print(f"Checking prices for {len(targets)} target(s)...")
    print()

    results = []
    for target in targets:
        print(f"  Checking: {target['name']}...", end=" ", flush=True)
        result = scrape_price(target['url'], target['selector_type'], target['selector'])

        if result['success']:
            print(f"✓ {result['price']} {result['currency']}")
            # Save to database
            from lib.storage import save_price, detect_price_change
            price = result['price']
            raw_text = result['raw_text']
            save_price(target['id'], price, raw_text)

            # Detect change
            change_info = detect_price_change(target['id'], price)
            result['target_id'] = target['id']
            result['target'] = target
            result['change_info'] = change_info
            results.append(result)
        else:
            print(f"✗ {result['error']}")

    print()

    # Detect and display alerts
    if args.alerts:
        alerts = detect_changes(results)
        if alerts:
            print(f"🚨 ALERTS ({len(alerts)})")
            print("-" * 70)
            for alert in alerts:
                print(f"  {alert['message']}")
            print()

            if args.telegram:
                sent = send_alerts(alerts)
                print(f"Sent {sent} alerts via Telegram")
        else:
            print("No price alerts to report")

    print(FOOTER)
    return True


def cmd_list(args):
    """List all price targets."""
    targets = list_targets()

    if not targets:
        print("No targets configured. Add targets with: nex-pricewatch add ...", file=sys.stderr)
        return False

    print("=" * 90)
    print(f"{'Name':<30} {'Competitor':<20} {'Type':<12} {'Current':<15} {'Status':<8}")
    print("=" * 90)

    for target in targets:
        current = target.get('current_price')
        if current:
            currency = target.get('currency', 'EUR')
            current_str = f"{current:.2f} {currency}"
        else:
            current_str = "N/A"

        status = "✓ ON" if target.get('enabled') else "✗ OFF"

        print(f"{target['name']:<30} {(target.get('competitor_name') or '-'):<20} {target['type']:<12} {current_str:<15} {status:<8}")

    print("=" * 90)
    print(f"Total: {len(targets)} targets")
    print()
    print(FOOTER)
    return True


def cmd_show(args):
    """Show target details with price history."""
    target = get_target(args.name)

    if not target:
        print(f"Target not found: {args.name}", file=sys.stderr)
        return False

    print(f"Target: {target['name']}")
    print(f"URL: {target['url']}")
    print(f"Competitor: {target.get('competitor_name', 'N/A')}")
    print(f"Type: {target['type']}")
    print(f"Selector: [{target['selector_type']}] {target['selector']}")
    print(f"Currency: {target.get('currency', 'EUR')}")
    print(f"Current Price: {target.get('current_price', 'N/A')}")
    print(f"Last Checked: {target.get('last_checked', 'Never')}")
    print(f"Status: {'ENABLED' if target['enabled'] else 'DISABLED'}")
    print()

    # Price history
    history = get_price_history(target['id'], limit=10)
    if history:
        print(f"Price History (last {len(history)} checks):")
        print("-" * 50)
        for h in history:
            print(f"  {h['checked_at']}: {h['price']} {target.get('currency', 'EUR')}")
    else:
        print("No price history yet.")

    print()

    # Stats
    stats = get_price_stats(target['id'])
    if stats['count'] > 0:
        print(f"Statistics:")
        print(f"  Total checks: {stats['count']}")
        print(f"  Min: {stats['min']}")
        print(f"  Max: {stats['max']}")
        print(f"  Avg: {stats['avg']}")
        print(f"  Trend: {stats['trend'].upper()}")
    else:
        print("No statistics yet.")

    print()
    print(FOOTER)
    return True


def cmd_history(args):
    """Show price history for a target."""
    target = get_target(args.name)

    if not target:
        print(f"Target not found: {args.name}", file=sys.stderr)
        return False

    since = None
    if args.since:
        try:
            since = datetime.fromisoformat(args.since)
        except:
            print(f"Invalid date format: {args.since}. Use YYYY-MM-DD", file=sys.stderr)
            return False

    history = get_price_history(target['id'], since=since, limit=args.limit)

    if not history:
        print(f"No price history for {target['name']}", file=sys.stderr)
        return False

    print(f"Price History for {target['name']}")
    print(f"{'Date':<20} {'Price':<15} {'Raw Text':<40}")
    print("-" * 75)

    for h in history:
        raw = h.get('raw_text', '')[:40].replace('\n', ' ')
        print(f"{h['checked_at']:<20} {h['price']:<15} {raw:<40}")

    print()
    print(FOOTER)
    return True


def cmd_changes(args):
    """Show recent price changes."""
    since = None
    if args.since:
        try:
            since = datetime.fromisoformat(args.since)
        except:
            since = datetime.now() - timedelta(days=7)

    changes = get_all_changes(since=since)

    if not changes:
        print("No price changes found")
        return True

    print(f"Recent Price Changes ({len(changes)} total)")
    print("=" * 90)

    for change in changes:
        alert_type = change.get('alert_type', '').upper()
        target_name = change.get('target_name', 'Unknown')
        old_price = change.get('old_price', 'N/A')
        new_price = change.get('new_price', 'N/A')
        change_pct = change.get('change_pct', 0)

        icon = "⬆️" if alert_type == "INCREASE" else "⬇️" if alert_type == "DECREASE" else "🔔"
        print(f"{icon} {target_name}: {old_price} → {new_price} ({change_pct:+.1f}%)")

    print()
    print(FOOTER)
    return True


def cmd_compare(args):
    """Compare pricing side-by-side."""
    targets = list_targets()

    if not targets:
        print("No targets configured", file=sys.stderr)
        return False

    # Group by competitor
    grouped = {}
    for target in targets:
        competitor = target.get('competitor_name', 'Unknown')
        if competitor not in grouped:
            grouped[competitor] = []
        grouped[competitor].append(target)

    print("=" * 100)
    print("COMPETITIVE PRICE COMPARISON")
    print("=" * 100)

    for competitor in sorted(grouped.keys()):
        items = grouped[competitor]
        print(f"\n{competitor}:")
        for item in items:
            price = item.get('current_price')
            if price:
                print(f"  • {item['name']}: {price} {item.get('currency', 'EUR')}")

    print("\n" + "=" * 100)
    print(FOOTER)
    return True


def cmd_dashboard(args):
    """Show full price monitoring dashboard."""
    targets = list_targets(enabled_only=True)

    if not targets:
        print("No enabled targets", file=sys.stderr)
        return False

    print()

    # Fetch latest prices
    results = []
    for target in targets:
        result = {
            'target_id': target['id'],
            'target': target,
            'success': bool(target.get('current_price')),
            'price': target.get('current_price'),
            'currency': target.get('currency', 'EUR'),
        }
        results.append(result)

    print(format_price_dashboard(results))
    print()


def cmd_remove(args):
    """Remove a price target."""
    target = get_target(args.name)

    if not target:
        print(f"Target not found: {args.name}", file=sys.stderr)
        return False

    if not args.force:
        response = input(f"Delete target '{args.name}'? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled")
            return False

    delete_target(args.name)
    print(f"✓ Target removed: {args.name}")
    print()
    print(FOOTER)
    return True


def cmd_export(args):
    """Export price history."""
    target = get_target(args.name)

    if not target:
        print(f"Target not found: {args.name}", file=sys.stderr)
        return False

    format_ = args.format.lower()
    if format_ not in ['json', 'csv']:
        print(f"Unsupported format: {format_}", file=sys.stderr)
        return False

    export = export_history(target['id'], format_=format_)

    if args.output:
        path = Path(args.output)
        with open(path, 'w') as f:
            f.write(export)
        print(f"✓ Exported to {path}")
    else:
        print(export)

    return True


def cmd_stats(args):
    """Show statistics."""
    targets = list_targets()

    if not targets:
        print("No targets configured", file=sys.stderr)
        return False

    total_targets = len(targets)
    enabled_targets = sum(1 for t in targets if t['enabled'])

    # Find biggest changes
    changes = get_all_changes(since=datetime.now() - timedelta(days=30))
    biggest_increase = max(changes, key=lambda x: x.get('change_pct', 0)) if changes else None
    biggest_decrease = min(changes, key=lambda x: x.get('change_pct', 0)) if changes else None

    print("=" * 70)
    print("STATISTICS")
    print("=" * 70)
    print(f"Total targets: {total_targets}")
    print(f"Enabled targets: {enabled_targets}")
    print(f"Recent changes (30 days): {len(changes)}")

    if biggest_increase:
        print(f"\nBiggest price increase:")
        print(f"  {biggest_increase['target_name']}: {biggest_increase['change_pct']:+.1f}%")

    if biggest_decrease:
        print(f"\nBiggest price decrease:")
        print(f"  {biggest_decrease['target_name']}: {biggest_decrease['change_pct']:+.1f}%")

    print("\n" + "=" * 70)
    print(FOOTER)
    return True


def cmd_config(args):
    """Show configuration."""
    print("=" * 70)
    print("CONFIGURATION")
    print("=" * 70)
    print(f"Data directory: {DATA_DIR}")
    print(f"Check interval: {CHECK_INTERVAL_HOURS} hours")
    print(f"Price increase alert threshold: {5}%")
    print(f"Price decrease alert threshold: {10}%")
    print("=" * 70)
    print(FOOTER)
    return True


def main():
    """Main entry point."""
    # Initialize database
    init_db()

    parser = argparse.ArgumentParser(
        description="Nex PriceWatch - Competitive Price Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=FOOTER
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # add command
    add_parser = subparsers.add_parser('add', help='Add price target')
    add_parser.add_argument('--name', required=True, help='Target name')
    add_parser.add_argument('--url', required=True, help='URL to monitor')
    add_parser.add_argument('--competitor', help='Competitor name')
    add_parser.add_argument('--type', default='competitor', choices=['competitor', 'supplier', 'market'], help='Type')
    add_parser.add_argument('--selector-type', required=True, choices=['css', 'xpath', 'regex', 'text'], help='Selector type')
    add_parser.add_argument('--selector', required=True, help='CSS/XPath selector or pattern')
    add_parser.add_argument('--currency', default='EUR', help='Currency code')
    add_parser.add_argument('--interval', type=int, default=24, help='Check interval in hours')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    add_parser.add_argument('--notes', help='Notes')
    add_parser.set_defaults(func=cmd_add)

    # check command
    check_parser = subparsers.add_parser('check', help='Check prices')
    check_parser.add_argument('--name', help='Check specific target')
    check_parser.add_argument('--alerts', action='store_true', help='Show alerts')
    check_parser.add_argument('--telegram', action='store_true', help='Send to Telegram')
    check_parser.set_defaults(func=cmd_check)

    # list command
    list_parser = subparsers.add_parser('list', help='List targets')
    list_parser.set_defaults(func=cmd_list)

    # show command
    show_parser = subparsers.add_parser('show', help='Show target details')
    show_parser.add_argument('name', help='Target name')
    show_parser.set_defaults(func=cmd_show)

    # history command
    history_parser = subparsers.add_parser('history', help='Show price history')
    history_parser.add_argument('name', help='Target name')
    history_parser.add_argument('--since', help='Since date (YYYY-MM-DD)')
    history_parser.add_argument('--limit', type=int, default=50, help='Limit results')
    history_parser.set_defaults(func=cmd_history)

    # changes command
    changes_parser = subparsers.add_parser('changes', help='Show recent changes')
    changes_parser.add_argument('--since', help='Since date (YYYY-MM-DD)')
    changes_parser.set_defaults(func=cmd_changes)

    # compare command
    compare_parser = subparsers.add_parser('compare', help='Compare pricing')
    compare_parser.set_defaults(func=cmd_compare)

    # dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Show dashboard')
    dashboard_parser.set_defaults(func=cmd_dashboard)

    # remove command
    remove_parser = subparsers.add_parser('remove', help='Remove target')
    remove_parser.add_argument('name', help='Target name')
    remove_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    remove_parser.set_defaults(func=cmd_remove)

    # export command
    export_parser = subparsers.add_parser('export', help='Export history')
    export_parser.add_argument('name', help='Target name')
    export_parser.add_argument('--format', default='json', choices=['json', 'csv'], help='Export format')
    export_parser.add_argument('--output', help='Output file')
    export_parser.set_defaults(func=cmd_export)

    # stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.set_defaults(func=cmd_stats)

    # config command
    config_parser = subparsers.add_parser('config', help='Show config')
    config_parser.set_defaults(func=cmd_config)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if hasattr(args, 'func'):
        try:
            success = args.func(args)
            return 0 if success else 1
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

    return 1


if __name__ == '__main__':
    sys.exit(main())
