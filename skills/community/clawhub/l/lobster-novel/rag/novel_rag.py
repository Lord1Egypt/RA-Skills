#!/usr/bin/env python3
"""
novel_rag.py — RAG semantic retrieval for novel writing context.

Builds a local TF-IDF index from story-state.json + knowledge_graph + bible,
then retrieves top-K relevant context items (characters, hooks, locations,
past chapter events, relations) for each chapter being written.

No external API calls. Uses sklearn + numpy, both already installed.

Usage:
    from rag.novel_rag import NovelRAGIndex, format_rag_prompt

    index = NovelRAGIndex(project_dir)
    index.build()                           # 构建索引
    results = index.search("query text")    # 检索 top-K
    prompt_block = format_rag_prompt(results)
"""

from __future__ import annotations

import hashlib
import json
import pickle
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── 确保能找到 core/ 及上级目录（用于相对和绝对导入）────
_base = Path(__file__).resolve().parent.parent
for p in [str(_base), str(_base / "core")]:
    if p not in sys.path:
        sys.path.insert(0, p)

from core.story_state import StoryState


# ═══════════════════════════════════════════════════════════════
#  Constants
# ═══════════════════════════════════════════════════════════════

DEFAULT_TOP_K = 8               # 默认返回 top-K

RAG_CACHE_FILE = ".rag_index.pkl"

CATEGORY_ICONS = {
    "character": "👤",
    "hook": "🎣",
    "location": "📍",
    "chapter_summary": "📖",
    "relation": "🔗",
    "setting": "🏰",
}


# ═══════════════════════════════════════════════════════════════
#  Data classes
# ═══════════════════════════════════════════════════════════════


@dataclass
class RAGDocument:
    """A single indexed document."""

    doc_id: str
    content: str
    category: str  # character / hook / location / chapter_summary / relation / setting
    chapter: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """Single retrieval hit."""

    doc_id: str
    content: str
    category: str
    score: float
    chapter: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def icon(self) -> str:
        return CATEGORY_ICONS.get(self.category, "•")

    def short(self, max_len: int = 80) -> str:
        txt = self.content.replace("\n", " ")[:max_len]
        if len(self.content) > max_len:
            txt += "…"
        return txt


# ═══════════════════════════════════════════════════════════════
#  NovelRAGIndex — build, persist, search
# ═══════════════════════════════════════════════════════════════


class NovelRAGIndex:
    """
    TF-IDF based RAG index for novel writing context.

    Builds from:
      - StoryState.chapters           → chapter summaries
      - StoryState.hooks              → active hooks
      - StoryState.characters         → character profiles
      - knowledge_graph/entities.jsonl → locations & items
      - knowledge_graph/relations.jsonl → relationships
      - bible.json                     → extended character bios
    """

    def __init__(self, project_dir: str | Path) -> None:
        self.project_dir = Path(project_dir)
        self._docs: list[RAGDocument] = []
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._tfidf_matrix: Optional[np.ndarray] = None
        self._story_state: Optional[StoryState] = None

    # ── Public API ────────────────────────────────────────────

    def build(self, story_state: Optional[StoryState] = None) -> int:
        """
        Build (or rebuild) the index from project data.
        Returns document count.
        """
        if story_state is not None:
            self._story_state = story_state
        else:
            self._story_state = StoryState.load(self.project_dir)

        self._docs = []
        state = self._story_state

        # 1. Chapter summaries
        self._index_chapters(state)

        # 2. Characters (from story-state + bible)
        self._index_characters(state)

        # 3. Hooks
        self._index_hooks(state)

        # 4. Locations (from knowledge graph)
        self._index_knowledge_graph()

        # 5. Bible settings
        self._index_bible()

        # 6. Build TF-IDF matrix
        self._build_vectorizer()

        print(f"[NovelRAG] Index built: {len(self._docs)} documents across "
              f"{len(set(d.category for d in self._docs))} categories")
        return len(self._docs)

    def search(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        categories: Optional[list[str]] = None,
        min_score: float = 0.0,
        boost_recent: bool = True,
    ) -> list[SearchResult]:
        """
        Search the index, return top-K results.

        Parameters
        ----------
        query : str
            Search query (typically the chapter outline or key phrase).
        top_k : int
            Maximum results to return.
        categories : list[str] or None
            Filter to specific categories (e.g. ['character', 'hook']).
        min_score : float
            Minimum similarity threshold.
        boost_recent : bool
            Boost documents from recent chapters (last 10).
        """
        if self._tfidf_matrix is None or self._vectorizer is None:
            print("[NovelRAG] No index loaded. Call build() first.")
            return []

        # Vectorize query
        query_vec = self._vectorizer.transform([query])

        # Cosine similarity
        sims = cosine_similarity(query_vec, self._tfidf_matrix).flatten()

        # Apply filters
        valid: list[tuple[int, float]] = []
        for i, score in enumerate(sims):
            if score < min_score:
                continue
            if categories and self._docs[i].category not in categories:
                continue
            valid.append((i, score))

        # Sort by score (descending)
        valid.sort(key=lambda x: -x[1])

        # Compute max chapter once (outside loop) for boost calculation
        max_ch = 0
        if boost_recent:
            max_ch = max(
                (d.chapter for d in self._docs if d.chapter > 0),
                default=0,
            )

        # Build results (top_k)
        hits: list[SearchResult] = []
        for idx, score in valid[:top_k]:
            doc = self._docs[idx]
            final_score = float(score)

            # Recent chapter boost: +10% per chapter within last 10
            if boost_recent and doc.chapter > 0 and max_ch > 0 and doc.chapter >= max_ch - 10:
                recency_boost = 1.0 + 0.15 * (1 - (max_ch - doc.chapter) / 10)
                final_score *= recency_boost

            hits.append(SearchResult(
                doc_id=doc.doc_id,
                content=doc.content,
                category=doc.category,
                score=round(final_score, 4),
                chapter=doc.chapter,
                metadata=doc.metadata,
            ))

        # Re-sort after boost
        hits.sort(key=lambda x: -x.score)
        return hits

    def save(self) -> None:
        """Persist index to disk."""
        path = self.project_dir / RAG_CACHE_FILE
        data = {
            "docs": self._docs,
            "vectorizer": self._vectorizer,
            "tfidf_matrix": self._tfidf_matrix,
        }
        path.write_bytes(pickle.dumps(data))
        print(f"[NovelRAG] Index saved to {path} ({len(self._docs)} docs)")

    @classmethod
    def load(cls, project_dir: str | Path) -> Optional[NovelRAGIndex]:
        """Load persisted index from disk."""
        path = Path(project_dir) / RAG_CACHE_FILE
        if not path.exists():
            return None
        try:
            data = pickle.loads(path.read_bytes())
            idx = cls.__new__(cls)
            idx.project_dir = Path(project_dir)
            idx._docs = data["docs"]
            idx._vectorizer = data["vectorizer"]
            idx._tfidf_matrix = data["tfidf_matrix"]
            idx._story_state = None
            print(f"[NovelRAG] Index loaded from {path} ({len(idx._docs)} docs)")
            return idx
        except Exception as e:
            print(f"[NovelRAG] Failed to load cache: {e}")
            return None

    # ── Internal: Index builders ──────────────────────────────

    def _index_chapters(self, state: StoryState) -> None:
        """Index past chapter key_events as searchable summaries."""
        for num, ch in sorted(state.chapters.items()):
            events = ch.key_events or []
            if not events:
                continue
            content = f"第{num}章 {ch.title or ''}: " + "；".join(events[:10])
            char_list = "、".join(ch.characters_present or [])
            self._docs.append(RAGDocument(
                doc_id=f"ch{num}",
                content=content,
                category="chapter_summary",
                chapter=num,
                metadata={
                    "title": ch.title or f"第{num}章",
                    "scene": ch.scene or "",
                    "word_count": ch.word_count,
                    "characters": char_list,
                },
            ))

    def _index_characters(self, state: StoryState) -> None:
        """Index characters from story-state + bible."""
        # From story-state
        for cid, ch in state.characters.items():
            parts = [ch.name or cid]
            if ch.role:
                parts.append(f"角色定位：{ch.role}")
            if ch.state:
                parts.append(ch.state)
            if ch.key_items:
                parts.append(f"关键物品：{'、'.join(ch.key_items)}")
            self._docs.append(RAGDocument(
                doc_id=f"char_{cid}",
                content="。".join(parts),
                category="character",
                chapter=ch.last_appearance,
                metadata={
                    "name": ch.name or cid,
                    "role": ch.role,
                    "status": ch.status,
                    "first_appearance": ch.first_appearance,
                    "last_appearance": ch.last_appearance,
                },
            ))

        # From bible.json (extended bios)
        bible_path = self.project_dir / "bible.json"
        if bible_path.exists():
            try:
                bible = json.loads(bible_path.read_text(encoding="utf-8"))
                for name, info in (bible.get("characters") or {}).items():
                    cid = f"bible_{name}"
                    parts = [f"{name}"]
                    for key in ("traits", "background", "motivation", "arc", "notes"):
                        val = info.get(key)
                        if val:
                            if isinstance(val, list):
                                parts.append(f"{key}：{'、'.join(val)}")
                            else:
                                parts.append(f"{key}：{val}")
                    # Merge/upsert: replace content and update metadata
                    existing = [d for d in self._docs if d.doc_id == cid]
                    merged_content = "。".join(parts)
                    if not existing:
                        self._docs.append(RAGDocument(
                            doc_id=cid,
                            content=merged_content,
                            category="character",
                            chapter=info.get("last_appearance", 0),
                            metadata={"name": name, "role": info.get("role", "")},
                        ))
                    else:
                        existing[0].content = merged_content
                        # 更新 chapter 和 metadata（取较大值）
                        bib_ch = info.get("last_appearance", 0)
                        bib_role = info.get("role", "")
                        if bib_ch:
                            existing[0].chapter = max(existing[0].chapter, bib_ch)
                        if bib_role:
                            existing[0].metadata["role"] = bib_role
            except (json.JSONDecodeError, OSError):
                pass

    def _index_hooks(self, state: StoryState) -> None:
        """Index active and resolved hooks."""
        for hid, hook in state.hooks.items():
            status_tag = "【活跃】" if hook.status == "活跃" else "【已兑现】"
            content = f"{status_tag}{hook.description} (类型：{hook.type})"
            self._docs.append(RAGDocument(
                doc_id=f"hook_{hid}",
                content=content,
                category="hook",
                chapter=hook.chapter_created,
                metadata={
                    "hook_id": hid,
                    "type": hook.type,
                    "status": hook.status,
                    "created": hook.chapter_created,
                    "resolved": hook.chapter_resolved,
                },
            ))

    def _index_knowledge_graph(self) -> None:
        """Index entities and relations from knowledge_graph/."""
        kg_dir = self.project_dir / "knowledge_graph"

        # Entities
        entities_file = kg_dir / "entities.jsonl"
        if entities_file.exists():
            for line in entities_file.read_text(encoding="utf-8").splitlines():
                if not line:
                    continue
                try:
                    ent = json.loads(line)
                    etype = ent.get("type", "")
                    label = ent.get("label", "")
                    props = ent.get("properties", {})
                    chapter = ent.get("last_seen", 0)

                    if etype == "location":
                        desc = props.get("description", "")
                        content = f"地点：{label}。{desc}" if desc else f"地点：{label}"
                        self._docs.append(RAGDocument(
                            doc_id=f"loc_{label}",
                            content=content,
                            category="location",
                            chapter=chapter,
                            metadata={"label": label},
                        ))
                    elif etype == "item":
                        desc = props.get("description", "")
                        owner = props.get("owner", "")
                        parts = [f"物品：{label}"]
                        if owner:
                            parts.append(f"持有者：{owner}")
                        if desc:
                            parts.append(desc)
                        self._docs.append(RAGDocument(
                            doc_id=f"item_{label}",
                            content="。".join(parts),
                            category="setting",
                            chapter=chapter,
                            metadata={"label": label, "type": "item"},
                        ))
                except (json.JSONDecodeError, KeyError):
                    continue

        # Relations
        relations_file = kg_dir / "relations.jsonl"
        if relations_file.exists():
            for line in relations_file.read_text(encoding="utf-8").splitlines():
                if not line:
                    continue
                try:
                    rel = json.loads(line)
                    src = rel.get("source", "").replace("char_", "").replace("loc_", "")
                    tgt = rel.get("target", "").replace("char_", "").replace("loc_", "")
                    rel_type = rel.get("relation", "")
                    ctx = rel.get("context", "")
                    chapter = rel.get("chapter", 0)
                    content = f"{src} → {rel_type} → {tgt}"
                    if ctx:
                        content += f" ({ctx})"
                    self._docs.append(RAGDocument(
                        doc_id=f"rel_{src}_{rel_type}_{tgt}_{chapter}",
                        content=content,
                        category="relation",
                        chapter=chapter,
                        metadata={"source": src, "target": tgt, "relation": rel_type},
                    ))
                except (json.JSONDecodeError, KeyError):
                    continue

    def _index_bible(self) -> None:
        """Index setting/lore from bible.json (non-character fields)."""
        bible_path = self.project_dir / "bible.json"
        if not bible_path.exists():
            return
        try:
            bible = json.loads(bible_path.read_text(encoding="utf-8"))
            # Settings & world info
            for key in ("world_info", "settings", "locations", "lore", "factions", "magic_system"):
                val = bible.get(key)
                if val:
                    if isinstance(val, dict):
                        for name, desc in val.items():
                            # 展开嵌套 dict（如 {type, description, first_appearance}）
                            if isinstance(desc, dict):
                                parts = [f"{key}：{name}"]
                                for dk, dv in desc.items():
                                    if isinstance(dv, str):
                                        parts.append(f"{dk}：{dv}")
                                txt = "，".join(parts)
                            else:
                                txt = f"{key}：{name}。{desc}" if isinstance(desc, str) else f"{key}：{name}"
                            self._docs.append(RAGDocument(
                                doc_id=f"bible_{key}_{name}",
                                content=txt[:500],
                                category="setting",
                                metadata={"source_key": key, "label": name},
                            ))
                    elif isinstance(val, list):
                        for item in val:
                            txt = f"{key}：{item}" if isinstance(item, str) else str(item)
                            self._docs.append(RAGDocument(
                                doc_id=f"bible_{key}_{hashlib.md5(txt.encode()).hexdigest()[:8]}",
                                content=txt[:500],
                                category="setting",
                                metadata={"source_key": key},
                            ))
                    elif isinstance(val, str):
                        self._docs.append(RAGDocument(
                            doc_id=f"bible_{key}",
                            content=f"{key}：{val[:500]}",
                            category="setting",
                            metadata={"source_key": key},
                        ))
            # Title, logline, theme
            for key in ("title", "logline", "theme", "tone"):
                val = bible.get(key)
                if val:
                    self._docs.append(RAGDocument(
                        doc_id=f"bible_{key}",
                        content=f"{key}：{val}",
                        category="setting",
                        metadata={"source_key": key},
                    ))
        except (json.JSONDecodeError, OSError):
            pass

    def _build_vectorizer(self) -> None:
        """Build TF-IDF matrix from indexed documents."""
        if not self._docs:
            self._vectorizer = None
            self._tfidf_matrix = None
            return

        texts = [d.content for d in self._docs]
        self._vectorizer = TfidfVectorizer(
            analyzer="char_wb",         # character n-grams with word boundaries
            ngram_range=(2, 4),         # 2-4 character grams (good for Chinese)
            max_features=10000,         # limit to 10K features
            sublinear_tf=True,          # use 1+log(tf)
            strip_accents="unicode",
            lowercase=False,            # Chinese doesn't need lowercasing
        )
        self._tfidf_matrix = self._vectorizer.fit_transform(texts)


# ═══════════════════════════════════════════════════════════════
#  Prompt formatting helpers
# ═══════════════════════════════════════════════════════════════


def format_rag_prompt(results: list[SearchResult], top_k: int = 5) -> str:
    """
    Format search results into a prompt block for injection into
    the writing context.
    """
    lines = ["【RAG 语义检索 — 相关设定/角色/伏笔】"]
    if not results:
        lines.append("  （无相关结果）")
        return "\n".join(lines)

    # Group by category
    grouped: dict[str, list[SearchResult]] = OrderedDict()
    categories_order = ["character", "hook", "setting", "location", "chapter_summary", "relation"]
    for cat in categories_order:
        hits = [r for r in results if r.category == cat]
        if hits:
            grouped[cat] = hits[:3]  # max 3 per category

    # Also include any that didn't match an ordered category
    for r in results[:top_k]:
        if r.category not in grouped:
            grouped.setdefault(r.category, []).append(r)

    count = 0
    for cat, hits in grouped.items():
        icon = CATEGORY_ICONS.get(cat, "•")
        label = {"character": "角色", "hook": "伏笔", "setting": "设定",
                 "location": "地点", "chapter_summary": "历史章节", "relation": "关系"}.get(cat, cat)
        lines.append(f"\n{icon} {label}：")
        for h in hits[:top_k]:
            if count >= top_k:
                break
            count += 1
            lines.append(f"  [{h.score:.2f}] {h.short(120)}")
        if count >= top_k:
            break

    # 如果分组后什么也没输出（极罕见），平铺所有结果
    if not any(lines.count(f"  [{h.score:.2f}] ") for h in results):
        for h in results[:top_k]:
            lines.append(f"  [{h.score:.2f}] [{h.category}] {h.short(120)}")

    return "\n".join(lines)


def build_and_search(
    project_dir: str | Path,
    query: str,
    top_k: int = DEFAULT_TOP_K,
    force_rebuild: bool = False,
    categories: Optional[list[str]] = None,
    min_score: float = 0.0,
) -> list[SearchResult]:
    """
    Convenience: load or build index, then search.
    """
    idx = None
    if not force_rebuild:
        idx = NovelRAGIndex.load(project_dir)
    if idx is None:
        idx = NovelRAGIndex(project_dir)
        idx.build()
        idx.save()

    return idx.search(query, top_k=top_k, categories=categories, min_score=min_score)


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Novel RAG index builder & searcher")
    parser.add_argument("--dir", default=".", help="novel project directory")
    parser.add_argument("--rebuild", action="store_true", help="force index rebuild")
    parser.add_argument("--search", help="search query")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="results count")
    args = parser.parse_args()

    project = Path(args.dir)

    if args.rebuild or not (project / RAG_CACHE_FILE).exists():
        print(f"Building index for {project}...")
        idx = NovelRAGIndex(project)
        count = idx.build()
        idx.save()
        print(f"Indexed {count} documents")
    else:
        idx = NovelRAGIndex.load(project)

    if args.search and idx:
        results = idx.search(args.search, top_k=args.top_k)
        print(f"\nQuery: {args.search}")
        print(f"Results: {len(results)}")
        for r in results:
            print(f"  [{r.icon()}] [{r.score:.3f}] [{r.category}] {r.short(120)}")
        print()
        print(format_rag_prompt(results, top_k=args.top_k))
