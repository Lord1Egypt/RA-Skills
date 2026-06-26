import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch
from ghostclaw.core.adapters.metric.pyscn import PySCNAdapter

@pytest.fixture
def adapter():
    return PySCNAdapter()

@pytest.mark.asyncio
async def test_pyscn_adapter_metadata(adapter):
    meta = adapter.get_metadata()
    assert meta.name == "pyscn"
    assert "pyscn" in meta.dependencies

@pytest.mark.asyncio
async def test_pyscn_adapter_is_available_success(adapter):
    with patch.object(adapter, 'run_tool', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {"returncode": 0, "stdout": "pyscn 0.1.0"}
        assert await adapter.is_available() is True
        mock_run.assert_called_with(["pyscn", "--version"])

@pytest.mark.asyncio
async def test_pyscn_adapter_is_available_failure(adapter):
    with patch.object(adapter, 'run_tool', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {"returncode": 127, "stderr": "not found"}
        assert await adapter.is_available() is False

@pytest.mark.asyncio
async def test_pyscn_adapter_analyze_success(adapter):
    mock_pyscn_output = {
        "clones": [{"file": "test.py", "lines": [1, 10]}],
        "dead_code": [{"file": "utils.py", "symbol": "unused_func"}]
    }
    
    with patch.object(adapter, 'run_tool', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {
            "returncode": 0, 
            "stdout": json.dumps(mock_pyscn_output)
        }
        # Mock is_available to avoid redundant subprocess call
        with patch.object(adapter, 'is_available', new_callable=AsyncMock) as mock_avail:
            mock_avail.return_value = True
            
            result = await adapter.analyze("/tmp", ["test.py"])
            
            assert len(result["architectural_ghosts"]) == 1
            assert "structural clones" in result["architectural_ghosts"][0]
            assert len(result["issues"]) == 1
            assert "dead code" in result["issues"][0]

@pytest.mark.asyncio
async def test_pyscn_adapter_analyze_unavailable(adapter):
    with patch.object(adapter, 'is_available', new_callable=AsyncMock) as mock_avail:
        mock_avail.return_value = False
        result = await adapter.analyze("/tmp", [])
        assert result == {}
