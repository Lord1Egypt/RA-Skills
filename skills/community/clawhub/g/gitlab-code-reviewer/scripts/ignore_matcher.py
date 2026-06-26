#!/usr/bin/env python3
"""
File ignore matcher for MR diff filtering.

Usage:
    python ignore_matcher.py <file_path> [<pattern1> <pattern2> ...]

Reads ignore_patterns from ~/.openclaw/credentials/gitlab.json,
then merges with built-in defaults and any extra patterns provided on the CLI.

Exits 0 if the file should be IGNORED, exits 1 if it should be REVIEWED.
Prints "IGNORE" or "REVIEW" to stdout.

Importable API:
    from ignore_matcher import should_ignore
    should_ignore("src/main/App.java")         # False  -> review
    should_ignore("package-lock.json")         # True   -> ignore
"""

import fnmatch
import json
import sys
from pathlib import Path


CREDS_PATH = Path.home() / ".openclaw" / "credentials" / "gitlab.json"

DEFAULT_IGNORE_PATTERNS = [
    "*.min.js",
    "*.min.css",
    "*.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "forms/*.json",
]

# Binary / generated file extensions always skipped
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".ico",
    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".woff", ".woff2", ".ttf", ".eot",
    ".class", ".jar", ".war", ".ear",
    ".exe", ".dll", ".so", ".dylib",
    ".pyc", ".pyo",
    ".map",  # source maps
}


def _load_credential_patterns() -> list[str]:
    if not CREDS_PATH.exists():
        return []
    try:
        with open(CREDS_PATH) as f:
            creds = json.load(f)
        return creds.get("ignore_patterns", [])
    except Exception:
        return []


def build_patterns(extra: list[str] | None = None) -> list[str]:
    """Merge default + credential + extra patterns, deduplicated, order preserved."""
    seen = set()
    patterns = []
    for p in DEFAULT_IGNORE_PATTERNS + _load_credential_patterns() + (extra or []):
        if p not in seen:
            seen.add(p)
            patterns.append(p)
    return patterns


def should_ignore(file_path: str, extra_patterns: list[str] | None = None) -> bool:
    """
    Return True if file_path matches any ignore pattern or has a binary extension.
    Matching is done against the full path, basename, and all path suffixes
    (e.g. "forms/file.json", "resources/forms/file.json") so that patterns like
    "forms/*.json" correctly match deep paths such as
    "task-service/src/main/resources/forms/file.json".
    """
    path = Path(file_path)

    # Binary extension check
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True

    patterns = build_patterns(extra_patterns)

    # Build candidates: full path, all trailing sub-paths, and basename.
    # Normalise separators to forward slash for consistent fnmatch behaviour.
    normalised = file_path.replace("\\", "/")
    parts = normalised.split("/")
    candidates = ["/".join(parts[i:]) for i in range(len(parts))]  # includes full path and basename

    for pattern in patterns:
        for candidate in candidates:
            if fnmatch.fnmatch(candidate, pattern):
                return True
    return False


def filter_diffs(diffs: list[dict], extra_patterns: list[str] | None = None) -> list[dict]:
    """
    Filter a list of diff objects (as returned by gitlab_client.fetch_diff).
    Returns only entries that should be reviewed.
    Uses new_path for matching; falls back to old_path for deleted files.
    """
    result = []
    for d in diffs:
        path = d.get("new_path") or d.get("old_path", "")
        if not should_ignore(path, extra_patterns):
            result.append(d)
    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    file_path = sys.argv[1]
    extra = sys.argv[2:] if len(sys.argv) > 2 else None

    if should_ignore(file_path, extra):
        print("IGNORE")
        sys.exit(0)
    else:
        print("REVIEW")
        sys.exit(1)


if __name__ == "__main__":
    main()
