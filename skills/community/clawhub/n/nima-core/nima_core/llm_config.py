from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_ANTHROPIC_BASE_URL = "https://api.anthropic.com"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_ANTHROPIC_MODEL = "claude-haiku-4-5"
DEFAULT_GENERIC_MODEL = "qwen3.5:cloud"


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    api_key: str
    model: str
    base_url: str


def _clean(value: Optional[str]) -> str:
    return (value or "").strip()


def _infer_provider(base_url: str) -> Optional[str]:
    base = (base_url or "").lower()
    if not base:
        return None
    if "anthropic.com" in base:
        return "anthropic"
    if any(token in base for token in ("api.openai.com", "openai", "ollama", "vllm", "litellm", "openrouter", "/chat/completions")):
        return "openai"
    return None


def _default_model(provider: str) -> str:
    if provider == "anthropic":
        return DEFAULT_ANTHROPIC_MODEL
    if provider == "openai":
        return DEFAULT_OPENAI_MODEL
    return DEFAULT_GENERIC_MODEL


def resolve_llm_config(
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMConfig:
    env_base = _clean(os.environ.get("NIMA_LLM_BASE_URL")) or _clean(os.environ.get("NIMA_LLM_BASE"))
    resolved_base_url = _clean(base_url) or env_base

    resolved_provider = _clean(provider) or _clean(os.environ.get("NIMA_LLM_PROVIDER"))
    if not resolved_provider:
        resolved_provider = _infer_provider(resolved_base_url) or "openai"
    resolved_provider = resolved_provider.lower()
    if resolved_provider in {"openai-compatible", "generic"}:
        resolved_provider = "openai"

    resolved_api_key = _clean(api_key) or _clean(os.environ.get("NIMA_LLM_API_KEY")) or _clean(os.environ.get("NIMA_LLM_KEY"))
    if not resolved_api_key:
        if resolved_provider == "openai":
            resolved_api_key = _clean(os.environ.get("OPENAI_API_KEY"))
        elif resolved_provider == "anthropic":
            resolved_api_key = _clean(os.environ.get("ANTHROPIC_API_KEY"))

    if not resolved_base_url:
        if resolved_provider == "anthropic":
            resolved_base_url = _clean(os.environ.get("ANTHROPIC_BASE_URL")) or DEFAULT_ANTHROPIC_BASE_URL
        else:
            resolved_base_url = _clean(os.environ.get("OPENAI_BASE_URL")) or DEFAULT_OPENAI_BASE_URL

    resolved_model = (
        _clean(model)
        or _clean(os.environ.get("NIMA_LLM_MODEL"))
        or (_clean(os.environ.get("NIMA_DISTILL_MODEL")) if resolved_provider == "anthropic" else "")
        or _default_model(resolved_provider)
    )

    return LLMConfig(
        provider=resolved_provider,
        api_key=resolved_api_key,
        model=resolved_model,
        base_url=resolved_base_url.rstrip("/"),
    )
