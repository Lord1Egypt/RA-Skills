"""Unit tests for ACPReader module."""

import asyncio
import json

import pytest

from acp_openai_bridge.acp_reader import ACPReader


def _make_stream(lines: list[str]) -> asyncio.StreamReader:
    """Create a StreamReader pre-loaded with the given lines."""
    reader = asyncio.StreamReader()
    for line in lines:
        reader.feed_data((line + "\n").encode("utf-8"))
    reader.feed_eof()
    return reader


@pytest.mark.asyncio
async def test_response_dispatched_to_future():
    """A JSON-RPC response (with id) should resolve the registered Future."""
    response = {"jsonrpc": "2.0", "result": {"sessionId": "s1"}, "id": 1}
    stream = _make_stream([json.dumps(response)])

    reader = ACPReader(stream)
    future = reader.register_request(1)
    reader.start()

    result = await asyncio.wait_for(future, timeout=2.0)
    assert result == response
    await reader.stop()


@pytest.mark.asyncio
async def test_notification_dispatched_to_queue():
    """A session/update notification should be pushed into the session queue."""
    notification = {
        "jsonrpc": "2.0",
        "method": "session/update",
        "params": {
            "sessionId": "abc-123",
            "update": {"type": "agent_message_chunk", "text": "Hello"},
        },
    }
    stream = _make_stream([json.dumps(notification)])

    reader = ACPReader(stream)
    queue = reader.register_session("abc-123")
    reader.start()

    params = await asyncio.wait_for(queue.get(), timeout=2.0)
    assert params["sessionId"] == "abc-123"
    assert params["update"]["text"] == "Hello"
    await reader.stop()


@pytest.mark.asyncio
async def test_invalid_json_skipped():
    """Invalid JSON lines should be skipped without affecting subsequent messages."""
    valid_response = {"jsonrpc": "2.0", "result": {"ok": True}, "id": 42}
    stream = _make_stream([
        "this is not json",
        json.dumps(valid_response),
    ])

    reader = ACPReader(stream)
    future = reader.register_request(42)
    reader.start()

    result = await asyncio.wait_for(future, timeout=2.0)
    assert result == valid_response
    await reader.stop()


@pytest.mark.asyncio
async def test_eof_notifies_pending_futures():
    """When EOF is reached, all pending Futures should receive ConnectionError."""
    stream = asyncio.StreamReader()
    stream.feed_eof()

    reader = ACPReader(stream)
    future = reader.register_request(99)
    reader.start()

    with pytest.raises(ConnectionError):
        await asyncio.wait_for(future, timeout=2.0)
    await reader.stop()


@pytest.mark.asyncio
async def test_eof_notifies_session_queues():
    """When EOF is reached, session queues should receive a None sentinel."""
    stream = asyncio.StreamReader()
    stream.feed_eof()

    reader = ACPReader(stream)
    queue = reader.register_session("sess-1")
    reader.start()

    sentinel = await asyncio.wait_for(queue.get(), timeout=2.0)
    assert sentinel is None
    await reader.stop()


@pytest.mark.asyncio
async def test_multiple_responses_routed_correctly():
    """Multiple responses should be routed to their respective Futures by id."""
    resp1 = {"jsonrpc": "2.0", "result": {"data": "first"}, "id": 1}
    resp2 = {"jsonrpc": "2.0", "result": {"data": "second"}, "id": 2}
    stream = _make_stream([json.dumps(resp1), json.dumps(resp2)])

    reader = ACPReader(stream)
    future1 = reader.register_request(1)
    future2 = reader.register_request(2)
    reader.start()

    result1 = await asyncio.wait_for(future1, timeout=2.0)
    result2 = await asyncio.wait_for(future2, timeout=2.0)
    assert result1["result"]["data"] == "first"
    assert result2["result"]["data"] == "second"
    await reader.stop()


@pytest.mark.asyncio
async def test_unregister_session_stops_routing():
    """After unregistering a session, notifications for it should not be queued."""
    notification = {
        "jsonrpc": "2.0",
        "method": "session/update",
        "params": {"sessionId": "s1", "update": {"type": "agent_message_chunk"}},
    }
    stream = _make_stream([json.dumps(notification)])

    reader = ACPReader(stream)
    queue = reader.register_session("s1")
    reader.unregister_session("s1")
    reader.start()

    # Give the reader time to process
    await asyncio.sleep(0.1)

    assert queue.empty()
    await reader.stop()


@pytest.mark.asyncio
async def test_stop_cancels_read_task():
    """Calling stop() should cancel the background read task."""
    # Use a stream that never ends to test cancellation
    stream = asyncio.StreamReader()

    reader = ACPReader(stream)
    reader.start()

    # Verify the task is running
    assert reader._read_task is not None
    assert not reader._read_task.done()

    await reader.stop()

    # After stop, the task should be cleaned up
    assert reader._read_task is None
    assert reader._is_running is False


@pytest.mark.asyncio
async def test_register_request_returns_future():
    """register_request should return an asyncio.Future."""
    stream = asyncio.StreamReader()
    reader = ACPReader(stream)
    future = reader.register_request(1)
    assert isinstance(future, asyncio.Future)
    await reader.stop()


@pytest.mark.asyncio
async def test_register_session_returns_queue():
    """register_session should return an asyncio.Queue."""
    stream = asyncio.StreamReader()
    reader = ACPReader(stream)
    queue = reader.register_session("test-session")
    assert isinstance(queue, asyncio.Queue)
    await reader.stop()
