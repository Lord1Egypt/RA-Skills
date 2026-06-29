#!/usr/bin/env python3
"""
Shared utility functions for the Email Assistant skill.

Functions:
- save_sync_state / get_sync_state: manage last-sync cursor per account
- format_email_list: pretty-print email summaries for LLM consumption
- save_attachments: download IMAP attachments to a temp directory
"""

import datetime
import json
import os
import sys
import tempfile

# Force UTF-8 for console output
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_dir import SYNC_STATE_PATH, ACCOUNTS_DIR


def save_sync_state(account_id, last_uid=None, last_time=None):
    """Save sync cursor for an account."""
    state = {}
    if os.path.exists(SYNC_STATE_PATH):
        with open(SYNC_STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)

    state[account_id] = {
        "last_uid": last_uid,
        "last_sync": (last_time or datetime.datetime.now()).isoformat(),
    }

    with open(SYNC_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_sync_state(account_id=None):
    """Get sync state. Returns all if account_id is None, else single."""
    if not os.path.exists(SYNC_STATE_PATH):
        return {} if account_id is None else None

    with open(SYNC_STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)

    if account_id:
        return state.get(account_id)
    return state


def format_email_list(emails, max_preview=80):
    """
    Format a list of email dicts into a human-readable string for LLM context.

    Args:
        emails: list of email dicts (from outlook_api or email_client output)
        max_preview: max chars for subject/from in preview

    Returns:
        Formatted string
    """
    if not emails:
        return "（没有邮件）"

    lines = []
    for i, email in enumerate(emails, 1):
        subject = (email.get("subject") or "(无主题)")[:max_preview]
        sender = (email.get("from") or email.get("from_name") or "?")[:max_preview]
        date = (email.get("received") or email.get("date") or "?")[:25]
        read_status = "✓" if email.get("is_read") else "○"
        has_att = " 📎" if email.get("has_attachments") else ""

        lines.append(f"{i}. [{read_status}] {subject}")
        lines.append(f"   发件人: {sender}  时间: {date}{has_att}")

    return "\n".join(lines)


def format_email_detail(email):
    """
    Format a single email detail into readable text.

    Args:
        email: full email dict (with body)

    Returns:
        Formatted string
    """
    subject = email.get("subject", "(无主题)")
    sender = email.get("from", "?")
    to = email.get("to", "")
    date = email.get("received") or email.get("date") or "?"
    body = email.get("body_text") or email.get("body") or ""
    if isinstance(body, dict):
        body = body.get("content", "")
    attachments = email.get("attachments", [])

    lines = [
        f"主题: {subject}",
        f"发件人: {sender}",
        f"收件人: {to}" if to else None,
        f"时间: {date}",
    ]
    lines = [l for l in lines if l]

    if attachments:
        att_names = []
        for a in attachments:
            if isinstance(a, dict):
                att_names.append(a.get("filename") or a.get("name", "?"))
            else:
                att_names.append(str(a))
        lines.append(f"附件: {', '.join(att_names)}")

    if body:
        body_preview = body[:3000]
        lines.append("")
        lines.append("--- 正文 ---")
        lines.append(body_preview)

    return "\n".join(lines)


def save_attachments(account_type, email_data, target_dir=None):
    """
    Placeholder: download and save attachments from an email.

    Currently returns a list of (filename, path_hint) pairs.
    Real attachment download requires IMAP fetch or Graph API download.

    Args:
        account_type: 'outlook', '163', or 'qq'
        email_data: email dict with attachments info
        target_dir: directory to save into (default: temp dir)

    Returns:
        list of (filename, saved_path)
    """
    save_dir = target_dir or tempfile.mkdtemp(prefix="email_attachments_")
    saved = []

    attachments = email_data.get("attachments", [])
    for att in attachments:
        filename = att.get("filename") or att.get("name", "attachment")
        saved.append((filename, os.path.join(save_dir, filename)))

    return saved


def main():
    """CLI entry point for debugging."""
    if len(sys.argv) < 2:
        print("Usage: python email_utils.py test-data")
        print("  Writes test JSON to stdout for LLM preview.")
        return

    if sys.argv[1] == "test-data":
        sample = [
            {
                "subject": "关于下周会议的安排",
                "from": "老板 <boss@company.com>",
                "received": "2026-06-21T10:30:00Z",
                "is_read": False,
                "has_attachments": True,
            },
            {
                "subject": "您的快递已送达",
                "from": "快递通知 <noreply@express.com>",
                "received": "2026-06-21T09:00:00Z",
                "is_read": True,
                "has_attachments": False,
            },
        ]
        print(format_email_list(sample))
        print()
        detail = {
            "subject": "关于下周会议的安排",
            "from": "老板 <boss@company.com>",
            "to": "我 <me@company.com>",
            "received": "2026-06-21T10:30:00Z",
            "body_text": "请准备下周一的项目进度汇报材料，包括已完成内容和后续计划。",
            "attachments": [{"filename": "会议议程.docx"}],
        }
        print(format_email_detail(detail))


if __name__ == "__main__":
    main()
