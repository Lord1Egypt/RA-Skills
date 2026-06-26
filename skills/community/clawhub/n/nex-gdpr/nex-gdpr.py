#!/usr/bin/env python3
# Nex GDPR - GDPR Data Request Handler
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from tabulate import tabulate

from lib.config import (
    FOOTER,
    REQUEST_TYPES,
    REQUEST_STATUSES,
    RESPONSE_DEADLINE_DAYS,
    EXTENSION_DAYS,
    RESPONSE_LETTER_TEMPLATE_NL,
    RESPONSE_LETTER_TEMPLATE_EN,
)
from lib.storage import GDPRStorage
from lib.scanner import DataScanner
from lib.processor import RequestProcessor


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def cmd_new(args):
    """Register new GDPR request."""
    storage = GDPRStorage()

    if not args.type or not args.name or not args.email:
        print("ERROR: --type, --name, and --email are required")
        sys.exit(1)

    if args.type.upper() not in REQUEST_TYPES:
        print(f"ERROR: Invalid request type. Must be one of: {', '.join(REQUEST_TYPES.keys())}")
        sys.exit(1)

    request_id = storage.save_request(
        request_type=args.type.upper(),
        name=args.name,
        email=args.email,
        data_subject_id=args.id,
        notes=args.notes or "",
    )

    print(f"Created request #{request_id}")
    print(f"  Type: {REQUEST_TYPES[args.type.upper()]}")
    print(f"  Subject: {args.name} ({args.email})")
    print(f"  Deadline: {RESPONSE_DEADLINE_DAYS} days from now")
    print(FOOTER)


def cmd_list(args):
    """List GDPR requests."""
    storage = GDPRStorage()

    filters = {}
    if args.status:
        if args.status.upper() not in REQUEST_STATUSES:
            print(f"ERROR: Invalid status. Must be one of: {', '.join(REQUEST_STATUSES.keys())}")
            sys.exit(1)
        filters["status"] = args.status.upper()

    if args.type:
        if args.type.upper() not in REQUEST_TYPES:
            print(f"ERROR: Invalid type. Must be one of: {', '.join(REQUEST_TYPES.keys())}")
            sys.exit(1)
        filters["request_type"] = args.type.upper()

    requests = storage.list_requests(**filters)

    if not requests:
        print("No requests found.")
        return

    table_data = []
    for req in requests:
        deadline = req["extended_deadline"] or req["deadline_date"]
        is_overdue = deadline < datetime.now().isoformat() and req["status"] not in ["COMPLETED", "DENIED"]
        overdue_mark = " [OVERDUE]" if is_overdue else ""

        table_data.append([
            req["id"],
            req["request_type"],
            req["data_subject_name"],
            req["status"],
            deadline[:10],
            overdue_mark,
        ])

    headers = ["ID", "Type", "Subject", "Status", "Deadline", ""]
    print(tabulate(table_data, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(requests)} request(s)")
    print(FOOTER)


def cmd_show(args):
    """Show request details."""
    storage = GDPRStorage()
    request = storage.get_request(args.request_id)

    if not request:
        print(f"ERROR: Request #{args.request_id} not found")
        sys.exit(1)

    print(f"\n=== Request #{args.request_id} ===")
    print(f"Type: {REQUEST_TYPES.get(request['request_type'], request['request_type'])}")
    print(f"Subject: {request['data_subject_name']} ({request['data_subject_email']})")
    if request['data_subject_id']:
        print(f"ID: {request['data_subject_id']}")
    print(f"Status: {REQUEST_STATUSES.get(request['status'], request['status'])}")
    print(f"Received: {request['received_date']}")
    print(f"Deadline: {request['deadline_date']}")
    if request['extended_deadline']:
        print(f"Extended Deadline: {request['extended_deadline']}")
    if request['verified']:
        print(f"Verified: Yes ({request['verification_method']})")
    if request['assigned_to']:
        print(f"Assigned to: {request['assigned_to']}")
    if request['notes']:
        print(f"Notes: {request['notes']}")

    # Show findings
    findings = storage.list_findings(args.request_id)
    if findings:
        print(f"\nFindings ({len(findings)}):")
        for finding in findings:
            print(f"  - {finding['file_path']}")
            print(f"    Source: {finding['data_source']}")
            print(f"    Type: {finding['data_type']}")
            print(f"    Size: {format_size(finding['size_bytes'])}")
            print(f"    PII: {'Yes' if finding['contains_pii'] else 'No'}")
            print(f"    Action: {finding['action_taken']}")

    # Show audit trail
    audit = storage.get_audit_trail(args.request_id)
    if audit:
        print(f"\nAudit Trail ({len(audit)} entries):")
        for entry in audit[:5]:
            print(f"  [{entry['timestamp'][:19]}] {entry['action']} by {entry['actor']}")
        if len(audit) > 5:
            print(f"  ... and {len(audit) - 5} more")

    print(FOOTER)


def cmd_scan(args):
    """Scan for user data."""
    storage = GDPRStorage()
    scanner = DataScanner()

    if args.request:
        request = storage.get_request(args.request)
        if not request:
            print(f"ERROR: Request #{args.request} not found")
            sys.exit(1)
        identifier = request["data_subject_email"] or request["data_subject_id"]
        request_id = args.request
        print(f"Scanning for data related to request #{request_id}...")
    else:
        identifier = args.identifier
        request_id = None
        print(f"Scanning for data related to: {identifier}")

    findings = scanner.scan_for_user_data(identifier)

    if not findings:
        print("No data found.")
        return

    total_size = 0
    pii_count = 0

    for finding in findings:
        if finding.get("contains_pii"):
            pii_count += 1
        total_size += finding.get("size_bytes", 0)

        print(f"\nFound: {finding['file_path']}")
        print(f"  Size: {format_size(finding['size_bytes'])}")
        print(f"  Type: {finding['data_type']}")
        print(f"  Source: {finding['data_source']}")
        if finding.get("contains_pii"):
            print(f"  PII Types: {', '.join(finding.get('pii_types', []))}")

    print(f"\n{len(findings)} data source(s) found")
    print(f"Total size: {format_size(total_size)}")
    print(f"PII detected: {pii_count} source(s)")

    # If scanning for request, save findings
    if request_id:
        for finding in findings:
            storage.save_finding(
                request_id,
                finding.get("data_source", "unknown"),
                finding["file_path"],
                finding.get("data_type", "personal_data"),
                finding.get("description", ""),
                finding.get("size_bytes", 0),
                finding.get("contains_pii", False),
            )
        print(f"\nSaved {len(findings)} findings to request #{request_id}")

    print(FOOTER)


def cmd_process(args):
    """Process a GDPR request."""
    storage = GDPRStorage()
    processor = RequestProcessor()

    request = storage.get_request(args.request_id)
    if not request:
        print(f"ERROR: Request #{args.request_id} not found")
        sys.exit(1)

    if request["status"] not in ["VERIFIED", "IN_PROGRESS"]:
        print(f"ERROR: Can only process VERIFIED or IN_PROGRESS requests")
        print(f"Current status: {request['status']}")
        sys.exit(1)

    request_type = request["request_type"]
    print(f"Processing {request_type} request #{args.request_id}...")

    storage.update_request_status(args.request_id, "IN_PROGRESS")

    try:
        if request_type == "ACCESS":
            result = processor.process_access_request(args.request_id)
            print(f"Access request processed")
            print(f"  Findings: {result['findings_count']}")
            print(f"  Total size: {format_size(result['total_size'])}")
            print(f"  Export: {result['export_path']}")

        elif request_type == "ERASURE":
            result = processor.process_erasure_request(args.request_id)
            print(f"Erasure request processed")
            print(f"  Deleted: {result['deleted_count']}")
            print(f"  Retained: {result['retained_count']}")
            if result['retained_reasons']:
                for reason in result['retained_reasons']:
                    print(f"    - {reason}")

        elif request_type == "PORTABILITY":
            result = processor.process_portability_request(args.request_id)
            print(f"Portability request processed")
            print(f"  Export: {result['export_path']}")

        elif request_type == "RECTIFICATION":
            print("ERROR: Use 'rectify' command for rectification requests")
            sys.exit(1)

        else:
            print(f"ERROR: Unknown request type: {request_type}")
            sys.exit(1)

        storage.update_request_status(args.request_id, "COMPLETED")
        print(f"Request marked as COMPLETED")

    except Exception as e:
        print(f"ERROR: {e}")
        storage.update_request_status(args.request_id, "IN_PROGRESS")
        sys.exit(1)

    print(FOOTER)


def cmd_verify(args):
    """Verify request identity."""
    storage = GDPRStorage()

    request = storage.get_request(args.request_id)
    if not request:
        print(f"ERROR: Request #{args.request_id} not found")
        sys.exit(1)

    conn = storage.db_path.parent / storage.db_path.name
    import sqlite3

    db_conn = sqlite3.connect(storage.db_path)
    cursor = db_conn.cursor()
    cursor.execute(
        "UPDATE requests SET verified = 1, verification_method = ?, updated_at = ? WHERE id = ?",
        (args.method or "manual", datetime.now().isoformat(), args.request_id),
    )
    db_conn.commit()
    db_conn.close()

    storage.update_request_status(args.request_id, "VERIFIED", details=f"Method: {args.method or 'manual'}")

    print(f"Request #{args.request_id} verified")
    print(f"Method: {args.method or 'manual'}")
    print(FOOTER)


def cmd_deny(args):
    """Deny a request."""
    storage = GDPRStorage()

    request = storage.get_request(args.request_id)
    if not request:
        print(f"ERROR: Request #{args.request_id} not found")
        sys.exit(1)

    import sqlite3

    db_conn = sqlite3.connect(storage.db_path)
    cursor = db_conn.cursor()
    cursor.execute(
        "UPDATE requests SET status = 'DENIED', denied_reason = ?, updated_at = ? WHERE id = ?",
        (args.reason or "Not specified", datetime.now().isoformat(), args.request_id),
    )
    db_conn.commit()
    db_conn.close()

    storage.save_audit_entry(args.request_id, "request_denied", "system",
                            f"Reason: {args.reason or 'Not specified'}")

    print(f"Request #{args.request_id} denied")
    print(f"Reason: {args.reason or 'Not specified'}")
    print(FOOTER)


def cmd_complete(args):
    """Complete a request."""
    storage = GDPRStorage()

    request = storage.get_request(args.request_id)
    if not request:
        print(f"ERROR: Request #{args.request_id} not found")
        sys.exit(1)

    storage.update_request_status(args.request_id, "COMPLETED")

    print(f"Request #{args.request_id} marked as COMPLETED")
    print(FOOTER)


def cmd_overdue(args):
    """List overdue requests."""
    storage = GDPRStorage()
    overdue = storage.get_overdue_requests()

    if not overdue:
        print("No overdue requests.")
        return

    table_data = []
    for req in overdue:
        days_overdue = (datetime.now() - datetime.fromisoformat(req["deadline_date"])).days
        table_data.append([
            req["id"],
            req["request_type"],
            req["data_subject_name"],
            req["deadline_date"][:10],
            f"{days_overdue} days",
        ])

    headers = ["ID", "Type", "Subject", "Deadline", "Overdue"]
    print(tabulate(table_data, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(overdue)} overdue request(s)")
    print(FOOTER)


def cmd_findings(args):
    """Show data findings for a request."""
    storage = GDPRStorage()
    findings = storage.list_findings(args.request_id)

    if not findings:
        print(f"No findings for request #{args.request_id}")
        return

    table_data = []
    for finding in findings:
        table_data.append([
            finding["id"],
            finding["data_source"],
            Path(finding["file_path"]).name,
            format_size(finding["size_bytes"]),
            "Yes" if finding["contains_pii"] else "No",
            finding["action_taken"],
        ])

    headers = ["ID", "Source", "File", "Size", "PII", "Action"]
    print(tabulate(table_data, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(findings)} finding(s)")
    print(FOOTER)


def cmd_export(args):
    """Export request report."""
    storage = GDPRStorage()
    report = storage.export_request_report(args.request_id)

    if not report:
        print(f"ERROR: Request #{args.request_id} not found")
        sys.exit(1)

    # Save as JSON
    export_path = Path.home() / ".nex-gdpr" / f"report_{args.request_id}.json"
    with open(export_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"Exported report to: {export_path}")
    print(FOOTER)


def cmd_audit(args):
    """Show audit trail."""
    storage = GDPRStorage()
    audit = storage.get_audit_trail(args.request_id)

    if not audit:
        print(f"No audit trail for request #{args.request_id}")
        return

    for entry in audit:
        print(f"[{entry['timestamp']}] {entry['action']}")
        print(f"  Actor: {entry['actor']}")
        if entry['details']:
            print(f"  Details: {entry['details']}")

    print(FOOTER)


def cmd_stats(args):
    """Show GDPR statistics."""
    storage = GDPRStorage()
    stats = storage.get_request_stats()

    print("\n=== GDPR Request Statistics ===")
    print(f"\nBy Status:")
    for status in REQUEST_STATUSES.keys():
        count = stats.get(f"count_{status}", 0)
        print(f"  {status}: {count}")

    print(f"\nBy Type:")
    for req_type in REQUEST_TYPES.keys():
        count = stats.get(f"count_{req_type}", 0)
        print(f"  {req_type}: {count}")

    print(f"\nOverall:")
    print(f"  Overdue: {stats.get('overdue', 0)}")
    print(f"  Total Findings: {stats.get('total_findings', 0)}")
    print(f"  PII Findings: {stats.get('pii_findings', 0)}")
    print(f"  Total Data Size: {format_size(stats.get('total_size_bytes', 0))}")

    print(FOOTER)


def cmd_letter(args):
    """Generate response letter."""
    storage = GDPRStorage()
    request = storage.get_request(args.request_id)

    if not request:
        print(f"ERROR: Request #{args.request_id} not found")
        sys.exit(1)

    request_type = request["request_type"]
    article_map = {
        "ACCESS": "15",
        "ERASURE": "17",
        "PORTABILITY": "20",
        "RECTIFICATION": "16",
        "RESTRICTION": "18",
        "OBJECTION": "21",
    }
    article = article_map.get(request_type, "15")

    # Generate letter (Dutch)
    body_nl = "Uw verzoek is in behandeling."
    if request["status"] == "COMPLETED":
        body_nl = "Uw verzoek is verwerkt. Zie bijlagen voor gegevens."
    elif request["status"] == "DENIED":
        body_nl = f"Uw verzoek is afgewezen. Reden: {request['denied_reason']}"

    letter_nl = RESPONSE_LETTER_TEMPLATE_NL.format(
        name=request["data_subject_name"],
        article=article,
        received_date=request["received_date"][:10],
        deadline_date=request["deadline_date"][:10],
        request_type=REQUEST_TYPES[request_type],
        status=REQUEST_STATUSES[request["status"]],
        body=body_nl,
        organization="Nex AI",
    )

    print("=== GDPR Response Letter (Dutch) ===")
    print(letter_nl)
    print()

    # Generate letter (English)
    body_en = "Your request is being processed."
    if request["status"] == "COMPLETED":
        body_en = "Your request has been processed. See attachments for data."
    elif request["status"] == "DENIED":
        body_en = f"Your request has been denied. Reason: {request['denied_reason']}"

    letter_en = RESPONSE_LETTER_TEMPLATE_EN.format(
        name=request["data_subject_name"],
        article=article,
        received_date=request["received_date"][:10],
        deadline_date=request["deadline_date"][:10],
        request_type=REQUEST_TYPES[request_type],
        status=REQUEST_STATUSES[request["status"]],
        body=body_en,
        organization="Nex AI",
    )

    print("=== GDPR Response Letter (English) ===")
    print(letter_en)

    print(FOOTER)


def cmd_retention(args):
    """Manage retention policies."""
    storage = GDPRStorage()

    if args.subcommand == "show":
        policies = storage.get_retention_policies()
        if not policies:
            print("No retention policies configured.")
            return

        table_data = []
        for policy in policies:
            table_data.append([
                policy["data_type"],
                policy["retention_days"],
                "Yes" if policy["auto_delete"] else "No",
                policy.get("last_cleanup", "Never"),
            ])

        headers = ["Data Type", "Retention Days", "Auto Delete", "Last Cleanup"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))

    elif args.subcommand == "set":
        if not args.type or not args.days:
            print("ERROR: --type and --days are required")
            sys.exit(1)

        storage.save_retention_policy(args.type, args.days, args.auto_delete or False)
        print(f"Retention policy set: {args.type} = {args.days} days")

    print(FOOTER)


def cmd_cleanup(args):
    """Run retention cleanup."""
    print("Running retention cleanup...")
    if args.dry_run:
        print("[DRY RUN] Would delete expired data...")
    else:
        print("[EXECUTE] Deleting expired data...")

    print("(Cleanup routine not implemented in this demo)")
    print(FOOTER)


def main():
    parser = argparse.ArgumentParser(
        description="Nex GDPR - GDPR Data Request Handler for agency operators",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # new command
    new_parser = subparsers.add_parser("new", help="Register new GDPR request")
    new_parser.add_argument("--type", required=True, help="Request type (ACCESS, ERASURE, PORTABILITY, RECTIFICATION, RESTRICTION, OBJECTION)")
    new_parser.add_argument("--name", required=True, help="Data subject name")
    new_parser.add_argument("--email", required=True, help="Data subject email")
    new_parser.add_argument("--id", help="Internal data subject ID")
    new_parser.add_argument("--notes", help="Additional notes")
    new_parser.set_defaults(func=cmd_new)

    # list command
    list_parser = subparsers.add_parser("list", help="List GDPR requests")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--type", help="Filter by request type")
    list_parser.set_defaults(func=cmd_list)

    # show command
    show_parser = subparsers.add_parser("show", help="Show request details")
    show_parser.add_argument("request_id", type=int, help="Request ID")
    show_parser.set_defaults(func=cmd_show)

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for user data")
    scan_group = scan_parser.add_mutually_exclusive_group(required=True)
    scan_group.add_argument("--request", type=int, help="Request ID")
    scan_group.add_argument("identifier", nargs="?", help="Email or identifier")
    scan_parser.set_defaults(func=cmd_scan)

    # process command
    process_parser = subparsers.add_parser("process", help="Process a request")
    process_parser.add_argument("request_id", type=int, help="Request ID")
    process_parser.set_defaults(func=cmd_process)

    # verify command
    verify_parser = subparsers.add_parser("verify", help="Verify request identity")
    verify_parser.add_argument("request_id", type=int, help="Request ID")
    verify_parser.add_argument("--method", help="Verification method")
    verify_parser.set_defaults(func=cmd_verify)

    # deny command
    deny_parser = subparsers.add_parser("deny", help="Deny a request")
    deny_parser.add_argument("request_id", type=int, help="Request ID")
    deny_parser.add_argument("--reason", help="Denial reason")
    deny_parser.set_defaults(func=cmd_deny)

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Complete a request")
    complete_parser.add_argument("request_id", type=int, help="Request ID")
    complete_parser.set_defaults(func=cmd_complete)

    # overdue command
    overdue_parser = subparsers.add_parser("overdue", help="Show overdue requests")
    overdue_parser.set_defaults(func=cmd_overdue)

    # findings command
    findings_parser = subparsers.add_parser("findings", help="Show data findings")
    findings_parser.add_argument("request_id", type=int, help="Request ID")
    findings_parser.set_defaults(func=cmd_findings)

    # export command
    export_parser = subparsers.add_parser("export", help="Export request report")
    export_parser.add_argument("request_id", type=int, help="Request ID")
    export_parser.set_defaults(func=cmd_export)

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Show audit trail")
    audit_parser.add_argument("request_id", type=int, help="Request ID")
    audit_parser.set_defaults(func=cmd_audit)

    # stats command
    stats_parser = subparsers.add_parser("stats", help="Show GDPR statistics")
    stats_parser.set_defaults(func=cmd_stats)

    # letter command
    letter_parser = subparsers.add_parser("letter", help="Generate response letter")
    letter_parser.add_argument("request_id", type=int, help="Request ID")
    letter_parser.set_defaults(func=cmd_letter)

    # retention command
    retention_parser = subparsers.add_parser("retention", help="Manage retention policies")
    retention_subparsers = retention_parser.add_subparsers(dest="subcommand", help="Subcommand")
    retention_show = retention_subparsers.add_parser("show", help="Show policies")
    retention_show.set_defaults(func=cmd_retention)
    retention_set = retention_subparsers.add_parser("set", help="Set policy")
    retention_set.add_argument("--type", required=True, help="Data type")
    retention_set.add_argument("--days", type=int, required=True, help="Retention days")
    retention_set.add_argument("--auto-delete", action="store_true", help="Auto delete after retention")
    retention_set.set_defaults(func=cmd_retention)

    # cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Run retention cleanup")
    cleanup_parser.add_argument("--dry-run", action="store_true", help="Dry run")
    cleanup_parser.add_argument("--execute", action="store_true", help="Execute cleanup")
    cleanup_parser.set_defaults(func=cmd_cleanup)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    try:
        args.func(args)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
