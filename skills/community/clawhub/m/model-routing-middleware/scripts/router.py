"""
Model Router — Main routing logic

Classifies a prompt, checks context size, and returns the optimal
model + think mode configuration.

Flow:
    1. Check context size → if > threshold, override to large-context model
    2. Classify task type → keyword matching
    3. Look up routing rule → model + think mode
    4. Return Route with full model metadata


"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

import yaml

from router.classifiers import TaskType, classify_task, ClassificationResult
from router.models import ModelRegistry, ModelInfo

logger = logging.getLogger("router")


@dataclass
class Route:
    """Result of a routing decision."""
    model: str                    # Model ID to use (e.g., "qwen3:14b")
    model_key: str                # Config key (e.g., "qwen3-14b")
    think: bool                   # Whether to enable think/reasoning mode
    task_type: TaskType           # Detected task type
    confidence: float             # Classification confidence
    context_overridden: bool      # True if context size forced a model change
    original_task: Optional[TaskType] = None  # Task type before context override
    provider: str = "ollama"     # Provider to use
    endpoint: str = ""           # API endpoint
    context_limit: int = 0       # Model's context window limit
    reason: str = ""              # Human-readable routing reason
    timestamp: str = ""           # ISO timestamp of routing decision

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


class ModelRouter:
    """
    Routes prompts to the optimal model based on task type and context size.

    Priority:
        1. Context size check — if prompt + context > threshold, use large-context model
        2. Task classification — keyword-based detection
        3. Routing rules — map task type to model + think mode
        4. Fallback — default model with no think mode
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the router with configuration.

        Args:
            config_path: Path to config.yaml. Defaults to ./config.yaml.
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.registry = ModelRegistry(self.config)
        self._routing_rules = self.config.get("routing", {})
        self._context_config = self.config.get("context", {})
        self._log_routing = self.config.get("logging", {}).get("enabled", True)

        # Set up logging
        log_config = self.config.get("logging", {})
        if log_config.get("enabled", True):
            log_level = getattr(logging, log_config.get("level", "INFO"), logging.INFO)
            logger.setLevel(log_level)
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
                ))
                logger.addHandler(handler)

    @staticmethod
    def _load_config(config_path: str) -> dict:
        """Load YAML configuration."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def route_request(
        self,
        prompt: str,
        context_size: int = 0,
        context_messages: Optional[list] = None,
    ) -> Route:
        """
        Route a request to the optimal model.

        Args:
            prompt: The user prompt to route.
            context_size: Size of context in tokens (if known).
            context_messages: List of context messages (for size estimation).

        Returns:
            Route with model, think mode, and metadata.
        """
        large_ctx_threshold = self._context_config.get("large_context_threshold", 120000)

        # Step 1: Classify the task
        classification = classify_task(prompt)
        task_type = classification.task_type
        confidence = classification.confidence

        # Step 2: Check context size — override if too large
        effective_context = context_size
        if effective_context == 0 and context_messages:
            # Rough estimate: ~4 chars per token
            total_chars = sum(len(str(m)) for m in context_messages)
            effective_context = total_chars // 4

        context_overridden = False
        original_task = None

        if effective_context > large_ctx_threshold:
            # Context too large for local models → use cloud model
            context_overridden = True
            original_task = task_type
            task_type = TaskType.CHAT  # Reset to chat, but force large context model
            logger.info(
                f"Context override: {effective_context} tokens > {large_ctx_threshold} threshold. "
                f"Original task: {original_task.value} → routing to large-context model."
            )

        # Step 3: Look up routing rule
        rule = self._routing_rules.get(task_type.value, self._routing_rules.get("default", {}))
        model_key = rule.get("model", "qwen3-14b")
        think = rule.get("think", False)

        # Step 4: If context override, force the large-context model
        if context_overridden:
            model_key = "glm-5-1-cloud"
            think = rule.get("think", False)  # Preserve think mode from original task

        # Step 5: Get model info from registry
        model_info = self.registry.get_model(model_key)

        # Step 6: Build route
        reason = self._build_reason(
            task_type, classification, context_overridden, original_task,
            effective_context, large_ctx_threshold, model_key, think,
        )

        route = Route(
            model=model_info.model_id if model_info else model_key,
            model_key=model_key,
            think=think,
            task_type=task_type,
            confidence=confidence,
            context_overridden=context_overridden,
            original_task=original_task,
            provider=model_info.provider if model_info else "ollama",
            endpoint=model_info.endpoint if model_info else "http://127.0.0.1:11434",
            context_limit=model_info.context_limit if model_info else 0,
            reason=reason,
        )

        # Step 7: Log the routing decision
        if self._log_routing:
            self._log_route(route, prompt, classification, effective_context)

        return route

    def _build_reason(
        self,
        task_type: TaskType,
        classification: ClassificationResult,
        context_overridden: bool,
        original_task: Optional[TaskType],
        context_size: int,
        threshold: int,
        model_key: str,
        think: bool,
    ) -> str:
        """Build a human-readable routing reason."""
        if context_overridden:
            return (
                f"Context size {context_size} exceeds threshold {threshold}. "
                f"Original task {original_task.value if original_task else 'unknown'} "
                f"→ overridden to {model_key} (large context). Think={think}."
            )

        matches = classification.matched_keywords[:5]  # Show first 5 matches
        return (
            f"Task classified as {task_type.value} "
            f"(confidence: {classification.confidence:.2f}, "
            f"keywords: {matches}) "
            f"→ {model_key} with think={think}."
        )

    def _log_route(
        self,
        route: Route,
        prompt: str,
        classification: ClassificationResult,
        context_size: int,
    ) -> None:
        """Log routing decision for analysis."""
        log_config = self.config.get("logging", {})
        preview_len = log_config.get("prompt_preview_length", 200)
        preview = prompt[:preview_len] + "..." if len(prompt) > preview_len else prompt

        logger.info(
            f"ROUTE | model={route.model} | think={route.think} | "
            f"task={route.task_type.value} | confidence={route.confidence:.2f} | "
            f"ctx_override={route.context_overridden} | context={context_size} | "
            f"prompt=\"{preview}\""
        )


def route_request(
    prompt: str,
    context_size: int = 0,
    context_messages: Optional[list] = None,
    config_path: Optional[str] = None,
) -> Route:
    """
    Convenience function to route a request without instantiating ModelRouter.

    Args:
        prompt: The user prompt to route.
        context_size: Size of context in tokens (if known).
        context_messages: List of context messages (for size estimation).
        config_path: Path to config.yaml.

    Returns:
        Route with model, think mode, and metadata.
    """
    router = ModelRouter(config_path=config_path)
    return router.route_request(prompt, context_size, context_messages)