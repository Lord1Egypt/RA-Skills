#!/usr/bin/env python3
"""TTS Client for RunPod Qwen3-TTS Endpoint."""

import os
import base64
import time
import tempfile
from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass

import requests
import numpy as np
import soundfile as sf

from kiwi.tts.base import (
    STYLES,
    TTSCacheMixin,
    normalize_model_size,
    normalize_voice,
)
from kiwi.utils import kiwi_log


@dataclass
class TTSConfig:
    """TTS client configuration."""
    endpoint_id: str = ""
    api_key: str = ""
    default_voice: str = "Ono_Anna"
    model_size: str = "1.7B"
    timeout: int = 60
    poll_interval: float = 0.3
    cache_size: int = 100
    cache_ttl: int = 3600


class TTSClient(TTSCacheMixin):
    """RunPod TTS client with caching for realtime."""

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.config.default_voice = normalize_voice(self.config.default_voice)
        self.config.model_size = normalize_model_size(self.config.model_size)
        self.base_url = f"https://api.runpod.ai/v2/{self.config.endpoint_id}"
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

        self._cache_size = self.config.cache_size
        self._cache_ttl = self.config.cache_ttl
        self._init_cache()

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        style: str = "neutral",
        language: str = "Russian",
        use_cache: bool = True,
        **kwargs: Any,
    ) -> Tuple[Optional[np.ndarray], int]:
        voice = normalize_voice(voice or self.config.default_voice)
        model_size = normalize_model_size(kwargs.pop("model_size", None) or self.config.model_size)

        if use_cache:
            cache_key = self._make_cache_key(text, voice, style, language, model_size)
            cached = self._get_cached(cache_key)
            if cached:
                return cached

        instruct = kwargs.pop("instruct", None) or STYLES.get(style, STYLES["neutral"])

        payload = {
            "input": {
                "mode": "custom",
                "text": text,
                "speaker": voice,
                "instruct": instruct,
                "language": language,
                "model_size": model_size,
                **kwargs
            }
        }

        result = self._generate(payload)

        if use_cache and result[0] is not None:
            self._set_cached(cache_key, *result)

        return result

    # Backward compatibility alias
    def generate_custom_voice(self, text: str, **kwargs: Any) -> Tuple[Optional[np.ndarray], int]:
        return self.synthesize(text, **kwargs)

    def generate_voice_clone(
        self,
        text: str,
        ref_audio: str,
        ref_text: str,
        language: str = "Auto",
        x_vector_only_mode: bool = False,
        model_size: Optional[str] = None,
        **kwargs
    ) -> Tuple[Optional[np.ndarray], int]:
        if os.path.exists(ref_audio):
            with open(ref_audio, "rb") as f:
                ref_audio = base64.b64encode(f.read()).decode()

        payload = {
            "input": {
                "mode": "clone",
                "text": text,
                "ref_audio": ref_audio,
                "ref_text": ref_text,
                "language": language,
                "x_vector_only_mode": x_vector_only_mode,
                "model_size": normalize_model_size(model_size or self.config.model_size),
                **kwargs
            }
        }

        return self._generate(payload)

    def generate_voice_design(
        self,
        text: str,
        voice_description: str,
        language: str = "Auto",
        model_size: Optional[str] = None,
        **kwargs
    ) -> Tuple[Optional[np.ndarray], int]:
        payload = {
            "input": {
                "mode": "design",
                "text": text,
                "voice_description": voice_description,
                "language": language,
                "model_size": normalize_model_size(model_size or self.config.model_size),
                **kwargs
            }
        }

        return self._generate(payload)

    def _generate(self, payload: Dict[str, Any]) -> Tuple[Optional[np.ndarray], int]:
        try:
            response = requests.post(
                f"{self.base_url}/run",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            job = response.json()
            job_id = job.get("id")

            if not job_id:
                kiwi_log("RUNPOD", f"No job ID in response: {job}", level="ERROR")
                return None, 0

            return self._poll_result(job_id)

        except Exception as e:
            kiwi_log("RUNPOD", f"TTS request error: {e}", level="ERROR")
            return None, 0

    def _poll_result(self, job_id: str) -> Tuple[Optional[np.ndarray], int]:
        start_time = time.time()
        kiwi_log("RUNPOD", f"Job {job_id[:8]}... started")

        while time.time() - start_time < self.config.timeout:
            try:
                response = requests.get(
                    f"{self.base_url}/status/{job_id}",
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()

                status = response.json()
                current_status = status.get("status")

                if current_status == "COMPLETED":
                    elapsed = time.time() - start_time
                    kiwi_log("RUNPOD", f"Job {job_id[:8]} completed in {elapsed:.1f}s")
                    return self._extract_audio(status.get("output", {}))

                elif current_status == "FAILED":
                    error = status.get("error") or status.get("output", {}).get("error")
                    kiwi_log("RUNPOD", f"TTS job failed: {error}", level="ERROR")
                    return None, 0

                time.sleep(self.config.poll_interval)

            except Exception as e:
                kiwi_log("RUNPOD", f"Poll error: {e}", level="ERROR")
                time.sleep(self.config.poll_interval)

        elapsed = time.time() - start_time
        kiwi_log("RUNPOD", f"TTS timeout after {elapsed:.1f}s", level="ERROR")
        return None, 0

    def _extract_audio(self, output: Dict[str, Any]) -> Tuple[Optional[np.ndarray], int]:
        audio_data = output.get("audio", "")
        sample_rate = output.get("sample_rate", 24000)

        if not audio_data:
            kiwi_log("RUNPOD", "No audio in response", level="ERROR")
            return None, 0

        try:
            if audio_data.startswith("data:"):
                audio_data = audio_data.split(",", 1)[1]

            audio_bytes = base64.b64decode(audio_data)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio_bytes)
                temp_path = f.name

            try:
                audio, sr = sf.read(temp_path)
                return audio.astype(np.float32), sr
            finally:
                os.unlink(temp_path)

        except Exception as e:
            kiwi_log("RUNPOD", f"Audio decode error: {e}", level="ERROR")
            return None, 0

    def save_audio(self, audio: np.ndarray, sample_rate: int, path: str, format: str = "wav"):
        sf.write(path, audio, sample_rate, format=format)
        kiwi_log("RUNPOD", f"Saved: {path}")


def main():
    """Test run."""
    client = TTSClient()

    print("[TEST] Testing Custom Voice...")
    audio, sr = client.synthesize(
        text="Привет! Я - Киви, твой голосовой ИИ ассистент!",
        voice="Ono_Anna",
        style="cheerful",
        language="Russian"
    )

    if audio is not None:
        print(f"[TEST] Generated {len(audio)/sr:.2f}s audio @ {sr}Hz")
        from kiwi import PROJECT_ROOT
        output_path = os.path.join(PROJECT_ROOT, "test_output.wav")
        client.save_audio(audio, sr, output_path)
        import sounddevice as sd
        print("[TEST] Playing...")
        sd.play(audio, sr)
        sd.wait()
    else:
        print("[TEST] Generation failed")


if __name__ == "__main__":
    main()
