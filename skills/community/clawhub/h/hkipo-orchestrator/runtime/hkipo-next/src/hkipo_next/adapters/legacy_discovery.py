"""Compatibility adapter for legacy discovery functions."""

from __future__ import annotations

from typing import Any

from hkipo_next.adapters.legacy_loader import load_legacy_module


class LegacyDiscoveryAdapter:
    """Thin wrapper around legacy discovery-related functions."""

    def fetch_margin_list(self) -> list[dict[str, Any]]:
        return load_legacy_module("aipo").fetch_margin_list()

    def fetch_ipo_brief(self, symbol: str) -> dict[str, Any] | None:
        return load_legacy_module("aipo").fetch_ipo_brief(symbol)
