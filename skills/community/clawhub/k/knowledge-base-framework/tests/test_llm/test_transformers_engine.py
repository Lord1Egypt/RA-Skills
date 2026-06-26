#!/usr/bin/env python3
"""
Tests for TransformersEngine - HuggingFace Transformers LLM Integration

All tests use mocks — no real models are loaded.
Runs: python3 -m pytest tests/test_llm/test_transformers_engine.py -v
"""

import asyncio
import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from types import ModuleType

from kb.biblio.config import LLMConfig, LLMConfigError
from kb.biblio.engine.base import LLMProvider, LLMResponse, LLMStreamChunk
from kb.biblio.engine.transformers_engine import (
    TransformersEngine,
    TransformersEngineError,
    TransformersModelLoadError,
    TransformersGenerationError,
)


# ======================================================================
# Helper: set engine to "loaded" state
# ======================================================================

def _setup_loaded_engine(engine, device_type="cpu"):
    """Put engine into loaded state with mock model/tokenizer."""
    engine._model_loaded = True
    engine._model = MagicMock()
    engine._tokenizer = MagicMock()
    engine._device = MagicMock()
    engine._device.type = device_type


# ======================================================================
# Test 1: Initialization
# ======================================================================

class TestTransformersEngineInit:
    """TransformersEngine instantiation and basic properties."""

    def test_init(self, transformers_engine):
        """TransformersEngine instanziiert korrekt."""
        assert transformers_engine is not None
        assert transformers_engine._model is None
        assert transformers_engine._tokenizer is None
        assert transformers_engine._model_loaded is False
        assert transformers_engine._executor is None
        assert transformers_engine._load_lock is not None


# ======================================================================
# Test 2-3: Availability
# ======================================================================

class TestTransformersEngineAvailability:
    """is_available() with and without torch/transformers."""

    def test_is_available_true(self, transformers_engine):
        """torch+transformers installiert → is_available() True."""
        mock_torch = MagicMock()
        mock_transformers = MagicMock()
        with patch.dict("sys.modules", {
            "torch": mock_torch,
            "transformers": mock_transformers,
        }):
            assert transformers_engine.is_available() is True

    def test_is_available_false(self, transformers_engine):
        """torch fehlt → is_available() False."""
        with patch.dict("sys.modules", {"torch": None, "transformers": MagicMock()}):
            assert transformers_engine.is_available() is False


# ======================================================================
# Test 4-5: Model name and provider
# ======================================================================

class TestTransformersEngineIdentity:
    """get_model_name() and get_provider()."""

    def test_get_model_name(self, transformers_engine, hf_config):
        """Config-Name wird zurueckgegeben."""
        assert transformers_engine.get_model_name() == hf_config.hf_model_name

    def test_get_provider(self, transformers_engine):
        """Provider ist HUGGINGFACE."""
        assert transformers_engine.get_provider() == LLMProvider.HUGGINGFACE


# ======================================================================
# Test 6-9: Model loading and unloading
# ======================================================================

class TestTransformersEngineLoading:
    """Model load, reload, OOM fallback, and unload."""

    def test_load_model_success(self, transformers_engine, mock_torch, mock_transformers):
        """Modell laedt erfolgreich mit Mock-Dependencies."""
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_tokenizer.pad_token = "<pad>"
        mock_transformers.AutoModelForCausalLM.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.is_bf16_supported.return_value = False
        mock_torch.float16 = "float16"
        mock_torch.float32 = "float32"
        mock_torch.device.return_value = MagicMock(type="cuda")

        with patch.dict("sys.modules", {
            "torch": mock_torch,
            "transformers": mock_transformers,
        }):
            transformers_engine.load_model()
            assert transformers_engine._model_loaded is True
            assert transformers_engine._model is not None
            assert transformers_engine._tokenizer is not None

    def test_load_model_already_loaded(self, transformers_engine, mock_torch, mock_transformers):
        """Zweimal load_model() ist idempotent — laedt nicht doppelt."""
        transformers_engine._model_loaded = True
        transformers_engine._model = MagicMock()
        transformers_engine._tokenizer = MagicMock()

        with patch.dict("sys.modules", {
            "torch": mock_torch,
            "transformers": mock_transformers,
        }):
            transformers_engine.load_model()
            # from_pretrained should NOT be called again
            mock_transformers.AutoModelForCausalLM.from_pretrained.assert_not_called()

    def test_load_model_oom_fallback(self, transformers_engine, mock_torch, mock_transformers):
        """GPU OOM → CPU Fallback funktioniert."""
        mock_model_cpu = MagicMock()
        mock_tokenizer = MagicMock()
        mock_tokenizer.pad_token = "<pad>"
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.is_bf16_supported.return_value = False
        mock_torch.float16 = "float16"
        mock_torch.float32 = "float32"

        OOMError = type("OutOfMemoryError", (RuntimeError,), {})
        mock_torch.cuda.OutOfMemoryError = OOMError
        mock_torch.device.return_value = MagicMock(type="cpu")

        # First call OOMs, second call (CPU fallback) succeeds
        mock_transformers.AutoModelForCausalLM.from_pretrained.side_effect = [
            OOMError("OOM"),
            mock_model_cpu,
        ]
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer

        with patch.dict("sys.modules", {
            "torch": mock_torch,
            "transformers": mock_transformers,
        }):
            transformers_engine.load_model()
            assert transformers_engine._model_loaded is True

    def test_unload_model(self, transformers_engine, mock_torch):
        """unload_model() gibt Speicher frei."""
        transformers_engine._model = MagicMock()
        transformers_engine._tokenizer = MagicMock()
        transformers_engine._model_loaded = True
        mock_torch.cuda.is_available.return_value = True

        with patch.dict("sys.modules", {"torch": mock_torch}):
            transformers_engine.unload_model()

        assert transformers_engine._model is None
        assert transformers_engine._tokenizer is None
        assert transformers_engine._model_loaded is False
        mock_torch.cuda.empty_cache.assert_called()


# ======================================================================
# Test 10-13: Generation (sync, lazy-load, OOM, async)
# ======================================================================

class TestTransformersEngineGeneration:
    """generate(), lazy-load, OOM handling, and async."""

    def test_generate_success(self, transformers_engine, mock_torch, mock_transformers):
        """Synchrone Generierung liefert LLMResponse."""
        _setup_loaded_engine(transformers_engine)

        # Mock tokenizer encode + decode
        mock_input_ids = MagicMock()
        mock_input_ids.shape = [1, 5]
        transformers_engine._tokenizer.return_value = {"input_ids": mock_input_ids}
        transformers_engine._tokenizer.decode.return_value = "Hello world"

        # Mock model.generate output
        mock_output = MagicMock()
        mock_output.__getitem__ = Mock(
            return_value=MagicMock(__getitem__=Mock(return_value=MagicMock()))
        )
        transformers_engine._model.generate.return_value = mock_output

        with patch.dict("sys.modules", {"torch": mock_torch}):
            response = transformers_engine.generate("Test prompt")

        assert isinstance(response, LLMResponse)
        assert response.provider == LLMProvider.HUGGINGFACE
        assert response.done is True

    def test_generate_lazy_load(self, transformers_engine, mock_torch, mock_transformers):
        """generate() loest lazy-load aus wenn Modell nicht geladen."""
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_tokenizer.pad_token = "<pad>"
        mock_torch.cuda.is_available.return_value = False
        mock_torch.float32 = "float32"
        mock_torch.device.return_value = MagicMock(type="cpu")

        mock_transformers.AutoModelForCausalLM.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = mock_tokenizer

        with patch.dict("sys.modules", {
            "torch": mock_torch,
            "transformers": mock_transformers,
        }):
            assert transformers_engine._model_loaded is False
            transformers_engine._ensure_model_loaded()
            assert transformers_engine._model_loaded is True

    def test_generate_oom(self, transformers_engine, mock_torch, mock_transformers):
        """GPU OOM waehrend Generation → TransformersGenerationError."""
        _setup_loaded_engine(transformers_engine, device_type="cuda")

        OOMError = type("OutOfMemoryError", (RuntimeError,), {})
        mock_torch.cuda.OutOfMemoryError = OOMError
        transformers_engine._model.generate.side_effect = OOMError("OOM")

        with patch.dict("sys.modules", {"torch": mock_torch}):
            with pytest.raises(TransformersGenerationError):
                transformers_engine.generate("Test prompt")

    def test_generate_async(self, transformers_engine, mock_torch, mock_transformers):
        """Async generation via ThreadPoolExecutor."""
        _setup_loaded_engine(transformers_engine)

        mock_input_ids = MagicMock()
        mock_input_ids.shape = [1, 3]
        transformers_engine._tokenizer.return_value = {"input_ids": mock_input_ids}
        transformers_engine._tokenizer.decode.return_value = "Async response"

        mock_output = MagicMock()
        transformers_engine._model.generate.return_value = mock_output

        loop = asyncio.new_event_loop()
        try:
            response = loop.run_until_complete(
                transformers_engine.generate_async("Test prompt")
            )
            assert isinstance(response, LLMResponse)
            assert response.content == "Async response"
        finally:
            loop.close()


# ======================================================================
# Test 14-15: Streaming
# ======================================================================

class TestTransformersEngineStreaming:
    """Streaming generation (sync and async)."""

    def test_generate_stream(self, transformers_engine, mock_torch, mock_transformers):
        """Streaming Generator liefert LLMStreamChunk-Objekte."""
        _setup_loaded_engine(transformers_engine)

        mock_input_ids = MagicMock()
        mock_input_ids.shape = [1, 3]
        transformers_engine._tokenizer.return_value = {"input_ids": mock_input_ids}

        # Mock TextIteratorStreamer
        mock_streamer = MagicMock()
        mock_streamer.__iter__ = Mock(return_value=iter(["Hello", " world"]))
        mock_transformers.TextIteratorStreamer.return_value = mock_streamer

        # Patch threading.Thread (used inside generate_stream)
        import threading
        original_thread = threading.Thread
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = False
        mock_thread.start = MagicMock()
        mock_thread.join = MagicMock()

        with patch.object(threading, "Thread", return_value=mock_thread):
            with patch.dict("sys.modules", {
                "torch": mock_torch,
                "transformers": mock_transformers,
            }):
                chunks = list(transformers_engine.generate_stream("Test prompt"))

        # At least the final done=True chunk
        assert len(chunks) >= 1
        assert any(c.done is True for c in chunks)

    def test_generate_stream_async(self, transformers_engine):
        """Async streaming Methode existiert und liefert async generator."""
        # generate_stream_async is an async generator, not a regular coroutine
        import inspect
        assert inspect.isasyncgenfunction(transformers_engine.generate_stream_async)
        assert transformers_engine.supports_streaming is True


# ======================================================================
# Test 16-17: Batch processing
# ======================================================================

class TestTransformersEngineBatch:
    """Batch generation (sync and async)."""

    def test_generate_batch(self, transformers_engine, mock_torch, mock_transformers):
        """Batch processing mehrerer Prompts."""
        _setup_loaded_engine(transformers_engine)

        mock_input_ids = MagicMock()
        mock_input_ids.shape = [1, 3]
        transformers_engine._tokenizer.return_value = {"input_ids": mock_input_ids}
        transformers_engine._tokenizer.decode.return_value = "Batch response"

        mock_output = MagicMock()
        transformers_engine._model.generate.return_value = mock_output

        progress_calls = []

        def on_progress(completed, total):
            progress_calls.append((completed, total))

        results = transformers_engine.generate_batch(
            ["Prompt 1", "Prompt 2", "Prompt 3"],
            on_progress=on_progress,
        )

        assert len(results) == 3
        assert all(isinstance(r, LLMResponse) for r in results)
        assert len(progress_calls) == 3
        assert progress_calls[-1] == (3, 3)

    def test_generate_batch_async(self, transformers_engine, mock_torch, mock_transformers):
        """Async batch processing via ThreadPoolExecutor."""
        _setup_loaded_engine(transformers_engine)

        mock_input_ids = MagicMock()
        mock_input_ids.shape = [1, 3]
        transformers_engine._tokenizer.return_value = {"input_ids": mock_input_ids}
        transformers_engine._tokenizer.decode.return_value = "Async batch"

        mock_output = MagicMock()
        transformers_engine._model.generate.return_value = mock_output

        loop = asyncio.new_event_loop()
        try:
            results = loop.run_until_complete(
                transformers_engine.generate_batch_async(["A", "B"])
            )
            assert len(results) == 2
            assert all(isinstance(r, LLMResponse) for r in results)
        finally:
            loop.close()


# ======================================================================
# Test 18: Chat template
# ======================================================================

class TestTransformersEngineChatTemplate:
    """apply_chat_template() message formatting."""

    def test_apply_chat_template(self, transformers_engine, mock_torch, mock_transformers):
        """Chat template formatiert Messages korrekt."""
        _setup_loaded_engine(transformers_engine)

        messages = [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"},
        ]

        # Tokenizer has native apply_chat_template
        transformers_engine._tokenizer.apply_chat_template = Mock(
            return_value="<|user|>\nHello!\n<|assistant|>\nHi there!"
        )

        result = transformers_engine.apply_chat_template(messages)
        assert "Hello!" in result
        transformers_engine._tokenizer.apply_chat_template.assert_called_once()

    def test_apply_chat_template_fallback(self, transformers_engine):
        """Fallback-Formatierung wenn tokenizer kein Template hat."""
        _setup_loaded_engine(transformers_engine)

        # Tokenizer without apply_chat_template
        del transformers_engine._tokenizer.apply_chat_template

        messages = [{"role": "user", "content": "Hello!"}]
        result = transformers_engine.apply_chat_template(messages)
        assert "user" in result
        assert "Hello!" in result


# ======================================================================
# Test 19: GPU stats
# ======================================================================

class TestTransformersEngineGPUStats:
    """get_gpu_stats() with mocked CUDA."""

    def test_get_gpu_stats(self, transformers_engine, mock_torch):
        """GPU info wird zurueckgegeben (Mock)."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = "Mock GPU"
        mock_torch.cuda.memory_allocated.return_value = 2 * (1024 ** 3)
        mock_torch.cuda.memory_reserved.return_value = 3 * (1024 ** 3)

        mock_props = MagicMock()
        mock_props.total_memory = 8 * (1024 ** 3)
        mock_torch.cuda.get_device_properties.return_value = mock_props

        with patch.dict("sys.modules", {"torch": mock_torch}):
            stats = transformers_engine.get_gpu_stats()

        assert stats["available"] is True
        assert len(stats["devices"]) == 1
        assert stats["devices"][0]["name"] == "Mock GPU"
        assert stats["devices"][0]["allocated_gb"] == 2.0
        assert stats["devices"][0]["total_gb"] == 8.0


# ======================================================================
# Test 20: Invalid quantization
# ======================================================================

class TestTransformersEngineQuantization:
    """Invalid quantization handling."""

    def test_invalid_quantization(self):
        """Ungueltiger Quantisierungswert laesst Config-Validierung fehlschlagen."""
        LLMConfig.reset()
        with pytest.raises(LLMConfigError, match="Invalid quantization"):
            LLMConfig(
                model_source="huggingface",
                hf_quantization="3bit",
                skip_validation=False,
            )


# ======================================================================
# Test 21: Config validation
# ======================================================================

class TestTransformersEngineConfigValidation:
    """LLMConfig validation for HuggingFace settings."""

    def test_config_validation_invalid_source(self):
        """Ungueltige model_source wird abgelehnt."""
        LLMConfig.reset()
        with pytest.raises(LLMConfigError, match="Invalid model_source"):
            LLMConfig(
                model_source="invalid_provider",
                skip_validation=False,
            )

    def test_config_validation_invalid_device(self):
        """Ungueltiges Device wird abgelehnt."""
        LLMConfig.reset()
        with pytest.raises(LLMConfigError, match="Invalid device"):
            LLMConfig(
                model_source="huggingface",
                hf_device="tpu",
                skip_validation=False,
            )

    def test_config_validation_invalid_dtype(self):
        """Ungueltiger dtype wird abgelehnt."""
        LLMConfig.reset()
        with pytest.raises(LLMConfigError, match="Invalid dtype"):
            LLMConfig(
                model_source="huggingface",
                hf_torch_dtype="float64",
                skip_validation=False,
            )

    def test_config_validation_valid_hf(self):
        """Gueltige HF-Config wird akzeptiert."""
        LLMConfig.reset()
        config = LLMConfig(
            model_source="huggingface",
            hf_model_name="test/model",
            hf_device="cpu",
            hf_quantization="4bit",
            hf_torch_dtype="float16",
            skip_validation=False,
        )
        assert config.model_source == "huggingface"
        assert config.hf_quantization == "4bit"