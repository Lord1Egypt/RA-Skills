#!/usr/bin/env python3
"""
EngineRegistry - Singleton registry for LLM engine instances.

Manages engine lifecycle for multi-source configurations:
- "auto" mode: HF primary, Ollama fallback
- "compare" mode: Both engines side-by-side
- Single source: Direct delegation

Usage:
    from kb.biblio.engine.registry import EngineRegistry
    
    registry = EngineRegistry.get_instance()
    engine = registry.get_primary()      # Returns primary engine
    fallback = registry.get_secondary()   # Returns fallback engine (auto/compare)
    both = registry.get_both()            # Returns (primary, secondary) tuple
"""

import logging
import threading
from typing import Optional, Tuple, Dict

from kb.biblio.config import LLMConfig, LLMConfigError, get_llm_config
from kb.biblio.engine.base import BaseLLMEngine, LLMProvider
from kb.biblio.engine.factory import EngineFactory, DefaultEngineFactory

logger = logging.getLogger(__name__)


class EngineRegistryError(Exception):
    """Errors from EngineRegistry operations."""
    pass


class EngineRegistry:
    """
    Singleton registry for LLM engine instances.
    
    Manages creation and caching of engine instances based on
    model_source configuration. Supports:
    - "ollama": Single OllamaEngine
    - "huggingface": Single TransformersEngine
    - "auto": TransformersEngine primary, OllamaEngine fallback
    - "compare": Both engines for diff/merge
    
    Thread-safe: All operations are protected by a lock.
    
    Auto mode behavior (Lumen's decision):
        HF first, on error fallback to Ollama.
        Local model (HF) has token priority when configured.
    
    Compare mode behavior (Lumen's decision):
        Diff-view with subsequent merge if results complement each other.
    """
    
    _instance: Optional['EngineRegistry'] = None
    _lock = threading.Lock()
    
    def __init__(self, config: Optional[LLMConfig] = None,
                 engine_factory: Optional[EngineFactory] = None):
        if EngineRegistry._instance is not None:
            raise EngineRegistryError("Use EngineRegistry.get_instance() instead of constructor")
        
        self._config = config or get_llm_config()
        self._engine_factory: EngineFactory = engine_factory or DefaultEngineFactory()
        self._engines: Dict[str, BaseLLMEngine] = {}
        self._initialized = False
        
        EngineRegistry._instance = self
    
    @classmethod
    def get_instance(cls, config: Optional[LLMConfig] = None,
                     engine_factory: Optional[EngineFactory] = None) -> 'EngineRegistry':
        """Get or create the singleton registry instance.
        
        Thread-safe: Protected by class-level lock.
        On first call, creates instance with given config (or global LLMConfig).
        
        Args:
            config: LLMConfig instance. Uses global singleton if None.
            engine_factory: EngineFactory instance for dependency injection.
                Uses DefaultEngineFactory if None. Pass a mock factory
                in tests to avoid creating real engines.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(config=config, engine_factory=engine_factory)
            return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset the singleton registry.
        
        Call this when model_source changes to force re-creation
        of engines on next access.
        """
        with cls._lock:
            if cls._instance is not None:
                # Shutdown any cached engines that support it
                for source, engine in cls._instance._engines.items():
                    if hasattr(engine, 'shutdown'):
                        try:
                            engine.shutdown()
                        except Exception as e:
                            logger.warning("Error shutting down %s engine: %s", source, e)
                cls._instance._engines.clear()
                cls._instance._initialized = False
            cls._instance = None
    
    def _ensure_initialized(self) -> None:
        """Lazily initialize engines based on config."""
        if self._initialized:
            return
        
        with self._lock:
            if self._initialized:
                return
            
            source = self._config.model_source
            logger.info("Initializing EngineRegistry for model_source=%s", source)
            
            if source == "ollama":
                self._engines["primary"] = self._create_ollama_engine()
            
            elif source == "huggingface":
                self._engines["primary"] = self._create_hf_engine()
            
            elif source == "auto":
                # HF first (primary), Ollama as fallback (secondary)
                try:
                    self._engines["primary"] = self._create_hf_engine()
                    logger.info("Auto mode: HF engine created as primary")
                except Exception as e:
                    logger.warning("Auto mode: HF engine creation failed: %s", e)
                
                try:
                    self._engines["secondary"] = self._create_ollama_engine()
                    logger.info("Auto mode: Ollama engine created as secondary/fallback")
                except Exception as e:
                    logger.warning("Auto mode: Ollama engine creation failed: %s", e)
                
                if "primary" not in self._engines and "secondary" not in self._engines:
                    raise EngineRegistryError(
                        "Auto mode: Neither HF nor Ollama engine could be created"
                    )
                
                # If HF failed, promote Ollama to primary
                if "primary" not in self._engines:
                    logger.info("Auto mode: HF unavailable, Ollama promoted to primary")
                    self._engines["primary"] = self._engines.pop("secondary")
            
            elif source == "compare":
                # Both engines required for compare mode
                self._engines["primary"] = self._create_hf_engine()
                self._engines["secondary"] = self._create_ollama_engine()
                logger.info("Compare mode: Both engines initialized")
            
            else:
                raise EngineRegistryError(
                    f"Unknown model_source: {source}. "
                    f"Must be one of: ollama, huggingface, auto, compare"
                )
            
            self._initialized = True
    
    def _create_ollama_engine(self) -> BaseLLMEngine:
        """Create an OllamaEngine instance via the injected factory."""
        return self._engine_factory.create_ollama_engine(self._config)
    
    def _create_hf_engine(self) -> BaseLLMEngine:
        """Create a TransformersEngine instance via the injected factory."""
        return self._engine_factory.create_hf_engine(self._config)
    
    def get_engine(self, source: Optional[str] = None) -> BaseLLMEngine:
        """Get an engine by source type.
        
        Args:
            source: Engine source type. If None, returns primary engine.
                    Valid values: "huggingface", "ollama"
        
        Returns:
            BaseLLMEngine instance for the requested source.
        
        Raises:
            EngineRegistryError: If requested engine is not available.
        """
        self._ensure_initialized()
        
        if source is None:
            return self.get_primary()
        
        if source == "huggingface":
            # Check primary first (HF is primary in auto/compare), then check all
            primary = self._engines.get("primary")
            if primary and primary.get_provider() == LLMProvider.HUGGINGFACE:
                return primary
            secondary = self._engines.get("secondary")
            if secondary and secondary.get_provider() == LLMProvider.HUGGINGFACE:
                return secondary
            raise EngineRegistryError("HuggingFace engine not available in registry")
        
        elif source == "ollama":
            primary = self._engines.get("primary")
            if primary and primary.get_provider() == LLMProvider.OLLAMA:
                return primary
            secondary = self._engines.get("secondary")
            if secondary and secondary.get_provider() == LLMProvider.OLLAMA:
                return secondary
            raise EngineRegistryError("Ollama engine not available in registry")
        
        else:
            raise EngineRegistryError(
                f"Unknown source: {source}. Must be 'huggingface' or 'ollama'"
            )
    
    def get_primary(self) -> BaseLLMEngine:
        """Get the primary engine.
        
        In auto mode: HF (if available), otherwise Ollama.
        In compare mode: HF.
        In single-source mode: The configured engine.
        
        Returns:
            Primary BaseLLMEngine instance.
        
        Raises:
            EngineRegistryError: If no primary engine is available.
        """
        self._ensure_initialized()
        
        engine = self._engines.get("primary")
        if engine is None:
            raise EngineRegistryError("No primary engine available")
        return engine
    
    def get_secondary(self) -> Optional[BaseLLMEngine]:
        """Get the secondary/fallback engine.
        
        In auto mode: Ollama (fallback).
        In compare mode: Ollama.
        In single-source mode: None.
        
        Returns:
            Secondary BaseLLMEngine or None if not applicable.
        """
        self._ensure_initialized()
        return self._engines.get("secondary")
    
    def get_both(self) -> Tuple[BaseLLMEngine, Optional[BaseLLMEngine]]:
        """Get both primary and secondary engines.
        
        Useful for compare mode and auto-fallback scenarios.
        
        Returns:
            Tuple of (primary, secondary). Secondary may be None.
        """
        return (self.get_primary(), self.get_secondary())
    
    def is_engine_available(self, source: str) -> bool:
        """Check if an engine for the given source is available.
        
        Performs a health check using the engine's is_available() method.
        
        Args:
            source: "huggingface" or "ollama"
        
        Returns:
            True if the engine exists and passes health check.
        """
        try:
            engine = self.get_engine(source)
            return engine.is_available()
        except (EngineRegistryError, Exception) as e:
            logger.debug("Engine %s availability check failed: %s", source, e)
            return False
    
    @property
    def model_source(self) -> str:
        """Current model_source configuration."""
        return self._config.model_source
    
    @property
    def has_secondary(self) -> bool:
        """Whether a secondary/fallback engine is configured."""
        self._ensure_initialized()
        return "secondary" in self._engines
    
    @property
    def primary_provider(self) -> LLMProvider:
        """Provider type of the primary engine."""
        return self.get_primary().get_provider()
    
    def status(self) -> Dict[str, any]:
        """Get registry status summary."""
        self._ensure_initialized()
        result = {
            "model_source": self.model_source,
            "primary": None,
            "secondary": None,
        }
        primary = self._engines.get("primary")
        if primary:
            result["primary"] = {
                "provider": primary.get_provider().value,
                "model": primary.get_model_name(),
                "available": primary.is_available(),
            }
        secondary = self._engines.get("secondary")
        if secondary:
            result["secondary"] = {
                "provider": secondary.get_provider().value,
                "model": secondary.get_model_name(),
                "available": secondary.is_available(),
            }
        return result
    
    def __repr__(self) -> str:
        return f"EngineRegistry(source={self._config.model_source}, engines={list(self._engines.keys())})"


def get_engine_registry() -> EngineRegistry:
    """Get EngineRegistry singleton instance."""
    return EngineRegistry.get_instance()