"""glancely — single CLI entry point.

Subcommands dispatch to the per-component scripts. The component scripts stay
runnable directly too (matters for the dashboard, which subprocesses each
stats.py — keeps components independent).
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import webbrowser
from pathlib import Path

from glancely import __version__

PACKAGE_ROOT = Path(__file__).resolve().parent
SKILLS_ROOT = PACKAGE_ROOT / "examples"
DEFAULT_DASHBOARD_PATH = PACKAGE_ROOT / "dashboard" / "index.html"

USAGE = f"""\
glancely {__version__}

Usage: glancely <command> [<subcommand>] [args...]

Setup
  setup                       First-time setup: migrations + Google OAuth + sanity check
  doctor                      Diagnostic health check (creds, calendar, cron config)

Logging
  diary log [args]            Log a diary entry to Google Calendar
  mood log --raw "..."        Log a mood reply
  reminder add --title ...    Add a reminder
  reminder done --id N        Mark a reminder done
  reminder list               List active reminders
  reminder digest             Markdown digest (used by cron prompt)
  mit set --date YYYY-MM-DD --task "..." [--completed true|false]
  mit today                   Today's MIT as JSON

Stats (dashboard payloads as JSON)
  diary stats
  mood stats
  reminder stats
  mit stats

Components
  list                        Discovered components in dashboard order
  scaffold [args]             Create a new tracking component
  dashboard build [--out ...] Build the read-only HTML dashboard
  dashboard open              Build and open in your browser

Misc
  version                     Print version
  help                        This message

Run any subcommand with --help for details.
"""


def _forward(module_dotted: str, argv: list[str]) -> int:
    """Import the script module and run its main() with the given argv.

    Works whether the script's main accepts argv as a parameter or reads
    sys.argv directly — we swap sys.argv around the call.
    """
    mod = importlib.import_module(module_dotted)
    saved = sys.argv
    try:
        sys.argv = [module_dotted.split(".")[-1]] + argv
        rc = mod.main()
    finally:
        sys.argv = saved
    return rc or 0


# ── setup / doctor ─────────────────────────────────────────────────────────

def cmd_setup(argv: list[str]) -> int:
    """Minimal init: migrations only. Auth is per-component, run on demand."""
    from glancely.core.storage import apply_all_migrations
    from glancely.core.storage.db import GLANCE_HOME

    p = argparse.ArgumentParser(prog="glancely setup")
    p.parse_args(argv)

    print("Running migrations...")
    applied = apply_all_migrations(SKILLS_ROOT)
    print(json.dumps({"migrations_applied": applied, "glancely_home": str(GLANCE_HOME)}, indent=2))
    return 0


def cmd_doctor(argv: list[str]) -> int:
    from glancely.core.auth.google_oauth import CREDENTIALS_PATH, TOKEN_PATH
    from glancely.core.openclaw_cron import (
        JOBS_PATH,
        PR_OPENCLAW_CONFIG,
        list_component_crons,
    )
    from glancely.core.storage import get_connection
    from glancely.core.storage.db import get_db_path

    checks = {
        "version": __version__,
        "package_root": str(PACKAGE_ROOT),
        "data_db": {"path": str(get_db_path()), "exists": get_db_path().is_file()},
        "google_credentials": {"path": str(CREDENTIALS_PATH), "exists": CREDENTIALS_PATH.is_file()},
        "google_token": {"path": str(TOKEN_PATH), "exists": TOKEN_PATH.is_file()},
        "openclaw_cron_config": {"path": str(PR_OPENCLAW_CONFIG), "exists": PR_OPENCLAW_CONFIG.is_file()},
        "openclaw_jobs_json": {"path": str(JOBS_PATH), "exists": JOBS_PATH.is_file()},
        "registered_crons": len(list_component_crons()),
    }
    if checks["data_db"]["exists"]:
        try:
            with get_connection() as conn:
                tables = sorted(r[0] for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"))
            checks["data_db"]["tables"] = tables
        except Exception as exc:
            checks["data_db"]["error"] = str(exc)
    print(json.dumps(checks, indent=2))
    return 0


# ── components dispatch ────────────────────────────────────────────────────

def cmd_diary(argv: list[str]) -> int:
    sub = argv[0] if argv else "log"
    rest = argv[1:] if argv else []
    if sub == "log":
        return _forward("glancely.examples.diary_logger.scripts.log", rest)
    if sub == "stats":
        return _forward("glancely.examples.diary_logger.scripts.stats", rest)
    print(f"Unknown diary subcommand: {sub}", file=sys.stderr)
    return 2


def cmd_mood(argv: list[str]) -> int:
    sub = argv[0] if argv else "log"
    rest = argv[1:] if argv else []
    if sub == "log":
        return _forward("glancely.examples.mood.scripts.log", rest)
    if sub == "stats":
        return _forward("glancely.examples.mood.scripts.stats", rest)
    print(f"Unknown mood subcommand: {sub}", file=sys.stderr)
    return 2


def cmd_reminder(argv: list[str]) -> int:
    if not argv:
        print("Usage: reminder {add|done|cancel|list|digest|stats} [...]", file=sys.stderr)
        return 2
    sub, rest = argv[0], argv[1:]
    if sub in {"add", "done", "cancel", "list"}:
        return _forward("glancely.examples.reminder.scripts.log", [f"--{sub}", *rest])
    if sub == "digest":
        return _forward("glancely.examples.reminder.scripts.digest", rest)
    if sub == "stats":
        return _forward("glancely.examples.reminder.scripts.stats", rest)
    print(f"Unknown reminder subcommand: {sub}", file=sys.stderr)
    return 2


def cmd_mit(argv: list[str]) -> int:
    if not argv:
        print("Usage: mit {set|today|stats} [...]", file=sys.stderr)
        return 2
    sub, rest = argv[0], argv[1:]
    if sub == "set":
        return _forward("glancely.examples.mit.scripts.log", ["--upsert", *rest])
    if sub == "today":
        return _forward("glancely.examples.mit.scripts.today_brief", rest)
    if sub == "stats":
        return _forward("glancely.examples.mit.scripts.stats", rest)
    print(f"Unknown mit subcommand: {sub}", file=sys.stderr)
    return 2


def cmd_scaffold(argv: list[str]) -> int:
    return _forward("glancely.skills.scaffold_component.scripts.scaffold", argv)


def cmd_list(argv: list[str]) -> int:
    from glancely.core.registry import discover_components

    components = [
        {
            "name": c.name,
            "title": c.title,
            "order": c.panel_order,
            "panel_enabled": c.panel_enabled,
            "has_cron": c.cron is not None,
            "path": str(c.path),
        }
        for c in discover_components()
    ]
    print(json.dumps(components, indent=2))
    return 0


def cmd_dashboard(argv: list[str]) -> int:
    sub = argv[0] if argv else "build"
    rest = argv[1:] if argv else []
    if sub == "build":
        return _forward("glancely.dashboard.build", rest)
    if sub == "open":
        from glancely.core.storage.db import GLANCE_HOME
        from glancely.dashboard import build as dash_build
        out = GLANCE_HOME / "dashboard" / "index.html"
        result = dash_build.build(out)
        webbrowser.open(f"file://{result['output']}")
        print(json.dumps(result, indent=2))
        return 0
    print(f"Unknown dashboard subcommand: {sub}", file=sys.stderr)
    return 2


COMMANDS = {
    "setup": cmd_setup,
    "doctor": cmd_doctor,
    "diary": cmd_diary,
    "mood": cmd_mood,
    "reminder": cmd_reminder,
    "mit": cmd_mit,
    "scaffold": cmd_scaffold,
    "list": cmd_list,
    "dashboard": cmd_dashboard,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(USAGE)
        return 0
    if argv[0] in {"-V", "--version", "version"}:
        print(__version__)
        return 0

    cmd = argv[0]
    handler = COMMANDS.get(cmd)
    if handler is None:
        print(f"Unknown command: {cmd}\n", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2
    return handler(argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
