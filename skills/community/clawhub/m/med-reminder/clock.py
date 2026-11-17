"""
clock.py — injectable time source for the med reminder skill (issue #1 PR 1).

All new code reads the current instant through a Clock so tests can freeze
and advance time deterministically. The system clock is the default.

MEDS_FAKE_NOW is honored only when MEDS_TEST=1, so a stray env var can never
shift a real run's clock.
"""

import os
import time as _time
from datetime import datetime, timedelta, timezone


def parse_instant(raw: str) -> datetime:
    """Parse an ISO 8601 instant ('Z' suffix tolerated) to an aware UTC datetime."""
    raw = raw.strip()
    if raw.endswith(("Z", "z")):
        raw = raw[:-1] + "+00:00"
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class Clock:
    """The real clock. Subclass (or use FakeClock) to control time in tests."""

    def now_utc(self) -> datetime:
        """Current instant, timezone-aware UTC. All comparisons use this."""
        return datetime.now(tz=timezone.utc)

    def now_in(self, tz) -> datetime:
        """Current instant as wall time in tz (display and local keys only)."""
        return self.now_utc().astimezone(tz)

    def now_iso(self) -> str:
        return self.now_utc().isoformat()

    def sleep(self, seconds: float) -> None:
        _time.sleep(seconds)


class FakeClock(Clock):
    """Frozen clock for tests. sleep() advances time instead of blocking."""

    def __init__(self, start: datetime):
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        self._now = start.astimezone(timezone.utc)

    def now_utc(self) -> datetime:
        return self._now

    def sleep(self, seconds: float) -> None:
        self._now += timedelta(seconds=seconds)


def get_clock() -> Clock:
    """The process clock. MEDS_FAKE_NOW applies only under MEDS_TEST=1."""
    if os.environ.get("MEDS_TEST") == "1":
        raw = os.environ.get("MEDS_FAKE_NOW")
        if raw:
            return FakeClock(parse_instant(raw))
    return Clock()
