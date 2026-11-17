"""Human / expert panel protocols & aggregation (module B, v0.6).

Dimension 7 (domain expertise), dimension 8 (κ > 0.70 human scoring) and ethics
review are **human judgements**. Consistent with the NOMOS kernel, this layer
does not let the engine adjudicate: it defines protocols and a deterministic
aggregation surface, and treats human input as an explicit, attributable input.
Concrete panels are supplied by the operating body.

Implemented here
----------------
- ``aggregate_panel_agreement`` — Fleiss' kappa over expert scores.
- ``aggregate_by_dimension``    — per-dimension agreement.
- ``kappa_metric_result``       — agreement expressed as a ``MetricResult`` so it
  plugs straight into the measurement layer's ``methodology-control`` pack.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Protocol, Sequence

from ..measurement.base import MetricResult


@dataclass(frozen=True)
class ExpertScore:
    """One expert's discrete score for one item on one dimension.

    ``score`` is a discrete category (e.g. 1..5) so inter-rater agreement is
    well-defined; free-text justification rides along in ``rationale``.
    """

    item_id: str
    expert_id: str
    dimension: str
    score: int
    rationale: str = ""


class ExpertPanel(Protocol):
    """A source of expert judgements (to be implemented by an operating body)."""

    id: str
    description: str

    def collect(self, items: Sequence[object]) -> list[ExpertScore]: ...


@dataclass(frozen=True)
class PanelAgreement:
    kappa: float
    meets_threshold: bool
    n_items: int
    n_experts: int
    threshold: float = 0.70


def aggregate_panel_agreement(
    scores: Sequence[ExpertScore], threshold: float = 0.70
) -> PanelAgreement:
    """Fleiss' kappa over expert scores, restricted to fully-rated items.

    Only items rated by *all* experts contribute (rectangular requirement of
    Fleiss' kappa). The default ``threshold=0.70`` mirrors the audit standard.
    """
    if not scores:
        raise ValueError("aggregate_panel_agreement: empty score list")

    by_item: dict[str, list[int]] = defaultdict(list)
    experts: set[str] = set()
    for s in scores:
        by_item[s.item_id].append(s.score)
        experts.add(s.expert_id)

    n_experts = len(experts)
    rows = [v for v in by_item.values() if len(v) == n_experts]
    if not rows:
        raise ValueError("no item is rated by all experts")

    from ..measurement.metrics import fleiss_kappa

    res = fleiss_kappa(rows)
    return PanelAgreement(
        kappa=res.value,
        meets_threshold=res.value >= threshold,
        n_items=len(rows),
        n_experts=n_experts,
        threshold=threshold,
    )


def aggregate_by_dimension(
    scores: Sequence[ExpertScore], threshold: float = 0.70
) -> dict[str, PanelAgreement]:
    """Per-dimension agreement (expert scoring is naturally per-domain)."""
    by_dim: dict[str, list[ExpertScore]] = defaultdict(list)
    for s in scores:
        by_dim[s.dimension].append(s)
    return {
        dim: aggregate_panel_agreement(by_dim[dim], threshold)
        for dim in sorted(by_dim)
    }


def kappa_metric_result(
    scores: Sequence[ExpertScore], threshold: float = 0.70
) -> MetricResult:
    """Express panel agreement as a ``MetricResult`` (metric_id ``fleiss_kappa``).

    The result plugs straight into the measurement layer's
    ``methodology-control`` pack, whose gate is ``fleiss_kappa >= 0.70``.
    """
    ag = aggregate_panel_agreement(scores, threshold)
    return MetricResult(
        metric_id="fleiss_kappa",
        value=ag.kappa,
        unit="kappa",
        n=ag.n_items,
        passed=ag.meets_threshold,
        threshold=f">= {threshold}",
        meta={
            "n_experts": ag.n_experts,
            "n_items": ag.n_items,
            "dimensions": sorted({s.dimension for s in scores}),
        },
    )


__all__ = [
    "ExpertPanel",
    "ExpertScore",
    "PanelAgreement",
    "aggregate_by_dimension",
    "aggregate_panel_agreement",
    "kappa_metric_result",
]
