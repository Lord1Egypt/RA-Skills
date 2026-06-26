from __future__ import annotations

import email
import imaplib
import re
from datetime import datetime, timezone
from email.header import decode_header
from email.utils import parsedate_to_datetime
from html import unescape
from typing import Iterable

from .config import RuntimeConfig
from .models import AttachmentPayload, ParsedMessage


def _decode_header(value: str | None) -> str:
    if not value:
        return ""
    parts: list[str] = []
    for text, enc in decode_header(value):
        if isinstance(text, bytes):
            try:
                parts.append(text.decode(enc or "utf-8", errors="replace"))
            except LookupError:
                parts.append(text.decode("utf-8", errors="replace"))
        else:
            parts.append(text)
    return "".join(parts)


def _normalize_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class IMAPMailbox:
    def __init__(self, config: RuntimeConfig, account: str, password: str, folder: str = "INBOX") -> None:
        self.config = config
        self.account = account
        self.password = password
        self.folder = folder
        self.connection: imaplib.IMAP4_SSL | None = None
        self.connected_host: str | None = None

    def connect(self) -> tuple[str, str]:
        last_error: Exception | None = None
        for host in self.config.host_candidates:
            try:
                conn = imaplib.IMAP4_SSL(host, self.config.imap_port)
                conn.login(self.account, self.password)
                if self.config.imap_send_id and self.config.imap_client_id:
                    imaplib.Commands["ID"] = "AUTH"
                    try:
                        conn._simple_command("ID", self.config.imap_client_id)
                    except Exception:
                        pass
                conn.select(self.folder, readonly=True)
                self.connection = conn
                self.connected_host = host
                return host, self.folder
            except Exception as exc:
                last_error = exc
        if last_error is None:
            raise RuntimeError("No IMAP host candidates configured")
        raise RuntimeError(f"Unable to connect to IMAP: {last_error}") from last_error

    def close(self) -> None:
        if not self.connection:
            return
        try:
            self.connection.logout()
        except Exception:
            pass
        self.connection = None

    def month_status(self, month: str) -> dict[str, object]:
        if not self.connection:
            self.connect()
        assert self.connection is not None
        year, month_num = map(int, month.split("-"))
        since, before = _month_bounds(year, month_num)
        typ, data = self.connection.search(None, "SINCE", since, "BEFORE", before)
        if typ != "OK":
            raise RuntimeError(f"IMAP SEARCH failed: {data}")
        ids = data[0].split() if data and data[0] else []
        return {
            "message_count": len(ids),
            "ids": [item.decode() for item in ids],
        }

    def iter_month_messages(self, month: str, limit: int | None = None) -> Iterable[ParsedMessage]:
        if not self.connection:
            self.connect()
        assert self.connection is not None
        year, month_num = map(int, month.split("-"))
        since, before = _month_bounds(year, month_num)
        typ, data = self.connection.search(None, "SINCE", since, "BEFORE", before)
        if typ != "OK":
            raise RuntimeError(f"IMAP SEARCH failed: {data}")
        ids = data[0].split() if data and data[0] else []
        if limit:
            ids = ids[-limit:]
        for raw_id in ids:
            typ, msg_data = self.connection.fetch(raw_id, "(BODY.PEEK[])")
            if typ != "OK":
                continue
            raw = b""
            for part in msg_data:
                if isinstance(part, tuple):
                    raw += part[1]
            if not raw:
                continue
            message = email.message_from_bytes(raw)
            sender = _decode_header(message.get("From", ""))
            subject = _decode_header(message.get("Subject", ""))
            received_at = None
            try:
                received_at = parsedate_to_datetime(message.get("Date"))
                if received_at.tzinfo is None:
                    received_at = received_at.replace(tzinfo=timezone.utc)
            except Exception:
                received_at = None
            body_text = _extract_body_text(message)
            preview = body_text[:180]
            attachments: list[AttachmentPayload] = []
            part_counter = 0
            for part in message.walk():
                filename = part.get_filename()
                if not filename:
                    continue
                payload = part.get_payload(decode=True) or b""
                attachments.append(
                    AttachmentPayload(
                        part_ref=f"part-{part_counter}",
                        filename=_decode_header(filename),
                        content_type=part.get_content_type(),
                        data=payload,
                        source_ref=_decode_header(filename),
                    )
                )
                part_counter += 1
            yield ParsedMessage(
                uid=raw_id.decode(),
                account=self.account,
                folder=self.folder,
                received_at=received_at,
                sender=sender,
                subject=subject,
                preview=preview,
                body_text=body_text,
                attachments=attachments,
            )


def _month_bounds(year: int, month: int) -> tuple[str, str]:
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    return start.strftime("%d-%b-%Y"), end.strftime("%d-%b-%Y")


def _extract_body_text(message: email.message.Message) -> str:
    texts: list[str] = []
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = (part.get("Content-Disposition") or "").lower()
            if "attachment" in disposition:
                continue
            if content_type not in {"text/plain", "text/html"}:
                continue
            payload = part.get_payload(decode=True) or b""
            charset = part.get_content_charset() or "utf-8"
            try:
                text = payload.decode(charset, errors="replace")
            except LookupError:
                text = payload.decode("utf-8", errors="replace")
            texts.append(_normalize_text(text))
    else:
        payload = message.get_payload(decode=True) or b""
        charset = message.get_content_charset() or "utf-8"
        try:
            text = payload.decode(charset, errors="replace")
        except LookupError:
            text = payload.decode("utf-8", errors="replace")
        texts.append(_normalize_text(text))
    return _normalize_text(" ".join(texts))
