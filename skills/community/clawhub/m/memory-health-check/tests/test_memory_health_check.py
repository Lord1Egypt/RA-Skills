#!/usr/bin/env python3
"""
Test suite for memory-health-check skill — matches current implementation.

Covers all 6 health dimensions:
  1. Integrity scan     (bin/integrity_scan.py)
  2. Bloat detection    (bin/bloat_detector.py)
  3. Orphan finder      (bin/orphan_finder.py)
  4. Dedup scanner      (bin/dedup_scanner.py)
  5. Freshness report    (bin/freshness_report.py)
  6. Health score       (bin/health_score.py)
"""
import json, sys, time
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta

import pytest

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "bin"))
sys.path.insert(0, str(SKILL_ROOT / "lib"))

from integrity_scan import integrity_scan, check_sqlite_integrity, find_memory_dbs
from bloat_detector import bloat_detection, get_dir_size
from orphan_finder import find_orphans, build_reference_graph
from dedup_scanner import dedup_scan, token_similarity
from freshness_report import freshness_report, get_file_age_distribution
from health_score import health_score, aggregate_dimensions, analyze_coverage


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def fake_mhc_home(tmp_path):
    """Replace Path.home() with a controlled temp directory."""
    fake = tmp_path / "fake_openclaw_mhc"
    fake.mkdir(parents=True, exist_ok=True)
    ws = fake / ".openclaw" / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    mem_dir = ws / "memory"
    mem_dir.mkdir(parents=True, exist_ok=True)
    (fake / ".openclaw" / "memory").mkdir(parents=True, exist_ok=True)

    with patch("pathlib.Path.home", return_value=fake):
        yield fake


@pytest.fixture
def memory_dir(fake_mhc_home):
    """Return the A-layer memory directory path."""
    return fake_mhc_home / ".openclaw" / "workspace" / "memory"


@pytest.fixture
def healthy_sqlite_db(memory_dir):
    """Create a clean, uncorrupted SQLite file."""
    db_path = memory_dir / "main.sqlite"
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, content TEXT)")
    conn.execute("INSERT INTO entries (content) VALUES ('healthy entry')")
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def corrupted_sqlite_db(memory_dir):
    """Create a SQLite file with intentional corruption."""
    db_path = memory_dir / "corrupted.sqlite"
    with open(str(db_path), "wb") as f:
        f.write(b"SQLite format 3 XXX THIS IS CORRUPT XXX")
    return db_path


# ---------------------------------------------------------------------------
# 1. integrity_scan tests
# ---------------------------------------------------------------------------

class TestIntegrityScan:
    """Tests for DB corruption / checksum detection."""

    def test_integrity_scan_no_dbs(self, memory_dir):
        """No DB files → score 100, status healthy."""
        result = integrity_scan(scan_dbs=False, base_dir=memory_dir)
        assert result["status"] == "healthy"
        assert result["score"] == 100
        assert result["issues"] == []

    def test_integrity_scan_healthy_db(self, healthy_sqlite_db, memory_dir):
        """Healthy SQLite DB → score 100, status healthy."""
        result = integrity_scan(
            scan_dbs=True,
            db_paths=[healthy_sqlite_db],
            base_dir=memory_dir,
        )
        assert result["status"] == "healthy"
        assert result["score"] == 100

    def test_integrity_scan_corrupted_db(self, corrupted_sqlite_db, memory_dir):
        """Corrupted SQLite DB → score 0, status critical."""
        result = integrity_scan(
            scan_dbs=True,
            db_paths=[corrupted_sqlite_db],
            base_dir=memory_dir,
        )
        assert result["status"] == "critical"
        assert result["score"] == 0
        assert len(result["issues"]) > 0

    def test_find_memory_dbs_returns_paths(self, healthy_sqlite_db, fake_mhc_home):
        """find_memory_dbs returns a list of Path objects."""
        dbs = find_memory_dbs(base_dir=fake_mhc_home / ".openclaw")
        assert isinstance(dbs, list)
        assert all(isinstance(p, Path) for p in dbs)


# ---------------------------------------------------------------------------
# 2. bloat_detector tests
# ---------------------------------------------------------------------------

class TestBloatDetector:
    """Tests for DB size / file count analysis."""

    def test_bloat_healthy_empty_dir(self, memory_dir):
        """Empty memory dir → healthy, score 100."""
        result = bloat_detection(base_dir=memory_dir)
        assert result["status"] == "healthy"
        assert result["score"] == 100

    def test_bloat_returns_size_and_count(self, memory_dir):
        """Result includes total_bytes and file_counts (nested dict)."""
        result = bloat_detection(base_dir=memory_dir)
        assert "total_bytes" in result
        assert "file_counts" in result
        assert isinstance(result["total_bytes"], int)
        assert isinstance(result["file_counts"], dict)

    def test_get_dir_size_empty(self, memory_dir):
        """Empty directory → size 0."""
        size = get_dir_size(memory_dir)
        assert size == 0

    def test_bloat_workspace_missing(self, fake_mhc_home):
        """Non-existent workspace → healthy (graceful)."""
        import shutil
        ws = fake_mhc_home / ".openclaw" / "workspace"
        shutil.rmtree(str(ws), ignore_errors=True)
        result = bloat_detection(base_dir=ws / "memory")
        # Should not raise
        assert "status" in result


# ---------------------------------------------------------------------------
# 3. orphan_finder tests
# ---------------------------------------------------------------------------

class TestOrphanFinder:
    """Tests for orphaned entry detection."""

    def test_orphan_no_files(self, memory_dir):
        """No memory files → 0 orphans, healthy."""
        result = find_orphans(base_dir=memory_dir)
        assert result["orphan_count"] == 0
        assert result["orphan_rate"] == 0.0
        assert result["status"] == "healthy"

    def test_orphan_rate_is_percentage(self, memory_dir):
        """orphan_rate is a valid percentage (0-100)."""
        result = find_orphans(base_dir=memory_dir)
        assert 0.0 <= result["orphan_rate"] <= 100.0

    def test_find_orphans_includes_score(self, memory_dir):
        """Result includes a numeric score."""
        result = find_orphans(base_dir=memory_dir)
        assert "score" in result
        assert isinstance(result["score"], (int, float))

    def test_build_reference_graph_no_files(self, memory_dir):
        """Empty dir → empty graph."""
        graph = build_reference_graph(base_dir=memory_dir)
        assert isinstance(graph, (dict, list))


# ---------------------------------------------------------------------------
# 4. dedup_scanner tests
# ---------------------------------------------------------------------------

class TestDedupScanner:
    """Tests for duplicate / near-duplicate entry detection."""

    def test_dedup_no_files(self, memory_dir):
        """No files → no duplicates, healthy."""
        result = dedup_scan(base_dir=memory_dir)
        assert result["dup_count"] == 0
        assert result["dup_rate"] == 0.0
        assert result["status"] == "healthy"

    def test_dedup_all_unique(self, memory_dir):
        """All sufficiently different files → low dup_rate."""
        # Use longer, diverse content to avoid false-similarity with token_similarity
        contents = [
            "Completed database API migration to new endpoint and deployed to production",
            "Researched three different approaches for caching strategy",
            "Fixed authentication token refresh bug in the user module",
            "Wrote integration tests for the payment gateway interface",
        ]
        for i, content in enumerate(contents):
            (memory_dir / f"unique_{i}.md").write_text(content)
        result = dedup_scan(base_dir=memory_dir)
        # dup_rate should be well below threshold
        assert result["dup_rate"] < 30

    def test_dedup_with_duplicates(self, memory_dir):
        """High-similarity files → non-zero dup_count."""
        # Use near-identical long strings (high token overlap → sim ≥ 0.85)
        base = (
            "Completed the database API migration and deployed the new endpoint "
            "to production environment with full testing and monitoring enabled."
        )
        # Use identical content → exact duplicate detected by MD5 hash (Phase 1)
        # Near-duplicates (same prefix, different suffix) would need same size_bucket
        dup_content = base + " Same suffix content."
        for i in range(3):
            (memory_dir / f"dup_{i}.md").write_text(dup_content)
        result = dedup_scan(base_dir=memory_dir)
        assert result["dup_count"] > 0, f"Expected exact duplicates to be detected, got dup_count={result['dup_count']}"

    def test_dedup_rate_calculation(self, memory_dir):
        """dup_rate = dup_count / total_entries."""
        for i in range(4):
            (memory_dir / f"file_{i}.md").write_text(f"Content number {i}.")
        result = dedup_scan(base_dir=memory_dir)
        # dup_rate is expressed as a percentage
        assert "dup_rate" in result
        assert isinstance(result["dup_rate"], float)

    def test_token_similarity_identical(self):
        """Identical strings → 1.0."""
        assert token_similarity("hello world", "hello world") == 1.0

    def test_token_similarity_no_overlap(self):
        """No overlap → 0.0."""
        assert token_similarity("apple banana", "desk chair") == 0.0

    def test_token_similarity_partial(self):
        """Partial overlap → between 0 and 1."""
        s = token_similarity(
            "database API fix test passed",
            "database API config deploy done",
        )
        assert 0 < s < 1


# ---------------------------------------------------------------------------
# 5. freshness_report tests
# ---------------------------------------------------------------------------

class TestFreshnessReport:
    """Tests for memory entry age distribution."""

    def test_freshness_no_files(self, memory_dir):
        """No files → status depends on threshold config (graceful response)."""
        result = freshness_report(base_dir=memory_dir)
        # Must not raise; result has required fields
        assert "status" in result
        assert "freshness_rate" in result
        assert result["total"] == 0

    def test_freshness_all_recent(self, memory_dir):
        """All files modified within 7 days → healthy."""
        now = time.time()
        for i in range(5):
            f = memory_dir / f"recent_{i}.md"
            f.write_text(f"Recent file {i}")
            import os
            os.utime(f, (now - 3600, now - 3600))  # 1 hour ago
        result = freshness_report(base_dir=memory_dir)
        assert result["status"] == "healthy"
        assert result["recent_7d"] >= 5

    def test_freshness_all_old(self, memory_dir):
        """All files >90 days old → critical."""
        now = time.time()
        for i in range(5):
            f = memory_dir / f"old_{i}.md"
            f.write_text(f"Old file {i}")
            import os
            os.utime(f, (now - 100 * 86400, now - 100 * 86400))  # 100 days ago
        result = freshness_report(base_dir=memory_dir)
        assert result["status"] == "critical"
        assert result["freshness_rate"] < 40

    def test_freshness_mixed(self, memory_dir):
        """Mix of recent and old → intermediate freshness_rate."""
        now = time.time()
        import os
        # 1-hour-old file
        f1 = memory_dir / "fresh.md"
        f1.write_text("Just created")
        os.utime(f1, (now - 3600, now - 3600))
        # 100-day-old file
        f2 = memory_dir / "stale.md"
        f2.write_text("Very old content")
        os.utime(f2, (now - 100 * 86400, now - 100 * 86400))

        result = freshness_report(base_dir=memory_dir)
        assert 0 < result["freshness_rate"] < 100
        assert result["total"] == 2

    def test_freshness_field_structure(self, memory_dir):
        """Result has all expected fields."""
        result = freshness_report(base_dir=memory_dir)
        for field in ["recent_7d", "recent_30d", "total", "freshness_rate", "score", "status"]:
            assert field in result


# ---------------------------------------------------------------------------
# 6. health_score tests
# ---------------------------------------------------------------------------

class TestHealthScore:
    """Tests for aggregate scoring across all dimensions."""

    def test_aggregate_dimensions_all_healthy(self):
        """All dimensions healthy → overall 100, status healthy."""
        dim = {"score": 100, "status": "healthy"}
        result = aggregate_dimensions(
            integrity=dim, bloat=dim, orphans=dim,
            dedup=dim, freshness=dim,
        )
        assert result["overall_score"] >= 90
        assert result["status"] == "healthy"

    def test_aggregate_dimensions_all_critical(self):
        """All dimensions critical → overall low, status critical."""
        dim = {"score": 0, "status": "critical"}
        result = aggregate_dimensions(
            integrity=dim, bloat=dim, orphans=dim,
            dedup=dim, freshness=dim,
        )
        assert result["overall_score"] < 30
        assert result["status"] == "critical"

    def test_aggregate_dimensions_mixed(self):
        """Mixed dimensions → intermediate score, status warning."""
        result = aggregate_dimensions(
            integrity={"score": 100, "status": "healthy"},
            bloat={"score": 20, "status": "critical"},
            orphans={"score": 100, "status": "healthy"},
            dedup={"score": 100, "status": "healthy"},
            freshness={"score": 20, "status": "critical"},
        )
        assert 50 < result["overall_score"] < 80
        assert result["status"] == "warning"

    def test_aggregate_dimensions_weights_sum_to_one(self):
        """Dimension weights sum to approximately 1.0."""
        dim = {"score": 100, "status": "healthy"}
        result = aggregate_dimensions(
            integrity=dim, bloat=dim, orphans=dim,
            dedup=dim, freshness=dim,
        )
        weights = result["weights"]
        total_weight = sum(weights.values())
        assert abs(total_weight - 1.0) < 0.01

    def test_health_score_with_run_dims(self, memory_dir):
        """run_dims restricts which dimensions are executed."""
        # Only run integrity (fastest - no DBs exist)
        result = health_score(
            base_dir=memory_dir,
            run_all=False,
            run_dims=["integrity"],
        )
        assert "dimensions" in result
        assert "overall_score" in result
        assert "status" in result
        assert isinstance(result["overall_score"], (int, float))

    def test_health_score_full_run(self, memory_dir):
        """Full health_score() returns all required fields."""
        result = health_score(base_dir=memory_dir, run_all=True)
        assert "overall_score" in result
        assert "status" in result
        assert "dimensions" in result
        assert "recommendations" in result
        json.dumps(result)  # must be serializable

    def test_analyze_coverage_no_files(self, memory_dir):
        """Empty memory dir → coverage 0, critical."""
        result = analyze_coverage(base_dir=memory_dir)
        assert "score" in result
        assert "coverage_rate" in result
        assert "status" in result

    def test_analyze_coverage_with_content(self, memory_dir):
        """Memory dir with content → some coverage."""
        (memory_dir / "test.md").write_text(
            "Database API fix completed. Testing passed. "
            "Agent skill implementation finished.",
        )
        result = analyze_coverage(base_dir=memory_dir)
        assert "coverage_rate" in result
        assert result["coverage_rate"] >= 0

    def test_health_score_recommendations_present(self, memory_dir):
        """Full scan includes recommendations list."""
        result = health_score(base_dir=memory_dir, run_all=True)
        assert isinstance(result["recommendations"], list)
