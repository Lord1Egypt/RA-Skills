#!/usr/bin/env python3
"""Create a lightweight repository audit snapshot.

The snapshot avoids reading source bodies. It reports intent docs, config files,
git status/diff stats, and high-risk paths so the auditor can load context
selectively.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
from pathlib import Path
from typing import List, Optional


INTENT_NAMES = {
    "AGENTS.md",
    "README.md",
    "README.rst",
    "README.txt",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "ARCHITECTURE.md",
}
CONFIG_NAMES = {
    "pyproject.toml",
    "package.json",
    "requirements.txt",
    "go.mod",
    "Cargo.toml",
    "pytest.ini",
    "tox.ini",
    "Dockerfile",
}
RISK_TERMS = (
    "auth",
    "permission",
    "role",
    "tenant",
    "route",
    "api",
    "server",
    "db",
    "migration",
    "upload",
    "import",
    "export",
    "path",
    "file",
    "storage",
    "archive",
    "llm",
    "network",
    "secret",
    "audit",
)
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".codex",
    ".clawhub",
    ".agenthub",
    "build",
    "coverage",
    "data",
    "dist",
    "portable",
}


def run_git(root: Path, args: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode in (0, 1) else None


def load_ignore_patterns(root: Path, extra_patterns: Optional[List[str]] = None) -> List[str]:
    patterns = list(extra_patterns or [])
    ignore_file = root / ".auditignore"
    if ignore_file.exists():
        for raw_line in ignore_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def ignored_by_pattern(relative: str, patterns: List[str]) -> bool:
    normalized = relative.replace("\\", "/")
    parts = normalized.split("/")
    for pattern in patterns:
        pat = pattern.replace("\\", "/").strip()
        if not pat:
            continue
        if pat.endswith("/") and (
            normalized == pat.rstrip("/") or normalized.startswith(pat.rstrip("/") + "/")
        ):
            return True
        if "/" not in pat and any(fnmatch.fnmatch(part, pat) for part in parts):
            return True
        if fnmatch.fnmatch(normalized, pat):
            return True
    return False


def iter_files(root: Path, limit: int, ignore_patterns: List[str]) -> List[str]:
    files: List[str] = []
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        rel_dir = current_path.relative_to(root).as_posix()
        if rel_dir == ".":
            rel_dir = ""

        kept_dirs = []
        for dirname in dirnames:
            rel_child = f"{rel_dir}/{dirname}" if rel_dir else dirname
            if dirname in SKIP_DIRS or ignored_by_pattern(rel_child, ignore_patterns):
                continue
            kept_dirs.append(dirname)
        dirnames[:] = kept_dirs

        for filename in filenames:
            if len(files) >= limit:
                return files
            relative = f"{rel_dir}/{filename}" if rel_dir else filename
            if ignored_by_pattern(relative, ignore_patterns):
                continue
            files.append(relative)
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true", help="Emit JSON; default is text.")
    parser.add_argument("--file-limit", type=int, default=5000)
    parser.add_argument(
        "--skip",
        action="append",
        default=[],
        help="Additional .auditignore-style pattern. Can be repeated.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    ignore_patterns = load_ignore_patterns(root, args.skip)
    files = iter_files(root, args.file_limit, ignore_patterns)
    lower_pairs = [(f, Path(f).name.lower()) for f in files]

    intent = [
        f
        for f, name in lower_pairs
        if Path(f).name in INTENT_NAMES or f.startswith("docs/")
    ]
    config = [f for f, _ in lower_pairs if Path(f).name in CONFIG_NAMES or f.startswith(".github/")]
    tests = [f for f, _ in lower_pairs if f.startswith("tests/") or "/test" in f or f.endswith("_test.py")]
    risky = [f for f, _ in lower_pairs if any(term in f.lower() for term in RISK_TERMS)]

    snapshot = {
        "root": str(root),
        "intent_files": sorted(intent)[:80],
        "config_files": sorted(config)[:80],
        "test_files_sample": sorted(tests)[:120],
        "high_risk_paths_sample": sorted(risky)[:160],
        "git_branch": run_git(root, ["branch", "--show-current"]),
        "git_status_short": (run_git(root, ["status", "--short"]) or "").splitlines()[:200],
        "git_diff_stat": (run_git(root, ["diff", "--stat"]) or "").splitlines()[:120],
        "file_count_seen": len(files),
        "file_limit": args.file_limit,
        "auditignore_patterns": ignore_patterns,
    }

    if args.json:
        print(json.dumps(snapshot, indent=2, sort_keys=True))
    else:
        for key, value in snapshot.items():
            print(f"{key}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  {item}")
            else:
                print(f"  {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
