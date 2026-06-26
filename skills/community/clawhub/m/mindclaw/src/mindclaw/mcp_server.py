"""
mindclaw.mcp_server — MCP (Model Context Protocol) server for MindClaw.

Exposes all MindClaw capabilities as native MCP tools so any
MCP-compatible agent runtime (Claude Desktop, OpenClaw, etc.)
can call them directly without shell commands.

Usage:
    # Start the server (stdio transport, for Claude Desktop / OpenClaw)
    mindclaw-mcp

    # Register with Claude Desktop automatically
    mindclaw mcp install

    # Register with a custom agent runtime
    mindclaw mcp install --target openClaw

Environment:
    MINDCLAW_DB      Path to SQLite database (default: ~/.mindclaw/memory.db)
    MINDCLAW_AGENT   Default agent namespace for this server instance
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Graceful import of the MCP SDK
# ---------------------------------------------------------------------------

try:
    from mcp.server.fastmcp import FastMCP
    _MCP_AVAILABLE = True
except ImportError:
    _MCP_AVAILABLE = False
    FastMCP = None  # type: ignore

from .capture import AutoCapture
from .context import ContextBuilder, check_conflicts, summarize_cluster
from .graph import KnowledgeGraph
from .search import SearchEngine
from .store import Memory, MemoryStore


# ---------------------------------------------------------------------------
# Server factory
# ---------------------------------------------------------------------------

def _get_store() -> MemoryStore:
    """Create a store using env var > config file > built-in default."""
    from .config import load_config
    cfg = load_config()
    db_path = cfg.effective_db()
    return MemoryStore(db_path=db_path)


def _default_agent() -> str:
    """Resolve agent namespace using env var > config file > empty string."""
    from .config import load_config
    cfg = load_config()
    return cfg.effective_agent()


def _default_workspace() -> Optional[str]:
    """Resolve OpenClaw workspace using env var > config file > None (auto-detect)."""
    from .config import load_config
    cfg = load_config()
    return cfg.effective_workspace()


def create_server() -> Any:
    """Build and return the configured FastMCP server instance."""
    if not _MCP_AVAILABLE:
        raise ImportError(
            "MCP SDK not installed. Run: pip install mindclaw[mcp]"
        )

    mcp = FastMCP(
        "MindClaw",
        instructions=(
            "MindClaw is a persistent memory and knowledge graph tool.\n"
            "Use 'remember' to store important facts, decisions, and preferences.\n"
            "Use 'recall' before answering to retrieve relevant context.\n"
            "Use 'capture' to extract memories from conversation text automatically.\n"
            "Use 'context_block' to get a formatted memory block for your prompt.\n"
            "Agent namespace: set MINDCLAW_AGENT env var to scope memories per agent."
        ),
    )

    # -----------------------------------------------------------------------
    # Tool: remember
    # -----------------------------------------------------------------------

    @mcp.tool()
    def remember(
        content: str,
        category: str = "note",
        tags: str = "",
        importance: float = 0.6,
        source: str = "agent",
        summary: str = "",
        pin: bool = False,
        check_for_conflicts: bool = True,
    ) -> dict:
        """
        Store a new memory permanently.

        Args:
            content: The fact, decision, preference, or note to remember.
            category: One of: fact, decision, preference, error, note, todo, resource.
            tags: Comma-separated tags (e.g. "backend,database").
            importance: Priority score from 0.0 to 1.0 (default 0.6).
            source: Label describing where this memory comes from.
            summary: Optional short summary (auto-derived if empty).
            pin: If True, this memory will never be decayed or auto-archived.
            check_for_conflicts: Warn if a similar but conflicting memory exists.

        Returns:
            dict with memory id, and any detected conflicts.
        """
        store = _get_store()
        agent_id = _default_agent()

        conflicts = []
        if check_for_conflicts:
            reports = check_conflicts(content, store, agent_id=agent_id or None)
            conflicts = [
                {"id": r.conflicting_memory.id, "content": r.conflicting_memory.content,
                 "similarity": r.similarity, "suggestion": r.suggestion}
                for r in reports
            ]

        mem = Memory(
            content=content,
            summary=summary or "",
            category=category,
            tags=[t.strip() for t in tags.split(",") if t.strip()],
            source=source,
            importance=importance,
            agent_id=agent_id,
            pinned=pin,
        )
        store.add(mem)

        return {
            "stored": True,
            "id": mem.id,
            "category": mem.category,
            "importance": mem.importance,
            "pinned": mem.pinned,
            "conflicts_detected": conflicts,
        }

    # -----------------------------------------------------------------------
    # Tool: recall
    # -----------------------------------------------------------------------

    @mcp.tool()
    def recall(
        query: str,
        limit: int = 10,
        category: Optional[str] = None,
        temporal_decay: bool = True,
        mmr: bool = True,
    ) -> list[dict]:
        """
        Search memories using BM25 + Ollama semantic hybrid search.

        Applies temporal decay by default (recent memories rank higher) and
        MMR diversity re-ranking (reduces near-duplicate results) — same
        algorithms used by OpenClaw's native memory_search pipeline.

        Args:
            query: Natural language search query.
            limit: Maximum number of memories to return (default 10).
            category: Optional filter by category (fact/decision/preference/error/note).
            temporal_decay: Boost recent memories, fade old ones (default True).
            mmr: Apply diversity re-ranking to reduce near-duplicate results (default True).

        Returns:
            List of memory dicts ordered by relevance score.
        """
        store = _get_store()
        agent_id = _default_agent()

        engine = SearchEngine(store)
        engine.rebuild()
        results = engine.search(
            query,
            top_k=limit,
            agent_id=agent_id or None,
            temporal_decay=temporal_decay,
            mmr=mmr,
        )

        output = []
        for r in results:
            mem: Memory = r["memory"]
            if category and mem.category != category:
                continue
            output.append({
                "id": mem.id,
                "content": mem.content,
                "summary": mem.summary,
                "category": mem.category,
                "tags": mem.tags,
                "importance": mem.importance,
                "confirmed_count": mem.confirmed_count,
                "pinned": mem.pinned,
                "score": r["score"],
                "age_days": round((time.time() - mem.created_at) / 86400, 1),
                "method": r.get("method", "bm25"),
            })
        return output

    # -----------------------------------------------------------------------
    # Tool: context_block
    # -----------------------------------------------------------------------

    @mcp.tool()
    def context_block(
        query: str,
        max_tokens: int = 2000,
        format: str = "markdown",
    ) -> dict:
        """
        Get a formatted, token-limited memory context block to inject into
        your system prompt before answering a user.

        Args:
            query: What you are about to do or need context for.
            max_tokens: Hard token budget for the block (default 2000).
            format: Output format — "markdown", "plain", or "xml".

        Returns:
            dict with 'text' (ready to inject), token count, and truncation flag.
        """
        store = _get_store()
        agent_id = _default_agent()
        builder = ContextBuilder(store)
        block = builder.build(
            query,
            max_tokens=max_tokens,
            agent_id=agent_id or None,
            format=format,
        )
        return {
            "text": block.text,
            "memories_used": block.memories_used,
            "estimated_tokens": block.estimated_tokens,
            "truncated": block.truncated,
        }

    # -----------------------------------------------------------------------
    # Tool: capture
    # -----------------------------------------------------------------------

    @mcp.tool()
    def capture(
        text: str,
        source: str = "agent",
        dry_run: bool = False,
    ) -> dict:
        """
        Automatically extract and store memorable information from a block of text.
        Detects decisions, errors, preferences, TODOs, URLs, and credentials.

        Args:
            text: Raw text to analyze (conversation, log output, meeting notes, etc.).
            source: Label for where this text came from.
            dry_run: If True, detect but do not save.

        Returns:
            dict with count of captured memories and their details.
        """
        store = _get_store()
        auto = AutoCapture(store)
        results = auto.process(text, source=source, dry_run=dry_run)
        return {
            "captured": len(results),
            "dry_run": dry_run,
            "memories": [
                {
                    "id": r.memory.id,
                    "rule": r.rule_name,
                    "category": r.memory.category,
                    "content": r.memory.content,
                    "confidence": r.confidence,
                }
                for r in results
            ],
        }

    # -----------------------------------------------------------------------
    # Tool: confirm
    # -----------------------------------------------------------------------

    @mcp.tool()
    def confirm(memory_id: str) -> dict:
        """
        Confirm/reinforce an existing memory, boosting its importance score.
        Use this when something is mentioned again or proven correct.

        Args:
            memory_id: The ID of the memory to confirm.

        Returns:
            dict with updated importance and confirmed_count.
        """
        store = _get_store()
        mem = store.confirm(memory_id)
        if mem is None:
            return {"confirmed": False, "error": f"Memory {memory_id} not found"}
        return {
            "confirmed": True,
            "id": mem.id,
            "new_importance": mem.importance,
            "confirmed_count": mem.confirmed_count,
        }

    # -----------------------------------------------------------------------
    # Tool: forget
    # -----------------------------------------------------------------------

    @mcp.tool()
    def forget(memory_id: str, hard: bool = False) -> dict:
        """
        Archive or permanently delete a memory.

        Args:
            memory_id: The ID of the memory to forget.
            hard: If True, permanently delete; otherwise archive (recoverable).

        Returns:
            dict with result status.
        """
        store = _get_store()
        if hard:
            ok = store.delete(memory_id)
            action = "deleted"
        else:
            ok = store.archive(memory_id)
            action = "archived"
        return {"success": ok, "action": action, "id": memory_id}

    # -----------------------------------------------------------------------
    # Tool: link
    # -----------------------------------------------------------------------

    @mcp.tool()
    def link(
        source_id: str,
        target_id: str,
        relation: str = "related_to",
        bidirectional: bool = False,
    ) -> dict:
        """
        Create a relationship edge between two memories in the knowledge graph.

        Args:
            source_id: ID of the source memory.
            target_id: ID of the target memory.
            relation: Relation type (e.g. "depends_on", "causes", "related_to").
            bidirectional: If True, also create the inverse edge.

        Returns:
            dict with created edge IDs.
        """
        store = _get_store()
        graph = KnowledgeGraph(store)
        edge_ids = graph.link(source_id, target_id, relation, bidirectional=bidirectional)
        return {"linked": True, "edge_ids": edge_ids, "relation": relation}

    # -----------------------------------------------------------------------
    # Tool: stats
    # -----------------------------------------------------------------------

    @mcp.tool()
    def stats() -> dict:
        """
        Return statistics about the memory store.
        Useful for monitoring how much the agent has learned over time.
        """
        store = _get_store()
        return store.stats()

    # -----------------------------------------------------------------------
    # Tool: pin / unpin
    # -----------------------------------------------------------------------

    @mcp.tool()
    def pin_memory(memory_id: str) -> dict:
        """
        Pin a memory so it is never decayed or auto-archived.
        Use for critical facts, hard constraints, or permanent preferences.

        Args:
            memory_id: The ID of the memory to pin.
        """
        store = _get_store()
        ok = store.pin(memory_id)
        return {"pinned": ok, "id": memory_id}

    @mcp.tool()
    def unpin_memory(memory_id: str) -> dict:
        """
        Remove the pin from a memory, allowing normal decay to apply.

        Args:
            memory_id: The ID of the memory to unpin.
        """
        store = _get_store()
        ok = store.unpin(memory_id)
        return {"unpinned": ok, "id": memory_id}

    # -----------------------------------------------------------------------
    # Tool: timeline
    # -----------------------------------------------------------------------

    @mcp.tool()
    def timeline(since_hours: float = 24, limit: int = 30) -> list[dict]:
        """
        Return memories created in the last N hours, in chronological order.
        Useful for reconstructing what happened in a recent session.

        Args:
            since_hours: Look back this many hours (default 24).
            limit: Maximum number of memories to return.

        Returns:
            Chronological list of memory dicts.
        """
        store = _get_store()
        agent_id = _default_agent()
        since = time.time() - (since_hours * 3600)
        memories = store.get_timeline(
            since=since,
            agent_id=agent_id or None,
            limit=limit,
        )
        return [
            {
                "id": m.id,
                "content": m.content,
                "category": m.category,
                "importance": m.importance,
                "created_at": m.created_at,
                "age_minutes": round((time.time() - m.created_at) / 60, 1),
            }
            for m in memories
        ]

    # -----------------------------------------------------------------------
    # Tool: consolidate
    # -----------------------------------------------------------------------

    @mcp.tool()
    def consolidate(similarity_threshold: float = 0.85) -> dict:
        """
        Find and merge near-duplicate memories in the store.
        The weaker/older duplicate is archived; the stronger one inherits
        the combined confirmation count.

        Args:
            similarity_threshold: Jaccard similarity above which two memories
                                   are considered duplicates (default 0.85).

        Returns:
            dict with count of memories consolidated.
        """
        store = _get_store()
        agent_id = _default_agent()
        count = store.consolidate_duplicates(
            agent_id=agent_id or None,
            similarity_threshold=similarity_threshold,
        )
        return {"consolidated": count}

    # -----------------------------------------------------------------------
    # Tool: sync_openclaw  (Markdown bridge)
    # -----------------------------------------------------------------------

    @mcp.tool()
    def sync_openclaw(workspace_path: str = "") -> dict:
        """
        Export all MindClaw memories to OpenClaw's MEMORY.md file so they
        become searchable via OpenClaw's native memory_search tool.

        The MindClaw block in MEMORY.md is updated in-place; any content
        the agent has written to the file is preserved.

        Args:
            workspace_path: Path to the OpenClaw workspace directory.
                            Defaults to ~/.openclaw/workspace.

        Returns:
            dict with ok, exported count, path, workspace.
        """
        store = _get_store()
        agent_id = _default_agent()
        result = store.sync_openclaw(
            workspace_path=workspace_path or _default_workspace() or None,
            agent_id=agent_id,
        )
        return result

    # -----------------------------------------------------------------------
    # Tool: setup_mindclaw  (one-shot configuration for agents)
    # -----------------------------------------------------------------------

    @mcp.tool()
    def setup_mindclaw(
        openclaw_workspace: str = "",
        agent_name: str = "",
        db_path: str = "",
        register_openclaw_mcp: bool = True,
        initial_sync: bool = True,
    ) -> dict:
        """
        Configure MindClaw for this agent and register it with OpenClaw.

        Call this tool ONCE after installing MindClaw to set persistent
        defaults so every subsequent tool call works without extra parameters.

        Ask the user (or infer from context) what values to use before calling:
          - openclaw_workspace: path to the OpenClaw workspace directory
          - agent_name: a short name to scope memories to this agent (e.g. 'planner')

        Args:
            openclaw_workspace: Path to the OpenClaw workspace directory.
                                 Defaults to ~/.openclaw/workspace.
            agent_name: Short identifier to namespace memories to this agent.
                        Leave blank to use a shared namespace.
            db_path: Path to the MindClaw SQLite database.
                     Leave blank to use the default (~/.mindclaw/memory.db).
            register_openclaw_mcp: Write MindClaw into OpenClaw's tools registry
                                   so it is always available (default True).
            initial_sync: Export all current memories to MEMORY.md immediately
                          so they are searchable via OpenClaw's memory_search
                          right away (default True).

        Returns:
            dict with 'configured', 'config_path', 'sync' result, 'mcp_registered'.
        """
        from .config import MindClawConfig, save_config, config_path
        from pathlib import Path as _Path

        # Build effective workspace
        ws = (
            str(_Path(openclaw_workspace).expanduser())
            if openclaw_workspace
            else str(_Path.home() / ".openclaw" / "workspace")
        )

        # Built-in default DB
        builtin_db = str(_Path.home() / ".mindclaw" / "memory.db")
        db_save = (
            str(_Path(db_path).expanduser()) if db_path else None
        )
        if db_save == builtin_db:
            db_save = None

        cfg = MindClawConfig(
            db_path=db_save,
            agent_id=agent_name,
            openclaw_workspace=ws,
        )
        saved = save_config(cfg)

        result: dict = {
            "configured": True,
            "config_path": saved,
            "settings": {
                "db_path": db_save or builtin_db,
                "agent_id": agent_name,
                "openclaw_workspace": ws,
            },
        }

        # Register OpenClaw MCP
        mcp_path: Optional[str] = None
        if register_openclaw_mcp:
            try:
                mcp_path = install_openclaw(db_path=db_save, agent_id=agent_name or None)
            except Exception as exc:
                mcp_path = f"error: {exc}"
        result["mcp_registered"] = mcp_path

        # Initial sync
        sync_result: dict = {}
        if initial_sync:
            store = MemoryStore(db_path=db_save)
            sync_result = store.sync_openclaw(
                workspace_path=ws,
                agent_id=agent_name,
            )
        result["sync"] = sync_result

        return result

    # -----------------------------------------------------------------------
    # Tool: import_markdown  (Markdown bridge)
    # -----------------------------------------------------------------------

    @mcp.tool()
    def import_markdown(file_path: str, source: str = "") -> dict:
        """
        Import memories from an OpenClaw Markdown memory file into MindClaw.

        Works with MEMORY.md (long-term curated notes) and daily logs
        (memory/YYYY-MM-DD.md). Bullet-point lines become individual memories;
        heading sections control the category. Deduplicates automatically.

        Args:
            file_path: Path to the Markdown file to import.
            source: Optional label to record as the memory source.

        Returns:
            dict with imported count and file_path.
        """
        store = _get_store()
        agent_id = _default_agent()
        count = store.import_from_markdown(
            file_path,
            agent_id=agent_id,
            source=source or file_path,
        )
        return {"imported": count, "file_path": file_path}

    return mcp


# ---------------------------------------------------------------------------
# Entry point for `mindclaw-mcp` script
# ---------------------------------------------------------------------------

def serve() -> None:
    """Start the MCP server on stdio (for Claude Desktop / OpenClaw)."""
    if not _MCP_AVAILABLE:
        print(
            "ERROR: MCP SDK not installed.\n"
            "Install it with:  pip install mindclaw[mcp]",
            file=sys.stderr,
        )
        sys.exit(1)
    mcp = create_server()
    mcp.run(transport="stdio")


# ---------------------------------------------------------------------------
# Install helpers  (called from cli.py: `mindclaw mcp install`)
# ---------------------------------------------------------------------------

_CLAUDE_DESKTOP_CONFIGS = {
    "win32": Path.home() / "AppData/Roaming/Claude/claude_desktop_config.json",
    "darwin": Path.home() / "Library/Application Support/Claude/claude_desktop_config.json",
    "linux": Path.home() / ".config/claude/claude_desktop_config.json",
}

_OPENCLAW_CONFIG = Path.home() / ".openclaw" / "tools.json"


def _python_executable() -> str:
    return sys.executable


def install_claude_desktop(db_path: Optional[str] = None, agent_id: Optional[str] = None) -> str:
    """
    Write or update the Claude Desktop MCP config to include MindClaw.
    Returns the path that was written.
    """
    platform = sys.platform
    config_path = _CLAUDE_DESKTOP_CONFIGS.get(platform)
    if config_path is None:
        config_path = _CLAUDE_DESKTOP_CONFIGS["linux"]

    config_path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    if config_path.exists():
        try:
            existing = json.loads(config_path.read_text())
        except Exception:
            existing = {}

    env: dict[str, str] = {}
    if db_path:
        env["MINDCLAW_DB"] = db_path
    if agent_id:
        env["MINDCLAW_AGENT"] = agent_id

    entry: dict = {
        "command": _python_executable(),
        "args": ["-m", "mindclaw.mcp_server"],
    }
    if env:
        entry["env"] = env

    existing.setdefault("mcpServers", {})["mindclaw"] = entry
    config_path.write_text(json.dumps(existing, indent=2))
    return str(config_path)


def install_openclaw(db_path: Optional[str] = None, agent_id: Optional[str] = None) -> str:
    """
    Write or update the OpenClaw tools registry to include MindClaw.
    Returns the path that was written.
    """
    _OPENCLAW_CONFIG.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    if _OPENCLAW_CONFIG.exists():
        try:
            existing = json.loads(_OPENCLAW_CONFIG.read_text())
        except Exception:
            existing = {}

    env: dict[str, str] = {}
    if db_path:
        env["MINDCLAW_DB"] = db_path
    if agent_id:
        env["MINDCLAW_AGENT"] = agent_id

    existing.setdefault("tools", {})["mindclaw"] = {
        "command": _python_executable(),
        "args": ["-m", "mindclaw.mcp_server"],
        "transport": "stdio",
        "description": "Persistent memory and knowledge graph for AI agents.",
        **({"env": env} if env else {}),
    }
    _OPENCLAW_CONFIG.write_text(json.dumps(existing, indent=2))
    return str(_OPENCLAW_CONFIG)


# ---------------------------------------------------------------------------
# Allow running as a module: python -m mindclaw.mcp_server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    serve()
