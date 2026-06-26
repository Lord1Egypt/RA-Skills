"""
Tool Definitions for Memory Mode.

Three tools exposed to ClawHub:
  - recall_memory: retrieve relevant memory
  - write_memory: store structured memory event
  - check_task_memory: check if a task has already been executed
"""

import logging
from typing import Optional

import requests

from openmemo_clawhub_skill.config import (
    SkillConfig,
    MEMORY_RECALL_PATH,
    MEMORY_WRITE_PATH,
    MEMORY_SEARCH_PATH,
)

logger = logging.getLogger("openmemo_clawhub_skill")


def _post(endpoint: str, path: str, payload: dict,
          timeout: int = 10) -> dict:
    try:
        resp = requests.post(f"{endpoint}{path}", json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        return {"error": "OpenMemo adapter not reachable", "endpoint": endpoint}
    except requests.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code}", "detail": str(e)}
    except Exception as e:
        return {"error": str(e)}


def recall_memory(query: str, scene: str = "",
                  config: SkillConfig = None) -> dict:
    """Retrieve relevant memory from OpenMemo."""
    cfg = config or SkillConfig()
    payload = {"query": query, "limit": 5}
    if scene:
        payload["scene"] = scene
    return _post(cfg.endpoint, MEMORY_RECALL_PATH, payload, cfg.request_timeout)


def write_memory(content: str, scene: str = "", memory_type: str = "fact",
                 config: SkillConfig = None) -> dict:
    """Store structured memory event in OpenMemo."""
    cfg = config or SkillConfig()
    payload = {
        "content": content,
        "scene": scene,
        "type": memory_type,
        "confidence": 0.8,
    }
    return _post(cfg.endpoint, MEMORY_WRITE_PATH, payload, cfg.request_timeout)


def check_task_memory(task_description: str,
                      config: SkillConfig = None) -> dict:
    """Check if a task has already been executed."""
    cfg = config or SkillConfig()
    payload = {
        "query": task_description,
        "limit": 5,
    }
    result = _post(cfg.endpoint, MEMORY_SEARCH_PATH, payload, cfg.request_timeout)

    if "error" in result:
        return result

    results = result.get("results", [])
    if not results:
        return {
            "matched": False,
            "recommended_action": "proceed",
            "message": "No previous execution found for this task.",
        }

    top = results[0]
    score = top.get("score", 0)
    if score > 0.8:
        return {
            "matched": True,
            "recommended_action": "reuse_or_skip",
            "previous_content": top.get("content", ""),
            "confidence": score,
            "message": "Similar task found with high confidence. Consider reusing.",
        }
    elif score > 0.5:
        return {
            "matched": True,
            "recommended_action": "adapt",
            "previous_content": top.get("content", ""),
            "confidence": score,
            "message": "Related task found. Consider adapting previous approach.",
        }
    else:
        return {
            "matched": False,
            "recommended_action": "proceed",
            "message": "No closely matching task found.",
        }


TOOL_DEFINITIONS = [
    {
        "name": "recall_memory",
        "description": "Retrieve relevant memory from OpenMemo. Use this to recall past experience, decisions, and knowledge before executing tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for memory recall",
                },
                "scene": {
                    "type": "string",
                    "description": "Optional scene context (e.g., coding, debug, research)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "write_memory",
        "description": "Store structured memory event in OpenMemo. Use this after completing important tasks to save experience for future use.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The memory content to store",
                },
                "scene": {
                    "type": "string",
                    "description": "Scene context (e.g., coding, debug, research)",
                },
                "type": {
                    "type": "string",
                    "description": "Memory type: fact, decision, observation, preference",
                    "enum": ["fact", "decision", "observation", "preference"],
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "check_task_memory",
        "description": "Check if a task has already been executed. Use this FIRST before starting any task to avoid duplication.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_description": {
                    "type": "string",
                    "description": "Description of the task to check",
                },
            },
            "required": ["task_description"],
        },
    },
]
