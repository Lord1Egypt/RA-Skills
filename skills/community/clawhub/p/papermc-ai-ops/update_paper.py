#!/usr/bin/env python3
"""
PaperMC Update Manager
Safe PaperMC jar updates with backup
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import urllib.request

SERVER_DIR = Path("/path/to/your/papermc-server")  # CHANGE THIS
JAR_BACKUP_DIR = SERVER_DIR / "jar_backup"
PAPER_JAR = SERVER_DIR / "papermc.jar"


def backup_jar() -> None:
    """Backup current PaperMC jar"""
    if not PAPER_JAR.exists():
        print("[backup] papermc.jar not found")
        return

    JAR_BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"papermc-{timestamp}.jar"
    dest = JAR_BACKUP_DIR / backup_name

    shutil.copy2(PAPER_JAR, dest)
    print(f"[backup] jar backed up to: {dest}")


def list_backups() -> None:
    """List available jar backups"""
    if not JAR_BACKUP_DIR.exists():
        print("[backups] no backup directory")
        return

    backups = sorted(JAR_BACKUP_DIR.glob("papermc-*.jar"))
    if not backups:
        print("[backups] no backups found")
        return

    print("[backups] available backups:")
    for backup in backups:
        size = backup.stat().st_size / (1024 * 1024)
        print(f" - {backup.name} ({size:.1f} MB)")


def update_from_url(url: str) -> None:
    """Update PaperMC from URL"""
    print(f"[update] downloading: {url}")

    # Backup first
    backup_jar()

    # Download new jar
    temp_jar = SERVER_DIR / "papermc.jar.new"
    try:
        urllib.request.urlretrieve(url, temp_jar)

        # Replace old jar
        if PAPER_JAR.exists():
            PAPER_JAR.unlink()
        temp_jar.rename(PAPER_JAR)

        print("[update] papermc.jar updated successfully")
        print("[update] restart server to apply changes")
    except Exception as e:
        print(f"[error] update failed: {e}")
        if temp_jar.exists():
            temp_jar.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="PaperMC Update Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Backup
    subparsers.add_parser("backup-jar", help="Backup current jar")

    # List backups
    subparsers.add_parser("list-backups", help="List jar backups")

    # Update
    update_parser = subparsers.add_parser("update-from-url", help="Update from URL")
    update_parser.add_argument("url", help="PaperMC download URL")

    args = parser.parse_args()

    if args.command == "backup-jar":
        backup_jar()
    elif args.command == "list-backups":
        list_backups()
    elif args.command == "update-from-url":
        update_from_url(args.url)


if __name__ == "__main__":
    main()
