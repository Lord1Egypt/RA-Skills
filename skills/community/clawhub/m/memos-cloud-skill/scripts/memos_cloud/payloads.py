from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional

from .errors import ValidationError


def generate_conversation_id(user_id: str, conversation_first_message: str) -> str:
    raw = f"{user_id}\n{conversation_first_message}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def resolve_conversation_id(
    user_id: str,
    conversation_id: Optional[str] = None,
    conversation_first_message: Optional[str] = None,
) -> Optional[str]:
    if conversation_id:
        return conversation_id
    if conversation_first_message:
        return generate_conversation_id(user_id, conversation_first_message)
    return None


def parse_csv(value: Optional[str]) -> list[str]:
    if not value:
        return []
    return [item for item in (s.strip() for s in value.split(",")) if item]


def search_memory_payload(
    user_id: str,
    query: str,
    conversation_id: Optional[str] = None,
    conversation_first_message: Optional[str] = None,
    filter_obj: Optional[Dict[str, Any]] = None,
    knowledgebase_ids: Optional[str] = None,
    memory_limit_number: Optional[int] = None,
    include_preference: Optional[bool] = None,
    preference_limit_number: Optional[int] = None,
    include_tool_memory: Optional[bool] = None,
    tool_memory_limit_number: Optional[int] = None,
    include_skill: Optional[bool] = None,
    skill_limit_number: Optional[int] = None,
    relativity: Optional[float] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "user_id": user_id,
        "query": query,
    }
    cid = resolve_conversation_id(user_id, conversation_id, conversation_first_message)
    if cid:
        payload["conversation_id"] = cid
    if filter_obj is not None:
        payload["filter"] = filter_obj
    if knowledgebase_ids is not None:
        if knowledgebase_ids == "all":
            payload["knowledgebase_ids"] = ["all"]
        else:
            payload["knowledgebase_ids"] = parse_csv(knowledgebase_ids)
    if memory_limit_number is not None:
        payload["memory_limit_number"] = memory_limit_number
    if include_preference is not None:
        payload["include_preference"] = include_preference
    if preference_limit_number is not None:
        payload["preference_limit_number"] = preference_limit_number
    if include_tool_memory is not None:
        payload["include_tool_memory"] = include_tool_memory
    if tool_memory_limit_number is not None:
        payload["tool_memory_limit_number"] = tool_memory_limit_number
    if include_skill is not None:
        payload["include_skill"] = include_skill
    if skill_limit_number is not None:
        payload["skill_limit_number"] = skill_limit_number
    if relativity is not None:
        payload["relativity"] = relativity
    return payload


def add_message_payload(
    user_id: str,
    conversation_id: str,
    messages_json_str: str,
    agent_id: Optional[str] = None,
    app_id: Optional[str] = None,
    tags: Optional[str] = None,
    info_json: Optional[str] = None,
    allow_public: Optional[bool] = None,
    allow_knowledgebase_ids: Optional[str] = None,
    async_mode: Optional[bool] = None,
) -> Dict[str, Any]:
    try:
        messages = json.loads(messages_json_str)
    except json.JSONDecodeError as exc:
        raise ValidationError("messages must be a valid JSON string") from exc

    payload: Dict[str, Any] = {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "messages": messages,
    }
    if agent_id is not None:
        payload["agent_id"] = agent_id
    if app_id is not None:
        payload["app_id"] = app_id
    if tags is not None:
        payload["tags"] = parse_csv(tags)
    if info_json is not None:
        try:
            payload["info"] = json.loads(info_json)
        except json.JSONDecodeError as exc:
            raise ValidationError("info must be a valid JSON string") from exc
    if allow_public is not None:
        payload["allow_public"] = allow_public
    if allow_knowledgebase_ids is not None:
        payload["allow_knowledgebase_ids"] = parse_csv(allow_knowledgebase_ids)
    if async_mode is not None:
        payload["async_mode"] = async_mode
    return payload


def delete_memory_payload(memory_ids_str: str) -> Dict[str, Any]:
    if not memory_ids_str:
        raise ValidationError("memory_ids is required")

    return {"memory_ids": parse_csv(memory_ids_str)}


def add_feedback_payload(
    user_id: str,
    conversation_id: str,
    feedback_content: str,
    allow_knowledgebase_ids: Optional[str] = None,
    agent_id: Optional[str] = None,
    app_id: Optional[str] = None,
    feedback_time: Optional[str] = None,
    allow_public: Optional[bool] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "feedback_content": feedback_content,
    }

    knowledgebase_ids = parse_csv(allow_knowledgebase_ids)
    if knowledgebase_ids:
        payload["allow_knowledgebase_ids"] = knowledgebase_ids
    if agent_id is not None:
        payload["agent_id"] = agent_id
    if app_id is not None:
        payload["app_id"] = app_id
    if feedback_time is not None:
        payload["feedback_time"] = feedback_time
    if allow_public is not None:
        payload["allow_public"] = allow_public
    return payload


def add_kb_doc_payload(knowledgebase_id: str, file_list: list[Dict[str, str]]) -> Dict[str, Any]:
    return {
        "knowledgebase_id": knowledgebase_id,
        "file": file_list,
    }


def get_user_profile_payload(
    user_id: str,
    page: Optional[int] = None,
    size: Optional[int] = None,
    filter_obj: Optional[Dict[str, Any]] = None,
    include_preference: Optional[bool] = None,
    include_tool_memory: Optional[bool] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"user_id": user_id}
    if page is not None:
        payload["page"] = page
    if size is not None:
        payload["size"] = size
    if filter_obj is not None:
        payload["filter"] = filter_obj
    if include_preference is not None:
        payload["include_preference"] = include_preference
    if include_tool_memory is not None:
        payload["include_tool_memory"] = include_tool_memory
    return payload


def create_knowledge_base_payload(
    knowledgebase_name: str,
    knowledgebase_description: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"knowledgebase_name": knowledgebase_name}
    if knowledgebase_description is not None:
        payload["knowledgebase_description"] = knowledgebase_description
    return payload


def get_kb_documents_payload(
    file_ids: Optional[str] = None,
    knowledgebase_id: Optional[str] = None,
    doc_type: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    if file_ids:
        return {"file_ids": parse_csv(file_ids)}
    if knowledgebase_id:
        payload: Dict[str, Any] = {"knowledgebase_id": knowledgebase_id}
        if doc_type is not None:
            payload["type"] = doc_type
        if page is not None:
            payload["page"] = page
        if page_size is not None:
            payload["page_size"] = page_size
        return payload
    raise ValidationError("Either file_ids or knowledgebase_id is required.")


def delete_kb_documents_payload(file_ids: str) -> Dict[str, Any]:
    if not file_ids:
        raise ValidationError("file_ids is required")
    return {"file_ids": parse_csv(file_ids)}


def remove_knowledge_base_payload(knowledgebase_id: str) -> Dict[str, Any]:
    if not knowledgebase_id:
        raise ValidationError("knowledgebase_id is required")
    return {"knowledgebase_id": knowledgebase_id}
