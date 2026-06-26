from __future__ import annotations

from collections.abc import Iterable

from .provider_types import ProviderModule


_PROVIDER_REGISTRY: dict[str, ProviderModule] = {}


def register_provider(provider: ProviderModule) -> None:
    _PROVIDER_REGISTRY[provider.slug] = provider


def get_provider(slug: str) -> ProviderModule:
    try:
        return _PROVIDER_REGISTRY[slug]
    except KeyError as exc:  # pragma: no cover - defensive branch
        available = ", ".join(sorted(_PROVIDER_REGISTRY)) or "<none>"
        raise KeyError(f"unknown provider '{slug}' (available: {available})") from exc


def list_providers() -> list[ProviderModule]:
    return [_PROVIDER_REGISTRY[key] for key in sorted(_PROVIDER_REGISTRY)]


def list_provider_slugs() -> Iterable[str]:
    return sorted(_PROVIDER_REGISTRY)
