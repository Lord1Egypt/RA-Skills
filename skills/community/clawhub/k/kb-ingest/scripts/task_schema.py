from __future__ import annotations


def validate_task(task: dict) -> list[dict]:
    errors = []
    if task.get("protocol") != "research_kb_agent_task":
        errors.append({"code": "INVALID_PROTOCOL", "message": "protocol must be research_kb_agent_task"})
    if task.get("taskType") != "kb_ingest":
        errors.append({"code": "INVALID_TASK_TYPE", "message": "taskType must be kb_ingest"})
    targets = task.get("kbTargets") or []
    if len(targets) != 1:
        errors.append({"code": "MISSING_KB_TARGET", "message": "exactly one kbTarget is required"})
    files = (task.get("payload") or {}).get("files") or []
    if not files:
        errors.append({"code": "MISSING_FILES", "message": "payload.files is required"})
    return errors
