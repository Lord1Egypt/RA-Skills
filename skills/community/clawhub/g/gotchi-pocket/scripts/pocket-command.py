#!/usr/bin/env python3
"""Natural-language command dispatcher for gotchi-pocket skill."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

TOKEN_ALIASES = ("GHST", "FUD", "FOMO", "ALPHA", "KEK", "USDC", "WETH", "DAI")
TOKEN_PATTERN = r"(0x[a-fA-F0-9]{40}|GHST|FUD|FOMO|ALPHA|KEK|USDC|WETH|DAI)"
AMOUNT_PATTERN = r"([0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)"
APPROVAL_EXIT_CODE = 3


class ParseError(Exception):
    pass


def extract_gotchi_id(text: str) -> str:
    m = re.search(r"\bgotchi(?:\s*id)?\s*#?\s*(\d+)\b", text, flags=re.IGNORECASE)
    if m:
        return m.group(1)

    m = re.search(r"#(\d+)\b", text)
    if m and ("gotchi" in text.lower() or "pocket" in text.lower()):
        return m.group(1)

    raise ParseError("Could not find gotchi ID (expected like 'gotchi 9638' or 'gotchi id 9638').")


def extract_amount_and_token(text: str) -> tuple[str, str]:
    m = re.search(
        rf"\b(?:send|transfer|withdraw|deposit|move|add)\b\s+{AMOUNT_PATTERN}\s+{TOKEN_PATTERN}\b",
        text,
        flags=re.IGNORECASE,
    )
    if not m:
        raise ParseError("Could not parse '<amount> <token>' (example: 'send 25 GHST ...').")
    amount = m.group(1)
    token = m.group(2)
    return amount, token


def extract_token(text: str) -> str:
    m = re.search(TOKEN_PATTERN, text, flags=re.IGNORECASE)
    if not m:
        aliases = ", ".join(TOKEN_ALIASES)
        raise ParseError(f"Could not find token symbol/address. Supported aliases: {aliases}")
    return m.group(1)


def extract_to_address(text: str) -> str:
    m = re.search(r"\bto\s+(0x[a-fA-F0-9]{40})\b", text, flags=re.IGNORECASE)
    if not m:
        raise ParseError("Could not find destination address (expected 'to 0x...').")
    return m.group(1)


def classify_intent(text: str) -> str:
    lower = text.lower()

    # Withdrawal from pocket to an address.
    if re.search(r"\bfrom\b[^\n]*\bpocket\b", lower) and re.search(
        r"\b(send|transfer|withdraw|move)\b", lower
    ):
        return "withdraw"

    # Deposit into pocket.
    if re.search(r"\b(to|into)\b[^\n]*\bpocket\b", lower) and re.search(
        r"\b(send|transfer|deposit|move|add)\b", lower
    ):
        return "deposit"

    # Balance query.
    if "balance" in lower and "pocket" in lower:
        return "balance"

    # Pocket info query.
    if any(
        phrase in lower
        for phrase in (
            "pocket info",
            "pocket address",
            "owner and pocket",
            "who owns",
            "who is owner",
            "wallet info",
        )
    ):
        return "info"

    raise ParseError(
        "Could not classify intent. Try phrases like: "
        "'send 25 GHST to gotchi 9638 pocket' or "
        "'send 25 GHST from gotchi 9638 pocket to 0x...'."
    )


def build_dispatch(text: str) -> tuple[str, list[str], str]:
    intent = classify_intent(text)
    gotchi_id = extract_gotchi_id(text)

    if intent == "deposit":
        amount, token = extract_amount_and_token(text)
        return "pocket-deposit.sh", [gotchi_id, token, amount], intent

    if intent == "withdraw":
        amount, token = extract_amount_and_token(text)
        to_address = extract_to_address(text)
        return "pocket-withdraw.sh", [gotchi_id, token, to_address, amount], intent

    if intent == "balance":
        token = extract_token(text)
        return "pocket-balance.sh", [gotchi_id, token], intent

    if intent == "info":
        # Auto-check Bankr ownership match in natural-language flow.
        return "pocket-info.sh", [gotchi_id, "--check-bankr"], intent

    raise ParseError(f"Unsupported intent: {intent}")


def run_dispatch(script_name: str, script_args: list[str], dry_run: bool) -> int:
    script_path = SCRIPT_DIR / script_name
    cmd = [str(script_path), *script_args]
    dispatch = " ".join(shlex.quote(part) for part in cmd)

    print(f"dispatch={dispatch}")

    if dry_run:
        return 0

    proc = subprocess.run(cmd, text=True, capture_output=True)

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)

    return proc.returncode


def require_withdraw_approval(intent: str, approve_withdraw: bool, dry_run: bool, text: str) -> int:
    if intent != "withdraw" or approve_withdraw or dry_run:
        return 0

    print("approval_required=true")
    print("message=Are you sure you want to send tokens from this gotchi pocket?")
    print('next=Re-run with --approve-withdraw "<same command>"')
    print(f"command={text}")
    return APPROVAL_EXIT_CODE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Interpret natural-language gotchi pocket commands and dispatch to skill scripts."
    )
    parser.add_argument("command", nargs="*", help="Natural language command text")
    parser.add_argument("--dry-run", action="store_true", help="Only print selected script and args")
    parser.add_argument(
        "--approve-withdraw",
        action="store_true",
        help="Approve and execute withdraw/send-from-pocket intents",
    )
    args = parser.parse_args()

    if args.command:
        text = " ".join(args.command).strip()
    else:
        text = sys.stdin.read().strip()

    if not text:
        parser.error("Provide a command string or pipe one through stdin.")

    try:
        script_name, script_args, intent = build_dispatch(text)
    except ParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    approval_result = require_withdraw_approval(
        intent=intent,
        approve_withdraw=args.approve_withdraw,
        dry_run=args.dry_run,
        text=text,
    )
    if approval_result != 0:
        return approval_result

    return run_dispatch(script_name, script_args, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
