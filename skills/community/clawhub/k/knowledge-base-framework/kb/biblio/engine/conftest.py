#!/usr/bin/env python3
"""
Test fixtures for kb.llm package.
"""

import pytest
from unittest.mock import Mock, MagicMock
from kb.biblio.config import LLMConfig, LLMConfigError


@pytest.fixture
def llm_config():
    """Create a test LLM config."""
    return LLMConfig(
        model="gemma4:e2b",
        ollama_url="http://localhost:11434",
        timeout=30,
        temperature=0.7,
        skip_validation=True
    )


@pytest.fixture
def mock_ollama_response():
    """Mock Ollama API response."""
    return {
        "model": "gemma4:e2b",
        "response": "Mocked LLM response text",
        "done": True,
        "total_duration": 1234567890,
        "eval_count": 50,
    }


@pytest.fixture
def mock_ollama_stream_response(mock_ollama_response):
    """Mock Ollama streaming response chunks."""
    chunks = []
    text = mock_ollama_response["response"]
    for i, char in enumerate(text):
        chunks.append({
            "response": char,
            "done": i == len(text) - 1,
            "total_duration": mock_ollama_response["total_duration"],
        })
    return chunks


@pytest.fixture
def ollama_engine(llm_config):
    """Create OllamaEngine instance with mocked config."""
    from kb.biblio.engine.ollama_engine import OllamaEngine
    OllamaEngine.reset()
    engine = OllamaEngine(config=llm_config)
    return engine


class TestLLMConfig:
    """Tests for LLMConfig."""
    
    def test_config_creation(self, llm_config):
        """Test basic config creation."""
        assert llm_config.model == "gemma4:e2b"
        assert llm_config.ollama_url == "http://localhost:11434"
        assert llm_config.timeout == 30
        assert llm_config.temperature == 0.7
    
    def test_config_defaults(self):
        """Test config defaults."""
        LLMConfig.reset()
        config = LLMConfig(skip_validation=True)
        assert config.model == LLMConfig.DEFAULT_MODEL
        assert config.timeout == LLMConfig.DEFAULT_TIMEOUT
        assert config.temperature == LLMConfig.DEFAULT_TEMPERATURE
    
    def test_config_singleton(self, llm_config):
        """Test that config is a singleton."""
        LLMConfig.reset()
        config1 = LLMConfig.get_instance()
        config2 = LLMConfig.get_instance()
        assert config1 is config2
    
    def test_derived_paths(self, llm_config):
        """Test derived path properties."""
        assert "essences" in str(llm_config.essences_path)
        assert "reports" in str(llm_config.reports_path)
        assert "graph" in str(llm_config.graph_path)
    
    def test_to_dict(self, llm_config):
        """Test to_dict export."""
        d = llm_config.to_dict()
        assert d["model"] == "gemma4:e2b"
        assert d["ollama_url"] == "http://localhost:11434"
        assert "essences_path" in d
        assert "reports_path" in d
        assert "graph_path" in d


class TestBaseLLMEngine:
    """Tests for BaseLLMEngine abstract class."""
    
    def test_llm_response_dataclass(self):
        """Test LLMResponse dataclass."""
        from kb.biblio.engine.base import LLMResponse, LLMProvider
        
        response = LLMResponse(
            content="Test content",
            model="test-model",
            provider=LLMProvider.OLLAMA,
            done=True,
        )
        
        assert response.content == "Test content"
        assert response.model == "test-model"
        assert response.success is True
        assert response.error is None
    
    def test_llm_response_with_error(self):
        """Test LLMResponse with error."""
        from kb.biblio.engine.base import LLMResponse, LLMProvider
        
        response = LLMResponse(
            content="",
            model="test-model",
            provider=LLMProvider.OLLAMA,
            done=False,
            error="Test error",
        )
        
        assert response.success is False
        assert response.error == "Test error"
    
    def test_llm_stream_chunk(self):
        """Test LLMStreamChunk dataclass."""
        from kb.biblio.engine.base import LLMStreamChunk
        
        chunk = LLMStreamChunk(content="Test", done=False)
        assert chunk.content == "Test"
        assert chunk.done is False
        
        final_chunk = LLMStreamChunk(content="", done=True)
        assert final_chunk.done is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])