"""
⊞ TPG — 无规则思维拓扑图 / Rule-Free Thinking Topology
==============================================================

Porting provenance
------------------
Copied verbatim（只搬不改）from ``second-perspective/Second Perspective Engine.py``
（``second-perspective`` 分支的「十算子 + 元因果账本 + 自主进化层」状态）。
进入本仓库时只动了两件事：

  1. 补了一段 import 前导（源文件是单文件，其模块级 import 在 6000 行文件的顶部）；
  2. 其余一字未改 —— 没有改逻辑、没有改常数、没有改阈值。

Nomos 的插件契约比源引擎薄：一个插件就是「带 PLUGIN_NAME / PLUGIN_VERSION /
PLUGIN_DESCRIPTION 与 analyze(ctx) -> dict 的类」。以下代码天然满足该契约。

Copyright (c) 2026 Shanghai Linming Junhua Technology Co., Ltd.
              and NOHN AI TECHNOLOGY PTE. LTD.
All rights reserved.  Dual-track license — see ../LICENSE.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

from .topology import (
    SYM_NODE, SYM_EDGE, SYM_CONSTRAINT, SYM_UPSTREAM, SYM_DOWNSTREAM,
    REL_INPUT, REL_OUTPUT,
    SEVERITY_HALT, SEVERITY_WARN,
    CHECK_CONSISTENCY, CHECK_CONSTRAINT, CHECK_CLOSURE, CHECK_TIME_ORDER,
    TOPOLOGY_VERSION, TOPOLOGY_GRAMMAR_VERSION,
    TopoNode, TopoEdge, Constraint, ValidationIssue,
    default_constraints, TopologyGraph, TopologyValidator,
    build_from_decision_context,
)

# ============================================================================
# 分区③ 算子 ⊞TPG — 无规则思维拓扑图 / Thinking Topology
# ============================================================================
# TPG — ⊞ 无规则思维拓扑图 / Rule-Free Thinking Topology Plugin
# ============================================================
#
# 把决策上下文投影成无语义拓扑图 G，并跑完三类编译期并行校验。
#
# 「无规则」的含义
# ----------------
# 不是「没有规则」，而是「不预设规则」。上游语言（.spd）带着 Decision /
# Assumption / Branch 这些语义标签进来；本算子把它们全部拆成 □ 与 →，
# 让结构先于命名成立。规范原话：
#
#     关系优先于实体。删除所有连接关系后实体自动消失。
#
# 因此本算子产出的图里不存在「这是决策节点」这种断言，只有
# 「□D 是 □0 的下游、□A1 的上游」。语义标签只在最后一步由
# relative_label() 做外部映射，不参与任何判定。
#
# 输出担保
# --------
#     G0          未校验的纯拓扑
#     validation  三类并行校验结果（一致性/约束满足/拓扑闭合）
#     graph_hash  纯结构指纹——不含标签、不含 provenance，
#                 因此「同一结构不同命名」得到同一指纹，
#                 「同一命名不同结构」得到不同指纹。
#
# 状态映射
# --------
#     存在致命错误（一致性/约束满足）  → BLOCKED     推演终止
#     存在闭合警告（悬空/悖论）        → WARNING     可强制继续，但结果无效
#     三类全过                        → PASS
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class TopologyGraphPlugin:
    """⊞ 算子：无规则思维拓扑图。"""

    PLUGIN_NAME = "TPG"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Rule-Free Thinking Topology — 无语义拓扑构建 + 三类并行校验"

    TOPOLOGY_KEYS = ("topology", "topo", "graph", "拓扑")

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        explicit = self._extract_explicit_topology(ctx)

        if explicit is not None:
            graph = self._parse_topology(explicit)
            source = "EXPLICIT"
        else:
            origin = ctx.get("origin") or ctx.get("origin_event")
            origin_text = origin if isinstance(origin, str) else ""
            graph = build_from_decision_context(ctx, origin=origin_text)
            source = "PROJECTED"

        validation = TopologyValidator.run_all(graph)
        labels = graph.labels()

        if validation["fatal"]:
            status, reason = "BLOCKED", "TOPOLOGY_ILLEGAL"
        elif not validation["result_valid"]:
            status, reason = "WARNING", "TOPOLOGY_OPEN"
        elif source == "PROJECTED" and not graph.edges:
            # 空图不算「通过」：没有边就没有结构，任何结论都不成立。
            status, reason = "WARNING", "EMPTY_TOPOLOGY"
        else:
            status, reason = "PASS", "TOPOLOGY_CLOSED"

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "source": source,
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "graph_hash": graph.graph_hash(),
            "topology": graph.to_dict(),
            # 公理 5：链内时序与观测位置。二者都不参与 pass/fail 判定
            # （判定在 validation.time_order 里），这里单独暴露一份，
            # 便于上层直接消费「这条链怎么排序、我站在哪条链上」。
            "time_order": graph.assign_time_order(),
            "validation": validation,
            "relative_labels": labels,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _extract_explicit_topology(ctx: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for key in TopologyGraphPlugin.TOPOLOGY_KEYS:
            val = ctx.get(key)
            if isinstance(val, dict) and val:
                return val
        return None

    @staticmethod
    def _parse_topology(spec: Dict[str, Any]) -> TopologyGraph:
        """解析显式拓扑声明。字段缺位不补默认值——缺就是缺。"""
        graph = TopologyGraph(layer=int(spec.get("layer", 0) or 0))

        raw_nodes = spec.get("nodes") or []
        for item in raw_nodes:
            if isinstance(item, str):
                graph.add_node(item)
            elif isinstance(item, dict) and item.get("id"):
                graph.add_node(str(item["id"]), note=str(item.get("note", "")))

        raw_edges = spec.get("edges") or []
        for item in raw_edges:
            if not isinstance(item, dict):
                continue
            src, dst = item.get("src"), item.get("dst")
            if not src or not dst:
                continue
            graph.add_edge(TopoEdge(
                src=str(src), dst=str(dst),
                relation=str(item.get("relation", "causal")),
                weight=item.get("weight"),
                validity=item.get("validity"),
                falsifiable=bool(item.get("falsifiable", True)),
                delta_d=item.get("delta_d"),
                note=str(item.get("note", "")),
                # 公理 5：允许显式声明链内时序；缺位即 None，由引擎按
                # 最长路径派生 —— 「缺就是缺」，不补默认值。
                t=item.get("t"),
            ))

        raw_constraints = spec.get("constraints")
        if isinstance(raw_constraints, list) and raw_constraints:
            graph.constraints = {}
            for c in raw_constraints:
                if isinstance(c, dict) and c.get("name"):
                    graph.constraints[str(c["name"])] = Constraint(
                        name=str(c["name"]),
                        kind=str(c.get("kind", "weight_range")),
                        params=dict(c.get("params", {})),
                        note=str(c.get("note", "")),
                    )
        elif not graph.constraints:
            graph.constraints = default_constraints()

        graph.trace("⊞TPG", "PARSE_EXPLICIT", {
            "nodes": len(graph.nodes), "edges": len(graph.edges),
        })
        return graph
