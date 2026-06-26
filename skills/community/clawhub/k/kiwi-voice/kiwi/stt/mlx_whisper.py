#!/usr/bin/env python3
"""MLX-accelerated Whisper backend for Apple Silicon.

Uses Lightning Whisper MLX for ~10x faster transcription on M-series chips.
Falls back gracefully when running on non-Apple-Silicon hardware.

Usage:
    from kiwi.stt.mlx_whisper import MLXWhisperSTT, MLX_AVAILABLE

    if MLX_AVAILABLE:
        stt = MLXWhisperSTT(model="distil-medium.en")
        stt.load()
        text = stt.transcribe(audio_np_array)
"""

import time
from typing import Optional, Tuple, List

import numpy as np

from kiwi.utils import kiwi_log

# Check MLX availability (Apple Silicon only)
MLX_AVAILABLE = False
try:
    from lightning_whisper_mlx import LightningWhisperMLX
    MLX_AVAILABLE = True
except ImportError:
    pass


# Model sizes available in Lightning Whisper MLX
MLX_MODELS = [
    "tiny", "tiny.en",
    "base", "base.en",
    "small", "small.en",
    "medium", "medium.en",
    "distil-medium.en",
    "large", "large-v2", "large-v3",
    "distil-large-v3",
]


class MLXWhisperSTT:
    """Apple Silicon optimized Whisper transcription via MLX.

    Only works on macOS with Apple Silicon (M1/M2/M3/M4).
    On other platforms, ``MLX_AVAILABLE`` is False and this class
    should not be instantiated.
    """

    def __init__(
        self,
        model: str = "distil-medium.en",
        language: str = "en",
        batch_size: int = 12,
        quant: Optional[str] = None,
    ) -> None:
        if not MLX_AVAILABLE:
            raise RuntimeError(
                "lightning-whisper-mlx is not installed or not available "
                "on this platform. MLX Whisper requires macOS on Apple Silicon."
            )

        self.model_name = model if model in MLX_MODELS else "distil-medium.en"
        self.language = language
        self.batch_size = batch_size
        self.quant = quant
        self._whisper = None

    def load(self) -> bool:
        """Load the MLX Whisper model.  Returns True on success."""
        try:
            kiwi_log("MLX-STT", f"Loading model: {self.model_name}")
            start = time.time()
            self._whisper = LightningWhisperMLX(
                model=self.model_name,
                batch_size=self.batch_size,
                quant=self.quant,
            )
            kiwi_log(
                "MLX-STT",
                f"Model loaded in {time.time() - start:.2f}s "
                f"(batch_size={self.batch_size})",
            )
            return True
        except Exception as e:
            kiwi_log("MLX-STT", f"Failed to load model: {e}", level="ERROR")
            self._whisper = None
            return False

    def transcribe(
        self,
        audio: np.ndarray,
        sample_rate: int = 16000,
    ) -> Optional[str]:
        """Transcribe audio to text.

        Args:
            audio: float32 numpy array, mono, at ``sample_rate`` Hz.
            sample_rate: Sample rate of the input audio (default 16000).

        Returns:
            Transcribed text, or None on failure.
        """
        if self._whisper is None:
            kiwi_log("MLX-STT", "Model not loaded", level="ERROR")
            return None

        if len(audio) == 0:
            return None

        try:
            start = time.time()
            result = self._whisper.transcribe(
                audio,
                language=self.language,
            )
            text = result.get("text", "").strip() if isinstance(result, dict) else str(result).strip()
            elapsed = time.time() - start
            duration = len(audio) / sample_rate

            if text:
                kiwi_log(
                    "MLX-STT",
                    f"Transcribed {duration:.1f}s in {elapsed:.2f}s "
                    f"({duration / elapsed:.1f}x real-time): "
                    f'"{text[:80]}{"..." if len(text) > 80 else ""}"',
                )

            return text if text else None

        except Exception as e:
            kiwi_log("MLX-STT", f"Transcription error: {e}", level="ERROR")
            return None

    @property
    def is_loaded(self) -> bool:
        return self._whisper is not None
