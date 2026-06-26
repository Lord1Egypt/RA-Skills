"""Tests for BM25 search via SQLite FTS5."""
import pytest
import asyncio
from pathlib import Path
from ghostclaw.core.qmd_store import QMDMemoryStore

# Check if SQLite has FTS5
import sqlite3
try:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE VIRTUAL TABLE test_fts USING fts5(content)")
    conn.close()
    HAS_FTS5 = True
except sqlite3.OperationalError:
    HAS_FTS5 = False

pytestmark = pytest.mark.skipif(not HAS_FTS5, reason="SQLite FTS5 not available")


@pytest.mark.asyncio
async def test_bm25_basic(tmp_path):
    """Test basic BM25 keyword search."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, use_enhanced=False)  # Use BM25-only

    # Create reports with distinct content
    report1 = {
        "vibe_score": 70,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": [{"message": "Authentication bypass vulnerability", "file": "auth.py"}],
        "architectural_ghosts": [],
        "ai_synthesis": "Critical security issue found.",
        "metadata": {"timestamp": "2026-03-14T10:00:00Z"}
    }
    report2 = {
        "vibe_score": 80,
        "stack": "node",
        "files_analyzed": 8,
        "total_lines": 300,
        "issues": [{"message": "Memory leak in event loop"}],
        "architectural_ghosts": [{"message": "Callback hell"}],
        "ai_synthesis": "Performance issues due to memory leaks.",
        "metadata": {"timestamp": "2026-03-14T10:01:00Z"}
    }

    rid1 = await store.save_run(report1, repo_path=str(tmp_path))
    rid2 = await store.save_run(report2, repo_path=str(tmp_path))

    # Search for "authentication"
    results = await store.search("authentication")
    assert len(results) >= 1
    assert any(r["id"] == rid1 for r in results)
    # First result should be the one with authentication
    assert results[0]["id"] == rid1
    assert "score" in results[0]  # BM25 score present

    # Search for "memory leak"
    results = await store.search("memory leak")
    assert any(r["id"] == rid2 for r in results)

    # Search for "callback"
    results = await store.search("callback")
    assert any(r["id"] == rid2 for r in results)


@pytest.mark.asyncio
async def test_bm25_stemming(tmp_path):
    """Test that stemming works (e.g., 'running' matches 'run')."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, use_enhanced=False)

    report = {
        "vibe_score": 75,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": [{"message": "The function is running too slowly"}],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T10:00:00Z"}
    }
    rid = await store.save_run(report, repo_path=str(tmp_path))

    # Search for "run" should match "running"
    results = await store.search("run")
    assert any(r["id"] == rid for r in results)


@pytest.mark.asyncio
async def test_bm25_phrase_search(tmp_path):
    """Test exact phrase search with quotes."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, use_enhanced=False)

    report = {
        "vibe_score": 65,
        "stack": "java",
        "files_analyzed": 10,
        "total_lines": 500,
        "issues": [{"message": "Null pointer exception risk"}],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T10:00:00Z"}
    }
    rid = await store.save_run(report, repo_path=str(tmp_path))

    # Phrase search
    results = await store.search('"null pointer"')
    assert any(r["id"] == rid for r in results)

    # Non-matching phrase
    results = await store.search('"pointer null"')  # reversed
    assert not any(r["id"] == rid for r in results)


@pytest.mark.asyncio
async def test_bm25_filters(tmp_path):
    """Test repo_path and stack filters."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, use_enhanced=False)

    report1 = {
        "vibe_score": 60,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": ["Filter test issue"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T10:00:00Z"}
    }
    report2 = {
        "vibe_score": 70,
        "stack": "node",
        "files_analyzed": 8,
        "total_lines": 300,
        "issues": ["Another filter test"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T10:01:00Z"}
    }
    rid1 = await store.save_run(report1, repo_path=str(tmp_path / "repo1"))
    rid2 = await store.save_run(report2, repo_path=str(tmp_path / "repo2"))

    # Search without filter — both found
    results = await store.search("filter test")
    ids = [r["id"] for r in results]
    assert rid1 in ids and rid2 in ids

    # Filter by repo_path
    results = await store.search("filter test", repo_path=str(tmp_path / "repo1"))
    ids = [r["id"] for r in results]
    assert rid1 in ids and rid2 not in ids

    # Filter by stack
    results = await store.search("filter test", stack="node")
    ids = [r["id"] for r in results]
    assert rid2 in ids and rid1 not in ids

    # Filter by vibe_score range
    results = await store.search("filter test", min_score=65)
    ids = [r["id"] for r in results]
    assert rid2 in ids and rid1 not in ids


@pytest.mark.asyncio
async def test_bm25_ranking(tmp_path):
    """Test that BM25 returns results ordered by score (lower bm25 = better)."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, use_enhanced=False)

    # Create reports with varying term frequency
    report1 = {
        "vibe_score": 70,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": [{"message": "security security security security"}],  # high TF
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T10:00:00Z"}
    }
    report2 = {
        "vibe_score": 70,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": [{"message": "security issue"}],  # lower TF
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T10:01:00Z"}
    }
    rid1 = await store.save_run(report1, repo_path=str(tmp_path))
    rid2 = await store.save_run(report2, repo_path=str(tmp_path))

    results = await store.search("security")
    ids = [r["id"] for r in results]
    # Report with higher term frequency should rank higher (score closer to 0)
    if len(ids) >= 2:
        # BM25 score is negative of raw bm25 (so higher = better)
        # Expect high TF to have higher score (less negative bm25)
        score1 = next(r["score"] for r in results if r["id"] == rid1)
        score2 = next(r["score"] for r in results if r["id"] == rid2)
        assert score1 >= score2, "Higher term frequency should yield better BM25 score"
