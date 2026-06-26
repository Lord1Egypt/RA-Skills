from __future__ import annotations

import math
import re

import requests

from ima_runtime.shared.catalog import canonicalize_model_id
from ima_runtime.shared.config import VIDEO_RECORDS_URL


def normalize_model_id(model_id: str | None) -> str | None:
    """Normalize known model aliases; return original model_id when no alias applies."""
    return canonicalize_model_id(model_id)


def to_user_facing_model_name(model_name: str | None, model_id: str | None) -> str:
    """Return user-facing product branding for known canonical model IDs."""
    canonical = normalize_model_id(model_id)
    if canonical == "ima-pro":
        return "Seedance 2.0"
    if canonical == "ima-pro-fast":
        return "Seedance 2.0 Fast"
    return model_name or "IMA Model"


def extract_error_info(exception: Exception) -> dict:
    """
    Extract error code and message from exception.

    Handles:
    - RuntimeError from create_task with code in message
    - requests.HTTPError (500, 400, etc.)
    - TimeoutError from poll_task

    Returns: {"code": int|str, "message": str, "type": str}
    """
    error_str = str(exception)

    # Check for HTTP status codes (500, 400, etc.)
    if isinstance(exception, requests.HTTPError):
        status_code = exception.response.status_code
        try:
            response_data = exception.response.json()
            api_code = response_data.get("code")
            api_msg = response_data.get("message", "")
            return {
                "code": api_code if api_code else status_code,
                "message": api_msg or error_str,
                "type": f"http_{status_code}",
                "raw_response": response_data
            }
        except:
            return {
                "code": status_code,
                "message": error_str,
                "type": f"http_{status_code}"
            }

    # Check for API error codes in RuntimeError message (6009, 6010, etc.)
    code_match = re.search(r'code[=:]?\s*(\d+)', error_str, re.IGNORECASE)
    if code_match:
        code = int(code_match.group(1))
        return {
            "code": code,
            "message": error_str,
            "type": f"api_{code}"
        }

    # Timeout error
    if isinstance(exception, TimeoutError):
        return {
            "code": "timeout",
            "message": error_str,
            "type": "timeout"
        }

    # Generic error
    return {
        "code": "unknown",
        "message": error_str,
        "type": "unknown"
    }


def _normalize_compare_value(value) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().upper()


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


def _format_rule_attributes(rule: dict, max_items: int = 4) -> str:
    attrs = rule.get("attributes") or {}
    parts = [f"{k}={v}" for k, v in attrs.items() if not (k == "default" and v == "enabled")]
    if not parts:
        return "<default rule>"
    return ", ".join(parts[:max_items])


def _best_rule_mismatch(credit_rules: list, merged_params: dict) -> dict | None:
    if not credit_rules:
        return None
    best = None
    normalized_params = {
        str(k).strip().lower(): _normalize_compare_value(v)
        for k, v in merged_params.items()
    }
    for rule in credit_rules:
        attrs = rule.get("attributes") or {}
        if not attrs:
            continue
        missing: list[str] = []
        conflicts: list[tuple[str, str, str]] = []
        matched = 0
        for key, expected in attrs.items():
            if key == "default" and expected == "enabled":
                continue
            k = str(key).strip().lower()
            expected_norm = _normalize_compare_value(expected)
            actual_norm = normalized_params.get(k)
            if actual_norm is None:
                missing.append(str(key))
            elif actual_norm == expected_norm:
                matched += 1
            else:
                actual_raw = merged_params.get(key, merged_params.get(k, ""))
                conflicts.append((str(key), str(actual_raw), str(expected)))
        score = matched * 3 - len(missing) * 2 - len(conflicts) * 3
        candidate = {
            "rule": rule,
            "missing": missing,
            "conflicts": conflicts,
            "score": score,
        }
        if best is None or candidate["score"] > best["score"]:
            best = candidate
    return best


def build_contextual_diagnosis(error_info: dict,
                               task_type: str,
                               model_params: dict,
                               current_params: dict | None,
                               input_images: list[str] | None,
                               credit_rules: list | None) -> dict:
    code = error_info.get("code")
    code_str = str(code).strip() if code is not None else ""
    raw_message = str(error_info.get("message") or "")
    msg_lower = raw_message.lower()
    merged_params = dict(model_params.get("form_params") or {})
    merged_params.update(current_params or {})
    media_inputs = input_images or []
    model_name = model_params.get("model_name") or "unknown_model"
    model_id = model_params.get("model_id") or "unknown_model_id"

    diagnosis = {
        "code": code,
        "confidence": "medium",
        "headline": "Model task failed with current configuration",
        "reasoning": [],
        "actions": [],
        "model_name": model_name,
        "model_id": model_id,
        "task_type": task_type,
    }

    input_required = {
        "image_to_video",
        "first_last_frame_to_video",
        "reference_image_to_video",
    }
    if task_type in input_required and not media_inputs:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Missing required reference media for this task type"
        diagnosis["reasoning"].append(f"{task_type} requires input media, but input_images is empty.")
        diagnosis["actions"].append("Provide at least one URL/path via --input-images.")
        if task_type == "first_last_frame_to_video":
            diagnosis["actions"].append("Provide at least 2 frames: first and last.")
        return diagnosis

    if task_type == "first_last_frame_to_video" and 0 < len(media_inputs) < 2:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Insufficient frames for first_last_frame_to_video"
        diagnosis["actions"].append("Pass two frame URLs in --input-images.")
        return diagnosis

    api_key_error_patterns = (
        r"\bunauthorized\b",
        r"\binvalid\s+api(?:\s|_|-)key\b",
        r"\bmissing\s+api(?:\s|_|-)key\b",
        r"\bapi(?:\s|_|-)key\s+is\s+required\b",
        r"\bapi(?:\s|_|-)key\s+required\b",
        r"\brequires?\s+an?\s+api(?:\s|_|-)key\b",
    )
    if code_str == "401" or any(re.search(pattern, msg_lower) for pattern in api_key_error_patterns):
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "API key is missing, invalid, or unauthorized"
        diagnosis["actions"].append("Create or regenerate your API key: https://www.imaclaw.ai/imaclaw/apikey")
        diagnosis["actions"].append("Retry with the new key in --api-key.")
        return diagnosis

    if code in (4014, "4014") or code_str == "4014" or "requires a subscription" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Current model requires an active subscription plan"
        diagnosis["actions"].append("Activate or upgrade your plan: https://www.imaclaw.ai/imaclaw/subscription")
        diagnosis["actions"].append("Then retry the same request.")
        return diagnosis

    if code in (4008, "4008") or code_str == "4008" or "insufficient points" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Account points are not enough for this video request"
        diagnosis["actions"].append("Top up credits: https://www.imaclaw.ai/imaclaw/subscription")
        diagnosis["actions"].append("Or switch to a lower-cost model profile.")
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
            target = int(math.ceil(math.sqrt(min_pixels)))
            diagnosis["actions"].append(f"Increase --size to at least around {target}x{target}.")
            diagnosis["actions"].append("Retry with the same model.")
            return diagnosis

    credit_rules = credit_rules or []
    rule_mismatch = _best_rule_mismatch(credit_rules, merged_params)
    if (
        code in (6009, 6010)
        or "invalid product attribute" in msg_lower
        or "no matching" in msg_lower
        or "attribute" in msg_lower
    ):
        diagnosis["confidence"] = "high" if code in (6009, 6010) else "medium"
        diagnosis["headline"] = "Current parameter combination does not fit this model rule set"
        if rule_mismatch:
            if rule_mismatch["missing"]:
                diagnosis["reasoning"].append(
                    "Missing parameters for best-matching rule: "
                    + ", ".join(rule_mismatch["missing"][:4])
                )
            if rule_mismatch["conflicts"]:
                compact = ", ".join(
                    f"{k}={got} (expected {expected})"
                    for k, got, expected in rule_mismatch["conflicts"][:3]
                )
                diagnosis["reasoning"].append(f"Conflicting values: {compact}")
            diagnosis["actions"].append(
                "Use a rule-compatible profile: " + _format_rule_attributes(rule_mismatch["rule"])
            )
        diagnosis["actions"].append("Remove custom --extra-params and retry with defaults.")
        return diagnosis

    if code == "timeout" or "timed out" in msg_lower:
        diagnosis["headline"] = "Task exceeded polling timeout for current video settings"
        diagnosis["actions"].append("Retry with lower resolution/duration.")
        diagnosis["actions"].append(f"Check your creation record: {VIDEO_RECORDS_URL}")
        return diagnosis

    if code == 500 or "internal server error" in msg_lower:
        diagnosis["headline"] = "Backend rejected current parameter complexity"
        for key in ("resolution", "duration", "mode", "quality"):
            if key in merged_params:
                fallback = get_param_degradation_strategy(key, str(merged_params[key]))
                if fallback:
                    diagnosis["actions"].append(f"Try {key}={fallback[0]} (current {merged_params[key]}).")
                    break
        diagnosis["actions"].append("Retry after simplifying parameters.")
        return diagnosis

    diagnosis["reasoning"].append(
        f"Model context: {to_user_facing_model_name(model_name, model_id)}, "
        f"task={task_type}, media_count={len(media_inputs)}."
    )
    diagnosis["actions"].append("Retry with defaults (remove --extra-params).")
    diagnosis["actions"].append("Use --list-models to verify supported settings.")
    return diagnosis


def format_user_failure_message(diagnosis: dict,
                                attempts_used: int,
                                max_attempts: int) -> str:
    display_model = to_user_facing_model_name(
        diagnosis.get("model_name"),
        diagnosis.get("model_id"),
    )
    lines = [
        f"Task failed after {attempts_used}/{max_attempts} attempt(s).",
        (
            f"Model: {display_model} | "
            f"Task: {diagnosis.get('task_type')}"
        ),
        f"Likely cause ({diagnosis.get('confidence', 'medium')} confidence): {diagnosis.get('headline')}",
    ]
    reasoning = diagnosis.get("reasoning") or []
    if reasoning:
        lines.append("Why this diagnosis:")
        for item in reasoning[:3]:
            lines.append(f"- {item}")
    actions = diagnosis.get("actions") or []
    if actions:
        lines.append("What to do next:")
        for i, action in enumerate(actions[:4], 1):
            lines.append(f"{i}. {action}")
    code = diagnosis.get("code")
    if code not in (None, "", "unknown"):
        lines.append(f"Reference code: {code}")
    lines.append("Technical details were recorded in local logs.")
    return "\n".join(lines)


def format_preflight_failure_message(operation_name: str, diagnosis: dict) -> str:
    lines = [
        f"Unable to load {operation_name}.",
        f"Likely cause ({diagnosis.get('confidence', 'medium')} confidence): {diagnosis.get('headline')}",
    ]
    actions = diagnosis.get("actions") or []
    if actions:
        lines.append("What to do next:")
        for i, action in enumerate(actions[:4], 1):
            lines.append(f"{i}. {action}")
    return "\n".join(lines)


def get_param_degradation_strategy(param_key: str, current_value: str) -> list:
    """
    Get degradation sequence for a parameter when error occurs.

    Returns list of fallback values to try, from high-quality to low-quality.
    Empty list means no degradation available.
    """
    # Resolution degradation (1080p → 720p → 480p) for video
    if param_key.lower() == "resolution":
        res_map = {
            "1080p": ["720p", "480p"],
            "720p": ["480p"],
            "480p": []
        }
        return res_map.get(current_value.lower(), [])

    # Duration degradation (10s → 5s) for video
    if param_key.lower() == "duration":
        dur_map = {
            "10s": ["5s"],
            "5s": []
        }
        return dur_map.get(current_value.lower(), [])

    # Mode degradation for video models
    if param_key.lower() == "mode":
        mode_map = {
            "professional": ["standard"],
            "standard": []
        }
        return mode_map.get(current_value.lower(), [])

    # Quality degradation
    if param_key.lower() == "quality":
        quality_map = {
            "高清": ["标清"],
            "high": ["standard", "low"],
            "standard": ["low"],
            "low": []
        }
        return quality_map.get(current_value.lower(), [])

    return []
