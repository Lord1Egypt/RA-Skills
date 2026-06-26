"""
Context Manager — Context window management for model routing

Monitors context usage and provides summarize/prune functionality
to keep conversations within model context limits.

Thresholds:
    - >60% usage → summarize old messages
    - >75% usage → prune old context
    - Always preserve the N most recent messages


"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Optional

import yaml

logger = logging.getLogger("router.memory")


@dataclass
class ContextStatus:
    """Current context window status."""
    total_tokens: int          # Estimated total tokens in context
    context_limit: int         # Model's context window limit
    usage_percent: float      # Percentage of context window used
    needs_summarize: bool     # Whether context exceeds summarize threshold
    needs_prune: bool         # Whether context exceeds prune threshold
    message_count: int        # Number of messages in context
    action: str               # Recommended action: "none", "summarize", "prune"

    @property
    def is_healthy(self) -> bool:
        """Context is within acceptable limits."""
        return not self.needs_summarize and not self.needs_prune


@dataclass
class Message:
    """A single message in the conversation context."""
    role: str                  # "user", "assistant", "system"
    content: str
    tokens: int = 0           # Estimated token count
    timestamp: str = ""        # ISO timestamp
    metadata: dict = field(default_factory=dict)

    def estimate_tokens(self) -> int:
        """Estimate token count from content length (~4 chars per token)."""
        if self.tokens > 0:
            return self.tokens
        return max(1, len(self.content) // 4)


class ContextManager:
    """
    Manages context window usage for model routing.

    Monitors context size relative to model limits and
    recommends when to summarize or prune old messages.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize context manager with configuration.

        Args:
            config_path: Path to config.yaml. Defaults to ./config.yaml.
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        self.config_path = config_path
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        ctx_config = self.config.get("context", {})
        self.summarize_threshold = ctx_config.get("summarize_threshold", 0.60)
        self.prune_threshold = ctx_config.get("prune_threshold", 0.75)
        self.preserve_recent_count = ctx_config.get("preserve_recent_count", 10)
        self.large_context_threshold = ctx_config.get("large_context_threshold", 120000)

    def check_context(
        self,
        messages: list[Message],
        context_limit: int,
    ) -> ContextStatus:
        """
        Check context window status and recommend actions.

        Args:
            messages: List of messages in context.
            context_limit: Model's context window limit in tokens.

        Returns:
            ContextStatus with usage info and recommended action.
        """
        total_tokens = sum(m.estimate_tokens() for m in messages)
        usage_percent = total_tokens / context_limit if context_limit > 0 else 1.0

        needs_summarize = usage_percent >= self.summarize_threshold
        needs_prune = usage_percent >= self.prune_threshold

        if needs_prune:
            action = "prune"
        elif needs_summarize:
            action = "summarize"
        else:
            action = "none"

        return ContextStatus(
            total_tokens=total_tokens,
            context_limit=context_limit,
            usage_percent=round(usage_percent, 3),
            needs_summarize=needs_summarize,
            needs_prune=needs_prune,
            message_count=len(messages),
            action=action,
        )

    def get_messages_to_summarize(
        self,
        messages: list[Message],
        context_limit: int,
    ) -> list[Message]:
        """
        Get messages that should be summarized (all except recent N).

        Args:
            messages: All messages in context.
            context_limit: Model's context window limit in tokens.

        Returns:
            List of messages that can be summarized.
        """
        status = self.check_context(messages, context_limit)
        if not status.needs_summarize:
            return []

        # Preserve the most recent messages
        preserve_count = min(self.preserve_recent_count, len(messages))
        return messages[:-preserve_count] if preserve_count < len(messages) else []

    def get_messages_to_prune(
        self,
        messages: list[Message],
        context_limit: int,
    ) -> list[Message]:
        """
        Get messages that should be pruned (removed from context).

        Args:
            messages: All messages in context.
            context_limit: Model's context window limit in tokens.

        Returns:
            List of messages that can be safely removed.
        """
        status = self.check_context(messages, context_limit)
        if not status.needs_prune:
            return []

        # Prune oldest messages, keeping recent ones
        preserve_count = min(self.preserve_recent_count, len(messages))

        # Calculate how many tokens we need to remove
        target_tokens = int(context_limit * self.summarize_threshold)  # Target: back below summarize threshold
        total_tokens = sum(m.estimate_tokens() for m in messages)
        excess_tokens = total_tokens - target_tokens

        # Find how many oldest messages to prune to get below target
        prune_messages = []
        prune_tokens = 0
        preserve_messages = messages[-preserve_count:] if preserve_count > 0 else []

        for msg in messages[:-preserve_count] if preserve_count < len(messages) else []:
            if prune_tokens < excess_tokens:
                prune_messages.append(msg)
                prune_tokens += msg.estimate_tokens()
            else:
                break

        return prune_messages

    def should_use_large_context_model(
        self,
        messages: list[Message],
        context_limit: int = 0,
    ) -> bool:
        """
        Check if context is large enough to require a large-context model.

        Args:
            messages: All messages in context.
            context_limit: Current model's context limit (0 = unknown).

        Returns:
            True if a large-context model should be used instead.
        """
        total_tokens = sum(m.estimate_tokens() for m in messages)

        # If we know the current model's limit, check if we exceed it
        if context_limit > 0 and total_tokens > context_limit:
            return True

        # Check against the large context threshold
        return total_tokens > self.large_context_threshold

    def estimate_tokens_for_text(self, text: str) -> int:
        """
        Estimate token count for a text string.

        Uses the ~4 chars per token approximation.
        For production, this should be replaced with a proper tokenizer.

        Args:
            text: Text to estimate tokens for.

        Returns:
            Estimated token count.
        """
        return max(1, len(text) // 4)

    def create_summary_prompt(
        self,
        messages: list[Message],
    ) -> str:
        """
        Create a prompt that asks a model to summarize the given messages.

        This is the prompt to send to the model when summarizing context.

        Args:
            messages: Messages to summarize.

        Returns:
            A prompt string asking for a summary.
        """
        conversation = "\n".join(
            f"{m.role}: {m.content[:500]}{'...' if len(m.content) > 500 else ''}"
            for m in messages
        )

        return (
            "Summarize the following conversation concisely, preserving key decisions, "
            "facts, and context. The summary will be used to continue the conversation.\n\n"
            f"{conversation}\n\n"
            "Summary:"
        )


def check_context_status(
    messages: list[dict],
    context_limit: int,
    config_path: Optional[str] = None,
) -> ContextStatus:
    """
    Convenience function to check context status.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.
        context_limit: Model's context window limit in tokens.
        config_path: Path to config.yaml.

    Returns:
        ContextStatus with usage info and recommended action.
    """
    manager = ContextManager(config_path=config_path)
    msg_objects = [
        Message(role=m.get("role", "user"), content=m.get("content", ""))
        for m in messages
    ]
    return manager.check_context(msg_objects, context_limit)