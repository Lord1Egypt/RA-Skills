#!/usr/bin/env python3
"""Persist a ShiyunApi key as SHIYUN_API_KEY.

This script is intended for use by the shiyunapi-image-generation skill when the
user explicitly provides an API key. It avoids printing the key and stores it in
an OS-appropriate user environment location.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

ENV_NAME = "SHIYUN_API_KEY"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Persist SHIYUN_API_KEY for ShiyunApi calls.")
    parser.add_argument("--api-key", default=None, help="ShiyunApi key provided by the user.")
    parser.add_argument("--api-key-stdin", action="store_true", help="Read the API key from stdin instead of an argument.")
    parser.add_argument(
        "--scope",
        choices=("user", "process"),
        default="user",
        help="Persist to user environment when possible, or only current process. Default: user.",
    )
    return parser.parse_args()


def fail(message: str, exit_code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def validate_api_key(api_key: str) -> str:
    key = api_key.strip()
    if not key:
        fail("API key is empty.")
    if re.search(r"\s", key):
        fail("API key contains whitespace; please provide the raw key only.")
    if len(key) < 8:
        fail("API key looks too short; please verify it before saving.")
    return key


def save_windows_user_env(api_key: str) -> None:
    command = ["setx", ENV_NAME, api_key]
    result = subprocess.run(command, capture_output=True, text=True, shell=False)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "setx failed").strip()
        fail(f"Failed to persist Windows user environment variable: {message}")


def shell_quote_single(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def upsert_line(path: Path, line_prefix: str, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = ""
    if path.exists():
        existing = path.read_text(encoding="utf-8", errors="replace")
    lines = [item for item in existing.splitlines() if not item.strip().startswith(line_prefix)]
    lines.append(line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_posix_user_env(api_key: str) -> Path:
    shell = os.environ.get("SHELL", "")
    home = Path.home()
    if shell.endswith("zsh"):
        target = home / ".zshrc"
    elif shell.endswith("fish"):
        target = home / ".config" / "fish" / "config.fish"
        line = f"set -gx {ENV_NAME} {shell_quote_single(api_key)}"
        upsert_line(target, f"set -gx {ENV_NAME}", line)
        return target
    else:
        target = home / ".bashrc"
    line = f"export {ENV_NAME}={shell_quote_single(api_key)}"
    upsert_line(target, f"export {ENV_NAME}=", line)
    return target


def main() -> None:
    args = parse_args()
    raw_api_key = sys.stdin.read().strip() if args.api_key_stdin else args.api_key
    if raw_api_key is None:
        fail("Missing API key. Pass --api-key or use --api-key-stdin.")
    api_key = validate_api_key(raw_api_key)
    os.environ[ENV_NAME] = api_key

    persistence_target = "current process only"
    if args.scope == "user":
        if platform.system().lower() == "windows":
            save_windows_user_env(api_key)
            persistence_target = "Windows user environment via setx"
        else:
            path = save_posix_user_env(api_key)
            persistence_target = str(path)

    summary = {
        "saved": True,
        "env_name": ENV_NAME,
        "persistence": persistence_target,
        "note": "API key value is intentionally not printed. Restart shells or WorkBuddy if a future session cannot see the updated environment.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
