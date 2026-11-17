"""Version-drift monitoring scheduler (module C, v0.6) — in-memory.

Tracks which subjects are *due* for re-evaluation given a cadence and the last
run time. Cadences accept ``hourly`` / ``daily`` / ``weekly`` or an explicit
``<n><s|m|h|d>`` form.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta

from .base import DriftSchedule

_CADENCE_WORDS = {"hourly": 3600, "daily": 86400, "weekly": 604800}
_CADENCE_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def cadence_seconds(cadence: str) -> int:
    """Parse a cadence string into seconds."""
    c = cadence.strip().lower()
    if c in _CADENCE_WORDS:
        return _CADENCE_WORDS[c]
    if len(c) >= 2 and c[-1] in _CADENCE_UNITS and c[:-1].isdigit():
        return int(c[:-1]) * _CADENCE_UNITS[c[-1]]
    raise ValueError(f"unsupported cadence: {cadence!r}")


class InMemoryDriftScheduler:
    id = "in-memory-drift-scheduler"

    def __init__(self) -> None:
        self._schedules: dict[str, DriftSchedule] = {}

    def register(self, schedule: DriftSchedule) -> None:
        self._schedules[schedule.subject_id] = schedule

    def due(self, now: datetime) -> list[DriftSchedule]:
        """Schedules that are enabled and past their cadence (never run -> due)."""
        out: list[DriftSchedule] = []
        for sc in self._schedules.values():
            if not sc.enabled:
                continue
            if sc.last_run is None:
                out.append(sc)
                continue
            if now - sc.last_run >= timedelta(seconds=cadence_seconds(sc.cadence)):
                out.append(sc)
        return sorted(out, key=lambda s: s.subject_id)

    def mark_run(self, subject_id: str, at: datetime) -> DriftSchedule:
        sc = self._schedules.get(subject_id)
        if sc is None:
            raise KeyError(f"unknown schedule: {subject_id}")
        updated = replace(sc, last_run=at)
        self._schedules[subject_id] = updated
        return updated

    def all(self) -> list[DriftSchedule]:
        return [self._schedules[k] for k in sorted(self._schedules)]


__all__ = ["InMemoryDriftScheduler", "cadence_seconds"]
