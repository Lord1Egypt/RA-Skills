#!/usr/bin/env python3
"""
Nex Deliverables - Client Deliverable Tracker
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Track deliverables for agency clients and freelance projects.
All data stored locally at ~/.nex-deliverables
"""
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from config import DATA_DIR, DB_PATH, STATUSES, DELIVERABLE_TYPES, PRIORITY_LEVELS, DATE_FORMAT
from storage import (
    init_db, save_client, get_client, get_client_by_name, list_clients,
    save_deliverable, get_deliverable, list_deliverables, update_deliverable_status,
    search_deliverables, get_client_summary, get_overdue_deliverables, get_workload_summary,
    generate_status_email, export_deliverables, get_status_history, add_milestone,
    complete_milestone, get_milestones
)

FOOTER = "[Nex Deliverables by Nex AI | nex-ai.be]"


def ensure_db():
    """Ensure database exists"""
    if not DB_PATH.exists():
        init_db()


def cmd_add(args):
    """Add a new deliverable"""
    ensure_db()

    # Get or create client
    client = get_client_by_name(args.client)
    if not client:
        client_id = save_client(args.client)
        print(f"Created new client: {args.client}")
    else:
        client_id = client['id']

    # Parse deadline if provided
    deadline = args.deadline
    if deadline and deadline.lower() == "today":
        deadline = datetime.now().strftime(DATE_FORMAT)
    elif deadline and deadline.lower() in ["tomorrow", "next day"]:
        deadline = (datetime.now() + timedelta(days=1)).strftime(DATE_FORMAT)
    elif deadline and deadline.lower() == "next week":
        deadline = (datetime.now() + timedelta(days=7)).strftime(DATE_FORMAT)
    elif deadline and deadline.lower() == "next friday":
        days_ahead = 4 - datetime.now().weekday()  # Friday = 4
        if days_ahead <= 0:
            days_ahead += 7
        deadline = (datetime.now() + timedelta(days=days_ahead)).strftime(DATE_FORMAT)

    deliv_id = save_deliverable(
        client_id=client_id,
        title=args.title,
        type=args.type,
        deadline=deadline,
        description=args.description,
        priority=args.priority,
        assigned_to=args.assigned_to,
        estimated_hours=args.estimated_hours
    )

    print(f"\nDeliverable added (ID: {deliv_id})")
    print(f"  Client: {args.client}")
    print(f"  Title: {args.title}")
    print(f"  Type: {args.type}")
    if deadline:
        print(f"  Deadline: {deadline}")
    print(f"  Priority: {args.priority}")
    print(f"\n{FOOTER}")


def cmd_client(args):
    """Manage clients"""
    ensure_db()

    if args.action == "add":
        client_id = save_client(
            name=args.name,
            contact_name=args.contact_name,
            email=args.email,
            phone=args.phone,
            retainer_amount=args.retainer_amount,
            retainer_tier=args.retainer_tier,
            status=args.status,
            notes=args.notes
        )
        print(f"Client saved: {args.name} (ID: {client_id})")

    elif args.action == "show":
        client = get_client_by_name(args.name)
        if not client:
            print(f"Client not found: {args.name}")
            return

        print(f"\n{client['name']}")
        print("=" * 60)
        if client['contact_name']:
            print(f"Contact: {client['contact_name']}")
        if client['email']:
            print(f"Email: {client['email']}")
        if client['phone']:
            print(f"Phone: {client['phone']}")
        if client['retainer_tier']:
            print(f"Tier: {client['retainer_tier']}")
        if client['retainer_amount']:
            print(f"Retainer: ${client['retainer_amount']}")
        print(f"Status: {client['status']}")

        # Show deliverables
        deliverables = list_deliverables(client_id=client['id'])
        summary = get_client_summary(client['id'])

        print(f"\nDeliverables Summary:")
        print(f"  Total: {summary['total']}")
        print(f"  In Progress: {summary['by_status'].get('in_progress', 0)}")
        print(f"  Delivered: {summary['by_status'].get('delivered', 0)}")
        print(f"  Approved: {summary['by_status'].get('approved', 0)}")
        print(f"  Overdue: {summary['overdue']}")

        if deliverables:
            print(f"\nAll Deliverables:")
            for d in deliverables:
                deadline = d['deadline'] or "—"
                print(f"  [{d['id']}] {d['title']} ({d['type']}) - {d['status']} - Due: {deadline}")

        print(f"\n{FOOTER}")

    elif args.action == "list":
        clients = list_clients(status=args.status)
        if not clients:
            print("No clients found")
            return

        print(f"\nClients ({len(clients)})")
        print("=" * 60)
        for c in clients:
            status_display = f" [{c['status']}]" if c['status'] != "active" else ""
            print(f"  {c['name']}{status_display}")
            if c['email']:
                print(f"    Email: {c['email']}")
            summary = get_client_summary(c['id'])
            print(f"    Deliverables: {summary['total']} (open: {summary['by_status'].get('in_progress', 0)}, overdue: {summary['overdue']})")

        print(f"\n{FOOTER}")


def cmd_list(args):
    """List deliverables with filters"""
    ensure_db()

    filters = {}
    if args.client:
        client = get_client_by_name(args.client)
        if not client:
            print(f"Client not found: {args.client}")
            return
        filters['client_id'] = client['id']

    if args.status:
        filters['status'] = args.status

    if args.type:
        filters['type'] = args.type

    if args.priority:
        filters['priority'] = args.priority

    if args.overdue:
        filters['overdue'] = True

    deliverables = list_deliverables(**filters, limit=200)

    if not deliverables:
        print("No deliverables found")
        return

    print(f"\nDeliverables ({len(deliverables)})")
    print("=" * 100)

    for d in deliverables:
        deadline = d['deadline'] or "—"
        status_color = {"planned": "⚪", "in_progress": "🟡", "review": "🟠",
                       "delivered": "🟢", "approved": "✅", "rejected": "❌"}.get(d['status'], "•")

        client_obj = get_client(d['client_id'])
        client_name = client_obj['name'] if client_obj else "?"

        print(f"{status_color} [{d['id']}] {d['title']}")
        print(f"   Client: {client_name} | Type: {d['type']} | Priority: {d['priority']}")
        print(f"   Status: {d['status']} | Deadline: {deadline}")

    print(f"\n{FOOTER}")


def cmd_show(args):
    """Show detailed deliverable information"""
    ensure_db()

    # Try to get by ID first, then search by title
    deliv = None
    if args.deliverable.isdigit():
        deliv = get_deliverable(int(args.deliverable))
    else:
        results = search_deliverables(args.deliverable)
        if results:
            deliv = results[0]

    if not deliv:
        print(f"Deliverable not found: {args.deliverable}")
        return

    client = get_client(deliv['client_id'])

    print(f"\n{deliv['title']}")
    print("=" * 60)
    print(f"ID: {deliv['id']}")
    print(f"Client: {client['name']}")
    print(f"Type: {deliv['type']}")
    print(f"Status: {deliv['status']}")
    print(f"Priority: {deliv['priority']}")

    if deliv['description']:
        print(f"\nDescription:\n{deliv['description']}")

    print(f"\nDates:")
    print(f"  Created: {deliv['created_at']}")
    if deliv['deadline']:
        print(f"  Deadline: {deliv['deadline']}")
    if deliv['started_at']:
        print(f"  Started: {deliv['started_at']}")
    if deliv['delivered_at']:
        print(f"  Delivered: {deliv['delivered_at']}")
    if deliv['approved_at']:
        print(f"  Approved: {deliv['approved_at']}")

    if deliv['assigned_to']:
        print(f"\nAssigned to: {deliv['assigned_to']}")

    if deliv['estimated_hours']:
        print(f"Estimated: {deliv['estimated_hours']} hours")
    if deliv['actual_hours']:
        print(f"Actual: {deliv['actual_hours']} hours")

    # Show milestones
    milestones = get_milestones(deliv['id'])
    if milestones:
        print(f"\nMilestones ({len(milestones)}):")
        for m in milestones:
            status = "✓" if m['completed'] else "○"
            print(f"  {status} {m['title']}")

    # Show status history
    history = get_status_history(deliv['id'])
    if history:
        print(f"\nStatus History:")
        for h in history[-5:]:  # Last 5 changes
            print(f"  {h['created_at']}: {h['old_status']} → {h['new_status']}")
            if h['message']:
                print(f"    {h['message']}")

    if deliv['notes']:
        print(f"\nNotes:\n{deliv['notes']}")

    print(f"\n{FOOTER}")


def cmd_status(args):
    """Update deliverable status"""
    ensure_db()

    deliv_id = int(args.deliverable_id)
    deliv = get_deliverable(deliv_id)

    if not deliv:
        print(f"Deliverable not found: {deliv_id}")
        return

    if args.status not in STATUSES:
        print(f"Invalid status. Use one of: {', '.join(STATUSES)}")
        return

    success = update_deliverable_status(deliv_id, args.status, args.message)

    if success:
        client = get_client(deliv['client_id'])
        print(f"\nStatus updated: {deliv['title']}")
        print(f"Client: {client['name']}")
        print(f"Old status: {deliv['status']}")
        print(f"New status: {args.status}")
        if args.message:
            print(f"Message: {args.message}")
    else:
        print("Failed to update status")

    print(f"\n{FOOTER}")


def cmd_mark(args):
    """Mark deliverable by title (convenience command)"""
    ensure_db()

    results = search_deliverables(args.title)
    if not results:
        print(f"Deliverable not found: {args.title}")
        return

    deliv = results[0]
    success = update_deliverable_status(deliv['id'], args.status)

    if success:
        client = get_client(deliv['client_id'])
        print(f"\n✓ Marked as {args.status}: {deliv['title']}")
        print(f"  Client: {client['name']}")
    else:
        print(f"Failed to update")

    print(f"\n{FOOTER}")


def cmd_overdue(args):
    """Show all overdue deliverables"""
    ensure_db()

    overdue = get_overdue_deliverables()

    if not overdue:
        print("No overdue deliverables! ✓")
        print(f"\n{FOOTER}")
        return

    print(f"\nOverdue Deliverables ({len(overdue)})")
    print("=" * 100)

    for d in overdue:
        days_late = (datetime.now() - datetime.strptime(d['deadline'], DATE_FORMAT)).days
        print(f"⚠️  [{d['id']}] {d['title']}")
        print(f"   Client: {d['client_name']} | Type: {d['type']}")
        print(f"   Was due: {d['deadline']} ({days_late} days ago)")
        print(f"   Status: {d['status']}")

    print(f"\n{FOOTER}")


def cmd_search(args):
    """Search deliverables"""
    ensure_db()

    results = search_deliverables(args.query)

    if not results:
        print(f"No results for: {args.query}")
        print(f"\n{FOOTER}")
        return

    print(f"\nSearch Results for '{args.query}' ({len(results)})")
    print("=" * 100)

    for d in results:
        client = get_client(d['client_id'])
        print(f"[{d['id']}] {d['title']}")
        print(f"  Client: {client['name']} | Type: {d['type']} | Status: {d['status']}")
        print(f"  Deadline: {d['deadline'] or '—'}")

    print(f"\n{FOOTER}")


def cmd_workload(args):
    """Show workload summary"""
    ensure_db()

    summary = get_workload_summary()

    print(f"\nWorkload Summary")
    print("=" * 60)
    print(f"Total Deliverables: {summary['total_deliverables']}")
    print(f"Active Clients: {summary['clients_active']}")
    print(f"Overdue: {summary['overdue']}")

    print(f"\nBy Status:")
    for status in STATUSES:
        count = summary['by_status'].get(status, 0)
        if count > 0:
            print(f"  {status}: {count}")

    print(f"\nBy Priority:")
    for priority, count in sorted(summary['by_priority'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {priority}: {count}")

    print(f"\nBy Type (top 10):")
    for type_name, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {type_name}: {count}")

    print(f"\n{FOOTER}")


def cmd_email(args):
    """Generate status update email for a client"""
    ensure_db()

    client = get_client_by_name(args.client)
    if not client:
        print(f"Client not found: {args.client}")
        return

    email = generate_status_email(client['id'])
    print(email)


def cmd_export(args):
    """Export deliverables"""
    ensure_db()

    client_id = None
    if args.client:
        client = get_client_by_name(args.client)
        if not client:
            print(f"Client not found: {args.client}")
            return
        client_id = client['id']

    data = export_deliverables(format=args.format, client_id=client_id)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(data)
        print(f"Exported to: {output_path}")
    else:
        print(data)

    print(f"\n{FOOTER}")


def cmd_stats(args):
    """Show statistics"""
    ensure_db()

    deliverables = list_deliverables(limit=10000)

    if not deliverables:
        print("No deliverables yet")
        return

    # Calculate stats
    total = len(deliverables)
    delivered = len([d for d in deliverables if d['status'] == 'delivered'])
    approved = len([d for d in deliverables if d['status'] == 'approved'])
    overdue = len([d for d in deliverables if d['deadline'] and
                   d['deadline'] < datetime.now().strftime(DATE_FORMAT) and
                   d['status'] not in ['delivered', 'approved']])

    delivery_rate = (delivered + approved) / total * 100 if total > 0 else 0

    # Average time to deliver
    avg_time = 0
    delivered_items = [d for d in deliverables if d['delivered_at']]
    if delivered_items:
        total_days = 0
        for d in delivered_items:
            if d['created_at'] and d['delivered_at']:
                created = datetime.fromisoformat(d['created_at'].replace('Z', '+00:00'))
                delivered = datetime.fromisoformat(d['delivered_at'].replace('Z', '+00:00'))
                total_days += (delivered - created).days
        avg_time = total_days / len(delivered_items)

    print(f"\nStatistics")
    print("=" * 60)
    print(f"Total Deliverables: {total}")
    print(f"Delivered: {delivered}")
    print(f"Approved: {approved}")
    print(f"Overdue: {overdue}")
    print(f"\nDelivery Rate: {delivery_rate:.1f}%")
    print(f"Overdue Rate: {overdue / total * 100 if total > 0 else 0:.1f}%")
    print(f"Avg Days to Deliver: {avg_time:.1f}")

    print(f"\n{FOOTER}")


def main():
    parser = argparse.ArgumentParser(
        description="Nex Deliverables - Client Deliverable Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  nex-deliverables add --client "Ribbens Airco" --title "Homepage redesign" --type website --deadline 2026-05-01
  nex-deliverables client add --name "Ribbens Airco" --contact-name "John" --email "john@ribbens.be"
  nex-deliverables client show --name "Ribbens Airco"
  nex-deliverables list
  nex-deliverables list --client "Ribbens Airco" --status in_progress
  nex-deliverables show 42
  nex-deliverables status 42 delivered
  nex-deliverables mark "Homepage redesign" delivered
  nex-deliverables overdue
  nex-deliverables search "website"
  nex-deliverables workload
  nex-deliverables email "Ribbens Airco"
  nex-deliverables export --format csv
  nex-deliverables stats
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # add command
    add_parser = subparsers.add_parser('add', help='Add a new deliverable')
    add_parser.add_argument('--client', required=True, help='Client name')
    add_parser.add_argument('--title', required=True, help='Deliverable title')
    add_parser.add_argument('--type', required=True, choices=DELIVERABLE_TYPES, help='Deliverable type')
    add_parser.add_argument('--deadline', help='Deadline (YYYY-MM-DD or "today", "tomorrow", "next week", etc.)')
    add_parser.add_argument('--description', help='Description')
    add_parser.add_argument('--priority', choices=PRIORITY_LEVELS, default='normal', help='Priority')
    add_parser.add_argument('--assigned-to', help='Assigned to person')
    add_parser.add_argument('--estimated-hours', type=float, help='Estimated hours')

    # client command
    client_parser = subparsers.add_parser('client', help='Manage clients')
    client_subparsers = client_parser.add_subparsers(dest='action', required=True)

    client_add = client_subparsers.add_parser('add', help='Add a client')
    client_add.add_argument('--name', required=True, help='Client name')
    client_add.add_argument('--contact-name', help='Contact name')
    client_add.add_argument('--email', help='Email')
    client_add.add_argument('--phone', help='Phone')
    client_add.add_argument('--retainer-amount', type=float, help='Retainer amount')
    client_add.add_argument('--retainer-tier', help='Retainer tier')
    client_add.add_argument('--status', choices=['active', 'paused', 'churned'], default='active')
    client_add.add_argument('--notes', help='Notes')

    client_show = client_subparsers.add_parser('show', help='Show client details')
    client_show.add_argument('--name', required=True, help='Client name')

    client_list = client_subparsers.add_parser('list', help='List clients')
    client_list.add_argument('--status', choices=['active', 'paused', 'churned'], help='Filter by status')

    # list command
    list_parser = subparsers.add_parser('list', help='List deliverables')
    list_parser.add_argument('--client', help='Filter by client name')
    list_parser.add_argument('--status', choices=STATUSES, help='Filter by status')
    list_parser.add_argument('--type', choices=DELIVERABLE_TYPES, help='Filter by type')
    list_parser.add_argument('--priority', choices=PRIORITY_LEVELS, help='Filter by priority')
    list_parser.add_argument('--overdue', action='store_true', help='Show only overdue')

    # show command
    show_parser = subparsers.add_parser('show', help='Show deliverable details')
    show_parser.add_argument('deliverable', help='Deliverable ID or title')

    # status command
    status_parser = subparsers.add_parser('status', help='Update deliverable status')
    status_parser.add_argument('deliverable_id', type=int, help='Deliverable ID')
    status_parser.add_argument('status', choices=STATUSES, help='New status')
    status_parser.add_argument('--message', help='Status message')

    # mark command
    mark_parser = subparsers.add_parser('mark', help='Mark deliverable by title')
    mark_parser.add_argument('title', help='Deliverable title')
    mark_parser.add_argument('status', choices=STATUSES, help='New status')

    # overdue command
    subparsers.add_parser('overdue', help='Show overdue deliverables')

    # search command
    search_parser = subparsers.add_parser('search', help='Search deliverables')
    search_parser.add_argument('query', help='Search query')

    # workload command
    subparsers.add_parser('workload', help='Show workload summary')

    # email command
    email_parser = subparsers.add_parser('email', help='Generate status email')
    email_parser.add_argument('client', help='Client name')

    # export command
    export_parser = subparsers.add_parser('export', help='Export deliverables')
    export_parser.add_argument('--format', choices=['csv', 'json'], default='csv')
    export_parser.add_argument('--client', help='Filter by client')
    export_parser.add_argument('--output', help='Output file path')

    # stats command
    subparsers.add_parser('stats', help='Show statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Route to appropriate command handler
    handlers = {
        'add': cmd_add,
        'client': cmd_client,
        'list': cmd_list,
        'show': cmd_show,
        'status': cmd_status,
        'mark': cmd_mark,
        'overdue': cmd_overdue,
        'search': cmd_search,
        'workload': cmd_workload,
        'email': cmd_email,
        'export': cmd_export,
        'stats': cmd_stats,
    }

    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
