#!/usr/bin/env python3
"""workspace-cleanup.py — Scan and clean temp/stale files in workspace.

Safe mode (default): only reports findings, does NOT delete.
Add --apply to actually clean.

Usage:
  python workspace-cleanup.py [workspace_path] [--apply]
"""

import os
import sys
from datetime import datetime, timezone

def get_workspace():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        return os.path.abspath(sys.argv[1])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.dirname(script_dir)
    test_path = os.path.dirname(skills_dir)
    if os.path.isfile(os.path.join(test_path, "SOUL.md")):
        return test_path
    return test_path

WORKSPACE = get_workspace()
TEMP_DIR = os.path.join(WORKSPACE, ".temp")
DAYS_STALE = 7
NOW = datetime.now(timezone.utc).timestamp()

def age_days(path):
    try:
        return (NOW - os.path.getmtime(path)) / 86400
    except OSError:
        return 0

def msg(tag, text):
    print(f"[{tag}]  {text}")

def scan_temp(apply=False):
    findings = []
    if not os.path.isdir(TEMP_DIR):
        msg("OK", ".temp/ directory does not exist")
        return findings

    for root, dirs, files in os.walk(TEMP_DIR):
        for f in files:
            fp = os.path.join(root, f)
            d = age_days(fp)
            if d > DAYS_STALE:
                findings.append((fp, d))
                if apply:
                    os.remove(fp)
                    msg("DEL", f"{fp} ({d:.1f} days old)")
                else:
                    msg("FOUND", f"{fp} ({d:.1f} days old)")

    for root, dirs, files in os.walk(TEMP_DIR, topdown=False):
        if root != TEMP_DIR and not files and not dirs:
            if apply:
                try:
                    os.rmdir(root)
                    msg("RMDIR", root)
                except OSError:
                    pass
    return findings

def scan_scattered(apply=False):
    findings = []
    allowed_roots = {
        "projects", "knowledge", "output", "memory",
        "logs", ".temp", "slides", "skills", ".learnings",
        "scripts",
    }
    allowed_files = {
        "SOUL.md", "IDENTITY.md", "USER.md", "AGENTS.md",
        "MEMORY.md", "TOOLS.md", "HEARTBEAT.md",
        ".gitignore", ".npmrc",
    }

    for entry in os.listdir(WORKSPACE):
        if entry.startswith("."):
            continue
        fp = os.path.join(WORKSPACE, entry)
        if os.path.isfile(fp):
            if entry in allowed_files:
                continue
            findings.append((fp, "root-level file"))
            msg("SCATTERED", fp)
        elif os.path.isdir(fp):
            if entry in allowed_roots:
                continue
            findings.append((fp, f"unknown dir: {entry}"))
            msg("SCATTERED", fp)

    return findings

def main():
    apply = "--apply" in sys.argv
    mode = "REPORT (add --apply to execute)" if not apply else "EXECUTING"

    print(f"=== Workspace Cleanup [{mode}] ===")
    print(f"Workspace: {WORKSPACE}")
    print()

    f1 = scan_temp(apply=apply)
    f2 = scan_scattered(apply=apply)

    print()
    print("=== Summary ===")
    print(f"  Stale temp files found:   {len(f1)}")
    print(f"  Scattered items found:    {len(f2)}")

    if not f1 and not f2:
        print("  [OK] Workspace is clean.")
    elif not apply:
        print("  Run with --apply to clean.")

if __name__ == "__main__":
    main()
