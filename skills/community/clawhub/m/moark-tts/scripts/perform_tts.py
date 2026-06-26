#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

"""
Generate speech with Gitee AI TTS models.

This script supports the model aliases used by the moark-tts skill:
- audiofly -> AudioFly
- chattts -> ChatTTS
- cosyvoice2 -> CosyVoice2
- cosyvoice3 -> CosyVoice3
- cosyvoice-300m -> FunAudioLLM-CosyVoice-300M
- fish-speech-1.2-sft -> fish-speech-1.2-sft
- index-tts-1.5 -> IndexTTS-1.5
- index-tts-2 -> IndexTTS-2
- glm-tts -> GLM-TTS
- megatts3 -> MegaTTS3
- moss-ttsd-v0.5 -> MOSS-TTSD-v0.5
- qwen-tts -> Qwen3-TTS
- spark-tts-0.5b -> Spark-TTS-0.5B
- step-audio-tts-3b -> Step-Audio-TTS-3B
- vibevoice-large -> VibeVoice-Large
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

BASE_URL = "https://ai.gitee.com/v1"
DEFAULT_TIMEOUT = 1800
DEFAULT_POLL_INTERVAL = 3

MODEL_CONFIGS = {
    "audiofly": {
        "official": "AudioFly",
        "modes": {"async"},
    },
    "audio-fly": {
        "official": "AudioFly",
        "modes": {"async"},
    },
    "chattts": {
        "official": "ChatTTS",
        "modes": {"sync"},
    },
    "chat-tts": {
        "official": "ChatTTS",
        "modes": {"sync"},
    },
    "cosyvoice2": {
        "official": "CosyVoice2",
        "modes": {"sync"},
    },
    "cosyvoice3": {
        "official": "CosyVoice3",
        "modes": {"async"},
    },
    "cosyvoice-3": {
        "official": "CosyVoice3",
        "modes": {"async"},
    },
    "cosyvoice3.0": {
        "official": "CosyVoice3",
        "modes": {"async"},
    },
    "cosyvoice-3.0": {
        "official": "CosyVoice3",
        "modes": {"async"},
    },
    "cosyvoice-300m": {
        "official": "FunAudioLLM-CosyVoice-300M",
        "modes": {"sync"},
    },
    "funaudiollm-cosyvoice-300m": {
        "official": "FunAudioLLM-CosyVoice-300M",
        "modes": {"sync"},
    },
    "fish-speech-1.2-sft": {
        "official": "fish-speech-1.2-sft",
        "modes": {"sync"},
    },
    "index-tts-1.5": {
        "official": "IndexTTS-1.5",
        "modes": {"sync"},
    },
    "index-tts-2": {
        "official": "IndexTTS-2",
        "modes": {"sync", "async"},
    },
    "glm-tts": {
        "official": "GLM-TTS",
        "modes": {"sync"},
    },
    "megatts3": {
        "official": "MegaTTS3",
        "modes": {"sync"},
    },
    "moss-ttsd-v0.5": {
        "official": "MOSS-TTSD-v0.5",
        "modes": {"async"},
    },
    "moss-ttsd-v05": {
        "official": "MOSS-TTSD-v0.5",
        "modes": {"async"},
    },
    "mega-tts3": {
        "official": "MegaTTS3",
        "modes": {"sync"},
    },
    "mega_tts3": {
        "official": "MegaTTS3",
        "modes": {"sync"},
    },
    "qwen-tts": {
        "official": "Qwen3-TTS",
        "modes": {"async"},
    },
    "qwen3-tts": {
        "official": "Qwen3-TTS",
        "modes": {"async"},
    },
    "vibevoice-large": {
        "official": "VibeVoice-Large",
        "modes": {"async"},
    },
    "vibevoice": {
        "official": "VibeVoice-Large",
        "modes": {"async"},
    },
    "spark-tts-0.5b": {
        "official": "Spark-TTS-0.5B",
        "modes": {"async"},
    },
    "spark_tts_0.5b": {
        "official": "Spark-TTS-0.5B",
        "modes": {"async"},
    },
    "step-audio-tts-3b": {
        "official": "Step-Audio-TTS-3B",
        "modes": {"sync"},
    },
    "step_audio_tts_3b": {
        "official": "Step-Audio-TTS-3B",
        "modes": {"sync"},
    },
}

QWEN3_TTS_BUILTIN_SPEAKERS = (
    "Vivian",
    "Serena",
    "Uncle_Fu",
    "Dylan",
    "Eric",
    "Ryan",
    "Aiden",
    "Ono_Anna",
    "Sohee",
)

QWEN3_TTS_LANGUAGES = ("Chinese", "English")


class TTSConfigError(RuntimeError):
    """Raised when the requested model/mode combination is invalid."""


@dataclass
class HttpResponse:
    status_code: int
    headers: dict[str, str]
    content: bytes

    def get_header(self, name: str) -> str:
        for key, value in self.headers.items():
            if key.lower() == name.lower():
                return value
        return ""

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")

    def json(self) -> Any:
        return json.loads(self.text)


def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("GITEEAI_API_KEY")


def normalize_model(model_name: str) -> dict[str, Any]:
    key = model_name.strip().lower()
    if key in MODEL_CONFIGS:
        return MODEL_CONFIGS[key]

    for config in MODEL_CONFIGS.values():
        if key == config["official"].lower():
            return config

    supported = ", ".join(sorted({cfg["official"] for cfg in MODEL_CONFIGS.values()}))
    raise TTSConfigError(f"Unsupported model '{model_name}'. Supported models: {supported}")


def parse_extra_body_json(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TTSConfigError(f"Invalid --extra-body-json: {exc}") from exc

    if not isinstance(parsed, dict):
        raise TTSConfigError("--extra-body-json must be a JSON object")
    return parsed


def choose_mode(args: argparse.Namespace, config: dict[str, Any]) -> str:
    if args.mode != "auto":
        if args.mode not in config["modes"]:
            official = config["official"]
            allowed = ", ".join(sorted(config["modes"]))
            raise TTSConfigError(f"Model '{official}' only supports mode(s): {allowed}")
        return args.mode

    if "async" not in config["modes"]:
        return "sync"
    if "sync" not in config["modes"]:
        return "async"

    # When a model supports both sync and async endpoints, default auto mode
    # to sync unless the user explicitly sets --mode async.
    return "sync"


def normalize_audio_mode(raw_mode: str | None) -> str | None:
    if raw_mode is None:
        return None
    lowered = raw_mode.strip().lower()
    if lowered == "single":
        return "Single"
    if lowered == "role":
        return "Role"
    raise TTSConfigError("--audio-mode must be 'single' or 'role'")


def validate_moss_ttsd_args(args: argparse.Namespace) -> str:
    audio_mode = normalize_audio_mode(args.audio_mode)
    has_single_fields = bool(args.prompt_audio_single_url or args.prompt_text_single)
    has_role_fields = bool(
        args.prompt_audio_1_url
        or args.prompt_text_1
        or args.prompt_audio_2_url
        or args.prompt_text_2
    )

    if audio_mode is None:
        if has_single_fields and has_role_fields:
            raise TTSConfigError(
                "MOSS-TTSD-v0.5 received both single and role fields. "
                "Set --audio-mode explicitly and only pass matching fields."
            )
        if has_single_fields:
            audio_mode = "Single"
        elif has_role_fields:
            audio_mode = "Role"
        else:
            raise TTSConfigError(
                "MOSS-TTSD-v0.5 requires --audio-mode and reference prompt fields."
            )

    if audio_mode == "Single":
        if has_role_fields:
            raise TTSConfigError(
                "MOSS-TTSD-v0.5 --audio-mode single cannot be combined with role fields."
            )
        if not args.prompt_audio_single_url:
            raise TTSConfigError(
                "MOSS-TTSD-v0.5 single mode requires --prompt-audio-single-url."
            )
        if not args.prompt_text_single:
            raise TTSConfigError("MOSS-TTSD-v0.5 single mode requires --prompt-text-single.")
        return audio_mode

    if has_single_fields:
        raise TTSConfigError(
            "MOSS-TTSD-v0.5 --audio-mode role cannot be combined with single fields."
        )
    if not args.prompt_audio_1_url:
        raise TTSConfigError("MOSS-TTSD-v0.5 role mode requires --prompt-audio-1-url.")
    if not args.prompt_text_1:
        raise TTSConfigError("MOSS-TTSD-v0.5 role mode requires --prompt-text-1.")
    if not args.prompt_audio_2_url:
        raise TTSConfigError("MOSS-TTSD-v0.5 role mode requires --prompt-audio-2-url.")
    if not args.prompt_text_2:
        raise TTSConfigError("MOSS-TTSD-v0.5 role mode requires --prompt-text-2.")
    return audio_mode


def normalize_prompt_audio_url(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise TTSConfigError("--prompt-audio-urls contains an empty URL")
    if not normalized.startswith(("http://", "https://")):
        raise TTSConfigError(
            "--prompt-audio-urls only supports http(s) URLs "
            f"(got: {normalized})"
        )
    return normalized


def normalize_prompt_audio_urls_value(value: Any) -> str | list[str]:
    if isinstance(value, str):
        return normalize_prompt_audio_url(value)

    if isinstance(value, list):
        if not value:
            raise TTSConfigError("--prompt-audio-urls JSON array cannot be empty")
        urls: list[str] = []
        for index, item in enumerate(value):
            if not isinstance(item, str):
                raise TTSConfigError(
                    "--prompt-audio-urls JSON array must contain URL strings "
                    f"(invalid item at index {index})"
                )
            urls.append(normalize_prompt_audio_url(item))
        return urls

    raise TTSConfigError(
        "--prompt-audio-urls must be either one URL string "
        "or a JSON array of URL strings"
    )


def parse_prompt_audio_urls(raw: str | None) -> str | list[str] | None:
    if raw is None:
        return None

    candidate = raw.strip()
    if not candidate:
        raise TTSConfigError("--prompt-audio-urls cannot be empty")

    if candidate.startswith(("http://", "https://")):
        return normalize_prompt_audio_urls_value(candidate)

    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise TTSConfigError(
            "--prompt-audio-urls must be one URL string or a JSON array, "
            "for example: https://a.wav or "
            "'[\"https://a.wav\", \"https://b.wav\"]'"
        ) from exc

    return normalize_prompt_audio_urls_value(parsed)


def validate_qwen_language(language: str, field_name: str) -> str:
    if language not in QWEN3_TTS_LANGUAGES:
        allowed = ", ".join(QWEN3_TTS_LANGUAGES)
        raise TTSConfigError(f"{field_name} must be one of: {allowed}")
    return language


def validate_qwen_speaker(speaker: str, field_name: str) -> str:
    if speaker not in QWEN3_TTS_BUILTIN_SPEAKERS:
        allowed = ", ".join(QWEN3_TTS_BUILTIN_SPEAKERS)
        raise TTSConfigError(f"{field_name} must be one of: {allowed}")
    return speaker


def validate_qwen_custom_voice_fields(
        *,
        speaker: str | None,
        prompt_audio_url: str | None,
        prompt_text: str | None,
        field_prefix: str,
) -> None:
    if speaker and (prompt_audio_url or prompt_text):
        raise TTSConfigError(
            f"{field_prefix} cannot mix built-in speaker with custom voice fields "
            "(prompt_audio_url/prompt_text)"
        )

    if prompt_audio_url is None and prompt_text is None:
        return

    if prompt_audio_url is None or prompt_text is None:
        raise TTSConfigError(
            f"{field_prefix} custom voice requires both prompt_audio_url and prompt_text"
        )

    if not prompt_audio_url.startswith(("http://", "https://")):
        raise TTSConfigError(
            f"{field_prefix} prompt_audio_url must be an http(s) URL"
        )


def parse_qwen_inputs_json(raw: str) -> list[dict[str, Any]]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TTSConfigError(
            "Invalid --qwen-inputs-json. It must be a JSON array of objects."
        ) from exc

    if isinstance(parsed, dict):
        parsed = [parsed]

    if not isinstance(parsed, list) or not parsed:
        raise TTSConfigError("--qwen-inputs-json must be a non-empty JSON array")

    normalized_inputs: list[dict[str, Any]] = []
    for index, item in enumerate(parsed):
        field_prefix = f"--qwen-inputs-json[{index}]"
        if not isinstance(item, dict):
            raise TTSConfigError(f"{field_prefix} must be a JSON object")

        prompt = item.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise TTSConfigError(f"{field_prefix}.prompt must be a non-empty string")

        current: dict[str, Any] = {"prompt": prompt}

        language = item.get("language")
        if language is not None:
            if not isinstance(language, str):
                raise TTSConfigError(f"{field_prefix}.language must be a string")
            current["language"] = validate_qwen_language(language, f"{field_prefix}.language")

        speaker = item.get("speaker")
        if speaker is not None:
            if not isinstance(speaker, str):
                raise TTSConfigError(f"{field_prefix}.speaker must be a string")
            current["speaker"] = validate_qwen_speaker(speaker, f"{field_prefix}.speaker")

        instruction = item.get("instruction")
        if instruction is not None:
            if not isinstance(instruction, str):
                raise TTSConfigError(f"{field_prefix}.instruction must be a string")
            current["instruction"] = instruction

        prompt_audio_url = item.get("prompt_audio_url")
        if prompt_audio_url is not None and not isinstance(prompt_audio_url, str):
            raise TTSConfigError(f"{field_prefix}.prompt_audio_url must be a string")
        prompt_text = item.get("prompt_text")
        if prompt_text is not None and not isinstance(prompt_text, str):
            raise TTSConfigError(f"{field_prefix}.prompt_text must be a string")

        validate_qwen_custom_voice_fields(
            speaker=speaker,
            prompt_audio_url=prompt_audio_url,
            prompt_text=prompt_text,
            field_prefix=field_prefix,
        )

        if prompt_audio_url is not None:
            current["prompt_audio_url"] = prompt_audio_url
        if prompt_text is not None:
            current["prompt_text"] = prompt_text

        normalized_inputs.append(current)

    return normalized_inputs


def build_qwen_single_input(args: argparse.Namespace) -> dict[str, Any]:
    if not args.text:
        raise TTSConfigError(
            "Qwen3-TTS single-input mode requires --text "
            "(or pass --qwen-inputs-json for multi-input mode)"
        )
    qwen_input: dict[str, Any] = {"prompt": args.text}

    if args.language is not None:
        qwen_input["language"] = validate_qwen_language(args.language, "--language")
    if args.speaker is not None:
        qwen_input["speaker"] = validate_qwen_speaker(args.speaker, "--speaker")
    if args.instruction is not None:
        qwen_input["instruction"] = args.instruction

    validate_qwen_custom_voice_fields(
        speaker=args.speaker,
        prompt_audio_url=args.prompt_audio_url,
        prompt_text=args.prompt_text,
        field_prefix="Qwen3-TTS input",
    )
    if args.prompt_audio_url is not None:
        qwen_input["prompt_audio_url"] = args.prompt_audio_url
    if args.prompt_text is not None:
        qwen_input["prompt_text"] = args.prompt_text

    return qwen_input


def validate_text_requirement(args: argparse.Namespace, official_model: str) -> None:
    if official_model == "Qwen3-TTS" and args.qwen_inputs_json:
        return
    if args.text:
        return
    raise TTSConfigError("--text is required for the selected model")


def build_headers(api_key: str, failover_enabled: str = "true") -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    headers["X-Failover-Enabled"] = failover_enabled
    return headers


def request_http(
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
) -> HttpResponse:
    data = None
    request_headers = dict(headers or {})
    if json_body is not None:
        data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")

    req = request.Request(
        url=url,
        data=data,
        headers=request_headers,
        method=method,
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            return HttpResponse(
                status_code=response.status,
                headers=dict(response.headers.items()),
                content=response.read(),
            )
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"API request failed ({exc.code}): {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc


def maybe_add(payload: dict[str, Any], name: str, value: Any) -> None:
    if value is not None:
        payload[name] = value


def save_binary_content(response: HttpResponse, output_path: str | None) -> str:
    path = Path(output_path or "tts-output.bin")
    path.write_bytes(response.content)
    return str(path.resolve())


def extract_first_url(data: Any) -> str | None:
    if isinstance(data, str):
        if data.startswith("http://") or data.startswith("https://"):
            return data
        return None

    if isinstance(data, list):
        for item in data:
            url = extract_first_url(item)
            if url:
                return url
        return None

    if isinstance(data, dict):
        for key in ("url", "audio_url", "download_url", "file_url"):
            value = data.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                return value
        for value in data.values():
            url = extract_first_url(value)
            if url:
                return url
    return None


def run_sync(
        *,
        api_key: str,
        official_model: str,
        args: argparse.Namespace,
        extra_body: dict[str, Any],
) -> None:
    payload: dict[str, Any] = {
        "model": official_model,
        "input": args.text,
        "response_data_format": args.response_data_format,
    }
    maybe_add(payload, "voice", args.voice)

    # Some TTS models accept extra top-level fields through the OpenAI-compatible
    # request body. Only pass them when the user explicitly provided them.
    maybe_add(payload, "prompt", args.prompt)
    maybe_add(payload, "prompt_text", args.prompt_text)
    maybe_add(payload, "prompt_audio_url", args.prompt_audio_url)
    maybe_add(payload, "emo_audio_prompt_url", args.emo_audio_prompt_url)
    maybe_add(payload, "emo_alpha", args.emo_alpha)
    maybe_add(payload, "emo_text", args.emo_text)
    if args.use_emo_text is not None:
        payload["use_emo_text"] = args.use_emo_text == "true"
    maybe_add(payload, "prompt_wav_url", args.prompt_wav_url)
    maybe_add(payload, "voice_url", args.voice_url)
    maybe_add(payload, "instruct_text", args.instruct_text)
    maybe_add(payload, "seed", args.seed)
    maybe_add(payload, "prompt_language", args.prompt_language)
    maybe_add(payload, "intelligibility_weight", args.intelligibility_weight)
    maybe_add(payload, "similarity_weight", args.similarity_weight)
    maybe_add(payload, "temperature", args.temperature)
    maybe_add(payload, "top_P", args.top_p)
    maybe_add(payload, "top_K", args.top_k)
    maybe_add(payload, "gender", args.gender)
    maybe_add(payload, "pitch", args.pitch)
    maybe_add(payload, "speed", args.speed)
    payload.update(extra_body)

    response = request_http(
        "POST",
        f"{BASE_URL}/audio/speech",
        headers=build_headers(api_key, args.failover_enabled),
        json_body=payload,
    )

    print(f"MODEL: {official_model}")
    print("MODE: sync")

    content_type = response.get_header("Content-Type")
    if args.response_data_format == "blob" or "application/json" not in content_type:
        file_path = save_binary_content(response, args.output)
        print(f"AUDIO_FILE: {file_path}")
        return

    try:
        body = response.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON response, got invalid JSON: {exc}") from exc

    audio_url = extract_first_url(body)
    if audio_url:
        print(f"AUDIO_URL: {audio_url}")
    print(f"TTS_RESULT: {json.dumps(body, ensure_ascii=False)}")


def wait_for_async_result(
        *,
        api_key: str,
        task: dict[str, Any],
        timeout_seconds: int,
        poll_interval_seconds: int,
) -> dict[str, Any]:
    started = time.time()
    urls = task.get("urls") or {}
    poll_url = urls.get("get")
    task_id = task.get("task_id")
    if not poll_url and task_id:
        poll_url = f"{BASE_URL}/task/{task_id}"
    if not poll_url:
        fallback_task_id = task_id or "<unknown>"
        raise RuntimeError(f"Async task '{fallback_task_id}' does not contain a poll URL")

    while True:
        response = request_http(
            "GET",
            poll_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        current = response.json()
        status = current.get("status")
        print(f"TASK_STATUS: {status}")

        if status == "success":
            return current
        if status in {"failure", "cancelled"}:
            raise RuntimeError(json.dumps(current, ensure_ascii=False))
        if time.time() - started > timeout_seconds:
            raise RuntimeError(
                f"Timed out waiting for async TTS result after {timeout_seconds} seconds"
            )
        time.sleep(poll_interval_seconds)


def run_async(
        *,
        api_key: str,
        official_model: str,
        args: argparse.Namespace,
        extra_body: dict[str, Any],
) -> None:
    payload: dict[str, Any] = {
        "model": official_model,
        "inputs": args.text,
    }
    maybe_add(payload, "prompt", args.prompt)
    maybe_add(payload, "prompt_text", args.prompt_text)
    maybe_add(payload, "prompt_audio_url", args.prompt_audio_url)
    maybe_add(payload, "emo_audio_prompt_url", args.emo_audio_prompt_url)
    maybe_add(payload, "emo_alpha", args.emo_alpha)
    maybe_add(payload, "emo_text", args.emo_text)
    if args.use_emo_text is not None:
        payload["use_emo_text"] = args.use_emo_text == "true"
    maybe_add(payload, "prompt_wav_url", args.prompt_wav_url)
    maybe_add(payload, "voice_url", args.voice_url)
    maybe_add(payload, "instruct_text", args.instruct_text)
    maybe_add(payload, "seed", args.seed)
    maybe_add(payload, "prompt_language", args.prompt_language)
    maybe_add(payload, "intelligibility_weight", args.intelligibility_weight)
    maybe_add(payload, "similarity_weight", args.similarity_weight)
    maybe_add(payload, "temperature", args.temperature)
    maybe_add(payload, "top_P", args.top_p)
    maybe_add(payload, "top_K", args.top_k)
    maybe_add(payload, "gender", args.gender)
    maybe_add(payload, "pitch", args.pitch)
    maybe_add(payload, "speed", args.speed)

    if official_model == "MOSS-TTSD-v0.5":
        audio_mode = validate_moss_ttsd_args(args)
        payload["audio_mode"] = audio_mode
        maybe_add(payload, "prompt_audio_single_url", args.prompt_audio_single_url)
        maybe_add(payload, "prompt_text_single", args.prompt_text_single)
        maybe_add(payload, "prompt_audio_1_url", args.prompt_audio_1_url)
        maybe_add(payload, "prompt_text_1", args.prompt_text_1)
        maybe_add(payload, "prompt_audio_2_url", args.prompt_audio_2_url)
        maybe_add(payload, "prompt_text_2", args.prompt_text_2)
        if args.use_normalize is not None:
            payload["use_normalize"] = args.use_normalize == "true"

    if official_model == "VibeVoice-Large":
        prompt_audio_urls = parse_prompt_audio_urls(args.prompt_audio_urls)
        if prompt_audio_urls is None and args.prompt_audio_url:
            prompt_audio_urls = normalize_prompt_audio_urls_value(args.prompt_audio_url)
        if prompt_audio_urls is not None:
            payload["prompt_audio_urls"] = prompt_audio_urls
            payload.pop("prompt_audio_url", None)

    if official_model == "AudioFly":
        maybe_add(payload, "num_inference_steps", args.num_inference_steps)
        maybe_add(payload, "guidance_scale", args.guidance_scale)
        maybe_add(payload, "output_format", args.output_format)

    if official_model == "Qwen3-TTS":
        if args.qwen_inputs_json:
            payload["inputs"] = parse_qwen_inputs_json(args.qwen_inputs_json)
        else:
            payload["inputs"] = [build_qwen_single_input(args)]
        maybe_add(payload, "output_format", args.output_format)

        # Qwen3-TTS uses structured items in "inputs", not top-level prompt fields.
        for key in (
                "prompt",
                "prompt_text",
                "prompt_audio_url",
                "voice_url",
                "instruct_text",
                "gender",
                "pitch",
                "speed",
        ):
            payload.pop(key, None)

    payload.update(extra_body)

    response = request_http(
        "POST",
        f"{BASE_URL}/async/audio/speech",
        headers=build_headers(api_key, args.failover_enabled),
        json_body=payload,
    )
    task = response.json()

    print(f"MODEL: {official_model}")
    print("MODE: async")
    if task.get("task_id"):
        print(f"TASK_ID: {task['task_id']}")

    result = wait_for_async_result(
        api_key=api_key,
        task=task,
        timeout_seconds=args.timeout,
        poll_interval_seconds=args.poll_interval,
    )

    output = result.get("output")
    audio_url = extract_first_url(output) or extract_first_url(result)
    if audio_url:
        print(f"AUDIO_URL: {audio_url}")
    print(f"TTS_RESULT: {json.dumps(result, ensure_ascii=False)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate speech with Gitee AI TTS models")
    parser.add_argument(
        "--model",
        "-m",
        required=True,
        help="Model alias or official model name, e.g. audiofly / chattts / cosyvoice2 / cosyvoice3 / cosyvoice-300m / fish-speech-1.2-sft / index-tts-1.5 / index-tts-2 / glm-tts / megatts3 / moss-ttsd-v0.5 / qwen-tts / spark-tts-0.5b / step-audio-tts-3b / vibevoice-large",
    )
    parser.add_argument(
        "--text",
        "-t",
        help="Text content to convert into speech. Optional for Qwen3-TTS when --qwen-inputs-json is provided",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "sync", "async"],
        default="auto",
        help="Force sync/async mode. Default: auto",
    )
    parser.add_argument(
        "--response-data-format",
        choices=["url", "blob"],
        default="url",
        help="Sync response format. Default: url",
    )
    parser.add_argument(
        "--voice",
        help="Optional voice name for OpenAI-compatible TTS models such as ChatTTS, fish-speech-1.2-sft, FunAudioLLM-CosyVoice-300M, IndexTTS-1.5, CosyVoice2, CosyVoice3, MegaTTS3, and Step-Audio-TTS-3B",
    )
    parser.add_argument(
        "--prompt",
        help="Model-specific prompt token, such as ChatTTS style tags like [oral_1]",
    )
    parser.add_argument(
        "--prompt-text",
        help="Style/reference transcript text. Primarily useful for Spark-TTS-0.5B, Step-Audio-TTS-3B, IndexTTS-2, and Qwen3-TTS",
    )
    parser.add_argument(
        "--prompt-audio-url",
        help="Reference audio URL. Primarily useful for Spark-TTS-0.5B, Step-Audio-TTS-3B, IndexTTS-1.5, IndexTTS-2, and Qwen3-TTS",
    )
    parser.add_argument(
        "--qwen-inputs-json",
        help="Qwen3-TTS structured inputs JSON (array or single object). Each item supports prompt, speaker/language/instruction, or custom voice prompt_audio_url+prompt_text.",
    )
    parser.add_argument(
        "--speaker",
        help="Qwen3-TTS built-in speaker for single input. Options: Vivian, Serena, Uncle_Fu, Dylan, Eric, Ryan, Aiden, Ono_Anna, Sohee",
    )
    parser.add_argument(
        "--language",
        choices=QWEN3_TTS_LANGUAGES,
        help="Qwen3-TTS language for single input: Chinese or English",
    )
    parser.add_argument(
        "--instruction",
        help="Qwen3-TTS speaking style instruction for single input",
    )
    parser.add_argument(
        "--prompt-audio-urls",
        help="VibeVoice-Large prompt audio URLs. Pass one URL, or a JSON array string such as '[\"https://a.wav\", \"https://b.wav\"]'",
    )
    parser.add_argument(
        "--emo-audio-prompt-url",
        help="Emotion audio prompt URL for IndexTTS-2 emotion-controlled generation",
    )
    parser.add_argument(
        "--emo-alpha",
        type=float,
        help="Emotion mix weight for IndexTTS-2 when using emo_audio_prompt_url",
    )
    parser.add_argument(
        "--emo-text",
        help="Emotion control text for IndexTTS-2",
    )
    parser.add_argument(
        "--use-emo-text",
        choices=["true", "false"],
        help="Whether to enable emo_text for IndexTTS-2",
    )
    parser.add_argument(
        "--prompt-wav-url",
        help="Reference prompt wav URL. Primarily useful for CosyVoice2 and CosyVoice3",
    )
    parser.add_argument(
        "--voice-url",
        help="Reference voice audio URL. Primarily useful for ChatTTS, fish-speech-1.2-sft, and FunAudioLLM-CosyVoice-300M",
    )
    parser.add_argument(
        "--instruct-text",
        help="Instruction text for models that expose controllable style prompts, such as CosyVoice2 and CosyVoice3",
    )
    parser.add_argument(
        "--seed",
        help="Seed value for models that expose deterministic generation controls, such as CosyVoice2 and CosyVoice3",
    )
    parser.add_argument(
        "--audio-mode",
        help="MOSS-TTSD-v0.5 audio mode: single or role",
    )
    parser.add_argument(
        "--prompt-audio-single-url",
        help="MOSS-TTSD-v0.5 single mode reference audio URL",
    )
    parser.add_argument(
        "--prompt-text-single",
        help="MOSS-TTSD-v0.5 single mode reference transcript text",
    )
    parser.add_argument(
        "--prompt-audio-1-url",
        help="MOSS-TTSD-v0.5 role mode speaker-1 reference audio URL",
    )
    parser.add_argument(
        "--prompt-text-1",
        help="MOSS-TTSD-v0.5 role mode speaker-1 reference transcript text",
    )
    parser.add_argument(
        "--prompt-audio-2-url",
        help="MOSS-TTSD-v0.5 role mode speaker-2 reference audio URL",
    )
    parser.add_argument(
        "--prompt-text-2",
        help="MOSS-TTSD-v0.5 role mode speaker-2 reference transcript text",
    )
    parser.add_argument(
        "--use-normalize",
        choices=["true", "false"],
        help="MOSS-TTSD-v0.5 text normalization switch",
    )
    parser.add_argument(
        "--prompt-language",
        help="Prompt language hint for models that expose it, such as MegaTTS3",
    )
    parser.add_argument(
        "--intelligibility-weight",
        type=float,
        help="Intelligibility weight for models that expose it, such as MegaTTS3",
    )
    parser.add_argument(
        "--similarity-weight",
        type=float,
        help="Similarity weight for models that expose it, such as MegaTTS3",
    )
    parser.add_argument(
        "--failover-enabled",
        choices=["true", "false"],
        default="true",
        help="X-Failover-Enabled header value. Default: true",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Sampling temperature for models that expose it, such as ChatTTS",
    )
    parser.add_argument(
        "--top-p",
        type=float,
        help="Top-p sampling value for models that expose it, such as ChatTTS",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        help="Top-k sampling value for models that expose it, such as ChatTTS",
    )
    parser.add_argument(
        "--gender",
        help="Gender hint for async TTS models",
    )
    parser.add_argument(
        "--pitch",
        type=int,
        help="Pitch hint for async TTS models",
    )
    parser.add_argument(
        "--speed",
        type=int,
        help="Speed hint for async TTS models, such as CosyVoice3, Spark-TTS-0.5B, and Qwen3-TTS",
    )
    parser.add_argument(
        "--num-inference-steps",
        type=int,
        help="AudioFly inference steps for diffusion-style generation",
    )
    parser.add_argument(
        "--guidance-scale",
        type=float,
        help="AudioFly guidance scale",
    )
    parser.add_argument(
        "--output-format",
        help="AudioFly or Qwen3-TTS output format, for example mp3 or wav",
    )
    parser.add_argument(
        "--extra-body-json",
        help="Extra request body fields as a JSON object",
    )
    parser.add_argument(
        "--output",
        help="Output file path when response_data_format=blob",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Async wait timeout in seconds. Default: {DEFAULT_TIMEOUT}",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL,
        help=f"Async poll interval in seconds. Default: {DEFAULT_POLL_INTERVAL}",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        help="Gitee AI API key (overrides GITEEAI_API_KEY env var)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GITEEAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    try:
        config = normalize_model(args.model)
        mode = choose_mode(args, config)
        validate_text_requirement(args, config["official"])
        extra_body = parse_extra_body_json(args.extra_body_json)

        if mode == "sync":
            run_sync(
                api_key=api_key,
                official_model=config["official"],
                args=args,
                extra_body=extra_body,
            )
        else:
            run_async(
                api_key=api_key,
                official_model=config["official"],
                args=args,
                extra_body=extra_body,
            )
    except TTSConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(2)
    except RuntimeError as exc:
        print(f"Error generating speech: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
