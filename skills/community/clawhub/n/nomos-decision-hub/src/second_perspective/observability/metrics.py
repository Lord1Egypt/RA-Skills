"""Lightweight observability (v0.5): in-process metrics + structured logging.

No external dependency required. Exposes per-route request counters, error
counters, and latency averages, plus a middleware that records them and stamps
responses with ``X-Process-Time-Ms``. A JSON snapshot is served at
``/v1/metrics``.
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict

from fastapi import Request

logger = logging.getLogger("nomos.observability")


class Metrics:
    def __init__(self) -> None:
        self.request_count: dict[str, int] = defaultdict(int)
        self.error_count: dict[str, int] = defaultdict(int)
        self.latency_sum: dict[str, float] = defaultdict(float)
        self.latency_count: dict[str, int] = defaultdict(int)

    def record(self, route: str, status_code: int, latency: float) -> None:
        self.request_count[route] += 1
        if status_code >= 500:
            self.error_count[route] += 1
        self.latency_sum[route] += latency
        self.latency_count[route] += 1

    def snapshot(self) -> dict:
        out: dict[str, dict[str, float | int]] = {}
        for route, count in self.request_count.items():
            out[route] = {
                "requests": count,
                "errors": self.error_count[route],
                "avg_latency_ms": round(
                    (self.latency_sum[route] / self.latency_count[route]) * 1000, 3
                )
                if count
                else 0,
            }
        return out


_metrics = Metrics()


def get_metrics() -> Metrics:
    return _metrics


class ObservabilityMiddleware:
    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, request: Request, call_next):
        start = time.monotonic()
        try:
            response = await call_next(request)
        except Exception:
            _metrics.record(request.url.path, 500, time.monotonic() - start)
            raise
        latency = time.monotonic() - start
        _metrics.record(request.url.path, response.status_code, latency)
        logger.info(
            "metric path=%s status=%d latency_ms=%.3f",
            request.url.path,
            response.status_code,
            latency * 1000,
        )
        response.headers["X-Process-Time-Ms"] = f"{latency * 1000:.3f}"
        return response
