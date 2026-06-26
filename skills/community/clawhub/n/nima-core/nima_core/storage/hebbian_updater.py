#!/usr/bin/env python3
"""
Hebbian Graph Updater
=====================

Live edge-weight updates for NIMA's memory graph, based on co-activation.

    "Neurons that fire together, wire together."
    — Donald O. Hebb, *The Organization of Behavior*, 1949.

This module implements:
  • Hebbian strengthening of edges between concurrently recalled memories.
  • Exponential decay of edges that fall out of use.
  • Bulk boost scores for graph-augmented re-ranking.

All SQL uses parameterised queries (? placeholders).  No user-controlled
data is ever interpolated into SQL text, so SQL-injection is structurally
impossible.

Usage:
    from nima_core.storage.hebbian_updater import HebbianGraphUpdater

    updater = HebbianGraphUpdater(db_path="/path/to/graph.sqlite")
    updater.update_from_query_result([node_id_1, node_id_2, node_id_3])
    boosts  = updater.get_hebbian_boost(candidates, top_results)
"""

import sqlite3
import time
import os
import logging
import threading
from pathlib import Path
from typing import Dict, List, Set, Tuple
from contextlib import contextmanager

# Import connection pool components
from nima_core.connection_pool import get_pool, SQLiteConnectionPool

logger = logging.getLogger(__name__)


class HebbianGraphUpdater:
    """
    Manages Hebbian associative learning for NIMA memory graph edges.

    Hebbian update rule
    -------------------
        w_new = w_old + α · (1 − w_old)

    Where:
        α  = learning_rate  (default 0.1)

    Decay (applied to edges that were NOT co-activated)
    ---------------------------------------------------
        w_new = w_old · (1 − decay_rate)

    Storage
    -------
    Writes to a dedicated ``hebbian_edges`` table in the memory-graph
    SQLite database.  The table is created automatically on first use.

    Performance
    -----------
    All hot paths use indexed queries.  Target: < 50 ms per recall update
    for typical result sets of 7–10 memories.
    """

    def __init__(
        self,
        db_path: str,
        learning_rate: float = 0.1,
        decay_rate: float = 0.02,
        max_weight: float = 1.0,
        min_weight: float = 0.0,
    ) -> None:
        """
        Args:
            db_path:       Absolute path to the SQLite memory-graph database.
            learning_rate: α in the Hebbian rule — how quickly edges strengthen.
            decay_rate:    Fractional decay per update cycle for unused edges.
            max_weight:    Upper clamp on edge weight.
            min_weight:    Lower clamp (edges below 0.01 are pruned automatically).
        """
        self.db_path = str(Path(db_path))  # Keep as string for pool compatibility
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate
        self.max_weight = max_weight
        self.min_weight = min_weight

        self._init_schema()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_schema(self) -> None:
        """Create the ``hebbian_edges`` table and indexes if absent."""
        with get_pool(self.db_path).get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS hebbian_edges (
                    node_a         INTEGER NOT NULL,
                    node_b         INTEGER NOT NULL,
                    weight         REAL    NOT NULL DEFAULT 0.0,
                    co_activations INTEGER NOT NULL DEFAULT 0,
                    last_updated   INTEGER,
                    PRIMARY KEY (node_a, node_b)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_hebb_a
                ON hebbian_edges (node_a)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_hebb_b
                ON hebbian_edges (node_b)
            """)
            conn.commit()

    @staticmethod
    def _ordered(a: int, b: int) -> Tuple[int, int]:
        """Return *(min, max)* so edges are always stored in consistent order."""
        return (a, b) if a < b else (b, a)

    @staticmethod
    def _now_ms() -> int:
        """Current wall-clock time in milliseconds."""
        return int(time.time() * 1_000)

    @staticmethod
    def _gen_pairs(node_ids: List[int]) -> List[Tuple[int, int]]:
        """Generate all unique ordered pairs from *node_ids*."""
        pairs = []
        for i, a in enumerate(node_ids):
            for b in node_ids[i + 1 :]:
                pairs.append(HebbianGraphUpdater._ordered(a, b))
        return pairs

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update_from_query_result(self, activated_node_ids: List[int]) -> int:
        """
        Strengthen edges between all pairs of co-activated memories.

        Call this after every recall query with the full list of returned
        node IDs.  If fewer than two nodes are provided the call is a no-op.

        Args:
            activated_node_ids: Node IDs returned by the current query.

        Returns:
            Number of edges created or updated.
        """
        if not activated_node_ids or len(activated_node_ids) < 2:
            return 0

        # Validate all IDs are integers (SQLite row IDs).
        # Only convert floats that are whole numbers, then deduplicate preserving order.
        activated_node_ids = [
            int(n) if isinstance(n, float) else n
            for n in activated_node_ids
            if isinstance(n, (int, float))
            and not isinstance(n, bool)
            and (not isinstance(n, float) or n.is_integer())
        ]
        activated_node_ids = list(dict.fromkeys(activated_node_ids))
        if len(activated_node_ids) < 2:
            return 0

        pairs = self._gen_pairs(activated_node_ids)
        if not pairs:
            return 0

        t0 = time.time()
        with get_pool(self.db_path).get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            ts = self._now_ms()

            # Batch UPSERT: single executemany() with ON CONFLICT DO UPDATE
            conn.executemany(
                """
                INSERT INTO hebbian_edges (node_a, node_b, weight, co_activations, last_updated)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(node_a, node_b) DO UPDATE SET
                    weight = MIN(?, weight + ? * (1.0 - weight)),
                    co_activations = co_activations + 1,
                    last_updated = ?
                """,
                [
                    (
                        na,
                        nb,
                        self.learning_rate,
                        1,
                        ts,
                        self.max_weight,
                        self.learning_rate,
                        ts,
                    )
                    for na, nb in pairs
                ],
            )

            updated = len(pairs)
            conn.commit()

        elapsed_ms = (time.time() - t0) * 1_000
        if elapsed_ms > 50:
            logger.warning(
                "[hebbian] SLOW: %.1f ms for %d edges", elapsed_ms, len(pairs)
            )

        return updated

    def get_hebbian_boost(
        self,
        candidate_node_ids: List[int],
        top_results: List[int],
    ) -> Dict[int, float]:
        """
        Compute associative-strength boost scores for re-ranking candidates.

        For each candidate, aggregate its Hebbian weights to all ``top_results``
        and normalise by the number of top results.

        Args:
            candidate_node_ids: All candidates being re-ranked.
            top_results:        Node IDs of the initial top-K hits.

        Returns:
            Dict mapping candidate node ID → boost score (0.0–1.0).
        """
        if not candidate_node_ids or not top_results:
            return {}

        with get_pool(self.db_path).get_connection() as conn:
            boost_scores: Dict[int, float] = {}

            # Collect all unique (node_a, node_b) pairs needed
            pairs_needed: Set[Tuple[int, int]] = set()
            for cand in candidate_node_ids:
                for top in top_results:
                    if cand != top:
                        na, nb = self._ordered(cand, top)
                        pairs_needed.add((na, nb))

            if not pairs_needed:
                return {}

            # Build single batched query: WHERE (node_a, node_b) IN (VALUES ...)
            pairs_list = list(pairs_needed)
            placeholders = ",".join(f"({a},{b})" for a, b in pairs_list)
            query = f"""
                SELECT node_a, node_b, weight
                FROM hebbian_edges
                WHERE (node_a, node_b) IN (VALUES {placeholders})
            """
            rows = conn.execute(query).fetchall()

            # Build weight lookup
            pair_weights: Dict[Tuple[int, int], float] = {
                (r[0], r[1]): r[2] for r in rows
            }

            # Aggregate weights per candidate
            n_top = len(top_results)
            for cand in candidate_node_ids:
                total = 0.0
                for top in top_results:
                    if cand != top:
                        na, nb = self._ordered(cand, top)
                        total += pair_weights.get((na, nb), 0.0)
                boost_scores[cand] = total / n_top if n_top else 0.0

        return boost_scores

    def add_hebbian_edges_if_missing(self, node_ids: List[int]) -> None:
        """
        Pre-populate zero-weight edges between all pairs in *node_ids*.

        Safe to call multiple times — existing edges are not modified.

        Args:
            node_ids: Node IDs to inter-connect.
        """
        if len(node_ids) < 2:
            return

        pairs = self._gen_pairs(node_ids)
        ts = self._now_ms()

        with get_pool(self.db_path).get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executemany(
                "INSERT OR IGNORE INTO hebbian_edges"
                " (node_a, node_b, weight, co_activations, last_updated)"
                " VALUES (?, ?, ?, ?, ?)",
                [(node_a, node_b, 0.0, 0, ts) for node_a, node_b in pairs],
            )
            conn.commit()

    def decay_unused_edges(self, activated_node_ids: Set[int]) -> int:
        """
        Decay all edges whose *both* endpoints were NOT in *activated_node_ids*.

        This implements associative forgetting.  Because it scans every edge in
        the table, prefer calling it periodically (e.g., every N queries or in a
        background maintenance pass) rather than on every recall.

        Args:
            activated_node_ids: Set of node IDs that were activated this cycle.

        Returns:
            Number of edges that were decayed or pruned.
        """
        if not activated_node_ids:
            return 0

        with get_pool(self.db_path).get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")

            # Identify active pairs (either endpoint in activated set).
            # Preserve edges where EITHER node_a OR node_b is active.
            # Decay only edges where NEITHER endpoint is active.
            activated_list = list(activated_node_ids)
            placeholders = ",".join("?" * len(activated_list))
            active_pairs: Set[Tuple[int, int]] = set(
                (row[0], row[1])
                for row in conn.execute(
                    f"SELECT node_a, node_b FROM hebbian_edges"
                    f" WHERE node_a IN ({placeholders})"
                    f"    OR node_b IN ({placeholders})",
                    activated_list + activated_list,
                ).fetchall()
            )

            # Fetch all edges and decay those not in active_pairs.
            all_edges = conn.execute(
                "SELECT node_a, node_b, weight FROM hebbian_edges"
            ).fetchall()

            ts = self._now_ms()
            decayed = 0

            for node_a, node_b, weight in all_edges:
                if (node_a, node_b) in active_pairs:
                    continue
                new_w = weight * (1.0 - self.decay_rate)
                new_w = max(self.min_weight, new_w)

                if new_w < 0.01:
                    conn.execute(
                        "DELETE FROM hebbian_edges WHERE node_a = ? AND node_b = ?",
                        (node_a, node_b),
                    )
                else:
                    conn.execute(
                        "UPDATE hebbian_edges"
                        " SET weight = ?, last_updated = ?"
                        " WHERE node_a = ? AND node_b = ?",
                        (new_w, ts, node_a, node_b),
                    )
                decayed += 1

            conn.commit()
            return decayed

    def get_edge_weight(self, node_a: int, node_b: int) -> float:
        """
        Return the Hebbian weight between *node_a* and *node_b*.

        Args:
            node_a: First node ID.
            node_b: Second node ID.

        Returns:
            Weight (0.0–1.0), or 0.0 if no edge exists.
        """
        na, nb = self._ordered(node_a, node_b)
        with get_pool(self.db_path).get_connection() as conn:
            row = conn.execute(
                "SELECT weight FROM hebbian_edges WHERE node_a = ? AND node_b = ?",
                (na, nb),
            ).fetchone()
            return row[0] if row else 0.0

    def stats(self) -> Dict:
        """
        Return summary statistics for the Hebbian edge table.

        Returns:
            Dict with keys: total_edges, avg_weight, max_weight, top_pairs.
        """
        with get_pool(self.db_path).get_connection() as conn:
            row = conn.execute(
                "SELECT COUNT(*), AVG(weight), MAX(weight) FROM hebbian_edges"
            ).fetchone()
            total = row[0] or 0
            avg_w = row[1] or 0.0
            max_w = row[2] or 0.0

            top_pairs = conn.execute(
                "SELECT node_a, node_b, weight, co_activations"
                " FROM hebbian_edges"
                " ORDER BY weight DESC LIMIT 10"
            ).fetchall()

            return {
                "total_edges": total,
                "avg_weight": avg_w,
                "max_weight": max_w,
                "top_pairs": [(r[0], r[1], r[2], r[3]) for r in top_pairs],
            }


# ---------------------------------------------------------------------------
# CLI (python -m storage.hebbian_updater --test)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import tempfile
    import shutil

    parser = argparse.ArgumentParser(description="Hebbian Graph Updater")
    parser.add_argument(
        "--db",
        default=os.path.expanduser(
            os.environ.get("NIMA_SQLITE_DB", "~/.nima/memory/graph.sqlite")
        ),
        help="Path to memory graph SQLite DB (default: $NIMA_SQLITE_DB or ~/.nima/memory/graph.sqlite)",
    )
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    args = parser.parse_args()

    if args.test:
        # Use a fresh temp DB so tests never touch real data.
        tmp_dir = tempfile.mkdtemp()
        tmp_db = os.path.join(tmp_dir, "hebb_test.db")

        # Bootstrap minimal schema that HebbianGraphUpdater depends on.
        conn = sqlite3.connect(tmp_db)
        conn.execute(
            "CREATE TABLE memory_nodes (id INTEGER PRIMARY KEY, turn_id TEXT, themes TEXT DEFAULT '[]')"
        )
        conn.commit()
        conn.close()

        u = HebbianGraphUpdater(tmp_db)

        try:
            print("🧠 Hebbian Updater — self-test\n" + "=" * 40)

            u.add_hebbian_edges_if_missing([1, 2, 3, 4, 5])
            print("  ✅ add_hebbian_edges_if_missing")

            for _ in range(5):
                u.update_from_query_result([1, 2, 3])
            print("  ✅ update_from_query_result (5 × [1,2,3])")

            w12 = u.get_edge_weight(1, 2)
            w45 = u.get_edge_weight(4, 5)
            assert w12 > w45, f"Expected 1–2 stronger than 4–5 ({w12} vs {w45})"
            print(f"  ✅ get_edge_weight: 1-2={w12:.4f}, 4-5={w45:.4f}")

            boost = u.get_hebbian_boost([1, 2, 3, 4, 5], [1, 2])
            assert boost[3] > 0, "Node 3 co-activated with 1&2 — should have boost"
            print(f"  ✅ get_hebbian_boost: {boost}")

            s = u.stats()
            assert s["total_edges"] >= 3
            print(f"  ✅ stats: {s['total_edges']} edges, max_w={s['max_weight']:.4f}")

            print("\n🎉 All tests passed!")
        finally:
            shutil.rmtree(tmp_dir)
    else:
        u = HebbianGraphUpdater(args.db)
        s = u.stats()
        print(
            f"📊 Hebbian Graph — {s['total_edges']} edges"
            f" | avg={s['avg_weight']:.4f} | max={s['max_weight']:.4f}"
        )
