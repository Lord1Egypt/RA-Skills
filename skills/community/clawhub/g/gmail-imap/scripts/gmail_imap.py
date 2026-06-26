#!/usr/bin/env python3
"""
gmail_imap.py — Gmail IMAP helper for OpenClaw agents.

Credentials from env:
  GMAIL_IMAP_USER      e.g. user@gmail.com
  GMAIL_IMAP_PASSWORD  App password (never print)

Commands:
  list   [--folder INBOX] [--limit 20] [--search CRITERION] [--unread]
  read   <uid> [--folder INBOX]
  search <query> [--limit 20] [--folder all]   (full-text Gmail search)
  trash  <uid> [--folder INBOX]
  move   <uid> <destination_folder>
  label  <uid> <label>
  send   --to ADDR --subject SUBJ --body TEXT [--html]

IMAP search examples (--search flag):
  UNSEEN                        unread messages
  FROM "someone@example.com"   from address
  SUBJECT "keyword"            subject contains
  SINCE 01-Apr-2026            after date (DD-Mon-YYYY)
  BEFORE 10-Apr-2026           before date
  TEXT "keyword"               body or header contains (header-only on some servers)

Full-text search (search subcommand uses Gmail X-GM-RAW):
  invoice                      any message containing "invoice"
  from:boss@example.com        Gmail search syntax
  is:unread subject:meeting    Gmail search syntax
"""

import imaplib
import email
import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

SERVER = "imap.gmail.com"
PORT = 993
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
TRASH = "[Gmail]/Trash"
ALL_MAIL = "[Gmail]/All Mail"


def connect():
    user = os.environ.get("GMAIL_IMAP_USER")
    password = os.environ.get("GMAIL_IMAP_PASSWORD")
    if not user or not password:
        sys.exit("ERROR: GMAIL_IMAP_USER and GMAIL_IMAP_PASSWORD must be set.")
    mail = imaplib.IMAP4_SSL(SERVER, PORT)
    mail.login(user, password)
    return mail, user, password


def decode_str(s):
    if s is None:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def imap_quote_folder(folder):
    """Quote folder name for IMAP if it contains spaces or special chars."""
    if ' ' in folder or any(c in folder for c in ['[', ']', '(', ')']):
        # Already quoted?
        if folder.startswith('"') and folder.endswith('"'):
            return folder
        return f'"{folder}"'
    return folder


def print_message_list(mail, uids, limit, use_uid=False):
    """Print a formatted table of messages given a list of UIDs."""
    uids = uids[-limit:]
    if not uids:
        print("No messages found.")
        return
    print(f"{'UID':<8} {'FROM':<30} {'DATE':<20} SUBJECT")
    print("-" * 90)
    for uid in reversed(uids):
        try:
            if use_uid:
                uid_str = uid.decode() if isinstance(uid, bytes) else str(uid)
                _, msg_data = mail.uid("FETCH", uid_str, "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])")
            else:
                _, msg_data = mail.fetch(uid, "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])")
            if not msg_data or msg_data[0] is None:
                continue
            raw = msg_data[0][1] if isinstance(msg_data[0], tuple) else msg_data[0]
            msg = email.message_from_bytes(raw)
            frm = decode_str(msg.get("From", ""))[:28]
            date = decode_str(msg.get("Date", ""))[:18]
            subj = decode_str(msg.get("Subject", ""))[:50]
            uid_display = uid.decode() if isinstance(uid, bytes) else str(uid)
            print(f"{uid_display:<8} {frm:<30} {date:<20} {subj}")
        except Exception as e:
            uid_display = uid.decode() if isinstance(uid, bytes) else str(uid)
            print(f"{uid_display:<8} (fetch error: {e})")


def cmd_list(args):
    mail, _, _ = connect()
    folder = getattr(args, "folder", "INBOX")
    limit = int(getattr(args, "limit", 20))
    search = getattr(args, "search", "ALL") or "ALL"

    # --unread shorthand
    if getattr(args, "unread", False):
        search = "UNSEEN"

    mail.select(imap_quote_folder(folder), readonly=True)
    _, data = mail.search(None, search)
    uids = data[0].split()
    print_message_list(mail, uids, limit)
    mail.logout()


def cmd_search(args):
    """Full-text search using Gmail's X-GM-RAW IMAP extension."""
    mail, _, _ = connect()
    query = args.query
    limit = int(getattr(args, "limit", 20))
    folder = getattr(args, "folder", ALL_MAIL)

    mail.select(imap_quote_folder(folder), readonly=True)

    # Try Gmail X-GM-RAW first (supports full Gmail search syntax including body)
    try:
        _, data = mail.uid("SEARCH", None, f'X-GM-RAW "{query}"')
        uids = data[0].split() if data and data[0] else []
    except Exception:
        # Fall back to standard IMAP TEXT search (headers + body, slower)
        _, data = mail.search(None, f'TEXT "{query}"')
        uids = data[0].split() if data and data[0] else []

    print(f"Search: {query!r}  ({len(uids)} results, showing {min(limit, len(uids))})")
    print()
    print_message_list(mail, uids, limit, use_uid=True)
    mail.logout()


def cmd_read(args):
    mail, _, _ = connect()
    folder = getattr(args, "folder", "INBOX")
    mail.select(imap_quote_folder(folder), readonly=True)
    uid = args.uid.encode()
    _, msg_data = mail.fetch(uid, "(RFC822)")
    if not msg_data or msg_data[0] is None:
        print(f"ERROR: UID {args.uid} not found in {folder}.")
        mail.logout()
        sys.exit(1)
    msg = email.message_from_bytes(msg_data[0][1])

    print(f"From:    {decode_str(msg.get('From'))}")
    print(f"To:      {decode_str(msg.get('To'))}")
    print(f"Date:    {decode_str(msg.get('Date'))}")
    print(f"Subject: {decode_str(msg.get('Subject'))}")
    print("-" * 60)

    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in disp:
                body = part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8", errors="replace"
                )
                print(body)
                break
    else:
        body = msg.get_payload(decode=True).decode(
            msg.get_content_charset() or "utf-8", errors="replace"
        )
        print(body)

    mail.logout()


def cmd_trash(args):
    """Move message to [Gmail]/Trash — the correct way to delete in Gmail."""
    mail, _, _ = connect()
    folder = getattr(args, "folder", "INBOX")
    mail.select(folder)
    uid = args.uid.encode()
    result = mail.uid("MOVE", uid, TRASH)
    if result[0] != "OK":
        mail.uid("COPY", uid, TRASH)
        mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
        mail.expunge()
    print(f"Moved UID {args.uid} to {TRASH}.")
    mail.logout()


def cmd_move(args):
    mail, _, _ = connect()
    mail.select("INBOX")
    uid = args.uid.encode()
    dest = args.destination
    result = mail.uid("MOVE", uid, dest)
    if result[0] != "OK":
        mail.uid("COPY", uid, dest)
        mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
        mail.expunge()
    print(f"Moved UID {args.uid} to {dest}.")
    mail.logout()


def cmd_label(args):
    """Apply a Gmail label to a message by copying to the label folder."""
    mail, _, _ = connect()
    mail.select("INBOX")
    uid = args.uid.encode()
    label_name = args.label

    typ, _ = mail.list('""', label_name)
    if typ != "OK":
        mail.create(label_name)

    result = mail.uid("COPY", uid, label_name)
    if result[0] == "OK":
        print(f"Applied label '{label_name}' to UID {args.uid}.")
    else:
        print(f"Warning: Could not apply label '{label_name}' to UID {args.uid}: {result[1]}")
    mail.logout()


def cmd_send(args):
    _, user, password = connect()
    msg = MIMEMultipart("alternative") if args.html else MIMEText(args.body, "plain")
    if args.html:
        msg.attach(MIMEText(args.body, "plain"))
        msg.attach(MIMEText(args.body, "html"))
    msg["From"] = user
    msg["To"] = args.to
    msg["Subject"] = args.subject
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(user, password)
        smtp.sendmail(user, [args.to], msg.as_string())
    print(f"Sent to {args.to}: {args.subject}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gmail IMAP helper")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="List messages")
    p_list.add_argument("--folder", default="INBOX")
    p_list.add_argument("--limit", type=int, default=20, help="Max messages to show (default: 20)")
    p_list.add_argument("--search", default="ALL", help='IMAP search criterion e.g. UNSEEN, FROM "x@y.com"')
    p_list.add_argument("--unread", action="store_true", help="Shorthand for --search UNSEEN")

    p_search = sub.add_parser("search", help="Full-text search via Gmail X-GM-RAW")
    p_search.add_argument("query", help='Gmail search query e.g. "invoice" or "from:boss is:unread"')
    p_search.add_argument("--limit", type=int, default=20, help="Max results to show (default: 20)")
    p_search.add_argument("--folder", default=ALL_MAIL, help=f"Folder to search (default: {ALL_MAIL})")

    p_read = sub.add_parser("read", help="Read a message by UID")
    p_read.add_argument("uid")
    p_read.add_argument("--folder", default="INBOX", help="Folder containing the message")

    p_trash = sub.add_parser("trash", help="Move message to Trash")
    p_trash.add_argument("uid")
    p_trash.add_argument("--folder", default="INBOX", help="Folder containing the message")

    p_move = sub.add_parser("move", help="Move message to a folder/label")
    p_move.add_argument("uid")
    p_move.add_argument("destination")

    p_label = sub.add_parser("label", help="Apply a Gmail label")
    p_label.add_argument("uid")
    p_label.add_argument("label")

    p_send = sub.add_parser("send", help="Send an email")
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--body", required=True)
    p_send.add_argument("--html", action="store_true")

    args = parser.parse_args()
    dispatch = {
        "list": cmd_list,
        "search": cmd_search,
        "read": cmd_read,
        "trash": cmd_trash,
        "move": cmd_move,
        "label": cmd_label,
        "send": cmd_send,
    }
    if args.command not in dispatch:
        parser.print_help()
        sys.exit(1)
    dispatch[args.command](args)
