"""
Model Registry — Model definitions and endpoint management

Provides a registry of available models with their metadata,
endpoints, and capabilities. Used by the router to look up
model information after routing decisions.


"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("router.models")


@dataclass
class ModelInfo:
    """Metadata for a single model."""
    key: str                    # Config key (e.g., "qwen3-14b")
    model_id: str               # Ollama model ID (e.g., "qwen3:14b")
    provider: str               # Provider name (e.g., "ollama")
    endpoint: str               # API endpoint URL
    context_limit: int          # Max context window in tokens
    supports_think: bool        # Whether model supports think/reasoning mode
    cost_per_token_input: float # Cost per 1M input tokens
    cost_per_token_output: float# Cost per 1M output tokens
    description: str            # Human-readable description
    status: str                 # "available" | "needs_pull" | "offline"

    @property
    def is_available(self) -> bool:
        """Check if model is available for use."""
        return self.status == "available"

    @property
    def is_local(self) -> bool:
        """Check if model runs locally (free)."""
        return self.cost_per_token_input == 0.0 and self.cost_per_token_output == 0.0

    @property
    def is_cloud(self) -> bool:
        """Check if model is cloud-hosted (costs money)."""
        return not self.is_local


class ModelRegistry:
    """
    Registry of available models with lookup capabilities.

    Loads model definitions from config.yaml and provides
    methods to query model info by key or ID.
    """

    def __init__(self, config: dict):
        """
        Initialize the registry from parsed config.

        Args:
            config: Parsed config.yaml dictionary.
        """
        self._models: dict[str, ModelInfo] = {}
        self._model_id_map: dict[str, str] = {}  # model_id → key

        models_config = config.get("models", {})
        for key, model_data in models_config.items():
            cost = model_data.get("cost_per_token", {})
            info = ModelInfo(
                key=key,
                model_id=model_data.get("model_id", key),
                provider=model_data.get("provider", "ollama"),
                endpoint=model_data.get("endpoint", "http://127.0.0.1:11434"),
                context_limit=model_data.get("context_limit", 32768),
                supports_think=model_data.get("supports_think", False),
                cost_per_token_input=cost.get("input", 0.0),
                cost_per_token_output=cost.get("output", 0.0),
                description=model_data.get("description", ""),
                status=model_data.get("status", "available"),
            )
            self._models[key] = info
            self._model_id_map[info.model_id] = key

    def get_model(self, key: str) -> Optional[ModelInfo]:
        """
        Look up model by config key.

        Args:
            key: Config key (e.g., "qwen3-14b", "glm-5-1-cloud").

        Returns:
            ModelInfo or None if not found.
        """
        return self._models.get(key)

    def get_model_by_id(self, model_id: str) -> Optional[ModelInfo]:
        """
        Look up model by Ollama model ID.

        Args:
            model_id: Ollama model ID (e.g., "qwen3:14b", "glm-5.1:cloud").

        Returns:
            ModelInfo or None if not found.
        """
        key = self._model_id_map.get(model_id)
        if key:
            return self._models.get(key)
        return None

    def list_models(self) -> list[ModelInfo]:
        """Return list of all registered models."""
        return list(self._models.values())

    def list_available_models(self) -> list[ModelInfo]:
        """Return list of models that are currently available."""
        return [m for m in self._models.values() if m.is_available]

    def list_local_models(self) -> list[ModelInfo]:
        """Return list of models that run locally (free)."""
        return [m for m in self._models.values() if m.is_local]

    def list_cloud_models(self) -> list[ModelInfo]:
        """Return list of models that are cloud-hosted (paid)."""
        return [m for m in self._models.values() if m.is_cloud]

    def get_fallback_model(self) -> ModelInfo:
        """
        Return the default fallback model.

        Tries qwen3-14b first, then any available model.
        Raises ValueError if no models are available.
        """
        # Try default first
        default_key = "qwen3-14b"
        model = self._models.get(default_key)
        if model and model.is_available:
            return model

        # Try any available model
        available = self.list_available_models()
        if available:
            logger.warning(f"Default model '{default_key}' not available, using '{available[0].key}'")
            return available[0]

        raise ValueError("No models available in the registry")

    def find_model_for_context(self, context_size: int) -> Optional[ModelInfo]:
        """
        Find the best model that can handle the given context size.

        Prefers local models over cloud. Prefers cheaper models.
        Returns None if no model can handle the context size.
        """
        candidates = [
            m for m in self.list_available_models()
            if m.context_limit >= context_size
        ]
        if not candidates:
            return None

        # Sort: local first, then by cost, then by context limit (smallest that fits)
        def sort_key(m: ModelInfo) -> tuple:
            return (
                0 if m.is_local else 1,         # Local first
                m.cost_per_token_input,          # Cheaper first
                m.context_limit,                  # Smallest context that fits
            )

        candidates.sort(key=sort_key)
        return candidates[0]

    def __repr__(self) -> str:
        return f"ModelRegistry(models={list(self._models.keys())})"