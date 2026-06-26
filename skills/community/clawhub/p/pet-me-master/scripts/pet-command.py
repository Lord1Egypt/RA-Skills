#!/usr/bin/env python3
"""Natural-language command dispatcher for pet-me-master."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


class ParseError(Exception):
    pass


def normalize(text: str) -> str:
    return " ".join(text.strip().split()).lower()


def extract_gotchi_id(text: str) -> str | None:
    match = re.search(r"\bgotchi(?:\s*id)?\s*#?\s*(\d+)\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)

    hash_match = re.search(r"#(\d+)\b", text)
    if hash_match:
        return hash_match.group(1)

    return None


def classify(text: str) -> tuple[str, list[str]]:
    lowered = normalize(text)
    gotchi_id = extract_gotchi_id(text)

    if any(phrase in lowered for phrase in ("pet status", "status", "when can i pet", "when pet")):
        return "pet-status.sh", []

    if "check cooldown" in lowered or "cooldown" in lowered:
        return "check-cooldown.sh", [gotchi_id] if gotchi_id else []

    # Enforced behavior: any pet action is batch-only (pet-all.sh).
    if "pet" in lowered:
        return "pet-all.sh", []

    raise ParseError(
        "Could not classify command. Try: 'pet my gotchis', 'pet status', or 'check cooldown for gotchi 9638'."
    )


def build_dispatch(text: str, tx_dry_run: bool) -> list[str]:
    script_name, args = classify(text)
    cmd = [str(SCRIPT_DIR / script_name)]

    if tx_dry_run and script_name in {"pet.sh", "pet-all.sh", "pet-via-bankr.sh"}:
        cmd.append("--dry-run")

    cmd.extend([arg for arg in args if arg])
    return cmd


def run_command(cmd: list[str], dry_run: bool) -> int:
    print(f"dispatch={' '.join(shlex.quote(part) for part in cmd)}")

    if dry_run:
        return 0

    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Interpret natural-language pet-me-master commands and dispatch to scripts."
    )
    parser.add_argument("--dry-run", action="store_true", help="Only print which script would run")
    parser.add_argument(
        "--tx-dry-run",
        action="store_true",
        help="Forward --dry-run to mutating scripts (pet-all.sh)",
    )
    parser.add_argument("command", nargs="*", help="Natural language command text")
    args = parser.parse_args()

    if args.command:
        text = " ".join(args.command).strip()
    else:
        text = sys.stdin.read().strip()

    if not text:
        parser.error("Provide a command string or pipe one through stdin.")

    try:
        cmd = build_dispatch(text, tx_dry_run=args.tx_dry_run)
    except ParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return run_command(cmd, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
