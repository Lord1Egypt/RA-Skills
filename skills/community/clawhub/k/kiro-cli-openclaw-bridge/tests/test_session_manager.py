"""Unit tests for SessionManager module."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

from acp_openai_bridge.session_manager import SessionManager


@pytest.fixture
def mock_writer():
    """Create a mock JSONRPCWriter."""
    writer = AsyncMock()
    writer.send_request = AsyncMock(return_value=2)
    return writer


@pytest.fixture
def mock_reader():
    """Create a mock ACPReader."""
    reader = MagicMock()
    return reader


@pytest.fixture
def session_manager(mock_writer, mock_reader):
    """Create a SessionManager with mocked dependencies."""
    return SessionManager(writer=mock_writer, reader=mock_reader)


class TestSessionManagerCreateSession:
    """Tests for SessionManager.create_session()."""

    @pytest.mark.asyncio
    async def test_create_session_sends_session_new_request(
        self, session_manager, mock_writer, mock_reader
    ):
        """create_session sends session/new with cwd param."""
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {"sessionId": "abc-123"}, "id": 2})
        mock_reader.register_request.return_value = future

        await session_manager.create_session("/home/user/project")

        mock_writer.send_request.assert_awaited_once_with(
            "session/new", {"cwd": "/home/user/project"}
        )

    @pytest.mark.asyncio
    async def test_create_session_registers_request_with_correct_id(
        self, session_manager, mock_writer, mock_reader
    ):
        """create_session registers the request id returned by writer."""
        mock_writer.send_request.return_value = 5
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {"sessionId": "sess-42"}, "id": 5})
        mock_reader.register_request.return_value = future

        await session_manager.create_session("/tmp")

        mock_reader.register_request.assert_called_once_with(5)

    @pytest.mark.asyncio
    async def test_create_session_returns_session_id(
        self, session_manager, mock_reader
    ):
        """create_session returns the sessionId from the response."""
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {"sessionId": "xyz-789"}, "id": 2})
        mock_reader.register_request.return_value = future

        result = await session_manager.create_session("/workspace")

        assert result == "xyz-789"

    @pytest.mark.asyncio
    async def test_create_session_stores_session_id(
        self, session_manager, mock_reader
    ):
        """create_session stores the sessionId for later access."""
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {"sessionId": "stored-id"}, "id": 2})
        mock_reader.register_request.return_value = future

        await session_manager.create_session("/workspace")

        assert session_manager.session_id == "stored-id"

    @pytest.mark.asyncio
    async def test_create_session_registers_session_queue(
        self, session_manager, mock_reader
    ):
        """create_session registers the session in ACPReader for notifications."""
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {"sessionId": "notify-sess"}, "id": 2})
        mock_reader.register_request.return_value = future

        await session_manager.create_session("/workspace")

        mock_reader.register_session.assert_called_once_with("notify-sess")

    @pytest.mark.asyncio
    async def test_create_session_raises_on_missing_session_id(
        self, session_manager, mock_reader
    ):
        """create_session raises RuntimeError if response has no sessionId."""
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {}, "id": 2})
        mock_reader.register_request.return_value = future

        with pytest.raises(RuntimeError, match="missing sessionId"):
            await session_manager.create_session("/workspace")

    @pytest.mark.asyncio
    async def test_create_session_raises_on_empty_session_id(
        self, session_manager, mock_reader
    ):
        """create_session raises RuntimeError if sessionId is empty string."""
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {"sessionId": ""}, "id": 2})
        mock_reader.register_request.return_value = future

        with pytest.raises(RuntimeError, match="missing sessionId"):
            await session_manager.create_session("/workspace")

    @pytest.mark.asyncio
    async def test_create_session_propagates_connection_error(
        self, session_manager, mock_reader
    ):
        """create_session propagates ConnectionError from ACPReader."""
        future = asyncio.get_event_loop().create_future()
        future.set_exception(ConnectionError("ACP reader stopped"))
        mock_reader.register_request.return_value = future

        with pytest.raises(ConnectionError, match="ACP reader stopped"):
            await session_manager.create_session("/workspace")


class TestSessionManagerSessionIdProperty:
    """Tests for SessionManager.session_id property."""

    def test_session_id_raises_before_creation(self, session_manager):
        """session_id raises RuntimeError if no session created."""
        with pytest.raises(RuntimeError, match="No session has been created"):
            _ = session_manager.session_id

    @pytest.mark.asyncio
    async def test_session_id_returns_id_after_creation(
        self, session_manager, mock_reader
    ):
        """session_id returns the correct id after create_session."""
        future = asyncio.get_event_loop().create_future()
        future.set_result({"jsonrpc": "2.0", "result": {"sessionId": "my-session"}, "id": 2})
        mock_reader.register_request.return_value = future

        await session_manager.create_session("/workspace")

        assert session_manager.session_id == "my-session"
