# SPDX-License-Identifier: Apache-2.0
"""Tests for the ic-engine envelope-parsing seam in mcp_server._run_ic_engine.

This is the load-bearing parsing logic that determines whether structured
`ic_result` envelopes get extracted correctly from ic-engine's stdout.
If this is wrong, every MCP tool returns garbage to the agent.

We monkeypatch asyncio.create_subprocess_exec to feed canned stdout
samples and verify the envelope detection + narrative split.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bridge"))

from investorclaw_bridge import mcp_server  # noqa: E402


class FakeProcess:
    """Stand-in for asyncio.subprocess.Process — feeds canned output."""

    def __init__(self, stdout: bytes, stderr: bytes = b"", returncode: int = 0):
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = returncode

    async def communicate(self) -> tuple[bytes, bytes]:
        return self._stdout, self._stderr

    def kill(self) -> None:
        pass


def _patched_subprocess_exec(stdout: bytes, returncode: int = 0):
    """Return a context-manager-style patch for asyncio.create_subprocess_exec."""
    fake = FakeProcess(stdout, returncode=returncode)
    return patch(
        "asyncio.create_subprocess_exec",
        new=AsyncMock(return_value=fake),
    )


def _patch_binary_present() -> None:
    """Helper: pretend the IC_ENGINE_BIN exists so _run_ic_engine doesn't bail."""
    pass  # Path.exists() check uses real FS — see test fixture below


@pytest.fixture
def fake_ic_bin(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Create a fake ic-engine binary at a known path so existence check passes."""
    binary = tmp_path / "investorclaw"
    binary.write_text("#!/bin/sh\necho fake\n")
    binary.chmod(0o755)
    monkeypatch.setattr(mcp_server, "IC_ENGINE_BIN", str(binary))
    return binary


def test_run_ic_engine_extracts_envelope(fake_ic_bin: Path) -> None:
    """Stdout with a trailing `{"ic_result": ...}` line — envelope extracted."""
    stdout = (
        b"Portfolio Summary\n"
        b"Total Value: $2,640,740\n"
        b"Top Holdings: MSFT, NVDA, AAPL\n"
        b'{"ic_result": {"script": "ask.py", "exit_code": 0, "duration_ms": 648}}\n'
    )
    with _patched_subprocess_exec(stdout, returncode=0):
        result = asyncio.run(mcp_server._run_ic_engine(["ask", "what is in my portfolio?"]))

    assert result["exit_code"] == 0
    assert result["ic_result"] is not None
    assert result["ic_result"]["ic_result"]["script"] == "ask.py"
    assert result["ic_result"]["ic_result"]["exit_code"] == 0
    # Narrative is everything BEFORE the envelope line
    assert "Portfolio Summary" in result["narrative"]
    assert "Total Value: $2,640,740" in result["narrative"]
    assert "ic_result" not in result["narrative"]


def test_run_ic_engine_handles_missing_envelope(fake_ic_bin: Path) -> None:
    """If ic-engine emits no envelope, ic_result is None and narrative = full stdout."""
    stdout = b"Some plain output\nNo envelope here\n"
    with _patched_subprocess_exec(stdout, returncode=0):
        result = asyncio.run(mcp_server._run_ic_engine(["ask", "x"]))

    assert result["exit_code"] == 0
    assert result["ic_result"] is None
    assert "Some plain output" in result["narrative"]


def test_run_ic_engine_propagates_nonzero_exit(fake_ic_bin: Path) -> None:
    """Non-zero exit + no envelope → exit_code reflected; ic_result None."""
    stdout = b"command failed: missing portfolio\n"
    with _patched_subprocess_exec(stdout, returncode=1):
        result = asyncio.run(mcp_server._run_ic_engine(["ask", "x"]))

    assert result["exit_code"] == 1
    assert result["ic_result"] is None


def test_run_ic_engine_handles_envelope_with_narrative_after(fake_ic_bin: Path) -> None:
    """Envelope NOT on the last line — handled gracefully (still found via reverse scan)."""
    stdout = (
        b"Header\n"
        b'{"ic_result": {"script": "holdings.py", "exit_code": 0}}\n'
        b"trailing whitespace\n"
        b"\n"
    )
    with _patched_subprocess_exec(stdout, returncode=0):
        result = asyncio.run(mcp_server._run_ic_engine(["ask", "x"]))

    assert result["ic_result"] is not None
    assert result["ic_result"]["ic_result"]["script"] == "holdings.py"


def test_run_ic_engine_ignores_malformed_envelope(fake_ic_bin: Path) -> None:
    """A line that LOOKS like an envelope but is malformed JSON is ignored."""
    stdout = b'Real output\n{"ic_result": malformed because of this}\n'
    with _patched_subprocess_exec(stdout, returncode=0):
        result = asyncio.run(mcp_server._run_ic_engine(["ask", "x"]))

    # Malformed envelope is not extracted
    assert result["ic_result"] is None
    # Full stdout preserved as narrative
    assert "Real output" in result["narrative"]


def test_run_ic_engine_handles_unicode(fake_ic_bin: Path) -> None:
    """Non-ASCII output (emoji, accents) decodes cleanly."""
    stdout = (
        "📊 Portfolio (2,640,740 USD)\n"
        '{"ic_result": {"script": "ask.py", "exit_code": 0}}\n'
    ).encode("utf-8")
    with _patched_subprocess_exec(stdout, returncode=0):
        result = asyncio.run(mcp_server._run_ic_engine(["ask", "x"]))

    assert result["ic_result"] is not None
    assert "📊" in result["narrative"]


def test_health_check_reports_bin_status(fake_ic_bin: Path) -> None:
    h = mcp_server.health_check()
    assert h["status"] == "ok"
    assert h["ic_engine_bin_found"] is True


def test_health_check_degraded_when_bin_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    # Post-reorg (2026-05-02): IC_ENGINE_BIN lives in mcp._runtime; the
    # mcp_server shim re-exports it but health_check() reads the canonical
    # value from _runtime. Patch there so health_check sees the override.
    # Also monkeypatch shutil.which because health_check falls back to a
    # PATH-lookup of "investorclaw"; pytest under the ic-engine venv
    # finds the binary on PATH, which would otherwise mask the degraded
    # signal even when the explicit IC_ENGINE_BIN is missing.
    from investorclaw_bridge.mcp import _runtime
    monkeypatch.setattr(_runtime, "IC_ENGINE_BIN", "/nonexistent/path/investorclaw")
    monkeypatch.setattr(_runtime.shutil, "which", lambda _: None)
    h = mcp_server.health_check()
    assert h["status"] == "degraded"
    assert h["ic_engine_bin_found"] is False
