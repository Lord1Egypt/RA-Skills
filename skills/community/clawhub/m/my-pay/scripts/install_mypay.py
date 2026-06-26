#!/usr/bin/env python3
"""
install_mypay.py - Dependency checker for mypay-bot npm package.

This script ONLY checks whether mypay-bot is installed and whether an update
is available. It does NOT install or update anything automatically.
It exits with:
  0 — mypay-bot is installed and up to date (or version check was skipped)
  1 — mypay-bot is not installed (user action required)
  2 — mypay-bot is installed but outdated (informational, non-blocking)
"""

import subprocess
import sys
import json
import shutil

# Pin to a known-good version to prevent silent upgrades to untested releases.
REQUIRED_VERSION = "1.0.0"


def run_cmd(cmd):
    """Run a shell command and return (returncode, stdout)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout.strip()
    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"[mypay] Command failed: {cmd} -> {e}")
        return 1, ""


def check_npm_available():
    """Verify npm is on PATH."""
    if not shutil.which("npm"):
        print("[mypay] ERROR: npm is not found on PATH.")
        print("[mypay] Please install Node.js and npm first: https://nodejs.org/")
        return False
    return True


def get_installed_version():
    """Get the currently installed global version of mypay-bot, or None."""
    code, output = run_cmd("npm list -g mypay-bot --json 2>/dev/null")
    if code != 0 or not output:
        return None
    try:
        data = json.loads(output)
        deps = data.get("dependencies", {})
        if "mypay-bot" in deps:
            return deps["mypay-bot"].get("version")
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def main():
    if not check_npm_available():
        sys.exit(1)

    installed = get_installed_version()

    if installed is None:
        print("[mypay] MISSING: mypay-bot is not installed.")
        print(f"[mypay] To install the required version, run manually:")
        print(f"[mypay]   npm install -g mypay-bot@{REQUIRED_VERSION}")
        print("[mypay] After installing, re-run this skill.")
        sys.exit(1)

    if installed != REQUIRED_VERSION:
        print(f"[mypay] WARNING: installed version is {installed}, expected {REQUIRED_VERSION}.")
        print(f"[mypay] To update, run manually:")
        print(f"[mypay]   npm install -g mypay-bot@{REQUIRED_VERSION}")
        print("[mypay] Proceeding with the installed version for now.")
        sys.exit(2)

    print(f"[mypay] OK: mypay-bot {installed} is installed and matches the required version.")
    sys.exit(0)


if __name__ == "__main__":
    main()
