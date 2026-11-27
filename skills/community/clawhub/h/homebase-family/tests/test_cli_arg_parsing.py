"""
test_cli_arg_parsing.py — the tools.py CLI argument contract.

Regression cover for the documented stdin form (SKILL.md "Calling a tool").
Values holding an apostrophe cannot travel through the single-quoted inline
arg: the `'` closes the shell string and the command dies with `unmatched "`
before Python runs, so the tool never executes and no `❌` is ever printed.
Production hit this 15 times across add_calendar_event, save_snack_schedule
and get_trip_data (kid birthday titles like "Romy's Birthday Lunch").

These drive the real CLI in a subprocess -- the failure is in argv/stdin
handling, so an in-process call to execute_tool would not exercise it.
`__probe__` is a deliberately unknown tool name: reaching the dispatcher at
all proves the args parsed, and nothing is written to household state.
"""
import subprocess
import sys
from pathlib import Path

TOOLS = str(Path(__file__).parent.parent / "tools.py")

TRICKY = (
    '{"title":"Romy\'s Birthday Lunch",'
    '"note":"Cheez It\'s \U0001F392",'
    '"desc":"Parent\'s Day Picnic"}'
)


def _run(args, stdin=None):
    return subprocess.run(
        [sys.executable, TOOLS] + args,
        input=stdin, capture_output=True, text=True, timeout=120,
    )


def test_stdin_sentinel_accepts_apostrophes_and_emoji():
    """The documented escape hatch: `-` plus JSON on stdin."""
    r = _run(["__probe__", "-"], stdin=TRICKY)
    # Reached dispatch => the JSON parsed cleanly.
    assert "Unknown tool" in r.stdout
    assert "Invalid JSON" not in r.stdout


def test_inline_arg_still_works_for_plain_values():
    """Backward compatibility: the inline form is unchanged for safe values."""
    r = _run(["__probe__", '{"date":"2026-08-05"}'])
    assert "Unknown tool" in r.stdout
    assert "Invalid JSON" not in r.stdout


def test_malformed_stdin_json_reports_error_and_exits_nonzero():
    r = _run(["__probe__", "-"], stdin="{not json")
    assert "Invalid JSON args on stdin" in r.stdout
    assert r.returncode != 0


def test_malformed_inline_json_reports_error_and_exits_nonzero():
    r = _run(["__probe__", "{not json"])
    assert "Invalid JSON args" in r.stdout
    assert r.returncode != 0


def test_empty_json_arg_is_accepted():
    """The explicit '{}' form. Renamed 2026-09-10: the old name promised
    cover for the NO-third-argument form and the body passed '{}', which is a
    different code path. That gap is how the argv[2] IndexError below shipped."""
    r = _run(["__probe__", "{}"])
    assert "Unknown tool" in r.stdout


def test_omitted_json_arg_is_accepted():
    """SKILL.md: "Tools taking no args need no third argument at all."

    `elif _sys.argv[2] in ("--help", ...)` had no length guard, so every
    zero-arg invocation raised IndexError before reaching the dispatcher. The
    agent got a bare traceback with no `❌`, and SKILL.md tells it a non-zero
    exit is a real failure -- so a working tool was reported broken."""
    r = _run(["__probe__"])
    assert "Unknown tool" in r.stdout, r.stderr
    assert "IndexError" not in r.stderr


def test_bare_help_is_accepted():
    """`tools.py --help` is the recovery path the dispatcher's own error
    message points at, so it must not raise on the same missing argv[2]."""
    r = _run(["--help"])
    assert "Usage:" in r.stdout, r.stderr
    assert "IndexError" not in r.stderr
