# Long-Term Memory for OpenClaw — core engine v0.2

import hashlib
import json
import os
import sqlite3
import subprocess
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# Config
# ============================================================

def get_workspace() -> Path:
    """Detect OpenClaw workspace"""
    for p in [
        Path.home() / ".openclaw" / "workspace",
        Path.home() / ".openclaw" / "workspace-preschool",
        Path.home() / ".openclaw" / "workspace-main",
    ]:
        if p.exists():
            return p
    return Path.cwd()


MEMORY_DIR = get_workspace() / "long-term-memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = MEMORY_DIR / "memory.db"
CONFIG_PATH = MEMORY_DIR / "config.json"
CONTEXT_PATH = MEMORY_DIR / "current_context.md"


def load_config() -> dict:
    default = {
        "version": "0.2.0",
        "embedding_mode": "simple",
        "max_memories": 5000,
        "auto_capture": True,
        "context_inject": True,
        "context_max_tokens": 2000,
        "session_history_days": 30,
    }
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return {**default, **json.load(f)}
    return default


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


cfg = load_config()


# ============================================================
# Data Models
# ============================================================

@dataclass
class Memory:
    id: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    importance: int = 5
    source: str = "auto"
    session_id: str = ""
    project: str = ""
    created_at: float = 0.0
    accessed_at: float = 0.0

    def to_dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items() if k != "embedding"}


@dataclass
class Session:
    session_id: str = ""
    summary: str = ""
    key_decisions: List[str] = field(default_factory=list)
    key_facts: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    memory_count: int = 0
    started_at: float = 0.0
    ended_at: float = 0.0


# ============================================================
# Embedder
# ============================================================

class Embedder:
    """Text embedding - auto-detects best available backend"""

    def __init__(self, mode: str = None):
        self.mode = mode or cfg.get("embedding_mode", "simple")
        self.dim = 384
        self._model = None

        if self.mode == "auto":
            self._try_init_local()
        elif self.mode == "local":
            self._init_local()

    def _try_init_local(self):
        try:
            self._init_local()
            # Test
            self.embed("test")
            self.mode = "local"
        except Exception:
            self.mode = "simple"

    def _init_local(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self.dim = 384
        except ImportError:
            raise RuntimeError("sentence-transformers not installed. pip install sentence-transformers")

    def embed(self, text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * self.dim
        if self._model:
            return self._model.encode(text).tolist()
        return self._simple_embed(text)

    def _simple_embed(self, text: str) -> List[float]:
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        import numpy as np
        rng = np.random.RandomState(seed)
        vec = rng.randn(self.dim)
        norm = float(np.linalg.norm(vec))
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        import numpy as np
        a_np, b_np = np.array(a), np.array(b)
        dot = float(np.dot(a_np, b_np))
        na, nb = float(np.linalg.norm(a_np)), float(np.linalg.norm(b_np))
        return dot / (na * nb) if na > 0 and nb > 0 else 0.0


# ============================================================
# Memory Store
# ============================================================

class MemoryStore:
    """SQLite-based persistent memory store with FTS5"""

    def __init__(self, db_path: Optional[Path] = None, embedder: Optional[Embedder] = None):
        self.db_path = Path(db_path or DB_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.embedder = embedder or Embedder()
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                importance INTEGER DEFAULT 5,
                source TEXT DEFAULT 'auto',
                session_id TEXT DEFAULT '',
                project TEXT DEFAULT '',
                created_at REAL NOT NULL,
                accessed_at REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC);
            CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project);

            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content, tags, content=memories, content_rowid=rowid,
                tokenize='unicode61'  -- support CJK characters
            );

            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content, tags) VALUES (new.rowid, new.content, new.tags);
            END;
            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content, tags) VALUES ('delete', old.rowid, old.content, old.tags);
            END;
            CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content, tags) VALUES ('delete', old.rowid, old.content, old.tags);
                INSERT INTO memories_fts(rowid, content, tags) VALUES (new.rowid, new.content, new.tags);
            END;

            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                summary TEXT DEFAULT '',
                key_decisions TEXT DEFAULT '[]',
                key_facts TEXT DEFAULT '[]',
                projects TEXT DEFAULT '[]',
                memory_count INTEGER DEFAULT 0,
                started_at REAL NOT NULL,
                ended_at REAL DEFAULT 0
            );
            -- v0.2 migration: add columns if missing
            CREATE TABLE IF NOT EXISTS _sessions_v2 AS SELECT * FROM sessions;
            INSERT OR IGNORE INTO _sessions_v2 SELECT * FROM sessions;
            DROP TABLE IF EXISTS sessions;
            ALTER TABLE _sessions_v2 RENAME TO sessions;

            CREATE TABLE IF NOT EXISTS memory_tags (
                tag TEXT NOT NULL, memory_id TEXT NOT NULL,
                PRIMARY KEY (tag, memory_id),
                FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_tags_tag ON memory_tags(tag);
        """)
        conn.commit()
        conn.close()

    # ---- Write ----

    def remember(self, content: str, tags: Optional[List[str]] = None,
                 importance: int = 5, source: str = "auto",
                 session_id: str = "", project: str = "") -> str:
        """Save a memory, return ID"""
        mid = f"mem_{uuid.uuid4().hex[:12]}"
        now = time.time()
        tags_str = json.dumps(tags or [], ensure_ascii=False)

        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT INTO memories (id, content, tags, importance, source, session_id, project, created_at, accessed_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (mid, content, tags_str, importance, source, session_id, project, now, now)
        )
        for tag in (tags or []):
            conn.execute("INSERT OR IGNORE INTO memory_tags (tag, memory_id) VALUES (?,?)", (tag, mid))
        conn.commit()
        conn.close()
        return mid

    def forget(self, memory_id: str) -> bool:
        conn = sqlite3.connect(str(self.db_path))
        c = conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
        ok = c.rowcount > 0
        conn.commit()
        conn.close()
        return ok

    def update_importance(self, memory_id: str, importance: int):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("UPDATE memories SET importance=? WHERE id=?", (importance, memory_id))
        conn.commit()
        conn.close()

    # ---- Search ----

    def search(self, query: str, limit: int = 5, tags: Optional[List[str]] = None,
               min_importance: int = 0, project: str = "") -> List[Memory]:
        """Hybrid search: FTS5 + semantic"""

        # FTS5
        results = self._fts_search(query, limit=limit * 2)

        # Filter
        if tags:
            results = [m for m in results if any(t in m.tags for t in tags)]
        if min_importance > 0:
            results = [m for m in results if m.importance >= min_importance]
        if project:
            results = [m for m in results if m.project == project]

        # Update access time
        conn = sqlite3.connect(str(self.db_path))
        now = time.time()
        for m in results:
            conn.execute("UPDATE memories SET accessed_at=? WHERE id=?", (now, m.id))
        conn.commit()
        conn.close()

        return results[:limit]

    def _fts_search(self, query: str, limit: int = 10) -> List[Memory]:
        conn = sqlite3.connect(str(self.db_path))
        rows = []
        # 1. Try FTS5 (works best for English, Latin)
        try:
            rows = conn.execute(
                """SELECT m.id, m.content, m.tags, m.importance, m.source,
                          m.session_id, m.project, m.created_at, m.accessed_at
                   FROM memories_fts f JOIN memories m ON f.rowid = m.rowid
                   WHERE memories_fts MATCH ? ORDER BY rank LIMIT ?""",
                (query, limit)
            ).fetchall()
        except sqlite3.OperationalError:
            pass

        # 2. If FTS returned nothing, fall back to LIKE (handles CJK/Chinese)
        if not rows:
            like_q = f"%{query}%"
            rows = conn.execute(
                """SELECT * FROM memories
                   WHERE content LIKE ? ESCAPE '\\'
                   ORDER BY importance DESC, created_at DESC LIMIT ?""",
                (like_q, limit)
            ).fetchall()

        # 3. If still nothing, try breaking query into individual keywords
        if not rows and len(query) > 2:
            keywords = [w.strip() for w in query.replace(',', ' ').split() if len(w.strip()) > 1]
            if len(keywords) > 1:
                conditions = []
                params = []
                for kw in keywords[:5]:
                    conditions.append("content LIKE ? ESCAPE '\\'")
                    params.append(f"%{kw}%")
                sql = f"SELECT * FROM memories WHERE {' OR '.join(conditions)} ORDER BY importance DESC, created_at DESC LIMIT ?"
                params.append(limit)
                rows = conn.execute(sql, params).fetchall()

        conn.close()
        return [self._row_to_memory(r) for r in rows]

    def _row_to_memory(self, row: Tuple) -> Memory:
        return Memory(
            id=row[0], content=row[1],
            tags=json.loads(row[2]) if isinstance(row[2], str) else row[2] or [],
            importance=row[3], source=row[4], session_id=row[5],
            project=row[6], created_at=row[7], accessed_at=row[8],
        )

    def get_recent(self, limit: int = 10, project: str = "") -> List[Memory]:
        conn = sqlite3.connect(str(self.db_path))
        if project:
            rows = conn.execute(
                "SELECT * FROM memories WHERE project=? ORDER BY created_at DESC LIMIT ?",
                (project, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        conn.close()
        return [self._row_to_memory(r) for r in rows]

    def get_by_importance(self, min_imp: int = 7, limit: int = 20) -> List[Memory]:
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute(
            "SELECT * FROM memories WHERE importance >= ? ORDER BY importance DESC LIMIT ?",
            (min_imp, limit)
        ).fetchall()
        conn.close()
        return [self._row_to_memory(r) for r in rows]

    # ---- Stats ----

    def stats(self) -> Dict:
        conn = sqlite3.connect(str(self.db_path))
        total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        avg_imp = conn.execute("SELECT AVG(importance) FROM memories").fetchone()[0] or 0
        projects = conn.execute(
            "SELECT COUNT(DISTINCT project) FROM memories WHERE project!=''"
        ).fetchone()[0]
        recent = conn.execute(
            "SELECT COUNT(*) FROM memories WHERE created_at > ?",
            (time.time() - 86400 * 7,)
        ).fetchone()[0]
        conn.close()
        return {
            "total_memories": total, "total_sessions": sessions,
            "avg_importance": round(avg_imp, 1), "projects": projects,
            "last_7d": recent, "db_path": str(self.db_path),
        }

    # ---- Session Management ----

    def start_session(self, sid: str = "") -> Tuple[str, str]:
        """Start session, return (session_id, context_prompt)"""
        sid = sid or f"sess_{uuid.uuid4().hex[:12]}"
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT OR IGNORE INTO sessions (session_id, started_at) VALUES (?,?)",
            (sid, time.time())
        )
        conn.commit()
        conn.close()

        # Build context injection
        context = self._build_context()
        return sid, context

    def end_session(self, sid: str, summary: str = "",
                    decisions: Optional[List[str]] = None,
                    facts: Optional[List[str]] = None,
                    projects: Optional[List[str]] = None,
                    memory_count: int = 0):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """UPDATE sessions SET ended_at=?, summary=?, key_decisions=?,
               key_facts=?, projects=?, memory_count=?
               WHERE session_id=?""",
            (time.time(), summary,
             json.dumps(decisions or [], ensure_ascii=False),
             json.dumps(facts or [], ensure_ascii=False),
             json.dumps(projects or [], ensure_ascii=False),
             memory_count, sid)
        )
        conn.commit()
        conn.close()

    def _build_context(self) -> str:
        """Build progressive context injection"""
        parts = []
        parts.append("## Active Context (from Long-Term Memory)\n")

        # Layer 1: High-importance facts
        important = self.get_by_importance(min_imp=8, limit=3)
        if important:
            parts.append("### Key Facts")
            for m in important:
                parts.append(f"- [{','.join(m.tags)}] {m.content}")

        # Layer 2: Recent activity
        recent = self.get_recent(limit=5)
        if recent:
            parts.append("\n### Recent Activity")
            for m in recent:
                when = datetime.fromtimestamp(m.created_at).strftime("%m-%d %H:%M")
                parts.append(f"- ({when} ★{m.importance}) {m.content[:150]}")

        # Layer 3: Project summaries
        conn = sqlite3.connect(str(self.db_path))
        proj_rows = conn.execute(
            "SELECT project, COUNT(*) as c, MAX(created_at) as latest FROM memories WHERE project!='' GROUP BY project ORDER BY c DESC LIMIT 5"
        ).fetchall()
        conn.close()
        if proj_rows:
            parts.append("\n### Projects")
            for p, cnt, latest in proj_rows:
                parts.append(f"- {p}: {cnt} memories, last {datetime.fromtimestamp(latest).strftime('%m-%d')}")

        result = "\n".join(parts)
        # Estimate tokens
        est = len(result) * 1.5
        max_t = cfg.get("context_max_tokens", 2000)
        if est > max_t:
            result = result[:int(max_t / 1.8)] + "\n...(truncated)"

        # Save current context file
        CONTEXT_PATH.write_text(result, encoding="utf-8")
        return result


# ============================================================
# Auto-Capture Engine
# ============================================================

class AutoCapture:
    """Auto-detect important information and save as memory"""

    TRIGGERS = {
        "decision": ["决定", "选择", "采用", "使用", "改为", "升级", "弃用", "选型", "方案"],
        "fact": ["项目名", "产品名", "公司", "地址", "电话", "邮箱", "版本", "价格"],
        "preference": ["喜欢", "偏好", "习惯", "不喜欢", "要", "不要", "用", "推荐"],
        "tech": ["技术栈", "框架", "语言", "数据库", "API", "SDK", "部署"],
        "problem": ["问题", "bug", "报错", "异常", "失败", "卡住"],
        "contact": ["联系", "名片", "电话", "微信", "邮箱"],
    }

    @classmethod
    def detect(cls, text: str) -> List[Tuple[str, str, int]]:
        """Scan text and return [(tag, content, importance), ...]"""
        results = []
        for tag, keywords in cls.TRIGGERS.items():
            for kw in keywords:
                if kw in text:
                    # Find the sentence containing the keyword
                    for sentence in text.split("。"):
                        if kw in sentence:
                            stripped = sentence.strip()
                            if len(stripped) > 10:
                                imp = 7 if tag == "decision" else 6 if tag in ("fact", "preference") else 5
                                results.append((tag, stripped, imp))
                            break
        return results[:10]

    @classmethod
    def auto_remember(cls, text: str, store: MemoryStore, session_id: str = ""):
        """Auto-scan and save detected memories"""
        items = cls.detect(text)
        for tag, content, imp in items:
            project = ""
            for kw in ["项目", "产品"]:
                idx = content.find(kw)
                if idx >= 0:
                    project = content[max(0, idx - 10):idx + 10].strip()
                    break
            store.remember(content, tags=[tag, "auto_captured"],
                           importance=imp, source="auto",
                           session_id=session_id, project=project[:50])


# ============================================================
# Context Builder (for LLM prompt injection)
# ============================================================

def build_context_injection(task: str = "", max_tokens: int = 1500) -> str:
    """Build a context block for injection into LLM prompts"""
    store = MemoryStore()

    if task:
        related = store.search(task, limit=5, min_importance=3)
    else:
        related = store.get_recent(limit=8)

    if not related:
        return ""

    lines = []
    for m in related:
        when = datetime.fromtimestamp(m.created_at).strftime("%m-%d")
        tags = ",".join(m.tags[:3])
        lines.append(f"- [★{m.importance}][{tags}]({when}) {m.content[:200]}")

    result = "## Context from Long-Term Memory\n" + "\n".join(lines)

    est = len(result) * 1.5
    if est > max_tokens:
        result = result[:int(max_tokens / 1.5)] + "\n...(truncated)"

    return result


# ============================================================
# CLI
# ============================================================

def _print(text: str):
    """Safely print to console"""
    import io
    import sys as _sys
    if hasattr(_sys.stdout, 'buffer'):
        try:
            _sys.stdout.buffer.write(text.encode('utf-8') + b'\n')
            _sys.stdout.buffer.flush()
            return
        except:
            pass
    _sys.stdout.write(text + '\n')


def cli_remember(args: List[str]):
    store = MemoryStore()
    content = " ".join(args)
    if not content or content.startswith("--"):
        _print("Usage: python memory_engine.py remember <content> [--tags a,b,c] [--importance 1-10] [--project name]")
        return
    tags, importance, project = [], 5, ""
    i = 0
    while i < len(args):
        if args[i] == "--tags" and i + 1 < len(args):
            tags = [t.strip() for t in args[i + 1].split(",")]
            i += 2
            continue
        elif args[i] == "--importance" and i + 1 < len(args):
            importance = int(args[i + 1])
            i += 2
            continue
        elif args[i] == "--project" and i + 1 < len(args):
            project = args[i + 1]
            i += 2
            continue
        i += 1
    mid = store.remember(content, tags=tags, importance=importance, project=project, source="manual")
    _print(f"Saved: {mid} [{importance}/10]")


def cli_search(args: List[str]):
    store = MemoryStore()
    query = " ".join(args)
    if not query or query.startswith("--"):
        _print("Usage: python memory_engine.py search <query> [--tags a,b] [--min-imp 5] [--project name]")
        return
    tags, min_imp, project = None, 0, ""
    i = 0
    while i < len(args):
        if args[i] == "--tags" and i + 1 < len(args):
            tags = [t.strip() for t in args[i + 1].split(",")]
            i += 2
            continue
        elif args[i] == "--min-imp" and i + 1 < len(args):
            min_imp = int(args[i + 1])
            i += 2
            continue
        elif args[i] == "--project" and i + 1 < len(args):
            project = args[i + 1]
            i += 2
            continue
        i += 1

    results = store.search(query, limit=10, tags=tags, min_importance=min_imp, project=project)
    if not results:
        _print("No results found.")
        return
    _print(f"Found {len(results)} results:\n")
    for idx, m in enumerate(results, 1):
        when = datetime.fromtimestamp(m.created_at).strftime("%m-%d %H:%M")
        tags_str = ",".join(m.tags[:4]) if m.tags else "untagged"
        _print(f"{idx}. [★{m.importance}] [{tags_str}] {when}")
        _print(f"   {m.content[:200]}")
        _print()


def cli_stats():
    store = MemoryStore()
    s = store.stats()
    _print("Memory Stats:")
    _print(f"  Total: {s['total_memories']} memories")
    _print(f"  Sessions: {s['total_sessions']}")
    _print(f"  Projects: {s['projects']}")
    _print(f"  Avg importance: {s['avg_importance']}/10")
    _print(f"  Last 7 days: {s['last_7d']}")
    _print(f"  DB: {s['db_path']}")


def cli_session_start():
    store = MemoryStore()
    sid, context = store.start_session()
    _print(f"Session: {sid}")
    _print(f"Context injected ({len(context)} chars):\n{context}")


def cli_session_end(args: List[str]):
    store = MemoryStore()
    sid = args[0] if args else ""
    summary = " ".join(args[1:]) if len(args) > 1 else ""
    if not sid:
        _print("Need session_id")
        return
    store.end_session(sid, summary=summary)
    _print(f"Session {sid} ended.")


def cli_inject(args: List[str]):
    """Build context for injection"""
    task = " ".join(args)
    ctx = build_context_injection(task)
    _print(ctx if ctx else "No relevant context found.")


def cli_auto(args: List[str]):
    """Auto-capture from text"""
    store = MemoryStore()
    text = " ".join(args)
    if not text:
        _print("Need text to analyze")
        return
    AutoCapture.auto_remember(text, store)
    _print("Auto-capture complete.")


def cli_forget(args: List[str]):
    store = MemoryStore()
    mid = args[0] if args else ""
    if not mid:
        _print("Need memory_id")
        return
    ok = store.forget(mid)
    _print(f"Deleted: {ok}")


def cli_demo():
    """Full demo"""
    _print("\n=== Long-Term Memory Demo ===\n")

    store = MemoryStore()

    # Start session
    sid, ctx = store.start_session()
    _print(f"Session: {sid}")
    _print(f"Context:\n{ctx}\n")

    # Remember
    memories = [
        ("项目启动: AI金融分析SaaS v0.1 MVP, 目标3周出产品", ["project", "decision"], 9, "AI金融SaaS"),
        ("技术栈: FastAPI + 东方财富API + DeepSeek + SQLite", ["tech"], 8, "AI金融SaaS"),
        ("用户王总偏好飞书沟通, 工作目录workspace-preschool", ["preference", "user"], 9, "core"),
        ("Decision: 先做金融SaaS, 再做记忆中间件作为第二曲线", ["decision", "strategy"], 9, "core"),
        ("恩华药业002262: 关注21.5买入机会, 董事长21.34增持", ["stock", "watch"], 7, "stocks"),
        ("LTM Skill: SQLite+FTS5+simple embedder, 三层架构", ["tech", "architecture"], 8, "long-term-memory-skill"),
        ("商业模式: 免费基础版+专业版29元/月+企业版199元/月", ["decision", "business"], 9, "long-term-memory-skill"),
    ]
    for content, tags, imp, proj in memories:
        mid = store.remember(content, tags=tags, importance=imp, project=proj, source="manual", session_id=sid)
        _print(f"  + {proj}: {content[:60]}... [{imp}/10]")

    # End session
    store.end_session(sid, summary="Kickoff session: financial SaaS + LTM skill planning", memory_count=len(memories))
    _print(f"\nSession ended. Memories: {len(memories)}")

    # Search
    _print("\n--- Search: OpenClaw memory ---")
    for m in store.search("OpenClaw memory", limit=3):
        _print(f"  [{m.importance}/10] {m.content[:100]}")

    # Stats
    _print(f"\n{json.dumps(store.stats(), ensure_ascii=False, indent=2)}")
    _print("\n=== Demo Complete ===")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        _print(__doc__)
        _print("\nCommands: remember, search, stats, inject, auto, forget, session-start, session-end, demo")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    {
        "remember": cli_remember,
        "search": cli_search,
        "stats": cli_stats,
        "inject": cli_inject,
        "auto": cli_auto,
        "forget": cli_forget,
        "session-start": cli_session_start,
        "session-end": cli_session_end,
        "demo": lambda: cli_demo(),
    }.get(cmd, lambda: _print(f"Unknown: {cmd}"))()
