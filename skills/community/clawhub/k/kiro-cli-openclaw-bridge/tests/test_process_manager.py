"""Unit tests for ProcessManager module."""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from acp_openai_bridge.process_manager import ProcessManager


def _make_mock_process(
    init_response: dict | None = None,
    returncode: int | None = None,
) -> MagicMock:
    """Create a mock asyncio.subprocess.Process with stdin/stdout pipes.

    Args:
        init_response: The JSON-RPC response to feed into stdout.
            Defaults to a successful initialize response.
        returncode: The process returncode. None means still running.
    """
    if init_response is None:
        init_response = {
            "jsonrpc": "2.0",
            "result": {"protocolVersion": 1, "serverInfo": {"name": "kiro-cli"}},
            "id": 1,
        }

    stdout = asyncio.StreamReader()
    stdout.feed_data((json.dumps(init_response) + "\n").encode("utf-8"))

    stdin = MagicMock()
    stdin.write = MagicMock()
    stdin.drain = AsyncMock()

    process = MagicMock()
    process.stdin = stdin
    process.stdout = stdout
    process.returncode = returncode
    process.terminate = MagicMock()
    process.kill = MagicMock()
    process.wait = AsyncMock(return_value=0)

    return process


@pytest.mark.asyncio
async def test_start_spawns_process_and_initializes():
    """start() should spawn the subprocess and complete the initialize handshake."""
    mock_process = _make_mock_process()

    with patch("acp_openai_bridge.process_manager.asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_process

        pm = ProcessManager("/usr/bin/kiro-cli", "/home/user/project")
        await pm.start()

        # Verify subprocess was spawned with correct args
        mock_exec.assert_called_once_with(
            "/usr/bin/kiro-cli",
            "acp",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            cwd="/home/user/project",
        )

        # Verify state
        assert pm.is_available is True
        assert pm.reader is not None
        assert pm.writer is not None

        # Verify initialize request was written to stdin
        mock_process.stdin.write.assert_called_once()
        written_data = mock_process.stdin.write.call_args[0][0]
        written_msg = json.loads(written_data.decode("utf-8").strip())
        assert written_msg["method"] == "initialize"
        assert written_msg["params"]["protocolVersion"] == 1
        assert written_msg["params"]["clientInfo"]["name"] == "acp-openai-bridge"
        assert written_msg["params"]["clientInfo"]["version"] == "1.0.0"
        assert written_msg["params"]["clientCapabilities"] == {}
        assert written_msg["jsonrpc"] == "2.0"

        await pm.shutdown()


@pytest.mark.asyncio
async def test_shutdown_terminates_process():
    """shutdown() should stop the reader and terminate the subprocess."""
    mock_process = _make_mock_process()

    with patch("acp_openai_bridge.process_manager.asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_process

        pm = ProcessManager("/usr/bin/kiro-cli", "/tmp")
        await pm.start()
        assert pm.is_available is True

        await pm.shutdown()

        assert pm.is_available is False
        mock_process.terminate.assert_called_once()


@pytest.mark.asyncio
async def test_properties_raise_when_not_started():
    """reader and writer properties should raise RuntimeError when not started."""
    pm = ProcessManager("/usr/bin/kiro-cli", "/tmp")

    with pytest.raises(RuntimeError, match="not available"):
        _ = pm.reader

    with pytest.raises(RuntimeError, match="not available"):
        _ = pm.writer

    assert pm.is_available is False


@pytest.mark.asyncio
async def test_ensure_available_no_restart_when_running():
    """ensure_available() should not restart if the process is still running."""
    mock_process = _make_mock_process()

    with patch("acp_openai_bridge.process_manager.asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_process

        pm = ProcessManager("/usr/bin/kiro-cli", "/tmp")
        await pm.start()

        # Process is still running (returncode is None)
        assert mock_process.returncode is None

        await pm.ensure_available()

        # Should only have been called once (during start)
        assert mock_exec.call_count == 1

        await pm.shutdown()


@pytest.mark.asyncio
async def test_ensure_available_restarts_after_crash():
    """ensure_available() should restart the process if it has exited."""
    init_response = {
        "jsonrpc": "2.0",
        "result": {"protocolVersion": 1},
        "id": 1,
    }

    # First process: will be started, then simulate crash
    first_process = _make_mock_process(init_response)
    # Second process: will be started on restart
    second_process = _make_mock_process(init_response)

    call_count = 0

    async def mock_create_subprocess(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return first_process
        return second_process

    with patch("acp_openai_bridge.process_manager.asyncio.create_subprocess_exec", side_effect=mock_create_subprocess):
        pm = ProcessManager("/usr/bin/kiro-cli", "/tmp")
        await pm.start()
        assert pm.is_available is True

        # Simulate process crash by setting returncode
        first_process.returncode = 1

        await pm.ensure_available()

        # Should have spawned a second process
        assert call_count == 2
        assert pm.is_available is True

        await pm.shutdown()


@pytest.mark.asyncio
async def test_ensure_available_starts_when_never_started():
    """ensure_available() should start the process if it was never started."""
    mock_process = _make_mock_process()

    with patch("acp_openai_bridge.process_manager.asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_process

        pm = ProcessManager("/usr/bin/kiro-cli", "/tmp")
        assert pm.is_available is False

        await pm.ensure_available()

        assert pm.is_available is True
        mock_exec.assert_called_once()

        await pm.shutdown()


@pytest.mark.asyncio
async def test_start_fails_on_initialize_error():
    """start() should raise RuntimeError if the initialize handshake returns an error."""
    error_response = {
        "jsonrpc": "2.0",
        "error": {"code": -32600, "message": "Invalid request"},
        "id": 1,
    }
    mock_process = _make_mock_process(init_response=error_response)

    with patch("acp_openai_bridge.process_manager.asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = mock_process

        pm = ProcessManager("/usr/bin/kiro-cli", "/tmp")

        with pytest.raises(RuntimeError, match="handshake failed"):
            await pm.start()

        assert pm.is_available is False
