'''
模块说明：输出后处理层
负责：
统一 confidence band / risk level
保证 trend 结构存在
把分类器输出和规范化 payload 融合
去重 identity_markers 等字段
'''

from __future__ import annotations

from typing import Any, Dict, List

from config import HIGH_CONFIDENCE_THRESHOLD, LOW_CONFIDENCE_THRESHOLD


ALLOWED_NEXT_STEPS = {
    "collect_more_context",
    "review_by_human",
    "safe_to_continue",
    "monitor_future_sessions",
}


def _safe_text(value: Any, default: str = "") -> str:
    text = str(value or "").strip()
    return text or default


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _confidence_band(confidence: float) -> str:
    if confidence < LOW_CONFIDENCE_THRESHOLD:
        return "low"
    if confidence < HIGH_CONFIDENCE_THRESHOLD:
        return "medium"
    return "high"


def _risk_level(is_minor: bool, confidence: float) -> str:
    if is_minor and confidence >= HIGH_CONFIDENCE_THRESHOLD:
        return "High"
    if is_minor or confidence >= LOW_CONFIDENCE_THRESHOLD:
        return "Medium"
    return "Low"


def _unique(items: List[Any]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in items:
        text = _safe_text(item)
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return ordered


def _ensure_trajectory(output: Dict[str, Any], normalized_payload: Dict[str, Any]) -> Dict[str, Any]:
    trend = output.setdefault("trend", {})
    trajectory = trend.get("trajectory")
    if isinstance(trajectory, list) and trajectory:
        return output
    if normalized_payload["mode"] != "multi_session":
        trend["trajectory"] = []
        trend["trend_summary"] = _safe_text(trend.get("trend_summary"))
        return output

    confidence = float(output.get("decision", {}).get("minor_confidence", 0.5) or 0.5)
    trend["trajectory"] = [
        {
            "session_id": _safe_text(session.get("session_id")) or f"session_{index + 1}",
            "session_time": _safe_text(session.get("session_time")) or None,
            "minor_confidence": confidence,
        }
        for index, session in enumerate(normalized_payload.get("sessions", []))
    ]
    trend["trend_summary"] = _safe_text(trend.get("trend_summary"))
    return output


def merge_output(output: Dict[str, Any], normalized_payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = output.setdefault("decision", {})
    confidence = float(decision.get("minor_confidence", 0.5) or 0.5)
    is_minor = bool(decision.get("is_minor", confidence >= HIGH_CONFIDENCE_THRESHOLD))
    decision["is_minor"] = is_minor
    decision["minor_confidence"] = round(max(0.0, min(1.0, confidence)), 4)
    decision["confidence_band"] = _confidence_band(decision["minor_confidence"])
    decision["risk_level"] = _safe_text(decision.get("risk_level")) or _risk_level(is_minor, decision["minor_confidence"])

    profile = output.setdefault("user_profile", {})
    prior_profile = normalized_payload.get("context", {}).get("prior_profile", {})
    profile["age_range"] = _safe_text(profile.get("age_range")) or _safe_text(prior_profile.get("age_range"), "未明确")
    profile["education_stage"] = _safe_text(profile.get("education_stage")) or _safe_text(prior_profile.get("education_stage"), "未明确")
    profile["identity_markers"] = _unique(
        _safe_list(profile.get("identity_markers"))
        + _safe_list(prior_profile.get("identity_markers"))
        + normalized_payload.get("identity_hints", [])
    )

    evidence = output.setdefault("evidence", {})
    for key in ("direct_evidence", "historical_evidence", "retrieval_evidence", "time_evidence", "conflicting_signals"):
        evidence[key] = _unique(_safe_list(evidence.get(key)))

    icbo = output.setdefault("icbo_features", {})
    for key in ("intention", "cognition", "behavior_style"):
        icbo[key] = _safe_text(icbo.get(key), "未明确")
    icbo["opportunity_time"] = _safe_text(icbo.get("opportunity_time")) or _safe_text(
        normalized_payload.get("context", {}).get("raw_time_hint")
        or normalized_payload.get("context", {}).get("opportunity_time"),
        "未明确",
    )

    output["reasoning_summary"] = _safe_text(output.get("reasoning_summary"), "未提供推理摘要")
    output["uncertainty_notes"] = _unique(_safe_list(output.get("uncertainty_notes")))
    next_step = _safe_text(output.get("recommended_next_step"))
    if next_step not in ALLOWED_NEXT_STEPS:
        if evidence["conflicting_signals"]:
            next_step = "review_by_human"
        elif output["uncertainty_notes"]:
            next_step = "collect_more_context"
        elif is_minor:
            next_step = "monitor_future_sessions"
        else:
            next_step = "safe_to_continue"
    output["recommended_next_step"] = next_step
    return _ensure_trajectory(output, normalized_payload)
