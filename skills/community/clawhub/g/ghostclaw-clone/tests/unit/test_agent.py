import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.agent import GhostAgent, AgentEvent

@pytest.fixture
def config():
    return GhostclawConfig(api_key="test-key", use_ai=True, ai_provider="openrouter")

@pytest.mark.asyncio
async def test_agent_lifecycle_hooks(config):
    agent = GhostAgent(config, ".")
    
    events_triggered = []
    
    async def hook(data):
        events_triggered.append(data["event"])
    
    for event in AgentEvent:
        agent.on(event, hook)
    
    # Mock analyzer and llm_client
    mock_report = MagicMock()
    mock_report.model_dump.return_value = {
        "vibe_score": 80, 
        "ai_prompt": "test",
        "stack": "python",
        "files_analyzed": 10,
        "total_lines": 100
    }
    agent.analyzer.analyze = AsyncMock(return_value=mock_report)
    
    # Mock stream_analysis to yield content and reasoning
    async def mock_stream(prompt):
        yield {"type": "reasoning", "content": "Thinking..."}
        yield {"type": "content", "content": "Test synthesis"}
    agent.llm_client.stream_analysis = mock_stream

    with patch("ghostclaw.core.adapters.registry.registry") as mock_registry:
        mock_registry.save_report = AsyncMock()
        mock_registry.emit_event = AsyncMock()
        
        await agent.run()
        
        # Verify registry was called
        mock_registry.register_internal_plugins.assert_called()
        mock_registry.save_report.assert_called()
    
    expected_events = [
        AgentEvent.INIT,
        AgentEvent.PRE_ANALYZE,
        AgentEvent.POST_METRICS,
        AgentEvent.PRE_SYNTHESIS,
        AgentEvent.REASONING_CHUNK,
        AgentEvent.SYNTHESIS_CHUNK,
        AgentEvent.POST_SYNTHESIS
    ]
    
    for event in expected_events:
        assert event.name in events_triggered

@pytest.mark.asyncio
async def test_agent_error_hook(config):
    agent = GhostAgent(config, ".")
    
    error_triggered = False
    async def error_hook(data):
        nonlocal error_triggered
        error_triggered = True
        assert "error" in data
    
    agent.on(AgentEvent.ERROR, error_hook)
    
    # Force an error
    agent.analyzer.analyze = AsyncMock(side_effect=ValueError("Test Error"))
    
    with pytest.raises(ValueError, match="Test Error"):
        await agent.run()
    
    assert error_triggered is True

