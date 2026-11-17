"""Evaluation measurement layer — metric & result protocols (v0.6).

This module defines the *interfaces* the measurement harness is built on:

- ``MetricResult`` — every metric returns one of these (value + optional
  threshold verdict + evidence metadata), mirroring NOMOS' invariant that a
  number is never reported without its provenance.
- ``Metric`` — a lightweight structural protocol for pluggable metrics.
- ``MetricError`` — raised when a metric is handed input it cannot compute on.

Design invariants (aligned with the NOMOS kernel):

- Determinism: a metric is a pure function of its declared inputs.
- No invention: metrics never impute missing observations; they raise instead.
- Provenance: results carry ``n`` (sample size) and ``meta`` for re-computation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


class MetricError(ValueError):
    """Raised when a metric receives unusable input (empty / mismatched / OOR)."""


@dataclass(frozen=True)
class MetricResult:
    """A single measurement, with provenance.

    ``passed`` / ``threshold`` are intentionally *not* computed by the metric
    itself: the same measurement may be judged against different SLOs per
    deployment. Threshold verdicts are attached by the dimension control packs.
    """

    metric_id: str
    value: float
    unit: str = ""
    n: int = 0
    passed: bool | None = None
    threshold: str | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "value": self.value,
            "unit": self.unit,
            "n": self.n,
            "passed": self.passed,
            "threshold": self.threshold,
            "meta": dict(self.meta),
        }


@runtime_checkable
class Metric(Protocol):
    """Structural contract for a pluggable metric.

    Concrete metrics in ``metrics.py`` are plain functions; this protocol exists
    so custom metrics (registered by an operating body) can be type-checked.
    """

    id: str
    description: str
    unit: str

    def compute(self, *args: Any, **kwargs: Any) -> MetricResult: ...


__all__ = ["Metric", "MetricError", "MetricResult"]
