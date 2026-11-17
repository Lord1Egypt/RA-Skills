"""Paired comparison statistics for audit reporting (module C, v0.6).

Implements the three statistical outputs the test specification (§5.3)
requires of every report, on top of per-item records:

- ``wilson_interval`` — the Margin layer: confidence interval of a pass rate.
- ``mcnemar_exact``   — the Paired Test layer: two systems on the same items.
- ``churn``           — the Churn layer: which item outcomes flipped.

Design invariants (aligned with the NOMOS kernel):

- Determinism: every function is a pure function of its declared inputs.
  No resampling, no randomness — the exact McNemar p-value is computed with
  integer arithmetic and the Wilson interval is closed-form, so a third party
  can recompute byte-identical numbers.
- No invention: unusable input (empty, mismatched id sets, out-of-range
  counts) raises :class:`ComparisonError` instead of being coerced. Where a
  test is undefined (no discordant pairs) the result says ``None`` rather
  than fabricating a p-value.
- Provenance: result objects carry the raw counts, ``n`` and the confidence
  level each number was derived from.

``churn`` doubles as the replay check for iron law 2: re-running identical
inputs must produce zero churn — any flip is a counterexample.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Mapping


class ComparisonError(ValueError):
    """Raised when comparison input is unusable (empty / mismatched / OOR)."""


# Two-sided z values for the declared confidence levels. Kept as an explicit
# table rather than computed from a rational approximation: a third party can
# verify every value against any statistics reference and re-derive the
# intervals with textbook arithmetic.
_Z_TABLE: dict[float, float] = {
    0.80: 1.2815515655446004,
    0.90: 1.6448536269514722,
    0.95: 1.959963984540054,
    0.98: 2.3263478740408408,
    0.99: 2.5758293035489004,
    0.999: 3.2905267314919255,
}


def _z_for(confidence: float) -> float:
    for level, z in _Z_TABLE.items():
        if abs(confidence - level) < 1e-12:
            return z
    supported = ", ".join(f"{level:g}" for level in sorted(_Z_TABLE))
    raise ComparisonError(
        f"unsupported confidence level {confidence!r}; supported: {supported}"
    )


def _validate_outcomes(records: Mapping[str, bool], where: str) -> None:
    for item_id, outcome in records.items():
        if not isinstance(outcome, bool):
            raise ComparisonError(
                f"{where}[{item_id!r}] must be bool, "
                f"got {type(outcome).__name__}"
            )


def _enumerate_ids(label: str, ids: tuple[str, ...], cap: int = 10) -> str:
    shown = ", ".join(ids[:cap])
    more = f" (+{len(ids) - cap} more)" if len(ids) > cap else ""
    return f"{label}: {shown}{more}"


# ── margin layer ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class WilsonInterval:
    """Wilson score interval for a binomial proportion."""

    k: int
    n: int
    confidence: float
    estimate: float
    lo: float
    hi: float
    z: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "k": self.k,
            "n": self.n,
            "confidence": self.confidence,
            "estimate": self.estimate,
            "lo": self.lo,
            "hi": self.hi,
            "z": self.z,
        }


def wilson_interval(k: int, n: int, confidence: float = 0.95) -> WilsonInterval:
    """Closed-form Wilson score interval for ``k`` successes in ``n`` trials.

    Preferred over the textbook normal (Wald) interval because it keeps
    coverage at extreme rates and small samples: ``k=0`` still yields a
    non-zero upper bound instead of a degenerate zero-width interval, and the
    bounds never leave ``[0, 1]``.
    """
    if n <= 0:
        raise ComparisonError("wilson_interval: n must be > 0")
    if not 0 <= k <= n:
        raise ComparisonError(f"wilson_interval: k must be in [0, n], got {k}/{n}")
    z = _z_for(confidence)
    p_hat = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p_hat + z2 / (2.0 * n)) / denom
    half = (z / denom) * math.sqrt(
        p_hat * (1.0 - p_hat) / n + z2 / (4.0 * n * n)
    )
    # Exact boundary values: k=0 -> lo=0 and k=n -> hi=1 hold mathematically;
    # pin them so floating-point cancellation cannot leave a residue.
    lo = 0.0 if k == 0 else max(0.0, center - half)
    hi = 1.0 if k == n else min(1.0, center + half)
    return WilsonInterval(
        k=k,
        n=n,
        confidence=confidence,
        estimate=p_hat,
        lo=lo,
        hi=hi,
        z=z,
    )


# ── paired test layer ─────────────────────────────────────────────────


@dataclass(frozen=True)
class McNemarResult:
    """Exact McNemar test over discordant pairs.

    Orientation follows the standard convention: ``b`` counts items where the
    first system passes and the second fails; ``c`` the reverse.
    """

    b: int
    c: int
    n_discordant: int
    p_value: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "b": self.b,
            "c": self.c,
            "n_discordant": self.n_discordant,
            "p_value": self.p_value,
        }


def mcnemar_exact(b: int, c: int) -> McNemarResult:
    """Exact two-sided McNemar test, no normal approximation.

    Under the null hypothesis the discordant pairs split with probability
    ``1/2``, so ``b | (b + c) ~ Binomial(b + c, 1/2)`` and the two-sided
    p-value is ``min(1, 2 * P(X <= min(b, c)))``. The sum is accumulated with
    exact integer arithmetic (``math.comb`` values via the multiplicative
    recurrence ``C(n, i) = C(n, i-1) * (n - i + 1) / i``), so the result is
    deterministic and independent of any floating-point library.

    Intended for the discordant counts seen in audit practice; the integer
    accumulator grows linearly with ``b + c``.
    """
    if b < 0 or c < 0:
        raise ComparisonError(
            f"mcnemar_exact: counts must be >= 0, got b={b}, c={c}"
        )
    n = b + c
    if n == 0:
        raise ComparisonError("mcnemar_exact: no discordant pairs (b + c == 0)")
    m = min(b, c)
    total = 1 << n
    acc = 1  # C(n, 0)
    term = 1
    for i in range(1, m + 1):
        term = term * (n - i + 1) // i  # exact: term == C(n, i)
        acc += term
        if 2 * acc >= total:
            # p is capped at 1.0 and the sum only grows — safe to stop.
            return McNemarResult(b=b, c=c, n_discordant=n, p_value=1.0)
    p = min(1.0, 2 * acc / total)
    return McNemarResult(b=b, c=c, n_discordant=n, p_value=p)


# ── churn layer ───────────────────────────────────────────────────────


@dataclass(frozen=True)
class ChurnReport:
    """Item-level outcome accounting between two runs.

    Ids present in only one run are reported in their own buckets — never
    silently intersected away, so the report shows exactly what was compared.
    """

    n_common: int
    stable: int
    flipped_up: tuple[str, ...]  # fail -> pass
    flipped_down: tuple[str, ...]  # pass -> fail
    only_in_a: tuple[str, ...]
    only_in_b: tuple[str, ...]

    @property
    def n_flips(self) -> int:
        return len(self.flipped_up) + len(self.flipped_down)

    def is_zero(self) -> bool:
        return not (
            self.flipped_up
            or self.flipped_down
            or self.only_in_a
            or self.only_in_b
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_common": self.n_common,
            "stable": self.stable,
            "n_flips": self.n_flips,
            "flipped_up": list(self.flipped_up),
            "flipped_down": list(self.flipped_down),
            "only_in_a": list(self.only_in_a),
            "only_in_b": list(self.only_in_b),
        }


def churn(
    records_a: Mapping[str, bool], records_b: Mapping[str, bool]
) -> ChurnReport:
    """Which item outcomes flipped from ``records_a`` to ``records_b``.

    Ordering of every bucket is deterministic (sorted ids), so two parties
    computing churn over the same records get byte-identical reports.
    """
    _validate_outcomes(records_a, "records_a")
    _validate_outcomes(records_b, "records_b")
    keys_a = set(records_a)
    keys_b = set(records_b)
    common = sorted(keys_a & keys_b)
    flipped_up = tuple(
        i for i in common if not records_a[i] and records_b[i]
    )
    flipped_down = tuple(
        i for i in common if records_a[i] and not records_b[i]
    )
    return ChurnReport(
        n_common=len(common),
        stable=len(common) - len(flipped_up) - len(flipped_down),
        flipped_up=flipped_up,
        flipped_down=flipped_down,
        only_in_a=tuple(sorted(keys_a - keys_b)),
        only_in_b=tuple(sorted(keys_b - keys_a)),
    )


def assert_zero_churn(
    records_a: Mapping[str, bool], records_b: Mapping[str, bool]
) -> ChurnReport:
    """Replay check for iron law 2: identical inputs must produce zero churn.

    Raises :class:`ComparisonError` enumerating the offending item ids;
    returns the (zero) report otherwise.
    """
    report = churn(records_a, records_b)
    if not report.is_zero():
        details = "; ".join(
            _enumerate_ids(label, ids)
            for label, ids in (
                ("flipped_up", report.flipped_up),
                ("flipped_down", report.flipped_down),
                ("only_in_a", report.only_in_a),
                ("only_in_b", report.only_in_b),
            )
            if ids
        )
        raise ComparisonError(f"zero-churn replay violated — {details}")
    return report


# ── combined report ───────────────────────────────────────────────────


@dataclass(frozen=True)
class PairedComparison:
    """A paired comparison of two systems over the same items.

    ``only_a`` is McNemar's ``b`` (A passes, B fails); ``only_b`` is ``c``
    (A fails, B passes). ``mcnemar_p`` is ``None`` when the systems never
    disagreed — the paired test is undefined and no p-value is fabricated.
    """

    n_pairs: int
    both_pass: int
    both_fail: int
    only_a: int
    only_b: int
    rate_a: float
    rate_b: float
    rate_delta: float  # rate_a - rate_b
    interval_a: WilsonInterval
    interval_b: WilsonInterval
    mcnemar_p: float | None
    churn: ChurnReport

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_pairs": self.n_pairs,
            "both_pass": self.both_pass,
            "both_fail": self.both_fail,
            "only_a": self.only_a,
            "only_b": self.only_b,
            "rate_a": self.rate_a,
            "rate_b": self.rate_b,
            "rate_delta": self.rate_delta,
            "interval_a": self.interval_a.to_dict(),
            "interval_b": self.interval_b.to_dict(),
            "mcnemar_p": self.mcnemar_p,
            "churn": self.churn.to_dict(),
        }


def compare_paired(
    records_a: Mapping[str, bool],
    records_b: Mapping[str, bool],
    confidence: float = 0.95,
) -> PairedComparison:
    """Full paired report: margin + paired test + churn over the same items.

    ``records_a`` / ``records_b`` map item id -> pass/fail. The id sets must
    match exactly; a mismatch raises with the offending ids enumerated
    (aligning the inputs is the caller's job — the comparison layer never
    guesses which items correspond).
    """
    _validate_outcomes(records_a, "records_a")
    _validate_outcomes(records_b, "records_b")
    churn_report = churn(records_a, records_b)
    if churn_report.only_in_a or churn_report.only_in_b:
        details = "; ".join(
            _enumerate_ids(label, ids)
            for label, ids in (
                ("only_in_a", churn_report.only_in_a),
                ("only_in_b", churn_report.only_in_b),
            )
            if ids
        )
        raise ComparisonError(
            f"compare_paired: id sets do not match — {details}"
        )
    n = churn_report.n_common
    if n == 0:
        raise ComparisonError("compare_paired: no items to compare")

    common = sorted(set(records_a) & set(records_b))
    both_pass = sum(1 for i in common if records_a[i] and records_b[i])
    both_fail = sum(1 for i in common if not records_a[i] and not records_b[i])
    only_a = sum(1 for i in common if records_a[i] and not records_b[i])
    only_b = sum(1 for i in common if not records_a[i] and records_b[i])
    passes_a = both_pass + only_a
    passes_b = both_pass + only_b
    rate_a = passes_a / n
    rate_b = passes_b / n
    mcnemar = (
        mcnemar_exact(b=only_a, c=only_b) if (only_a + only_b) else None
    )
    return PairedComparison(
        n_pairs=n,
        both_pass=both_pass,
        both_fail=both_fail,
        only_a=only_a,
        only_b=only_b,
        rate_a=rate_a,
        rate_b=rate_b,
        rate_delta=rate_a - rate_b,
        interval_a=wilson_interval(passes_a, n, confidence),
        interval_b=wilson_interval(passes_b, n, confidence),
        mcnemar_p=mcnemar.p_value if mcnemar else None,
        churn=churn_report,
    )


__all__ = [
    "ChurnReport",
    "ComparisonError",
    "McNemarResult",
    "PairedComparison",
    "WilsonInterval",
    "assert_zero_churn",
    "churn",
    "compare_paired",
    "mcnemar_exact",
    "wilson_interval",
]
