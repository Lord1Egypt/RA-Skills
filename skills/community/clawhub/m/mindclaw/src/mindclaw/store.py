"""
mindclaw.store — SQLite-backed persistent memory store.

Stores memories as structured records with metadata, timestamps,
importance scores, and access tracking for decay/relevance.
"""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Generator, Optional


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class Memory:
    """A single memory record."""

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    content: str = ""
    summary: str = ""
    category: str = "general"          # fact, decision, preference, error, note
    tags: list[str] = field(default_factory=list)
    source: str = ""                   # where this memory was captured
    importance: float = 0.5            # 0.0 – 1.0
    access_count: int = 0
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    decay_rate: float = 0.01           # how fast importance decays
    archived: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    # v0.2 fields
    agent_id: str = ""                 # namespace: which agent owns this memory
    pinned: bool = False               # pinned memories are never decayed/archived
    confirmed_count: int = 0           # how many times this memory was confirmed/reinforced

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["tags"] = json.dumps(d["tags"])
        d["metadata"] = json.dumps(d["metadata"])
        return d

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Memory":
        d = dict(row)
        d["tags"] = json.loads(d["tags"])
        d["metadata"] = json.loads(d["metadata"])
        return cls(**d)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS memories (
    id              TEXT PRIMARY KEY,
    content         TEXT NOT NULL,
    summary         TEXT DEFAULT '',
    category        TEXT DEFAULT 'general',
    tags            TEXT DEFAULT '[]',
    source          TEXT DEFAULT '',
    importance      REAL DEFAULT 0.5,
    access_count    INTEGER DEFAULT 0,
    created_at      REAL,
    last_accessed   REAL,
    updated_at      REAL,
    decay_rate      REAL DEFAULT 0.01,
    archived        INTEGER DEFAULT 0,
    metadata        TEXT DEFAULT '{}',
    agent_id        TEXT DEFAULT '',
    pinned          INTEGER DEFAULT 0,
    confirmed_count INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_archived ON memories(archived);
CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(agent_id);
CREATE INDEX IF NOT EXISTS idx_memories_pinned ON memories(pinned);

CREATE TABLE IF NOT EXISTS edges (
    id              TEXT PRIMARY KEY,
    source_id       TEXT NOT NULL,
    target_id       TEXT NOT NULL,
    relation        TEXT NOT NULL,
    weight          REAL DEFAULT 1.0,
    created_at      REAL,
    metadata        TEXT DEFAULT '{}',
    FOREIGN KEY (source_id) REFERENCES memories(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES memories(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);
CREATE INDEX IF NOT EXISTS idx_edges_relation ON edges(relation);

CREATE TABLE IF NOT EXISTS embeddings_cache (
    memory_id       TEXT PRIMARY KEY,
    vector          BLOB NOT NULL,
    model           TEXT DEFAULT 'tfidf',
    updated_at      REAL,
    FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
);
"""


# ---------------------------------------------------------------------------
# MemoryStore
# ---------------------------------------------------------------------------

class MemoryStore:
    """SQLite-backed persistent memory store with knowledge graph edges."""

    def __init__(self, db_path: str | Path | None = None):
        if db_path is None:
            db_path = Path.home() / ".mindclaw" / "memory.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    # -- connection helpers -------------------------------------------------

    @contextmanager
    def _conn(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._conn() as conn:
            conn.executescript(_SCHEMA)
        # Migrate existing databases to v0.2 schema
        self._migrate()

    def _migrate(self) -> None:
        """Apply schema migrations for databases created before v0.2."""
        migrations = [
            "ALTER TABLE memories ADD COLUMN agent_id TEXT DEFAULT ''",
            "ALTER TABLE memories ADD COLUMN pinned INTEGER DEFAULT 0",
            "ALTER TABLE memories ADD COLUMN confirmed_count INTEGER DEFAULT 0",
        ]
        with self._conn() as conn:
            for sql in migrations:
                try:
                    conn.execute(sql)
                except Exception:
                    pass  # Column already exists

    # -- CRUD ---------------------------------------------------------------

    def add(self, memory: Memory) -> Memory:
        """Insert a new memory. Returns the memory with its id."""
        with self._conn() as conn:
            d = memory.to_dict()
            cols = ", ".join(d.keys())
            placeholders = ", ".join(["?"] * len(d))
            conn.execute(
                f"INSERT INTO memories ({cols}) VALUES ({placeholders})",
                list(d.values()),
            )
        return memory

    def get(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a memory by id, updating access stats."""
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM memories WHERE id = ?", (memory_id,)
            ).fetchone()
            if row is None:
                return None
            conn.execute(
                "UPDATE memories SET access_count = access_count + 1, "
                "last_accessed = ? WHERE id = ?",
                (time.time(), memory_id),
            )
            return Memory.from_row(row)

    def update(self, memory_id: str, **kwargs: Any) -> Optional[Memory]:
        """Update fields of an existing memory."""
        if not kwargs:
            return self.get(memory_id)

        kwargs["updated_at"] = time.time()

        # Serialize complex fields
        if "tags" in kwargs:
            kwargs["tags"] = json.dumps(kwargs["tags"])
        if "metadata" in kwargs:
            kwargs["metadata"] = json.dumps(kwargs["metadata"])

        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [memory_id]

        with self._conn() as conn:
            conn.execute(
                f"UPDATE memories SET {sets} WHERE id = ?", vals
            )
        return self.get(memory_id)

    def delete(self, memory_id: str) -> bool:
        """Hard-delete a memory and its edges."""
        with self._conn() as conn:
            cur = conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            return cur.rowcount > 0

    def archive(self, memory_id: str) -> bool:
        """Soft-archive a memory (mark as archived, not deleted). Refuses if pinned."""
        with self._conn() as conn:
            row = conn.execute(
                "SELECT pinned FROM memories WHERE id = ?", (memory_id,)
            ).fetchone()
            if row and row["pinned"]:
                return False  # Cannot archive a pinned memory
            cur = conn.execute(
                "UPDATE memories SET archived = 1, updated_at = ? WHERE id = ?",
                (time.time(), memory_id),
            )
            return cur.rowcount > 0

    def pin(self, memory_id: str) -> bool:
        """Pin a memory so it is never decayed or auto-archived."""
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE memories SET pinned = 1, updated_at = ? WHERE id = ?",
                (time.time(), memory_id),
            )
            return cur.rowcount > 0

    def unpin(self, memory_id: str) -> bool:
        """Remove pin from a memory."""
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE memories SET pinned = 0, updated_at = ? WHERE id = ?",
                (time.time(), memory_id),
            )
            return cur.rowcount > 0

    def confirm(self, memory_id: str) -> Optional[Memory]:
        """
        Confirm/reinforce a memory: increments confirmed_count and
        boosts importance slightly (up to a maximum of 0.95).
        """
        mem = self.get(memory_id)
        if mem is None:
            return None
        new_importance = min(mem.importance + 0.05, 0.95)
        new_count = mem.confirmed_count + 1
        with self._conn() as conn:
            conn.execute(
                "UPDATE memories SET confirmed_count = ?, importance = ?, "
                "updated_at = ? WHERE id = ?",
                (new_count, new_importance, time.time(), memory_id),
            )
        return self.get(memory_id)

    # -- Queries ------------------------------------------------------------

    def list_memories(
        self,
        *,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        include_archived: bool = False,
        limit: int = 50,
        offset: int = 0,
        order_by: str = "importance DESC",
        agent_id: Optional[str] = None,
        pinned_only: bool = False,
    ) -> list[Memory]:
        """List memories with optional filters."""
        clauses: list[str] = []
        params: list[Any] = []

        if not include_archived:
            clauses.append("archived = 0")
        if category:
            clauses.append("category = ?")
            params.append(category)
        if tag:
            clauses.append("tags LIKE ?")
            params.append(f"%{tag}%")
        if agent_id is not None:
            clauses.append("agent_id = ?")
            params.append(agent_id)
        if pinned_only:
            clauses.append("pinned = 1")

        where = " AND ".join(clauses) if clauses else "1=1"
        allowed_orders = {
            "importance DESC", "importance ASC",
            "created_at DESC", "created_at ASC",
            "last_accessed DESC", "last_accessed ASC",
            "access_count DESC", "access_count ASC",
        }
        if order_by not in allowed_orders:
            order_by = "importance DESC"

        with self._conn() as conn:
            rows = conn.execute(
                f"SELECT * FROM memories WHERE {where} "
                f"ORDER BY {order_by} LIMIT ? OFFSET ?",
                params + [limit, offset],
            ).fetchall()
        return [Memory.from_row(r) for r in rows]

    def search_text(self, query: str, *, limit: int = 20) -> list[Memory]:
        """Simple LIKE-based text search across content and summary."""
        pattern = f"%{query}%"
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM memories WHERE archived = 0 AND "
                "(content LIKE ? OR summary LIKE ? OR tags LIKE ?) "
                "ORDER BY importance DESC LIMIT ?",
                (pattern, pattern, pattern, limit),
            ).fetchall()
        return [Memory.from_row(r) for r in rows]

    def stats(self) -> dict[str, Any]:
        """Return aggregate statistics about the memory store."""
        with self._conn() as conn:
            total = conn.execute(
                "SELECT COUNT(*) AS c FROM memories"
            ).fetchone()["c"]
            active = conn.execute(
                "SELECT COUNT(*) AS c FROM memories WHERE archived = 0"
            ).fetchone()["c"]
            archived = total - active
            pinned = conn.execute(
                "SELECT COUNT(*) AS c FROM memories WHERE pinned = 1"
            ).fetchone()["c"]
            categories = conn.execute(
                "SELECT category, COUNT(*) AS c FROM memories "
                "WHERE archived = 0 GROUP BY category ORDER BY c DESC"
            ).fetchall()
            agents = conn.execute(
                "SELECT agent_id, COUNT(*) AS c FROM memories "
                "WHERE archived = 0 GROUP BY agent_id ORDER BY c DESC"
            ).fetchall()
            edges_count = conn.execute(
                "SELECT COUNT(*) AS c FROM edges"
            ).fetchone()["c"]
        return {
            "total_memories": total,
            "active": active,
            "archived": archived,
            "pinned": pinned,
            "edges": edges_count,
            "categories": {r["category"]: r["c"] for r in categories},
            "agents": {(r["agent_id"] or "default"): r["c"] for r in agents},
            "db_path": str(self.db_path),
            "db_size_kb": round(self.db_path.stat().st_size / 1024, 1)
            if self.db_path.exists()
            else 0,
        }

    # -- Knowledge Graph Edges ----------------------------------------------

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float = 1.0,
        metadata: Optional[dict] = None,
    ) -> str:
        """Create a directed edge between two memories."""
        edge_id = uuid.uuid4().hex[:12]
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO edges (id, source_id, target_id, relation, weight, "
                "created_at, metadata) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    edge_id,
                    source_id,
                    target_id,
                    relation,
                    weight,
                    time.time(),
                    json.dumps(metadata or {}),
                ),
            )
        return edge_id

    def get_edges(
        self, memory_id: str, *, direction: str = "both"
    ) -> list[dict[str, Any]]:
        """Get edges connected to a memory. direction: out, in, both."""
        results: list[dict[str, Any]] = []
        with self._conn() as conn:
            if direction in ("out", "both"):
                rows = conn.execute(
                    "SELECT * FROM edges WHERE source_id = ?", (memory_id,)
                ).fetchall()
                results.extend(dict(r) for r in rows)
            if direction in ("in", "both"):
                rows = conn.execute(
                    "SELECT * FROM edges WHERE target_id = ?", (memory_id,)
                ).fetchall()
                results.extend(dict(r) for r in rows)
        return results

    def remove_edge(self, edge_id: str) -> bool:
        """Delete an edge by id."""
        with self._conn() as conn:
            cur = conn.execute("DELETE FROM edges WHERE id = ?", (edge_id,))
            return cur.rowcount > 0

    # -- Embeddings Cache ---------------------------------------------------

    def save_embedding(
        self, memory_id: str, vector: bytes, model: str = "tfidf"
    ) -> None:
        """Cache an embedding vector for a memory."""
        with self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO embeddings_cache "
                "(memory_id, vector, model, updated_at) VALUES (?, ?, ?, ?)",
                (memory_id, vector, model, time.time()),
            )

    def get_embedding(self, memory_id: str) -> Optional[tuple[bytes, str]]:
        """Retrieve cached embedding. Returns (vector_bytes, model) or None."""
        with self._conn() as conn:
            row = conn.execute(
                "SELECT vector, model FROM embeddings_cache WHERE memory_id = ?",
                (memory_id,),
            ).fetchone()
        if row is None:
            return None
        return (row["vector"], row["model"])

    def get_all_embeddings(self, model: str = "tfidf") -> list[tuple[str, bytes]]:
        """Return all (memory_id, vector) pairs for a given model."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT memory_id, vector FROM embeddings_cache WHERE model = ?",
                (model,),
            ).fetchall()
        return [(r["memory_id"], r["vector"]) for r in rows]

    # -- Maintenance --------------------------------------------------------

    def apply_decay(self, *, threshold: float = 0.05, agent_id: Optional[str] = None) -> int:
        """
        Decay importance of memories based on time since last access.
        Archives memories that fall below threshold.
        Pinned memories are never decayed.
        Returns count of archived memories.
        """
        now = time.time()
        archived_count = 0
        sql = "SELECT id, importance, decay_rate, last_accessed FROM memories WHERE archived = 0 AND pinned = 0"
        params: list[Any] = []
        if agent_id is not None:
            sql += " AND agent_id = ?"
            params.append(agent_id)
        with self._conn() as conn:
            rows = conn.execute(sql, params).fetchall()
            for r in rows:
                days_since = (now - r["last_accessed"]) / 86400
                new_importance = r["importance"] * (1 - r["decay_rate"]) ** days_since
                if new_importance < threshold:
                    conn.execute(
                        "UPDATE memories SET archived = 1, importance = ?, "
                        "updated_at = ? WHERE id = ?",
                        (new_importance, now, r["id"]),
                    )
                    archived_count += 1
                elif abs(new_importance - r["importance"]) > 0.001:
                    conn.execute(
                        "UPDATE memories SET importance = ?, updated_at = ? "
                        "WHERE id = ?",
                        (new_importance, now, r["id"]),
                    )
        return archived_count

    def get_timeline(
        self,
        *,
        since: Optional[float] = None,
        until: Optional[float] = None,
        agent_id: Optional[str] = None,
        limit: int = 50,
    ) -> list[Memory]:
        """
        Return memories ordered chronologically within a time window.
        since/until are Unix timestamps.
        """
        clauses: list[str] = ["archived = 0"]
        params: list[Any] = []
        if since is not None:
            clauses.append("created_at >= ?")
            params.append(since)
        if until is not None:
            clauses.append("created_at <= ?")
            params.append(until)
        if agent_id is not None:
            clauses.append("agent_id = ?")
            params.append(agent_id)
        where = " AND ".join(clauses)
        with self._conn() as conn:
            rows = conn.execute(
                f"SELECT * FROM memories WHERE {where} ORDER BY created_at ASC LIMIT ?",
                params + [limit],
            ).fetchall()
        return [Memory.from_row(r) for r in rows]

    def find_conflicts(
        self, content: str, *, agent_id: Optional[str] = None, threshold: float = 0.20
    ) -> list[Memory]:
        """
        Find existing memories that may conflict with new content.
        Uses Jaccard similarity on tokens. Returns memories above threshold
        that have meaningfully different content (potential contradictions).
        """
        words_new = set(_simple_tokenize(content))
        if not words_new:
            return []

        # Search by each significant keyword so we cast a wide net
        candidates_map: dict[str, Memory] = {}
        for keyword in list(words_new)[:5]:  # top 5 tokens
            for mem in self.search_text(keyword, limit=10):
                candidates_map[mem.id] = mem

        if agent_id is not None:
            candidates_map = {k: v for k, v in candidates_map.items() if v.agent_id == agent_id}

        conflicts: list[Memory] = []
        for mem in candidates_map.values():
            words_mem = set(_simple_tokenize(mem.content))
            if not words_mem:
                continue
            intersection = words_new & words_mem
            union = words_new | words_mem
            similarity = len(intersection) / len(union)
            # Similar topic but different enough content (not near-identical)
            if threshold <= similarity < 0.85:
                conflicts.append(mem)
        return conflicts

    def consolidate_duplicates(
        self, *, agent_id: Optional[str] = None, similarity_threshold: float = 0.85
    ) -> int:
        """
        Find near-duplicate memories and archive the older/weaker one.
        Returns the number of memories consolidated.
        """
        memories = self.list_memories(limit=1000, agent_id=agent_id)
        consolidated = 0
        archived_ids: set[str] = set()
        for i, m1 in enumerate(memories):
            if m1.id in archived_ids:
                continue
            words1 = set(_simple_tokenize(m1.content))
            for m2 in memories[i + 1:]:
                if m2.id in archived_ids or m2.pinned:
                    continue
                words2 = set(_simple_tokenize(m2.content))
                union = words1 | words2
                if not union:
                    continue
                sim = len(words1 & words2) / len(union)
                if sim >= similarity_threshold:
                    # Keep the higher-importance / more confirmed one
                    keep, drop = (m1, m2) if (
                        m1.importance + m1.confirmed_count * 0.05
                        >= m2.importance + m2.confirmed_count * 0.05
                    ) else (m2, m1)
                    # Merge confirmed_count into the keeper
                    self.update(
                        keep.id,
                        confirmed_count=keep.confirmed_count + drop.confirmed_count,
                    )
                    self.archive(drop.id)
                    archived_ids.add(drop.id)
                    consolidated += 1
        return consolidated

    def export_json(self) -> str:
        """Export entire memory store as JSON string."""
        with self._conn() as conn:
            memories = conn.execute("SELECT * FROM memories").fetchall()
            edges = conn.execute("SELECT * FROM edges").fetchall()
        return json.dumps(
            {
                "version": "0.1.0",
                "exported_at": time.time(),
                "memories": [dict(r) for r in memories],
                "edges": [dict(r) for r in edges],
            },
            indent=2,
        )

    def import_json(self, data: str, *, merge: bool = True) -> dict[str, int]:
        """
        Import memories and edges from JSON string.
        If merge=True, skip existing ids. If False, replace all.
        """
        payload = json.loads(data)
        imported = {"memories": 0, "edges": 0, "skipped": 0}

        with self._conn() as conn:
            if not merge:
                conn.execute("DELETE FROM edges")
                conn.execute("DELETE FROM memories")
                conn.execute("DELETE FROM embeddings_cache")

            for m in payload.get("memories", []):
                try:
                    conn.execute(
                        "INSERT OR IGNORE INTO memories "
                        "(id, content, summary, category, tags, source, "
                        "importance, access_count, created_at, last_accessed, "
                        "updated_at, decay_rate, archived, metadata) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            m["id"], m["content"], m.get("summary", ""),
                            m.get("category", "general"),
                            m.get("tags", "[]"), m.get("source", ""),
                            m.get("importance", 0.5), m.get("access_count", 0),
                            m.get("created_at", time.time()),
                            m.get("last_accessed", time.time()),
                            m.get("updated_at", time.time()),
                            m.get("decay_rate", 0.01),
                            m.get("archived", 0),
                            m.get("metadata", "{}"),
                        ),
                    )
                    imported["memories"] += 1
                except sqlite3.IntegrityError:
                    imported["skipped"] += 1

            for e in payload.get("edges", []):
                try:
                    conn.execute(
                        "INSERT OR IGNORE INTO edges "
                        "(id, source_id, target_id, relation, weight, "
                        "created_at, metadata) VALUES (?,?,?,?,?,?,?)",
                        (
                            e["id"], e["source_id"], e["target_id"],
                            e["relation"], e.get("weight", 1.0),
                            e.get("created_at", time.time()),
                            e.get("metadata", "{}"),
                        ),
                    )
                    imported["edges"] += 1
                except sqlite3.IntegrityError:
                    imported["skipped"] += 1

        return imported
    # -- OpenClaw / Markdown integration ------------------------------------

    def export_to_markdown(
        self,
        path: "str | Path",
        *,
        agent_id: Optional[str] = None,
        overwrite: bool = False,
    ) -> int:
        """
        Export memories to a Markdown file in OpenClaw-compatible format.

        If the file already exists and overwrite=False, this replaces only
        the ``<!-- mindclaw:start --> … <!-- mindclaw:end -->`` block so any
        other content the agent has written to MEMORY.md is preserved.

        Returns the number of memories written.
        """
        import re as _re

        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)

        memories = [
            m for m in self.list_memories(
                agent_id=agent_id,   # None = all namespaces; "" = default only
                limit=5000,
            )
            if not m.archived
        ]
        if not memories:
            return 0

        # Group by category
        by_cat: dict[str, list[Memory]] = {}
        for m in memories:
            by_cat.setdefault(m.category.upper(), []).append(m)

        # Build the MindClaw block
        lines: list[str] = [
            "<!-- mindclaw:start -->",
            "",
            "## MindClaw Memories",
            "",
            f"*Last synced: {time.strftime('%Y-%m-%d %H:%M')} · {len(memories)} memories*",
            "",
        ]
        for cat in sorted(by_cat):
            mems = sorted(by_cat[cat], key=lambda x: -x.importance)
            lines.append(f"### {cat}")
            lines.append("")
            for m in mems:
                tags_str = "  `" + "` `".join(m.tags) + "`" if m.tags else ""
                pin = "  📌" if m.pinned else ""
                lines.append(f"- {m.content}{tags_str}{pin}")
            lines.append("")
        lines.append("<!-- mindclaw:end -->")
        block = "\n".join(lines)

        if not overwrite and target.exists():
            existing = target.read_text(encoding="utf-8")
            start_tok = "<!-- mindclaw:start -->"
            end_tok = "<!-- mindclaw:end -->"
            if start_tok in existing and end_tok in existing:
                before = existing[: existing.index(start_tok)].rstrip()
                after = existing[existing.index(end_tok) + len(end_tok) :].lstrip("\n")
                content = before + "\n\n" + block + ("\n\n" + after if after.strip() else "\n")
            else:
                content = existing.rstrip() + "\n\n" + block + "\n"
        else:
            content = block + "\n"

        target.write_text(content, encoding="utf-8")
        return len(memories)

    def import_from_markdown(
        self,
        path: "str | Path",
        *,
        agent_id: str = "",
        source: str = "",
        skip_mindclaw_block: bool = True,
    ) -> int:
        """
        Import memories from a Markdown file (OpenClaw's MEMORY.md or daily log).

        Parses heading sections to detect category, then treats every
        bullet-point line as an individual memory. Deduplicates against
        existing content. Returns the number of new memories created.
        """
        import datetime
        import re as _re

        target = Path(path)
        if not target.exists():
            return 0

        text = target.read_text(encoding="utf-8")

        # Skip our own exported block to avoid round-trip duplicates
        if skip_mindclaw_block:
            s, e = "<!-- mindclaw:start -->", "<!-- mindclaw:end -->"
            if s in text and e in text:
                text = text[: text.index(s)] + text[text.index(e) + len(e) :]

        # Detect date from filename (for daily logs like YYYY-MM-DD.md)
        file_date: Optional[float] = None
        try:
            file_date = datetime.datetime.strptime(target.stem, "%Y-%m-%d").timestamp()
        except ValueError:
            pass

        cat_map = {
            "decision": "decision", "fact": "fact", "preference": "preference",
            "error": "error", "bug": "error", "note": "note", "general": "general",
            "todo": "todo",
        }
        current_category = "note"

        # Pre-load existing content for dedup
        existing = self.list_memories(agent_id=agent_id, limit=5000)
        seen: set[str] = {m.content.strip().lower() for m in existing}

        imported = 0
        for line in text.splitlines():
            stripped = line.strip()

            # Category headings
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip().lower()
                current_category = next(
                    (cat for key, cat in cat_map.items() if key in heading),
                    "note",
                )
                continue

            # Bullet points → memories
            if stripped.startswith(("- ", "* ", "+ ")):
                content = stripped[2:].strip()
                if len(content) < 5:
                    continue

                # Extract backtick-wrapped tags and strip them from content
                tags = _re.findall(r"`([^`]+)`", content)
                content_clean = _re.sub(r"\s*`[^`]+`", "", content).strip(" 📌").strip()

                if not content_clean or content_clean.lower() in seen:
                    continue

                m = Memory(
                    content=content_clean,
                    category=current_category,
                    tags=tags,
                    source=source or str(target),
                    agent_id=agent_id,
                    created_at=file_date or time.time(),
                )
                self.add(m)
                seen.add(content_clean.lower())
                imported += 1

        return imported

    def sync_openclaw(
        self,
        workspace_path: "Optional[str | Path]" = None,
        *,
        agent_id: str = "",
    ) -> dict[str, Any]:
        """
        Sync MindClaw memories to OpenClaw's MEMORY.md.

        Auto-detects the OpenClaw workspace (``~/.openclaw/workspace``) if
        workspace_path is not provided.  The MindClaw block in MEMORY.md is
        updated in-place, preserving everything else the agent has written.

        Returns a stats dict with keys: ok, exported, path, workspace.
        """
        import os

        if workspace_path is None:
            # Allow override via env var
            env_ws = os.environ.get("MINDCLAW_OPENCLAW_WORKSPACE")
            workspace_path = Path(env_ws) if env_ws else Path.home() / ".openclaw" / "workspace"

        workspace_path = Path(workspace_path)

        if not workspace_path.exists():
            return {
                "ok": False,
                "error": f"OpenClaw workspace not found: {workspace_path}",
                "tip": (
                    "Pass workspace_path explicitly or set "
                    "MINDCLAW_OPENCLAW_WORKSPACE env var."
                ),
            }

        memory_md = workspace_path / "MEMORY.md"
        exported = self.export_to_markdown(memory_md, agent_id=agent_id or None)
        return {
            "ok": True,
            "exported": exported,
            "path": str(memory_md),
            "workspace": str(workspace_path),
        }

# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

import re as _re
_TOKEN_RE = _re.compile(r"[^a-z0-9]+")
_STOP = frozenset(
    "a an the is are was were be been have has had do does did will would "
    "shall should may might can could to of in for on with at by from as "
    "and or but not no i me my we you he she they it its".split()
)


def _simple_tokenize(text: str) -> list[str]:
    """Basic tokenizer for conflict/dedup detection (no external deps)."""
    tokens = _TOKEN_RE.split(text.lower())
    return [t for t in tokens if len(t) > 1 and t not in _STOP]
