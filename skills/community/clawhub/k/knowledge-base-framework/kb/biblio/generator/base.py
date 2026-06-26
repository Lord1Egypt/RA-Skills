#!/usr/bin/env python3
"""
BaseGenerator - Abstract Base Class for LLM Generators

Provides the common interface and shared functionality for all generators
(EssenceGenerator, ReportGenerator, etc.) including:

- Parallel mode configuration and dispatch
- Engine registry access (primary + secondary)
- Retry logic with exponential backoff
- Content reading utilities
- Template loading

All concrete generators inherit from BaseGenerator and ParallelMixin,
which together provide the full feature set.

Usage:
    from kb.biblio.generator.base import BaseGenerator

    class MyGenerator(BaseGenerator):
        async def generate(self, topic: str, **kwargs) -> GenerationResult:
            prompt = self.build_prompt(topic, ...)
            response = await self._generate_with_retry(prompt)
            return self.process_response(response, ...)
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from kb.biblio.config import LLMConfig, get_llm_config
from kb.biblio.engine.base import BaseLLMEngine, LLMResponse
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError, get_engine_registry
from kb.biblio.generator.parallel_mixin import (
    ParallelMixin, ParallelStrategy, ParallelResult,
)

logger = logging.getLogger(__name__)


class BaseGeneratorError(Exception):
    """Base error for generator operations."""
    pass


class BaseGenerator(ParallelMixin, ABC):
    """
    Abstract base class for LLM generators with parallel support.

    Combines ParallelMixin (diff/merge/parallel dispatch) with a standard
    generator interface. Subclasses must implement:
        - generate() - core generation logic
        - build_prompt() - prompt construction

    Provides:
        - Parallel mode configuration (via ParallelMixin.__init_parallel__)
        - Engine registry access (primary + secondary engines)
        - Retry logic with exponential backoff
        - Content reading from source files

    Attributes:
        _config: LLMConfig instance
        _engine: Primary LLM engine (backward compat)
        _parallel_strategy: Current parallel strategy
        _parallel_registry: Engine registry for parallel mode
    """

    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        engine: Optional[BaseLLMEngine] = None,
        registry: Optional[EngineRegistry] = None,
    ):
        """
        Initialize the base generator.

        Args:
            llm_config: Optional LLMConfig override (defaults to singleton)
            engine: Optional primary engine override (defaults to registry primary)
            registry: Optional EngineRegistry override (defaults to singleton)
        """
        self._config = llm_config or get_llm_config()

        # Try to get engine from registry if not provided
        if engine is not None:
            self._engine = engine
        else:
            try:
                self._engine = get_engine_registry().get_primary()
            except (EngineRegistryError, Exception) as e:
                logger.warning(
                    "Could not get primary engine from registry: %s. "
                    "Will use engine on first access.",
                    e
                )
                self._engine = None

        # Initialize parallel mixin support
        self.__init_parallel__(llm_config)
        if registry is not None:
            self._parallel_registry = registry

        logger.debug(
            "BaseGenerator initialized",
            extra={
                "model_source": self._config.model_source,
                "parallel_mode": self._config.parallel_mode,
                "parallel_strategy": self._config.parallel_strategy,
            }
        )

    # --- Abstract Methods ---

    @abstractmethod
    async def generate(self, **kwargs) -> Any:
        """
        Core generation method. Must be implemented by subclasses.

        Returns:
            Generator-specific result object
        """
        pass

    # --- Retry Logic ---

    async def _generate_with_retry(
        self,
        prompt: str,
        max_retries: Optional[int] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        Generate LLM response with retry logic and exponential backoff.

        Args:
            prompt: The prompt to send
            max_retries: Override config max_retries
            temperature: Override LLM temperature
            max_tokens: Override max tokens

        Returns:
            LLMResponse on success

        Raises:
            BaseGeneratorError: After all retries exhausted
        """
        retries = max_retries if max_retries is not None else self._config.max_retries
        last_error = None

        for attempt in range(retries):
            try:
                kwargs = {}
                if temperature is not None:
                    kwargs["temperature"] = temperature
                if max_tokens is not None:
                    kwargs["max_tokens"] = max_tokens

                engine = self._get_engine()
                response = await engine.generate_async(prompt, **kwargs)

                if response.success and response.content:
                    return response

                last_error = BaseGeneratorError(
                    f"Empty LLM response (attempt {attempt + 1}/{retries})"
                )
                logger.warning(
                    "Empty LLM response, retrying",
                    extra={"attempt": attempt + 1, "retries": retries}
                )

            except Exception as e:
                last_error = BaseGeneratorError(f"LLM engine error: {e}")
                logger.warning(
                    "LLM engine error, retrying",
                    extra={
                        "attempt": attempt + 1,
                        "retries": retries,
                        "error": str(e)
                    }
                )

            # Exponential backoff
            if attempt < retries - 1:
                delay = self._config.retry_delay * (2 ** attempt)
                logger.info(f"Retrying in {delay:.1f}s", extra={"attempt": attempt + 1})
                await asyncio.sleep(delay)

        raise BaseGeneratorError(
            f"All {retries} retries exhausted. Last error: {last_error}"
        )

    # --- Engine Access ---

    def _get_engine(self) -> BaseLLMEngine:
        """
        Get the primary LLM engine.

        Tries the registry first, falls back to the stored engine.

        Returns:
            Primary BaseLLMEngine instance

        Raises:
            BaseGeneratorError: If no engine is available
        """
        if self._engine is not None:
            return self._engine

        try:
            self._engine = self._get_parallel_registry().get_primary()
            return self._engine
        except EngineRegistryError as e:
            raise BaseGeneratorError(f"No primary engine available: {e}")

    # --- Configuration Accessors ---

    @property
    def parallel_mode(self) -> bool:
        """Whether parallel mode is enabled."""
        return self._config.parallel_mode

    @property
    def parallel_strategy(self) -> str:
        """Current parallel strategy name."""
        return self._parallel_strategy.value

    @property
    def model_source(self) -> str:
        """Current model source configuration."""
        return self._config.model_source

    @property
    def primary_model_name(self) -> str:
        """Name of the primary model."""
        try:
            return self._get_parallel_registry().get_primary().get_model_name()
        except EngineRegistryError:
            return self._config.model

    @property
    def secondary_model_name(self) -> Optional[str]:
        """Name of the secondary model, if available."""
        try:
            secondary = self._get_parallel_registry().get_secondary()
            return secondary.get_model_name() if secondary else None
        except EngineRegistryError:
            return None

    # --- Utility Methods ---

    def get_status(self) -> Dict[str, Any]:
        """
        Get generator status information.

        Returns:
            Dict with generator configuration and engine status
        """
        status = {
            "model_source": self._config.model_source,
            "parallel_mode": self._config.parallel_mode,
            "parallel_strategy": self._parallel_strategy.value,
            "primary_model": self.primary_model_name,
            "secondary_model": self.secondary_model_name,
        }

        try:
            registry = self._get_parallel_registry()
            status["registry"] = registry.status()
        except Exception as e:
            status["registry_error"] = str(e)

        return status

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"model_source={self._config.model_source}, "
            f"parallel_mode={self._config.parallel_mode}, "
            f"strategy={self._parallel_strategy.value})"
        )