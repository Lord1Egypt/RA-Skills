#!/usr/bin/env python3
"""
NIMA Core — LadybugDB Schema Initializer
==========================================

Creates all required node tables and relationship tables in the LadybugDB
(Kùzu-backed) database.  Safe to run on an existing database — all
``CREATE … IF NOT EXISTS`` statements are idempotent.

Also runs column migrations: any column added to the schema after initial
install is applied via ``ALTER TABLE … ADD IF NOT EXISTS`` so existing
databases stay in sync without a full rebuild.

Usage:
    python scripts/init_ladybug.py [--db PATH] [--dry-run]

Environment:
    NIMA_HOME   — data root (default: ~/.nima)
"""

import argparse
import os
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Schema definitions
# ---------------------------------------------------------------------------

# Each entry: (Cypher CREATE statement, description)
NODE_TABLES = [
    # ── Core memory graph ──────────────────────────────────────────────
    (
        """CREATE NODE TABLE IF NOT EXISTS MemoryNode (
            id              INT64   PRIMARY KEY,
            timestamp       INT64,
            layer           STRING,
            text            STRING,
            summary         STRING,
            who             STRING,
            affect_json     STRING,
            session_key     STRING,
            conversation_id STRING,
            turn_id         STRING,
            fe_score        DOUBLE,
            embedding       FLOAT[512],
            strength        FLOAT    DEFAULT 1.0,
            decay_rate      FLOAT    DEFAULT 0.01,
            last_accessed   INT64    DEFAULT 0,
            is_ghost        BOOL     DEFAULT false,
            dismissal_count INT64    DEFAULT 0,
            recall_count    INT64    DEFAULT 0,
            memory_type     STRING,
            importance      DOUBLE,
            emotions        STRING,
            themes          STRING,
            source_agent    STRING,
            model           STRING
        )""",
        "MemoryNode — primary memory storage with embeddings",
    ),
    (
        """CREATE NODE TABLE IF NOT EXISTS Turn (
            id          INT64  PRIMARY KEY,
            turn_id     STRING,
            timestamp   INT64,
            affect_json STRING
        )""",
        "Turn — conversation turn structure",
    ),
    # ── Dream consolidation ────────────────────────────────────────────
    (
        """CREATE NODE TABLE IF NOT EXISTS DreamNode (
            id           STRING PRIMARY KEY,
            date         STRING,
            narrative    STRING,
            source_count INT64,
            created_at   STRING
        )""",
        "DreamNode — nightly dream consolidation narratives",
    ),
    (
        """CREATE NODE TABLE IF NOT EXISTS InsightNode (
            id         STRING PRIMARY KEY,
            content    STRING,
            type       STRING,
            confidence FLOAT,
            sources    STRING,
            domains    STRING,
            timestamp  STRING,
            importance FLOAT,
            validated  BOOL
        )""",
        "InsightNode — extracted insights from dream consolidation",
    ),
    (
        """CREATE NODE TABLE IF NOT EXISTS PatternNode (
            id          STRING PRIMARY KEY,
            name        STRING,
            description STRING,
            occurrences INT64,
            domains     STRING,
            examples    STRING,
            first_seen  STRING,
            last_seen   STRING,
            strength    DOUBLE
        )""",
        "PatternNode — recurring patterns detected across memories",
    ),
]

REL_TABLES = [
    # ── Core relationships ─────────────────────────────────────────────
    (
        """CREATE REL TABLE IF NOT EXISTS relates_to (
            FROM MemoryNode TO MemoryNode,
            relation STRING,
            weight   DOUBLE
        )""",
        "relates_to — general memory-to-memory associations",
    ),
    (
        """CREATE REL TABLE IF NOT EXISTS has_input (
            FROM Turn TO MemoryNode
        )""",
        "has_input — Turn → input MemoryNode",
    ),
    (
        """CREATE REL TABLE IF NOT EXISTS has_contemplation (
            FROM Turn TO MemoryNode
        )""",
        "has_contemplation — Turn → contemplation MemoryNode",
    ),
    (
        """CREATE REL TABLE IF NOT EXISTS has_output (
            FROM Turn TO MemoryNode
        )""",
        "has_output — Turn → output MemoryNode",
    ),
    # ── Dream / insight ────────────────────────────────────────────────
    (
        """CREATE REL TABLE IF NOT EXISTS derived_from (
            FROM InsightNode TO MemoryNode,
            FROM DreamNode   TO MemoryNode
        )""",
        "derived_from — InsightNode/DreamNode → source MemoryNodes",
    ),
    (
        """CREATE REL TABLE IF NOT EXISTS governs (
            FROM ProtocolNode TO MemoryNode
        )""",
        "governs — ProtocolNode → MemoryNode (governance link)",
    ),
]

NODE_TABLES = NODE_TABLES + [
    (
        """CREATE NODE TABLE IF NOT EXISTS ProtocolNode (
            id     STRING PRIMARY KEY,
            name   STRING,
            rule   STRING,
            domain STRING DEFAULT 'general',
            priority INT64 DEFAULT 3,
            trigger_keywords STRING DEFAULT '[]',
            active INT64 DEFAULT 1,
            created_at STRING,
            updated_at STRING
        )""",
        "ProtocolNode — constitutional governance rules (Athena-inspired)",
    ),
]

# ---------------------------------------------------------------------------
# Column migrations
# ---------------------------------------------------------------------------
# Canonical list of MemoryNode columns to enforce via migrations.
# We use ALTER TABLE … ADD IF NOT EXISTS for each entry, which is idempotent
# and safe to run every time.
# When you add, remove, or change a column in the CREATE TABLE above, update
# this list to match.
# Format: (column_name, kuzu_type, default_clause_or_empty_string)
MEMORYNODE_COLUMN_MIGRATIONS = [
    ("strength",        "FLOAT",   "DEFAULT 1.0"),
    ("decay_rate",      "FLOAT",   "DEFAULT 0.01"),
    ("last_accessed",   "INT64",   "DEFAULT 0"),
    ("is_ghost",        "BOOL",    "DEFAULT false"),
    ("dismissal_count", "INT64",   "DEFAULT 0"),
    ("recall_count",    "INT64",   "DEFAULT 0"),
    ("memory_type",     "STRING",  ""),
    ("importance",      "DOUBLE",  ""),
    ("emotions",        "STRING",  ""),
    ("themes",          "STRING",  ""),
    ("source_agent",    "STRING",  ""),
    ("model",           "STRING",  ""),
]


# ---------------------------------------------------------------------------
# Init logic
# ---------------------------------------------------------------------------

def init_ladybug(db_path: Path, dry_run: bool = False) -> None:
    if dry_run:
        print(f"[DRY-RUN] Would initialize: {db_path}")
        print("\nNode tables:")
        for _, desc in NODE_TABLES:
            print(f"  + {desc}")
        print("\nRel tables:")
        for _, desc in REL_TABLES:
            print(f"  + {desc}")
        print("\nColumn migrations (MemoryNode):")
        for col, typ, default in MEMORYNODE_COLUMN_MIGRATIONS:
            print(f"  + {col} {typ} {default}".strip())
        return

    try:
        import real_ladybug as lb
    except ImportError:
        print(
            "❌  real-ladybug is not installed.\n"
            "    Install with: pip install real-ladybug\n"
            "    Or run: ./install.sh --with-ladybug",
            file=sys.stderr,
        )
        sys.exit(1)

    db_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"🗄️  Initializing LadybugDB at: {db_path}")

    db   = lb.Database(str(db_path))
    conn = lb.Connection(db)

    changes = 0

    print("\nNode tables:")
    for cypher, desc in NODE_TABLES:
        try:
            conn.execute(cypher)
            print(f"  ✅ {desc}")
            changes += 1
        except Exception as exc:
            msg = str(exc)
            if "already exist" in msg.lower() or "already exists" in msg.lower():
                print(f"  ✓  {desc} (already exists)")
            else:
                print(f"  ⚠️  {desc}: {exc}")

    print("\nRel tables:")
    for cypher, desc in REL_TABLES:
        try:
            conn.execute(cypher)
            print(f"  ✅ {desc}")
            changes += 1
        except Exception as exc:
            msg = str(exc)
            if "already exist" in msg.lower() or "already exists" in msg.lower():
                print(f"  ✓  {desc} (already exists)")
            else:
                print(f"  ⚠️  {desc}: {exc}")

    # ── Column migrations ──────────────────────────────────────────────
    print("\nColumn migrations (MemoryNode):")
    for col, typ, default in MEMORYNODE_COLUMN_MIGRATIONS:
        default_clause = f" {default}" if default else ""
        cypher = f"ALTER TABLE MemoryNode ADD IF NOT EXISTS {col} {typ}{default_clause}"
        try:
            conn.execute(cypher)
            print(f"  ✅ {col} {typ}{default_clause}")
            changes += 1
        except Exception as exc:
            msg = str(exc)
            if "already exist" in msg.lower() or "already exists" in msg.lower():
                print(f"  ✓  {col} (already present)")
            else:
                print(f"  ⚠️  {col}: {exc}")

    conn.close()
    print(f"\n✅ LadybugDB schema initialized/migrated ({changes} changes applied)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Initialize NIMA LadybugDB schema"
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Path to ladybug.lbug (default: $NIMA_HOME/memory/ladybug.lbug)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without touching the database",
    )
    args = parser.parse_args()

    if args.db:
        db_path = Path(args.db)
    else:
        nima_home = os.environ.get("NIMA_HOME", os.path.expanduser("~/.nima"))
        db_path = Path(nima_home) / "memory" / "ladybug.lbug"

    init_ladybug(db_path, dry_run=args.dry_run)
