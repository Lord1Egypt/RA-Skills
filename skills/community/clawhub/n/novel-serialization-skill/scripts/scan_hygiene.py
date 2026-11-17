#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_hygiene.py —— 文件卫生扫描（CRLF / 乱码 / 垃圾 / 体量）。

Why this exists
---------------
Two failure modes cost the -1928 subproject the most rework, and both are
invisible in review:

1. **CRLF recurrence.** On Windows, ``io.open(p, 'w', encoding='utf-8')``
   defaults to ``newline=None``: it normalises CRLF to LF on read *and converts
   LF back to CRLF on write*. Any Markdown file that a Python script touches
   — even for a one-line edit — is rewritten entirely as CRLF.
   ``.gitattributes`` cannot stop it, because the conversion happens at write
   time inside the script. The repository rule is therefore:

       **凡写文本，一律 io.open(..., newline='\\n')**
       (always write text files with newline='\\n')

2. **Junk accumulation.** ``*.bak``, ``*.tmp``, editor droppings and ad-hoc
   backup stacks bloat the tree until the signal-to-noise ratio collapses.

Checks
------
crlf        Files containing CRLF line endings.
mojibake    Replacement char U+FFFD or classic UTF-8-as-CP1252 sequences.
junk        Temp / backup / OS droppings that should not be committed.
empty       Zero-byte text files.
no-eol      Files without a trailing newline.
lines       Files over the line budget (default 500, configurable).

Usage
-----
    python scripts/scan_hygiene.py --root .
    python scripts/scan_hygiene.py --root . --fix           # rewrite CRLF -> LF
    python scripts/scan_hygiene.py --root . --max-lines 500 \
        --allow "README FOR AI.md,CHANGELOG.md,LICENSE"
    python scripts/scan_hygiene.py --root . --json
    python scripts/scan_hygiene.py --root . --fail-on crlf,junk,mojibake

Exit codes
----------
0  clean (or no finding in a --fail-on bucket)
1  at least one finding in a --fail-on bucket
2  usage / IO error

This script writes LF endings only.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}

TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".json", ".txt", ".cfg", ".toml", ".sh"}

JUNK_EXACT = {".DS_Store", "Thumbs.db", "Desktop.ini", "ehthumbs.db"}
JUNK_SUFFIXES = (".bak", ".tmp", ".orig", ".rej", ".swp", ".swo")
JUNK_PREFIXES = ("~$",)

# NOTE: written as escapes on purpose. Literal mojibake in this file would make
# the scanner flag itself — the same self-trigger trap the -1928 project hit
# when it quoted banned words inside the documents that ban them.
MOJIBAKE_MARKERS = (
    "\ufffd",                    # replacement character
    "\u00ef\u00bf\u00bd",        # U+FFFD read back as CP1252
    "\u00e2\u20ac",              # UTF-8 euro / curly quote lead byte pair
    "\u00c3\u00a5",              # 'å' read as CP1252
    "\u00e6\u2013",              # CJK lead byte read as CP1252
    "\u00ef\u00bc",              # fullwidth lead byte read as CP1252
)

DEFAULT_BUDGET = 500

CHECK_ORDER = ["crlf", "mojibake", "junk", "empty", "no-eol", "lines"]

MEANING = {
    "crlf": "file uses CRLF line endings; repository policy is LF",
    "mojibake": "encoding damage (replacement char or UTF-8-as-CP1252 sequence)",
    "junk": "temp / backup / OS droppings that must not be committed",
    "empty": "zero-byte file",
    "no-eol": "missing trailing newline",
    "lines": "over the line budget",
}


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield Path(dirpath) / name


def is_junk(p: Path) -> bool:
    n = p.name
    if n in JUNK_EXACT:
        return True
    if n.endswith(JUNK_SUFFIXES):
        return True
    if n.startswith(JUNK_PREFIXES):
        return True
    if n.endswith("~"):
        return True
    return False


def scan(root: Path, max_lines: int, allow: set):
    root = root.resolve()
    findings = {k: [] for k in CHECK_ORDER}

    for p in iter_files(root):
        try:
            rel = p.resolve().relative_to(root).as_posix()
        except ValueError:
            continue

        if is_junk(p):
            findings["junk"].append({"file": rel, "detail": p.name})
            continue

        if p.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            raw = p.read_bytes()
        except OSError as exc:
            print(f"[warn] unreadable: {rel} ({exc})", file=sys.stderr)
            continue

        if not raw:
            findings["empty"].append({"file": rel, "detail": "0 bytes"})
            continue

        if b"\r\n" in raw:
            findings["crlf"].append({"file": rel, "detail": f"{raw.count(b'\r\n')} CRLF"})

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            findings["mojibake"].append({"file": rel, "detail": "not valid UTF-8"})
            continue

        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                findings["mojibake"].append({"file": rel, "detail": f"marker {marker!r}"})
                break

        if not text.endswith("\n"):
            findings["no-eol"].append({"file": rel, "detail": "no trailing newline"})

        n_lines = text.count("\n") + (0 if text.endswith("\n") else 1)
        if n_lines > max_lines and rel not in allow:
            findings["lines"].append({"file": rel, "detail": f"{n_lines} > {max_lines}"})

    return findings


def fix_crlf(root: Path, items) -> int:
    fixed = 0
    for it in items:
        p = root / it["file"]
        raw = p.read_bytes()
        p.write_bytes(raw.replace(b"\r\n", b"\n"))
        fixed += 1
    return fixed


def render(findings, root: Path, max_lines: int) -> str:
    lines = [f"# scan_hygiene.py — file hygiene report", "",
             f"- root: `{root}`", f"- line budget: {max_lines}", "",
             "| Check | Count | Meaning |", "|---|---|---|"]
    for k in CHECK_ORDER:
        lines.append(f"| {k} | {len(findings[k])} | {MEANING[k]} |")
    lines.append("")
    for k in CHECK_ORDER:
        items = findings[k]
        lines.append(f"## {k} ({len(items)})")
        lines.append("")
        if not items:
            lines.append("_none_")
            lines.append("")
            continue
        for it in items[:200]:
            lines.append(f"- `{it['file']}` — {it['detail']}")
        if len(items) > 200:
            lines.append(f"- … {len(items) - 200} more")
        lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="File hygiene scan (CRLF / mojibake / junk / line budget).")
    ap.add_argument("--root", default=".", help="project root (default: cwd)")
    ap.add_argument("--fix", action="store_true", help="rewrite CRLF files as LF in place")
    ap.add_argument("--max-lines", type=int, default=DEFAULT_BUDGET,
                    help=f"line budget (default {DEFAULT_BUDGET}); 0 disables the check")
    ap.add_argument("--allow", default="",
                    help="comma-separated files exempt from the line budget")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    ap.add_argument("--fail-on", default="",
                    help="comma-separated checks that cause exit code 1 (default: none)")
    ap.add_argument("--out", help="write the report to this file (LF endings)")
    args = ap.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: root not a directory: {root}", file=sys.stderr)
        return 2

    allow = {s.strip().replace("\\", "/") for s in args.allow.split(",") if s.strip()}
    max_lines = args.max_lines if args.max_lines > 0 else 10 ** 9

    findings = scan(root, max_lines, allow)

    if args.fix:
        n = fix_crlf(root, findings["crlf"])
        print(f"[fix] rewrote {n} file(s) as LF", file=sys.stderr)
        if n:
            findings = scan(root, max_lines, allow)

    payload = (json.dumps(findings, ensure_ascii=False, indent=2)
               if args.json else render(findings, root, max_lines))

    if args.out:
        with io.open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload + "\n")
    else:
        print(payload)

    fail_on = [s.strip() for s in args.fail_on.split(",") if s.strip()]
    for k in fail_on:
        if k not in CHECK_ORDER:
            print(f"error: unknown check in --fail-on: {k}", file=sys.stderr)
            return 2
        if findings.get(k):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
