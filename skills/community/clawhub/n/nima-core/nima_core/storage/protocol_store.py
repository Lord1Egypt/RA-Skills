"""
Protocol Store — Governance layer for NIMA cognitive memory.

Stores and retrieves ProtocolNodes: constitutional rules that govern agent
behaviour. Retrieved contextually (JIT) by keyword and domain matching.

Inspired by Athena's constitutional law system. Fills the gap between raw
memory (episodic) and active reasoning (what the agent *should* do).
"""

from __future__ import annotations

import json
import logging
import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from nima_core.connection_pool import get_pool

logger = logging.getLogger(__name__)

MAX_NODE_ID_LEN = 256
NIMA_HOME_DEFAULT = str(Path.home() / ".nima")


class ProtocolStore:
    """
    CRUD manager for ProtocolNodes in a SQLite backend.

    ProtocolNodes are constitutional rules the agent uses to govern its
    reasoning. They are retrieved contextually — matched by domain tag or
    keyword overlap with the current user message — and injected into the
    agent context before it responds.

    Schema (managed internally, separate from main graph.sqlite):
        protocols(
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            rule TEXT NOT NULL,
            domain TEXT DEFAULT 'general',
            priority INTEGER DEFAULT 3,
            trigger_keywords TEXT DEFAULT '[]',  -- JSON array
            active INTEGER DEFAULT 1,
            created_at TEXT,
            updated_at TEXT
        )

    Priority: 1 = highest (always surface), 5 = lowest (surface only if highly relevant)
    """

    def __init__(self, db_path: Optional[str] = None):
        """Initialize ProtocolStore with SQLite path, creating DB if needed."""
        if db_path is None:
            nima_home = os.environ.get("NIMA_HOME", NIMA_HOME_DEFAULT)
            db_path = str(Path(nima_home) / "memory" / "protocols.db")

        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        """Return a context-managed SQLite connection from the pool."""
        pool_conn = get_pool(self.db_path).get_connection()

        class ConfiguredConnection:
            def __enter__(self):
                self.conn = pool_conn.__enter__()
                self.conn.row_factory = sqlite3.Row
                self.conn.execute("PRAGMA foreign_keys=ON")
                return self.conn

            def __exit__(self, exc_type, exc_val, exc_tb):
                return pool_conn.__exit__(exc_type, exc_val, exc_tb)

        return ConfiguredConnection()

    def _init_db(self) -> None:
        """Create the protocols table if it does not already exist."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS protocols (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    rule TEXT NOT NULL,
                    domain TEXT DEFAULT 'general',
                    priority INTEGER DEFAULT 3,
                    trigger_keywords TEXT DEFAULT '[]',
                    active INTEGER DEFAULT 1,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_proto_domain ON protocols(domain)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_proto_priority ON protocols(priority)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_proto_active ON protocols(active)")

    # ─── Write ────────────────────────────────────────────────────────────────

    def add(
        self,
        name: str,
        rule: str,
        domain: str = "general",
        priority: int = 3,
        keywords: Optional[list[str]] = None,
    ) -> str:
        """Add a new protocol. Returns the generated ID."""
        if not isinstance(priority, int) or not (1 <= priority <= 5):
            raise ValueError("priority must be an integer 1-5")
        if not isinstance(domain, str):
            raise TypeError(f"domain must be a str, got {type(domain).__name__}")
        if keywords is not None:
            if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
                raise TypeError("keywords must be a list of strings or None")
        protocol_id = str(uuid.uuid4())[:MAX_NODE_ID_LEN]
        now = datetime.now(timezone.utc).isoformat()
        kw_json = json.dumps(keywords or [])
        try:
            with self._connect() as conn:
                conn.execute(
                    """INSERT INTO protocols
                       (id, name, rule, domain, priority, trigger_keywords, active, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)""",
                    (protocol_id, name, rule, domain, priority, kw_json, now, now),
                )
            return protocol_id
        except Exception as exc:
            logger.warning("ProtocolStore.add error: %s", exc)
            raise

    def update(self, protocol_id: str, **kwargs) -> bool:
        """Update fields on an existing protocol. Returns True if found."""
        if len(protocol_id) > MAX_NODE_ID_LEN:
            raise ValueError("protocol_id exceeds max length")
        allowed = {"name", "rule", "domain", "priority", "trigger_keywords", "active"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return False
        if "priority" in updates:
            p = updates["priority"]
            if not isinstance(p, int) or not (1 <= p <= 5):
                raise ValueError("priority must be an integer 1-5")
        if "domain" in updates and not isinstance(updates["domain"], str):
            raise TypeError(f"domain must be a str, got {type(updates['domain']).__name__}")
        if "trigger_keywords" in updates:
            kw = updates["trigger_keywords"]
            if kw is not None and isinstance(kw, list) and not all(isinstance(k, str) for k in kw):
                raise TypeError("trigger_keywords must be a list of strings or None")
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        if "trigger_keywords" in updates and isinstance(updates["trigger_keywords"], list):
            updates["trigger_keywords"] = json.dumps(updates["trigger_keywords"])
        cols = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [protocol_id]
        try:
            with self._connect() as conn:
                cur = conn.execute(f"UPDATE protocols SET {cols} WHERE id = ?", vals)  # noqa: S608
                return cur.rowcount > 0 if cur.rowcount != -1 else True
        except Exception as exc:
            logger.warning("ProtocolStore.update error: %s", exc)
            return False

    def delete(self, protocol_id: str) -> bool:
        """Hard delete. Returns True if found."""
        if len(protocol_id) > MAX_NODE_ID_LEN:
            raise ValueError("protocol_id exceeds max length")
        try:
            with self._connect() as conn:
                cur = conn.execute("DELETE FROM protocols WHERE id = ?", (protocol_id,))
                return cur.rowcount > 0 if cur.rowcount != -1 else True
        except Exception as exc:
            logger.warning("ProtocolStore.delete error: %s", exc)
            return False

    # ─── Read ─────────────────────────────────────────────────────────────────

    def get(self, protocol_id: str) -> Optional[dict]:
        """Fetch a single protocol by ID."""
        if len(protocol_id) > MAX_NODE_ID_LEN:
            return None
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT * FROM protocols WHERE id = ?", (protocol_id,)
                ).fetchone()
                return self._row_to_dict(row) if row else None
        except Exception as exc:
            logger.warning("ProtocolStore.get error: %s", exc)
            return None

    def retrieve(
        self,
        query: str,
        domain: Optional[str] = None,
        max_results: int = 3,
    ) -> list[dict]:
        """
        Contextual retrieval: returns active protocols whose keywords or domain
        match the query. Priority 1 protocols are always included first.

        Args:
            query: The user message or context to match against.
            domain: Optional domain filter (e.g. 'family', 'emjac').
            max_results: Max protocols to return.

        Returns:
            List of protocol dicts sorted by priority (1=highest first).
        """
        query_lower = query.lower()
        try:
            with self._connect() as conn:
                if domain:
                    # Always include P1 protocols regardless of domain filter
                    # Use COLLATE NOCASE to match Python .lower()-based logic
                    rows = conn.execute(
                        "SELECT * FROM protocols WHERE active=1 AND (priority=1 OR domain=? COLLATE NOCASE) ORDER BY priority ASC",
                        (domain,),
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT * FROM protocols WHERE active=1 ORDER BY priority ASC"
                    ).fetchall()
        except Exception as exc:
            logger.warning("ProtocolStore.retrieve error: %s", exc)
            return []

        scored: list[tuple[int, dict]] = []
        for row in rows:
            proto = self._row_to_dict(row)
            # Priority 1 always surfaces
            if proto["priority"] == 1:
                scored.append((0, proto))
                continue
            # Keyword match
            keywords = proto.get("trigger_keywords") or []
            matched = any(re.search(re.escape(kw.lower()), query_lower) for kw in keywords)
            # Domain match: explicit param takes precedence, then query text
            explicit_domain_match = domain is not None and proto["domain"].lower() == domain.lower()
            domain_match = explicit_domain_match or (
                proto["domain"] != "general" and proto["domain"].lower() in query_lower
            )
            if matched or domain_match:
                scored.append((proto["priority"], proto))

        scored.sort(key=lambda x: x[0])
        return [p for _, p in scored[:max_results]]

    def list_all(self, include_inactive: bool = False) -> list[dict]:
        """Return all protocols."""
        try:
            with self._connect() as conn:
                q = "SELECT * FROM protocols ORDER BY priority ASC"
                if not include_inactive:
                    q = "SELECT * FROM protocols WHERE active=1 ORDER BY priority ASC"
                rows = conn.execute(q).fetchall()
                return [self._row_to_dict(r) for r in rows]
        except Exception as exc:
            logger.warning("ProtocolStore.list_all error: %s", exc)
            return []

    def get_stats(self) -> dict:
        """Summary stats."""
        try:
            with self._connect() as conn:
                total = conn.execute("SELECT COUNT(*) FROM protocols").fetchone()[0]
                active = conn.execute("SELECT COUNT(*) FROM protocols WHERE active=1").fetchone()[0]
                by_domain = conn.execute(
                    "SELECT domain, COUNT(*) FROM protocols GROUP BY domain"
                ).fetchall()
                return {
                    "total": total,
                    "active": active,
                    "by_domain": dict(by_domain),
                }
        except Exception as exc:
            logger.warning("ProtocolStore.get_stats error: %s", exc)
            return {}

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _row_to_dict(self, row: sqlite3.Row) -> dict:
        """Convert a sqlite3.Row to a dict with trigger_keywords parsed from JSON."""
        d = dict(row)
        try:
            d["trigger_keywords"] = json.loads(d.get("trigger_keywords") or "[]")
        except (json.JSONDecodeError, TypeError):
            d["trigger_keywords"] = []
        d["active"] = bool(d.get("active", 1))
        return d

    def self_test(self) -> bool:
        """In-memory smoke test. Returns True if all operations succeed."""
        import tempfile
        import os
        _tf = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp = _tf.name
        _tf.close()
        try:
            store = ProtocolStore(db_path=tmp)
            pid = store.add(
                name="Test Protocol",
                rule="Never do bad things",
                domain="test",
                priority=2,
                keywords=["bad", "wrong"],
            )
            assert pid
            proto = store.get(pid)
            assert proto and proto["name"] == "Test Protocol"
            results = store.retrieve("this is bad and wrong", domain="test")
            assert any(p["id"] == pid for p in results)
            updated = store.update(pid, priority=1)
            assert updated
            stats = store.get_stats()
            assert stats["total"] == 1
            deleted = store.delete(pid)
            assert deleted
            assert store.get(pid) is None
            return True
        except Exception as exc:
            logger.error("ProtocolStore.self_test failed: %s", exc)
            return False
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass


# ─── Seed Protocols ───────────────────────────────────────────────────────────

SEED_PROTOCOLS = [
    {
        "name": "No Irreversible Actions",
        "rule": "Never recommend or execute an irreversible action (delete, send, publish, pay) without explicitly flagging it as irreversible and getting confirmation.",
        "domain": "general",
        "priority": 1,
        "keywords": ["delete", "remove", "send", "publish", "pay", "transfer", "drop", "destroy"],
    },
    {
        "name": "Personal Privacy",
        "rule": "Protect personal and family information. Do not share names, contact details, schedules, or private data with external services or untrusted parties without explicit permission.",
        "domain": "privacy",
        "priority": 1,
        "keywords": ["personal", "private", "family", "contact", "address", "schedule", "photo"],
    },
    {
        "name": "Financial Caution",
        "rule": "Before recommending any financial action, confirm the user has considered downside risk. Never recommend betting or investing irreversible capital.",
        "domain": "finance",
        "priority": 2,
        "keywords": ["invest", "bet", "trade", "buy", "sell", "money", "dollar", "crypto", "stock"],
    },
    {
        "name": "Hive Routing First",
        "rule": "Before spawning a local subagent for any task, check if a hive bot (distributed agent network) can handle it. Prefer delegating code, research, and data tasks to specialized bots.",
        "domain": "general",
        "priority": 3,
        "keywords": ["research", "build", "code", "implement", "deploy", "analyze"],
    },
    # ─── CosmoDestiny Protocols (Manolo Remiddi, 2026-03-05) ───────────────────
    {
        "name": "Completion Skepticism",
        "rule": "Never trust a bare 'done' or 'fixed' response — from bots, subagents, or self. Always require evidence of completion: file exists, command output, test passes, curl response, or diff. If evidence is absent, explicitly ask for it before marking a task complete.",
        "domain": "general",
        "priority": 1,
        "keywords": ["done", "fixed", "complete", "finished", "saved", "deployed", "applied", "resolved", "committed"],
    },
    {
        "name": "Resist Binary Thinking",
        "rule": "When a question or situation presents exactly two options, pause before accepting the binary frame. Reality is almost never binary. Always consider: what is option C? What is option D? What is the human locked inside that they cannot see? Surface at least one non-binary alternative before proceeding.",
        "domain": "general",
        "priority": 2,
        "keywords": ["or", "either", "choice", "option", "versus", "vs", "decide", "pick", "choose", "which"],
    },
    {
        "name": "Dissonance as Compass",
        "rule": "When the user or Lilu expresses discomfort, friction, or 'something feels off' — do not proceed or dismiss. Treat dissonance as a compass pointing at something important. Stop and investigate: what specifically creates the friction? What is being missed? Explore before continuing.",
        "domain": "general",
        "priority": 2,
        "keywords": ["feels off", "not happy", "something wrong", "not right", "uncomfortable", "friction", "dissonance", "doesn't feel", "not sure about", "hesitant"],
    },
    {
        "name": "Gardener Mindset",
        "rule": "Before producing an output (plan, implementation, document), tend the soil first: gather constraints, risks, missing context, user intent, and open questions. The output (the plant) should emerge from prepared conditions — not be forced before the ground is ready. When asked to build or plan something, first confirm: do we have everything we need?",
        "domain": "general",
        "priority": 2,
        "keywords": ["build", "create", "plan", "design", "implement", "write", "generate", "make"],
    },
]


def seed_protocols(store: Optional[ProtocolStore] = None) -> int:
    """Seed default protocols if not already present. Returns count seeded."""
    if store is None:
        store = ProtocolStore()
    existing = {p["name"] for p in store.list_all(include_inactive=True)}
    seeded = 0
    for proto in SEED_PROTOCOLS:
        if proto["name"] not in existing:
            store.add(**proto)
            seeded += 1
            logger.info("Seeded protocol: %s", proto["name"])
    return seeded


if __name__ == "__main__":
    import sys
    store = ProtocolStore()
    if "--self-test" in sys.argv:
        ok = store.self_test()
        print("self_test:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    if "--seed" in sys.argv:
        n = seed_protocols(store)
        print(f"Seeded {n} protocols")
        stats = store.get_stats()
        print("Stats:", stats)
