#!/usr/bin/env python3
"""Local Gmail IMAP/SMTP helper using Google App Passwords.

No third-party proxy is used. The app password is read from a local file.
"""

from __future__ import annotations

import argparse
import email
import imaplib
import os
import smtplib
import ssl
import sys
from email.header import decode_header, make_header
from email.message import EmailMessage, Message
from email.utils import parseaddr
from typing import Iterable


IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def _fail(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _credential() -> tuple[str, str]:
    address = os.environ.get("GMAIL_ADDRESS", "").strip()
    password_file = os.environ.get("GMAIL_APP_PASSWORD_FILE", "").strip()
    if not address:
        _fail("GMAIL_ADDRESS is not set")
    if not password_file:
        _fail("GMAIL_APP_PASSWORD_FILE is not set")
    password_path = os.path.expanduser(password_file)
    info = os.stat(password_path)
    if info.st_uid != os.getuid():
        _fail("GMAIL_APP_PASSWORD_FILE must be owned by the current user")
    if info.st_mode & 0o077:
        _fail("GMAIL_APP_PASSWORD_FILE must not be readable by group or others")
    with open(password_path, "r", encoding="utf-8") as handle:
        password = handle.read().strip()
    if not password:
        _fail("GMAIL_APP_PASSWORD_FILE is empty")
    return address, password


def _decode(value: str | None) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def _imap(mailbox: str = "INBOX") -> imaplib.IMAP4_SSL:
    address, password = _credential()
    conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    conn.login(address, password)
    status, _ = conn.select(mailbox, readonly=True)
    if status != "OK":
        conn.logout()
        _fail(f"cannot select mailbox: {mailbox}")
    return conn


def _message_text(msg: Message, max_chars: int) -> str:
    parts: list[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disposition = (part.get("Content-Disposition") or "").lower()
            if "attachment" in disposition:
                continue
            if ctype not in {"text/plain", "text/html"}:
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            charset = part.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace")
            if ctype == "text/plain":
                parts.insert(0, text)
            else:
                parts.append(text)
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            parts.append(payload.decode(charset, errors="replace"))
    body = "\n\n".join(p.strip() for p in parts if p.strip())
    if len(body) > max_chars:
        body = body[:max_chars] + "\n...[truncated]"
    return body


def _fetch_headers(conn: imaplib.IMAP4_SSL, uid: bytes) -> dict[str, str]:
    fields = b"(BODY.PEEK[HEADER.FIELDS (DATE FROM TO SUBJECT MESSAGE-ID)] RFC822.SIZE FLAGS)"
    status, data = conn.uid("FETCH", uid, fields)
    if status != "OK" or not data:
        return {}
    raw_header = b""
    for item in data:
        if isinstance(item, tuple):
            raw_header += item[1]
    msg = email.message_from_bytes(raw_header)
    return {
        "uid": uid.decode(),
        "date": _decode(msg.get("Date")),
        "from": _decode(msg.get("From")),
        "to": _decode(msg.get("To")),
        "subject": _decode(msg.get("Subject")),
        "message_id": _decode(msg.get("Message-ID")),
    }


def cmd_search(args: argparse.Namespace) -> None:
    conn = _imap(args.mailbox)
    try:
        criteria = args.query.strip() or "ALL"
        status, data = conn.uid("SEARCH", None, criteria)
        if status != "OK":
            _fail(f"search failed for query: {criteria}")
        uids = data[0].split() if data and data[0] else []
        for uid in uids[-args.limit :]:
            print(uid.decode())
    finally:
        conn.logout()


def cmd_list(args: argparse.Namespace) -> None:
    conn = _imap(args.mailbox)
    try:
        status, data = conn.uid("SEARCH", None, args.query)
        if status != "OK":
            _fail(f"search failed for query: {args.query}")
        uids = data[0].split() if data and data[0] else []
        for uid in reversed(uids[-args.limit :]):
            item = _fetch_headers(conn, uid)
            print(f"{item.get('uid','')}\t{item.get('date','')}\t{item.get('from','')}\t{item.get('subject','')}")
    finally:
        conn.logout()


def cmd_read(args: argparse.Namespace) -> None:
    conn = _imap(args.mailbox)
    try:
        status, data = conn.uid("FETCH", str(args.uid), "(RFC822)")
        if status != "OK" or not data:
            _fail(f"message not found: {args.uid}")
        raw = next((item[1] for item in data if isinstance(item, tuple)), None)
        if not raw:
            _fail(f"message body not returned: {args.uid}")
        msg = email.message_from_bytes(raw)
        print(f"UID: {args.uid}")
        print(f"Date: {_decode(msg.get('Date'))}")
        print(f"From: {_decode(msg.get('From'))}")
        print(f"To: {_decode(msg.get('To'))}")
        print(f"Subject: {_decode(msg.get('Subject'))}")
        print("")
        print(_message_text(msg, args.max_chars))
    finally:
        conn.logout()


def _split_addresses(values: Iterable[str] | None) -> list[str]:
    result: list[str] = []
    for value in values or []:
        for item in value.split(","):
            item = item.strip()
            if item:
                result.append(item)
    return result


def cmd_send(args: argparse.Namespace) -> None:
    if not args.confirm_send:
        _fail("send requires --confirm-send after explicit user approval")
    address, password = _credential()
    to_addrs = _split_addresses(args.to)
    cc_addrs = _split_addresses(args.cc)
    bcc_addrs = _split_addresses(args.bcc)
    if not to_addrs:
        _fail("at least one --to address is required")
    for addr in [*to_addrs, *cc_addrs, *bcc_addrs]:
        if not parseaddr(addr)[1]:
            _fail(f"invalid email address: {addr}")
    msg = EmailMessage()
    msg["From"] = address
    msg["To"] = ", ".join(to_addrs)
    if cc_addrs:
        msg["Cc"] = ", ".join(cc_addrs)
    msg["Subject"] = args.subject
    msg.set_content(args.body)
    context = ssl.create_default_context()
    recipients = [*to_addrs, *cc_addrs, *bcc_addrs]
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as smtp:
        smtp.login(address, password)
        smtp.send_message(msg, from_addr=address, to_addrs=recipients)
    print(f"sent: {len(recipients)} recipient(s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Gmail IMAP/SMTP helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("search", help="print matching message UIDs")
    p.add_argument("--mailbox", default="INBOX")
    p.add_argument("--query", default="ALL", help='IMAP search query, e.g. UNSEEN or FROM "a@b.com"')
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("list", help="list recent message headers")
    p.add_argument("--mailbox", default="INBOX")
    p.add_argument("--query", default="ALL")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("read", help="read message by UID")
    p.add_argument("--mailbox", default="INBOX")
    p.add_argument("--uid", required=True, type=int)
    p.add_argument("--max-chars", type=int, default=8000)
    p.set_defaults(func=cmd_read)

    p = sub.add_parser("send", help="send email over Gmail SMTP")
    p.add_argument("--to", action="append", required=True)
    p.add_argument("--cc", action="append")
    p.add_argument("--bcc", action="append")
    p.add_argument("--subject", required=True)
    p.add_argument("--body", required=True)
    p.add_argument("--confirm-send", action="store_true", help="required after explicit user approval")
    p.set_defaults(func=cmd_send)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
