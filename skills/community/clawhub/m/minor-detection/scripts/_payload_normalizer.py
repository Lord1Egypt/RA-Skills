'''
模块说明：输入预处理层
负责：
判断是 single_session 还是多 session 模式
把 conversation/sessions/context 整理成统一结构
展平对话
提取原始时间线索
从历史 profile 和对话里抽身份 hints
生成规范化 payload
'''


from __future__ import annotations

import json
import re
from typing import Any, Dict, List


TIMESTAMP_PATTERN = re.compile(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}[^\n]{0,24}\d{1,2}:\d{2}(?::\d{2})?)")


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def infer_mode(raw_payload: Dict[str, Any], context: Dict[str, Any]) -> str:
    mode = _safe_text(raw_payload.get("mode")).lower()
    if mode in {"single_session", "multi_session", "enriched"}:
        return mode
    if _safe_list(raw_payload.get("sessions")):
        return "multi_session"
    if any(context.get(key) for key in ("time_features", "retrieved_cases", "prior_profile", "raw_time_hint", "opportunity_time")):
        return "enriched"
    return "single_session"


def flatten_conversation(mode: str, conversation: List[Dict[str, Any]], sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if mode != "multi_session":
        return [item for item in conversation if isinstance(item, dict)]
    flattened: List[Dict[str, Any]] = []
    for session in sessions:
        for turn in _safe_list(_safe_dict(session).get("conversation")):
            if isinstance(turn, dict):
                flattened.append(turn)
    return flattened


def conversation_text(conversation: List[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for turn in conversation:
        if not isinstance(turn, dict):
            continue
        role = _safe_text(turn.get("role")) or "user"
        content = _safe_text(turn.get("content"))
        if content:
            parts.append(f"[{role}] {content}")
    return "\n".join(parts)


def extract_timestamp_candidate(conversation: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
    for key in ("raw_time_hint", "opportunity_time"):
        value = _safe_text(context.get(key))
        if value:
            return value
    for turn in conversation:
        if not isinstance(turn, dict):
            continue
        for key in ("timestamp", "time", "created_at", "datetime"):
            value = _safe_text(turn.get(key))
            if value:
                return value
        content = _safe_text(turn.get("content"))
        match = TIMESTAMP_PATTERN.search(content)
        if match:
            return match.group(1).strip()
    return ""


def build_identity_hints(conversation: List[Dict[str, Any]], prior_profile: Dict[str, Any]) -> List[str]:
    hints: List[str] = []
    text = conversation_text(conversation)
    patterns = (
        "初中",
        "初一",
        "初二",
        "初三",
        "高中",
        "高一",
        "高二",
        "高三",
        "大学",
        "本科",
        "实习",
        "上班",
        "老师",
        "家长",
    )
    for token in patterns:
        if token in text and token not in hints:
            hints.append(token)
    for marker in _safe_list(prior_profile.get("identity_markers")):
        marker_text = _safe_text(marker)
        if marker_text and marker_text not in hints:
            hints.append(marker_text)
    return hints


def normalize_payload(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    context = _safe_dict(raw_payload.get("context"))
    meta = _safe_dict(raw_payload.get("meta"))
    mode = infer_mode(raw_payload, context)
    sessions = [_safe_dict(item) for item in _safe_list(raw_payload.get("sessions"))]
    conversation = [_safe_dict(item) for item in _safe_list(raw_payload.get("conversation"))]
    flattened_conversation = flatten_conversation(mode, conversation, sessions)

    request_id = _safe_text(raw_payload.get("request_id")) or _safe_text(meta.get("request_id"))
    sample_id = _safe_text(raw_payload.get("sample_id")) or request_id or _safe_text(meta.get("sample_id"))
    user_id = _safe_text(raw_payload.get("user_id")) or _safe_text(meta.get("user_id"))

    normalized_context = {
        "raw_time_hint": _safe_text(context.get("raw_time_hint")),
        "opportunity_time": _safe_text(context.get("opportunity_time")),
        "time_features": _safe_dict(context.get("time_features")),
        "prior_profile": _safe_dict(context.get("prior_profile")),
        "retrieved_cases": _safe_list(context.get("retrieved_cases")),
        "channel": _safe_text(context.get("channel")),
        "locale": _safe_text(context.get("locale")),
    }
    return {
        "mode": mode,
        "conversation": flattened_conversation,
        "conversation_text": conversation_text(flattened_conversation),
        "sessions": sessions,
        "context": normalized_context,
        "meta": {
            "request_id": request_id or sample_id,
            "sample_id": sample_id or request_id,
            "user_id": user_id,
            "source": _safe_text(raw_payload.get("source")) or _safe_text(meta.get("source")),
        },
        "raw_payload_json": json.dumps(raw_payload, ensure_ascii=False, indent=2),
        "identity_hints": build_identity_hints(flattened_conversation, normalized_context["prior_profile"]),
        "timestamp_candidate": extract_timestamp_candidate(flattened_conversation, normalized_context),
    }
