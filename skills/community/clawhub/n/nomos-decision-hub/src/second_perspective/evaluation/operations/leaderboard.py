"""Public leaderboard (module C, v0.6) — in-memory implementation.

Ranking is deterministic: composite score descending, with subjects lacking a
composite ranked last, and ties broken by ``subject_id`` ascending.
"""

from __future__ import annotations

from .base import LeaderboardEntry


class InMemoryLeaderboard:
    """A deterministic, zero-dependency leaderboard."""

    id = "in-memory-leaderboard"

    def __init__(self) -> None:
        self._entries: dict[str, LeaderboardEntry] = {}

    def publish(self, entry: LeaderboardEntry) -> None:
        self._entries[entry.subject_id] = entry

    def get(self, subject_id: str) -> LeaderboardEntry | None:
        return self._entries.get(subject_id)

    def all(self) -> list[LeaderboardEntry]:
        return [self._entries[k] for k in sorted(self._entries)]

    def top(self, n: int) -> list[LeaderboardEntry]:
        if n <= 0:
            return []
        ranked = sorted(
            self._entries.values(),
            key=lambda e: (
                -(1 if e.composite is not None else 0),
                -(e.composite if e.composite is not None else 0.0),
                e.subject_id,
            ),
        )
        return ranked[:n]


__all__ = ["InMemoryLeaderboard"]
