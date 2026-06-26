"""
NIMA Core — Dream Consolidation
================================

Nightly memory consolidation system that discovers patterns, generates insights,
and creates narrative summaries of agent experiences.

The dream consolidation pipeline:
  1. Load memories from database (past N hours)
  2. Detect patterns across memories (recurring themes, participants, emotions)
  3. Generate insights (connections, questions, emotional shifts)
  4. Calculate top domains and dominant emotion
  5. Generate LLM dream narrative
  6. Persist to database and JSON files

Modules
-------
models
    Core data models: Insight, Pattern, DreamSession, and utility functions
    for timestamps and atomic JSON writes.

domain_classifier
    Domain taxonomy and classification logic. Categorizes memories into
    semantic domains (work, creative, technical, social, etc.) using
    keyword matching and domain-specific patterns.

vsa_blender
    Vector Symbolic Architecture (VSA) operations for blending memory
    embeddings into a unified dream vector using Fourier Holographic
    Reduced Representations (FHRR).

db_operations
    Database connection management, table schema creation, and memory
    loading from both nima_memories and chat_turns tables.

pattern_detector
    Pattern detection across memories. Identifies recurring themes,
    participants, emotional patterns, domain clusters, and cross-domain
    connections using statistical analysis and similarity measures.

insight_generator
    Insight generation from detected patterns. Creates pattern insights,
    tracks emotional trajectories, detects domain gaps, and discovers
    creative cross-domain connections.

narrative_generator
    LLM-powered dream narrative generation. Creates poetic summaries
    of memory patterns and saves daily dream journals in markdown format.

consolidator
    Main orchestrator (DreamConsolidator class) that coordinates the
    entire consolidation pipeline, manages state persistence, and
    provides query helpers for historical data.

Typical usage::

    from nima_core.dream import DreamConsolidator, consolidate

    # Full-featured class API
    dc = DreamConsolidator(db_path="~/.nima/memory/nima.sqlite", bot_name="mybot")
    result = dc.run(hours=24, verbose=True)
    print(result["summary"])

    # Convenience function API
    result = consolidate(hours=24, dry_run=False, verbose=True)
    print(result["summary"])

Environment Variables
--------------------
NIMA_DB_PATH         Path to SQLite database
NIMA_DATA_DIR        Base data directory (default: ~/.nima)
NIMA_BOT_NAME        Bot identity (default: bot)
NIMA_DREAM_HOURS     Lookback window in hours (default: 24)
NIMA_MAX_INSIGHTS    Max insights to keep in memory (default: 500)
NIMA_MAX_PATTERNS    Max patterns to keep in memory (default: 200)
NIMA_MAX_DREAM_LOG   Max dream sessions to keep in log (default: 100)
NIMA_LLM_PROVIDER    Provider for narrative generation
NIMA_LLM_API_KEY     API key for narrative generation
NIMA_LLM_BASE_URL    API base URL override (optional)
NIMA_LLM_MODEL       Model to use for narratives
"""

import os
import sys
import json
import logging
import argparse
from typing import Dict, Optional, Union, List
from pathlib import Path

# Core data models
from .models import (
    Insight,
    Pattern,
    DreamSession,
)

# Main orchestrator
from .consolidator import DreamConsolidator, MAX_INSIGHTS, MAX_PATTERNS, MAX_DREAM_LOG, DEFAULT_HOURS

# Domain classification
from .domain_classifier import DOMAINS, classify_domain

# Pattern detection
from .pattern_detector import PatternDetector, PATTERN_MIN_OCC, CROSS_DOMAIN_WINDOW_S

# Insight generation
from .insight_generator import InsightGenerator, STRONG_PATTERN

# Narrative generation
from .narrative_generator import generate_dream_narrative, save_dream_markdown

# Database operations
from .db_operations import open_connection, ensure_tables, load_memories, load_sqlite_turns, MAX_MEMORIES, MIN_IMPORTANCE

# VSA operations (optional, requires numpy)
try:
    from .vsa_blender import blend_dream_vector, has_numpy
    HAS_VSA = True
except ImportError:
    blend_dream_vector = None  # type: ignore
    has_numpy = None  # type: ignore
    HAS_VSA = False


# ── Constants ─────────────────────────────────────────────────────────────────
# Re-exported from submodules (see imports above)


# ── Convenience API ───────────────────────────────────────────────────────────


def consolidate(
    hours: int = 24,
    db_path: Optional[Union[str, Path]] = None,
    bot_name: str = "bot",
    dry_run: bool = False,
    verbose: bool = False,
    data_dir: Optional[Union[str, Path]] = None,
) -> Dict:
    """
    Run a dream consolidation cycle (convenience function).

    This is a simplified API that creates a DreamConsolidator instance
    and runs a single consolidation cycle. For more control, use the
    DreamConsolidator class directly.

    Args:
        hours: Lookback window in hours (default: 24)
        db_path: Path to SQLite database (default: from env or ~/.nima/memory/nima.sqlite)
        bot_name: Bot identity for multi-bot environments (default: "bot")
        dry_run: If True, skip database writes and external API calls
        verbose: If True, log progress messages
        data_dir: Base data directory (default: from env or ~/.nima)

    Returns:
        Dict with consolidation results:
            - memories_in: Number of memories processed
            - patterns: Number of patterns found
            - insights: Number of insights generated
            - top_domains: List of top 3 domains
            - dominant_emotion: Most common emotion (or None)
            - narrative: LLM dream narrative (or None if dry_run)
            - summary: Human-readable summary string
            - session_id: Unique session identifier
            - dry_run: Boolean flag indicating dry run mode

    Example::

        from nima_core.dream import consolidate

        result = consolidate(hours=24, verbose=True)
        print(result["summary"])
        print(f"Found {result['patterns']} patterns")
        print(f"Generated {result['insights']} insights")
    """
    dc = DreamConsolidator(
        db_path=db_path,
        bot_name=bot_name,
        dry_run=dry_run,
        data_dir=data_dir,
    )
    return dc.run(hours=hours, verbose=verbose)


def _cmd_history(dc: "DreamConsolidator") -> None:
    """Print the last 5 consolidation run summaries."""
    runs = dc.last_runs(5)
    if not runs:
        print("No consolidation history.")
        return
    print("Last consolidation runs:")
    for r in runs:
        domains = r.get("top_domains", "[]")
        try:
            domains = ", ".join(json.loads(domains))
        except Exception:
            pass
        print(f"  {str(r.get('started_at',''))[:16]}  "
              f"{r.get('memories_processed',0)} memories → "
              f"{r.get('insights_generated',0)} insights  "
              f"[{domains}]")


def _cmd_insights(dc: "DreamConsolidator", hours: int) -> None:
    """Print recent insights for the given lookback window."""
    insights = dc.recent_insights(hours=hours)
    if not insights:
        print("No recent insights.")
        return
    print(f"Recent insights (last {hours}h):")
    for ins in insights:
        domains = ins.get("domains", "[]")
        try:
            domains = ", ".join(json.loads(domains))
        except Exception:
            pass
        print(f"  [{ins.get('type','?')}] [{domains}] {ins.get('content','')[:100]}…")


def _cmd_patterns(dc: "DreamConsolidator") -> None:
    """Print currently active patterns."""
    patterns = dc.active_patterns()
    if not patterns:
        print("No active patterns.")
        return
    print("Active patterns:")
    for p in patterns:
        print(f"  [{p.get('strength', 0):.2f}] {p.get('name','?')} "
              f"({p.get('occurrences',0)}×) — {p.get('description','')[:80]}…")


def _cmd_run(dc: "DreamConsolidator", hours: int, verbose: bool) -> None:
    """Execute a full consolidation cycle and print the results."""
    result = dc.run(hours=hours, verbose=verbose)

    if "error" in result:
        print(f"❌ {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"\n🌙 Dream Consolidation — {result.get('session_id','')}")
    print(f"   {result['summary']}")
    print(f"   VSA blending: {'✅' if result.get('vsa_available') else '⚠️ numpy not installed'}")

    if result.get("pattern_details"):
        print("\n🔁 Top patterns:")
        for p in result["pattern_details"][:5]:
            print(f"   [{p['strength']:.2f}] {p['name']} ({p['occurrences']}×)")

    if result.get("insight_details"):
        print(f"\n💡 Insights ({len(result['insight_details'])}):")
        for ins in result["insight_details"][:6]:
            domains = ", ".join(ins["domains"]) if isinstance(ins["domains"], list) else ins["domains"]
            print(f"   [{ins['type']}] [{domains}] {ins['content']}")

    if result.get("narrative"):
        print(f"\n✨ Dream narrative:\n   {result['narrative'][:300]}…")

    if result["dry_run"]:
        print("\n(dry run — nothing written)")


def main(argv: Optional[List[str]] = None) -> None:
    """
    CLI entry point for nima-dream command.

    Provides command-line interface for dream consolidation with options
    for consolidation runs, history viewing, insights display, and more.

    Args:
        argv: Command-line arguments (default: None uses sys.argv)

    Example::

        # Run from command line
        python -m nima_core.dream --hours 24 --verbose

        # Programmatic usage
        from nima_core.dream import main
        main(["--dry-run", "--hours", "1"])
    """
    parser = argparse.ArgumentParser(
        prog="nima-dream",
        description=(
            "Nightly dream consolidation — emotion patterns, cross-domain insights, "
            "creative connections, dream journal."
        ),
    )
    parser.add_argument("--db",       help="Path to SQLite DB (overrides NIMA_DB_PATH)")
    parser.add_argument("--hours",    type=int, default=DEFAULT_HOURS,
                        help=f"Lookback window in hours (default: {DEFAULT_HOURS})")
    parser.add_argument("--bot-name", default=os.environ.get("NIMA_BOT_NAME", "bot"))
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--history",  action="store_true", help="Show last 5 run history")
    parser.add_argument("--insights", action="store_true", help="Show recent insights")
    parser.add_argument("--patterns", action="store_true", help="Show active patterns")
    parser.add_argument("--journal",  action="store_true", help="Show today's dream journal")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    dc = DreamConsolidator(
        db_path=args.db,
        bot_name=args.bot_name,
        dry_run=args.dry_run,
    )

    if args.history:
        _cmd_history(dc)
        return

    if args.insights:
        _cmd_insights(dc, args.hours)
        return

    if args.patterns:
        _cmd_patterns(dc)
        return

    if args.journal:
        journal = dc.today_journal()
        if not journal:
            print("No journal entry for today.")
            return
        print(journal)
        return

    # ── Full run ──
    _cmd_run(dc, args.hours, args.verbose)


__all__ = [
    # Core data models
    "Insight",
    "Pattern",
    "DreamSession",
    # Main orchestrator
    "DreamConsolidator",
    # Convenience API
    "consolidate",
    "main",
    # Domain classification
    "DOMAINS",
    "classify_domain",
    # Pattern detection
    "PatternDetector",
    # Insight generation
    "InsightGenerator",
    # Narrative generation
    "generate_dream_narrative",
    "save_dream_markdown",
    # Database operations
    "open_connection",
    "ensure_tables",
    "load_memories",
    "load_sqlite_turns",
    # VSA operations (optional)
    "blend_dream_vector",
    "has_numpy",
    "HAS_VSA",
    # Constants
    "MAX_INSIGHTS",
    "MAX_PATTERNS",
    "MAX_DREAM_LOG",
    "MAX_MEMORIES",
    "DEFAULT_HOURS",
    "MIN_IMPORTANCE",
    "PATTERN_MIN_OCC",
    "STRONG_PATTERN",
    "CROSS_DOMAIN_WINDOW_S",
]
