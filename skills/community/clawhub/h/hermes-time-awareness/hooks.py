"""
pre_llm_call hook for Hermes time awareness.

Injects current time and elapsed-since-last-message context into the
user message before each LLM turn. The injection is ephemeral — it
rides the API copy only and is never persisted to the session DB.

Token cost: ~20-30 tokens per turn (time only), ~35-45 tokens (with idle).
"""

from time_awareness.time_context import (
    format_time_context,
    record_user_message,
)


def on_pre_llm_call(
    *,
    session_id: str = "",
    user_message: str = "",
    conversation_history=None,
    is_first_turn: bool = False,
    model: str = "",
    platform: str = "",
    sender_id: str = "",
    **kwargs,
) -> dict:
    """Inject time awareness context into the current turn's user message."""
    # Record this user message timestamp for future idle calculation
    if session_id:
        record_user_message(session_id)

    ctx = format_time_context(
        session_id=session_id,
        conversation_history=conversation_history,
        is_first_turn=is_first_turn,
    )
    if ctx:
        return {"context": ctx}
    return {}


def register_hooks(ctx) -> None:
    ctx.register_hook("pre_llm_call", on_pre_llm_call)
