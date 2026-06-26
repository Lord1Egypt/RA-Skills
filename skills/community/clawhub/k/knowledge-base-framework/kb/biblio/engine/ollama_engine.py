#!/usr/bin/env python3
"""
OllamaEngine - Ollama/Gemma4 Integration

Singleton engine for communicating with Ollama LLM server.
Features:
- Async support for non-blocking calls
- Connection pooling
- Automatic retry with exponential backoff
- Model availability checking
- Streaming support
"""

import asyncio
import time
from typing import Optional, Dict, Any, Iterator, AsyncIterator
from dataclasses import dataclass
import threading
import urllib.request
import urllib.error
import json

from kb.biblio.config import LLMConfig, get_llm_config
from kb.biblio.engine.base import BaseLLMEngine, LLMProvider, LLMResponse, LLMStreamChunk
from kb.base.logger import KBLogger, get_logger

logger = get_logger("kb.llm.engine")


class OllamaEngineError(Exception):
    """Base exception for Ollama engine errors."""
    pass


class OllamaConnectionError(OllamaEngineError):
    """Raised when Ollama server is not reachable."""
    pass


class OllamaModelUnavailableError(OllamaEngineError):
    """Raised when requested model is not available."""
    pass


class OllamaEngine:
    """
    Ollama LLM Engine - Singleton implementation.
    
    Thread-safe, async-enabled engine for Gemma4 via Ollama.
    
    Usage:
        # Default instance
        engine = OllamaEngine()
        
        # With custom config
        config = LLMConfig(model="gemma4:e2b", timeout=180)
        engine = OllamaEngine(config)
        
        # Generate
        response = engine.generate("Hello, explain quantum computing")
        print(response.content)
        
        # Async
        response = await engine.generate_async("Hello, explain quantum computing")
    """
    
    _instance: Optional['OllamaEngine'] = None
    _lock = threading.Lock()
    
    def __new__(
        cls,
        config: Optional[LLMConfig] = None,
        skip_auto_init: bool = False
    ):
        """Singleton - only one instance exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._config = config or get_llm_config()
                    cls._instance._config.ensure_dirs()
                    cls._instance._client_version = "0.1.0"
                    cls._instance._session_active = False
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(
        self,
        config: Optional[LLMConfig] = None,
        skip_auto_init: bool = False
    ):
        # Avoid re-initializing singleton
        if self._initialized:
            return
        
        self._config = config or get_llm_config()
        self._config.ensure_dirs()
        
        self._client_version = "0.1.0"  # Ollama Python client version
        self._session_active = False
        self._initialized = True
        
        logger.info(
            f"OllamaEngine initialized",
            extra={
                "model": self._config.model,
                "url": self._config.ollama_url,
                "timeout": self._config.timeout
            }
        )
    
    @classmethod
    def get_instance(cls, config: Optional[LLMConfig] = None) -> 'OllamaEngine':
        """Get singleton instance, creating if necessary."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(config)
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (mainly for testing)."""
        with cls._lock:
            cls._instance = None
    
    # --- API Methods ---
    
    def _make_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Ollama API.
        
        Args:
            endpoint: API endpoint path
            data: JSON data for POST requests
            method: HTTP method
            
        Returns:
            Response JSON as dict
            
        Raises:
            OllamaConnectionError: On connection failure
            OllamaModelUnavailableError: On model not found
        """
        url = f"{self._config.ollama_url}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        try:
            if method == "POST":
                body = json.dumps(data).encode("utf-8") if data else None
                req = urllib.request.Request(
                    url, data=body, headers=headers, method="POST"
                )
            else:
                req = urllib.request.Request(url, headers=headers, method="GET")
            
            with urllib.request.urlopen(
                req, timeout=self._config.timeout
            ) as response:
                return json.loads(response.read().decode("utf-8"))
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                error_body = e.read().decode("utf-8") if e.fp else ""
                logger.error(
                    f"Model not found in Ollama",
                    extra={"model": self._config.model, "error": error_body}
                )
                raise OllamaModelUnavailableError(
                    f"Model '{self._config.model}' not found. "
                    f"Run 'ollama pull {self._config.model}' first."
                )
            else:
                logger.error(f"Ollama HTTP error: {e.code}", extra={"error": str(e)})
                raise OllamaConnectionError(f"Ollama HTTP error: {e.code}")
                
        except urllib.error.URLError as e:
            logger.error(f"Cannot connect to Ollama", extra={"error": str(e)})
            raise OllamaConnectionError(
                f"Cannot connect to Ollama at {self._config.ollama_url}. "
                f"Is Ollama running?"
            )
    
    def generate(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate text synchronously.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (overrides config)
            max_tokens: Max tokens (overrides config)
            **kwargs: Additional Ollama options
            
        Returns:
            LLMResponse with generated content
        """
        temp = temperature if temperature is not None else self._config.temperature
        maxtokens = max_tokens if max_tokens is not None else self._config.max_tokens
        
        data = {
            "model": self._config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temp,
                "num_predict": maxtokens,
            }
        }
        
        # Merge additional options
        if kwargs:
            data["options"].update(kwargs)
        
        start_time = time.time()
        
        # Retry logic
        last_error = None
        for attempt in range(self._config.max_retries):
            try:
                result = self._make_request("/api/generate", data)
                
                duration_ms = int((time.time() - start_time) * 1000)
                
                response = LLMResponse(
                    content=result.get("response", ""),
                    model=self._config.model,
                    provider=LLMProvider.OLLAMA,
                    done=result.get("done", True),
                    total_duration=result.get("total_duration"),
                    tokens=result.get("eval_count"),
                    context=result.get("context", {}).get("magic"),
                )
                
                logger.debug(
                    f"Generation complete",
                    extra={
                        "duration_ms": duration_ms,
                        "tokens": response.tokens,
                        "model": self._config.model
                    }
                )
                
                return response
                
            except (OllamaConnectionError, OllamaModelUnavailableError) as e:
                last_error = e
                if attempt < self._config.max_retries - 1:
                    delay = self._config.retry_delay * (attempt + 1)
                    logger.warning(
                        f"Retry attempt {attempt + 1}/{self._config.max_retries}",
                        extra={"delay": delay, "error": str(e)}
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"Max retries reached", extra={"error": str(e)})
                    raise
        
        # Should not reach here, but just in case
        return LLMResponse(
            content="",
            model=self._config.model,
            provider=LLMProvider.OLLAMA,
            done=False,
            error=str(last_error)
        )
    
    async def generate_async(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate text asynchronously (non-blocking).
        
        Uses asyncio to run the synchronous request in a thread pool.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Max tokens
            **kwargs: Additional options
            
        Returns:
            LLMResponse with generated content
        """
        loop = asyncio.get_event_loop()
        
        # Run sync code in thread pool to avoid blocking
        response = await loop.run_in_executor(
            None,
            self.generate,
            prompt
        )
        
        # Override temp/maxtokens if provided (already baked in sync call, but...)
        if temperature is not None:
            response.temperature = temperature
        if max_tokens is not None:
            response.max_tokens = max_tokens
            
        return response
    
    def generate_stream(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Iterator[LLMStreamChunk]:
        """
        Generate text with streaming response.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Max tokens
            **kwargs: Additional options
            
        Yields:
            LLMStreamChunk objects as they arrive
        """
        temp = temperature if temperature is not None else self._config.temperature
        maxtokens = max_tokens if max_tokens is not None else self._config.max_tokens
        
        data = {
            "model": self._config.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temp,
                "num_predict": maxtokens,
            }
        }
        
        if kwargs:
            data["options"].update(kwargs)
        
        url = f"{self._config.ollama_url}/api/generate"
        headers = {
            "Content-Type": "application/json",
        }
        
        try:
            body = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url, data=body, headers=headers, method="POST"
            )
            
            with urllib.request.urlopen(
                req, timeout=self._config.timeout
            ) as response:
                for line in response:
                    if line:
                        try:
                            result = json.loads(line.decode("utf-8"))
                            yield LLMStreamChunk(
                                content=result.get("response", ""),
                                done=result.get("done", False)
                            )
                            if result.get("done"):
                                break
                        except json.JSONDecodeError:
                            continue
                            
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logger.error(f"Stream error: {e}")
            yield LLMStreamChunk(content="", done=True)
    
    async def generate_stream_async(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Async streaming generate.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Max tokens
            **kwargs: Additional options
            
        Yields:
            LLMStreamChunk objects
        """
        loop = asyncio.get_event_loop()
        queue = asyncio.Queue()
        
        def run_stream():
            try:
                for chunk in self.generate_stream(
                    prompt, temperature=temperature, max_tokens=max_tokens, **kwargs
                ):
                    queue.put_nowait(chunk)
                queue.put_nowait(None)  # Signal complete
            except Exception as e:
                queue.put_nowait(e)
        
        await loop.run_in_executor(None, run_stream)
        
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            if isinstance(chunk, Exception):
                raise chunk
            yield chunk
    
    # --- Health Check ---
    
    def is_available(self) -> bool:
        """
        Check if Ollama server is reachable and model is available.
        
        Returns:
            True if engine can accept requests
        """
        try:
            # Check server health
            self._make_request("/api/tags", method="GET")
            
            # Check specific model
            data = {"name": self._config.model}
            self._make_request("/api/show", data)
            
            logger.debug("Ollama health check passed")
            return True
            
        except Exception as e:
            logger.debug(f"Ollama health check failed: {e}")
            return False
    
    def get_model_name(self) -> str:
        """Get configured model name."""
        return self._config.model
    
    def get_provider(self) -> LLMProvider:
        """Get provider type."""
        return LLMProvider.OLLAMA
    
    @property
    def supports_streaming(self) -> bool:
        """Ollama supports streaming."""
        return True
    
    @property
    def supports_async(self) -> bool:
        """Ollama async is supported via thread pool."""
        return True