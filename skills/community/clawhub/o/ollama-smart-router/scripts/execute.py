#!/usr/bin/env python3
"""
Execute tasks using Ollama API (local or remote/cloud instances).
"""

import json
import requests
import os
from typing import Iterator

def execute_ollama(
    task: str,
    model: str,
    base_url: str = "http://localhost:11434",
    stream: bool = True,
    temperature: float = 0.7,
    system: str | None = None,
    max_retries: int = 2
) -> str | Iterator[str]:
    """
    Execute a task using Ollama API with retry logic.
    
    Args:
        task: The user prompt
        model: Model name (e.g., "llama3.2", "qwen2.5:14b")
        base_url: Ollama API base URL (localhost for local, remote URL for cloud)
        stream: Whether to stream response
        temperature: Sampling temperature
        system: Optional system prompt
        max_retries: Number of retry attempts on failure
    
    Returns:
        Full response string (or iterator if streaming)
    """
    
    import time
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            url = f"{base_url}/api/generate"
            
            payload = {
                "model": model,
                "prompt": task,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                }
            }
            
            if system:
                payload["system"] = system
            
            response = requests.post(url, json=payload, stream=stream, timeout=120)
            response.raise_for_status()
            
            if stream:
                return _stream_response(response)
            else:
                # Non-streaming: accumulate full response
                full_text = ""
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            full_text += data["response"]
                return full_text
                
        except requests.exceptions.ConnectionError as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            raise RuntimeError(f"Cannot connect to Ollama at {base_url}. Is it running?")
        except requests.exceptions.Timeout as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            raise RuntimeError(f"Request to {base_url} timed out after {max_retries + 1} attempts")
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            raise RuntimeError(f"Ollama API error: {e}")

def _stream_response(response) -> Iterator[str]:
    """Stream generator for Ollama responses."""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]
                if data.get("done", False):
                    break
            except json.JSONDecodeError:
                continue

def execute_chat_ollama(
    messages: list[dict],
    model: str,
    base_url: str = "http://localhost:11434",
    stream: bool = False,
    temperature: float = 0.7
) -> str:
    """
    Execute chat using Ollama chat API (/api/chat).
    
    Args:
        messages: List of {"role": "user|assistant|system", "content": "..."}
        model: Model name
        base_url: Ollama API base URL
        stream: Whether to stream
        temperature: Sampling temperature
    
    Returns:
        Assistant's response text
    """
    
    url = f"{base_url}/api/chat"
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "options": {
            "temperature": temperature,
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        return data.get("message", {}).get("content", "")
        
    except Exception as e:
        raise RuntimeError(f"Ollama chat API error: {e}")

def list_models(base_url: str = "http://localhost:11434") -> list[str]:
    """List available models from Ollama instance."""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        response.raise_for_status()
        data = response.json()
        return [m["name"] for m in data.get("models", [])]
    except Exception as e:
        return []

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: execute.py <model> <task> [base_url]")
        print("Example: execute.py llama3.2 'What is 2+2?'")
        print("Example: execute.py qwen2.5:14b 'Write a poem' http://remote-server:11434")
        sys.exit(1)
    
    model = sys.argv[1]
    task = sys.argv[2]
    base_url = sys.argv[3] if len(sys.argv) > 3 else "http://localhost:11434"
    
    print(f"Executing with {model} at {base_url}...")
    print("-" * 50)
    
    try:
        result = execute_ollama(task, model, base_url, stream=False)
        print(result)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
