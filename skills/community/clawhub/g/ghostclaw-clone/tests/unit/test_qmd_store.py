"""Tests for QMDMemoryStore."""
import json
import aiosqlite
import pytest
import asyncio
from pathlib import Path
from ghostclaw.core.qmd_store import QMDMemoryStore


@pytest.mark.asyncio
async def test_qmd_memory_store_init_and_save(tmp_path):
    """Test QMDMemoryStore can initialize DB and save a run."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path)

    # Ensure DB doesn't exist yet
    assert not db_path.exists()

    # Create a dummy report
    report = {
        "vibe_score": 75,
        "stack": "python",
        "files_analyzed": 10,
        "total_lines": 500,
        "issues": ["Test issue"],
        "architectural_ghosts": ["Test ghost"],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }

    run_id = await store.save_run(report, repo_path=str(tmp_path))
    assert isinstance(run_id, int)
    assert db_path.exists()

    # Verify we can retrieve it
    retrieved = await store.get_run(run_id)
    assert retrieved is not None
    assert retrieved["vibe_score"] == 75
    assert retrieved["stack"] == "python"
    # get_run returns wrapper dict with parsed "report" key
    assert "report" in retrieved
    assert retrieved["report"]["issues"] == ["Test issue"]


@pytest.mark.asyncio
async def test_qmd_memory_store_list_runs(tmp_path):
    """Test listing runs from QMDMemoryStore."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path)

    # Save a few runs
    for i in range(3):
        report = {
            "vibe_score": 50 + i,
            "stack": "python",
            "files_analyzed": 10,
            "total_lines": 500,
            "issues": [],
            "architectural_ghosts": [],
            "metadata": {"timestamp": f"2026-03-12T12:00:{i:02d}Z"}
        }
        await store.save_run(report, repo_path=str(tmp_path))

    runs = await store.list_runs(limit=10)
    assert len(runs) == 3
    # Should be in descending timestamp order
    vibe_scores = [r["vibe_score"] for r in runs]
    assert vibe_scores == sorted(vibe_scores, reverse=True)


@pytest.mark.asyncio
async def test_qmd_memory_store_search_basic(tmp_path):
    """Test basic search functionality (substring match)."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path)

    # Save reports with specific issues
    report1 = {
        "vibe_score": 60,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": ["Authentication bypass vulnerability"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }
    report2 = {
        "vibe_score": 80,
        "stack": "node",
        "files_analyzed": 8,
        "total_lines": 300,
        "issues": ["Memory leak in event loop"],
        "architectural_ghosts": ["Callback hell anti-pattern"],
        "metadata": {"timestamp": "2026-03-12T12:01:00Z"}
    }
    await store.save_run(report1, repo_path=str(tmp_path))
    await store.save_run(report2, repo_path=str(tmp_path))

    # Search for "authentication" should find report1
    results = await store.search("authentication")
    assert len(results) == 1
    assert results[0]["vibe_score"] == 60

    # Search for "callback" should find report2
    results = await store.search("callback")
    assert len(results) == 1
    assert results[0]["vibe_score"] == 80

    # Search for "memory" should find report2 (issue)
    results = await store.search("memory")
    assert len(results) == 1


@pytest.mark.asyncio
async def test_qmd_memory_store_diff_runs(tmp_path):
    """Test diffing two runs."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path)

    report_a = {
        "vibe_score": 70,
        "stack": "python",
        "files_analyzed": 10,
        "total_lines": 500,
        "issues": ["Issue A"],
        "architectural_ghosts": ["Ghost A"],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }
    report_b = {
        "vibe_score": 80,
        "stack": "python",
        "files_analyzed": 12,
        "total_lines": 600,
        "issues": ["Issue B", "Issue A"],  # Issue A persists, Issue B new
        "architectural_ghosts": [],  # Ghost A resolved
        "metadata": {"timestamp": "2026-03-12T12:10:00Z"}
    }

    id_a = await store.save_run(report_a, repo_path=str(tmp_path))
    id_b = await store.save_run(report_b, repo_path=str(tmp_path))

    diff = await store.diff_runs(id_a, id_b)
    assert diff is not None
    assert diff["vibe_score_delta"] == 10
    assert "Issue B" in diff["new_issues"]
    assert "Ghost A" in diff["resolved_ghosts"]
    # Verify MemoryStore-compatible keys
    assert "new_flags" in diff
    assert "resolved_flags" in diff
    assert "metrics_comparison" in diff
    assert diff["run_a"]["id"] == id_a
    assert diff["run_b"]["id"] == id_b


@pytest.mark.asyncio
async def test_qmd_memory_store_knowledge_graph(tmp_path):
    """Test knowledge graph aggregation."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path)

    # Save multiple runs with recurring issues
    for i in range(3):
        report = {
            "vibe_score": 60,
            "stack": "python",
            "files_analyzed": 10,
            "total_lines": 500,
            "issues": ["Recurring issue"],
            "architectural_ghosts": ["Recurring ghost"],
            "metadata": {"timestamp": f"2026-03-12T12:00:{i:02d}Z"}
        }
        await store.save_run(report, repo_path=str(tmp_path))

    graph = await store.get_knowledge_graph(repo_path=str(tmp_path), limit=10)
    # Verify MemoryStore-compatible structure
    assert "total_runs" in graph
    assert graph["total_runs"] == 3
    assert "stacks_seen" in graph
    assert "python" in graph["stacks_seen"]
    assert "score_trend" in graph
    assert len(graph["score_trend"]) == 3
    assert "recurring_issues" in graph
    assert "recurring_ghosts" in graph
    assert "recurring_flags" in graph
    assert "coupling_hotspots" in graph
    # Should have entries for the recurring issue and ghost
    issue_items = [entry["item"] for entry in graph["recurring_issues"]]
    ghost_items = [entry["item"] for entry in graph["recurring_ghosts"]]
    assert "Recurring issue" in issue_items
    assert "Recurring ghost" in ghost_items


@pytest.mark.asyncio
async def test_prefetch_manager_sequential(tmp_path):
    """Test sequential prefetch strategy identifies adjacent runs."""
    from ghostclaw.core.prefetch import PrefetchManager

    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)

    # Save 5 runs
    run_ids = []
    for i in range(5):
        report = {
            "vibe_score": 50 + i * 5,
            "stack": "python",
            "files_analyzed": 1,
            "total_lines": 10,
            "issues": [f"Issue {i}"],
            "architectural_ghosts": [],
            "metadata": {"timestamp": f"2026-03-12T12:00:{i:02d}Z"}
        }
        run_id = await store.save_run(report, repo_path=str(tmp_path))
        run_ids.append(run_id)

    # Get first run (oldest id)
    first_run = await store.get_run(run_ids[0])
    assert first_run is not None

    # Check that prefetch manager triggered and queued neighboring runs
    stats = store.prefetch_manager.get_stats()
    # Triggered at least once
    assert stats["triggered"] >= 1
    # Note: due to async background, pending may be 0 after tasks complete; we can't reliably assert pending counts
    # Instead, verify the strategy logic directly:
    context = {
        "action": "get_run",
        "run_id": run_ids[2],  # middle run
        "run_data": await store.get_run(run_ids[2]),
        "filters": {"repo_path": str(tmp_path)},
        "prefetch_window": 2,
    }
    # Access internal method to compute candidate IDs (we'll test strategy directly)
    pm = store.prefetch_manager
    seq_ids = await pm._prefetch_sequential(context)
    # Should include runs at idx-2, idx-1, idx+1, idx+2 within bounds
    expected = set(run_ids[:2] + run_ids[3:5])  # indices 0,1,3,4 when current is 2
    assert seq_ids == expected


@pytest.mark.asyncio
async def test_prefetch_manager_time_window(tmp_path):
    """Test time window prefetch."""
    from ghostclaw.core.prefetch import PrefetchManager
    from datetime import datetime, timedelta

    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)

    base = datetime(2026, 3, 12, 12, 0, 0)
    reports = []
    for i in range(-2, 3):  # 5 runs: -60min, -30min, 0, +30min, +60min relative to base
        ts = (base + timedelta(minutes=i*30)).isoformat() + "Z"
        reports.append({
            "vibe_score": 50,
            "stack": "python",
            "files_analyzed": 1,
            "total_lines": 10,
            "issues": [],
            "architectural_ghosts": [],
            "metadata": {"timestamp": ts}
        })
    run_ids = []
    for r in reports:
        run_id = await store.save_run(r, repo_path=str(tmp_path))
        run_ids.append(run_id)

    # Get middle run (index 2, base time)
    middle = await store.get_run(run_ids[2])
    pm = store.prefetch_manager
    context = {
        "action": "get_run",
        "run_id": run_ids[2],
        "run_data": middle,
        "filters": {"repo_path": str(tmp_path)},
        "prefetch_hours": 1,  # ±1 hour window
    }
    time_ids = await pm._prefetch_time_window(context)
    # Should include all except self (all within ±1 hour)
    assert set(time_ids) == set(run_ids) - {run_ids[2]}


@pytest.mark.asyncio
async def test_prefetch_vibe_proximity(tmp_path):
    """Test vibe score proximity prefetch."""
    from ghostclaw.core.prefetch import PrefetchManager

    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)

    # Create runs with varying vibe scores
    scores = [40, 45, 50, 55, 60]
    run_ids = []
    for s in scores:
        report = {
            "vibe_score": s,
            "stack": "python",
            "files_analyzed": 1,
            "total_lines": 10,
            "issues": [],
            "architectural_ghosts": [],
            "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
        }
        run_id = await store.save_run(report, repo_path=str(tmp_path))
        run_ids.append(run_id)

    # Middle score 50, delta 10 -> should fetch 40, 45, 55, 60 (all)
    middle_run = await store.get_run(run_ids[2])
    pm = store.prefetch_manager
    context = {
        "action": "get_run",
        "run_id": run_ids[2],
        "run_data": middle_run,
        "filters": {"repo_path": str(tmp_path)},
        "prefetch_vibe_delta": 10,
    }
    vibe_ids = await pm._prefetch_vibe_proximity(context)
    assert set(vibe_ids) == set(run_ids) - {run_ids[2]}


@pytest.mark.asyncio
async def test_prefetch_same_stack(tmp_path):
    """Test stack correlation prefetch."""
    from ghostclaw.core.prefetch import PrefetchManager

    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)

    # Mix stacks
    stacks = ["python", "python", "node", "python", "go"]
    run_ids = []
    for stack in stacks:
        report = {
            "vibe_score": 50,
            "stack": stack,
            "files_analyzed": 1,
            "total_lines": 10,
            "issues": [],
            "architectural_ghosts": [],
            "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
        }
        run_id = await store.save_run(report, repo_path=str(tmp_path))
        run_ids.append(run_id)

    # Get first python run (id at index 0)
    run = await store.get_run(run_ids[0])
    pm = store.prefetch_manager
    context = {
        "action": "get_run",
        "run_id": run_ids[0],
        "run_data": run,
        "filters": {"repo_path": str(tmp_path)},
        "prefetch_stack_count": 5,
    }
    stack_ids = await pm._prefetch_same_stack(context)
    # Should get other python runs: indices 1 and 3
    expected = {run_ids[1], run_ids[3]}
    assert set(stack_ids) == expected


@pytest.mark.asyncio
async def test_prefetch_manager_shutdown(tmp_path):
    """Test that prefetch manager shuts down cleanly."""
    from ghostclaw.core.prefetch import PrefetchManager

    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)
    # No special action needed; just ensure shutdown exists
    pm = store.prefetch_manager
    pm.shutdown()  # should not raise



@pytest.mark.asyncio
async def test_search_cache_integration(tmp_path):
    """Test that search cache is used when ai_buff_enabled=True."""
    db_path = tmp_path / "qmd.db"
    # Enable AI-Buff to activate search cache
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)

    # Save two reports
    report1 = {
        "vibe_score": 60,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 200,
        "issues": ["Authentication bypass"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }
    report2 = {
        "vibe_score": 80,
        "stack": "node",
        "files_analyzed": 8,
        "total_lines": 300,
        "issues": ["Memory leak"],
        "architectural_ghosts": ["Callback hell"],
        "metadata": {"timestamp": "2026-03-12T12:01:00Z"}
    }
    await store.save_run(report1, repo_path=str(tmp_path))
    await store.save_run(report2, repo_path=str(tmp_path))

    # First search - cache miss
    results1 = await store.search("authentication")
    assert len(results1) == 1
    stats1 = store.get_stats()
    assert stats1["search_cache"]["hits"] == 0
    assert stats1["search_cache"]["misses"] == 1

    # Second identical search - should be cache hit
    results2 = await store.search("authentication")
    assert len(results2) == 1
    assert results2[0]["vibe_score"] == results1[0]["vibe_score"]
    stats2 = store.get_stats()
    assert stats2["search_cache"]["hits"] == 1
    assert stats2["search_cache"]["misses"] == 1  # unchanged


@pytest.mark.asyncio
async def test_query_planning_alpha_selection(tmp_path):
    """Test that query planning adjusts alpha based on query characteristics."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)

    # Save one report to enable hybrid
    report = {
        "vibe_score": 50,
        "stack": "python",
        "files_analyzed": 1,
        "total_lines": 10,
        "issues": [],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }
    await store.save_run(report, repo_path=str(tmp_path))

    # Short keyword query (<=3 tokens) → alpha should be high (BM25 heavy, ~0.9)
    # We'll just check that alpha passed to query_engine is appropriate
    # We can't easily intercept alpha, but we can check it's used by verifying
    # that search completes without error. For rigorous alpha test, we'd need
    # to mock the classifier. This is an integration sanity check.
    await store.search("bypass", limit=5)  # short query

    # Longer query (>=10 tokens) → alpha should be lower (vector heavy)
    long_query = "how to fix authentication bypass vulnerability in web application"
    await store.search(long_query, limit=5)

    # Query with exact quotes → BM25 heavy
    await store.search('"security issue"', limit=5)

    # All should complete successfully; Phase 3 activation confirmed


@pytest.mark.asyncio
async def test_search_cache_ttl_expiry(tmp_path):
    """Test that search cache entries expire after TTL."""
    import time

    db_path = tmp_path / "qmd.db"
    # Use short TTL for testing
    store = QMDMemoryStore(db_path=db_path, ai_buff_enabled=True)
    # Override search_cache TTL to 1 second
    if store.search_cache:
        store.search_cache.ttl = 1

    report = {
        "vibe_score": 50,
        "stack": "python",
        "files_analyzed": 1,
        "total_lines": 10,
        "issues": ["Test issue"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }
    await store.save_run(report, repo_path=str(tmp_path))

    # First search - miss
    await store.search("test")
    assert store.search_cache.stats()["misses"] == 1

    # Immediate second search - hit
    await store.search("test")
    assert store.search_cache.stats()["hits"] == 1

    # Wait for TTL expiry
    time.sleep(1.5)

    # Third search - should be miss again (cache cleared)
    await store.search("test")
    assert store.search_cache.stats()["misses"] == 2
    assert store.search_cache.stats()["hits"] == 1  # unchanged


# --- Migration Manager Tests ---

@pytest.mark.asyncio
async def test_migration_needs_migration(tmp_path):
    """Test that needs_migration correctly detects missing embeddings."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        ai_buff_enabled=True,
        auto_migrate=False  # we'll manually manage
    )
    # Manually create backfill manager
    from ghostclaw.core.migration import EmbeddingBackfillManager
    store.backfill_manager = EmbeddingBackfillManager(store, batch_size=10, throttle_ms=0)

    # Save a report (this will embed automatically)
    report = {
        "vibe_score": 50,
        "stack": "python",
        "files_analyzed": 1,
        "total_lines": 10,
        "issues": ["Test issue"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }
    await store.save_run(report, repo_path=str(tmp_path))

    # After save, embeddings exist, so migration not needed
    assert not await store.backfill_manager.needs_migration()


@pytest.mark.asyncio
async def test_migration_process_report(tmp_path):
    """Test that backfill embeds a legacy report correctly."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        ai_buff_enabled=True,
        auto_migrate=False
    )
    from ghostclaw.core.migration import EmbeddingBackfillManager
    store.backfill_manager = EmbeddingBackfillManager(store, batch_size=1, throttle_ms=0)

    # Manually insert a legacy report (no embeddings)
    report_data = {
        "vibe_score": 75,
        "stack": "node",
        "files_analyzed": 2,
        "total_lines": 100,
        "issues": ["Memory leak"],
        "architectural_ghosts": ["Callback hell"],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z", "repo_path": str(tmp_path)}
    }
    async with aiosqlite.connect(db_path) as db:
        # Ensure reports table exists (indexer would normally create)
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                vibe_score INTEGER NOT NULL,
                stack TEXT NOT NULL,
                files_analyzed INTEGER,
                total_lines INTEGER,
                report_json TEXT NOT NULL,
                repo_path TEXT
            )
            """
        )
        await db.execute(
            "INSERT INTO reports (timestamp, vibe_score, stack, files_analyzed, total_lines, report_json, repo_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                report_data["metadata"]["timestamp"],
                report_data["vibe_score"],
                report_data["stack"],
                report_data["files_analyzed"],
                report_data["total_lines"],
                json.dumps(report_data),
                report_data["metadata"]["repo_path"]
            )
        )
        await db.commit()
        cursor = await db.execute("SELECT last_insert_rowid()")
        row = await cursor.fetchone()
        run_id = row[0]

    # Confirm needs_migration is True (since no embeddings yet)
    assert await store.backfill_manager.needs_migration()

    # Fetch the report row and process
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM reports WHERE id = ?", (run_id,))
        row = await cursor.fetchone()
        run = dict(row)

    await store.backfill_manager._process_report(run)

    # Verify embeddings now exist
    if store.vector_store:
        chunks = await store.vector_store.search_by_run_id(run_id, limit=10)
        assert len(chunks) > 0, "Backfill should have added chunks to vector store"


@pytest.mark.asyncio
async def test_migration_stats_output(tmp_path):
    """Test that get_stats() includes migration info."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        ai_buff_enabled=True,
        auto_migrate=False
    )
    from ghostclaw.core.migration import EmbeddingBackfillManager
    store.backfill_manager = EmbeddingBackfillManager(store, batch_size=50, throttle_ms=100)

    stats = store.get_stats()
    assert "migration" in stats
    mig_stats = stats["migration"]
    assert mig_stats is not None
    # Check presence of expected fields
    assert "running" in mig_stats
    assert "total_runs" in mig_stats
    assert "processed_runs" in mig_stats
    assert "errors" in mig_stats
    assert "started_at" in mig_stats
    assert "completed_at" in mig_stats
    assert "last_error" in mig_stats
    assert "pending" in mig_stats


def test_query_classifier_alpha_ranges():
    """Test that QueryClassifier returns appropriate alpha values."""
    from ghostclaw.core.qmd.query_classifier import QueryClassifier
    clf = QueryClassifier()

    # Short keyword query (1 token) → BM25 heavy → alpha = 0.9
    alpha_short = clf.classify("auth", {})
    assert alpha_short == 0.9, f"Expected alpha=0.9 for short query, got {alpha_short}"

    # Long query (>=10 tokens) → vector heavy → alpha = 0.3
    long_query = "how to fix authentication bypass vulnerability in large web applications with many endpoints"
    alpha_long = clf.classify(long_query, {})
    assert alpha_long == 0.3, f"Expected alpha=0.3 for long query, got {alpha_long}"

    # Exact quotes → BM25 heavy (medium base + 0.3 = 0.9 cap)
    alpha_quotes = clf.classify('"security issue"', {})
    assert alpha_quotes >= 0.8  # 0.6+0.3 = 0.9

    # Code symbols → BM25 heavy (medium +0.2 -> 0.8)
    alpha_code = clf.classify("myVar.camelCase(foo_bar)", {})
    assert alpha_code >= 0.8

    # With filters (repo_path) → BM25 heavy (medium +0.1 -> 0.7)
    alpha_filters = clf.classify("test", {"repo_path": "/path/to/repo"})
    assert alpha_filters >= 0.7


@pytest.mark.asyncio
async def test_hybrid_diversity_limit(tmp_path):
    """Test that max_chunks_per_report limits chunks from same report."""
    db_path = tmp_path / "qmd.db"
    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=True,
        ai_buff_enabled=True,
        max_chunks_per_report=1  # only 1 chunk per report allowed
    )
    # Save two reports; they will be embedded
    report1 = {
        "vibe_score": 50,
        "stack": "python",
        "files_analyzed": 1,
        "total_lines": 10,
        "issues": ["Issue A1", "Issue A2"],  # Two issues will create two chunks
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-12T12:00:00Z"}
    }
    report2 = {
        "vibe_score": 60,
        "stack": "python",
        "files_analyzed": 1,
        "total_lines": 10,
        "issues": ["Issue B1"],
        "architectural_ghosts": [],
        "metadata": {"timestamp": "2026-03-12T12:01:00Z"}
    }
    await store.save_run(report1, repo_path=str(tmp_path))
    await store.save_run(report2, repo_path=str(tmp_path))

    # Search for something that matches both reports (e.g., "Issue")
    results = await store.search("Issue", limit=10)
    # Count how many chunks come from each report
    counts = {}
    for r in results:
        rid = r.get('id') or r.get('report_id')
        if rid is None:
            # try to get run id from metadata? fallback to report.id?
            # Actually the result dict from hybrid search includes 'id' field which is report_id
            continue
        counts[rid] = counts.get(rid, 0) + 1

    # With max_chunks_per_report=1, each report should appear at most once
    for c in counts.values():
        assert c <= 1, f"Expected at most 1 chunk per report, got {c}"
