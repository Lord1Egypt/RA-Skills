#!/usr/bin/env python3
"""
inbox_cleanup.py — IMAP bulk email triage with dry-run mode.

Classify inbox messages by sender domain / subject keywords, then:
  - DELETE matched messages (expunge)
  - ARCHIVE matched messages (copy to archive folder, then expunge)
  - LEAVE everything else

Uses UIDs (not sequence numbers) for reliable bulk ops — critical when deleting
mid-session shifts message numbering.

Usage:
  python3 inbox_cleanup.py --config patterns.yaml --dry-run   # preview
  python3 inbox_cleanup.py --config patterns.yaml --no-dry-run  # apply

Environment variables (or use --imap-* flags):
  IMAP_HOST              IMAP server host (default: 127.0.0.1)
  IMAP_PORT              IMAP port (default: 1143)
  IMAP_USER              IMAP username
  IMAP_PASSWORD          IMAP password
  IMAP_STARTTLS          true/false — use STARTTLS (default: true)
  IMAP_SKIP_CERT_VERIFY  true/false — skip cert verify for self-signed (default: false)
  ARCHIVE_FOLDER         Archive folder name (default: Archive)
"""
from __future__ import annotations

import argparse
import email
import email.header
import imaplib
import json
import os
import re
import ssl
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── Config loading ────────────────────────────────────────────────────────────

def load_patterns(config_path: str) -> dict:
    """Load delete/archive/leave patterns from YAML or JSON config file."""
    p = Path(config_path)
    if not p.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    text = p.read_text()
    if p.suffix in (".yaml", ".yml"):
        if not HAS_YAML:
            print("PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
            sys.exit(1)
        return yaml.safe_load(text)
    return json.loads(text)


def default_patterns() -> dict:
    return {
        "delete_domains": [],
        "archive_domains": [],
        "archive_keywords": ["newsletter", "digest", "weekly", "roundup", "unsubscribe"],
        "delete_subject_patterns": [],
        "leave_domains": [],
    }


# ── IMAP connection ───────────────────────────────────────────────────────────

def connect_imap(host: str, port: int, user: str, password: str,
                 starttls: bool = True, skip_cert_verify: bool = False) -> imaplib.IMAP4:
    """Connect and authenticate to IMAP server."""
    ctx = ssl.create_default_context()
    if skip_cert_verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    if starttls:
        mail = imaplib.IMAP4(host, port)
        mail.starttls(ssl_context=ctx)
    else:
        mail = imaplib.IMAP4_SSL(host, port, ssl_context=ctx)

    mail.login(user, password)
    return mail


# ── Header parsing ────────────────────────────────────────────────────────────

def decode_header(raw: Optional[str]) -> str:
    if raw is None:
        return ""
    parts = email.header.decode_header(raw)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return " ".join(decoded)


def extract_domain(from_header: str) -> str:
    match = re.search(r'@([\w.-]+)', from_header)
    return match.group(1).lower() if match else "unknown"


# ── Message fetching ──────────────────────────────────────────────────────────

def fetch_all_headers(mail: imaplib.IMAP4, one_at_a_time: bool = False) -> list[dict]:
    """Fetch FROM + SUBJECT headers for all inbox messages. Returns list of dicts with uid."""
    status, data = mail.uid("SEARCH", None, "ALL")
    if status != "OK":
        print(f"UID SEARCH failed: {status}", file=sys.stderr)
        return []

    uids = data[0].split() if data[0] else []
    print(f"Found {len(uids)} messages in INBOX")

    messages = []

    if one_at_a_time:
        # Reliable for edge-case servers; slower but no UID extraction issues
        for uid in uids:
            status, msg_data = mail.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
            if status != "OK":
                continue
            for item in msg_data:
                if isinstance(item, tuple) and len(item) == 2:
                    header_data = item[1]
                    if isinstance(header_data, bytes):
                        msg = email.message_from_bytes(header_data)
                        uid_str = uid.decode() if isinstance(uid, bytes) else uid
                        messages.append(_parse_msg(uid_str, msg))
                        break
    else:
        # Batch fetch (50 at a time) — faster for large inboxes
        for i in range(0, len(uids), 50):
            batch = uids[i:i + 50]
            uid_set = b",".join(batch)
            status, msg_data = mail.uid("FETCH", uid_set, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
            if status != "OK":
                print(f"Batch fetch failed at offset {i}")
                continue

            j = 0
            while j < len(msg_data):
                item = msg_data[j]
                if isinstance(item, tuple) and len(item) == 2:
                    resp_line = item[0].decode() if isinstance(item[0], bytes) else item[0]
                    uid_match = re.search(r'UID (\d+)', resp_line)
                    uid_str = uid_match.group(1) if uid_match else None
                    if uid_str:
                        header_data = item[1]
                        if isinstance(header_data, bytes):
                            msg = email.message_from_bytes(header_data)
                            messages.append(_parse_msg(uid_str, msg))
                j += 1

    print(f"Parsed {len(messages)} message headers")
    return messages


def _parse_msg(uid: str, msg) -> dict:
    from_hdr = decode_header(msg.get("From", ""))
    subject = decode_header(msg.get("Subject", ""))
    return {
        "uid": uid,
        "from": from_hdr,
        "subject": subject,
        "domain": extract_domain(from_hdr),
    }


# ── Classification ────────────────────────────────────────────────────────────

def classify(messages: list[dict], patterns: dict) -> tuple[list, list, list]:
    """Returns (to_delete, to_archive, to_leave)."""
    delete_domains = set(patterns.get("delete_domains", []))
    archive_domains = set(patterns.get("archive_domains", []))
    archive_keywords = [kw.lower() for kw in patterns.get("archive_keywords", [])]
    delete_subject_patterns = [re.compile(p) for p in patterns.get("delete_subject_patterns", [])]
    leave_domains = set(patterns.get("leave_domains", []))

    to_delete, to_archive, to_leave = [], [], []

    for m in messages:
        domain = m["domain"]
        subject_lower = m["subject"].lower()
        from_lower = m["from"].lower()

        if domain in leave_domains:
            to_leave.append(m)
        elif domain in delete_domains:
            to_delete.append(m)
        elif any(pat.search(m["subject"]) for pat in delete_subject_patterns):
            to_delete.append(m)
        elif domain in archive_domains:
            to_archive.append(m)
        elif any(kw in subject_lower for kw in archive_keywords):
            to_archive.append(m)
        elif any(kw in from_lower for kw in ["newsletter", "noreply", "no-reply", "digest", "marketing"]):
            to_archive.append(m)
        else:
            to_leave.append(m)

    return to_delete, to_archive, to_leave


# ── Actions ───────────────────────────────────────────────────────────────────

def apply_delete(mail: imaplib.IMAP4, messages: list[dict], dry_run: bool) -> int:
    if not messages:
        return 0
    print(f"{'[DRY RUN] Would delete' if dry_run else 'Deleting'} {len(messages)} messages...")
    if dry_run:
        for m in messages[:5]:
            print(f"  [{m['domain']}] {m['subject'][:70]}")
        if len(messages) > 5:
            print(f"  ... and {len(messages) - 5} more")
        return len(messages)

    count = 0
    for m in messages:
        uid = m["uid"]
        uid_b = uid.encode() if isinstance(uid, str) else uid
        mail.uid("STORE", uid_b, "+FLAGS", "\\Deleted")
        count += 1
    mail.expunge()
    return count


def apply_archive(mail: imaplib.IMAP4, messages: list[dict],
                  archive_folder: str, dry_run: bool) -> int:
    if not messages:
        return 0
    print(f"{'[DRY RUN] Would archive' if dry_run else 'Archiving'} {len(messages)} messages "
          f"to '{archive_folder}'...")
    if dry_run:
        for m in messages[:5]:
            print(f"  [{m['domain']}] {m['subject'][:70]}")
        if len(messages) > 5:
            print(f"  ... and {len(messages) - 5} more")
        return len(messages)

    count = 0
    for m in messages:
        uid = m["uid"]
        uid_b = uid.encode() if isinstance(uid, str) else uid
        try:
            s, _ = mail.uid("COPY", uid_b, archive_folder)
            if s == "OK":
                mail.uid("STORE", uid_b, "+FLAGS", "\\Deleted")
                count += 1
            else:
                print(f"  COPY failed for UID {uid}: {s}")
        except Exception as e:
            print(f"  Error archiving UID {uid}: {e}")
    if count:
        mail.expunge()
    return count


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="IMAP bulk inbox triage")
    parser.add_argument("--config", help="Path to YAML/JSON patterns config file")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview only — no changes (default: true)")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false",
                        help="Apply changes (required to actually delete/archive)")
    parser.add_argument("--one-at-a-time", action="store_true",
                        help="Fetch headers one-at-a-time (slower but reliable for some servers)")
    parser.add_argument("--imap-host", default=os.environ.get("IMAP_HOST", "127.0.0.1"))
    parser.add_argument("--imap-port", type=int, default=int(os.environ.get("IMAP_PORT", "1143")))
    parser.add_argument("--imap-user", default=os.environ.get("IMAP_USER", ""))
    parser.add_argument("--imap-password", default=os.environ.get("IMAP_PASSWORD", ""))
    parser.add_argument("--imap-no-starttls", action="store_true",
                        default=os.environ.get("IMAP_STARTTLS", "true").lower() == "false")
    parser.add_argument("--imap-skip-cert-verify", action="store_true",
                        default=os.environ.get("IMAP_SKIP_CERT_VERIFY", "false").lower() == "true")
    parser.add_argument("--archive-folder",
                        default=os.environ.get("ARCHIVE_FOLDER", "Archive"))
    parser.add_argument("--mailbox", default="INBOX")
    parser.add_argument("--report-json", help="Write JSON report to this file")
    args = parser.parse_args()

    if not args.imap_user or not args.imap_password:
        print("IMAP_USER and IMAP_PASSWORD are required (env vars or --imap-* flags)", file=sys.stderr)
        sys.exit(1)

    # Load patterns
    if args.config:
        patterns = load_patterns(args.config)
    else:
        patterns = default_patterns()
        print("No --config provided — using built-in defaults (archive common newsletter keywords)")

    # Connect
    print(f"Connecting to {args.imap_host}:{args.imap_port} "
          f"({'STARTTLS' if not args.imap_no_starttls else 'SSL'})...")
    mail = connect_imap(
        host=args.imap_host,
        port=args.imap_port,
        user=args.imap_user,
        password=args.imap_password,
        starttls=not args.imap_no_starttls,
        skip_cert_verify=args.imap_skip_cert_verify,
    )
    mail.select(args.mailbox)

    # Fetch + classify
    messages = fetch_all_headers(mail, one_at_a_time=args.one_at_a_time)
    to_delete, to_archive, to_leave = classify(messages, patterns)

    print(f"\nClassification: delete={len(to_delete)}, archive={len(to_archive)}, leave={len(to_leave)}")
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE — no changes will be made. Use --no-dry-run to apply.\n")

    # Apply
    deleted = apply_delete(mail, to_delete, args.dry_run)
    archived = apply_archive(mail, to_archive, args.archive_folder, args.dry_run)

    # Report
    report = {
        "timestamp": datetime.now().isoformat(),
        "dry_run": args.dry_run,
        "total_inbox": len(messages),
        "deleted": deleted,
        "archived": archived,
        "left": len(to_leave),
        "deleted_domains": sorted(set(m["domain"] for m in to_delete)),
        "archived_domains": sorted(set(m["domain"] for m in to_archive)),
        "left_messages": [{"domain": m["domain"], "subject": m["subject"][:80]}
                          for m in to_leave],
    }

    print(f"\n=== {'DRY RUN ' if args.dry_run else ''}REPORT ===")
    print(f"Total: {len(messages)}  |  Would delete: {deleted}  |  Would archive: {archived}  |  Left: {len(to_leave)}")
    if to_leave:
        print("\nMessages left in inbox:")
        for m in to_leave[:20]:
            print(f"  [{m['domain']}] {m['subject'][:70]}")
        if len(to_leave) > 20:
            print(f"  ... and {len(to_leave) - 20} more")

    if args.report_json:
        Path(args.report_json).write_text(json.dumps(report, indent=2))
        print(f"\nReport written to {args.report_json}")

    mail.close()
    mail.logout()


if __name__ == "__main__":
    main()
