#!/usr/bin/env python3
"""Token-bucket rate limiter for the GKN-Phantom Penetration Testing Skill.

Gates every httpRequest / runShell call that produces network traffic.
Default 3 req/sec with a bounded burst queue. Over-limit requests are QUEUED
(never dropped, never crash).

Importable:
    from rate_limiter import RateLimiter
    rl = RateLimiter(rps=3, burst=5)
    rl.acquire()   # blocks until a token is available

CLI (drain test):
    python rate_limiter.py --rps 3 --burst 5 --count 10

Thread-safe.
"""

from __future__ import annotations

import argparse
import threading
import time
from collections import deque


class RateLimiter:
    """Token-bucket limiter with a bounded wait queue.

    Tokens refill continuously at `rps` per second up to `burst` tokens.
    acquire() blocks until a token is granted. If the wait queue exceeds
    `max_queue`, acquire() raises QueueFullError instead of blocking forever
    (the caller should log and skip, never crash the run).
    """

    def __init__(self, rps: float = 3.0, burst: int = 5, max_queue: int = 100):
        if rps <= 0:
            raise ValueError("rps must be > 0")
        if burst < 1:
            raise ValueError("burst must be >= 1")
        self.rps = float(rps)
        self.burst = int(burst)
        self.max_queue = int(max_queue)
        self._tokens = float(burst)
        self._last = time.monotonic()
        self._lock = threading.Lock()
        self._waiters: deque = deque()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last
        self._tokens = min(self.burst, self._tokens + elapsed * self.rps)
        self._last = now

    def acquire(self, timeout: float | None = None) -> float:
        """Block until a token is available. Return wait time in seconds.

        Raises QueueFullError if the wait queue is full.
        """
        deadline = (time.monotonic() + timeout) if timeout is not None else None
        with self._lock:
            if len(self._waiters) >= self.max_queue:
                raise QueueFullError(
                    f"rate limiter wait queue full ({self.max_queue}); request rejected"
                )
            ticket = threading.Event()
            self._waiters.append(ticket)

        # Wait for this ticket to be at the head AND a token to be available.
        while True:
            with self._lock:
                self._refill()
                head = self._waiters[0] if self._waiters else None
                if head is ticket and self._tokens >= 1.0:
                    self._tokens -= 1.0
                    self._waiters.popleft()
                    if self._waiters:
                        self._waiters[0].set()
                    return 0.0
                if self._tokens < 1.0:
                    needed = 1.0 - self._tokens
                    wait = needed / self.rps
                else:
                    wait = 0.0
            if deadline is not None and time.monotonic() + wait > deadline:
                raise TimeoutError("rate limiter acquire timed out")
            time.sleep(min(wait, 0.05) if wait > 0 else 0.01)


class QueueFullError(RuntimeError):
    pass


def main() -> int:
    ap = argparse.ArgumentParser(description="Rate limiter drain test")
    ap.add_argument("--rps", type=float, default=3.0)
    ap.add_argument("--burst", type=int, default=5)
    ap.add_argument("--count", type=int, default=10)
    args = ap.parse_args()

    rl = RateLimiter(rps=args.rps, burst=args.burst)
    for i in range(args.count):
        t0 = time.monotonic()
        rl.acquire()
        print(f"req {i + 1:02d} granted at +{time.monotonic() - t0:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
