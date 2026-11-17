#!/usr/bin/env python3
"""Create and find branch-scoped Codex session handshake files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


def run_git(cwd: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def project_root(cwd: Path) -> Path:
    git_root = run_git(cwd, ["rev-parse", "--show-toplevel"])
    if git_root:
        return Path(git_root).resolve()
    return cwd.resolve()


def branch_name(root: Path) -> str | None:
    return run_git(root, ["branch", "--show-current"])


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-._").lower()
    return slug or "project"


def project_key(root: Path) -> str:
    digest = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:10]
    return f"{slugify(root.name)}-{digest}"


def handshake_dir(root: Path) -> Path:
    base = os.environ.get("CODEX_SESSION_HANDSHAKE_DIR")
    if base:
        return Path(base).expanduser() / project_key(root)
    return Path.home() / "codex-session-handshakes" / project_key(root)


def handshake_path(root: Path) -> Path:
    branch = slugify(branch_name(root) or "no-branch")
    return handshake_dir(root) / f"handshake-{branch}.md"


def metadata(root: Path, mode: str) -> dict[str, str | None]:
    return {
        "mode": mode,
        "project": str(root),
        "project_key": project_key(root),
        "branch": branch_name(root),
        "handshake_dir": str(handshake_dir(root)),
    }


def do_open(cwd: Path) -> None:
    root = project_root(cwd)
    found = handshake_path(root)
    payload = metadata(root, "open")
    payload["handshake"] = str(found) if found.is_file() else None
    print(json.dumps(payload, indent=2))


def do_close(cwd: Path) -> None:
    root = project_root(cwd)
    directory = handshake_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    payload = metadata(root, "close")
    payload["handshake"] = str(handshake_path(root))
    print(json.dumps(payload, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["open", "close"])
    parser.add_argument("--cwd", default=os.getcwd())
    args = parser.parse_args()

    cwd = Path(args.cwd).expanduser().resolve()
    if args.mode == "open":
        do_open(cwd)
    else:
        do_close(cwd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
