"""
拓扑底座 — 无语义因果拓扑 / De-semantic Causal Topology Substrate
=========================================================================

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

# ============================================================================
# 分区② 拓扑底座 — 无语义因果拓扑 / De-semantic Causal Topology
# ============================================================================
# TOPOLOGY — 无语义因果拓扑底座 / De-semantic Causal Topology Substrate
# =====================================================================
#
# 本模块是「第二视角引擎 SPE 1.0」的拓扑层底座，对齐腾讯文档规范
# 《SPL因果论 · 无语义拓扑语法规范》的符号体系与编译期校验机制。
#
# 符号表（无语义：符号不携带语义，语义由算子在运算中生成）
# --------------------------------------------------------
#   □   实体节点        无固有属性，仅代表拓扑位置；删除所有连接边后自动消失
#   →   因果有向边      带约束参数（weight / validity），方向决定两端的相对标签
#   ⦿   全局公理约束    不可修改，全局生效
#   △   上游节点（相对标签）  对下游表现为「可证伪的输入假设」
#   ◇   下游节点（相对标签）  对上游表现为「不可篡改的输出决策」
#   ✅ / ❌  编译状态
#
# 相对标签定理
# ------------
#   1. 标签相对：同一节点在 A→B 链上是 ◇，在 B→C 链上就是 △，无固定语义。
#   2. 标签无副作用：推演可完全剥离标签进行纯结构运算，不影响收敛结果。
#   3. 标签不参与判定：本模块只提供标签映射函数，任何判定都不读标签。
#
# 三类并行约束校验（编译期自动执行，无串行等待）
# ----------------------------------------------
#   一致性校验 consistency   节点全局身份唯一、无自相矛盾的边定义      致命，直接终止
#   约束满足校验 constraint  所有边参数符合全局公理 ⦿，无越界            致命，直接终止
#   拓扑闭合校验 closure     无悬空节点/边、无因果悖论（含自环）        警告，可强制继续但结果无效
#
# 确定性 · 零随机 · 零 LLM 调用 · 零外部依赖
# ----------------------------------------------------------------------------

TOPOLOGY_VERSION = "1.0.0"
# 拓扑层**文法**版本：与 TOPOLOGY_VERSION（底座结构版本）分开记。
# 文法增补（如 2026.3 的链内时序 t、元因果账本字段）没有改动底座结构，
# 但必须可追溯到「这条链是在哪一版语法下产生的」，否则跨代际比对无从谈起。
TOPOLOGY_GRAMMAR_VERSION = "2026.3"

# ── 无语义符号表 ──
SYM_NODE = "□"
SYM_EDGE = "→"
SYM_CONSTRAINT = "⦿"
SYM_UPSTREAM = "△"
SYM_DOWNSTREAM = "◇"
SYM_PASS = "✅"
SYM_FAIL = "❌"

# 相对标签常量（唯一来源，禁止在别处硬编码 △/◇）
REL_INPUT = SYM_UPSTREAM      # 对下游表现为可证伪的输入假设
REL_OUTPUT = SYM_DOWNSTREAM   # 对上游表现为不可篡改的输出决策

# ── 校验分级 ──
SEVERITY_HALT = "HALT"        # 致命：直接终止推演
SEVERITY_WARN = "WARN"        # 警告：可强制继续，但结果无效

CHECK_CONSISTENCY = "consistency"
CHECK_CONSTRAINT = "constraint"
CHECK_CLOSURE = "closure"
# 第四个并行进程：链内时序（公理 5「绝对前提：时间」）。
# 之所以单列而不并入 closure：闭合问「图自洽吗」，时序问「这张图还是不是一条链」。
# 两者可以同时通过、也可以各自失败，语义不可合并。
CHECK_TIME_ORDER = "time_order"

# ── 诊断码 ──
T101_ROLE_CONFLICT = "T101"      # 同一 (src,dst) 同时存在 requires 与 depends_on
T102_CONTRADICTORY_EDGE = "T102" # 同一 (src,dst,relation) 重复且参数不一致
T201_PARAM_OUT_OF_RANGE = "T201"
T202_REQUIRED_PARAM_MISSING = "T202"
T203_DEGREE_EXCEEDED = "T203"
T301_DANGLING_EDGE = "T301"
T302_DANGLING_NODE = "T302"
T303_CAUSAL_PARADOX = "T303"     # 有向环 / 自环 = 因果悖论
# —— 公理 5 专用诊断码（语法扩展 2026.3）——
T305_FORK_VIOLATION = "T305"     # 同一对节点被声明多条边 = 未来在节点上分叉
T307_TIME_ORDER_INVERTED = "T307"   # 声明时序与链内派生序冲突 = 序被倒置
T308_TIME_UNASSIGNABLE = "T308"     # 无法赋予单调时序（有环）= 链不成立

# 允许的因果边关系（与 decision.ebnf 的 verb 保持一致）
ALLOWED_RELATIONS = ("causal", "requires", "depends_on")


# ==================== 数据结构 ====================

@dataclass
class TopoNode:
    """□ 实体节点。

    无语义：不承载「决策 / 假设 / 实体」等任何语义属性。
    id 是它在拓扑中的唯一定位；其余字段只是外部映射的挂载点。
    """

    id: str
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "note": self.note}


@dataclass
class TopoEdge:
    """→ 因果有向边。

    relation    causal | requires | depends_on（与 .spd 的 verb 对齐）
    weight      边权；是否越界由 ⦿ 约束判定，本类不自行设限
    validity    有效期描述（字符串，不做时间运算）
    falsifiable 该边作为输入时是否可证伪（不可证伪 = 失效无预警）
    delta_d     该边失效时下游的结构性变更 ΔD（描述，不是建议）
    t           链内时序（公理 5「时间即链之序」）。

        规范公理 5 把时间定为**构成条件**而非可拆分支：「前置因先于后继果，
        因果结构不可自我循环……剥离、透视、对冲、锚定、重构五大算子的全部操作，
        都在该前提下进行」。所以时序不是附加字段，而是「链」这个概念成立的前提。

        None  = 未声明，由 TopologyGraph.assign_time_order() 按最长路径确定性派生
        非 None = 显式声明的链内序，必须满足 t(前置) < t(后继)，否则 T307。

        为什么 t 可选而非必填：存量 .spd / 投影拓扑不声明时序时，其派生序仍可
        被完整算出（派生序是纯结构的函数），因此**默认为 None 不改变任何既有
        拓扑指纹**；只有真正声明了时序的拓扑，其结构才因此不同。
    """

    src: str
    dst: str
    relation: str = "causal"
    weight: Optional[float] = None
    validity: Optional[str] = None
    falsifiable: bool = True
    delta_d: Optional[str] = None
    note: str = ""
    t: Optional[int] = None

    @property
    def key(self) -> Tuple[str, str, str]:
        return (self.src, self.dst, self.relation)

    @property
    def shape(self) -> Tuple[str, str]:
        return (self.src, self.dst)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "src": self.src, "dst": self.dst, "relation": self.relation,
            "weight": self.weight, "validity": self.validity,
            "falsifiable": self.falsifiable, "delta_d": self.delta_d,
            "note": self.note, "t": self.t,
        }


@dataclass
class Constraint:
    """⦿ 全局公理约束。不可修改，全局生效。

    kind = weight_range        params {"lo": 0.0, "hi": 1.0}
    kind = max_out_degree      params {"max": 4}
    kind = required_param      params {"param": "weight"}
    """

    name: str
    kind: str
    params: Dict[str, Any] = field(default_factory=dict)
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "kind": self.kind,
                "params": self.params, "note": self.note}


@dataclass
class ValidationIssue:
    code: str
    check: str
    severity: str
    message: str
    where: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"code": self.code, "check": self.check, "severity": self.severity,
                "message": self.message, "where": self.where}


def default_constraints() -> Dict[str, Constraint]:
    """规范默认的 ⦿ 全局约束集。

    注意：拓扑闭合（含无环）不放在这里——规范把「无因果悖论」列为
    闭合校验（警告级），与「参数不越界」的致命级约束是两个进程。
    """
    return {
        "weight_range": Constraint(
            name="weight_range", kind="weight_range",
            params={"lo": 0.0, "hi": 1.0},
            note="边权必须落在闭区间内，否则视为越界",
        ),
    }


# ==================== 拓扑图 ====================

@dataclass
class TopologyGraph:
    """G = (□, →, ⦿)。节点无固有属性，关系优先于实体。"""

    nodes: Dict[str, TopoNode] = field(default_factory=dict)
    edges: List[TopoEdge] = field(default_factory=list)
    constraints: Dict[str, Constraint] = field(default_factory=dict)
    layer: int = 0
    provenance: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.constraints:
            self.constraints = default_constraints()

    # -------- 变更 --------

    def add_node(self, node_id: str, note: str = "") -> str:
        if node_id not in self.nodes:
            self.nodes[node_id] = TopoNode(id=node_id, note=note)
        return node_id

    def add_edge(self, edge: TopoEdge) -> TopoEdge:
        # 关系优先于实体：边会隐式创建它连接的两个节点
        self.add_node(edge.src)
        self.add_node(edge.dst)
        self.edges.append(edge)
        return edge

    def trace(self, operator: str, action: str, detail: Dict[str, Any]) -> None:
        """结构化元审计：每一次算子作用于拓扑都留痕。

        留痕只记「谁、对拓扑做了什么、拓扑长什么样」——
        不记语义判断，因为本层不产生语义。
        """
        self.provenance.append({
            "layer": self.layer,
            "operator": operator,
            "action": action,
            "detail": detail,
        })

    def clone(self, layer: Optional[int] = None) -> "TopologyGraph":
        """深拷贝一层。螺旋叠加时为上层留一份不可变快照。"""
        return TopologyGraph(
            nodes={k: TopoNode(v.id, v.note) for k, v in self.nodes.items()},
            edges=[TopoEdge(**e.to_dict()) for e in self.edges],
            constraints={k: Constraint(c.name, c.kind, dict(c.params), c.note)
                         for k, c in self.constraints.items()},
            layer=self.layer if layer is None else layer,
            provenance=[dict(p) for p in self.provenance],
        )

    def freeze(self, node_ids: Sequence[str]) -> List[str]:
        """冻结已收敛子图：被冻结的节点在后续螺旋层不再重开。"""
        frozen = sorted({n for n in node_ids if n in self.nodes})
        self.trace("↻SPR", "FREEZE", {"frozen_nodes": frozen})
        return frozen

    # -------- 相对标签（仅供外部映射，不参与判定） --------

    def relative_label(self, edge: TopoEdge, endpoint: str) -> str:
        """相对标签定理：同一条边，上游端是 △，下游端是 ◇。

        标签无副作用——推演过程可完全剥离标签，不影响任何判定结果。
        """
        if endpoint == edge.src:
            return REL_INPUT
        if endpoint == edge.dst:
            return REL_OUTPUT
        return ""

    def labels(self) -> Dict[str, Dict[str, List[str]]]:
        """全图相对标签映射。同一节点可同时是 △ 与 ◇。"""
        out: Dict[str, Dict[str, List[str]]] = {
            n: {"upstream": [], "downstream": []} for n in self.nodes
        }
        for e in self.edges:
            if e.src in out:
                out[e.src]["upstream"].append(e.dst)
            if e.dst in out:
                out[e.dst]["downstream"].append(e.src)
        return out

    def adjacency(self) -> Dict[str, List[str]]:
        """出邻接表。节点全部列出（含无出边的节点），顺序确定。"""
        adj: Dict[str, List[str]] = {n: [] for n in sorted(self.nodes)}
        for e in self.edges:
            if e.src in adj:
                adj[e.src].append(e.dst)
        return adj

    def find_cycles(self) -> List[List[str]]:
        """定位所有有向环（含自环）= 因果悖论 A→B→C→¬A。

        迭代式 DFS 三色标记，确定性遍历顺序（节点按 id 排序），
        环路径按发现顺序返回；不追求「所有环」的完备枚举，
        只保证「有环必报」且路径可复核。
        """
        WHITE, GREY, BLACK = 0, 1, 2
        color: Dict[str, int] = {n: WHITE for n in sorted(self.nodes)}
        adj: Dict[str, List[str]] = {n: [] for n in sorted(self.nodes)}
        for e in self.edges:
            if e.src in adj:
                adj[e.src].append(e.dst)

        cycles: List[List[str]] = []
        seen_signature: Set[Tuple[str, ...]] = set()

        for root in sorted(self.nodes):
            if color[root] != WHITE:
                continue
            stack: List[Tuple[str, int]] = [(root, 0)]
            path: List[str] = []
            while stack:
                node, idx = stack[-1]
                if idx == 0:
                    color[node] = GREY
                    path.append(node)
                if idx < len(adj.get(node, [])):
                    stack[-1] = (node, idx + 1)
                    nxt = adj[node][idx]
                    if nxt not in color:
                        continue
                    if color[nxt] == GREY:
                        # 找到回边：截取环路径
                        try:
                            start = path.index(nxt)
                        except ValueError:
                            start = 0
                        cyc = path[start:] + [nxt]
                        sig = tuple(sorted(cyc))
                        if sig not in seen_signature:
                            seen_signature.add(sig)
                            cycles.append(cyc)
                    elif color[nxt] == WHITE:
                        stack.append((nxt, 0))
                else:
                    color[node] = BLACK
                    path.pop()
                    stack.pop()
        return cycles

    # -------- 公理 5：链内时序 --------

    def assign_time_order(self) -> Dict[str, Any]:
        """赋予全图链内时序 t（公理 5）。

        规范原文：「时间即链之序……前置因先于后继果，因果结构不可自我循环。
        没有这一前提，『链』这个概念本身无法成立——因果链的『链』，
        其含义就是可排序。」因此本方法是「这张图还能不能叫一条链」的判定器。

        规则（全部确定性，无随机、无估算）
        ----------------------------------
        1. 时序 t 按**最长路径**派生：入度 0 的节点为 t=0，其余 t = max(前置 t) + 1。
           用最长路径而非最短路径，是因为「前置因先于后继果」要求 t 必须晚于
           **全部**前置因，否则序就只是某一条路径的序，而不是链的序。
        2. 若存在有向环，则不存在单调赋值 —— 报 unassignable，链不成立（T308）。
           这也解释了规范为什么说因果承接「不是链的自环」：自环会让序无处安放。
        3. 观测位置：规范原文「一个观测者本身就是一条类时曲线，因此只能位于一条
           链上」。故此处同时给出 observer_anchor —— 本次审计所站的那条链的起点。
           它是 □0（第一原点）在拓扑中的镜像；无原点节点时退回唯一的起点，
           多起点且无原点时为空（此时「站在哪条链上」这件事没有被声明）。
        4. 平行 ≠ 分支：平行是「多条各自有序的链」，表现为多个 roots，**合法**；
           分支是「未来在某个节点真的分叉」，表现为同一对节点被声明多条边（T305），
           规范明确「SPL 是强决定论，只承认前者」。
        """
        nodes = sorted(self.nodes)
        indeg: Dict[str, int] = {n: 0 for n in nodes}
        adj: Dict[str, List[str]] = {n: [] for n in nodes}
        for e in self.edges:
            if e.src in adj:
                adj[e.src].append(e.dst)
            if e.dst in indeg:
                indeg[e.dst] += 1

        roots = [n for n in nodes if indeg[n] == 0]

        # --- 最长路径序（Kahn，队列按 id 排序保证跨进程一致）---
        t: Dict[str, int] = {n: 0 for n in roots}
        remaining = dict(indeg)
        queue: List[str] = sorted(roots)
        visited: Set[str] = set()
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            for nxt in sorted(adj.get(node, [])):
                t[nxt] = max(t.get(nxt, 0), t.get(node, 0) + 1)
                remaining[nxt] -= 1
                if remaining[nxt] <= 0:
                    queue.append(nxt)
                    queue.sort()
        unassignable = [n for n in nodes if n not in visited]

        # --- 分叉：同一对节点被声明多条边（平行 ≠ 分支）---
        shapes: Dict[Tuple[str, str], int] = {}
        for e in self.edges:
            shapes[e.shape] = shapes.get(e.shape, 0) + 1
        forks = [{"src": s[0], "dst": s[1], "count": c}
                 for s, c in sorted(shapes.items()) if c > 1]

        # --- 声明时序与派生序冲突：序被倒置 ---
        inverted: List[Dict[str, Any]] = []
        for e in self.edges:
            if e.t is None:
                continue
            src_t = t.get(e.src, 0)
            dst_t = t.get(e.dst, 0)
            if e.t < src_t or e.t >= dst_t:
                inverted.append({
                    "edge": f"{e.src}→{e.dst}",
                    "declared": e.t,
                    "expected_range": [src_t, dst_t - 1],
                })

        # --- 观测位置：这条链的起点 ---
        if SYM_NODE + "0" in self.nodes:
            anchor = SYM_NODE + "0"
        elif len(roots) == 1:
            anchor = roots[0]
        else:
            anchor = ""

        seen: Set[str] = set()
        if anchor:
            stack = [anchor]
            while stack:
                cur = stack.pop()
                if cur in seen:
                    continue
                seen.add(cur)
                stack.extend(adj.get(cur, []))

        return {
            "assignable": not unassignable,
            "node_order": dict(sorted(t.items())),
            "roots": roots,
            "parallel_chains": len(roots),
            "forks": forks,
            "inverted": inverted,
            "unassignable": unassignable,
            "observer_anchor": anchor,
            "observer_chain_size": len(seen),
            "max_depth": max(t.values()) if t else 0,
        }

    # -------- 序列化 --------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topology_version": TOPOLOGY_VERSION,
            "layer": self.layer,
            "symbols": {"node": SYM_NODE, "edge": SYM_EDGE, "constraint": SYM_CONSTRAINT},
            "nodes": [self.nodes[k].to_dict() for k in sorted(self.nodes)],
            "edges": [e.to_dict() for e in self.edges],
            "constraints": [self.constraints[k].to_dict() for k in sorted(self.constraints)],
            "provenance": self.provenance,
            "time_order": self.assign_time_order(),
        }

    def graph_hash(self) -> str:
        """拓扑指纹：仅由纯结构决定，与标签、与 provenance 无关。

        含声明时序 t（公理 5 把时间定为构成条件，故它属于结构）；
        但 t 默认为 None，因此**未声明时序的拓扑指纹与本字段引入前完全一致**——
        既能表达时序，又不会让存量拓扑凭空换指纹。
        """
        blob = json.dumps({
            "nodes": sorted(self.nodes),
            "edges": sorted(
                [e.src, e.dst, e.relation, e.weight, e.validity, e.falsifiable, e.t]
                for e in self.edges
            ),
            "constraints": sorted(
                [k, c.kind, json.dumps(c.params, sort_keys=True)]
                for k, c in self.constraints.items()
            ),
        }, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ==================== 三类并行校验 ====================

class TopologyValidator:
    """编译期并行校验：一致性 / 约束满足 / 拓扑闭合。

    三个进程互不串行等待，任何一步不通过即返回编译状态；
    致命错误终止推演，闭合警告允许强制继续但结果标记为无效。
    """

    # -------- 进程一：一致性（致命） --------

    @staticmethod
    def check_consistency(g: TopologyGraph) -> Dict[str, Any]:
        issues: List[ValidationIssue] = []

        # 节点全局身份唯一
        lowered: Dict[str, List[str]] = {}
        for nid in g.nodes:
            lowered.setdefault(nid.lower(), []).append(nid)
        for key, members in sorted(lowered.items()):
            if len(members) > 1:
                issues.append(ValidationIssue(
                    T101_ROLE_CONFLICT, CHECK_CONSISTENCY, SEVERITY_HALT,
                    f"节点身份不唯一：{members} 仅大小写不同，视为同一身份的冲突定义",
                    where=f"nodes={members}",
                ))

        # 自相矛盾的边定义
        shapes: Dict[Tuple[str, str], Set[str]] = {}
        by_key: Dict[Tuple[str, str, str], List[TopoEdge]] = {}
        for e in g.edges:
            shapes.setdefault(e.shape, set()).add(e.relation)
            by_key.setdefault(e.key, []).append(e)

        for shape, relations in sorted(shapes.items()):
            if len(relations) > 1:
                issues.append(ValidationIssue(
                    T101_ROLE_CONFLICT, CHECK_CONSISTENCY, SEVERITY_HALT,
                    f"边 {shape[0]}→{shape[1]} 同时声明了互相矛盾的关系 {sorted(relations)}",
                    where=f"edge={shape[0]}→{shape[1]}",
                ))

        for key, group in sorted(by_key.items()):
            if len(group) < 2:
                continue
            sigs = {(e.weight, e.validity, e.falsifiable) for e in group}
            if len(sigs) > 1:
                issues.append(ValidationIssue(
                    T102_CONTRADICTORY_EDGE, CHECK_CONSISTENCY, SEVERITY_HALT,
                    f"边 {key[0]}→{key[1]}({key[2]}) 重复定义且参数不一致 {sorted(sigs, key=str)}",
                    where=f"edge={key[0]}→{key[1]}({key[2]})",
                ))

        halts = [i for i in issues if i.severity == SEVERITY_HALT]
        return {
            "check": CHECK_CONSISTENCY,
            "status": SYM_FAIL if halts else SYM_PASS,
            "fatal": bool(halts),
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 进程二：约束满足（致命） --------

    @staticmethod
    def check_constraints(g: TopologyGraph) -> Dict[str, Any]:
        issues: List[ValidationIssue] = []
        by_kind: Dict[str, List[Constraint]] = {}
        for c in g.constraints.values():
            by_kind.setdefault(c.kind, []).append(c)

        # ⦿ weight_range：所有显式声明的边权必须落在区间内
        ranges = by_kind.get("weight_range", [])
        if ranges:
            lo = min(float(c.params.get("lo", 0.0)) for c in ranges)
            hi = max(float(c.params.get("hi", 1.0)) for c in ranges)
            for e in g.edges:
                if e.weight is None:
                    continue
                if not (lo <= float(e.weight) <= hi):
                    issues.append(ValidationIssue(
                        T201_PARAM_OUT_OF_RANGE, CHECK_CONSTRAINT, SEVERITY_HALT,
                        f"边 {e.src}→{e.dst} 的 weight={e.weight} 越界 [{lo}, {hi}]",
                        where=f"edge={e.src}→{e.dst}",
                    ))

        # ⦿ required_param：声明为必填的参数不得缺位
        for c in by_kind.get("required_param", []):
            param = c.params.get("param")
            for e in g.edges:
                if getattr(e, str(param), None) is None:
                    issues.append(ValidationIssue(
                        T202_REQUIRED_PARAM_MISSING, CHECK_CONSTRAINT, SEVERITY_HALT,
                        f"边 {e.src}→{e.dst} 缺少必需参数 {param}",
                        where=f"edge={e.src}→{e.dst}",
                    ))

        # ⦿ max_out_degree：出度上限
        for c in by_kind.get("max_out_degree", []):
            cap = int(c.params.get("max", 0))
            out_deg: Dict[str, int] = {}
            for e in g.edges:
                out_deg[e.src] = out_deg.get(e.src, 0) + 1
            for nid, deg in sorted(out_deg.items()):
                if deg > cap:
                    issues.append(ValidationIssue(
                        T203_DEGREE_EXCEEDED, CHECK_CONSTRAINT, SEVERITY_HALT,
                        f"节点 {nid} 出度 {deg} 超过 ⦿ 上限 {cap}",
                        where=f"node={nid}",
                    ))

        halts = [i for i in issues if i.severity == SEVERITY_HALT]
        return {
            "check": CHECK_CONSTRAINT,
            "status": SYM_FAIL if halts else SYM_PASS,
            "fatal": bool(halts),
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 进程三：拓扑闭合（警告，结果无效） --------

    @staticmethod
    def check_closure(g: TopologyGraph) -> Dict[str, Any]:
        issues: List[ValidationIssue] = []

        # 悬空边：端点不在节点集内
        for e in g.edges:
            dangling = [p for p in (e.src, e.dst) if p not in g.nodes]
            if dangling:
                issues.append(ValidationIssue(
                    T301_DANGLING_EDGE, CHECK_CLOSURE, SEVERITY_WARN,
                    f"悬空边 {e.src}→{e.dst}：端点 {dangling} 未声明为节点",
                    where=f"edge={e.src}→{e.dst}",
                ))

        # 悬空节点：无任何入边或出边
        touched: Set[str] = set()
        for e in g.edges:
            touched.add(e.src)
            touched.add(e.dst)
        for nid in sorted(g.nodes):
            if nid not in touched:
                issues.append(ValidationIssue(
                    T302_DANGLING_NODE, CHECK_CLOSURE, SEVERITY_WARN,
                    f"悬空节点 {SYM_NODE}{nid}：无任何连接边，按「关系优先于实体」应自动消失",
                    where=f"node={nid}",
                ))

        # 因果悖论：有向环（自环 A→A 亦属其中）
        for cyc in g.find_cycles():
            path = " → ".join(cyc)
            issues.append(ValidationIssue(
                T303_CAUSAL_PARADOX, CHECK_CLOSURE, SEVERITY_WARN,
                f"因果悖论：{path} 自我循环，链不可排序（绝对前提：时间序）",
                where=f"cycle={path}",
            ))

        fatal = any(i.severity == SEVERITY_HALT for i in issues)
        return {
            "check": CHECK_CLOSURE,
            "status": SYM_FAIL if issues else SYM_PASS,
            "fatal": fatal,          # 闭合问题恒为警告级，fatal 恒 False
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 进程四：链内时序（警告，结果无效） --------

    @staticmethod
    def check_time_order(g: TopologyGraph) -> Dict[str, Any]:
        """公理 5 校验：这张图还成不成立为「一条链」。

        与闭合校验的分工：
            闭合  问「图自洽吗」   —— 悬空、有环
            时序  问「序排得出来吗、排出来被倒置了吗、未来分叉了吗」
        两者可各自独立失败，因此不可合并成一个进程。

        级别沿用规范的分级（警告，可强制继续但结果无效）——
        本层不自行发明致命级别，也不把规范里的警告擅自升级。
        """
        order = g.assign_time_order()
        issues: List[ValidationIssue] = []

        # T305 分叉：同一对节点被声明多条边
        for fork in order["forks"]:
            issues.append(ValidationIssue(
                T305_FORK_VIOLATION, CHECK_TIME_ORDER, SEVERITY_WARN,
                f"分叉违规：{fork['src']}→{fork['dst']} 被声明 {fork['count']} 条边 — "
                f"同一对因果不容许两个未来（平行 ≠ 分支）",
                where=f"edge={fork['src']}→{fork['dst']}",
            ))

        # T307 序被倒置：声明时序与链内派生序冲突
        for item in order["inverted"]:
            issues.append(ValidationIssue(
                T307_TIME_ORDER_INVERTED, CHECK_TIME_ORDER, SEVERITY_WARN,
                f"时序倒置：{item['edge']} 声明 t={item['declared']}，"
                f"但链内序要求落在 {item['expected_range']}（前置因必须先于后继果）",
                where=f"edge={item['edge']}",
            ))

        # T308 序排不出来：有向环使单调赋值不存在
        if order["unassignable"]:
            issues.append(ValidationIssue(
                T308_TIME_UNASSIGNABLE, CHECK_TIME_ORDER, SEVERITY_WARN,
                f"无法赋予单调时序：节点 {order['unassignable']} 落在有向环上 — "
                f"时间是不可剥离的构成条件，无时序则「链」不成立",
                where=f"nodes={order['unassignable']}",
            ))

        return {
            "check": CHECK_TIME_ORDER,
            "status": SYM_FAIL if issues else SYM_PASS,
            "fatal": False,          # 时序问题恒为警告级，与 closure 同级
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 并行调度 --------

    @classmethod
    def run_all(cls, g: TopologyGraph) -> Dict[str, Any]:
        """四个进程并行执行，任一致命即终止推演。

        result_valid 与 pass 的差别是本模块的关键语义：
          pass         四个进程全 ✅
          fatal        存在致命错误 —— 推演终止，无结果
          result_valid 无致命错误，但可能有闭合/时序警告 —— 可强制继续，**结果无效**

        时序进程是「语法扩展 2026.3」新增（公理 5 的落地）：它无致命级，
        因此不会改变「哪些输入会被阻断」这一既有事实，只会改变「结果是否有效」。
        """
        consistency = cls.check_consistency(g)
        constraint = cls.check_constraints(g)
        closure = cls.check_closure(g)
        time_order = cls.check_time_order(g)

        parts = (consistency, constraint, closure, time_order)
        fatal = any(p["fatal"] for p in parts)
        ok = all(p["status"] == SYM_PASS for p in parts)

        return {
            "consistency": consistency,
            "constraint": constraint,
            "closure": closure,
            "time_order": time_order,
            "compile_status": SYM_FAIL if fatal else SYM_PASS,
            "pass": ok,
            "fatal": fatal,
            "result_valid": (not fatal)
                            and closure["status"] == SYM_PASS
                            and time_order["status"] == SYM_PASS,
            "halt_count": sum(
                1 for part in parts
                for i in part["issues"] if i["severity"] == SEVERITY_HALT
            ),
            "warn_count": sum(
                1 for part in parts
                for i in part["issues"] if i["severity"] == SEVERITY_WARN
            ),
        }


# ==================== 上层语言投影（.spd ⇄ 拓扑） ====================

def build_from_decision_context(ctx: Dict[str, Any],
                                origin: Optional[str] = None) -> TopologyGraph:
    """把上层决策上下文投影成无语义拓扑 G0。

    投影规则（刻意保持机械、不含任何语义推断）：
        □0      原点事件        （第一原点，若声明）
        □D      决策节点        ← decision / p / premise / action
        □Q      结果节点        ← outcome / q / result / consequence
        □Ai     每条假设        ← assumptions / premises / hypotheses
        □ΔDj    每条分支响应    ← branches[].delta_d
        →       依赖          Ai requires Aj   ← dependencies {"Ai": ["Aj"]}
        →       输入边         Ai → □D
        →       主干边         □0 → □D → □Q
        →       分支边         Ai → □ΔDj（边携带 delta_d：该边失效时的结构性变更）

    只做连接，不做解释——这正是 ⊗ 去语义化的力学后果。
    """
    g = TopologyGraph(layer=0)

    def _first_str(*keys: str) -> str:
        for k in keys:
            v = ctx.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return ""

    origin_text = origin or _first_str("origin", "origin_event")
    decision = _first_str("decision", "p", "premise", "action")
    outcome = _first_str("outcome", "q", "result", "consequence")

    if origin_text:
        g.add_node("□0", note="原点事件")
        g.trace("⊞TPG", "ADD_ORIGIN_NODE", {"node": "□0"})
    if decision:
        g.add_node("□D", note="决策")
    if outcome:
        g.add_node("□Q", note="结果")

    if origin_text and decision:
        g.add_edge(TopoEdge("□0", "□D", relation="causal", note="原点→决策"))
    if decision and outcome:
        g.add_edge(TopoEdge("□D", "□Q", relation="causal", note="决策→结果"))

    assumptions: List[str] = []
    for key in ("assumptions", "premises", "hypotheses", "core_assumptions"):
        val = ctx.get(key)
        if isinstance(val, list):
            assumptions = [str(a) for a in val if a]
            break
        if isinstance(val, str) and val.strip():
            assumptions = [val]
            break

    aid_of: Dict[str, str] = {}
    for i, a in enumerate(assumptions):
        aid = f"□A{i + 1}"
        aid_of[a] = aid
        g.add_node(aid, note=a[:60])
        if decision:
            g.add_edge(TopoEdge(aid, "□D", relation="requires",
                                falsifiable=True, note="输入假设边"))

    branches = ctx.get("branches") or ctx.get("branch_responses") or ctx.get("failure_paths")
    if isinstance(branches, list):
        for j, b in enumerate(branches):
            if not isinstance(b, dict):
                continue
            target = b.get("assumption", b.get("premise", b.get("target", "")))
            delta_d = b.get("delta_d", b.get("deltaD", b.get("response", "")))
            did = f"□ΔD{j + 1}"
            g.add_node(did, note=str(delta_d)[:60])
            src = aid_of.get(str(target), f"□A{j + 1}")
            g.add_edge(TopoEdge(src, did, relation="causal",
                                delta_d=str(delta_d) if delta_d else None,
                                note="分支响应边"))

    deps = ctx.get("dependencies") or ctx.get("dependency_graph") or ctx.get("deps")
    if isinstance(deps, dict):
        for a, targets in deps.items():
            if not isinstance(targets, list):
                continue
            for t in targets:
                g.add_edge(TopoEdge(f"□{t}", f"□{a}", relation="requires",
                                    note="依赖边"))

    g.trace("⊞TPG", "BUILD_G0", {
        "nodes": len(g.nodes), "edges": len(g.edges),
        "origin": bool(origin_text), "decision": bool(decision), "outcome": bool(outcome),
    })
    return g
