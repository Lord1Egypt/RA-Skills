"""Projection：神经图纯投影（spec §7.3, §10）。

v3 核心纠偏：
- 神经图是 Memory IR 的可视化投影，不是事实数据库
- get_neuron_graph() 只读取已有投影
- 未构建时返回 {empty: true, reason: "not_built"}
- build_projection() 需用户确认
- 删除 projection/neuron.json 后可从 IR + DecisionLog 完整重建
- 不做自动晋升/凋亡/基于 use_count 的强结论（spec §7.3）

与 v2.1 light_graph.py 的区别：
- light_graph.py 是事实源，自动挂载+晋升+凋亡
- Projection 只读 IR + decisions，生成投影 JSON
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .memory_ir import MemoryIR
from .schema_v3 import MemoryStatus, stable_hash, _now_iso


# ---------------------------------------------------------------------------
# 投影数据结构（供 Cytoscape.js 消费）
# ---------------------------------------------------------------------------


@dataclass
class ProjectionNode:
    """神经图节点。"""
    id: str
    parent_id: str
    label: str
    node_kind: str  # root/topic/claim_anchor
    status: str = "confirmed"  # 永远 confirmed，不再 tentative（无自动晋升）
    memory_id: str = ""
    kind: str = ""  # MemoryKind
    provenance_count: int = 0
    bg: str = "#5b8def"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "parent_id": self.parent_id, "label": self.label,
            "node_kind": self.node_kind, "status": self.status,
            "memory_id": self.memory_id, "kind": self.kind,
            "provenance_count": self.provenance_count, "bg": self.bg,
        }


@dataclass
class ProjectionEdge:
    """神经图边。"""
    id: str
    source: str
    target: str
    edge_type: str = "derived_from"  # derived_from/duplicate/conflict

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "source": self.source, "target": self.target,
            "edge_type": self.edge_type,
        }


@dataclass
class NeuronProjection:
    """神经图投影。"""
    snapshot_id: str = ""
    built_at: str = ""
    nodes: list[ProjectionNode] = field(default_factory=list)
    edges: list[ProjectionEdge] = field(default_factory=list)
    # v3.1 §6.3：确定性内容哈希（不含 built_at），用于验证重建一致性
    content_hash: str = ""
    # v3.1 §6.3 七项状态 meta：Agent 实例 / Profile / 规范版本 / Release / 接管状态 / 覆盖状态 / 漂移
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        # v3.1 §6.3：统一 v3 图契约，并附 stats 给前端展示
        node_count = len(self.nodes)
        edge_count = len(self.edges)
        # 按 node_kind 统计
        kind_counts: dict[str, int] = {}
        provenance_total = 0
        for n in self.nodes:
            kind_counts[n.node_kind] = kind_counts.get(n.node_kind, 0) + 1
            provenance_total += n.provenance_count
        return {
            "snapshot_id": self.snapshot_id, "built_at": self.built_at,
            "content_hash": self.content_hash,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "stats": {
                "node_count": node_count,
                "edge_count": edge_count,
                "root_count": kind_counts.get("root", 0),
                "topic_count": kind_counts.get("topic", 0),
                "claim_anchor_count": kind_counts.get("claim_anchor", 0),
                "provenance_total": provenance_total,
            },
            "meta": dict(self.meta),
        }


# ---------------------------------------------------------------------------
# 颜色映射
# ---------------------------------------------------------------------------

KIND_COLORS = {
    "preference": "#e6a23c",   # 橙
    "fact": "#409eff",         # 蓝
    "project": "#67c23a",      # 绿
    "episode": "#f56c6c",      # 红
    "procedure": "#909399",    # 灰
}


# ---------------------------------------------------------------------------
# ProjectionBuilder：从 IR + decisions 重建投影
# ---------------------------------------------------------------------------


class ProjectionBuilder:
    """从 Memory IR + DecisionLog 重建神经图投影。"""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.proj_path = self.workspace / ".memoryguard" / "projections" / "neuron.json"

    def build(self, ir: MemoryIR, meta: dict[str, Any] | None = None) -> NeuronProjection:
        """从 IR 构建投影。不自动晋升/凋亡。

        v3.1 §6.3：meta 携带 7 项状态信息（Agent 实例 / Profile / 规范版本 /
        Release / 接管状态 / 覆盖状态 / 漂移），由调用方聚合后传入。
        """
        nodes: list[ProjectionNode] = []
        edges: list[ProjectionEdge] = []

        # root
        root_id = "main"
        nodes.append(ProjectionNode(
            id=root_id, parent_id="", label="Memory Root", node_kind="root",
        ))

        # 按 kind 分组为 topic 节点
        kind_groups: dict[str, list[str]] = {}
        for rec in ir.records:
            if rec.status == MemoryStatus.REJECTED:
                continue  # 被拒绝的不显示
            kind_groups.setdefault(rec.kind.value, []).append(rec.memory_id)

        # topic 节点
        for kind, record_ids in kind_groups.items():
            topic_id = "topic-" + kind
            nodes.append(ProjectionNode(
                id=topic_id, parent_id=root_id, label=kind, node_kind="topic",
                bg=KIND_COLORS.get(kind, "#5b8def"),
            ))
            # claim_anchor 节点
            for rid in record_ids:
                rec = next((r for r in ir.records if r.memory_id == rid), None)
                if not rec:
                    continue
                node_id = "claim-" + rid[:12]
                label = rec.title[:40] if rec.title else rec.memory_id[:8]
                nodes.append(ProjectionNode(
                    id=node_id, parent_id=topic_id, label=label,
                    node_kind="claim_anchor", memory_id=rid,
                    kind=rec.kind.value, provenance_count=len(rec.provenance),
                    bg=KIND_COLORS.get(rec.kind.value, "#5b8def"),
                ))
                # derived_from 边
                edges.append(ProjectionEdge(
                    id="e-" + stable_hash(node_id, topic_id),
                    source=topic_id, target=node_id,
                    edge_type="derived_from",
                ))

        # 重复组边
        for grp in ir.duplicate_groups:
            if len(grp.member_ids) < 2:
                continue
            for i in range(1, len(grp.member_ids)):
                src = "claim-" + grp.member_ids[0][:12]
                tgt = "claim-" + grp.member_ids[i][:12]
                edges.append(ProjectionEdge(
                    id="e-dup-" + stable_hash(src, tgt),
                    source=src, target=tgt, edge_type="duplicate",
                ))

        proj = NeuronProjection(
            snapshot_id=ir.snapshot_id, built_at=_now_iso(),
            nodes=nodes, edges=edges,
            meta=dict(meta) if meta else {},
        )
        # v3.1 §6.3：确定性 content_hash（不含 built_at 和 meta，仅基于图结构）
        proj.content_hash = self._compute_content_hash(proj)
        return proj

    def _compute_content_hash(self, proj: NeuronProjection) -> str:
        """计算投影内容哈希（不含 built_at，相同输入产生相同 hash）。"""
        content = json.dumps({
            "snapshot_id": proj.snapshot_id,
            "nodes": [n.to_dict() for n in proj.nodes],
            "edges": [e.to_dict() for e in proj.edges],
        }, sort_keys=True, ensure_ascii=False)
        return stable_hash(content)

    def save(self, proj: NeuronProjection) -> None:
        """持久化到 .memoryguard/projections/neuron.json。"""
        self.proj_path.parent.mkdir(parents=True, exist_ok=True)
        self.proj_path.write_text(
            json.dumps(proj.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8")

    def load(self) -> NeuronProjection | None:
        if not self.proj_path.exists():
            return None
        try:
            data = json.loads(self.proj_path.read_text(encoding="utf-8"))
            return NeuronProjection(
                snapshot_id=data.get("snapshot_id", ""),
                built_at=data.get("built_at", ""),
                content_hash=data.get("content_hash", ""),
                nodes=[ProjectionNode(**n) for n in data.get("nodes", [])],
                edges=[ProjectionEdge(**e) for e in data.get("edges", [])],
                meta=data.get("meta", {}) if isinstance(data.get("meta"), dict) else {},
            )
        except (OSError, json.JSONDecodeError):
            return None

    def delete(self) -> None:
        """删除投影（可从 IR + decisions 重建）。"""
        if self.proj_path.exists():
            self.proj_path.unlink()

    def get_or_empty(self) -> dict[str, Any]:
        """GUI API 用：未构建时返回 empty 状态。"""
        proj = self.load()
        if proj is None:
            return {"empty": True, "reason": "not_built"}
        return proj.to_dict()
