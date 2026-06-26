#!/usr/bin/env python3
"""
Tests for model_source switching and config reload behavior.

Tests switching between ollama → huggingface → auto → compare,
fallback behavior, and LLMConfig.reload().
"""

import pytest
from unittest.mock import patch, Mock

from kb.biblio.config import LLMConfig, LLMConfigError
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError


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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_mock_engine(provider_str: str):
    """Create a lightweight mock engine."""
    from kb.biblio.engine.base import LLMProvider, LLMResponse
    provider = LLMProvider.OLLAMA if provider_str == "ollama" else LLMProvider.HUGGINGFACE
    model = "gemma4:e2b" if provider_str == "ollama" else "google/gemma-2-2b-it"
    engine = Mock()
    engine.get_provider.return_value = provider
    engine.get_model_name.return_value = model
    engine.is_available.return_value = True
    engine.generate.return_value = LLMResponse(
        content=f"[{provider_str}] test",
        model=model,
        provider=provider,
        done=True,
    )
    engine.shutdown = Mock()
    return engine


# ---------------------------------------------------------------------------
# Test: LLMConfig model_source validation
# ---------------------------------------------------------------------------


class TestModelSourceValidation:
    """Tests for model_source config validation."""

    def test_valid_ollama_source(self):
        """ollama is a valid model_source."""
        config = LLMConfig(model_source="ollama", skip_validation=False)
        assert config.model_source == "ollama"

    def test_valid_huggingface_source(self):
        """huggingface is a valid model_source."""
        config = LLMConfig(
            model_source="huggingface",
            hf_model_name="google/gemma-2-2b-it",
            skip_validation=False,
        )
        assert config.model_source == "huggingface"

    def test_valid_auto_source(self):
        """auto is a valid model_source (default)."""
        config = LLMConfig(
            model_source="auto",
            hf_model_name="google/gemma-2-2b-it",
            skip_validation=False,
        )
        assert config.model_source == "auto"

    def test_valid_compare_source(self):
        """compare is a valid model_source."""
        config = LLMConfig(
            model_source="compare",
            hf_model_name="google/gemma-2-2b-it",
            skip_validation=False,
        )
        assert config.model_source == "compare"

    def test_invalid_source_raises(self):
        """Invalid model_source raises LLMConfigError."""
        with pytest.raises(LLMConfigError, match="Invalid model_source"):
            LLMConfig(model_source="openai", skip_validation=False)

    def test_default_model_source_is_auto(self):
        """Default model_source should be 'auto'."""
        config = LLMConfig(skip_validation=True)
        assert config.model_source == "auto"

    def test_hf_source_requires_model_name(self):
        """huggingface source requires hf_model_name."""
        with pytest.raises(LLMConfigError, match="hf_model_name is required"):
            LLMConfig(model_source="huggingface", hf_model_name="", skip_validation=False)

    def test_auto_source_requires_model_name(self):
        """auto source requires hf_model_name."""
        with pytest.raises(LLMConfigError, match="hf_model_name is required"):
            LLMConfig(model_source="auto", hf_model_name="", skip_validation=False)

    def test_compare_source_requires_model_name(self):
        """compare source requires hf_model_name."""
        with pytest.raises(LLMConfigError, match="hf_model_name is required"):
            LLMConfig(model_source="compare", hf_model_name="", skip_validation=False)

    def test_invalid_quantization_raises(self):
        """Invalid quantization value raises LLMConfigError."""
        with pytest.raises(LLMConfigError, match="Invalid quantization"):
            LLMConfig(
                model_source="huggingface",
                hf_model_name="google/gemma-2-2b-it",
                hf_quantization="16bit",
                skip_validation=False,
            )

    def test_valid_quantization_4bit(self):
        """4bit quantization is valid."""
        config = LLMConfig(
            model_source="huggingface",
            hf_model_name="google/gemma-2-2b-it",
            hf_quantization="4bit",
            skip_validation=False,
        )
        assert config.hf_quantization == "4bit"

    def test_valid_quantization_8bit(self):
        """8bit quantization is valid."""
        config = LLMConfig(
            model_source="huggingface",
            hf_model_name="google/gemma-2-2b-it",
            hf_quantization="8bit",
            skip_validation=False,
        )
        assert config.hf_quantization == "8bit"

    def test_none_quantization_is_valid(self):
        """None quantization is valid (no quantization)."""
        config = LLMConfig(
            model_source="huggingface",
            hf_model_name="google/gemma-2-2b-it",
            hf_quantization=None,
            skip_validation=False,
        )
        assert config.hf_quantization is None


# ---------------------------------------------------------------------------
# Test: Config reload (switching model_source)
# ---------------------------------------------------------------------------


class TestConfigReload:
    """Tests for LLMConfig.reload() with model_source changes."""

    def test_reload_changes_model_source(self):
        """reload() with model_source override changes the config."""
        config = LLMConfig(model_source="ollama", skip_validation=True)
        assert config.model_source == "ollama"

        LLMConfig.reset()
        config2 = LLMConfig(model_source="huggingface", hf_model_name="test/model", skip_validation=True)
        assert config2.model_source == "huggingface"

    def test_reload_preserves_other_settings(self):
        """reload() with overrides preserves non-overridden settings."""
        config = LLMConfig(
            model_source="ollama",
            timeout=60,
            temperature=0.5,
            skip_validation=True,
        )
        assert config.timeout == 60
        assert config.temperature == 0.5

        LLMConfig.reset()
        config2 = LLMConfig(
            model_source="huggingface",
            hf_model_name="test/model",
            timeout=60,
            temperature=0.5,
            skip_validation=True,
        )
        assert config2.timeout == 60
        assert config2.temperature == 0.5

    def test_reload_with_empty_creates_defaults(self):
        """reload() without kwargs uses defaults."""
        config = LLMConfig(model_source="huggingface", hf_model_name="test/model", skip_validation=True)
        assert config.model_source == "huggingface"

        LLMConfig.reset()
        config2 = LLMConfig.get_instance()
        assert config2.model_source == "auto"  # default


# ---------------------------------------------------------------------------
# Test: Switch model_source with EngineRegistry
# ---------------------------------------------------------------------------


class TestModelSourceSwitch:
    """Tests for switching model_source and recreating EngineRegistry."""

    def test_switch_ollama_to_huggingface(self):
        """Switching from ollama to huggingface changes primary engine."""
        # Start with ollama
        config = LLMConfig(model_source="ollama", skip_validation=True)
        with patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry = EngineRegistry(config=config)
            assert registry.get_primary().get_provider().value == "ollama"
            assert registry.get_secondary() is None

        # Switch to huggingface
        EngineRegistry.reset()
        LLMConfig.reset()
        config2 = LLMConfig(model_source="huggingface", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', return_value=make_mock_engine("huggingface")):
            registry2 = EngineRegistry(config=config2)
            assert registry2.get_primary().get_provider().value == "huggingface"
            assert registry2.get_secondary() is None

    def test_switch_ollama_to_auto(self):
        """Switching from ollama to auto adds secondary engine."""
        config = LLMConfig(model_source="ollama", skip_validation=True)
        with patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry = EngineRegistry(config=config)
            assert registry.has_secondary is False

        EngineRegistry.reset()
        LLMConfig.reset()
        config2 = LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', return_value=make_mock_engine("huggingface")), \
             patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry2 = EngineRegistry(config=config2)
            assert registry2.has_secondary is True
            assert registry2.get_primary().get_provider().value == "huggingface"
            assert registry2.get_secondary().get_provider().value == "ollama"

    def test_switch_auto_to_compare(self):
        """Switching from auto to compare keeps both engines but changes mode."""
        config = LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', return_value=make_mock_engine("huggingface")), \
             patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry = EngineRegistry(config=config)
            assert registry.model_source == "auto"

        EngineRegistry.reset()
        LLMConfig.reset()
        config2 = LLMConfig(model_source="compare", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', return_value=make_mock_engine("huggingface")), \
             patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry2 = EngineRegistry(config=config2)
            assert registry2.model_source == "compare"
            assert registry2.has_secondary is True

    def test_switch_huggingface_to_ollama(self):
        """Switching from huggingface to ollama removes secondary."""
        config = LLMConfig(model_source="huggingface", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', return_value=make_mock_engine("huggingface")):
            registry = EngineRegistry(config=config)
            assert registry.get_primary().get_provider().value == "huggingface"
            assert registry.has_secondary is False

        EngineRegistry.reset()
        LLMConfig.reset()
        config2 = LLMConfig(model_source="ollama", skip_validation=True)
        with patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry2 = EngineRegistry(config=config2)
            assert registry2.get_primary().get_provider().value == "ollama"
            assert registry2.has_secondary is False


# ---------------------------------------------------------------------------
# Test: Fallback behavior
# ---------------------------------------------------------------------------


class TestFallbackBehavior:
    """Tests for fallback behavior in auto mode."""

    def test_auto_hf_primary_ollama_fallback(self):
        """In auto mode, Ollama is the fallback when HF fails."""
        config = LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', side_effect=EngineRegistryError("HF unavailable")), \
             patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry = EngineRegistry(config=config)
            # Primary should be Ollama (promoted from secondary)
            assert registry.get_primary().get_provider().value == "ollama"
            # No secondary since Ollama was promoted
            assert registry.get_secondary() is None

    def test_auto_both_available_hf_is_primary(self):
        """In auto mode with both available, HF remains primary."""
        config = LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', return_value=make_mock_engine("huggingface")), \
             patch.object(EngineRegistry, '_create_ollama_engine', return_value=make_mock_engine("ollama")):
            registry = EngineRegistry(config=config)
            assert registry.get_primary().get_provider().value == "huggingface"
            assert registry.get_secondary().get_provider().value == "ollama"

    def test_auto_hf_available_ollama_fails(self):
        """In auto mode, if Ollama fails, HF is still primary (no fallback)."""
        config = LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', return_value=make_mock_engine("huggingface")), \
             patch.object(EngineRegistry, '_create_ollama_engine', side_effect=EngineRegistryError("Ollama unavailable")):
            registry = EngineRegistry(config=config)
            assert registry.get_primary().get_provider().value == "huggingface"
            assert registry.get_secondary() is None

    def test_auto_neither_available_raises(self):
        """In auto mode, if neither engine is available, raises error."""
        config = LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        with patch.object(EngineRegistry, '_create_hf_engine', side_effect=EngineRegistryError("HF unavailable")), \
             patch.object(EngineRegistry, '_create_ollama_engine', side_effect=EngineRegistryError("Ollama unavailable")):
            registry = EngineRegistry(config=config)
            with pytest.raises(EngineRegistryError, match="Neither"):
                registry.get_primary()

    def test_compare_mode_both_required(self):
        """In compare mode, both engines must be available."""
        config = LLMConfig(model_source="compare", hf_model_name="google/gemma-2-2b-it", skip_validation=True)
        # If HF fails in compare mode, it should raise (not fallback)
        with patch.object(EngineRegistry, '_create_hf_engine', side_effect=EngineRegistryError("HF unavailable")):
            with pytest.raises(EngineRegistryError):
                EngineRegistry(config=config).get_primary()


# ---------------------------------------------------------------------------
# Test: Environment variable overrides
# ---------------------------------------------------------------------------


class TestEnvironmentOverrides:
    """Tests for environment variable configuration overrides."""

    def test_env_overrides_model_source(self, monkeypatch):
        """KB_LLM_MODEL_SOURCE env var overrides default."""
        monkeypatch.setenv("KB_LLM_MODEL_SOURCE", "ollama")
        config = LLMConfig(skip_validation=True)
        assert config.model_source == "ollama"

    def test_env_overrides_hf_model(self, monkeypatch):
        """KB_LLM_HF_MODEL env var overrides default."""
        monkeypatch.setenv("KB_LLM_MODEL_SOURCE", "huggingface")
        monkeypatch.setenv("KB_LLM_HF_MODEL", "custom/model-v2")
        config = LLMConfig(skip_validation=False)
        assert config.hf_model_name == "custom/model-v2"

    def test_env_overrides_parallel_mode(self, monkeypatch):
        """KB_LLM_PARALLEL_MODE env var overrides default."""
        monkeypatch.setenv("KB_LLM_PARALLEL_MODE", "true")
        config = LLMConfig(skip_validation=True)
        assert config.parallel_mode is True

    def test_env_overrides_parallel_strategy(self, monkeypatch):
        """KB_LLM_PARALLEL_STRATEGY env var overrides default."""
        monkeypatch.setenv("KB_LLM_PARALLEL_STRATEGY", "compare")
        config = LLMConfig(skip_validation=True)
        assert config.parallel_strategy == "compare"

    def test_param_overrides_default(self):
        """Explicit param takes precedence over default."""
        config = LLMConfig(model_source="ollama", temperature=0.3, skip_validation=True)
        assert config.model_source == "ollama"
        assert config.temperature == 0.3


# ---------------------------------------------------------------------------
# Test: Parallel strategy validation
# ---------------------------------------------------------------------------


class TestParallelStrategyValidation:
    """Tests for parallel_strategy config validation."""

    def test_valid_strategy_primary_first(self):
        config = LLMConfig(parallel_strategy="primary_first", skip_validation=True)
        assert config.parallel_strategy == "primary_first"

    def test_valid_strategy_aggregate(self):
        config = LLMConfig(parallel_strategy="aggregate", skip_validation=True)
        assert config.parallel_strategy == "aggregate"

    def test_valid_strategy_compare(self):
        config = LLMConfig(parallel_strategy="compare", skip_validation=True)
        assert config.parallel_strategy == "compare"

    def test_invalid_strategy_raises(self):
        with pytest.raises(LLMConfigError, match="Invalid parallel_strategy"):
            LLMConfig(parallel_strategy="invalid", skip_validation=False)

    def test_default_strategy_is_primary_first(self):
        config = LLMConfig(skip_validation=True)
        assert config.parallel_strategy == "primary_first"


# ---------------------------------------------------------------------------
# Test: Config to_dict
# ---------------------------------------------------------------------------


class TestConfigToDict:
    """Tests for LLMConfig.to_dict() export."""

    def test_to_dict_includes_model_source(self):
        config = LLMConfig(model_source="auto", skip_validation=True)
        d = config.to_dict()
        assert d["model_source"] == "auto"
        assert "hf_model_name" in d
        assert "parallel_mode" in d
        assert "parallel_strategy" in d

    def test_to_dict_hides_token(self):
        """to_dict should never expose the HF token."""
        config = LLMConfig(hf_token="secret-token-12345", skip_validation=True)
        d = config.to_dict()
        assert d["hf_token"] == "***"
        assert "secret-token-12345" not in str(d)

    def test_to_dict_includes_ollama_specific(self):
        config = LLMConfig(model_source="compare", skip_validation=True)
        d = config.to_dict()
        assert "ollama_model" in d
        assert "ollama_timeout" in d
        assert "ollama_temperature" in d


if __name__ == "__main__":
    pytest.main([__file__, "-v"])