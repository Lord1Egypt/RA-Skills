"""Server-Sent Events emitter for streaming responses.

Converts ACP session/update notifications into OpenAI SSE chat.completion.chunk
format, managing the async generator lifecycle from first chunk through
finish_reason and [DONE] sentinel.
"""

import asyncio
import logging
from collections.abc import AsyncGenerator

from acp_openai_bridge.response_translator import ResponseTranslator

logger = logging.getLogger(__name__)


def _extract_chunk_text(item: dict) -> str:
    """Extract text from an ACP session/update notification item.

    Handles both the actual Kiro format and the ACP spec format:
    - Kiro:  {"update": {"sessionUpdate": "agent_message_chunk", "content": {"type": "text", "text": "..."}}}
    - Spec:  {"update": {"type": "agent_message_chunk", "chunk": {"text": "..."}}}

    Returns empty string if the item is not an agent_message_chunk or has no text.
    """
    update = item.get("update", {})
    # Check both field names for the update type
    update_type = update.get("sessionUpdate") or update.get("type", "")
    if update_type != "agent_message_chunk":
        return ""
    # Try Kiro format first: content.text
    content = update.get("content", {})
    if isinstance(content, dict):
        text = content.get("text", "")
        if text:
            return text
    # Fallback to spec format: chunk.text
    chunk = update.get("chunk", {})
    if isinstance(chunk, dict):
        return chunk.get("text", "")
    return ""


class SSEEmitter:
    """ACP 通知 → OpenAI SSE 流转换器。

    Consumes ACP ``session/update`` notification params from an
    ``asyncio.Queue`` and yields OpenAI-compatible SSE chunk strings.

    The emitter simultaneously monitors the queue (for streaming chunks)
    and a response Future (for the final ``session/prompt`` result) using
    ``asyncio.wait`` with ``FIRST_COMPLETED``.

    Args:
        queue: An asyncio.Queue that receives notification params dicts
            from the ACPReader.  A ``None`` sentinel signals reader shutdown.
        request_id: The OpenAI-style request id (e.g. ``"chatcmpl-xxx"``).
        response_future: An asyncio.Future that resolves with the
            ``session/prompt`` JSON-RPC response dict.
    """

    def __init__(
        self,
        queue: asyncio.Queue,
        request_id: str,
        response_future: asyncio.Future,
    ) -> None:
        self._queue = queue
        self._request_id = request_id
        self._response_future = response_future
        self._is_first_chunk = True

    async def stream(self) -> AsyncGenerator[str, None]:
        """Async generator that yields OpenAI SSE chunk strings.

        Flow:
        1. Yield the first chunk containing ``role: assistant`` and empty
           content.
        2. Loop: use ``asyncio.wait`` to monitor both a ``queue.get()``
           task and the ``response_future``.
           - Queue item with ``agent_message_chunk``: extract text, yield
             SSE chunk.
           - Queue item is ``None`` (sentinel): break.
           - ``response_future`` done: break.
        3. After loop: extract ``stopReason`` from the response, map it to
           an OpenAI ``finish_reason``, yield the final chunk, then yield
           ``data: [DONE]\\n\\n``.
        """
        # 1. Send the first chunk with role=assistant
        yield ResponseTranslator.to_sse_chunk(
            request_id=self._request_id,
            content="",
            role="assistant",
        )
        self._is_first_chunk = False

        # 2. Stream loop — simultaneously watch queue and response_future
        while True:
            queue_task = asyncio.ensure_future(self._queue.get())

            # Build the set of awaitables.  If the response future is
            # already done we still enter the loop once to drain any
            # remaining queued chunks before emitting the final events.
            pending = {queue_task}
            if not self._response_future.done():
                pending.add(self._response_future)

            done, _ = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED,
            )

            # --- Handle queue item ---
            if queue_task in done:
                item = queue_task.result()

                if item is None:
                    # Sentinel — reader stopped
                    logger.debug("SSEEmitter received None sentinel, ending stream")
                    break

                # Extract text from agent_message_chunk notifications
                text = _extract_chunk_text(item)
                if text:
                    yield ResponseTranslator.to_sse_chunk(
                        request_id=self._request_id,
                        content=text,
                    )
                # Other notification types are silently ignored
            else:
                # queue_task was not completed — cancel it so it doesn't
                # linger and consume the next queue item.
                queue_task.cancel()

            # --- Check if response_future completed ---
            if self._response_future.done():
                # Drain any remaining items already in the queue before
                # sending the final chunk.
                while not self._queue.empty():
                    item = self._queue.get_nowait()
                    if item is None:
                        break
                    text = _extract_chunk_text(item)
                    if text:
                        yield ResponseTranslator.to_sse_chunk(
                            request_id=self._request_id,
                            content=text,
                        )
                break

        # 3. Check for error in response and send final chunk
        error_message = self._get_error_message()
        if error_message:
            # Send error as a content chunk so the client sees it
            yield ResponseTranslator.to_sse_chunk(
                request_id=self._request_id,
                content=f"\n\n[Error from backend: {error_message}]",
            )
            yield ResponseTranslator.to_sse_chunk(
                request_id=self._request_id,
                finish_reason="stop",
            )
        else:
            stop_reason = self._get_stop_reason()
            finish_reason = ResponseTranslator.map_stop_reason(stop_reason)
            yield ResponseTranslator.to_sse_chunk(
                request_id=self._request_id,
                finish_reason=finish_reason,
            )
        yield "data: [DONE]\n\n"

    def _get_error_message(self) -> str | None:
        """Extract error message from the response future if it's an error response.

        Returns the error message string, or None if the response is not an error.
        """
        if not self._response_future.done():
            return None
        try:
            result = self._response_future.result()
        except Exception:
            return "Backend connection lost"
        if isinstance(result, dict) and "error" in result:
            err = result["error"]
            msg = err.get("message", "Unknown error")
            data = err.get("data", "")
            return f"{msg}: {data}" if data else msg
        return None

    def _get_stop_reason(self) -> str:
        """Extract the ACP stopReason from the response future result.

        Returns ``"end_turn"`` as a safe default if the future is not done
        or the result does not contain a stopReason.
        """
        if not self._response_future.done():
            return "end_turn"

        try:
            result = self._response_future.result()
        except Exception:
            logger.warning("response_future raised an exception", exc_info=True)
            return "end_turn"

        # The future result is the full JSON-RPC response dict:
        # {"jsonrpc": "2.0", "result": {"sessionId": "...", "stopReason": "..."}, "id": N}
        if isinstance(result, dict):
            return result.get("result", {}).get("stopReason", "end_turn")

        return "end_turn"
