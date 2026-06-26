"""
IMA Reflection Module
Version: 1.0.0

Handles automatic error reflection and retry logic:
- Error analysis and classification
- Parameter degradation strategies
- Automatic retry with adjusted parameters
"""

import re
import time
import json

import requests

from ima_constants import (
    ALLOWED_MODEL_IDS,
    normalize_model_id,
    MAX_POLL_WAIT_SECONDS,
    VIDEO_RECORDS_URL,
    to_user_facing_model_name,
)
from ima_logger import get_logger
from ima_api_client import create_task

logger = get_logger()


# ─── Error Analysis ───────────────────────────────────────────────────────────

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

    bare_code_match = re.search(r'\b(6009|6010|4008|401)\b', error_str)
    if bare_code_match:
        code = int(bare_code_match.group(1))
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


# ─── Parameter Degradation Strategies ────────────────────────────────────────

def get_param_degradation_strategy(param_key: str, current_value: str) -> list:
    """
    Get degradation sequence for a parameter when error occurs.
    
    Returns list of fallback values to try, from high-quality to low-quality.
    Empty list means no degradation available.
    """
    if param_key.lower() == "resolution":
        res_map = {
            "1080p": ["720p", "480p"],
            "720p": ["480p"],
            "480p": []
        }
        return res_map.get(current_value.lower(), [])
    
    if param_key.lower() == "duration":
        dur_map = {
            "15s": ["10s", "5s"],
            "15": ["10", "5"],
            "10s": ["5s"],
            "10": ["5"],
            "5s": [],
            "5": []
        }
        return dur_map.get(str(current_value).lower(), [])
    
    if param_key.lower() == "mode":
        mode_map = {
            "professional": ["standard"],
            "standard": []
        }
        return mode_map.get(current_value.lower(), [])
    
    if param_key.lower() == "quality":
        quality_map = {
            "high": ["standard", "low"],
            "standard": ["low"],
            "low": []
        }
        return quality_map.get(current_value.lower(), [])
    
    return []


def reflect_on_failure(error_info: dict, 
                      attempt: int,
                      current_params: dict,
                      credit_rules: list,
                      model_params: dict) -> dict:
    """
    Analyze failure and determine corrective action.
    
    Args:
        error_info: Output from extract_error_info()
        attempt: Current attempt number (1, 2, or 3)
        current_params: Parameters used in failed attempt
        credit_rules: All available credit_rules for this model
        model_params: Model metadata (name, id, form_params, etc.)
    
    Returns:
        {
            "action": "retry" | "give_up",
            "new_params": dict (if action=="retry"),
            "reason": str (explanation of what changed),
            "suggestion": str (user-facing suggestion if give_up)
        }
    """
    code = error_info.get("code")
    error_type = error_info.get("type", "")
    
    # Strategy 1: 500 Internal Server Error → Degrade parameters
    if code == 500 or "http_500" in error_type:
        # Try to degrade a parameter
        for key in ["resolution", "duration", "mode", "quality"]:
            if key in current_params:
                current_val = current_params[key]
                fallbacks = get_param_degradation_strategy(key, current_val)
                
                if fallbacks:
                    new_val = fallbacks[0]
                    new_params = current_params.copy()
                    new_params[key] = new_val
                    
                    return {
                        "action": "retry",
                        "new_params": new_params,
                        "reason": f"500 error with {key}='{current_val}', degrading to '{new_val}'"
                    }
        
        return {
            "action": "give_up",
            "suggestion": f"Model '{model_params['model_name']}' returned 500 Internal Server Error. "
                         f"Try a different model or contact IMA support."
        }
    
    # Strategy 2: 6009 (No matching rule) → Extract required params from first rule
    if code == 6009:
        if credit_rules and len(credit_rules) > 0:
            min_rule = min(credit_rules, key=lambda r: r.get("points", 9999))
            rule_attrs = min_rule.get("attributes", {})
            
            if rule_attrs:
                new_params = current_params.copy()
                added = []
                
                for key, val in rule_attrs.items():
                    if key not in new_params:
                        new_params[key] = val
                        added.append(f"{key}={val}")
                
                if added:
                    return {
                        "action": "retry",
                        "new_params": new_params,
                        "reason": f"6009 error: added missing parameters {', '.join(added)} from credit_rules"
                    }
        
        return {
            "action": "give_up",
            "suggestion": f"No matching credit rule found for parameters: {current_params}. "
                         f"Model '{model_params['model_name']}' may not support this parameter combination."
        }
    
    # Strategy 3: 6010 (attribute_id mismatch) → Reselect credit_rule
    if code == 6010:
        if credit_rules:
            from ima_param_resolver import select_credit_rule_by_params
            selected = select_credit_rule_by_params(credit_rules, current_params)
            
            if selected:
                new_attr_id = selected.get("attribute_id")
                new_points = selected.get("points")
                rule_attrs = selected.get("attributes", {})
                
                new_params = current_params.copy()
                new_params.update(rule_attrs)
                
                return {
                    "action": "retry",
                    "new_params": new_params,
                    "reason": f"6010 error: reselected credit_rule (attribute_id={new_attr_id}, {new_points} pts)",
                    "new_attribute_id": new_attr_id,
                    "new_credit": new_points
                }
        
        return {
            "action": "give_up",
            "suggestion": f"Parameter mismatch (error 6010) for model '{model_params['model_name']}'. "
                         f"Could not find compatible credit_rule."
        }
    
    # Strategy 4: Timeout → Can't retry
    if code == "timeout":
        return {
            "action": "give_up",
            "suggestion": f"Task generation timed out for model '{model_params['model_name']}'. "
                         f"Please check your creation record at {VIDEO_RECORDS_URL}."
        }
    
    # Default: Unknown error
    return {
        "action": "give_up",
        "suggestion": f"Unexpected error (code={code}): {error_info.get('message')}"
    }


def create_task_with_reflection(base_url: str, api_key: str,
                                task_type: str, model_params: dict,
                                prompt: str,
                                input_urls: list[str] | None = None,
                                extra_params: dict | None = None,
                                src_image: list[dict] | None = None,
                                src_video: list[dict] | None = None,
                                src_audio: list[dict] | None = None,
                                max_attempts: int = 3) -> str:
    """
    Create task with automatic error reflection and retry.
    
    Attempts up to max_attempts times, using reflection to adjust parameters
    between attempts based on error codes (500, 6009, 6010, timeout).
    
    Returns task_id on success, raises exception after max_attempts.
    """
    current_params = extra_params.copy() if extra_params else {}
    attempt_log = []
    
    credit_rules = model_params.get("all_credit_rules", [])
    
    for attempt in range(1, max_attempts + 1):
        try:
            
            if attempt > 1 and "last_reflection" in locals():
                reflection = locals()["last_reflection"]
                if "new_attribute_id" in reflection:
                    model_params["attribute_id"] = reflection["new_attribute_id"]
                    model_params["credit"] = reflection["new_credit"]
            
            task_id = create_task(
                base_url=base_url,
                api_key=api_key,
                task_type=task_type,
                model_params=model_params,
                prompt=prompt,
                input_urls=input_urls,
                extra_params=current_params,
                src_image=src_image,
                src_video=src_video,
                src_audio=src_audio,
            )
            
            # Success
            attempt_log.append({
                "attempt": attempt,
                "result": "success",
                "params": current_params.copy()
            })
            
            return task_id
            
        except Exception as e:
            error_info = extract_error_info(e)
            
            attempt_log.append({
                "attempt": attempt,
                "result": "failed",
                "params": current_params.copy(),
                "error": error_info
            })
            
            logger.error(f"❌ Attempt {attempt} failed: {error_info['type']} - {error_info['message']}")
            
            if attempt < max_attempts:
                reflection = reflect_on_failure(
                    error_info=error_info,
                    attempt=attempt,
                    current_params=current_params,
                    credit_rules=credit_rules,
                    model_params=model_params
                )
                
                last_reflection = reflection
                
                if reflection["action"] == "retry":
                    current_params = reflection["new_params"]
                    continue
                else:
                    logger.error(f"💡 Giving up: {reflection.get('suggestion')}")
                    raise RuntimeError(reflection.get('suggestion')) from e
            else:
                logger.error(f"❌ All {max_attempts} attempts failed")
                raise
