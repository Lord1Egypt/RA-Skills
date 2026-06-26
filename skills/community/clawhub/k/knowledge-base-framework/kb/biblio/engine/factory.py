#!/usr/bin/env python3
"""
Engine Factory - Create LLM engine instances based on configuration.

Provides:
- EngineFactory Protocol for dependency injection / testability
- DefaultEngineFactory for production use
- create_engine() convenience function (backward compatible)

Usage:
    from kb.biblio.config import LLMConfig
    from kb.biblio.engine import create_engine

    # Single source (backward compatible)
    config = LLMConfig(model_source="huggingface")
    engine = create_engine(config)

    # Auto mode: returns primary engine (HF with Ollama fallback)
    config = LLMConfig(model_source="auto")
    engine = create_engine(config)

    # Access both engines for compare mode
    from kb.biblio.engine.registry import get_engine_registry
    registry = get_engine_registry()
    primary, secondary = registry.get_both()

    # Inject custom factory for testing
    from kb.biblio.engine.factory import EngineFactory
    class MockFactory:
        def create_ollama_engine(self, config): ...
        def create_hf_engine(self, config): ...
    registry = EngineRegistry.get_instance(engine_factory=MockFactory())
"""

from typing import Optional, Protocol, runtime_checkable

from kb.biblio.config import LLMConfig, LLMConfigError, get_llm_config


@runtime_checkable
class EngineFactory(Protocol):
    """Protocol for engine creation – inject into EngineRegistry for testability.

    Implement this protocol to replace engine creation with mocks or
    alternative implementations. The DefaultEngineFactory uses the
    real OllamaEngine and TransformersEngine singletons.
    """

    def create_ollama_engine(self, config: LLMConfig) -> 'BaseLLMEngine': ...
    def create_hf_engine(self, config: LLMConfig) -> 'BaseLLMEngine': ...


class DefaultEngineFactory:
    """Production engine factory – creates real engine instances.

    Uses OllamaEngine.get_instance() and TransformersEngine.get_instance()
    just like the original EngineRegistry._create_* methods did.
    """

    def create_ollama_engine(self, config: LLMConfig) -> 'BaseLLMEngine':
        """Create an OllamaEngine instance."""
        from kb.biblio.engine.ollama_engine import OllamaEngine
        return OllamaEngine.get_instance(config)

    def create_hf_engine(self, config: LLMConfig) -> 'BaseLLMEngine':
        """Create a TransformersEngine instance."""
        from kb.biblio.engine.transformers_engine import TransformersEngine
        from kb.biblio.engine.registry import EngineRegistryError
        engine = TransformersEngine.get_instance(config)
        if not engine.is_available():
            raise EngineRegistryError(
                "HuggingFace dependencies not installed. "
                "Install with: pip install -r requirements-transformers.txt"
            )
        return engine


def create_engine(config: Optional[LLMConfig] = None) -> 'BaseLLMEngine':
    """
    Create an LLM engine based on the model_source configuration.
    
    For single-source modes ("ollama", "huggingface"), returns the
    corresponding engine directly.
    
    For multi-source modes ("auto", "compare"), delegates to
    EngineRegistry and returns the primary engine. Use
    get_engine_registry() for access to both engines.
    
    Args:
        config: LLMConfig instance. Uses global singleton if None.
    
    Returns:
        BaseLLMEngine instance (primary engine for multi-source modes)
    
    Raises:
        LLMConfigError: If model_source is invalid or required
            dependencies are missing.
    """
    if config is None:
        config = get_llm_config()
    
    source = config.model_source
    
    # Single-source modes: direct creation (backward compatible)
    if source == "ollama":
        from kb.biblio.engine.ollama_engine import OllamaEngine
        return OllamaEngine.get_instance(config)
    
    elif source == "huggingface":
        from kb.biblio.engine.transformers_engine import TransformersEngine
        engine = TransformersEngine.get_instance(config)
        if not engine.is_available():
            raise LLMConfigError(
                "HuggingFace dependencies not installed. "
                "Install with: pip install -r requirements-transformers.txt"
            )
        return engine
    
    # Multi-source modes: delegate to EngineRegistry
    elif source in ("auto", "compare"):
        from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError
        try:
            registry = EngineRegistry.get_instance(config)
            return registry.get_primary()
        except EngineRegistryError as e:
            raise LLMConfigError(str(e)) from e
    
    else:
        raise LLMConfigError(
            f"Unknown model_source: {source}. "
            f"Must be 'ollama', 'huggingface', 'auto', or 'compare'"
        )