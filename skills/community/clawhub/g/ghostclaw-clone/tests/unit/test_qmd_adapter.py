"""Tests for QMDStorageAdapter plugin."""
import pytest
import asyncio
import json
from pathlib import Path
from ghostclaw.core.adapters.storage.qmd import QMDStorageAdapter
import aiosqlite


@pytest.fixture
def temp_qmd_db(tmp_path):
    """Create a temporary directory with a QMD DB path."""
    return tmp_path / "qmd" / "ghostclaw.db"


def get_qmd_adapter(db_path):
    """Helper to create QMDStorageAdapter with custom db_path."""
    adapter = QMDStorageAdapter()
    adapter.db_path = db_path
    adapter._initialized = False
    return adapter


@pytest.mark.asyncio
async def test_qmd_adapter_save_and_metadata(temp_qmd_db):
    """Test QMDStorageAdapter can initialize DB, save a report, and return metadata."""
    adapter = get_qmd_adapter(temp_qmd_db)

    # Check metadata
    meta = adapter.get_metadata()
    assert meta.name == "qmd"
    assert meta.version == "0.2.0-alpha"
    assert "aiosqlite" in meta.dependencies

    # Check is_available (should be True if aiosqlite installed)
    available = await adapter.is_available()
    assert available is True

    # Save a report using the core method
    report = {
        "vibe_score": 72,
        "stack": "python",
        "files_analyzed": 15,
        "total_lines": 800,
        "issues": ["Test issue"],
        "architectural_ghosts": ["Test ghost"],
        "metadata": {"timestamp": "2026-03-12T18:00:00Z"}
    }
    run_id = await adapter.save_report(report)
    assert isinstance(run_id, str)
    assert temp_qmd_db.exists()

    # Verify data in DB
    async with aiosqlite.connect(temp_qmd_db) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM reports WHERE id = ?", (int(run_id),)) as cursor:
            row = await cursor.fetchone()
            assert row is not None
            assert row["vibe_score"] == 72
            assert row["stack"] == "python"
            stored_report = json.loads(row["report_json"])
            assert stored_report["vibe_score"] == 72


@pytest.mark.asyncio
async def test_qmd_adapter_hook_metadata():
    """Test that ghost_get_metadata hook returns expected dict."""
    adapter = QMDStorageAdapter()
    meta_dict = adapter.ghost_get_metadata()
    assert "name" in meta_dict
    assert meta_dict["name"] == "qmd"
    assert meta_dict["available"] is True


@pytest.mark.asyncio
async def test_qmd_adapter_multiple_saves(temp_qmd_db):
    """Test saving multiple reports and listing."""
    adapter = get_qmd_adapter(temp_qmd_db)

    for i in range(5):
        report = {
            "vibe_score": 60 + i * 5,
            "stack": "node",
            "files_analyzed": 10,
            "total_lines": 400,
            "issues": [],
            "architectural_ghosts": [],
            "metadata": {"timestamp": f"2026-03-12T18:00:{i:02d}Z"}
        }
        await adapter.save_report(report)

    # Verify count via get_history
    history = await adapter.get_history(limit=10)
    assert len(history) == 5
    # Should be in descending timestamp order (higher i later? timestamps increasing, so later should be first)
    vibe_scores = [h["vibe_score"] for h in history]
    # Since timestamps increase with i, order should be reversed (newest first: 80,75,70,65,60)
    assert vibe_scores == sorted(vibe_scores, reverse=True)


@pytest.mark.asyncio
async def test_qmd_adapter_hook_save(temp_qmd_db):
    """Test ghost_save_report hook calls save_report correctly."""
    adapter = get_qmd_adapter(temp_qmd_db)
    report = {"vibe_score": 50, "stack": "go", "metadata": {"timestamp": "2026-03-12T18:00:00Z"}}
    run_id = await adapter.ghost_save_report(report)
    assert isinstance(run_id, str)
    # Verify it's in DB
    async with aiosqlite.connect(temp_qmd_db) as db:
        async with db.execute("SELECT COUNT(*) FROM reports") as cursor:
            (count,) = await cursor.fetchone()
            assert count == 1
