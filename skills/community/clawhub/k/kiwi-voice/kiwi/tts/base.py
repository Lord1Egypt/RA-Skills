"""Shared TTS Protocol, cache mixin, and constants for all TTS providers."""

import hashlib
import time
from threading import Lock
from typing import Any, Dict, Optional, Protocol, Tuple

import numpy as np


# ── Shared constants ────────────────────────────────────────────────

STYLES: Dict[str, str] = {
    "neutral": "Speak with warmth and a gentle smile",
    "excited": "Speak with excitement and high energy",
    "calm": "Speak slowly and calmly, relaxed tone",
    "confident": "Speak with authority and confidence",
    "whisper": "Speak softly, like telling a secret",
    "sad": "Speak with sadness in voice",
    "angry": "Speak angrily with sharp emphasis",
    "playful": "Speak in a playful, teasing manner",
    "serious": "Speak in a serious, professional tone",
    "cheerful": "Speak cheerfully with a bright voice",
}

QWEN_VOICES = [
    "Vivian", "Serena", "Uncle_Fu", "Dylan",
    "Eric", "Ryan", "Aiden", "Ono_Anna", "Sohee",
]

QWEN_VOICE_ALIASES: Dict[str, str] = {
    "vivian": "Vivian",
    "serena": "Serena",
    "uncle_fu": "Uncle_Fu",
    "uncle-fu": "Uncle_Fu",
    "dylan": "Dylan",
    "eric": "Eric",
    "ryan": "Ryan",
    "aiden": "Aiden",
    "ono_anna": "Ono_Anna",
    "ono-anna": "Ono_Anna",
    "sohee": "Sohee",
}


def normalize_voice(voice: Optional[str]) -> str:
    if not voice:
        return "Ono_Anna"
    cleaned = str(voice).strip()
    if cleaned in QWEN_VOICES:
        return cleaned
    return QWEN_VOICE_ALIASES.get(cleaned.lower(), "Ono_Anna")


def normalize_model_size(model_size: Optional[str]) -> str:
    raw = str(model_size or "").strip().lower()
    if raw in {"0.6b", "0.6", "06", "600m"}:
        return "0.6B"
    if raw in {"1.7b", "1.7", "17", "1700m"}:
        return "1.7B"
    return "1.7B"


# ── Protocol ────────────────────────────────────────────────────────

class TTSProvider(Protocol):
    """Unified interface for all TTS providers."""

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        style: str = "neutral",
        language: str = "Russian",
        use_cache: bool = True,
        **kwargs: Any,
    ) -> Tuple[Optional[np.ndarray], int]:
        """Generate audio from text.

        Returns:
            (audio_array, sample_rate) or (None, 0) on failure.
        """
        ...

    def clear_cache(self) -> None: ...


# ── Cache mixin ─────────────────────────────────────────────────────

class TTSCacheMixin:
    """In-memory TTS cache with TTL eviction.

    Subclasses must set ``_cache_size`` and ``_cache_ttl`` (or rely on defaults).
    """

    _cache_size: int = 100
    _cache_ttl: int = 3600

    def _init_cache(self) -> None:
        self._cache: Dict[str, Tuple[np.ndarray, int, float]] = {}
        self._cache_lock = Lock()

    def _make_cache_key(self, text: str, *parts: Any) -> str:
        key_str = "|".join(str(p) for p in (text, *parts))
        return hashlib.md5(key_str.encode("utf-8")).hexdigest()

    def _get_cached(self, key: str) -> Optional[Tuple[np.ndarray, int]]:
        with self._cache_lock:
            item = self._cache.get(key)
            if not item:
                return None
            audio, sr, saved_at = item
            if time.time() - saved_at > self._cache_ttl:
                del self._cache[key]
                return None
            return audio, sr

    def _set_cached(self, key: str, audio: np.ndarray, sr: int) -> None:
        with self._cache_lock:
            if len(self._cache) >= self._cache_size:
                oldest = min(self._cache, key=lambda k: self._cache[k][2])
                del self._cache[oldest]
            self._cache[key] = (audio, sr, time.time())

    def clear_cache(self) -> None:
        with self._cache_lock:
            self._cache.clear()

    @staticmethod
    def _coerce_audio(audio_like: Any) -> np.ndarray:
        """Normalize to float32 mono, clip to [-1, 1]."""
        audio = np.asarray(audio_like, dtype=np.float32)
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        if peak > 1.0:
            audio = audio / peak
        return audio
