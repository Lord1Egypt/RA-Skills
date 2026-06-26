from __future__ import annotations

import math
import re

import requests


def extract_error_info(exception: Exception) -> dict:
    error_str = str(exception)
    if isinstance(exception, requests.HTTPError):
        status_code = exception.response.status_code
        try:
            payload = exception.response.json()
            return {
                "code": payload.get("code") if payload.get("code") else status_code,
                "message": payload.get("message", "") or error_str,
                "type": f"http_{status_code}",
                "raw_response": payload,
            }
        except Exception:
            return {"code": status_code, "message": error_str, "type": f"http_{status_code}"}
    code_match = re.search(r"code[=:]?\s*(\d+)", error_str, re.IGNORECASE)
    if code_match:
        code = int(code_match.group(1))
        return {"code": code, "message": error_str, "type": f"api_{code}"}
    if isinstance(exception, TimeoutError):
        return {"code": "timeout", "message": error_str, "type": "timeout"}
    return {"code": "unknown", "message": error_str, "type": "unknown"}


def _parse_min_pixels(text: str) -> int | None:
    match = re.search(
        r"(?:at\s+least\s+(\d+)\s+pixels|pixels?\s+should\s+be\s+at\s+least\s+(\d+))",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None
    return int(match.group(1) or match.group(2))


def _parse_size_dims(value) -> tuple[int, int] | None:
    if not isinstance(value, str):
        return None
    match = re.search(r"(\d{2,5})\s*[xX×]\s*(\d{2,5})", value)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def build_contextual_diagnosis(
    error_info: dict,
    task_type: str,
    model_params: dict,
    current_params: dict | None,
    input_images: list[str] | None,
    credit_rules: list | None,
) -> dict:
    del credit_rules
    code = error_info.get("code")
    raw_message = str(error_info.get("message") or "")
    msg_lower = raw_message.lower()
    merged_params = dict(model_params.get("form_params") or {})
    merged_params.update(current_params or {})

    diagnosis = {
        "code": code,
        "confidence": "medium",
        "headline": "Model task failed with current configuration",
        "reasoning": [],
        "actions": [],
        "model_name": model_params.get("model_name") or "unknown_model",
        "model_id": model_params.get("model_id") or "unknown_model_id",
        "task_type": task_type,
    }

    if task_type == "image_to_image" and not (input_images or []):
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Missing required reference image for image_to_image"
        diagnosis["reasoning"].append("image_to_image requires at least one input image URL/path.")
        diagnosis["actions"].append("Provide --input-images with at least one image URL/path.")
        return diagnosis

    if code == 401 or "unauthorized" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "API key is invalid or unauthorized"
        diagnosis["actions"].append("Regenerate API key: https://www.imaclaw.ai/imaclaw/apikey")
        diagnosis["actions"].append("Retry with the new key in --api-key.")
        return diagnosis

    if code == 4008 or "insufficient points" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Account points are not enough for this image request"
        diagnosis["actions"].append("Top up credits: https://www.imaclaw.ai/imaclaw/subscription")
        diagnosis["actions"].append("Or switch to a lower-cost model/size.")
        return diagnosis

    min_pixels = _parse_min_pixels(raw_message)
    dims = _parse_size_dims(str(merged_params.get("size") or "")) or _parse_size_dims(raw_message)
    if min_pixels is not None and dims is not None:
        requested_pixels = dims[0] * dims[1]
        if requested_pixels < min_pixels:
            diagnosis["confidence"] = "high"
            diagnosis["headline"] = "Output size is below this model's minimum pixel requirement"
            diagnosis["reasoning"].append(
                f"Requested size {dims[0]}x{dims[1]} ({requested_pixels} px) is below required {min_pixels} px."
            )
            approx_edge = int(math.ceil(math.sqrt(min_pixels)))
            diagnosis["actions"].append(f"Increase --size to at least around {approx_edge}x{approx_edge}.")
            return diagnosis

    if "output aspect ratio does not match requested aspect_ratio" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Generated image aspect ratio does not match the requested constraint"
        diagnosis["actions"].append("Retry with a model that explicitly supports the requested aspect ratio in the live catalog.")
        diagnosis["actions"].append("Or remove the aspect ratio constraint and adjust the prompt.")
        return diagnosis

    if "output dimensions do not match requested size" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Generated image dimensions do not match the requested size constraint"
        diagnosis["actions"].append("Retry with a model that explicitly supports the requested size in the live catalog.")
        diagnosis["actions"].append("Or remove the size constraint and adjust the prompt.")
        return diagnosis

    if code in (6009, 6010) or "attribute" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Current parameter combination does not fit this model rule set"
        diagnosis["actions"].append("Remove custom --extra-params and retry with defaults.")
        return diagnosis

    if code == "timeout" or "timed out" in msg_lower:
        diagnosis["headline"] = "Task exceeded polling timeout for current image settings"
        diagnosis["actions"].append("Retry with lower size/quality.")
        return diagnosis

    diagnosis["actions"].append("Retry with defaults (remove --extra-params).")
    diagnosis["actions"].append("Use --list-models to verify supported settings.")
    return diagnosis


def format_user_failure_message(diagnosis: dict, attempts_used: int, max_attempts: int) -> str:
    lines = [
        f"Task failed after {attempts_used}/{max_attempts} attempt(s).",
        f"Likely cause ({diagnosis.get('confidence', 'medium')} confidence): {diagnosis.get('headline')}",
    ]
    for index, action in enumerate(diagnosis.get("actions") or [], 1):
        lines.append(f"{index}. {action}")
    if diagnosis.get("code") not in (None, "", "unknown"):
        lines.append(f"Reference code: {diagnosis['code']}")
    return "\n".join(lines)
