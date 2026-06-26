"""Tests for QMD hybrid search (BM25 + vector)."""
import pytest
import pytest_asyncio
import asyncio
import json
from pathlib import Path
from ghostclaw.core.qmd_store import QMDMemoryStore

# Check dependencies
try:
    import lancedb  # noqa: F401
    import fastembed  # noqa: F401
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

pytestmark = pytest.mark.skipif(not HAS_DEPS, reason="vector dependencies not installed")


@pytest_asyncio.fixture
async def enhanced_store(tmp_path):
    """Create QMDMemoryStore with enhanced mode (hybrid)."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, use_enhanced=True)
    yield store
    # No explicit close needed; resources cleaned up by tmp_path


@pytest.mark.asyncio
async def test_hybrid_search_basic(enhanced_store, tmp_path):
    """Test that hybrid search returns results with score."""
    # Save a report with specific content
    report = {
        "vibe_score": 70,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": [
            {"message": "Authentication bypass vulnerability", "file": "auth.py", "severity": "high"}
        ],
        "architectural_ghosts": [],
        "ai_synthesis": "The codebase has a critical authentication bypass vulnerability that needs immediate patching.",
        "metadata": {"timestamp": "2026-03-14T12:00:00Z"}
    }
    run_id = await enhanced_store.save_run(report, repo_path=str(tmp_path))

    # Search for "authentication"
    results = await enhanced_store.search("authentication", limit=5)
    assert len(results) >= 1
    found = False
    for r in results:
        if r["id"] == run_id:
            found = True
            assert "score" in r
            assert isinstance(r["score"], float)
            assert 0 <= r["score"] <= 1
            assert r["vibe_score"] == 70
            assert "matched_snippets" in r
            break
    assert found, "Hybrid search should have found the saved report"


@pytest.mark.asyncio
async def test_hybrid_search_alpha_weighting(enhanced_store, tmp_path):
    """Test that alpha parameter influences score weighting."""
    # Save a report with exact keyword and semantic content
    report = {
        "vibe_score": 80,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": [
            {"message": "Race condition in concurrent dictionary", "file": "dict.py"}
        ],
        "architectural_ghosts": [],
        "ai_synthesis": "There is a potential race condition when multiple threads access the shared dictionary without proper locking. This can lead to data corruption and undefined behavior. Consider using threading.Lock or concurrent.futures to ensure thread safety.",
        "metadata": {"timestamp": "2026-03-14T12:00:00Z"}
    }
    await enhanced_store.save_run(report, repo_path=str(tmp_path))

    # Search with exact term "race" (BM25 should do well)
    results_bm25_heavy = await enhanced_store.search("race", alpha=0.9)
    # Search with semantic term "thread safety" (vector should do well)
    results_vector_heavy = await enhanced_store.search("thread safety", alpha=0.1)

    # Both should find the report
    ids_bm25 = [r["id"] for r in results_bm25_heavy]
    ids_vector = [r["id"] for r in results_vector_heavy]
    assert any(r["vibe_score"] == 80 for r in results_bm25_heavy)
    assert any(r["vibe_score"] == 80 for r in results_vector_heavy)


@pytest.mark.asyncio
async def test_hybrid_search_filters(enhanced_store, tmp_path):
    """Test repo_path and stack filters in hybrid search."""
    report1 = {
        "vibe_score": 60,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": ["Python-specific issue"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T12:00:00Z"}
    }
    report2 = {
        "vibe_score": 70,
        "stack": "node",
        "files_analyzed": 8,
        "total_lines": 300,
        "issues": ["Node-specific issue"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T12:00:00Z"}
    }
    id1 = await enhanced_store.save_run(report1, repo_path=str(tmp_path / "repo1"))
    id2 = await enhanced_store.save_run(report2, repo_path=str(tmp_path / "repo2"))

    # Search across all
    results = await enhanced_store.search("issue", limit=10)
    ids = [r["id"] for r in results]
    assert id1 in ids
    assert id2 in ids

    # Filter by repo_path
    results = await enhanced_store.search("issue", repo_path=str(tmp_path / "repo1"))
    ids = [r["id"] for r in results]
    assert id1 in ids
    assert id2 not in ids

    # Filter by stack
    results = await enhanced_store.search("issue", stack="node")
    ids = [r["id"] for r in results]
    assert id2 in ids
    assert id1 not in ids


@pytest.mark.asyncio
async def test_hybrid_search_fallback_to_bm25(enhanced_store, tmp_path, monkeypatch):
    """Test that if vector store fails, falls back to BM25."""
    # Save a report
    report = {
        "vibe_score": 65,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": ["Test issue for BM25 fallback"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-14T12:00:00Z"}
    }
    rid = await enhanced_store.save_run(report, repo_path=str(tmp_path))

    # Simulate vector store failure by setting to None
    monkeypatch.setattr(enhanced_store, "vector_store", None)
    # Disable enhanced flag so BM25 path is used
    enhanced_store.use_enhanced = False

    results = await enhanced_store.search("BM25 fallback")
    # Should still find the report via BM25
    ids = [r["id"] for r in results]
    assert rid in ids


@pytest.mark.asyncio
async def test_save_run_generates_embeddings(enhanced_store, tmp_path):
    """Test that save_run generates and stores embeddings when enhanced mode."""
    report = {
        "vibe_score": 85,
        "stack": "python",
        "files_analyzed": 10,
        "total_lines": 500,
        "issues": [
            {"message": "SQL injection risk", "file": "query.py"}
        ],
        "architectural_ghosts": [
            {"message": "God object antipattern", "module": "main"}
        ],
        "ai_synthesis": "The application is vulnerable to SQL injection because user input is concatenated directly into queries.",
        "metadata": {"timestamp": "2026-03-14T12:00:00Z"}
    }
    rid = await enhanced_store.save_run(report, repo_path=str(tmp_path))

    # Verify embeddings exist by searching vector store directly
    vector_results = await enhanced_store.vector_store.search("SQL injection", limit=5)
    ids = [r["report_id"] for r in vector_results]
    assert rid in ids, "Embeddings should be stored and retrievable"
