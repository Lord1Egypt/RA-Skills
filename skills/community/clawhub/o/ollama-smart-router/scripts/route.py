#!/usr/bin/env python3
"""
Smart Router - Main entry point for intelligent model routing.
Routes tasks between local Ollama and cloud Ollama instances based on complexity.
"""

import sys
import os
import json
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Iterator, Optional

# Add parent dir for imports
sys.path.insert(0, str(Path(__file__).parent))

from execute import execute_ollama, list_models
from cache import get_cache
from conversation import get_memory
from health_check import check_ollama_health

try:
    from search_integration import is_search_query, get_search_context
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

def load_config(config_path: Path | None = None) -> dict:
    """Load router configuration from config file."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "router.yaml"
    
    # Load system profile if exists
    profile_path = Path(__file__).parent.parent / "config" / "system_profile.json"
    system_profile = {}
    if profile_path.exists():
        try:
            with open(profile_path) as f:
                system_profile = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load system profile: {e}", file=sys.stderr)
    
    default_config = {
        "local": {"model": system_profile.get("recommended_local", "llama3.2"), 
                  "base_url": "http://localhost:11434"},
        "cloud": {"model": "qwen2.5:14b", 
                  "base_url": "http://localhost:11434"},
        "threshold": 3,
        "log_file": "logs/router.log",
        "specialists": {},
        "cache": {"enabled": True, "db_path": "cache/router.db", "ttl_seconds": 86400},
        "performance": {"timeout_seconds": 60, "stream_responses": True, "retry_attempts": 2},
        "system_profile": system_profile,
        "search": {"enabled": True, "limit": 5, "category": "general"}
    }
    
    if config_path.exists():
        try:
            import yaml
            with open(config_path) as f:
                user_config = yaml.safe_load(f) or {}
                # Deep merge for nested dicts
                config = default_config.copy()
                for key, value in user_config.items():
                    if isinstance(value, dict) and key in config:
                        config[key].update(value)
                    else:
                        config[key] = value
                return config
        except Exception as e:
            print(f"Warning: Could not load config: {e}", file=sys.stderr)
    
    return default_config

def log_route(task: str, decision: str, model: str, base_url: str, latency: float, config: dict, 
              conversation_id: Optional[str] = None, search_used: bool = False):
    """Log routing decision."""
    log_path = Path(config.get("log_file", "logs/router.log"))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().isoformat()
    url_hint = "local" if "localhost" in base_url else "cloud"
    conv_hint = f" | conv: {conversation_id[:8]}" if conversation_id else ""
    search_hint = " | +search" if search_used else ""
    log_line = f"[{timestamp}] task: '{task[:50]}{'...' if len(task) > 50 else ''}' -> {decision} | model: {model} ({url_hint}) | latency: {latency:.2f}s{conv_hint}{search_hint}\n"
    
    with open(log_path, "a") as f:
        f.write(log_line)

def check_specialists(task: str, specialists: dict) -> dict | None:
    """Check if task matches any specialist triggers."""
    task_lower = task.lower()
    
    for name, spec in specialists.items():
        triggers = spec.get("triggers", [])
        for trigger in triggers:
            if trigger.lower() in task_lower:
                return {
                    "name": name,
                    "model": spec.get("model"),
                    "base_url": spec.get("base_url", "http://localhost:11434")
                }
    
    return None

def get_model_info(config: dict, decision: str) -> tuple[str, str]:
    """Get model name and base_url for a decision."""
    if decision == "local":
        return config["local"]["model"], config["local"]["base_url"]
    elif decision == "cloud":
        return config["cloud"]["model"], config["cloud"]["base_url"]
    else:
        return config["local"]["model"], config["local"]["base_url"]

def is_endpoint_healthy(base_url: str, cache) -> bool:
    """Check if endpoint is healthy (with caching)."""
    # Check cache first
    cached = cache.get_health_status(base_url)
    if cached:
        return cached.get("status") == "healthy"
    
    # Fresh check
    health = check_ollama_health(base_url)
    cache.set_health_status(base_url, health)
    return health["status"] == "healthy"

def verify_model_available(model: str, base_url: str, cache) -> bool:
    """Check if a model is available (with caching)."""
    # Check cache first
    cached_models = cache.get_available_models(base_url)
    if cached_models is not None:
        return model in cached_models or f"{model}:latest" in cached_models
    
    # Fetch fresh list
    try:
        available = list_models(base_url)
        cache.set_available_models(base_url, available)
        return model in available or f"{model}:latest" in available
    except Exception:
        return False

def classify_with_cache(task: str, conversation_id: Optional[str], cache, memory) -> tuple[int, str]:
    """
    Classify task with caching and conversation context.
    
    Returns: (score, reason)
    """
    # Check cache first
    cached = cache.get_classification(task)
    if cached:
        return cached
    
    # Run classifier via subprocess
    classify_script = Path(__file__).parent / "classify.py"
    result = subprocess.run(
        [sys.executable, str(classify_script), task],
        capture_output=True,
        text=True
    )
    
    output = result.stdout.strip()
    try:
        score = int(output.split(":")[0])
        reason = output.split(":")[1] if ":" in output else "unknown"
    except (ValueError, IndexError):
        score = result.returncode if result.returncode in range(1, 6) else 2
        reason = "default"
    
    # Adjust for conversation context
    if conversation_id:
        score = memory.adjust_classification(conversation_id, score, task)
    
    # Cache result
    cache.set_classification(task, score, reason)
    
    return score, reason

def route_task(task: str, config: dict | None = None, conversation_id: Optional[str] = None) -> Iterator[str]:
    """
    Route task to appropriate model and stream response.
    
    Args:
        task: The task to route
        config: Router configuration
        conversation_id: Optional conversation ID for context
        
    Yields: Response chunks from the selected model.
    """
    if config is None:
        config = load_config()
    
    start_time = time.time()
    
    # Initialize cache and memory
    cache_enabled = config.get("cache", {}).get("enabled", True)
    cache = get_cache() if cache_enabled else None
    memory = get_memory() if conversation_id else None
    
    # Start conversation if needed
    if memory and not conversation_id:
        conversation_id = memory.start_conversation()
    
    # Step 1: Check specialists first
    specialist = check_specialists(task, config.get("specialists", {}))
    if specialist:
        decision = f"specialist:{specialist['name']}"
        model = specialist["model"]
        base_url = specialist["base_url"]
    else:
        # Step 2: Classify complexity (with cache + context)
        score, reason = classify_with_cache(task, conversation_id, cache, memory)
        
        # Step 3: Route based on threshold
        threshold = config.get("threshold", 3)
        
        if score < threshold:
            decision = "local"
        else:
            decision = "cloud"
        
        model, base_url = get_model_info(config, decision)
    
    # Step 4: Check endpoint health
    if not is_endpoint_healthy(base_url, cache):
        # Fallback to local if cloud unhealthy
        if decision == "cloud":
            decision = "local (fallback)"
            model, base_url = get_model_info(config, "local")
        else:
            # Local also unhealthy - will fail later with error
            pass
    
    # Step 5: Verify model availability (with cache)
    if not verify_model_available(model, base_url, cache):
        # Try fallback models from system profile
        compatible = config.get("system_profile", {}).get("compatible_models", [])
        for alt_model in compatible:
            if verify_model_available(alt_model, base_url, cache):
                model = alt_model
                break
    
    # Step 6: Check if web search needed and fetch context
    search_enabled = config.get("search", {}).get("enabled", True)
    search_context = ""
    search_used = False
    if SEARCH_AVAILABLE and search_enabled and is_search_query(task):
        yield "\n[Detected web search query, fetching results...]\n"
        search_context = get_search_context(
            task, 
            limit=config.get("search", {}).get("limit", 5)
        )
        if search_context:
            search_used = True
            yield "[Web search results added to context]\n\n"
    
    # Step 7: Log the decision
    latency = time.time() - start_time
    log_route(task, decision, model, base_url, latency, config, conversation_id, search_used)
    
    # Step 8: Record in conversation memory
    if memory:
        memory.add_turn(conversation_id, task, 
                         score if 'score' in locals() else 0, 
                         decision, model)
    
    # Step 9: Execute with Ollama
    stream = config.get("performance", {}).get("stream_responses", True)
    retry_attempts = config.get("performance", {}).get("retry_attempts", 2)
    
    # Yield routing info first
    routing_info = {
        "type": "routing",
        "decision": decision,
        "model": model,
        "base_url": base_url,
        "latency_seconds": latency,
        "conversation_id": conversation_id,
        "search_used": search_used
    }
    yield json.dumps(routing_info) + "\n"
    
    # Yield search context if available
    if search_context:
        yield "\n---SEARCH-CONTEXT---\n"
        yield search_context
        yield "\n---END-SEARCH-CONTEXT---\n"
    
    yield "\n---RESPONSE---\n"
    
    # Execute with retry
    last_error = None
    for attempt in range(retry_attempts):
        try:
            # If search context exists, prepend to task
            full_task = task
            if search_context:
                full_task = f"{search_context}\n\nBased on the above web search results, please answer:\n{task}"
            
            response_iter = execute_ollama(full_task, model, base_url, stream=stream)
            
            if stream:
                for chunk in response_iter:
                    yield chunk
            else:
                yield response_iter
            
            # Success - return
            return
            
        except RuntimeError as e:
            last_error = e
            if attempt < retry_attempts - 1:
                time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                continue
    
    # All retries failed
    yield f"\n[Error after {retry_attempts} attempts: {last_error}]\n"
    
    # Final fallback to local if not already
    if decision != "local" and "local" not in decision:
        yield "\n[Final fallback to local model...]\n"
        local_model, local_url = get_model_info(config, "local")
        try:
            fallback_iter = execute_ollama(task, local_model, local_url, stream=stream)
            if stream:
                for chunk in fallback_iter:
                    yield chunk
            else:
                yield fallback_iter
        except RuntimeError as e2:
            yield f"\n[Fallback also failed: {e2}]\n"

def main():
    parser = argparse.ArgumentParser(description='Smart Router')
    parser.add_argument('task', help='The task to route')
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--no-stream', action='store_true', help='Don\'t stream output')
    parser.add_argument('--profile', action='store_true', help='Run system profiler first')
    parser.add_argument('--conversation', help='Conversation ID for context')
    args = parser.parse_args()
    
    # Run profiler if requested
    if args.profile:
        profiler_script = Path(__file__).parent / "system_profiler.py"
        subprocess.run([sys.executable, str(profiler_script)])
        print("\n" + "=" * 50)
        print("Now routing your task...")
        print("=" * 50 + "\n")
    
    # Load config
    config = None
    if args.config:
        import yaml
        with open(args.config) as f:
            config = yaml.safe_load(f)
    
    # Route and stream results
    for chunk in route_task(args.task, config, args.conversation):
        print(chunk, end='', flush=True)

if __name__ == '__main__':
    main()
