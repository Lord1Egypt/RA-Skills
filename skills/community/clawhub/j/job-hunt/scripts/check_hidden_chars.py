#!/usr/bin/env python3
"""Whether the shipped tree is free of invisible and BiDi control characters.

A static review of this skill flagged U+00AD in `check_pages.py` and U+202B /
U+202C in a `render_cv.py` comment. Both were legitimate in intent — a hyphen
class that has to ignore the hyphen LaTeX inserts at a line break, and a comment
quoting the Arabic that pdftotext actually returned — and that is the reason this
gate is mechanical rather than a judgement call.

WHY IT MATTERS ANYWAY. U+202E and its siblings change the order a reader sees
without changing what the interpreter reads, so a line can display as one thing
and parse as another (Trojan Source, CVE-2021-42574). U+00AD and the zero-width
family are the same gap in the other direction: a character nobody can see,
inside an identifier, a URL or a regex. This repo asks an agent to read its own
source and documentation and act on them, so a line that reads differently to
the reader than to the machine is a correctness problem here, not only a supply
chain one.

THE REMEDY IS ESCAPE OR REMOVE, NOT DELETE-AND-HOPE. `\\xad` in a regex is the
same pattern with nothing invisible in the file. A comment that needed BiDi
controls to display correctly says so in words instead. There is deliberately no
allowlist: a waiver file is how the next one gets in, and the gate's own fixtures
are built from `chr(cp)` at runtime so it never needs one.

In a Git checkout, scan tracked files and non-ignored untracked files. Ignored
local archives are not shipped source; tracked files remain in scope even when
an ignore rule matches them. Without Git metadata, scan the exported tree using
the same directory and binary-file exclusions. A Git listing failure is an
incomplete check, never permission to report a clean scan.

Exit 0 = nothing found. 1 = findings on stdout, one per line. 2 = could not run,
which includes finding no files to read at all — 0 findings over 0 files is how a
gate goes green after a path change.

A REPO-LEVEL CHECK, NOT A WORKSPACE GATE. It takes no --workspace, imports no
journal and writes no receipt, because it reads files that live in this repo
rather than artifacts that live in a user's run; a receipt would be bookkeeping
about nobody. This is the same named exception check_skill_lossless.py and
check_conventions.py --ci carry. The exit codes are the shared ones, so CI and a
local run cannot disagree about a file.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import cli_io  # noqa: E402

try:
    import paths  # noqa: E402
    DEFAULT_ROOT = paths.SKILL_ROOT
except Exception:  # pragma: no cover - paths is part of this repo
    DEFAULT_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Named, not a bare codepoint list, because a finding has to be readable by the
# person who has to decide what to do about it.
TARGETS = {
    0x00AD: "SOFT HYPHEN",
    0x061C: "ARABIC LETTER MARK",
    0x200B: "ZERO WIDTH SPACE",
    0x200C: "ZERO WIDTH NON-JOINER",
    0x200D: "ZERO WIDTH JOINER",
    0x200E: "LEFT-TO-RIGHT MARK",
    0x200F: "RIGHT-TO-LEFT MARK",
    0x202A: "LEFT-TO-RIGHT EMBEDDING",
    0x202B: "RIGHT-TO-LEFT EMBEDDING",
    0x202C: "POP DIRECTIONAL FORMATTING",
    0x202D: "LEFT-TO-RIGHT OVERRIDE",
    0x202E: "RIGHT-TO-LEFT OVERRIDE",
    0x2060: "WORD JOINER",
    0x2066: "LEFT-TO-RIGHT ISOLATE",
    0x2067: "RIGHT-TO-LEFT ISOLATE",
    0x2068: "FIRST STRONG ISOLATE",
    0x2069: "POP DIRECTIONAL ISOLATE",
    0xFEFF: "ZERO WIDTH NO-BREAK SPACE",
}
# U+E0000..U+E007F: the tag block, which encodes ASCII invisibly and is the
# newer form of the same trick. Matched by range rather than listed.
TAG_RANGE = range(0xE0000, 0xE0080)

# U+00A0 is deliberately NOT a target. It is visible as a space, this repo's
# own prose uses it (`8 × H200`), and a gate that fires on correct input is one
# someone eventually switches off.

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv",
             ".mypy_cache", ".ruff_cache", "dist", "build"}
# Extension-based, because sniffing content would have to decode the file first,
# which is the thing that fails on a binary.
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".tiff",
    ".pdf", ".zip", ".gz", ".tgz", ".bz2", ".xz", ".7z",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".docx", ".xlsx", ".pptx", ".odt", ".mp3", ".mp4", ".wav", ".mov",
    ".pyc", ".pyo", ".so", ".dylib", ".dll", ".exe", ".bin",
}


def describe(cp: int) -> str:
    if cp in TARGETS:
        return TARGETS[cp]
    return unicodedata.name(chr(cp), "TAG CHARACTER" if cp in TAG_RANGE else "UNNAMED")


def is_target(cp: int) -> bool:
    return cp in TARGETS or cp in TAG_RANGE


def scan_text(text: str):
    """(line, col, codepoint) for every target character. 1-based, like an editor."""
    for lineno, line in enumerate(text.splitlines(), 1):
        for col, ch in enumerate(line, 1):
            if is_target(ord(ch)):
                yield lineno, col, ord(ch)


def candidate_files(root: pathlib.Path):
    resolved = root.resolve()
    if any((parent / ".git").exists() for parent in (resolved, *resolved.parents)):
        listing = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
             "--exclude-standard", "--"], stderr=subprocess.PIPE, timeout=30)
        candidates = (root / os.fsdecode(name) for name in listing.split(b"\0") if name)
    else:
        candidates = root.rglob("*")
    for path in sorted(set(candidates)):
        if path.is_symlink() or not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() in BINARY_SUFFIXES:
            continue
        yield path


def main(argv: list[str] | None = None) -> int:
    cli_io.configure_output()
    ap = argparse.ArgumentParser(
        description="Find invisible and BiDi control characters in source and docs.")
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT,
                    help="tree to scan (default: the skill root)")
    args = ap.parse_args(argv)

    root = args.root
    if not root.is_dir():
        print(f"NO_INPUT: {root} is not a directory", file=sys.stderr)
        return 2

    findings = 0
    scanned = 0
    unreadable = []
    try:
        files = list(candidate_files(root))
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"SCAN_FAILED: could not select source files ({exc})", file=sys.stderr)
        return 2
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            unreadable.append((path.relative_to(root), exc.__class__.__name__))
            continue
        scanned += 1
        for lineno, col, cp in scan_text(text):
            findings += 1
            print(f"HIDDEN_CHAR: {path.relative_to(root)}:{lineno}:{col} "
                  f"U+{cp:04X} {describe(cp)}")

    for rel, why in unreadable:
        print(f"UNREADABLE: {rel} could not be decoded as UTF-8 ({why}); not scanned",
              file=sys.stderr)

    if scanned == 0:
        print(f"NO_FILES: nothing to scan under {root} — 0 findings over 0 files is "
              "not a clean scan", file=sys.stderr)
        return 2

    if findings:
        print(f"{findings} hidden character(s) in {scanned} files scanned. Replace the "
              "literal with an escape, or remove it — there is no allowlist.",
              file=sys.stderr)
        return 1

    print(f"NO_HIDDEN_CHARS: {scanned} files scanned.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
