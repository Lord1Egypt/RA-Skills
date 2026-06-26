from __future__ import annotations

import re
import time

import requests

from ima_runtime.capabilities.video.params import build_video_model_params, normalize_video_binding
from ima_runtime.shared.client import create_task, poll_task
from ima_runtime.shared.config import POLL_CONFIG
from ima_runtime.shared.types import ExecutionResult, MediaPayloadBundle, ModelBinding, TaskSpec


_NON_RETRYABLE_CREATE_CODES = {"401", "4014", "4008", "6009", "6010"}
_NON_RETRYABLE_CREATE_PATTERNS = (
    "missing-media",
    "missing media",
    "validation failed",
    "validation error",
)
_RETRYABLE_REQUEST_EXCEPTION_TYPES = (
    requests.ConnectionError,
    requests.Timeout,
)
_RETRYABLE_REQUEST_MESSAGE_PATTERNS = (
    "connection aborted",
    "connection broken",
    "connection reset",
    "connection refused",
    "temporarily unavailable",
    "temporary failure",
    "name resolution",
    "remote disconnected",
)


def _extract_error_code(message: str) -> str | None:
    match = re.search(r"code[=:]?\s*(\d+)", message, re.IGNORECASE)
    if not match:
        return None
    return match.group(1)


def _is_non_retryable_create_error(exc: Exception) -> bool:
    message = str(exc).lower()
    code = _extract_error_code(message)
    if code in _NON_RETRYABLE_CREATE_CODES:
        return True
    return any(pattern in message for pattern in _NON_RETRYABLE_CREATE_PATTERNS)


def _is_retryable_create_error(exc: Exception) -> bool:
    if _is_non_retryable_create_error(exc):
        return False

    if isinstance(exc, TimeoutError):
        return True

    if isinstance(exc, requests.HTTPError):
        response = exc.response
        status_code = response.status_code if response is not None else None
        return status_code is not None and 500 <= status_code < 600

    if isinstance(exc, requests.RequestException):
        if isinstance(exc, _RETRYABLE_REQUEST_EXCEPTION_TYPES):
            return True
        message = str(exc).lower()
        return any(pattern in message for pattern in _RETRYABLE_REQUEST_MESSAGE_PATTERNS)

    message = str(exc).lower()
    code = _extract_error_code(message)
    if code == "500":
        return True
    return "internal server error" in message or "timed out" in message or "timeout" in message


def _retry_sleep(delay_seconds: int) -> None:
    time.sleep(delay_seconds)


def create_task_with_reflection(base_url: str, api_key: str, task_type: str, model_params: dict, prompt: str, input_images: list[str], extra_params: dict | None = None, src_image: list[dict] | None = None, src_video: list[dict] | None = None, src_audio: list[dict] | None = None, max_attempts: int = 3) -> str:
    last_error: Exception | None = None
    attempts_used = 0
    for attempts_used in range(1, max_attempts + 1):
        try:
            return create_task(
                base_url,
                api_key,
                task_type,
                model_params,
                prompt,
                input_images,
                extra_params,
                src_image=src_image,
                src_video=src_video,
                src_audio=src_audio,
            )
        except (RuntimeError, requests.RequestException, TimeoutError) as exc:
            last_error = exc
            if attempts_used >= max_attempts or not _is_retryable_create_error(exc):
                break
            _retry_sleep(attempts_used)
    assert last_error is not None
    error = RuntimeError(
        f"Task creation failed after {attempts_used}/{max_attempts} attempt(s): {last_error}"
    )
    error.attempts_used = attempts_used
    error.max_attempts = max_attempts
    raise error from last_error


def execute_video_task(base_url: str, api_key: str, spec: TaskSpec, binding: ModelBinding, media_bundle: MediaPayloadBundle | None = None) -> ExecutionResult:
    model_params = build_video_model_params(binding)
    extra_params, _ = normalize_video_binding(spec, model_params)
    cfg = POLL_CONFIG.get(spec.task_type, {"interval": 8, "max_wait": 300})
    bundle = media_bundle or MediaPayloadBundle(input_images=tuple(spec.input_images))
    task_id = create_task_with_reflection(
        base_url=base_url,
        api_key=api_key,
        task_type=spec.task_type,
        model_params=model_params,
        prompt=spec.prompt,
        input_images=list(bundle.input_images),
        extra_params=extra_params or None,
        src_image=list(bundle.src_image) or None,
        src_video=list(bundle.src_video) or None,
        src_audio=list(bundle.src_audio) or None,
    )
    media = poll_task(
        base_url,
        api_key,
        task_id,
        estimated_max=cfg["max_wait"] // 2,
        poll_interval=cfg["interval"],
        max_wait=cfg["max_wait"],
    )
    return ExecutionResult(
        task_id=task_id,
        url=media.get("url") or media.get("preview_url") or "",
        cover_url=media.get("cover_url") or "",
        model_id=binding.candidate.model_id,
        model_name=binding.candidate.name,
        credit=binding.credit,
    )
