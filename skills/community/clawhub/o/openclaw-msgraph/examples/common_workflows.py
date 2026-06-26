#!/usr/bin/env python3
"""
Common OpenClaw Microsoft Graph Skill workflows.

These examples show typical patterns for using the msgraph skill
in OpenClaw agents and assistants.
"""

import sys
import json
from pathlib import Path

# Add scripts to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import auth
import mail
import cal
import graph_api


# ── Example 1: Daily Standup (Email + Calendar) ────────────────────────────

def daily_standup():
    """
    Daily standup routine: check inbox, upcoming events, and summarize.
    
    This is a typical LLM workflow:
    1. Verify auth status
    2. Get inbox summary
    3. Get today's calendar
    4. Combine for context/summary
    """
    print("=== Daily Standup ===\n")
    
    # Check auth
    if not auth.load_tokens():
        print("❌ Not authenticated. Run: python scripts/auth.py login")
        return
    
    print("✓ Authenticated\n")
    
    # Get recent emails
    print("📧 Recent emails:")
    try:
        path = "/me/mailFolders/inbox/messages"
        params = {
            "$select": "id,subject,from,receivedDateTime",
            "$top": "5",
            "$orderby": "receivedDateTime desc"
        }
        result = graph_api.graph_get(path, params)
        for msg in result.get("value", []):
            sender = msg.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = msg.get("subject", "(no subject)")
            print(f"  • {sender}: {subject}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()
    
    # Get today's events
    print("📅 Today's events:")
    try:
        path = "/me/calendarview"
        # For real usage, use proper date range
        params = {
            "$select": "subject,start,end,organizer",
            "$orderby": "start/dateTime",
            "$top": "10"
        }
        result = graph_api.graph_get(path, params)
        for event in result.get("value", []):
            subject = event.get("subject", "(no title)")
            start = event.get("start", {}).get("dateTime", "")
            print(f"  • {start[:16]}: {subject}")
    except Exception as e:
        print(f"  Error: {e}")


# ── Example 2: Email Summary with HTML Stripping ────────────────────────────

def email_summary(message_id):
    """
    Get a message and extract clean text content.
    
    Usage: email_summary("<message-id>")
    """
    print(f"📧 Reading message: {message_id}\n")
    
    try:
        # Fetch message
        path = f"/me/messages/{message_id}"
        params = {"$select": "subject,from,body,receivedDateTime"}
        msg = graph_api.graph_get(path, params)
        
        # Display summary
        print(f"From: {msg.get('from', {}).get('emailAddress', {}).get('name', 'Unknown')}")
        print(f"Subject: {msg.get('subject', '(no subject)')}")
        print(f"Date: {msg.get('receivedDateTime', 'Unknown')}")
        print()
        
        # Strip HTML and display content
        from utils import strip_html
        body_content = msg.get("body", {}).get("content", "")
        clean_content = strip_html(body_content)
        print("Content:")
        print(clean_content[:500] + ("..." if len(clean_content) > 500 else ""))
        
    except Exception as e:
        print(f"Error: {e}")


# ── Example 3: Folder Organization ────────────────────────────────────────

def organize_inbox():
    """
    Example: Move messages matching criteria to folders.
    
    Real workflow would:
    1. List inbox messages
    2. Check subject/sender against rules
    3. Resolve folder by name
    4. Move message to folder
    """
    print("📁 Folder organization workflow\n")
    
    try:
        # List folders to show available destinations
        path = "/me/mailFolders"
        params = {"$select": "id,displayName,childFolderCount"}
        folders = graph_api.graph_get(path, params)
        
        print("Available folders:")
        for folder in folders.get("value", []):
            name = folder.get("displayName", "Unknown")
            print(f"  • {name}")
        
        print()
        print("Example: Move receipts to 'Receipts' folder")
        print("  1. Search for messages from receipt-related senders")
        print("  2. Use mail.resolve_folder_id('Receipts') to get folder ID")
        print("  3. Use graph_post() with /move endpoint")
        
    except Exception as e:
        print(f"Error: {e}")


# ── Example 4: Create Calendar Event ───────────────────────────────────────

def create_meeting(subject, attendees, start_time, end_time):
    """
    Create a calendar event with attendees.
    
    Usage: create_meeting(
        "Team Sync",
        ["alice@example.com", "bob@example.com"],
        "2026-03-10T14:00",
        "2026-03-10T15:00"
    )
    """
    print(f"📅 Creating event: {subject}\n")
    
    try:
        from utils import parse_local_datetime
        
        # Parse times
        start_dt = parse_local_datetime(start_time)
        end_dt = parse_local_datetime(end_time)
        
        # Build attendees list
        attendee_list = [
            {
                "emailAddress": {"address": addr, "name": addr.split("@")[0]},
                "type": "required"
            }
            for addr in attendees
        ]
        
        # Create event
        payload = {
            "subject": subject,
            "start": {"dateTime": start_dt.isoformat(), "timeZone": "America/New_York"},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": "America/New_York"},
            "attendees": attendee_list
        }
        
        path = "/me/events"
        result = graph_api.graph_post(path, payload)
        
        print(f"✓ Event created!")
        print(f"  ID: {result.get('id')}")
        print(f"  Link: {result.get('webLink', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")


# ── Example 5: Search and Filter ───────────────────────────────────────────

def search_recent_emails(query, days=7):
    """
    Search for recent emails from specific senders or with keywords.
    
    Usage: search_recent_emails("from:alice@example.com", days=7)
    """
    print(f"🔍 Searching: {query}\n")
    
    try:
        # Build OData filter (simplified—Graph API uses KQL for complex searches)
        params = {
            "$search": f'"{query}"',
            "$select": "subject,from,receivedDateTime",
            "$top": "20",
            "$orderby": "receivedDateTime desc"
        }
        
        path = "/me/messages"
        result = graph_api.graph_get(path, params)
        
        matches = result.get("value", [])
        print(f"Found {len(matches)} messages:\n")
        
        for msg in matches:
            from_name = msg.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = msg.get("subject", "(no subject)")
            date = msg.get("receivedDateTime", "")[:10]
            print(f"  [{date}] {from_name}: {subject}")
        
    except Exception as e:
        print(f"Error: {e}")


# ── Example 6: Unread Email Count ──────────────────────────────────────────

def unread_summary():
    """
    Quick summary of unread counts by folder.
    Useful for "check my email" type commands.
    """
    print("📨 Unread Summary\n")
    
    try:
        path = "/me/mailFolders"
        params = {"$select": "displayName,unreadItemCount"}
        folders = graph_api.graph_get(path, params)
        
        total_unread = 0
        for folder in folders.get("value", []):
            name = folder.get("displayName", "Unknown")
            unread = folder.get("unreadItemCount", 0)
            if unread > 0:
                print(f"  {name}: {unread} unread")
                total_unread += unread
        
        print(f"\nTotal unread: {total_unread}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw msgraph skill examples")
    parser.add_argument("--example", choices=[
        "standup", "summary", "organize", "create", "search", "unread"
    ], help="Which example to run")
    
    args = parser.parse_args()
    
    if args.example == "standup":
        daily_standup()
    elif args.example == "summary":
        # Would need to pass message_id
        print("Usage: python examples.py --example summary")
        print("Then edit the script to add a message ID")
    elif args.example == "organize":
        organize_inbox()
    elif args.example == "create":
        create_meeting(
            "Demo Meeting",
            ["demo@example.com"],
            "2026-03-10T14:00",
            "2026-03-10T15:00"
        )
    elif args.example == "search":
        search_recent_emails("test", days=7)
    elif args.example == "unread":
        unread_summary()
    else:
        print("Examples:")
        print("  python examples.py --example standup     # Daily standup")
        print("  python examples.py --example organize    # Folder organization")
        print("  python examples.py --example search      # Search emails")
        print("  python examples.py --example unread      # Unread summary")
        print("\nOr import and use functions directly in your code:")
        print("  from examples import daily_standup, search_recent_emails")
