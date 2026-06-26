#!/usr/bin/env python3
"""Local Qwen3-TTS client (CustomVoice mode) for Kiwi Voice."""

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import numpy as np

from kiwi.utils import kiwi_log
from kiwi.tts.base import (
    STYLES,
    QWEN_VOICES,
    QWEN_VOICE_ALIASES,
    TTSCacheMixin,
    normalize_model_size as normalize_qwen_model_size,
    normalize_voice as normalize_qwen_voice,
)


@dataclass
class LocalQwenTTSConfig:
    model_size: str = "1.7B"
    model_path: Optional[str] = None
    tokenizer_path: Optional[str] = None
    default_voice: str = "Ono_Anna"
    device: str = "auto"  # auto|cpu|cuda
    attn_implementation: str = "auto"  # auto|flash_attention_2|sdpa|none
    cache_ttl: int = 3600
    cache_size: int = 100
    max_new_tokens: int = 768


class LocalQwenTTSClient(TTSCacheMixin):
    """Local Qwen3-TTS client with in-memory caching."""

    def __init__(self, config: Optional[LocalQwenTTSConfig] = None):
        self.config = config or LocalQwenTTSConfig()
        self.config.model_size = normalize_qwen_model_size(self.config.model_size)
        self.config.default_voice = normalize_qwen_voice(self.config.default_voice)

        self._cache_size = self.config.cache_size
        self._cache_ttl = self.config.cache_ttl
        self._init_cache()

        # Optional deps are imported lazily to avoid breaking Piper-only setups.
        try:
            import torch
            from qwen_tts import Qwen3TTSModel
        except ImportError as exc:
            raise ImportError(
                "Local Qwen3-TTS requires `qwen_tts` and `torch`. "
                "Install dependencies or switch backend to runpod/piper."
            ) from exc

        self._torch = torch
        self._Qwen3TTSModel = Qwen3TTSModel

        model_path = self.config.model_path
        if not model_path:
            from kiwi import PROJECT_ROOT
            model_path = os.path.join(
                PROJECT_ROOT,
                "models",
                f"Qwen3-TTS-12Hz-{self.config.model_size}-CustomVoice",
            )

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Qwen model path not found: {model_path}. "
                f"Place Qwen3-TTS-12Hz-{self.config.model_size}-CustomVoice there "
                "or set tts.local_model_path."
            )

        device = self._resolve_device(self.config.device)
        self.model_path = model_path
        self.runtime_device = device
        dtype = torch.bfloat16 if device == "cuda" else torch.float32
        attn_impl = self._resolve_attn_impl(device)

        kiwi_log("QWEN-LOCAL", f"Loading model: {model_path}")
        kiwi_log("QWEN-LOCAL", f"device={device} dtype={dtype} attn={attn_impl}")
        started_at = time.time()

        kwargs: Dict[str, Any] = {
            "device_map": device,
            "dtype": dtype,
            "attn_implementation": attn_impl,
        }
        if self.config.tokenizer_path:
            kwargs["tokenizer_path"] = self.config.tokenizer_path

        try:
            self.model = self._Qwen3TTSModel.from_pretrained(model_path, **kwargs)
        except TypeError:
            # Some qwen_tts builds may not accept tokenizer_path.
            kwargs.pop("tokenizer_path", None)
            self.model = self._Qwen3TTSModel.from_pretrained(model_path, **kwargs)

        kiwi_log("QWEN-LOCAL", f"Model loaded in {time.time() - started_at:.2f}s")

    def _resolve_device(self, configured: str) -> str:
        value = (configured or "auto").strip().lower()
        if value in {"cpu", "cuda"}:
            if value == "cuda" and not self._torch.cuda.is_available():
                kiwi_log("QWEN-LOCAL", "CUDA requested but unavailable; falling back to CPU", level="WARNING")
                return "cpu"
            return value
        return "cuda" if self._torch.cuda.is_available() else "cpu"

    def _resolve_attn_impl(self, device: str) -> Optional[str]:
        value = (self.config.attn_implementation or "auto").strip().lower()
        if value == "none":
            return None
        if value in {"flash_attention_2", "sdpa"}:
            return value
        if device != "cuda":
            return None
        try:
            import flash_attn  # noqa: F401
            return "flash_attention_2"
        except ImportError:
            return "sdpa"

    def _speaker_candidates(self, voice: str) -> Tuple[str, ...]:
        canonical = normalize_qwen_voice(voice)
        lowered = canonical.lower()
        if canonical == lowered:
            return (canonical,)
        return canonical, lowered

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        style: str = "neutral",
        language: str = "Russian",
        use_cache: bool = True,
        **kwargs: Any,
    ) -> Tuple[Optional[np.ndarray], int]:
        if not text or not text.strip():
            return None, 0

        model_size = kwargs.pop("model_size", None)
        requested_model = normalize_qwen_model_size(model_size or self.config.model_size)
        if requested_model != self.config.model_size:
            raise ValueError(
                f"Local Qwen client loaded for {self.config.model_size}, "
                f"but requested {requested_model}. Restart with matching model."
            )

        resolved_voice = normalize_qwen_voice(voice or self.config.default_voice)
        instruct = kwargs.pop("instruct", None)
        resolved_instruct = instruct or STYLES.get(style, STYLES["neutral"])

        cache_key = self._make_cache_key(text, resolved_voice, style, language, self.config.model_size)
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached is not None:
                return cached

        generation_kwargs = {
            "max_new_tokens": kwargs.get("max_tokens", self.config.max_new_tokens),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "top_k": kwargs.get("top_k", 50),
            "repetition_penalty": kwargs.get("repetition_penalty", 1.05),
        }

        last_error: Optional[Exception] = None
        for speaker in self._speaker_candidates(resolved_voice):
            try:
                with self._torch.inference_mode():
                    wavs, sr = self.model.generate_custom_voice(
                        text=text,
                        language=language,
                        speaker=speaker,
                        instruct=resolved_instruct,
                        **generation_kwargs,
                    )
                if not wavs:
                    return None, 0
                audio = self._coerce_audio(wavs[0])
                if use_cache and audio.size > 0:
                    self._set_cached(cache_key, audio, int(sr))
                return audio, int(sr)
            except Exception as exc:
                last_error = exc

        if last_error is not None:
            raise last_error
        return None, 0

    # Backward compatibility alias
    def generate_custom_voice(self, text: str, **kwargs: Any) -> Tuple[Optional[np.ndarray], int]:
        return self.synthesize(text, **kwargs)
