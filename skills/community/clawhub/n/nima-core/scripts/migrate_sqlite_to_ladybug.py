"""
migrate_sqlite_to_ladybug.py — One-shot idempotent migration of memory_nodes
from SQLite (graph.sqlite) into LadybugDB (ladybug.lbug).

Usage:
    python3 scripts/migrate_sqlite_to_ladybug.py [OPTIONS]

Options:
    --dry-run        Count rows and preview first 3, do not write anything
    --batch-size N   Process N rows per batch (default: 100)
    --db PATH        Override SQLite source path
    --ladybug PATH   Override LadybugDB target path
    --force          Re-migrate nodes already in LadybugDB (overwrite)
    --verbose        Print each node id as it is migrated

Environment:
    NIMA_HOME        Base directory (default: ~/.nima)
    NIMA_DB_PATH     SQLite path (default: $NIMA_HOME/memory/graph.sqlite)
    NIMA_LADYBUG_DB  LadybugDB path (default: $NIMA_HOME/memory/ladybug.lbug)

Notes:
    CRITICAL: conn.execute("LOAD VECTOR") must be called before any
    CREATE/SET/DELETE on tables with FLOAT[512] columns (like MemoryNode).
    Without it, mutations cause SIGSEGV in the Kùzu engine.
"""

import argparse
import logging
import os
import sqlite3
import struct
import sys

# ---------------------------------------------------------------------------
# Config import — try package first, fall back to env/defaults
# ---------------------------------------------------------------------------
try:
    from nima_core.config import NIMA_HOME, NIMA_DB_PATH, NIMA_LADYBUG_DB
except ImportError:
    # Fallback: script may be run directly from repo root
    _repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, _repo_root)
    try:
        from nima_core.config import NIMA_HOME, NIMA_DB_PATH, NIMA_LADYBUG_DB
    except ImportError:
        # Last resort: compute from environment
        NIMA_HOME = os.path.expanduser(os.environ.get("NIMA_HOME", "~/.nima"))
        NIMA_DB_PATH = os.environ.get(
            "NIMA_DB_PATH", os.path.join(NIMA_HOME, "memory", "graph.sqlite")
        )
        NIMA_LADYBUG_DB = os.environ.get(
            "NIMA_LADYBUG_DB", os.path.join(NIMA_HOME, "memory", "ladybug.lbug")
        )

# ---------------------------------------------------------------------------
# LadybugDB import
# ---------------------------------------------------------------------------
try:
    import real_ladybug as lb
except ImportError:
    # Try common venv paths
    _nima_home = os.path.expanduser(os.environ.get("NIMA_HOME", "~/.nima"))
    _venv_paths = [
        os.path.join(_nima_home, ".venv", "lib", f"python{v}", "site-packages")
        for v in ["3.14", "3.13", "3.12", "3.11"]
    ]
    _imported = False
    for _vp in _venv_paths:
        if os.path.exists(_vp) and _vp not in sys.path:
            sys.path.insert(0, _vp)
            try:
                import real_ladybug as lb
                _imported = True
                break
            except ImportError:
                continue
    if not _imported:
        print(
            "ERROR: 'real_ladybug' package not found.\n"
            "Install it with: pip install real-ladybug\n"
            "Or activate your virtual environment: source ~/.nima/.venv/bin/activate",
            file=sys.stderr,
        )
        sys.exit(1)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

EMBEDDING_DIM = 512


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_embedding(blob) -> list | None:
    """Unpack raw BLOB bytes into a list of 512 floats, or return None."""
    if blob is None:
        return None
    expected = EMBEDDING_DIM * 4  # float32 = 4 bytes
    if len(blob) != expected:
        return None
    try:
        return list(struct.unpack(f"{EMBEDDING_DIM}f", blob))
    except struct.error:
        return None


def node_exists(conn, node_id: int) -> bool:
    """Return True if a MemoryNode with this id already exists in LadybugDB."""
    try:
        result = conn.execute(
            "MATCH (n:MemoryNode {id: $id}) RETURN n.id",
            {"id": node_id}
        ).fetch()
        return len(result) > 0
    except Exception:
        return False


def build_params(row: dict) -> dict:
    """Map a SQLite row dict to LadybugDB MemoryNode params."""
    embedding = parse_embedding(row.get("embedding"))

    params = {
        "id": int(row["id"]),
        "timestamp": int(row["timestamp"]),
        "layer": row["layer"] or "",
        "text": row["text"] or "",
        "summary": row["summary"] or "",
        "who": row.get("who") or "",
        "affect_json": row.get("affect_json") or "{}",
        "session_key": row.get("session_key") or "",
        "conversation_id": row.get("conversation_id") or "",
        "turn_id": row.get("turn_id") or "",
        "fe_score": float(row["fe_score"]) if row.get("fe_score") is not None else 0.5,
        "strength": float(row["strength"]) if row.get("strength") is not None else 1.0,
        "decay_rate": float(row["decay_rate"]) if row.get("decay_rate") is not None else 0.01,
        "last_accessed": int(row.get("last_accessed") or 0),
        "is_ghost": bool(row.get("is_ghost", 0)),
        "dismissal_count": int(row.get("dismissal_count") or 0),
        "themes": row.get("themes") or "[]",
        # LadybugDB-only columns — defaults
        "recall_count": 0,
        "memory_type": None,
        "importance": None,
        "emotions": None,
        "source_agent": None,
        "model": None,
    }

    if embedding is not None:
        params["embedding"] = embedding

    return params


def insert_node(conn, params: dict) -> None:
    """INSERT a new MemoryNode into LadybugDB."""
    if "embedding" in params:
        query = """
        CREATE (n:MemoryNode {
            id: $id,
            timestamp: $timestamp,
            layer: $layer,
            text: $text,
            summary: $summary,
            who: $who,
            affect_json: $affect_json,
            session_key: $session_key,
            conversation_id: $conversation_id,
            turn_id: $turn_id,
            fe_score: $fe_score,
            embedding: $embedding,
            strength: $strength,
            decay_rate: $decay_rate,
            last_accessed: $last_accessed,
            is_ghost: $is_ghost,
            dismissal_count: $dismissal_count,
            themes: $themes,
            recall_count: $recall_count,
            memory_type: $memory_type,
            importance: $importance,
            emotions: $emotions,
            source_agent: $source_agent,
            model: $model
        })
        """
    else:
        query = """
        CREATE (n:MemoryNode {
            id: $id,
            timestamp: $timestamp,
            layer: $layer,
            text: $text,
            summary: $summary,
            who: $who,
            affect_json: $affect_json,
            session_key: $session_key,
            conversation_id: $conversation_id,
            turn_id: $turn_id,
            fe_score: $fe_score,
            strength: $strength,
            decay_rate: $decay_rate,
            last_accessed: $last_accessed,
            is_ghost: $is_ghost,
            dismissal_count: $dismissal_count,
            themes: $themes,
            recall_count: $recall_count,
            memory_type: $memory_type,
            importance: $importance,
            emotions: $emotions,
            source_agent: $source_agent,
            model: $model
        })
        """
    conn.execute(query, params)


def upsert_node(conn, params: dict) -> None:
    """MERGE (upsert) a MemoryNode into LadybugDB (--force mode)."""
    if "embedding" in params:
        query = """
        MERGE (n:MemoryNode {id: $id})
        SET n.timestamp = $timestamp,
            n.layer = $layer,
            n.text = $text,
            n.summary = $summary,
            n.who = $who,
            n.affect_json = $affect_json,
            n.session_key = $session_key,
            n.conversation_id = $conversation_id,
            n.turn_id = $turn_id,
            n.fe_score = $fe_score,
            n.embedding = $embedding,
            n.strength = $strength,
            n.decay_rate = $decay_rate,
            n.last_accessed = $last_accessed,
            n.is_ghost = $is_ghost,
            n.dismissal_count = $dismissal_count,
            n.themes = $themes,
            n.recall_count = $recall_count,
            n.memory_type = $memory_type,
            n.importance = $importance,
            n.emotions = $emotions,
            n.source_agent = $source_agent,
            n.model = $model
        """
    else:
        query = """
        MERGE (n:MemoryNode {id: $id})
        SET n.timestamp = $timestamp,
            n.layer = $layer,
            n.text = $text,
            n.summary = $summary,
            n.who = $who,
            n.affect_json = $affect_json,
            n.session_key = $session_key,
            n.conversation_id = $conversation_id,
            n.turn_id = $turn_id,
            n.fe_score = $fe_score,
            n.strength = $strength,
            n.decay_rate = $decay_rate,
            n.last_accessed = $last_accessed,
            n.is_ghost = $is_ghost,
            n.dismissal_count = $dismissal_count,
            n.themes = $themes,
            n.recall_count = $recall_count,
            n.memory_type = $memory_type,
            n.importance = $importance,
            n.emotions = $emotions,
            n.source_agent = $source_agent,
            n.model = $model
        """
    conn.execute(query, params)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Migrate memory_nodes from SQLite to LadybugDB (idempotent)."
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--batch-size", type=int, default=100, metavar="N")
    parser.add_argument("--db", default=None, metavar="PATH", help="SQLite source path")
    parser.add_argument("--ladybug", default=None, metavar="PATH", help="LadybugDB path")
    parser.add_argument("--force", action="store_true", help="Overwrite existing nodes")
    parser.add_argument("--verbose", action="store_true", help="Print each node id")
    args = parser.parse_args()

    sqlite_path = args.db or NIMA_DB_PATH
    ladybug_path = args.ladybug or NIMA_LADYBUG_DB

    # Validate paths
    if not os.path.exists(sqlite_path):
        print(f"ERROR: SQLite database not found: {sqlite_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(ladybug_path):
        print(
            f"ERROR: LadybugDB not found: {ladybug_path}\n"
            "Run: python3 scripts/init_ladybug.py first",
            file=sys.stderr,
        )
        sys.exit(1)

    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_conn.execute("PRAGMA journal_mode=WAL")

    # Connect to LadybugDB
    db = lb.Database(str(ladybug_path))
    conn = lb.Connection(db)

    # CRITICAL: Load VECTOR extension before any CREATE/SET/DELETE on FLOAT[512] columns
    try:
        conn.execute("LOAD VECTOR")
    except (OSError, RuntimeError) as e:
        logger.debug("LOAD VECTOR skipped (may not exist yet): %s", e)

    # Fetch all non-ghost rows
    cursor = sqlite_conn.execute(
        "SELECT * FROM memory_nodes WHERE is_ghost = 0 ORDER BY id"
    )
    rows = cursor.fetchall()
    total = len(rows)

    if args.dry_run:
        print(f"DRY RUN — {total} non-ghost nodes found in SQLite")
        print(f"SQLite:   {sqlite_path}")
        print(f"LadybugDB: {ladybug_path}")
        print()
        preview = rows[:3]
        for i, row in enumerate(preview, 1):
            r = dict(row)
            emb_blob = r.get("embedding")
            embedding_info = f"embedding={len(emb_blob)} bytes" if emb_blob else "embedding=None"
            print(
                f"  [{i}] id={r['id']} layer={r['layer']!r} "
                f"timestamp={r['timestamp']} {embedding_info}"
            )
        sqlite_conn.close()
        return

    migrated = 0
    skipped = 0
    error_count = 0

    for batch_start in range(0, total, args.batch_size):
        batch = rows[batch_start : batch_start + args.batch_size]
        print(f"Migrating: {min(batch_start + args.batch_size, total)}/{total}...")

        for row in batch:
            row_dict = dict(row)
            node_id = row_dict["id"]

            try:
                if not args.force:
                    exists = node_exists(conn, node_id)
                    if exists:
                        if args.verbose:
                            print(f"  SKIP id={node_id} (already exists)")
                        skipped += 1
                        continue

                params = build_params(row_dict)

                if args.force:
                    upsert_node(conn, params)
                    if args.verbose:
                        print(f"  UPSERT id={node_id}")
                else:
                    insert_node(conn, params)
                    if args.verbose:
                        print(f"  INSERT id={node_id}")

                migrated += 1

            except Exception as exc:
                logger.warning("Failed to migrate node id=%s: %s", node_id, exc)
                error_count += 1

    sqlite_conn.close()

    print(
        f"✅ Migration complete: {migrated} nodes migrated, "
        f"{skipped} skipped, {error_count} errors"
    )

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
