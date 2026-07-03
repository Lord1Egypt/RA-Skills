"""ACP session lifecycle manager.

Manages ACP session creation via session/new JSON-RPC requests,
maintains session ID mapping, and coordinates notification routing.
"""

import logging

from acp_openai_bridge.jsonrpc_writer import JSONRPCWriter
from acp_openai_bridge.acp_reader import ACPReader

logger = logging.getLogger(__name__)


class SessionManager:
    """ACP 会话管理器

    Coordinates session creation by sending session/new JSON-RPC requests
    through the JSONRPCWriter, waiting for the response via ACPReader,
    and registering the session queue for notification routing.
    """

    # Keywords indicating context window overflow in error messages
    CONTEXT_OVERFLOW_KEYWORDS = (
        "context", "token", "limit", "overflow", "too long",
        "maximum", "exceeded", "capacity", "truncat",
    )

    def __init__(self, writer: JSONRPCWriter, reader: ACPReader) -> None:
        self._writer = writer
        self._reader = reader
        self._session_id: str | None = None
        self._cwd: str | None = None

    def is_context_overflow_error(self, response: dict) -> bool:
        """判断 JSON-RPC 错误是否为上下文溢出。"""
        error = response.get("error", {})
        msg = (error.get("message", "") + " " + str(error.get("data", ""))).lower()
        return any(kw in msg for kw in self.CONTEXT_OVERFLOW_KEYWORDS)

    async def reset_session(self) -> str:
        """重建 session（上下文溢出时调用）。"""
        if self._session_id:
            self._reader.unregister_session(self._session_id)
        return await self.create_session(self._cwd)

    async def create_session(self, cwd: str) -> str:
        """创建新会话，返回 sessionId。

        Sends a session/new JSON-RPC request with the given cwd parameter,
        waits for the response containing the sessionId, registers the
        session queue in ACPReader for notification routing, and stores
        the session ID.

        Args:
            cwd: The current working directory to pass to the ACP backend.

        Returns:
            The sessionId string returned by the ACP backend.

        Raises:
            ConnectionError: If the ACP reader is stopped or subprocess exited.
            RuntimeError: If the response does not contain a valid sessionId.
        """
        self._cwd = cwd

        # Send session/new request and get the request id
        request_id = await self._writer.send_request("session/new", {"cwd": cwd, "mcpServers": []})

        # Register the request so ACPReader routes the response to our Future
        future = self._reader.register_request(request_id)

        # Wait for the JSON-RPC response
        response = await future

        # Extract sessionId from the response result
        result = response.get("result", {})
        session_id = result.get("sessionId")

        if not session_id:
            raise RuntimeError(
                f"session/new response missing sessionId: {response}"
            )

        # Register the session queue in ACPReader for notification routing
        self._reader.register_session(session_id)

        # Store the session id
        self._session_id = session_id
        logger.info("Created ACP session: %s", session_id)

        return session_id

    @property
    def session_id(self) -> str:
        """获取当前会话 ID。

        Returns:
            The current active session ID.

        Raises:
            RuntimeError: If no session has been created yet.
        """
        if self._session_id is None:
            raise RuntimeError("No session has been created yet")
        return self._session_id
