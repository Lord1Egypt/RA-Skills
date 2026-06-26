#!/usr/bin/env python3
"""
Check AgentMail inbox for messages

Usage:
    # List recent messages
    python check_inbox.py --inbox "myagent@agentmail.to"
    
    # Get specific message
    python check_inbox.py --inbox "myagent@agentmail.to" --message "msg_123abc"
    
    # List threads
    python check_inbox.py --inbox "myagent@agentmail.to" --threads
    
    # Monitor for new messages (poll every N seconds)
    python check_inbox.py --inbox "myagent@agentmail.to" --monitor 30

Environment:
    AGENTMAIL_API_KEY: Your AgentMail API key
"""

import argparse
import os
import sys
import time
from datetime import datetime

try:
    from agentmail import AgentMail
except ImportError:
    print("Error: agentmail package not found. Install with: pip install agentmail")
    sys.exit(1)

def format_timestamp(iso_string):
    """Format ISO timestamp for display"""
    try:
        # strip fractional seconds if present, as fromisoformat might not like it without 'Z'
        if '.' in iso_string and not iso_string.endswith('Z'):
            iso_string = iso_string.split('.')[0]
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return iso_string # Return original string if format is unexpected

def get_from_info(from_list):
    """Helper to safely extract from address and name"""
    from_info = from_list[0] if from_list else None
    
    if isinstance(from_info, str):
        return from_info, '' # Address, no name
    elif from_info and hasattr(from_info, 'email'):
        return (from_info.email if from_info.email else 'Unknown'), (from_info.name if from_info.name else '')
    else:
        return 'Unknown', '' # Default if no valid info

def get_to_info_list(to_list):
    """Helper to safely extract list of 'to' addresses"""
    if not to_list:
        return []
    recipients = []
    for to_item in to_list:
        if isinstance(to_item, str):
            recipients.append(to_item)
        elif hasattr(to_item, 'email') and to_item.email:
            name = to_item.name if to_item.name else ''
            recipients.append(f"{name} <{to_item.email}>" if name else to_item.email)
    return recipients

def print_message_summary(message):
    """Print a summary of a message (using direct attribute access and defensive checks)"""
    from_addr, from_name = get_from_info(message.from_)

    subject = message.subject if message.subject else '(no subject)'
    timestamp = format_timestamp(message.timestamp) if message.timestamp else ''
    preview = (message.preview[:100] if message.preview else (message.text[:100] if message.text else ''))
    
    print(f"📧 {message.message_id if message.message_id else 'N/A'}")
    print(f"   From: {from_name} <{from_addr}>" if from_name else f"   From: {from_addr}")
    print(f"   Subject: {subject}")
    print(f"   Time: {timestamp}")
    if preview:
        print(f"   Preview: {preview}{'...' if len(preview) == 100 else ''}")
    print()

def print_thread_summary(thread):
    """Print a summary of a thread (using direct attribute access)"""
    subject = thread.subject if thread.subject else '(no subject)'
    # Ensure participants is a list of objects with email attribute
    participants = ', '.join([p.email for p in thread.participants if hasattr(p, 'email') and p.email]) if thread.participants else ''
    count = thread.message_count if thread.message_count is not None else 0
    timestamp = format_timestamp(thread.last_message_at) if thread.last_message_at else ''
    
    print(f"🧵 {thread.thread_id if thread.thread_id else 'N/A'}")
    print(f"   Subject: {subject}")
    print(f"   Participants: {participants}")
    print(f"   Messages: {count}")
    print(f"   Last: {timestamp}")
    print()

def main():
    parser = argparse.ArgumentParser(description='Check AgentMail inbox')
    parser.add_argument('--inbox', required=True, help='Inbox email address')
    parser.add_argument('--message', help='Get specific message by ID')
    parser.add_argument('--threads', action='store_true', help='List threads instead of messages')
    parser.add_argument('--monitor', type=int, metavar='SECONDS', help='Monitor for new messages (poll interval)')
    parser.add_argument('--limit', type=int, default=10, help='Number of items to fetch (default: 10)')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = os.getenv('AGENTMAIL_API_KEY')
    if not api_key:
        print("Error: AGENTMAIL_API_KEY environment variable not set")
        sys.exit(1)
    
    # Initialize client
    client = AgentMail(api_key=api_key)
    
    if args.monitor:
        print(f"🔍 Monitoring {args.inbox} (checking every {args.monitor} seconds)")
        print("Press Ctrl+C to stop\n")
        
        last_message_ids = set()
        
        try:
            while True:
                try:
                    messages_response = client.inboxes.messages.list(
                        inbox_id=args.inbox,
                        limit=args.limit
                    )
                    messages_list = messages_response.messages if messages_response and messages_response.messages else []
                    
                    new_messages = []
                    current_message_ids = set()
                    
                    for message in messages_list:
                        msg_id = message.message_id
                        current_message_ids.add(msg_id)
                        
                        if msg_id not in last_message_ids:
                            new_messages.append(message)
                    
                    if new_messages:
                        print(f"🆕 Found {len(new_messages)} new message(s):")
                        for message in new_messages:
                            print_message_summary(message)
                    
                    last_message_ids = current_message_ids
                    
                except Exception as e:
                    print(f"❌ Error checking inbox: {e}")
                
                time.sleep(args.monitor)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
            return
    
    elif args.message:
        # Get specific message
        try:
            message = client.inboxes.messages.get(
                inbox_id=args.inbox,
                message_id=args.message
            )
            
            print(f"📧 Message Details:")
            print(f"   ID: {message.message_id}")
            print(f"   Thread: {message.thread_id}")
            
            from_addr, from_name = get_from_info(message.from_)
            print(f"   From: {from_name} <{from_addr}>" if from_name else f"   From: {from_addr}")
            
            to_addrs_formatted = ', '.join(get_to_info_list(message.to))
            print(f"   To: {to_addrs_formatted}")
            
            print(f"   Subject: {message.subject if message.subject else '(no subject)'}")
            print(f"   Time: {format_timestamp(message.timestamp) if message.timestamp else ''}")
            
            if message.labels:
                print(f"   Labels: {', '.join(message.labels)}")
            
            print("\n📝 Content:")
            if message.text:
                print(message.text)
            elif message.html:
                print("(HTML content - use API to get full HTML)")
            else:
                print("(No text content)")
            
            if message.attachments:
                print(f"\n📎 Attachments ({len(message.attachments)}):")
                for att in message.attachments:
                    print(f"   • {att.filename if att.filename else 'unnamed'} ({att.content_type if att.content_type else 'unknown type'})")
            
        except Exception as e:
            print(f"❌ Error getting message: {e}")
            sys.exit(1)
    
    elif args.threads:
        # List threads
        try:
            threads_response = client.inboxes.threads.list(
                inbox_id=args.inbox,
                limit=args.limit
            )
            threads_list = threads_response.threads if threads_response and threads_response.threads else []
            
            if not threads_list:
                print(f"📭 No threads found in {args.inbox}")
                return
            
            print(f"🧵 Threads in {args.inbox} (showing {len(threads_list)}):\n")
            for thread in threads_list:
                print_thread_summary(thread)
                
        except Exception as e:
            print(f"❌ Error listing threads: {e}")
            sys.exit(1)
    
    else:
        # List recent messages
        try:
            messages_response = client.inboxes.messages.list(
                inbox_id=args.inbox,
                limit=args.limit
            )
            messages_list = messages_response.messages if messages_response and messages_response.messages else []
            
            if not messages_list:
                print(f"📭 No messages found in {args.inbox}")
                return
            
            print(f"📧 Messages in {args.inbox} (showing {len(messages_list)}):\n")
            for message in messages_list:
                print_message_summary(message)
                
        except Exception as e:
            print(f"❌ Error listing messages: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()