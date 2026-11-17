"""
↻ 叠加螺旋层栈 / Superimposed Spiral Stack
=================================================

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
# 分区④ 编排层 ↻ — 叠加螺旋层栈 / Superimposed Spiral Stack
# ============================================================================
# SPR — ↻ 叠加螺旋式迭代思考链路 / Superimposed Spiral Chain
# =========================================================
#
# 实现 p♾️q 因果螺旋：每一次 ⊛ 拓扑重构生成**新的拓扑层**，而**不是覆盖旧层**。
#
# 叠加 ≠ 覆盖
# -----------
# 引擎 v1 时代的迭代是一行 `ctx.update(delta)`：上一轮的结构被新字典抹掉，
# 所以它只能做「重试」，做不成「螺旋」。螺旋的定义性特征是：
#
#     已收敛的子图被冻结为骨架，后续每一层在这个骨架上继续生长。
#
# 因此本模块把「收敛了什么」变成不可撤销的账目：
#
#     frozen 集合单调不减。第 n 层冻结的节点，第 n+1 层不得解冻。
#     一旦检出解冻，记 SUPERPOSITION_VIOLATION —— 螺旋退化为覆盖，
#     此时「迭代」只是在原地打转，正是规范要拦截的那类「假螺旋」。
#
# 三道硬约束
# ----------
#   1. 原点不可漂移   origin_hash 一旦确立即为锚点；后续层不同即 ORIGIN_DRIFT。
#                     这是螺旋最致命的失效模式——绕圈绕到目标已经不是原来那个。
#   2. 能量守恒       ↻ 每层消耗 loop_cost；预算不足以再走一层即停。
#                     拓扑无边界，但预算有硬顶（因果承接公理）。
#   3. 半径单调       radius = 未收敛风险集规模。半径必须随层数收敛；
#                     若连续两层半径不降且状态为 DIVERGED，标记 FLAT_SPIRAL。
#
# 本模块只做账，不做判定——收敛状态由引擎的 ConvergenceChecker 给出。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

@dataclass
class SpiralLayer:
    """螺旋的一圈。层是只读快照，生成后不再改动。"""

    index: int
    state: str
    origin_hash: str
    radius: int
    risk_set: List[str]
    frozen_nodes: List[str]
    graph_hash: str
    topology: Dict[str, Any]
    layer_hash: str
    cost: float
    energy_left: Optional[float]
    # 到目标稳态 S* 的距离 = (风险集规模, 是否有未决假设)，字典序比较。
    # 极限收敛器判定「还在不在逼近」的唯一依据。
    distance: Tuple[int, int] = (0, 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index, "state": self.state,
            "origin_hash": self.origin_hash, "radius": self.radius,
            "risk_set": self.risk_set, "frozen_nodes": self.frozen_nodes,
            "graph_hash": self.graph_hash, "layer_hash": self.layer_hash,
            "cost": self.cost, "energy_left": self.energy_left,
            "distance": list(self.distance),
            "topology": self.topology,
        }


class SpiralStack:
    """螺旋层栈：管账、管冻结、管漂移。"""

    def __init__(self, energy_budget: Optional[float] = None, loop_cost: float = 1.0):
        if loop_cost <= 0:
            raise ValueError("loop_cost must be > 0")
        if energy_budget is not None and energy_budget < 0:
            raise ValueError("energy_budget must be >= 0")
        self.energy_budget = None if energy_budget is None else float(energy_budget)
        self.loop_cost = float(loop_cost)
        self.layers: List[SpiralLayer] = []
        self._origin_anchor: Optional[str] = None
        self._frozen: Set[str] = set()
        self._spent: float = 0.0
        self.violations: List[Dict[str, Any]] = []

    # -------- 账目 --------

    @property
    def energy_left(self) -> Optional[float]:
        if self.energy_budget is None:
            return None
        return round(self.energy_budget - self._spent, 6)

    def can_run(self, count: int = 1) -> bool:
        """预算是否还够再走 count 层。无预算声明时恒为 True（拓扑无边界）。"""
        if self.energy_budget is None:
            return True
        return (self._spent + self.loop_cost * count) <= self.energy_budget + 1e-9

    @property
    def frozen_nodes(self) -> List[str]:
        return sorted(self._frozen)

    # -------- 漂移 --------

    def origin_drift(self, origin_hash: str) -> bool:
        """原点漂移检测。首次确立锚点，其后不一致即为漂移。"""
        if not origin_hash:
            return False
        if self._origin_anchor is None:
            self._origin_anchor = origin_hash
            return False
        return origin_hash != self._origin_anchor

    @property
    def origin_anchor(self) -> Optional[str]:
        return self._origin_anchor

    # -------- 压栈 --------

    def push(
        self,
        *,
        state: str,
        origin_hash: str,
        risk_set: Sequence[str],
        graph_hash: str,
        topology: Dict[str, Any],
        converged_nodes: Sequence[str] = (),
        index: Optional[int] = None,
        unresolved: bool = False,
    ) -> SpiralLayer:
        """压入新的一层。

        converged_nodes 是本层**新增**收敛的节点（引擎按相邻两层 1-邻域一致判定），
        压栈时并入冻结集合——只增不减。

        覆盖检测：已冻结节点必须仍存在于本层拓扑中。若某个被宣布收敛的节点
        在后续层里消失了，说明这一层把上层抹掉了——螺旋退化成了覆盖。

        unresolved 表示本层是否仍有未决假设（IAP missing_required）；它与半径共同
        构成本层的「距离」distance = (风险集规模, 是否有未决假设)。
        """
        idx = len(self.layers) if index is None else index

        node_ids = {
            str(n.get("id")) for n in (topology or {}).get("nodes", [])
            if isinstance(n, dict) and n.get("id")
        }
        vanished = sorted(self._frozen - node_ids)
        if vanished:
            self.violations.append({
                "code": "SUPERPOSITION_VIOLATION",
                "severity": "HALT",
                "message": (f"第 {idx} 层拓扑中已冻结节点 {vanished} 消失 — "
                            "螺旋退化为覆盖，已收敛子图必须叠加保留。"),
            })

        incoming = {str(n) for n in converged_nodes}
        self._frozen |= incoming

        risks = sorted(str(r) for r in risk_set)
        layer_hash = hashlib.sha256(json.dumps({
            "index": idx, "state": state, "origin_hash": origin_hash,
            "radius": len(risks), "graph_hash": graph_hash,
        }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]

        self._spent += self.loop_cost
        layer = SpiralLayer(
            index=idx, state=state, origin_hash=origin_hash,
            radius=len(risks), risk_set=risks,
            frozen_nodes=self.frozen_nodes,
            graph_hash=graph_hash, topology=topology,
            layer_hash=layer_hash, cost=self.loop_cost,
            energy_left=self.energy_left,
            distance=(len(risks), 1 if unresolved else 0),
        )
        self.layers.append(layer)
        return layer

    # -------- 层间差分 --------

    def diff(self, i: int, j: int) -> Dict[str, Any]:
        """第 i 层 → 第 j 层的结构差分。

        只报「新增/消失的节点、边、风险」，不下「变好了」这种结论。
        """
        if not (0 <= i < len(self.layers) and 0 <= j < len(self.layers)):
            raise IndexError("layer index out of range")
        a, b = self.layers[i], self.layers[j]

        def nodes_of(layer: SpiralLayer) -> Set[str]:
            return {n["id"] for n in layer.topology.get("nodes", []) if isinstance(n, dict)}

        def edges_of(layer: SpiralLayer) -> Set[str]:
            return {f'{e.get("src")}→{e.get("dst")}:{e.get("relation")}'
                    for e in layer.topology.get("edges", []) if isinstance(e, dict)}

        na, nb = nodes_of(a), nodes_of(b)
        ea, eb = edges_of(a), edges_of(b)
        return {
            "from_layer": i, "to_layer": j,
            "radius_delta": b.radius - a.radius,
            "nodes_added": sorted(nb - na), "nodes_removed": sorted(na - nb),
            "edges_added": sorted(eb - ea), "edges_removed": sorted(ea - eb),
            "risks_added": sorted(set(b.risk_set) - set(a.risk_set)),
            "risks_cleared": sorted(set(a.risk_set) - set(b.risk_set)),
            "origin_drift": a.origin_hash != b.origin_hash,
        }

    def radius_trend(self) -> List[int]:
        return [layer.radius for layer in self.layers]

    def distance_trend(self) -> List[Tuple[int, int]]:
        """到目标稳态 S* 的距离序列：distance = (风险集规模, 是否有未决假设)。

        字典序比较——风险集更小者更近；规模相同时无未决假设者更近。
        整条序列不含任何权重估计，因此可跨进程复算。
        """
        return [layer.distance for layer in self.layers]

    def check_flat(self, layers: int = 3) -> bool:
        """半径连续 layers 层不降 → 平螺旋（在原地扩圈，没有上升）。"""
        r = self.radius_trend()
        if len(r) < layers:
            return False
        return all(r[i] >= r[i - 1] for i in range(len(r) - layers + 1, len(r)))

    def is_static(self, layers: int = 3) -> bool:
        """半径连续 layers 层**完全不变** → 画地为牢：这一圈和上一圈一模一样。

        与 is_plateau 的区别：is_plateau 覆盖「不变或变差」，本方法只认「纹丝不动」。
        必须由本方法先分流，否则 is_plateau 会永远抢先命中：因为 distance 的首分量
        就是半径，一旦半径下降，distance 必然严格下降，所以「距离不严格下降」蕴含
        「半径未下降」——不先分流「原地不动」，FLAT_SPIRAL 就成了死代码。
        """
        r = self.radius_trend()
        if len(r) < layers:
            return False
        return len(set(r[-layers:])) == 1

    def is_plateau(self, layers: int = 3) -> bool:
        """距离连续 layers 层**不严格下降** → 不再逼近 S*。

        宽容口径：拓扑变形常有平台期，故要求连续 layers 层都没出现严格下降才判。
        """
        d = self.distance_trend()
        if len(d) < layers:
            return False
        return all(d[i] >= d[i - 1] for i in range(len(d) - layers + 1, len(d)))

    def limit_reached(self, layers: int = 2) -> bool:
        """距离连续 layers 层均为 (0, 0) → 抵达极限 S∞ = S*。

        注意它要求「保持」而非「碰到」：一次归零可能只是碰巧，连续归零才是极限。
        """
        d = self.distance_trend()
        return len(d) >= layers and all(x == (0, 0) for x in d[-layers:])

    # -------- 续跑（外部驱动无限迭代） --------

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpiralStack":
        """从 to_dict() 的快照恢复栈状态，供外部逐层推进续跑。

        只恢复账目与层快照，不恢复任何可调用对象——所以快照可以落盘、可以跨进程
        传递，但**伪造不出引擎没算过的层**。
        """
        stack = cls(energy_budget=data.get("energy_budget"),
                    loop_cost=float(data.get("loop_cost", 1.0) or 1.0))
        stack._spent = float(data.get("energy_spent", 0.0) or 0.0)
        stack._origin_anchor = data.get("origin_anchor")
        stack._frozen = {str(n) for n in (data.get("frozen_nodes") or [])}
        stack.violations = [dict(v) for v in (data.get("violations") or [])]

        for ld in (data.get("layers") or []):
            raw = ld.get("distance")
            distance = (tuple(raw) if isinstance(raw, (list, tuple)) and len(raw) == 2
                        else (int(ld.get("radius", 0)), 0))
            stack.layers.append(SpiralLayer(
                index=int(ld["index"]), state=str(ld["state"]),
                origin_hash=str(ld.get("origin_hash", "")),
                radius=int(ld.get("radius", 0)),
                risk_set=[str(x) for x in (ld.get("risk_set") or [])],
                frozen_nodes=[str(x) for x in (ld.get("frozen_nodes") or [])],
                graph_hash=str(ld.get("graph_hash", "")),
                topology=ld.get("topology") or {},
                layer_hash=str(ld.get("layer_hash", "")),
                cost=float(ld.get("cost", 0.0) or 0.0),
                energy_left=ld.get("energy_left"),
                distance=(int(distance[0]), int(distance[1])),
            ))
        return stack

    # -------- 汇总 --------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "spiral_version": "1.0.0",
            "layer_count": len(self.layers),
            "energy_budget": self.energy_budget,
            "loop_cost": self.loop_cost,
            "energy_spent": round(self._spent, 6),
            "energy_left": self.energy_left,
            "origin_anchor": self._origin_anchor,
            "frozen_nodes": self.frozen_nodes,
            "radius_trend": self.radius_trend(),
            "distance_trend": [list(d) for d in self.distance_trend()],
            "flat_spiral": self.check_flat(),
            "plateau": self.is_plateau(),
            "limit_reached": self.limit_reached(),
            "violations": self.violations,
            "layers": [layer.to_dict() for layer in self.layers],
        }
# ==================== 第二视角引擎核心 ====================
