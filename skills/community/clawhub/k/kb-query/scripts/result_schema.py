from __future__ import annotations


def result(task: dict, success: bool, payload: dict | None = None, errors: list[dict] | None = None) -> dict:
    return {
        "protocol": "research_kb_agent_result",
        "protocolVersion": "1.0",
        "taskId": task.get("taskId", ""),
        "taskType": task.get("taskType", "kb_query"),
        "success": success,
        "result": payload,
        "errors": errors or [],
    }
