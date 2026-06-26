"""Helpers for loading canonical fixture assets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FIXTURES_DIR = Path(__file__).with_name("fixtures")
DEMO_REQUEST_PATH = FIXTURES_DIR / "demo_request.json"
MOCK_EVIDENCE_PATH = FIXTURES_DIR / "mock_evidence.json"
EXPECTED_BRIEF_PATH = FIXTURES_DIR / "expected_brief.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_demo_request_payload() -> dict[str, Any]:
    return _read_json(DEMO_REQUEST_PATH)


def load_mock_evidence() -> list[dict[str, Any]]:
    return _read_json(MOCK_EVIDENCE_PATH)


def load_expected_brief() -> str:
    content = EXPECTED_BRIEF_PATH.read_text(encoding="utf-8")
    marker = "\nDelivery status:"
    marker_index = content.find(marker)
    if marker_index == -1:
        return content
    line_end_index = content.find("\n", marker_index + 1)
    if line_end_index == -1:
        return content
    return content[: line_end_index + 1]
