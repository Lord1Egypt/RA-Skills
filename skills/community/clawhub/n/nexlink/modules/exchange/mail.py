#!/usr/bin/env python3
"""
Email operations for Exchange.
Commands: read, get, send, draft, reply, forward, mark, download-attachment.
"""

import argparse
import os
import sys
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connection import get_account
from utils import out, die, parse_recipients, add_json_argument, confirm_or_die, add_yes_argument
from logger import get_logger

_logger = get_logger()


def email_to_dict(item, preview_len: int = 150, folder_name: str = "") -> dict:
    """Serialize an exchangelib Message to a plain dict."""
    sender = ""
    if item.sender:
        sender = item.sender.email_address or ""
        if item.sender.name:
            sender = f"{item.sender.name} <{sender}>"

    to_list = []
    if item.to_recipients:
        for r in item.to_recipients:
            to_list.append(r.email_address or "")

    cc_list = []
    if item.cc_recipients:
        for r in item.cc_recipients:
            cc_list.append(r.email_address or "")

    preview = ""
    if item.text_body:
        preview = item.text_body.strip().replace("\n", " ")[:preview_len]

    attachments = []
    if item.attachments:
        for att in item.attachments:
            if hasattr(att, "name"):
                attachments.append(
                    {
                        "name": att.name,
                        "size": getattr(att, "size", None),
                        "content_id": getattr(att, "content_id", None),
                    }
                )

    return {
        "id": item.id,
        "subject": item.subject or "(no subject)",
        "from": sender,
        "to": to_list,
        "cc": cc_list,
        "date": str(item.datetime_received) if item.datetime_received else None,
        "is_read": item.is_read,
        "preview": preview,
        "has_attachments": len(attachments) > 0,
        "attachments": attachments,
        "folder": folder_name,
    }


def get_folder(account, folder_name: str):
    """Get folder by name (case-insensitive)."""
    folder_name = folder_name.lower()

    # Standard folders
    folder_map = {
        "inbox": account.inbox,
        "drafts": account.drafts,
        "sent": account.sent,
        "sentitems": account.sent,
        "deleted": account.trash,
        "deleteditems": account.trash,
        "trash": account.trash,
        "junk": account.junk,
        "spam": account.junk,
        "outbox": account.outbox,
    }

    if folder_name in folder_map:
        return folder_map[folder_name]

    # Try to find custom folder
    try:
        for folder in account.root.walk():
            if folder.name and folder.name.lower() == folder_name:
                return folder
    except Exception:
        pass

    # Default to inbox
    return account.inbox


# ── Commands ────────────────────────────────────────────────────────────────


def cmd_connect(_args):
    """Test connection and show mailbox stats."""
    account = get_account()
    out(
        {
            "ok": True,
            "email": str(account.primary_smtp_address),
            "server": os.environ.get("EXCHANGE_SERVER", ""),
            "inbox_total": account.inbox.total_count,
            "inbox_unread": account.inbox.unread_count,
            "calendar_count": account.calendar.total_count,
            "tasks_count": account.tasks.total_count,
            "contacts_count": account.contacts.total_count,
        }
    )


def cmd_read(args):
    """List emails from a folder."""
    account = get_account()
    folder = get_folder(account, args.folder)

    qs = folder.all().order_by("-datetime_received")

    if args.unread:
        qs = qs.filter(is_read=False)
    if args.frm:
        qs = qs.filter(sender__email_address=args.frm)
    if args.subject:
        qs = qs.filter(subject__contains=args.subject)

    qs = qs[: args.limit]

    emails = [email_to_dict(item, folder_name=args.folder) for item in qs]
    out({"ok": True, "count": len(emails), "emails": emails})


def cmd_get(args):
    """Get full email details including body."""
    account = get_account()

    try:
        # Search inbox first (most common)
        try:
            item = account.inbox.get(id=args.id)
        except Exception:
            # Search sent items (second most common)
            try:
                item = account.sent.get(id=args.id)
            except Exception:
                # Fallback: search all folders (slow)
                items = list(account.root.walk().get_items([args.id]))
                if not items:
                    die(f"Email not found: {args.id}")
                item = items[0]
    except Exception as e:
        die(f"Email not found: {e}")

    # Get body
    body = ""
    if item.text_body:
        body = item.text_body
    elif item.body:
        body = str(item.body)

    # Get attachments info
    attachments = []
    if item.attachments:
        for att in item.attachments:
            attachments.append(
                {
                    "name": getattr(att, "name", "unknown"),
                    "size": getattr(att, "size", None),
                    "content_type": getattr(att, "content_type", None),
                }
            )

    out(
        {
            "ok": True,
            "email": {
                "id": item.id,
                "subject": item.subject or "(no subject)",
                "from": item.sender.email_address if item.sender else "",
                "from_name": (
                    item.sender.name
                    if item.sender and hasattr(item.sender, "name")
                    else None
                ),
                "to": (
                    [r.email_address for r in item.to_recipients]
                    if item.to_recipients
                    else []
                ),
                "cc": (
                    [r.email_address for r in item.cc_recipients]
                    if item.cc_recipients
                    else []
                ),
                "date": str(item.datetime_received) if item.datetime_received else None,
                "body": body,
                "attachments": attachments,
            },
        }
    )


def cmd_send(args):
    """Send an email."""
    confirm_or_die(f"Send email to {args.to} with subject \"{args.subject}\"", getattr(args, 'yes', False))

    from exchangelib import Message, HTMLBody, FileAttachment

    account = get_account()

    # Prepare body
    body = HTMLBody(args.body) if args.html else args.body

    # Prepare message
    message = Message(
        account=account,
        subject=args.subject,
        body=body,
        to_recipients=parse_recipients(args.to),
        cc_recipients=parse_recipients(args.cc) if args.cc else None,
        bcc_recipients=parse_recipients(args.bcc) if args.bcc else None,
    )

    # Add attachments
    if args.attach:
        attach_paths = [p.strip() for p in args.attach.split(",")]
        for path in attach_paths:
            p = Path(path)
            if not p.exists():
                die(f"Attachment not found: {path}")
            with open(p, "rb") as f:
                content = f.read()
            message.attach(FileAttachment(name=p.name, content=content))

    message.send()
    out({"ok": True, "message": "Email sent"})


def cmd_draft(args):
    """Create a draft email."""
    from pathlib import Path

    account = get_account()

    body = HTMLBody(args.body) if args.html else args.body

    message = Message(
        account=account,
        folder=account.drafts,
        subject=args.subject,
        body=body,
        to_recipients=parse_recipients(args.to) if args.to else None,
        cc_recipients=parse_recipients(args.cc) if args.cc else None,
    )

    # Add attachments
    if args.attach:
        attach_paths = [p.strip() for p in args.attach.split(",")]
        for path in attach_paths:
            p = Path(path)
            if not p.exists():
                die(f"Attachment not found: {path}")
            with open(p, "rb") as f:
                content = f.read()
            message.attach(FileAttachment(name=p.name, content=content))

    message.save()
    out({"ok": True, "message": "Draft saved", "id": message.id})


def cmd_reply(args):
    """Reply to an email."""
    confirm_or_die(f"Reply to email {args.id}", getattr(args, 'yes', False))

    account = get_account()

    try:
        item = account.inbox.get(id=args.id)
    except Exception as e:
        die(f"Email not found: {e}")

    if args.all:
        reply = item.create_reply_all(subject=f"RE: {item.subject}", body=args.body)
    else:
        reply = item.create_reply(subject=f"RE: {item.subject}", body=args.body)

    reply.send()
    out({"ok": True, "message": "Reply sent"})


def cmd_forward(args):
    """Forward an email."""
    confirm_or_die(f"Forward email {args.id} to {args.to}", getattr(args, 'yes', False))

    account = get_account()

    try:
        item = account.inbox.get(id=args.id)
    except Exception as e:
        die(f"Email not found: {e}")

    fwd = item.create_forward(
        subject=f"FW: {item.subject}",
        body=args.body or "",
        to_recipients=parse_recipients(args.to),
    )
    fwd.send()
    out({"ok": True, "message": "Email forwarded"})


def cmd_mark(args):
    """Mark email as read or unread."""
    account = get_account()

    try:
        item = account.inbox.get(id=args.id)
    except Exception as e:
        die(f"Email not found: {e}")

    if args.read:
        item.is_read = True
    elif args.unread:
        item.is_read = False
    else:
        die("Specify --read or --unread")

    item.save(update_fields=["is_read"])
    state = "read" if item.is_read else "unread"
    out({"ok": True, "message": f"Marked as {state}"})


def cmd_mark_all_read(args):
    """Mark all unread emails as read (skips calendar items)."""
    from exchangelib.items import Message

    account = get_account()
    folder = get_folder(account, getattr(args, 'folder', 'inbox'))

    # Get all unread items
    unread = list(folder.filter(is_read=False))
    _logger.info(f"Found {len(unread)} unread items")

    marked = 0
    skipped = 0
    errors = []

    # Prepare Message objects for bulk update
    message_items = []
    for item in unread:
        # Skip non-Message items (calendar, etc.)
        if not isinstance(item, Message):
            skipped += 1
            _logger.debug(f"Skipping non-message: {item.subject[:50]}")
            continue
        
        item.is_read = True
        message_items.append(item)
    
    # Bulk update all messages at once
    if message_items:
        try:
            updated_count = account.bulk_update(message_items, update_fields=["is_read"])
            marked = updated_count
            _logger.info(f"Bulk updated {marked} messages as read")
        except Exception as e:
            # Fallback to individual saves on bulk failure
            _logger.warning(f"Bulk update failed: {e}, falling back to individual saves")
            for item in message_items:
                try:
                    item.is_read = True
                    item.save(update_fields=["is_read"])
                    marked += 1
                    _logger.debug(f"Marked: {item.subject[:50]}")
                except Exception as e2:
                    errors.append(f"{item.subject[:30]}: {str(e2)[:50]}")
                    _logger.warning(f"Error marking {item.subject[:30]}: {e2}")

    out({
        "ok": True,
        "marked": marked,
        "skipped": skipped,
        "errors": errors,
        "total_unread": len(unread)
    })


def cmd_download_attachment(args):
    """Download an attachment from an email."""

    account = get_account()

    try:
        # Get the email
        item = account.inbox.get(id=args.id)
    except Exception as e:
        die(f"Email not found: {e}")

    if not item.attachments:
        die("Email has no attachments")

    # Find the attachment by name or index
    attachment = None
    if args.name:
        for att in item.attachments:
            if getattr(att, "name", "") == args.name:
                attachment = att
                break
        if not attachment:
            names = [getattr(a, "name", "?") for a in item.attachments]
            die(f"Attachment '{args.name}' not found. Available: {', '.join(names)}")
    elif args.index is not None:
        try:
            attachment = item.attachments[args.index]
        except IndexError:
            die(
                f"Attachment index {args.index} out of range (0-{len(item.attachments)-1})"
            )
    else:
        # Default to first attachment
        attachment = item.attachments[0]

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(attachment.name)

    # Download
    try:
        content = attachment.content
        with open(output_path, "wb") as f:
            f.write(content)
        out(
            {
                "ok": True,
                "message": "Attachment downloaded",
                "name": attachment.name,
                "size": len(content),
                "path": str(output_path),
            }
        )
    except Exception as e:
        die(f"Failed to download attachment: {e}")


def cmd_list_attachments(args):
    """List attachments in an email."""
    account = get_account()

    try:
        item = account.inbox.get(id=args.id)
    except Exception as e:
        die(f"Email not found: {e}")

    if not item.attachments:
        out({"ok": True, "count": 0, "attachments": []})
        return

    attachments = []
    for i, att in enumerate(item.attachments):
        attachments.append(
            {
                "index": i,
                "name": getattr(att, "name", "unknown"),
                "size": getattr(att, "size", None),
                "content_type": getattr(att, "content_type", None),
            }
        )

    out({"ok": True, "count": len(attachments), "attachments": attachments})


# ── CLI ───────────────────────────────────────────────────────────────────────


def main():
    add_json_argument(parser)
    parser = argparse.ArgumentParser(
        prog="mail.py",
        description="Exchange email operations",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # connect
    sub.add_parser("connect", help="Test connection")

    # read
    p_read = sub.add_parser("read", help="List emails")
    p_read.add_argument("--folder", "-f", default="inbox")
    p_read.add_argument("--limit", "-n", type=int, default=10)
    p_read.add_argument("--unread", "-u", action="store_true")
    p_read.add_argument("--from", dest="frm", metavar="ADDR")
    p_read.add_argument("--subject", "-s", metavar="TEXT")

    # get
    p_get = sub.add_parser("get", help="Get full email")
    p_get.add_argument("--id", required=True)

    # send
    p_send = sub.add_parser("send", help="Send email")
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--body", required=True)
    p_send.add_argument("--cc")
    p_send.add_argument("--bcc")
    p_send.add_argument("--html", action="store_true")
    p_send.add_argument("--attach", metavar="FILE1,FILE2")

    # draft
    p_draft = sub.add_parser("draft", help="Create draft")
    p_draft.add_argument("--subject", required=True)
    p_draft.add_argument("--body", required=True)
    p_draft.add_argument("--to")
    p_draft.add_argument("--cc")
    p_draft.add_argument("--html", action="store_true")
    p_draft.add_argument("--attach", metavar="FILE1,FILE2")

    # reply
    p_reply = sub.add_parser("reply", help="Reply to email")
    p_reply.add_argument("--id", required=True)
    p_reply.add_argument("--body", required=True)
    p_reply.add_argument("--all", action="store_true")

    # forward
    p_fwd = sub.add_parser("forward", help="Forward email")
    p_fwd.add_argument("--id", required=True)
    p_fwd.add_argument("--to", required=True)
    p_fwd.add_argument("--body", default="")

    # mark
    p_mark = sub.add_parser("mark", help="Mark read/unread")
    p_mark.add_argument("--id", required=True)
    grp = p_mark.add_mutually_exclusive_group(required=True)
    grp.add_argument("--read", action="store_true")
    grp.add_argument("--unread", action="store_true")

    # list-attachments
    p_latt = sub.add_parser("list-attachments", help="List email attachments")
    p_latt.add_argument("--id", required=True)

    # download-attachment
    p_datt = sub.add_parser("download-attachment", help="Download attachment")
    p_datt.add_argument("--id", required=True)
    p_datt.add_argument("--name", metavar="FILENAME")
    p_datt.add_argument("--index", type=int)
    p_datt.add_argument("--output", "-o")

    args = parser.parse_args()

    dispatch = {
        "connect": cmd_connect,
        "read": cmd_read,
        "get": cmd_get,
        "send": cmd_send,
        "draft": cmd_draft,
        "reply": cmd_reply,
        "forward": cmd_forward,
        "mark": cmd_mark,
        "list-attachments": cmd_list_attachments,
        "download-attachment": cmd_download_attachment,
    }

    try:
        dispatch[args.cmd](args)
    except SystemExit:
        raise
    except Exception as e:
        die(str(e))


def add_parser(subparsers):
    """Add mail commands to CLI parser."""
    # connect
    p_connect = subparsers.add_parser("connect", help="Test mail connection")
    p_connect.set_defaults(func=cmd_connect)
    add_json_argument(p_connect)

    # read
    p_read = subparsers.add_parser("read", help="List emails")
    p_read.add_argument("--folder", "-f", default="inbox", help="Folder name")
    p_read.add_argument("--limit", "-n", type=int, default=10, help="Max emails")
    p_read.add_argument("--unread", "-u", action="store_true", help="Unread only")
    p_read.add_argument("--from", dest="frm", metavar="ADDR", help="Filter by sender")
    p_read.add_argument("--subject", "-s", metavar="TEXT", help="Filter by subject")
    p_read.set_defaults(func=cmd_read)
    add_json_argument(p_read)

    # get
    p_get = subparsers.add_parser("get", help="Get email details")
    p_get.add_argument("--id", "-i", required=True, help="Email ID")
    p_get.set_defaults(func=cmd_get)
    add_json_argument(p_get)

    # send
    p_send = subparsers.add_parser("send", help="Send email")
    p_send.add_argument("--to", "-t", required=True, help="Recipient(s)")
    p_send.add_argument("--subject", "-s", required=True, help="Subject")
    p_send.add_argument("--body", "-b", required=True, help="Body text")
    p_send.add_argument("--cc", "-c", help="CC recipients")
    p_send.add_argument("--bcc", help="BCC recipients")
    p_send.add_argument("--html", action="store_true", help="HTML body")
    p_send.add_argument(
        "--attach", "-a", metavar="FILE", help="Attachments (comma-separated)"
    )
    p_send.set_defaults(func=cmd_send)
    add_json_argument(p_send)
    add_yes_argument(p_send)

    # draft
    p_draft = subparsers.add_parser("draft", help="Create draft")
    p_draft.add_argument("--subject", "-s", required=True, help="Subject")
    p_draft.add_argument("--body", "-b", required=True, help="Body text")
    p_draft.add_argument("--to", "-t", help="Recipient(s)")
    p_draft.add_argument("--cc", "-c", help="CC recipients")
    p_draft.add_argument("--html", action="store_true", help="HTML body")
    p_draft.add_argument(
        "--attach", "-a", metavar="FILE", help="Attachments (comma-separated)"
    )
    p_draft.set_defaults(func=cmd_draft)
    add_json_argument(p_draft)

    # reply
    p_reply = subparsers.add_parser("reply", help="Reply to email")
    p_reply.add_argument("--id", "-i", required=True, help="Email ID")
    p_reply.add_argument("--body", "-b", required=True, help="Reply text")
    p_reply.add_argument(
        "--all", "-a", action="store_true", dest="reply_all", help="Reply to all"
    )
    p_reply.set_defaults(func=cmd_reply)
    add_json_argument(p_reply)
    add_yes_argument(p_reply)

    # forward
    p_fwd = subparsers.add_parser("forward", help="Forward email")
    p_fwd.add_argument("--id", "-i", required=True, help="Email ID")
    p_fwd.add_argument("--to", "-t", required=True, help="Recipient(s)")
    p_fwd.add_argument("--body", "-b", default="", help="Forward message")
    p_fwd.set_defaults(func=cmd_forward)
    add_json_argument(p_fwd)
    add_yes_argument(p_fwd)

    # mark
    p_mark = subparsers.add_parser("mark", help="Mark email read/unread")
    p_mark.add_argument("--id", "-i", required=True, help="Email ID")
    grp = p_mark.add_mutually_exclusive_group(required=True)
    grp.add_argument("--read", action="store_true", help="Mark as read")
    grp.add_argument("--unread", action="store_true", help="Mark as unread")
    p_mark.set_defaults(func=cmd_mark)
    add_json_argument(p_mark)

    # mark-all-read
    p_markall = subparsers.add_parser("mark-all-read", help="Mark all unread emails as read")
    p_markall.add_argument("--folder", "-f", default="inbox", help="Folder (default: inbox)")
    p_markall.set_defaults(func=cmd_mark_all_read)
    add_json_argument(p_markall)

    # list-attachments
    p_latt = subparsers.add_parser("list-attachments", help="List attachments")
    p_latt.add_argument("--id", "-i", required=True, help="Email ID")
    p_latt.set_defaults(func=cmd_list_attachments)
    add_json_argument(p_latt)

    # download-attachment
    p_datt = subparsers.add_parser("download-attachment", help="Download attachment")
    p_datt.add_argument("--id", "-i", required=True, help="Email ID")
    p_datt.add_argument("--name", "-n", metavar="FILENAME", help="Attachment filename")
    p_datt.add_argument("--index", type=int, help="Attachment index")
    p_datt.add_argument("--output", "-o", help="Output path")
    p_datt.set_defaults(func=cmd_download_attachment)
    add_json_argument(p_datt)


if __name__ == "__main__":
    main()
