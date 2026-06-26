from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests


DEFAULT_TIMEOUT = 120

# Create a session that bypasses proxy for local API calls
_session = requests.Session()
_session.trust_env = False  # Ignore http_proxy/https_proxy env vars


def _request(method: str, url: str, **kwargs) -> requests.Response:
    """Make a request using the no-proxy session."""
    return _session.request(method, url, **kwargs)
VALID_TTS_FORMATS = {"wav", "mp4", "ogg_opus"}
VALID_ASR_OUTPUTS = {"json", "text"}


class ConfigError(RuntimeError):
    """Raised when configuration is invalid."""


class ApiError(RuntimeError):
    """Raised when API request fails."""


def load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def str_to_bool(value: str | bool | None) -> bool | None:
    if value is None or isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


def load_config_json(config_path: Path) -> dict[str, Any]:
    default_config = {
        "asr": {
            "model": "openai/whisper-large-v3",
            "language": "zh",
            "task": "transcribe",
            "timestamps": "chunk",
            "batch_size": "default",
            "flash": "default",
            "hf_token": "default",
            "diarization_model": "default",
            "num_speakers": "default",
            "min_speakers": "default",
            "max_speakers": "default",
            "transcript_path": "default"
        },
        "tts": {
            "model": "multilingual",
            "language": "zh",
            "format": "wav",
            "repetition_penalty": "default",
            "temperature": "default",
            "top_p": "default",
            "top_k": "default",
            "norm_loudness": "default",
            "exaggeration": "default",
            "cfg_weight": "default",
            "audio_prompt_path": "default"
        },
        "global": {
            "voice_summary_limit": 100,
            "default_clone_audio": "tmp/clone.wav",
            "telegram_tts_format": "ogg_opus",
            "asr_output": "json"
        }
    }

    if not config_path.exists():
        return default_config

    try:
        user_config = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ConfigError(f"Failed to load config.json: {exc}") from exc

    merged_config = copy.deepcopy(default_config)
    for section in ("asr", "tts", "global"):
        if isinstance(user_config.get(section), dict):
            for key, value in user_config[section].items():
                if key == "timestamp":
                    key = "timestamps"
                if key in merged_config[section]:
                    merged_config[section][key] = value

    return merged_config


def load_env() -> dict[str, Any]:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent

    # First, try loading from environment variables
    base_url = os.getenv("LIBER_API_BASE_URL", "").strip().rstrip("/")
    api_key = os.getenv("LIBER_API_KEY", "").strip()

    # If not found in environment variables, try loading from ~/.openclaw/.env
    if not base_url or not api_key:
        openclaw_env_path = Path.home() / ".openclaw" / ".env"
        load_dotenv(openclaw_env_path)
        base_url = os.getenv("LIBER_API_BASE_URL", "").strip().rstrip("/")
        api_key = os.getenv("LIBER_API_KEY", "").strip()

    # Finally, try loading from local .env files (skill directory or current working directory)
    if not base_url or not api_key:
        for candidate in (skill_dir / ".env", Path.cwd() / ".env"):
            load_dotenv(candidate)
            base_url = os.getenv("LIBER_API_BASE_URL", "").strip().rstrip("/")
            api_key = os.getenv("LIBER_API_KEY", "").strip()
            if base_url and api_key:
                break

    if not base_url:
        raise ConfigError("Missing LIBER_API_BASE_URL. Please set it in environment variables, ~/.openclaw/.env, or local .env file")
    if not api_key:
        raise ConfigError("Missing LIBER_API_KEY. Please set it in environment variables, ~/.openclaw/.env, or local .env file")

    # Load config from external location to prevent overwrites during skill updates
    config_path = Path.home() / ".openclaw" / "workspace" / "config" / "speechapi_config.json"
    if config_path.exists():
        config_json = load_config_json(config_path)
    else:
        # Fallback to local config if external config doesn't exist
        config_json = load_config_json(skill_dir / "config.json")

    return {
        "base_url": base_url,
        "api_key": api_key,
        "config_json": config_json,
        "skill_dir": skill_dir,
    }


def build_headers(api_key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"}


def process_parameter(value: Any) -> Any:
    if value == "default" or value is None:
        return None
    return value


def resolve_clone_audio(config: dict[str, Any], override: str | None = None) -> Path | None:
    tts_audio_prompt = config["config_json"]["tts"].get("audio_prompt_path")
    clone_audio_config = config["config_json"]["global"].get("default_clone_audio")
    raw_value = override if override is not None else tts_audio_prompt

    if raw_value in (None, "default"):
        raw_value = clone_audio_config
    if raw_value is None:
        return None

    value = str(raw_value).strip()
    if not value or value.lower() == "none" or value == "default":
        return None

    path = Path(value)
    if not path.is_absolute():
        path = config["skill_dir"] / value

    return path if path.exists() and path.is_file() else None


def build_asr_params(config: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    asr_config = config["config_json"]["asr"]

    for key in asr_config:
        value = overrides.get(key, asr_config[key])
        processed_value = process_parameter(value)
        if processed_value is not None:
            params[key] = processed_value

    return params


def build_tts_params(config: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    tts_config = config["config_json"]["tts"]

    # Add text parameter first (required field)
    text_value = overrides.get("text")
    if text_value is not None:
        params["text"] = text_value

    for key in tts_config:
        if key == "audio_prompt_path":
            continue
        value = overrides.get(key, tts_config[key])
        processed_value = process_parameter(value)
        if processed_value is not None:
            params[key] = processed_value

    return params


def check_health(config: dict[str, Any]) -> dict[str, Any]:
    url = f'{config["base_url"]}/health'
    response = _request("GET", url, headers=build_headers(config["api_key"]), timeout=DEFAULT_TIMEOUT)
    _raise_for_status(response, "health check failed")
    return response.json()


def download_audio_file(
    config: dict[str, Any],
    audio_url: str,
    output_path: str | None = None,
    fmt: str = "wav",
) -> Path | None:
    """Download audio file from API and save to local path.
    
    According to Liber_SpeechAPI source code, the TTS endpoint is synchronous
    and returns only after the file is fully generated and saved. The audio_url
    in the response points to an existing file that can be downloaded immediately.
    
    Args:
        config: Configuration dict with base_url and api_key
        audio_url: URL path from API response (e.g., /api/v1/results/xxx.wav)
        output_path: Custom output path, or None to use results/ directory
        fmt: Audio format extension
    
    Returns:
        Path to saved file, or None if download failed
    """
    from datetime import datetime
    
    try:
        # Build full URL
        if audio_url.startswith("http"):
            full_url = audio_url
        else:
            # API returns path like /api/v1/results/xxx.wav
            # base_url is like http://host:port/api/v1
            from urllib.parse import urlparse
            parsed = urlparse(config["base_url"])
            full_url = f"{parsed.scheme}://{parsed.netloc}{audio_url}"
        
        # Determine output directory
        if output_path:
            target_path = Path(output_path)
        else:
            # Default: results/ directory under skill root
            results_dir = config["skill_dir"] / "results"
            results_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_path = results_dir / f"tts_{timestamp}.{fmt}"
        
        # Download the file (single attempt, no retry needed for synchronous API)
        response = _request("GET", full_url, headers=build_headers(config["api_key"]), timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        
        # Verify content is audio, not error JSON
        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type.lower():
            # Might be an error response
            try:
                error_data = response.json()
                raise ApiError(f"Server returned error: {error_data}")
            except:
                pass  # Not JSON, proceed with save
        
        # Save file
        target_path.write_bytes(response.content)
        
        # Verify file was written and has content
        if target_path.stat().st_size == 0:
            raise ApiError("Downloaded file is empty")
        
        return target_path
        
    except Exception as e:
        raise ApiError(f"Failed to download audio file: {e}") from e


def transcribe_file(
    audio_path: str,
    language: str | None = None,
    task: str | None = None,
    timestamps: str | None = None,
    model: str | None = None,
    batch_size: int | None = None,
    flash: bool | None = None,
    hf_token: str | None = None,
    diarization_model: str | None = None,
    num_speakers: int | None = None,
    min_speakers: int | None = None,
    max_speakers: int | None = None,
    output: str | None = None,
) -> dict[str, Any] | str:
    config = load_env()
    file_path = Path(audio_path)
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    default_output = str(config["config_json"]["global"].get("asr_output", "json")).strip().lower() or "json"
    output_mode = (output or default_output).strip().lower()
    if output_mode not in VALID_ASR_OUTPUTS:
        raise ValueError(f"Invalid ASR output mode: {output_mode}")

    overrides = {
        "language": language,
        "task": task,
        "timestamps": timestamps,
        "model": model,
        "batch_size": batch_size,
        "flash": flash,
        "hf_token": hf_token,
        "diarization_model": diarization_model,
        "num_speakers": num_speakers,
        "min_speakers": min_speakers,
        "max_speakers": max_speakers,
    }
    data = build_asr_params(config, overrides)
    url = f'{config["base_url"]}/asr/transcribe'

    with file_path.open("rb") as fh:
        files = {"file": (file_path.name, fh)}
        response = _request(
            "POST",
            url,
            headers=build_headers(config["api_key"]),
            data=data,
            files=files,
            timeout=DEFAULT_TIMEOUT,
        )

    _raise_for_status(response, "ASR transcription failed")
    payload = response.json()
    text = payload.get("text", "")
    if not isinstance(text, str) or not text.strip():
        raise ApiError("ASR succeeded but returned empty text")

    if output_mode == "text":
        return text
    return payload


def synthesize_text(
    text: str,
    language: str | None = None,
    model: str | None = None,
    fmt: str | None = None,
    clone_audio: str | None = None,
    repetition_penalty: float | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    top_k: int | None = None,
    norm_loudness: bool | None = None,
    exaggeration: float | None = None,
    cfg_weight: float | None = None,
    telegram: bool = False,
    output_path: str | None = None,
) -> dict[str, Any]:
    config = load_env()
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        raise ValueError("TTS text must not be empty")

    default_format = str(config["config_json"]["tts"].get("format", "wav")).strip() or "wav"
    telegram_format = str(config["config_json"]["global"].get("telegram_tts_format", "ogg_opus")).strip() or "ogg_opus"
    effective_format = telegram_format if telegram else (fmt or default_format)
    if effective_format not in VALID_TTS_FORMATS:
        raise ValueError(f"Invalid TTS format: {effective_format}")

    overrides = {
        "text": cleaned_text,
        "language": language,
        "model": model,
        "format": effective_format,
        "repetition_penalty": repetition_penalty,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "norm_loudness": norm_loudness,
        "exaggeration": exaggeration,
        "cfg_weight": cfg_weight,
    }
    data = build_tts_params(config, overrides)
    url = f'{config["base_url"]}/tts/synthesize'
    clone_path = resolve_clone_audio(config, clone_audio)

    if clone_path is not None:
        with clone_path.open("rb") as clone_fh:
            files = {"audio_prompt": (clone_path.name, clone_fh)}
            response = _request(
                "POST",
                url,
                headers=build_headers(config["api_key"]),
                data=data,
                files=files,
                timeout=DEFAULT_TIMEOUT,
            )
    else:
        response = _request(
            "POST",
            url,
            headers=build_headers(config["api_key"]),
            data=data,
            timeout=DEFAULT_TIMEOUT,
        )

    _raise_for_status(response, "TTS synthesis failed")
    payload = response.json()
    audio_url = payload.get("audio_url", "")
    if not isinstance(audio_url, str) or not audio_url.strip():
        raise ApiError("TTS succeeded but returned empty audio_url")
    
    # Download audio file to local path
    local_path = download_audio_file(config, audio_url, output_path, effective_format)
    if local_path:
        payload["local_path"] = str(local_path)
    
    return payload


def _raise_for_status(response: requests.Response, message: str) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        detail = response.text[:1000]
        raise ApiError(f"{message}: HTTP {response.status_code}: {detail}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Liber SpeechAPI client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    health_parser = subparsers.add_parser("health", help="Run health check")
    health_parser.set_defaults(command="health")

    asr_parser = subparsers.add_parser("asr", help="Transcribe audio file")
    asr_parser.add_argument("audio_path", help="Path to local audio file")
    asr_parser.add_argument("--language", default=None)
    asr_parser.add_argument("--task", default=None)
    asr_parser.add_argument("--timestamps", default=None)
    asr_parser.add_argument("--timestamp", dest="timestamps", default=None)
    asr_parser.add_argument("--model", default=None)
    asr_parser.add_argument("--batch-size", type=int, default=None)
    asr_parser.add_argument("--flash", type=str_to_bool, default=None)
    asr_parser.add_argument("--hf-token", default=None)
    asr_parser.add_argument("--diarization-model", default=None)
    asr_parser.add_argument("--num-speakers", type=int, default=None)
    asr_parser.add_argument("--min-speakers", type=int, default=None)
    asr_parser.add_argument("--max-speakers", type=int, default=None)
    asr_parser.add_argument("--output", choices=sorted(VALID_ASR_OUTPUTS), default=None)

    tts_parser = subparsers.add_parser("tts", help="Synthesize text")
    tts_parser.add_argument("text", help="Text to synthesize")
    tts_parser.add_argument("--language", default=None)
    tts_parser.add_argument("--model", default=None)
    tts_parser.add_argument("--format", choices=sorted(VALID_TTS_FORMATS), default=None)
    tts_parser.add_argument("--clone-audio", default=None)
    tts_parser.add_argument("--repetition-penalty", type=float, default=None)
    tts_parser.add_argument("--temperature", type=float, default=None)
    tts_parser.add_argument("--top-p", type=float, default=None)
    tts_parser.add_argument("--top-k", type=int, default=None)
    tts_parser.add_argument("--norm-loudness", type=str_to_bool, default=None)
    tts_parser.add_argument("--exaggeration", type=float, default=None)
    tts_parser.add_argument("--cfg-weight", type=float, default=None)
    tts_parser.add_argument("--telegram", action="store_true", help="Force Telegram ogg_opus output")
    tts_parser.add_argument("--output", "-o", default=None, help="Output file path (default: results/tts_YYYYMMDD_HHMMSS.wav)")

    args = parser.parse_args()

    try:
        if args.command == "health":
            result: Any = check_health(load_env())
        elif args.command == "asr":
            result = transcribe_file(
                audio_path=args.audio_path,
                language=args.language,
                task=args.task,
                timestamps=args.timestamps,
                model=args.model,
                batch_size=args.batch_size,
                flash=args.flash,
                hf_token=args.hf_token,
                diarization_model=args.diarization_model,
                num_speakers=args.num_speakers,
                min_speakers=args.min_speakers,
                max_speakers=args.max_speakers,
                output=args.output,
            )
        elif args.command == "tts":
            result = synthesize_text(
                text=args.text,
                language=args.language,
                model=args.model,
                fmt=args.format,
                clone_audio=args.clone_audio,
                repetition_penalty=args.repetition_penalty,
                temperature=args.temperature,
                top_p=args.top_p,
                top_k=args.top_k,
                norm_loudness=args.norm_loudness,
                exaggeration=args.exaggeration,
                cfg_weight=args.cfg_weight,
                telegram=args.telegram,
                output_path=args.output,
            )
        else:
            raise RuntimeError(f"Unsupported command: {args.command}")

        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
