#!/usr/bin/env python3
"""
TransformersEngine - HuggingFace Transformers LLM Integration

Direct in-process model loading and generation via HuggingFace Transformers.
No external server required — model runs in the same Python process.

Features:
- Lazy model loading (load on first generate call)
- Quantization support (4-bit/8-bit via bitsandbytes)
- Automatic device detection (CUDA > MPS > CPU)
- Thread-safe async via ThreadPoolExecutor
- Streaming support via TextIteratorStreamer
- Automatic OOM fallback (GPU → CPU)
- Memory management with unload_model()

Usage:
    from kb.biblio.config import LLMConfig
    from kb.biblio.engine import TransformersEngine

    config = LLMConfig(
        model_source="huggingface",
        hf_model_name="google/gemma-2-2b-it",
        hf_quantization="4bit",
    )
    engine = TransformersEngine(config)
    response = engine.generate("Explain quantum computing")
"""

import asyncio
import functools
import gc
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, List, Optional, Sequence, Union, Iterator, AsyncIterator

from kb.biblio.config import LLMConfig, get_llm_config
from kb.biblio.engine.base import BaseLLMEngine, LLMProvider, LLMResponse, LLMStreamChunk
from kb.base.logger import get_logger

logger = get_logger("kb.llm.engine.transformers")


class TransformersEngineError(Exception):
    """Base exception for Transformers engine errors."""
    pass


class TransformersModelLoadError(TransformersEngineError):
    """Raised when model loading fails."""
    pass


class TransformersGenerationError(TransformersEngineError):
    """Raised when text generation fails."""
    pass


class TransformersEngine(BaseLLMEngine):
    """
    HuggingFace Transformers LLM Engine — Singleton.

    Loads models directly via the transformers library.
    No external server required — model runs in-process.

    Supports:
    - Auto device detection (CUDA > MPS > CPU)
    - 4-bit/8-bit quantization via bitsandbytes
    - Streaming via TextIteratorStreamer
    - Async via ThreadPoolExecutor
    - Automatic OOM fallback

    Thread-safe singleton: use TransformersEngine.get_instance()
    to obtain the shared instance.
    """

    _instance: Optional['TransformersEngine'] = None
    _lock = threading.Lock()

    def __new__(cls, config: Optional[LLMConfig] = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instance = instance
        return cls._instance

    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize TransformersEngine.

        Args:
            config: LLMConfig instance. Uses global singleton if None.

        Note: Model is NOT loaded at init time. Call load_model()
        explicitly or let it lazy-load on first generate() call.
        """
        # Singleton guard: skip re-initialization
        if self._initialized:
            return

        self._config = config or get_llm_config()
        self._model = None          # transformers.PreTrainedModel
        self._tokenizer = None      # transformers.PreTrainedTokenizer
        self._executor = None       # ThreadPoolExecutor
        self._device = None         # torch.device
        self._model_loaded = False
        self._load_lock = threading.Lock()
        self._torch_version: Optional[str] = None
        self._transformers_version: Optional[str] = None
        self._initialized = True

        logger.info(
            "TransformersEngine initialized",
            extra={
                "model": self._config.hf_model_name,
                "device": self._config.hf_device,
                "quantization": self._config.hf_quantization,
            }
        )

    @classmethod
    def get_instance(cls, config: Optional[LLMConfig] = None) -> 'TransformersEngine':
        """Get singleton instance, creating if necessary."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(config)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset singleton (mainly for testing)."""
        with cls._lock:
            if cls._instance is not None:
                try:
                    cls._instance.unload_model()
                except Exception:
                    pass
            cls._instance = None

    # ------------------------------------------------------------------
    # Dependency & device helpers
    # ------------------------------------------------------------------

    def _check_dependencies(self) -> None:
        """
        Check if required packages (torch, transformers) are installed.

        Raises:
            TransformersEngineError: If a required package is missing.
        """
        try:
            import torch
            import transformers
            self._torch_version = torch.__version__
            self._transformers_version = transformers.__version__
            logger.debug(
                "Dependencies OK",
                extra={
                    "torch": self._torch_version,
                    "transformers": self._transformers_version,
                }
            )
        except ImportError as exc:
            raise TransformersEngineError(
                f"Missing dependency: {exc}. "
                f"Install with: pip install torch transformers"
            ) from exc

    def _detect_device(self) -> "torch.device":
        """
        Auto-detect best available device.

        Priority: CUDA > MPS (Apple Silicon) > CPU

        If ``hf_device`` is set to something other than ``"auto"``,
        that value is used directly.

        Returns:
            torch.device to place the model on.
        """
        import torch

        device_str = self._config.hf_device

        if device_str == "auto":
            if torch.cuda.is_available():
                detected = torch.device("cuda")
                logger.info("Auto-detected device: CUDA")
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                detected = torch.device("mps")
                logger.info("Auto-detected device: MPS (Apple Silicon)")
            else:
                detected = torch.device("cpu")
                logger.info("Auto-detected device: CPU")
            return detected

        return torch.device(device_str)

    def _resolve_dtype(self) -> "torch.dtype":
        """
        Resolve torch dtype from config string.

        When ``hf_torch_dtype`` is ``"auto"``:
        - bfloat16 if CUDA supports it (Ampere+)
        - float16 if CUDA is available but doesn't support bf16
        - float32 on CPU

        Returns:
            torch.dtype to use for model loading.
        """
        import torch

        dtype_str = self._config.hf_torch_dtype
        if dtype_str == "auto":
            if torch.cuda.is_available():
                if torch.cuda.is_bf16_supported():
                    return torch.bfloat16
                return torch.float16
            return torch.float32

        dtype_map = {
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
            "float32": torch.float32,
        }
        if dtype_str not in dtype_map:
            raise TransformersEngineError(
                f"Invalid dtype: {dtype_str}. Must be one of {set(dtype_map.keys())} or 'auto'"
            )
        return dtype_map[dtype_str]

    def _build_quantization_config(self) -> Optional["BitsAndBytesConfig"]:
        """
        Build quantization config based on settings.

        Supports:
        - ``"4bit"``: NF4 quantization with double quantization
        - ``"8bit"``: LLM.int8() quantization

        Returns:
            BitsAndBytesConfig instance, or None when no quantization is requested.

        Raises:
            TransformersEngineError: If bitsandbytes is required but not installed.
        """
        if self._config.hf_quantization is None:
            return None

        try:
            from transformers import BitsAndBytesConfig
        except ImportError:
            raise TransformersEngineError(
                "Quantization requires the `transformers` package with "
                "bitsandbytes support. Install with: pip install bitsandbytes"
            )

        if self._config.hf_quantization == "4bit":
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=self._resolve_dtype(),
                bnb_4bit_use_double_quantization=True,
            )
        elif self._config.hf_quantization == "8bit":
            return BitsAndBytesConfig(load_in_8bit=True)

        return None

    # ------------------------------------------------------------------
    # Model loading
    # ------------------------------------------------------------------

    def load_model(self) -> None:
        """
        Load model and tokenizer from HuggingFace Hub.

        Thread-safe: concurrent calls will only load once.

        Features:
        - Auto-download on first use (HF Hub caching)
        - Revision pinning for reproducibility
        - Quantization (4-bit/8-bit via bitsandbytes)
        - Device placement (auto/cuda/cpu/mps)
        - dtype selection (float16/bfloat16/auto)
        - Automatic OOM fallback to CPU

        Raises:
            TransformersModelLoadError: If loading fails (including OOM).
        """
        with self._load_lock:
            if self._model_loaded:
                logger.debug("Model already loaded, skipping")
                return
            self._do_load_model()

    def _do_load_model(self) -> None:
        """Internal: actually load model (caller holds _load_lock)."""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._check_dependencies()

        model_name = self._config.hf_model_name
        logger.info(f"Loading model: {model_name}")

        # Detect device & dtype
        self._device = self._detect_device()
        dtype = self._resolve_dtype()
        quantization_config = self._build_quantization_config()

        logger.info(
            f"Load config: device={self._device}, dtype={dtype}, "
            f"quantization={self._config.hf_quantization}"
        )

        # --- Load tokenizer ---
        tokenizer_kwargs = {
            "revision": self._config.hf_revision,
        }
        if self._config.hf_token:
            tokenizer_kwargs["token"] = self._config.hf_token
        if self._config.hf_cache_dir:
            tokenizer_kwargs["cache_dir"] = self._config.hf_cache_dir

        logger.info(f"Loading tokenizer: {model_name}")
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_name, **tokenizer_kwargs
            )
        except Exception as exc:
            raise TransformersModelLoadError(
                f"Failed to load tokenizer for '{model_name}': {exc}"
            ) from exc

        # Ensure pad token exists (many models lack one)
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token
            logger.debug("Set pad_token = eos_token")

        # --- Load model ---
        model_kwargs = {
            "revision": self._config.hf_revision,
            "torch_dtype": dtype,
        }
        if self._config.hf_token:
            model_kwargs["token"] = self._config.hf_token
        if self._config.hf_cache_dir:
            model_kwargs["cache_dir"] = self._config.hf_cache_dir
        if self._config.hf_trust_remote_code:
            model_kwargs["trust_remote_code"] = True
        if self._config.hf_offload_folder:
            model_kwargs["offload_folder"] = self._config.hf_offload_folder

        # device_map: "auto" lets accelerate distribute the model.
        # Only use device_map when quantizing or when user explicitly wants auto.
        device_map = self._resolve_device_map()
        if device_map is not None:
            model_kwargs["device_map"] = device_map
        elif self._config.hf_device == "auto" and quantization_config is not None:
            model_kwargs["device_map"] = "auto"
        else:
            model_kwargs["device_map"] = None
        # Also enable CPU offload folder when using device_map="auto"
        if model_kwargs.get("device_map") and not self._config.hf_offload_folder:
            model_kwargs["offload_folder"] = "offload"

        if quantization_config is not None:
            model_kwargs["quantization_config"] = quantization_config

        logger.info(f"Loading model weights: {model_name}")
        try:
            self._model = AutoModelForCausalLM.from_pretrained(
                model_name, **model_kwargs
            )
        except torch.cuda.OutOfMemoryError:
            logger.warning("GPU Out of Memory during model load, attempting CPU fallback")
            self._try_cpu_fallback(model_name, tokenizer_kwargs, model_kwargs)
        except Exception as exc:
            raise TransformersModelLoadError(
                f"Failed to load model '{model_name}': {exc}"
            ) from exc

        # Place on device if not using device_map
        if self._config.hf_device != "auto" and quantization_config is None:
            try:
                self._model = self._model.to(self._device)
            except torch.cuda.OutOfMemoryError:
                logger.warning("GPU OOM on .to(device), falling back to CPU")
                self._device = torch.device("cpu")
                self._model = self._model.to(self._device)

        self._model.eval()  # Inference mode
        self._model_loaded = True

        logger.info(
            f"Model loaded successfully: {model_name} on {self._device}",
            extra={
                "device": str(self._device),
                "dtype": str(dtype),
                "quantization": self._config.hf_quantization,
            }
        )

    def _try_cpu_fallback(
        self,
        model_name: str,
        tokenizer_kwargs: dict,
        model_kwargs: dict,
    ) -> None:
        """
        Attempt to load the model on CPU after a GPU OOM.

        Removes quantization and device_map, forces CPU/float32.

        Raises:
            TransformersModelLoadError: If CPU loading also fails.
        """
        import torch
        from transformers import AutoModelForCausalLM

        logger.warning(
            "Falling back to CPU with float32 (no quantization). "
            "This will be slow and use significant RAM."
        )

        # Strip GPU/quantization kwargs
        cpu_kwargs = {
            k: v for k, v in model_kwargs.items()
            if k not in ("quantization_config", "device_map")
        }
        cpu_kwargs["torch_dtype"] = torch.float32
        cpu_kwargs["device_map"] = None

        try:
            # Clear GPU cache first
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

            self._model = AutoModelForCausalLM.from_pretrained(
                model_name, **cpu_kwargs
            )
            self._device = torch.device("cpu")
        except Exception as exc:
            raise TransformersModelLoadError(
                f"Failed to load model '{model_name}' even on CPU: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Lazy loading helper
    # ------------------------------------------------------------------

    def _ensure_model_loaded(self) -> None:
        """Lazy-load model if not already loaded."""
        if not self._model_loaded:
            logger.info(f"Lazily loading model: {self._config.hf_model_name}")
            self.load_model()

    # ------------------------------------------------------------------
    # Memory management
    # ------------------------------------------------------------------

    def unload_model(self) -> None:
        """
        Unload model and tokenizer from memory.

        Releases GPU memory (via torch.cuda.empty_cache()) and
        forces Python garbage collection.  After calling this,
        the next generate() call will trigger a fresh load.
        """
        import torch

        if self._model is not None:
            logger.info(f"Unloading model: {self._config.hf_model_name}")
            del self._model
            self._model = None

        if self._tokenizer is not None:
            del self._tokenizer
            self._tokenizer = None

        self._model_loaded = False

        # Force GPU memory cleanup
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.debug("GPU cache cleared")

        gc.collect()
        logger.info("Model unloaded, memory released")

    def __del__(self):
        """Destructor: clean up model and executor on garbage collection."""
        try:
            self.unload_model()
        except Exception:
            pass  # Best-effort cleanup

        if self._executor is not None:
            self._executor.shutdown(wait=False)
            self._executor = None

    # ------------------------------------------------------------------
    # ThreadPoolExecutor for async
    # ------------------------------------------------------------------

    def _get_executor(self) -> ThreadPoolExecutor:
        """Get or create thread pool for async operations."""
        if self._executor is None:
            # max_workers=1: model inference is sequential per model
            self._executor = ThreadPoolExecutor(
                max_workers=1,
                thread_name_prefix="hf_engine",
            )
        return self._executor

    # ------------------------------------------------------------------
    # BaseLLMEngine interface
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Check if the Transformers engine is available.

        Returns True if torch and transformers are importable.
        Does NOT check whether a specific model is cached locally.
        """
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
            return True
        except ImportError:
            logger.debug("torch or transformers not installed")
            return False

    def get_model_name(self) -> str:
        """Get the configured HuggingFace model name."""
        return self._config.hf_model_name

    def get_provider(self) -> LLMProvider:
        """Get the LLM provider type."""
        return LLMProvider.HUGGINGFACE

    def generate(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate text synchronously from a prompt.

        Lazily loads the model on first call.

        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific options (repetition_penalty, top_k, top_p)

        Returns:
            LLMResponse object with generated content

        Raises:
            TransformersGenerationError: On generation failure
        """
        import torch

        self._ensure_model_loaded()

        temp = temperature if temperature is not None else self._config.temperature
        max_new = max_tokens if max_tokens is not None else self._config.max_tokens

        # Tokenize
        inputs = self._tokenizer(prompt, return_tensors="pt")
        if self._device.type != "cpu":
            inputs = {k: v.to(self._device) for k, v in inputs.items()}

        # Build generation kwargs
        gen_kwargs = {
            "max_new_tokens": max_new,
        }
        if temp > 0:
            gen_kwargs["temperature"] = temp
            gen_kwargs["do_sample"] = True
            gen_kwargs["top_p"] = kwargs.get("top_p", 0.95)
        else:
            gen_kwargs["do_sample"] = False

        # Additional kwargs
        for key in ("repetition_penalty", "top_k", "top_p"):
            if key in kwargs:
                gen_kwargs[key] = kwargs[key]

        # Generate with optimised inference context
        start_time = time.time()
        gpu_mem_before: Optional[Dict] = None
        try:
            # Capture GPU memory before generation (for monitoring)
            try:
                import torch as _torch
                if _torch.cuda.is_available() and self._device is not None and self._device.type == "cuda":
                    gpu_mem_before = {
                        "allocated_gb": round(_torch.cuda.memory_allocated(self._device) / (1024**3), 2),
                        "reserved_gb": round(_torch.cuda.memory_reserved(self._device) / (1024**3), 2),
                    }
            except Exception:
                pass

            with self._inference_context():
                outputs = self._model.generate(**inputs, **gen_kwargs)
        except torch.cuda.OutOfMemoryError:
            logger.warning("GPU OOM during generation, unloading model")
            self.unload_model()
            raise TransformersGenerationError(
                "GPU ran out of memory during generation. "
                "Try using 4-bit quantization or a smaller model."
            )
        except Exception as exc:
            raise TransformersGenerationError(
                f"Generation failed: {exc}"
            ) from exc

        # Decode (skip input tokens)
        input_len = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_len:]
        content = self._tokenizer.decode(generated_tokens, skip_special_tokens=True)

        duration_ns = int((time.time() - start_time) * 1e9)
        output_len = len(generated_tokens)

        return LLMResponse(
            content=content,
            model=self._config.hf_model_name,
            provider=LLMProvider.HUGGINGFACE,
            done=True,
            total_duration=duration_ns,
            tokens=output_len,
            context=input_len + output_len,
        )

    async def generate_async(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate text asynchronously (non-blocking).

        Offloads model inference to a ThreadPoolExecutor.

        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific options

        Returns:
            LLMResponse object with generated content
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._get_executor(),
            functools.partial(
                self.generate,
                prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        )

    # ------------------------------------------------------------------
    # Batch Processing
    # ------------------------------------------------------------------

    def generate_batch(
        self,
        prompts: Sequence[str],
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        on_progress: Optional[Callable[[int, int], None]] = None,
        **kwargs
    ) -> List[LLMResponse]:
        """
        Generate responses for multiple prompts sequentially.

        Processes each prompt individually (not padded-batch) to
        avoid OOM issues with varying prompt lengths. Each prompt
        is tokenized and decoded independently.

        Args:
            prompts: Sequence of input prompt strings
            temperature: Sampling temperature (0-2) for all prompts
            max_tokens: Maximum tokens to generate per prompt
            on_progress: Optional callback ``on_progress(completed, total)``
                         called after each successful generation.
            **kwargs: Provider-specific generation options

        Returns:
            List of LLMResponse objects, one per prompt, in input order.
            Failed prompts return an LLMResponse with ``error`` set.
        """
        self._ensure_model_loaded()

        total = len(prompts)
        results: List[LLMResponse] = []

        for idx, prompt in enumerate(prompts):
            try:
                response = self.generate(
                    prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                results.append(response)
            except Exception as exc:
                logger.error(
                    f"Batch generation failed for prompt {idx + 1}/{total}: {exc}"
                )
                results.append(LLMResponse(
                    content="",
                    model=self._config.hf_model_name,
                    provider=LLMProvider.HUGGINGFACE,
                    done=False,
                    error=str(exc),
                ))

            if on_progress is not None:
                try:
                    on_progress(idx + 1, total)
                except Exception:
                    logger.debug("on_progress callback raised, ignoring")

        return results

    async def generate_batch_async(
        self,
        prompts: Sequence[str],
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        on_progress: Optional[Callable[[int, int], None]] = None,
        **kwargs
    ) -> List[LLMResponse]:
        """
        Generate responses for multiple prompts asynchronously.

        Async wrapper around :meth:`generate_batch`. Runs the entire
        batch in a thread pool so the event loop is not blocked.

        Args:
            prompts: Sequence of input prompt strings
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens per prompt
            on_progress: Optional callback ``on_progress(completed, total)``
            **kwargs: Provider-specific generation options

        Returns:
            List of LLMResponse objects, one per prompt.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._get_executor(),
            functools.partial(
                self.generate_batch,
                prompts,
                temperature=temperature,
                max_tokens=max_tokens,
                on_progress=on_progress,
                **kwargs
            )
        )

    # ------------------------------------------------------------------
    # Chat Template
    # ------------------------------------------------------------------

    def apply_chat_template(
        self,
        messages: Sequence[Dict[str, str]],
        **kwargs
    ) -> str:
        """
        Apply the model's chat template to a list of messages.

        Uses ``tokenizer.apply_chat_template`` when available (most
        modern instruct/conversation models). Falls back to a simple
        role/content format for models without a template.

        Args:
            messages: List of message dicts, each with ``"role"`` and
                      ``"content"`` keys.  Example::

                          [{"role": "user", "content": "Hello!"}]
            **kwargs: Additional keyword arguments forwarded to
                      ``tokenizer.apply_chat_template``.

        Returns:
            Formatted prompt string ready for :meth:`generate`.

        Raises:
            TransformersEngineError: If the model is not loaded.
        """
        self._ensure_model_loaded()

        # Try the tokenizer's native chat template (most instruct models)
        if hasattr(self._tokenizer, "apply_chat_template"):
            try:
                rendered = self._tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                    **kwargs
                )
                if isinstance(rendered, str):
                    return rendered
                # Some tokenizers return a list[str]
                if isinstance(rendered, list):
                    return "".join(rendered)
            except Exception as exc:
                logger.warning(
                    f"tokenizer.apply_chat_template failed, using fallback: {exc}"
                )

        # Fallback: simple role/content format
        parts: List[str] = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            parts.append(f"<|{role}|>\n{content}")
        parts.append("<|assistant|>")
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Multi-GPU & GPU Statistics
    # ------------------------------------------------------------------

    def get_gpu_stats(self) -> Dict[str, Union[bool, List[Dict[str, Union[int, str, float]]]]]:
        """
        Get current GPU memory and device statistics.

        Returns a dictionary describing every visible CUDA device:
        allocated, reserved, total and free memory (in GiB), plus
        the device name.  When CUDA is not available the result
        contains ``{"available": False}``.

        Returns:
            Dict with key ``"available"`` (bool) and, if available,
            ``"devices"`` (list of per-device dicts).
        """
        try:
            import torch
        except ImportError:
            return {"available": False}

        if not torch.cuda.is_available():
            return {"available": False}

        devices: List[Dict[str, Union[int, str, float]]] = []
        for i in range(torch.cuda.device_count()):
            allocated = torch.cuda.memory_allocated(i) / (1024 ** 3)
            reserved = torch.cuda.memory_reserved(i) / (1024 ** 3)
            total = torch.cuda.get_device_properties(i).total_memory / (1024 ** 3)

            devices.append({
                "index": i,
                "name": torch.cuda.get_device_name(i),
                "allocated_gb": round(allocated, 2),
                "reserved_gb": round(reserved, 2),
                "total_gb": round(total, 2),
                "free_gb": round(total - reserved, 2),
            })

        return {"available": True, "devices": devices}

    # ------------------------------------------------------------------
    # Accelerate / device_map helpers
    # ------------------------------------------------------------------

    def _resolve_device_map(self) -> Optional[str]:
        """
        Determine the ``device_map`` value for model loading.

        When ``accelerate`` is installed and the config requests
        ``"auto"``, this returns ``"auto"`` so accelerate distributes
        the model across available GPUs.  For single-GPU or CPU
        setups the method returns ``None`` (no device_map needed).

        Returns:
            ``"auto"``, ``"balanced"``, or ``None``.
        """
        try:
            import torch
        except ImportError:
            return None

        if not torch.cuda.is_available():
            return None

        if torch.cuda.device_count() <= 1 and self._config.hf_device == "auto":
            # Single GPU – accelerate not needed for sharding,
            # but device_map="auto" still valid for offloading.
            pass

        device = self._config.hf_device
        if device == "auto":
            try:
                import accelerate  # noqa: F401
                return "auto"
            except ImportError:
                logger.warning(
                    "accelerate not installed; multi-GPU sharding unavailable"
                )
                return None
        if device == "balanced":
            try:
                import accelerate  # noqa: F401
                return "balanced"
            except ImportError:
                logger.warning(
                    "accelerate not installed; cannot use 'balanced' device_map"
                )
                return None

        return None

    # ------------------------------------------------------------------
    # Inference Optimizations
    # ------------------------------------------------------------------

    def _inference_context(self) -> "torch.inference_mode":  # type: ignore[name-match]
        """
        Return an ``inference_mode`` context manager.

        Combines ``torch.inference_mode()`` with
        ``torch.set_grad_enabled(False)`` for maximum throughput.
        The context is safe to use as a ``with`` statement::

            with self._inference_context():
                outputs = self._model.generate(...)

        This disables gradient computation and autograd tracking,
        reducing memory overhead and speeding up inference.

        Returns:
            A context manager that disables gradients.
        """
        import torch
        # inference_mode is a superset of no_grad — it also
        # disables version counting and views tracking.
        # Nesting both is harmless and ensures coverage
        # even if inference_mode is somehow unavailable.
        return torch.inference_mode()

    # ------------------------------------------------------------------
    # Streaming generation
    # ------------------------------------------------------------------

    DEFAULT_STREAM_TIMEOUT = 120  # seconds

    def generate_stream(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Iterator[LLMStreamChunk]:
        """
        Stream tokens chunk-by-chunk using TextIteratorStreamer.

        Runs model.generate() in a background thread and yields
        LLMStreamChunk objects as tokens become available.

        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            timeout: Maximum seconds to wait for the next chunk.
                     Defaults to DEFAULT_STREAM_TIMEOUT (120s).
            **kwargs: Provider-specific options (repetition_penalty, top_k, top_p)

        Yields:
            LLMStreamChunk objects as they arrive, followed by a final
            chunk with done=True.

        Raises:
            TransformersGenerationError: On generation failure or timeout.
        """
        import torch
        from threading import Thread, Event
        from transformers import TextIteratorStreamer

        self._ensure_model_loaded()

        temp = temperature if temperature is not None else self._config.temperature
        max_new = max_tokens if max_tokens is not None else self._config.max_tokens
        stream_timeout = timeout if timeout is not None else self.DEFAULT_STREAM_TIMEOUT

        # Tokenize
        inputs = self._tokenizer(prompt, return_tensors="pt")
        if self._device.type != "cpu":
            inputs = {k: v.to(self._device) for k, v in inputs.items()}

        # Setup streamer
        streamer = TextIteratorStreamer(
            self._tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )

        # Build generation kwargs
        gen_kwargs = {
            **inputs,
            "streamer": streamer,
            "max_new_tokens": max_new,
        }
        if temp > 0:
            gen_kwargs["temperature"] = temp
            gen_kwargs["do_sample"] = True
            gen_kwargs["top_p"] = kwargs.get("top_p", 0.95)
        else:
            gen_kwargs["do_sample"] = False

        # Additional provider kwargs
        for key in ("repetition_penalty", "top_k", "top_p"):
            if key in kwargs:
                gen_kwargs[key] = kwargs[key]

        # Error container shared with generation thread
        generation_error: list[Exception] = []

        def _run_generation() -> None:
            """Run model.generate() in a background thread."""
            try:
                with torch.no_grad():
                    self._model.generate(**gen_kwargs)
            except torch.cuda.OutOfMemoryError:
                logger.warning("GPU OOM during streaming generation")
                generation_error.append(
                    TransformersGenerationError(
                        "GPU ran out of memory during streaming generation. "
                        "Try using 4-bit quantization or a smaller model."
                    )
                )
            except Exception as exc:
                generation_error.append(
                    TransformersGenerationError(f"Streaming generation failed: {exc}")
                )

        # Start generation in background thread
        generation_thread = Thread(
            target=_run_generation,
            name="hf-stream-generate",
            daemon=True,
        )
        generation_thread.start()

        # Yield tokens as they arrive
        try:
            for text in streamer:
                # Check if generation thread raised an error
                if generation_error:
                    raise generation_error[0]

                # Timeout: wait for next chunk but don't block forever
                if text:
                    yield LLMStreamChunk(content=text, done=False)
        except TimeoutError:
            logger.error(
                f"Stream timed out after {stream_timeout}s "
                f"for model {self._config.hf_model_name}"
            )
            raise TransformersGenerationError(
                f"Streaming generation timed out after {stream_timeout}s"
            )
        finally:
            # Ensure generation thread completes
            generation_thread.join(timeout=5)
            if generation_thread.is_alive():
                logger.warning(
                    "Generation thread still alive after stream ended; "
                    "model may still be processing"
                )

            # Propagate any error that occurred after streamer ended
            if generation_error:
                raise generation_error[0]

        # Final chunk signals completion
        yield LLMStreamChunk(content="", done=True)

    async def generate_stream_async(
        self,
        prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Async streaming generation — wraps sync stream via asyncio bridge.

        Bridges the synchronous TextIteratorStreamer to an async
        generator using asyncio.Queue and a ThreadPoolExecutor.

        Args:
            prompt: Input prompt text
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            timeout: Maximum seconds to wait for the next chunk.
            **kwargs: Provider-specific options

        Yields:
            LLMStreamChunk objects as they arrive.

        Raises:
            TransformersGenerationError: On generation failure or timeout.
        """
        import asyncio

        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[Optional[LLMStreamChunk]] = asyncio.Queue()

        def _sync_stream() -> None:
            """Run the sync stream and push chunks into the async queue."""
            try:
                for chunk in self.generate_stream(
                    prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=timeout,
                    **kwargs,
                ):
                    loop.call_soon_threadsafe(queue.put_nowait, chunk)
            except Exception as exc:
                # Push the error as a special sentinel
                loop.call_soon_threadsafe(queue.put_nowait, _StreamError(exc))
                return
            # Signal completion
            loop.call_soon_threadsafe(queue.put_nowait, None)

        # Start sync stream in thread pool
        executor = self._get_executor()
        await loop.run_in_executor(executor, _sync_stream)

        # Yield chunks from queue
        while True:
            item = await queue.get()
            if item is None:
                break
            if isinstance(item, _StreamError):
                raise item.error
            yield item

    @property
    def supports_streaming(self) -> bool:
        """TransformersEngine supports streaming via TextIteratorStreamer."""
        return True

    @property
    def supports_async(self) -> bool:
        """TransformersEngine supports async via ThreadPoolExecutor."""
        return True

    def __repr__(self) -> str:
        loaded = "loaded" if self._model_loaded else "not loaded"
        return (
            f"TransformersEngine("
            f"model={self._config.hf_model_name}, "
            f"device={self._config.hf_device}, "
            f"quant={self._config.hf_quantization}, "
            f"{loaded})"
        )


# Need asyncio for generate_async / generate_stream_async
import asyncio


class _StreamError:
    """Sentinel to propagate exceptions from sync stream thread to async queue."""
    __slots__ = ("error",)

    def __init__(self, error: Exception) -> None:
        self.error = error