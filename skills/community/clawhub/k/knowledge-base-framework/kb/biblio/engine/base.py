#!/usr/bin/env python3
"""
BaseLLMEngine - Abstract Base Class for LLM Engines

Defines the interface all LLM engines must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers."""
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    MOCK = "mock"


@dataclass
class LLMResponse:
    """
    Standardized LLM response object.
    
    Attributes:
        content: The generated text content
        model: The model used for generation
        provider: The provider used (OLLAMA, OPENAI, etc.)
        done: Whether generation completed naturally
        total_duration: Generation time in nanoseconds
        tokens: Number of tokens generated (if available)
        context: Context window size (provider-specific)
        error: Error message if generation failed
    """
    content: str
    model: str
    provider: LLMProvider
    done: bool = True
    total_duration: Optional[int] = None
    tokens: Optional[int] = None
    context: Optional[int] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'content': self.content,
            'model': self.model,
            'provider': self.provider.value,
            'done': self.done,
            'total_duration': self.total_duration,
            'tokens': self.tokens,
            'context': self.context,
            'error': self.error,
        }
    
    @property
    def success(self) -> bool:
        """Check if response was successful."""
        return self.error is None and self.done


@dataclass
class LLMStreamChunk:
    """
    Single chunk from streaming response.
    
    Attributes:
        content: Text chunk received
        done: Whether this is the final chunk
    """
    content: str
    done: bool = False


class BaseLLMEngine(ABC):
    """
    Abstract Base Class for LLM Engines.
    
    All LLM engine implementations must inherit from this class
    and implement the abstract methods.
    
    Usage:
        class MyEngine(BaseLLMEngine):
            def generate(self, prompt: str, **kwargs) -> LLMResponse:
                # Implement generation
                pass
        
        engine = MyEngine()
        response = engine.generate("Hello, world!")
    """
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific options
            
        Returns:
            LLMResponse object with generated content
            
        Raises:
            LLMEngineError: On generation failure
        """
        pass
    
    @abstractmethod
    async def generate_async(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Async version of generate().
        
        Non-blocking call for concurrent operations.
        
        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific options
            
        Returns:
            LLMResponse object with generated content
            
        Raises:
            LLMEngineError: On generation failure
        """
        pass
    
    def generate_stream(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Generate text with streaming response.
        
        Default implementation uses generate() for engines
        that don't support streaming.
        
        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific options
            
        Yields:
            LLMStreamChunk objects as they arrive
        """
        # Default: accumulate full response
        response = self.generate(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        yield LLMStreamChunk(content=response.content, done=True)
    
    async def generate_stream_async(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Async version of generate_stream().
        
        Default implementation awaits generate_async().
        
        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific options
            
        Yields:
            LLMStreamChunk objects as they arrive
        """
        response = await self.generate_async(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        yield LLMStreamChunk(content=response.content, done=True)
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the LLM engine is available/healthy.
        
        Returns:
            True if engine can accept requests
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the configured model name.
        
        Returns:
            Model identifier string
        """
        pass
    
    @abstractmethod
    def get_provider(self) -> LLMProvider:
        """
        Get the LLM provider type.
        
        Returns:
            LLMProvider enum value
        """
        pass
    
    @property
    def supports_streaming(self) -> bool:
        """
        Whether this engine supports streaming responses.
        
        Override in subclass if streaming is supported.
        """
        return False
    
    @property
    def supports_async(self) -> bool:
        """
        Whether this engine supports async operations.
        
        Override in subclass if async is supported.
        """
        return True