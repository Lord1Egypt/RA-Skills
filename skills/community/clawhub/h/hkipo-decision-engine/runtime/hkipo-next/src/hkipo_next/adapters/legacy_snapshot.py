"""Compatibility adapter for legacy snapshot data sources."""

from __future__ import annotations

from typing import Any

from hkipo_next.adapters.legacy_loader import load_legacy_module


class LegacySnapshotAdapter:
    """Thin wrapper around legacy snapshot-related functions."""

    def fetch_ipo_brief(self, symbol: str) -> dict[str, Any] | None:
        return load_legacy_module("aipo").fetch_ipo_brief(symbol)

    def fetch_aastocks_detail(self, symbol: str) -> dict[str, Any] | None:
        return load_legacy_module("aastocks").get_ipo_detail(symbol)

    def fetch_aastocks_upcoming_ipos(self) -> list[dict[str, Any]]:
        return load_legacy_module("aastocks").get_upcoming_ipos()
