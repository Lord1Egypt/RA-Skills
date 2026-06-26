#!/usr/bin/env python3
"""Render semantic snapshot from the rule snapshot plus semantic sections."""

from __future__ import annotations

import json
import re
from typing import Dict, List

import memory_consolidate as mc


TARGET_SECTIONS = {
    "## Top Facts": "top_facts",
    "## Active Issues": "active_issues",
    "## Chosen Solutions": "chosen_solutions",
    "## Working Patterns": "working_patterns",
    "## Recent": "recent",
}

SECTION_LABELS = {
    "top_facts": "Top Facts",
    "active_issues": "Active Issues",
    "chosen_solutions": "Chosen Solutions",
    "working_patterns": "Working Patterns",
    "recent": "Recent",
}


def render_bullets(items: List[Dict[str, str]]) -> str:
    lines = []
    for item in items:
        text = mc.normalize_content(str(item.get("text") or ""))
        if not text:
            continue
        lines.append(f"- {text}")
    return "\n".join(lines) if lines else "-"


def replace_section(text: str, heading: str, bullets: str) -> str:
    pattern = rf"({re.escape(heading)}\n)(.*?)(?=\n## |\Z)"
    return re.sub(pattern, rf"\1{bullets}\n", text, flags=re.S)


def main() -> int:
    base_snapshot_path = mc.SNAPSHOT_RULE_PATH if mc.SNAPSHOT_RULE_PATH.exists() else mc.SNAPSHOT_PATH
    if not base_snapshot_path.exists():
        raise FileNotFoundError(base_snapshot_path)
    if not mc.SEMANTIC_LATEST_PATH.exists():
        raise FileNotFoundError(mc.SEMANTIC_LATEST_PATH)

    base_text = base_snapshot_path.read_text("utf-8")
    semantic = json.loads(mc.SEMANTIC_LATEST_PATH.read_text("utf-8"))
    sections = semantic.get("sections") or {}
    active_section_keys = [key for key in semantic.get("active_sections") or [] if key in SECTION_LABELS]
    active_section_labels = [SECTION_LABELS[key] for key in active_section_keys]
    section_note = " / ".join(active_section_labels) if active_section_labels else "none"

    rendered = base_text
    note = (
        "This is the injected working-memory snapshot. Keep it short and high-signal.\n\n"
        f"> V2-lite semantic sections active: {section_note}. Other sections remain rule-based.\n\n"
    )
    rendered = re.sub(
        r"This is the injected working-memory snapshot\. Keep it short and high-signal\.\n\n(?:> V2-lite semantic sections active: .*?\n\n)?",
        note,
        rendered,
        count=1,
        flags=re.S,
    )

    for heading, key in TARGET_SECTIONS.items():
        items = list(sections.get(key) or [])
        if not items:
            continue
        rendered = replace_section(rendered, heading, render_bullets(items))

    mc.SNAPSHOT_SEMANTIC_PATH.write_text(rendered, "utf-8")
    print(str(mc.SNAPSHOT_SEMANTIC_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
