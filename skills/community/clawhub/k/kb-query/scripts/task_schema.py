from __future__ import annotations


def validate_task(task: dict) -> list[dict]:
    errors = []
    if task.get("protocol") != "research_kb_agent_task":
        errors.append({"code": "INVALID_PROTOCOL", "message": "protocol must be research_kb_agent_task"})
    if task.get("taskType") != "kb_query":
        errors.append({"code": "INVALID_TASK_TYPE", "message": "taskType must be kb_query"})
    targets = task.get("kbTargets") or []
    if len(targets) not in {1, 2}:
        errors.append({"code": "INVALID_KB_TARGETS", "message": "kbTargets must contain one or two targets"})
    if not (task.get("payload") or {}).get("question"):
        errors.append({"code": "MISSING_QUESTION", "message": "payload.question is required"})
    return errors
