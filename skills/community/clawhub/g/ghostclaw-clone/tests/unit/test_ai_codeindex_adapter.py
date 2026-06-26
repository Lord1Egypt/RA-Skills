import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch
from ghostclaw.core.adapters.metric.ai_codeindex import AICodeIndexAdapter

@pytest.fixture
def adapter():
    return AICodeIndexAdapter()

@pytest.mark.asyncio
async def test_ai_codeindex_adapter_metadata(adapter):
    meta = adapter.get_metadata()
    assert meta.name == "ai-codeindex"
    assert "ai-codeindex" in meta.dependencies

@pytest.mark.asyncio
async def test_ai_codeindex_adapter_is_available(adapter):
    with patch.object(adapter, 'run_tool', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {"returncode": 0}
        assert await adapter.is_available() is True

@pytest.mark.asyncio
async def test_ai_codeindex_adapter_analyze(adapter):
    with patch.object(adapter, 'run_tool', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {"returncode": 0, "stdout": "Successfully indexed"}
        
        with patch.object(adapter, 'is_available', return_value=asyncio.Future()) as mock_avail:
            mock_avail.return_value.set_result(True)
            
            result = await adapter.analyze("/tmp", [])
            
            assert len(result["architectural_ghosts"]) == 1
            assert "PROJECT_SYMBOLS.md" in result["architectural_ghosts"][0]
            mock_run.assert_called_with(["ai-codeindex", "symbols", "--root", "/tmp", "-o", "PROJECT_SYMBOLS.md"])
