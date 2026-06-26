#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Sequence


FILENAME_RE = re.compile(r"(HEARTBEAT\.md|openclaw|feishu|lark|gateway|webhook|health)", re.I)
CONTENT_RE = re.compile(
    r"(@openclaw/feishu|channels\.feishu|connectionMode|verificationToken|heartbeat|HEARTBEAT_OK|HEARTBEAT\.md|/health|healthCheck|webhook|gateway|feishu|lark)",
    re.I,
)
LOG_RE = re.compile(r"(heartbeat|health|feishu|lark|HEARTBEAT_OK)", re.I)
IGNORE_DIRS = {".git", "node_modules", "dist", "build", ".next", "coverage", "__pycache__"}
TEXT_EXTS = {
    ".json",
    ".jsonc",
    ".md",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
    ".js",
    ".cjs",
    ".mjs",
    ".ts",
    ".tsx",
    ".sh",
    ".ps1",
    ".cmd",
    ".bat",
    ".log",
    ".py",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find OpenClaw/Feishu quota-burn candidates such as heartbeat settings, gateway files, webhook code, and health routes."
    )
    parser.add_argument("roots", nargs="*", help="Roots to scan")
    return parser.parse_args()


def add_root(roots: List[Path], candidate: Path) -> None:
    if candidate.is_dir():
        resolved = candidate.resolve()
        if resolved not in roots:
            roots.append(resolved)


def default_roots() -> List[Path]:
    roots: List[Path] = []
    home = Path.home()
    cwd = Path.cwd()
    for candidate in [
        cwd,
        home / ".openclaw",
        home / ".config" / "openclaw",
        home / "OpenClaw",
        home / "openclaw",
        home / "Documents",
        home / "Downloads",
    ]:
        add_root(roots, candidate)
    return roots


def should_skip_dir(dirname: str) -> bool:
    return dirname in IGNORE_DIRS


def iter_files(root: Path) -> Iterable[Path]:
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for filename in filenames:
            yield Path(current_root) / filename


def relabel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def looks_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS or path.name.lower() == "heartbeat.md"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def candidate_files(root: Path) -> List[str]:
    hits: List[str] = []
    for path in iter_files(root):
        if FILENAME_RE.search(path.name):
            hits.append(str(path))
            if len(hits) >= 80:
                break
    return hits


def content_hits(root: Path) -> List[str]:
    hits: List[str] = []
    for path in iter_files(root):
        if not looks_text_file(path):
            continue
        text = read_text(path)
        if not text:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if CONTENT_RE.search(line):
                hits.append("{}:{}:{}".format(path, lineno, line.strip()))
                if len(hits) >= 120:
                    return hits
    return hits


def log_hits(root: Path) -> List[str]:
    hits: List[str] = []
    for path in iter_files(root):
        if path.suffix.lower() != ".log":
            continue
        text = read_text(path)
        if not text:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if LOG_RE.search(line):
                hits.append("{}:{}:{}".format(path, lineno, line.strip()))
                if len(hits) >= 80:
                    return hits
    return hits


def print_section(title: str, lines: Sequence[str]) -> None:
    print(title)
    for line in lines:
        print(line)
    print()


def main() -> int:
    args = parse_args()
    roots: List[Path] = []

    if args.roots:
        for arg in args.roots:
            add_root(roots, Path(arg).expanduser())
    else:
        roots = default_roots()

    if not roots:
        print("No searchable directories found.")
        return 0

    print("Searching these roots:")
    for root in roots:
        print("  {}".format(root))
    print()

    for root in roots:
        print("== Root: {} ==".format(root))
        print()
        print_section("-- Candidate files --", candidate_files(root))
        print_section("-- Config/code lines --", content_hits(root))
        print_section("-- Repeated probe clues (logs only) --", log_hits(root))

    print("Next step:")
    print("  - If you see official Feishu plugin/config entries, tune heartbeat cost first.")
    print("  - If you see webhook or custom gateway health routes, patch /health so it does not invoke the model.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
