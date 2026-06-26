#!/usr/bin/env python3
"""
notes-know-you helper: sync Evernote and export all notebooks to ENEX files.

Usage:
    python sync_export.py <db_path> <enex_output_dir> [--backend china|evernote] [--token TOKEN]

Exit codes:
    0  success
    2  rate limited (wait 25-30 min and retry)
    3  auth error (need to reauth)
    1  other error
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], label: str) -> subprocess.CompletedProcess:
    print(f"[notes-know-you] {label}...")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result


def sync(db_path: str) -> None:
    result = run(
        ["python", "-m", "evernote_backup", "sync", "-d", db_path],
        "Syncing from Evernote",
    )
    if result.returncode != 0:
        stderr = result.stderr or ""
        if "Rate limit" in stderr or "rate limit" in stderr:
            print("[notes-know-you] ERROR: Rate limit reached. Wait 25-30 minutes and retry.", file=sys.stderr)
            sys.exit(2)
        if "auth" in stderr.lower() or "token" in stderr.lower() or "login" in stderr.lower():
            print("[notes-know-you] ERROR: Authentication failed. Run reauth with your developer token.", file=sys.stderr)
            sys.exit(3)
        print(f"[notes-know-you] ERROR: sync failed (exit {result.returncode})", file=sys.stderr)
        sys.exit(1)


def export(db_path: str, enex_dir: str) -> None:
    Path(enex_dir).mkdir(parents=True, exist_ok=True)
    result = run(
        ["python", "-m", "evernote_backup", "export", "-d", db_path, enex_dir],
        f"Exporting notebooks to {enex_dir}",
    )
    if result.returncode != 0:
        print(f"[notes-know-you] ERROR: export failed (exit {result.returncode})", file=sys.stderr)
        sys.exit(1)


def list_enex_files(enex_dir: str) -> list[Path]:
    return sorted(Path(enex_dir).rglob("*.enex"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Evernote and export all notebooks.")
    parser.add_argument("db_path", help="Path to evernote-backup database")
    parser.add_argument("enex_output_dir", help="Directory to export ENEX files into")
    parser.add_argument("--skip-sync", action="store_true", help="Skip sync, only export")
    args = parser.parse_args()

    if not args.skip_sync:
        sync(args.db_path)

    export(args.db_path, args.enex_output_dir)

    enex_files = list_enex_files(args.enex_output_dir)
    print(f"\n[notes-know-you] Exported {len(enex_files)} notebook(s):")
    for f in enex_files:
        print(f"  {f}")


if __name__ == "__main__":
    main()
