#!/usr/bin/env python3
"""
Nex Ghostwriter - Meeting follow-up email drafter.
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sys
import os
import json
import argparse
import datetime as dt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.storage import (
    init_db, save_meeting, get_meeting, list_meetings, update_meeting,
    search_meetings, save_draft, get_draft, mark_draft_sent, mark_draft_skipped,
    list_drafts, save_contact, get_contact, find_contact_by_name,
    list_contacts, update_contact, get_stats, export_meetings,
)
from lib.templates import generate_email, generate_subject, generate_internal_recap
from lib.config import (
    MEETING_TYPES, TONES, DEFAULT_TONE, URGENCY_LEVELS,
    STATUS_DRAFT, STATUS_SENT, STATUS_SKIPPED,
    SEPARATOR, SUBSEPARATOR, EXPORT_DIR,
)

FOOTER = "[Ghostwriter by Nex AI | nex-ai.be]"


# --- Helpers ---

def _format_date(iso_str):
    if not iso_str:
        return "N/A"
    try:
        d = dt.date.fromisoformat(iso_str[:10])
        return d.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return iso_str


def _parse_action_items(raw):
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return raw
    except (json.JSONDecodeError, TypeError):
        pass
    return json.dumps([i.strip() for i in raw.split(',') if i.strip()])


# --- Commands ---

def cmd_draft(args):
    init_db()

    action_items = _parse_action_items(args.actions) if args.actions else None

    meeting_id = save_meeting(
        title=args.title,
        meeting_type=args.type,
        meeting_date=args.date or dt.date.today().isoformat(),
        attendees=args.attendees,
        client_name=args.client,
        client_email=args.email,
        notes=args.notes,
        action_items=action_items,
        next_steps=args.next_steps,
        deadline=args.deadline,
    )

    # Check if contact exists for personalized greeting
    preferred_greeting = None
    if args.client:
        contacts = find_contact_by_name(args.client)
        if contacts:
            preferred_greeting = contacts[0].get('preferred_greeting')

    tone = args.tone or DEFAULT_TONE

    if args.type == "internal":
        body = generate_internal_recap(
            meeting_title=args.title,
            notes=args.notes,
            action_items=action_items,
            next_steps=args.next_steps,
            attendees=args.attendees,
            meeting_date=args.date or dt.date.today().isoformat(),
        )
        subject = f"Recap: {args.title}"
    else:
        body = generate_email(
            meeting_title=args.title,
            notes=args.notes,
            action_items=action_items,
            next_steps=args.next_steps,
            deadline=args.deadline,
            client_name=args.client,
            client_email=args.email,
            attendees=args.attendees,
            preferred_greeting=preferred_greeting,
            tone=tone,
            meeting_date=args.date or dt.date.today().isoformat(),
        )
        subject = generate_subject(args.title, args.client)

    draft_id = save_draft(meeting_id, subject, body, tone)

    print(f"\nMeeting logged (ID: {meeting_id}) + Draft generated (ID: {draft_id})")
    print(f"{SEPARATOR}")
    if args.email:
        print(f"To: {args.email}")
    print(f"Subject: {subject}")
    print(f"{SUBSEPARATOR}")
    print(body)
    print(f"{SUBSEPARATOR}")
    print(f"\nTone: {tone} | Status: draft")
    print(f"Use: nex-ghostwriter sent {draft_id}  (after sending)")
    print(f"     nex-ghostwriter redraft {meeting_id} --tone formal  (to regenerate)")
    print(FOOTER)


def cmd_redraft(args):
    init_db()

    meeting = get_meeting(args.meeting_id)
    if not meeting:
        print(f"Meeting {args.meeting_id} not found.")
        return

    preferred_greeting = None
    if meeting['client_name']:
        contacts = find_contact_by_name(meeting['client_name'])
        if contacts:
            preferred_greeting = contacts[0].get('preferred_greeting')

    tone = args.tone or DEFAULT_TONE

    if meeting['meeting_type'] == "internal":
        body = generate_internal_recap(
            meeting_title=meeting['title'],
            notes=meeting['notes'],
            action_items=meeting['action_items'],
            next_steps=meeting['next_steps'],
            attendees=meeting['attendees'],
            meeting_date=meeting['meeting_date'],
        )
        subject = f"Recap: {meeting['title']}"
    else:
        body = generate_email(
            meeting_title=meeting['title'],
            notes=meeting['notes'],
            action_items=meeting['action_items'],
            next_steps=meeting['next_steps'],
            deadline=meeting['deadline'],
            client_name=meeting['client_name'],
            client_email=meeting['client_email'],
            attendees=meeting['attendees'],
            preferred_greeting=preferred_greeting,
            tone=tone,
            meeting_date=meeting['meeting_date'],
        )
        subject = generate_subject(meeting['title'], meeting['client_name'])

    draft_id = save_draft(args.meeting_id, subject, body, tone)

    print(f"\nNew draft generated (ID: {draft_id})")
    print(f"{SEPARATOR}")
    print(f"Subject: {subject}")
    print(f"{SUBSEPARATOR}")
    print(body)
    print(f"{SUBSEPARATOR}")
    print(f"Tone: {tone}")
    print(FOOTER)


def cmd_show(args):
    init_db()

    meeting = get_meeting(args.id)
    if not meeting:
        print(f"Meeting {args.id} not found.")
        return

    print(f"\n{SEPARATOR}")
    print(f"MEETING #{meeting['id']}: {meeting['title']}")
    print(f"{SEPARATOR}\n")

    print(f"Type: {meeting['meeting_type']}")
    print(f"Date: {_format_date(meeting['meeting_date'])}")
    if meeting['client_name']:
        print(f"Client: {meeting['client_name']}")
    if meeting['client_email']:
        print(f"Email: {meeting['client_email']}")
    if meeting['attendees']:
        print(f"Attendees: {meeting['attendees']}")

    if meeting['notes']:
        print(f"\nNotes: {meeting['notes']}")

    if meeting['action_items']:
        print(f"\nAction Items:")
        try:
            items = json.loads(meeting['action_items'])
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item}")
        except (json.JSONDecodeError, TypeError):
            print(f"  {meeting['action_items']}")

    if meeting['next_steps']:
        print(f"\nNext Steps: {meeting['next_steps']}")

    if meeting['deadline']:
        print(f"Deadline: {_format_date(meeting['deadline'])}")

    if meeting['drafts']:
        print(f"\n{SUBSEPARATOR}")
        print(f"DRAFTS ({len(meeting['drafts'])})")
        print(f"{SUBSEPARATOR}")
        for draft in meeting['drafts']:
            status_marker = {"draft": "[DRAFT]", "sent": "[SENT]", "skipped": "[SKIP]"}.get(draft['status'], "[?]")
            print(f"\n  Draft #{draft['id']} {status_marker} ({draft['tone']})")
            print(f"  Subject: {draft['subject']}")
            print(f"  Created: {_format_date(draft['created_at'])}")
            if draft['sent_at']:
                print(f"  Sent: {_format_date(draft['sent_at'])}")

    print(f"\n{FOOTER}")


def cmd_show_draft(args):
    init_db()

    draft = get_draft(args.id)
    if not draft:
        print(f"Draft {args.id} not found.")
        return

    print(f"\n{SEPARATOR}")
    print(f"DRAFT #{draft['id']} - Meeting: {draft['meeting_title']}")
    print(f"{SEPARATOR}\n")

    if draft['client_email']:
        print(f"To: {draft['client_email']}")
    print(f"Subject: {draft['subject']}")
    print(f"Tone: {draft['tone']} | Status: {draft['status']}")
    print(f"{SUBSEPARATOR}")
    print(draft['body'])
    print(f"{SUBSEPARATOR}")
    print(FOOTER)


def cmd_list(args):
    init_db()

    meetings = list_meetings(
        meeting_type=args.type,
        client_name=args.client,
        limit=args.limit or 50,
    )

    if not meetings:
        print("No meetings found.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Date':<12} {'Title':<35} {'Client':<20} {'Type':<12}")
    print("-" * 84)

    for m in meetings:
        title = m['title'][:34]
        client = (m['client_name'] or "")[:19]
        date = _format_date(m['meeting_date'])
        print(f"{m['id']:<5} {date:<12} {title:<35} {client:<20} {m['meeting_type']:<12}")

    print(f"\nTotal: {len(meetings)} meetings")
    print(FOOTER)


def cmd_drafts(args):
    init_db()

    drafts = list_drafts(status=args.status, limit=args.limit or 50)

    if not drafts:
        print("No drafts found.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Date':<12} {'Meeting':<30} {'Client':<20} {'Tone':<12} {'Status':<8}")
    print("-" * 87)

    for d in drafts:
        title = (d['meeting_title'] or "")[:29]
        client = (d['client_name'] or "")[:19]
        date = _format_date(d['created_at'])
        print(f"{d['id']:<5} {date:<12} {title:<30} {client:<20} {d['tone']:<12} {d['status']:<8}")

    print(f"\nTotal: {len(drafts)} drafts")
    print(FOOTER)


def cmd_sent(args):
    init_db()

    success = mark_draft_sent(args.id)
    if success:
        print(f"Draft #{args.id} marked as sent.")
    else:
        print(f"Draft {args.id} not found.")
    print(FOOTER)


def cmd_skip(args):
    init_db()

    success = mark_draft_skipped(args.id)
    if success:
        print(f"Draft #{args.id} marked as skipped.")
    else:
        print(f"Draft {args.id} not found.")
    print(FOOTER)


def cmd_search(args):
    init_db()

    results = search_meetings(args.query)
    if not results:
        print(f"No meetings matching '{args.query}'")
        print(FOOTER)
        return

    print(f"\nSearch: '{args.query}' ({len(results)} found)\n")
    for m in results:
        print(f"  [{m['id']}] {m['title']}")
        print(f"       {m['meeting_type']} | {_format_date(m['meeting_date'])}", end="")
        if m['client_name']:
            print(f" | {m['client_name']}", end="")
        print()
        if m['notes']:
            preview = m['notes'][:80]
            if len(m['notes']) > 80:
                preview += "..."
            print(f"       {preview}")
        print()

    print(FOOTER)


def cmd_contact_add(args):
    init_db()

    cid = save_contact(
        name=args.name,
        email=args.email,
        company=args.company,
        role=args.role,
        preferred_greeting=args.greeting,
        notes=args.notes,
    )

    print(f"Contact added (ID: {cid})")
    print(f"  Name: {args.name}")
    if args.email:
        print(f"  Email: {args.email}")
    if args.company:
        print(f"  Company: {args.company}")
    if args.greeting:
        print(f"  Greeting: {args.greeting}")
    print(FOOTER)


def cmd_contact_list(args):
    init_db()

    contacts = list_contacts()
    if not contacts:
        print("No contacts saved.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Company':<20}")
    print("-" * 80)

    for c in contacts:
        email = (c['email'] or "")[:29]
        company = (c['company'] or "")[:19]
        print(f"{c['id']:<5} {c['name'][:24]:<25} {email:<30} {company:<20}")

    print(f"\nTotal: {len(contacts)} contacts")
    print(FOOTER)


def cmd_edit(args):
    init_db()

    updates = {}
    if args.title:
        updates['title'] = args.title
    if args.notes:
        updates['notes'] = args.notes
    if args.actions:
        updates['action_items'] = _parse_action_items(args.actions)
    if args.next_steps:
        updates['next_steps'] = args.next_steps
    if args.client:
        updates['client_name'] = args.client
    if args.email:
        updates['client_email'] = args.email
    if args.deadline:
        updates['deadline'] = args.deadline

    if not updates:
        print("No updates specified.")
        return

    success = update_meeting(args.id, **updates)
    if success:
        print(f"Meeting #{args.id} updated.")
        for k, v in updates.items():
            print(f"  {k}: {v}")
    else:
        print(f"Meeting {args.id} not found.")
    print(FOOTER)


def cmd_stats(args):
    init_db()

    stats = get_stats()

    print(f"\n{SEPARATOR}")
    print(f"GHOSTWRITER STATISTICS")
    print(f"{SEPARATOR}\n")

    print(f"Total meetings: {stats['total_meetings']}")
    print(f"Total drafts: {stats['total_drafts']}")
    print(f"  Sent: {stats['drafts_sent']}")
    print(f"  Pending: {stats['drafts_pending']}")
    print(f"Contacts: {stats['total_contacts']}")

    if stats['by_type']:
        print(f"\nMeetings by Type:")
        for mtype, count in stats['by_type'].items():
            print(f"  {mtype:<16} {count}")

    if stats['top_clients']:
        print(f"\nTop Clients:")
        for client, count in stats['top_clients'].items():
            print(f"  {client:<25} {count} meetings")

    if stats['by_month']:
        print(f"\nMeetings per Month:")
        for month, count in stats['by_month'].items():
            bar = '#' * count
            print(f"  {month} {bar} ({count})")

    print(f"\n{FOOTER}")


def cmd_export(args):
    init_db()

    data = export_meetings(format_type=args.format)
    if not data:
        print("No meetings to export.")
        return

    output_file = args.output or f"meetings_export.{args.format}"
    output_path = EXPORT_DIR / output_file

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(data)

    print(f"Exported to {output_path}")
    print(FOOTER)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Nex Ghostwriter - Meeting follow-up email drafter.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # DRAFT
    p = subparsers.add_parser('draft', help='Log meeting + generate follow-up email')
    p.add_argument('title', help='Meeting title or summary')
    p.add_argument('--notes', '-n', help='What was discussed')
    p.add_argument('--actions', '-a', help='Action items (comma-separated or JSON array)')
    p.add_argument('--next-steps', help='Agreed next steps')
    p.add_argument('--client', help='Client/recipient name')
    p.add_argument('--email', help='Client/recipient email')
    p.add_argument('--attendees', help='Who attended')
    p.add_argument('--type', default='client', choices=MEETING_TYPES, help='Meeting type')
    p.add_argument('--tone', choices=TONES, help=f'Email tone (default: {DEFAULT_TONE})')
    p.add_argument('--date', help='Meeting date (YYYY-MM-DD, default: today)')
    p.add_argument('--deadline', help='Deadline for deliverables (YYYY-MM-DD)')
    p.set_defaults(func=cmd_draft)

    # REDRAFT
    p = subparsers.add_parser('redraft', help='Regenerate email for existing meeting')
    p.add_argument('meeting_id', type=int, help='Meeting ID')
    p.add_argument('--tone', choices=TONES, help='New tone')
    p.set_defaults(func=cmd_redraft)

    # SHOW (meeting)
    p = subparsers.add_parser('show', help='Show meeting details + drafts')
    p.add_argument('id', type=int, help='Meeting ID')
    p.set_defaults(func=cmd_show)

    # VIEW (draft)
    p = subparsers.add_parser('view', help='View a draft\'s full email')
    p.add_argument('id', type=int, help='Draft ID')
    p.set_defaults(func=cmd_show_draft)

    # LIST
    p = subparsers.add_parser('list', help='List meetings')
    p.add_argument('--type', choices=MEETING_TYPES, help='Filter by type')
    p.add_argument('--client', help='Filter by client name')
    p.add_argument('--limit', type=int, default=50, help='Max results')
    p.set_defaults(func=cmd_list)

    # DRAFTS
    p = subparsers.add_parser('drafts', help='List all drafts')
    p.add_argument('--status', choices=[STATUS_DRAFT, STATUS_SENT, STATUS_SKIPPED], help='Filter by status')
    p.add_argument('--limit', type=int, default=50, help='Max results')
    p.set_defaults(func=cmd_drafts)

    # SENT
    p = subparsers.add_parser('sent', help='Mark draft as sent')
    p.add_argument('id', type=int, help='Draft ID')
    p.set_defaults(func=cmd_sent)

    # SKIP
    p = subparsers.add_parser('skip', help='Mark draft as skipped')
    p.add_argument('id', type=int, help='Draft ID')
    p.set_defaults(func=cmd_skip)

    # SEARCH
    p = subparsers.add_parser('search', help='Search meetings')
    p.add_argument('query', help='Search query')
    p.set_defaults(func=cmd_search)

    # EDIT
    p = subparsers.add_parser('edit', help='Edit meeting details')
    p.add_argument('id', type=int, help='Meeting ID')
    p.add_argument('--title', help='New title')
    p.add_argument('--notes', help='New notes')
    p.add_argument('--actions', help='New action items')
    p.add_argument('--next-steps', help='New next steps')
    p.add_argument('--client', help='New client name')
    p.add_argument('--email', help='New client email')
    p.add_argument('--deadline', help='New deadline')
    p.set_defaults(func=cmd_edit)

    # CONTACT ADD
    p = subparsers.add_parser('contact-add', help='Add a contact')
    p.add_argument('name', help='Contact name')
    p.add_argument('--email', help='Email address')
    p.add_argument('--company', help='Company name')
    p.add_argument('--role', help='Role/title')
    p.add_argument('--greeting', help='Preferred greeting (e.g., "Dear Mr. Smith,")')
    p.add_argument('--notes', help='Notes about this contact')
    p.set_defaults(func=cmd_contact_add)

    # CONTACT LIST
    p = subparsers.add_parser('contacts', help='List contacts')
    p.set_defaults(func=cmd_contact_list)

    # STATS
    p = subparsers.add_parser('stats', help='Show statistics')
    p.set_defaults(func=cmd_stats)

    # EXPORT
    p = subparsers.add_parser('export', help='Export meetings')
    p.add_argument('format', choices=['json', 'csv'], help='Export format')
    p.add_argument('--output', help='Output filename')
    p.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
