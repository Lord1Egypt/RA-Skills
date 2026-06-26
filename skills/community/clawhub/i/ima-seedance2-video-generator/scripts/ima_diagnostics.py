"""
IMA Video Generation - Diagnostic Functions

This module provides error diagnosis and failure analysis for IMA API interactions.
It helps interpret API errors and suggest corrective actions.

Functions:
    - build_contextual_diagnosis: Analyze errors and build detailed diagnosis
    - format_user_failure_message: Format user-friendly failure messages
    - get_param_degradation_strategy: Get parameter degradation sequences
"""

import re
import math
from typing import Optional

# Import constants for model name formatting
try:
    from ima_constants import (
        to_user_facing_model_name,
        normalize_model_id,
        MAX_POLL_WAIT_SECONDS,
        VIDEO_RECORDS_URL
    )
except ImportError:
    # Fallback definitions if ima_constants is not available
    def to_user_facing_model_name(model_name, model_id):
        return f"{model_name} ({model_id})"
    
    def normalize_model_id(model_id):
        return str(model_id).strip().lower()
    
    MAX_POLL_WAIT_SECONDS = 2400
    VIDEO_RECORDS_URL = "https://www.imaclaw.ai/imaclaw/creation"


def _normalize_compare_value(value) -> str:
    """Normalize value for comparison (uppercase, trimmed)."""
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().upper()


def _parse_min_pixels(text: str) -> Optional[int]:
    """
    Extract minimum pixel requirement from error message.
    
    Args:
        text: Error message text
        
    Returns:
        Minimum pixel count if found, None otherwise
    """
    match = re.search(
        r"(?:at\s+least\s+(\d+)\s+pixels|pixels?\s+should\s+be\s+at\s+least\s+(\d+))",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None
    return int(match.group(1) or match.group(2))


def _parse_size_dims(value) -> Optional[tuple[int, int]]:
    """
    Parse dimensions from size string (e.g., "1920x1080").
    
    Args:
        value: Size string
        
    Returns:
        (width, height) tuple if parsed, None otherwise
    """
    if not isinstance(value, str):
        return None
    match = re.search(r"(\d{2,5})\s*[xX×]\s*(\d{2,5})", value)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _format_rule_attributes(rule: dict, task_type: str, max_items: int = 4) -> str:
    """
    Format credit rule attributes for display.
    
    Args:
        rule: Credit rule dictionary
        task_type: Task type string
        max_items: Maximum number of items to display
        
    Returns:
        Formatted attribute string
    """
    attrs = rule.get("attributes") or {}
    parts: list[str] = []
    for key, value in attrs.items():
        if task_type != "text_to_speech" and key == "default" and value == "enabled":
            continue
        parts.append(f"{key}={value}")
    if not parts:
        return "<default rule>"
    return ", ".join(parts[:max_items])


def _best_rule_mismatch(credit_rules: list, merged_params: dict, task_type: str) -> Optional[dict]:
    """
    Find the best matching credit rule and identify mismatches.
    
    Args:
        credit_rules: List of available credit rules
        merged_params: User-provided parameters
        task_type: Task type string
        
    Returns:
        Dictionary with best rule, missing params, conflicts, and score
    """
    if not credit_rules:
        return None

    best: Optional[dict] = None
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
            if task_type != "text_to_speech" and key == "default" and expected == "enabled":
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
            "matched": matched,
            "score": score,
        }
        if best is None or candidate["score"] > best["score"]:
            best = candidate

    return best


def build_contextual_diagnosis(error_info: dict,
                               task_type: str,
                               model_params: dict,
                               current_params: Optional[dict],
                               input_images: Optional[list[str]],
                               credit_rules: Optional[list] = None) -> dict:
    """
    Diagnose failure using model context + effective params + raw error.
    
    Args:
        error_info: Error information from extract_error_info()
        task_type: Task type (e.g., "text_to_video", "image_to_video")
        model_params: Model parameters including form_params, model_id, model_name
        current_params: User-provided parameters for current attempt
        input_images: List of input image URLs/paths
        credit_rules: Available credit rules for this model
        
    Returns:
        Diagnosis dictionary with:
            - code: Error code
            - confidence: "high", "medium", or "low"
            - headline: Short diagnosis summary
            - reasoning: List of diagnostic reasons
            - actions: List of suggested corrective actions
            - model_name, model_id, task_type: Context info
    """
    code = error_info.get("code")
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

    # Check for missing input media
    input_required = {
        "image_to_video",
        "first_last_frame_to_video",
        "reference_image_to_video",
    }
    if task_type in input_required and not media_inputs:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Missing required reference media for this task type"
        diagnosis["reasoning"].append(
            f"{task_type} requires input media, but input_images is empty."
        )
        diagnosis["actions"].append("Provide at least one URL/path via --input-images.")
        if task_type == "first_last_frame_to_video":
            diagnosis["actions"].append("Provide at least 2 frames: first and last.")
        return diagnosis

    # Check for insufficient frames
    if task_type == "first_last_frame_to_video" and 0 < len(media_inputs) < 2:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Insufficient frames for first_last_frame_to_video"
        diagnosis["reasoning"].append(
            f"Received {len(media_inputs)} media item(s); this mode typically needs first+last frames."
        )
        diagnosis["actions"].append("Pass two frame URLs in --input-images.")
        return diagnosis

    # Check for authentication errors
    if code == 401 or "unauthorized" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "API key is invalid or unauthorized"
        diagnosis["actions"].append("Regenerate API key: https://www.imaclaw.ai/imaclaw/apikey")
        diagnosis["actions"].append("Retry with the new key in --api-key.")
        return diagnosis

    # Check for insufficient points
    if code == 4008 or "insufficient points" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Account points are not enough for this model request"
        diagnosis["reasoning"].append(
            f"Model {model_name} ({model_id}) requires points based on selected attribute rule."
        )
        diagnosis["actions"].append("Top up credits: https://www.imaclaw.ai/imaclaw/subscription")
        diagnosis["actions"].append("Or switch to a lower-cost model/parameter profile.")
        return diagnosis

    # Check for pixel requirement errors
    min_pixels = _parse_min_pixels(raw_message)
    requested_dims = _parse_size_dims(str(merged_params.get("size") or ""))
    fallback_dims = _parse_size_dims(raw_message)
    dims = requested_dims or fallback_dims
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
            diagnosis["actions"].append("Then retry with the same model.")
            return diagnosis

    # Check for parameter attribute mismatches (6009, 6010)
    credit_rules = credit_rules or []
    rule_mismatch = _best_rule_mismatch(credit_rules, merged_params, task_type)
    if (
        code in (6009, 6010)
        or "invalid product attribute" in msg_lower
        or "no matching" in msg_lower
        or "attribute" in msg_lower
    ):
        diagnosis["headline"] = "Current parameter combination does not fit this model rule set"
        diagnosis["confidence"] = "high" if code in (6009, 6010) else "medium"
        diagnosis["reasoning"].append(
            f"Model {model_name} uses attribute-based rules; current overrides conflict with matched rule."
        )
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
                "Use a rule-compatible profile: "
                + _format_rule_attributes(rule_mismatch["rule"], task_type)
            )
        diagnosis["actions"].append("Remove custom --extra-params and retry with defaults.")
        return diagnosis

    # Check for timeout errors
    if code == "timeout" or "timed out" in msg_lower:
        diagnosis["confidence"] = "medium"
        diagnosis["headline"] = "Task exceeded polling timeout for current model settings"
        diagnosis["reasoning"].append(
            f"Current polling max is {MAX_POLL_WAIT_SECONDS}s; backend did not return a ready result in time."
        )
        if normalize_model_id(model_id) == "ima-pro":
            diagnosis["actions"].append("Switch to ima-pro-fast for quicker turnaround.")
        diagnosis["actions"].append("Retry with shorter duration or lower resolution.")
        diagnosis["actions"].append(f"Check your creation record: {VIDEO_RECORDS_URL}")
        return diagnosis

    # Check for 500 errors (backend issues)
    if code == 500 or "internal server error" in msg_lower:
        diagnosis["confidence"] = "medium"
        diagnosis["headline"] = "Backend rejected current parameter complexity"
        for key in ("resolution", "duration", "mode", "quality"):
            if key in merged_params:
                fallback = get_param_degradation_strategy(key, str(merged_params[key]))
                if fallback:
                    diagnosis["actions"].append(
                        f"Try {key}={fallback[0]} (current {merged_params[key]})."
                    )
                    break
        if normalize_model_id(model_id) == "ima-pro":
            diagnosis["actions"].append("If latency is critical, try ima-pro-fast.")
        diagnosis["actions"].append("Retry after simplifying parameters.")
        return diagnosis

    # Generic diagnosis
    diagnosis["reasoning"].append(
        f"Model context: {to_user_facing_model_name(model_name, model_id)}, task={task_type}, media_count={len(media_inputs)}."
    )
    if merged_params:
        focus_keys = ["size", "resolution", "duration", "quality", "mode"]
        hints = [f"{k}={merged_params[k]}" for k in focus_keys if k in merged_params]
        if hints:
            diagnosis["reasoning"].append("Active key parameters: " + ", ".join(hints))
    diagnosis["actions"].append("Retry with defaults (remove --extra-params).")
    diagnosis["actions"].append("Use --list-models to verify model and supported settings.")
    return diagnosis


def format_user_failure_message(diagnosis: dict,
                                attempts_used: int,
                                max_attempts: int) -> str:
    """
    Render a user-facing failure summary without exposing raw backend errors.
    
    Args:
        diagnosis: Diagnosis dictionary from build_contextual_diagnosis()
        attempts_used: Number of attempts made
        max_attempts: Maximum attempts allowed
        
    Returns:
        Formatted multi-line failure message string
    """
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
        for index, action in enumerate(actions[:4], 1):
            lines.append(f"{index}. {action}")

    code = diagnosis.get("code")
    if code not in (None, "", "unknown"):
        lines.append(f"Reference code: {code}")
    lines.append("Technical details were recorded in local logs.")
    return "\n".join(lines)


def get_param_degradation_strategy(param_key: str, current_value: str) -> list:
    """
    Get degradation sequence for a parameter when error occurs.
    
    This function provides fallback values to try when a parameter causes
    errors, typically moving from high-quality/complex to lower-quality/simpler.
    
    Args:
        param_key: Parameter name (e.g., "resolution", "duration", "quality")
        current_value: Current parameter value
        
    Returns:
        List of fallback values to try, from high-quality to low-quality.
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
