"""
NovaMemory Core Engine
Nova 工作空间自研记忆引擎 — 纯本地 TF-IDF + JSON 存储
"""

from __future__ import annotations

import json
import math
import os
import re
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "nova_memory requires scikit-learn. Install with: pip install scikit-learn --break-system-packages"
    ) from exc


# ---------------------------------------------------------------------------
# 类型别名
# ---------------------------------------------------------------------------
MemoryRecord = dict[str, Any]  # 单条记忆的结构
EntityGraph = dict[str, dict[str, Any]]  # 实体图谱


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def _utc_now() -> str:
    """返回 UTC ISO 格式时间字符串。"""
    return datetime.now(timezone.utc).isoformat()


def _normalize_text(text: str) -> str:
    """小写 + 去除非字母数字，保留空格。"""
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def _ensure_dir(path: Path) -> None:
    """确保目录存在。"""
    path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# NovaMemory 主类
# ---------------------------------------------------------------------------

class NovaMemory:
    """
    Nova 工作空间自研记忆引擎。

    存储结构::

        storage_dir/
        ├── memories/          # 每条记忆一个 .json 文件
        │   └── <uuid>.json
        ├── entities.json      # 实体图谱
        ├── index.json         # tag 倒排索引
        └── meta.json          # 全局元数据

    参数:
        storage_dir: 存储根目录，默认为 /workspace/memory/nova-memory/
    """

    MEMORIES_DIR = "memories"
    ENTITIES_FILE = "entities.json"
    INDEX_FILE = "index.json"
    META_FILE = "meta.json"

    def __init__(self, storage_dir: str = "/workspace/memory/nova-memory/") -> None:
        self.storage_dir = Path(storage_dir)
        self.memories_dir = self.storage_dir / self.MEMORIES_DIR
        self.entities_path = self.storage_dir / self.ENTITIES_FILE
        self.index_path = self.storage_dir / self.INDEX_FILE
        self.meta_path = self.storage_dir / self.META_FILE

        # 内存状态
        self._memories: dict[str, MemoryRecord] = {}  # memory_id → record
        self._entities: EntityGraph = {}  # entity_name → facts
        self._tag_index: dict[str, list[str]] = defaultdict(list)  # tag → [memory_id, ...]
        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=5000,
            stop_words="english",
        )
        self._vectors: dict[str, list[float]] = {}  # memory_id → vector

        _ensure_dir(self.memories_dir)
        self.load()

    # ------------------------------------------------------------------
    # 公共 API
    # ------------------------------------------------------------------

    def remember(
        self,
        content: str,
        tags: list[str] | None = None,
        entity: str | None = None,
    ) -> str:
        """
        记忆一条信息，返回 memory_id。

        参数:
            content: 记忆内容（任意文本）
            tags: 可选标签列表，用于分类和检索
            entity: 可选关联实体名称

        返回:
            新记忆的 UUID 字符串
        """
        memory_id = str(uuid.uuid4())
        now = _utc_now()

        record: MemoryRecord = {
            "id": memory_id,
            "content": content,
            "tags": [t.strip().lower() for t in (tags or [])],
            "entity": entity.strip() if entity else None,
            "created_at": now,
            "updated_at": now,
        }

        # 写入文件
        path = self.memories_dir / f"{memory_id}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

        # 更新内存状态
        self._memories[memory_id] = record

        # 更新 tag 倒排索引
        for tag in record["tags"]:
            if memory_id not in self._tag_index[tag]:
                self._tag_index[tag].append(memory_id)

        # 更新 TF-IDF 向量（追加到现有 vocab）
        self._refresh_vectors([record])

        return memory_id

    def recall(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        语义检索，返回最相关的记忆。

        使用 TF-IDF + Cosine Similarity 匹配，实体关联和标签可额外加权。

        参数:
            query: 自然语言查询
            top_k: 返回结果数量上限

        返回:
            按相似度降序排列的记忆列表，每项包含 id/content/tags/score/created_at
        """
        if not self._memories:
            return []

        # 构建语料库
        ids = list(self._memories.keys())
        texts = [
            self._memories[mid]["content"] for mid in ids
        ]

        try:
            tfidf_matrix = self._vectorizer.fit_transform(texts)
            query_vec = self._vectorizer.transform([_normalize_text(query)])
        except Exception:  # 词汇表为空或无法向量化
            return []

        # Cosine Similarity
        sims = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # 组装结果（包含标签和实体加权）
        results = []
        for idx, score in enumerate(sims):
            mid = ids[idx]
            rec = self._memories[mid]

            # 标签/实体加权：查询词出现在 tags 中 +0.2
            q_lower = query.lower()
            tag_bonus = 0.0
            if any(q_lower in t or t in q_lower for t in rec.get("tags", [])):
                tag_bonus = 0.2
            entity_bonus = 0.1 if rec.get("entity") and rec["entity"].lower() in q_lower else 0.0

            final_score = min(score + tag_bonus + entity_bonus, 1.0)
            results.append(
                {
                    "id": mid,
                    "content": rec["content"],
                    "tags": rec.get("tags", []),
                    "entity": rec.get("entity"),
                    "score": round(float(final_score), 4),
                    "created_at": rec.get("created_at", ""),
                }
            )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def remember_entity(self, name: str, facts: dict[str, Any]) -> None:
        """
        记住一个实体的多个属性。

        参数:
            name: 实体名称（如 "Eric"）
            facts: 实体属性字典，如 {"职业": "投资者", "城市": "重庆"}
        """
        name_key = name.strip()
        if name_key not in self._entities:
            self._entities[name_key] = {"_meta": {"created_at": _utc_now()}}
        self._entities[name_key]["_meta"]["updated_at"] = _utc_now()
        for k, v in facts.items():
            self._entities[name_key][k.strip()] = v

    def get_entity(self, name: str) -> dict[str, Any] | None:
        """
        获取实体信息。

        参数:
            name: 实体名称

        返回:
            实体属性字典，不存在则返回 None
        """
        return self._entities.get(name.strip())

    def search_by_tag(self, tag: str) -> list[dict[str, Any]]:
        """
        按标签精确搜索记忆。

        参数:
            tag: 标签名（大小写不敏感）

        返回:
            匹配的记忆列表（按创建时间倒序）
        """
        tag_key = tag.strip().lower()
        memory_ids = self._tag_index.get(tag_key, [])
        results = []
        for mid in memory_ids:
            rec = self._memories.get(mid)
            if rec:
                results.append(
                    {
                        "id": mid,
                        "content": rec["content"],
                        "tags": rec.get("tags", []),
                        "entity": rec.get("entity"),
                        "created_at": rec.get("created_at", ""),
                    }
                )
        # 按时间倒序
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return results

    def get_memory_graph(self) -> dict[str, Any]:
        """
        返回记忆图谱结构。

        返回:
            包含实体节点、记忆节点和边的完整图谱字典
        """
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, str]] = []

        # 实体节点
        for entity_name, facts in self._entities.items():
            nodes.append({
                "type": "entity",
                "id": entity_name,
                "label": entity_name,
                "facts": {k: v for k, v in facts.items() if not k.startswith("_")},
            })

        # 记忆节点（按 entity 聚合，最多展示最近 20 条）
        recent = sorted(
            [r for r in self._memories.values() if r.get("entity")],
            key=lambda x: x.get("created_at", ""),
            reverse=True,
        )[:20]

        for rec in recent:
            entity = rec.get("entity")
            nodes.append({
                "type": "memory",
                "id": rec["id"],
                "label": rec["content"][:60] + ("…" if len(rec["content"]) > 60 else ""),
                "tags": rec.get("tags", []),
                "entity": entity,
                "created_at": rec.get("created_at", ""),
            })
            if entity:
                edges.append({"from": entity, "to": rec["id"], "label": "recalled_by"})

        # 实体间关系（共享相同 tags 的实体视为相关）
        entity_names = list(self._entities.keys())
        seen_rels: set[tuple[str, str]] = set()
        for i, e1 in enumerate(entity_names):
            for e2 in entity_names[i + 1 :]:
                t1 = set(k for k in self._entities[e1].keys() if not k.startswith("_"))
                t2 = set(k for k in self._entities[e2].keys() if not k.startswith("_"))
                common = t1 & t2
                if common:
                    key = tuple(sorted([e1, e2]))
                    if key not in seen_rels:
                        seen_rels.add(key)
                        edges.append({
                            "from": e1,
                            "to": e2,
                            "label": f"shares: {', '.join(list(common)[:3])}",
                        })

        return {"nodes": nodes, "edges": edges, "stats": {
            "total_memories": len(self._memories),
            "total_entities": len(self._entities),
            "total_tags": len(self._tag_index),
        }}

    def auto_reflect(self) -> str:
        """
        自动反思：基于近期记忆生成洞察摘要。

        分析最近 50 条记忆，提取：
        - 高频标签
        - 关联最多的实体
        - 近期主题趋势

        返回:
            洞察摘要文本
        """
        if not self._memories:
            return "📭 记忆库为空，无法生成反思。"

        # 取最近 50 条
        recent = sorted(
            self._memories.values(),
            key=lambda x: x.get("created_at", ""),
            reverse=True,
        )[:50]

        # 统计标签频率
        tag_counts: dict[str, int] = defaultdict(int)
        for rec in recent:
            for tag in rec.get("tags", []):
                tag_counts[tag] += 1

        # 统计实体出现频率
        entity_counts: dict[str, int] = defaultdict(int)
        for rec in recent:
            if rec.get("entity"):
                entity_counts[rec["entity"]] += 1

        # 近期主题（recency 加权）
        all_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

        lines = [
            "🪞 **Nova 自动反思报告**",
            f"📊 分析样本：最近 {len(recent)} 条记忆（总记忆 {len(self._memories)} 条）",
            "",
        ]

        if all_tags[:5]:
            lines.append("**🏷️ 高频标签 TOP5**")
            for tag, cnt in all_tags[:5]:
                bar = "█" * cnt
                lines.append(f"  {tag:<20} {bar} ({cnt})")
            lines.append("")

        if entity_counts:
            top_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            lines.append("**👤 高关联实体 TOP5**")
            for name, cnt in top_entities:
                lines.append(f"  {name:<20} 出现 {cnt} 次")
            lines.append("")

        # 洞察
        insights: list[str] = []
        if all_tags:
            top_tag = all_tags[0][0]
            insights.append(f"近期最活跃话题是「{top_tag}」")
        if entity_counts:
            top_entity = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[0][0]
            insights.append(f"「{top_entity}」是记忆网络中最重要的实体")

        if len(self._memories) > 100:
            insights.append("记忆库规模较大，建议定期归档旧记忆")
        if tag_counts and len(all_tags) > 20:
            insights.append("标签体系丰富，可考虑合并相似标签")

        if insights:
            lines.append("**💡 洞察**")
            for ins in insights:
                lines.append(f"  • {ins}")

        lines.append("")
        lines.append(f"_生成时间：{_utc_now()}_")

        return "\n".join(lines)

    def save(self) -> None:
        """
        将内存状态持久化写入磁盘。
        """
        _ensure_dir(self.storage_dir)

        # entities
        with open(self.entities_path, "w", encoding="utf-8") as f:
            json.dump(self._entities, f, ensure_ascii=False, indent=2)

        # tag 倒排索引
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(dict(self._tag_index), f, ensure_ascii=False, indent=2)

        # meta
        meta = {
            "saved_at": _utc_now(),
            "total_memories": len(self._memories),
            "total_entities": len(self._entities),
            "total_tags": len(self._tag_index),
        }
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        """
        从磁盘加载持久化状态到内存。
        """
        # 加载 memories
        self._memories.clear()
        if self.memories_dir.exists():
            for fpath in self.memories_dir.glob("*.json"):
                try:
                    rec = json.loads(fpath.read_text(encoding="utf-8"))
                    self._memories[rec["id"]] = rec
                except Exception:
                    pass  # 跳过损坏的文件

        # 加载 entities
        self._entities.clear()
        if self.entities_path.exists():
            try:
                self._entities = json.loads(self.entities_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        # 重建 tag 倒排索引
        self._tag_index.clear()
        for rec in self._memories.values():
            for tag in rec.get("tags", []):
                if rec["id"] not in self._tag_index[tag]:
                    self._tag_index[tag].append(rec["id"])

        # 重建 TF-IDF 向量
        self._refresh_vectors(list(self._memories.values()))

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _refresh_vectors(self, records: list[MemoryRecord]) -> None:
        """
        基于所有当前记忆重建 TF-IDF 向量。
        """
        if not self._memories:
            self._vectors.clear()
            return

        ids = list(self._memories.keys())
        texts = [self._memories[mid]["content"] for mid in ids]

        try:
            tfidf_matrix = self._vectorizer.fit_transform(texts)
            for idx, mid in enumerate(ids):
                self._vectors[mid] = tfidf_matrix[idx].toarray().flatten().tolist()
        except Exception:
            self._vectors.clear()

    # ------------------------------------------------------------------
    # 便捷属性
    # ------------------------------------------------------------------

    @property
    def stats(self) -> dict[str, int]:
        """返回记忆库统计信息。"""
        return {
            "total_memories": len(self._memories),
            "total_entities": len(self._entities),
            "total_tags": len(self._tag_index),
        }

    def __repr__(self) -> str:
        return f"NovaMemory(storage_dir={str(self.storage_dir)!r}, memories={len(self._memories)})"
