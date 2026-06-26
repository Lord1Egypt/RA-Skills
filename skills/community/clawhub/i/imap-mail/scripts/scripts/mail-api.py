#!/usr/bin/env python3
"""
IMAP Mail API — REST bridge over IMAP/SMTP.
Listens on 127.0.0.1:8025 by default.

Configuration via environment variables or env file (IMAP_MAIL_ENV).
See SKILL.md for full setup instructions.
"""

import base64
import email
import email.header
import email.utils
import imaplib
import json
import smtplib
import socket
import sqlite3
import ssl
import os
import re
import threading
import time
import urllib.request
from contextlib import contextmanager
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

# Load env file if present
_env_file = os.getenv("IMAP_MAIL_ENV", "/etc/imap-mail.env")
if Path(_env_file).exists():
    for line in Path(_env_file).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

try:
    from fastapi import FastAPI, HTTPException, Query
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    raise SystemExit("Missing dependencies. Run: pip3 install fastapi uvicorn")

# ── Config ─────────────────────────────────────────────────────────────────

IMAP_HOST     = os.getenv("MAIL_IMAP_HOST", "")
IMAP_PORT     = int(os.getenv("MAIL_IMAP_PORT", "993"))
SMTP_HOST     = os.getenv("MAIL_SMTP_HOST", "")
SMTP_PORT     = int(os.getenv("MAIL_SMTP_PORT", "465"))
MAIL_USER     = os.getenv("MAIL_USER", "")
MAIL_PASS     = os.getenv("MAIL_PASS", "")
FROM_NAME     = os.getenv("MAIL_FROM_NAME", "Agent")
LISTEN_PORT   = int(os.getenv("IMAP_MAIL_PORT", "8025"))

# IMAP IDLE + VIP
IDLE_WEBHOOK  = os.getenv("MAIL_IDLE_WEBHOOK", "")
IDLE_FOLDER   = os.getenv("MAIL_IDLE_FOLDER", "INBOX")
VIP_SENDERS   = {
    s.strip().lower()
    for s in os.getenv("MAIL_VIP_SENDERS", "").split(",")
    if s.strip()
}

# Scheduled send
SCHEDULED_DB  = os.getenv("MAIL_SCHEDULED_DB", "/tmp/imap-mail-scheduled.db")

if not IMAP_HOST or not MAIL_USER or not MAIL_PASS:
    raise SystemExit(
        "Missing required env vars: MAIL_IMAP_HOST, MAIL_USER, MAIL_PASS\n"
        f"Looked for env file at: {_env_file}"
    )

_allow_self_signed = os.getenv("MAIL_ALLOW_SELF_SIGNED", "").lower() in ("1", "true", "yes")
SSL_CTX = ssl._create_unverified_context() if _allow_self_signed else ssl.create_default_context()

# ── IMAP helpers ───────────────────────────────────────────────────────────

@contextmanager
def imap_conn():
    m = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=SSL_CTX)
    try:
        m.login(MAIL_USER, MAIL_PASS)
        yield m
    finally:
        try:
            m.logout()
        except Exception:
            pass


def decode_header_value(raw: str) -> str:
    parts = email.header.decode_header(raw or "")
    result = []
    for chunk, enc in parts:
        if isinstance(chunk, bytes):
            result.append(chunk.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(str(chunk))
    return "".join(result)


def parse_address_list(header_val: str) -> list:
    if not header_val:
        return []
    return [
        {"name": decode_header_value(name), "email": addr}
        for name, addr in email.utils.getaddresses([header_val])
        if addr
    ]


def msg_to_dict(uid: str, raw_bytes: bytes, folder: str = "INBOX") -> dict:
    msg = email.message_from_bytes(raw_bytes)

    subject     = decode_header_value(msg.get("Subject", ""))
    from_list   = parse_address_list(msg.get("From", ""))
    to_list     = parse_address_list(msg.get("To", ""))
    cc_list     = parse_address_list(msg.get("Cc", ""))
    message_id  = msg.get("Message-ID", f"uid-{uid}").strip()
    in_reply_to = msg.get("In-Reply-To", "").strip()
    references  = msg.get("References", "").strip()

    try:
        ts = email.utils.parsedate_to_datetime(msg.get("Date", ""))
        timestamp = ts.astimezone(timezone.utc).isoformat()
    except Exception:
        timestamp = datetime.now(timezone.utc).isoformat()

    thread_id = (
        in_reply_to
        or (references.split()[0] if references else "")
        or message_id
    )

    text_body, html_body, attachments = "", "", []

    if msg.is_multipart():
        for part in msg.walk():
            ct   = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if "attachment" in disp:
                attachments.append({
                    "filename":     part.get_filename() or "attachment",
                    "content_type": ct,
                    "size":         len(part.get_payload(decode=True) or b""),
                })
            elif ct == "text/plain" and not text_body:
                text_body = (part.get_payload(decode=True) or b"").decode(
                    part.get_content_charset() or "utf-8", errors="replace"
                )
            elif ct == "text/html" and not html_body:
                html_body = (part.get_payload(decode=True) or b"").decode(
                    part.get_content_charset() or "utf-8", errors="replace"
                )
    else:
        payload   = msg.get_payload(decode=True) or b""
        text_body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")

    preview = re.sub(r"\s+", " ", text_body).strip()[:200]

    # VIP flag
    vip = any(a.get("email", "").lower() in VIP_SENDERS for a in from_list) if VIP_SENDERS else False

    return {
        "message_id":  message_id,
        "thread_id":   thread_id,
        "inbox_id":    MAIL_USER,
        "folder":      folder,
        "subject":     subject,
        "from_":       from_list,
        "to":          to_list,
        "cc":          cc_list,
        "timestamp":   timestamp,
        "text":        text_body,
        "html":        html_body,
        "preview":     preview,
        "in_reply_to": in_reply_to,
        "references":  references,
        "labels":      [],
        "attachments": attachments,
        "uid":         uid,
        "vip":         vip,
    }


def fetch_uids(m: imaplib.IMAP4_SSL, criteria: str = "ALL") -> list[bytes]:
    typ, data = m.search(None, criteria)
    if typ != "OK" or not data[0]:
        return []
    return data[0].split()


def fetch_messages(m: imaplib.IMAP4_SSL, uids: list[bytes], folder: str) -> list[dict]:
    results = []
    for uid in uids:
        typ, raw = m.fetch(uid, "(RFC822)")
        if typ != "OK" or not raw or not isinstance(raw[0], tuple):
            continue
        results.append(msg_to_dict(uid.decode(), raw[0][1], folder))
    return results


# ── Folder helpers ─────────────────────────────────────────────────────────

def list_folders_imap() -> list[dict]:
    with imap_conn() as m:
        typ, data = m.list()
        if typ != "OK":
            return []
        folders = []
        for item in data:
            if not item:
                continue
            decoded = item.decode() if isinstance(item, bytes) else item
            # Parse: (\HasNoChildren) "/" "INBOX"
            match = re.match(r'\(([^)]*)\)\s+"([^"]+)"\s+"?([^"]+)"?', decoded)
            if match:
                flags_str, sep, name = match.groups()
                flags = [f.strip().lstrip("\\") for f in flags_str.split() if f.strip()]
                folders.append({"name": name.strip(), "flags": flags, "delimiter": sep})
        return folders


# ── Search helpers ─────────────────────────────────────────────────────────

def build_imap_search(
    from_: str = "", to: str = "", subject: str = "",
    body: str = "", since: str = "", before: str = "",
    unseen: bool = False, seen: bool = False,
    flagged: bool = False, unflagged: bool = False,
    has_attachments: bool = False,
) -> str:
    """Build IMAP SEARCH criteria string."""
    parts = []
    if unseen:
        parts.append("UNSEEN")
    if seen:
        parts.append("SEEN")
    if flagged:
        parts.append("FLAGGED")
    if unflagged:
        parts.append("UNFLAGGED")
    if from_:
        parts.append(f'FROM "{from_}"')
    if to:
        parts.append(f'TO "{to}"')
    if subject:
        parts.append(f'SUBJECT "{subject}"')
    if body:
        parts.append(f'BODY "{body}"')
    if since:
        try:
            dt = datetime.fromisoformat(since)
            parts.append(f'SINCE {dt.strftime("%d-%b-%Y")}')
        except ValueError:
            parts.append(f'SINCE {since}')
    if before:
        try:
            dt = datetime.fromisoformat(before)
            parts.append(f'BEFORE {dt.strftime("%d-%b-%Y")}')
        except ValueError:
            parts.append(f'BEFORE {before}')
    return " ".join(parts) if parts else "ALL"


# ── SMTP helpers ───────────────────────────────────────────────────────────

def send_email(to: list, subject: str, text: str, html: str = "",
               in_reply_to: str = "", references: str = "") -> str:
    if html:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(text, "plain", "utf-8"))
        msg.attach(MIMEText(html,  "html",  "utf-8"))
    else:
        msg = MIMEText(text, "plain", "utf-8")

    msg["From"]       = email.utils.formataddr((FROM_NAME, MAIL_USER))
    msg["To"]         = ", ".join(to)
    msg["Subject"]    = subject
    msg["Message-ID"] = email.utils.make_msgid(domain=MAIL_USER.split("@")[1])
    msg["Date"]       = email.utils.formatdate(localtime=True)
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references

    smtp_host = SMTP_HOST or IMAP_HOST
    with smtplib.SMTP_SSL(smtp_host, SMTP_PORT, context=SSL_CTX, timeout=15) as s:
        s.login(MAIL_USER, MAIL_PASS)
        s.sendmail(MAIL_USER, to, msg.as_bytes())

    return msg["Message-ID"]


def group_threads(messages: list) -> list:
    threads: dict = {}
    for msg in messages:
        tid = msg["thread_id"]
        if tid not in threads:
            threads[tid] = {
                "thread_id":       tid,
                "subject":         msg["subject"],
                "participants":    [],
                "message_count":   0,
                "last_message_at": msg["timestamp"],
                "folder":          msg.get("folder", "INBOX"),
            }
        t = threads[tid]
        t["message_count"] += 1
        for addr in msg.get("from_", []):
            e = addr.get("email", "")
            if e and e not in t["participants"]:
                t["participants"].append(e)
        if msg["timestamp"] > t["last_message_at"]:
            t["last_message_at"] = msg["timestamp"]
    return list(threads.values())


# ── IMAP IDLE watcher ──────────────────────────────────────────────────────

_idle_status = {"running": False, "last_event": None, "error": None}


def _post_webhook(payload: dict):
    if not IDLE_WEBHOOK:
        return
    try:
        data = json.dumps(payload, default=str).encode()
        req  = urllib.request.Request(
            IDLE_WEBHOOK, data=data,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        _idle_status["error"] = f"webhook: {e}"


def _idle_loop(stop_event: threading.Event):
    """Background thread: IMAP IDLE push watcher."""
    _idle_status["running"] = True
    while not stop_event.is_set():
        conn = None
        try:
            conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=SSL_CTX)
            conn.login(MAIL_USER, MAIL_PASS)
            conn.select(f'"{IDLE_FOLDER}"')

            while not stop_event.is_set():
                # Enter IDLE
                tag = conn._new_tag()
                conn.send(tag + b" IDLE\r\n")
                line = conn.readline()
                if not line.startswith(b"+"):
                    break  # server didn't accept IDLE

                # Wait up to 28 min for EXISTS/RECENT notification
                conn.socket().settimeout(28 * 60)
                got_new = False
                try:
                    while True:
                        line = conn.readline()
                        if b"EXISTS" in line or b"RECENT" in line:
                            got_new = True
                        if not line or b"BYE" in line:
                            break
                except OSError:
                    pass  # socket timeout — reconnect

                # Exit IDLE
                try:
                    conn.send(b"DONE\r\n")
                    conn.readline()
                    conn.socket().settimeout(None)
                except Exception:
                    break

                if got_new:
                    typ, data = conn.search(None, "UNSEEN")
                    if typ == "OK" and data[0]:
                        uids = data[0].split()[-10:]
                        msgs = fetch_messages(conn, uids, IDLE_FOLDER)
                        for msg in msgs:
                            _idle_status["last_event"] = msg["timestamp"]
                            _post_webhook({**msg, "event": "new_mail"})

        except Exception as e:
            _idle_status["error"] = str(e)
        finally:
            if conn:
                try:
                    conn.logout()
                except Exception:
                    pass

        if not stop_event.is_set():
            stop_event.wait(30)  # back-off before reconnect

    _idle_status["running"] = False


_idle_stop  = threading.Event()
_idle_thread: Optional[threading.Thread] = None

if IDLE_WEBHOOK:
    _idle_thread = threading.Thread(target=_idle_loop, args=(_idle_stop,), daemon=True)
    _idle_thread.start()


# ── Scheduled send ─────────────────────────────────────────────────────────

def _init_scheduled_db():
    with sqlite3.connect(SCHEDULED_DB) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                email       TEXT PRIMARY KEY,
                name        TEXT DEFAULT '',
                notes       TEXT DEFAULT '',
                tags        TEXT DEFAULT '',
                message_count INTEGER DEFAULT 0,
                last_seen   TEXT,
                created_at  TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                inbox       TEXT,
                folder      TEXT DEFAULT 'INBOX',
                match_field TEXT,
                match_value TEXT,
                action      TEXT DEFAULT 'flag',
                enabled     INTEGER DEFAULT 1,
                created_at  TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS scheduled (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                inbox       TEXT,
                to_json     TEXT,
                subject     TEXT,
                body_text   TEXT,
                body_html   TEXT,
                in_reply_to TEXT,
                refs        TEXT,
                send_at     TEXT,
                sent        INTEGER DEFAULT 0,
                error       TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT
            )
        """)


def _scheduled_loop():
    """Background thread: send scheduled messages when due."""
    while True:
        try:
            now = datetime.now(timezone.utc).isoformat()
            with sqlite3.connect(SCHEDULED_DB) as db:
                rows = db.execute(
                    "SELECT id, to_json, subject, body_text, body_html, in_reply_to, refs "
                    "FROM scheduled WHERE sent=0 AND error IS NULL AND send_at <= ?",
                    (now,)
                ).fetchall()
                for row in rows:
                    id_, to_json, subject, text, html, irt, refs = row
                    try:
                        send_email(json.loads(to_json), subject, text or "", html or "", irt or "", refs or "")
                        db.execute("UPDATE scheduled SET sent=1 WHERE id=?", (id_,))
                    except Exception as e:
                        db.execute("UPDATE scheduled SET error=? WHERE id=?", (str(e), id_))
        except Exception:
            pass
        time.sleep(60)


_init_scheduled_db()
threading.Thread(target=_scheduled_loop, daemon=True).start()


# ── FastAPI app ────────────────────────────────────────────────────────────

app = FastAPI(title="IMAP Mail API", version="1.2.1")


@app.get("/health")
def health():
    return {
        "status":       "ok",
        "inbox":        MAIL_USER,
        "imap_host":    IMAP_HOST,
        "idle_active":  _idle_thread is not None and _idle_thread.is_alive(),
        "vip_senders":  sorted(VIP_SENDERS),
    }


# ── IDLE status ────────────────────────────────────────────────────────────

@app.get("/idle/status")
def idle_status():
    """Current state of the IMAP IDLE watcher."""
    return {
        **_idle_status,
        "webhook":     IDLE_WEBHOOK or None,
        "folder":      IDLE_FOLDER,
        "vip_senders": sorted(VIP_SENDERS),
    }


# ── Folders ────────────────────────────────────────────────────────────────

@app.get("/inboxes/{inbox}/folders")
def list_folders(inbox: str):
    """List all IMAP folders/mailboxes."""
    try:
        return {"folders": list_folders_imap()}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/inboxes/{inbox}/folders", status_code=201)
def create_folder(inbox: str, body: dict):
    """Create a new IMAP folder."""
    name = body.get("name", "").strip()
    if not name:
        raise HTTPException(400, "folder name required")
    try:
        with imap_conn() as m:
            typ, data = m.create(f'"{name}"')
            if typ != "OK":
                raise HTTPException(500, f"IMAP error: {data}")
        return {"name": name, "created": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/inboxes/{inbox}/folders/{folder_name}", status_code=200)
def delete_folder(inbox: str, folder_name: str):
    """Delete an IMAP folder."""
    try:
        with imap_conn() as m:
            typ, data = m.delete(f'"{folder_name}"')
            if typ != "OK":
                raise HTTPException(500, f"IMAP error: {data}")
        return {"name": folder_name, "deleted": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Messages ───────────────────────────────────────────────────────────────

@app.get("/inboxes/{inbox}/messages")
def list_messages(
    inbox: str,
    folder: str = Query(default="INBOX"),
    limit: int  = Query(default=20, le=100),
    unseen: bool = Query(default=False),
):
    """List messages from any folder, newest first."""
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"', readonly=True)
            criteria = "UNSEEN" if unseen else "ALL"
            uids = fetch_uids(m, criteria)
            uids = uids[-limit:][::-1]
            msgs = fetch_messages(m, uids, folder)
        return {"messages": msgs, "total": len(msgs), "folder": folder}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/inboxes/{inbox}/messages/{uid}")
def get_message(inbox: str, uid: str, folder: str = Query(default="INBOX")):
    """Fetch a single message by IMAP UID."""
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"', readonly=True)
            typ, raw = m.fetch(uid.encode(), "(RFC822)")
            if typ != "OK" or not raw or not isinstance(raw[0], tuple):
                raise HTTPException(404, "Message not found")
            return msg_to_dict(uid, raw[0][1], folder)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/inboxes/{inbox}/messages/{uid}/attachments/{index}")
def get_attachment(inbox: str, uid: str, index: int,
                   folder: str = Query(default="INBOX")):
    """Download a specific attachment by index (base64-encoded)."""
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"', readonly=True)
            typ, raw = m.fetch(uid.encode(), "(RFC822)")
            if typ != "OK" or not raw or not isinstance(raw[0], tuple):
                raise HTTPException(404, "Message not found")
            msg = email.message_from_bytes(raw[0][1])
            parts = [
                p for p in msg.walk()
                if "attachment" in str(p.get("Content-Disposition", ""))
            ]
            if index >= len(parts):
                raise HTTPException(404, f"Attachment index {index} not found (total: {len(parts)})")
            part = parts[index]
            data = part.get_payload(decode=True) or b""
            return {
                "filename":     part.get_filename() or f"attachment-{index}",
                "content_type": part.get_content_type(),
                "data":         base64.b64encode(data).decode(),
                "size":         len(data),
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


class SendRequest(BaseModel):
    to: list[str]
    subject: str
    text: str = ""
    html: str = ""
    in_reply_to: str = ""
    references: str = ""


@app.post("/inboxes/{inbox}/messages", status_code=201)
def send_message(inbox: str, body: SendRequest):
    """Send an email via SMTP."""
    try:
        msg_id = send_email(
            to=body.to, subject=body.subject,
            text=body.text, html=body.html,
            in_reply_to=body.in_reply_to, references=body.references,
        )
        return {"message_id": msg_id, "status": "sent"}
    except Exception as e:
        raise HTTPException(500, str(e))


class MoveRequest(BaseModel):
    destination: str


@app.post("/inboxes/{inbox}/messages/{uid}/move")
def move_message(inbox: str, uid: str, body: MoveRequest,
                 folder: str = Query(default="INBOX")):
    """Move a message to another folder."""
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"')
            typ, data = m.uid("COPY", uid.encode(), f'"{body.destination}"')
            if typ != "OK":
                raise HTTPException(500, f"COPY failed: {data}")
            m.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
            m.expunge()
        return {"uid": uid, "moved_to": body.destination}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/inboxes/{inbox}/messages/{uid}")
def delete_message(inbox: str, uid: str, folder: str = Query(default="INBOX")):
    """Delete (expunge) a message."""
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"')
            m.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
            m.expunge()
        return {"uid": uid, "deleted": True}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Mark seen ──────────────────────────────────────────────────────────────

@app.post("/inboxes/{inbox}/mark-seen")
def mark_all_seen(
    inbox: str,
    folder: str = Query(default="INBOX"),
    uid: str = Query(default="", description="Single UID to mark seen (omit for all)"),
):
    """Mark one, several, or all messages in a folder as read (\\Seen flag).
    uid can be a single UID or comma-separated list: '42,55,73'
    """
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"')
            if uid:
                m.uid("STORE", uid.encode(), "+FLAGS", "\\Seen")
            else:
                m.store(b"1:*", "+FLAGS", "\\Seen")
        label = f"uid:{uid}" if uid else "all messages"
        return {"folder": folder, "marked_seen": label}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Flag (star) ────────────────────────────────────────────────────────────

@app.post("/inboxes/{inbox}/flag")
def flag_messages(
    inbox: str,
    folder: str  = Query(default="INBOX"),
    uid: str     = Query(default="", description="UID or comma-separated UIDs: '42,55,73'"),
    sender: str  = Query(default="", description="Flag all messages from this address"),
    unflag: bool = Query(default=False, description="Remove flag instead of setting it"),
):
    """Set or remove \\Flagged (star) on messages — by UID list or by sender address."""
    flag_op = "-FLAGS" if unflag else "+FLAGS"
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"')

            if sender:
                # Find all messages from this sender, then flag them
                typ, data = m.uid("SEARCH", None, f'FROM "{sender}"')
                if typ != "OK" or not data[0]:
                    return {"folder": folder, "flagged": [], "sender": sender}
                uids = data[0].decode().split()
                for u in uids:
                    m.uid("STORE", u.encode(), flag_op, "\\Flagged")
                label = f"{len(uids)} message(s) from {sender}"
                return {"folder": folder, "flagged": uids, "sender": sender, "count": len(uids)}

            if uid:
                m.uid("STORE", uid.encode(), flag_op, "\\Flagged")
                label = f"uid:{uid}"
            else:
                m.store(b"1:*", flag_op, "\\Flagged")
                label = "all messages"

        action = "unflagged" if unflag else "flagged"
        return {"folder": folder, action: label}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Auto-rules ─────────────────────────────────────────────────────────────

class RuleRequest(BaseModel):
    match_field: str   # "from", "subject", "to"
    match_value: str   # e.g. "craig@example.com"
    action: str = "flag"  # currently only "flag" supported
    folder: str = "INBOX"


@app.get("/inboxes/{inbox}/rules")
def list_rules(inbox: str):
    """List all auto-rules for this inbox."""
    with sqlite3.connect(SCHEDULED_DB) as db:
        rows = db.execute(
            "SELECT id, folder, match_field, match_value, action, enabled, created_at "
            "FROM rules WHERE inbox=? ORDER BY id",
            (inbox,)
        ).fetchall()
    return {"rules": [
        {"id": r[0], "folder": r[1], "match_field": r[2], "match_value": r[3],
         "action": r[4], "enabled": bool(r[5]), "created_at": r[6]}
        for r in rows
    ]}


@app.post("/inboxes/{inbox}/rules", status_code=201)
def create_rule(inbox: str, body: RuleRequest):
    """Create a new auto-rule (e.g. auto-flag all mail from a sender)."""
    now = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(SCHEDULED_DB) as db:
        cur = db.execute(
            "INSERT INTO rules (inbox, folder, match_field, match_value, action, enabled, created_at) "
            "VALUES (?,?,?,?,?,1,?)",
            (inbox, body.folder, body.match_field, body.match_value, body.action, now)
        )
    return {"id": cur.lastrowid, "match_field": body.match_field,
            "match_value": body.match_value, "action": body.action, "enabled": True}


@app.delete("/inboxes/{inbox}/rules/{rule_id}")
def delete_rule(inbox: str, rule_id: int):
    """Delete an auto-rule."""
    with sqlite3.connect(SCHEDULED_DB) as db:
        row = db.execute("SELECT id FROM rules WHERE id=? AND inbox=?", (rule_id, inbox)).fetchone()
        if not row:
            raise HTTPException(404, "Rule not found")
        db.execute("DELETE FROM rules WHERE id=?", (rule_id,))
    return {"id": rule_id, "deleted": True}


@app.patch("/inboxes/{inbox}/rules/{rule_id}")
def toggle_rule(inbox: str, rule_id: int, body: dict):
    """Enable or disable a rule. Body: {"enabled": true/false}"""
    enabled = 1 if body.get("enabled", True) else 0
    with sqlite3.connect(SCHEDULED_DB) as db:
        row = db.execute("SELECT id FROM rules WHERE id=? AND inbox=?", (rule_id, inbox)).fetchone()
        if not row:
            raise HTTPException(404, "Rule not found")
        db.execute("UPDATE rules SET enabled=? WHERE id=?", (enabled, rule_id))
    return {"id": rule_id, "enabled": bool(enabled)}


@app.post("/inboxes/{inbox}/rules/apply")
def apply_rules(inbox: str):
    """Apply all enabled rules to recent UNSEEN messages. Returns count of affected messages."""
    enc_inbox = inbox
    with sqlite3.connect(SCHEDULED_DB) as db:
        rules = db.execute(
            "SELECT id, folder, match_field, match_value, action FROM rules "
            "WHERE inbox=? AND enabled=1",
            (enc_inbox,)
        ).fetchall()

    if not rules:
        return {"applied": 0, "rules_checked": 0}

    total = 0
    for rule_id, folder, match_field, match_value, action in rules:
        try:
            imap_field = {"from": "FROM", "to": "TO", "subject": "SUBJECT"}.get(match_field, "FROM")
            criteria = f'UNSEEN {imap_field} "{match_value}"'
            with imap_conn() as m:
                m.select(f'"{folder}"')
                typ, data = m.uid("SEARCH", None, criteria)
                if typ != "OK" or not data[0]:
                    continue
                uids = data[0].decode().split()
                for uid in uids:
                    if action == "flag":
                        m.uid("STORE", uid.encode(), "+FLAGS", "\\Flagged")
                    elif action == "mark-seen":
                        m.uid("STORE", uid.encode(), "+FLAGS", "\\Seen")
                total += len(uids)
        except Exception:
            pass

    return {"applied": total, "rules_checked": len(rules)}


# ── Contacts (CRM memory) ──────────────────────────────────────────────────

class ContactUpsert(BaseModel):
    email: str
    name: str = ""
    notes: str = ""
    tags: str = ""


@app.get("/contacts")
def list_contacts():
    """List all saved contacts."""
    with sqlite3.connect(SCHEDULED_DB) as db:
        rows = db.execute(
            "SELECT email, name, notes, tags, message_count, last_seen FROM contacts ORDER BY last_seen DESC"
        ).fetchall()
    return {"contacts": [
        {"email": r[0], "name": r[1], "notes": r[2], "tags": r[3],
         "message_count": r[4], "last_seen": r[5]}
        for r in rows
    ]}


@app.get("/contacts/{email}")
def get_contact(email: str):
    """Get a contact by email address."""
    with sqlite3.connect(SCHEDULED_DB) as db:
        row = db.execute(
            "SELECT email, name, notes, tags, message_count, last_seen, created_at "
            "FROM contacts WHERE email=?", (email,)
        ).fetchone()
    if not row:
        raise HTTPException(404, f"Contact {email!r} not found")
    return {"email": row[0], "name": row[1], "notes": row[2], "tags": row[3],
            "message_count": row[4], "last_seen": row[5], "created_at": row[6]}


@app.put("/contacts/{email}", status_code=200)
def upsert_contact(email: str, body: ContactUpsert):
    """Create or fully update a contact."""
    now = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(SCHEDULED_DB) as db:
        existing = db.execute("SELECT created_at FROM contacts WHERE email=?", (email,)).fetchone()
        created_at = existing[0] if existing else now
        db.execute(
            "INSERT INTO contacts (email, name, notes, tags, message_count, last_seen, created_at) "
            "VALUES (?,?,?,?,0,?,?) "
            "ON CONFLICT(email) DO UPDATE SET "
            "name=excluded.name, notes=excluded.notes, tags=excluded.tags, last_seen=excluded.last_seen",
            (email, body.name, body.notes, body.tags, now, created_at)
        )
    return {"email": email, "updated": True}


@app.post("/contacts/{email}/notes")
def append_note(email: str, body: dict):
    """Append a timestamped note to a contact. Body: {'note': '...'}"""
    note_text = body.get("note", "").strip()
    if not note_text:
        raise HTTPException(400, "note required")
    now = datetime.now(timezone.utc).isoformat()
    timestamp = now[:16].replace("T", " ")
    new_note = f"[{timestamp}] {note_text}"
    with sqlite3.connect(SCHEDULED_DB) as db:
        existing = db.execute("SELECT notes, created_at FROM contacts WHERE email=?", (email,)).fetchone()
        if existing:
            prev = existing[0] or ""
            updated = (prev + "\n" + new_note).strip()
            db.execute("UPDATE contacts SET notes=?, last_seen=? WHERE email=?", (updated, now, email))
        else:
            db.execute(
                "INSERT INTO contacts (email, name, notes, tags, message_count, last_seen, created_at) "
                "VALUES (?,?,?,?,0,?,?)",
                (email, "", new_note, "", now, now)
            )
    return {"email": email, "note_added": new_note}


@app.post("/contacts/{email}/seen")
def contact_seen(email: str, body: dict):
    """Record that a message was received from this contact. Body: {'name': '...'}"""
    now  = datetime.now(timezone.utc).isoformat()
    name = body.get("name", "")
    with sqlite3.connect(SCHEDULED_DB) as db:
        existing = db.execute("SELECT message_count, created_at FROM contacts WHERE email=?", (email,)).fetchone()
        if existing:
            count = (existing[0] or 0) + 1
            db.execute(
                "UPDATE contacts SET message_count=?, last_seen=?{} WHERE email=?".format(
                    ", name=?" if name else ""
                ),
                (count, now, name, email) if name else (count, now, email)
            )
        else:
            db.execute(
                "INSERT INTO contacts (email, name, notes, tags, message_count, last_seen, created_at) "
                "VALUES (?,?,?,?,1,?,?)",
                (email, name, "", "", now, now)
            )
    return {"email": email, "recorded": True}


@app.delete("/contacts/{email}")
def delete_contact(email: str):
    """Remove a contact and all their notes."""
    with sqlite3.connect(SCHEDULED_DB) as db:
        row = db.execute("SELECT email FROM contacts WHERE email=?", (email,)).fetchone()
        if not row:
            raise HTTPException(404, "Contact not found")
        db.execute("DELETE FROM contacts WHERE email=?", (email,))
    return {"email": email, "deleted": True}


# ── Scheduled messages ─────────────────────────────────────────────────────

class ScheduleRequest(BaseModel):
    to: list[str]
    subject: str
    text: str = ""
    html: str = ""
    in_reply_to: str = ""
    references: str = ""
    send_at: str  # ISO datetime, e.g. "2026-03-10T09:00:00Z"


@app.post("/inboxes/{inbox}/scheduled", status_code=201)
def schedule_message(inbox: str, body: ScheduleRequest):
    """Queue an email for future delivery."""
    try:
        # Validate send_at
        datetime.fromisoformat(body.send_at.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(400, "send_at must be ISO datetime e.g. 2026-03-10T09:00:00Z")
    try:
        with sqlite3.connect(SCHEDULED_DB) as db:
            cur = db.execute(
                "INSERT INTO scheduled (inbox, to_json, subject, body_text, body_html, "
                "in_reply_to, refs, send_at) VALUES (?,?,?,?,?,?,?,?)",
                (inbox, json.dumps(body.to), body.subject, body.text, body.html,
                 body.in_reply_to, body.references, body.send_at)
            )
            return {"id": cur.lastrowid, "send_at": body.send_at, "status": "scheduled"}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/inboxes/{inbox}/scheduled")
def list_scheduled(inbox: str):
    """List pending scheduled messages."""
    try:
        with sqlite3.connect(SCHEDULED_DB) as db:
            rows = db.execute(
                "SELECT id, to_json, subject, send_at, sent, error "
                "FROM scheduled WHERE inbox=? ORDER BY send_at",
                (inbox,)
            ).fetchall()
        items = [
            {"id": r[0], "to": json.loads(r[1]), "subject": r[2],
             "send_at": r[3], "sent": bool(r[4]), "error": r[5]}
            for r in rows
        ]
        return {"scheduled": items, "total": len(items)}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/inboxes/{inbox}/scheduled/{item_id}")
def cancel_scheduled(inbox: str, item_id: int):
    """Cancel a pending scheduled message."""
    try:
        with sqlite3.connect(SCHEDULED_DB) as db:
            row = db.execute(
                "SELECT sent FROM scheduled WHERE id=? AND inbox=?", (item_id, inbox)
            ).fetchone()
            if not row:
                raise HTTPException(404, "Scheduled message not found")
            if row[0]:
                raise HTTPException(409, "Message already sent")
            db.execute("DELETE FROM scheduled WHERE id=?", (item_id,))
        return {"id": item_id, "cancelled": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Search ─────────────────────────────────────────────────────────────────

@app.get("/inboxes/{inbox}/search")
def search_messages(
    inbox: str,
    folder: str  = Query(default="INBOX"),
    q: str       = Query(default="", description="Search all text fields"),
    from_: str   = Query(default="", alias="from"),
    to: str      = Query(default=""),
    subject: str = Query(default=""),
    body: str    = Query(default=""),
    since: str   = Query(default="", description="ISO date: 2026-01-01"),
    before: str  = Query(default="", description="ISO date: 2026-12-31"),
    unseen: bool = Query(default=False),
    seen: bool   = Query(default=False),
    has_attachments: bool = Query(default=False),
    vip_only: bool  = Query(default=False, description="Only VIP senders"),
    flagged: bool   = Query(default=False, description="Only flagged/starred messages"),
    unflagged: bool = Query(default=False, description="Only unflagged messages"),
    limit: int      = Query(default=20, le=100),
):
    """
    Search messages using IMAP SEARCH criteria.
    'q' searches subject + body + from simultaneously.
    """
    try:
        eff_subject = subject or q
        eff_body    = body

        criteria = build_imap_search(
            from_=from_, to=to, subject=eff_subject,
            body=eff_body, since=since, before=before,
            unseen=unseen, seen=seen, flagged=flagged, unflagged=unflagged,
        )

        with imap_conn() as m:
            m.select(f'"{folder}"', readonly=True)
            uids = fetch_uids(m, criteria)

            if not uids and q and not subject and not body:
                criteria = build_imap_search(body=q, from_=from_, to=to,
                                             since=since, before=before,
                                             unseen=unseen, seen=seen,
                                             flagged=flagged, unflagged=unflagged)
                uids = fetch_uids(m, criteria)

            uids = uids[-limit:][::-1]
            msgs = fetch_messages(m, uids, folder)

        if has_attachments:
            msgs = [m for m in msgs if m.get("attachments")]
        if vip_only:
            msgs = [m for m in msgs if m.get("vip")]

        return {
            "messages": msgs,
            "total":    len(msgs),
            "folder":   folder,
            "criteria": criteria,
        }
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Threads ────────────────────────────────────────────────────────────────

@app.get("/inboxes/{inbox}/threads")
def list_threads(
    inbox: str,
    folder: str = Query(default="INBOX"),
    limit: int  = Query(default=20, le=100),
):
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"', readonly=True)
            uids = fetch_uids(m, "ALL")
            uids = uids[-(limit * 3):][::-1]
            msgs = fetch_messages(m, uids, folder)
        threads = group_threads(msgs)[:limit]
        return {"threads": threads, "total": len(threads), "folder": folder}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Settings helpers ───────────────────────────────────────────────────────

def _get_setting(key: str, default: str = "") -> str:
    with sqlite3.connect(SCHEDULED_DB) as db:
        row = db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row[0] if row else default


def _set_setting(key: str, value: str):
    with sqlite3.connect(SCHEDULED_DB) as db:
        db.execute(
            "INSERT INTO settings (key, value) VALUES (?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )


# ── Analyze / group inbox ───────────────────────────────────────────────────

def _normalize_subject(subject: str) -> str:
    """Strip reply/forward prefixes and normalize for grouping."""
    s = re.sub(r"(?i)^(re|fwd?|fw|пересл(ано)?)\s*:\s*", "", subject.strip())
    return s.strip().lower()


def _folder_name_from_email(addr: str) -> str:
    """alice@example.com → Alice"""
    local = addr.split("@")[0]
    # CamelCase from dot/hyphen/underscore-separated parts
    return "".join(p.capitalize() for p in re.split(r"[._\-+]", local) if p)


def _folder_name_from_subject(subject: str) -> str:
    """'project update weekly' → 'ProjectUpdateWeekly' (max 3 words)"""
    words = re.findall(r"[a-zA-Zа-яА-ЯіїєґІЇЄҐ0-9]+", subject)[:3]
    return "".join(w.capitalize() for w in words) or "Misc"


def _analyze_messages(messages: list[dict], threshold: int) -> list[dict]:
    """
    Group messages by sender email and by normalized subject.
    Returns candidates with count >= threshold, sorted by count desc.
    """
    from collections import defaultdict

    by_sender:  dict[str, list[str]] = defaultdict(list)
    by_subject: dict[str, list[str]] = defaultdict(list)

    for m in messages:
        uid = m["uid"]
        # Group by sender
        for addr in m.get("from_", []):
            email_addr = addr.get("email", "").lower()
            if email_addr:
                by_sender[email_addr].append(uid)
                break
        # Group by normalized subject
        norm = _normalize_subject(m.get("subject", ""))
        if norm:
            by_subject[norm].append(uid)

    candidates = []
    seen_uids: set = set()

    # Sender candidates (higher priority)
    for addr, uids in sorted(by_sender.items(), key=lambda x: -len(x[1])):
        if len(uids) >= threshold:
            candidates.append({
                "type":             "sender",
                "key":              addr,
                "count":            len(uids),
                "uids":             uids,
                "suggested_folder": _folder_name_from_email(addr),
                "rule_field":       "from",
                "rule_value":       addr,
            })
            seen_uids.update(uids)

    # Subject candidates — skip UIDs already covered by a sender rule
    for subj, uids in sorted(by_subject.items(), key=lambda x: -len(x[1])):
        new_uids = [u for u in uids if u not in seen_uids]
        if len(new_uids) >= threshold:
            candidates.append({
                "type":             "subject",
                "key":              subj,
                "count":            len(new_uids),
                "uids":             new_uids,
                "suggested_folder": _folder_name_from_subject(subj),
                "rule_field":       "subject",
                "rule_value":       subj,
            })

    return candidates


# ── Sort inbox ─────────────────────────────────────────────────────────────

def _is_forwarded(msg: email.message.Message) -> bool:
    """Detect whether a message is a forward.

    Checks (in order):
    1. Subject starts with Fwd: / FW: / Пересл: (case-insensitive)
    2. X-Forwarded-* or Resent-* headers present
    """
    subject = decode_header_value(msg.get("Subject", ""))
    if re.match(r"(?i)^(fwd?|пересл(ано)?)\s*:", subject.strip()):
        return True
    for header in msg.keys():
        if header.lower().startswith(("x-forwarded", "resent-")):
            return True
    return False


def _is_personal(msg: email.message.Message, inbox: str) -> bool:
    """Return True when the inbox address appears in To: or Cc: headers."""
    inbox_lower = inbox.lower()
    for header in ("To", "Cc"):
        for _, addr in email.utils.getaddresses([msg.get(header, "")]):
            if addr.lower() == inbox_lower:
                return True
    return False


@app.post("/inboxes/{inbox}/sort")
def sort_inbox(
    inbox: str,
    folder: str         = Query(default="INBOX"),
    personal_folder: str = Query(default="Personal"),
    forwarded_folder: str = Query(default="Forwarded"),
    unseen_only: bool    = Query(default=False),
    dry_run: bool        = Query(default=False,
                                 description="Report moves without executing them"),
):
    """Sort messages into Personal or Forwarded sub-folders.

    - **Personal**: inbox address is in To: or Cc:
    - **Forwarded**: subject starts with Fwd/FW, or X-Forwarded/Resent headers present
    - Messages that match neither (or both) stay in the source folder.
    """
    try:
        moved_personal  = []
        moved_forwarded = []
        skipped         = []

        with imap_conn() as m:
            # Ensure target folders exist
            if not dry_run:
                for target in (personal_folder, forwarded_folder):
                    m.create(f'"{target}"')  # silently fails if already exists

            criteria = "UNSEEN" if unseen_only else "ALL"
            m.select(f'"{folder}"')
            uids = fetch_uids(m, criteria)

            for uid_bytes in uids:
                uid = uid_bytes.decode()
                typ, raw = m.fetch(uid_bytes, "(RFC822)")
                if typ != "OK" or not raw or not isinstance(raw[0], tuple):
                    continue
                msg = email.message_from_bytes(raw[0][1])

                forwarded = _is_forwarded(msg)
                personal  = _is_personal(msg, inbox)

                if forwarded:
                    # Forwarded takes priority over personal
                    dest = forwarded_folder
                    moved_forwarded.append(uid)
                elif personal:
                    dest = personal_folder
                    moved_personal.append(uid)
                else:
                    skipped.append(uid)
                    continue

                if not dry_run:
                    typ2, _ = m.uid("COPY", uid_bytes, f'"{dest}"')
                    if typ2 == "OK":
                        m.uid("STORE", uid_bytes, "+FLAGS", "\\Deleted")

            if not dry_run:
                m.expunge()

        return {
            "folder":           folder,
            "personal_folder":  personal_folder,
            "forwarded_folder": forwarded_folder,
            "moved_personal":   moved_personal,
            "moved_forwarded":  moved_forwarded,
            "skipped":          skipped,
            "dry_run":          dry_run,
            "total_moved":      len(moved_personal) + len(moved_forwarded),
        }
    except Exception as e:
        raise HTTPException(500, str(e))


# ── Auto-group settings ────────────────────────────────────────────────────

@app.get("/inboxes/{inbox}/autogroup/status")
def autogroup_status(inbox: str):
    """Return auto-group settings for this inbox."""
    key = f"autogroup:{inbox}"
    enabled   = _get_setting(f"{key}:enabled",   "false") == "true"
    threshold = int(_get_setting(f"{key}:threshold", "3"))
    folder    = _get_setting(f"{key}:parent_folder", "Groups")
    return {"enabled": enabled, "threshold": threshold, "parent_folder": folder}


@app.post("/inboxes/{inbox}/autogroup/enable")
def autogroup_enable(
    inbox: str,
    threshold:     int = Query(default=3, ge=2, le=50),
    parent_folder: str = Query(default="Groups"),
):
    """Enable auto-grouping for this inbox."""
    key = f"autogroup:{inbox}"
    _set_setting(f"{key}:enabled",       "true")
    _set_setting(f"{key}:threshold",     str(threshold))
    _set_setting(f"{key}:parent_folder", parent_folder)
    return {"enabled": True, "threshold": threshold, "parent_folder": parent_folder}


@app.post("/inboxes/{inbox}/autogroup/disable")
def autogroup_disable(inbox: str):
    """Disable auto-grouping for this inbox."""
    _set_setting(f"autogroup:{inbox}:enabled", "false")
    return {"enabled": False}


# ── Analyze inbox ──────────────────────────────────────────────────────────

@app.get("/inboxes/{inbox}/analyze")
def analyze_inbox(
    inbox: str,
    folder:    str = Query(default="INBOX"),
    threshold: int = Query(default=3, ge=2, le=100,
                           description="Min messages to suggest a group folder"),
    limit:     int = Query(default=200, le=500),
):
    """
    Scan messages and find candidates for dedicated sub-folders.
    Groups by sender email and by normalized subject.
    Returns candidates with count >= threshold, sorted by count desc.
    """
    try:
        with imap_conn() as m:
            m.select(f'"{folder}"', readonly=True)
            uids = fetch_uids(m, "ALL")[-limit:][::-1]
            msgs = fetch_messages(m, uids, folder)
        candidates = _analyze_messages(msgs, threshold)
        return {
            "folder":     folder,
            "threshold":  threshold,
            "scanned":    len(msgs),
            "candidates": candidates,
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/inboxes/{inbox}/analyze/apply")
def analyze_apply(
    inbox: str,
    body: dict,
    folder:        str = Query(default="INBOX"),
    parent_folder: str = Query(default="Groups"),
    dry_run:       bool = Query(default=False),
):
    """
    Apply selected grouping candidates: create sub-folder, move existing
    messages, and add a persistent auto-rule for future messages.

    Body: {"candidates": [{"suggested_folder": "Alice", "uids": [...],
                            "rule_field": "from", "rule_value": "alice@example.com"}]}
    """
    candidates = body.get("candidates", [])
    if not candidates:
        raise HTTPException(400, "candidates list required")

    now    = datetime.now(timezone.utc).isoformat()
    report = []

    for c in candidates:
        dest        = f"{parent_folder}/{c['suggested_folder']}"
        uids        = c.get("uids", [])
        rule_field  = c.get("rule_field", "from")
        rule_value  = c.get("rule_value", "")
        moved_count = 0

        if not dry_run:
            # 1. Create parent + sub-folder
            with imap_conn() as m:
                m.create(f'"{parent_folder}"')
                m.create(f'"{dest}"')

            # 2. Move existing messages
            if uids:
                with imap_conn() as m:
                    m.select(f'"{folder}"')
                    for uid in uids:
                        t, _ = m.uid("COPY", uid.encode(), f'"{dest}"')
                        if t == "OK":
                            m.uid("STORE", uid.encode(), "+FLAGS", "\\Deleted")
                            moved_count += 1
                    m.expunge()

            # 3. Add persistent auto-rule
            if rule_value:
                with sqlite3.connect(SCHEDULED_DB) as db:
                    # Avoid duplicate rules
                    exists = db.execute(
                        "SELECT id FROM rules WHERE inbox=? AND match_field=? AND match_value=?",
                        (inbox, rule_field, rule_value),
                    ).fetchone()
                    if not exists:
                        db.execute(
                            "INSERT INTO rules (inbox, folder, match_field, match_value, "
                            "action, enabled, created_at) VALUES (?,?,?,?,?,1,?)",
                            (inbox, folder, rule_field, rule_value, "move-to:" + dest, now),
                        )

        report.append({
            "folder":      dest,
            "moved":       moved_count if not dry_run else len(uids),
            "rule_added":  bool(rule_value) and not dry_run,
            "dry_run":     dry_run,
        })

    return {"applied": report, "total": len(report), "dry_run": dry_run}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=LISTEN_PORT)
