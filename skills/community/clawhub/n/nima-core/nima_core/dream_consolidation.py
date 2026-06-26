#!/usr/bin/env python3
"""
Dream Consolidation
===================
Nightly memory consolidation for nima-core bots.

Biologically inspired by sleep-phase memory consolidation:
  - Replay and strengthen important memories
  - Detect recurring emotions, participants, cross-domain patterns
  - Find temporal co-occurrence between domains
  - Generate creative cross-domain connections (aha moments)
  - Track emotional trajectory shifts
  - Surface domain gaps (what's been neglected?)
  - Write dream journal (markdown narrative)
  - Optional: VSA circular convolution for holographic blending

Runs standalone via `nima-dream` CLI or imported as a module.
Works on any nima-core SQLite database — core requires no extra deps.
Optional: numpy (VSA binding), openai (dream narrative LLM).

Usage:
    nima-dream                        # consolidate last 24h
    nima-dream --hours 48             # custom window
    nima-dream --dry-run              # preview without writing
    nima-dream --db /path/to/db       # explicit DB path
    nima-dream --history              # show last 5 run history
    nima-dream --insights             # show recent insights
    nima-dream --journal              # show today's dream journal

Environment:
    NIMA_DB_PATH         Path to SQLite database
    NIMA_DATA_DIR        Base data directory (default: ~/.nima)
    NIMA_BOT_NAME        Bot identity (default: bot)
    NIMA_DREAM_HOURS     Lookback window in hours (default: 24)
    NIMA_LLM_PROVIDER    Provider for dream narrative generation (optional)
    NIMA_LLM_API_KEY     API key for dream narrative generation (optional)
    NIMA_LLM_BASE_URL    API base URL override
    NIMA_LLM_MODEL       Model for narrative

Author: Lilu / nima-core

NOTE: This module has been refactored into nima_core.dream submodule.
      This file maintains backward compatibility by re-exporting from there.
"""

from __future__ import annotations

import os
import sys
import json
import logging
import argparse
from typing import Optional, List

# ── Re-export all public API from dream submodule ────────────────────────────
from nima_core.dream import (
    # Core data models
    Insight,
    Pattern,
    DreamSession,
    # Main orchestrator
    DreamConsolidator,
    # Convenience API
    consolidate,
    main,
    # Domain classification
    DOMAINS,
    classify_domain,
    # Pattern detection
    PatternDetector,
    # Insight generation
    InsightGenerator,
    # Narrative generation
    generate_dream_narrative,
    save_dream_markdown,
    # Database operations
    open_connection,
    ensure_tables,
    load_memories,
    load_sqlite_turns,
    # VSA operations (optional)
    blend_dream_vector,
    has_numpy,
    HAS_VSA,
    # Constants
    MAX_INSIGHTS,
    MAX_PATTERNS,
    MAX_DREAM_LOG,
    MAX_MEMORIES,
    DEFAULT_HOURS,
    MIN_IMPORTANCE,
    PATTERN_MIN_OCC,
    STRONG_PATTERN,
    CROSS_DOMAIN_WINDOW_S,
)

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
    # VSA operations
    "blend_dream_vector",
    "has_numpy",
    "HAS_VSA",
    # Constants (for backward compatibility)
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

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────
# All constants are now imported from nima_core.dream and re-exported for
# backward compatibility (see imports above)


# ── CLI Entry Point ───────────────────────────────────────────────────────────
# main() is now imported from nima_core.dream (see imports above)

if __name__ == "__main__":
    main()
