#!/usr/bin/env python3
"""
📧 Gmail Lead Monitor
======================
Monitor Gmail inbox via IMAP and send Telegram alerts for important emails.
Zero dependencies beyond Python stdlib.

Usage:
    python3 gmail_monitor.py              # daemon mode (uses config interval)
    python3 gmail_monitor.py --once       # check once and exit
    python3 gmail_monitor.py --interval 10  # custom interval in minutes

Config: ~/.config/gmail_monitor/config.json
{
    "email": "you@gmail.com",
    "app_password": "xxxx xxxx xxxx xxxx",
    "telegram_token": "bot_token",
    "telegram_chat_id": "chat_id",
    "keywords": ["order", "purchase", "setup", "interested", "question"],
    "check_interval_minutes": 5,
    "max_emails_per_check": 20
}
"""

import imaplib
import email
import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from email.header import decode_header
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

CONFIG_PATH  = Path.home() / ".config" / "gmail_monitor" / "config.json"
STATE_FILE   = Path.home() / ".config" / "gmail_monitor" / "seen_ids.json"
GMAIL_IMAP   = "imap.gmail.com"
GMAIL_PORT   = 993


# ── Config ────────────────────────────────────────────────────────────────────

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"[gmail] Config not found: {CONFIG_PATH}")
        print("[gmail] Create it with: email, app_password, telegram_token, telegram_chat_id, keywords")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_seen() -> set:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            # Keep only last 5000 IDs
            ids = data.get("ids", [])
            return set(ids[-5000:])
        except Exception:
            pass
    return set()


def save_seen(seen: set):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ids = sorted(seen)[-5000:]  # trim to 5k most recent
    STATE_FILE.write_text(json.dumps({"ids": ids}, indent=2))


# ── Email helpers ─────────────────────────────────────────────────────────────

def decode_mime_header(value: str) -> str:
    """Decode encoded email header (handles UTF-8, base64, etc.)."""
    if not value:
        return ""
    parts = decode_header(value)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                decoded.append(part.decode(charset or "utf-8", errors="replace"))
            except Exception:
                decoded.append(part.decode("utf-8", errors="replace"))
        else:
            decoded.append(str(part))
    return " ".join(decoded).strip()


def get_body_snippet(msg: email.message.Message, max_chars: int = 300) -> str:
    """Extract first N chars of email body."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode("utf-8", errors="replace").strip()
                    break
            elif content_type == "text/html" and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    # Very basic HTML strip
                    text = payload.decode("utf-8", errors="replace")
                    import re
                    text = re.sub(r"<[^>]+>", " ", text)
                    text = re.sub(r"\s+", " ", text).strip()
                    body = text[:max_chars]
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode("utf-8", errors="replace").strip()

    return body[:max_chars].strip()


def is_important(subject: str, sender: str, body: str, keywords: list) -> tuple[bool, str]:
    """Check if email matches any keyword. Returns (is_important, matched_keyword)."""
    check_text = f"{subject} {sender} {body}".lower()
    for kw in keywords:
        if kw.lower() in check_text:
            return True, kw
    return False, ""


# ── Telegram ──────────────────────────────────────────────────────────────────

def send_telegram(token: str, chat_id: str, message: str) -> bool:
    """Send Telegram message. Returns True on success."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        print(f"[gmail] Telegram error {e.code}: {e.read().decode()[:100]}")
        return False
    except Exception as e:
        print(f"[gmail] Telegram error: {e}")
        return False


def format_alert(sender: str, subject: str, snippet: str,
                 timestamp: str, is_important: bool, keyword: str) -> str:
    """Format Telegram alert message."""
    icon = "📧⭐" if is_important else "📧"
    msg = (
        f"{icon} <b>New Email</b>\n"
        f"<b>From:</b> {sender}\n"
        f"<b>Subject:</b> {subject}\n"
        f"<b>Time:</b> {timestamp}\n"
    )
    if snippet:
        msg += f"\n<i>{snippet[:200]}...</i>\n"
    if is_important:
        msg += f"\n⭐ <b>Flagged as important</b> (keyword: {keyword})"
    return msg


# ── Gmail IMAP ────────────────────────────────────────────────────────────────

def check_gmail(config: dict, seen: set) -> list[dict]:
    """
    Connect to Gmail, fetch UNSEEN emails, return list of new email dicts.
    Marks important emails with STARRED flag.
    """
    email_addr   = config["email"]
    app_password = config["app_password"].replace(" ", "")
    keywords     = config.get("keywords", ["order", "purchase", "setup", "interested", "question"])
    max_check    = config.get("max_emails_per_check", 20)

    new_emails = []

    try:
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP, GMAIL_PORT)
        mail.login(email_addr, app_password)
        mail.select("INBOX")

        # Search for UNSEEN emails
        status, data = mail.search(None, "UNSEEN")
        if status != "OK" or not data[0]:
            mail.logout()
            return []

        email_ids = data[0].split()
        # Most recent first, limit to max_check
        email_ids = email_ids[::-1][:max_check]

        for eid in email_ids:
            # Fetch headers + body
            status, msg_data = mail.fetch(eid, "(RFC822)")
            if status != "OK":
                continue

            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)

            msg_id = msg.get("Message-ID", "").strip()
            if not msg_id:
                msg_id = f"eid_{eid.decode()}"

            if msg_id in seen:
                continue

            sender  = decode_mime_header(msg.get("From", ""))
            subject = decode_mime_header(msg.get("Subject", "(no subject)"))
            snippet = get_body_snippet(msg)

            # Parse timestamp
            date_str = msg.get("Date", "")
            try:
                dt = parsedate_to_datetime(date_str)
                timestamp = dt.strftime("%Y-%m-%d %H:%M %Z")
            except Exception:
                timestamp = date_str[:25] if date_str else "unknown"

            important, keyword = is_important(subject, sender, snippet, keywords)

            # Star important emails
            if important:
                try:
                    mail.store(eid, "+FLAGS", "\\Flagged")
                except Exception:
                    pass

            seen.add(msg_id)
            new_emails.append({
                "msg_id":    msg_id,
                "sender":    sender,
                "subject":   subject,
                "snippet":   snippet,
                "timestamp": timestamp,
                "important": important,
                "keyword":   keyword,
            })

        mail.logout()

    except imaplib.IMAP4.error as e:
        print(f"[gmail] IMAP error: {e}")
        if "authentication" in str(e).lower():
            print("[gmail] Check your app password at myaccount.google.com/security")
    except Exception as e:
        print(f"[gmail] Error: {e}")

    return new_emails


# ── Main ──────────────────────────────────────────────────────────────────────

def run_once(config: dict, seen: set) -> int:
    """Check Gmail once. Returns number of new emails alerted."""
    token   = config.get("telegram_token", "")
    chat_id = config.get("telegram_chat_id", "")

    new_emails = check_gmail(config, seen)

    if not new_emails:
        print(f"[gmail] {datetime.now().strftime('%H:%M')} — No new emails")
        return 0

    print(f"[gmail] {len(new_emails)} new email(s) found")
    alerted = 0
    for e in new_emails:
        print(f"  {'⭐' if e['important'] else '  '} {e['sender'][:30]:<30}  {e['subject'][:50]}")
        if token and chat_id:
            msg = format_alert(
                e["sender"], e["subject"], e["snippet"],
                e["timestamp"], e["important"], e["keyword"]
            )
            ok = send_telegram(token, chat_id, msg)
            if ok:
                alerted += 1

    save_seen(seen)
    return alerted


def main():
    parser = argparse.ArgumentParser(description="Gmail Lead Monitor")
    parser.add_argument("--once",     action="store_true", help="Check once and exit")
    parser.add_argument("--interval", type=int, default=None,
                        help="Override check interval in minutes")
    args = parser.parse_args()

    config   = load_config()
    seen     = load_seen()
    interval = args.interval or config.get("check_interval_minutes", 5)

    print(f"[gmail] Gmail Lead Monitor | {config['email']} | interval={interval}m")
    print(f"[gmail] Keywords: {config.get('keywords', [])}")

    if args.once:
        run_once(config, seen)
        return

    print(f"[gmail] Daemon mode: checking every {interval} minutes. Ctrl-C to stop.")
    while True:
        try:
            run_once(config, seen)
        except KeyboardInterrupt:
            print("[gmail] Stopped.")
            break
        except Exception as e:
            print(f"[gmail] Unexpected error: {e}")
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()
