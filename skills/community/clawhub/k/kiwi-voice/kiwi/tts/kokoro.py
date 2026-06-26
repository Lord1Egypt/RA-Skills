#!/usr/bin/env python3
"""Local Kokoro ONNX TTS provider for Kiwi Voice.

Free, fully local text-to-speech using Kokoro ONNX models.
Supports 14 voices, 24kHz output, ~340MB total model size.
Auto-downloads models on first use.

Supported languages: en, ja, zh, ko, fr, de, it, es, pt, pl, tr, hi
Note: Russian is NOT supported by Kokoro v1.0.
"""

import re
import time
import urllib.request
from pathlib import Path
from typing import Any, Optional, Tuple

import numpy as np

from kiwi.utils import kiwi_log
from kiwi.tts.base import TTSCacheMixin
from kiwi import PROJECT_ROOT

MODEL_FILE = "kokoro-v1.0.onnx"
VOICES_FILE = "voices-v1.0.bin"
DOWNLOAD_BASE_URL = (
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
)

# Mapping from Kiwi language codes to Kokoro lang codes
LANG_MAP = {
    "en": "en-us",
    "ja": "ja",
    "zh": "cmn",
    "ko": "ko",
    "fr": "fr-fr",
    "de": "de",
    "it": "it",
    "es": "es",
    "pt": "pt-br",
    "pl": "pl",
    "tr": "tr",
    "hi": "hi",
    "id": "id",
}

# Available Kokoro voices
KOKORO_VOICES = [
    "af_heart", "af_star", "af_sky", "af_bella", "af_nicole",
    "am_adam", "am_michael",
    "bf_emma", "bf_isabella",
    "bm_george", "bm_lewis",
    "af_sarah", "am_fenrir", "bf_alice",
]

DEFAULT_VOICE = "af_heart"


class KokoroTTS(TTSCacheMixin):
    """Local Kokoro ONNX TTS provider.

    Free, high-quality, fully local TTS.  Models are auto-downloaded
    on first use (~340 MB total).
    """

    def __init__(
        self,
        voice: str = DEFAULT_VOICE,
        speed: float = 1.0,
        lang: str = "en-us",
        model_dir: str = None,
    ):
        self.voice = voice if voice in KOKORO_VOICES else DEFAULT_VOICE
        self.speed = speed
        self.lang = lang
        self.model_dir = Path(model_dir or str(Path(PROJECT_ROOT) / "models" / "kokoro"))
        self.sample_rate = 24000
        self._kokoro = None

        self._init_cache()

    def _download_models(self) -> None:
        """Download Kokoro model files from GitHub releases."""
        self.model_dir.mkdir(parents=True, exist_ok=True)
        for filename in [MODEL_FILE, VOICES_FILE]:
            dest = self.model_dir / filename
            if not dest.exists():
                url = f"{DOWNLOAD_BASE_URL}/{filename}"
                kiwi_log("KOKORO", f"Downloading {filename} ({url})...")
                urllib.request.urlretrieve(url, str(dest))
                kiwi_log("KOKORO", f"Downloaded {filename}")

    def _ensure_loaded(self) -> bool:
        """Lazy-load the Kokoro model. Returns True on success."""
        if self._kokoro is not None:
            return True

        model_path = self.model_dir / MODEL_FILE
        voices_path = self.model_dir / VOICES_FILE

        if not model_path.exists() or not voices_path.exists():
            try:
                self._download_models()
            except Exception as e:
                kiwi_log("KOKORO", f"Model download failed: {e}", level="ERROR")
                return False

        try:
            from kokoro_onnx import Kokoro

            kiwi_log("KOKORO", f"Loading model: voice={self.voice}, speed={self.speed}")
            start = time.time()
            self._kokoro = Kokoro(str(model_path), str(voices_path))
            kiwi_log("KOKORO", f"Model loaded in {time.time() - start:.2f}s")
            return True
        except Exception as e:
            kiwi_log("KOKORO", f"Failed to load model: {e}", level="ERROR")
            return False

    def _resolve_lang(self, language: str) -> str:
        """Map a Kiwi language code to a Kokoro lang code."""
        lang = language.lower().strip()
        # Already a Kokoro code (e.g. "en-us")
        if "-" in lang:
            return lang
        return LANG_MAP.get(lang, self.lang)

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        style: str = "neutral",
        language: str = "en",
        use_cache: bool = True,
        **kwargs: Any,
    ) -> Tuple[Optional[np.ndarray], int]:
        """Synthesize text to audio.

        Returns:
            (audio_float32, 24000) or (None, 0) on failure.
        """
        if not text or not text.strip():
            return None, self.sample_rate

        # Clean markdown
        text_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text_clean = re.sub(r'\*(.+?)\*', r'\1', text_clean)
        text_clean = re.sub(r'_(.+?)_', r'\1', text_clean)
        text_clean = re.sub(r'`(.+?)`', r'\1', text_clean)
        text_clean = text_clean.strip()

        effective_voice = voice if voice and voice in KOKORO_VOICES else self.voice
        effective_lang = self._resolve_lang(language)

        # Cache lookup
        cache_key = self._make_cache_key(text_clean, effective_voice, effective_lang)
        if use_cache:
            cached = self._get_cached(cache_key)
            if cached is not None:
                kiwi_log("KOKORO", f'Cache hit: "{text_clean[:40]}..."')
                return cached

        if not self._ensure_loaded():
            return None, 0

        try:
            start = time.time()
            samples, sample_rate = self._kokoro.create(
                text_clean,
                voice=effective_voice,
                speed=self.speed,
                lang=effective_lang,
            )

            audio = self._coerce_audio(samples)
            elapsed = time.time() - start
            duration = len(audio) / sample_rate

            kiwi_log(
                "KOKORO",
                f"Generated {duration:.2f}s audio in {elapsed:.2f}s "
                f"({duration / elapsed:.1f}x real-time) "
                f"voice={effective_voice} lang={effective_lang}",
            )

            if use_cache and duration < 30:
                self._set_cached(cache_key, audio, sample_rate)

            return audio, sample_rate

        except Exception as e:
            kiwi_log("KOKORO", f"Synthesis failed: {e}", level="ERROR")
            return None, 0
