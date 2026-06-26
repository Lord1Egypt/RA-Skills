#!/usr/bin/env python3
"""Download Gmail attachments via IMAP with explicit CLI arguments."""

from __future__ import annotations

import argparse
import email
import imaplib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from email.header import decode_header
from email.message import Message
from pathlib import Path
from typing import Iterable


GMAIL_IMAP_HOST = "imap.gmail.com"
DEFAULT_ALL_MAIL_CANDIDATES = (
    "[Gmail]/All Mail",
    "[Google Mail]/All Mail",
    "[Gmail]/&YkBnCZCuTvY-",
)


@dataclass
class Config:
    gmail_user: str
    gmail_pass: str
    sender: str
    subject: str
    since: str
    before: str
    save_folder: Path
    extensions: list[str]
    max_results: int
    mailbox: str
    dry_run: bool
    summary_json: str


def parse_args(argv: list[str]) -> Config:
    parser = argparse.ArgumentParser(
        description="Download Gmail attachments through IMAP."
    )
    parser.add_argument("--gmail-user", default=os.environ.get("GMAIL_USER", ""))
    parser.add_argument("--gmail-pass", default=os.environ.get("GMAIL_PASS", ""))
    parser.add_argument("--sender", default="")
    parser.add_argument("--subject", default="")
    parser.add_argument("--since", default="")
    parser.add_argument("--before", default="")
    parser.add_argument(
        "--save-folder",
        default="~/Documents/gmail-attachments",
    )
    parser.add_argument(
        "--extensions",
        default="",
        help="Comma-separated list such as .pdf,.ofd. Empty means all.",
    )
    parser.add_argument("--max-results", type=int, default=500)
    parser.add_argument(
        "--mailbox",
        default="auto",
        help="Mailbox name. Default auto-detects Gmail All Mail and falls back to INBOX.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List matching attachments without writing files.",
    )
    parser.add_argument(
        "--summary-json",
        default="",
        help="Optional path for a JSON summary report.",
    )
    args = parser.parse_args(argv)

    return Config(
        gmail_user=args.gmail_user.strip(),
        gmail_pass=args.gmail_pass.strip(),
        sender=args.sender.strip(),
        subject=args.subject.strip(),
        since=args.since.strip(),
        before=args.before.strip(),
        save_folder=Path(os.path.expanduser(args.save_folder)).resolve(),
        extensions=normalize_extensions(args.extensions),
        max_results=max(args.max_results, 1),
        mailbox=args.mailbox.strip() or "auto",
        dry_run=args.dry_run,
        summary_json=args.summary_json.strip(),
    )


def normalize_extensions(value: str) -> list[str]:
    items = []
    for raw in value.split(","):
        ext = raw.strip().lower()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        items.append(ext)
    return items


def decode_mime_text(value: str | None) -> str:
    if not value:
        return ""

    parts = []
    for chunk, encoding in decode_header(value):
        if isinstance(chunk, bytes):
            tried = [encoding, "utf-8", "gb18030", "gbk", "latin1"]
            for candidate in tried:
                if not candidate:
                    continue
                try:
                    parts.append(chunk.decode(candidate))
                    break
                except (LookupError, UnicodeDecodeError):
                    continue
            else:
                parts.append(chunk.decode("utf-8", errors="replace"))
        else:
            parts.append(chunk)
    return "".join(parts)


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\r\n]+", "_", filename).strip()
    return cleaned or "attachment"


def build_search_terms(config: Config) -> list[str]:
    terms = ["ALL"]
    if config.sender:
        terms.extend(["FROM", f'"{config.sender}"'])
    if config.subject:
        terms.extend(["SUBJECT", f'"{config.subject}"'])
    if config.since:
        terms.extend(["SINCE", f'"{config.since}"'])
    if config.before:
        terms.extend(["BEFORE", f'"{config.before}"'])
    return terms


def validate_imap_date(value: str, label: str) -> None:
    if not value:
        return
    try:
        datetime.strptime(value, "%d-%b-%Y")
    except ValueError as exc:
        raise ValueError(f"Invalid {label} date: {value}. Expected DD-Mon-YYYY.") from exc


def choose_mailbox(mail: imaplib.IMAP4_SSL, requested: str) -> str:
    if requested.lower() != "auto":
        return requested

    status, data = mail.list()
    if status == "OK":
        available = b"\n".join(item for item in data if item)
        for candidate in DEFAULT_ALL_MAIL_CANDIDATES:
            if candidate.encode() in available:
                return candidate
    return "INBOX"


def extract_filename(part: Message) -> str:
    filename = part.get_filename()
    if filename:
        return sanitize_filename(decode_mime_text(filename))

    content_disposition = str(part.get("Content-Disposition") or "")
    match = re.search(r"filename\*?=\"?([^;\"]+)\"?", content_disposition, re.IGNORECASE)
    if match:
        return sanitize_filename(decode_mime_text(match.group(1).strip()))
    return ""


def iter_attachments(msg: Message) -> Iterable[tuple[str, bytes]]:
    for part in msg.walk():
        if part.is_multipart():
            continue

        disposition = str(part.get("Content-Disposition") or "")
        filename = extract_filename(part)
        if not filename:
            continue
        if "attachment" not in disposition.lower() and not filename:
            continue

        payload = part.get_payload(decode=True)
        if payload:
            yield filename, payload


def unique_destination(folder: Path, filename: str, date_str: str) -> Path:
    base_name, ext = os.path.splitext(filename)
    candidate = f"{base_name}_{date_str}{ext}" if date_str else filename
    path = folder / candidate
    counter = 1
    while path.exists():
        suffix = f"{base_name}_{date_str}_{counter}{ext}" if date_str else f"{base_name}_{counter}{ext}"
        path = folder / suffix
        counter += 1
    return path


def message_date_string(msg: Message) -> str:
    raw = msg.get("Date")
    if not raw:
        return ""
    parsed = email.utils.parsedate(raw)
    if not parsed:
        return ""
    try:
        return datetime(*parsed[:6]).strftime("%Y%m%d")
    except ValueError:
        return ""


def validate_config(config: Config) -> int:
    if not config.gmail_user:
        print("Missing Gmail user. Pass --gmail-user or set GMAIL_USER.", file=sys.stderr)
        return 2
    if not config.gmail_pass:
        print("Missing Gmail app password. Pass --gmail-pass or set GMAIL_PASS.", file=sys.stderr)
        return 2
    try:
        validate_imap_date(config.since, "since")
        validate_imap_date(config.before, "before")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


def write_summary(path: str, summary: dict[str, object]) -> None:
    if not path:
        return
    summary_path = Path(os.path.expanduser(path)).resolve()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def run(config: Config) -> int:
    validation_code = validate_config(config)
    if validation_code:
        return validation_code

    config.save_folder.mkdir(parents=True, exist_ok=True)
    print(f"Connecting to Gmail: {config.gmail_user}")
    print(f"Save folder: {config.save_folder}")
    print(f"Extensions: {', '.join(config.extensions) if config.extensions else 'all'}")
    if config.dry_run:
        print("Mode: dry-run")

    mail: imaplib.IMAP4_SSL | None = None
    downloaded = 0
    skipped = 0
    matched_messages = 0
    mailbox = config.mailbox
    matched_files: list[str] = []
    try:
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP_HOST)
        mail.login(config.gmail_user, config.gmail_pass)
        mailbox = choose_mailbox(mail, config.mailbox)
        status, _ = mail.select(mailbox)
        if status != "OK":
            print(f"Unable to select mailbox: {mailbox}", file=sys.stderr)
            return 1

        terms = build_search_terms(config)
        status, data = mail.search(None, *terms)
        if status != "OK":
            print("IMAP search failed.", file=sys.stderr)
            return 1

        message_ids = data[0].split()
        matched_messages = len(message_ids)
        if len(message_ids) > config.max_results:
            print(f"Matched {len(message_ids)} messages; limiting to {config.max_results}.")
            message_ids = message_ids[: config.max_results]

        if not message_ids:
            print("No matching messages found.")
            return 0

        print(f"Using mailbox: {mailbox}")
        print(f"Matched messages: {len(message_ids)}")

        for index, message_id in enumerate(message_ids, start=1):
            if index % 10 == 0:
                print(f"Processed {index}/{len(message_ids)} messages...")

            status, msg_data = mail.fetch(message_id, "(RFC822)")
            if status != "OK" or not msg_data or not msg_data[0]:
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            date_str = message_date_string(msg)

            for filename, payload in iter_attachments(msg):
                ext = os.path.splitext(filename)[1].lower()
                if config.extensions and ext not in config.extensions:
                    skipped += 1
                    continue

                destination = unique_destination(config.save_folder, filename, date_str)
                matched_files.append(destination.name)
                if config.dry_run:
                    print(f"Matched: {destination.name}")
                    continue
                destination.write_bytes(payload)
                downloaded += 1
                print(f"Downloaded: {destination.name}")

    except imaplib.IMAP4.error as exc:
        print(f"IMAP authentication or mailbox error: {exc}", file=sys.stderr)
        print("Check that IMAP is enabled and the Gmail app password is correct.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Filesystem or network error: {exc}", file=sys.stderr)
        return 1
    finally:
        if mail is not None:
            try:
                mail.close()
            except (imaplib.IMAP4.error, OSError):
                pass
            try:
                mail.logout()
            except (imaplib.IMAP4.error, OSError):
                pass

    summary = {
        "gmail_user": config.gmail_user,
        "mailbox": mailbox,
        "dry_run": config.dry_run,
        "matched_messages": matched_messages,
        "matched_files": matched_files,
        "downloaded": downloaded,
        "skipped": skipped,
        "save_folder": str(config.save_folder),
    }
    write_summary(config.summary_json, summary)

    action = "Matched" if config.dry_run else "Completed. Downloaded"
    count = len(matched_files) if config.dry_run else downloaded
    print(f"{action} {count} attachments; skipped {skipped}.")
    print(f"Files saved to: {config.save_folder}")
    if downloaded == 0 and config.extensions:
        print("Hint: retry without --extensions to confirm the mailbox has attachments with different file types.")
    if config.summary_json:
        print(f"Summary written to: {Path(os.path.expanduser(config.summary_json)).resolve()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run(parse_args(argv or sys.argv[1:]))


if __name__ == "__main__":
    raise SystemExit(main())
