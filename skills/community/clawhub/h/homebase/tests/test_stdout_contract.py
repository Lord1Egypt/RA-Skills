"""
test_stdout_contract.py — stdout belongs to the tool's return value.

Every tool goes out through `tools.py`, whose caller reads stdout: the agent
in chat, or a launchd runner that pipes it into `json.loads`. Anything a
library function prints therefore lands *in front of* the tool's answer.

That is not hypothetical. `sync_with_google_calendar()` printed two progress
lines to stdout, so `get_morning_briefing`, `get_evening_prep` and
`get_travel_status` all returned unparseable JSON —
every day, for as long as the briefing runner has existed. It only survived
because the consumer was a model tolerant of the noise. `weather.py` added
more on every Open-Meteo failure, which is exactly the degraded case the
briefing exists to report cleanly.

Two guards here:

  1. A static sweep of `features/` and `core/` for bare `print()` outside a
     CLI entry point. This is the one that actually holds the line — it fails
     on the next stray print, before anything reaches a family.
  2. Functional checks that the JSON-returning tools parse, with the network
     mocked out.
"""

import ast
import io
import json
import os
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

import pytest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY_DIRS = ("features", "core")

# Root-level library modules. tools.py above all: it is the file this whole
# contract is about — every tool's return value leaves through it and a launchd
# runner pipes that straight into json.loads — yet the sweep walked only the
# package directories, so a stray print() in any tool function was invisible to
# the guard that exists to catch exactly that.
ROOT_LIBRARY_FILES = ("tools.py", "utils.py")

# Functions that ARE the CLI entry point for their module and legitimately
# write their payload to stdout. Everything else in these packages is a
# library function reached through tools.py, and must use stderr.
CLI_ENTRY_POINTS = {
    ("features/bills/watcher.py", "_cli_main"),
    ("features/trips/trip_detector.py", "run_check"),
}


def _library_sources():
    for name in ROOT_LIBRARY_FILES:
        path = os.path.join(SKILL_DIR, name)
        if os.path.exists(path):
            yield name, path
    for rel_dir in LIBRARY_DIRS:
        for root, _dirs, files in os.walk(os.path.join(SKILL_DIR, rel_dir)):
            if "__pycache__" in root:
                continue
            for name in sorted(files):
                if name.endswith(".py"):
                    path = os.path.join(root, name)
                    yield os.path.relpath(path, SKILL_DIR), path


def _stdout_prints(rel_path, path):
    """Yield (lineno, enclosing_function) for print() calls that reach stdout.

    Skips calls under `if __name__ == "__main__":` and calls that pass an
    explicit `file=` (stderr, or a real file handle).
    """
    tree = ast.parse(open(path).read(), filename=path)

    main_guards = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test = ast.dump(node.test)
            if "__name__" in test and "__main__" in test:
                main_guards.append((node.lineno, max(
                    getattr(n, "lineno", node.lineno) for n in ast.walk(node)
                )))

    def in_main(lineno):
        return any(lo <= lineno <= hi for lo, hi in main_guards)

    # Map line -> enclosing function name.
    owner = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            last = max(getattr(n, "lineno", node.lineno) for n in ast.walk(node))
            for ln in range(node.lineno, last + 1):
                owner.setdefault(ln, node.name)

    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "print"):
            continue
        if in_main(node.lineno):
            continue
        if any(kw.arg == "file" for kw in node.keywords):
            continue
        fn = owner.get(node.lineno, "<module>")
        if (rel_path, fn) in CLI_ENTRY_POINTS or (rel_path, "*") in CLI_ENTRY_POINTS:
            continue
        yield node.lineno, fn


class TestNoLibraryPrintsToStdout:
    def test_no_bare_print_in_library_code(self):
        offenders = []
        for rel_path, path in _library_sources():
            for lineno, fn in _stdout_prints(rel_path, path):
                offenders.append(f"{rel_path}:{lineno} in {fn}()")
        assert not offenders, (
            "These print() calls reach stdout from library code, so they land in "
            "front of the tool's return value and break json.loads on it. Pass "
            "file=sys.stderr, or add the function to CLI_ENTRY_POINTS if it really "
            "is a module's CLI entry point:\n  " + "\n  ".join(offenders)
        )

    def test_the_guard_can_actually_fail(self, tmp_path):
        """A guard that cannot fail is not a guard."""
        bad = tmp_path / "bad.py"
        bad.write_text(
            "def helper():\n"
            "    print('leaks to stdout')\n"
            "\n"
            "def ok():\n"
            "    import sys\n"
            "    print('fine', file=sys.stderr)\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    print('also fine')\n"
        )
        found = list(_stdout_prints("bad.py", str(bad)))
        assert [(ln, fn) for ln, fn in found] == [(2, "helper")]


# ─── Functional: the JSON tools parse ────────────────────────────────────────

JSON_TOOLS = [
    "get_evening_prep",
    "get_travel_status",
    "get_weather_context",
    "get_school_roster",
    "get_message_targets",
]


@pytest.fixture
def quiet_calendar():
    """A synced-looking aggregator that performs no network I/O but still
    exercises the code path that used to print."""
    import tools

    agg = MagicMock()
    agg.calendar = {}
    agg.get_events_by_date.return_value = []
    agg.SYNC_WINDOW_DAYS_FORWARD = 30

    def _sync(detect_restaurants=False, force=False):
        # Stand-in for the real sync's diagnostics. If a future change routes
        # these back to stdout, the tools below stop parsing and this fails.
        import sys
        print("Syncing with Google Calendar...", file=sys.stderr)
        return True

    agg.sync_with_google_calendar.side_effect = _sync
    with patch("features.calendar.calendar_aggregator.FamilyCalendarAggregator",
               return_value=agg):
        yield tools


class TestJsonToolsReturnParseableJson:
    @pytest.mark.parametrize("tool", JSON_TOOLS)
    def test_stdout_is_pure_json(self, tool, quiet_calendar):
        tools = quiet_calendar
        buf = io.StringIO()
        with patch("features.briefing.weather.fetch_weather_context",
                   return_value=None), \
             redirect_stdout(buf):
            result = tools.execute_tool(tool, {})

        assert not result.startswith("❌"), f"{tool} errored: {result}"
        json.loads(result)                       # the return value is JSON
        assert buf.getvalue() == "", (           # and nothing raced it to stdout
            f"{tool} wrote to stdout: {buf.getvalue()!r}"
        )

    def test_morning_briefing_payload_is_json(self):
        """get_morning_briefing composes from get_briefing_data directly."""
        import tools
        with patch("features.briefing.morning_briefing.get_briefing_data",
                   return_value={"date": "Monday, August 31", "events": []}):
            out = tools.get_morning_briefing()
        assert json.loads(out)["date"] == "Monday, August 31"
