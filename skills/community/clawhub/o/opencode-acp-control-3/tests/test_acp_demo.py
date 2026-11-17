"""Tests for examples/acp_demo.py.

These tests cover the parts of the demo that do NOT require a real `opencode`
binary: JSON-RPC frame construction and the stdout framing parser.

The frame/parser code uses bytes (because subprocess.PIPE yields bytes), so the
tests use io.BytesIO. The CLI smoke tests exercise --help and --dry-run paths.

Run with:

    pytest tests/

"""

from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_PATH = REPO_ROOT / "examples" / "acp_demo.py"

# Make acp_demo importable without polluting global sys.path for other suites.
sys.path.insert(0, str(REPO_ROOT / "examples"))

import acp_demo

# ---------------------------------------------------------------------------
# frame() — JSON-RPC 2.0 builder that returns bytes
# ---------------------------------------------------------------------------


def test_frame_returns_bytes_with_trailing_newline():
    payload = acp_demo.frame({"jsonrpc": "2.0", "id": 0, "method": "initialize"})
    assert isinstance(payload, bytes)
    assert payload.endswith(b"\n")
    # Body before the trailing \n must be valid JSON
    json.loads(payload.rstrip(b"\n"))


def test_frame_is_single_line_plus_newline():
    payload = acp_demo.frame({"a": 1, "b": 2})
    # Strip trailing newline then check there are no other newlines in the body
    body = payload.rstrip(b"\n")
    assert b"\n" not in body, f"frame must be single-line, got {body!r}"


def test_frame_preserves_key_order():
    payload = acp_demo.frame({"b": 2, "a": 1})
    body = json.loads(payload.rstrip(b"\n"))
    # dict insertion order is preserved from Python 3.7+
    assert list(body.keys()) == ["b", "a"]


def test_frame_round_trips_nested_params():
    request = {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "session/prompt",
        "params": {
            "sessionId": "sess_abc",
            "prompt": [{"type": "text", "text": "hello"}],
        },
    }
    decoded = json.loads(acp_demo.frame(request).rstrip(b"\n"))
    assert decoded == request


# ---------------------------------------------------------------------------
# read_frame() — newline-delimited stdout parser (bytes stream)
# ---------------------------------------------------------------------------


def test_read_frame_parses_single_line_bytes():
    stream = io.BytesIO(b'{"jsonrpc":"2.0","id":0,"result":{"ok":true}}\n')
    frame = acp_demo.read_frame(stream, timeout=0.0)
    assert frame == {"jsonrpc": "2.0", "id": 0, "result": {"ok": True}}


def test_read_frame_returns_none_on_empty_stream():
    stream = io.BytesIO(b"")
    assert acp_demo.read_frame(stream, timeout=0.0) is None


def test_read_frame_returns_none_on_blank_line():
    stream = io.BytesIO(b"\n")
    assert acp_demo.read_frame(stream, timeout=0.0) is None


def test_read_frame_returns_none_on_malformed_json():
    # Malformed JSON is logged to stderr and read_frame returns None
    stream = io.BytesIO(b"not valid json\n")
    assert acp_demo.read_frame(stream, timeout=0.0) is None


# ---------------------------------------------------------------------------
# CLI smoke — no opencode binary required
# ---------------------------------------------------------------------------


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(DEMO_PATH), *args],
        capture_output=True,
        check=False,
        cwd=str(REPO_ROOT),
    )


def test_cli_help_exits_clean_and_mentions_modes():
    proc = _run_cli("--help")
    assert proc.returncode == 0
    # Help text should describe the no-prompt / dry-run escape hatches
    out = proc.stdout.decode("utf-8", errors="replace")
    assert "--no-prompt" in out
    assert "--dry-run" in out


def test_cli_dry_run_does_not_spawn_opencode():
    """--dry-run must short-circuit before any subprocess invocation.

    We assert by exit code 0 and the absence of `opencode` not-found errors
    on stderr (which would appear if it tried to spawn and the binary was
    missing from PATH).
    """
    proc = _run_cli("--dry-run")
    assert proc.returncode == 0, proc.stderr.decode("utf-8", errors="replace")
    err = proc.stderr.decode("utf-8", errors="replace").lower()
    assert "command not found" not in err
    assert "no such file" not in err


def test_cli_dry_run_emits_initial_frames_only_when_no_prompt():
    proc = _run_cli("--dry-run", "--no-prompt")
    assert proc.returncode == 0, proc.stderr.decode("utf-8", errors="replace")
    text = proc.stdout.decode("utf-8", errors="replace")
    # --dry-run prints one section per frame, with a header like "=== initialize ==="
    methods_in_order = [
        line.split("=== ", 1)[1].split(" ===")[0]
        for line in text.splitlines()
        if line.startswith("=== ") and line.endswith(" ===")
    ]
    # All three canonical frames are shown for documentation; --no-prompt
    # only prevents the prompt from being actually sent to a live server.
    assert methods_in_order == ["initialize", "session/new", "session/prompt"], (
        methods_in_order
    )


def test_cli_dry_run_help_text_mentions_no_prompt():
    """--no-prompt is the documented escape hatch for environments without
    an LLM provider. The help text must mention it so users can find it."""
    proc = _run_cli("--help")
    out = proc.stdout.decode("utf-8", errors="replace")
    assert "--no-prompt" in out