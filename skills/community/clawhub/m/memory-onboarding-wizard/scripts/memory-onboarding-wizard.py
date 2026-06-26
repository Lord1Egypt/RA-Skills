#!/usr/bin/env python3
"""
memory-onboarding-wizard.py
Bootstrap an OpenClaw agent's memory system in one command.

Usage:
  python3 memory-onboarding-wizard.py
  python3 memory-onboarding-wizard.py --workspace /path/to/workspace
  python3 memory-onboarding-wizard.py --non-interactive
"""

import argparse
import os
import sys
from datetime import datetime, timezone


# ─── Color helpers ────────────────────────────────────────────────────────────

def bold(s): return f"\033[1m{s}\033[0m"
def green(s): return f"\033[32m{s}\033[0m"
def yellow(s): return f"\033[33m{s}\033[0m"
def cyan(s): return f"\033[36m{s}\033[0m"
def red(s): return f"\033[31m{s}\033[0m"
def dim(s): return f"\033[2m{s}\033[0m"

def ok(msg): print(f"  {green('✅')} {msg}")
def created(msg): print(f"  {cyan('✨')} {msg}")
def skip(msg): print(f"  {dim('⏭️  ' + msg)}")
def warn(msg): print(f"  {yellow('⚠️')}  {msg}")
def err(msg): print(f"  {red('❌')} {msg}")


# ─── Templates ─────────────────────────────────────────────────────────────────

def memory_md_template(today: str) -> str:
    return f"""# MEMORY.md — Long-Term Memory

> This is your curated long-term memory. Update it with significant events,
> lessons learned, decisions made, and context worth keeping across sessions.
> Think of it like a human's long-term memory — distilled wisdom, not raw logs.
> Raw logs go in `memory/YYYY-MM-DD.md` files.

---

## Who I Am

*(Your agent's identity and purpose — fill this in after setup)*

## Key People & Projects

*(Important context about who you're working with and what you're building)*

## Important Decisions

*(Significant choices made and why)*

## Lessons Learned

*(Things not to repeat, things that work well)*

## Current Focus

*(What's being worked on right now — update regularly)*

---
*Created: {today}*
*Last updated: {today}*
"""


def daily_note_template(today: str) -> str:
    return f"""# Daily Notes — {today}

## Session Log

- 🚀 Memory system initialized via memory-onboarding-wizard

## What Happened Today

*(Agent fills this in as the session progresses)*

## Decisions Made

*(Any significant choices or directions agreed upon)*

## Things to Remember

*(Carry-forward items for tomorrow)*

---
*Created by memory-onboarding-wizard*
"""


def heartbeat_md_template() -> str:
    return """# HEARTBEAT.md — Periodic Checklist

> The agent reads this file on every heartbeat poll.
> Keep it SHORT — tokens are precious. Remove completed items.
> Add time-sensitive reminders or recurring checks here.

## Active Checks (rotate through these 2-4x/day)

- [ ] Email — any urgent unread messages?
- [ ] Calendar — upcoming events in the next 24-48h?
- [ ] Weather — relevant if your human might go out?

## Reminders

*(Add one-off reminders here, remove once done)*

## Rules

- If nothing needs attention → reply `HEARTBEAT_OK`
- Don't check the same thing twice within 30 minutes
- Late night (23:00–08:00): stay quiet unless urgent

---
*Tip: Edit this file anytime to add reminders or tasks.*
"""


def user_md_template(name: str, timezone_str: str, use_case: str, today: str) -> str:
    return f"""# USER.md — About Your Human

- **Name:** {name}
- **Timezone:** {timezone_str}
- **Main Use Case:** {use_case}

## Notes

*(Add personal preferences, context, and anything the agent should know here)*

---
*Created by memory-onboarding-wizard on {today}*
*Update this file anytime to help your agent serve you better.*
"""


# ─── Core logic ───────────────────────────────────────────────────────────────

def ensure_memory_md(workspace: str, today: str) -> bool:
    path = os.path.join(workspace, "MEMORY.md")
    if os.path.exists(path):
        skip(f"MEMORY.md already exists — keeping it")
        return False
    with open(path, "w") as f:
        f.write(memory_md_template(today))
    created(f"Created MEMORY.md with starter template")
    return True


def ensure_daily_note(workspace: str, today: str) -> bool:
    memory_dir = os.path.join(workspace, "memory")
    os.makedirs(memory_dir, exist_ok=True)
    path = os.path.join(memory_dir, f"{today}.md")
    if os.path.exists(path):
        skip(f"memory/{today}.md already exists — keeping it")
        return False
    with open(path, "w") as f:
        f.write(daily_note_template(today))
    created(f"Created memory/{today}.md (today's daily note)")
    return True


def ensure_heartbeat_md(workspace: str) -> bool:
    path = os.path.join(workspace, "HEARTBEAT.md")
    if os.path.exists(path):
        skip(f"HEARTBEAT.md already exists — keeping it")
        return False
    with open(path, "w") as f:
        f.write(heartbeat_md_template())
    created(f"Created HEARTBEAT.md with starter checklist")
    return True


def ask_user_questions(non_interactive: bool) -> tuple[str, str, str]:
    """Ask 3 quick questions. Returns (name, timezone, use_case)."""
    if non_interactive:
        return ("You", "UTC", "General AI assistance")

    print()
    print(bold("  3 quick questions to personalize your agent:"))
    print()

    try:
        name = input(f"  {cyan('1.')} What should your agent call you? [You]: ").strip()
        if not name:
            name = "You"

        tz = input(f"  {cyan('2.')} Your timezone? (e.g. UTC, Europe/London, US/Eastern) [UTC]: ").strip()
        if not tz:
            tz = "UTC"

        use_case = input(f"  {cyan('3.')} Main use case for your agent? (e.g. productivity, trading, coding): ").strip()
        if not use_case:
            use_case = "General AI assistance"
    except (EOFError, KeyboardInterrupt):
        print()
        warn("Non-interactive environment detected — using defaults")
        return ("You", "UTC", "General AI assistance")

    return name, tz, use_case


def write_user_md(workspace: str, name: str, timezone_str: str, use_case: str, today: str) -> bool:
    path = os.path.join(workspace, "USER.md")
    if os.path.exists(path):
        # Offer to update if interactive, but don't overwrite blindly
        skip(f"USER.md already exists — keeping it (edit manually to update)")
        return False
    with open(path, "w") as f:
        f.write(user_md_template(name, timezone_str, use_case, today))
    created(f"Created USER.md for {name}")
    return True


def validate(workspace: str, today: str) -> dict:
    checks = {
        "MEMORY.md": os.path.join(workspace, "MEMORY.md"),
        f"memory/{today}.md": os.path.join(workspace, "memory", f"{today}.md"),
        "HEARTBEAT.md": os.path.join(workspace, "HEARTBEAT.md"),
        "USER.md": os.path.join(workspace, "USER.md"),
    }
    results = {}
    for label, path in checks.items():
        results[label] = os.path.exists(path)
    return results


def print_banner():
    print()
    print(bold(cyan("  ╔══════════════════════════════════════════════╗")))
    print(bold(cyan("  ║      🧠 Memory Onboarding Wizard             ║")))
    print(bold(cyan("  ║      OpenClaw Agent Memory Setup             ║")))
    print(bold(cyan("  ╚══════════════════════════════════════════════╝")))
    print()


def print_summary(validation: dict, name: str):
    all_ok = all(validation.values())
    print()
    print(bold("  ─── Validation Summary ─────────────────────────"))
    for label, exists in validation.items():
        if exists:
            ok(f"{label}")
        else:
            err(f"{label} — MISSING")
    print()

    if all_ok:
        print(bold(green("  🎉 You're set up! Your agent has a memory system.")))
        print()
        print(f"  {bold('What your agent will do each session:')}")
        print(f"   • Read USER.md to know who it's serving")
        print(f"   • Read memory/ files for recent context")
        print(f"   • Read MEMORY.md (in main sessions) for long-term context")
        print(f"   • Check HEARTBEAT.md on periodic polls")
    else:
        print(bold(yellow("  ⚠️  Setup incomplete — check missing files above")))

    print()
    print(bold("  ─── First 3 Things to Try ───────────────────────"))
    print(f"  {cyan('1.')} {bold('Talk to your agent:')} Open a chat and say: \"Read your memory files and introduce yourself\"")
    print(f"  {cyan('2.')} {bold('Test the heartbeat:')} Send the message: \"Read HEARTBEAT.md if it exists, then check in\"")
    print(f"  {cyan('3.')} {bold('Personalize USER.md:')} Open USER.md and add more context about yourself — hobbies, goals, preferences")
    print()
    print(dim("  Tip: Update MEMORY.md after important conversations so your agent remembers them."))
    print(dim("  Tip: The memory/ folder grows automatically — each session adds a daily note."))
    print()


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap an OpenClaw agent's memory system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 memory-onboarding-wizard.py
  python3 memory-onboarding-wizard.py --workspace ~/my-workspace
  python3 memory-onboarding-wizard.py --non-interactive
        """
    )
    parser.add_argument(
        "--workspace", "-w",
        default=os.path.expanduser("~/.openclaw/workspace"),
        help="Path to OpenClaw workspace (default: ~/.openclaw/workspace)"
    )
    parser.add_argument(
        "--non-interactive", "-n",
        action="store_true",
        help="Skip interactive questions, use defaults"
    )
    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print_banner()

    # Validate workspace
    if not os.path.isdir(workspace):
        print(f"  {yellow('⚠️')}  Workspace not found at: {workspace}")
        try:
            answer = input(f"  Create it? [Y/n]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = "y"
        if answer in ("", "y", "yes"):
            os.makedirs(workspace, exist_ok=True)
            ok(f"Created workspace at {workspace}")
        else:
            err("Workspace missing — exiting")
            sys.exit(1)

    print(f"  {dim('Workspace:')} {workspace}")
    print(f"  {dim('Date:     ')} {today}")
    print()
    print(bold("  ─── Setting Up Memory Files ─────────────────────"))
    print()

    # Step 1–3: Create files
    ensure_memory_md(workspace, today)
    ensure_daily_note(workspace, today)
    ensure_heartbeat_md(workspace)

    # Step 4: Ask questions and write USER.md
    print()
    print(bold("  ─── User Profile ────────────────────────────────"))
    name, tz, use_case = ask_user_questions(args.non_interactive)
    write_user_md(workspace, name, tz, use_case, today)

    # Step 5: Validate
    print()
    print(bold("  ─── Running Validation ──────────────────────────"))
    print()
    validation = validate(workspace, today)
    for label, exists in validation.items():
        if exists:
            ok(f"{label}")
        else:
            err(f"{label}")

    # Step 6: Summary and suggestions
    print_summary(validation, name)


if __name__ == "__main__":
    main()
