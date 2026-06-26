#!/usr/bin/env python3
"""
Kapsel — Project Memory Capsules

Archive completed project knowledge to cloud storage (via rclone)
and reload it on demand. Keeps your agent's working memory clean
while preserving full project context for later.

Each capsule is a folder with:
  - summary.md   — Short overview (max 500 words)
  - details.md   — Decisions, timeline, links, background
  - context.md   — Technical details, configs, code snippets
  - files/       — Associated files (optional)

Configuration (environment variables):
  KAPSEL_REMOTE  — rclone remote path (default: gdrive:Kapseln)
  KAPSEL_TMP     — Local temp directory (default: /tmp/openclaw/kapseln)

Requires: rclone (https://rclone.org)
"""
import sys
import os
import subprocess
from datetime import datetime

# --- Configuration ---
# Override these with environment variables or edit directly
KAPSELN_REMOTE = os.environ.get("KAPSEL_REMOTE", "gdrive:Kapseln")
LOCAL_TMP = os.environ.get("KAPSEL_TMP", "/tmp/openclaw/kapseln")


def run(cmd):
    """Run a shell command and return (stdout, stderr)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "Error: Command timed out after 30 seconds"


def check_rclone():
    """Verify rclone is installed and accessible."""
    out, err = run("rclone version 2>/dev/null")
    if not out:
        print("Error: rclone is not installed or not in PATH.")
        print("Install it from https://rclone.org/install/")
        print("Then configure a remote: rclone config")
        sys.exit(1)


def cmd_list():
    """List all capsules with their summaries."""
    out, err = run(f"rclone lsd {KAPSELN_REMOTE}/ 2>/dev/null")
    if not out:
        print("No capsules found.")
        print(f"  Remote: {KAPSELN_REMOTE}/")
        print(f"  Create one with: kapsel.py create <name>")
        return

    print("## Project Capsules\n")
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            name = parts[-1]
            summary, _ = run(
                f'rclone cat "{KAPSELN_REMOTE}/{name}/summary.md" 2>/dev/null'
            )
            if summary:
                lines = [l for l in summary.splitlines() if l.strip()][:3]
                desc = " | ".join(lines)
            else:
                desc = "(no summary)"
            print(f"  - **{name}**: {desc}")
    print()


def cmd_create(name):
    """Create a new capsule with template files."""
    os.makedirs(f"{LOCAL_TMP}/{name}", exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d")

    summary = f"""# {name}
Created: {now}
Status: active

## Summary
[Short description of the project]

## People
[Who is involved?]

## Outcome
[What was the result?]
"""

    details = f"""# {name} — Details
Created: {now}

## Background
[Why was this project started?]

## Decisions
[Key decisions and their reasoning]

## Timeline
- {now}: Project started

## Links & Resources
[Relevant URLs, documents, etc.]
"""

    context = f"""# {name} — Technical Context
Created: {now}

## Configuration
[Relevant configs, settings, environment variables]

## Code & Snippets
[Important code sections]

## Files
[Paths to relevant files]
"""

    for fname, content in [
        ("summary.md", summary),
        ("details.md", details),
        ("context.md", context),
    ]:
        path = f"{LOCAL_TMP}/{name}/{fname}"
        with open(path, "w") as f:
            f.write(content)

    out, err = run(f'rclone copy "{LOCAL_TMP}/{name}" "{KAPSELN_REMOTE}/{name}/"')
    if err and "error" in err.lower():
        print(f"Error: {err}")
    else:
        print(f"Capsule '{name}' created.")
        print(f"  Remote: {KAPSELN_REMOTE}/{name}/")
        print(f"  Files: summary.md, details.md, context.md")
        print(f"\nEdit the files and re-upload, or use 'save' to add files.")


def cmd_load(name):
    """Load a capsule — display all documents."""
    summary, _ = run(f'rclone cat "{KAPSELN_REMOTE}/{name}/summary.md" 2>/dev/null')
    if not summary:
        print(f"Capsule '{name}' not found.")
        return

    print(f"## Capsule loaded: {name}\n")
    print("### Summary")
    print(summary)

    print("\n### Details")
    details, _ = run(f'rclone cat "{KAPSELN_REMOTE}/{name}/details.md" 2>/dev/null')
    print(details or "(no details)")

    print("\n### Technical Context")
    context, _ = run(f'rclone cat "{KAPSELN_REMOTE}/{name}/context.md" 2>/dev/null')
    print(context or "(no context)")

    files, _ = run(f'rclone ls "{KAPSELN_REMOTE}/{name}/files/" 2>/dev/null')
    if files:
        print("\n### Files")
        for line in files.splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                print(f"  - {parts[1]}")


def cmd_summary(name):
    """Show only the summary of a capsule."""
    summary, _ = run(f'rclone cat "{KAPSELN_REMOTE}/{name}/summary.md" 2>/dev/null')
    if summary:
        print(summary)
    else:
        print(f"Capsule '{name}' not found.")


def cmd_archive(name):
    """Mark a capsule as completed."""
    now = datetime.now().strftime("%Y-%m-%d")
    summary, _ = run(f'rclone cat "{KAPSELN_REMOTE}/{name}/summary.md" 2>/dev/null')
    if not summary:
        print(f"Capsule '{name}' not found.")
        return

    summary = summary.replace("Status: active", f"Status: archived ({now})")
    # Also handle German status from older versions
    summary = summary.replace("Status: aktiv", f"Status: archived ({now})")

    os.makedirs(f"{LOCAL_TMP}/{name}", exist_ok=True)
    with open(f"{LOCAL_TMP}/{name}/summary.md", "w") as f:
        f.write(summary)
    run(f'rclone copy "{LOCAL_TMP}/{name}/summary.md" "{KAPSELN_REMOTE}/{name}/"')
    print(f"Capsule '{name}' archived ({now}).")


def cmd_save(name, filepath):
    """Add a file to a capsule."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    out, err = run(f'rclone copy "{filepath}" "{KAPSELN_REMOTE}/{name}/files/"')
    if err and "error" in err.lower():
        print(f"Error: {err}")
    else:
        fname = os.path.basename(filepath)
        print(f"File '{fname}' added to capsule '{name}'.")


def cmd_help():
    """Show usage information."""
    print("Kapsel — Project Memory Capsules\n")
    print(f"  Remote: {KAPSELN_REMOTE}")
    print(f"  Temp:   {LOCAL_TMP}\n")
    print("Commands:")
    print("  kapsel.py list                  — Show all capsules")
    print("  kapsel.py create <name>         — Create new capsule")
    print("  kapsel.py load <name>           — Load full capsule")
    print("  kapsel.py summary <name>        — Show only summary")
    print("  kapsel.py archive <name>        — Mark as completed")
    print("  kapsel.py save <name> <file>    — Add file to capsule")
    print("\nConfiguration:")
    print("  KAPSEL_REMOTE  — rclone remote path (current: {})".format(KAPSELN_REMOTE))
    print("  KAPSEL_TMP     — Local temp dir (current: {})".format(LOCAL_TMP))


def main():
    check_rclone()

    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)

    cmd = sys.argv[1]
    commands = {
        "list": lambda: cmd_list(),
        "create": lambda: cmd_create(sys.argv[2]) if len(sys.argv) > 2 else print("Usage: kapsel.py create <name>"),
        "load": lambda: cmd_load(sys.argv[2]) if len(sys.argv) > 2 else print("Usage: kapsel.py load <name>"),
        "summary": lambda: cmd_summary(sys.argv[2]) if len(sys.argv) > 2 else print("Usage: kapsel.py summary <name>"),
        "archive": lambda: cmd_archive(sys.argv[2]) if len(sys.argv) > 2 else print("Usage: kapsel.py archive <name>"),
        "save": lambda: cmd_save(sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else print("Usage: kapsel.py save <name> <file>"),
        "help": lambda: cmd_help(),
    }

    if cmd in commands:
        commands[cmd]()
    else:
        print(f"Unknown command: {cmd}")
        cmd_help()


if __name__ == "__main__":
    main()
