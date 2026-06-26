from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

try:
    from .core import OtpEntry, Vault, format_entry_name, render_codes, totp_code
except ImportError:  # Allows running as `python cli.py`
    from core import OtpEntry, Vault, format_entry_name, render_codes, totp_code


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="otpforge", description="Manage and view 2FA TOTP codes")
    parser.add_argument(
        "--store",
        help="Path to secrets store JSON (overrides OTPFORGE_STORE env var)",
        default=None,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add or update an account")
    add.add_argument("label", help="Account label, e.g. email@domain.com")
    add.add_argument("secret", help="Base32 secret key")
    add.add_argument("--issuer", default="", help="Issuer name, e.g. GitHub")
    add.add_argument("--digits", type=int, default=6, help="Code length (default: 6)")
    add.add_argument("--period", type=int, default=30, help="TOTP period in seconds (default: 30)")

    list_cmd = sub.add_parser("list", help="List all stored accounts")
    list_cmd.add_argument("--codes", action="store_true", help="Include live codes")

    code = sub.add_parser("code", help="Show a current code for one account")
    code.add_argument("label", help="Account label")

    remove = sub.add_parser("remove", help="Delete an account")
    remove.add_argument("label", help="Account label")

    sub.add_parser("gui", help="Launch desktop GUI")

    return parser


def _cmd_add(args: argparse.Namespace, vault: Vault) -> int:
    vault.upsert(
        OtpEntry(
            label=args.label,
            secret=args.secret,
            issuer=args.issuer,
            digits=args.digits,
            period=args.period,
        )
    )
    print(f"Saved: {args.label}")
    return 0


def _cmd_list(args: argparse.Namespace, vault: Vault) -> int:
    entries = vault.list_entries()
    if not entries:
        print("No accounts stored yet.")
        return 0

    if args.codes:
        for entry, code, remain in render_codes(entries):
            print(f"{format_entry_name(entry):30} {code}  ({remain:2d}s)")
        return 0

    for entry in entries:
        print(format_entry_name(entry))
    return 0


def _cmd_code(args: argparse.Namespace, vault: Vault) -> int:
    entry = vault.get(args.label)
    if not entry:
        print(f"No account found for label: {args.label}", file=sys.stderr)
        return 1

    code = totp_code(entry.secret, digits=entry.digits, period=entry.period)
    remain = entry.period - (int(time.time()) % entry.period)
    print(f"{format_entry_name(entry)}")
    print(f"Code: {code} ({remain}s left)")
    return 0


def _cmd_remove(args: argparse.Namespace, vault: Vault) -> int:
    removed = vault.remove(args.label)
    if not removed:
        print(f"No account found for label: {args.label}", file=sys.stderr)
        return 1
    print(f"Removed: {args.label}")
    return 0


def run(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    vault = Vault(path=Path(args.store).expanduser().resolve()) if args.store else Vault()

    if args.command == "add":
        return _cmd_add(args, vault)
    if args.command == "list":
        return _cmd_list(args, vault)
    if args.command == "code":
        return _cmd_code(args, vault)
    if args.command == "remove":
        return _cmd_remove(args, vault)
    if args.command == "gui":
        try:
            from .gui import launch
        except ImportError:
            from gui import launch

        launch(vault)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(run())
