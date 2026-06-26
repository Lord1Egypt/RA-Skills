"""Private DSPy configuration helpers used only by iterate_prompt.py."""
import os
from pathlib import Path
from typing import Optional


def configure_lm(provider: Optional[str] = None, model: Optional[str] = None):
    """Configure DSPy's LM. Returns the configured LM, or raises ImportError if dspy is missing."""
    try:
        import dspy
    except ImportError:
        raise ImportError(
            "dspy is not installed. Install with `pip install n8n-evol-I[dspy]` "
            "or `pip install dspy litellm`."
        )

    provider = provider or _detect_provider()
    model = model or _default_model(provider)

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY missing")
        lm = dspy.LM(model, api_key=api_key)
    elif provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY missing")
        lm = dspy.LM(f"openrouter/{model}", api_key=api_key, api_base="https://openrouter.ai/api/v1")
    elif provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY missing")
        lm = dspy.LM(f"anthropic/{model}", api_key=api_key)
    else:
        raise ValueError(f"unknown provider: {provider}")

    dspy.configure(lm=lm)
    return lm


def _detect_provider() -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("OPENROUTER_API_KEY"):
        return "openrouter"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    raise ValueError("No LLM API key in env. Set OPENAI_API_KEY, OPENROUTER_API_KEY, or ANTHROPIC_API_KEY.")


def _default_model(provider: str) -> str:
    return {
        "openai": "openai/gpt-4o-mini",
        "openrouter": "anthropic/claude-3.5-haiku",
        "anthropic": "claude-3-5-haiku-latest",
    }[provider]
