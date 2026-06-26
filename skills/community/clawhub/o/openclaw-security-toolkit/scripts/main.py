#!/usr/bin/env python3
"""
OpenClaw Security Guard - Main Entry Point
A comprehensive security tool for OpenClaw users.

Usage:
    python3 main.py <command> [options]

Commands:
    audit       Run security audit
    scan        Scan for secrets
    access      Manage access control
    token       Manage tokens
    report      Generate security report
    harden      Apply security hardening
    status      Quick security status

Options:
    --format, -f    Output format (json, md, table)
    --lang, -l      Language (en, zh)
    --quiet, -q     Quiet mode
    --verbose, -v   Verbose output
    --output, -o    Output file
    --deep          Deep scan mode
    --fix           Auto-fix issues
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from utils import (
    VERSION, load_i18n, detect_language, print_header,
    check_openclaw_installed, Colors
)
from audit import run_audit, print_audit_results
from scanner import scan_secrets, print_scan_results
from access import list_access_info, print_access_info
from token import get_token_info, rotate_token, print_token_status
from report import generate_report, format_json, format_markdown, print_table_report
from harden import apply_hardening, print_hardening_results


def cmd_audit(args, i18n: dict):
    """Run security audit."""
    print_header(i18n.get("title", "OpenClaw Security Guard"), i18n)

    results = run_audit(
        deep=args.deep,
        auto_fix=args.fix,
        quiet=args.quiet
    )

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.format == "md":
        print(format_markdown(results))
    else:
        print_audit_results(results, i18n, verbose=args.verbose)

    return 0 if results["score"] >= 50 else 1


def cmd_scan(args, i18n: dict):
    """Scan for secrets."""
    print_header(i18n.get("title", "OpenClaw Security Guard"), i18n)

    results = scan_secrets(
        custom_patterns=None,
        deep=args.deep,
        quiet=args.quiet
    )

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.format == "md":
        lines = ["# Secret Scan Results\n"]
        for f in results["findings"]:
            lines.append(f"- `{f['file']}:{f['line']}` - {f['name']} ({f['severity']})")
        print("\n".join(lines))
    else:
        print_scan_results(results, i18n, verbose=args.verbose)

    return 0 if not results["findings"] else 1


def cmd_access(args, i18n: dict):
    """Manage access control."""
    print_header(i18n.get("title", "OpenClaw Security Guard"), i18n)

    results = list_access_info(verbose=args.verbose)

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_access_info(results, i18n, verbose=args.verbose)

    return 0


def cmd_token(args, i18n: dict):
    """Manage tokens."""
    print_header(i18n.get("title", "OpenClaw Security Guard"), i18n)

    if args.token_command == "status":
        info = get_token_info()
        if args.format == "json":
            print(json.dumps(info, indent=2))
        else:
            print_token_status(info, i18n)

    elif args.token_command == "rotate":
        if not args.fix and not args.yes:
            print(f"{Colors.YELLOW}Warning: This will change your authentication token.{Colors.RESET}")
            print(f"Run with --fix or --yes to confirm.")
            return 1

        result = rotate_token(length=args.length)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print(f"{Colors.GREEN}✅ Token rotated successfully{Colors.RESET}")
                print(f"New token: {result['new_token']}")
                print(f"\n{Colors.CYAN}Restart gateway for changes to take effect:{Colors.RESET}")
                print(f"  openclaw gateway restart")
            else:
                print(f"{Colors.RED}❌ Failed to rotate token: {result.get('error')}{Colors.RESET}")

    else:
        # Default: show status
        info = get_token_info()
        if args.format == "json":
            print(json.dumps(info, indent=2))
        else:
            print_token_status(info, i18n)

    return 0


def cmd_report(args, i18n: dict):
    """Generate security report."""
    report = generate_report(
        format=args.format,
        deep=args.deep,
        include_secrets=True
    )

    output = ""
    if args.format == "json":
        output = format_json(report)
    elif args.format == "md":
        output = format_markdown(report)
    else:
        print_table_report(report, i18n)

    if output:
        if args.output:
            Path(args.output).write_text(output)
            print(f"Report saved to: {args.output}")
        else:
            print(output)

    return 0 if report["score"] >= 50 else 1


def cmd_harden(args, i18n: dict):
    """Apply security hardening."""
    print_header(i18n.get("title", "OpenClaw Security Guard"), i18n)

    results = apply_hardening(
        fix=args.fix,
        dry_run=args.dry_run
    )

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_hardening_results(results, i18n)

    return 0


def cmd_status(args, i18n: dict):
    """Quick security status check."""
    if not check_openclaw_installed():
        print(f"{Colors.RED}❌ OpenClaw not found or not configured{Colors.RESET}")
        return 1

    results = run_audit()
    score = results["score"]
    summary = results["summary"]

    if score >= 75:
        color = Colors.GREEN
        status = "✅ Good"
    elif score >= 50:
        color = Colors.YELLOW
        status = "⚠️ Warning"
    else:
        color = Colors.RED
        status = "🔴 Needs Attention"

    print()
    print(f"{Colors.BOLD}🔐 OpenClaw Security Status{Colors.RESET}")
    print()
    print(f"  Score: {color}{score}/100{Colors.RESET} {status}")
    print()
    print(f"  Issues:")
    print(f"    Critical: {summary['critical']}")
    print(f"    High: {summary['high']}")
    print(f"    Medium: {summary['medium']}")
    print(f"    Low: {summary['low']}")
    print()

    if args.format == "json":
        print(json.dumps({
            "score": score,
            "status": status,
            "summary": summary
        }, indent=2))

    return 0 if score >= 50 else 1


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Security Guard - Protect your AI assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audit                    Run security audit
  %(prog)s audit --deep --fix       Deep audit with auto-fix
  %(prog)s scan                     Scan for secrets
  %(prog)s report --format md       Generate markdown report
  %(prog)s token status             Check token status
  %(prog)s harden --fix             Apply security fixes
  %(prog)s status                   Quick status check
        """
    )

    # Global options
    parser.add_argument("--format", "-f", choices=["json", "md", "table"], default="table",
                        help="Output format (default: table)")
    parser.add_argument("--lang", "-l", choices=["en", "zh"],
                        help="Language (default: auto-detect)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Quiet mode")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    parser.add_argument("--output", "-o",
                        help="Output file path")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Run security audit")
    audit_parser.add_argument("--deep", action="store_true", help="Deep scan")
    audit_parser.add_argument("--fix", action="store_true", help="Auto-fix issues")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for secrets")
    scan_parser.add_argument("--deep", action="store_true", help="Deep scan")
    scan_parser.add_argument("--pattern", help="Custom pattern to scan")

    # access command
    access_parser = subparsers.add_parser("access", help="Manage access control")
    access_parser.add_argument("access_command", nargs="?", choices=["list", "devices", "users"],
                               default="list", help="Access subcommand")

    # token command
    token_parser = subparsers.add_parser("token", help="Manage tokens")
    token_parser.add_argument("token_command", nargs="?", choices=["status", "rotate"],
                              default="status", help="Token subcommand")
    token_parser.add_argument("--length", type=int, default=32,
                              help="Token length for rotation")
    token_parser.add_argument("--fix", action="store_true", help="Confirm token rotation")
    token_parser.add_argument("--yes", "-y", action="store_true", help="Confirm action")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate security report")
    report_parser.add_argument("--deep", action="store_true", help="Deep scan")

    # harden command
    harden_parser = subparsers.add_parser("harden", help="Apply security hardening")
    harden_parser.add_argument("--fix", action="store_true", help="Apply fixes")
    harden_parser.add_argument("--dry-run", action="store_true", help="Show what would be done")

    # status command
    status_parser = subparsers.add_parser("status", help="Quick security status")

    args = parser.parse_args()

    # Detect language
    lang = args.lang if args.lang else detect_language()
    i18n = load_i18n(lang)

    # Check if OpenClaw is installed (except for help)
    if args.command and args.command not in ["--help", "-h"]:
        if not check_openclaw_installed():
            print(f"{Colors.RED}❌ OpenClaw not found or not configured{Colors.RESET}")
            print(f"   Please ensure OpenClaw is installed and configured.")
            return 1

    # Dispatch commands
    if args.command == "audit":
        return cmd_audit(args, i18n)
    elif args.command == "scan":
        return cmd_scan(args, i18n)
    elif args.command == "access":
        return cmd_access(args, i18n)
    elif args.command == "token":
        return cmd_token(args, i18n)
    elif args.command == "report":
        return cmd_report(args, i18n)
    elif args.command == "harden":
        return cmd_harden(args, i18n)
    elif args.command == "status":
        return cmd_status(args, i18n)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())