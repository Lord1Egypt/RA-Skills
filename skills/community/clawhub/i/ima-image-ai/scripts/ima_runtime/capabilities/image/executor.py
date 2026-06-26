from __future__ import annotations

from ima_runtime.capabilities.image.params import build_image_model_params, normalize_image_binding
from ima_runtime.shared.catalog import apply_virtual_param_specs
from ima_runtime.shared.client import create_task, poll_task
from ima_runtime.shared.output_validation import validate_output_constraints

try:
    from ima_runtime.shared.config import POLL_CONFIG
except Exception:  # pragma: no cover - fallback during partial migration
    POLL_CONFIG = {
        "text_to_image": {"interval": 5, "max_wait": 600},
        "image_to_image": {"interval": 5, "max_wait": 600},
    }

from ima_runtime.shared.types import ExecutionResult, ModelBinding, TaskSpec


def create_task_with_reflection(
    base_url: str,
    api_key: str,
    task_type: str,
    model_params: dict,
    prompt: str,
    input_images: list[str],
    extra_params: dict | None = None,
    max_attempts: int = 3,
) -> str:
    last_error: Exception | None = None
    for attempts_used in range(1, max_attempts + 1):
        try:
            return create_task(base_url, api_key, task_type, model_params, prompt, input_images, extra_params)
        except RuntimeError as exc:
            last_error = exc
            if attempts_used >= max_attempts:
                break
    assert last_error is not None
    error = RuntimeError(f"Task creation failed after {max_attempts}/{max_attempts} attempt(s): {last_error}")
    error.attempts_used = max_attempts
    error.max_attempts = max_attempts
    raise error from last_error


def execute_image_task(base_url: str, api_key: str, spec: TaskSpec, binding: ModelBinding) -> ExecutionResult:
    model_params = build_image_model_params(binding)
    extra_params, _ = normalize_image_binding(spec, model_params)
    effective_params, _ = apply_virtual_param_specs(extra_params, model_params.get("virtual_param_specs") or [])
    cfg = POLL_CONFIG.get(spec.task_type, {"interval": 5, "max_wait": 300})
    task_id = create_task_with_reflection(
        base_url=base_url,
        api_key=api_key,
        task_type=spec.task_type,
        model_params=model_params,
        prompt=spec.prompt,
        input_images=list(spec.input_images),
        extra_params=effective_params or None,
    )
    media = poll_task(
        base_url,
        api_key,
        task_id,
        estimated_max=cfg["max_wait"] // 2,
        poll_interval=cfg["interval"],
        max_wait=cfg["max_wait"],
    )
    result_url = media.get("url") or media.get("preview_url") or ""
    validate_output_constraints(result_url, raw_params=dict(spec.extra_params), effective_params=effective_params)
    return ExecutionResult(
        task_id=task_id,
        url=result_url,
        cover_url=media.get("cover_url") or "",
        model_id=binding.candidate.model_id,
        model_name=binding.candidate.name,
        credit=binding.credit,
    )
