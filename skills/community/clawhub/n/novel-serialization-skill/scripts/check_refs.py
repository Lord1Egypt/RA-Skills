#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_refs.py —— 引用完整性体检（七档判定）。

The rule
--------
    **Release files may only reference release files.**
    **Non-release files may reference anything.**

A "release" file is one that ships: `SKILL.md`, `README.md`, `modules/`,
`references/`, `scripts/`, `.github/`. A "non-release" file lives in a private
work area — `notes-personal/`, `_trash/`, `.workbuddy/` (reports, memory,
ad-hoc scripts). Reports and working notes legitimately need to point at drafts
and private ledgers; shipped documentation must not point at something the
reader cannot open.

Why this exists
---------------
Long-running serialisation projects accumulate Markdown files that reference
each other by relative path. A file that is renamed, moved or retired leaves
behind dangling references that no linter catches, because they are plain text
inside prose. This script classifies every reference into one of eight buckets so
that a maintainer can triage rather than eyeball.

Buckets (same vocabulary as the -1928 subproject's field tooling)
----------------------------------------------------------------
OK          Target exists and lives inside the release tree.
LOCAL       Real link ``[x](y)`` resolving to an existing file outside the
            release tree as currently configured — recorded for audit.
TEMPLATE    Placeholder path, never meant to resolve (``角色名.md``,
            ``{name}.md``, ``<path>``, ``tools/xxx.py``).
BARE        Path written inside backticks. Backtick paths are documentation,
            not links, and are resolved from the repository root — listed, not
            judged.
PRIVATE_OK  Target sits in a private work area **and the referencing file is
            itself non-release**. Allowed by the rule above.
NONRELEASE  Target sits in a private work area **and the referencing file is
            release**. This is the violation: shipped docs must not point at
            files the reader cannot open.
MISSING          Target does not exist, and the referencing file is release.
                This is a defect: a shipped document points at nothing.
PRIVATE_MISSING  Target does not exist, and the referencing file is a report
                or working note. Expected — those were written about another
                tree — so it is listed but never gated on.

Two systems, never mixed
------------------------
* Backtick paths  -> resolved from the repository root.
* Real links ``[x](y)`` -> resolved relative to the file that contains them.

Rewriting one using the other's convention silently corrupts the tree. This
script keeps them apart on purpose.

Usage
-----
    python scripts/check_refs.py --root .                 # human report
    python scripts/check_refs.py --root . --json          # machine readable
    python scripts/check_refs.py --root . --kind MISSING  # only one bucket
    python scripts/check_refs.py --root . --fail-on MISSING,NONRELEASE
    python scripts/check_refs.py --root . --ignore-file ''  # exemptions off

Exemptions
----------
Paths that are *described* but do not exist in this repository — subproject
state files, example manuscripts, paths written from a subproject's point of
view — are listed in ``.refsignore``, one regex per line. The same file is
read locally, in pre-commit and in CI, so the three cannot disagree.

Exit codes
----------
0  clean (or nothing matched --fail-on)
1  findings in a bucket listed by --fail-on
2  usage / IO error

LF-only writes: every file this script writes uses ``newline='\\n'``.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

# Scanned as sources unless excluded. `.workbuddy/` is NOT excluded by default:
# reports and working notes are non-release sources, and their references to
# private files must be allowed rather than flagged.
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}

# Exemption patterns live here, not in a CI flag, so that a local run, the
# pre-commit hook and CI all judge the same tree. See .refsignore.
DEFAULT_IGNORE_FILE = ".refsignore"

# Directories whose contents are real files but must never be referenced from
# released content.
NONRELEASE_DIRS = ("notes-personal", "_trash", "_drafts", "drafts", ".workbuddy")

# Path shapes that are documentation placeholders, never real targets.
TEMPLATE_PATTERNS = (
    re.compile(r"^\{[^{}]+\}"),          # {name}.md
    re.compile(r"^<[^>]+>"),             # <path>
    re.compile(r"^[A-Z_]+$"),            # PLACEHOLDER
)
TEMPLATE_NAMES = {
    "角色名.md", "群体名.md", "章节名.md", "文件名.md", "xxx.py", "yyy.md",
    "tools/xxx.py", "path/to/file.md", "your-file.md",
}

# Markdown link: [text](target) — image syntax skipped.
LINK_RE = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^()\s]+)\)")
# Backtick-quoted path-ish token (Chinese and ASCII both allowed).
BACKTICK_RE = re.compile(r"`([^`\n]+)`")

# A backtick token is only treated as a path when it looks like one.
PATHISH_RE = re.compile(r"^[\w\-./\\一-鿿]+\.(md|py|yml|yaml|json|txt|sh)$", re.UNICODE)

SEVERITY_ORDER = ["OK", "LOCAL", "TEMPLATE", "BARE", "PRIVATE_OK", "NONRELEASE",
                 "MISSING", "PRIVATE_MISSING"]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def is_template(target: str) -> bool:
    t = target.strip()
    if t in TEMPLATE_NAMES:
        return True
    if any(p.match(t) for p in TEMPLATE_PATTERNS):
        return True
    if "{" in t or "<" in t or "*" in t:
        return True
    return False


def in_nonrelease(rel: str) -> bool:
    parts = rel.replace("\\", "/").split("/")
    return any(p in NONRELEASE_DIRS for p in parts)


def iter_markdown(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.lower().endswith(".md"):
                yield Path(dirpath) / name


def classify(target: str, source: Path, root: Path, released: set,
             src_release: bool = True) -> tuple:
    """Return (bucket, resolved_relative_path_or_None).

    ``src_release`` applies the rule: a release file may only point at release
    files. A non-release file (report, working note) may point at anything.
    """
    t = target.strip()
    if not t or t.startswith(("#", "mailto:", "tel:")):
        return None, None
    if t.startswith(("http://", "https://")):
        return None, None

    # Links are written URL-encoded (`README%20FOR%20AI.md`) but live on disk
    # decoded. Without this, every link into a filename with a space is a
    # false MISSING.
    t = unquote(t)
    # Strip the anchor; a heading fragment is not part of the path.
    t = t.split("#", 1)[0].strip()
    # A leading "/" is repo-root-absolute in GitHub-flavoured Markdown, not
    # filesystem-absolute.
    root_relative = t.startswith("/")
    if root_relative:
        t = t.lstrip("/")

    if is_template(t):
        return "TEMPLATE", t

    if in_nonrelease(t):
        if not src_release:
            return "PRIVATE_OK", t
        return "NONRELEASE", t

    # Real link: relative to the containing file, unless it was root-absolute.
    candidate = (root / t) if root_relative else (source.parent / t)
    candidate = candidate.resolve()
    try:
        rel = candidate.relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = None

    if candidate.exists():
        if rel in released:
            return "OK", rel
        return "LOCAL", rel or t
    return "MISSING", t


def classify_backtick(token: str, root: Path, released: set,
                      src_release: bool = True) -> tuple:
    t = unquote(token.strip())
    if t.startswith("/"):
        t = t.lstrip("/")
    if not PATHISH_RE.match(t) or is_template(t):
        return None, None
    if any(ch in t for ch in (" ", "　")):
        return None, None
    if in_nonrelease(t):
        return ("NONRELEASE" if src_release else "PRIVATE_OK"), t
    candidate = (root / t)
    if candidate.exists():
        try:
            rel = candidate.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            rel = t
        return ("OK" if rel in released else "LOCAL"), rel
    return "MISSING", t


# --------------------------------------------------------------------------
# Core
# --------------------------------------------------------------------------

def load_ignore_file(root: Path, name: str) -> list:
    """Read exemption patterns from ``root/name``; return the pattern list.

    Blank lines and ``#`` comments are ignored, so the file can explain why
    each pattern exists. Keeping the exemptions in a file rather than in a CI
    flag means the same list applies locally, in pre-commit and in CI.
    """
    if not name:
        return []
    p = root / name
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def build_ignore(root: Path, cli_patterns: list, ignore_file: str) -> "re.Pattern | None":
    patterns = cli_patterns + load_ignore_file(root, ignore_file)
    if not patterns:
        return None
    try:
        return re.compile("|".join(patterns))
    except re.error as exc:
        raise SystemExit(f"error: bad ignore pattern: {exc}")


def scan(root: Path, ignore_re=None):
    root = root.resolve()
    # Release tree = everything tracked-ish that is not a private area.
    released = set()
    for p in iter_markdown(root):
        try:
            rel = p.resolve().relative_to(root).as_posix()
        except ValueError:
            continue
        if not in_nonrelease(rel):
            released.add(rel)

    findings = {k: [] for k in SEVERITY_ORDER}
    for p in iter_markdown(root):
        try:
            rel = p.resolve().relative_to(root).as_posix()
        except ValueError:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"[warn] unreadable: {rel} ({exc})", file=sys.stderr)
            continue

        # The rule: a release file may only reference release files.
        src_release = not in_nonrelease(rel)

        seen = set()
        for target in LINK_RE.findall(text):
            if ignore_re is not None and ignore_re.search(target):
                continue
            bucket, resolved = classify(target, p, root, released, src_release)
            if bucket is None:
                continue
            if bucket == "MISSING" and not src_release:
                # A report or working note pointing at something that is not
                # here is expected — it was written about a different tree.
                bucket = "PRIVATE_MISSING"
            key = (bucket, resolved)
            if key in seen:
                continue
            seen.add(key)
            findings[bucket].append({"file": rel, "target": target, "resolved": resolved})

        for token in BACKTICK_RE.findall(text):
            if ignore_re is not None and ignore_re.search(token):
                continue
            if "/" not in token and "\\" not in token:
                continue
            bucket, resolved = classify_backtick(token, root, released, src_release)
            if bucket is None:
                continue
            # Backtick paths are documentation: record them in their own bucket.
            bucket = "BARE" if bucket in ("OK", "LOCAL") else bucket
            if bucket == "MISSING" and not src_release:
                bucket = "PRIVATE_MISSING"
            key = (bucket, resolved)
            if key in seen:
                continue
            seen.add(key)
            findings[bucket].append({"file": rel, "target": token, "resolved": resolved})

    return findings


def render(findings, root: Path) -> str:
    lines = []
    lines.append("# check_refs.py — reference integrity report")
    lines.append("")
    lines.append(f"- root: `{root}`")
    lines.append("")
    lines.append("| Bucket | Count | Meaning |")
    lines.append("|---|---|---|")
    meaning = {
        "OK": "target exists inside the release tree",
        "LOCAL": "target exists but is outside the release tree",
        "TEMPLATE": "placeholder path, never meant to resolve",
        "BARE": "backtick path (documentation, root-relative)",
        "PRIVATE_OK": "private target, referenced from a non-release file — allowed",
        "NONRELEASE": "private target, referenced from a RELEASE file — must be fixed",
        "MISSING": "target does not exist, and the source is a release file",
        "PRIVATE_MISSING": "target does not exist; source is a report or working note",
    }
    for b in SEVERITY_ORDER:
        lines.append(f"| {b} | {len(findings[b])} | {meaning[b]} |")
    lines.append("")
    lines.append("> Rule: release files reference release files only; "
                 "non-release files may reference anything.")
    lines.append("")
    for b in ("NONRELEASE", "MISSING"):
        items = findings[b]
        lines.append(f"## {b} ({len(items)})")
        lines.append("")
        if not items:
            lines.append("_none_")
            lines.append("")
            continue
        for it in items:
            lines.append(f"- `{it['file']}` -> `{it['target']}`")
        lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Reference integrity check (eight buckets).")
    ap.add_argument("--root", default=".", help="project root (default: cwd)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    ap.add_argument("--kind", action="append", choices=SEVERITY_ORDER,
                    help="restrict output to a bucket (repeatable)")
    ap.add_argument("--fail-on", default="",
                    help="comma-separated buckets that cause exit code 1 (e.g. MISSING,NONRELEASE)")
    ap.add_argument("--out", help="write the report to this file (LF endings)")
    ap.add_argument("--ignore", default="",
                    help="regex; reference targets matching it are skipped "
                         "(e.g. '^state/|^worldbuilding/' to exempt described-but-absent paths)")
    ap.add_argument("--ignore-file", default=DEFAULT_IGNORE_FILE,
                    help=f"file of exemption patterns, one regex per line, '#' comments "
                         f"allowed (default: {DEFAULT_IGNORE_FILE}; '' disables)")
    args = ap.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: root not a directory: {root}", file=sys.stderr)
        return 2

    cli = [args.ignore.strip()] if args.ignore.strip() else []
    ignore_re = build_ignore(root, cli, args.ignore_file)
    findings = scan(root, ignore_re)

    if args.kind:
        keep = set(args.kind)
        findings = {k: v for k, v in findings.items() if k in keep}

    if args.json:
        payload = json.dumps(findings, ensure_ascii=False, indent=2)
    else:
        payload = render(findings, root)

    if args.out:
        with io.open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload + "\n")
    else:
        print(payload)

    fail_on = {s.strip() for s in args.fail_on.split(",") if s.strip()}
    for b in fail_on:
        if b not in SEVERITY_ORDER:
            print(f"error: unknown bucket in --fail-on: {b}", file=sys.stderr)
            return 2
        if findings.get(b):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
