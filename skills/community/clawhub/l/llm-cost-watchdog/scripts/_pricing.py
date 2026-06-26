"""
Pricing router. Picks the right source for each model:

  openrouter/*   -> OpenRouterSource (live)
  everything else -> LiteLLMSource (near-live) -> StaticMarkdownSource fallback

Public API (unchanged for callers):
  canonical_slug(name) -> str
  get_price(model)     -> ModelPrice | None
  require_price(model) -> ModelPrice        (raises KeyError if missing)
  list_models()        -> list[str]         (static universe only)
  load_pricing()       -> dict[slug, ModelPrice]   (static universe only)

Static-only is intentional for list_models / load_pricing: iterating the
full 400-model LiteLLM DB for "cheaper alternatives" would be slow and
noisy. The static pricing.md is the curated set.

ModelPrice includes `source` and `fetched_at` so callers can surface
where a number came from.
"""
from __future__ import annotations

from typing import NamedTuple, Optional

import _sources
from _sources import canonical_slug  # re-export


class ModelPrice(NamedTuple):
    slug: str
    display_name: str
    provider: str
    input_per_1m: float
    output_per_1m: float
    source: str = "static"
    fetched_at: float = 0.0
    mode: str = "chat"
    unit: str = "token"


# Singletons. Each caches its own network data on disk.
_LITELLM = _sources.LiteLLMSource()
_OPENROUTER = _sources.OpenRouterSource()
_STATIC = _sources.StaticMarkdownSource()


def _to_model_price(slug: str, sp: _sources.SourcedPrice) -> ModelPrice:
    return ModelPrice(
        slug=slug,
        display_name=sp.display_name,
        provider=sp.provider,
        input_per_1m=sp.input_per_1m,
        output_per_1m=sp.output_per_1m,
        source=sp.source,
        fetched_at=sp.fetched_at,
        mode=sp.mode,
        unit=sp.unit,
    )


def _is_openrouter(model: str) -> bool:
    return model.startswith("openrouter/")


def get_price(model: str) -> Optional[ModelPrice]:
    """
    Route-aware lookup. Source preference by prefix:

      openrouter/*  :  OpenRouter (strict) -> static
      everything else: LiteLLM -> OpenRouter (permissive) -> static

    OpenRouter is tried as a fallback for non-prefixed queries because
    sometimes the user's actual provider is OpenRouter, or OpenRouter
    has a model LiteLLM doesn't know yet.
    """
    slug = canonical_slug(model)

    if _is_openrouter(model):
        sp = _OPENROUTER.get(model)
        if sp is not None:
            return _to_model_price(slug, sp)
        sp = _STATIC.get(model)
        return _to_model_price(slug, sp) if sp else None

    # Non-openrouter: LiteLLM -> OpenRouter (permissive) -> static.
    sp = _LITELLM.get(model)
    if sp is not None:
        return _to_model_price(slug, sp)

    sp = _OPENROUTER.get_permissive(model)
    if sp is not None:
        return _to_model_price(slug, sp)

    sp = _STATIC.get(model)
    return _to_model_price(slug, sp) if sp else None


def require_price(model: str) -> ModelPrice:
    price = get_price(model)
    if price is not None:
        return price
    raise KeyError(f"No price found for model {model!r} in any source")


def load_pricing() -> dict:
    """Static universe only. {slug: ModelPrice} for every model in pricing.md."""
    return {
        slug: _to_model_price(slug, sp)
        for slug, sp in _STATIC.all_models().items()
    }


def list_models() -> list:
    return sorted(load_pricing().keys())
