#!/usr/bin/env python3
"""Read mailbox messages via IMAP."""

from __future__ import annotations

import argparse
import email
import email.policy
import imaplib
import json
import os
import re
import ssl
import sys
from datetime import datetime, timedelta, timezone
from email.header import decode_header
from email.utils import parsedate_to_datetime
from pathlib import Path

from mail_accounts import load_raw_config, select_account

_EN_MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

# ---------------------------------------------------------------------------
# Module-level compiled regexes – compiled once, reused for every message.
# ---------------------------------------------------------------------------
_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_P_CLOSE_RE = re.compile(r"</p\s*>", re.IGNORECASE)
_TAG_RE = re.compile(r"</?[^>]+>")
_MULTI_NL_RE = re.compile(r"\n{3,}")
_HREF_RE = re.compile(
    r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.IGNORECASE | re.DOTALL
)
_PLAIN_URL_RE = re.compile(r"https?://[^\s<>'\")，。；、]+", re.IGNORECASE)
_FETCH_SEQ_RE = re.compile(rb"(\d+)\s+FETCH")
_FETCH_UID_RE = re.compile(rb"UID\s+(\d+)", re.IGNORECASE)


def load_config(path_str: str) -> dict:
    return load_raw_config(path_str)


def decode_mime_header(value: str) -> str:
    if not value:
        return ""
    decoded = []
    for part, charset in decode_header(value):
        if isinstance(part, bytes):
            decoded.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return "".join(decoded)


def _decode_payload(part: email.message.Message) -> str:
    payload = part.get_payload(decode=True)
    if payload is None:
        return ""
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except (LookupError, UnicodeDecodeError):
        return payload.decode("utf-8", errors="replace")


def html_to_text(html: str) -> str:
    text = _BR_RE.sub("\n", html)
    text = _P_CLOSE_RE.sub("\n", text)
    text = _TAG_RE.sub("", text)
    replacements = {
        "&nbsp;": " ",
        "&lt;": "<",
        "&gt;": ">",
        "&amp;": "&",
        "&quot;": '"',
        "&#39;": "'",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return _MULTI_NL_RE.sub("\n\n", text).strip()


def extract_links(html: str, text: str) -> list[dict]:
    links: list[dict] = []
    for href, label_html in _HREF_RE.findall(html or ""):
        label = html_to_text(label_html)
        links.append({"url": href.strip(), "text": label.strip()})
    seen = {item["url"] for item in links}
    for url in _PLAIN_URL_RE.findall((text or "") + "\n" + (html or "")):
        if url not in seen:
            links.append({"url": url, "text": ""})
            seen.add(url)
    return links


def extract_message_parts(
    msg: email.message.Message,
) -> tuple[str, list[dict], list[str]]:
    text_body = ""
    html_body = ""
    attachments: list[str] = []

    for part in msg.walk() if msg.is_multipart() else [msg]:
        content_disposition = str(part.get("Content-Disposition", "")).lower()
        filename = part.get_filename()
        if filename:
            attachments.append(decode_mime_header(filename))
            continue
        if "attachment" in content_disposition:
            attachments.append(decode_mime_header(filename or "(unnamed attachment)"))
            continue

        content_type = part.get_content_type()
        decoded = _decode_payload(part)
        if content_type == "text/plain" and not text_body:
            text_body = decoded
        elif content_type == "text/html" and not html_body:
            html_body = decoded

    body = text_body.strip() if text_body.strip() else html_to_text(html_body)
    return body, extract_links(html_body, body), attachments


def _imap_since_date(dt: datetime) -> str:
    return f"{dt.day:02d}-{_EN_MONTHS[dt.month - 1]}-{dt.year}"


def _parse_email_date(date_str: str) -> datetime | None:
    try:
        parsed = parsedate_to_datetime(date_str)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _safe_raw_name(message_id: str, fallback: bytes) -> str:
    value = message_id or fallback.decode("ascii", errors="ignore") or "message"
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip("<> "))
    return (value[:120] or "message") + ".eml"


def _parse_fetch_response(data: list) -> list[tuple[bytes, bytes]]:
    """Extract (meta_bytes, content_bytes) pairs from an IMAP FETCH response."""
    return [
        (item[0], item[1])
        for item in data
        if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], bytes)
    ]


def _extract_date_from_header_bytes(raw: bytes) -> str:
    """Return the Date header value from raw IMAP header bytes."""
    for line in raw.decode("utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("date:"):
            return stripped[5:].strip()
    return ""


def fetch_emails(
    imap_host: str,
    imap_port: int,
    user: str,
    client_value: str,
    since_hours: int = 2,
    mailbox: str = "INBOX",
    max_emails: int = 30,
    mark_seen: bool = False,
    raw_dir: str = "",
    account_id: str = "",
    timeout: int = 60,
) -> list[dict]:
    context = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(
        imap_host,
        imap_port,
        ssl_context=context,
        timeout=max(1, int(timeout)),
    )
    try:
        imap.login(user, client_value)
        imap.select(mailbox, readonly=not mark_seen)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        since_str = _imap_since_date(cutoff)
        status, data = imap.search(None, f"(SINCE {since_str})")
        if status != "OK":
            print(f"SEARCH failed: {data}", file=sys.stderr)
            return []

        # IMAP SINCE is day-granular; take a modest buffer beyond max_emails
        # to catch messages near the hour boundary without fetching the whole day.
        candidate_ids = data[0].split()[-max(max_emails * 3, max_emails + 30) :]
        if not candidate_ids:
            return []

        # Full fetch only when we need to preserve the raw .eml or mark seen.
        # Otherwise fetch only the first 32 KB (covers headers + body start),
        # which is enough for analysis and cuts download time by up to 80%.
        if mark_seen:
            fetch_cmd = "(UID RFC822)"
        elif raw_dir:
            fetch_cmd = "(UID BODY.PEEK[])"
        else:
            fetch_cmd = "(UID BODY.PEEK[]<0.32768>)"

        print("正在检索候选邮件...", file=sys.stderr, flush=True)

        # ------------------------------------------------------------------
        # Phase 1: Batch-fetch Date headers in ONE round-trip to filter out
        # messages older than the exact cutoff before downloading full bodies.
        # ------------------------------------------------------------------
        id_pass: dict[bytes, bool] = {}
        hdr_status, hdr_data = imap.fetch(
            b",".join(candidate_ids),
            "(BODY.PEEK[HEADER.FIELDS (DATE)])",
        )
        if hdr_status == "OK" and hdr_data:
            for meta, content in _parse_fetch_response(hdr_data):
                m = _FETCH_SEQ_RE.match(meta)
                if not m:
                    continue
                seq_id = m.group(1)
                date_str = _extract_date_from_header_bytes(content)
                parsed = _parse_email_date(date_str) if date_str else None
                # Keep if date is unknown (err on inclusive side) or within window.
                id_pass[seq_id] = parsed is None or parsed >= cutoff

        # Preserve original order; IDs missing from Phase 1 response are kept.
        recent_ids = [mid for mid in candidate_ids if id_pass.get(mid, True)]
        recent_ids = recent_ids[-max_emails:]

        if not recent_ids:
            return []

        # ------------------------------------------------------------------
        # Phase 2: Batch-fetch messages for the filtered IDs in ONE round-trip.
        # ------------------------------------------------------------------
        print(f"正在下载 {len(recent_ids)} 封邮件正文...", file=sys.stderr, flush=True)
        full_status, full_data = imap.fetch(b",".join(recent_ids), fetch_cmd)
        if full_status != "OK" or not full_data:
            return []

        raw_out_dir = Path(raw_dir) if raw_dir else None
        if raw_out_dir:
            raw_out_dir.mkdir(parents=True, exist_ok=True)

        results: list[dict] = []
        for meta, content in _parse_fetch_response(full_data):
            msg = email.message_from_bytes(content, policy=email.policy.compat32)
            date_str = msg.get("Date", "")
            parsed_date = _parse_email_date(date_str)
            # Safety re-check in case Phase 1 header bytes were ambiguous.
            if parsed_date and parsed_date < cutoff:
                continue
            body, links, attachments = extract_message_parts(msg)
            message_id = msg.get("Message-ID", "").strip("<> ")
            seq_m = _FETCH_SEQ_RE.match(meta)
            mid = seq_m.group(1) if seq_m else b"unknown"
            uid_m = _FETCH_UID_RE.search(meta)
            uid = uid_m.group(1).decode("ascii", errors="replace") if uid_m else ""
            item = {
                "account": account_id,
                "uid": uid,
                "mailbox": mailbox,
                "subject": decode_mime_header(msg.get("Subject", "")),
                "from": decode_mime_header(msg.get("From", "")),
                "to": decode_mime_header(msg.get("To", "")),
                "date": date_str,
                "message_id": message_id,
                "body": body[:8000],
                "links": links[:50],
                "attachments": attachments[:50],
            }
            if raw_out_dir:
                raw_path = raw_out_dir / _safe_raw_name(message_id, mid)
                raw_path.write_bytes(content)
                item["raw_path"] = str(raw_path)
            results.append(item)

        return results[-max_emails:]
    finally:
        try:
            imap.close()
        except Exception:
            pass
        imap.logout()


def main() -> int:
    parser = argparse.ArgumentParser(description="Read emails via IMAP")
    parser.add_argument(
        "--config", default=""
    )
    parser.add_argument("--account", default="", help="配置账号 ID；默认使用 default_account")
    parser.add_argument("--imap-host")
    parser.add_argument("--imap-port", type=int)
    parser.add_argument("--user")
    parser.add_argument("--value-env", default="")
    parser.add_argument("--since-hours", type=int, default=2)
    parser.add_argument("--mailbox", default="INBOX")
    parser.add_argument("--max-emails", type=int, default=30)
    parser.add_argument("--mark-seen", action="store_true")
    parser.add_argument(
        "--raw-dir",
        default="",
        help="Save original .eml files here and include raw_path in JSON",
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        account = select_account(args.account, args.config or None)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    user = args.user or account.get("user", "")
    env_client_value = os.environ.get(args.value_env, "") if args.value_env else ""
    client_value = env_client_value or account.get("imap_client_value", "")
    host = args.imap_host or account.get("imap_host", "")
    port = args.imap_port or account.get("imap_port", 993)
    if not user or not client_value or not host:
        print("Error: IMAP host, user and client value are required.", file=sys.stderr)
        return 1

    try:
        emails = fetch_emails(
            host,
            int(port),
            user,
            client_value,
            args.since_hours,
            args.mailbox,
            args.max_emails,
            args.mark_seen,
            args.raw_dir,
            account.get("id", ""),
        )
    except imaplib.IMAP4.error as exc:
        print(f"IMAP error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Connection error: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(emails, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
