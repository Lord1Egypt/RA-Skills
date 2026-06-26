"""Human behavior simulation parameters (delays, scrolling, rate limiting)."""

import json
import logging
import math
import random
import time
from pathlib import Path

logger = logging.getLogger(__name__)


def sleep_random(min_ms: int, max_ms: int) -> None:
    """Random delay within a range to simulate human pacing."""
    if max_ms <= min_ms:
        time.sleep(min_ms / 1000.0)
        return
    delay = random.randint(min_ms, max_ms) / 1000.0
    time.sleep(delay)


def sleep_gaussian(mean_ms: int, std_ms: int) -> None:
    """Gaussian-distributed delay for more realistic human timing."""
    delay = max(100, random.gauss(mean_ms, std_ms)) / 1000.0
    time.sleep(delay)


INACCESSIBLE_KEYWORDS = [
    "this profile is not available",
    "page not found",
    "this content isn't available",
    "you can't view this profile",
    "your account has been restricted",
    "temporarily unavailable",
]

BAN_KEYWORDS = [
    "your account has been restricted",
    "we've restricted your account",
    "unusual activity",
    "temporarily limited",
    "verify your identity",
    "complete a security check",
    "you've reached the",
    "too many requests",
    "rate limit",
]


class RateLimiter:
    """Session-level rate limiter to stay under LinkedIn's safety thresholds.

    Default limits per hour:
        - profile_view: 40  (LinkedIn limit ~50/day, conservative)
        - search: 80        (LinkedIn limit ~100/day)
        - connect: 15       (LinkedIn limit ~20/day)
        - message: 20
        - like: 30
        - comment: 15
        - general: 100
    """

    DEFAULT_LIMITS: dict[str, int] = {
        "profile_view": 40,
        "search": 80,
        "connect": 15,
        "message": 20,
        "like": 30,
        "comment": 15,
        "general": 100,
    }

    def __init__(self, limits: dict[str, int] | None = None) -> None:
        self._limits = {**self.DEFAULT_LIMITS, **(limits or {})}
        self._actions: dict[str, list[float]] = {}

    def _prune(self, action_type: str) -> None:
        """Remove entries older than 1 hour."""
        cutoff = time.time() - 3600
        self._actions[action_type] = [
            t for t in self._actions.get(action_type, []) if t > cutoff
        ]

    def can_act(self, action_type: str = "general") -> bool:
        """Check if an action is allowed under the rate limit."""
        self._prune(action_type)
        limit = self._limits.get(action_type, self._limits["general"])
        return len(self._actions.get(action_type, [])) < limit

    def record(self, action_type: str = "general") -> None:
        """Record an action timestamp."""
        self._actions.setdefault(action_type, []).append(time.time())

    def remaining(self, action_type: str = "general") -> int:
        """Return how many actions remain in the current window."""
        self._prune(action_type)
        limit = self._limits.get(action_type, self._limits["general"])
        return max(0, limit - len(self._actions.get(action_type, [])))

    def wait_if_needed(self, action_type: str = "general") -> bool:
        """If at limit, wait until a slot frees up. Returns False if waited > 5 min."""
        if self.can_act(action_type):
            return True
        entries = sorted(self._actions.get(action_type, []))
        if not entries:
            return True
        wait_until = entries[0] + 3600
        wait_secs = wait_until - time.time()
        if wait_secs > 300:
            logger.warning("Rate limit: %s exhausted, would need to wait %.0fs", action_type, wait_secs)
            return False
        logger.info("Rate limit: waiting %.0fs for %s slot", wait_secs, action_type)
        time.sleep(wait_secs + 1)
        return True


class ActionLogger:
    """Append-only JSON log of all outreach actions for audit and tracking.

    Writes to ~/.linkedin-skills/actions.jsonl
    """

    def __init__(self, log_path: str | None = None) -> None:
        self._path = Path(log_path or Path.home() / ".linkedin-skills" / "actions.jsonl")
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        action: str,
        target_url: str,
        target_name: str = "",
        success: bool = True,
        details: dict | None = None,
    ) -> None:
        """Append one action entry."""
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "action": action,
            "target_url": target_url,
            "target_name": target_name,
            "success": success,
        }
        if details:
            entry["details"] = details
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def recent(self, n: int = 20) -> list[dict]:
        """Read the last N log entries."""
        if not self._path.exists():
            return []
        with open(self._path, encoding="utf-8") as f:
            lines = f.readlines()
        return [json.loads(l) for l in lines[-n:]]


def check_for_ban(page_text: str) -> str | None:
    """Check page text for ban/restriction signals. Returns the matched keyword or None."""
    lower = page_text.lower()
    for kw in BAN_KEYWORDS:
        if kw in lower:
            return kw
    return None
