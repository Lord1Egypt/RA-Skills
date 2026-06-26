#!/usr/bin/env python3
"""
Memory Cascade — Auto-escalating search across all storage tiers.

Instead of the agent deciding "should I grep or search LanceDB?", the cascade
tries each tier from fastest to slowest and stops when it finds a good answer.

Tiers (in order, fastest to slowest):
  T0: in-memory session cache         <1ms     (hot lookups, normalized keys)
  T1: JSON state files                <5ms     (exact key match)
  T2: SQLite pipeline_synergy.db      <5ms     (structured query)
  T3: SQLite keyword (quality_scores) <1ms     (multi-word LIKE on 22K rows)
  T4: Grep over 46K chunks            ~3000ms  (brute force ripgrep)
  T5: LanceDB keyword (670K vectors)  slow     (BM25, no embeddings)
  T5b: LanceDB semantic (670K vectors) ~3-30s  (embedding similarity — fallback)

Question queries (how/what/why/...) skip keyword tiers and route directly
to semantic search after T0 cache check. T5b semantic is also forced as
a last-resort fallback whenever confidence remains below threshold.

The cascade records which tier answered and how fast, feeding self-tuning
back to memory_router.py.

Usage:
    from tools.memory.memory_cascade import recall, store

    # Recall: finds the best answer across all tiers
    result = recall("adaptive alpha reranking")
    # → {"answer": "...", "tier": "T5:lancedb", "latency_ms": 340, "confidence": 0.87}

    # Store: routes to the right tier automatically
    store("pattern", content="...", tags=["ml", "reranking"])
    # → writes to docs/patterns/ (staging)

CLI:
    python tools/memory_cascade.py recall "query here"
    python tools/memory_cascade.py stats
"""

import json
import re
import sqlite3
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DB_PATH = ROOT / "knowledge" / "SYSTEM" / "pipeline_synergy.db"
SYSTEM_DIR = ROOT / "knowledge" / "SYSTEM"
CASCADE_STATS_PATH = SYSTEM_DIR / "cascade_stats.json"

# Session cache (T0) — shared across calls within one process
_session_cache: dict[str, dict] = {}
_CACHE_LOCK = threading.Lock()
_STATS_LOCK = threading.Lock()
_JSONL_LOCK = threading.Lock()

# Question patterns — queries that are semantic in nature and poor for keyword matching
_QUESTION_PREFIXES = re.compile(
    r"^\s*(how|what|why|when|where|which|can|should|is|are|does|do|will|could|would)\b",
    re.IGNORECASE,
)


def _is_question_query(query: str) -> bool:
    """Detect if a query is a natural-language question (poor for keyword search)."""
    return bool(_QUESTION_PREFIXES.match(query)) or "?" in query


def _normalize_cache_key(query: str) -> str:
    """Normalize query for T0 cache: lowercase, strip punctuation, collapse whitespace."""
    key = query.strip().lower()
    key = re.sub(r"[^\w\s]", "", key)  # strip punctuation
    key = re.sub(r"\s+", " ", key).strip()  # collapse whitespace
    return key


def jsonl_append(path: Path, entry: str):
    """Thread-safe + OS-level locked JSONL line append.

    Uses msvcrt.locking (Windows) or fcntl.flock (Unix) to prevent
    interleaved writes from concurrent processes/threads.
    """
    import os

    path.parent.mkdir(parents=True, exist_ok=True)
    line = entry if entry.endswith("\n") else entry + "\n"

    with _JSONL_LOCK:  # thread-level lock
        fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        try:
            # OS-level lock for cross-process safety
            if sys.platform == "win32":
                import msvcrt

                msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
                try:
                    os.write(fd, line.encode("utf-8"))
                finally:
                    try:
                        os.lseek(fd, -len(line.encode("utf-8")), os.SEEK_CUR)
                        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                    except Exception:
                        pass
            else:
                import fcntl

                fcntl.flock(fd, fcntl.LOCK_EX)
                try:
                    os.write(fd, line.encode("utf-8"))
                finally:
                    fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


# ═══════════════════════════════════════════════════════════════
# TIER 0: IN-MEMORY SESSION CACHE
# ═══════════════════════════════════════════════════════════════


def _t0_lookup(query: str) -> dict | None:
    """Exact match in session cache. <1us. Uses normalized key for better hit rate."""
    key = _normalize_cache_key(query)
    with _CACHE_LOCK:
        if key in _session_cache:
            return _session_cache[key]
        # Fuzzy: check if query is substring of any cached key
        # Snapshot items to avoid RuntimeError on concurrent mutation
        for k, v in list(_session_cache.items()):
            if key in k or k in key:
                return v
    return None


def _t0_store(query: str, result: dict):
    """Cache a result for session-local reuse. Uses normalized key."""
    key = _normalize_cache_key(query)
    with _CACHE_LOCK:
        _session_cache[key] = result
        # Evict oldest if too large
        if len(_session_cache) > 500:
            oldest = next(iter(_session_cache))
            del _session_cache[oldest]


# ═══════════════════════════════════════════════════════════════
# TIER 1: JSON STATE FILES
# ═══════════════════════════════════════════════════════════════


def _t1_lookup(query: str) -> dict | None:
    """Search JSON state files for key or filename match. ~67us per file."""
    q_lower = query.strip().lower()
    tokens = set(t for t in q_lower.split() if len(t) > 2)

    # Only check files whose names match query tokens
    for json_file in SYSTEM_DIR.glob("*.json"):
        fname = json_file.stem.lower()
        fname_tokens = set(fname.split("_"))
        overlap = tokens & fname_tokens
        name_match = any(t in fname for t in tokens) or any(
            t in q_lower for t in fname_tokens if len(t) > 2
        )

        if not name_match:
            continue

        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue

            # If filename strongly matches query, return top-level summary
            if overlap or fname in q_lower or q_lower in fname:
                summary = {}
                for k, v in list(data.items())[:8]:
                    if isinstance(v, (str, int, float, bool)):
                        summary[k] = v
                    elif isinstance(v, (dict, list)):
                        summary[k] = f"[{type(v).__name__}:{len(v)}]"
                return {
                    "source": f"json:{json_file.name}",
                    "key": fname,
                    "value": json.dumps(summary, default=str)[:500],
                    "tier": "T1:json_state",
                }

            # Deeper: check if any top-level key matches
            for k, v in data.items():
                if q_lower in k.lower() or any(t in k.lower() for t in tokens):
                    return {
                        "source": f"json:{json_file.name}",
                        "key": k,
                        "value": (
                            v
                            if not isinstance(v, (dict, list))
                            else json.dumps(v)[:500]
                        ),
                        "tier": "T1:json_state",
                    }
        except (json.JSONDecodeError, OSError):
            pass
    return None


# ═══════════════════════════════════════════════════════════════
# TIER 2: SQLITE STRUCTURED QUERY
# ═══════════════════════════════════════════════════════════════


def _t2_lookup(query: str) -> dict | None:
    """Search SQLite for matching chunks/scores/events. ~700us."""
    if not DB_PATH.exists():
        return None

    q_lower = query.strip().lower()
    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    try:
        # Search quality_scores by chunk_name
        row = conn.execute(
            "SELECT chunk_name, score_total, chunk_path FROM quality_scores "
            "WHERE chunk_name LIKE ? ORDER BY score_total DESC LIMIT 1",
            (f"%{q_lower.replace(' ', '%')}%",),
        ).fetchone()
        if row:
            return {
                "source": f"sqlite:quality_scores",
                "chunk_name": row["chunk_name"],
                "score": row["score_total"],
                "path": row["chunk_path"],
                "tier": "T2:sqlite",
            }

        # Search retrieval_events by query
        row = conn.execute(
            "SELECT query, chunk_name, score, method FROM retrieval_events "
            "WHERE query LIKE ? ORDER BY retrieved_at DESC LIMIT 1",
            (f"%{q_lower[:50]}%",),
        ).fetchone()
        if row:
            return {
                "source": "sqlite:retrieval_events",
                "matched_query": row["query"],
                "chunk_name": row["chunk_name"],
                "score": row["score"],
                "tier": "T2:sqlite",
            }
    except Exception:
        pass
    finally:
        conn.close()
    return None


# ═══════════════════════════════════════════════════════════════
# TIER 3: LANCEDB VECTOR SEARCH
# ═══════════════════════════════════════════════════════════════


def _t3_lookup(query: str, top_k: int = 3) -> dict | None:
    """LanceDB keyword search (BM25, no embeddings, no cross-encoder).

    Hybrid/semantic modes require Gemini API call (~3-30s) + optional
    cross-encoder BERT load (~5s). For a cascade tier that needs to answer
    in <2s, keyword-only is the right trade-off. Semantic search is still
    available via the MCP server and explicit search tools.
    """
    try:
        from hive_commons.vector_store import search_memory

        results = search_memory(query, top_k=top_k, search_mode="keyword", rerank=False)
        if results:
            best = results[0]
            return {
                "source": f"lancedb:{best.get('source', 'unknown')}",
                "file": best.get("file", Path(best.get("source", "unknown")).name),
                "text": best.get("text", "")[:800],
                "score": best.get("score", 0),
                "n_results": len(results),
                "tier": "T5:lancedb",
                "all_sources": [r.get("source", "") for r in results[:5]],
            }
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════════════════
# TIER 5B: LANCEDB SEMANTIC SEARCH (embeddings, true vector similarity)
# ═══════════════════════════════════════════════════════════════


def _t5_semantic_lookup(query: str, top_k: int = 5) -> dict | None:
    """LanceDB semantic search using embeddings. Slower (~3-30s) but finds
    answers that keyword matching misses entirely.

    This is the ultimate fallback — if keyword tiers all fail, semantic
    similarity over 670K vectors will likely find something relevant.
    """
    try:
        from hive_commons.vector_store import search_memory

        results = search_memory(query, top_k=top_k, search_mode="hybrid", rerank=False)
        if results:
            best = results[0]
            return {
                "source": f"lancedb_semantic:{best.get('source', 'unknown')}",
                "file": best.get("file", Path(best.get("source", "unknown")).name),
                "text": best.get("text", "")[:800],
                "score": best.get("score", 0),
                "n_results": len(results),
                "tier": "T5:lancedb_semantic",
                "all_sources": [r.get("source", "") for r in results[:5]],
            }
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════════════════
# TIER 4: GREP BRUTE FORCE
# ═══════════════════════════════════════════════════════════════


def _t4_lookup(query: str) -> dict | None:
    """Grep across all chunks. ~7000ms. Last resort."""
    import subprocess

    # Use first 3 significant words for grep
    words = [w for w in query.split() if len(w) > 3][:3]
    if not words:
        return None

    pattern = ".*".join(words)
    try:
        result = subprocess.run(
            ["grep", "-rl", "-i", pattern, "knowledge/chunks/"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=15,
        )
        files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        if files:
            # Read snippet from first match
            first = ROOT / files[0]
            if first.exists():
                content = first.read_text(encoding="utf-8", errors="replace")[:500]
                return {
                    "source": f"grep:{files[0]}",
                    "file": Path(files[0]).name,
                    "snippet": content,
                    "n_matches": len(files),
                    "tier": "T4:grep",
                    "matched_files": files[:5],
                }
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════════════════
# TIER 5: MCP MEMORY (graph memory — curated, verified relations)
# ═══════════════════════════════════════════════════════════════


def _t5_mcp_lookup(query: str) -> dict | None:
    """SQLite FTS5 full-text search over pipeline_synergy.db. <100ms.

    Searches the quality_scores table (chunk_name + chunk_path) and
    retrieval_events (query log). FTS5 is sub-second even on large DBs.
    This complements T2 (exact SQL LIKE) with proper full-text ranking.
    """
    if not DB_PATH.exists():
        return None

    words = [w for w in query.split() if len(w) > 2][:5]
    if not words:
        return None

    conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=3000")
    conn.row_factory = sqlite3.Row

    try:
        # Try FTS5 if available
        fts_query = " OR ".join(words)
        try:
            rows = conn.execute(
                "SELECT chunk_name, score_total, chunk_path FROM quality_scores "
                "WHERE chunk_name MATCH ? ORDER BY score_total DESC LIMIT 3",
                (fts_query,),
            ).fetchall()
            if rows:
                return {
                    "source": f"sqlite_fts:{rows[0]['chunk_name']}",
                    "chunk_name": rows[0]["chunk_name"],
                    "score": rows[0]["score_total"],
                    "path": rows[0]["chunk_path"],
                    "n_results": len(rows),
                    "tier": "T3:sqlite_fts",
                }
        except Exception:
            pass  # FTS5 not available, fallback to multi-word LIKE

        # Fallback: OR-style LIKE across chunk_name AND chunk_path
        name_conds = " OR ".join(["chunk_name LIKE ?"] * len(words))
        path_conds = " OR ".join(["chunk_path LIKE ?"] * len(words))
        params = [f"%{w}%" for w in words]
        all_params = params + params  # once for name, once for path
        row = conn.execute(
            f"SELECT chunk_name, score_total, chunk_path FROM quality_scores "
            f"WHERE ({name_conds}) OR ({path_conds}) ORDER BY score_total DESC LIMIT 1",
            all_params,
        ).fetchone()
        if row:
            return {
                "source": f"sqlite_multi:{row['chunk_name']}",
                "chunk_name": row["chunk_name"],
                "score": row["score_total"],
                "path": row["chunk_path"],
                "tier": "T3:sqlite_fts",
            }
    except Exception:
        pass
    finally:
        conn.close()
    return None


def _t5_mcp_store(query: str, content: str, tags: list | None = None):
    """No-op: actual persistence is the filesystem write that triggered this.

    The cascade auto-store fires when EUREKA/truth/SOTA files are written.
    The file IS the store. LanceDB indexes it on next vector index run.
    """
    pass


# ═══════════════════════════════════════════════════════════════
# CASCADE ENGINE
# ═══════════════════════════════════════════════════════════════

_TIERS = [
    ("T0:session_cache", _t0_lookup),  # <1ms — in-memory dict
    ("T1:json_state", _t1_lookup),  # <5ms — JSON file key match
    ("T2:sqlite", _t2_lookup),  # <5ms — structured SQL match
    ("T3:sqlite_fts", _t5_mcp_lookup),  # <1ms — keyword LIKE on 22K rows
    ("T4:grep", _t4_lookup),  # ~3s  — brute force ripgrep
    ("T5:lancedb", _t3_lookup),  # slow — LanceDB keyword (670K rows)
    ("T5:lancedb_semantic", _t5_semantic_lookup),  # ~3-30s — embedding similarity
]

# Question-optimized tiers: skip keyword tiers, go straight to semantic
_QUESTION_TIERS = [
    ("T0:session_cache", _t0_lookup),  # <1ms — check cache first
    ("T5:lancedb", _t3_lookup),  # keyword over vectors (fast)
    ("T5:lancedb_semantic", _t5_semantic_lookup),  # semantic (best for questions)
    ("T2:sqlite", _t2_lookup),  # structured fallback
    ("T3:sqlite_fts", _t5_mcp_lookup),  # FTS fallback
]

# Confidence thresholds — stop escalating if confidence is high enough
_CONFIDENCE = {
    "T0:session_cache": 1.0,  # exact match, trust it
    "T1:json_state": 0.9,  # structured key match
    "T2:sqlite": 0.55,  # SQL LIKE match — lowered to allow escalation
    "T3:sqlite_fts": 0.6,  # keyword match on scored chunks
    "T4:grep": 0.4,  # brute force, lowest confidence
    "T5:lancedb": 0.65,  # keyword search over 670K vectors
    "T5:lancedb_semantic": 0.8,  # embedding similarity — high trust
}

# Learned shortcuts: query pattern → tier that usually resolves it
# Loaded from cascade_stats.json at module init, updated by evolve()
_SHORTCUTS: dict[str, str] = {}  # pattern → tier_name
_TIER_SKIP: set[str] = set()  # tiers to skip (0% hit for certain patterns)


def _load_shortcuts():
    """Load learned shortcuts from cascade_stats.json."""
    global _SHORTCUTS, _TIER_SKIP
    try:
        if CASCADE_STATS_PATH.exists():
            stats = json.loads(CASCADE_STATS_PATH.read_text(encoding="utf-8"))
            _SHORTCUTS = stats.get("shortcuts", {})
            _TIER_SKIP = set(stats.get("tier_skip", []))
    except Exception:
        pass


# Load on import
_load_shortcuts()


def _estimate_confidence(result: dict, query: str) -> float:
    """Estimate how well the result answers the query.

    Formula: base_confidence * (floor + term_overlap * 0.50 + score_bonus * 0.20)
    The floor is low (0.15) so that results with NO term overlap get penalized
    heavily, forcing the cascade to keep escalating to semantic search.

    A perfect keyword match: base * (0.15 + 0.50 + 0.20) = base * 0.85
    Zero overlap, zero score: base * 0.15 (forces escalation)
    Half term match, some score: base * (0.15 + 0.25 + 0.10) = base * 0.50
    """
    if not result:
        return 0.0

    tier = result.get("tier", "")
    base = _CONFIDENCE.get(tier, 0.5)

    # Term overlap: fraction of query words (len>2) found in result
    q_terms = {t for t in query.lower().split() if len(t) > 2}
    result_text = json.dumps(result, default=str).lower()
    term_hits = sum(1 for t in q_terms if t in result_text)
    term_ratio = term_hits / max(len(q_terms), 1)

    # Score from the result itself — normalize from various scales
    score = result.get("score", 0)
    if isinstance(score, (int, float)) and score > 0:
        # Scores can be 0-100 (quality_scores) or 0-1 (LanceDB similarity)
        if score <= 1.0:
            score_bonus = score  # already normalized
        elif score <= 100:
            score_bonus = score / 100  # quality score scale
        else:
            score_bonus = min(1.0, score / 1000)  # very large scores
    else:
        score_bonus = 0.0

    # Content richness: penalize results with very short text
    text = result.get("text", result.get("snippet", result.get("value", "")))
    if isinstance(text, str) and len(text) > 200:
        richness_bonus = 0.15
    elif isinstance(text, str) and len(text) > 50:
        richness_bonus = 0.08
    else:
        richness_bonus = 0.0

    # Multiplier: ranges 0.15 (no overlap, no score) to 1.0 (full match)
    quality = 0.15 + term_ratio * 0.50 + score_bonus * 0.20 + richness_bonus
    return min(1.0, base * min(quality, 1.0))


def _query_signature(query: str) -> str:
    """Extract a reusable pattern from a query for shortcut matching.

    Strips specifics, keeps structure: "how does X work" → "how_does_*_work"
    """
    q = query.strip().lower()
    # Replace quoted strings
    q = re.sub(r'"[^"]*"', "*", q)
    # Replace backtick content
    q = re.sub(r"`[^`]*`", "*", q)
    # Replace numbers
    q = re.sub(r"\d+", "#", q)
    # Collapse whitespace
    q = re.sub(r"\s+", "_", q)
    return q[:60]


def recall(query: str, min_confidence: float = 0.5, max_tier: int = 6) -> dict:
    """Cascading search across all memory tiers.

    Starts at T0 (fastest), escalates until confidence >= min_confidence
    or all tiers exhausted. Question-type queries skip keyword tiers and
    go straight to semantic search.

    Args:
        query: What to find.
        min_confidence: Stop when confidence reaches this (0.0-1.0).
        max_tier: Maximum tier index to try (0-6). Lower = faster but may miss.

    Returns:
        dict with: answer, tier, latency_ms, confidence, escalation_path
    """
    escalation = []
    best_result = None
    best_confidence = 0.0
    total_t0 = time.perf_counter()
    shortcut_used = False
    is_question = _is_question_query(query)

    # Question-type queries use a different tier order: skip keyword tiers,
    # go straight to semantic search after T0 cache check
    base_tiers = _QUESTION_TIERS if is_question else _TIERS

    # Check learned shortcuts: if this query pattern resolved at a specific
    # tier before, try that tier FIRST (skip lower tiers)
    sig = _query_signature(query)
    preferred_tier = _SHORTCUTS.get(sig)

    tiers_to_try = list(enumerate(base_tiers))

    if preferred_tier:
        # Reorder: try shortcut tier first, then normal order
        shortcut_idx = next(
            (i for i, (name, _) in enumerate(base_tiers) if name == preferred_tier),
            None,
        )
        if shortcut_idx is not None:
            tiers_to_try = [(shortcut_idx, base_tiers[shortcut_idx])] + [
                (i, t) for i, t in enumerate(base_tiers) if i != shortcut_idx
            ]
            shortcut_used = True

    for i, (tier_name, tier_fn) in tiers_to_try:
        if i > max_tier:
            continue

        # Skip tiers marked as dead for this query type
        if tier_name in _TIER_SKIP and not shortcut_used:
            escalation.append(
                {
                    "tier": tier_name,
                    "found": False,
                    "latency_ms": 0,
                    "skipped": True,
                }
            )
            continue

        t0 = time.perf_counter()
        try:
            result = tier_fn(query)
        except Exception:
            result = None
        latency_ms = (time.perf_counter() - t0) * 1000

        if result:
            confidence = _estimate_confidence(result, query)
            escalation.append(
                {
                    "tier": tier_name,
                    "found": True,
                    "confidence": round(confidence, 3),
                    "latency_ms": round(latency_ms, 2),
                }
            )
            if confidence > best_confidence:
                best_result = result
                best_confidence = confidence

            # Stop if confident enough
            if confidence >= min_confidence:
                break
        else:
            escalation.append(
                {
                    "tier": tier_name,
                    "found": False,
                    "latency_ms": round(latency_ms, 2),
                }
            )

    # SEMANTIC FALLBACK: if all tiers failed or confidence is still low,
    # force T5 semantic search as last resort (unless already tried)
    already_tried_semantic = any(e["tier"] == "T5:lancedb_semantic" for e in escalation)
    if best_confidence < min_confidence and not already_tried_semantic:
        t0 = time.perf_counter()
        try:
            result = _t5_semantic_lookup(query)
        except Exception:
            result = None
        latency_ms = (time.perf_counter() - t0) * 1000

        if result:
            confidence = _estimate_confidence(result, query)
            escalation.append(
                {
                    "tier": "T5:lancedb_semantic",
                    "found": True,
                    "confidence": round(confidence, 3),
                    "latency_ms": round(latency_ms, 2),
                    "forced_fallback": True,
                }
            )
            if confidence > best_confidence:
                best_result = result
                best_confidence = confidence
        else:
            escalation.append(
                {
                    "tier": "T5:lancedb_semantic",
                    "found": False,
                    "latency_ms": round(latency_ms, 2),
                    "forced_fallback": True,
                }
            )

    total_ms = (time.perf_counter() - total_t0) * 1000

    # Cache the result for T0 reuse
    if best_result:
        _t0_store(query, best_result)

    # Record stats + learn from this cascade
    _record_cascade(query, escalation, best_confidence, total_ms)

    return {
        "answer": best_result,
        "confidence": round(best_confidence, 3),
        "latency_ms": round(total_ms, 2),
        "tiers_tried": len([e for e in escalation if not e.get("skipped")]),
        "resolved_at": best_result.get("tier", "none") if best_result else "none",
        "shortcut": preferred_tier if shortcut_used else None,
        "question_routed": is_question,
        "escalation": escalation,
    }


def _record_cascade(query: str, escalation: list, confidence: float, total_ms: float):
    """Record cascade stats for self-tuning. Thread-safe via _STATS_LOCK."""
    try:
        with _STATS_LOCK:
            stats = {}
            if CASCADE_STATS_PATH.exists():
                stats = json.loads(CASCADE_STATS_PATH.read_text(encoding="utf-8"))

            if "cascades" not in stats:
                stats["cascades"] = {
                    "total": 0,
                    "by_tier": {},
                    "avg_ms": 0,
                    "avg_confidence": 0,
                }

            c = stats["cascades"]
            c["total"] += 1

            # Find where it actually resolved (not skipped, had a hit)
            resolved = "none"
            for e in escalation:
                if e.get("found") and not e.get("skipped"):
                    resolved = e["tier"]
            c["by_tier"][resolved] = c["by_tier"].get(resolved, 0) + 1

            # Running average
            n = c["total"]
            c["avg_ms"] = round(c["avg_ms"] * (n - 1) / n + total_ms / n, 2)
            c["avg_confidence"] = round(
                c["avg_confidence"] * (n - 1) / n + confidence / n, 3
            )

            # Track tier resolution distribution
            total = sum(c["by_tier"].values())
            c["tier_pct"] = {
                k: round(v / total * 100, 1) for k, v in c["by_tier"].items()
            }

            # Track query signature → tier resolution for shortcut learning
            sig = _query_signature(query)
            sig_map = stats.setdefault("sig_resolutions", {})
            if sig not in sig_map:
                sig_map[sig] = {}
            sig_map[sig][resolved] = sig_map[sig].get(resolved, 0) + 1

            # Limit sig_map growth: keep only top 200 by total count
            if len(sig_map) > 250:
                by_count = sorted(
                    sig_map.items(), key=lambda x: sum(x[1].values()), reverse=True
                )
                stats["sig_resolutions"] = dict(by_count[:200])

            CASCADE_STATS_PATH.write_text(
                json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8"
            )
    except Exception:
        pass  # stats are nice-to-have, never block


def evolve() -> dict:
    """Self-evolution: learn shortcuts and tier skips from cascade history.

    Analyzes sig_resolutions to find patterns:
    - If a query signature ALWAYS resolves at the same tier (>=5 times),
      create a shortcut to skip directly to that tier.
    - If a tier has 0% hits across all recent cascades, mark it for skip.

    Returns:
        dict with: shortcuts_added, skips_added, shortcuts_total, skips_total
    """
    if not CASCADE_STATS_PATH.exists():
        return {"error": "no cascade data yet"}

    stats = json.loads(CASCADE_STATS_PATH.read_text(encoding="utf-8"))
    sig_map = stats.get("sig_resolutions", {})
    cascades = stats.get("cascades", {})

    shortcuts = stats.get("shortcuts", {})
    tier_skip = stats.get("tier_skip", [])

    added_shortcuts = 0
    added_skips = 0

    # Learn shortcuts: query pattern → tier
    for sig, tier_counts in sig_map.items():
        total = sum(tier_counts.values())
        if total < 3:
            continue
        # Find dominant tier
        dominant = max(tier_counts, key=tier_counts.get)
        dominance = tier_counts[dominant] / total
        if dominance >= 0.8 and dominant != "none":
            if sig not in shortcuts or shortcuts[sig] != dominant:
                shortcuts[sig] = dominant
                added_shortcuts += 1

    # Learn tier skips: only skip tiers that are expensive AND never resolve
    # Never skip cheap tiers (T1/T2 are <5ms, always worth trying)
    total_cascades = cascades.get("total", 0)
    if total_cascades >= 100:
        by_tier = cascades.get("by_tier", {})
        # Only consider skipping expensive tiers (T4:grep ~3s)
        for tier_name in ["T4:grep"]:
            hits = by_tier.get(tier_name, 0)
            if hits / total_cascades < 0.01 and tier_name not in tier_skip:
                tier_skip.append(tier_name)
                added_skips += 1

    # SAFETY: remove bad skips for cheap tiers that should never be skipped
    safe_tiers = {
        "T1:json_state",
        "T2:sqlite",
        "T3:sqlite_fts",
        "T5:lancedb",
        "T5:lancedb_semantic",
    }
    tier_skip = [t for t in tier_skip if t not in safe_tiers]

    # Learn write patterns: detect misroute trends
    write_insights = {}
    obs_writes = stats.get("observed_writes", {})
    if obs_writes.get("total", 0) >= 10:
        misroute_pct = obs_writes.get("misroute_pct", 0)
        write_insights["misroute_pct"] = misroute_pct
        write_insights["total_writes"] = obs_writes["total"]
        write_insights["top_store"] = max(
            obs_writes.get("by_store", {}),
            key=obs_writes["by_store"].get,
            default="none",
        )
        # If misroute rate is high, flag for attention
        if misroute_pct > 20:
            write_insights["alert"] = (
                f"High misroute rate: {misroute_pct}% of writes go to non-recommended stores"
            )

    # Save
    stats["shortcuts"] = shortcuts
    stats["tier_skip"] = tier_skip
    stats["write_insights"] = write_insights
    stats["last_evolve"] = time.time()
    CASCADE_STATS_PATH.write_text(
        json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Reload into memory
    _load_shortcuts()

    return {
        "shortcuts_added": added_shortcuts,
        "skips_added": added_skips,
        "shortcuts_total": len(shortcuts),
        "skips_total": len(tier_skip),
        "write_insights": write_insights,
    }


# ═══════════════════════════════════════════════════════════════
# STORE — route writes through memory_router
# ═══════════════════════════════════════════════════════════════


def store(data_type: str, content: str, **kwargs) -> dict:
    """Route a write to the right storage tier.

    Args:
        data_type: "state" | "pattern" | "knowledge" | "log" | "event"
        content: What to write.
        **kwargs: durability, searchable, tags, filename

    Returns:
        dict with: store, path, success
    """
    from tools.memory.memory_router import route as memory_route

    decision = memory_route(
        "write",
        data_type=data_type,
        durability=kwargs.get("durability", "permanent"),
        searchable=kwargs.get("searchable", False),
    )

    store_name = decision["store"]

    if store_name in ("docs_patterns", "chunks", "topic_files"):
        # File-based stores
        if store_name == "docs_patterns":
            target_dir = ROOT / "docs" / "patterns"
        elif store_name == "chunks":
            target_dir = ROOT / "knowledge" / "chunks"
        else:
            target_dir = Path(
                "C:/Users/Leandro/.claude/projects/D--Proyectos-1midos/memory"
            )

        target_dir.mkdir(parents=True, exist_ok=True)
        filename = kwargs.get("filename", f"{data_type}_{int(time.time())}.md")
        path = target_dir / filename
        path.write_text(content, encoding="utf-8")
        return {"store": store_name, "path": str(path), "success": True}

    elif store_name == "json_state":
        filename = kwargs.get("filename", f"{data_type}_state.json")
        path = SYSTEM_DIR / filename
        try:
            existing = (
                json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            )
        except (json.JSONDecodeError, OSError):
            existing = {}
        if isinstance(existing, dict):
            existing["_last_write"] = time.time()
            existing["data"] = content if len(content) < 10000 else content[:10000]
        path.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return {"store": store_name, "path": str(path), "success": True}

    elif store_name == "hook_state":
        state_dir = ROOT / "hooks" / "state"
        state_dir.mkdir(parents=True, exist_ok=True)
        filename = kwargs.get("filename", f"{data_type}_state.json")
        path = state_dir / filename
        path.write_text(
            json.dumps({"data": content, "ts": time.time()}, ensure_ascii=False),
            encoding="utf-8",
        )
        return {"store": store_name, "path": str(path), "success": True}

    elif store_name == "jsonl_logs":
        logs_dir = ROOT / "hooks" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        filename = kwargs.get("filename", f"{data_type}.jsonl")
        path = logs_dir / filename
        entry = json.dumps(
            {"data": content[:5000], "ts": time.time()}, ensure_ascii=False
        )
        jsonl_append(path, entry)
        return {"store": store_name, "path": str(path), "success": True}

    return {
        "store": store_name,
        "success": False,
        "reason": "store not implemented for writes",
    }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Memory Cascade")
    sub = parser.add_subparsers(dest="command")

    rec = sub.add_parser("recall", help="Cascading search")
    rec.add_argument("query", help="What to find")
    rec.add_argument("--max-tier", type=int, default=6, help="Max tier (0-6)")
    rec.add_argument("--min-confidence", type=float, default=0.5)

    sub.add_parser("stats", help="Cascade usage stats")
    sub.add_parser("evolve", help="Run self-evolution (learn shortcuts + skips)")

    args = parser.parse_args()

    if args.command == "recall":
        result = recall(
            args.query, min_confidence=args.min_confidence, max_tier=args.max_tier
        )
        print(f"Resolved at: {result['resolved_at']}")
        print(f"Confidence:  {result['confidence']}")
        print(f"Latency:     {result['latency_ms']:.1f}ms")
        print(f"Tiers tried: {result['tiers_tried']}")
        if result.get("shortcut"):
            print(f"Shortcut:    {result['shortcut']} (learned)")
        print(f"\nEscalation:")
        for e in result["escalation"]:
            if e.get("skipped"):
                status = "SKIPPED (learned)"
            elif e["found"]:
                status = f"HIT conf={e['confidence']}"
            else:
                status = "MISS"
            print(f"  {e['tier']:25s} {e['latency_ms']:>8.1f}ms  {status}")
        if result["answer"]:
            print(f"\nAnswer:")
            for k, v in result["answer"].items():
                val = str(v)[:120]
                print(f"  {k}: {val}")

    elif args.command == "stats":
        if CASCADE_STATS_PATH.exists():
            stats = json.loads(CASCADE_STATS_PATH.read_text(encoding="utf-8"))
            c = stats.get("cascades", {})
            print(f"Total cascades: {c.get('total', 0)}")
            print(f"Avg latency:    {c.get('avg_ms', 0):.1f}ms")
            print(f"Avg confidence: {c.get('avg_confidence', 0):.3f}")
            print(f"\nTier resolution:")
            for tier, pct in sorted(c.get("tier_pct", {}).items()):
                count = c.get("by_tier", {}).get(tier, 0)
                print(f"  {tier:25s} {pct:>5.1f}%  ({count} hits)")
            # Shortcuts
            sc = stats.get("shortcuts", {})
            if sc:
                print(f"\nLearned shortcuts: {len(sc)}")
                for sig, tier in list(sc.items())[:10]:
                    print(f"  {sig:40s} -> {tier}")
            sk = stats.get("tier_skip", [])
            if sk:
                print(f"\nTier skips: {sk}")
            # Observed accesses
            obs = stats.get("observed_accesses", {})
            if obs.get("total"):
                print(f"\nObserved accesses (from agent): {obs['total']}")
                for tier, pct in sorted(obs.get("tier_pct", {}).items()):
                    print(f"  {tier}  {pct}%")
        else:
            print("No cascade data yet.")

    elif args.command == "evolve":
        result = evolve()
        if "error" in result:
            print(result["error"])
        else:
            print(
                f"Shortcuts added: {result['shortcuts_added']} (total: {result['shortcuts_total']})"
            )
            print(
                f"Skips added:     {result['skips_added']} (total: {result['skips_total']})"
            )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
