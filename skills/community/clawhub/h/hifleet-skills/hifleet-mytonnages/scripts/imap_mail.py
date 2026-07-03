#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IMAP 拉信、本地 .eml 归档、按 Message-ID / UID 取回原始邮件。"""

from __future__ import annotations

import base64
import email
import email.policy
import hashlib
import imaplib
import json
import logging
import os
import re
import sqlite3
from datetime import datetime, timezone
from email.header import decode_header
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("imap_mail")

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(_SCRIPT_DIR))

from charter_facts_tool import CharterFactsDB, default_db_path, default_skill_dir  # noqa: E402

ARCHIVE_DIR_NAME = "mail_archive"


def _decode_password(raw: str) -> str:
    if not raw:
        return ""
    s = str(raw).strip()
    if s.startswith("base64:"):
        try:
            return base64.b64decode(s[7:]).decode("utf-8")
        except Exception:
            return s[7:]
    return s


def load_imap_config() -> dict[str, Any]:
    cfg_path = default_skill_dir() / "config.json"
    cfg: dict[str, Any] = {}
    if cfg_path.is_file():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg = data
        except (json.JSONDecodeError, OSError):
            pass
    host = str(cfg.get("imap_host") or os.environ.get("IMAP_HOST") or "").strip()
    user = str(cfg.get("email") or cfg.get("imap_user") or os.environ.get("IMAP_USER") or "").strip()
    password = _decode_password(
        str(cfg.get("email_password") or cfg.get("imap_password") or os.environ.get("IMAP_PASSWORD") or "")
    )
    port = int(cfg.get("imap_port") or os.environ.get("IMAP_PORT") or 993)
    mailbox = str(cfg.get("imap_mailbox") or "INBOX").strip() or "INBOX"
    return {
        "imap_host": host,
        "email": user,
        "imap_user": user,
        "email_password": password,
        "imap_password": password,
        "imap_port": port,
        "imap_mailbox": mailbox,
    }


def load_preview_config() -> dict[str, Any]:
    cfg_path = default_skill_dir() / "config.json"
    cfg: dict[str, Any] = {}
    if cfg_path.is_file():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg = data
        except (json.JSONDecodeError, OSError):
            pass
    host = str(cfg.get("mail_preview_host") or os.environ.get("HIFLEET_MAIL_PREVIEW_HOST") or "127.0.0.1").strip()
    port = int(cfg.get("mail_preview_port") or os.environ.get("HIFLEET_MAIL_PREVIEW_PORT") or 8765)
    base = str(
        cfg.get("mail_preview_base_url")
        or os.environ.get("HIFLEET_MAIL_PREVIEW_BASE_URL")
        or f"http://{host}:{port}"
    ).strip().rstrip("/")
    token = str(cfg.get("mail_preview_token") or os.environ.get("HIFLEET_MAIL_PREVIEW_TOKEN") or "").strip()
    return {"mail_preview_host": host, "mail_preview_port": port, "mail_preview_base_url": base, "mail_preview_token": token}


def preview_token_for_message_id(message_id: str) -> str:
    mid = (message_id or "").strip()
    return hashlib.sha256(mid.encode("utf-8")).hexdigest()[:32]


def build_preview_url(message_id: str, base_url: str | None = None) -> str:
    base = (base_url or load_preview_config()["mail_preview_base_url"]).rstrip("/")
    token = preview_token_for_message_id(message_id)
    return f"{base}/mail/preview/{token}"


def archive_dir() -> Path:
    d = default_skill_dir() / ARCHIVE_DIR_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def archive_path_for_token(token: str) -> Path:
    safe = re.sub(r"[^a-f0-9]", "", (token or "").lower())[:32]
    return archive_dir() / f"{safe}.eml"


def message_id_from_raw(raw: bytes) -> str:
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    mid = (msg.get("Message-ID") or msg.get("Message-Id") or "").strip()
    if mid:
        return mid
    digest = hashlib.sha256(raw).hexdigest()[:32]
    return f"generated-{digest}@local"


def decode_mime_header(raw: str) -> str:
    if not raw:
        return ""
    try:
        parts = decode_header(raw)
        out: list[str] = []
        for frag, enc in parts:
            if isinstance(frag, bytes):
                out.append(frag.decode(enc or "utf-8", errors="replace"))
            else:
                out.append(str(frag))
        return "".join(out).strip()
    except Exception:
        return str(raw).strip()


def email_date_utc(msg: email.message.Message) -> str:
    for hdr in ("Date", "Received"):
        val = msg.get(hdr)
        if not val:
            continue
        try:
            dt = parsedate_to_datetime(val)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except (TypeError, ValueError, IndexError):
            continue
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_netease_imap(host: str) -> bool:
    h = (host or "").lower()
    return any(x in h for x in ("163.com", "126.com", "yeah.net", "188.com", "vip.163.com"))


def _netease_imap_id(mail: imaplib.IMAP4_SSL, email_user: str) -> None:
    imaplib.Commands["ID"] = ("AUTH",)
    args = ("name", email_user, "contact", email_user, "version", "1.0.0", "vendor", "hifleet_mytonnages")
    id_param = str(args).replace(",", "").replace("'", '"')
    typ, data = mail._simple_command("ID", id_param)
    if typ != "OK":
        raise RuntimeError(f"网易 IMAP ID 失败: {typ} {data}")


def connect_imap(cfg: dict[str, Any] | None = None) -> tuple[imaplib.IMAP4_SSL, dict[str, Any]]:
    c = cfg or load_imap_config()
    host = str(c.get("imap_host") or "").strip()
    user = str(c.get("email") or c.get("imap_user") or "").strip()
    password = _decode_password(str(c.get("email_password") or c.get("imap_password") or ""))
    port = int(c.get("imap_port") or 993)
    if not host or not user or not password:
        raise ValueError("IMAP 配置不完整（imap_host / email / email_password）")
    mail = imaplib.IMAP4_SSL(host, port, timeout=60)
    mail.login(user, password)
    if _is_netease_imap(host):
        _netease_imap_id(mail, user)
    return mail, c


def _escape_imap_header_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _fetch_uid_by_message_id(mail: imaplib.IMAP4_SSL, mailbox: str, message_id: str) -> Optional[int]:
    mail.select(mailbox)
    needle = (message_id or "").strip()
    if not needle or needle.startswith("generated-"):
        return None
    for search_val in (needle, needle.strip("<>")):
        criteria = f'HEADER Message-ID "{_escape_imap_header_value(search_val)}"'
        status, data = mail.uid("search", None, criteria)
        if status == "OK" and data and data[0]:
            uids = data[0].split()
            if uids:
                return int(uids[-1])
    return None


def _fetch_rfc822_by_uid(mail: imaplib.IMAP4_SSL, uid: int) -> bytes:
    status, msg_data = mail.uid("fetch", str(uid).encode(), "(RFC822)")
    if status != "OK" or not msg_data or not msg_data[0]:
        raise RuntimeError(f"IMAP UID FETCH 失败 uid={uid}")
    raw = msg_data[0][1]
    if not isinstance(raw, (bytes, bytearray)):
        raise RuntimeError(f"IMAP 返回非二进制 uid={uid}")
    return bytes(raw)


def ensure_mail_index_table(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mail_index (
          message_id TEXT PRIMARY KEY,
          preview_token TEXT NOT NULL UNIQUE,
          email_date_utc TEXT,
          from_addr TEXT,
          subject TEXT,
          imap_uid INTEGER,
          mailbox TEXT DEFAULT 'INBOX',
          archive_path TEXT,
          archived_at TEXT
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_mail_index_token ON mail_index(preview_token)")
    conn.commit()


def upsert_mail_index(
    conn: sqlite3.Connection,
    *,
    message_id: str,
    email_date_utc: str = "",
    from_addr: str = "",
    subject: str = "",
    imap_uid: int | None = None,
    mailbox: str = "INBOX",
    archive_path: str = "",
) -> str:
    ensure_mail_index_table(conn)
    mid = (message_id or "").strip()
    if not mid:
        raise ValueError("message_id 为空")
    token = preview_token_for_message_id(mid)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO mail_index (
          message_id, preview_token, email_date_utc, from_addr, subject,
          imap_uid, mailbox, archive_path, archived_at
        ) VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(message_id) DO UPDATE SET
          email_date_utc=COALESCE(excluded.email_date_utc, mail_index.email_date_utc),
          from_addr=COALESCE(excluded.from_addr, mail_index.from_addr),
          subject=COALESCE(excluded.subject, mail_index.subject),
          imap_uid=COALESCE(excluded.imap_uid, mail_index.imap_uid),
          mailbox=COALESCE(excluded.mailbox, mail_index.mailbox),
          archive_path=CASE
            WHEN excluded.archive_path != '' THEN excluded.archive_path
            ELSE mail_index.archive_path
          END,
          archived_at=CASE
            WHEN excluded.archive_path != '' THEN excluded.archived_at
            ELSE mail_index.archived_at
          END
        """,
        (
            mid,
            token,
            email_date_utc or None,
            from_addr or None,
            subject or None,
            imap_uid,
            mailbox or "INBOX",
            archive_path or None,
            now if archive_path else None,
        ),
    )
    conn.commit()
    return token


def get_mail_index_by_token(conn: sqlite3.Connection, token: str) -> Optional[dict[str, Any]]:
    ensure_mail_index_table(conn)
    cur = conn.cursor()
    cur.execute("SELECT * FROM mail_index WHERE preview_token = ?", (token,))
    row = cur.fetchone()
    return dict(row) if row else None


def get_mail_index_by_message_id(conn: sqlite3.Connection, message_id: str) -> Optional[dict[str, Any]]:
    ensure_mail_index_table(conn)
    cur = conn.cursor()
    cur.execute("SELECT * FROM mail_index WHERE message_id = ?", ((message_id or "").strip(),))
    row = cur.fetchone()
    return dict(row) if row else None


def save_archive_eml(raw: bytes, message_id: str) -> Path:
    token = preview_token_for_message_id(message_id)
    path = archive_path_for_token(token)
    path.write_bytes(raw)
    return path


def archive_fetched_message(
    raw: bytes,
    *,
    message_id: str,
    imap_uid: int | None = None,
    mailbox: str = "INBOX",
    email_date_utc: str = "",
    from_addr: str = "",
    subject: str = "",
    db_path: Path | None = None,
) -> Path:
    path = save_archive_eml(raw, message_id)
    db = CharterFactsDB(db_path or default_db_path())
    conn = db.connect()
    try:
        upsert_mail_index(
            conn,
            message_id=message_id,
            email_date_utc=email_date_utc,
            from_addr=from_addr,
            subject=subject,
            imap_uid=imap_uid,
            mailbox=mailbox,
            archive_path=str(path),
        )
    finally:
        conn.close()
    return path


def load_raw_from_archive(archive_path: str | Path) -> Optional[bytes]:
    p = Path(archive_path)
    if p.is_file():
        return p.read_bytes()
    return None


def fetch_raw_email(
    message_id: str,
    *,
    db_path: Path | None = None,
    prefer_imap: bool = False,
) -> tuple[bytes, dict[str, Any]]:
    """返回 (RFC822, meta)。优先本地归档；缺失时 IMAP 拉取并写回归档。"""
    mid = (message_id or "").strip()
    if not mid:
        raise ValueError("message_id 为空")

    db = CharterFactsDB(db_path or default_db_path())
    conn = db.connect()
    meta: dict[str, Any] = {"message_id": mid}
    try:
        row = get_mail_index_by_message_id(conn, mid)
        if row:
            meta.update(row)
        if row and row.get("archive_path") and not prefer_imap:
            raw = load_raw_from_archive(str(row["archive_path"]))
            if raw:
                return raw, meta
    finally:
        conn.close()

    cfg = load_imap_config()
    mailbox = str(meta.get("mailbox") or cfg.get("imap_mailbox") or "INBOX")
    mail, _ = connect_imap(cfg)
    try:
        uid = meta.get("imap_uid")
        raw: bytes | None = None
        if uid:
            try:
                mail.select(mailbox)
                raw = _fetch_rfc822_by_uid(mail, int(uid))
            except Exception as e:
                logger.warning("UID 拉信失败 uid=%s: %s，改按 Message-ID 搜索", uid, e)
        if raw is None:
            found_uid = _fetch_uid_by_message_id(mail, mailbox, mid)
            if found_uid is None:
                raise FileNotFoundError(f"邮箱中未找到邮件: {mid}")
            raw = _fetch_rfc822_by_uid(mail, found_uid)
            meta["imap_uid"] = found_uid
    finally:
        try:
            mail.logout()
        except Exception:
            pass

    msg = email.message_from_bytes(raw, policy=email.policy.default)
    meta.setdefault("email_date_utc", email_date_utc(msg))
    meta.setdefault("from_addr", decode_mime_header(msg.get("From") or ""))
    meta.setdefault("subject", decode_mime_header(msg.get("Subject") or ""))
    meta.setdefault("mailbox", mailbox)

    archive_fetched_message(
        raw,
        message_id=mid,
        imap_uid=int(meta["imap_uid"]) if meta.get("imap_uid") else None,
        mailbox=mailbox,
        email_date_utc=str(meta.get("email_date_utc") or ""),
        from_addr=str(meta.get("from_addr") or ""),
        subject=str(meta.get("subject") or ""),
        db_path=db_path,
    )
    return raw, meta


def fetch_raw_by_preview_token(
    token: str,
    *,
    db_path: Path | None = None,
) -> tuple[bytes, dict[str, Any]]:
    db = CharterFactsDB(db_path or default_db_path())
    conn = db.connect()
    try:
        row = get_mail_index_by_token(conn, token)
    finally:
        conn.close()
    if not row:
        raise FileNotFoundError(f"未知 preview_token: {token}")
    mid = str(row.get("message_id") or "")
    raw, meta = fetch_raw_email(mid, db_path=db_path)
    meta.update(row)
    return raw, meta


def body_text_from_message(msg: email.message.Message) -> str:
    if msg.is_multipart():
        chunks: list[str] = []
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get_content_disposition() == "attachment":
                continue
            ctype = (part.get_content_type() or "").lower()
            if ctype not in ("text/plain", "text/html"):
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            charset = part.get_content_charset() or "utf-8"
            try:
                chunks.append(payload.decode(charset, errors="replace"))
            except Exception:
                chunks.append(payload.decode("utf-8", errors="replace"))
        return "\n".join(chunks)
    payload = msg.get_payload(decode=True)
    if not payload:
        return str(msg.get_payload() or "")
    charset = msg.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except Exception:
        return payload.decode("utf-8", errors="replace")


def _html_to_plain(html: str) -> str:
    if not html:
        return ""
    s = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    s = re.sub(r"</p\s*>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s, flags=re.I)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\n\s*\n", "\n", s).strip()


def _sanitize_html(html: str) -> str:
    s = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html, flags=re.I)
    s = re.sub(r"<iframe[^>]*>[\s\S]*?</iframe>", "", s, flags=re.I)
    s = re.sub(r"\s+on\w+\s*=\s*[^>\s]+", "", s, flags=re.I)
    s = re.sub(r"javascript:", "", s, flags=re.I)
    return s


def _attachment_filename(part: email.message.Message) -> str:
    name = part.get_filename()
    if name:
        return decode_mime_header(name)
    return "attachment"


def parse_for_preview(raw: bytes, preview_token: str) -> dict[str, Any]:
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    text_body = ""
    html_body = ""
    attachments: list[dict[str, Any]] = []
    idx = 0
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        disp = (part.get_content_disposition() or "").lower()
        ctype = (part.get_content_type() or "").lower()
        if disp == "attachment" or (disp != "inline" and part.get_filename()):
            attachments.append(
                {
                    "index": idx,
                    "filename": _attachment_filename(part),
                    "content_type": ctype or "application/octet-stream",
                    "size": len(part.get_payload(decode=True) or b""),
                    "url": f"/mail/attachment/{preview_token}/{idx}",
                }
            )
            idx += 1
            continue
        if ctype == "text/plain" and not text_body:
            payload = part.get_payload(decode=True)
            if payload:
                charset = part.get_content_charset() or "utf-8"
                try:
                    text_body = payload.decode(charset, errors="replace")
                except Exception:
                    text_body = payload.decode("utf-8", errors="replace")
        elif ctype == "text/html" and not html_body:
            payload = part.get_payload(decode=True)
            if payload:
                charset = part.get_content_charset() or "utf-8"
                try:
                    html_body = _sanitize_html(payload.decode(charset, errors="replace"))
                except Exception:
                    html_body = _sanitize_html(payload.decode("utf-8", errors="replace"))
    if not text_body and html_body:
        text_body = _html_to_plain(html_body)
    return {
        "subject": decode_mime_header(msg.get("Subject") or ""),
        "from_addr": decode_mime_header(msg.get("From") or ""),
        "to_addr": decode_mime_header(msg.get("To") or ""),
        "date": decode_mime_header(msg.get("Date") or ""),
        "text_body": text_body,
        "html_body": html_body,
        "attachments": attachments,
    }


def get_attachment_part(raw: bytes, part_index: int) -> tuple[email.message.Message, str, str]:
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    idx = 0
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        disp = (part.get_content_disposition() or "").lower()
        if disp == "attachment" or (disp != "inline" and part.get_filename()):
            if idx == part_index:
                filename = _attachment_filename(part)
                ctype = part.get_content_type() or "application/octet-stream"
                return part, filename, ctype
            idx += 1
    raise FileNotFoundError(f"附件不存在 index={part_index}")
