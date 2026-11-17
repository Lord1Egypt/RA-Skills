"""
SPL Core Audit Plugins — Official Ten-Operator Pack
====================================================

This package contains the ten core audit operators that form the
deterministic causal-audit pipeline of the Second Perspective Language,
in pipeline order:

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

All plugins are pure-Python, zero-dependency, deterministic (no RNG,
no LLM calls). ``CORE_PLUGINS`` is listed in the order the engine runs them:
the engine keeps registration order and only forces STATE last.

The topology substrate (``.topology``) and the spiral layer stack
(``.spiral``) are not plugins; they are the machinery TPG / META rely on,
re-exported here so callers need only one import site.

Copyright (c) 2026 Shanghai Linming Junhua Technology Co., Ltd.
              and NOHN AI TECHNOLOGY PTE. LTD.
All rights reserved.  Dual-track license — see ../LICENSE.
"""

from .ns   import NarrativeStripPlugin
from .iap  import ImplicitAssumptionPlugin
from .lch  import FragilityLatchPlugin
from .ccs  import CausalChainSyncPlugin
from .state import StateAnchorPlugin
from .report import ReportRenderer

from .topology import (
    TOPOLOGY_VERSION,
    TOPOLOGY_GRAMMAR_VERSION,
    SYM_NODE, SYM_EDGE, SYM_CONSTRAINT, SYM_UPSTREAM, SYM_DOWNSTREAM,
    REL_INPUT, REL_OUTPUT,
    SEVERITY_HALT, SEVERITY_WARN,
    CHECK_CONSISTENCY, CHECK_CONSTRAINT, CHECK_CLOSURE, CHECK_TIME_ORDER,
    T101_ROLE_CONFLICT, T102_CONTRADICTORY_EDGE,
    T201_PARAM_OUT_OF_RANGE, T202_REQUIRED_PARAM_MISSING, T203_DEGREE_EXCEEDED,
    T301_DANGLING_EDGE, T302_DANGLING_NODE, T303_CAUSAL_PARADOX,
    T305_FORK_VIOLATION, T307_TIME_ORDER_INVERTED, T308_TIME_UNASSIGNABLE,
    TopoNode, TopoEdge, Constraint, ValidationIssue,
    default_constraints, TopologyGraph, TopologyValidator,
    build_from_decision_context,
)
from .ori  import OriginAnchorPlugin
from .tpg  import TopologyGraphPlugin
from .bfc  import BinaryFactCheckPlugin
from .grf  import GrayFeedbackPlugin
from .meta import MetaCausalLedgerPlugin, TRACE_ATTRIBUTION_PATTERNS
from .spiral import SpiralLayer, SpiralStack

# 官方十算子，按流水线顺序排列。引擎只额外强制 STATE 最后，
# 其余保持注册顺序 —— 所以这张列表的顺序就是执行顺序。
CORE_PLUGINS = [
    OriginAnchorPlugin,          # ⊙ 第一原点锚定
    NarrativeStripPlugin,        # ⊗ 去语义化
    ImplicitAssumptionPlugin,    # ⊕ 约束挖掘
    FragilityLatchPlugin,        # ⊿ 薄弱点加固
    TopologyGraphPlugin,         # ⊞ 无规则思维拓扑图
    BinaryFactCheckPlugin,       #   二元事实校验
    CausalChainSyncPlugin,       # ⚙ 因果链同步
    GrayFeedbackPlugin,          # ⇄ 灰度执行与现实反馈
    MetaCausalLedgerPlugin,      #   元因果账本（永不阻断）
    StateAnchorPlugin,           # ⊚ 责任锚定 + 最终裁定
]

__all__ = [
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
    "T101_ROLE_CONFLICT", "T102_CONTRADICTORY_EDGE",
    "T201_PARAM_OUT_OF_RANGE", "T202_REQUIRED_PARAM_MISSING", "T203_DEGREE_EXCEEDED",
    "T301_DANGLING_EDGE", "T302_DANGLING_NODE", "T303_CAUSAL_PARADOX",
    "T305_FORK_VIOLATION", "T307_TIME_ORDER_INVERTED", "T308_TIME_UNASSIGNABLE",
    "TopoNode", "TopoEdge", "Constraint", "ValidationIssue",
    "default_constraints", "TopologyGraph", "TopologyValidator",
    "build_from_decision_context",
    "SpiralLayer", "SpiralStack",
]
