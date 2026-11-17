"""Cognitive risk scanner — structured challenge layer backed by GCAE.

This module wraps the vendored SPL/GCAE cognitive audit engine behind NOMOS
typed models.  It does NOT diagnose people, read motives, or replace human
judgment.  Every finding is derived deterministically from declared inputs
and the decision structure.

The engine ships **ten** operators.  Which of them this scanner can actually
*feed* is determined by NOMOS's input contract and is declared explicitly in
:data:`second_perspective.audit.cognitive.adapter.ADAPTER_BASE_OPERATORS` plus the
conditional set — see the rationale there.  Registering an operator whose
required inputs a given request cannot declare does not make the audit stronger;
it makes every audit halt on a permanent vacuum (a measured fact, not a guess).
Hence ORI / GRF engage only when the request actually declares an origin or a
rollout ladder.

The raw GCAE audit dictionary is preserved on the returned report so that
callers that want the full operator-level output (e.g. bilingual report
rendering) can use it directly.
"""

from __future__ import annotations

from typing import Any

from ..audit.cognitive.adapter import run_gcae_audit
from ..models.schemas import CognitiveAuditReport, DecisionRequest, DecisionResult


class CognitiveRiskScanner:
    """Deterministic structural cognitive-risk scanner (GCAE-backed).

    Wraps the SPL/GCAE pipeline.  Operators actually fed by this scanner:

        NS    — narrative strip (rhetoric/emotion/moral veneer)
        IAP   — implicit assumption perspective (unstated premises)
        LCH   — fragility latch (weakest variable, Delta D)
        TPG   — rule-free thinking topology (□/→/⦿ + four parallel checks,
                including chain-internal time order — new in 1.1.0)
        BFC   — binary fact check (off unless ``facts`` are declared)
        CCS   — causal-chain sync (inverse / counterfactual / integrity)
        META  — meta-causal ledger (A6 narrative entropy · A10 audit entropy ·
                gap ledger; measures only, can never block — new in 1.1.0)
        STATE — responsibility anchor + final verdict
    """

    SCANNER_VERSION = "GCAE-1.1.0"

    def __init__(self, policy: Any) -> None:
        self.policy = policy

    def scan(self, request: DecisionRequest, result: DecisionResult) -> CognitiveAuditReport:
        """Run the GCAE five-operator audit and return a NOMOS CognitiveAuditReport."""
        report, _raw = run_gcae_audit(request, result, self.policy)
        return report