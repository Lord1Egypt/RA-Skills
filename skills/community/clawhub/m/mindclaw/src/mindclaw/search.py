"""
mindclaw.search — Hybrid search: BM25 + Ollama semantic embeddings.

Search layers (combined automatically when available):
  1. BM25    — always on, zero deps, superior to TF-IDF for recall/precision
  2. Ollama  — optional semantic layer via local Ollama (stdlib HTTP only)

Post-processing (opt-in):
  3. Temporal decay  — recency boost: score × e^(-λ × ageInDays)
  4. MMR re-ranking  — diversity filter (Maximal Marginal Relevance)

Compatible with OpenClaw's hybrid BM25+vector approach.
"""

from __future__ import annotations

import json
import math
import re
import struct
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from typing import Any, Optional

from .store import Memory, MemoryStore


# ===========================================================================
# Tokenizer
# ===========================================================================

_SPLIT_RE = re.compile(r"[^a-z0-9]+")
_STOP_WORDS = frozenset(
    "a an the is are was were be been being have has had do does did "
    "will would shall should may might can could to of in for on with "
    "at by from as into through during about after before between "
    "and or but not no nor so yet both either neither each every all "
    "any few more most other some such that this these those it its "
    "i me my we our you your he him his she her they them their what "
    "which who whom how when where why if then else than too very".split()
)


def _tokenize(text: str) -> list[str]:
    """Lowercase tokenizer with stopword removal."""
    tokens = _SPLIT_RE.split(text.lower())
    return [t for t in tokens if len(t) > 1 and t not in _STOP_WORDS]


def _jaccard(m1: Memory, m2: Memory) -> float:
    """Jaccard similarity between two memories on content tokens."""
    t1 = set(_tokenize(m1.content))
    t2 = set(_tokenize(m2.content))
    if not t1 and not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)


# ===========================================================================
# Layer 1: BM25 Index (zero dependencies — replaces TF-IDF)
# ===========================================================================

class BM25Index:
    """
    Okapi BM25 full-text index.
    Superior to TF-IDF for short documents: normalises for doc length and
    applies saturating term-frequency. Matches OpenClaw's BM25 approach.
    k1=1.5, b=0.75 are the standard defaults.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._doc_tokens: dict[str, list[str]] = {}
        self._idf: dict[str, float] = {}
        self._avgdl: float = 0.0
        self._doc_count: int = 0

    def build(self, memories: list[Memory]) -> None:
        """Build the BM25 index from a list of memories."""
        self._doc_tokens.clear()
        self._idf.clear()
        self._doc_count = len(memories)

        if not memories:
            return

        df: dict[str, int] = defaultdict(int)
        for mem in memories:
            text = f"{mem.content} {mem.summary} {' '.join(mem.tags)}"
            tokens = _tokenize(text)
            self._doc_tokens[mem.id] = tokens
            for t in set(tokens):
                df[t] += 1

        total_len = sum(len(t) for t in self._doc_tokens.values())
        self._avgdl = total_len / max(1, self._doc_count)

        n = self._doc_count
        for term, cnt in df.items():
            # BM25 IDF: log((N - df + 0.5) / (df + 0.5) + 1)
            self._idf[term] = math.log((n - cnt + 0.5) / (cnt + 0.5) + 1)

    def score(self, memory_id: str, query_tokens: list[str]) -> float:
        """Compute BM25 score for a single document."""
        if memory_id not in self._doc_tokens:
            return 0.0
        doc_tokens = self._doc_tokens[memory_id]
        dl = len(doc_tokens)
        tf_count = Counter(doc_tokens)
        total = 0.0
        for t in query_tokens:
            if t not in self._idf:
                continue
            tf = tf_count.get(t, 0)
            numer = tf * (self.k1 + 1)
            denom = tf + self.k1 * (1 - self.b + self.b * dl / max(1, self._avgdl))
            total += self._idf[t] * (numer / denom)
        return total

    def search(self, query: str, *, top_k: int = 10) -> list[tuple[str, float]]:
        """Search the index. Returns [(memory_id, score)] sorted desc."""
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []
        scores = [(mid, self.score(mid, query_tokens)) for mid in self._doc_tokens]
        scores.sort(key=lambda x: -x[1])
        return [(mid, s) for mid, s in scores[:top_k] if s > 0]

    def to_vector(self, text: str) -> bytes:
        """Encode text as a sparse BM25 vector (bytes) for the embeddings cache."""
        tokens = _tokenize(text)
        counter = Counter(tokens)
        total = len(tokens) if tokens else 1
        components: list[tuple[int, float]] = []
        for term, count in counter.items():
            tf = count / total
            idf = self._idf.get(term, 1.0)
            h = hash(term) & 0xFFFFFFFF
            components.append((h, tf * idf))
        components.sort(key=lambda x: x[0])
        return struct.pack(
            f"<{len(components) * 2}f",
            *[x for h, val in components for x in (float(h), val)],
        )


# ===========================================================================
# Layer 2: Ollama semantic embeddings (optional — zero new deps)
# ===========================================================================

class OllamaEmbedder:
    """
    Semantic embeddings via a local Ollama instance.
    Uses only Python stdlib (urllib) — no extra packages required.
    Falls back silently if Ollama is not running.

    Compatible with the same Ollama installation OpenClaw users already have.
    Default model: nomic-embed-text (768-dim, runs on CPU, ~274 MB).
    """

    def __init__(
        self,
        model: str = "nomic-embed-text",
        base_url: str = "http://localhost:11434",
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._available: Optional[bool] = None

    @property
    def available(self) -> bool:
        """Check if Ollama is reachable (result is cached after first call)."""
        if self._available is None:
            try:
                req = urllib.request.urlopen(f"{self.base_url}/api/tags", timeout=2)
                self._available = req.status == 200
            except Exception:
                self._available = False
        return self._available

    def reset(self) -> None:
        """Reset availability cache (useful after Ollama restarts)."""
        self._available = None

    def embed(self, text: str) -> Optional[list[float]]:
        """Request an embedding from Ollama. Returns None on any failure."""
        if not self.available:
            return None
        try:
            data = json.dumps({"model": self.model, "prompt": text}).encode()
            req = urllib.request.Request(
                f"{self.base_url}/api/embeddings",
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
                return result.get("embedding")
        except Exception:
            return None

    @staticmethod
    def cosine(a: list[float], b: list[float]) -> float:
        """Cosine similarity between two float vectors."""
        if not a or not b:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)


# ===========================================================================
# Post-processing: temporal decay + MMR diversity
# ===========================================================================

def _temporal_decay(score: float, created_at: float, halflife_days: float = 30.0) -> float:
    """
    Apply exponential temporal decay — mirrors OpenClaw's recency boost.
      decayedScore = score × e^(-λ × ageInDays)
      where λ = ln(2) / halfLifeDays
    Pinned memories should bypass this (checked by caller).
    """
    age_days = (time.time() - created_at) / 86400.0
    lam = math.log(2) / max(1, halflife_days)
    return score * math.exp(-lam * age_days)


def _mmr_rerank(
    candidates: list[tuple[Memory, float]],
    *,
    lambda_: float = 0.7,
    top_k: int = 10,
) -> list[tuple[Memory, float]]:
    """
    Maximal Marginal Relevance re-ranking — mirrors OpenClaw's MMR.
    Iteratively picks the result that maximises:
      λ × relevance − (1−λ) × max_similarity_to_already_selected
    λ=1.0 → pure relevance;  λ=0.0 → maximum diversity.
    """
    if not candidates:
        return []
    selected: list[tuple[Memory, float]] = []
    remaining = list(candidates)

    while remaining and len(selected) < top_k:
        if not selected:
            best = max(remaining, key=lambda x: x[1])
        else:
            def _mmr(c: tuple[Memory, float]) -> float:
                rel = c[1]
                max_sim = max(_jaccard(c[0], s[0]) for s in selected)
                return lambda_ * rel - (1 - lambda_) * max_sim
            best = max(remaining, key=_mmr)
        selected.append(best)
        remaining.remove(best)

    return selected


# ===========================================================================
# Backwards compat stub (was SemanticIndex / ONNX)
# ===========================================================================

class _NoopSemantic:
    """Stub replacing old SemanticIndex. ONNX path removed; use Ollama instead."""

    available = False

    def encode(self, texts: list[str]) -> None:  # noqa: ARG002
        return None

    def cosine_similarity(self, a: Any, b: Any) -> float:  # noqa: ARG002
        return 0.0


# Alias so any code that imported SemanticIndex still works
SemanticIndex = _NoopSemantic


# ===========================================================================
# Unified Search Interface
# ===========================================================================

class SearchEngine:
    """
    Unified hybrid search: BM25 (always) + Ollama semantic (optional).
    Post-processing: temporal decay + MMR diversity re-ranking.

    Mirrors OpenClaw's hybrid BM25+vector pipeline with the same
    post-processing options (temporal decay, MMR) so MindClaw results
    are consistent with what OpenClaw's memory_search would return.

    Usage:
        engine = SearchEngine(store)
        engine.rebuild()
        results = engine.search("payment API issue", temporal_decay=True, mmr=True)
    """

    def __init__(self, store: MemoryStore) -> None:
        self.store = store
        self.bm25 = BM25Index()
        self.ollama = OllamaEmbedder()
        self._memories_cache: dict[str, Memory] = {}
        # Backwards-compat alias
        self.semantic = _NoopSemantic()
        # Backwards-compat alias (old attribute name)
        self.tfidf = self.bm25

    def rebuild(self) -> dict[str, Any]:
        """Rebuild the search index from all active memories."""
        memories = self.store.list_memories(limit=10_000, include_archived=False)
        self._memories_cache = {m.id: m for m in memories}
        self.bm25.build(memories)

        # Cache BM25 vectors in the store
        for mem in memories:
            text = f"{mem.content} {mem.summary} {' '.join(mem.tags)}"
            vec = self.bm25.to_vector(text)
            self.store.save_embedding(mem.id, vec, model="bm25")

        return {
            "indexed": len(memories),
            "bm25": True,
            "semantic_available": self.ollama.available,
            "semantic_model": self.ollama.model if self.ollama.available else None,
        }

    def search(
        self,
        query: str,
        *,
        top_k: int = 10,
        boost_importance: bool = True,
        temporal_decay: bool = False,
        temporal_halflife: float = 30.0,
        mmr: bool = False,
        mmr_lambda: float = 0.7,
        agent_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """
        Hybrid memory search.

        Parameters
        ----------
        query             : natural-language search string
        top_k             : max results to return
        boost_importance  : multiply raw score by (0.5 + importance)
        temporal_decay    : apply exponential recency decay (pinned memories exempt)
        temporal_halflife : half-life in days (default 30 — score halves every month)
        mmr               : apply MMR re-ranking to reduce near-duplicate results
        mmr_lambda        : MMR λ — 1.0=pure relevance, 0.0=maximum diversity
        agent_id          : filter to a specific agent namespace

        Returns list of {memory, score, method} dicts.
        """
        # --- BM25 pass ---
        bm25_hits = self.bm25.search(query, top_k=top_k * 3)

        # --- Ollama semantic pass (if running) ---
        sem_scores: dict[str, float] = {}
        query_vec = self.ollama.embed(query) if self.ollama.available else None
        if query_vec is not None:
            for mid, mem in self._memories_cache.items():
                if agent_id and mem.agent_id != agent_id:
                    continue
                mem_vec = self.ollama.embed(mem.content)
                if mem_vec:
                    sem_scores[mid] = OllamaEmbedder.cosine(query_vec, mem_vec)

        # --- Weighted merge (70% BM25 + 30% semantic) ---
        bm25_max = max((s for _, s in bm25_hits), default=1.0) or 1.0
        merged: dict[str, float] = {}
        for mid, s in bm25_hits:
            merged[mid] = 0.7 * (s / bm25_max)
        for mid, s in sem_scores.items():
            merged[mid] = merged.get(mid, 0.0) + 0.3 * s

        method = "bm25+semantic" if sem_scores else "bm25"

        # --- Build result list ---
        results: list[dict[str, Any]] = []
        for mid, raw_score in merged.items():
            mem = self._memories_cache.get(mid) or self.store.get(mid)
            if mem is None or mem.archived:
                continue
            if agent_id and mem.agent_id != agent_id:
                continue
            score = raw_score
            if boost_importance:
                score *= 0.5 + mem.importance
            if temporal_decay and not mem.pinned:
                score = _temporal_decay(score, mem.created_at, temporal_halflife)
            results.append({"memory": mem, "score": round(score, 4), "method": method})

        results.sort(key=lambda x: -x["score"])
        candidates = results[: top_k * 2]

        if mmr and len(candidates) > 1:
            pairs = [(r["memory"], r["score"]) for r in candidates]
            reranked = _mmr_rerank(pairs, lambda_=mmr_lambda, top_k=top_k)
            mem_to_result = {r["memory"].id: r for r in candidates}
            return [mem_to_result[m.id] for m, _ in reranked if m.id in mem_to_result]

        return candidates[:top_k]

    def similar(self, memory_id: str, *, top_k: int = 5) -> list[dict[str, Any]]:
        """Find memories similar to a given memory."""
        mem = self.store.get(memory_id)
        if mem is None:
            return []
        query = f"{mem.content} {mem.summary}"
        results = self.search(query, top_k=top_k + 1)
        return [r for r in results if r["memory"].id != memory_id][:top_k]

