#!/usr/bin/env python3
"""
PaperMC Plugin Manager
Safe plugin installation and backup
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
import urllib.request

SERVER_DIR = Path("/path/to/your/papermc-server")  # CHANGE THIS
PLUGINS_DIR = SERVER_DIR / "plugins"
BACKUP_DIR = SERVER_DIR / "plugin_backup"


def backup_plugin(plugin_name: str) -> None:
    """Backup a plugin jar"""
    source = PLUGINS_DIR / plugin_name
    if not source.exists():
        print(f"[backup] plugin not found: {plugin_name}")
        return

    BACKUP_DIR.mkdir(exist_ok=True)
    dest = BACKUP_DIR / plugin_name
    shutil.copy2(source, dest)
    print(f"[backup] copied to: {dest}")


def list_plugins() -> None:
    """List all installed plugins"""
    if not PLUGINS_DIR.exists():
        print("[plugins] directory not found")
        return

    jars = sorted(PLUGINS_DIR.glob("*.jar"))
    if not jars:
        print("[plugins] no plugins installed")
        return

    print("[plugins] installed plugins:")
    for jar in jars:
        print(f" - {jar.name}")


def install_from_file(filepath: str) -> None:
    """Install plugin from local file"""
    source = Path(filepath)
    if not source.exists():
        print(f"[install] file not found: {filepath}")
        return

    dest = PLUGINS_DIR / source.name
    shutil.copy2(source, dest)
    print(f"[install] installed: {dest.name}")


def install_from_url(url: str, filename: str | None = None) -> None:
    """Download and install plugin from URL"""
    if filename is None:
        filename = url.split("/")[-1]

    dest = PLUGINS_DIR / filename
    print(f"[download] fetching: {url}")

    try:
        urllib.request.urlretrieve(url, dest)
        print(f"[install] installed: {filename}")
    except Exception as e:
        print(f"[error] download failed: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PaperMC Plugin Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List
    subparsers.add_parser("list", help="List installed plugins")

    # Backup
    backup_parser = subparsers.add_parser("backup", help="Backup a plugin")
    backup_parser.add_argument("plugin", help="Plugin jar name")

    # Install from file
    file_parser = subparsers.add_parser("install-file", help="Install from local file")
    file_parser.add_argument("filepath", help="Path to plugin jar")

    # Install from URL
    url_parser = subparsers.add_parser("install-url", help="Install from URL")
    url_parser.add_argument("url", help="Download URL")
    url_parser.add_argument("--filename", help="Save as filename")

    args = parser.parse_args()

    if args.command == "list":
        list_plugins()
    elif args.command == "backup":
        backup_plugin(args.plugin)
    elif args.command == "install-file":
        install_from_file(args.filepath)
    elif args.command == "install-url":
        install_from_url(args.url, args.filename)


if __name__ == "__main__":
    main()
