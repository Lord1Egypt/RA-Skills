#!/usr/bin/env python3
"""
IMAP IDLE Watcher Daemon

Maintains a persistent IMAP connection and uses IDLE to receive real-time
push notifications when new emails arrive. On notification, runs a
user-configured command.

No OAuth, no token expiry — uses app passwords.
Auto-reconnects on disconnect with exponential backoff.
"""

import imaplib
import email
import email.header
import os
import ssl
import sys
import time
import subprocess
import logging
import socket
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# ── Configuration (env vars) ──────────────────────────────────────────────

IMAP_ACCOUNT = os.environ.get("IMAP_ACCOUNT", "")
IMAP_PASSWORD = os.environ.get("IMAP_PASSWORD", "")
IMAP_HOST = os.environ.get("IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(os.environ.get("IMAP_PORT", "993"))
IMAP_FOLDER = os.environ.get("IMAP_FOLDER", "INBOX")

# Command to run when new mail arrives.
# Receives env vars: MAIL_FROM, MAIL_SUBJECT, MAIL_DATE, MAIL_UID
ON_NEW_MAIL_CMD = os.environ.get("ON_NEW_MAIL_CMD", "")

# Filters (optional). Comma-separated substrings, case-insensitive.
# If both set, both must match (AND). Within each, any value matches (OR).
FILTER_FROM = os.environ.get("FILTER_FROM", "")
FILTER_SUBJECT = os.environ.get("FILTER_SUBJECT", "")

# IDLE timeout — RFC says max 29min; renew every 20min to be safe
IDLE_TIMEOUT = int(os.environ.get("IDLE_TIMEOUT", str(20 * 60)))

# Min seconds between command runs (debounce)
DEBOUNCE_SECONDS = int(os.environ.get("DEBOUNCE_SECONDS", "10"))

# Reconnect backoff sequence (seconds)
RECONNECT_DELAYS = [5, 10, 30, 60, 120]

# ── State ─────────────────────────────────────────────────────────────────

_last_run = 0
_cmd_running = False


def _parse_filter(raw):
    """Parse comma-separated filter string into list of lowercase substrings."""
    if not raw or not raw.strip():
        return []
    return [v.strip().lower() for v in raw.split(",") if v.strip()]


def _matches_filter(value, patterns):
    """Check if value contains any of the patterns (case-insensitive OR)."""
    if not patterns:
        return True  # no filter = match all
    value_lower = value.lower()
    return any(p in value_lower for p in patterns)


def check_filters(mail_from, mail_subject):
    """
    Check if email matches configured filters.
    Both FILTER_FROM and FILTER_SUBJECT must match (AND).
    Within each filter, any comma-separated value matches (OR).
    Returns True if email should be processed.
    """
    from_patterns = _parse_filter(FILTER_FROM)
    subject_patterns = _parse_filter(FILTER_SUBJECT)

    from_ok = _matches_filter(mail_from, from_patterns)
    subject_ok = _matches_filter(mail_subject, subject_patterns)

    if not (from_ok and subject_ok):
        log.debug(f"Filtered out: from={mail_from!r} subject={mail_subject!r}")
        return False
    return True


def decode_header(raw):
    """Decode an email header value to a string."""
    if not raw:
        return ""
    parts = email.header.decode_header(raw)
    decoded = []
    for data, charset in parts:
        if isinstance(data, bytes):
            decoded.append(data.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(data)
    return " ".join(decoded)


def fetch_latest_metadata(imap):
    """Fetch metadata of the most recent unseen email."""
    status, data = imap.search(None, "UNSEEN")
    if status != "OK" or not data[0]:
        return None

    uids = data[0].split()
    latest_uid = uids[-1]

    status, msg_data = imap.fetch(latest_uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    if status != "OK":
        return None

    raw_header = msg_data[0][1]
    msg = email.message_from_bytes(raw_header)

    return {
        "uid": latest_uid.decode(),
        "from": decode_header(msg.get("From", "")),
        "subject": decode_header(msg.get("Subject", "")),
        "date": msg.get("Date", ""),
    }


def trigger_command(imap):
    """Run the configured command with email metadata as env vars."""
    global _last_run, _cmd_running

    if not ON_NEW_MAIL_CMD:
        log.info("No ON_NEW_MAIL_CMD configured — skipping.")
        return

    now = time.time()
    if _cmd_running:
        log.info("Command already running, skipping.")
        return
    if now - _last_run < DEBOUNCE_SECONDS:
        log.info("Debounce — command triggered too recently, skipping.")
        return

    _cmd_running = True
    _last_run = now

    # Try to get metadata for the command
    env = os.environ.copy()
    meta = None
    try:
        meta = fetch_latest_metadata(imap)
        if meta:
            env["MAIL_UID"] = meta["uid"]
            env["MAIL_FROM"] = meta["from"]
            env["MAIL_SUBJECT"] = meta["subject"]
            env["MAIL_DATE"] = meta["date"]
            log.info(f"📬 New mail: {meta['from']} — {meta['subject']}")
        else:
            log.info("📬 New mail signal (no unseen metadata available)")
    except Exception as e:
        log.warning(f"Could not fetch metadata: {e}")

    # Apply filters (skip if no metadata available to filter against)
    has_filters = FILTER_FROM or FILTER_SUBJECT
    if has_filters and meta and not check_filters(meta["from"], meta["subject"]):
        _cmd_running = False
        return

    log.info(f"🔄 Running: {ON_NEW_MAIL_CMD}")
    try:
        result = subprocess.run(
            ON_NEW_MAIL_CMD,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
            env=env,
        )
        log.info(f"✅ Command done (exit {result.returncode})")
        if result.stdout.strip():
            log.info(f"   stdout: {result.stdout.strip()[:500]}")
        if result.stderr.strip():
            log.warning(f"   stderr: {result.stderr.strip()[:500]}")
    except subprocess.TimeoutExpired:
        log.error("❌ Command timed out after 300s")
    except Exception as e:
        log.error(f"❌ Command error: {e}")
    finally:
        _cmd_running = False


def connect_imap():
    """Connect and authenticate to IMAP server."""
    if not IMAP_ACCOUNT or not IMAP_PASSWORD:
        log.error("IMAP_ACCOUNT and IMAP_PASSWORD must be set.")
        sys.exit(1)

    context = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context)
    imap.login(IMAP_ACCOUNT, IMAP_PASSWORD)
    imap.select(IMAP_FOLDER)
    log.info(f"✅ Connected to {IMAP_HOST} as {IMAP_ACCOUNT} [{IMAP_FOLDER}]")
    return imap


def idle_loop(imap):
    """
    Run IMAP IDLE loop. Blocks until new mail or timeout.
    Returns True if new mail detected, False on timeout.
    """
    tag = imap._new_tag().decode()
    imap.send(f"{tag} IDLE\r\n".encode())

    resp = imap.readline()
    if not resp.startswith(b"+"):
        raise RuntimeError(f"IDLE not accepted: {resp}")

    log.info(f"💤 IDLE active (renew in {IDLE_TIMEOUT // 60}min)...")
    imap.socket().settimeout(IDLE_TIMEOUT)

    new_mail = False
    try:
        while True:
            line = imap.readline()
            if not line:
                break
            line_str = line.decode("utf-8", errors="replace").strip()
            log.debug(f"IDLE: {line_str}")

            if "EXISTS" in line_str or "RECENT" in line_str or "FETCH" in line_str:
                log.info(f"📬 Signal: {line_str}")
                new_mail = True
                break
    except socket.timeout:
        log.info("⏱️ IDLE timeout — renewing...")
    finally:
        imap.send(b"DONE\r\n")
        imap.socket().settimeout(30)
        try:
            imap.readline()
        except Exception:
            pass

    return new_mail


def preflight():
    """Validate configuration before starting."""
    errors = []
    if not IMAP_ACCOUNT:
        errors.append("IMAP_ACCOUNT is not set")
    if not IMAP_PASSWORD:
        errors.append("IMAP_PASSWORD is not set")
    if not ON_NEW_MAIL_CMD:
        log.warning("⚠️  ON_NEW_MAIL_CMD is not set — daemon will watch but not run anything")

    if errors:
        for e in errors:
            log.error(f"❌ {e}")
        sys.exit(1)

    # Test connection
    log.info(f"🔍 Testing connection to {IMAP_HOST}:{IMAP_PORT}...")
    try:
        imap = connect_imap()
        # Check IDLE capability
        typ, caps = imap.capability()
        cap_str = caps[0].decode() if caps and caps[0] else ""
        if "IDLE" not in cap_str:
            log.error(f"❌ Server does not support IDLE. Capabilities: {cap_str}")
            sys.exit(1)
        log.info(f"✅ IDLE supported. Capabilities: {cap_str[:200]}")
        imap.logout()
    except imaplib.IMAP4.error as e:
        log.error(f"❌ Auth failed: {e}")
        log.error("   Check your credentials. For Gmail, use an App Password.")
        sys.exit(1)
    except Exception as e:
        log.error(f"❌ Connection failed: {e}")
        sys.exit(1)


def run():
    """Main daemon loop with auto-reconnect."""
    log.info("🚀 IMAP IDLE Watcher starting...")
    log.info(f"   Account:  {IMAP_ACCOUNT}")
    log.info(f"   Host:     {IMAP_HOST}:{IMAP_PORT}")
    log.info(f"   Folder:   {IMAP_FOLDER}")
    log.info(f"   Command:  {ON_NEW_MAIL_CMD or '(none)'}")

    preflight()

    delay_idx = 0

    while True:
        try:
            imap = connect_imap()
            delay_idx = 0

            while True:
                new_mail = idle_loop(imap)
                if new_mail:
                    trigger_command(imap)

        except imaplib.IMAP4.error as e:
            log.error(f"IMAP error: {e}")
        except (ConnectionError, OSError, socket.error) as e:
            log.error(f"Connection error: {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}", exc_info=True)

        delay = RECONNECT_DELAYS[min(delay_idx, len(RECONNECT_DELAYS) - 1)]
        delay_idx += 1
        log.info(f"🔁 Reconnecting in {delay}s...")
        time.sleep(delay)


if __name__ == "__main__":
    run()
