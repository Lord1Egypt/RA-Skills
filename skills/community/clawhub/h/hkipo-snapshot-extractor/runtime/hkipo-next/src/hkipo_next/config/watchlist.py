"""Watchlist persistence helpers."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from hkipo_next.utils.normalization import normalize_symbol


class WatchlistState(BaseModel):
    """Stored watchlist state."""

    model_config = ConfigDict(extra="forbid")

    symbols: list[str] = Field(default_factory=list)


class WatchlistRepository:
    """Persist and mutate the user's watchlist."""

    def __init__(self, path: Path):
        self.path = path

    def read(self) -> WatchlistState:
        if not self.path.exists():
            return WatchlistState()
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return WatchlistState.model_validate(payload)

    def save(self, state: WatchlistState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(state.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def list_symbols(self) -> list[str]:
        return self.read().symbols

    def add(self, raw_symbols: list[str]) -> tuple[WatchlistState, list[str]]:
        state = self.read()
        changed: list[str] = []
        existing = list(state.symbols)
        for raw_symbol in raw_symbols:
            symbol = normalize_symbol(raw_symbol)
            if symbol is None:
                continue
            if symbol not in existing:
                existing.append(symbol)
                changed.append(symbol)
        updated = WatchlistState(symbols=existing)
        self.save(updated)
        return updated, changed

    def remove(self, raw_symbols: list[str]) -> tuple[WatchlistState, list[str]]:
        targets = {
            symbol
            for raw_symbol in raw_symbols
            if (symbol := normalize_symbol(raw_symbol)) is not None
        }
        state = self.read()
        if not targets:
            return state, []
        changed = [symbol for symbol in state.symbols if symbol in targets]
        updated = WatchlistState(symbols=[symbol for symbol in state.symbols if symbol not in targets])
        self.save(updated)
        return updated, changed
