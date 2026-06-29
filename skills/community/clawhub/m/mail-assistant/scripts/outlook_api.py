#!/usr/bin/env python3
"""
Microsoft Graph API wrapper for Outlook / Microsoft 365 accounts.

Requires a configured account (.json) and stored OAuth token (.token.json),
both managed by oauth_manager.py.

Usage:
    python outlook_api.py <account-id> list-inbox [--limit N] [--unread] [--folder <folder>]
    python outlook_api.py <account-id> read-mail <message-id>
    python outlook_api.py <account-id> send <json-file> [--confirm]
    python outlook_api.py <account-id> mark-read <message-id>
    python outlook_api.py <account-id> mark-unread <message-id>
    python outlook_api.py <account-id> search <query> [--limit N]
    python outlook_api.py <account-id> list-folders
"""

import json
import os
import sys
import urllib.request
import urllib.error

# Force UTF-8 for console output (handle Unicode in email subjects/bodies)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_dir import ACCOUNTS_DIR, confirm_action
# ⚠️ SECURITY: Use direct import instead of subprocess to avoid command injection risks
import oauth_manager as _oauth_mgr

GRAPH_API = "https://graph.microsoft.com/v1.0"


# ── Helpers ────────────────────────────────────────────────────────────────


def _get_token(account_id):
    """Get access token via direct import (no subprocess)."""
    token_str = _oauth_mgr.get_access_token(account_id)
    if token_str is None:
        print(f"[ERROR] Failed to get token for {account_id}.", file=sys.stderr)
        sys.exit(1)
    return token_str


def _graph_get(token, path, params=None):
    """GET request to Graph API."""
    url = f"{GRAPH_API}{path}"
    if params:
        qs = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in params.items())
        url += f"?{qs}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[ERROR] Graph API {e.code}: {body}", file=sys.stderr)
        return None


def _graph_post(token, path, body, method="POST"):
    """POST/PATCH/DELETE request to Graph API."""
    url = f"{GRAPH_API}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[ERROR] Graph API {e.code}: {body}", file=sys.stderr)
        return None


def _format_mail_preview(msg):
    return {
        "id": msg.get("id"),
        "subject": msg.get("subject", "(no subject)"),
        "from": msg.get("from", {}).get("emailAddress", {}).get("address", "unknown"),
        "from_name": msg.get("from", {}).get("emailAddress", {}).get("name", ""),
        "received": msg.get("receivedDateTime", ""),
        "is_read": msg.get("isRead", False),
        "has_attachments": msg.get("hasAttachments", False),
        "importance": msg.get("importance", "normal"),
    }


# ── Commands ───────────────────────────────────────────────────────────────


def cmd_list_inbox(token, args):
    limit = 20
    folder = "inbox"
    unread_only = False
    i = 2
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif args[i] == "--unread":
            unread_only = True
            i += 1
        elif args[i] == "--folder" and i + 1 < len(args):
            folder = args[i + 1]
            i += 2
        else:
            i += 1

    path = f"/me/mailFolders/{folder}/messages"
    params = {
        "$top": limit,
        "$select": "id,subject,from,receivedDateTime,isRead,hasAttachments,importance",
        "$orderby": "receivedDateTime DESC",
    }
    if unread_only:
        params["$filter"] = "isRead eq false"

    data = _graph_get(token, path, params)
    if not data:
        return

    mails = [_format_mail_preview(m) for m in data.get("value", [])]
    print(json.dumps(mails, indent=2, ensure_ascii=False))


def cmd_read_mail(token, args):
    if len(args) < 3:
        print("[ERROR] Usage: outlook_api.py <account-id> read-mail <message-id>", file=sys.stderr)
        sys.exit(1)
    msg_id = args[2]
    path = f"/me/messages/{urllib.request.quote(msg_id, safe='')}"
    params = {
        "$select": "id,subject,from,toRecipients,ccRecipients,receivedDateTime,isRead,body,hasAttachments,attachments"
    }
    data = _graph_get(token, path, params)
    if data:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_send(token, args):
    if len(args) < 3:
        print("[ERROR] Usage: outlook_api.py <account-id> send <json-file> [--yes]", file=sys.stderr)
        sys.exit(1)
    json_path = args[2]

    if not os.path.exists(json_path):
        print(f"[ERROR] File not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        email_data = json.load(f)

    # Show a dry-run preview first
    print("[DRY-RUN] 即将发送邮件:")
    print(json.dumps(email_data, indent=2, ensure_ascii=False))
    print()

    # ⚠️ CONSENT: Require user confirmation before sending
    to_list = email_data.get("to", [])
    subject = email_data.get("subject", "")
    desc = f"发送邮件至 {', '.join(to_list)}，主题: {subject}"
    if not confirm_action(desc, args):
        print("[CANCELLED] 用户取消操作。")
        sys.exit(1)

    # Build Graph API send mail payload
    message = {
        "subject": email_data.get("subject", ""),
        "toRecipients": [{"emailAddress": {"address": addr}} for addr in email_data.get("to", [])],
    }
    if email_data.get("cc"):
        message["ccRecipients"] = [{"emailAddress": {"address": addr}} for addr in email_data["cc"]]
    if email_data.get("bcc"):
        # BCC in Graph is hidden; include as singleRecipient
        message["bccRecipients"] = [{"emailAddress": {"address": addr}} for addr in email_data["bcc"]]
    if email_data.get("body_text"):
        message["body"] = {"contentType": "Text", "content": email_data["body_text"]}
    elif email_data.get("body_html"):
        message["body"] = {"contentType": "HTML", "content": email_data["body_html"]}

    payload = {"message": message, "saveToSentItems": True}

    # Handle attachments
    attachments = []
    for att_path in email_data.get("attachments", []):
        if os.path.exists(att_path):
            with open(att_path, "rb") as f:
                import base64
                content_bytes = f.read()
                attachments.append({
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": os.path.basename(att_path),
                    "contentBytes": base64.b64encode(content_bytes).decode("utf-8"),
                })

    if attachments:
        payload["message"]["attachments"] = attachments

    result = _graph_post(token, "/me/sendMail", payload)
    if result is not None:
        print("[OK] Email sent successfully.")
    else:
        print("[ERROR] Failed to send email.", file=sys.stderr)
        sys.exit(1)


def cmd_mark_read(token, args):
    if len(args) < 3:
        print("[ERROR] Usage: outlook_api.py <account-id> mark-read <message-id> [--yes]", file=sys.stderr)
        sys.exit(1)
    msg_id = args[2]
    # ⚠️ CONSENT: Require user confirmation before modifying mailbox state
    desc = f"将邮件 {msg_id[:20]}... 标记为已读"
    if not confirm_action(desc, args):
        print("[CANCELLED] 用户取消操作。")
        return
    print(f"[INFO] Marking message {msg_id} as read...", file=sys.stderr)
    path = f"/me/messages/{urllib.request.quote(msg_id, safe='')}"
    result = _graph_post(token, path, {"isRead": True}, method="PATCH")
    if result is not None:
        print("[OK] Marked as read.")


def cmd_mark_unread(token, args):
    if len(args) < 3:
        print("[ERROR] Usage: outlook_api.py <account-id> mark-unread <message-id> [--yes]", file=sys.stderr)
        sys.exit(1)
    msg_id = args[2]
    # ⚠️ CONSENT: Require user confirmation before modifying mailbox state
    desc = f"将邮件 {msg_id[:20]}... 标记为未读"
    if not confirm_action(desc, args):
        print("[CANCELLED] 用户取消操作。")
        return
    print(f"[INFO] Marking message {msg_id} as unread...", file=sys.stderr)
    path = f"/me/messages/{urllib.request.quote(msg_id, safe='')}"
    result = _graph_post(token, path, {"isRead": False}, method="PATCH")
    if result is not None:
        print("[OK] Marked as unread.")


def cmd_search(token, args):
    if len(args) < 3:
        print("[ERROR] Usage: outlook_api.py <account-id> search <query> [--limit N]", file=sys.stderr)
        sys.exit(1)
    query = args[2]
    limit = 20
    if "--limit" in args:
        idx = args.index("--limit")
        if idx + 1 < len(args):
            limit = int(args[idx + 1])

    path = "/me/messages"
    params = {
        "$top": limit,
        "$search": f'"{query}"',
        "$select": "id,subject,from,receivedDateTime,isRead,hasAttachments,importance",
    }
    data = _graph_get(token, path, params)
    if data:
        mails = [_format_mail_preview(m) for m in data.get("value", [])]
        print(json.dumps(mails, indent=2, ensure_ascii=False))


def cmd_list_folders(token, args):
    path = "/me/mailFolders"
    params = {"$select": "id,displayName,unreadItemCount,totalItemCount"}
    data = _graph_get(token, path, params)
    if data:
        folders = [
            {"id": f.get("id"), "name": f.get("displayName"),
             "unread": f.get("unreadItemCount", 0), "total": f.get("totalItemCount", 0)}
            for f in data.get("value", [])
        ]
        print(json.dumps(folders, indent=2, ensure_ascii=False))


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    account_id = sys.argv[1]
    action = sys.argv[2]
    args = sys.argv[3:]

    # Verify account exists
    account_path = os.path.join(ACCOUNTS_DIR, f"{account_id}.json")
    if not os.path.exists(account_path):
        print(f"[ERROR] Account not found: {account_id}", file=sys.stderr)
        print(f"  Config file expected at: {account_path}", file=sys.stderr)
        sys.exit(1)

    token = _get_token(account_id)

    actions = {
        "list-inbox": cmd_list_inbox,
        "read-mail": cmd_read_mail,
        "send": cmd_send,
        "mark-read": cmd_mark_read,
        "mark-unread": cmd_mark_unread,
        "search": cmd_search,
        "list-folders": cmd_list_folders,
    }

    if action not in actions:
        print(f"[ERROR] Unknown action: {action}", file=sys.stderr)
        print(f"  Available: {', '.join(actions.keys())}", file=sys.stderr)
        sys.exit(1)

    actions[action](token, args)



# ── Module-level convenience functions (for import use) ────────────────────


def list_inbox(account_id, limit=20, unread_only=False):
    """List inbox emails for the given account. Returns parsed JSON."""
    token = _get_token(account_id)
    args = []
    if limit != 20:
        args += ["--limit", str(limit)]
    if unread_only:
        args.append("--unread")
    cmd_list_inbox(token, args)


def read_mail(account_id, message_id):
    """Read a single email by message ID."""
    token = _get_token(account_id)
    cmd_read_mail(token, ["", "", message_id])


def mark_read(account_id, message_id):
    """Mark an email as read."""
    token = _get_token(account_id)
    cmd_mark_read(token, ["", "", message_id])


def mark_unread(account_id, message_id):
    """Mark an email as unread."""
    token = _get_token(account_id)
    cmd_mark_unread(token, ["", "", message_id])


def search(account_id, query, limit=20):
    """Search emails by keyword."""
    token = _get_token(account_id)
    cmd_search(token, ["", "", query, "--limit", str(limit)])


if __name__ == "__main__":
    main()
