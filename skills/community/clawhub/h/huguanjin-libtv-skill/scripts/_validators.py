"""Shared input validators for CLI scripts."""

import json
import mimetypes
import os

from _logger import error_exit

TRUE_VALUES = {"1", "true", "yes", "y", "on"}
FALSE_VALUES = {"0", "false", "no", "n", "off"}


def parse_positive_int(raw_value: str, field_name: str):
    if raw_value in (None, ""):
        return None
    try:
        value = int(raw_value)
    except ValueError:
        error_exit(f"{field_name} 必须是整数")
    if value <= 0:
        error_exit(f"{field_name} 必须大于 0")
    return value


def parse_optional_bool(raw_value: str, field_name: str):
    if raw_value in (None, ""):
        return None
    text = str(raw_value).strip().lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    error_exit(f"{field_name} 仅支持 true/false、1/0、yes/no")


def parse_json_array(raw_value: str, field_name: str):
    if raw_value in (None, ""):
        return None
    try:
        value = json.loads(raw_value)
    except json.JSONDecodeError:
        error_exit(f"{field_name} 必须是合法 JSON")
    if not isinstance(value, list):
        error_exit(f"{field_name} 必须是 JSON 数组")
    return value


def check_reference_image(file_path: str) -> str:
    if not os.path.isfile(file_path):
        error_exit(f"参考图不存在: {file_path}")

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and not mime_type.startswith("image/"):
        error_exit(f"参考图仅支持 image/*，当前文件类型为 {mime_type}: {file_path}")

    return mime_type or "application/octet-stream"
