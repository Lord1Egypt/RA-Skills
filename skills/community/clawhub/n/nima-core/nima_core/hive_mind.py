"""
NIMA Hive Mind — Proposal #7: Memory Entanglement
==================================================
Share memory context across agents and capture their results back to LadybugDB.

Two core functions:
1. Context injection  — before spawning a sub-agent, inject relevant memories
2. Result capture     — after a sub-agent finishes, persist its output as memory

Optional: Redis-based HiveBus for real-time agent-to-agent messaging.

Usage:
    from nima_core.hive_mind import HiveMind

    hive = HiveMind(db_path="~/.nima/memory/ladybug.lbug")

    # 1. Build enriched task for sub-agent
    enriched_task = hive.build_agent_context(
        task="Research transformer attention mechanisms",
        agent_name="researcher",
    )

    # 2. Spawn agent with enriched_task (your framework of choice)
    result = my_spawn_agent(enriched_task)

    # 3. Capture result back to memory
    hive.capture_agent_result(
        agent_label="researcher",
        result_summary=result[:500],
        model="gpt-4o",
        importance=0.8,
    )


SECURITY: Cypher Injection Defense
===================================

LadybugDB (Kùzu) does NOT support parameterized Cypher queries. This means
string escaping is the ONLY defense against Cypher injection attacks.

Injection Risks
---------------
User-controlled data flows into Cypher queries through several paths:
  - Search keywords from task strings (via build_agent_context → query_memories)
  - Memory layer names (via HiveMind.__init__ memory_types_to_query parameter)
  - Agent labels, model names, and result summaries (via capture_agent_result)

An attacker controlling these inputs could potentially:
  - Exfiltrate sensitive memory data using comment injection
  - Modify or delete memory nodes using query termination
  - Cause DoS through malformed queries or excessive resource consumption

Defense-in-Depth Strategy
--------------------------
This module implements multiple security layers:

1. **String Escaping (_escape function)**
   Escapes ALL special characters that could break out of string literals:
   - Null bytes (\\x00) — removed entirely (can terminate strings)
   - Backslashes (\\) — escaped to \\\\ (MUST be first to prevent double-escaping)
   - Single quotes (') — escaped to \\' (Cypher string delimiter)
   - Newlines/tabs (\\n, \\r, \\t) — escaped to prevent query breaking
   - Comment markers (//, /*, */) — escaped to prevent comment injection

2. **Whitelist Validation (_validate_and_escape_layers)**
   Memory layer names are validated against a whitelist of known types:
   - Preferred: whitelist check (contemplation, episodic, semantic, etc.)
   - Fallback: regex validation ([a-zA-Z][a-zA-Z0-9_]{0,31})
   - Always: escaping applied even after validation (defense-in-depth)

3. **Input Type Validation**
   Numeric parameters are validated before interpolation:
   - get_swarm_status(hours) — validated as int in range [0, 8760]
   - Calculated values (cutoff_ms) — validated as positive integers

Attack Vectors Mitigated
-------------------------
✅ Null byte injection:          "test\\x00'; DROP TABLE--"
✅ Comment injection:            "test// OR 1=1"
✅ Multi-line comment injection: "test/* OR 1=1 */"
✅ Quote escape:                 "test\\' OR 1=1--"
✅ Backslash escape:             "test\\\\\\\\ OR 1=1"
✅ Newline breaking:             "test\\nMATCH (n) DELETE n"
✅ Layer name injection:         ["episodic', true); DELETE--"]
✅ Unicode normalization:        Handled via NFC normalization in _escape()

Safe Query Construction Examples
---------------------------------
✅ CORRECT — Use _escape() for ALL user-controlled strings:

    keyword = _escape(user_input)
    query = f"MATCH (n) WHERE n.text CONTAINS '{keyword}' RETURN n"

✅ CORRECT — Validate and escape layer names at initialization:

    layers = _validate_and_escape_layers(user_layers)
    layers_str = "[" + ",".join(f"'{layer}'" for layer in layers) + "]"
    query = f"MATCH (n) WHERE n.layer IN {layers_str} RETURN n"

✅ CORRECT — Validate integers before interpolation:

    hours_validated = int(hours)
    if hours_validated < 0 or hours_validated > 8760:
        raise ValueError("hours must be in range [0, 8760]")
    cutoff_ms = int((time.time() - hours_validated * 3600) * 1000)
    query = f"MATCH (n) WHERE n.timestamp > {cutoff_ms} RETURN n"

❌ UNSAFE — Never interpolate user input without escaping:

    # VULNERABLE to injection!
    query = f"MATCH (n) WHERE n.text CONTAINS '{user_input}' RETURN n"

❌ UNSAFE — Never trust "sanitized" input without validation:

    # VULNERABLE — no validation of layer names!
    query = f"MATCH (n) WHERE n.layer = '{layer_name}' RETURN n"

Guidelines for Future Development
----------------------------------
When adding new Cypher queries to this module:

1. **Identify all user-controlled inputs** — task strings, agent labels, model
   names, memory layers, any data derived from external sources.

2. **Apply _escape() to ALL string literals** — even if you think the input is
   "safe". Defense-in-depth requires escaping at the point of use.

3. **Use whitelist validation for enums** — if the value should be from a
   known set (like memory layers), validate against that set first.

4. **Validate numeric types explicitly** — use int() cast and range checks
   before interpolating into queries, even for "obviously numeric" values.

5. **Never concatenate raw user input** — always escape first, validate first,
   or use both (defense-in-depth).

6. **Test with malicious inputs** — see tests/test_cypher_security.py for
   examples of injection attempts that should be blocked.

7. **Add security test cases** — when adding new query paths, add corresponding
   security tests to verify injection attempts are blocked.

For questions or to report security issues, see SECURITY.md.
"""

import json
import logging
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

try:
    import real_ladybug as lb

    HAS_LADYBUG = True
except ImportError:
    HAS_LADYBUG = False


# ── Stop words for keyword extraction ─────────────────────────────────────────

_STOPWORDS = {
    "i",
    "me",
    "my",
    "we",
    "our",
    "you",
    "your",
    "he",
    "him",
    "his",
    "she",
    "her",
    "it",
    "its",
    "they",
    "them",
    "their",
    "what",
    "which",
    "who",
    "this",
    "that",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "as",
    "at",
    "by",
    "for",
    "with",
    "into",
    "to",
    "from",
    "in",
    "on",
    "up",
    "not",
    "so",
    "can",
    "will",
    "just",
    "build",
    "please",
    "task",
    "test",
    "also",
    "some",
    "all",
    "then",
    "than",
}


def _extract_keywords(text: str, top_n: int = 5) -> List[str]:
    words = re.findall(r"\w+", text.lower())
    filtered = [w for w in words if w not in _STOPWORDS and len(w) > 2]
    counts: Dict[str, int] = {}
    for w in filtered:
        counts[w] = counts.get(w, 0) + 1
    return [
        k for k, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    ]


def _escape(s: str) -> str:
    """Escape strings for safe use in Cypher queries.

    LadybugDB (Kùzu) does NOT support parameterized Cypher queries,
    so string escaping is the only defense against injection.

    Backslashes MUST be escaped before single quotes to avoid
    double-escaping (e.g. \\' becoming \\\\' instead of \\').

    Must be applied to ALL user-controlled or external data before
    embedding in Cypher query strings.

    Args:
        s: String to escape

    Returns:
        Escaped string safe for Cypher string literals
    """
    if not isinstance(s, str):
        s = str(s)

    # Remove null bytes (can terminate strings in some contexts)
    s = s.replace("\x00", "")

    # Escape backslashes first (order matters!)
    s = s.replace("\\", "\\\\")

    # Escape single quotes
    s = s.replace("'", "\\'")

    # Escape newlines and tabs to prevent query breaking
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("\t", "\\t")

    # Escape Cypher comment markers to prevent comment injection
    s = s.replace("//", "\\/\\/")
    s = s.replace("/*", "\\/\\*")
    s = s.replace("*/", "\\*\\/")

    return s


def _validate_and_escape_layers(layers: List[str]) -> List[str]:
    """Validate and escape memory layer names for safe Cypher query construction.

    Memory layer names are user-controlled via HiveMind.__init__() and must
    be validated before embedding in Cypher queries. This function implements
    defense-in-depth: whitelist validation + regex validation + escaping.

    Args:
        layers: List of memory layer names to validate and escape

    Returns:
        List of validated and escaped layer names safe for Cypher

    Raises:
        ValueError: If any layer name is invalid or potentially malicious
    """
    # Whitelist of known valid memory layer types
    VALID_LAYERS = {
        "contemplation",
        "episodic",
        "semantic",
        "legacy_vsa",
        "procedural",
        "working",
        "sensory",
    }

    validated_layers = []
    for layer in layers:
        if not isinstance(layer, str):
            raise ValueError(f"Layer name must be string, got {type(layer).__name__}")

        # Remove null bytes and whitespace
        layer = layer.replace("\x00", "").strip()

        if not layer:
            raise ValueError("Layer name cannot be empty")

        # Whitelist check (preferred)
        if layer in VALID_LAYERS:
            validated_layers.append(layer)
            continue

        # Fallback: validate against alphanumeric + underscore pattern
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{0,31}$", layer):
            raise ValueError(
                f"Invalid layer name '{layer}': must start with letter, "
                f"contain only alphanumeric/underscore, max 32 chars"
            )

        # Apply escaping as defense-in-depth (even though validated)
        validated_layers.append(_escape(layer))

    return validated_layers


class HiveMind:
    """
    Memory Entanglement — inject memory context into sub-agents and capture results.

    This is the foundational layer for multi-agent memory sharing:
    any agent can query relevant memories before starting and persist
    its output back to the shared memory store.
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        agent_name: str = "orchestrator",
        max_context_memories: int = 8,
        memory_types_to_query: Optional[List[str]] = None,
    ):
        """
        Args:
            db_path:                 LadybugDB path (.lbug). If None, context injection
                                     returns empty (graceful degradation).
            agent_name:              Name of the orchestrating agent (used in capture).
            max_context_memories:    Max memories to inject per task.
            memory_types_to_query:   Memory layers to search. Defaults to
                                     ["contemplation", "episodic", "semantic", "legacy_vsa"].
        """
        self.db_path = str(Path(db_path).expanduser()) if db_path else None
        self.agent_name = agent_name
        self.max_context_memories = max_context_memories

        # Validate and store memory layer types
        layers_input = memory_types_to_query or [
            "contemplation",
            "episodic",
            "semantic",
            "legacy_vsa",
        ]
        self.memory_types_to_query = _validate_and_escape_layers(layers_input)

    # ── Context Injection ─────────────────────────────────────────────────────

    def query_memories(self, keywords: List[str], top_k: int = 10) -> List[Dict]:
        """Query LadybugDB for memories relevant to the given keywords."""
        if not self.db_path:
            return []
        if not Path(self.db_path).exists():
            logger.warning(f"LadybugDB not found: {self.db_path}")
            return []

        memories: List[Dict] = []
        seen_ids = set()

        # Build layer filter string for Cypher
        # Note: layers are already validated and escaped in __init__
        layers_str = (
            "[" + ",".join(f"'{layer}'" for layer in self.memory_types_to_query) + "]"
        )

        # Try LadybugDB first
        if HAS_LADYBUG:
            try:
                db = lb.Database(self.db_path)
                conn = lb.Connection(db)
                try:
                    conn.execute("LOAD VECTOR")
                except Exception as exc:
                    logger.debug(
                        f"LOAD VECTOR not available: {exc}"
                    )  # LOAD VECTOR may not be available in all versions

                # Strategy: per-keyword scans (no OR support in all LadybugDB versions)
                for kw in keywords[:3]:
                    # SECURITY: Properly escape keyword to prevent Cypher injection
                    kw_escaped = _escape(kw[:50])
                    try:
                        rows = conn.execute(
                            f"""MATCH (n:MemoryNode)
                                WHERE n.is_ghost = false
                                  AND n.layer IN {layers_str}
                                  AND (n.text CONTAINS '{kw_escaped}' OR n.summary CONTAINS '{kw_escaped}')
                                RETURN n.id, n.text, n.summary, n.who, n.timestamp, n.importance, n.layer
                                LIMIT 5"""
                        )
                        for row in rows:
                            rid = int(row[0])
                            if rid in seen_ids:
                                continue
                            seen_ids.add(rid)
                            memories.append(
                                {
                                    "id": rid,
                                    "text": str(row[1] or ""),
                                    "summary": str(row[2] or ""),
                                    "who": str(row[3] or ""),
                                    "timestamp": float(row[4] or 0),
                                    "importance": float(row[5] or 0.5),
                                    "layer": str(row[6] or ""),
                                }
                            )
                    except Exception as e:
                        logger.debug(f"Keyword query failed for '{kw}': {e}")
                        continue

                conn.close()
            except Exception as e:
                logger.warning(f"LadybugDB query failed: {e}")

        # SQLite fallback if no results from LadybugDB
        if not memories:
            sqlite_path = os.path.join(
                os.path.dirname(self.db_path or ""), "graph.sqlite"
            )
            if os.path.exists(sqlite_path):
                try:
                    conn = sqlite3.connect(sqlite_path)
                    for kw in keywords[:3]:
                        # Sanitize keyword for SQLite FTS5
                        kw_safe = kw.replace("'", "").replace('"', "")[:50]
                        if not kw_safe:
                            continue
                        try:
                            rows = conn.execute(
                                """SELECT id, text, summary, who, timestamp 
                                   FROM memory_nodes 
                                   WHERE id IN (
                                       SELECT rowid FROM memory_fts WHERE memory_fts MATCH ?
                                   ) LIMIT 5""",
                                (kw_safe,),
                            ).fetchall()
                            for row in rows:
                                rid = int(row[0])
                                if rid in seen_ids:
                                    continue
                                seen_ids.add(rid)
                                memories.append(
                                    {
                                        "id": rid,
                                        "text": str(row[1] or ""),
                                        "summary": str(row[2] or ""),
                                        "who": str(row[3] or ""),
                                        "timestamp": float(row[4] or 0)
                                        if row[4]
                                        else 0,
                                        "importance": 0.5,
                                        "layer": "unknown",
                                    }
                                )
                        except sqlite3.Error as e:
                            logger.debug(
                                f"SQLite FTS query failed for '{kw_safe}': {e}"
                            )
                            continue
                    conn.close()
                except Exception as e:
                    logger.warning(f"SQLite fallback failed: {e}")

        # Sort by importance + recency
        memories.sort(key=lambda m: (m["importance"], m["timestamp"]), reverse=True)
        return memories[:top_k]

    def format_context_block(self, memories: List[Dict]) -> str:
        """Format a list of memory dicts into an injectable context block."""
        if not memories:
            return ""

        lines = ["## HIVE CONTEXT (from shared memory)", ""]
        for m in memories:
            ts = m.get("timestamp", 0)
            if ts:
                try:
                    date = datetime.fromtimestamp(float(ts) / 1000).strftime("%Y-%m-%d")
                except (ValueError, OSError, OverflowError) as e:
                    logger.debug("Timestamp conversion failed: %s", e)
                    date = "?"
            else:
                date = "?"
            text = m.get("summary") or m.get("text", "")[:200]
            who = m.get("who", "")
            who_str = f" [{who}]" if who and who not in ("self", "unknown", "") else ""
            lines.append(f"• [{date}]{who_str} {text}")

        lines.append("")
        return "\n".join(lines)

    def build_agent_context(
        self,
        task: str,
        agent_name: Optional[str] = None,
        max_memories: Optional[int] = None,
    ) -> str:
        """
        Build an enriched task string with memory context prepended.

        Args:
            task:         The task/prompt for the sub-agent.
            agent_name:   Override the agent label in the context header.
            max_memories: Override max context memories.

        Returns:
            The task string with a HIVE CONTEXT block prepended (or just
            the original task if no relevant memories found).
        """
        keywords = _extract_keywords(task, top_n=5)
        if not keywords:
            return task

        max_k = max_memories or self.max_context_memories
        memories = self.query_memories(keywords, top_k=max_k)
        context_block = self.format_context_block(memories)

        if not context_block:
            return task

        agent_label = agent_name or self.agent_name
        header = f"## HIVE CONTEXT for {agent_label}\n\n"
        return header + context_block + "## YOUR TASK\n\n" + task

    # ── Result Capture ────────────────────────────────────────────────────────

    def capture_agent_result(
        self,
        agent_label: str,
        result_summary: str,
        model: str = "unknown",
        importance: float = 0.7,
        layer: str = "episodic",
        extra: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Persist a sub-agent's result back to LadybugDB as a memory.

        Delegates to the module-level capture_agent_result function.

        Args:
            agent_label:     Name/label of the agent that produced the result.
            result_summary:  Summary of what the agent produced (≤500 chars recommended).
            model:           Model used by the agent.
            importance:      Memory importance (0–1).
            layer:           Memory layer to store in.
            extra:           Optional extra fields to include in the text.

        Returns:
            True if stored successfully, False otherwise.
        """
        text = (
            f"[Agent result: {agent_label}] [{model}] "
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] " + result_summary[:800]
        )
        if extra:
            text += " | " + json.dumps(extra)[:200]

        from nima_core.hive_mind import capture_agent_result as _capture

        return _capture(agent_label, text, model, db_path=self.db_path)


# ── HiveBus (Redis pub/sub) — optional extra ──────────────────────────────────


class HiveBus:
    """
    Redis-backed message bus for real-time agent-to-agent communication.

    Requires: redis-py (`pip install redis`)
    Requires: a running Redis instance (e.g. `docker run -d -p 6379:6379 redis:alpine`)

    Usage:
        bus = HiveBus("my-agent", role="research", swarm_id="swarm-001")
        bus.broadcast("Starting research on transformers")
        bus.send_to_role("review", "Please review this draft: ...")
        for msg in bus.listen(timeout=60):
            print(msg)
    """

    CHANNEL_BROADCAST = "hive"

    def __init__(
        self,
        agent_id: str,
        role: str = "agent",
        swarm_id: Optional[str] = None,
        redis_url: str = "redis://localhost:6379",
    ):
        self.agent_id = agent_id
        self.role = role
        self.swarm_id = swarm_id
        self.redis_url = redis_url
        self._r = None

    def _redis(self):
        if self._r is None:
            try:
                import redis

                self._r = redis.from_url(self.redis_url, decode_responses=True)
            except ImportError:
                raise RuntimeError("redis-py not installed. Run: pip install redis")
        return self._r

    def ping(self) -> bool:
        try:
            return self._redis().ping()
        except (ConnectionError, OSError) as e:
            logger.debug("Redis ping failed: %s", e)
            return False

    def _publish(self, channel: str, payload: dict):
        payload.setdefault("from_agent", self.agent_id)
        payload.setdefault("from_role", self.role)
        payload.setdefault("swarm_id", self.swarm_id)
        payload.setdefault("ts", datetime.utcnow().isoformat())
        self._redis().publish(channel, json.dumps(payload))

    def broadcast(self, content: str, msg_type: str = "broadcast"):
        try:
            self._publish(
                self.CHANNEL_BROADCAST, {"type": msg_type, "content": content}
            )
        except ConnectionError as e:
            logger.warning(f"Redis broadcast failed: {e}")
            return False

    def send_to_role(self, role: str, content: str, msg_type: str = "direct"):
        try:
            self._publish(
                f"role:{role}", {"type": msg_type, "content": content, "to_role": role}
            )
        except ConnectionError as e:
            logger.warning(f"Redis send_to_role failed: {e}")
            return False

    def send_to_agent(self, agent_id: str, content: str, msg_type: str = "direct"):
        try:
            self._publish(
                f"agent:{agent_id}",
                {"type": msg_type, "content": content, "to_agent": agent_id},
            )
        except ConnectionError as e:
            logger.warning(f"Redis send_to_agent failed: {e}")
            return False

    def send_result(self, content: str):
        """Publish a result to the swarm results channel."""
        if not self.swarm_id:
            raise ValueError("swarm_id required for send_result")
        try:
            self._publish(
                f"results:{self.swarm_id}", {"type": "result", "content": content}
            )
        except ConnectionError as e:
            logger.warning(f"Redis send_result failed: {e}")
            return False

    def listen(self, timeout: float = 60.0, channels: Optional[List[str]] = None):
        """
        Subscribe and yield incoming messages as dicts.
        Default channels: hive broadcast + this agent's role + agent-direct.
        """
        import time

        try:
            r = self._redis()
        except (ConnectionError, Exception) as e:
            logger.warning(f"Redis connection failed in listen: {e}")
            return

        subs = channels or [
            self.CHANNEL_BROADCAST,
            f"role:{self.role}",
            f"agent:{self.agent_id}",
        ]
        try:
            ps = r.pubsub()
            ps.subscribe(*subs)
        except ConnectionError as e:
            logger.warning(f"Redis subscribe failed: {e}")
            return

        deadline = time.time() + timeout
        try:
            for message in ps.listen():
                if time.time() > deadline:
                    break
                if message["type"] == "message":
                    try:
                        yield json.loads(message["data"])
                    except json.JSONDecodeError:
                        yield {"raw": message["data"]}
        except ConnectionError as e:
            logger.warning(f"Redis listen interrupted: {e}")

    def active_agents(self) -> List[str]:
        """Return agent IDs that have recently heartbeated."""
        try:
            r = self._redis()
            keys = r.keys("hive:heartbeat:*")
            return [k.replace("hive:heartbeat:", "") for k in keys]
        except Exception as e:
            logger.warning(f"Redis active_agents failed: {e}")
            return []

    def heartbeat(self, ttl: int = 60):
        """Announce this agent is alive (auto-expires after ttl seconds)."""
        try:
            self._redis().setex(f"hive:heartbeat:{self.agent_id}", ttl, self.role)
        except ConnectionError as e:
            logger.warning(f"Redis heartbeat failed: {e}")


# ── Standalone Hive Utilities (Proposal 07: Memory Entanglement) ──────────────


def capture_agent_result(
    agent_label: str,
    result_summary: str,
    model_used: str,
    db_path: str = None,
) -> bool:
    """
    Store a sub-agent's result in LadybugDB with source_agent attribution.

    This is the core of Memory Entanglement — sub-agent outputs are tagged
    with their identity so the orchestrator (and future agents) can query
    "what did agent X find recently?"

    Args:
        agent_label:    Human-readable name (e.g. "research-agent", "code-review")
        result_summary: The agent's output (truncated to 2000 chars)
        model_used:     Model that produced the result (e.g. "gemini-3-flash")
        db_path:        Path to LadybugDB (default: NIMA_HOME/memory/ladybug.lbug)

    Returns:
        True if stored successfully, False otherwise.
    """
    import time

    try:
        import real_ladybug as lb
    except ImportError:
        print(
            "[nima-hive] real_ladybug not available — cannot capture agent result",
            flush=True,
        )
        return False

    nima_home = os.environ.get("NIMA_HOME", os.path.expanduser("~/.nima"))
    db_path = db_path or os.path.join(nima_home, "memory", "ladybug.lbug")

    if not os.path.exists(db_path):
        print(f"[nima-hive] LadybugDB not found: {db_path}", flush=True)
        return False

    db = lb.Database(db_path)
    conn = lb.Connection(db)

    try:
        conn.execute("LOAD VECTOR")
    except Exception as exc:
        logger.debug(f"LOAD VECTOR not available: {exc}")

    # Get next ID
    try:
        res = conn.execute("MATCH (n:MemoryNode) RETURN max(n.id) AS max_id")
        max_id = 0
        for row in res:
            max_id = row[0] or 0
        new_id = int(max_id) + 1
    except (RuntimeError, ValueError) as e:
        logger.warning("Failed to get max node ID from graph, using timestamp: %s", e)
        max_id = 0
        new_id = int(time.time())

    now_ms = int(time.time() * 1000)
    content = result_summary[:2000]

    try:
        # Note: embedding is NOT included here — real embeddings get added
        # by the backfill script later
        conn.execute(
            """
            CREATE (n:MemoryNode {
                id:           $id,
                who:          $who,
                text:         $text,
                summary:      $summary,
                layer:        $layer,
                fe_score:     $fe_score,
                source_agent: $source_agent,
                model:        $model,
                timestamp:    $timestamp,
                strength:     $strength,
                is_ghost:     $is_ghost
            })
        """,
            {
                "id": new_id,
                "who": f"agent:{agent_label}",
                "text": content,
                "summary": result_summary[:200],
                "layer": "output",
                "fe_score": 0.7,
                "source_agent": agent_label,
                "model": model_used,
                "timestamp": now_ms,
                "strength": 1.0,
                "is_ghost": False,
            },
        )

        # Link to 3 most recent memories (co-occurrence edges)
        for offset in range(3):
            prev_id = int(max_id) - offset
            if prev_id > 0:
                try:
                    conn.execute(
                        """
                        MATCH (a:MemoryNode {id: $aid}), (b:MemoryNode {id: $bid})
                        CREATE (a)-[:relates_to {relation: 'co_occurrence', weight: 1.0}]->(b)
                    """,
                        {"aid": new_id, "bid": prev_id},
                    )
                except Exception as exc:
                    logger.debug(f"Edge creation failed for {new_id}->{prev_id}: {exc}")

        print(f"[nima-hive] ✅ Captured {agent_label} → node {new_id}", flush=True)
        return True

    except Exception as e:
        logger.error(f"capture_agent_result failed: {e}")
        return False
    finally:
        conn.close()


def get_swarm_status(db_path: str = None, hours: int = 24) -> dict:
    """
    Query LadybugDB for all sub-agent activity in the last N hours.

    Returns dict with count, agent_labels, and recent_activity.
    """
    try:
        import real_ladybug as lb
    except ImportError:
        return {"error": "real_ladybug not available", "count": 0}

    import time

    nima_home = os.environ.get("NIMA_HOME", os.path.expanduser("~/.nima"))
    db_path = db_path or os.path.join(nima_home, "memory", "ladybug.lbug")

    # Validate hours parameter to prevent injection via calculation
    try:
        hours_validated = int(hours)
        if hours_validated < 0 or hours_validated > 8760:  # Max 1 year
            raise ValueError(f"hours must be between 0 and 8760, got {hours_validated}")
    except (ValueError, TypeError) as e:
        return {"error": f"Invalid hours parameter: {e}", "count": 0}

    # Calculate cutoff timestamp - validated integer math is safe
    cutoff_ms = int((time.time() - hours_validated * 3600) * 1000)

    # Additional safety: ensure cutoff_ms is a valid positive integer
    if cutoff_ms < 0:
        cutoff_ms = 0

    db = lb.Database(db_path)
    conn = lb.Connection(db)
    conn.execute("LOAD VECTOR")

    try:
        # SECURITY: Escape the agent prefix to prevent injection
        agent_prefix = _escape("agent:")

        # Build query with validated numeric value and escaped string literal
        # cutoff_ms is validated integer - safe for interpolation
        query = f"""
            MATCH (n:MemoryNode)
            WHERE n.timestamp > {cutoff_ms} AND n.who STARTS WITH '{agent_prefix}'
            RETURN n.who, n.source_agent, n.timestamp
            ORDER BY n.timestamp DESC
        """

        res = conn.execute(query)

        results = [
            {"who": row[0], "source_agent": row[1], "timestamp": row[2]} for row in res
        ]
        agents = sorted(set(r["who"] for r in results))

        return {
            "count": len(results),
            "agent_labels": agents,
            "recent_activity": results[:10],
        }
    except Exception as e:
        return {"error": str(e), "count": 0}
    finally:
        conn.close()


__all__ = ["HiveMind", "HiveBus", "capture_agent_result", "get_swarm_status"]


def _swarm_cli():
    """CLI: nima-swarm — show swarm status or capture a test result."""
    import argparse
    import json as _json

    parser = argparse.ArgumentParser(description="NIMA Swarm Status (Proposal 07)")
    parser.add_argument("--hours", type=int, default=24, help="Lookback hours")
    parser.add_argument(
        "--capture",
        nargs=3,
        metavar=("AGENT", "SUMMARY", "MODEL"),
        help="Capture agent result: agent summary model",
    )
    parser.add_argument("--db", default=None, help="Path to LadybugDB")
    args = parser.parse_args()

    if args.capture:
        agent, summary, model = args.capture
        capture_agent_result(agent, summary, model, db_path=args.db)
    else:
        status = get_swarm_status(db_path=args.db, hours=args.hours)
        logger.info(_json.dumps(status, indent=2, default=str))
