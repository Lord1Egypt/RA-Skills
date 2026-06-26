#!/usr/bin/env python3
"""
Multi-LLM Adapter - Universal LLM client with fallback support

Unified interface for multiple LLM providers
"""

import os
import json
import time
from typing import Dict, List, Optional, Any, Callable, Iterator, Union
from dataclasses import dataclass, field
from pathlib import Path
from abc import ABC, abstractmethod


@dataclass
class Message:
    """Chat message"""
    role: str  # system, user, assistant, tool
    content: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role}
        if self.content:
            result["content"] = self.content
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        return result


@dataclass
class LLMResponse:
    """LLM response"""
    content: str
    provider: str
    model: str
    usage: Dict[str, int] = field(default_factory=dict)
    cost_usd: Optional[float] = None
    raw_response: Any = None


@dataclass
class ProviderConfig:
    """Provider configuration"""
    name: str
    api_key: Optional[str] = None
    model: str = "gpt-4"
    base_url: Optional[str] = None
    priority: int = 1
    timeout: int = 30
    max_retries: int = 3


class BaseProvider(ABC):
    """Base class for LLM providers"""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.name = config.name
    
    @abstractmethod
    def chat(self, messages: List[Message], tools: Optional[List[Dict]] = None,
             **kwargs) -> LLMResponse:
        """Send chat request"""
        pass
    
    @abstractmethod
    def chat_stream(self, messages: List[Message], tools: Optional[List[Dict]] = None,
                    **kwargs) -> Iterator[str]:
        """Stream chat response"""
        pass
    
    def is_available(self) -> bool:
        """Check if provider is available"""
        return bool(self.config.api_key)


class OpenAIProvider(BaseProvider):
    """OpenAI provider"""
    
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=config.api_key,
                base_url=config.base_url
            )
        except ImportError:
            self.client = None
    
    def chat(self, messages: List[Message], tools: Optional[List[Dict]] = None,
             **kwargs) -> LLMResponse:
        if not self.client:
            raise RuntimeError("OpenAI client not available")
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[m.to_dict() for m in messages],
            tools=tools,
            **kwargs
        )
        
        return LLMResponse(
            content=response.choices[0].message.content or "",
            provider=self.name,
            model=self.config.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            raw_response=response
        )
    
    def chat_stream(self, messages: List[Message], tools: Optional[List[Dict]] = None,
                    **kwargs) -> Iterator[str]:
        if not self.client:
            raise RuntimeError("OpenAI client not available")
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[m.to_dict() for m in messages],
            tools=tools,
            stream=True,
            **kwargs
        )
        
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content


class AnthropicProvider(BaseProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=config.api_key)
        except ImportError:
            self.client = None
    
    def chat(self, messages: List[Message], tools: Optional[List[Dict]] = None,
             **kwargs) -> LLMResponse:
        if not self.client:
            raise RuntimeError("Anthropic client not available")
        
        # Convert messages to Anthropic format
        system = None
        chat_messages = []
        for m in messages:
            if m.role == "system":
                system = m.content
            else:
                chat_messages.append({"role": m.role, "content": m.content})
        
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=kwargs.get("max_tokens", 4096),
            system=system,
            messages=chat_messages,
            tools=tools
        )
        
        return LLMResponse(
            content=response.content[0].text if response.content else "",
            provider=self.name,
            model=self.config.model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            raw_response=response
        )
    
    def chat_stream(self, messages: List[Message], tools: Optional[List[Dict]] = None,
                    **kwargs) -> Iterator[str]:
        if not self.client:
            raise RuntimeError("Anthropic client not available")
        
        system = None
        chat_messages = []
        for m in messages:
            if m.role == "system":
                system = m.content
            else:
                chat_messages.append({"role": m.role, "content": m.content})
        
        with self.client.messages.stream(
            model=self.config.model,
            max_tokens=kwargs.get("max_tokens", 4096),
            system=system,
            messages=chat_messages
        ) as stream:
            for text in stream.text_stream:
                yield text


class OllamaProvider(BaseProvider):
    """Ollama local provider"""
    
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"
    
    def chat(self, messages: List[Message], tools: Optional[List[Dict]] = None,
             **kwargs) -> LLMResponse:
        import requests
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.config.model,
                "messages": [m.to_dict() for m in messages],
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        
        return LLMResponse(
            content=data["message"]["content"],
            provider=self.name,
            model=self.config.model,
            usage={},
            raw_response=data
        )
    
    def chat_stream(self, messages: List[Message], tools: Optional[List[Dict]] = None,
                    **kwargs) -> Iterator[str]:
        import requests
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.config.model,
                "messages": [m.to_dict() for m in messages],
                "stream": True
            },
            stream=True
        )
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "message" in data and "content" in data["message"]:
                    yield data["message"]["content"]


class LLMClient:
    """Universal LLM client with fallback"""
    
    def __init__(self):
        self._providers: Dict[str, BaseProvider] = {}
        self._configs: Dict[str, ProviderConfig] = {}
        self._fallback_enabled = True
    
    def add_provider(self, config: ProviderConfig) -> None:
        """Add a provider"""
        self._configs[config.name] = config
        
        # Create provider instance
        if config.name == "openai":
            self._providers[config.name] = OpenAIProvider(config)
        elif config.name == "anthropic":
            self._providers[config.name] = AnthropicProvider(config)
        elif config.name == "ollama":
            self._providers[config.name] = OllamaProvider(config)
    
    def load_config(self, path: str) -> None:
        """Load configuration from file"""
        config = json.loads(Path(path).read_text())
        
        for name, provider_config in config.get("providers", {}).items():
            # Expand environment variables
            api_key = provider_config.get("api_key", "")
            if api_key.startswith("${") and api_key.endswith("}"):
                env_var = api_key[2:-1]
                api_key = os.environ.get(env_var)
            
            self.add_provider(ProviderConfig(
                name=name,
                api_key=api_key,
                model=provider_config.get("model", "gpt-4"),
                base_url=provider_config.get("base_url"),
                priority=provider_config.get("priority", 1),
                timeout=provider_config.get("timeout", 30)
            ))
    
    def chat(self, messages: List[Message], provider: str,
             tools: Optional[List[Dict]] = None, **kwargs) -> LLMResponse:
        """Chat with specific provider"""
        prov = self._providers.get(provider)
        if not prov:
            raise ValueError(f"Provider not found: {provider}")
        
        return prov.chat(messages, tools, **kwargs)
    
    def chat_auto(self, messages: List[Message], tools: Optional[List[Dict]] = None,
                  **kwargs) -> LLMResponse:
        """Auto-select provider by priority"""
        # Sort by priority
        sorted_providers = sorted(
            self._providers.items(),
            key=lambda x: self._configs[x[0]].priority
        )
        
        last_error = None
        for name, provider in sorted_providers:
            if not provider.is_available():
                continue
            
            try:
                return provider.chat(messages, tools, **kwargs)
            except Exception as e:
                last_error = e
                continue
        
        if last_error:
            raise last_error
        raise RuntimeError("No available providers")
    
    def chat_stream(self, messages: List[Message], provider: str,
                    tools: Optional[List[Dict]] = None, **kwargs) -> Iterator[str]:
        """Stream chat with specific provider"""
        prov = self._providers.get(provider)
        if not prov:
            raise ValueError(f"Provider not found: {provider}")
        
        return prov.chat_stream(messages, tools, **kwargs)
    
    def compare(self, messages: List[Message], 
                providers: List[str]) -> Dict[str, LLMResponse]:
        """Compare responses from multiple providers"""
        results = {}
        for name in providers:
            if name in self._providers:
                try:
                    results[name] = self._providers[name].chat(messages)
                except Exception as e:
                    results[name] = LLMResponse(
                        content=f"Error: {str(e)}",
                        provider=name,
                        model="error"
                    )
        return results
    
    def list_providers(self) -> List[str]:
        """List available providers"""
        return [name for name, p in self._providers.items() if p.is_available()]
