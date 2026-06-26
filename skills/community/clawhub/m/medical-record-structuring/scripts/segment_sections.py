"""Split a Chinese clinical record into canonical sections."""
from __future__ import annotations
import re
from typing import Dict, List

# Patterns ordered by typical EMR layout. Each value is the canonical key.
SECTION_PATTERNS = [
    (r"^主\s*诉[:：]?", "chief_complaint"),
    (r"^现\s*病\s*史[:：]?", "history_present_illness"),
    (r"^既\s*往\s*史[:：]?", "past_history"),
    (r"^个\s*人\s*史[:：]?", "personal_history"),
    (r"^家\s*族\s*史[:：]?", "family_history"),
    (r"^体\s*格\s*检\s*查[:：]?", "physical_exam"),
    (r"^辅\s*助\s*检\s*查[:：]?", "auxiliary_exam"),
    (r"^初\s*步\s*诊\s*断[:：]?", "diagnosis"),
    (r"^出\s*院\s*诊\s*断[:：]?", "diagnosis"),
    (r"^诊\s*疗\s*经\s*过[:：]?", "treatment_course"),
    (r"^出\s*院\s*医\s*嘱[:：]?", "discharge_instructions"),
]


def segment_sections(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    sections: Dict[str, List[str]] = {}
    current = "preamble"
    sections[current] = []
    for line in lines:
        matched = False
        for pat, key in SECTION_PATTERNS:
            if re.match(pat, line.strip()):
                current = key
                sections.setdefault(current, [])
                # also keep the section header line minus the marker
                header_text = re.sub(pat, "", line.strip()).strip()
                if header_text:
                    sections[current].append(header_text)
                matched = True
                break
        if not matched:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items() if "".join(v).strip()}
