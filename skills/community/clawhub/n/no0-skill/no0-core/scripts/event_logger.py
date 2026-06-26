import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional

WRITE_LOCK = Lock()

CHANGE_LOG_JSON_FIELDS = [
    "record_time",
    "event_id",
    "file_name",
    "event_payload",
    "level",
    "reason",
    "labeled_record_time",
]


def _stringify_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _level_text(level: Optional[Any]) -> str:
    if level is None:
        return "null"
    return str(level)


def _safe_get_nested(payload: Dict[str, Any], field_name: str) -> Any:
    parts = field_name.split(".")
    current: Any = payload
    for part in parts:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _stringify_json_pretty(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def _format_markdown_code_block(content: str, language: str = "bash") -> List[str]:
    text = content if isinstance(content, str) else _stringify_value(content)
    longest_backtick_run = 0
    current_backtick_run = 0
    for char in text:
        if char == "`":
            current_backtick_run += 1
            if current_backtick_run > longest_backtick_run:
                longest_backtick_run = current_backtick_run
        else:
            current_backtick_run = 0

    fence = "`" * max(3, longest_backtick_run + 1)
    return [f"{fence}{language}", text, fence]


def _build_json_record(
    record_time: str,
    event_id: str,
    file_name: str,
    event_payload: Dict[str, Any],
    level: Optional[Any],
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "record_time": record_time,
        "event_id": event_id,
        "file_name": file_name,
        "event_payload": event_payload,
        "level": level,
        "reason": _stringify_value(reason),
        "labeled_record_time": "",
    }


def _build_markdown_block(
    record_time: str,
    file_name: str,
    event_payload: Dict[str, Any],
    level: Optional[Any],
    reason: Optional[str] = None,
    record_type: str = "detected",
) -> str:
    payload_file_name = _stringify_value(event_payload.get("file_name")) or file_name
    event_id = _stringify_value(event_payload.get("event_id"))
    timestamp = _stringify_value(event_payload.get("timestamp"))
    source = _stringify_value(event_payload.get("source"))
    monitor_version = _stringify_value(event_payload.get("monitor_version"))
    trigger_type = _stringify_value(event_payload.get("trigger_type"))
    check_time = _stringify_value(event_payload.get("check_time"))
    file_path = _stringify_value(event_payload.get("file_path"))
    old_hash = _stringify_value(event_payload.get("old_hash"))
    new_hash = _stringify_value(event_payload.get("new_hash"))
    before_content = _stringify_value(event_payload.get("before_content"))
    after_content = _stringify_value(event_payload.get("after_content"))
    content_truncated_before = _stringify_value(_safe_get_nested(event_payload, "content_truncated.before"))
    content_truncated_after = _stringify_value(_safe_get_nested(event_payload, "content_truncated.after"))
    max_chars = _stringify_value(_safe_get_nested(event_payload, "content_truncated.max_chars"))
    diff = _stringify_json_pretty(event_payload.get("diff"))

    lines = [
        f"## {record_time} - {payload_file_name} [Level {_level_text(level)}] ({record_type})",
        f"- 时间id（event_id）: {event_id}",
        f"- 记录类型（record_type）: {record_type}",
        f"- 分级原因（reason）: {_stringify_value(reason)}",
        f"- 事件发生时间，ISO 8601 格式（timestamp）: {timestamp}",
        f"- 事件来源（source）: {source}",
        f"- 监控版本（monitor_version）: {monitor_version}",
        f"- 触发类型（trigger_type）: {trigger_type}",
        f"- 检查时间（check_time）: {check_time}",
        f"- 文件名（file_name）: {payload_file_name}",
        f"- 文件路径（file_path）: {file_path}",
        f"- 旧哈希值（old_hash）: {old_hash}",
        f"- 新哈希值（new_hash）: {new_hash}",
        "- 修改前内容（before_content）:",
        *_format_markdown_code_block(before_content, language="bash"),
        f"- 修改前内容是否被截断（content_truncated_before）: {content_truncated_before}",
        f"- 修改后内容是否被截断（content_truncated_after）: {content_truncated_after}",
        f"- 内容最大截断字符数（max_chars）: {max_chars}",
        "- 修改后内容（after_content）:",
        *_format_markdown_code_block(after_content, language="bash"),
        "- 结构化 diff 数据（diff）:",
        *_format_markdown_code_block(diff, language="bash"),
        "",
    ]
    return "\n".join(lines)


def _append_json_record(file_path: Path, json_record: Dict[str, Any]) -> None:
    records = _load_json_records(file_path)
    sanitized = {key: json_record.get(key) for key in CHANGE_LOG_JSON_FIELDS}
    records.append(sanitized)
    file_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_json_records(file_path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    if not file_path.exists():
        return records
    raw = file_path.read_text(encoding="utf-8").strip()
    if not raw:
        return records
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return records
    if isinstance(parsed, list):
        records = [item for item in parsed if isinstance(item, dict)]
    return records


def _append_markdown_block(file_path: Path, markdown_block: str) -> None:
    has_content = file_path.exists() and file_path.stat().st_size > 0
    with open(file_path, "a", encoding="utf-8") as f:
        if has_content:
            f.write("\n")
        f.write(markdown_block)


def write_change_log(
    record_time: str,
    event_id: str,
    file_name: str,
    event_payload: Dict[str, Any],
    json_file_path: Path,
    md_file_path: Path,
    level: Optional[Any] = None,
    reason: Optional[str] = None,
    record_type: str = "detected",
) -> None:
    """Write a change event to both JSON and Markdown log files."""
    safe_payload = event_payload if isinstance(event_payload, dict) else {}

    json_record = _build_json_record(
        record_time=record_time,
        event_id=event_id,
        file_name=file_name,
        event_payload=safe_payload,
        level=level,
        reason=reason,
    )
    markdown_block = _build_markdown_block(
        record_time=record_time,
        file_name=file_name,
        event_payload=safe_payload,
        level=level,
        reason=reason,
        record_type=record_type,
    )

    json_file_path.parent.mkdir(parents=True, exist_ok=True)
    md_file_path.parent.mkdir(parents=True, exist_ok=True)

    with WRITE_LOCK:
        _append_json_record(json_file_path, json_record)
    _append_markdown_block(md_file_path, markdown_block)


def update_change_log_label(
    event_id: str,
    level: Any,
    reason: str,
    json_file_path: Path,
    md_file_path: Path,
    labeled_record_time: Optional[str] = None,
) -> bool:
    """Update an existing change log entry with a classification label."""
    record_time = labeled_record_time or datetime.now().astimezone().isoformat(timespec="seconds")
    json_file_path.parent.mkdir(parents=True, exist_ok=True)
    md_file_path.parent.mkdir(parents=True, exist_ok=True)

    with WRITE_LOCK:
        records = _load_json_records(json_file_path)
        matched_index = -1

        for idx, row in enumerate(records):
            if str(row.get("event_id", "")) == str(event_id):
                matched_index = idx
                break

        if matched_index < 0:
            return False

        matched = records[matched_index]
        matched["level"] = level
        matched["reason"] = _stringify_value(reason)
        matched["labeled_record_time"] = record_time
        records[matched_index] = matched
        json_file_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

        event_payload = matched.get("event_payload", {})
        if not isinstance(event_payload, dict):
            event_payload = {}
        matched_file_name = _stringify_value(matched.get("file_name")) or _stringify_value(event_payload.get("file_name"))

    markdown_block = _build_markdown_block(
        record_time=record_time,
        file_name=matched_file_name,
        event_payload=event_payload,
        level=level,
        reason=reason,
        record_type="labeled",
    )
    _append_markdown_block(md_file_path, markdown_block)

    return True
