#!/usr/bin/env python3
"""IMAP/SMTP client helpers for Mail Assistant."""

from __future__ import annotations

import email
import email.policy
import imaplib
import re
import smtplib
import ssl
from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
from email.utils import formatdate, make_msgid, parsedate_to_datetime
from pathlib import Path

from mail_accounts import DEFAULT_JSON_CONFIG, load_raw_config, load_accounts, select_account
from read_emails import decode_mime_header, extract_links, html_to_text

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = DEFAULT_JSON_CONFIG

_TAG_RE = re.compile(r"[^A-Za-z0-9_.-]+")
_BLOCKED_ATTACHMENT_EXTENSIONS = {".app", ".bat", ".cmd", ".com", ".exe", ".js", ".ps1", ".scr", ".sh", ".vbs"}
_DEFAULT_MAX_ATTACHMENT_BYTES = 25 * 1024 * 1024
_FETCH_UID_RE = re.compile(rb"UID\s+(\d+)", re.IGNORECASE)
ACCOUNT_HEADER = "X-Agent-Mail-Account"
DEFAULT_IMAP_TIMEOUT_SECONDS = 45


@dataclass
class MailAccount:
    account_id: str
    provider: str
    user: str
    imap_host: str
    imap_port: int
    imap_client_value: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_client_value: str
    from_name: str = "邮箱智能体"


def load_config(path: Path | None = None) -> dict:
    return load_raw_config(path)


def _to_account(cfg: dict) -> MailAccount:
    return MailAccount(
        account_id=cfg.get("id", ""),
        provider=cfg.get("provider", "custom"),
        user=cfg.get("user", ""),
        imap_host=cfg.get("imap_host", ""),
        imap_port=int(cfg.get("imap_port", 993) or 993),
        imap_client_value=cfg.get("imap_client_value", ""),
        smtp_host=cfg.get("smtp_host", ""),
        smtp_port=int(cfg.get("smtp_port", 465) or 465),
        smtp_user=cfg.get("smtp_user") or cfg.get("user", ""),
        smtp_client_value=cfg.get("smtp_client_value") or cfg.get("imap_client_value", ""),
        from_name=cfg.get("from_name", "邮箱智能体"),
    )


def load_account(account_id: str = "", path: Path | None = None) -> MailAccount:
    return _to_account(select_account(account_id, path))


def load_all_accounts(path: Path | None = None) -> list[MailAccount]:
    _, accounts = load_accounts(path)
    return [_to_account(account) for account in accounts.values()]


def connect_imap(
    account: MailAccount | None = None,
    timeout: int = DEFAULT_IMAP_TIMEOUT_SECONDS,
) -> imaplib.IMAP4_SSL:
    account = account or load_account()
    if not account.imap_host or not account.user or not account.imap_client_value:
        raise ValueError("缺少 IMAP 配置：请先运行 init_config.py。")
    context = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(
        account.imap_host,
        account.imap_port,
        ssl_context=context,
        timeout=max(1, int(timeout)),
    )
    imap.login(account.user, account.imap_client_value)
    return imap


def _decode_body(part: email.message.Message) -> str:
    payload = part.get_payload(decode=True)
    if payload is None:
        return ""
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except (LookupError, UnicodeDecodeError):
        return payload.decode("utf-8", errors="replace")


def _safe_name(value: str, fallback: str = "message") -> str:
    cleaned = _TAG_RE.sub("_", (value or fallback).strip("<> "))
    return cleaned[:120] or fallback


def parse_message(raw: bytes, uid: str = "", mailbox: str = "INBOX", include_body_limit: int = 20000) -> dict:
    msg = email.message_from_bytes(raw, policy=email.policy.compat32)
    text_body = ""
    html_body = ""
    attachments: list[str] = []
    attachment_parts: list[dict] = []

    for part_no, part in enumerate(msg.walk() if msg.is_multipart() else [msg], 1):
        content_disposition = str(part.get("Content-Disposition", "")).lower()
        filename = part.get_filename()
        content_type = part.get_content_type()
        if filename or "attachment" in content_disposition:
            decoded_name = decode_mime_header(filename or f"attachment-{part_no}")
            attachments.append(decoded_name)
            attachment_parts.append(
                {
                    "part": str(part_no),
                    "filename": decoded_name,
                    "content_type": content_type,
                    "size": len(part.get_payload(decode=True) or b""),
                }
            )
            continue
        decoded = _decode_body(part)
        if content_type == "text/plain" and not text_body:
            text_body = decoded
        elif content_type == "text/html" and not html_body:
            html_body = decoded

    body = text_body.strip() if text_body.strip() else html_to_text(html_body)
    return {
        "uid": uid,
        "mailbox": mailbox,
        "subject": decode_mime_header(msg.get("Subject", "")),
        "from": decode_mime_header(msg.get("From", "")),
        "to": decode_mime_header(msg.get("To", "")),
        "cc": decode_mime_header(msg.get("Cc", "")),
        "date": msg.get("Date", ""),
        "message_id": msg.get("Message-ID", "").strip("<> "),
        "in_reply_to": msg.get("In-Reply-To", "").strip("<> "),
        "references": msg.get("References", ""),
        "body": body[:include_body_limit],
        "links": extract_links(html_body, body)[:100],
        "attachments": attachments[:100],
        "attachment_parts": attachment_parts[:100],
    }


def parse_header_message(raw: bytes, uid: str = "", mailbox: str = "INBOX") -> dict:
    msg = email.message_from_bytes(raw, policy=email.policy.compat32)
    return {
        "uid": uid,
        "mailbox": mailbox,
        "subject": decode_mime_header(msg.get("Subject", "")),
        "from": decode_mime_header(msg.get("From", "")),
        "to": decode_mime_header(msg.get("To", "")),
        "cc": decode_mime_header(msg.get("Cc", "")),
        "date": msg.get("Date", ""),
        "message_id": msg.get("Message-ID", "").strip("<> "),
        "in_reply_to": msg.get("In-Reply-To", "").strip("<> "),
        "references": msg.get("References", ""),
        "body": "",
        "links": [],
        "attachments": [],
        "attachment_parts": [],
    }


def _imap_date(value: str) -> str:
    parsed = datetime.fromisoformat(value).date()
    return parsed.strftime("%d-%b-%Y")


def build_search_criteria(
    query: str = "",
    sender: str = "",
    subject: str = "",
    since: str = "",
    before: str = "",
    unseen: bool = False,
    seen: bool = False,
) -> list[str]:
    criteria = ["ALL"]
    if unseen:
        criteria.append("UNSEEN")
    if seen:
        criteria.append("SEEN")
    if since:
        criteria.extend(["SINCE", _imap_date(since)])
    if before:
        criteria.extend(["BEFORE", _imap_date(before)])
    if sender:
        criteria.extend(["FROM", f'"{sender}"'])
    if subject and subject.isascii():
        criteria.extend(["SUBJECT", f'"{subject}"'])
    if query and query.isascii():
        criteria.extend(["TEXT", f'"{query}"'])
    return criteria


def search_messages(
    query: str = "",
    sender: str = "",
    subject: str = "",
    since: str = "",
    before: str = "",
    has_attachment: bool = False,
    unseen: bool = False,
    seen: bool = False,
    mailbox: str = "INBOX",
    limit: int = 20,
    account: MailAccount | None = None,
) -> list[dict]:
    account = account or load_account()
    imap = connect_imap(account)
    try:
        imap.select(mailbox, readonly=True)
        criteria = build_search_criteria(query, sender, subject, since, before, unseen, seen)
        status, data = imap.uid("SEARCH", None, *criteria)
        if status != "OK" or not data:
            return []
        server_filtered_query = bool(query and query.isascii())
        needs_body = bool(has_attachment or (query and not query.isascii()))
        candidate_limit = max(limit * 5, limit + 50) if needs_body else limit
        uids = data[0].split()[-candidate_limit:]
        if not uids:
            return []

        fetch_cmd = (
            "(UID BODY.PEEK[]<0.16384>)"
            if needs_body
            else "(UID BODY.PEEK[HEADER.FIELDS (SUBJECT FROM TO CC DATE MESSAGE-ID IN-REPLY-TO REFERENCES)])"
        )
        status, fetched_items = imap.uid(
            "FETCH", b",".join(uids).decode("ascii"), fetch_cmd
        )
        if status != "OK" or not fetched_items:
            return []

        results = []
        for meta, raw in reversed(_fetch_pairs(fetched_items)):
            uid_match = _FETCH_UID_RE.search(meta)
            uid = uid_match.group(1).decode("ascii", errors="replace") if uid_match else ""
            if not uid or not raw:
                continue
            item = (
                parse_message(raw, uid=uid, mailbox=mailbox, include_body_limit=4000)
                if needs_body
                else parse_header_message(raw, uid=uid, mailbox=mailbox)
            )
            item["account"] = account.account_id
            if has_attachment and not item["attachments"]:
                continue
            searchable = "\n".join([item.get("subject", ""), item.get("from", ""), item.get("body", "")]).lower()
            if query and not server_filtered_query and query.lower() not in searchable:
                continue
            if subject and subject.lower() not in item.get("subject", "").lower():
                continue
            results.append(item)
            if len(results) >= limit:
                break
        return results
    finally:
        _close_imap(imap)


def _first_fetch_bytes(data: list) -> bytes:
    for item in data:
        if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], bytes):
            return item[1]
    return b""


def _fetch_pairs(data: list) -> list[tuple[bytes, bytes]]:
    return [
        (item[0], item[1])
        for item in data
        if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[0], bytes) and isinstance(item[1], bytes)
    ]


def fetch_message(uid: str, mailbox: str = "INBOX", mark_seen: bool = False, account: MailAccount | None = None) -> tuple[dict, bytes]:
    account = account or load_account()
    imap = connect_imap(account)
    try:
        imap.select(mailbox, readonly=not mark_seen)
        fetch_cmd = "(RFC822)" if mark_seen else "(BODY.PEEK[])"
        status, data = imap.uid("FETCH", uid, fetch_cmd)
        if status != "OK":
            raise ValueError(f"读取邮件失败：UID {uid}")
        raw = _first_fetch_bytes(data)
        if not raw:
            raise ValueError(f"未找到邮件：UID {uid}")
        item = parse_message(raw, uid=uid, mailbox=mailbox)
        item["account"] = account.account_id
        return item, raw
    finally:
        _close_imap(imap)


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for idx in range(2, 1000):
        candidate = path.with_name(f"{path.stem}_{idx}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise ValueError(f"无法生成不冲突的文件名：{path.name}")


def download_attachments(
    uid: str,
    output_dir: Path,
    mailbox: str = "INBOX",
    account: MailAccount | None = None,
    allow_risky: bool = False,
    max_attachment_bytes: int = _DEFAULT_MAX_ATTACHMENT_BYTES,
) -> list[Path]:
    item, raw = fetch_message(uid, mailbox=mailbox, account=account)
    msg = email.message_from_bytes(raw, policy=email.policy.compat32)
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for part_no, part in enumerate(msg.walk() if msg.is_multipart() else [msg], 1):
        content_disposition = str(part.get("Content-Disposition", "")).lower()
        filename = part.get_filename()
        if not filename and "attachment" not in content_disposition:
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        name = _safe_name(decode_mime_header(filename or f"attachment-{part_no}"), f"attachment-{part_no}")
        path = _unique_path(output_dir / name)
        if not allow_risky and path.suffix.lower() in _BLOCKED_ATTACHMENT_EXTENSIONS:
            raise ValueError(f"附件类型风险较高，已阻止保存：{name}")
        if max_attachment_bytes > 0 and len(payload) > max_attachment_bytes:
            raise ValueError(f"附件超过大小限制，已阻止保存：{name}")
        path.write_bytes(payload)
        saved.append(path)
    if not saved and item.get("attachments"):
        raise ValueError("邮件声明了附件，但未能解析附件内容。")
    return saved


def mark_seen(uid: str, mailbox: str = "INBOX", seen: bool = True, account: MailAccount | None = None) -> None:
    imap = connect_imap(account)
    try:
        imap.select(mailbox, readonly=False)
        op = "+FLAGS" if seen else "-FLAGS"
        imap.uid("STORE", uid, op, r"(\Seen)")
    finally:
        _close_imap(imap)


def move_message(uid: str, target_mailbox: str, mailbox: str = "INBOX", account: MailAccount | None = None) -> None:
    imap = connect_imap(account)
    try:
        imap.select(mailbox, readonly=False)
        status, _ = imap.uid("COPY", uid, target_mailbox)
        if status != "OK":
            raise ValueError(f"复制到目标文件夹失败：{target_mailbox}")
        imap.uid("STORE", uid, "+FLAGS", r"(\Deleted)")
        imap.expunge()
    finally:
        _close_imap(imap)


def save_raw_message(uid: str, output_dir: Path, mailbox: str = "INBOX", account: MailAccount | None = None) -> Path:
    item, raw = fetch_message(uid, mailbox=mailbox, account=account)
    output_dir.mkdir(parents=True, exist_ok=True)
    name = _safe_name(item.get("message_id") or uid, f"message-{uid}") + ".eml"
    path = output_dir / name
    path.write_bytes(raw)
    return path


def build_reply_draft(original: dict, body: str, account: MailAccount | None = None) -> EmailMessage:
    account = account or load_account()
    msg = EmailMessage()
    msg[ACCOUNT_HEADER] = account.account_id
    msg["From"] = account.smtp_user or account.user
    msg["To"] = original.get("from", "")
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    if original.get("message_id"):
        msg["In-Reply-To"] = f"<{original['message_id']}>"
        msg["References"] = (original.get("references", "") + f" <{original['message_id']}>").strip()
    subject = original.get("subject") or "(无主题)"
    msg["Subject"] = subject if subject.lower().startswith("re:") else "Re: " + subject
    quoted = "\n".join(["> " + line for line in (original.get("body") or "").splitlines()[:120]])
    msg.set_content((body or "").strip() + "\n\n---------- 原邮件 ----------\n" + quoted + "\n", charset="utf-8")
    return msg


def build_forward_draft(original: dict, recipient: str, body: str = "", account: MailAccount | None = None) -> EmailMessage:
    account = account or load_account()
    msg = EmailMessage()
    msg[ACCOUNT_HEADER] = account.account_id
    msg["From"] = account.smtp_user or account.user
    msg["To"] = recipient
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    subject = original.get("subject") or "(无主题)"
    msg["Subject"] = subject if subject.lower().startswith("fw:") else "Fw: " + subject
    msg.set_content(
        "\n".join(
            [
                (body or "请查阅以下邮件。").strip(),
                "",
                "---------- 原邮件信息 ----------",
                f"发件人：{original.get('from', '')}",
                f"时间：{original.get('date', '')}",
                f"主题：{subject}",
                "",
                "---------- 原邮件内容 ----------",
                original.get("body", ""),
                "",
            ]
        ),
        charset="utf-8",
    )
    return msg


def save_draft(message: EmailMessage, output_dir: Path, prefix: str = "draft") -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.eml"
    path.write_bytes(bytes(message))
    return path


def send_message(message: EmailMessage, account: MailAccount | None = None) -> None:
    account = account or load_account()
    if not account.smtp_host or not account.smtp_user or not account.smtp_client_value:
        raise ValueError("缺少 SMTP 配置，无法发送。")
    if account.smtp_port == 587:
        with smtplib.SMTP(account.smtp_host, account.smtp_port, timeout=60) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(account.smtp_user, account.smtp_client_value)
            smtp.send_message(message)
    else:
        with smtplib.SMTP_SSL(account.smtp_host, account.smtp_port, timeout=60) as smtp:
            smtp.login(account.smtp_user, account.smtp_client_value)
            smtp.send_message(message)


def load_draft(path: Path) -> EmailMessage:
    return email.message_from_bytes(path.read_bytes(), policy=email.policy.default)


def parse_date_for_sort(item: dict) -> datetime | None:
    try:
        return parsedate_to_datetime(item.get("date", ""))
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def _close_imap(imap: imaplib.IMAP4_SSL) -> None:
    try:
        imap.close()
    except Exception:
        pass
    try:
        imap.logout()
    except Exception:
        pass
