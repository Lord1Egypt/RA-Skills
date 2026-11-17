"""Token-bucket rate limiting middleware (v0.5).

Opt-in via ``SP_RATE_LIMIT`` (requests per minute per client; default off).
Keyed by client identifier (API-key subject or source IP). In-memory only;
designed to be swapped for a shared store (e.g. Redis) in clustered deploys.
"""

from __future__ import annotations

import os
import time
from collections import defaultdict

from fastapi import HTTPException, Request, status


class _Bucket:
    def __init__(self, rate: float, capacity: float) -> None:
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class RateLimitMiddleware:
    def __init__(self, app, rate_per_minute: int = 0, burst: int = 0) -> None:
        self.app = app
        self.rate = rate_per_minute / 60.0 if rate_per_minute > 0 else 0
        self.burst = burst or max(1, rate_per_minute)
        self._buckets: dict[str, _Bucket] = defaultdict(
            lambda: _Bucket(self.rate, self.burst)
        )

    @staticmethod
    def _client_id(request: Request) -> str:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            return "bearer:" + auth[7:]
        if request.client is not None:
            return request.client.host
        return "anonymous"

    async def __call__(self, request: Request, call_next):
        if self.rate <= 0:
            return await call_next(request)
        bucket = self._buckets[self._client_id(request)]
        if not bucket.allow():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )
        return await call_next(request)


def rate_limit_enabled() -> int:
    """Return configured requests-per-minute, or 0 when disabled."""
    try:
        return int(os.getenv("SP_RATE_LIMIT", "0") or 0)
    except ValueError:
        return 0
