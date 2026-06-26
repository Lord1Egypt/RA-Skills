from __future__ import annotations

import re

from ima_runtime.shared.types import ModelBinding, TaskSpec

"""
Prompt control inference.

Conflict resolution:
- Explicit `--model-id` always wins over prompt inference.
- When multiple model hints appear in the prompt, choose the first match by prompt position.
- If two model patterns start at the same position, prefer the earlier pattern in MODEL_ALIAS_HINTS.
- `aspect_ratio` and `size` are preserved together; backend validation decides whether the
  combination is supported by the chosen model.
"""

MODEL_ALIAS_HINTS = (
    (r"(?<![a-z0-9])gpt[- ]image[- ]?2(?![a-z0-9])", "gpt-image-2"),
    (r"(?<![a-z0-9])gptimage2(?![a-z0-9])", "gpt-image-2"),
    (r"(?<![a-z0-9])mj(?![a-z0-9])", "midjourney"),
    (r"(?<![a-z0-9])midjourney(?![a-z0-9])", "midjourney"),
    (r"香蕉\s*pro", "gemini-3-pro-image"),
    (r"(?<![a-z0-9])nano banana pro(?![a-z0-9])", "gemini-3-pro-image"),
    (r"(?<![a-z0-9])banana pro(?![a-z0-9])", "gemini-3-pro-image"),
    (r"香蕉", "gemini-3.1-flash-image"),
    (r"(?<![a-z0-9])nano banana 2(?![a-z0-9])", "gemini-3.1-flash-image"),
    (r"(?<![a-z0-9])nano banana2(?![a-z0-9])", "gemini-3.1-flash-image"),
    (r"(?<![a-z0-9])nano banana(?![a-z0-9])", "gemini-3.1-flash-image"),
    (r"可梦", "doubao-seedream-4.5"),
    (r"(?<![a-z0-9])seedream 4\.5(?![a-z0-9])", "doubao-seedream-4.5"),
    (r"(?<![a-z0-9])seedream(?![a-z0-9])", "doubao-seedream-4.5"),
)

ASPECT_RATIO_HINTS = ("21:9", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2", "1:1")


def infer_prompt_controls(prompt: str) -> dict:
    controls: dict[str, str] = {}
    if not prompt:
        return controls

    lowered = prompt.lower()
    matched_model: tuple[int, int, str] | None = None
    for index, (pattern, model_id) in enumerate(MODEL_ALIAS_HINTS):
        match = re.search(pattern, lowered)
        if not match:
            continue
        candidate = (match.start(), index, model_id)
        if matched_model is None or candidate < matched_model:
            matched_model = candidate
    if matched_model is not None:
        controls["__model_id__"] = matched_model[2]

    for ratio in ASPECT_RATIO_HINTS:
        if ratio in prompt:
            controls["aspect_ratio"] = ratio
            break

    if re.search(r"(?<![a-z0-9])4k(?![a-z0-9])", lowered):
        controls["size"] = "4k"
    elif re.search(r"(?<![a-z0-9])2k(?![a-z0-9])", lowered):
        controls["size"] = "2k"
    elif re.search(r"(?<![a-z0-9])1k(?![a-z0-9])", lowered):
        controls["size"] = "1k"
    elif "512" in lowered:
        controls["size"] = "512px"

    return controls


def build_image_model_params(binding: ModelBinding) -> dict:
    resolved_params = dict(binding.resolved_params)
    if "form_params" not in resolved_params:
        raise RuntimeError("Image model binding missing required resolved param: form_params")
    return {
        "attribute_id": binding.attribute_id,
        "credit": binding.credit,
        "model_id": binding.candidate.model_id,
        "model_name": binding.candidate.name,
        "model_version": binding.candidate.version_id,
        "form_params": dict(resolved_params["form_params"]),
        "rule_attributes": dict(resolved_params.get("rule_attributes", {})),
        "all_credit_rules": list(resolved_params.get("all_credit_rules", [])),
        "virtual_param_specs": list(resolved_params.get("virtual_param_specs", [])),
        "field_option_specs": dict(resolved_params.get("field_option_specs", {})),
    }


def normalize_image_binding(spec: TaskSpec, model_params: dict) -> tuple[dict, dict]:
    del model_params
    extra = dict(spec.extra_params)
    dropped = {}
    if spec.task_type == "text_to_image":
        for key in ("input_images", "src_img_url"):
            if key in extra:
                dropped[key] = extra.pop(key)
    return extra, dropped
