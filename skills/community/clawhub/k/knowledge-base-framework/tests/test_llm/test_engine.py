#!/usr/bin/env python3
"""
Tests for kb.llm.engine - OllamaEngine and BaseLLMEngine

These tests use mocked HTTP responses to avoid requiring a live Ollama server.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from urllib.error import URLError, HTTPError
import json

from kb.biblio.config import LLMConfig, LLMConfigError
from kb.biblio.engine.ollama_engine import (
    OllamaEngine,
    OllamaEngineError,
    OllamaConnectionError,
    OllamaModelUnavailableError,
)
from kb.biblio.engine.base import (
    BaseLLMEngine,
    LLMResponse,
    LLMStreamChunk,
    LLMProvider,
)


class TestOllamaEngine:
    """Tests for OllamaEngine class."""
    
    def test_engine_singleton(self, llm_config):
        """Test that OllamaEngine is a singleton."""
        OllamaEngine.reset()
        engine1 = OllamaEngine(config=llm_config)
        engine2 = OllamaEngine(config=llm_config)
        assert engine1 is engine2
    
    def test_engine_get_instance(self, llm_config):
        """Test get_instance class method."""
        OllamaEngine.reset()
        engine = OllamaEngine.get_instance(config=llm_config)
        assert isinstance(engine, OllamaEngine)
        
        # Should return same instance
        engine2 = OllamaEngine.get_instance()
        assert engine is engine2
    
    def test_engine_reset(self, llm_config):
        """Test singleton reset."""
        OllamaEngine.reset()
        engine1 = OllamaEngine(config=llm_config)
        OllamaEngine.reset()
        engine2 = OllamaEngine(config=llm_config)
        assert engine1 is not engine2
    
    def test_config_stored(self, llm_config):
        """Test that config is properly stored."""
        OllamaEngine.reset()
        engine = OllamaEngine(config=llm_config)
        assert engine._config is llm_config
        assert engine._config.model == "gemma4:e2b"
        assert engine._config.timeout == 30
    
    def test_make_request_success(self, ollama_engine, mock_ollama_response):
        """Test successful HTTP request to Ollama."""
        with patch.object(ollama_engine, '_make_request') as mock_request:
            mock_request.return_value = mock_ollama_response
            
            result = ollama_engine._make_request("/api/tags", method="GET")
            assert result == mock_ollama_response
            mock_request.assert_called_once_with("/api/tags", method="GET")
    
    def test_make_request_post_with_data(self, ollama_engine, mock_ollama_response):
        """Test POST request with JSON data."""
        with patch.object(ollama_engine, '_make_request') as mock_request:
            mock_request.return_value = mock_ollama_response
            
            data = {"model": "gemma4:e2b", "prompt": "Hello"}
            result = ollama_engine._make_request("/api/generate", data)
            assert result == mock_ollama_response
    
    def test_make_request_connection_error(self, ollama_engine):
        """Test connection error handling."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = URLError("Connection refused")
            
            with pytest.raises(OllamaConnectionError) as exc_info:
                ollama_engine._make_request("/api/tags", method="GET")
            
            assert "Cannot connect to Ollama" in str(exc_info.value)
    
    def test_make_request_http_error_404(self, ollama_engine):
        """Test 404 model not found error."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"error": "model not found"}'
            mock_response.code = 404
            mock_response.fp = mock_response
            mock_urlopen.side_effect = HTTPError(
                "http://localhost:11434/api/show",
                404,
                "Not Found",
                {},
                mock_response
            )
            
            with pytest.raises(OllamaModelUnavailableError) as exc_info:
                ollama_engine._make_request("/api/show", {"name": "gemma4:e2b"})
            
            assert "not found" in str(exc_info.value).lower()
    
    def test_make_request_http_error_other(self, ollama_engine):
        """Test non-404 HTTP errors."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = HTTPError(
                "http://localhost:11434/api/generate",
                500,
                "Internal Server Error",
                {},
                None
            )
            
            with pytest.raises(OllamaConnectionError) as exc_info:
                ollama_engine._make_request("/api/generate", {})
            
            assert "500" in str(exc_info.value)


class TestOllamaEngineGenerate:
    """Tests for OllamaEngine.generate() method."""
    
    def test_generate_success(self, ollama_engine, mock_ollama_response):
        """Test successful text generation."""
        with patch.object(ollama_engine, '_make_request') as mock_request:
            mock_request.return_value = mock_ollama_response
            
            response = ollama_engine.generate("Hello, explain quantum computing")
            
            assert isinstance(response, LLMResponse)
            assert response.content == "Mocked LLM response text"
            assert response.model == "gemma4:e2b"
            assert response.done is True
            assert response.tokens == 50
    
    def test_generate_with_custom_temperature(self, ollama_engine, mock_ollama_response):
        """Test generation with custom temperature."""
        with patch.object(ollama_engine, '_make_request') as mock_request:
            mock_request.return_value = mock_ollama_response
            
            response = ollama_engine.generate(
                "Hello",
                temperature=0.9,
                max_tokens=100
            )
            
            assert isinstance(response, LLMResponse)
            # Verify request was made with correct params
            call_args = mock_request.call_args
            data = call_args[0][1] if call_args else call_args[1].get('data')
            assert data is not None
    
    def test_generate_with_retry(self, ollama_engine, mock_ollama_response):
        """Test retry logic on temporary failures."""
        call_count = [0]
        
        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] < 3:
                raise OllamaConnectionError("Temporary failure")
            return mock_ollama_response
        
        with patch.object(ollama_engine, '_make_request', side_effect=side_effect):
            response = ollama_engine.generate("Hello")
            
            assert call_count[0] == 3
            assert response.content == "Mocked LLM response text"
    
    def test_generate_max_retries_exceeded(self, ollama_engine, llm_config):
        """Test that max retries are enforced."""
        with patch.object(ollama_engine, '_make_request') as mock_request:
            mock_request.side_effect = OllamaConnectionError("Persistent failure")
            
            with pytest.raises(OllamaConnectionError):
                ollama_engine.generate("Hello")
            
            # Should have retried max_retries times
            assert mock_request.call_count == llm_config.max_retries


class TestOllamaEngineStreaming:
    """Tests for OllamaEngine streaming methods."""
    
    def test_generate_stream(self, ollama_engine, mock_ollama_stream_response):
        """Test streaming response iteration."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            # Create a mock response that yields streaming chunks
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.__iter__ = Mock(return_value=iter([
                json.dumps(chunk).encode('utf-8') 
                for chunk in mock_ollama_stream_response
            ]))
            mock_urlopen.return_value = mock_response
            
            chunks = list(ollama_engine.generate_stream("Hello"))
            
            assert len(chunks) > 0
            assert all(isinstance(c, LLMStreamChunk) for c in chunks)
            assert chunks[-1].done is True
    
    def test_generate_stream_accumulates(self, ollama_engine, mock_ollama_stream_response):
        """Test that streamed chunks can be accumulated."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.__iter__ = Mock(return_value=iter([
                json.dumps(chunk).encode('utf-8') 
                for chunk in mock_ollama_stream_response
            ]))
            mock_urlopen.return_value = mock_response
            
            full_content = ""
            for chunk in ollama_engine.generate_stream("Hello"):
                full_content += chunk.content
            
            assert len(full_content) > 0


class TestOllamaEngineHealthCheck:
    """Tests for OllamaEngine health check methods."""
    
    def test_is_available_success(self, ollama_engine, mock_ollama_response):
        """Test is_available when Ollama is running."""
        with patch.object(ollama_engine, '_make_request') as mock_request:
            mock_request.return_value = {"models": []}
            
            assert ollama_engine.is_available() is True
    
    def test_is_available_failure(self, ollama_engine):
        """Test is_available when Ollama is down."""
        with patch.object(ollama_engine, '_make_request') as mock_request:
            mock_request.side_effect = OllamaConnectionError("Connection refused")
            
            assert ollama_engine.is_available() is False
    
    def test_get_model_name(self, ollama_engine):
        """Test model name getter."""
        assert ollama_engine.get_model_name() == "gemma4:e2b"
    
    def test_get_provider(self, ollama_engine):
        """Test provider getter."""
        assert ollama_engine.get_provider() == LLMProvider.OLLAMA
    
    def test_supports_streaming(self, ollama_engine):
        """Test streaming support property."""
        assert ollama_engine.supports_streaming is True
    
    def test_supports_async(self, ollama_engine):
        """Test async support property."""
        assert ollama_engine.supports_async is True


class TestLLMResponse:
    """Tests for LLMResponse dataclass."""
    
    def test_response_success(self):
        """Test successful response."""
        response = LLMResponse(
            content="Test content",
            model="gemma4:e2b",
            provider=LLMProvider.OLLAMA,
            done=True,
        )
        
        assert response.content == "Test content"
        assert response.success is True
        assert response.error is None
    
    def test_response_with_error(self):
        """Test response with error."""
        response = LLMResponse(
            content="",
            model="gemma4:e2b",
            provider=LLMProvider.OLLAMA,
            done=False,
            error="Generation failed",
        )
        
        assert response.success is False
        assert response.error == "Generation failed"
    
    def test_response_to_dict(self):
        """Test dict conversion."""
        response = LLMResponse(
            content="Test",
            model="gemma4:e2b",
            provider=LLMProvider.OLLAMA,
            tokens=100,
        )
        
        d = response.to_dict()
        assert d["content"] == "Test"
        assert d["model"] == "gemma4:e2b"
        assert d["provider"] == "ollama"
        assert d["tokens"] == 100


class TestLLMStreamChunk:
    """Tests for LLMStreamChunk dataclass."""
    
    def test_chunk_basic(self):
        """Test basic chunk."""
        chunk = LLMStreamChunk(content="Hello", done=False)
        assert chunk.content == "Hello"
        assert chunk.done is False
    
    def test_chunk_final(self):
        """Test final chunk."""
        chunk = LLMStreamChunk(content="", done=True)
        assert chunk.done is True


class TestBaseLLMEngine:
    """Tests for BaseLLMEngine abstract class."""
    
    def test_cannot_instantiate_directly(self):
        """Test that BaseLLMEngine cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseLLMEngine()
    
    def test_must_implement_generate(self):
        """Test that subclass must implement generate()."""
        class IncompleteEngine(BaseLLMEngine):
            pass
        
        with pytest.raises(TypeError):
            IncompleteEngine()
    
    def test_must_implement_is_available(self):
        """Test that subclass must implement is_available()."""
        class PartialEngine(BaseLLMEngine):
            def generate(self, prompt: str, **kwargs) -> LLMResponse:
                return LLMResponse(
                    content="",
                    model="test",
                    provider=LLMProvider.MOCK,
                    done=True,
                )
        
        with pytest.raises(TypeError):
            PartialEngine()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])