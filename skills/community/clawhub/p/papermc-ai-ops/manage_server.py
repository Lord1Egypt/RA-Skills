#!/usr/bin/env python3
"""
PaperMC Server Management Script
Safe server lifecycle management through controlled interfaces
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Configuration - Update these paths for your installation
SERVER_DIR = Path("/path/to/your/papermc-server")  # CHANGE THIS
SERVICE_NAME = "paper-mc.service"                   # CHANGE THIS if needed
BACKUP_SCRIPT = SERVER_DIR / "backup.sh"


def run_command(cmd: list[str], check: bool = True) -> int:
    """Execute command in server directory"""
    print(f"[cmd] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=SERVER_DIR)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def service_action(action: str) -> None:
    """Start/stop/restart service"""
    run_command(["sudo", "systemctl", action, SERVICE_NAME])


def service_status() -> None:
    """Show service status"""
    run_command(["systemctl", "status", SERVICE_NAME], check=False)


def service_logs(lines: int = 50, follow: bool = False) -> None:
    """View service logs"""
    cmd = ["journalctl", "-u", SERVICE_NAME, "-n", str(lines), "--no-pager"]
    if follow:
        cmd = ["journalctl", "-u", SERVICE_NAME, "-f"]
    run_command(cmd, check=False)


def backup_world() -> None:
    """Execute world backup"""
    if not BACKUP_SCRIPT.exists():
        raise SystemExit(f"backup script not found: {BACKUP_SCRIPT}")
    run_command(["bash", str(BACKUP_SCRIPT)])


def plugin_list() -> None:
    """List installed plugins"""
    plugins_dir = SERVER_DIR / "plugins"
    if not plugins_dir.exists():
        print("[plugins] plugins directory not found")
        return

    jars = sorted(plugins_dir.glob("*.jar"))
    if not jars:
        print("[plugins] no plugins installed")
        return

    print("[plugins] installed plugins:")
    for jar in jars:
        print(f" - {jar.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PaperMC Server Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Status
    subparsers.add_parser("status", help="Show service status")

    # Logs
    logs_parser = subparsers.add_parser("logs", help="View logs")
    logs_parser.add_argument("-n", "--lines", type=int, default=50, help="Number of lines")
    logs_parser.add_argument("-f", "--follow", action="store_true", help="Follow logs")

    # Backup
    subparsers.add_parser("backup", help="Backup world")

    # Plugins
    subparsers.add_parser("plugins", help="List plugins")

    # Restart
    subparsers.add_parser("restart", help="Restart service")

    args = parser.parse_args()

    if args.command == "status":
        service_status()
    elif args.command == "logs":
        service_logs(args.lines, args.follow)
    elif args.command == "backup":
        backup_world()
    elif args.command == "plugins":
        plugin_list()
    elif args.command == "restart":
        service_action("restart")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
