import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.llm_client import LLMClient, TokenBudgetExceededError
import asyncio

@pytest.fixture
def config():
    return GhostclawConfig(api_key="test-key", use_ai=True, ai_provider="openrouter")

@pytest.mark.asyncio
async def test_generate_analysis_dry_run():
    # Patch AsyncOpenAI and AsyncAnthropic to avoid needing real API keys during construction
    with patch("ghostclaw.core.llm_client.AsyncOpenAI"), \
         patch("ghostclaw.core.llm_client.AsyncAnthropic"):
        config = GhostclawConfig(dry_run=True, use_ai=True)
        client = LLMClient(config, ".")
        result = await client.generate_analysis("test prompt")
        assert result == {"content": "Dry run enabled. API call skipped."}

@pytest.mark.asyncio
async def test_generate_analysis_missing_api_key():
    # Mock SDKs so LLMClient can be instantiated without a valid key
    with patch("ghostclaw.core.llm_client.AsyncOpenAI"), \
         patch("ghostclaw.core.llm_client.AsyncAnthropic"):
        config = GhostclawConfig(api_key=None, use_ai=True, ai_provider="openrouter")
        client = LLMClient(config, ".")
        with pytest.raises(ValueError, match="API key not provided"):
            await client.generate_analysis("test prompt")

def test_token_budget_exceeded(config):
    client = LLMClient(config, ".")
    client.max_tokens = 10  # Artificial limit
    with pytest.raises(TokenBudgetExceededError):
        client._check_token_budget("This is a very long prompt that will exceed the artificial ten token budget")

@pytest.mark.asyncio
async def test_generate_analysis_success(config):
    # Mock AsyncOpenAI
    with patch("ghostclaw.core.llm_client.AsyncOpenAI") as mock_openai:
        mock_client = mock_openai.return_value
        
        # Mock the completions.create call
        mock_message = MagicMock()
        mock_message.content = "Test synthesis"
        # Ensure reasoning_content is NOT present (simulating normal model)
        del mock_message.reasoning_content
        
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message = mock_message
        mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)

        client = LLMClient(config, ".")
        result = await client.generate_analysis("Analyze this codebase")

        assert result == {"content": "Test synthesis", "reasoning": None}

@pytest.mark.asyncio
async def test_generate_analysis_with_reasoning(config):
    with patch("ghostclaw.core.llm_client.AsyncOpenAI") as mock_openai:
        mock_client = mock_openai.return_value
        
        mock_message = MagicMock()
        mock_message.content = "Test synthesis"
        mock_message.reasoning_content = "Thinking hard..."
        
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message = mock_message
        mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)

        client = LLMClient(config, ".")
        result = await client.generate_analysis("Analyze this codebase")

        assert result == {"content": "Test synthesis", "reasoning": "Thinking hard..."}

@pytest.mark.asyncio
async def test_test_connection_success(config):
    with patch("ghostclaw.core.llm_client.AsyncOpenAI") as mock_openai:
        mock_client = mock_openai.return_value
        mock_client.models.list = AsyncMock(return_value=MagicMock())
        
        client = LLMClient(config, ".")
        result = await client.test_connection()
        assert result is True

@pytest.mark.asyncio
async def test_list_models(config):
    with patch("ghostclaw.core.llm_client.AsyncOpenAI") as mock_openai:
        mock_client = mock_openai.return_value

        mock_model_1 = MagicMock()
        mock_model_1.id = "model-1"
        mock_model_2 = MagicMock()
        mock_model_2.id = "model-2"

        mock_response = MagicMock()
        mock_response.data = [mock_model_1, mock_model_2]
        mock_client.models.list = AsyncMock(return_value=mock_response)

        client = LLMClient(config, ".")
        models = await client.list_models()
        assert models == ["model-1", "model-2"]


@pytest.mark.asyncio
async def test_retry_on_transient_failure():
    """Test that _retry retries on transient exceptions and eventually succeeds."""
    with patch("ghostclaw.core.llm_client.AsyncOpenAI"), \
         patch("ghostclaw.core.llm_client.AsyncAnthropic"):
        config = GhostclawConfig(retry_attempts=3, retry_backoff_factor=0.01, api_key="dummy")
        client = LLMClient(config, ".")

        call_count = 0

        async def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("simulated transient failure")
            return "success"

        result = await client._retry(flaky_func)
        assert result == "success"
        assert call_count == 3


@pytest.mark.asyncio
async def test_retry_exhaustion_raises():
    """Test that _retry raises after exhausting attempts."""
    with patch("ghostclaw.core.llm_client.AsyncOpenAI"), \
         patch("ghostclaw.core.llm_client.AsyncAnthropic"):
        config = GhostclawConfig(retry_attempts=2, retry_backoff_factor=0.01, api_key="dummy")
        client = LLMClient(config, ".")

        call_count = 0

        async def always_fails():
            nonlocal call_count
            call_count += 1
            raise RuntimeError("persistent failure")

        with pytest.raises(RuntimeError):
            await client._retry(always_fails)

        assert call_count == 2


@pytest.mark.asyncio
async def test_retry_stream():
    """Test that _retry_stream retries on transient failure during streaming."""
    with patch("ghostclaw.core.llm_client.AsyncOpenAI"), \
         patch("ghostclaw.core.llm_client.AsyncAnthropic"):
        config = GhostclawConfig(retry_attempts=2, retry_backoff_factor=0.01, api_key="dummy")
        client = LLMClient(config, ".")

        call_count = 0

        async def flaky_stream():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("stream failed")
            yield {"type": "content", "content": "chunk1"}
            yield {"type": "content", "content": "chunk2"}

        chunks = []
        async for chunk in client._retry_stream(flaky_stream):
            chunks.append(chunk)

        assert len(chunks) == 2
        assert chunks[0]["content"] == "chunk1"
        assert chunks[1]["content"] == "chunk2"
        assert call_count == 2


@pytest.mark.asyncio
async def test_retry_stream_exhaustion():
    """Test that _retry_stream raises after exhausting attempts."""
    with patch("ghostclaw.core.llm_client.AsyncOpenAI"), \
         patch("ghostclaw.core.llm_client.AsyncAnthropic"):
        config = GhostclawConfig(retry_attempts=1, retry_backoff_factor=0.01, api_key="dummy")
        client = LLMClient(config, ".")

        async def always_fails():
            raise RuntimeError("stream always fails")
            yield  # unreachable, but makes it an async generator

        with pytest.raises(RuntimeError):
            async for _ in client._retry_stream(always_fails):
                pass
