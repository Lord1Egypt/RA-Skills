#!/usr/bin/env python3
"""
setup_cron.py — Add the daily OpenClaw backup cron job.
Also checks if cron already exists and warns if so.
"""

import subprocess
import sys


def cron_exists(name):
    result = subprocess.run(
        ["openclaw", "cron", "list", "--json"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        import json
        try:
            data = json.loads(result.stdout)
            crons = data if isinstance(data, list) else data.get("crons", [])
            for c in crons:
                if c.get("name") == name:
                    return True
        except Exception:
            pass
    return False


def add_cron():
    if cron_exists("openclaw-backup:daily"):
        print("⚠️  Cron 'openclaw-backup:daily' already exists.")
        print("   Run 'openclaw cron remove openclaw-backup:daily' to remove it first.")
        return False

    cmd = [
        "openclaw", "cron", "add",
        "--name", "openclaw-backup:daily",
        "--message", "backup openclaw",
        "--cron", "0 4 * * *",
        "--tz", "Asia/Hong_Kong",
        "--session", "isolated",
        "--description", "Daily OpenClaw backup to ~/openclaw_backups"
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def main():
    print("OpenClaw Backup — Cron Setup")
    print("=" * 40)
    print()

    success = add_cron()
    if success:
        print()
        print("✅ Cron job 'openclaw-backup:daily' added.")
        print("   Runs daily at 04:00 HKT.")
        print()
        print("Verify:")
        print("  openclaw cron list")
    else:
        print()
        print("⚠️  Cron was not added. Check output above.")


if __name__ == "__main__":
    main()