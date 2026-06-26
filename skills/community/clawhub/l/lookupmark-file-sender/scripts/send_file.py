#!/usr/bin/env python3
"""Send a local file to a chat channel via OpenClaw CLI.

Usage:
    send_file.py <file_path> --target <dest> [--channel telegram] [--force-document]

Security note: Behavioral controls are in SKILL.md and SOUL.md.
This script does NOT block files — the agent decides based on context.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time

WORKSPACE = os.path.realpath(os.path.expanduser("~/.openclaw/workspace"))
TEMP_SEND_DIR = os.path.join(WORKSPACE, ".tmp-send")
MAX_RETRIES = 3
RETRY_BACKOFF = [2, 5, 10]  # seconds


def resolve_path(path: str) -> str:
    return os.path.realpath(os.path.expanduser(path))


def stage_file(resolved: str) -> tuple[str, str | None]:
    """Stage file into workspace .tmp-send if outside it.
    openclaw only allows media paths under the workspace directory.
    Returns (staged_path, staged_dir or None)."""
    if os.path.commonpath([resolved, WORKSPACE]) == WORKSPACE:
        return resolved, None
    os.makedirs(TEMP_SEND_DIR, exist_ok=True)
    staged = os.path.join(TEMP_SEND_DIR, os.path.basename(resolved))
    shutil.copy2(resolved, staged)
    return staged, TEMP_SEND_DIR


def cleanup(send_path: str, original: str, staged_dir: str | None):
    """Remove staged files after send."""
    if send_path != original and os.path.exists(send_path):
        try:
            os.remove(send_path)
        except OSError:
            pass
    if staged_dir and os.path.isdir(staged_dir):
        try:
            if not os.listdir(staged_dir):
                os.rmdir(staged_dir)
        except OSError:
            pass


def send_file(file_path: str, target: str, channel: str = "telegram",
              force_document: bool = False) -> dict:
    resolved = resolve_path(file_path)

    if not os.path.exists(resolved):
        return {"error": f"File not found: {resolved}"}
    if not os.path.isfile(resolved):
        return {"error": f"Not a file: {resolved}"}
    if not os.access(resolved, os.R_OK):
        return {"error": f"Permission denied: {resolved}"}

    size_mb = os.path.getsize(resolved) / (1024 * 1024)
    if size_mb > 50:
        return {"error": f"File too large ({size_mb:.1f} MB). Telegram limit is 50 MB."}

    send_path, staged_dir = stage_file(resolved)

    cmd = [
        "openclaw", "message", "send",
        "--channel", channel,
        "--target", target,
        "--media", send_path,
    ]
    if force_document:
        cmd.append("--force-document")

    # Retry with exponential backoff
    last_error = None
    result = None
    for attempt in range(MAX_RETRIES):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                break
            last_error = f"openclaw returned {result.returncode}: {result.stderr.strip()}"
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF[attempt])
        except subprocess.TimeoutExpired:
            last_error = "openclaw timed out"
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF[attempt])

    cleanup(send_path, resolved, staged_dir)

    if result is None or result.returncode != 0:
        return {
            "file": resolved, "size_mb": round(size_mb, 2),
            "channel": channel, "target": target,
            "error": f"Failed after {MAX_RETRIES} attempts: {last_error}",
        }

    return {
        "file": resolved,
        "size_mb": round(size_mb, 2),
        "channel": channel,
        "target": target,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main():
    parser = argparse.ArgumentParser(description="Send a file via OpenClaw")
    parser.add_argument("file", help="Path to the file to send")
    parser.add_argument("--target", required=True)
    parser.add_argument("--channel", default="telegram")
    parser.add_argument("--force-document", action="store_true")
    args = parser.parse_args()

    result = send_file(args.file, args.target, args.channel, args.force_document)

    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Sent {result['file']} ({result['size_mb']} MB) via {result['channel']} to {result['target']}")


if __name__ == "__main__":
    main()
