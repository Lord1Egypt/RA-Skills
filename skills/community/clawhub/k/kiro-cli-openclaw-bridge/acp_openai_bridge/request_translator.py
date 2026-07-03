"""OpenAI request to ACP JSON-RPC translator.

Extracts user messages from OpenAI chat completion requests and constructs
ACP session/prompt JSON-RPC parameters. Handles both streaming and
non-streaming request modes.
"""

import logging
from dataclasses import dataclass
from uuid import uuid4

logger = logging.getLogger(__name__)


@dataclass
class TranslatedRequest:
    """Translated request ready for ACP session/prompt."""

    session_id: str
    content: list[dict]  # [{"type": "text", "text": "..."}]
    is_stream: bool
    request_id: str  # for OpenAI response id (chatcmpl-<uuid>)


class RequestTranslator:
    """OpenAI → ACP request translator."""

    @staticmethod
    def translate(openai_request: dict, session_id: str) -> TranslatedRequest:
        """Translate an OpenAI chat completion request into ACP session/prompt parameters.

        Args:
            openai_request: The parsed OpenAI chat completion request body.
            session_id: The current ACP session ID.

        Returns:
            A TranslatedRequest containing the ACP-compatible parameters.

        Raises:
            ValueError: If messages field is missing or empty.
        """
        messages = openai_request.get("messages")
        if not messages:
            raise ValueError("messages field is missing or empty")

        # Log incoming request details for debugging
        logger.info(
            "Incoming request: %d messages, roles=%s",
            len(messages),
            [m.get("role") for m in messages],
        )
        for i, msg in enumerate(messages):
            content = msg.get("content") or ""
            content_len = len(content) if isinstance(content, str) else sum(
                len(b.get("text", "")) for b in content if isinstance(b, dict)
            )
            logger.debug(
                "  msg[%d] role=%s len=%d preview=%.200s",
                i, msg.get("role"), content_len,
                content if isinstance(content, str) else str(content)[:200],
            )

        user_content = RequestTranslator.extract_user_message(messages)
        system_content = RequestTranslator.extract_system_message(messages)
        
        # Build prompt with system message if present
        if system_content:
            full_content = system_content + "\n\n" + user_content
        else:
            full_content = user_content
        
        content = [{"type": "text", "text": full_content}]
        is_stream = openai_request.get("stream", False)
        request_id = f"chatcmpl-{uuid4()}"

        return TranslatedRequest(
            session_id=session_id,
            content=content,
            is_stream=is_stream,
            request_id=request_id,
        )

    @staticmethod
    def extract_user_message(messages: list[dict]) -> str:
        """Extract the content of the last message with role=user.

        Handles both string content and array content formats:
        - String: {"role": "user", "content": "hello"}
        - Array:  {"role": "user", "content": [{"type": "text", "text": "hello"}]}

        Args:
            messages: The messages array from an OpenAI chat completion request.

        Returns:
            The content string of the last user message.

        Raises:
            ValueError: If no user message is found in the messages array.
        """
        for message in reversed(messages):
            if message.get("role") == "user":
                content = message.get("content", "")
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    # Extract text from content blocks: [{"type": "text", "text": "..."}]
                    parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            parts.append(block)
                    return " ".join(parts)
                return str(content)

        raise ValueError("No user message found in messages")

    @staticmethod
    def extract_system_message(messages: list[dict]) -> str:
        """Extract system message content if present."""
        for message in messages:
            if message.get("role") == "system":
                content = message.get("content") or ""
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    return " ".join(
                        b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
                    )
        return ""
