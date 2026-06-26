# Persona-aware unified memory — depends on core
import json
from enum import Enum
from pathlib import Path
from typing import Optional

from .core import *


def detect_persona() -> str:
    """Detect current agent persona from environment or workspace path."""
    import os
    persona = os.environ.get("OPENCLAW_AGENT_ID", "").strip().lower()
    if persona in ("main", "tseng", "wukong", "bajie", "bailong", "shaseng"):
        return persona
    cwd = os.getcwd()
    for p in ("workspace-tseng", "workspace-wukong", "workspace-bajie",
              "workspace-bailong", "workspace-shaseng"):
        if p in cwd:
            return p.replace("workspace-", "")
    return "main"


def get_workspace_for_persona(persona: str) -> Path:
    """Return the workspace path for a given persona."""
    home = Path.home()
    if persona == "main":
        return home / ".openclaw" / "workspace"
    return home / ".openclaw" / f"workspace-{persona}"


# ---- OpenClaw SQLite Memory -----------------------------------------------

class OpenClawMemory:
    """Read from OpenClaw's default SQLite memory store."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace

    def _get_db_path(self) -> Optional[Path]:
        memory_dir = self.workspace / "memory"
        if not memory_dir.exists():
            return None
        p = memory_dir / f"{detect_persona()}.sqlite"
        if p.exists():
            return p
        main = memory_dir / "main.sqlite"
        if main.exists():
            return main
        return None

    def is_available(self) -> bool:
        return self._get_db_path() is not None

    def search(self, query: str, top_k: int = 5) -> list[str]:
        db_path = self._get_db_path()
        if not db_path:
            return []
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content FROM messages WHERE content LIKE ? ORDER BY created_at DESC LIMIT ?",
                (f"%{query}%", top_k)
            )
            results = [row[0] for row in cursor.fetchall() if row[0]]
            conn.close()
            return results
        except Exception:
            return []

    def get_recent(self, limit: int = 20) -> list[dict]:
        db_path = self._get_db_path()
        if not db_path:
            return []
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content, created_at FROM messages ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
            results = [
                {"content": row[0], "created_at": row[1]}
                for row in cursor.fetchall() if row[0]
            ]
            conn.close()
            return results
        except Exception:
            return []

    def get_preferences(self, persona: str) -> dict[str, list[str]]:
        memories = self.get_recent(limit=50)
        disliked, liked = [], []
        for m in memories:
            content = (m.get("content") or "")[:200].lower()
            if any(kw in content for kw in ["不要", "别", "拒绝", "不喜欢", "讨厌", "反感"]):
                disliked.append(content)
            elif any(kw in content for kw in ["喜欢", "很好", "继续保持", "需要", "想要", "可以"]):
                liked.append(content)
        return {"liked": liked[:5], "disliked": disliked[:5]}


# ---- HawkBridge LanceDB Memory -------------------------------------------

class HawkBridgeMemory:
    """Read from hawk-bridge's LanceDB vector store."""

    LANCEDB_CANDIDATES = [
        "skills/hawk-bridge/python/lancedb",
        "skills/hawk-bridge/lancedb",
        "skills/hawk-bridge/python/.lancedb",
        "hawk-bridge/lancedb",
        "hawk-bridge/.lancedb",
    ]

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.db_path = self._find_lancedb()

    def _find_lancedb(self) -> Optional[Path]:
        for rel in self.LANCEDB_CANDIDATES:
            p = self.workspace / rel
            if p.exists():
                return p
        return None

    def is_available(self) -> bool:
        return self.db_path is not None

    def search(self, query: str, persona: str, top_k: int = 5) -> list[str]:
        if not self.is_available():
            return []
        try:
            import lancedb
            db = lancedb.connect(str(self.db_path))
            for table_name in ("memories", "memory", "default", "embeddings"):
                try:
                    tbl = db.open_table(table_name)
                    try:
                        results = (
                            tbl.search(query)
                            .where(f"persona = '{persona}'")
                            .limit(top_k)
                            .to_list()
                        )
                    except Exception:
                        results = tbl.search(query).limit(top_k).to_list()
                    texts = [r.get("text", r.get("content", "")) for r in results]
                    return [t for t in texts if t]
                except Exception:
                    continue
            return []
        except Exception:
            return []

    def get_preferences(self, persona: str) -> dict[str, list[str]]:
        disliked_queries = [f"{persona} 不要", f"{persona} 拒绝", f"{persona} 不喜欢", "不要 做"]
        liked_queries = [f"{persona} 喜欢", f"{persona} 需要", "很好 继续保持"]
        disliked, liked = set(), set()
        for q in disliked_queries:
            for r in self.search(q, persona, top_k=3):
                if r:
                    disliked.add(r[:200])
        for q in liked_queries:
            for r in self.search(q, persona, top_k=3):
                if r:
                    liked.add(r[:200])
        return {"liked": list(liked)[:5], "disliked": list(disliked)[:5]}


# ---- Unified Memory Retriever -------------------------------------------

class MemorySource(Enum):
    AUTO = "auto"
    OPENCLAW = "openclaw"
    HAWKBRIDGE = "hawkbridge"
    BOTH = "both"


class PersonaAwareMemory:
    """
    Unified memory retrieval with:
    - Persona-based workspace selection
    - OpenClaw SQLite + hawk-bridge LanceDB dual support
    - Graceful degradation (openclaw primary, hawkbridge supplement)
    - CLI override for recall persona and memory source
    """

    WORKSPACE_FILES = ("SOUL.md", "USER.md", "IDENTITY.md", "MEMORY.md", "AGENTS.md", "TOOLS.md")

    def __init__(self, recall_persona: str = "", memory_source: str = "auto") -> None:
        self.effective_persona = (recall_persona.strip().lower() or detect_persona())
        if self.effective_persona == "master":
            self.effective_persona = "main"
        self.workspace = get_workspace_for_persona(self.effective_persona)
        self.context_persona = self.effective_persona
        self.source = MemorySource(memory_source)
        self.openclaw_mem = OpenClawMemory(self.workspace)
        self.hawkbridge_mem = HawkBridgeMemory(self.workspace)
        self._use_openclaw = self.source in (MemorySource.OPENCLAW, MemorySource.AUTO)
        self._use_hawkbridge = self.source in (MemorySource.HAWKBRIDGE, MemorySource.AUTO)
        if self.source == MemorySource.AUTO:
            self._use_openclaw = True
            self._use_hawkbridge = self.hawkbridge_mem.is_available()

    def load_context_files(self) -> dict[str, str]:
        ctx = {}
        for fname in self.WORKSPACE_FILES:
            fp = self.workspace / fname
            if fp.exists() and fp.is_file():
                try:
                    ctx[fname] = fp.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    ctx[fname] = ""
            else:
                ctx[fname] = ""
        return ctx

    def get_context_summary(self) -> str:
        ctx = self.load_context_files()
        labels = {
            "SOUL.md": "价值观/风格",
            "USER.md": "偏好/习惯",
            "IDENTITY.md": "项目定位",
            "MEMORY.md": "长期记忆",
            "AGENTS.md": "Agent团队架构",
            "TOOLS.md": "工具配置",
        }
        lines = [f"【{self.context_persona} 上下文】"]
        for fname, label in labels.items():
            content = ctx.get(fname, "")
            if content:
                snippet = content[:250].replace("\n", " ").strip()
                lines.append(f"\n{label}（{fname}）: {snippet}")
            else:
                lines.append(f"\n{label}（{fname}）: 未配置")
        return "\n".join(lines)

    def get_preferences(self) -> dict[str, list[str]]:
        oc_prefs = {"liked": [], "disliked": []}
        hb_prefs = {"liked": [], "disliked": []}
        if self._use_openclaw and self.openclaw_mem.is_available():
            oc_prefs = self.openclaw_mem.get_preferences(self.context_persona)
        elif self._use_hawkbridge and self.hawkbridge_mem.is_available():
            hb_prefs = self.hawkbridge_mem.get_preferences(self.context_persona)
        if self.source == MemorySource.BOTH:
            return {
                "liked": oc_prefs.get("liked", []) + hb_prefs.get("liked", []),
                "disliked": oc_prefs.get("disliked", []) + hb_prefs.get("disliked", []),
            }
        if self._use_openclaw and (oc_prefs.get("liked") or oc_prefs.get("disliked")):
            return oc_prefs
        if hb_prefs.get("liked") or hb_prefs.get("disliked"):
            return hb_prefs
        return {"liked": [], "disliked": []}

    def search(self, query: str, top_k: int = 5) -> list[str]:
        results = []
        if self._use_openclaw and self.openclaw_mem.is_available():
            results.extend(self.openclaw_mem.search(query, top_k))
        if self._use_hawkbridge and self.hawkbridge_mem.is_available():
            results.extend(self.hawkbridge_mem.search(query, self.context_persona, top_k))
        seen = set()
        deduped = []
        for r in results:
            if r not in seen:
                seen.add(r)
                deduped.append(r)
        return deduped[:top_k]
