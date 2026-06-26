"""
mindclaw.cli — Command-line interface for MindClaw.

Usage:
    mindclaw remember "We chose PostgreSQL for the backend"
    mindclaw recall "database decision"
    mindclaw list --category decision --limit 10
    mindclaw link <id1> <id2> --relation "depends_on"
    mindclaw graph <id> --depth 2
    mindclaw capture "conversation text here..."
    mindclaw stats
    mindclaw decay
    mindclaw export > backup.json
    mindclaw import backup.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Optional

from .capture import AutoCapture
from .config import MindClawConfig, load_config, save_config
from .context import ContextBuilder, check_conflicts
from .graph import KnowledgeGraph
from .search import SearchEngine
from .store import Memory, MemoryStore


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _fmt_memory(mem: Memory, *, verbose: bool = False) -> str:
    """Format a memory for terminal display."""
    age = _human_time(time.time() - mem.created_at)
    stars = "★" * min(int(mem.importance * 5) + 1, 5)
    tags = ", ".join(mem.tags) if mem.tags else "—"
    pin_marker = " [PINNED]" if mem.pinned else ""
    conf_marker = f" [confirmed\u00d7{mem.confirmed_count}]" if mem.confirmed_count > 0 else ""
    agent_marker = f" [{mem.agent_id}]" if mem.agent_id else ""

    lines = [
        f"  [{mem.id}] {stars}  {mem.category.upper()}{pin_marker}{conf_marker}{agent_marker}",
        f"  {mem.content[:120]}",
    ]
    if mem.summary and mem.summary != mem.content and verbose:
        lines.append(f"  Summary: {mem.summary[:100]}")
    lines.append(f"  Tags: {tags}  |  Age: {age}  |  Accessed: {mem.access_count}x")
    if verbose:
        lines.append(f"  Source: {mem.source}  |  Importance: {mem.importance:.2f}")
    return "\n".join(lines)


def _human_time(seconds: float) -> str:
    """Convert seconds to human-readable time."""
    if seconds < 60:
        return "just now"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)}m ago"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)}h ago"
    days = hours / 24
    if days < 30:
        return f"{int(days)}d ago"
    months = days / 30
    return f"{int(months)}mo ago"


def _print_separator() -> None:
    print("─" * 60)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_remember(args: argparse.Namespace, store: MemoryStore) -> None:
    """Store a new memory."""
    # Conflict check
    agent_id = getattr(args, "agent", "") or ""
    conflicts = check_conflicts(args.content, store, agent_id=agent_id or None)
    if conflicts:
        print(f"  \u26a0\ufe0f  {len(conflicts)} potential conflict(s) detected:")
        for r in conflicts:
            print(f"    [{r.conflicting_memory.id}] {r.conflicting_memory.content[:80]}")
            print(f"    Similarity: {r.similarity:.0%} — {r.suggestion}")
        _print_separator()

    mem = Memory(
        content=args.content,
        summary=args.summary or "",
        category=args.category or "note",
        tags=args.tags.split(",") if args.tags else [],
        source=args.source or "cli",
        importance=args.importance,
        agent_id=agent_id,
        pinned=getattr(args, "pin", False),
    )
    store.add(mem)
    print(f"✓ Remembered [{mem.id}]")
    print(_fmt_memory(mem))


def cmd_recall(args: argparse.Namespace, store: MemoryStore) -> None:
    """Search and recall memories."""
    engine = SearchEngine(store)
    info = engine.rebuild()
    agent_id = getattr(args, "agent", "") or None
    use_decay = getattr(args, "decay", False)
    use_mmr = getattr(args, "mmr", False)

    results = engine.search(
        args.query,
        top_k=args.limit,
        temporal_decay=use_decay,
        temporal_halflife=getattr(args, "halflife", 30.0),
        mmr=use_mmr,
        mmr_lambda=getattr(args, "mmr_lambda", 0.7),
        agent_id=agent_id,
    )

    if not results:
        print("No memories found matching your query.")
        return

    method_note = results[0]["method"] if results else "bm25"
    sem_status = (
        f"  Ollama ({engine.ollama.model})" if info.get("semantic_available")
        else "  Ollama: not running (BM25 only)"
    )
    decay_note = "  temporal-decay ON" if use_decay else ""
    mmr_note = "  MMR diversity ON" if use_mmr else ""
    flags = ", ".join(x for x in [sem_status.strip(), decay_note.strip(), mmr_note.strip()] if x)
    print(f"Found {len(results)} memories  [{flags}]:\n")

    for i, r in enumerate(results, 1):
        mem = r["memory"]
        score = r["score"]
        print(f"  {i}. (score: {score:.3f})")
        print(_fmt_memory(mem, verbose=args.verbose))
        _print_separator()


def cmd_get(args: argparse.Namespace, store: MemoryStore) -> None:
    """Get a specific memory by ID."""
    mem = store.get(args.id)
    if mem is None:
        print(f"Memory [{args.id}] not found.")
        sys.exit(1)
    print(_fmt_memory(mem, verbose=True))

    # Show connected edges
    graph = KnowledgeGraph(store)
    neighbors = graph.neighbors(args.id, max_depth=1)
    if neighbors:
        print(f"\n  Connected to {len(neighbors)} memories:")
        for node in neighbors:
            print(f"    → [{node.memory.id}] {node.memory.content[:60]}")


def cmd_list(args: argparse.Namespace, store: MemoryStore) -> None:
    """List memories with filters."""
    memories = store.list_memories(
        category=args.category,
        tag=args.tag,
        include_archived=args.archived,
        limit=args.limit,
        order_by=args.sort,
        agent_id=getattr(args, "agent", "") or None,
        pinned_only=getattr(args, "pinned", False),
    )

    if not memories:
        print("No memories found.")
        return

    print(f"Showing {len(memories)} memories:\n")
    for mem in memories:
        print(_fmt_memory(mem, verbose=args.verbose))
        _print_separator()


def cmd_forget(args: argparse.Namespace, store: MemoryStore) -> None:
    """Delete or archive a memory."""
    if args.hard:
        ok = store.delete(args.id)
        action = "Deleted"
    else:
        ok = store.archive(args.id)
        action = "Archived"

    if ok:
        print(f"✓ {action} [{args.id}]")
    else:
        print(f"Memory [{args.id}] not found.")
        sys.exit(1)


def cmd_link(args: argparse.Namespace, store: MemoryStore) -> None:
    """Create an edge between two memories."""
    graph = KnowledgeGraph(store)
    edge_ids = graph.link(
        args.source_id,
        args.target_id,
        args.relation,
        bidirectional=args.bidirectional,
    )
    print(f"✓ Linked [{args.source_id}] —({args.relation})→ [{args.target_id}]")
    if args.bidirectional:
        print(f"  (bidirectional, {len(edge_ids)} edges created)")


def cmd_graph(args: argparse.Namespace, store: MemoryStore) -> None:
    """Show the knowledge subgraph around a memory."""
    graph = KnowledgeGraph(store)
    sub = graph.subgraph(args.id, depth=args.depth)

    nodes = sub["nodes"]
    edges = sub["edges"]

    if not nodes:
        print(f"Memory [{args.id}] not found or has no connections.")
        return

    print(f"Subgraph around [{args.id}] (depth={args.depth}):\n")
    print(f"  Nodes ({len(nodes)}):")
    for n in nodes:
        marker = "●" if n["id"] == args.id else "○"
        print(f"    {marker} [{n['id']}] {n['label']}")

    if edges:
        print(f"\n  Edges ({len(edges)}):")
        for e in edges:
            print(f"    [{e['source']}] —({e['relation']})→ [{e['target']}]")

    if args.json:
        print(f"\nJSON:\n{json.dumps(sub, indent=2)}")


def cmd_capture(args: argparse.Namespace, store: MemoryStore) -> None:
    """Auto-capture memories from text."""
    # Read from argument or stdin
    if args.text:
        text = args.text
    elif args.file:
        text = Path(args.file).read_text()
    else:
        print("Reading from stdin (Ctrl+D to finish)...")
        text = sys.stdin.read()

    capture = AutoCapture(store)
    results = capture.process(text, source=args.source or "capture-cli", dry_run=args.dry_run)

    if not results:
        print("No capturable information detected.")
        return

    mode = "DETECTED (dry run)" if args.dry_run else "CAPTURED"
    print(f"{mode} {len(results)} memories:\n")
    for r in results:
        print(f"  [{r.rule_name}] (confidence: {r.confidence:.0%})")
        print(f"    {r.memory.content[:100]}")
        print(f"    Category: {r.memory.category} | Importance: {r.memory.importance:.1f}")
        _print_separator()


def cmd_stats(args: argparse.Namespace, store: MemoryStore) -> None:
    """Show memory store statistics."""
    s = store.stats()
    print("MindClaw Stats")
    print("═" * 40)
    print(f"  Total memories:  {s['total_memories']}")
    print(f"  Active:          {s['active']}")
    print(f"  Archived:        {s['archived']}")
    print(f"  Pinned:          {s['pinned']}")
    print(f"  Knowledge edges: {s['edges']}")
    print(f"  DB size:         {s['db_size_kb']} KB")
    print(f"  DB path:         {s['db_path']}")
    if s["categories"]:
        print(f"\n  Categories:")
        for cat, count in s["categories"].items():
            print(f"    {cat}: {count}")
    if s.get("agents"):
        print(f"\n  Agents/Namespaces:")
        for agent, count in s["agents"].items():
            print(f"    {agent}: {count}")


def cmd_decay(args: argparse.Namespace, store: MemoryStore) -> None:
    """Apply decay to memory importance and archive stale memories."""
    agent_id = getattr(args, "agent", "") or None
    threshold = args.threshold
    archived = store.apply_decay(threshold=threshold, agent_id=agent_id)
    print(f"\u2713 Decay applied. {archived} memories archived (below {threshold:.2f}).")
    print("  Note: Pinned memories are never decayed.")


def cmd_export(args: argparse.Namespace, store: MemoryStore) -> None:
    """Export all memories to JSON."""
    data = store.export_json()
    if args.output:
        Path(args.output).write_text(data)
        print(f"✓ Exported to {args.output}")
    else:
        print(data)


def cmd_import(args: argparse.Namespace, store: MemoryStore) -> None:
    """Import memories from JSON file."""
    data = Path(args.file).read_text()
    result = store.import_json(data, merge=not args.replace)
    print(f"✓ Imported: {result['memories']} memories, {result['edges']} edges")
    if result["skipped"]:
        print(f"  Skipped {result['skipped']} duplicates")

# ---------------------------------------------------------------------------
# New v0.2 commands
# ---------------------------------------------------------------------------

def cmd_pin(args: argparse.Namespace, store: MemoryStore) -> None:
    """Pin a memory so it is never decayed or auto-archived."""
    ok = store.pin(args.id)
    if ok:
        print(f"\u2713 Pinned [{args.id}] — this memory will not decay.")
    else:
        print(f"Memory [{args.id}] not found.")
        sys.exit(1)


def cmd_unpin(args: argparse.Namespace, store: MemoryStore) -> None:
    """Remove pin from a memory."""
    ok = store.unpin(args.id)
    if ok:
        print(f"\u2713 Unpinned [{args.id}].")
    else:
        print(f"Memory [{args.id}] not found.")
        sys.exit(1)


def cmd_confirm(args: argparse.Namespace, store: MemoryStore) -> None:
    """Confirm/reinforce a memory, boosting its importance."""
    mem = store.confirm(args.id)
    if mem is None:
        print(f"Memory [{args.id}] not found.")
        sys.exit(1)
    print(f"\u2713 Confirmed [{mem.id}] (importance: {mem.importance:.2f}, confirmed\u00d7{mem.confirmed_count})")


def cmd_timeline(args: argparse.Namespace, store: MemoryStore) -> None:
    """Show memories created in the last N hours in chronological order."""
    since = time.time() - (args.hours * 3600)
    agent_id = getattr(args, "agent", "") or None
    memories = store.get_timeline(since=since, agent_id=agent_id, limit=args.limit)
    if not memories:
        print(f"No memories from the last {args.hours}h.")
        return
    print(f"Timeline — last {args.hours}h ({len(memories)} memories):\n")
    for mem in memories:
        age_min = int((time.time() - mem.created_at) / 60)
        print(f"  {age_min}m ago  [{mem.id}] {mem.category.upper()}")
        print(f"    {mem.content[:100]}")
    _print_separator()


def cmd_context(args: argparse.Namespace, store: MemoryStore) -> None:
    """Build and print a context block ready for LLM injection."""
    agent_id = getattr(args, "agent", "") or None
    builder = ContextBuilder(store)
    block = builder.build(
        args.query,
        max_tokens=args.max_tokens,
        agent_id=agent_id,
        format=args.format,
    )
    print(block.text)
    print(f"\n  [{block.memories_used} memories, ~{block.estimated_tokens} tokens"
          f"{', truncated' if block.truncated else ''}]")


def cmd_conflicts(args: argparse.Namespace, store: MemoryStore) -> None:
    """Check if a piece of content conflicts with existing memories."""
    agent_id = getattr(args, "agent", "") or None
    reports = check_conflicts(args.content, store, agent_id=agent_id)
    if not reports:
        print("\u2713 No conflicts detected.")
        return
    print(f"\u26a0\ufe0f  {len(reports)} potential conflict(s):\n")
    for r in reports:
        print(f"  [{r.conflicting_memory.id}] {r.conflicting_memory.content[:80]}")
        print(f"  Similarity: {r.similarity:.0%}")
        print(f"  {r.suggestion}")
        _print_separator()


def cmd_consolidate(args: argparse.Namespace, store: MemoryStore) -> None:
    """Find and merge near-duplicate memories."""
    agent_id = getattr(args, "agent", "") or None
    count = store.consolidate_duplicates(
        agent_id=agent_id,
        similarity_threshold=args.threshold,
    )
    print(f"\u2713 Consolidation complete. {count} duplicate memories archived.")


def cmd_sync(args: argparse.Namespace, store: MemoryStore) -> None:
    """Export memories to OpenClaw's MEMORY.md (or a custom Markdown file)."""
    agent_id = getattr(args, "agent", "") or ""
    target = getattr(args, "to", None)

    if target:
        # Export to a specific Markdown file
        from pathlib import Path as _Path
        count = store.export_to_markdown(_Path(target), agent_id=agent_id or None)
        print(f"\u2713 Exported {count} memories to {target}")
    else:
        # Auto-sync to OpenClaw workspace
        # Priority: --workspace flag > config file > env var > auto-detect
        ws = (
            getattr(args, "workspace", None)
            or (args._config.effective_workspace() if hasattr(args, "_config") else None)
        )
        result = store.sync_openclaw(workspace_path=ws or None, agent_id=agent_id)
        if result.get("ok"):
            print(f"\u2713 Synced {result['exported']} memories to {result['path']}")
            print(f"  OpenClaw workspace: {result['workspace']}")
            print("  Memories are now searchable via OpenClaw's memory_search tool.")
        else:
            print(f"\u2717 {result.get('error')}")
            if result.get("tip"):
                print(f"  Tip: {result['tip']}")
            sys.exit(1)


def cmd_md_import(args: argparse.Namespace, store: MemoryStore) -> None:
    """Import memories from a Markdown file (OpenClaw MEMORY.md or daily log)."""
    agent_id = getattr(args, "agent", "") or ""
    count = store.import_from_markdown(
        args.file,
        agent_id=agent_id,
        source=getattr(args, "source", "") or "",
    )
    print(f"\u2713 Imported {count} new memories from {args.file}")
    if count == 0:
        print("  (All bullet points were already in the store, or the file had none.)")


def cmd_setup(args: argparse.Namespace, store: MemoryStore) -> None:
    """
    Interactive setup wizard.
    Configures MindClaw once so every subsequent command works without flags.
    Also available as the `setup_mindclaw` MCP tool for OpenClaw agents.
    """
    cfg = load_config()

    print()
    print("\u2550" * 52)
    print("  MindClaw Setup Wizard")
    print("\u2550" * 52)
    print("  Press Enter to accept the default shown in [brackets].")
    print()

    def _ask(prompt: str, default: str) -> str:
        try:
            val = input(f"  {prompt} [{default}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return default
        return val if val else default

    def _yes(prompt: str) -> bool:
        try:
            val = input(f"  {prompt} [Y/n]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return True
        return val not in ("n", "no")

    # ------------------------------------------------------------------ 1. Workspace
    default_ws = cfg.openclaw_workspace or str(Path.home() / ".openclaw" / "workspace")
    workspace = Path(
        _ask("OpenClaw workspace path", default_ws)
    ).expanduser()
    workspace_str = str(workspace)

    # ------------------------------------------------------------------ 2. Agent
    default_agent = cfg.agent_id or ""
    raw_agent = _ask(
        "Default agent name  (leave blank = shared namespace)",
        default_agent if default_agent else "none",
    )
    agent = "" if raw_agent in ("none", "") else raw_agent

    # ------------------------------------------------------------------ 3. DB path
    builtin_default_db = str(Path.home() / ".mindclaw" / "memory.db")
    default_db = cfg.db_path or builtin_default_db
    db_str = str(Path(_ask("Database path", default_db)).expanduser())
    db_save: Optional[str] = None if db_str == builtin_default_db else db_str

    # ------------------------------------------------------------------ Save
    new_cfg = MindClawConfig(
        db_path=db_save,
        agent_id=agent,
        openclaw_workspace=workspace_str,
    )
    saved_path = save_config(new_cfg)
    print()
    print(f"  \u2713 Config saved \u2192 {saved_path}")
    print()

    # ------------------------------------------------------------------ 4. Claude Desktop MCP
    if _yes("Register with Claude Desktop MCP?"):
        try:
            from . import mcp_server as _mcp
            path = _mcp.install_claude_desktop(db_path=db_save, agent_id=agent or None)
            print(f"  \u2713 Claude Desktop config updated \u2192 {path}")
            print("    Restart Claude Desktop to activate.")
        except ImportError:
            print("  ! MCP SDK not installed. Run: pip install mindclaw[mcp]")

    # ------------------------------------------------------------------ 5. OpenClaw MCP
    if _yes("Register with OpenClaw MCP?"):
        try:
            from . import mcp_server as _mcp
            path = _mcp.install_openclaw(db_path=db_save, agent_id=agent or None)
            print(f"  \u2713 OpenClaw tools config updated \u2192 {path}")
        except ImportError:
            print("  ! MCP SDK not installed. Run: pip install mindclaw[mcp]")

    # ------------------------------------------------------------------ 6. Initial sync
    if _yes("Do an initial sync to MEMORY.md now?"):
        s = MemoryStore(db_path=db_save)
        result = s.sync_openclaw(workspace_path=workspace_str, agent_id=agent)
        if result.get("ok"):
            print(f"  \u2713 Synced {result['exported']} memories \u2192 {result['path']}")
            print("    Memories are now searchable via OpenClaw's memory_search tool.")
        else:
            print(f"  ! Sync skipped: {result.get('error', 'unknown error')}")

    print()
    print("  MindClaw is ready!  Run `mindclaw --help` to see all commands.")
    print()


def cmd_mcp(args: argparse.Namespace, store: MemoryStore) -> None:
    """MCP server management: install or serve."""
    from . import mcp_server as _mcp
    sub = getattr(args, "mcp_command", None)

    if sub == "serve" or sub is None:
        print("Starting MindClaw MCP server (stdio)...")
        _mcp.serve()

    elif sub == "install":
        target = getattr(args, "target", "claude") or "claude"
        db_path = getattr(args, "db", None)
        agent_id = getattr(args, "mcp_agent", None) or getattr(args, "agent", None)

        if target in ("claude", "claude-desktop"):
            path = _mcp.install_claude_desktop(db_path=db_path, agent_id=agent_id)
            print(f"\u2713 MindClaw registered in Claude Desktop config:")
            print(f"  {path}")
            print("  Restart Claude Desktop to activate.")
        elif target == "openclaw":
            path = _mcp.install_openclaw(db_path=db_path, agent_id=agent_id)
            print(f"\u2713 MindClaw registered in OpenClaw tools:")
            print(f"  {path}")
        else:
            print(f"Unknown target '{target}'. Use: claude, claude-desktop, openclaw")
            sys.exit(1)

    elif sub == "config":
        import sys as _sys
        print("MindClaw MCP server entry point:")
        print(f"  Executable: {_sys.executable}")
        print(f"  Args: -m mindclaw.mcp_server")
        print(f"  Transport: stdio")
        print("\nManual Claude Desktop config (mcpServers section):")
        print(json.dumps({
            "mindclaw": {
                "command": _sys.executable,
                "args": ["-m", "mindclaw.mcp_server"],
            }
        }, indent=2))

# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mindclaw",
        description="MindClaw \u2014 Persistent memory & knowledge graph for AI agents.",
    )
    parser.add_argument(
        "--db", type=str, default=None,
        help="Path to SQLite database (default: ~/.mindclaw/memory.db)",
    )
    parser.add_argument(
        "--agent", type=str, default="",
        help="Agent namespace / scope (isolates memories per agent)",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # remember
    p = sub.add_parser("remember", aliases=["r", "add"], help="Store a new memory")
    p.add_argument("content", help="The memory content")
    p.add_argument("-s", "--summary", help="Short summary")
    p.add_argument("-c", "--category", default="note",
                   help="Category: fact, decision, preference, error, note, todo")
    p.add_argument("-t", "--tags", help="Comma-separated tags")
    p.add_argument("--source", help="Source label")
    p.add_argument("-i", "--importance", type=float, default=0.6, help="0.0\u20131.0")
    p.add_argument("--pin", action="store_true", help="Pin this memory (never decayed)")

    # recall / search
    p = sub.add_parser("recall", aliases=["search", "q"], help="Search memories")
    p.add_argument("query", help="Search query")
    p.add_argument("-n", "--limit", type=int, default=10)
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument(
        "--decay", action="store_true",
        help="Apply temporal decay — boost recent memories, fade old ones",
    )
    p.add_argument(
        "--halflife", type=float, default=30.0,
        help="Temporal decay half-life in days (default 30)",
    )
    p.add_argument(
        "--mmr", action="store_true",
        help="Apply MMR diversity re-ranking to reduce near-duplicate results",
    )
    p.add_argument(
        "--mmr-lambda", dest="mmr_lambda", type=float, default=0.7,
        help="MMR λ: 1.0=pure relevance, 0.0=maximum diversity (default 0.7)",
    )

    # get
    p = sub.add_parser("get", help="Get a memory by ID")
    p.add_argument("id", help="Memory ID")

    # list
    p = sub.add_parser("list", aliases=["ls"], help="List memories")
    p.add_argument("-c", "--category", help="Filter by category")
    p.add_argument("-t", "--tag", help="Filter by tag")
    p.add_argument("-n", "--limit", type=int, default=20)
    p.add_argument("--sort", default="importance DESC",
                   help="Order: 'importance DESC', 'created_at DESC', etc.")
    p.add_argument("--archived", action="store_true", help="Include archived")
    p.add_argument("--pinned", action="store_true", help="Show only pinned memories")
    p.add_argument("-v", "--verbose", action="store_true")

    # forget
    p = sub.add_parser("forget", aliases=["rm", "del"], help="Archive or delete a memory")
    p.add_argument("id", help="Memory ID to forget")
    p.add_argument("--hard", action="store_true", help="Hard delete (not just archive)")

    # pin / unpin
    p = sub.add_parser("pin", help="Pin a memory (never decayed)")
    p.add_argument("id", help="Memory ID")

    p = sub.add_parser("unpin", help="Remove pin from a memory")
    p.add_argument("id", help="Memory ID")

    # confirm
    p = sub.add_parser("confirm", help="Reinforce a memory, boosting its importance")
    p.add_argument("id", help="Memory ID")

    # link
    p = sub.add_parser("link", help="Link two memories")
    p.add_argument("source_id", help="Source memory ID")
    p.add_argument("target_id", help="Target memory ID")
    p.add_argument("-r", "--relation", default="related_to", help="Relation type")
    p.add_argument("-b", "--bidirectional", action="store_true")

    # graph
    p = sub.add_parser("graph", help="Show knowledge subgraph")
    p.add_argument("id", help="Center memory ID")
    p.add_argument("-d", "--depth", type=int, default=2)
    p.add_argument("--json", action="store_true", help="Output JSON")

    # capture
    p = sub.add_parser("capture", aliases=["cap"], help="Auto-capture from text")
    p.add_argument("text", nargs="?", help="Text to analyze")
    p.add_argument("-f", "--file", help="Read from file")
    p.add_argument("--source", help="Source label")
    p.add_argument("--dry-run", action="store_true", help="Detect without saving")

    # timeline
    p = sub.add_parser("timeline", help="Show recent memories in chronological order")
    p.add_argument("--hours", type=float, default=24, help="Look back N hours (default 24)")
    p.add_argument("-n", "--limit", type=int, default=30)

    # context
    p = sub.add_parser("context", help="Build a context block for LLM injection")
    p.add_argument("query", help="What you need context for")
    p.add_argument("--max-tokens", type=int, default=2000)
    p.add_argument("--format", choices=["markdown", "plain", "xml"], default="markdown")

    # conflicts
    p = sub.add_parser("conflicts", help="Check if content conflicts with existing memories")
    p.add_argument("content", help="Content to check")

    # consolidate
    p = sub.add_parser("consolidate", help="Merge near-duplicate memories")
    p.add_argument("--threshold", type=float, default=0.85,
                   help="Jaccard similarity threshold for duplicates (default 0.85)")

    # stats
    sub.add_parser("stats", help="Show memory statistics")

    # decay
    p = sub.add_parser("decay", help="Apply importance decay")
    p.add_argument("--threshold", type=float, default=0.05,
                   help="Archive below this importance")

    # export
    p = sub.add_parser("export", help="Export memories to JSON")
    p.add_argument("-o", "--output", help="Output file path")

    # import (JSON)
    p = sub.add_parser("import", help="Import memories from JSON")
    p.add_argument("file", help="JSON file to import")
    p.add_argument("--replace", action="store_true",
                   help="Replace all (default: merge)")

    # sync — export to OpenClaw MEMORY.md
    p = sub.add_parser(
        "sync",
        help="Sync memories to OpenClaw's MEMORY.md (or any Markdown file)",
    )
    p.add_argument(
        "--to", metavar="PATH",
        help="Target Markdown file (default: auto-detect OpenClaw workspace)",
    )
    p.add_argument(
        "--workspace", metavar="PATH",
        help="OpenClaw workspace path (default: ~/.openclaw/workspace)",
    )

    # md-import — import from Markdown
    p = sub.add_parser(
        "md-import",
        help="Import memories from an OpenClaw Markdown memory file",
    )
    p.add_argument("file", help="Path to MEMORY.md or a YYYY-MM-DD.md daily log")
    p.add_argument("--source", help="Source label for imported memories")

    # setup
    sub.add_parser(
        "setup",
        help="Interactive setup wizard — configure MindClaw once, use everywhere",
    )

    # mcp
    p = sub.add_parser("mcp", help="MCP server management")
    mcp_sub = p.add_subparsers(dest="mcp_command")
    mcp_sub.add_parser("serve", help="Start the MCP stdio server")
    inst = mcp_sub.add_parser("install", help="Register with a client (Claude Desktop, OpenClaw)")
    inst.add_argument("--target", default="claude",
                      choices=["claude", "claude-desktop", "openclaw"],
                      help="Which client to register with (default: claude)")
    inst.add_argument("--agent", dest="mcp_agent", help="Default agent namespace")
    mcp_sub.add_parser("config", help="Print raw MCP config JSON")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

_COMMANDS = {
    "setup": cmd_setup,
    "remember": cmd_remember, "r": cmd_remember, "add": cmd_remember,
    "recall": cmd_recall, "search": cmd_recall, "q": cmd_recall,
    "get": cmd_get,
    "list": cmd_list, "ls": cmd_list,
    "forget": cmd_forget, "rm": cmd_forget, "del": cmd_forget,
    "pin": cmd_pin,
    "unpin": cmd_unpin,
    "confirm": cmd_confirm,
    "link": cmd_link,
    "graph": cmd_graph,
    "capture": cmd_capture, "cap": cmd_capture,
    "timeline": cmd_timeline,
    "context": cmd_context,
    "conflicts": cmd_conflicts,
    "consolidate": cmd_consolidate,
    "sync": cmd_sync,
    "md-import": cmd_md_import,
    "stats": cmd_stats,
    "decay": cmd_decay,
    "export": cmd_export,
    "import": cmd_import,
    "mcp": cmd_mcp,
}


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Load persistent config.  Priority: CLI flag > env var > config > default.
    cfg = load_config()
    args._config = cfg

    # Effective db path
    effective_db: Optional[str] = getattr(args, "db", None) or cfg.effective_db()

    # Effective agent: CLI --agent > env var > config
    if not getattr(args, "agent", None):
        args.agent = cfg.effective_agent()

    store = MemoryStore(db_path=effective_db)
    handler = _COMMANDS.get(args.command)

    if handler is None:
        parser.print_help()
        sys.exit(1)

    try:
        handler(args, store)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
