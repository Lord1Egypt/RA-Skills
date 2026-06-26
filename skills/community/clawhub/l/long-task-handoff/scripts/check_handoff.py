#!/usr/bin/env python3
"""Validate a long-task handoff Markdown file.

The checker is intentionally conservative and dependency-free so Codex,
OpenClaw, Hermes Agent, and other agents can run it before ending a session.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


RULES_PATH = Path(__file__).resolve().parent.parent / "references" / "secret-patterns.json"

REQUIRED_HEADINGS = [
    "Restart Instruction",
    "Current Goal",
    "Branch And Commit State",
    "Completed This Turn",
    "Delta Since Last Update",
    "Current Test Results",
    "Key Files",
    "Handoff Scope Boundary",
    "Current State",
    "Unfinished Items",
    "Next Actions",
    "Files And Artifacts",
    "Commands And Verification",
    "Fact Sources",
    "Decisions And Constraints",
    "Blockers, Risks, And Open Questions",
    "Known Risks",
    "Do Not Redo",
    "Do Not Do",
    "Sensitive Information Handling",
]

PLACEHOLDER_MARKERS = [
    "[short task name]",
    "[YYYY-MM-DD",
    "[previous handoff",
    "[yes/no",
    "[absolute path",
    "[branch name",
    "[short SHA",
    "[Concrete",
    "[What is",
    "[Specific",
    "[path]",
    "[command]",
    "[summary]",
    "[risk",
    "[Verified",
    "[Expensive",
    "[Action",
    "[Skill/tool",
]

DEFAULT_SECRET_PATTERNS = [
    r"(?i)\b(api[_-]?key|token|password|passwd|secret)\b\s*[:=]\s*['\"]?[^'\"\s`]{8,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"\bsk-[A-Za-z0-9_-]{16,}\b",
    r"(?m)^[A-Z][A-Z0-9_]{2,}=.{6,}$",
]


def load_secret_patterns() -> list[re.Pattern[str]]:
    pattern_texts = DEFAULT_SECRET_PATTERNS
    if RULES_PATH.exists():
        try:
            data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
            loaded = data if isinstance(data, list) else data.get("patterns", [])
            if loaded:
                pattern_texts = [str(item) for item in loaded]
        except Exception:
            pattern_texts = DEFAULT_SECRET_PATTERNS
    return [re.compile(pattern) for pattern in pattern_texts]


SECRET_PATTERNS = load_secret_patterns()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def extract_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[heading] = text[start:end].strip()
    return sections


def has_meaningful_content(section: str) -> bool:
    lines = [
        line.strip()
        for line in section.splitlines()
        if line.strip() and not line.strip().startswith("<!--")
    ]
    return bool(lines)


def check_required_sections(sections: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in sections:
            errors.append(f"Missing required section: ## {heading}")
        elif not has_meaningful_content(sections[heading]):
            errors.append(f"Required section is empty: ## {heading}")
    return errors


def check_restart_instruction(sections: dict[str, str]) -> list[str]:
    restart = sections.get("Restart Instruction", "")
    if not restart:
        return []
    lower = restart.lower()
    if "continue" not in lower and "load" not in lower and "use" not in lower:
        return ["Restart Instruction should contain an explicit startup command."]
    if "handoff" not in lower and ".md" not in lower:
        return ["Restart Instruction should point to the handoff file."]
    return []


def check_updated_timestamp(text: str) -> list[str]:
    if not re.search(r"(?m)^Updated:\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}", text):
        return ["Missing or malformed Updated timestamp. Expected: Updated: YYYY-MM-DD HH:MM ..."]
    return []


def check_authoritative_metadata(text: str) -> list[str]:
    errors: list[str] = []
    if not re.search(r"(?m)^Supersedes:\s+\S", text):
        errors.append('Missing Supersedes metadata. Expected: Supersedes: <path> or "none"')
    if not re.search(r"(?m)^Authoritative:\s+\S", text):
        errors.append("Missing Authoritative metadata.")
    return errors


def check_placeholders(text: str) -> list[str]:
    found = [marker for marker in PLACEHOLDER_MARKERS if marker in text]
    return [f"Template placeholder still present: {marker}" for marker in found]


def check_sensitive_content(text: str) -> list[str]:
    errors: list[str] = []
    seen: set[tuple[int, str]] = set()
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            line_no = text[: match.start()].count("\n") + 1
            snippet = match.group(0)[:80]
            key = (line_no, snippet)
            if key not in seen:
                seen.add(key)
                errors.append(f"Possible secret or .env-style value near line {line_no}: {snippet[:40]}...")
    return errors


def check_active_pointer(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    if path.name.upper() == "ACTIVE.MD":
        return errors
    if path.parent.name != "handoffs":
        return errors

    active = path.parent / "ACTIVE.md"
    if not active.exists():
        errors.append("handoffs/ACTIVE.md is missing.")
        return errors

    active_text = read_text(active)
    if path.name not in active_text and str(path.resolve()) not in active_text:
        errors.append("handoffs/ACTIVE.md does not reference this handoff file.")
    if "Restart Instruction" not in active_text and "Continue this task" not in active_text:
        errors.append("handoffs/ACTIVE.md should include or point to the restart instruction.")
    return errors


def validate_file(path: Path) -> list[str]:
    if not path.exists():
        return [f"File does not exist: {path}"]
    if path.suffix.lower() != ".md":
        return [f"Expected a Markdown file, got: {path}"]

    text = read_text(path)
    sections = extract_sections(text)

    errors: list[str] = []
    errors.extend(check_updated_timestamp(text))
    errors.extend(check_authoritative_metadata(text))
    errors.extend(check_required_sections(sections))
    errors.extend(check_restart_instruction(sections))
    errors.extend(check_placeholders(text))
    errors.extend(check_sensitive_content(text))
    errors.extend(check_active_pointer(path, text))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a long-task handoff Markdown file.")
    parser.add_argument("handoff", type=Path, help="Path to the handoff Markdown file")
    args = parser.parse_args()

    path = args.handoff
    errors = validate_file(path)

    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAIL: {path}")
        return 1
    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
