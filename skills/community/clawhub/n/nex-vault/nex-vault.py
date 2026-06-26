#!/usr/bin/env python3
"""
Nex Vault - Local Contract and Document Vault with Expiry Alerts
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sys
import argparse
import datetime as dt
from pathlib import Path

from lib.storage import (
    init_db, save_document, get_document, list_documents, update_document,
    search_documents, get_upcoming_alerts, mark_alert_sent, get_expiring_documents,
    get_document_stats, save_key_clause, get_key_clauses, export_documents,
    document_exists_by_hash
)
from lib.doc_parser import (
    extract_text, parse_dates, detect_auto_renewal, detect_termination_notice,
    extract_parties, extract_key_clauses, calculate_notice_deadline
)
from lib.alerter import (
    check_upcoming_alerts, send_telegram_alert, format_alert_message,
    run_daily_check, get_vault_summary
)
from lib.config import (
    DATA_DIR, VAULT_DIR, EXPORT_DIR, DOCUMENT_TYPES,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
)

FOOTER = "[Nex Vault by Nex AI | nex-ai.be]"


def cmd_add(args):
    """Add document to vault."""
    init_db()

    file_path = None
    file_content = None

    # Check if first argument is a file
    if Path(args.document).exists():
        file_path = Path(args.document).absolute()
        print(f"Extracting text from {file_path}...")
        file_content = extract_text(str(file_path))
    else:
        # Treat as document name/description
        print(f"Adding document: {args.document}")

    # Extract data from file if available
    end_date = args.end_date
    start_date = args.start_date
    renewal_date = args.renewal_date
    notice_days = args.notice_days
    auto_renewal = args.auto_renewal
    renewal_period = args.renewal_period

    if file_content:
        # Auto-detect dates from content
        dates = parse_dates(file_content)
        for d in dates:
            if d['type'] == 'start' and not start_date:
                start_date = d['date']
            elif d['type'] == 'end' and not end_date:
                end_date = d['date']
            elif d['type'] == 'renewal' and not renewal_date:
                renewal_date = d['date']

        # Detect auto-renewal
        if not auto_renewal:
            renewal_info = detect_auto_renewal(file_content)
            if renewal_info['has_auto_renewal']:
                auto_renewal = True
                renewal_period = renewal_info['renewal_period']

        # Detect termination notice
        if not notice_days:
            notice_info = detect_termination_notice(file_content)
            if notice_info['notice_days']:
                notice_days = notice_info['notice_days']

        # Extract parties
        if not args.party:
            parties = extract_parties(file_content)
            if parties:
                args.party = parties[0]

    # Save document
    doc_id = save_document(
        name=args.document if not file_path else file_path.name,
        doc_type=args.type.upper(),
        file_path=str(file_path) if file_path else None,
        party_name=args.party,
        party_contact=args.contact,
        start_date=start_date,
        end_date=end_date,
        renewal_date=renewal_date,
        termination_notice_days=notice_days,
        auto_renewal=auto_renewal,
        renewal_period=renewal_period,
        monthly_cost=args.monthly_cost,
        yearly_cost=args.yearly_cost,
        status=args.status,
        tags=args.tags,
        notes=args.notes,
        raw_text=file_content,
    )

    # Save key clauses if extracted
    if file_content:
        clauses = extract_key_clauses(file_content)
        for clause in clauses:
            save_key_clause(doc_id, clause['type'], clause['text'])

    print(f"Document added with ID: {doc_id}")
    print(f"  Name: {args.document}")
    print(f"  Type: {args.type}")
    if end_date:
        print(f"  Expires: {end_date}")
    if notice_days:
        deadline = calculate_notice_deadline(end_date, notice_days)
        print(f"  Notice deadline: {deadline}")
    print(FOOTER)


def cmd_show(args):
    """Show document details."""
    init_db()

    doc_data = get_document(args.id)
    if not doc_data:
        print(f"Document {args.id} not found.")
        return

    doc = doc_data['document']
    alerts = doc_data['alerts']
    clauses = doc_data['clauses']

    print(f"\n{'=' * 60}")
    print(f"DOCUMENT: {doc['name']}")
    print(f"{'=' * 60}\n")

    print(f"ID: {doc['id']}")
    print(f"Type: {doc['doc_type']}")
    print(f"Status: {doc['status']}")
    if doc['party_name']:
        print(f"Party: {doc['party_name']}")
    if doc['party_contact']:
        print(f"Contact: {doc['party_contact']}")

    print(f"\nDates:")
    if doc['start_date']:
        print(f"  Start: {doc['start_date']}")
    if doc['end_date']:
        print(f"  End: {doc['end_date']}")
    if doc['renewal_date']:
        print(f"  Renewal: {doc['renewal_date']}")
    if doc['termination_notice_date']:
        print(f"  Notice Due: {doc['termination_notice_date']}")
        if doc['termination_notice_days']:
            print(f"  Notice Period: {doc['termination_notice_days']} days")

    if doc['auto_renewal']:
        print(f"\nAuto-Renewal: Yes")
        if doc['renewal_period']:
            print(f"Renewal Period: {doc['renewal_period']}")

    print(f"\nCosts:")
    if doc['monthly_cost']:
        print(f"  Monthly: €{doc['monthly_cost']:.2f}")
    if doc['yearly_cost']:
        print(f"  Yearly: €{doc['yearly_cost']:.2f}")

    if doc['tags']:
        print(f"\nTags: {doc['tags']}")

    if doc['notes']:
        print(f"\nNotes: {doc['notes']}")

    if clauses:
        print(f"\nKey Clauses ({len(clauses)}):")
        for clause in clauses:
            print(f"  [{clause['clause_type']}] {clause['content'][:100]}...")

    if alerts:
        print(f"\nUpcoming Alerts ({len(alerts)}):")
        for alert in alerts:
            status = "SENT" if alert['sent'] else "PENDING"
            print(f"  [{status}] {alert['alert_date']}: {alert['message']}")

    print(f"\n{FOOTER}")


def cmd_list(args):
    """List documents."""
    init_db()

    if args.expiring:
        docs = get_expiring_documents(args.expiring if isinstance(args.expiring, int) else 90)
    else:
        docs = list_documents(
            doc_type=args.type,
            status=args.status,
            party_name=args.party,
            expiring_days=None
        )

    if not docs:
        print("No documents found.")
        print(FOOTER)
        return

    print(f"\n{'ID':<4} {'Name':<30} {'Type':<12} {'Party':<20} {'Expires':<12} {'Status':<10}")
    print("-" * 88)

    for doc in docs:
        expires = doc['end_date'][:10] if doc['end_date'] else "N/A"
        party = doc['party_name'][:20] if doc['party_name'] else "N/A"
        print(f"{doc['id']:<4} {doc['name'][:29]:<30} {doc['doc_type']:<12} {party:<20} {expires:<12} {doc['status']:<10}")

    print(f"\nTotal: {len(docs)} documents")
    print(FOOTER)


def cmd_search(args):
    """Search documents."""
    init_db()

    results = search_documents(args.query)
    if not results:
        print(f"No documents found matching '{args.query}'")
        print(FOOTER)
        return

    print(f"\nSearch Results for '{args.query}':\n")
    for doc in results:
        print(f"  [{doc['id']}] {doc['name']} ({doc['doc_type']}) - Status: {doc['status']}")
        if doc['end_date']:
            print(f"       Expires: {doc['end_date']}")

    print(f"\n{FOOTER}")


def cmd_expiring(args):
    """Show documents expiring soon."""
    init_db()

    days = args.days if args.days else 90
    docs = get_expiring_documents(days)

    if not docs:
        print(f"No documents expiring within {days} days.")
        print(FOOTER)
        return

    print(f"\nDocuments Expiring Within {days} Days:\n")
    today = dt.date.today()

    for doc in docs:
        end_date = dt.datetime.fromisoformat(doc['end_date']).date()
        days_left = (end_date - today).days
        print(f"  [{doc['id']}] {doc['name']}")
        print(f"       Type: {doc['doc_type']}")
        print(f"       Expires: {doc['end_date']} ({days_left} days)")
        if doc['party_name']:
            print(f"       Party: {doc['party_name']}")
        if doc['termination_notice_days']:
            notice_deadline = calculate_notice_deadline(doc['end_date'], doc['termination_notice_days'])
            notice_days_left = (dt.datetime.fromisoformat(notice_deadline).date() - today).days
            print(f"       Notice Due: {notice_deadline} ({notice_days_left} days)")
        print()

    print(FOOTER)


def cmd_alerts(args):
    """Manage alerts."""
    init_db()

    if args.action == 'list':
        alerts = get_upcoming_alerts(args.days if args.days else 90)

        if not alerts:
            print(f"No upcoming alerts in the next {args.days or 90} days.")
            print(FOOTER)
            return

        print(f"\nUpcoming Alerts (Next {args.days or 90} Days):\n")
        for alert in alerts:
            status = "SENT" if alert['sent'] else "PENDING"
            print(f"  [{alert['id']}] {alert['alert_date']} - {alert['alert_type'].upper()}")
            print(f"       Document: {alert['name']}")
            print(f"       Status: {status}")
            print(f"       Message: {alert['message']}")
            print()

        print(FOOTER)

    elif args.action == 'check':
        print("Running daily alert check...")
        alerts = check_upcoming_alerts(90)
        print(f"Found {len(alerts)} new alerts.")

        for alert in alerts:
            print(f"  - {alert['message']}")

        print(FOOTER)

    elif args.action == 'notify':
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("Telegram not configured. Run: nex-vault config set-telegram-token")
            print(FOOTER)
            return

        alerts = get_upcoming_alerts(90)
        sent = 0
        failed = 0

        for alert in alerts:
            if alert['sent']:
                continue

            formatted = format_alert_message(alert)
            if send_telegram_alert(formatted):
                mark_alert_sent(alert['id'])
                sent += 1
                print(f"Sent: {alert['name']}")
            else:
                failed += 1
                print(f"Failed: {alert['name']}")

        print(f"\nSent: {sent}, Failed: {failed}")
        print(FOOTER)

    elif args.action == 'mark-sent':
        mark_alert_sent(args.alert_id)
        print(f"Alert {args.alert_id} marked as sent.")
        print(FOOTER)


def cmd_scan(args):
    """Parse/re-parse a document."""
    init_db()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    print(f"Scanning {file_path}...")
    text = extract_text(str(file_path))

    dates = parse_dates(text)
    renewal = detect_auto_renewal(text)
    notice = detect_termination_notice(text)
    parties = extract_parties(text)
    clauses = extract_key_clauses(text)

    print(f"\nExtracted Data:\n")
    print(f"Dates Found: {len(dates)}")
    for d in dates:
        print(f"  {d['date']} ({d['type']}) - {d['context'][:50]}...")

    print(f"\nAuto-Renewal: {renewal['has_auto_renewal']}")
    if renewal['renewal_period']:
        print(f"  Period: {renewal['renewal_period']}")

    print(f"\nTermination Notice: {notice['notice_days']} days" if notice['notice_days'] else "None")

    print(f"\nParties: {', '.join(parties)}")

    print(f"\nKey Clauses: {len(clauses)}")
    for clause in clauses:
        print(f"  [{clause['type']}] {clause['text'][:60]}...")

    print(f"\n{FOOTER}")


def cmd_edit(args):
    """Edit document metadata."""
    init_db()

    updates = {}
    if args.end_date:
        updates['end_date'] = args.end_date
    if args.notice_days is not None:
        updates['termination_notice_days'] = args.notice_days
    if args.monthly_cost is not None:
        updates['monthly_cost'] = args.monthly_cost
    if args.party:
        updates['party_name'] = args.party
    if args.notes:
        updates['notes'] = args.notes
    if args.auto_renewal is not None:
        updates['auto_renewal'] = args.auto_renewal

    if not updates:
        print("No updates specified.")
        return

    success = update_document(args.id, **updates)
    if success:
        print(f"Document {args.id} updated.")
    else:
        print(f"Document {args.id} not found.")

    print(FOOTER)


def cmd_remove(args):
    """Remove document from vault."""
    init_db()

    # For now, just mark as removed (implement soft delete if needed)
    update_document(args.id, status='removed')
    print(f"Document {args.id} removed from tracking.")
    print(FOOTER)


def cmd_stats(args):
    """Show vault statistics."""
    init_db()

    stats = get_document_stats()

    print(f"\nVault Statistics:\n")
    print(f"Total Documents: {stats['total_documents']}")

    print(f"\nBy Type:")
    for dtype, count in stats['by_type'].items():
        print(f"  {dtype}: {count}")

    print(f"\nBy Status:")
    for status, count in stats['by_status'].items():
        print(f"  {status}: {count}")

    print(f"\nCosts (Active Documents):")
    print(f"  Monthly Total: €{stats['total_monthly_cost']:.2f}")
    print(f"  Yearly Total: €{stats['total_yearly_cost']:.2f}")

    if stats['top_parties']:
        print(f"\nTop Parties:")
        for party in stats['top_parties']:
            print(f"  {party['party_name']}: {party['count']} document(s)")

    print(f"\n{FOOTER}")


def cmd_export(args):
    """Export documents."""
    init_db()

    format_type = args.format.lower()
    data = export_documents(format_type)

    if not data:
        print("No data to export.")
        return

    output_file = args.output or f"vault_export.{format_type}"
    output_path = EXPORT_DIR / output_file

    with open(output_path, 'w') as f:
        f.write(data)

    print(f"Exported {format_type.upper()} to {output_path}")
    print(FOOTER)


def cmd_config(args):
    """Manage configuration."""
    init_db()

    if args.action == 'show':
        print(f"\nConfiguration:\n")
        print(f"Data Directory: {DATA_DIR}")
        print(f"Database: {DATA_DIR / 'vault.db'}")
        print(f"Telegram Bot Token: {'Configured' if TELEGRAM_BOT_TOKEN else 'Not configured'}")
        print(f"Telegram Chat ID: {TELEGRAM_CHAT_ID if TELEGRAM_CHAT_ID else 'Not configured'}")
        print(f"\n{FOOTER}")

    elif args.action == 'set-telegram-token':
        token = input("Enter Telegram Bot Token: ")
        import subprocess
        subprocess.run(['bash', '-c', f'echo "export NEX_VAULT_TELEGRAM_BOT_TOKEN={token}" >> ~/.bashrc'])
        print("Telegram Bot Token saved. Run 'source ~/.bashrc' to apply.")
        print(FOOTER)

    elif args.action == 'set-telegram-chat':
        chat_id = input("Enter Telegram Chat ID: ")
        import subprocess
        subprocess.run(['bash', '-c', f'echo "export NEX_VAULT_TELEGRAM_CHAT_ID={chat_id}" >> ~/.bashrc'])
        print("Telegram Chat ID saved. Run 'source ~/.bashrc' to apply.")
        print(FOOTER)

    elif args.action == 'test-telegram':
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("Telegram not configured.")
            return

        if send_telegram_alert("Test message from Nex Vault"):
            print("Telegram connection successful!")
        else:
            print("Telegram connection failed. Check your token and chat ID.")
        print(FOOTER)


def main():
    parser = argparse.ArgumentParser(description="Nex Vault - Local Contract and Document Vault")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # ADD command
    add_parser = subparsers.add_parser('add', help='Add document to vault')
    add_parser.add_argument('document', help='File path or document name')
    add_parser.add_argument('--type', default='OTHER', choices=DOCUMENT_TYPES + ['other'],
                            help='Document type')
    add_parser.add_argument('--party', help='Party name')
    add_parser.add_argument('--contact', help='Party contact info')
    add_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    add_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    add_parser.add_argument('--renewal-date', help='Renewal date (YYYY-MM-DD)')
    add_parser.add_argument('--notice-days', type=int, help='Termination notice days')
    add_parser.add_argument('--auto-renewal', action='store_true', help='Has auto-renewal')
    add_parser.add_argument('--renewal-period', help='Renewal period (e.g., "1 year")')
    add_parser.add_argument('--monthly-cost', type=float, default=0, help='Monthly cost')
    add_parser.add_argument('--yearly-cost', type=float, default=0, help='Yearly cost')
    add_parser.add_argument('--status', default='active', help='Status')
    add_parser.add_argument('--tags', help='Tags (comma-separated)')
    add_parser.add_argument('--notes', help='Notes')
    add_parser.set_defaults(func=cmd_add)

    # SHOW command
    show_parser = subparsers.add_parser('show', help='Show document details')
    show_parser.add_argument('id', type=int, help='Document ID')
    show_parser.set_defaults(func=cmd_show)

    # LIST command
    list_parser = subparsers.add_parser('list', help='List documents')
    list_parser.add_argument('--type', help='Filter by type')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--party', help='Filter by party name')
    list_parser.add_argument('--expiring', nargs='?', const=90, type=int, help='Show expiring within N days')
    list_parser.set_defaults(func=cmd_list)

    # SEARCH command
    search_parser = subparsers.add_parser('search', help='Search documents')
    search_parser.add_argument('query', help='Search query')
    search_parser.set_defaults(func=cmd_search)

    # EXPIRING command
    expiring_parser = subparsers.add_parser('expiring', help='Show expiring documents')
    expiring_parser.add_argument('--days', type=int, nargs='?', help='Days until expiry')
    expiring_parser.set_defaults(func=cmd_expiring)

    # ALERTS command
    alerts_parser = subparsers.add_parser('alerts', help='Manage alerts')
    alerts_parser.add_argument('action', choices=['list', 'check', 'notify', 'mark-sent'],
                               help='Alert action')
    alerts_parser.add_argument('--days', type=int, help='Days to check')
    alerts_parser.add_argument('alert_id', nargs='?', type=int, help='Alert ID (for mark-sent)')
    alerts_parser.set_defaults(func=cmd_alerts)

    # SCAN command
    scan_parser = subparsers.add_parser('scan', help='Parse document')
    scan_parser.add_argument('file', help='File to scan')
    scan_parser.set_defaults(func=cmd_scan)

    # EDIT command
    edit_parser = subparsers.add_parser('edit', help='Edit document')
    edit_parser.add_argument('id', type=int, help='Document ID')
    edit_parser.add_argument('--end-date', help='New end date')
    edit_parser.add_argument('--notice-days', type=int, help='Termination notice days')
    edit_parser.add_argument('--monthly-cost', type=float, help='Monthly cost')
    edit_parser.add_argument('--party', help='Party name')
    edit_parser.add_argument('--notes', help='Notes')
    edit_parser.add_argument('--auto-renewal', type=bool, help='Auto-renewal flag')
    edit_parser.set_defaults(func=cmd_edit)

    # REMOVE command
    remove_parser = subparsers.add_parser('remove', help='Remove document')
    remove_parser.add_argument('id', type=int, help='Document ID')
    remove_parser.set_defaults(func=cmd_remove)

    # STATS command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.set_defaults(func=cmd_stats)

    # EXPORT command
    export_parser = subparsers.add_parser('export', help='Export documents')
    export_parser.add_argument('format', choices=['csv', 'json'], help='Export format')
    export_parser.add_argument('--output', help='Output file')
    export_parser.set_defaults(func=cmd_export)

    # CONFIG command
    config_parser = subparsers.add_parser('config', help='Manage configuration')
    config_parser.add_argument('action', choices=['show', 'set-telegram-token', 'set-telegram-chat', 'test-telegram'],
                               help='Config action')
    config_parser.set_defaults(func=cmd_config)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
