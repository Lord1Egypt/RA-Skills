"""
Smart Router - Intelligent Ollama Model Routing

A complete system for routing AI tasks between local and cloud Ollama instances
based on task complexity classification.

Usage:
    from smart_router import SmartRouter
    
    router = SmartRouter()
    
    # Route with auto-generated conversation ID
    for chunk in router.route("Explain quantum computing"):
        print(chunk, end='')
    
    # Route with existing conversation context
    for chunk in router.route("What about entanglement?", conversation_id="conv_123"):
        print(chunk, end='')
"""

__version__ = "1.0.0"
__author__ = "OpenClaw Agent"

import sys
from pathlib import Path

# Ensure scripts are in path
scripts_dir = Path(__file__).parent / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

try:
    from route import route_task, load_config
    from execute import execute_ollama, list_models
    from classify import classify_task
    from cache import get_cache, RouterCache
    from conversation import get_memory, ConversationMemory
    from health_check import check_ollama_health, check_all_endpoints
except ImportError as e:
    raise ImportError(f"Failed to import smart_router components: {e}")

__all__ = [
    "SmartRouter",
    "route_task",
    "execute_ollama",
    "list_models",
    "classify_task",
    "load_config",
    "get_cache",
    "RouterCache",
    "get_memory",
    "ConversationMemory",
    "check_ollama_health",
    "check_all_endpoints",
]


class SmartRouter:
    """
    Main router interface for smart model selection.
    
    Features:
    - Automatic task classification (1-5 complexity)
    - System-aware model selection (local vs cloud)
    - Caching for speed (classifications, model lists, health)
    - Conversation memory for context-aware routing
    - Health checking with automatic fallback
    
    Example:
        router = SmartRouter(config_path="config/my-router.yaml")
        
        # Start a conversation
        conv_id = router.start_conversation()
        
        # First message (likely routes to cloud)
        for chunk in router.route("Explain quantum computing", conversation_id=conv_id):
            print(chunk, end='')
        
        # Follow-up (likely routes to local due to context)
        for chunk in router.route("What about entanglement?", conversation_id=conv_id):
            print(chunk, end='')
    """
    
    def __init__(self, config_path: str | None = None):
        """
        Initialize router with configuration.
        
        Args:
            config_path: Path to router.yaml config file
        """
        self.config_path = Path(config_path) if config_path else None
        self.config = load_config(self.config_path)
        self._cache = None
        self._memory = None
    
    def _get_cache(self):
        """Lazy-load cache."""
        if self._cache is None:
            cache_config = self.config.get("cache", {})
            db_path = cache_config.get("db_path", "cache/router.db")
            ttl = cache_config.get("ttl_seconds", 86400)
            self._cache = get_cache(db_path, ttl)
        return self._cache
    
    def _get_memory(self):
        """Lazy-load conversation memory."""
        if self._memory is None:
            self._memory = get_memory()
        return self._memory
    
    def start_conversation(self) -> str:
        """
        Start a new conversation for context-aware routing.
        
        Returns:
            conversation_id: Unique ID for this conversation
        """
        return self._get_memory().start_conversation()
    
    def route(self, task: str, conversation_id: str | None = None):
        """
        Route a task and stream the response.
        
        Args:
            task: The task/prompt to route
            conversation_id: Optional conversation ID for context. If not provided,
                           a new conversation is started automatically.
            
        Yields:
            Response chunks (first is JSON routing info)
        """
        if conversation_id is None:
            conversation_id = self.start_conversation()
        
        yield from route_task(task, self.config, conversation_id)
    
    def classify(self, task: str, use_context: bool = False, conversation_id: str | None = None) -> tuple[int, str]:
        """
        Classify task complexity without routing.
        
        Args:
            task: Task to classify
            use_context: Whether to use conversation context (requires conversation_id)
            conversation_id: Conversation ID for context adjustment
            
        Returns:
            (score: 1-5, reason: str)
        """
        if use_context and conversation_id:
            # Get base classification then adjust for context
            score, reason = classify_task(task)
            adjusted_score = self._get_memory().adjust_classification(conversation_id, score, task)
            return adjusted_score, reason
        else:
            return classify_task(task)
    
    def get_config(self) -> dict:
        """Get current configuration."""
        return self.config
    
    def check_health(self) -> dict:
        """
        Check health of all configured endpoints.
        
        Returns:
            Dict of endpoint names to health status
        """
        return check_all_endpoints(self.config_path)
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        return self._get_cache().get_stats()
    
    def get_conversation_stats(self) -> dict:
        """Get conversation memory statistics."""
        return self._get_memory().get_stats()
    
    def clear_cache(self):
        """Clear all cached entries."""
        self._get_cache().clear()
