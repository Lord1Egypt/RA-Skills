#!/usr/bin/env python3
"""
Tests for EngineRegistry - Singleton registry for LLM engine instances.

Tests engine creation, retrieval, fallback, and reset behavior
for all model_source modes: ollama, huggingface, auto, compare.

Uses EngineFactory injection for testability instead of
patching private methods.
"""

import pytest
import threading
from unittest.mock import Mock, MagicMock

from kb.biblio.config import LLMConfig
from kb.biblio.engine.base import LLMProvider, LLMResponse
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError, get_engine_registry
from kb.biblio.engine.factory import EngineFactory, DefaultEngineFactory


# ---------------------------------------------------------------------------
# Helpers: Lightweight mock engines and mock factory
# ---------------------------------------------------------------------------


def make_mock_engine(provider: LLMProvider, model_name: str, available: bool = True):
    """Create a mock engine that satisfies the BaseLLMEngine interface."""
    engine = Mock()
    engine.get_provider.return_value = provider
    engine.get_model_name.return_value = model_name
    engine.is_available.return_value = available
    engine.generate.return_value = LLMResponse(
        content=f"[{provider.value}] test",
        model=model_name,
        provider=provider,
        done=True,
    )
    engine.shutdown = Mock()
    return engine


def mock_ollama(available: bool = True):
    return make_mock_engine(LLMProvider.OLLAMA, "gemma4:e2b", available)


def mock_hf(available: bool = True):
    return make_mock_engine(LLMProvider.HUGGINGFACE, "google/gemma-2-2b-it", available)


class MockEngineFactory:
    """Test factory that returns mock engines.

    Supports per-call customization: set .ollama_engine or .hf_engine
    before creating a registry to control what gets injected.
    """

    def __init__(self, ollama_engine=None, hf_engine=None,
                 ollama_side_effect=None, hf_side_effect=None):
        self._ollama_engine = ollama_engine
        self._hf_engine = hf_engine
        self._ollama_side_effect = ollama_side_effect
        self._hf_side_effect = hf_side_effect

    def create_ollama_engine(self, config):
        if self._ollama_side_effect:
            raise self._ollama_side_effect
        return self._ollama_engine or mock_ollama()

    def create_hf_engine(self, config):
        if self._hf_side_effect:
            raise self._hf_side_effect
        return self._hf_engine or mock_hf()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset all singletons before and after each test."""
    EngineRegistry.reset()
    LLMConfig.reset()
    yield
    EngineRegistry.reset()
    LLMConfig.reset()


@pytest.fixture
def ollama_config():
    return LLMConfig(model_source="ollama", skip_validation=True)


@pytest.fixture
def hf_config():
    return LLMConfig(model_source="huggingface", hf_model_name="google/gemma-2-2b-it", skip_validation=True)


@pytest.fixture
def auto_config():
    return LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it", skip_validation=True)


@pytest.fixture
def compare_config():
    return LLMConfig(model_source="compare", hf_model_name="google/gemma-2-2b-it", skip_validation=True)


# ---------------------------------------------------------------------------
# Test: EngineFactory Protocol
# ---------------------------------------------------------------------------


class TestEngineFactoryProtocol:
    """Tests for EngineFactory protocol and DefaultEngineFactory."""

    def test_mock_factory_satisfies_protocol(self):
        """MockEngineFactory satisfies EngineFactory protocol."""
        factory = MockEngineFactory()
        assert isinstance(factory, EngineFactory)

    def test_default_factory_satisfies_protocol(self):
        """DefaultEngineFactory satisfies EngineFactory protocol."""
        factory = DefaultEngineFactory()
        assert isinstance(factory, EngineFactory)

    def test_registry_accepts_factory(self, ollama_config):
        """EngineRegistry accepts engine_factory parameter."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        assert registry._engine_factory is factory

    def test_registry_defaults_to_default_factory(self, ollama_config):
        """EngineRegistry uses DefaultEngineFactory when none provided."""
        registry = EngineRegistry(config=ollama_config)
        assert isinstance(registry._engine_factory, DefaultEngineFactory)


# ---------------------------------------------------------------------------
# Test: Singleton Pattern
# ---------------------------------------------------------------------------


class TestEngineRegistrySingleton:
    """Tests for EngineRegistry singleton behavior."""

    def test_get_instance_creates_singleton(self, ollama_config):
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        assert isinstance(registry, EngineRegistry)

    def test_get_instance_returns_same_instance(self, ollama_config):
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        r1 = EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        r2 = EngineRegistry.get_instance()
        assert r1 is r2

    def test_constructor_raises_if_instance_exists(self, ollama_config):
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        with pytest.raises(EngineRegistryError, match="Use EngineRegistry.get_instance"):
            EngineRegistry(config=ollama_config, engine_factory=factory)

    def test_reset_clears_singleton(self, ollama_config):
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        r1 = EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        EngineRegistry.reset()
        r2 = EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        assert r1 is not r2

    def test_thread_safety_of_get_instance(self, ollama_config):
        """Two threads racing to create instance should get the same one."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        results = []

        def create_registry():
            r = EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
            results.append(r)

        threads = [threading.Thread(target=create_registry) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All threads should have gotten the same instance
        assert all(r is results[0] for r in results)


# ---------------------------------------------------------------------------
# Test: Engine Creation per model_source
# ---------------------------------------------------------------------------


class TestEngineRegistryCreation:
    """Tests for engine creation based on model_source."""

    def test_ollama_mode_creates_ollama_primary(self, ollama_config):
        """In ollama mode, primary is OllamaEngine."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        primary = registry.get_primary()
        assert primary.get_provider() == LLMProvider.OLLAMA
        assert registry.get_secondary() is None

    def test_huggingface_mode_creates_hf_primary(self, hf_config):
        """In huggingface mode, primary is TransformersEngine."""
        factory = MockEngineFactory(hf_engine=mock_hf())
        registry = EngineRegistry(config=hf_config, engine_factory=factory)
        primary = registry.get_primary()
        assert primary.get_provider() == LLMProvider.HUGGINGFACE
        assert registry.get_secondary() is None

    def test_auto_mode_creates_hf_primary_ollama_secondary(self, auto_config):
        """In auto mode: HF primary, Ollama secondary."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        assert registry.get_primary().get_provider() == LLMProvider.HUGGINGFACE
        assert registry.get_secondary().get_provider() == LLMProvider.OLLAMA

    def test_compare_mode_creates_both_engines(self, compare_config):
        """In compare mode: both HF and Ollama engines are created."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=compare_config, engine_factory=factory)
        assert registry.get_primary().get_provider() == LLMProvider.HUGGINGFACE
        assert registry.get_secondary().get_provider() == LLMProvider.OLLAMA
        assert registry.has_secondary is True


# ---------------------------------------------------------------------------
# Test: get_engine(), get_primary(), get_secondary()
# ---------------------------------------------------------------------------


class TestEngineRegistryAccess:
    """Tests for engine access methods."""

    def test_get_engine_returns_primary_by_default(self, ollama_config):
        """get_engine() without source returns primary."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        engine = registry.get_engine()
        assert engine is registry.get_primary()

    def test_get_engine_by_source_ollama(self, ollama_config):
        """get_engine('ollama') returns the Ollama engine."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        engine = registry.get_engine("ollama")
        assert engine.get_provider() == LLMProvider.OLLAMA

    def test_get_engine_by_source_huggingface(self, auto_config):
        """get_engine('huggingface') returns the HF engine in auto mode."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        hf_engine = registry.get_engine("huggingface")
        assert hf_engine.get_provider() == LLMProvider.HUGGINGFACE
        ollama_engine = registry.get_engine("ollama")
        assert ollama_engine.get_provider() == LLMProvider.OLLAMA

    def test_get_engine_unknown_source_raises(self, ollama_config):
        """get_engine('unknown') raises EngineRegistryError."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        with pytest.raises(EngineRegistryError, match="Unknown source"):
            registry.get_engine("openai")

    def test_get_engine_unavailable_source_raises(self, ollama_config):
        """get_engine('huggingface') in ollama-only mode raises error."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        with pytest.raises(EngineRegistryError, match="not available"):
            registry.get_engine("huggingface")

    def test_get_primary_raises_when_no_engine(self):
        """get_primary() raises when no engines are available."""
        config = LLMConfig(model_source="auto", skip_validation=True)
        factory = MockEngineFactory(
            hf_side_effect=EngineRegistryError("HF unavailable"),
            ollama_side_effect=EngineRegistryError("Ollama unavailable"),
        )
        registry = EngineRegistry(config=config, engine_factory=factory)
        with pytest.raises(EngineRegistryError, match="Neither"):
            registry.get_primary()

    def test_get_secondary_none_in_single_source(self, ollama_config):
        """get_secondary() returns None in single-source mode."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        assert registry.get_secondary() is None

    def test_get_both_returns_tuple(self, auto_config):
        """get_both() returns (primary, secondary) tuple."""
        hf = mock_hf()
        ollama = mock_ollama()
        factory = MockEngineFactory(hf_engine=hf, ollama_engine=ollama)
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        primary, secondary = registry.get_both()
        assert primary.get_provider() == LLMProvider.HUGGINGFACE
        assert secondary.get_provider() == LLMProvider.OLLAMA

    def test_get_both_secondary_none_in_single_mode(self, ollama_config):
        """get_both() returns (primary, None) in single-source mode."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        primary, secondary = registry.get_both()
        assert primary.get_provider() == LLMProvider.OLLAMA
        assert secondary is None


# ---------------------------------------------------------------------------
# Test: is_engine_available()
# ---------------------------------------------------------------------------


class TestEngineRegistryAvailability:
    """Tests for is_engine_available() health checks."""

    def test_available_engine_returns_true(self, ollama_config):
        """is_engine_available returns True for healthy engine."""
        factory = MockEngineFactory(ollama_engine=mock_ollama(available=True))
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        assert registry.is_engine_available("ollama") is True

    def test_unavailable_engine_returns_false(self, ollama_config):
        """is_engine_available returns False for unhealthy engine."""
        factory = MockEngineFactory(ollama_engine=mock_ollama(available=False))
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        assert registry.is_engine_available("ollama") is False

    def test_missing_source_returns_false(self, ollama_config):
        """is_engine_available returns False for non-existent source in this mode."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        assert registry.is_engine_available("huggingface") is False

    def test_both_sources_available_in_auto(self, auto_config):
        """In auto mode, both sources are available."""
        factory = MockEngineFactory(hf_engine=mock_hf(available=True), ollama_engine=mock_ollama(available=True))
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        assert registry.is_engine_available("huggingface") is True
        assert registry.is_engine_available("ollama") is True


# ---------------------------------------------------------------------------
# Test: reset()
# ---------------------------------------------------------------------------


class TestEngineRegistryReset:
    """Tests for reset() behavior."""

    def test_reset_clears_singleton(self, ollama_config):
        """reset() clears the singleton so next get_instance creates new."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        r1 = EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        EngineRegistry.reset()
        r2 = EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        assert r1 is not r2

    def test_reset_calls_shutdown_on_engines(self, auto_config):
        """reset() calls shutdown() on cached engines."""
        hf = mock_hf()
        ollama = mock_ollama()
        factory = MockEngineFactory(hf_engine=hf, ollama_engine=ollama)
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        # Trigger initialization
        _ = registry.get_primary()
        _ = registry.get_secondary()

        EngineRegistry.reset()

        # Verify shutdown was called on both
        hf.shutdown.assert_called_once()
        ollama.shutdown.assert_called_once()

    def test_reset_handles_shutdown_error_gracefully(self, ollama_config):
        """reset() should not raise even if engine.shutdown() fails."""
        engine = mock_ollama()
        engine.shutdown.side_effect = RuntimeError("shutdown failed")
        factory = MockEngineFactory(ollama_engine=engine)
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        _ = registry.get_primary()
        # Should not raise
        EngineRegistry.reset()

    def test_reset_allows_recreation(self, auto_config):
        """After reset, a new registry can be created with different config."""
        factory1 = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry1 = EngineRegistry(config=auto_config, engine_factory=factory1)
        assert registry1.model_source == "auto"

        EngineRegistry.reset()
        LLMConfig.reset()

        # Create fresh config after LLMConfig reset
        new_config = LLMConfig(model_source="ollama", skip_validation=True)
        factory2 = MockEngineFactory(ollama_engine=mock_ollama())
        registry2 = EngineRegistry(config=new_config, engine_factory=factory2)
        assert registry2.model_source == "ollama"


# ---------------------------------------------------------------------------
# Test: Auto Mode Fallback
# ---------------------------------------------------------------------------


class TestAutoModeFallback:
    """Tests for auto mode fallback behavior."""

    def test_auto_falls_back_to_ollama_when_hf_fails(self, auto_config):
        """In auto mode, if HF creation fails, Ollama becomes primary."""
        factory = MockEngineFactory(
            hf_side_effect=EngineRegistryError("HF unavailable"),
            ollama_engine=mock_ollama(),
        )
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        primary = registry.get_primary()
        assert primary.get_provider() == LLMProvider.OLLAMA
        assert registry.get_secondary() is None

    def test_auto_raises_if_both_fail(self, auto_config):
        """In auto mode, raise error if both engines fail."""
        factory = MockEngineFactory(
            hf_side_effect=EngineRegistryError("HF unavailable"),
            ollama_side_effect=EngineRegistryError("Ollama unavailable"),
        )
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        with pytest.raises(EngineRegistryError, match="Neither"):
            registry.get_primary()

    def test_auto_hf_primary_ollama_secondary(self, auto_config):
        """In auto mode with both available, HF is primary, Ollama is secondary."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        assert registry.get_primary().get_provider() == LLMProvider.HUGGINGFACE
        assert registry.get_secondary().get_provider() == LLMProvider.OLLAMA
        assert registry.has_secondary is True

    def test_auto_hf_still_primary_when_ollama_fails(self, auto_config):
        """In auto mode, if Ollama fails, HF is still primary."""
        factory = MockEngineFactory(
            hf_engine=mock_hf(),
            ollama_side_effect=EngineRegistryError("Ollama unavailable"),
        )
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        assert registry.get_primary().get_provider() == LLMProvider.HUGGINGFACE
        assert registry.get_secondary() is None
        assert registry.has_secondary is False


# ---------------------------------------------------------------------------
# Test: Properties
# ---------------------------------------------------------------------------


class TestEngineRegistryProperties:
    """Tests for registry properties."""

    def test_model_source_property(self, auto_config):
        """model_source property returns config value."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        assert registry.model_source == "auto"

    def test_primary_provider_property(self, auto_config):
        """primary_provider returns the provider enum value."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        assert registry.primary_provider == LLMProvider.HUGGINGFACE

    def test_has_secondary_false_in_single_source(self, ollama_config):
        """has_secondary is False in single-source mode."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        assert registry.has_secondary is False

    def test_has_secondary_true_in_auto(self, auto_config):
        """has_secondary is True in auto mode."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        assert registry.has_secondary is True


# ---------------------------------------------------------------------------
# Test: status()
# ---------------------------------------------------------------------------


class TestEngineRegistryStatus:
    """Tests for status() summary method."""

    def test_status_auto_mode(self, auto_config):
        """status() returns correct info for auto mode."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=auto_config, engine_factory=factory)
        status = registry.status()

        assert status["model_source"] == "auto"
        assert status["primary"] is not None
        assert status["primary"]["provider"] == "huggingface"
        assert status["primary"]["available"] is True
        assert status["secondary"] is not None
        assert status["secondary"]["provider"] == "ollama"
        assert status["secondary"]["available"] is True

    def test_status_ollama_mode(self, ollama_config):
        """status() returns correct info for ollama mode."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        status = registry.status()

        assert status["model_source"] == "ollama"
        assert status["primary"]["provider"] == "ollama"
        assert status["secondary"] is None

    def test_status_compare_mode(self, compare_config):
        """status() returns correct info for compare mode."""
        factory = MockEngineFactory(hf_engine=mock_hf(), ollama_engine=mock_ollama())
        registry = EngineRegistry(config=compare_config, engine_factory=factory)
        status = registry.status()

        assert status["model_source"] == "compare"
        assert status["primary"]["provider"] == "huggingface"
        assert status["secondary"]["provider"] == "ollama"


# ---------------------------------------------------------------------------
# Test: Invalid model_source
# ---------------------------------------------------------------------------


class TestEngineRegistryInvalidSource:
    """Tests for invalid model_source values."""

    def test_unknown_model_source_raises(self):
        """Unknown model_source should raise EngineRegistryError."""
        config = LLMConfig(model_source="invalid_source", skip_validation=True)
        factory = MockEngineFactory()
        registry = EngineRegistry(config=config, engine_factory=factory)
        with pytest.raises(EngineRegistryError, match="Unknown model_source"):
            registry.get_primary()


# ---------------------------------------------------------------------------
# Test: get_engine_registry() convenience function
# ---------------------------------------------------------------------------


class TestGetEngineRegistry:
    """Tests for the module-level convenience function."""

    def test_get_engine_registry_returns_instance(self):
        """get_engine_registry() returns EngineRegistry instance."""
        registry = get_engine_registry()
        assert isinstance(registry, EngineRegistry)

    def test_get_engine_registry_singleton(self, ollama_config):
        """get_engine_registry() returns same instance as get_instance()."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        EngineRegistry.get_instance(config=ollama_config, engine_factory=factory)
        registry = get_engine_registry()
        assert registry is EngineRegistry.get_instance()


# ---------------------------------------------------------------------------
# Test: repr()
# ---------------------------------------------------------------------------


class TestEngineRegistryRepr:
    """Tests for __repr__."""

    def test_repr_contains_model_source(self, ollama_config):
        """__repr__ includes model_source."""
        factory = MockEngineFactory(ollama_engine=mock_ollama())
        registry = EngineRegistry(config=ollama_config, engine_factory=factory)
        # Trigger initialization so engines dict is populated
        registry.get_primary()
        r = repr(registry)
        assert "ollama" in r
        assert "primary" in r


if __name__ == "__main__":
    pytest.main([__file__, "-v"])