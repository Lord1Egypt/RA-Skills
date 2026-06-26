import pytest
import asyncio
import aiosqlite
from pathlib import Path
from ghostclaw.core.adapters.storage.sqlite import SQLiteStorageAdapter

@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test_history.db"

@pytest.fixture
def adapter(db_path):
    return SQLiteStorageAdapter(db_path=db_path)

@pytest.mark.asyncio
async def test_sqlite_adapter_metadata(adapter):
    # metadata is accessed via ghost_get_metadata hook
    meta = adapter.ghost_get_metadata()
    assert meta["name"] == "sqlite"
    assert "sqlite" in meta["description"].lower()

@pytest.mark.asyncio
async def test_sqlite_adapter_initialization(adapter, db_path):
    await adapter._ensure_db()
    assert db_path.exists()
    
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reports'") as cursor:
            row = await cursor.fetchone()
            assert row is not None

@pytest.mark.asyncio
async def test_sqlite_adapter_save_and_get(adapter):
    report = {
        "vibe_score": 95,
        "stack": "python",
        "files_analyzed": 5,
        "total_lines": 500
    }
    
    report_id = await adapter.save_report(report)
    assert report_id.isdigit()
    
    history = await adapter.get_history(limit=1)
    assert len(history) == 1
    assert history[0]["vibe_score"] == 95
    assert "report_json" in history[0]
