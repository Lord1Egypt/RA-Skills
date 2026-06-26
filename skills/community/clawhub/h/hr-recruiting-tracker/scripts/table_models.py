#!/usr/bin/env python3
"""Load Tencent Docs SmartSheet table models for hr-recruiting-tracker."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TABLE_MODEL_PATH = SKILL_DIR / "assets" / "schemas" / "recruiting_tables.json"

FIELD_INFO_KEYS = {
    "field_id",
    "field_title",
    "field_type",
    "property_auto_number",
    "property_checkbox",
    "property_created_time",
    "property_created_user",
    "property_currency",
    "property_date_time",
    "property_email",
    "property_image",
    "property_modified_time",
    "property_modified_user",
    "property_number",
    "property_percentage",
    "property_phone_number",
    "property_progress",
    "property_reference",
    "property_select",
    "property_single_select",
    "property_text",
    "property_url",
    "property_user",
}


def load_models() -> dict[str, Any]:
    return json.loads(TABLE_MODEL_PATH.read_text(encoding="utf-8"))


def get_table(table_name: str) -> dict[str, Any]:
    models = load_models()
    try:
        return models["tables"][table_name]
    except KeyError as exc:
        raise KeyError(f"未知招聘表模型: {table_name}") from exc


def get_fixed_sheet_title(table_name: str) -> str:
    return str(get_table(table_name)["fixed_sheet_title"])


def get_field_definitions(table_name: str) -> list[dict[str, Any]]:
    fields = get_table(table_name)["fields"]
    return [
        {key: value for key, value in field.items() if key in FIELD_INFO_KEYS}
        for field in fields
    ]


def get_field_titles(table_name: str) -> list[str]:
    return [field["field_title"] for field in get_table(table_name)["fields"]]


def get_field_key_to_title(table_name: str) -> dict[str, str]:
    return {
        field["key"]: field["field_title"]
        for field in get_table(table_name)["fields"]
    }
