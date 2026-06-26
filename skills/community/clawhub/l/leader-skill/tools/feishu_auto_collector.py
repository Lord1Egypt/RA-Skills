#!/usr/bin/env python3
"""
Feishu Auto Collector - Collect leader data from Feishu.
Part of create-leader skill.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Feishu Auto Collector')
    parser.add_argument('--setup', action='store_true',
                        help='Setup Feishu credentials')
    parser.add_argument('--name', required=not '--setup' in sys.argv,
                        help='Leader name to collect')
    parser.add_argument('--output-dir', required=not '--setup' in sys.argv,
                        help='Output directory for collected data')
    parser.add_argument('--msg-limit', type=int, default=2000,
                        help='Maximum messages to collect')
    parser.add_argument('--doc-limit', type=int, default=30,
                        help='Maximum documents to collect')
    parser.add_argument('--open-id', help='Target user open_id (for private chat)')
    parser.add_argument('--p2p-chat-id', help='Private chat ID')
    parser.add_argument('--user-token', help='User access token (for private chat)')
    parser.add_argument('--exchange-code', help='Exchange OAuth code for token')
    return parser.parse_args()


def setup_credentials():
    """Setup Feishu credentials interactively."""
    config_dir = os.path.expanduser('~/.create-leader')
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, 'feishu_config.json')

    print("=== Feishu Credential Setup ===\n")
    print("Please enter your Feishu app credentials:")
    print("(Get these from Feishu Open Platform: https://open.feishu.cn)")

    app_id = input("App ID: ").strip()
    app_secret = input("App Secret: ").strip()
    redirect_uri = input("Redirect URI (default: http://www.example.com): ").strip()
    if not redirect_uri:
        redirect_uri = 'http://www.example.com'

    config = {
        'app_id': app_id,
        'app_secret': app_secret,
        'redirect_uri': redirect_uri,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Config saved to: {config_path}")
    print("\nNext steps:")
    print("1. Add redirect URI to your Feishu app security settings")
    print("2. Enable required scopes: im:message, im:chat")
    print("3. Run collector with --name and --output-dir")


def exchange_code_for_token(code):
    """Exchange OAuth code for user access token."""
    config_dir = os.path.expanduser('~/.create-leader')
    config_path = os.path.join(config_dir, 'feishu_config.json')

    if not os.path.exists(config_path):
        print("Error: Config not found. Run with --setup first.", file=sys.stderr)
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)

    print("=== OAuth Token Exchange ===\n")
    print("Note: This is a placeholder. In production, implement actual API calls.")
    print(f"Would exchange code '{code}' for token using app: {config['app_id']}")
    print("\nFor now, please manually obtain user_access_token from Feishu.")


def collect_data(name, output_dir, msg_limit, doc_limit, open_id=None, p2p_chat_id=None, user_token=None):
    """Collect leader data from Feishu."""
    os.makedirs(output_dir, exist_ok=True)

    print(f"=== Feishu Data Collection ===\n")
    print(f"Leader: {name}")
    print(f"Output: {output_dir}")
    print(f"Message limit: {msg_limit}")
    print(f"Document limit: {doc_limit}")
    print()

    # This is a placeholder implementation
    # In production, implement actual Feishu API calls

    print("📝 Note: This is a placeholder collector.")
    print("   Full implementation requires:")
    print("   - Feishu app credentials (app_id, app_secret)")
    print("   - OAuth user authorization")
    print("   - Proper API error handling")
    print()

    # Create placeholder files
    summary = {
        'leader_name': name,
        'collected_at': datetime.utcnow().isoformat() + 'Z',
        'messages_collected': 0,
        'documents_collected': 0,
        'status': 'placeholder - needs full implementation'
    }

    # Write placeholder output files
    with open(os.path.join(output_dir, 'collection_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_dir, 'messages.txt'), 'w') as f:
        f.write(f"# Messages for {name}\n\n")
        f.write("[Placeholder - implement actual Feishu API collection]\n")

    with open(os.path.join(output_dir, 'docs.txt'), 'w') as f:
        f.write(f"# Documents for {name}\n\n")
        f.write("[Placeholder - implement actual Feishu API collection]\n")

    print("✅ Placeholder files created.")
    print(f"   Next: Implement actual Feishu API calls in this script.")
    print(f"   Output files in: {output_dir}")


def main():
    args = parse_args()

    if args.setup:
        setup_credentials()
    elif args.exchange_code:
        exchange_code_for_token(args.exchange_code)
    else:
        collect_data(args.name, args.output_dir,
                    args.msg_limit, args.doc_limit,
                    args.open_id, args.p2p_chat_id, args.user_token)


if __name__ == '__main__':
    main()
