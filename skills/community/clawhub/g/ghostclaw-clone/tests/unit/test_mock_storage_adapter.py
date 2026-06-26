import pytest
import asyncio
from ghostclaw.core.adapters.storage.mock import MockStorageAdapter

@pytest.fixture
def adapter():
    return MockStorageAdapter()

@pytest.mark.asyncio
async def test_mock_storage_metadata(adapter):
    meta = adapter.ghost_get_metadata()
    assert meta["name"] == "mock-storage"
    assert "in-memory" in meta["description"].lower()

@pytest.mark.asyncio
async def test_mock_storage_save_and_get(adapter):
    report1 = {"vibe_score": 80, "stack": "python"}
    report2 = {"vibe_score": 90, "stack": "nodejs"}
    
    id1 = await adapter.save_report(report1)
    id2 = await adapter.save_report(report2)
    
    assert id1 == "1"
    assert id2 == "2"
    
    history = await adapter.get_history(limit=10)
    assert len(history) == 2
    # LIFO order (latest first)
    assert history[0]["vibe_score"] == 90
    assert history[1]["vibe_score"] == 80
    assert history[0]["id"] == "2"

@pytest.mark.asyncio
async def test_mock_storage_hook_integration(adapter):
    report = {"test": "data"}
    report_id = await adapter.ghost_save_report(report)
    assert report_id == "1"
    assert len(adapter.reports) == 1
