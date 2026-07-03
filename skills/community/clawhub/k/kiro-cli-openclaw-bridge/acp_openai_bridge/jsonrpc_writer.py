"""JSON-RPC message writer for ACP subprocess stdin.

Provides thread-safe serialization and writing of JSON-RPC 2.0 requests
and notifications to the subprocess stdin pipe, with auto-incrementing
request IDs and asyncio.Lock protection.
"""

import asyncio
import json


class JSONRPCWriter:
    """JSON-RPC 消息写入器（线程安全）

    Uses asyncio.Lock to protect concurrent writes to the subprocess stdin,
    ensuring that only one message is written at a time.
    """

    def __init__(self, stdin: asyncio.StreamWriter) -> None:
        self._stdin = stdin
        self._lock = asyncio.Lock()
        self._next_id = 1

    async def send_request(self, method: str, params: dict) -> int:
        """发送 JSON-RPC 请求，返回请求 id。

        Constructs a JSON-RPC 2.0 request with an auto-incrementing integer id,
        serializes it as single-line JSON + newline, and writes it to stdin
        under lock protection.

        Args:
            method: The JSON-RPC method name (e.g. "initialize", "session/new").
            params: The parameters dict for the method call.

        Returns:
            The integer id assigned to this request.
        """
        request_id = self._next_id
        self._next_id += 1

        message = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id,
        }

        data = self._serialize(message)
        async with self._lock:
            self._stdin.write(data)
            await self._stdin.drain()

        return request_id

    async def send_notification(self, method: str, params: dict) -> None:
        """发送 JSON-RPC 通知（无 id）。

        Constructs a JSON-RPC 2.0 notification (no id field), serializes it
        as single-line JSON + newline, and writes it to stdin under lock
        protection.

        Args:
            method: The JSON-RPC method name.
            params: The parameters dict for the notification.
        """
        message = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        }

        data = self._serialize(message)
        async with self._lock:
            self._stdin.write(data)
            await self._stdin.drain()

    def _serialize(self, message: dict) -> bytes:
        """序列化为单行 JSON + 换行符。

        Args:
            message: The JSON-RPC message dict to serialize.

        Returns:
            The message serialized as a single-line JSON byte string
            followed by a newline character.
        """
        return (json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
