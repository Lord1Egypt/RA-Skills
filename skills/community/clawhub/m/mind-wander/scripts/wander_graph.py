"""
wander_graph.py — The wander agent's private knowledge graph.

Uses FalkorDB `wander` graph (separate from the `workspace` graph).
Tracks exploration history, dead ends, partial findings, and session provenance.
Never touches the workspace graph — clean separation.

Schema:
  Nodes:
    WanderSession {uuid, anchor, model, timestamp, outcome}
    ExploredTopic  {uuid, name, embedding, first_explored, last_explored}

  Edges:
    EXPLORED_AS_DEAD_END  {reason, depth, search_count, timestamp, session_uuid}
    EXPLORED_PARTIALLY    {notes, timestamp, session_uuid}
    LED_TO                {timestamp}  — topic chains
    ELEVATED_TO_MAIN      {title, timestamp}  — crossed the novelty gate

Dead end search:
  Embed the query → cosine search on ExploredTopic embeddings →
  return matching topics where EXPLORED_AS_DEAD_END edge exists.

Dead ends decay:
  EXPLORED_AS_DEAD_END edges have a timestamp. After DEAD_END_RECHECK_DAYS,
  the agent is told "this was a dead end N days ago — worth a quick recheck?"
"""

import json
import time
import asyncio
import sys
import math
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent / "memory-upgrade"))
sys.path.insert(0, str(Path(__file__).parent))

from mind_wander_config import FALKORDB_HOST, FALKORDB_PORT, WANDER_OLLAMA as OLLAMA_URL, WORKSPACE

WANDER_GRAPH_NAME  = "wander"
DEAD_END_RECHECK_DAYS = 14   # suggest re-examining dead ends older than this
DEAD_ENDS_FILE     = WORKSPACE / "DEAD_ENDS.md"


# ── Graph initialisation ──────────────────────────────────────────────────────

def get_graph():
    import falkordb
    r = falkordb.FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
    return r.select_graph(WANDER_GRAPH_NAME)


def init_wander_graph():
    """Create indexes on the wander graph. Idempotent."""
    g = get_graph()
    indexes = [
        "CREATE INDEX FOR (n:ExploredTopic) ON (n.uuid)",
        "CREATE INDEX FOR (n:ExploredTopic) ON (n.name)",
        "CREATE INDEX FOR (n:WanderSession) ON (n.uuid)",
        "CREATE FULLTEXT INDEX FOR (n:ExploredTopic) ON EACH [n.name, n.notes]",
    ]
    for idx in indexes:
        try:
            g.query(idx)
        except Exception:
            pass  # already exists

    # Vector index for semantic dead end search
    try:
        g.query("""
CREATE VECTOR INDEX FOR (n:ExploredTopic) ON (n.embedding)
OPTIONS {dimension: 768, similarityFunction: 'cosine'}
""")
    except Exception:
        pass

    return g


# ── Embedding helper ──────────────────────────────────────────────────────────

def embed_sync(text: str) -> list:
    import httpx
    resp = httpx.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": "nomic-embed-text", "input": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embeddings"][0]


# ── Dead end operations ───────────────────────────────────────────────────────

def record_dead_end_to_graph(
    topic: str,
    reason: str,
    depth: str,
    search_count: int,
    session_uuid: str,
    anchor: str,
) -> bool:
    """Write a dead end into the wander graph."""
    g = get_graph()
    now_iso = datetime.now(timezone.utc).isoformat()
    now_ts  = time.time()

    try:
        vec = embed_sync(topic)
    except Exception:
        vec = []

    vec_str = "[" + ",".join(str(v) for v in vec) + "]" if vec else "null"

    # Upsert ExploredTopic node
    g.query(f"""
MERGE (t:ExploredTopic {{name: $name}})
ON CREATE SET
    t.uuid           = randomUUID(),
    t.first_explored = $ts,
    t.last_explored  = $ts,
    t.notes          = $reason
ON MATCH SET
    t.last_explored  = $ts,
    t.notes          = $reason
{"SET t.embedding = vecf32(" + vec_str + ")" if vec else ""}
""", {"name": topic, "ts": now_iso, "reason": reason})

    # Add EXPLORED_AS_DEAD_END edge to itself (self-loop for annotation)
    # More precisely: create a session node and relate it
    g.query("""
MERGE (s:WanderSession {uuid: $session_uuid})
ON CREATE SET
    s.anchor    = $anchor,
    s.timestamp = $ts
""", {"session_uuid": session_uuid, "anchor": anchor, "ts": now_iso})

    g.query("""
MATCH (t:ExploredTopic {name: $name})
MATCH (s:WanderSession {uuid: $session_uuid})
MERGE (s)-[r:EXPLORED_AS_DEAD_END]->(t)
SET r.reason       = $reason,
    r.depth        = $depth,
    r.search_count = $search_count,
    r.timestamp    = $ts,
    r.ts_epoch     = $epoch
""", {
        "name": topic, "session_uuid": session_uuid,
        "reason": reason, "depth": depth,
        "search_count": search_count, "ts": now_iso, "epoch": now_ts,
    })

    return True


def search_dead_ends(query: str, limit: int = 5) -> list:
    """
    Find dead ends related to a query using Python-side cosine scoring.
    Returns list of {topic, reason, depth, age_days, recheck_suggested}.
    """
    g = get_graph()
    now_ts = time.time()

    # Fetch all dead ends with embeddings in one query
    try:
        result = g.query("""
MATCH (s:WanderSession)-[r:EXPLORED_AS_DEAD_END]->(t:ExploredTopic)
RETURN t.name, r.reason, r.depth, r.search_count, r.ts_epoch, t.embedding
""")
    except Exception:
        return []

    if not result.result_set:
        return []

    # Score in Python to avoid FalkorDB subquery ordering limitations
    try:
        import numpy as np
        qvec = np.array(embed_sync(query))
        scored = []
        for row in result.result_set:
            name, reason, depth, search_count, ts_epoch, emb = row
            if emb:
                dvec = np.array(emb)
                norm = np.linalg.norm(qvec) * np.linalg.norm(dvec)
                sim = float(np.dot(qvec, dvec) / (norm + 1e-10)) if norm > 0 else 0.0
            else:
                # Fallback: keyword match
                sim = 0.3 if any(w.lower() in str(name).lower()
                                 for w in query.split() if len(w) > 3) else 0.0
            if sim > 0.45:
                age_days = (now_ts - float(ts_epoch or now_ts)) / 86400
                scored.append({
                    "topic":              str(name),
                    "reason":             str(reason or ""),
                    "depth":              str(depth or "unknown"),
                    "search_count":       int(search_count or 0),
                    "age_days":           round(age_days, 1),
                    "similarity":         round(sim, 3),
                    "recheck_suggested":  age_days > DEAD_END_RECHECK_DAYS,
                })
        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:limit]
    except Exception:
        return []


def record_session(
    session_uuid: str,
    anchor: str,
    model: str,
    outcome: str,
    tool_calls: int,
    elevated_title: str = None,
):
    """Record a wander session in the graph."""
    g = get_graph()
    now_iso = datetime.now(timezone.utc).isoformat()
    g.query("""
MERGE (s:WanderSession {uuid: $uuid})
SET s.anchor         = $anchor,
    s.model          = $model,
    s.outcome        = $outcome,
    s.tool_calls     = $tool_calls,
    s.elevated_title = $elevated_title,
    s.timestamp      = $ts
""", {
        "uuid": session_uuid, "anchor": anchor, "model": model,
        "outcome": outcome, "tool_calls": tool_calls,
        "elevated_title": elevated_title or "", "ts": now_iso,
    })


def get_exploration_stats() -> dict:
    """Summary stats for the wander graph."""
    g = get_graph()
    try:
        sessions  = g.query("MATCH (n:WanderSession) RETURN count(n)").result_set[0][0]
        topics    = g.query("MATCH (n:ExploredTopic) RETURN count(n)").result_set[0][0]
        dead_ends = g.query("MATCH ()-[r:EXPLORED_AS_DEAD_END]->() RETURN count(r)").result_set[0][0]
        elevated  = g.query("MATCH ()-[r:ELEVATED_TO_MAIN]->() RETURN count(r)").result_set[0][0]
        return {
            "sessions": sessions, "topics": topics,
            "dead_ends": dead_ends, "elevated": elevated,
        }
    except Exception:
        return {"sessions": 0, "topics": 0, "dead_ends": 0, "elevated": 0}


# ── DEAD_ENDS.md generation ───────────────────────────────────────────────────

def regenerate_dead_ends_file():
    """
    Write a human-readable DEAD_ENDS.md from the wander graph.
    Called after each record_dead_end(). NOT added to memorySearch.extraPaths.
    """
    g = get_graph()
    try:
        result = g.query("""
MATCH (s:WanderSession)-[r:EXPLORED_AS_DEAD_END]->(t:ExploredTopic)
RETURN t.name, r.reason, r.depth, r.search_count, r.timestamp, s.anchor
ORDER BY r.timestamp DESC
LIMIT 50
""")
    except Exception:
        return

    if not result.result_set:
        return

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Dead Ends",
        f"*Auto-generated {now} from wander graph. Not in graph-rag context.*",
        "*Consulted by the wander agent before choosing what to explore.*",
        "",
    ]
    for row in result.result_set:
        name, reason, depth, search_count, ts, anchor = row
        try:
            age = datetime.now(timezone.utc) - datetime.fromisoformat(str(ts))
            age_str = f"{age.days}d ago" if age.days > 0 else "today"
        except Exception:
            age_str = "?"
        lines.append(f"## {name}")
        lines.append(f"*Explored {age_str} | Anchor: {anchor} | Searches: {search_count} | Depth: {depth}*")
        lines.append("")
        lines.append(f"{reason}")
        lines.append("")

    DEAD_ENDS_FILE.write_text("\n".join(lines))
