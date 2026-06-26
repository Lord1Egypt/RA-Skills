#!/usr/bin/env python3
"""ML-based wake word detection using OpenWakeWord.

Provides low-latency, always-on wake word detection on raw audio
without requiring full Whisper transcription.  Uses small ONNX models
(~10 MB) that run at ~2 % CPU.

Usage:
    detector = OpenWakeWordDetector(model="hey_jarvis", threshold=0.5)
    detector.load()

    # Feed 80 ms chunks (1280 samples @ 16 kHz, int16) continuously:
    if detector.process_chunk(audio_chunk):
        print("Wake word detected!")
"""

import logging
from typing import Optional

import numpy as np

from kiwi.utils import kiwi_log

logger = logging.getLogger(__name__)


class OpenWakeWordDetector:
    """Detects wake words using OpenWakeWord ONNX models."""

    def __init__(
        self,
        model: str = "hey_jarvis",
        threshold: float = 0.5,
        inference_framework: str = "onnx",
    ) -> None:
        self.model_name = model
        self.threshold = threshold
        self.inference_framework = inference_framework
        self._oww_model = None

    def load(self) -> bool:
        """Load the wake word model.  Downloads base models if needed.

        Returns True on success, False on failure.
        """
        try:
            import openwakeword
            from openwakeword.model import Model as OWWModel

            # Download shared preprocessing models (melspectrogram + embedding)
            openwakeword.utils.download_models()

            self._oww_model = OWWModel(
                wakeword_models=[self.model_name],
                inference_framework=self.inference_framework,
            )
            kiwi_log("OWW", f"Loaded wake word model: {self.model_name}")
            return True

        except Exception as e:
            kiwi_log("OWW", f"Failed to load wake word model: {e}", level="ERROR")
            self._oww_model = None
            return False

    def process_chunk(self, audio_chunk: np.ndarray) -> bool:
        """Process an audio chunk and check for wake word.

        Args:
            audio_chunk: int16 numpy array, 16 kHz mono.
                         Ideal size: 1280 samples (80 ms).

        Returns:
            True if wake word detected above threshold.
        """
        if self._oww_model is None:
            return False

        try:
            self._oww_model.predict(audio_chunk)

            for model_name in self._oww_model.prediction_buffer:
                scores = list(self._oww_model.prediction_buffer[model_name])
                if scores and scores[-1] > self.threshold:
                    kiwi_log(
                        "OWW",
                        f"Wake word detected: {model_name} "
                        f"(score={scores[-1]:.3f}, threshold={self.threshold})",
                    )
                    self._oww_model.reset()
                    return True

        except Exception as e:
            kiwi_log("OWW", f"Prediction error: {e}", level="ERROR")

        return False

    def reset(self) -> None:
        """Reset internal prediction buffers."""
        if self._oww_model is not None:
            self._oww_model.reset()

    @property
    def is_loaded(self) -> bool:
        return self._oww_model is not None
