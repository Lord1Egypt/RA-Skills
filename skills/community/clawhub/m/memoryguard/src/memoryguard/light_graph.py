"""光点神经树管理器（移植自 merakagent LightGraphManager）。

把工作区的记忆/RAG/指令萃取成 KnowledgeClaim，挂到光点树上:
  main -> memoryType(大类) -> domain(小类) -> claim_anchor(叶记忆)

治理能力（这才是治理，不是只读报告）:
- 三步挂载：精确匹配 -> 语义匹配(TF-IDF) -> 新建 tentative
- 密度分裂：claim 过多时聚类派生子光点
- 晋升/凋亡：tentative 满足条件晋升 confirmed，长期不用 dissolve
- 合并建议：相似光点产出建议（不自动合并）
- 存活图谱快照：供 UI 可视化
- 衰减/强化：useCount、decayScore

与 merakagent 的取舍：
- 用 TF-IDF 余弦相似度代替 embedding（保持零依赖）
- 用内存数据结构（dict）代替 SQLite（首期，规模小）
- 萃取规则用确定性文本分析（标题/列表项/关键句），不调 LLM
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .schema import AGR, AGRType, stable_id


# ---------------------------------------------------------------------------
# 数据模型（对应 merakagent VectorStore 表结构）
# ---------------------------------------------------------------------------


@dataclass
class KnowledgeClaim:
    """从记忆/RAG 萃取出的知识记忆片段。"""

    id: int
    display_label: str
    body: str
    memory_type: str  # profile/preference/schedule/knowledge/...
    source: str  # 来源文件路径
    light_id: str = ""
    status: str = "active"  # proposed/active/superseded
    use_count: int = 0
    last_used_at: float = 0.0
    confidence: float = 0.5
    pinned: bool = False
    priority: int = 0
    created_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "display_label": self.display_label, "body": self.body,
            "memory_type": self.memory_type, "source": self.source, "light_id": self.light_id,
            "status": self.status, "use_count": self.use_count,
            "last_used_at": self.last_used_at, "confidence": self.confidence,
            "pinned": self.pinned, "priority": self.priority, "created_at": self.created_at,
        }


@dataclass
class LightNode:
    """光点节点：main/topic/claim_anchor。"""

    light_id: str
    parent_id: str
    label: str
    alias: str = ""
    status: str = "tentative"  # tentative/confirmed/dissolved
    center_vec: list[float] = field(default_factory=list)  # TF-IDF 中心向量
    node_kind: str = "topic"  # root/topic/claim_anchor
    anchor_claim_id: int = 0
    created_at: float = 0.0
    updated_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "light_id": self.light_id, "parent_id": self.parent_id, "label": self.label,
            "alias": self.alias, "status": self.status, "node_kind": self.node_kind,
            "anchor_claim_id": self.anchor_claim_id,
            "created_at": self.created_at, "updated_at": self.updated_at,
            "claim_count": 0,  # 由 manager 填充
        }


@dataclass
class LightEdge:
    """光点边：derived_from/related/conflict。"""

    edge_id: str
    from_node_id: str
    to_node_id: str
    edge_type: str  # derived_from/related/conflict
    directed: bool
    strength: float
    confidence: float
    evidence: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id, "from": self.from_node_id, "to": self.to_node_id,
            "type": self.edge_type, "directed": self.directed,
            "strength": self.strength, "confidence": self.confidence,
            "evidence": self.evidence,
        }


@dataclass
class LightMergeSuggestion:
    from_light_id: str
    to_light_id: str
    similarity: float


# ---------------------------------------------------------------------------
# TF-IDF 轻量语义匹配（纯标准库，代替 embedding）
# ---------------------------------------------------------------------------


class TfidfVectorizer:
    """简单 TF-IDF 向量化器，纯标准库实现。

    用途：给 claim 和光点生成语义向量，做余弦相似度匹配。
    不依赖 numpy/sklearn，保持零依赖。
    """

    def __init__(self):
        self._vocab: dict[str, int] = {}
        self._idf: dict[str, float] = {}
        self._docs: list[list[str]] = []

    def _tokenize(self, text: str) -> list[str]:
        # 中英文混合分词：英文按非字母数字，中文按字
        tokens: list[str] = []
        # 英文词
        for m in re.finditer(r"[A-Za-z][A-Za-z0-9_\-]+", text):
            tokens.append(m.group(0).lower())
        # 中文字（单字 + 2-4字滑窗）
        chinese = re.findall(r"[\u4e00-\u9fff]+", text)
        for seg in chinese:
            for i in range(len(seg)):
                tokens.append(seg[i])  # 单字
                if i + 2 <= len(seg):
                    tokens.append(seg[i:i+2])  # 双字
        return [t for t in tokens if len(t) >= 1]

    def fit(self, docs: list[str]) -> None:
        """计算 idf。"""
        self._docs = [self._tokenize(d) for d in docs]
        df: dict[str, int] = {}
        for toks in self._docs:
            seen = set(toks)
            for t in seen:
                df[t] = df.get(t, 0) + 1
        n = len(self._docs) if self._docs else 1
        self._vocab = {t: i for i, t in enumerate(df)}
        self._idf = {t: math.log((1 + n) / (1 + df_t)) + 1 for t, df_t in df.items()}

    def transform(self, text: str) -> list[float]:
        """文本 -> TF-IDF 向量。"""
        toks = self._tokenize(text)
        if not toks or not self._vocab:
            return []
        dim = len(self._vocab)
        tf: dict[str, int] = {}
        for t in toks:
            if t in self._vocab:
                tf[t] = tf.get(t, 0) + 1
        vec = [0.0] * dim
        for t, cnt in tf.items():
            idx = self._vocab[t]
            vec[idx] = cnt * self._idf.get(t, 1.0)
        return vec

    def cosine(self, a: list[float], b: list[float]) -> float:
        n = min(len(a), len(b))
        if n == 0:
            return 0.0
        dot = sum(a[i] * b[i] for i in range(n))
        na = math.sqrt(sum(x * x for x in a[:n]))
        nb = math.sqrt(sum(x * x for x in b[:n]))
        if na <= 0 or nb <= 0:
            return 0.0
        return max(0.0, dot / (na * nb))


# ---------------------------------------------------------------------------
# 光点神经树管理器（移植自 merakagent LightGraphManager）
# ---------------------------------------------------------------------------


class LightGraphManager:
    """光点神经树管理器。

    职责（对应 merakagent）:
    - 三步挂载：精确 -> 语义(TF-IDF) -> 新建 tentative
    - 密度分裂：claim 过多时聚类派生子光点
    - 晋升/凋亡：tentative 满足条件晋升，长期不用 dissolve
    - 合并建议：相似光点产出建议
    - 存活图谱快照：供 UI 可视化
    """

    # 阈值（对应 merakagent KnowledgeCapability）
    LIGHT_ATTACH_THRESHOLD = 0.35
    LIGHT_MERGE_THRESHOLD = 0.75
    LIGHT_SPLIT_CLAIM_COUNT = 8
    LIGHT_PROMOTE_USE_COUNT = 3
    LIGHT_PROMOTE_ACTIVE_COUNT = 3
    LIGHT_PROMOTE_SURVIVE_DAYS = 7
    LIGHT_DISSOLVE_DAYS = 30
    DECAY_HALF_LIFE_DAYS = 30
    MAX_LIGHT_DEPTH = 6

    def __init__(self):
        self._nodes: dict[str, LightNode] = {}
        self._edges: dict[str, LightEdge] = {}
        self._claims: dict[int, KnowledgeClaim] = {}
        self._next_claim_id = 1
        self._vectorizer = TfidfVectorizer()
        self._fitted = False
        self._ensure_main()

    def _ensure_main(self) -> None:
        if "main" not in self._nodes:
            now = self._now()
            self._nodes["main"] = LightNode(
                light_id="main", parent_id="", label="主光点",
                status="confirmed", node_kind="root",
                created_at=now, updated_at=now,
            )

    def _now(self) -> float:
        return datetime.now(timezone.utc).timestamp()

    # --- 添加 claim ---

    def add_claim(self, label: str, body: str, memory_type: str, source: str,
                  confidence: float = 0.5) -> KnowledgeClaim:
        """添加一条知识记忆。"""
        claim = KnowledgeClaim(
            id=self._next_claim_id, display_label=label, body=body,
            memory_type=memory_type, source=source, confidence=confidence,
            created_at=self._now(),
        )
        self._claims[claim.id] = claim
        self._next_claim_id += 1
        return claim

    # --- 萃取后的批量挂载 ---

    def fit_vectorizer(self) -> None:
        """用所有 claim body 拟合 TF-IDF。"""
        docs = [c.body for c in self._claims.values()]
        if docs:
            self._vectorizer.fit(docs)
            self._fitted = True

    def attach_all_claims(self) -> None:
        """把所有 claim 挂到光点树（三步挂载）。"""
        if not self._fitted:
            self.fit_vectorizer()
        for claim in list(self._claims.values()):
            if not claim.light_id:
                self._attach_claim_path(claim)

    def _attach_claim_path(self, claim: KnowledgeClaim) -> None:
        """三步挂载：main -> memoryType -> claim_anchor。"""
        # 第一层：memoryType 挂到 main
        category_node = self._attach_to_level("main", claim.memory_type, claim.body)
        # 第二层：claim_anchor 挂到 category
        anchor_id = f"ca_{claim.id}"
        if anchor_id not in self._nodes:
            now = self._now()
            self._nodes[anchor_id] = LightNode(
                light_id=anchor_id, parent_id=category_node.light_id,
                label=claim.display_label[:60], status="confirmed",
                node_kind="claim_anchor", anchor_claim_id=claim.id,
                created_at=now, updated_at=now,
            )
            self._write_edge(category_node.light_id, anchor_id, "derived_from",
                             True, 1.0, 1.0, "claim anchor")
        claim.light_id = anchor_id

    def _attach_to_level(self, parent_id: str, label: str, content: str) -> LightNode:
        """在 parent_id 下执行三步挂载，返回命中的光点。"""
        siblings = [n for n in self._nodes.values()
                    if n.parent_id == parent_id and n.status != "dissolved"
                    and n.node_kind != "claim_anchor"]
        # ① 精确匹配
        for s in siblings:
            if s.label.strip().lower() == label.strip().lower():
                return s
        # ② 语义匹配
        if self._fitted:
            vec = self._vectorizer.transform(content)
            best, best_sim = None, self.LIGHT_ATTACH_THRESHOLD
            for s in siblings:
                center = self._parse_vec(s.center_vec)
                if center:
                    sim = self._vectorizer.cosine(vec, center)
                    if sim >= best_sim:
                        best_sim, best = sim, s
            if best:
                return best
        # ③ 新建 tentative
        now = self._now()
        new_id = stable_id("ln", parent_id, label)[:16]
        vec = self._vectorizer.transform(content) if self._fitted else []
        node = LightNode(
            light_id=new_id, parent_id=parent_id, label=label,
            status="tentative", node_kind="topic",
            center_vec=vec, created_at=now, updated_at=now,
        )
        self._nodes[new_id] = node
        self._write_edge(parent_id, new_id, "derived_from", True, 1.0, 1.0, "category branch")
        return node

    def _write_edge(self, from_id: str, to_id: str, edge_type: str,
                    directed: bool, strength: float, confidence: float,
                    evidence: str) -> None:
        if not from_id or not to_id or from_id == to_id:
            return
        nf = from_id if directed else min(from_id, to_id)
        nt = to_id if directed else max(from_id, to_id)
        eid = f"le_{nf}_{nt}_{edge_type}"
        self._edges[eid] = LightEdge(
            edge_id=eid, from_node_id=nf, to_node_id=nt, edge_type=edge_type,
            directed=directed, strength=strength, confidence=confidence,
            evidence=evidence[:200],
        )

    def _parse_vec(self, vec: list[float]) -> list[float]:
        return vec if vec else []

    # --- 维护：晋升/凋亡/合并建议 ---

    def promote_or_dissolve(self) -> None:
        """晋升/凋亡扫描。"""
        now = self._now()
        promote_survive_cutoff = now - self.LIGHT_PROMOTE_SURVIVE_DAYS * 86400
        dissolve_cutoff = now - self.LIGHT_DISSOLVE_DAYS * 86400
        for node in list(self._nodes.values()):
            if node.status != "tentative" or node.node_kind == "claim_anchor":
                continue
            anchor_claims = self._collect_anchor_claims(node.light_id)
            used_total = sum(c.use_count for c in anchor_claims)
            survive_ok = node.created_at <= promote_survive_cutoff
            active_enough = len(anchor_claims) >= self.LIGHT_PROMOTE_ACTIVE_COUNT
            if used_total >= self.LIGHT_PROMOTE_USE_COUNT or (survive_ok and active_enough):
                node.status = "confirmed"
                node.updated_at = now
            elif node.updated_at <= dissolve_cutoff:
                self._dissolve_node(node)

    def _dissolve_node(self, node: LightNode) -> None:
        """凋亡：dissolved，子 anchor 迁移到最近的 confirmed。"""
        confirmed = [n for n in self._nodes.values()
                     if n.status == "confirmed" and n.light_id != node.light_id
                     and n.node_kind == "topic"]
        target_id = "main"
        if confirmed and node.center_vec:
            best, best_sim = None, 0.0
            for c in confirmed:
                if c.center_vec:
                    sim = self._vectorizer.cosine(node.center_vec, c.center_vec)
                    if sim > best_sim:
                        best_sim, best = sim, c
            if best:
                target_id = best.light_id
        # 迁移子 anchor
        for child in list(self._nodes.values()):
            if child.parent_id == node.light_id and child.node_kind == "claim_anchor":
                child.parent_id = target_id
                child.updated_at = self._now()
                if child.anchor_claim_id:
                    c = self._claims.get(child.anchor_claim_id)
                    if c:
                        c.light_id = child.light_id
        node.status = "dissolved"
        node.updated_at = self._now()

    def suggest_merge(self) -> list[LightMergeSuggestion]:
        """合并建议：confirmed 光点对相似度 >= 阈值。"""
        suggestions = []
        confirmed = [n for n in self._nodes.values()
                     if n.status == "confirmed" and n.node_kind == "topic"
                     and n.center_vec]
        for i, a in enumerate(confirmed):
            for b in confirmed[i+1:]:
                sim = self._vectorizer.cosine(a.center_vec, b.center_vec)
                if sim >= self.LIGHT_MERGE_THRESHOLD:
                    suggestions.append(LightMergeSuggestion(
                        from_light_id=a.light_id, to_light_id=b.light_id, similarity=sim))
        return suggestions

    def _collect_anchor_claims(self, root_id: str) -> list[KnowledgeClaim]:
        """BFS 收集子树所有 anchor claim。"""
        result = []
        visited = {root_id}
        queue = [root_id]
        while queue:
            cur = queue.pop(0)
            for n in self._nodes.values():
                if n.parent_id == cur and n.light_id not in visited:
                    visited.add(n.light_id)
                    if n.node_kind == "claim_anchor" and n.anchor_claim_id:
                        c = self._claims.get(n.anchor_claim_id)
                        if c:
                            result.append(c)
                    queue.append(n.light_id)
        return result

    # --- 存活图谱快照（供 UI 可视化） ---

    def build_live_snapshot(self) -> dict[str, Any]:
        """构建存活图谱快照：只保留 active claim 的祖先链。"""
        alive = {"main"}
        anchor_claim_ids = []
        for c in self._claims.values():
            if c.status in ("active", "proposed") and c.light_id:
                anchor_claim_ids.append(c.id)
                cursor = c.light_id
                guard = 0
                while cursor and cursor != "main" and guard < 16:
                    if cursor in alive:
                        break
                    alive.add(cursor)
                    node = self._nodes.get(cursor)
                    if not node:
                        break
                    cursor = node.parent_id
                    guard += 1
        nodes = []
        for n in self._nodes.values():
            if n.light_id in alive and n.status != "dissolved":
                d = n.to_dict()
                anchors = self._collect_anchor_claims(n.light_id)
                d["claim_count"] = len(anchors)
                d["use_count"] = sum(c.use_count for c in anchors)
                d["last_used_at"] = max((c.last_used_at for c in anchors), default=0)
                d["decay_score"] = self._compute_decay(d["last_used_at"], d["use_count"])
                nodes.append(d)
        edges = [e.to_dict() for e in self._edges.values()
                 if e.from_node_id in alive and e.to_node_id in alive]
        return {
            "nodes": nodes, "edges": edges,
            "anchor_claim_ids": anchor_claim_ids,
            "claims": [c.to_dict() for c in self._claims.values()
                       if c.status in ("active", "proposed")],
        }

    def _compute_decay(self, last_used_at: float, use_count: int) -> float:
        if last_used_at <= 0:
            return 0.0
        days = (self._now() - last_used_at) / 86400
        decay = 0.5 ** (days / self.DECAY_HALF_LIFE_DAYS)
        boost = min(0.2, math.log2(use_count + 1) * 0.05)
        return max(0.0, min(1.0, decay + boost))

    # --- 治理操作（UI 可调） ---

    def promote_light(self, light_id: str) -> bool:
        """手动晋升 tentative -> confirmed。"""
        n = self._nodes.get(light_id)
        if n and n.status == "tentative":
            n.status = "confirmed"
            n.updated_at = self._now()
            return True
        return False

    def dissolve_light(self, light_id: str) -> bool:
        """手动凋亡光点。"""
        n = self._nodes.get(light_id)
        if n and n.light_id != "main" and n.node_kind != "claim_anchor":
            self._dissolve_node(n)
            return True
        return False

    def merge_lights(self, from_id: str, to_id: str) -> bool:
        """合并两个光点：from 的子节点迁移到 to，from dissolved。"""
        if from_id == to_id or from_id == "main":
            return False
        for n in list(self._nodes.values()):
            if n.parent_id == from_id:
                n.parent_id = to_id
                n.updated_at = self._now()
        self._nodes[from_id].status = "dissolved"
        self._nodes[from_id].updated_at = self._now()
        return True

    def delete_claim(self, claim_id: int) -> bool:
        """删除 claim + 其 anchor 节点。"""
        c = self._claims.pop(claim_id, None)
        if not c:
            return False
        anchor_id = f"ca_{claim_id}"
        # 删 anchor 的边
        self._edges = {e: e for e in self._edges.values()
                       if e.from_node_id != anchor_id and e.to_node_id != anchor_id}
        # 补回 values
        self._edges = {k: v for k, v in self._edges.items() if v.from_node_id != anchor_id and v.to_node_id != anchor_id}
        self._nodes.pop(anchor_id, None)
        return True

    # --- 统计 ---

    def stats(self) -> dict[str, Any]:
        return {
            "claim_count": len(self._claims),
            "node_count": len([n for n in self._nodes.values() if n.status != "dissolved"]),
            "topic_count": len([n for n in self._nodes.values()
                                if n.node_kind == "topic" and n.status != "dissolved"]),
            "anchor_count": len([n for n in self._nodes.values() if n.node_kind == "claim_anchor"]),
            "tentative_count": len([n for n in self._nodes.values() if n.status == "tentative"]),
            "confirmed_count": len([n for n in self._nodes.values() if n.status == "confirmed"]),
            "edge_count": len(self._edges),
        }
