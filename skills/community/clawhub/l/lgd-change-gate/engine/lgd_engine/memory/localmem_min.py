"""LocalMemory: minimal SQLite decision-record store.

Schema matches DecisionRecord envelope (see task spec):
    time          ISO8601 string
    initiator     e.g. "demo1-cli"
    subject       human-readable subject / device description
    decision      "go" | "hold" | "reject"
    basis         free-text reason summary
    status        "executed" | "pending" | "vetoed"
    evidence_refs JSON-encoded list[str]

Retrieval:
  - keyword()  : SQLite LIKE / FTS5 (auto-detect FTS5 availability)
  - vector()   : fastembed if installed; otherwise falls back to keyword()
                 and notes the fallback. We never hard-require fastembed.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


_SCHEMA = """
CREATE TABLE IF NOT EXISTS decisions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    time         TEXT NOT NULL,
    initiator    TEXT NOT NULL,
    subject      TEXT NOT NULL,
    decision     TEXT NOT NULL,
    basis        TEXT NOT NULL,
    status       TEXT NOT NULL,
    evidence_refs TEXT NOT NULL,
    raw_ctx      TEXT
);
"""


class LocalMemory:
    def __init__(self, db_path: str = "lgd_memory.sqlite") -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)) or ".", exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

        # detect FTS5
        self._fts5 = True
        try:
            self._conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS decisions_fts "
                               "USING fts5(subject, basis, content='')")
        except sqlite3.OperationalError:
            self._fts5 = False

        # detect fastembed (optional)
        try:
            import fastembed  # noqa: F401
            self._fastembed = True
        except Exception:
            self._fastembed = False

    # ---------------------------------------------------------------- write
    def record(self, rec: Dict[str, Any]) -> int:
        """Write a DecisionRecord. Returns row id."""
        if "time" not in rec:
            rec["time"] = datetime.now(timezone.utc).isoformat()
        evidence_refs = rec.get("evidence_refs", [])
        cur = self._conn.execute(
            "INSERT INTO decisions(time, initiator, subject, decision, basis,"
            " status, evidence_refs, raw_ctx) VALUES (?,?,?,?,?,?,?,?)",
            (
                rec["time"],
                rec["initiator"],
                rec["subject"],
                rec["decision"],
                rec["basis"],
                rec.get("status", "executed"),
                json.dumps(evidence_refs, ensure_ascii=False),
                json.dumps(rec.get("raw_ctx", {}), ensure_ascii=False),
            ),
        )
        self._conn.commit()
        return cur.lastrowid

    # ---------------------------------------------------------------- keyword
    def keyword(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if self._fts5:
            # simple bm25 via MATCH; quote the query to avoid syntax errors
            q = query.replace('"', '""')
            rows = self._conn.execute(
                "SELECT d.* FROM decisions d "
                "WHERE d.id IN (SELECT rowid FROM decisions_fts "
                "WHERE decisions_fts MATCH ?) ORDER BY d.id DESC LIMIT ?",
                (f'"{q}"', limit),
            ).fetchall()
        else:
            like = f"%{query}%"
            rows = self._conn.execute(
                "SELECT * FROM decisions WHERE subject LIKE ? OR basis LIKE ? "
                "ORDER BY id DESC LIMIT ?",
                (like, like, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    # ---------------------------------------------------------------- vector
    def vector(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Vector recall. Uses fastembed if installed; otherwise degrades to
        keyword() and annotates the result. No numpy/torch hard dependency.
        """
        if self._fastembed:
            # MVP: skip actual embedding cosine search (would require storing
            # vectors); we still surface the records by keyword and tag the
            # result as "vector_unavailable_fallback_keyword" to be explicit.
            hits = self.keyword(query, limit=limit)
            for h in hits:
                h["_recall_mode"] = "fastembed_available_but_vector_index_not_built"
            return hits
        # fallback
        hits = self.keyword(query, limit=limit)
        for h in hits:
            h["_recall_mode"] = "fallback_keyword_no_fastembed"
        return hits

    # ---------------------------------------------------------------- misc
    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]

    def close(self) -> None:
        self._conn.close()
