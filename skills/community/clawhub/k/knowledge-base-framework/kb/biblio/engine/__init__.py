#!/usr/bin/env python3
"""
kb.llm.engine - LLM Engine Package

Provides abstract base class and concrete engine implementations.

Available engines:
- OllamaEngine: Connects to external Ollama server (default)
- TransformersEngine: Loads HuggingFace models in-process

Usage:
    from kb.biblio.engine import BaseLLMEngine, OllamaEngine, TransformersEngine
    from kb.biblio.engine import create_engine
"""

from kb.biblio.engine.base import BaseLLMEngine, LLMProvider, LLMResponse, LLMStreamChunk
from kb.biblio.engine.ollama_engine import OllamaEngine, OllamaEngineError, OllamaConnectionError
from kb.biblio.engine.transformers_engine import (
    TransformersEngine,
    TransformersEngineError,
    TransformersModelLoadError,
    TransformersGenerationError,
)
from kb.biblio.engine.factory import create_engine, EngineFactory, DefaultEngineFactory
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError, get_engine_registry

__all__ = [
    "BaseLLMEngine",
    "LLMProvider",
    "LLMResponse",
    "LLMStreamChunk",
    "OllamaEngine",
    "OllamaEngineError",
    "OllamaConnectionError",
    "TransformersEngine",
    "TransformersEngineError",
    "TransformersModelLoadError",
    "TransformersGenerationError",
    "EngineFactory",
    "DefaultEngineFactory",
    "EngineRegistry",
    "EngineRegistryError",
    "get_engine_registry",
    "create_engine",
]