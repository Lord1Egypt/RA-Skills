from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path).expanduser().resolve()
    return json.loads(path.read_text(encoding="utf-8"))


def get_active_base(config: dict[str, Any]) -> dict[str, Any]:
    return config["feishu"]["active_base"]


def get_table(config: dict[str, Any], key: str) -> dict[str, Any]:
    return config["feishu"]["tables"][key]


def get_table_id(config: dict[str, Any], key: str) -> str | None:
    table = get_table(config, key)
    return table.get("table_id") or None


def get_threshold(config: dict[str, Any], *keys: str):
    value: Any = config
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def get_schema_field_names(config: dict[str, Any], table_key: str) -> list[str]:
    schema = config.get("schemas", {}).get(table_key, {})
    fields = schema.get("fields", []) or []
    names: list[str] = []
    for field in fields:
        if isinstance(field, dict):
            name = field.get("name")
            if isinstance(name, str) and name.strip():
                names.append(name.strip())
    return names


def get_field_aliases(config: dict[str, Any], table_key: str) -> dict[str, list[str]]:
    raw = config.get("field_aliases", {}).get(table_key, {})
    aliases: dict[str, list[str]] = {}
    if not isinstance(raw, dict):
        return aliases
    for logical_key, value in raw.items():
        if isinstance(value, str):
            values = [value]
        elif isinstance(value, list):
            values = [item for item in value if isinstance(item, str) and item.strip()]
        else:
            continue
        cleaned = [item.strip() for item in values if item.strip()]
        if cleaned:
            aliases[str(logical_key)] = cleaned
    return aliases
