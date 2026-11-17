"""Causal reconstruction runner — bridges the hub orchestrator to the
CausalReconstructor in the decision layer.
"""

from __future__ import annotations

from ..decision.reconstruction import CausalReconstructor
from ..models.schemas import CausalReconstructionReport, DecisionRequest, DeviationSignal


def run_causal_reconstruction(
    request: DecisionRequest,
    signals: list[DeviationSignal],
) -> CausalReconstructionReport:
    """Run the full causal reconstruction pipeline and return a report.

    This is a convenience wrapper so that the hub orchestrator does not
    need to import the CausalReconstructor directly.
    """
    reconstructor = CausalReconstructor()
    return reconstructor.reconstruct(request, signals)