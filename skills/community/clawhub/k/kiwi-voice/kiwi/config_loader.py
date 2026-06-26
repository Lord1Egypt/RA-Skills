#!/usr/bin/env python3
"""Configuration loader for Kiwi Voice."""

import os
import re
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field

from kiwi.utils import kiwi_log
from kiwi.tts.base import normalize_model_size as normalize_qwen_model_size, normalize_voice as normalize_qwen_voice
from kiwi.tts.elevenlabs import (
    normalize_elevenlabs_voice_id,
    DEFAULT_ELEVENLABS_VOICE_ID,
    DEFAULT_ELEVENLABS_MODEL_ID,
    DEFAULT_ELEVENLABS_STYLE_PRESETS,
)


def load_config_yaml(config_path: str = "config.yaml") -> dict:
    """Load configuration from a YAML file."""
    import yaml
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            kiwi_log("CONFIG", f"Warning: Failed to load {config_path}: {e}", level="WARNING")
    return {}


def check_cuda_available() -> bool:
    """Check CUDA availability for Whisper."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


@dataclass
class KiwiConfig:
    openclaw_bin: str = "openclaw"
    """Kiwi service configuration."""
    openclaw_session_id: str = "kiwi-voice"  # Separate session for voice
    openclaw_agent: Optional[str] = None
    openclaw_timeout: int = 120

    # Language / i18n — controls UI strings, STT locale, TTS locale
    language: str = "ru"

    # Voice system prompt - set on first connection (populated from i18n if empty)
    voice_system_prompt: str = ""

    # Soul system
    soul_default: str = "mindful-companion"
    soul_nsfw_model: str = "openrouter/mistralai/mistral-7b-instruct"
    soul_nsfw_session: str = ""  # OpenClaw session ID for NSFW soul (empty = same session)

    # LLM settings
    llm_model: str = "openrouter/moonshotai/kimi-k2.5"
    llm_filter_timeout: int = 15
    llm_filter_subprocess_timeout: int = 20
    llm_stream_stall_timeout: float = 12.0
    llm_stream_stall_retry_max: int = 1

    # Retry settings for rate_limit errors
    llm_retry_max: int = 3
    llm_retry_delays: list = None

    def __post_init__(self):
        if self.llm_retry_delays is None:
            self.llm_retry_delays = [0.5, 1.0, 2.0]

    # WebSocket settings
    ws_enabled: bool = True
    ws_port: int = 18789
    ws_host: str = "localhost"
    ws_reconnect_interval: float = 3.0
    ws_max_reconnect_attempts: int = 10
    ws_ping_interval: float = 30.0
    ws_ping_timeout: float = 20.0

    # TTS settings
    # provider: "qwen3" | "piper" | "elevenlabs" | "kokoro"
    # qwen backend: "runpod" | "local"
    tts_provider: str = "qwen3"
    tts_qwen_backend: str = "runpod"
    use_local_tts: bool = False  # legacy compatibility switch
    tts_endpoint_id: str = ""
    tts_api_key: str = ""
    tts_voice: str = "Ono_Anna"
    tts_model_size: str = "1.7B"
    tts_default_style: str = "neutral"
    tts_timeout: int = 60
    tts_poll_interval: float = 0.3
    tts_local_model_path: Optional[str] = None
    tts_local_tokenizer_path: Optional[str] = None
    tts_qwen_device: str = "auto"
    tts_piper_model_path: Optional[str] = None
    tts_elevenlabs_api_key: str = ""
    tts_elevenlabs_voice_id: str = DEFAULT_ELEVENLABS_VOICE_ID
    tts_elevenlabs_model_id: str = DEFAULT_ELEVENLABS_MODEL_ID
    tts_elevenlabs_output_format: str = "mp3_44100_128"
    tts_elevenlabs_use_streaming_endpoint: bool = True
    tts_elevenlabs_optimize_streaming_latency: int = 3
    tts_elevenlabs_stability: float = 0.45
    tts_elevenlabs_similarity_boost: float = 0.75
    tts_elevenlabs_style: float = 0.25
    tts_elevenlabs_use_speaker_boost: bool = True
    tts_elevenlabs_speed: float = 1.0
    tts_elevenlabs_ws_streaming: bool = True
    tts_elevenlabs_style_presets: Dict[str, Dict[str, float]] = field(
        default_factory=lambda: {
            style_name: dict(style_values)
            for style_name, style_values in DEFAULT_ELEVENLABS_STYLE_PRESETS.items()
        }
    )

    # Kokoro TTS settings
    tts_kokoro_voice: str = "af_heart"
    tts_kokoro_speed: float = 1.0
    tts_kokoro_model_dir: Optional[str] = None

    stt_model: str = "base"
    stt_device: str = "cpu"
    stt_compute_type: str = "int8"
    stt_language: str = "ru"

    # STT engine: "faster-whisper" | "mlx-whisper" | "elevenlabs"
    stt_engine: str = "faster-whisper"
    stt_mlx_batch_size: int = 12

    # ElevenLabs STT settings
    stt_elevenlabs_api_key: str = ""
    stt_elevenlabs_model_id: str = "scribe_v2"
    stt_elevenlabs_language_code: str = ""  # auto-detect if empty

    sample_rate: int = 24000
    output_device: Optional[str] = None
    input_device: Optional[str] = None
    wake_word_keyword: str = "киви"
    wake_word_position_limit: int = 3
    # Wake word engine: "text" (legacy fuzzy match) | "openwakeword" (ML model)
    wake_word_engine: str = "text"
    wake_word_model: str = "hey_jarvis"
    wake_word_threshold: float = 0.5

    # Owner name (from speaker_priority.owner.name in config.yaml)
    owner_name: str = "Owner"

    # REST API server
    api_enabled: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 7789
    api_auth_enabled: bool = False
    api_auth_tokens: List[Dict[str, Any]] = field(default_factory=list)

    # Web Audio (browser microphone via WebSocket)
    web_audio_enabled: bool = True
    web_audio_sample_rate: int = 16000
    web_audio_max_clients: int = 3

    # Home Assistant integration
    ha_enabled: bool = False
    ha_url: str = ""
    ha_token: str = ""
    ha_language: str = ""  # defaults to config.language at runtime

    @staticmethod
    def _sync_local_qwen_model_path(model_path: Optional[str], model_size: str) -> str:
        """Keep local Qwen path aligned with selected model size."""
        normalized_size = normalize_qwen_model_size(model_size)
        if not model_path:
            return f"./models/Qwen3-TTS-12Hz-{normalized_size}-CustomVoice"

        path = str(model_path).strip()
        pattern = r"(Qwen3-TTS-12Hz-)(0\.6B|1\.7B)(-CustomVoice)"
        if re.search(pattern, path):
            return re.sub(pattern, rf"\g<1>{normalized_size}\g<3>", path)
        return path

    @classmethod
    def from_yaml(cls, yaml_config: dict) -> "KiwiConfig":
        """Create config from YAML + env vars."""
        config = cls()

        # Language / i18n
        config.language = str(yaml_config.get("language", config.language)).strip() or "ru"

        stt_cfg = yaml_config.get("stt", {})
        tts_cfg = yaml_config.get("tts", {})
        eleven_cfg = tts_cfg.get("elevenlabs", {}) if isinstance(tts_cfg.get("elevenlabs", {}), dict) else {}
        audio_cfg = yaml_config.get("audio", {})
        wake_cfg = yaml_config.get("wake_word", {})
        llm_cfg = yaml_config.get("llm", {})
        ws_cfg = yaml_config.get("websocket", {})

        config.stt_model = stt_cfg.get("model", config.stt_model)
        config.stt_device = stt_cfg.get("device", config.stt_device)
        config.stt_compute_type = stt_cfg.get("compute_type", config.stt_compute_type)
        config.stt_language = stt_cfg.get("language", config.stt_language)
        config.stt_engine = str(stt_cfg.get("engine", config.stt_engine)).strip().lower()
        config.stt_mlx_batch_size = int(stt_cfg.get("mlx_batch_size", config.stt_mlx_batch_size))

        # ElevenLabs STT config
        el_stt_cfg = stt_cfg.get("elevenlabs", {}) if isinstance(stt_cfg.get("elevenlabs"), dict) else {}
        config.stt_elevenlabs_api_key = str(el_stt_cfg.get("api_key", config.stt_elevenlabs_api_key))
        config.stt_elevenlabs_model_id = str(el_stt_cfg.get("model_id", config.stt_elevenlabs_model_id))
        config.stt_elevenlabs_language_code = str(el_stt_cfg.get("language_code", config.stt_elevenlabs_language_code))

        raw_use_local_tts = tts_cfg.get("use_local_tts", config.use_local_tts)
        if isinstance(raw_use_local_tts, str):
            config.use_local_tts = raw_use_local_tts.strip().lower() in ("true", "1", "yes")
        else:
            config.use_local_tts = bool(raw_use_local_tts)
        config.tts_provider = str(tts_cfg.get("provider", config.tts_provider)).strip().lower()
        config.tts_qwen_backend = str(tts_cfg.get("qwen_backend", config.tts_qwen_backend)).strip().lower()
        config.tts_voice = tts_cfg.get("voice", config.tts_voice)
        config.tts_model_size = tts_cfg.get("model_size", config.tts_model_size)
        config.tts_default_style = tts_cfg.get("default_style", config.tts_default_style)
        config.tts_endpoint_id = tts_cfg.get("endpoint_id", config.tts_endpoint_id)
        config.tts_api_key = tts_cfg.get("api_key", config.tts_api_key)
        config.tts_timeout = int(tts_cfg.get("timeout", config.tts_timeout))
        config.tts_poll_interval = float(tts_cfg.get("poll_interval", config.tts_poll_interval))
        config.tts_local_model_path = tts_cfg.get("local_model_path", config.tts_local_model_path)
        config.tts_local_tokenizer_path = tts_cfg.get("local_tokenizer_path", config.tts_local_tokenizer_path)
        config.tts_qwen_device = tts_cfg.get("qwen_device", config.tts_qwen_device)
        config.tts_piper_model_path = tts_cfg.get("piper_model_path", config.tts_piper_model_path)
        # Kokoro TTS settings
        kokoro_cfg = tts_cfg.get("kokoro", {}) if isinstance(tts_cfg.get("kokoro"), dict) else {}
        config.tts_kokoro_voice = str(
            kokoro_cfg.get("voice", tts_cfg.get("kokoro_voice", config.tts_kokoro_voice))
        ).strip()
        config.tts_kokoro_speed = float(
            kokoro_cfg.get("speed", tts_cfg.get("kokoro_speed", config.tts_kokoro_speed))
        )
        kokoro_model_dir = kokoro_cfg.get("model_dir", tts_cfg.get("kokoro_model_dir", config.tts_kokoro_model_dir))
        if kokoro_model_dir:
            config.tts_kokoro_model_dir = str(kokoro_model_dir).strip()
        config.tts_elevenlabs_api_key = eleven_cfg.get(
            "api_key",
            tts_cfg.get("elevenlabs_api_key", config.tts_elevenlabs_api_key),
        )
        config.tts_elevenlabs_voice_id = eleven_cfg.get(
            "voice_id",
            tts_cfg.get("elevenlabs_voice_id", config.tts_elevenlabs_voice_id),
        )
        config.tts_elevenlabs_model_id = eleven_cfg.get(
            "model_id",
            tts_cfg.get("elevenlabs_model_id", config.tts_elevenlabs_model_id),
        )
        config.tts_elevenlabs_output_format = eleven_cfg.get(
            "output_format",
            tts_cfg.get("elevenlabs_output_format", config.tts_elevenlabs_output_format),
        )
        raw_streaming_endpoint = eleven_cfg.get(
            "use_streaming_endpoint",
            tts_cfg.get("elevenlabs_use_streaming_endpoint", config.tts_elevenlabs_use_streaming_endpoint),
        )
        if isinstance(raw_streaming_endpoint, str):
            config.tts_elevenlabs_use_streaming_endpoint = raw_streaming_endpoint.strip().lower() in ("true", "1", "yes")
        else:
            config.tts_elevenlabs_use_streaming_endpoint = bool(raw_streaming_endpoint)
        config.tts_elevenlabs_optimize_streaming_latency = int(
            eleven_cfg.get(
                "optimize_streaming_latency",
                tts_cfg.get(
                    "elevenlabs_optimize_streaming_latency",
                    config.tts_elevenlabs_optimize_streaming_latency,
                ),
            )
        )
        config.tts_elevenlabs_stability = float(
            eleven_cfg.get("stability", tts_cfg.get("elevenlabs_stability", config.tts_elevenlabs_stability))
        )
        config.tts_elevenlabs_similarity_boost = float(
            eleven_cfg.get(
                "similarity_boost",
                tts_cfg.get("elevenlabs_similarity_boost", config.tts_elevenlabs_similarity_boost),
            )
        )
        config.tts_elevenlabs_style = float(
            eleven_cfg.get("style", tts_cfg.get("elevenlabs_style", config.tts_elevenlabs_style))
        )
        raw_use_speaker_boost = eleven_cfg.get(
            "use_speaker_boost",
            tts_cfg.get("elevenlabs_use_speaker_boost", config.tts_elevenlabs_use_speaker_boost),
        )
        if isinstance(raw_use_speaker_boost, str):
            config.tts_elevenlabs_use_speaker_boost = raw_use_speaker_boost.strip().lower() in ("true", "1", "yes")
        else:
            config.tts_elevenlabs_use_speaker_boost = bool(raw_use_speaker_boost)
        config.tts_elevenlabs_speed = float(
            eleven_cfg.get("speed", tts_cfg.get("elevenlabs_speed", config.tts_elevenlabs_speed))
        )
        raw_ws_streaming = eleven_cfg.get(
            "ws_streaming",
            tts_cfg.get("elevenlabs_ws_streaming", config.tts_elevenlabs_ws_streaming),
        )
        if isinstance(raw_ws_streaming, str):
            config.tts_elevenlabs_ws_streaming = raw_ws_streaming.strip().lower() in ("true", "1", "yes")
        else:
            config.tts_elevenlabs_ws_streaming = bool(raw_ws_streaming)
        raw_style_presets = eleven_cfg.get(
            "style_presets",
            tts_cfg.get("elevenlabs_style_presets", config.tts_elevenlabs_style_presets),
        )
        if isinstance(raw_style_presets, dict):
            parsed_style_presets: Dict[str, Dict[str, float]] = {}
            for raw_style_name, raw_style_values in raw_style_presets.items():
                if not isinstance(raw_style_values, dict):
                    continue
                style_name = str(raw_style_name).strip().lower()
                if not style_name:
                    continue

                values: Dict[str, float] = {}
                for key in ("stability", "style", "speed"):
                    if key not in raw_style_values:
                        continue
                    try:
                        values[key] = float(raw_style_values[key])
                    except (TypeError, ValueError):
                        continue

                if values:
                    parsed_style_presets[style_name] = values
            if parsed_style_presets:
                config.tts_elevenlabs_style_presets = parsed_style_presets

        config.sample_rate = audio_cfg.get("sample_rate", config.sample_rate)
        config.output_device = audio_cfg.get("output_device", config.output_device)
        config.input_device = audio_cfg.get("input_device", config.input_device)
        if isinstance(wake_cfg, dict):
            config.wake_word_keyword = str(
                wake_cfg.get("keyword", config.wake_word_keyword)
            ).strip() or "киви"
            config.wake_word_position_limit = int(
                wake_cfg.get("position_limit", config.wake_word_position_limit)
            )
            config.wake_word_engine = str(
                wake_cfg.get("engine", config.wake_word_engine)
            ).strip().lower()
            config.wake_word_model = str(
                wake_cfg.get("model", config.wake_word_model)
            ).strip()
            config.wake_word_threshold = float(
                wake_cfg.get("threshold", config.wake_word_threshold)
            )

        # LLM settings from YAML
        config.llm_model = llm_cfg.get("model", config.llm_model)
        config.llm_filter_timeout = llm_cfg.get("filter_timeout", config.llm_filter_timeout)
        config.llm_filter_subprocess_timeout = llm_cfg.get("filter_subprocess_timeout", config.llm_filter_subprocess_timeout)
        config.llm_stream_stall_timeout = float(
            llm_cfg.get("stream_stall_timeout", config.llm_stream_stall_timeout)
        )
        config.llm_stream_stall_retry_max = int(
            llm_cfg.get("stream_stall_retry_max", config.llm_stream_stall_retry_max)
        )
        if llm_cfg.get("chat_timeout"):
            config.openclaw_timeout = llm_cfg.get("chat_timeout")
        config.llm_retry_max = llm_cfg.get("retry_max", config.llm_retry_max)
        config.llm_retry_delays = llm_cfg.get("retry_delays", config.llm_retry_delays)

        # Voice system prompt from YAML
        if llm_cfg.get("voice_system_prompt"):
            config.voice_system_prompt = llm_cfg.get("voice_system_prompt")

        # Souls configuration
        souls_cfg = yaml_config.get("souls", {})
        if souls_cfg:
            config.soul_default = souls_cfg.get("default", config.soul_default)
            nsfw_cfg = souls_cfg.get("nsfw", {})
            if isinstance(nsfw_cfg, dict):
                if nsfw_cfg.get("model"):
                    config.soul_nsfw_model = nsfw_cfg.get("model", config.soul_nsfw_model)
                if nsfw_cfg.get("session"):
                    config.soul_nsfw_session = nsfw_cfg.get("session", config.soul_nsfw_session)

        # WebSocket settings from YAML
        config.ws_enabled = ws_cfg.get("enabled", config.ws_enabled)
        config.ws_port = ws_cfg.get("port", config.ws_port)
        config.ws_host = ws_cfg.get("host", config.ws_host)
        config.ws_reconnect_interval = ws_cfg.get("reconnect_interval", config.ws_reconnect_interval)
        config.ws_max_reconnect_attempts = ws_cfg.get("max_reconnect_attempts", config.ws_max_reconnect_attempts)
        config.ws_ping_interval = float(ws_cfg.get("ping_interval", config.ws_ping_interval))
        config.ws_ping_timeout = float(ws_cfg.get("ping_timeout", config.ws_ping_timeout))

        # REST API settings from YAML
        api_cfg = yaml_config.get("api", {})
        if isinstance(api_cfg, dict):
            raw_api_enabled = api_cfg.get("enabled", config.api_enabled)
            if isinstance(raw_api_enabled, str):
                config.api_enabled = raw_api_enabled.strip().lower() in ("true", "1", "yes")
            else:
                config.api_enabled = bool(raw_api_enabled)
            config.api_host = str(api_cfg.get("host", config.api_host)).strip()
            config.api_port = int(api_cfg.get("port", config.api_port))

        # API auth settings
        auth_cfg = api_cfg.get("auth", {}) if isinstance(api_cfg, dict) else {}
        if isinstance(auth_cfg, dict):
            raw_auth_enabled = auth_cfg.get("enabled", config.api_auth_enabled)
            if isinstance(raw_auth_enabled, str):
                config.api_auth_enabled = raw_auth_enabled.strip().lower() in ("true", "1", "yes")
            else:
                config.api_auth_enabled = bool(raw_auth_enabled)
            raw_tokens = auth_cfg.get("tokens", [])
            if isinstance(raw_tokens, list):
                config.api_auth_tokens = [
                    {"token": str(t["token"]), "name": str(t.get("name", "")), "scopes": list(t.get("scopes", []))}
                    for t in raw_tokens
                    if isinstance(t, dict) and t.get("token")
                ]

        # Env var overrides for API
        if os.getenv("KIWI_API_AUTH_ENABLED"):
            config.api_auth_enabled = os.getenv("KIWI_API_AUTH_ENABLED").strip().lower() in ("true", "1", "yes")
        if os.getenv("KIWI_API_ENABLED"):
            config.api_enabled = os.getenv("KIWI_API_ENABLED").strip().lower() in ("true", "1", "yes")
        if os.getenv("KIWI_API_HOST"):
            config.api_host = os.getenv("KIWI_API_HOST").strip()
        if os.getenv("KIWI_API_PORT"):
            config.api_port = int(os.getenv("KIWI_API_PORT"))

        # Web Audio settings
        web_audio_cfg = yaml_config.get("web_audio", {})
        if isinstance(web_audio_cfg, dict):
            raw_wa_enabled = web_audio_cfg.get("enabled", config.web_audio_enabled)
            if isinstance(raw_wa_enabled, str):
                config.web_audio_enabled = raw_wa_enabled.strip().lower() in ("true", "1", "yes")
            else:
                config.web_audio_enabled = bool(raw_wa_enabled)
            config.web_audio_sample_rate = int(web_audio_cfg.get("sample_rate", config.web_audio_sample_rate))
            config.web_audio_max_clients = int(web_audio_cfg.get("max_clients", config.web_audio_max_clients))

        # Env var overrides for Web Audio
        if os.getenv("KIWI_WEB_AUDIO_ENABLED"):
            config.web_audio_enabled = os.getenv("KIWI_WEB_AUDIO_ENABLED").strip().lower() in ("true", "1", "yes")

        # Home Assistant integration
        ha_cfg = yaml_config.get("homeassistant", {})
        if isinstance(ha_cfg, dict):
            raw_ha_enabled = ha_cfg.get("enabled", config.ha_enabled)
            if isinstance(raw_ha_enabled, str):
                config.ha_enabled = raw_ha_enabled.strip().lower() in ("true", "1", "yes")
            else:
                config.ha_enabled = bool(raw_ha_enabled)
            config.ha_url = str(ha_cfg.get("url", config.ha_url)).strip()
            config.ha_token = str(ha_cfg.get("token", config.ha_token)).strip()
            config.ha_language = str(ha_cfg.get("language", config.ha_language)).strip()

        # Env var overrides for HA
        if os.getenv("KIWI_HA_ENABLED"):
            config.ha_enabled = os.getenv("KIWI_HA_ENABLED").strip().lower() in ("true", "1", "yes")
        if os.getenv("KIWI_HA_URL"):
            config.ha_url = os.getenv("KIWI_HA_URL").strip()
        if os.getenv("KIWI_HA_TOKEN"):
            config.ha_token = os.getenv("KIWI_HA_TOKEN").strip()
        if os.getenv("KIWI_HA_LANGUAGE"):
            config.ha_language = os.getenv("KIWI_HA_LANGUAGE").strip()

        # Default HA language to main language
        if not config.ha_language:
            config.ha_language = config.language

        # Soul env var overrides
        if os.getenv("KIWI_SOUL_DEFAULT"):
            config.soul_default = os.getenv("KIWI_SOUL_DEFAULT").strip()
        if os.getenv("KIWI_SOUL_NSFW_MODEL"):
            config.soul_nsfw_model = os.getenv("KIWI_SOUL_NSFW_MODEL").strip()
        if os.getenv("KIWI_SOUL_NSFW_SESSION"):
            config.soul_nsfw_session = os.getenv("KIWI_SOUL_NSFW_SESSION").strip()

        if os.getenv("KIWI_LANGUAGE"):
            config.language = os.getenv("KIWI_LANGUAGE").strip() or "ru"

        if os.getenv("RUNPOD_TTS_ENDPOINT_ID"):
            config.tts_endpoint_id = os.getenv("RUNPOD_TTS_ENDPOINT_ID")
        if os.getenv("RUNPOD_API_KEY"):
            config.tts_api_key = os.getenv("RUNPOD_API_KEY")
        if os.getenv("ELEVENLABS_API_KEY"):
            config.tts_elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if os.getenv("OPENCLAW_BIN"):
            config.openclaw_bin = os.getenv("OPENCLAW_BIN")
        if os.getenv("OPENCLAW_SESSION_ID"):
            config.openclaw_session_id = os.getenv("OPENCLAW_SESSION_ID")
        if os.getenv("OPENCLAW_AGENT"):
            config.openclaw_agent = os.getenv("OPENCLAW_AGENT")
        if os.getenv("OPENCLAW_TIMEOUT"):
            config.openclaw_timeout = int(os.getenv("OPENCLAW_TIMEOUT"))
        if os.getenv("LLM_MODEL"):
            config.llm_model = os.getenv("LLM_MODEL")
        if os.getenv("KIWI_STREAM_STALL_TIMEOUT"):
            config.llm_stream_stall_timeout = float(os.getenv("KIWI_STREAM_STALL_TIMEOUT"))
        if os.getenv("KIWI_STREAM_STALL_RETRY_MAX"):
            config.llm_stream_stall_retry_max = int(os.getenv("KIWI_STREAM_STALL_RETRY_MAX"))
        if os.getenv("KIWI_WS_ENABLED"):
            config.ws_enabled = os.getenv("KIWI_WS_ENABLED").lower() in ("true", "1", "yes")
        if os.getenv("KIWI_WS_PORT"):
            config.ws_port = int(os.getenv("KIWI_WS_PORT"))
        if os.getenv("KIWI_WS_HOST"):
            config.ws_host = os.getenv("KIWI_WS_HOST")
        if os.getenv("KIWI_WS_PING_INTERVAL"):
            config.ws_ping_interval = float(os.getenv("KIWI_WS_PING_INTERVAL"))
        if os.getenv("KIWI_WS_PING_TIMEOUT"):
            config.ws_ping_timeout = float(os.getenv("KIWI_WS_PING_TIMEOUT"))
        if os.getenv("KIWI_WAKE_WORD"):
            config.wake_word_keyword = os.getenv("KIWI_WAKE_WORD").strip() or "киви"
        if os.getenv("KIWI_WAKE_POSITION_LIMIT"):
            config.wake_word_position_limit = int(os.getenv("KIWI_WAKE_POSITION_LIMIT"))
        if os.getenv("KIWI_WAKE_ENGINE"):
            config.wake_word_engine = os.getenv("KIWI_WAKE_ENGINE").strip().lower()
        if os.getenv("KIWI_WAKE_MODEL"):
            config.wake_word_model = os.getenv("KIWI_WAKE_MODEL").strip()
        if os.getenv("KIWI_WAKE_THRESHOLD"):
            config.wake_word_threshold = float(os.getenv("KIWI_WAKE_THRESHOLD"))
        if os.getenv("KIWI_STT_ENGINE"):
            config.stt_engine = os.getenv("KIWI_STT_ENGINE").strip().lower()

        # ElevenLabs STT API key: dedicated env var → TTS key fallback
        config.stt_elevenlabs_api_key = (
            os.environ.get("KIWI_ELEVENLABS_STT_API_KEY", "").strip()
            or config.stt_elevenlabs_api_key
            or config.tts_elevenlabs_api_key
        )

        if os.getenv("KIWI_USE_LOCAL_TTS"):
            config.use_local_tts = os.getenv("KIWI_USE_LOCAL_TTS").lower() in ("true", "1", "yes")
        if os.getenv("KIWI_TTS_PROVIDER"):
            config.tts_provider = os.getenv("KIWI_TTS_PROVIDER").strip().lower()
        if os.getenv("KIWI_QWEN_BACKEND"):
            config.tts_qwen_backend = os.getenv("KIWI_QWEN_BACKEND").strip().lower()
        if os.getenv("KIWI_TTS_VOICE"):
            config.tts_voice = os.getenv("KIWI_TTS_VOICE").strip()
        if os.getenv("KIWI_TTS_MODEL_SIZE"):
            config.tts_model_size = os.getenv("KIWI_TTS_MODEL_SIZE").strip()
        if os.getenv("KIWI_TTS_TIMEOUT"):
            config.tts_timeout = int(os.getenv("KIWI_TTS_TIMEOUT"))
        if os.getenv("KIWI_TTS_POLL_INTERVAL"):
            config.tts_poll_interval = float(os.getenv("KIWI_TTS_POLL_INTERVAL"))
        if os.getenv("KIWI_TTS_LOCAL_MODEL_PATH"):
            config.tts_local_model_path = os.getenv("KIWI_TTS_LOCAL_MODEL_PATH").strip()
        if os.getenv("KIWI_TTS_LOCAL_TOKENIZER_PATH"):
            config.tts_local_tokenizer_path = os.getenv("KIWI_TTS_LOCAL_TOKENIZER_PATH").strip()
        if os.getenv("KIWI_TTS_QWEN_DEVICE"):
            config.tts_qwen_device = os.getenv("KIWI_TTS_QWEN_DEVICE").strip().lower()
        if os.getenv("KIWI_TTS_PIPER_MODEL_PATH"):
            config.tts_piper_model_path = os.getenv("KIWI_TTS_PIPER_MODEL_PATH").strip()
        if os.getenv("KIWI_ELEVENLABS_API_KEY"):
            config.tts_elevenlabs_api_key = os.getenv("KIWI_ELEVENLABS_API_KEY").strip()
        if os.getenv("KIWI_ELEVENLABS_VOICE_ID"):
            config.tts_elevenlabs_voice_id = os.getenv("KIWI_ELEVENLABS_VOICE_ID").strip()
        if os.getenv("KIWI_ELEVENLABS_MODEL_ID"):
            config.tts_elevenlabs_model_id = os.getenv("KIWI_ELEVENLABS_MODEL_ID").strip()
        if os.getenv("KIWI_ELEVENLABS_OUTPUT_FORMAT"):
            config.tts_elevenlabs_output_format = os.getenv("KIWI_ELEVENLABS_OUTPUT_FORMAT").strip()
        if os.getenv("KIWI_ELEVENLABS_STREAMING_ENDPOINT"):
            config.tts_elevenlabs_use_streaming_endpoint = os.getenv("KIWI_ELEVENLABS_STREAMING_ENDPOINT").strip().lower() in ("true", "1", "yes")
        if os.getenv("KIWI_ELEVENLABS_OPTIMIZE_STREAMING_LATENCY"):
            config.tts_elevenlabs_optimize_streaming_latency = int(os.getenv("KIWI_ELEVENLABS_OPTIMIZE_STREAMING_LATENCY"))
        if os.getenv("KIWI_ELEVENLABS_STABILITY"):
            config.tts_elevenlabs_stability = float(os.getenv("KIWI_ELEVENLABS_STABILITY"))
        if os.getenv("KIWI_ELEVENLABS_SIMILARITY_BOOST"):
            config.tts_elevenlabs_similarity_boost = float(os.getenv("KIWI_ELEVENLABS_SIMILARITY_BOOST"))
        if os.getenv("KIWI_ELEVENLABS_STYLE"):
            config.tts_elevenlabs_style = float(os.getenv("KIWI_ELEVENLABS_STYLE"))
        if os.getenv("KIWI_ELEVENLABS_USE_SPEAKER_BOOST"):
            config.tts_elevenlabs_use_speaker_boost = os.getenv("KIWI_ELEVENLABS_USE_SPEAKER_BOOST").strip().lower() in ("true", "1", "yes")
        if os.getenv("KIWI_ELEVENLABS_SPEED"):
            config.tts_elevenlabs_speed = float(os.getenv("KIWI_ELEVENLABS_SPEED"))
        if os.getenv("KIWI_ELEVENLABS_WS_STREAMING"):
            config.tts_elevenlabs_ws_streaming = os.getenv("KIWI_ELEVENLABS_WS_STREAMING").strip().lower() in ("true", "1", "yes")

        provider_explicit = ("provider" in tts_cfg) or bool(os.getenv("KIWI_TTS_PROVIDER"))
        qwen_backend_explicit = ("qwen_backend" in tts_cfg) or bool(os.getenv("KIWI_QWEN_BACKEND"))
        if not provider_explicit:
            if config.use_local_tts:
                config.tts_provider = "piper"
                if not qwen_backend_explicit:
                    config.tts_qwen_backend = "local"
            else:
                config.tts_provider = "qwen3"
                if not qwen_backend_explicit:
                    config.tts_qwen_backend = "runpod"

        provider_aliases = {
            "qwen": "qwen3",
            "qwen3_tts": "qwen3",
            "piper_tts": "piper",
            "eleven": "elevenlabs",
            "eleven_labs": "elevenlabs",
            "11labs": "elevenlabs",
            "kokoro_onnx": "kokoro",
            "kokoro-onnx": "kokoro",
        }
        config.tts_provider = provider_aliases.get(config.tts_provider, config.tts_provider)
        if config.tts_provider not in {"qwen3", "piper", "elevenlabs", "kokoro"}:
            kiwi_log("CONFIG", f"Unknown tts.provider='{config.tts_provider}', fallback to qwen3", level="WARNING")
            config.tts_provider = "qwen3"
        if config.tts_qwen_backend not in {"local", "runpod"}:
            kiwi_log("CONFIG", f"Unknown tts.qwen_backend='{config.tts_qwen_backend}', fallback to runpod", level="WARNING")
            config.tts_qwen_backend = "runpod"

        config.tts_model_size = normalize_qwen_model_size(config.tts_model_size)
        if config.tts_provider == "qwen3":
            config.tts_voice = normalize_qwen_voice(config.tts_voice)
        else:
            config.tts_voice = str(config.tts_voice or "").strip() or "Ono_Anna"
        config.tts_elevenlabs_voice_id = normalize_elevenlabs_voice_id(config.tts_elevenlabs_voice_id)
        config.use_local_tts = (
            config.tts_provider == "piper"
            or config.tts_provider == "kokoro"
            or (config.tts_provider == "qwen3" and config.tts_qwen_backend == "local")
        )
        if config.tts_provider == "qwen3" and config.tts_qwen_backend == "local":
            config.tts_local_model_path = cls._sync_local_qwen_model_path(
                config.tts_local_model_path,
                config.tts_model_size,
            )

        # Owner name from speaker_priority config
        sp_cfg = yaml_config.get("speaker_priority", {})
        owner_cfg = sp_cfg.get("owner", {})
        if owner_cfg.get("name"):
            config.owner_name = str(owner_cfg["name"]).strip()

        # STT engine aliases & validation
        stt_engine_aliases = {"eleven": "elevenlabs", "11labs": "elevenlabs", "whisper": "faster-whisper"}
        config.stt_engine = stt_engine_aliases.get(config.stt_engine, config.stt_engine)
        if config.stt_engine not in {"faster-whisper", "mlx-whisper", "elevenlabs"}:
            kiwi_log("CONFIG", f"Unknown stt.engine='{config.stt_engine}', fallback to faster-whisper", level="WARNING")
            config.stt_engine = "faster-whisper"

        if config.stt_device == "cuda" and not check_cuda_available():
            kiwi_log("CONFIG", "Requested CUDA for STT, but CUDA not available! Falling back to CPU", level="WARNING")
            config.stt_device = "cpu"
            # float16 does not work on CPU, use int8
            if config.stt_compute_type == "float16":
                kiwi_log("CONFIG", "Changing compute_type from float16 to int8 for CPU compatibility", level="INFO")
                config.stt_compute_type = "int8"

        # Populate voice_system_prompt from SOUL.md (project root), fallback to i18n
        if not config.voice_system_prompt:
            from kiwi import PROJECT_ROOT
            soul_md_path = os.path.join(PROJECT_ROOT, "SOUL.md")
            if os.path.isfile(soul_md_path):
                try:
                    with open(soul_md_path, "r", encoding="utf-8") as f:
                        config.voice_system_prompt = f.read().strip()
                except Exception:
                    pass
            if not config.voice_system_prompt:
                try:
                    from kiwi.i18n import setup as _i18n_setup, t as _t
                    _i18n_setup(config.language)
                    prompt = _t("system.voice_prompt")
                    if prompt != "system.voice_prompt":
                        config.voice_system_prompt = prompt
                except Exception:
                    pass

        return config

    def print_config_banner(self):
        """Print a startup summary with ASCII-safe formatting."""
        stt_device_label = "CUDA" if self.stt_device == "cuda" else "CPU"
        if self.stt_engine == "elevenlabs":
            stt_engine_label = "ElevenLabs (cloud)"
        elif self.stt_engine == "mlx-whisper":
            stt_engine_label = "MLX Whisper"
        else:
            stt_engine_label = "Faster Whisper"
        tts_device_label = None
        if self.tts_provider == "piper":
            tts_type = "Piper (local)"
            tts_model = self.tts_piper_model_path or "ru_RU-irina-medium.onnx"
            tts_voice = self.tts_voice
        elif self.tts_provider == "kokoro":
            tts_type = "Kokoro ONNX (local)"
            tts_model = self.tts_kokoro_model_dir or "models/kokoro"
            tts_voice = self.tts_kokoro_voice
        elif self.tts_provider == "elevenlabs":
            tts_type = "ElevenLabs (cloud)"
            tts_model = self.tts_elevenlabs_model_id
            tts_voice = self.tts_elevenlabs_voice_id
        elif self.tts_provider == "qwen3" and self.tts_qwen_backend == "local":
            tts_type = f"Qwen3-TTS {self.tts_model_size} (local)"
            tts_model = self.tts_local_model_path or f"Qwen3-TTS-12Hz-{self.tts_model_size}-CustomVoice"
            tts_device_label = self.tts_qwen_device.upper()
            tts_voice = self.tts_voice
        else:
            tts_type = f"Qwen3-TTS {self.tts_model_size} (RunPod)"
            tts_model = self.tts_endpoint_id
            tts_voice = self.tts_voice

        wake_engine_label = "OpenWakeWord" if self.wake_word_engine == "openwakeword" else "Text (fuzzy match)"

        line = "=" * 58
        print("\n" + line)
        print("KIWI VOICE SERVICE")
        print(line)
        print(f"STT   : {stt_engine_label} ({self.stt_model})")
        print(f"\t\tDevice: {stt_device_label}")
        print(f"TTS   : {tts_type}")
        print(f"\t\tModel : {tts_model}")
        if tts_device_label:
            print(f"\t\tDevice: {tts_device_label}")
        print(f"\t\tVoice : {tts_voice}")
        print(f"Wake  : {wake_engine_label}")
        if self.wake_word_engine == "openwakeword":
            print(f"\t\tModel : {self.wake_word_model}")
            print(f"\t\tThreshold: {self.wake_word_threshold}")
        else:
            print(f"\t\tKeyword: {self.wake_word_keyword}")
        print("VAD   : Silero VAD (ONNX)")
        print(f"LLM   : OpenClaw (session: {self.openclaw_session_id})")
        print(f"Lang  : {self.stt_language.upper()}")
        print(line + "\n")
