"""Tests for the API routes module.

Uses FastAPI TestClient with mocked ProcessManager and SessionManager
to test the /v1/chat/completions, /v1/models, and /health endpoints.
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from acp_openai_bridge.config import BridgeConfig
from acp_openai_bridge.routes import router


def _create_app(
    process_manager=None,
    session_manager=None,
    config=None,
) -> FastAPI:
    """Create a FastAPI app with mocked state for testing."""
    app = FastAPI()
    app.include_router(router)

    if config is None:
        config = BridgeConfig()

    app.state.process_manager = process_manager or MagicMock()
    app.state.session_manager = session_manager or MagicMock()
    app.state.config = config

    return app


def _make_process_manager(
    is_available: bool = True,
    session_queue: asyncio.Queue | None = None,
) -> MagicMock:
    """Create a mock ProcessManager."""
    pm = MagicMock()
    pm.is_available = is_available
    pm.ensure_available = AsyncMock()

    # Mock writer
    writer = MagicMock()
    writer.send_request = AsyncMock(return_value=42)
    pm.writer = writer

    # Mock reader
    reader = MagicMock()
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    reader.register_request = MagicMock(return_value=future)
    reader.get_session_queue = MagicMock(return_value=session_queue)
    pm.reader = reader

    return pm


def _make_session_manager(session_id: str = "test-session-123") -> MagicMock:
    """Create a mock SessionManager."""
    sm = MagicMock()
    sm.session_id = session_id
    return sm


class TestListModels:
    """Tests for GET /v1/models endpoint."""

    def test_returns_model_list(self):
        app = _create_app()
        client = TestClient(app)
        response = client.get("/v1/models")

        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "list"
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == "kiro-acp"
        assert data["data"][0]["object"] == "model"
        assert data["data"][0]["owned_by"] == "kiro"
        assert "created" in data["data"][0]

    def test_model_created_is_integer(self):
        app = _create_app()
        client = TestClient(app)
        response = client.get("/v1/models")

        data = response.json()
        assert isinstance(data["data"][0]["created"], int)


class TestHealthCheck:
    """Tests for GET /health endpoint."""

    def test_health_ok_when_available(self):
        pm = MagicMock()
        pm.is_available = True
        app = _create_app(process_manager=pm)
        client = TestClient(app)

        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["acp_available"] is True

    def test_health_degraded_when_unavailable(self):
        pm = MagicMock()
        pm.is_available = False
        app = _create_app(process_manager=pm)
        client = TestClient(app)

        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "degraded"
        assert data["acp_available"] is False


class TestChatCompletionsErrors:
    """Tests for error handling in POST /v1/chat/completions."""

    def test_invalid_json_returns_400(self):
        pm = MagicMock()
        pm.ensure_available = AsyncMock()
        app = _create_app(process_manager=pm)
        client = TestClient(app)

        response = client.post(
            "/v1/chat/completions",
            content=b"not valid json{{{",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert data["error"]["type"] == "invalid_request_error"

    def test_missing_messages_returns_400(self):
        pm = MagicMock()
        pm.ensure_available = AsyncMock()
        sm = _make_session_manager()
        app = _create_app(process_manager=pm, session_manager=sm)
        client = TestClient(app)

        response = client.post(
            "/v1/chat/completions",
            json={"model": "kiro-acp"},
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert data["error"]["type"] == "invalid_request_error"

    def test_empty_messages_returns_400(self):
        pm = MagicMock()
        pm.ensure_available = AsyncMock()
        sm = _make_session_manager()
        app = _create_app(process_manager=pm, session_manager=sm)
        client = TestClient(app)

        response = client.post(
            "/v1/chat/completions",
            json={"model": "kiro-acp", "messages": []},
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_subprocess_unavailable_returns_502(self):
        pm = MagicMock()
        pm.ensure_available = AsyncMock(side_effect=RuntimeError("subprocess crashed"))
        app = _create_app(process_manager=pm)
        client = TestClient(app)

        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "kiro-acp",
                "messages": [{"role": "user", "content": "hello"}],
            },
        )
        assert response.status_code == 502
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "backend_unavailable"


class TestChatCompletionsNonStreaming:
    """Tests for non-streaming POST /v1/chat/completions."""

    @pytest.mark.asyncio
    async def test_non_streaming_returns_chat_completion(self):
        """Test that a non-streaming request returns a full chat completion."""
        queue = asyncio.Queue()
        # Put some notification chunks
        await queue.put({
            "sessionId": "test-session-123",
            "update": {
                "type": "agent_message_chunk",
                "chunk": {"text": "Hello "},
            },
        })
        await queue.put({
            "sessionId": "test-session-123",
            "update": {
                "type": "agent_message_chunk",
                "chunk": {"text": "world!"},
            },
        })

        pm = MagicMock()
        pm.ensure_available = AsyncMock()
        writer = MagicMock()
        writer.send_request = AsyncMock(return_value=42)
        pm.writer = writer

        reader = MagicMock()

        # We need a real event loop future
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        reader.register_request = MagicMock(return_value=future)
        reader.get_session_queue = MagicMock(return_value=queue)
        pm.reader = reader

        sm = _make_session_manager()
        config = BridgeConfig(request_timeout=5.0)

        app = _create_app(process_manager=pm, session_manager=sm, config=config)

        # Resolve the future after a short delay
        async def _resolve():
            await asyncio.sleep(0.1)
            future.set_result({
                "jsonrpc": "2.0",
                "result": {
                    "sessionId": "test-session-123",
                    "stopReason": "end_turn",
                },
                "id": 42,
            })

        asyncio.ensure_future(_resolve())

        # Use httpx AsyncClient for async test
        from httpx import AsyncClient, ASGITransport

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/v1/chat/completions",
                json={
                    "model": "kiro-acp",
                    "messages": [{"role": "user", "content": "hi"}],
                    "stream": False,
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "chat.completion"
        assert data["choices"][0]["message"]["role"] == "assistant"
        assert "Hello " in data["choices"][0]["message"]["content"]
        assert "world!" in data["choices"][0]["message"]["content"]
        assert data["choices"][0]["finish_reason"] == "stop"

    @pytest.mark.asyncio
    async def test_non_streaming_json_rpc_error_returns_500(self):
        """Test that a JSON-RPC error response returns HTTP 500."""
        queue = asyncio.Queue()

        pm = MagicMock()
        pm.ensure_available = AsyncMock()
        writer = MagicMock()
        writer.send_request = AsyncMock(return_value=42)
        pm.writer = writer

        reader = MagicMock()
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        reader.register_request = MagicMock(return_value=future)
        reader.get_session_queue = MagicMock(return_value=queue)
        pm.reader = reader

        sm = _make_session_manager()
        config = BridgeConfig(request_timeout=5.0)

        app = _create_app(process_manager=pm, session_manager=sm, config=config)

        # Resolve with an error response
        async def _resolve():
            await asyncio.sleep(0.05)
            future.set_result({
                "jsonrpc": "2.0",
                "error": {"code": -32600, "message": "Invalid request"},
                "id": 42,
            })

        asyncio.ensure_future(_resolve())

        from httpx import AsyncClient, ASGITransport

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/v1/chat/completions",
                json={
                    "model": "kiro-acp",
                    "messages": [{"role": "user", "content": "hi"}],
                    "stream": False,
                },
            )

        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert "Invalid request" in data["error"]["message"]


class TestChatCompletionsStreaming:
    """Tests for streaming POST /v1/chat/completions."""

    @pytest.mark.asyncio
    async def test_streaming_returns_event_stream(self):
        """Test that a streaming request returns text/event-stream content type."""
        queue = asyncio.Queue()

        pm = MagicMock()
        pm.ensure_available = AsyncMock()
        writer = MagicMock()
        writer.send_request = AsyncMock(return_value=42)
        pm.writer = writer

        reader = MagicMock()
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        reader.register_request = MagicMock(return_value=future)
        reader.get_session_queue = MagicMock(return_value=queue)
        pm.reader = reader

        sm = _make_session_manager()
        config = BridgeConfig(request_timeout=5.0)

        app = _create_app(process_manager=pm, session_manager=sm, config=config)

        # Put a chunk and resolve
        await queue.put({
            "sessionId": "test-session-123",
            "update": {
                "type": "agent_message_chunk",
                "chunk": {"text": "Hi there"},
            },
        })

        async def _resolve():
            await asyncio.sleep(0.1)
            future.set_result({
                "jsonrpc": "2.0",
                "result": {"sessionId": "test-session-123", "stopReason": "end_turn"},
                "id": 42,
            })

        asyncio.ensure_future(_resolve())

        from httpx import AsyncClient, ASGITransport

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/v1/chat/completions",
                json={
                    "model": "kiro-acp",
                    "messages": [{"role": "user", "content": "hi"}],
                    "stream": True,
                },
            )

        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

        # Parse SSE events from the response body
        body = response.text
        events = [line for line in body.split("\n") if line.startswith("data: ")]
        assert len(events) >= 3  # first chunk, content, finish, [DONE]

        # First event should have role=assistant
        first_data = json.loads(events[0].removeprefix("data: "))
        assert first_data["choices"][0]["delta"]["role"] == "assistant"

        # Last event should be [DONE]
        assert events[-1] == "data: [DONE]"


class TestGlobalExceptionHandler:
    """Tests for the global exception handler registered in main.py's create_app."""

    def test_global_handler_catches_unhandled_route_exception(self):
        """Verify the global exception handler catches exceptions not handled by routes."""
        from acp_openai_bridge.main import create_app

        config = BridgeConfig()
        app = create_app(config)

        # Add a test route that raises an unhandled exception
        @app.get("/test-unhandled-error")
        async def raise_error():
            raise RuntimeError("Something completely unexpected")

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/test-unhandled-error")

        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert data["error"]["message"] == "Internal server error"
        assert data["error"]["type"] == "server_error"
        assert data["error"]["code"] == "internal_error"
