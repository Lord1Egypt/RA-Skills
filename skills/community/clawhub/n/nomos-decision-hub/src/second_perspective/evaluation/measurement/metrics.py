"""Concrete metric implementations for the measurement layer (v0.6).

Every metric is a pure function returning a :class:`MetricResult`. Thresholds
are deliberately *not* baked in here — pass/fail verdicts are attached by the
dimension control packs (see ``dimension_packs.py``) so the same measurement can
be judged against different SLOs per deployment.

Implemented metrics
-------------------
========================  ==========================================
metric_id                 meaning
========================  ==========================================
``asr``                   attack success rate
``brier``                 Brier score
``ece``                   expected calibration error
``fleiss_kappa``          inter-rater agreement (multi-rater)
``ttft_p99``              time-to-first-token, 99th percentile
``tpot``                  time per output token (s/token)
``tps``                   tokens per second
``cost_per_task``         cost per completed task
``token_metering_error``  declared vs measured token count (relative error)
========================  ==========================================

All functions raise :class:`MetricError` rather than guessing when inputs are
empty, mismatched, or out of range.
"""

from __future__ import annotations

import math
from typing import Sequence

from .base import MetricError, MetricResult


# ── generic statistics ────────────────────────────────────────────────


def percentile(values: Sequence[float], q: float) -> float:
    """Linear-interpolated percentile (numpy-style, ``q`` in ``[0, 100]``)."""
    if not values:
        raise MetricError("percentile: empty input")
    if not 0.0 <= q <= 100.0:
        raise MetricError(f"percentile: q must be in [0, 100], got {q}")
    xs = sorted(float(v) for v in values)
    if len(xs) == 1:
        return xs[0]
    pos = (q / 100.0) * (len(xs) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1.0 - frac) + xs[hi] * frac


def _mean(values: Sequence[float]) -> float:
    if not values:
        raise MetricError("mean: empty input")
    return sum(float(v) for v in values) / len(values)


# ── safety / privacy ──────────────────────────────────────────────────


def attack_success_rate(successes: Sequence[bool]) -> MetricResult:
    """ASR = (# successful attacks) / (# attacks). Lower is better."""
    if not successes:
        raise MetricError("ASR: empty attack list")
    n = len(successes)
    hits = sum(1 for s in successes if s)
    return MetricResult(
        "asr", hits / n, unit="ratio", n=n,
        meta={"successes": hits, "total": n},
    )


# ── quality / calibration ─────────────────────────────────────────────


def brier_score(
    probabilities: Sequence[float], outcomes: Sequence[int]
) -> MetricResult:
    """Brier score = mean((p - o)^2) over binary outcomes. Lower is better."""
    probs = _validate_probs(probabilities)
    outs = _validate_outcomes(outcomes, len(probs))
    n = len(probs)
    bs = sum((p - o) ** 2 for p, o in zip(probs, outs)) / n
    return MetricResult("brier", bs, unit="score", n=n)


def expected_calibration_error(
    probabilities: Sequence[float],
    outcomes: Sequence[int],
    n_bins: int = 10,
) -> MetricResult:
    """ECE: |confidence - accuracy| averaged over confidence bins.

    ``ECE = sum_b (|B_b| / N) * |acc(B_b) - conf(B_b)|`` — lower is better.
    """
    if n_bins < 1:
        raise MetricError("ECE: n_bins must be >= 1")
    probs = _validate_probs(probabilities)
    outs = _validate_outcomes(outcomes, len(probs))
    n = len(probs)

    bin_sum_conf = [0.0] * n_bins
    bin_sum_acc = [0.0] * n_bins
    bin_count = [0] * n_bins
    for p, o in zip(probs, outs):
        idx = min(int(p * n_bins), n_bins - 1)
        bin_sum_conf[idx] += p
        bin_sum_acc[idx] += o
        bin_count[idx] += 1

    ece = 0.0
    bins: list[dict[str, float]] = []
    for b in range(n_bins):
        c = bin_count[b]
        if c == 0:
            bins.append({"bin": b, "count": 0})
            continue
        conf = bin_sum_conf[b] / c
        acc = bin_sum_acc[b] / c
        gap = abs(acc - conf)
        ece += (c / n) * gap
        bins.append(
            {"bin": b, "count": c, "confidence": conf, "accuracy": acc, "gap": gap}
        )
    return MetricResult("ece", ece, unit="score", n=n, meta={"bins": bins})


# ── methodology: inter-rater agreement ────────────────────────────────


def fleiss_kappa(ratings: Sequence[Sequence[int]]) -> MetricResult:
    """Fleiss' kappa over ``N`` items rated by a fixed number of raters.

    ``ratings[i]`` is the list of category labels assigned to item ``i``.
    Every item must have the same number of raters (>= 2).
    """
    if not ratings:
        raise MetricError("fleiss_kappa: empty ratings")
    n_raters = len(ratings[0])
    if n_raters < 2:
        raise MetricError("fleiss_kappa: need >= 2 raters")
    for i, row in enumerate(ratings):
        if len(row) != n_raters:
            raise MetricError(
                f"fleiss_kappa: item {i} has {len(row)} raters, expected {n_raters}"
            )
    n_items = len(ratings)
    categories = sorted({c for row in ratings for c in row})
    k = len(categories)
    idx = {c: j for j, c in enumerate(categories)}

    counts = [[0] * k for _ in range(n_items)]
    for i, row in enumerate(ratings):
        for c in row:
            counts[i][idx[c]] += 1

    total = n_items * n_raters
    p_cat = [0.0] * k
    for i in range(n_items):
        for j in range(k):
            p_cat[j] += counts[i][j]
    p_cat = [x / total for x in p_cat]

    p_item = []
    for i in range(n_items):
        s = sum(counts[i][j] ** 2 for j in range(k))
        p_item.append((s - n_raters) / (n_raters * (n_raters - 1)))
    p_bar = sum(p_item) / n_items
    p_e = sum(x * x for x in p_cat)

    if abs(1.0 - p_e) < 1e-12:
        # Degenerate: all raters used a single category. Perfect agreement
        # (p_bar == 1) is reported as kappa 1.0, otherwise 0.0.
        kappa = 1.0 if abs(p_bar - 1.0) < 1e-12 else 0.0
    else:
        kappa = (p_bar - p_e) / (1.0 - p_e)

    return MetricResult(
        "fleiss_kappa", kappa, unit="kappa", n=n_items,
        meta={"raters": n_raters, "categories": k, "p_bar": p_bar, "p_e": p_e},
    )


# ── performance ───────────────────────────────────────────────────────


def ttft_p99(latencies_ms: Sequence[float]) -> MetricResult:
    """Time-to-first-token, 99th percentile (milliseconds). Lower is better."""
    if not latencies_ms:
        raise MetricError("ttft_p99: empty latencies")
    p99 = percentile(latencies_ms, 99.0)
    return MetricResult(
        "ttft_p99", p99, unit="ms", n=len(latencies_ms),
        meta={
            "p50": percentile(latencies_ms, 50.0),
            "p90": percentile(latencies_ms, 90.0),
            "mean": _mean(latencies_ms),
        },
    )


def time_per_output_token(
    output_tokens: int, decode_seconds: float
) -> MetricResult:
    """TPOT = decode_seconds / output_tokens (seconds per token). Lower better."""
    if output_tokens <= 0:
        raise MetricError("tpot: output_tokens must be > 0")
    if decode_seconds <= 0:
        raise MetricError("tpot: decode_seconds must be > 0")
    return MetricResult(
        "tpot", decode_seconds / output_tokens, unit="s/token", n=output_tokens
    )


def tokens_per_second(total_tokens: int, seconds: float) -> MetricResult:
    """Throughput = total_tokens / seconds. Higher is better."""
    if total_tokens <= 0:
        raise MetricError("tps: total_tokens must be > 0")
    if seconds <= 0:
        raise MetricError("tps: seconds must be > 0")
    return MetricResult(
        "tps", total_tokens / seconds, unit="tokens/s", n=total_tokens
    )


# ── billing / cost ────────────────────────────────────────────────────


def cost_per_task(total_cost: float, n_tasks: int) -> MetricResult:
    """Average cost per completed task. Lower is better."""
    if n_tasks <= 0:
        raise MetricError("cost_per_task: n_tasks must be > 0")
    if total_cost < 0:
        raise MetricError("cost_per_task: total_cost must be >= 0")
    return MetricResult(
        "cost_per_task", total_cost / n_tasks, unit="cost/task", n=n_tasks,
        meta={"total_cost": total_cost},
    )


def token_metering_error(declared_tokens: int, measured_tokens: int) -> MetricResult:
    """Relative error between declared and independently measured tokens.

    ``|declared - measured| / measured`` — lower is better. A non-zero value
    indicates a billing-metering discrepancy.
    """
    if measured_tokens <= 0:
        raise MetricError("token_metering_error: measured_tokens must be > 0")
    if declared_tokens < 0:
        raise MetricError("token_metering_error: declared_tokens must be >= 0")
    rel = abs(declared_tokens - measured_tokens) / measured_tokens
    return MetricResult(
        "token_metering_error", rel, unit="ratio", n=measured_tokens,
        meta={"declared": declared_tokens, "measured": measured_tokens},
    )


# ── internal validators ───────────────────────────────────────────────


def _validate_probs(probabilities: Sequence[float]) -> list[float]:
    if not probabilities:
        raise MetricError("empty probabilities")
    probs = [float(p) for p in probabilities]
    for p in probs:
        if not 0.0 <= p <= 1.0:
            raise MetricError(f"probability out of range [0, 1]: {p}")
    return probs


def _validate_outcomes(outcomes: Sequence[int], expected: int) -> list[int]:
    outs = [int(o) for o in outcomes]
    if len(outs) != expected:
        raise MetricError(
            f"length mismatch: {len(outs)} outcomes vs {expected} probabilities"
        )
    for o in outs:
        if o not in (0, 1):
            raise MetricError(f"outcome must be 0 or 1, got {o}")
    return outs


# ── registry ──────────────────────────────────────────────────────────

METRIC_REGISTRY = {
    "asr": attack_success_rate,
    "brier": brier_score,
    "ece": expected_calibration_error,
    "fleiss_kappa": fleiss_kappa,
    "ttft_p99": ttft_p99,
    "tpot": time_per_output_token,
    "tps": tokens_per_second,
    "cost_per_task": cost_per_task,
    "token_metering_error": token_metering_error,
}


__all__ = [
    "METRIC_REGISTRY",
    "attack_success_rate",
    "brier_score",
    "cost_per_task",
    "expected_calibration_error",
    "fleiss_kappa",
    "percentile",
    "time_per_output_token",
    "token_metering_error",
    "tokens_per_second",
    "ttft_p99",
]
