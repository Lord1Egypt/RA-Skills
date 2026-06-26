"""Source registry — maps type names in sources.yaml to classes."""

from __future__ import annotations

from typing import Type
from src.models import BaseSource

# type_name -> class
_REGISTRY: dict[str, Type[BaseSource]] = {}


def register(type_name: str):
    """Decorator to register a source class under a type name."""
    def decorator(cls: Type[BaseSource]):
        _REGISTRY[type_name] = cls
        return cls
    return decorator


def get_source_class(type_name: str) -> Type[BaseSource]:
    if type_name not in _REGISTRY:
        raise ValueError(
            f"Unknown source type: {type_name!r}. "
            f"Available: {list(_REGISTRY.keys())}"
        )
    return _REGISTRY[type_name]


def list_types() -> list[str]:
    return list(_REGISTRY.keys())


# Import all source modules so they self-register via @register.
from src.sources import hn, rss, github_trending, x_feed, web_search, anthropic_news, producthunt, reddit  # noqa: E402, F401
