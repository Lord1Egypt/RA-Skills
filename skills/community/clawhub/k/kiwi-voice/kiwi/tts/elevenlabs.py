#!/usr/bin/env python3
"""ElevenLabs TTS client for Kiwi Voice."""

import io
import re
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import numpy as np
import requests
from pydub import AudioSegment

from kiwi.tts.base import TTSCacheMixin
from kiwi.utils import kiwi_log


DEFAULT_ELEVENLABS_VOICE_ID = "NhY0kyTmsKuEpHvDMngm"
DEFAULT_ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"

# Per-style presets for ElevenLabs voice_settings.
DEFAULT_ELEVENLABS_STYLE_PRESETS: Dict[str, Dict[str, float]] = {
    "neutral": {"stability": 0.55, "style": 0.20, "speed": 0.95},
    "calm": {"stability": 0.70, "style": 0.10, "speed": 0.90},
    "serious": {"stability": 0.65, "style": 0.05, "speed": 0.92},
    "confident": {"stability": 0.55, "style": 0.25, "speed": 0.98},
    "whisper": {"stability": 0.65, "style": 0.15, "speed": 0.88},
    "cheerful": {"stability": 0.45, "style": 0.50, "speed": 1.02},
    "excited": {"stability": 0.35, "style": 0.60, "speed": 1.05},
    "playful": {"stability": 0.40, "style": 0.70, "speed": 1.02},
    "sad": {"stability": 0.65, "style": 0.10, "speed": 0.90},
    "angry": {"stability": 0.30, "style": 0.65, "speed": 1.08},
}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize_elevenlabs_voice_id(value: Optional[str]) -> str:
    if not value:
        return DEFAULT_ELEVENLABS_VOICE_ID

    raw = str(value).strip()
    if not raw:
        return DEFAULT_ELEVENLABS_VOICE_ID

    if "voiceId=" in raw:
        try:
            parsed = urlparse(raw)
            query_value = parse_qs(parsed.query).get("voiceId", [])
            if query_value and query_value[0]:
                return query_value[0].strip()
        except Exception:
            pass

        match = re.search(r"voiceId=([A-Za-z0-9]+)", raw)
        if match:
            return match.group(1)

    return raw


@dataclass
class ElevenLabsTTSConfig:
    api_key: str = ""
    default_voice_id: str = DEFAULT_ELEVENLABS_VOICE_ID
    model_id: str = DEFAULT_ELEVENLABS_MODEL_ID
    output_format: str = "mp3_44100_128"
    timeout: int = 60
    use_streaming_endpoint: bool = True
    optimize_streaming_latency: int = 3
    stability: float = 0.45
    similarity_boost: float = 0.75
    style: float = 0.25
    use_speaker_boost: bool = True
    speed: float = 1.0
    ws_streaming: bool = True
    style_presets: Dict[str, Dict[str, float]] = field(
        default_factory=lambda: deepcopy(DEFAULT_ELEVENLABS_STYLE_PRESETS)
    )
    cache_size: int = 100
    cache_ttl: int = 3600


class ElevenLabsTTSClient(TTSCacheMixin):
    """ElevenLabs TTS with in-memory cache and streaming endpoint support."""

    def __init__(self, config: Optional[ElevenLabsTTSConfig] = None):
        self.config = config or ElevenLabsTTSConfig()
        self.config.default_voice_id = normalize_elevenlabs_voice_id(self.config.default_voice_id)
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"

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
        # Strip kwargs not relevant to ElevenLabs
        kwargs.pop("instruct", None)
        kwargs.pop("model_size", None)

        return self.generate_custom_voice(
            text=text,
            voice=voice,
            style=style,
            language=language,
            use_cache=use_cache,
            **kwargs,
        )

    def _build_voice_settings(self, style: str, overrides: Dict[str, Any]) -> Dict[str, Any]:
        configured_presets = self.config.style_presets if isinstance(self.config.style_presets, dict) else {}
        neutral_preset = configured_presets.get("neutral")
        if not isinstance(neutral_preset, dict):
            neutral_preset = DEFAULT_ELEVENLABS_STYLE_PRESETS["neutral"]
        preset = configured_presets.get(style)
        if not isinstance(preset, dict):
            preset = neutral_preset

        stability = float(overrides.get("stability", preset.get("stability", self.config.stability)))
        similarity_boost = float(overrides.get("similarity_boost", self.config.similarity_boost))
        style_value = float(overrides.get("style_value", overrides.get("style", preset.get("style", self.config.style))))
        speed = float(overrides.get("speed", preset.get("speed", self.config.speed)))
        use_speaker_boost = bool(overrides.get("use_speaker_boost", self.config.use_speaker_boost))

        return {
            "stability": _clamp(stability, 0.0, 1.0),
            "similarity_boost": _clamp(similarity_boost, 0.0, 1.0),
            "style": _clamp(style_value, 0.0, 1.0),
            "use_speaker_boost": use_speaker_boost,
            "speed": _clamp(speed, 0.7, 1.2),
        }

    @staticmethod
    def _parse_pcm_sample_rate(output_format: str) -> Optional[int]:
        match = re.match(r"^pcm_(\d+)$", output_format.strip().lower())
        if not match:
            return None
        return int(match.group(1))

    def _decode_audio_bytes(self, audio_bytes: bytes, output_format: str) -> Tuple[Optional[np.ndarray], int]:
        pcm_sample_rate = self._parse_pcm_sample_rate(output_format)
        if pcm_sample_rate:
            audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            return audio, pcm_sample_rate

        try:
            if output_format.startswith("mp3_"):
                segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
            else:
                segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        except Exception as exc:
            kiwi_log("ELEVENLABS", f"Audio decode error: {exc}", level="ERROR")
            return None, 0

        samples = np.array(segment.get_array_of_samples(), dtype=np.float32)
        if segment.channels > 1:
            samples = samples.reshape((-1, segment.channels)).mean(axis=1)
        scale = float(1 << (8 * segment.sample_width - 1))
        audio = samples / scale
        return self._coerce_audio(audio), int(segment.frame_rate)

    def _request_audio_bytes(
        self,
        endpoint_path: str,
        headers: Dict[str, str],
        params: Dict[str, Any],
        payload: Dict[str, Any],
        endpoint_streaming: bool,
    ) -> bytes:
        response = requests.post(
            endpoint_path,
            headers=headers,
            params=params,
            json=payload,
            stream=endpoint_streaming,
            timeout=(15, self.config.timeout),
        )
        response.raise_for_status()

        if endpoint_streaming:
            chunks = []
            for chunk in response.iter_content(chunk_size=16384):
                if chunk:
                    chunks.append(chunk)
            return b"".join(chunks)
        return response.content

    def generate_custom_voice(
        self,
        text: str,
        voice: Optional[str] = None,
        style: str = "neutral",
        instruct: Optional[str] = None,
        language: str = "Russian",
        use_cache: bool = True,
        model_size: Optional[str] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[np.ndarray], int]:
        del instruct, language, model_size  # not used by ElevenLabs endpoint

        if not text or not text.strip():
            return None, 0

        if not self.config.api_key:
            kiwi_log("ELEVENLABS", "API key is empty", level="ERROR")
            return None, 0

        voice_id = normalize_elevenlabs_voice_id(voice or self.config.default_voice_id)
        model_id = str(kwargs.get("model_id") or self.config.model_id).strip() or DEFAULT_ELEVENLABS_MODEL_ID
        output_format = str(kwargs.get("output_format") or self.config.output_format).strip() or "mp3_44100_128"
        endpoint_streaming = bool(kwargs.get("use_streaming_endpoint", self.config.use_streaming_endpoint))
        optimize_streaming_latency = int(
            kwargs.get("optimize_streaming_latency", self.config.optimize_streaming_latency)
        )

        voice_settings = self._build_voice_settings(style=style, overrides=kwargs)
        cache_key = self._make_cache_key(
            text, voice_id, style, model_id, output_format,
            f"{float(voice_settings.get('speed', 1.0)):.4f}",
        )

        if use_cache:
            cached = self._get_cached(cache_key)
            if cached is not None:
                return cached

        payload: Dict[str, Any] = {
            "text": text,
            "model_id": model_id,
            "voice_settings": voice_settings,
        }
        if kwargs.get("seed") is not None:
            payload["seed"] = int(kwargs["seed"])

        endpoint_path = f"{self.base_url}/{voice_id}"
        params: Dict[str, Any] = {"output_format": output_format}
        if endpoint_streaming:
            endpoint_path = f"{endpoint_path}/stream"
            params["optimize_streaming_latency"] = optimize_streaming_latency

        headers = {
            "xi-api-key": self.config.api_key,
            "Accept": "application/octet-stream",
            "Content-Type": "application/json",
        }

        try:
            audio_bytes = self._request_audio_bytes(
                endpoint_path=endpoint_path,
                headers=headers,
                params=params,
                payload=payload,
                endpoint_streaming=endpoint_streaming,
            )
        except requests.HTTPError:
            voice_settings = dict(payload.get("voice_settings") or {})
            if "style" in voice_settings or "speed" in voice_settings:
                fallback_payload = dict(payload)
                fallback_voice_settings = dict(voice_settings)
                fallback_voice_settings.pop("style", None)
                fallback_voice_settings.pop("speed", None)
                fallback_payload["voice_settings"] = fallback_voice_settings
                try:
                    audio_bytes = self._request_audio_bytes(
                        endpoint_path=endpoint_path,
                        headers=headers,
                        params=params,
                        payload=fallback_payload,
                        endpoint_streaming=endpoint_streaming,
                    )
                except Exception as fallback_exc:
                    kiwi_log("ELEVENLABS", f"Request failed: {fallback_exc}", level="ERROR")
                    return None, 0
            else:
                kiwi_log("ELEVENLABS", "Request failed", level="ERROR")
                return None, 0
        except Exception as exc:
            kiwi_log("ELEVENLABS", f"Request failed: {exc}", level="ERROR")
            return None, 0

        if not audio_bytes:
            kiwi_log("ELEVENLABS", "Empty audio payload", level="ERROR")
            return None, 0

        audio, sample_rate = self._decode_audio_bytes(audio_bytes, output_format=output_format)
        if audio is None:
            return None, 0

        if use_cache and audio.size > 0:
            self._set_cached(cache_key, audio, sample_rate)
        return audio, sample_rate
