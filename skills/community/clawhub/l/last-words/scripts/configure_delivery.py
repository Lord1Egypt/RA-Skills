#!/usr/bin/env python3
"""
Configure delivery settings for last-words.
Usage: python3 configure_delivery.py --method email|wechat|phone --contact "value"
       [--smtp-host host] [--smtp-port port] [--smtp-user user] [--smtp-pass pass]

Or use environment variables (recommended for security):
  SMTP_USER, SMTP_PASS, CONTACT_EMAIL, SMTP_HOST, SMTP_PORT

Or create a .env file from .env.example
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import save_config, init_db


def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                # Only set if not already in environment
                if key not in os.environ:
                    os.environ[key] = value


def get_env_config():
    """Get configuration from environment variables."""
    return {
        'smtp_user': os.environ.get('SMTP_USER'),
        'smtp_pass': os.environ.get('SMTP_PASS'),
        'contact': os.environ.get('CONTACT_EMAIL'),
        'smtp_host': os.environ.get('SMTP_HOST', 'smtp.qq.com'),
        'smtp_port': int(os.environ.get('SMTP_PORT', '465')),
    }


def main():
    parser = argparse.ArgumentParser(description="Configure delivery settings")
    parser.add_argument("--method", "-m",
                        choices=["email", "wechat", "phone"],
                        help="Delivery method (default: email)")
    parser.add_argument("--contact", "-c",
                        help="Contact address (email, wechat id, or phone number)")
    parser.add_argument("--smtp-host", help="SMTP server host (for email)")
    parser.add_argument("--smtp-port", type=int, help="SMTP server port")
    parser.add_argument("--smtp-user", help="SMTP username")
    parser.add_argument("--smtp-pass", help="SMTP password")
    parser.add_argument("--from-env", "-e", action="store_true",
                        help="Load configuration from environment variables or .env file")

    args = parser.parse_args()

    try:
        init_db()

        # Load from env file if exists
        load_env_file()

        # If --from-env flag is set, use environment variables
        if args.from_env:
            env_config = get_env_config()
            if not env_config['smtp_user'] or not env_config['smtp_pass'] or not env_config['contact']:
                print("✗ Missing required environment variables:", file=sys.stderr)
                print("  Required: SMTP_USER, SMTP_PASS, CONTACT_EMAIL", file=sys.stderr)
                print("  Optional: SMTP_HOST (default: smtp.qq.com), SMTP_PORT (default: 465)", file=sys.stderr)
                sys.exit(1)

            save_config(
                method="email",
                contact=env_config['contact'],
                smtp_host=env_config['smtp_host'],
                smtp_port=env_config['smtp_port'],
                smtp_user=env_config['smtp_user'],
                smtp_pass=env_config['smtp_pass']
            )
            print(f"✓ Configuration loaded from environment/.env file")
            print(f"  SMTP User: {env_config['smtp_user']}")
            print(f"  Contact: {env_config['contact']}")
            print(f"  SMTP: {env_config['smtp_host']}:{env_config['smtp_port']}")
            return

        # Otherwise require manual arguments
        if not args.method or not args.contact:
            parser.print_help()
            print("\n✗ Error: --method and --contact are required (or use --from-env)", file=sys.stderr)
            sys.exit(1)

        # For non-email methods, warn that they're not fully implemented
        if args.method == "wechat":
            print("⚠ WeChat delivery is planned but not yet implemented.")
            print("  Configuration saved but delivery will not work until implemented.")
        elif args.method == "phone":
            print("⚠ Phone/SMS delivery is planned but not yet implemented.")
            print("  Configuration saved but delivery will not work until implemented.")

        save_config(
            method=args.method,
            contact=args.contact,
            smtp_host=args.smtp_host,
            smtp_port=args.smtp_port,
            smtp_user=args.smtp_user,
            smtp_pass=args.smtp_pass
        )

        print(f"✓ Delivery configuration saved")
        print(f"  Method: {args.method}")
        print(f"  Contact: {args.contact}")
        if args.smtp_host:
            print(f"  SMTP: {args.smtp_host}:{args.smtp_port}")

    except Exception as e:
        print(f"✗ Error saving configuration: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
