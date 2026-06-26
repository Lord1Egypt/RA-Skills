from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


TEMPLATE_MAP = {
    'word_work_report_v1': 'templates/docx/word_work_report_v1.json',
    'meeting_minutes_v1': 'templates/docx/meeting_minutes_v1.json',
    'excel_data_tracker_v1': 'templates/xlsx/excel_data_tracker_v1.json',
    'project_plan_v1': 'templates/xlsx/project_plan_v1.json',
    'ppt_business_brief_v1': 'templates/pptx/ppt_business_brief_v1.json',
    'project_status_brief_v1': 'templates/pptx/project_status_brief_v1.json',
}


def load_template(template_id: str) -> Dict[str, Any]:
    if template_id not in TEMPLATE_MAP:
        raise ValueError(f'Unknown templateId: {template_id}')
    path = Path(__file__).resolve().parent / TEMPLATE_MAP[template_id]
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
