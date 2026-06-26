import pytest
import json
from pathlib import Path
from ghostclaw.core.adapters.target.json import JsonTargetAdapter

@pytest.fixture
def output_path(tmp_path):
    return tmp_path / "last_report.json"

@pytest.fixture
def adapter(output_path):
    return JsonTargetAdapter(output_path=output_path)

@pytest.mark.asyncio
async def test_json_target_metadata(adapter):
    meta = adapter.ghost_get_metadata()
    assert meta["name"] == "json_target"
    assert "JSON" in meta["description"]

@pytest.mark.asyncio
async def test_json_target_emit_report(adapter, output_path):
    report_data = {"vibe_score": 100, "stack": "python"}
    
    # Simulate POST_SYNTHESIS event
    await adapter.ghost_emit("POST_SYNTHESIS", report_data)
    
    assert output_path.exists()
    with open(output_path, "r") as f:
        saved_data = json.load(f)
        assert saved_data["vibe_score"] == 100

@pytest.mark.asyncio
async def test_json_target_filters_events(adapter, output_path):
    # Simulate an event that should be ignored
    await adapter.ghost_emit("REASONING_CHUNK", {"chunk": "..."})
    
    assert not output_path.exists()
