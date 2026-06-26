#!/usr/bin/env python3
"""
Microsoft Graph mail operations for OpenClaw msgraph skill.

Usage:
  python mail.py inbox [--count N] [--folder FOLDER]
  python mail.py read <message_id>
  python mail.py move <message_id> <folder_name_or_id>
  python mail.py folders
  python mail.py search <query>
"""

import sys
from pathlib import Path

# Add skill root to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

import auth
import graph_api
import utils


# ── Folder resolution ──────────────────────────────────────────────────────────

# Well-known folder names accepted by Graph API directly
WELL_KNOWN = {
    "inbox", "drafts", "sentitems", "deleteditems", "junk",
    "archive", "outbox", "junkemail", "recoverableitemsdeletions",
}


def resolve_folder_id(name_or_id, parent_id=None):
    """
    Recursively search for a folder by display name or ID.
    Well-known names (inbox, drafts, etc.) are returned as-is.
    """
    lower = name_or_id.lower().replace(" ", "")
    if lower in WELL_KNOWN:
        return lower

    # Try direct ID (long string)
    if len(name_or_id) > 50:
        return name_or_id

    return _find_folder_recursive(name_or_id)


def _find_folder_recursive(name, parent_id=None):
    """Search folders and their children for a matching display name."""
    if parent_id:
        path = f"/me/mailFolders/{parent_id}/childFolders"
    else:
        path = "/me/mailFolders"

    params = {
        "$top": "100",
        "$select": "id,displayName",
    }
    result = graph_api.graph_get(path, params)
    folders = result.get("value", [])

    for f in folders:
        if f["displayName"].lower() == name.lower():
            return f["id"]

    # Not found at this level — recurse into children
    for f in folders:
        found = _find_folder_recursive(name, f["id"])
        if found:
            return found

    # Only raise error at top level
    if parent_id is None:
        print(f"ERROR: Folder '{name}' not found.", file=sys.stderr)
        print("Run: python mail.py folders   to see available folders.", file=sys.stderr)
        sys.exit(1)

    return None


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_inbox(args):
    count = 20
    folder = "inbox"
    i = 0
    while i < len(args):
        if args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1]); i += 2
        elif args[i] == "--folder" and i + 1 < len(args):
            folder = args[i + 1]; i += 2
        else:
            i += 1

    folder_id = resolve_folder_id(folder)
    params = {
        "$top": str(count),
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,isRead,bodyPreview,hasAttachments",
    }
    result = graph_api.graph_get(f"/me/mailFolders/{folder_id}/messages", params)
    messages = result.get("value", [])

    if not messages:
        print("No messages found.")
        return

    print(f"\n{'─'*80}")
    print(f"  {folder.upper()} — {len(messages)} messages")
    print(f"{'─'*80}\n")
    for msg in messages:
        sender = msg.get("from", {}).get("emailAddress", {})
        read_flag = " " if msg.get("isRead") else "●"
        attach_flag = "📎" if msg.get("hasAttachments") else "  "
        print(f"{read_flag} {attach_flag} [{msg['id']}]")
        print(f"   From:    {sender.get('name', '')} <{sender.get('address', '')}>")
        print(f"   Subject: {msg.get('subject', '(no subject)')}")
        print(f"   Date:    {utils.format_datetime(msg.get('receivedDateTime', ''))}")
        preview = msg.get("bodyPreview", "").replace("\n", " ").strip()
        if preview:
            print(f"   Preview: {preview[:120]}")
        print()


def cmd_read(args):
    if not args:
        print("Usage: python mail.py read <message_id>")
        sys.exit(1)
    msg_id = args[0]
    params = {"$select": "id,subject,from,toRecipients,receivedDateTime,body,hasAttachments,isRead"}
    msg = graph_api.graph_get(f"/me/messages/{msg_id}", params)

    # Mark as read
    graph_api.graph_patch(f"/me/messages/{msg_id}", {"isRead": True})

    sender = msg.get("from", {}).get("emailAddress", {})
    to_list = [r["emailAddress"]["address"] for r in msg.get("toRecipients", [])]
    body_type = msg.get("body", {}).get("contentType", "")
    body = msg.get("body", {}).get("content", "")

    print(f"\nSubject:  {msg.get('subject', '(no subject)')}")
    print(f"From:     {sender.get('name', '')} <{sender.get('address', '')}>")
    print(f"To:       {', '.join(to_list)}")
    print(f"Date:     {utils.format_datetime(msg.get('receivedDateTime', ''))}")
    print(f"ID:       {msg.get('id', '')}")
    print(f"{'─'*80}")
    if body_type == "html":
        body = utils.strip_html(body)
    print(body)


def cmd_move(args):
    if len(args) < 2:
        print("Usage: python mail.py move <message_id> <folder_name_or_id>")
        sys.exit(1)
    msg_id, folder = args[0], args[1]
    folder_id = resolve_folder_id(folder)
    result = graph_api.graph_post(f"/me/messages/{msg_id}/move", {"destinationId": folder_id})
    print(f"✓ Message moved to '{folder}' (new ID: {result.get('id', '?')[:32]}...)")


def get_folders_recursive(parent_id=None, indent=0):
    if parent_id:
        path = f"/me/mailFolders/{parent_id}/childFolders"
    else:
        path = "/me/mailFolders"
    params = {
        "$top": "100",
        "$select": "id,displayName,totalItemCount,unreadItemCount",
    }
    result = graph_api.graph_get(path, params)
    folders = result.get("value", [])
    for f in folders:
        unread = f.get("unreadItemCount", 0)
        total = f.get("totalItemCount", 0)
        unread_str = f" [{unread} unread]" if unread else ""
        prefix = "  " * indent
        print(f"{prefix}  {f['displayName']:<30} {total:>6} items{unread_str}")
        print(f"{prefix}  ID: {f['id']}")
        print()
        # Recurse into children
        get_folders_recursive(f["id"], indent + 1)

def cmd_folders(args):
    print(f"\n{'─'*70}")
    print(f"  MAIL FOLDERS")
    print(f"{'─'*70}\n")
    get_folders_recursive()


def cmd_search(args):
    if not args:
        print("Usage: python mail.py search <query>")
        sys.exit(1)
    query = " ".join(args)
    params = {
        "$search": f'"{query}"',
        "$top": "20",
        "$select": "id,subject,from,receivedDateTime,isRead,bodyPreview",
    }
    result = graph_api.graph_get("/me/messages", params)
    messages = result.get("value", [])
    if not messages:
        print(f"No results for: {query}")
        return
    print(f"\nSearch results for '{query}' ({len(messages)} found):\n")
    for msg in messages:
        sender = msg.get("from", {}).get("emailAddress", {})
        read_flag = " " if msg.get("isRead") else "●"
        print(f"{read_flag} [{msg['id'][:24]}...]")
        print(f"   From:    {sender.get('name', '')} <{sender.get('address', '')}>")
        print(f"   Subject: {msg.get('subject', '(no subject)')}")
        print(f"   Date:    {msg.get('receivedDateTime', '')}")
        print()


# ── Entry point ───────────────────────────────────────────────────────────────

COMMANDS = {
    "inbox": cmd_inbox,
    "read": cmd_read,
    "move": cmd_move,
    "folders": cmd_folders,
    "search": cmd_search,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Usage: python mail.py <command> [args]")
        print("Commands:", ", ".join(COMMANDS.keys()))
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])
