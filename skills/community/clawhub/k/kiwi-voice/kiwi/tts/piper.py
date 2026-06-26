#!/usr/bin/env python3
"""Local Piper TTS client for Kiwi Voice."""

import hashlib
import os
import re
import time
from pathlib import Path
from typing import Any, Optional, Tuple

import numpy as np
import sounddevice as sd
from piper import PiperVoice

from kiwi.utils import kiwi_log
from kiwi import PROJECT_ROOT


class PiperTTS:
    """Ultra-fast local TTS using Piper with disk caching."""

    def __init__(self, model_path: str = None, cache_dir: str = None):
        if model_path is None:
            model_path = os.path.join(PROJECT_ROOT, 'piper-models', 'ru_RU-irina-medium.onnx')

        kiwi_log('PIPER', f'Loading model: {model_path}')
        start = time.time()
        self.voice = PiperVoice.load(model_path)
        kiwi_log('PIPER', f'Model loaded in {time.time()-start:.2f}s')
        self.sample_rate = 22050

        if cache_dir is None:
            cache_dir = os.path.join(PROJECT_ROOT, 'tts_cache')
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._cache_hits = 0
        self._cache_misses = 0
        kiwi_log('PIPER', f'TTS cache dir: {self.cache_dir}')

    def _get_cache_key(self, text: str) -> str:
        normalized = text.lower().strip()
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        return self.cache_dir / f"{cache_key}.npz"

    def _load_from_cache(self, cache_key: str) -> Tuple[Optional[np.ndarray], Optional[int]]:
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            try:
                data = np.load(cache_path)
                audio = data['audio']
                sample_rate = int(data['sample_rate'])
                self._cache_hits += 1
                return audio, sample_rate
            except Exception as e:
                kiwi_log('PIPER', f'Cache load error: {e}', level='ERROR')
                return None, None
        return None, None

    def _save_to_cache(self, cache_key: str, audio: np.ndarray, sample_rate: int):
        cache_path = self._get_cache_path(cache_key)
        try:
            np.savez_compressed(cache_path, audio=audio, sample_rate=sample_rate)
        except Exception as e:
            kiwi_log('PIPER', f'Cache save error: {e}', level='ERROR')

    def get_cache_stats(self) -> dict:
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0
        return {
            'hits': self._cache_hits,
            'misses': self._cache_misses,
            'hit_rate': hit_rate,
            'cached_files': len(list(self.cache_dir.glob('*.npz')))
        }

    def clear_cache(self) -> None:
        for f in self.cache_dir.glob('*.npz'):
            f.unlink()
        self._cache_hits = 0
        self._cache_misses = 0

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        style: str = "neutral",
        language: str = "Russian",
        use_cache: bool = True,
        **kwargs: Any,
    ) -> Tuple[Optional[np.ndarray], int]:
        """Synthesize text to audio. Extra params (voice, style, etc.) are ignored by Piper."""
        if not text or not text.strip():
            return None, self.sample_rate

        # Clean markdown before TTS
        text_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text_clean = re.sub(r'\*(.+?)\*', r'\1', text_clean)
        text_clean = re.sub(r'_(.+?)_', r'\1', text_clean)
        text_clean = re.sub(r'`(.+?)`', r'\1', text_clean)
        text_clean = text_clean.strip()

        cache_key = self._get_cache_key(text_clean)
        if use_cache:
            cached_audio, cached_sr = self._load_from_cache(cache_key)
            if cached_audio is not None:
                kiwi_log('PIPER', f'Cache hit! "{text_clean[:40]}..."')
                return cached_audio, cached_sr

        self._cache_misses += 1

        start = time.time()
        chunks = []

        for chunk in self.voice.synthesize(text_clean):
            arr = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            chunks.append(arr)

        if not chunks:
            return None, self.sample_rate

        audio = np.concatenate(chunks).astype(np.float32) / 32767.0
        elapsed = time.time() - start
        duration = len(audio) / self.sample_rate

        kiwi_log('PIPER', f'Generated {duration:.2f}s audio in {elapsed:.2f}s ({duration/elapsed:.1f}x real-time)')

        if use_cache and duration < 30:
            self._save_to_cache(cache_key, audio, self.sample_rate)

        return audio, self.sample_rate

    def play(self, text: str):
        audio, sr = self.synthesize(text)
        if audio is not None:
            sd.play(audio, sr)
            sd.wait()


if __name__ == '__main__':
    tts = PiperTTS()
    tts.play('Привет! Это локальная система TTS. Она работает мгновенно!')
