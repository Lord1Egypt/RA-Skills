"""Budget tracker — time-based and API-call-based (not token estimation)."""

from __future__ import annotations
import time
import json
from datetime import datetime, timezone
from pathlib import Path


class NightBudget:
    """Track execution budget by wall-clock time and API calls."""

    DEFAULT_MAX_PHASE_SECONDS = 3600
    DEFAULT_MAX_PLAN_SECONDS = 86400
    DEFAULT_MAX_NIGHT_SECONDS = 86400
    DEFAULT_MAX_API_CALLS = 999999
    DEFAULT_MAX_429_RESPONSES = 50

    def __init__(
        self,
        max_phase_seconds: int = DEFAULT_MAX_PHASE_SECONDS,
        max_plan_seconds: int = DEFAULT_MAX_PLAN_SECONDS,
        max_night_seconds: int = DEFAULT_MAX_NIGHT_SECONDS,
        max_api_calls: int = DEFAULT_MAX_API_CALLS,
        max_429_responses: int = DEFAULT_MAX_429_RESPONSES,
    ):
        self.max_phase_seconds = max_phase_seconds
        self.max_plan_seconds = max_plan_seconds
        self.max_night_seconds = max_night_seconds
        self.max_api_calls = max_api_calls
        self.max_429_responses = max_429_responses

        self.phase_start: float = 0
        self.phase_seconds: float = 0
        self.plan_seconds: float = 0
        self.night_seconds: float = 0
        self.api_calls: int = 0
        self.rate_limit_hits: int = 0
        self.night_start: float = time.time()
        self.phases_completed: int = 0
        self.plans_completed: int = 0

    def start_phase(self):
        self.phase_start = time.time()

    def end_phase(self):
        elapsed = time.time() - self.phase_start
        self.phase_seconds = elapsed
        self.plan_seconds += elapsed
        self.night_seconds += elapsed

    def record_api_call(self, got_429: bool = False):
        self.api_calls += 1
        if got_429:
            self.rate_limit_hits += 1

    def phase_exceeded(self) -> bool:
        return self.phase_seconds >= self.max_phase_seconds

    def plan_exceeded(self) -> bool:
        return self.plan_seconds >= self.max_plan_seconds

    def night_exceeded(self) -> bool:
        return (
            self.night_seconds >= self.max_night_seconds
            or self.rate_limit_hits >= self.max_429_responses
        )

    def remaining_night_minutes(self) -> float:
        return max(0, (self.max_night_seconds - self.night_seconds) / 60)

    def remaining_plan_minutes(self) -> float:
        return max(0, (self.max_plan_seconds - self.plan_seconds) / 60)

    def summary(self) -> dict:
        return {
            "phase_seconds": round(self.phase_seconds, 1),
            "plan_seconds": round(self.plan_seconds, 1),
            "night_seconds": round(self.night_seconds, 1),
            "api_calls": self.api_calls,
            "rate_limit_hits": self.rate_limit_hits,
            "phases_completed": self.phases_completed,
            "plans_completed": self.plans_completed,
            "remaining_night_minutes": round(self.remaining_night_minutes(), 1),
        }

    def save(self, path: Path):
        data = {
            "max_phase_seconds": self.max_phase_seconds,
            "max_plan_seconds": self.max_plan_seconds,
            "max_night_seconds": self.max_night_seconds,
            "max_api_calls": self.max_api_calls,
            "max_429_responses": self.max_429_responses,
            "night_start": self.night_start,
            "phase_seconds": self.phase_seconds,
            "plan_seconds": self.plan_seconds,
            "night_seconds": self.night_seconds,
            "api_calls": self.api_calls,
            "rate_limit_hits": self.rate_limit_hits,
            "phases_completed": self.phases_completed,
            "plans_completed": self.plans_completed,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: Path) -> "NightBudget":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text())
        b = cls(
            max_phase_seconds=data.get("max_phase_seconds", cls.DEFAULT_MAX_PHASE_SECONDS),
            max_plan_seconds=data.get("max_plan_seconds", cls.DEFAULT_MAX_PLAN_SECONDS),
            max_night_seconds=data.get("max_night_seconds", cls.DEFAULT_MAX_NIGHT_SECONDS),
            max_api_calls=data.get("max_api_calls", cls.DEFAULT_MAX_API_CALLS),
            max_429_responses=data.get("max_429_responses", cls.DEFAULT_MAX_429_RESPONSES),
        )
        b.night_start = data.get("night_start", time.time())
        b.phase_seconds = data.get("phase_seconds", 0)
        b.plan_seconds = data.get("plan_seconds", 0)
        b.night_seconds = data.get("night_seconds", 0)
        b.api_calls = data.get("api_calls", 0)
        b.rate_limit_hits = data.get("rate_limit_hits", 0)
        b.phases_completed = data.get("phases_completed", 0)
        b.plans_completed = data.get("plans_completed", 0)
        return b
