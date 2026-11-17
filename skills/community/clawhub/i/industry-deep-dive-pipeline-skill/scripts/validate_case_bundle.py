from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

STAGES = {
    "input": ["00-case-brief.md"],
    "planning": [
        "00-case-brief.md",
        "01-fact-table.md",
        "02-originality-review.md",
        "03-planning-brief.md",
    ],
    "final": [
        "00-case-brief.md",
        "01-fact-table.md",
        "02-originality-review.md",
        "03-planning-brief.md",
        "04-draft.md",
        "05-machine-gate.json",
        "06-review-record.md",
        "07-final.md",
        "08-final-check.md",
        "FINAL-PACKAGE.md",
    ],
}

REQUIRED_INPUT_FIELDS = [
    "topic",
    "source_materials",
    "target_reader",
    "target_format",
    "length_range",
    "writing_profile",
    "timeliness",
    "confidentiality",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def field_has_value(text: str, field: str) -> bool:
    pattern = re.compile(rf"^\s*-\s*{re.escape(field)}\s*:\s*(.+)?$", re.I | re.M)
    match = pattern.search(text)
    if not match:
        return False
    value = (match.group(1) or "").strip()
    if field in {"source_materials", "target_reader", "length_range"}:
        following = text[match.end() : match.end() + 500]
        return bool(value or re.search(r"^\s{2,}-\s*\S+", following, re.M))
    return bool(value and value not in {"null", "[]", "{}"})


def has_gate_status(text: str, gate: str, allowed: set[str]) -> bool:
    block = re.search(rf"{gate}\s*:(.*?)(?:\n\S|\Z)", text, re.I | re.S)
    if not block:
        return False
    status = re.search(r"status\s*:\s*([a-z_]+)", block.group(1), re.I)
    return bool(status and status.group(1).lower() in allowed)


def validate_json(path: Path, issues: list[dict]) -> None:
    try:
        data = json.loads(read_text(path))
    except Exception as exc:
        issues.append({"severity": "P0", "file": path.name, "message": f"invalid JSON: {exc}"})
        return
    if not isinstance(data, dict):
        issues.append({"severity": "P1", "file": path.name, "message": "machine gate JSON must be an object"})
    if data.get("status") not in {"pass", "passed"}:
        issues.append({"severity": "P0", "file": path.name, "message": "machine gate did not pass"})


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an industry deep-dive case bundle")
    parser.add_argument("--case-dir", required=True)
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--output")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    case_dir = Path(args.case_dir)
    issues: list[dict] = []
    if not case_dir.is_dir():
        issues.append({"severity": "P0", "file": str(case_dir), "message": "case directory does not exist"})
    else:
        for filename in STAGES[args.stage]:
            path = case_dir / filename
            if not path.is_file() or path.stat().st_size == 0:
                issues.append({"severity": "P0", "file": filename, "message": "required file missing or empty"})

    brief = case_dir / "00-case-brief.md"
    if brief.is_file():
        text = read_text(brief)
        for field in REQUIRED_INPUT_FIELDS:
            if not field_has_value(text, field):
                issues.append({"severity": "P0", "file": brief.name, "message": f"required field missing: {field}"})
        if args.stage in {"planning", "final"} and not has_gate_status(text, "gate_a", {"approved"}):
            issues.append({"severity": "P0", "file": brief.name, "message": "Gate A is not approved"})
        if args.stage == "final" and not has_gate_status(text, "gate_b", {"approved", "not_required"}):
            issues.append({"severity": "P0", "file": brief.name, "message": "Gate B is neither approved nor not_required"})

    facts = case_dir / "01-fact-table.md"
    if args.stage == "final" and facts.is_file():
        text = read_text(facts)
        if re.search(r"\|\s*[^|]+\|[^\n]*\|\s*pending\s*\|", text, re.I):
            issues.append({"severity": "P0", "file": facts.name, "message": "pending fact remains"})
        if not re.search(r"fact gate\s*:\s*pass", text, re.I):
            issues.append({"severity": "P0", "file": facts.name, "message": "fact gate is not pass"})

    machine_gate = case_dir / "05-machine-gate.json"
    if args.stage == "final" and machine_gate.is_file():
        validate_json(machine_gate, issues)

    result = {
        "status": "pass" if not any(i["severity"] == "P0" for i in issues) else "fail",
        "stage": args.stage,
        "caseDir": str(case_dir),
        "issues": issues,
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    print(payload)
    if args.enforce and result["status"] != "pass":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
