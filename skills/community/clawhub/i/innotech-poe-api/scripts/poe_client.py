#!/usr/bin/env python3
"""
Poe API Client for OpenClaw
Simple interface to query multiple AI models with intelligent selection

Usage:
    from poe_client import PoeClient
    
    client = PoeClient()
    
    # Auto-select model
    result = client.query_for_task("programming", "Write a function")
    
    # Specific model
    result = client.query("claude-sonnet-4.6", "Your prompt")
    
    # Web search
    result = client.web_search("Latest AI news")
"""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import time

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("❌ openai not installed. Run: pip install openai")


# Model configurations by task type
MODEL_CONFIGS = {
    "programming": {
        "simple": "claude-haiku-4.5",
        "medium": "claude-sonnet-4.6",
        "complex": "claude-opus-4.6",
        "huge_context": "gemini-3.1-pro",
        "code_focused": "gpt-5.3-codex"
    },
    "ui_design": {
        "default": "gemini-3.1-pro",  # 1M context for design systems
        "fast": "claude-haiku-4.5",
        "components": "claude-sonnet-4.6"
    },
    "data_analysis": {
        "default": "claude-sonnet-4.6",
        "huge_data": "gemini-3.1-pro",
        "complex": "claude-opus-4.6"
    },
    "requirement_analysis": {
        "default": "claude-sonnet-4.6",
        "complex": "claude-opus-4.6",
        "huge_docs": "gemini-3.1-pro"
    },
    "web_search": {
        "simple": "perplexity-search",
        "complex": "perplexity-sonar-pro",
        "reasoning": "perplexity-sonar-rsn-pro",
        "deep": "o3-deep-research",
        "budget": "o4-mini-deep-research"
    },
    "image_generation": {
        "best": "imagen-4-ultra",
        "fast": "nano-banana-2",
        "text": "nano-banana-pro",
        "general": "nano-banana",
        "editing": "gpt-image-1.5"
    },
    "video_generation": {
        "best": "veo-3.1",
        "cinematic": "sora-2-pro",
        "versatile": "kling-o3",
        "standard": "sora-2",
        "storytelling": "wan-2.6"
    },
    "audio_generation": {
        "speech": "elevenlabs-v3",
        "fast_tts": "gemini-2.5-flash-tts",
        "controlled": "hailuo-speech-02",
        "music": "hailuo-music-v1.5"
    }
}


@dataclass
class PoeConfig:
    """Configuration for Poe API client"""
    api_key: str = field(default_factory=lambda: os.getenv("POE_API_KEY", ""))
    base_url: str = "https://api.poe.com/v1"
    
    # Budget control
    max_calls_per_task: int = 10
    max_retries: int = 3
    
    # Usage tracking
    call_count: int = 0
    total_tokens: int = 0


class PoeClient:
    """
    Simple Poe API client with intelligent model selection
    
    Example:
        client = PoeClient()
        
        # Auto-select model
        result = client.query_for_task("programming", "Write a function")
        
        # Specific model
        result = client.query("claude-sonnet-4.6", "Your prompt")
    """
    
    def __init__(self, config: Optional[PoeConfig] = None):
        self.config = config or PoeConfig()
        
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "openai not installed!\n"
                "Install with: pip install openai"
            )
        
        if not self.config.api_key:
            raise ValueError(
                "POE_API_KEY not set!\n"
                "Set with: export POE_API_KEY='your-api-key'\n"
                "Or pass in config"
            )
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )
    
    def query(
        self,
        model: str,
        message: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query a specific model
        
        Args:
            model: Model ID (e.g., "claude-sonnet-4.6")
            message: Your prompt
            context: Optional context to prepend
        
        Returns:
            {
                "success": bool,
                "response": str,
                "model": str,
                "tokens_used": int,
                "elapsed_time": float
            }
        """
        # Check call limit
        if self.config.call_count >= self.config.max_calls_per_task:
            return {
                "success": False,
                "error": f"Call limit exceeded: {self.config.call_count}/{self.config.max_calls_per_task}",
                "model": model
            }
        
        # Prepare message
        full_message = f"{context}\n\n{message}" if context else message
        
        try:
            start_time = time.time()
            
            # Query model (let Poe handle token limits)
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": full_message}]
            )
            
            elapsed = time.time() - start_time
            
            # Extract response
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
            
            # Update tracking
            self.config.call_count += 1
            self.config.total_tokens += tokens_used
            
            return {
                "success": True,
                "response": response_text,
                "model": model,
                "tokens_used": tokens_used,
                "elapsed_time": elapsed,
                "call_count": self.config.call_count
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model
            }
    
    def query_with_retry(
        self,
        model: str,
        message: str,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Query with automatic retry on failure"""
        max_retries = max_retries or self.config.max_retries
        
        for attempt in range(max_retries):
            result = self.query(model, message, **kwargs)
            
            if result["success"]:
                return result
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
        
        return result
    
    def query_for_task(
        self,
        task_type: str,
        message: str,
        complexity: str = "medium",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query with automatic model selection based on task type
        
        Args:
            task_type: "programming", "ui_design", "data_analysis", etc.
            message: Your prompt
            complexity: "simple", "medium", "complex"
        
        Returns:
            Result dict with model selection info
        """
        # Get model config for task
        task_config = MODEL_CONFIGS.get(task_type)
        
        if not task_config:
            # Default to claude-sonnet-4.6
            model = "claude-sonnet-4.6"
            selection_reason = "Default (unknown task type)"
        else:
            # Select based on complexity
            if complexity in task_config:
                model = task_config[complexity]
                selection_reason = f"Task: {task_type}, Complexity: {complexity}"
            elif "default" in task_config:
                model = task_config["default"]
                selection_reason = f"Task: {task_type}, Default"
            elif "medium" in task_config:
                model = task_config["medium"]
                selection_reason = f"Task: {task_type}, Medium"
            else:
                model = "claude-sonnet-4.6"
                selection_reason = "Fallback to default"
        
        # Query
        result = self.query_with_retry(model, message, **kwargs)
        result["model_selection"] = {
            "task_type": task_type,
            "complexity": complexity,
            "selected_model": model,
            "reason": selection_reason
        }
        
        return result
    
    # Convenience methods for common tasks
    
    def programming(
        self,
        task: str,
        complexity: str = "medium",
        **kwargs
    ) -> str:
        """
        Query for programming tasks
        
        Args:
            task: Programming task
            complexity: "simple", "medium", "complex"
        
        Returns:
            Response text or error message
        """
        result = self.query_for_task("programming", task, complexity, **kwargs)
        return result.get("response", f"Error: {result.get('error', 'Unknown error')}")
    
    def ui_design(
        self,
        task: str,
        **kwargs
    ) -> str:
        """Query for UI/UX design tasks"""
        result = self.query_for_task("ui_design", task, **kwargs)
        return result.get("response", f"Error: {result.get('error', 'Unknown error')}")
    
    def data_analysis(
        self,
        task: str,
        **kwargs
    ) -> str:
        """Query for data analysis tasks"""
        result = self.query_for_task("data_analysis", task, **kwargs)
        return result.get("response", f"Error: {result.get('error', 'Unknown error')}")
    
    def web_search(
        self,
        query: str,
        search_type: str = "complex",
        **kwargs
    ) -> str:
        """
        Perform web search
        
        Args:
            query: Search query
            search_type: "simple", "complex", "reasoning", "deep"
        """
        result = self.query_for_task("web_search", query, search_type, **kwargs)
        return result.get("response", f"Error: {result.get('error', 'Unknown error')}")
    
    def generate_image(
        self,
        prompt: str,
        quality: str = "fast",
        **kwargs
    ) -> str:
        """
        Generate image
        
        Args:
            prompt: Image description
            quality: "best", "fast", "text", "general", "editing"
        """
        result = self.query_for_task("image_generation", prompt, quality, **kwargs)
        return result.get("response", f"Error: {result.get('error', 'Unknown error')}")
    
    def generate_video(
        self,
        prompt: str,
        style: str = "best",
        **kwargs
    ) -> str:
        """
        Generate video
        
        Args:
            prompt: Video description
            style: "best", "cinematic", "versatile", "standard", "storytelling"
        """
        result = self.query_for_task("video_generation", prompt, style, **kwargs)
        return result.get("response", f"Error: {result.get('error', 'Unknown error')}")
    
    def generate_audio(
        self,
        text: str,
        audio_type: str = "speech",
        **kwargs
    ) -> str:
        """
        Generate audio
        
        Args:
            text: Text to convert
            audio_type: "speech", "fast_tts", "controlled", "music"
        """
        result = self.query_for_task("audio_generation", text, audio_type, **kwargs)
        return result.get("response", f"Error: {result.get('error', 'Unknown error')}")
    
    def reset_call_count(self):
        """Reset call counter"""
        self.config.call_count = 0
        self.config.total_tokens = 0
    
    def get_usage_stats(self) -> Dict[str, int]:
        """Get usage statistics"""
        return {
            "call_count": self.config.call_count,
            "total_tokens": self.config.total_tokens,
            "max_calls": self.config.max_calls_per_task
        }


# Convenience functions for quick use

def code(task: str, complexity: str = "medium") -> str:
    """
    Quick programming query
    
    Example:
        from poe_client import code
        result = code("Write a Python function to sort a list")
    """
    try:
        client = PoeClient()
        return client.programming(task, complexity)
    except Exception as e:
        return f"Error: {str(e)}"


def design(task: str) -> str:
    """Quick UI/UX design query"""
    try:
        client = PoeClient()
        return client.ui_design(task)
    except Exception as e:
        return f"Error: {str(e)}"


def analyze(task: str) -> str:
    """Quick data analysis query"""
    try:
        client = PoeClient()
        return client.data_analysis(task)
    except Exception as e:
        return f"Error: {str(e)}"


def search(query: str, search_type: str = "complex") -> str:
    """Quick web search"""
    try:
        client = PoeClient()
        return client.web_search(query, search_type)
    except Exception as e:
        return f"Error: {str(e)}"


def image(prompt: str, quality: str = "fast") -> str:
    """Quick image generation"""
    try:
        client = PoeClient()
        return client.generate_image(prompt, quality)
    except Exception as e:
        return f"Error: {str(e)}"


def video(prompt: str, style: str = "best") -> str:
    """Quick video generation"""
    try:
        client = PoeClient()
        return client.generate_video(prompt, style)
    except Exception as e:
        return f"Error: {str(e)}"


def audio(text: str, audio_type: str = "speech") -> str:
    """Quick audio generation"""
    try:
        client = PoeClient()
        return client.generate_audio(text, audio_type)
    except Exception as e:
        return f"Error: {str(e)}"
