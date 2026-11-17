"""
GCAE — Second Perspective Language Cognitive Audit Engine (vendored)
=====================================================================

Vendored from the `second-perspective` Cognitive Audit Engine (SPL/GCAE).

This is the **ten-operator** deterministic causal-audit pipeline:

    ⊙ ORI   Origin Anchor          — origin event / target state / energy constraints
    ⊗ NS    Narrative Strip        — strip rhetoric/emotion/moral veneer
    ⊕ IAP   Implicit Assumption    — surface unstated premises
    ⊿ LCH   Latch / Fragility      — locate weakest variable, compute Delta D
    ⊞ TPG   Rule-Free Thinking     — build □/→/⦿ topology + four parallel checks
    BFC     Binary Fact Check      — reduce a claim to true/false, never a third value
    ⚙ CCS   Causal-Chain Sync      — counterfactual & inverse-check
    ⇄ GRF   Gray Feedback          — rollout ladder + reality falsification alignment
    META    Meta-Causal Ledger     — chaos / wuji / illusion(A6) / tiandao(A10) / lunhui
    ⊚ STATE State Anchor           — pin responsibility + final verdict

The engine itself is a pure-Python, zero-dependency, fully deterministic
audit pipeline. No RNG, no LLM calls by default. An optional LLM provider
can be attached via :meth:`CognitiveAuditEngine.set_llm_provider`.

Two additions ride along with the operators, and neither of them can ever
block an audit on its own:

  * the **topology substrate** (:mod:`.plugins.topology`) — □/→/⦿ plus four
    parallel checks (consistency · constraint · closure · **time order**);
  * the **meta-causal ledger** (``META``) — a *measurement* tier operator:
    A6 narrative entropy, A10 audit entropy, gap ledger. Bad-looking numbers
    are not missing inputs, and only missing inputs halt a derivation.

For usage in NOMOS, prefer the :class:`CognitiveRiskScanner` adapter in
:mod:`second_perspective.audit.cognitive.adapter`, which bridges the
typed :class:`~second_perspective.models.schemas.DecisionRequest` /
:class:`~second_perspective.models.schemas.DecisionResult` models to the
dict-based context expected by the GCAE engine.

Reference: second-perspective/Second Perspective Engine.py
"""

from .engine import CognitiveAuditEngine, ResponsibilityAccount, AuditConfigLoader, AuditPlugin
from .plugins import (
    CORE_PLUGINS,
    OriginAnchorPlugin,
    NarrativeStripPlugin,
    ImplicitAssumptionPlugin,
    FragilityLatchPlugin,
    TopologyGraphPlugin,
    BinaryFactCheckPlugin,
    CausalChainSyncPlugin,
    GrayFeedbackPlugin,
    MetaCausalLedgerPlugin,
    StateAnchorPlugin,
    ReportRenderer,
    TRACE_ATTRIBUTION_PATTERNS,
    TOPOLOGY_VERSION,
    TOPOLOGY_GRAMMAR_VERSION,
    SYM_NODE, SYM_EDGE, SYM_CONSTRAINT, SYM_UPSTREAM, SYM_DOWNSTREAM,
    REL_INPUT, REL_OUTPUT,
    SEVERITY_HALT, SEVERITY_WARN,
    CHECK_CONSISTENCY, CHECK_CONSTRAINT, CHECK_CLOSURE, CHECK_TIME_ORDER,
    TopoNode, TopoEdge, Constraint, ValidationIssue,
    default_constraints, TopologyGraph, TopologyValidator,
    build_from_decision_context,
    SpiralLayer, SpiralStack,
)

__all__ = [
    "CognitiveAuditEngine",
    "ResponsibilityAccount",
    "AuditConfigLoader",
    "AuditPlugin",
    "CORE_PLUGINS",
    # 十算子
    "OriginAnchorPlugin",
    "NarrativeStripPlugin",
    "ImplicitAssumptionPlugin",
    "FragilityLatchPlugin",
    "TopologyGraphPlugin",
    "BinaryFactCheckPlugin",
    "CausalChainSyncPlugin",
    "GrayFeedbackPlugin",
    "MetaCausalLedgerPlugin",
    "StateAnchorPlugin",
    # 视图 / 底座 / 编排
    "ReportRenderer",
    "TRACE_ATTRIBUTION_PATTERNS",
    "TOPOLOGY_VERSION",
    "TOPOLOGY_GRAMMAR_VERSION",
    "SYM_NODE", "SYM_EDGE", "SYM_CONSTRAINT", "SYM_UPSTREAM", "SYM_DOWNSTREAM",
    "REL_INPUT", "REL_OUTPUT",
    "SEVERITY_HALT", "SEVERITY_WARN",
    "CHECK_CONSISTENCY", "CHECK_CONSTRAINT", "CHECK_CLOSURE", "CHECK_TIME_ORDER",
    "TopoNode", "TopoEdge", "Constraint", "ValidationIssue",
    "default_constraints", "TopologyGraph", "TopologyValidator",
    "build_from_decision_context",
    "SpiralLayer", "SpiralStack",
]
