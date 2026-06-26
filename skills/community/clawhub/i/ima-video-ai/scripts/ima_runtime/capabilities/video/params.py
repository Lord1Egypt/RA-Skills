from __future__ import annotations

from ima_runtime.shared.types import ModelBinding, TaskSpec


def build_video_model_params(binding: ModelBinding) -> dict:
    resolved_params = dict(binding.resolved_params)
    if "form_params" not in resolved_params:
        raise RuntimeError("Video model binding missing required resolved param: form_params")

    return {
        "attribute_id": binding.attribute_id,
        "credit": binding.credit,
        "model_id": binding.candidate.model_id,
        "model_id_raw": resolved_params.get("model_id_raw", binding.candidate.model_id),
        "model_name": binding.candidate.name,
        "model_version": binding.candidate.version_id,
        "form_params": dict(resolved_params["form_params"]),
        "rule_attributes": dict(resolved_params.get("rule_attributes", {})),
        "all_credit_rules": list(resolved_params.get("all_credit_rules", [])),
        "virtual_fields": list(resolved_params.get("virtual_fields", [])),
    }


def normalize_video_binding(spec: TaskSpec, model_params: dict) -> tuple[dict, dict]:
    extra = dict(spec.extra_params)
    dropped: dict = {}
    if spec.task_type == "text_to_video":
        extra.pop("src_img_url", None)
    return extra, dropped
