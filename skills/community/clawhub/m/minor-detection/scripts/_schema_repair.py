# 模块说明：
# - 校验并修复 classifier 输出的 schema 一致性。
# - 是 skill 内部避免输出漂移的最后一道保险。

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from _classifier_client import call_chat_completion
from _profile_merge import merge_output


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def validate_output(output: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    required_paths = [
        ("decision",),
        ("decision", "is_minor"),
        ("decision", "minor_confidence"),
        ("decision", "confidence_band"),
        ("decision", "risk_level"),
        ("user_profile",),
        ("user_profile", "age_range"),
        ("user_profile", "education_stage"),
        ("user_profile", "identity_markers"),
        ("icbo_features",),
        ("icbo_features", "intention"),
        ("icbo_features", "cognition"),
        ("icbo_features", "behavior_style"),
        ("icbo_features", "opportunity_time"),
        ("evidence",),
        ("reasoning_summary",),
        ("trend",),
        ("uncertainty_notes",),
        ("recommended_next_step",),
    ]
    for path in required_paths:
        current: Any = output
        for key in path:
            if not isinstance(current, dict) or key not in current:
                missing.append(".".join(path))
                break
            current = current[key]
    return missing


def deterministic_repair(output: Dict[str, Any], normalized_payload: Dict[str, Any]) -> Dict[str, Any]:
    repaired = merge_output(_safe_dict(output), normalized_payload)
    repaired.setdefault("trend", {})
    repaired["trend"].setdefault("trajectory", [])
    repaired["trend"].setdefault("trend_summary", "")
    repaired.setdefault("uncertainty_notes", [])
    repaired.setdefault("recommended_next_step", "collect_more_context")
    return repaired


def repair_output(
    *,
    candidate: Optional[Dict[str, Any]],
    raw_response_text: str,
    normalized_payload: Dict[str, Any],
    output_schema_text: str,
    repair_template_text: str,
    classifier_base_url: str,
    classifier_api_key: str,
    classifier_model: str,
    classifier_timeout_sec: int,
    classifier_max_retries: int,
    classifier_retry_backoff_sec: float,
) -> Dict[str, Any]:
    repaired = deterministic_repair(candidate or {}, normalized_payload)
    if not validate_output(repaired):
        return repaired

    repair_prompt = (
        repair_template_text
        .replace("{{RAW_RESPONSE_TEXT}}", raw_response_text or "{}")
        .replace("{{PAYLOAD_JSON}}", json.dumps(normalized_payload, ensure_ascii=False, indent=2))
        .replace("{{OUTPUT_SCHEMA}}", output_schema_text)
    )
    repaired_from_model, _ = call_chat_completion(
        base_url=classifier_base_url,
        api_key=classifier_api_key,
        model=classifier_model,
        timeout_sec=classifier_timeout_sec,
        max_retries=classifier_max_retries,
        retry_backoff_sec=classifier_retry_backoff_sec,
        messages=[
            {"role": "system", "content": "你是 minor-detection 的 schema repair 组件，只能返回合法 JSON。"},
            {"role": "user", "content": repair_prompt},
        ],
        temperature=0.0,
    )
    final_output = deterministic_repair(repaired_from_model, normalized_payload)
    return final_output