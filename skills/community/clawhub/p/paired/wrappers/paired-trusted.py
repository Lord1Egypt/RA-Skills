#!/usr/bin/env python3
"""paired-trusted — manage the trusted-numbers list.

Reads/writes ${HOME}/.config/paired/trusted-numbers.conf

Commands:
  paired-trusted list                            # show current trusted numbers
  paired-trusted add 07911123456 [name]          # add a number
  paired-trusted remove 07911123456              # remove
  paired-trusted check 07911123456               # is this number trusted?

Numbers are stored exactly as provided (any UK format) but matched after
normalization in the consumers (paired-respond, paired-call-handler).
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
_HOME = str(Path.home())

CONFIG_FILE = Path(f"{_HOME}/.config/paired/trusted-numbers.conf")


def normalize_uk(num: str) -> str:
    if not num:
        return ""
    n = num.strip().replace(" ", "").replace("-", "")
    if n.startswith("+44"):
        return "0" + n[3:]
    if n.startswith("0044"):
        return "0" + n[4:]
    if n.startswith("44") and len(n) == 12:
        return "0" + n[2:]
    return n


def parse_file() -> list[tuple[str, str, str]]:
    """Return list of (raw_number, comment, original_line) for each entry.
    raw_number is the number text. comment is anything after '#' on the line.
    Empty/comment-only lines have raw_number=''."""
    if not CONFIG_FILE.exists():
        return []
    out = []
    for line in CONFIG_FILE.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out.append(("", "", line))
            continue
        # Split number from inline comment
        if "#" in stripped:
            num_part, comment = stripped.split("#", 1)
            num = num_part.strip()
            comment = "# " + comment.strip()
        else:
            num = stripped
            comment = ""
        out.append((num, comment, line))
    return out


def load_normalized() -> dict:
    """Returns dict of normalized -> (original_number, comment)."""
    out = {}
    for num, comment, _ in parse_file():
        if not num:
            continue
        n = normalize_uk(num)
        if n:
            out[n] = (num, comment)
    return out


def write_entries(entries: list[str], header_lines: list[str]) -> None:
    """Rewrite the file with given header (preserved comments) + entries."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    out = "\n".join(header_lines) + "\n\n" + "\n".join(entries) + "\n"
    tmp = CONFIG_FILE.with_suffix(".conf.tmp")
    tmp.write_text(out)
    tmp.chmod(0o600)
    tmp.replace(CONFIG_FILE)


def cmd_list() -> int:
    entries = load_normalized()
    if not entries:
        print(f"(no trusted numbers in {CONFIG_FILE})")
        return 0
    print(f"Trusted numbers ({len(entries)}):")
    for normalized, (raw, comment) in sorted(entries.items()):
        print(f"  {raw:<20} {comment}")
    return 0


def cmd_check(number: str) -> int:
    n = normalize_uk(number)
    entries = load_normalized()
    if n in entries:
        raw, comment = entries[n]
        print(f"YES — {n} is trusted (stored as {raw!r} {comment})")
        return 0
    print(f"NO — {n} is NOT trusted")
    return 1


def cmd_add(number: str, name: str = "") -> int:
    n = normalize_uk(number)
    if not n:
        print(f"ERROR: could not normalize {number!r}")
        return 2

    existing = load_normalized()
    if n in existing:
        raw, comment = existing[n]
        print(f"Already present: {raw} {comment}")
        return 0

    # Read existing file content - keep header comments, append new entry before
    # any existing number lines? Actually simpler: just append at end.
    if CONFIG_FILE.exists():
        current = CONFIG_FILE.read_text().rstrip("\n")
    else:
        current = (
            "# paired trusted numbers list\n"
            "# One number per line. UK formats accepted: 07..., +447..., 00447...\n"
            "# Lines starting with # are comments. Empty lines ignored.\n"
            "# Edit with: paired-trusted add 07XXX [name]\n"
        )

    comment = f"  # {name}" if name else ""
    new_line = f"{number}{comment}"

    out = current + "\n" + new_line + "\n"
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CONFIG_FILE.with_suffix(".conf.tmp")
    tmp.write_text(out)
    tmp.chmod(0o600)
    tmp.replace(CONFIG_FILE)
    print(f"Added: {number} (normalized: {n}) {comment}")
    return 0


def cmd_remove(number: str) -> int:
    n = normalize_uk(number)
    existing = load_normalized()
    if n not in existing:
        print(f"Not present: {number} (normalized: {n})")
        return 1

    # Walk line-by-line, drop any line whose number normalizes to n
    new_lines = []
    removed = 0
    for line in CONFIG_FILE.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue
        num_part = stripped.split("#", 1)[0].strip()
        if num_part and normalize_uk(num_part) == n:
            removed += 1
            continue
        new_lines.append(line)

    out = "\n".join(new_lines).rstrip("\n") + "\n"
    tmp = CONFIG_FILE.with_suffix(".conf.tmp")
    tmp.write_text(out)
    tmp.chmod(0o600)
    tmp.replace(CONFIG_FILE)
    print(f"Removed {removed} entry(ies) matching {n}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Manage paired trusted numbers.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="Show trusted numbers")
    p_add = sub.add_parser("add", help="Add a trusted number")
    p_add.add_argument("number", help="UK number in any format")
    p_add.add_argument("name", nargs="?", default="", help="Friendly label (becomes inline comment)")
    p_rm = sub.add_parser("remove", help="Remove a trusted number")
    p_rm.add_argument("number", help="UK number in any format")
    p_chk = sub.add_parser("check", help="Check if a number is trusted")
    p_chk.add_argument("number", help="UK number in any format")
    args = p.parse_args()

    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "add":
        return cmd_add(args.number, args.name)
    if args.cmd == "remove":
        return cmd_remove(args.number)
    if args.cmd == "check":
        return cmd_check(args.number)
    return 1


if __name__ == "__main__":
    sys.exit(main())
