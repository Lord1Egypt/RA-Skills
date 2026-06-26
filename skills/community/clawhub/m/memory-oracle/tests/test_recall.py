#!/usr/bin/env python3
"""
memory-oracle: test_recall.py
Tests for recall ranking, budget allocation, and slot mechanics.

Usage:
  python3 test_recall.py
"""

import json
import os
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from init_db import init_db, generate_id, content_hash, load_settings, utcnow
from recall import (
    slot_guardrails, slot_fresh, slot_relevant,
    compute_live_score, estimate_tokens, fallback_grep
)

SETTINGS = load_settings()


def create_test_db():
    """Create an in-memory test database with sample data."""
    db_path = os.path.join(tempfile.gettempdir(), "memory_oracle_test.db")
    if os.path.exists(db_path):
        os.unlink(db_path)

    conn = init_db(db_path)
    now = utcnow()

    # Add guardrails
    conn.execute(
        "INSERT INTO guardrails (id, content, created_at, source, active) VALUES (?, ?, ?, 'test', 1)",
        ("g1", "Never execute trades without approval", now.isoformat()),
    )
    conn.execute(
        "INSERT INTO guardrails (id, content, created_at, source, active) VALUES (?, ?, ?, 'test', 1)",
        ("g2", "Always use WAL mode for SQLite", now.isoformat()),
    )

    # Add fresh facts (last 24h)
    for i in range(5):
        fid = f"fresh_{i}"
        age = timedelta(hours=i * 4)  # 0h, 4h, 8h, 12h, 16h ago
        created = (now - age).isoformat()
        conn.execute(
            """INSERT INTO facts (id, type, content, content_hash, base_importance,
               score, status, source, confidence, access_count, created_at, updated_at)
               VALUES (?, 'decision', ?, ?, ?, ?, 'active', 'test', 0.9, ?, ?, ?)""",
            (fid, f"Fresh fact number {i} about crypto trading", content_hash(f"fresh_{i}"),
             2.0 - i * 0.2, 2.0 - i * 0.2, i, created, now.isoformat()),
        )

    # Add older facts with varying scores
    for i in range(10):
        fid = f"old_{i}"
        age = timedelta(days=5 + i * 3)  # 5, 8, 11... days ago
        created = (now - age).isoformat()
        conn.execute(
            """INSERT INTO facts (id, type, content, content_hash, base_importance,
               score, status, source, confidence, access_count, created_at, updated_at)
               VALUES (?, 'insight', ?, ?, ?, ?, 'active', 'test', 0.8, ?, ?, ?)""",
            (fid, f"Old fact about {'crypto' if i < 5 else 'Python'} topic {i}",
             content_hash(f"old_{i}"), 1.5, 1.5 - i * 0.1, 10 - i, created, now.isoformat()),
        )

    # Add a low-score fact that should not appear
    conn.execute(
        """INSERT INTO facts (id, type, content, content_hash, base_importance,
           score, status, source, confidence, access_count, created_at, updated_at)
           VALUES (?, 'insight', ?, ?, 0.1, 0.05, 'active', 'test', 0.5, 0, ?, ?)""",
        ("dead_1", "Very old irrelevant fact", content_hash("dead_1"),
         (now - timedelta(days=100)).isoformat(), now.isoformat()),
    )

    conn.commit()
    conn.row_factory = sqlite3.Row
    return conn, db_path


def test_guardrails_slot():
    conn, db_path = create_test_db()
    facts, used = slot_guardrails(conn, 500)
    assert len(facts) == 2, f"Expected 2 guardrails, got {len(facts)}"
    assert all(f["slot"] == "guardrail" for f in facts)
    assert used > 0
    conn.close()
    os.unlink(db_path)
    print("  ✓ Guardrails slot: returns active guardrails")


def test_fresh_slot():
    conn, db_path = create_test_db()
    now = utcnow()
    facts, used = slot_fresh(conn, 1000, now)
    assert len(facts) > 0, "Expected fresh facts"
    assert all(f["slot"] == "fresh" for f in facts)
    # Should be ordered by importance
    importances = [f["score"] for f in facts]
    assert importances == sorted(importances, reverse=True), "Fresh facts should be sorted by score"
    conn.close()
    os.unlink(db_path)
    print("  ✓ Fresh slot: returns recent facts sorted by importance")


def test_relevant_slot():
    conn, db_path = create_test_db()
    now = utcnow()
    facts, used = slot_relevant(conn, "crypto trading", 1000, now, set())
    assert len(facts) > 0, "Expected relevant facts for 'crypto'"
    # Crypto facts should rank higher
    crypto_count = sum(1 for f in facts if "crypto" in f["content"].lower())
    assert crypto_count > 0, "Should find crypto-related facts"
    conn.close()
    os.unlink(db_path)
    print("  ✓ Relevant slot: FTS5 search finds matching facts")


def test_budget_enforcement():
    conn, db_path = create_test_db()
    now = utcnow()
    # Very small budget
    facts, used = slot_fresh(conn, 50, now)
    assert used <= 50, f"Budget exceeded: {used} > 50"
    conn.close()
    os.unlink(db_path)
    print("  ✓ Budget enforcement: respects token limits")


def test_dedup_across_slots():
    conn, db_path = create_test_db()
    now = utcnow()
    guard_facts, _ = slot_guardrails(conn, 500)
    fresh_facts, _ = slot_fresh(conn, 1000, now)
    exclude = {f["id"] for f in guard_facts + fresh_facts}
    relevant_facts, _ = slot_relevant(conn, "crypto", 1000, now, exclude)

    all_ids = [f["id"] for f in guard_facts + fresh_facts + relevant_facts]
    assert len(all_ids) == len(set(all_ids)), "Duplicate IDs found across slots"
    conn.close()
    os.unlink(db_path)
    print("  ✓ Dedup: no duplicates across slots")


def test_decay_scoring():
    now = utcnow()

    # Fresh fact
    fresh_row = {
        "base_importance": 1.0,
        "created_at": now.isoformat(),
        "access_count": 0,
    }
    fresh_score = compute_live_score(fresh_row, now)

    # 30-day old fact, no access
    old_row = {
        "base_importance": 1.0,
        "created_at": (now - timedelta(days=30)).isoformat(),
        "access_count": 0,
    }
    old_score = compute_live_score(old_row, now)

    # 30-day old fact, 10 accesses
    accessed_row = {
        "base_importance": 1.0,
        "created_at": (now - timedelta(days=30)).isoformat(),
        "access_count": 10,
    }
    accessed_score = compute_live_score(accessed_row, now)

    assert fresh_score > old_score, "Fresh should score higher than old"
    assert accessed_score > old_score, "Accessed should score higher than unaccessed"
    print(f"  ✓ Decay scoring: fresh={fresh_score:.3f}, old={old_score:.3f}, accessed={accessed_score:.3f}")


def test_token_estimation():
    assert estimate_tokens("hello") > 0
    assert estimate_tokens("a" * 400) == 100  # 400 chars / 4 chars_per_token
    print("  ✓ Token estimation: reasonable estimates")


def run_tests():
    print("Memory Oracle — Recall Tests\n")
    tests = [
        test_guardrails_slot,
        test_fresh_slot,
        test_relevant_slot,
        test_budget_enforcement,
        test_dedup_across_slots,
        test_decay_scoring,
        test_token_estimation,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except (AssertionError, Exception) as e:
            print(f"  ✗ {test.__name__}: {e}")
            failed += 1

    print(f"\nResults: {passed}/{len(tests)} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
