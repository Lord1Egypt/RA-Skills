"""Tests for the SSEEmitter module."""

import asyncio
import json

import pytest

from acp_openai_bridge.sse_emitter import SSEEmitter


def _parse_sse_chunk(chunk: str) -> dict:
    """Parse an SSE data line into a dict."""
    assert chunk.startswith("data: ")
    assert chunk.endswith("\n\n")
    return json.loads(chunk.removeprefix("data: ").strip())


def _make_notification(text: str) -> dict:
    """Create a queue notification item matching the ACP format."""
    return {
        "sessionId": "test-session",
        "update": {
            "type": "agent_message_chunk",
            "chunk": {
                "text": text,
            },
        },
    }


def _make_response_message(stop_reason: str = "end_turn") -> dict:
    """Create a JSON-RPC response dict for session/prompt."""
    return {
        "jsonrpc": "2.0",
        "result": {
            "sessionId": "test-session",
            "stopReason": stop_reason,
        },
        "id": 3,
    }


class TestSSEEmitterFirstChunk:
    """Tests that the first SSE chunk contains role: assistant."""

    @pytest.mark.asyncio
    async def test_first_chunk_has_role_assistant(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        # Immediately resolve the future so the stream ends quickly
        future.set_result(_make_response_message())

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        # First chunk should have role=assistant
        first = _parse_sse_chunk(chunks[0])
        assert first["choices"][0]["delta"]["role"] == "assistant"
        assert first["choices"][0]["delta"]["content"] == ""
        assert first["choices"][0]["finish_reason"] is None

    @pytest.mark.asyncio
    async def test_first_chunk_has_correct_request_id(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        future.set_result(_make_response_message())

        emitter = SSEEmitter(queue, "chatcmpl-xyz", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        first = _parse_sse_chunk(chunks[0])
        assert first["id"] == "chatcmpl-xyz"


class TestSSEEmitterContentChunks:
    """Tests that content chunks are correctly streamed."""

    @pytest.mark.asyncio
    async def test_single_content_chunk(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        # Put a notification in the queue, then resolve the future
        await queue.put(_make_notification("Hello"))

        async def _resolve_after_drain():
            # Give the emitter time to process the queue item
            await asyncio.sleep(0.05)
            future.set_result(_make_response_message())

        asyncio.ensure_future(_resolve_after_drain())

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        # chunks[0] = first chunk (role), chunks[1] = content, chunks[2] = finish, chunks[3] = [DONE]
        content_chunk = _parse_sse_chunk(chunks[1])
        assert content_chunk["choices"][0]["delta"]["content"] == "Hello"

    @pytest.mark.asyncio
    async def test_multiple_content_chunks(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        await queue.put(_make_notification("Hello"))
        await queue.put(_make_notification(", "))
        await queue.put(_make_notification("world!"))

        async def _resolve_after_drain():
            await asyncio.sleep(0.1)
            future.set_result(_make_response_message())

        asyncio.ensure_future(_resolve_after_drain())

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        # Extract content from all non-first, non-final chunks
        content_texts = []
        for c in chunks[1:]:
            if c.startswith("data: [DONE]"):
                continue
            parsed = _parse_sse_chunk(c)
            delta = parsed["choices"][0]["delta"]
            if "content" in delta:
                content_texts.append(delta["content"])

        assert "Hello" in content_texts
        assert ", " in content_texts
        assert "world!" in content_texts


class TestSSEEmitterFinish:
    """Tests for the finish chunk and [DONE] sentinel."""

    @pytest.mark.asyncio
    async def test_finish_chunk_has_stop_reason(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        future.set_result(_make_response_message("end_turn"))

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        # Second-to-last chunk should have finish_reason
        finish_chunk = _parse_sse_chunk(chunks[-2])
        assert finish_chunk["choices"][0]["finish_reason"] == "stop"

    @pytest.mark.asyncio
    async def test_finish_chunk_maps_max_tokens(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        future.set_result(_make_response_message("max_tokens"))

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        finish_chunk = _parse_sse_chunk(chunks[-2])
        assert finish_chunk["choices"][0]["finish_reason"] == "length"

    @pytest.mark.asyncio
    async def test_done_sentinel_is_last(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        future.set_result(_make_response_message())

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        assert chunks[-1] == "data: [DONE]\n\n"

    @pytest.mark.asyncio
    async def test_stream_ends_on_none_sentinel(self):
        """When the queue receives None (reader shutdown), stream should end."""
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        await queue.put(_make_notification("partial"))
        await queue.put(None)  # sentinel

        # Resolve future so final chunk can be emitted
        future.set_result(_make_response_message())

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        # Should still have first chunk, content, finish, and [DONE]
        assert chunks[-1] == "data: [DONE]\n\n"


class TestSSEEmitterIgnoresNonChunkNotifications:
    """Tests that non-agent_message_chunk notifications are ignored."""

    @pytest.mark.asyncio
    async def test_ignores_unknown_update_type(self):
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        # Put a notification with a different type
        await queue.put({
            "sessionId": "test-session",
            "update": {
                "type": "tool_use",
                "chunk": {"text": "should be ignored"},
            },
        })
        await queue.put(_make_notification("visible"))

        async def _resolve():
            await asyncio.sleep(0.05)
            future.set_result(_make_response_message())

        asyncio.ensure_future(_resolve())

        emitter = SSEEmitter(queue, "chatcmpl-test", future)
        chunks = []
        async for chunk in emitter.stream():
            chunks.append(chunk)

        # Only "visible" should appear as content, not "should be ignored"
        content_texts = []
        for c in chunks:
            if c.startswith("data: [DONE]"):
                continue
            parsed = _parse_sse_chunk(c)
            delta = parsed["choices"][0]["delta"]
            if "content" in delta and delta["content"]:
                content_texts.append(delta["content"])

        assert "visible" in content_texts
        assert "should be ignored" not in content_texts
