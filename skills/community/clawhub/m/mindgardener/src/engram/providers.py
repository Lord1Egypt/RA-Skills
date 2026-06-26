"""LLM provider abstraction — Google, OpenAI, Anthropic."""

import json
import os
import re
import urllib.request
from typing import Optional


class LLMProvider:
    """Base class for LLM providers."""
    
    def generate(self, prompt: str, json_mode: bool = True) -> Optional[dict | str]:
        raise NotImplementedError

    async def generate_json(self, prompt: str) -> dict:
        """Async JSON generation (used by PE engine)."""
        return self.generate(prompt, json_mode=True) or {}

    def generate_json_sync(self, prompt: str) -> dict:
        """Sync JSON generation (used by PE engine)."""
        return self.generate(prompt, json_mode=True) or {}


class GoogleProvider(LLMProvider):
    """Google Gemini API."""
    
    MODELS = {
        "gemini-2.0-flash": "gemini-2.0-flash",
        "gemini-flash": "gemini-2.0-flash",
        "gemini-pro": "gemini-2.5-pro-preview-05-06",
    }
    
    def __init__(self, api_key: str = "", model: str = "gemini-2.0-flash", temperature: float = 0.1):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = self.MODELS.get(model, model)
        self.temperature = temperature
    
    def generate(self, prompt: str, json_mode: bool = True) -> Optional[dict | str]:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        gen_config = {"temperature": self.temperature}
        if json_mode:
            gen_config["responseMimeType"] = "application/json"
        
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": gen_config,
        })
        
        req = urllib.request.Request(url, data=payload.encode(),
                                    headers={"Content-Type": "application/json"})
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        if json_mode:
            return _parse_json(text)
        return text


class OpenAIProvider(LLMProvider):
    """OpenAI-compatible API (works with any compatible endpoint)."""
    
    def __init__(self, api_key: str = "", model: str = "gpt-4o-mini", 
                 temperature: float = 0.1, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
    
    def generate(self, prompt: str, json_mode: bool = True) -> Optional[dict | str]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        url = f"{self.base_url}/chat/completions"
        
        body: dict = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
        )
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            text = data["choices"][0]["message"]["content"]
        
        if json_mode:
            return _parse_json(text)
        return text


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API."""
    
    def __init__(self, api_key: str = "", model: str = "claude-sonnet-4-20250514",
                 temperature: float = 0.1):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model
        self.temperature = temperature
    
    def generate(self, prompt: str, json_mode: bool = True) -> Optional[dict | str]:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        
        url = "https://api.anthropic.com/v1/messages"
        
        system = ""
        if json_mode:
            system = "You MUST respond with valid JSON only. No markdown fences, no explanation."
        
        body: dict = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }
        if system:
            body["system"] = system
        
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            }
        )
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            text = data["content"][0]["text"]
        
        if json_mode:
            return _parse_json(text)
        return text


class OllamaProvider(LLMProvider):
    """Ollama — local models, zero cost."""
    
    def __init__(self, model: str = "llama3.2", temperature: float = 0.1,
                 base_url: str = "http://localhost:11434", **kwargs):
        self.model = model
        self.temperature = temperature
        self.base_url = base_url.rstrip("/")
    
    def generate(self, prompt: str, json_mode: bool = True) -> Optional[dict | str]:
        url = f"{self.base_url}/api/generate"
        
        body: dict = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        if json_mode:
            body["format"] = "json"
        
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            text = data.get("response", "")
        
        if json_mode:
            return _parse_json(text)
        return text


class OpenAICompatibleProvider(LLMProvider):
    """Any OpenAI-compatible API — LM Studio, vLLM, Together, Groq, etc."""
    
    def __init__(self, api_key: str = "", model: str = "default",
                 temperature: float = 0.1, base_url: str = "http://localhost:1234/v1",
                 **kwargs):
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.model = model
        self.temperature = temperature
        self.base_url = base_url.rstrip("/")
    
    def generate(self, prompt: str, json_mode: bool = True) -> Optional[dict | str]:
        url = f"{self.base_url}/chat/completions"
        
        body: dict = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
        
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            text = data["choices"][0]["message"]["content"]
        
        if json_mode:
            return _parse_json(text)
        return text


def get_provider(provider: str = "google", **kwargs) -> LLMProvider:
    """Factory for LLM providers.
    
    Supported: google, openai, anthropic, ollama, compatible
    """
    providers = {
        "google": GoogleProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
        "compatible": OpenAICompatibleProvider,  # Any OpenAI-compatible API
        "lmstudio": OpenAICompatibleProvider,
        "vllm": OpenAICompatibleProvider,
        "together": OpenAICompatibleProvider,
        "groq": OpenAICompatibleProvider,
    }
    cls = providers.get(provider)
    if not cls:
        raise ValueError(f"Unknown provider: {provider}. Use: {list(providers.keys())}")
    return cls(**kwargs)


def _parse_json(text: str) -> Optional[dict]:
    """Parse JSON from text, handling markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*\n?', '', text)
        text = re.sub(r'\n?```\s*$', '', text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return None
