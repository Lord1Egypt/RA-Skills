"""ACP JSON-RPC to OpenAI response translator.

Converts ACP responses and notifications into OpenAI-compatible formats,
including chat completion responses, SSE chunks, stop reason mapping,
error responses, and token estimation.
"""

import json
import time


# ACP stopReason → OpenAI finish_reason mapping
_STOP_REASON_MAP: dict[str, str] = {
    "end_turn": "stop",
    "max_tokens": "length",
    "cancelled": "stop",
    "refused": "stop",
}


class ResponseTranslator:
    """ACP → OpenAI response translator."""

    @staticmethod
    def to_chat_completion(
        request_id: str,
        content: str,
        stop_reason: str,
        model: str = "kiro-acp",
    ) -> dict:
        """Construct a complete OpenAI chat completion response.

        Args:
            request_id: The unique request identifier (e.g. "chatcmpl-xxx").
            content: The full assistant reply text.
            stop_reason: The ACP stopReason value.
            model: The model name to include in the response.

        Returns:
            A dict matching the OpenAI chat completion response format.
        """
        finish_reason = ResponseTranslator.map_stop_reason(stop_reason)
        prompt_tokens = ResponseTranslator.estimate_tokens(content)
        completion_tokens = ResponseTranslator.estimate_tokens(content)
        return {
            "id": request_id,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content,
                    },
                    "finish_reason": finish_reason,
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }

    @staticmethod
    def to_sse_chunk(
        request_id: str,
        content: str | None = None,
        role: str | None = None,
        finish_reason: str | None = None,
        model: str = "kiro-acp",
    ) -> str:
        """Construct a single SSE chunk string in ``data: {...}\\n\\n`` format.

        Args:
            request_id: The unique request identifier.
            content: Optional text content for the delta.
            role: Optional role field for the delta (used in the first chunk).
            finish_reason: Optional finish reason (used in the final chunk).
            model: The model name to include in the chunk.

        Returns:
            A string formatted as ``data: <json>\\n\\n``.
        """
        delta: dict = {}
        if role is not None:
            delta["role"] = role
        if content is not None:
            delta["content"] = content

        chunk = {
            "id": request_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "delta": delta,
                    "index": 0,
                    "finish_reason": finish_reason,
                }
            ],
        }
        return f"data: {json.dumps(chunk)}\n\n"

    @staticmethod
    def map_stop_reason(acp_stop_reason: str) -> str:
        """Map an ACP stopReason to an OpenAI finish_reason.

        Mapping:
            - end_turn   → stop
            - max_tokens → length
            - cancelled  → stop
            - refused    → stop

        Unknown values default to ``stop``.

        Args:
            acp_stop_reason: The ACP stopReason string.

        Returns:
            The corresponding OpenAI finish_reason string.
        """
        return _STOP_REASON_MAP.get(acp_stop_reason, "stop")

    @staticmethod
    def to_error_response(
        message: str,
        error_type: str = "server_error",
        code: str | None = None,
    ) -> dict:
        """Construct an OpenAI-standard error response.

        Args:
            message: Human-readable error description.
            error_type: The error type category.
            code: Optional machine-readable error code.

        Returns:
            A dict matching the OpenAI error response format.
        """
        error: dict = {
            "message": message,
            "type": error_type,
            "code": code,
        }
        return {"error": error}

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate the number of tokens in a text string.

        Uses a simple approximation of ``len(text) / 4``.

        Args:
            text: The text to estimate tokens for.

        Returns:
            The estimated token count (minimum 0).
        """
        return max(0, len(text) // 4)
