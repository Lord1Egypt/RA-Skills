"""Basic provider registry."""

from __future__ import annotations

from .base import BaseProvider
from .google import GoogleProvider
from .x import XProvider
from .youtube import YouTubeProvider

__all__ = [
    "BaseProvider",
    "GoogleProvider",
    "TikTokProvider",
    "XProvider",
    "YouTubeProvider",
    "build_provider",
    "available_providers",
]


def available_providers() -> list[str]:
    """Return provider names supported by the basic runtime."""

    return ["google", "youtube", "x", "tiktok"]


def build_provider(name: str, config: dict | None = None) -> BaseProvider:
    """Build a provider by name."""

    normalized = name.strip().lower()
    if normalized == "google":
        return GoogleProvider(config)
    if normalized == "youtube":
        return YouTubeProvider(config)
    if normalized == "x":
        return XProvider(config)
    if normalized == "tiktok":
        from .tiktok import TikTokProvider

        return TikTokProvider(config)
    raise ValueError(f"unsupported provider: {name}")
