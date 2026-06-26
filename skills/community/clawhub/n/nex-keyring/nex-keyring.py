#!/usr/bin/env python3
"""
Nex Keyring - Local API Key & Secret Rotation Tracker
Track API keys and secrets, monitor rotation status, and maintain security policies.
"""

import sys
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from lib.config import (
    DATA_DIR, DB_PATH, SERVICE_PRESETS, SERVICE_CATEGORIES,
    DEFAULT_ROTATION_DAYS, ENCRYPTION_AVAILABLE, ENCRYPTION_METHOD
)
from lib.storage import Storage
from lib.scanner import (
    scan_env_file, scan_env_vars, detect_service, check_key_rotation,
    bulk_check, hash_key
)

FOOTER = "[Nex Keyring by Nex AI | nex-ai.be]"


class KeyringCLI:
    """Command-line interface for Nex Keyring."""

    def __init__(self):
        """Initialize CLI."""
        self.storage = Storage()
        self.parser = self._build_parser()

    def _build_parser(self) -> argparse.ArgumentParser:
        """Build argument parser."""
        parser = argparse.ArgumentParser(
            description="Nex Keyring - Local API Key & Secret Rotation Tracker",
            epilog=FOOTER,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # add command
        add_parser = subparsers.add_parser("add", help="Register a new secret")
        add_parser.add_argument("--name", required=True, help="Secret name (unique)")
        add_parser.add_argument("--service", help="Service name (e.g., openai, cloudflare)")
        add_parser.add_argument("--category", default="OTHER", choices=SERVICE_CATEGORIES, help="Service category")
        add_parser.add_argument("--env-var", help="Environment variable name to check")
        add_parser.add_argument("--env-file", help="Path to .env file")
        add_parser.add_argument("--rotation", type=int, help="Rotation policy in days")
        add_parser.add_argument("--description", help="Secret description")
        add_parser.add_argument("--tags", help="Comma-separated tags")
        add_parser.add_argument("--used-in", help="Project or script names using this key")

        # list command
        list_parser = subparsers.add_parser("list", help="List tracked secrets")
        list_parser.add_argument("--service", help="Filter by service")
        list_parser.add_argument("--category", help="Filter by category")
        list_parser.add_argument("--status", default="active", help="Filter by status")

        # show command
        show_parser = subparsers.add_parser("show", help="Show secret details")
        show_parser.add_argument("name", help="Secret name")

        # check command
        check_parser = subparsers.add_parser("check", help="Check rotation status")
        check_parser.add_argument("--service", help="Check specific service")
        check_parser.add_argument("--all", action="store_true", help="Show all secrets")

        # rotate command
        rotate_parser = subparsers.add_parser("rotate", help="Mark secret as rotated")
        rotate_parser.add_argument("name", help="Secret name")
        rotate_parser.add_argument("--hash", help="New key hash (SHA256)")
        rotate_parser.add_argument("--notes", help="Rotation notes")

        # scan command
        scan_parser = subparsers.add_parser("scan", help="Scan environment for keys")
        scan_group = scan_parser.add_mutually_exclusive_group()
        scan_group.add_argument("--env-file", help="Scan specific .env file")
        scan_group.add_argument("--environment", action="store_true", help="Scan environment variables")

        # stale command
        subparsers.add_parser("stale", help="Show stale/overdue secrets")

        # history command
        history_parser = subparsers.add_parser("history", help="Show rotation history")
        history_parser.add_argument("name", help="Secret name")

        # audit command
        audit_parser = subparsers.add_parser("audit", help="Show audit log")
        audit_parser.add_argument("--limit", type=int, default=50, help="Number of entries to show")
        audit_parser.add_argument("--secret", help="Filter by secret name")

        # import command
        import_parser = subparsers.add_parser("import", help="Import secrets from .env file")
        import_parser.add_argument("file", help="Path to .env file")
        import_parser.add_argument("--auto-register", action="store_true", help="Auto-register all found keys")

        # export command
        export_parser = subparsers.add_parser("export", help="Export secret registry")
        export_parser.add_argument("--format", choices=["json", "csv", "markdown"], default="json")
        export_parser.add_argument("--output", help="Output file path")

        # stats command
        subparsers.add_parser("stats", help="Show statistics")

        # config command
        subparsers.add_parser("config", help="Show configuration")

        return parser

    def run(self, args: Optional[List[str]] = None):
        """Run CLI."""
        parsed = self.parser.parse_args(args)

        if not parsed.command:
            self.parser.print_help()
            return 0

        try:
            method = getattr(self, f"cmd_{parsed.command}")
            method(parsed)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    def cmd_add(self, args):
        """Handle add command."""
        # Determine service if not provided
        service = args.service or detect_service(args.env_var or args.name or "")

        # Determine rotation policy
        rotation_days = args.rotation or SERVICE_PRESETS.get(service, DEFAULT_ROTATION_DAYS)

        secret_data = {
            "name": args.name,
            "service": service,
            "category": args.category,
            "description": args.description,
            "rotation_policy_days": rotation_days,
            "auto_check_env_var": args.env_var,
            "env_file_path": args.env_file,
            "status": "active",
            "tags": args.tags,
            "used_in": args.used_in,
            "key_prefix": "****",
            "created_date": datetime.now().isoformat(),
        }

        secret_id = self.storage.save_secret(secret_data)
        print(f"Added secret: {args.name} (ID: {secret_id})")
        print(f"  Service: {service}")
        print(f"  Category: {args.category}")
        print(f"  Rotation policy: {rotation_days} days")
        if args.env_var:
            print(f"  Watches: {args.env_var}")

    def cmd_list(self, args):
        """Handle list command."""
        secrets = self.storage.list_secrets(
            service=args.service,
            category=args.category,
            status=args.status
        )

        if not secrets:
            print("No secrets found.")
            return

        print(f"\nTracked Secrets ({len(secrets)} total)\n")
        print(f"{'Name':<30} {'Service':<15} {'Category':<12} {'Days Since':<12} {'Status':<10}")
        print("-" * 80)

        for secret in secrets:
            rotation_check = check_key_rotation(secret)
            days_since = rotation_check["days_since_rotation"]
            risk = rotation_check["risk_level"]

            status_display = f"{secret['status']} ({risk})"

            print(f"{secret['name']:<30} {secret['service']:<15} {secret['category']:<12} {days_since:<12} {status_display:<10}")

        print(f"\n{FOOTER}")

    def cmd_show(self, args):
        """Handle show command."""
        secret = self.storage.get_secret(args.name)

        if not secret:
            print(f"Secret not found: {args.name}")
            return

        rotation_check = check_key_rotation(secret)

        print(f"\nSecret Details: {secret['name']}\n")
        print(f"Service:              {secret['service']}")
        print(f"Category:             {secret['category']}")
        print(f"Status:               {secret['status']}")
        if secret['description']:
            print(f"Description:          {secret['description']}")
        print(f"Created:              {secret['created_date']}")
        print(f"Last Rotated:         {secret['last_rotated'] or 'Never'}")
        print(f"Rotation Policy:      {secret['rotation_policy_days']} days")
        print(f"Days Since Rotation:  {rotation_check['days_since_rotation']}")
        print(f"Risk Level:           {rotation_check['risk_level']}")
        print(f"Needs Rotation:       {'Yes' if rotation_check['needs_rotation'] else 'No'}")
        if secret['auto_check_env_var']:
            print(f"Watches Env Var:      {secret['auto_check_env_var']}")
        if secret['used_in']:
            print(f"Used In:              {secret['used_in']}")
        if secret['tags']:
            print(f"Tags:                 {secret['tags']}")
        print(f"\nKey Prefix:           {secret['key_prefix']}")
        print(f"Key Hash:             {secret['key_hash'][:16]}..." if secret['key_hash'] else "Key Hash:             Not set")

        print(f"\n{FOOTER}")

    def cmd_check(self, args):
        """Handle check command."""
        if args.service:
            secrets = self.storage.list_secrets(service=args.service)
        else:
            secrets = self.storage.list_secrets(status="active")

        if not secrets:
            print("No secrets to check.")
            return

        report = bulk_check(secrets)

        # Filter to show only overdue/stale
        if not args.all:
            report = [s for s in report if s["needs_rotation"]]

        if not report:
            print("All secrets are up to date!")
            return

        print(f"\nRotation Status Report\n")
        print(f"{'Secret':<30} {'Service':<15} {'Risk':<10} {'Days':<8} {'Status':<30}")
        print("-" * 95)

        for item in report:
            days = item["days_since_rotation"]
            status = "Needs Rotation" if item["needs_rotation"] else "OK"
            print(f"{item['name']:<30} {item['service']:<15} {item['risk_level']:<10} {days:<8} {status:<30}")

        print(f"\n{FOOTER}")

    def cmd_rotate(self, args):
        """Handle rotate command."""
        secret = self.storage.get_secret(args.name)

        if not secret:
            print(f"Secret not found: {args.name}")
            return

        old_hash = secret['key_hash']
        new_hash = args.hash or input("Enter new key hash (SHA256) or leave blank: ").strip()

        self.storage.record_rotation(
            secret['id'],
            old_hash=old_hash,
            new_hash=new_hash,
            notes=args.notes
        )

        print(f"Rotation recorded for: {args.name}")
        print(f"  Last rotated: {datetime.now().isoformat()}")
        if new_hash:
            print(f"  New hash: {new_hash[:16]}...")

        print(f"\n{FOOTER}")

    def cmd_scan(self, args):
        """Handle scan command."""
        if args.env_file:
            found = scan_env_file(args.env_file)
            print(f"\nScanned: {args.env_file}\n")
        elif args.environment:
            found = scan_env_vars()
            print(f"\nScanning environment variables...\n")
        else:
            print("Specify --env-file or --environment")
            return

        if not found:
            print("No API keys detected.")
            return

        print(f"{'Name':<30} {'Service':<15} {'Has Value':<12}")
        print("-" * 60)

        for key in found:
            has_val = "Yes" if key['has_value'] else "No"
            print(f"{key['name']:<30} {key['service']:<15} {has_val:<12}")

        print(f"\n{FOOTER}")

    def cmd_stale(self, args):
        """Handle stale command."""
        stale = self.storage.get_stale_secrets(90)
        overdue = self.storage.get_overdue_secrets()

        print(f"\nSecurity Status\n")
        print(f"Stale Secrets (>90 days):    {len(stale)}")
        print(f"Overdue Secrets:             {len(overdue)}")

        if stale or overdue:
            print(f"\n{'Secret':<30} {'Service':<15} {'Days':<8} {'Status':<20}")
            print("-" * 75)

            for secret in stale + overdue:
                check = check_key_rotation(secret)
                status = "STALE" if secret in stale else "OVERDUE"
                days = check["days_since_rotation"]
                print(f"{secret['name']:<30} {secret['service']:<15} {days:<8} {status:<20}")

        print(f"\n{FOOTER}")

    def cmd_history(self, args):
        """Handle history command."""
        secret = self.storage.get_secret(args.name)

        if not secret:
            print(f"Secret not found: {args.name}")
            return

        history = self.storage.get_rotation_history(secret['id'])

        print(f"\nRotation History: {args.name}\n")

        if not history:
            print("No rotation history recorded.")
            return

        for entry in history:
            print(f"Date:     {entry['rotated_at']}")
            print(f"Rotated by: {entry['rotated_by']}")
            if entry['notes']:
                print(f"Notes:    {entry['notes']}")
            print()

        print(f"{FOOTER}")

    def cmd_audit(self, args):
        """Handle audit command."""
        secret_id = None

        if args.secret:
            secret = self.storage.get_secret(args.secret)
            if not secret:
                print(f"Secret not found: {args.secret}")
                return
            secret_id = secret['id']

        entries = self.storage.get_audit_log(limit=args.limit, secret_id=secret_id)

        print(f"\nAudit Log (Latest {len(entries)} entries)\n")
        print(f"{'Timestamp':<20} {'Action':<12} {'Secret':<30} {'Details':<35}")
        print("-" * 100)

        for entry in entries:
            timestamp = entry['timestamp'][:19] if entry['timestamp'] else ""
            action = entry['action']
            secret_name = "N/A"
            details = entry['details'][:35] if entry['details'] else ""

            print(f"{timestamp:<20} {action:<12} {secret_name:<30} {details:<35}")

        print(f"\n{FOOTER}")

    def cmd_import(self, args):
        """Handle import command."""
        found = scan_env_file(args.file)

        if not found:
            print("No API keys found in file.")
            return

        print(f"\nFound {len(found)} keys in {args.file}\n")

        added_count = 0

        for key in found:
            existing = self.storage.get_secret(key['name'])

            if existing:
                print(f"  {key['name']:<30} (already tracked)")
                continue

            secret_data = {
                "name": key['name'],
                "service": key['service'],
                "category": "API",
                "rotation_policy_days": SERVICE_PRESETS.get(key['service'], DEFAULT_ROTATION_DAYS),
                "auto_check_env_var": key['name'],
                "env_file_path": args.file,
                "status": "active",
                "key_prefix": "****",
                "created_date": datetime.now().isoformat(),
            }

            self.storage.save_secret(secret_data)
            added_count += 1
            print(f"  {key['name']:<30} (added)")

        print(f"\nImported {added_count} new secrets.")
        print(f"\n{FOOTER}")

    def cmd_export(self, args):
        """Handle export command."""
        data = self.storage.export_secrets(format=args.format)

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(data)
            print(f"Exported to: {output_path}")
        else:
            print(data)

        print(f"\n{FOOTER}")

    def cmd_stats(self, args):
        """Handle stats command."""
        stats = self.storage.get_secret_stats()

        print(f"\nNex Keyring Statistics\n")
        print(f"Total Secrets:        {stats['total']}")
        print(f"Stale (>90 days):     {stats['stale_count']}")
        print(f"Overdue:              {stats['overdue_count']}")

        print(f"\nBy Category:")
        for category, count in sorted(stats['by_category'].items()):
            print(f"  {category:<20} {count}")

        print(f"\nBy Service:")
        for service, count in sorted(stats['by_service'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {service:<20} {count}")

        print(f"\n{FOOTER}")

    def cmd_config(self, args):
        """Handle config command."""
        print(f"\nNex Keyring Configuration\n")
        print(f"Data Directory:       {DATA_DIR}")
        print(f"Database:             {DB_PATH}")
        print(f"Encryption:           {ENCRYPTION_METHOD.upper()}")
        print(f"Encryption Available: {'Yes' if ENCRYPTION_AVAILABLE else 'No (base64 only)'}")
        print(f"Default Rotation:     {DEFAULT_ROTATION_DAYS} days")

        print(f"\nService Presets:")
        for service, days in sorted(SERVICE_PRESETS.items()):
            print(f"  {service:<20} {days} days")

        print(f"\n{FOOTER}")


def main():
    """Main entry point."""
    cli = KeyringCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
