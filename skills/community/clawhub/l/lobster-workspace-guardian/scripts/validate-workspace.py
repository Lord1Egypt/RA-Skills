#!/usr/bin/env python3
"""validate-workspace.py — Validate workspace structure against conventions.

Usage:
  python validate-workspace.py [workspace_path]

If no path given, uses parent of script's skills directory.
"""

import os
import re
import sys

def get_workspace():
    """Get workspace path: arg > parent of skills/ dir > fallback."""
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    # Walk up from script location, find workspace root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.dirname(script_dir)  # skills/ subdir
    test_path = os.path.dirname(skills_dir)   # parent of skills/
    if os.path.isdir(os.path.join(test_path, "SOUL.md")):
        return test_path
    return test_path

WORKSPACE = get_workspace()

# Required directories
REQUIRED_DIRS = ["projects", "knowledge", "output", "memory", "logs", ".temp"]

# Allowed root-level files
ALLOWED_ROOT_FILES = {
    "SOUL.md", "IDENTITY.md", "USER.md", "AGENTS.md",
    "MEMORY.md", "TOOLS.md", "HEARTBEAT.md",
    ".gitignore", ".npmrc",
}

# Allowed root-level directories
ALLOWED_ROOT_DIRS = {
    "projects", "knowledge", "output", "memory", "logs",
    ".temp", "slides", "skills", "scripts", ".learnings",
}

# Project dir pattern: YYYYNNNN_name
PROJECT_PATTERN = re.compile(r"^\d{4}\d{4}_.+$")

# Memory file pattern: YYYY-MM-DD.md or YYYY-MM-DD-HHMM.md
MEMORY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}(-\d{4})?\.md$")

def msg(tag, text):
    """Print with tag, encoding-safe."""
    print(f"[{tag}]  {text}")

def check_dir(name):
    path = os.path.join(WORKSPACE, name)
    exists = os.path.isdir(path)
    if not exists:
        msg("MISSING", f"Required dir: {name}/")
    return exists

def check_projects():
    errors = 0
    path = os.path.join(WORKSPACE, "projects")
    if not os.path.isdir(path):
        return 0
    for entry in os.listdir(path):
        fp = os.path.join(path, entry)
        if not os.path.isdir(fp):
            msg("ERROR", f"File in projects/: {entry}")
            errors += 1
            continue
        if not PROJECT_PATTERN.match(entry):
            msg("WARN", f"Project dir name not matching YYYYNNNN_name: {entry}")
            errors += 1
    return errors

def check_memory_files():
    errors = 0
    path = os.path.join(WORKSPACE, "memory")
    if not os.path.isdir(path):
        return 0
    for entry in os.listdir(path):
        fp = os.path.join(path, entry)
        if os.path.isdir(fp):
            continue
        if not MEMORY_PATTERN.match(entry):
            if entry != "session-summary.md":
                msg("WARN", f"Memory file name not matching YYYY-MM-DD.md: {entry}")
                errors += 1
    return errors

def check_root_scatter():
    errors = 0
    for entry in os.listdir(WORKSPACE):
        fp = os.path.join(WORKSPACE, entry)
        if entry.startswith("."):
            continue
        if os.path.isfile(fp):
            if entry not in ALLOWED_ROOT_FILES and not entry.endswith(".py"):
                msg("SCATTER", f"Root-level file: {entry}")
                errors += 1
        elif os.path.isdir(fp):
            if entry not in ALLOWED_ROOT_DIRS:
                msg("SCATTER", f"Root-level dir: {entry}/")
                errors += 1
    return errors

def check_empty_dirs():
    empty = 0
    for d in REQUIRED_DIRS:
        path = os.path.join(WORKSPACE, d)
        if not os.path.isdir(path):
            continue
        if not os.listdir(path):
            msg("EMPTY", f"{d}/ -- exists but empty")
            empty += 1
    return empty

def main():
    print(f"=== Workspace Validation ===")
    print(f"Workspace: {WORKSPACE}")
    print()

    print("--- Required Directories ---")
    for d in REQUIRED_DIRS:
        check_dir(d)

    print("")
    print("--- Root-level Scatter Check ---")
    r1 = check_root_scatter()

    print("")
    print("--- Project Directory Naming ---")
    r2 = check_projects()

    print("")
    print("--- Memory File Naming ---")
    r3 = check_memory_files()

    print("")
    print("--- Empty Directory Check ---")
    r4 = check_empty_dirs()

    print("")
    print("=== Validation Summary ===")
    total = r1 + r2 + r3 + r4
    if total == 0:
        print("  [OK] All checks passed!")
    else:
        print(f"  [WARN] {total} issue(s) found. Review warnings above.")

    return 0 if total == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
