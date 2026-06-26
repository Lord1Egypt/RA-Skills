#!/usr/bin/env python3
"""
ValidateModuleOrder.py
Validate References/ModuleOrder.json:
- referenced files exist
- duplicates in priority/exclude
- overlap between priority and exclude
Outputs:
- References/ModuleOrderReport.md
- References/ModuleOrderReport.json
"""

from __future__ import annotations

import json
from pathlib import Path

REF_DIR = Path(__file__).resolve().parents[1] / "References"
ORDER_FILE = REF_DIR / "ModuleOrder.json"
OUT_MD = REF_DIR / "ModuleOrderReport.md"
OUT_JSON = REF_DIR / "ModuleOrderReport.json"


def main() -> None:
    issues: list[str] = []
    warnings: list[str] = []

    if not ORDER_FILE.exists():
        issues.append("ModuleOrder.json not found")
        data = {"priority": [], "exclude": []}
    else:
        try:
            data = json.loads(ORDER_FILE.read_text(encoding="utf-8-sig"))
        except Exception as e:
            issues.append(f"ModuleOrder.json parse error: {e}")
            data = {"priority": [], "exclude": []}

    priority = data.get("priority", []) if isinstance(data, dict) else []
    exclude = data.get("exclude", []) if isinstance(data, dict) else []

    if len(priority) != len(set(priority)):
        warnings.append("duplicate entries found in priority")
    if len(exclude) != len(set(exclude)):
        warnings.append("duplicate entries found in exclude")

    overlap = sorted(set(priority).intersection(set(exclude)))
    if overlap:
        warnings.append("entries appear in both priority and exclude: " + ", ".join(overlap))

    existing = {p.name for p in REF_DIR.glob("*.md")}
    for name in priority:
        if name not in existing:
            issues.append(f"priority references missing module: {name}")
    for name in exclude:
        if name not in existing and name not in {"ReferenceMap.md", "ModuleGraph.md", "ConflictReport.md"}:
            warnings.append(f"exclude references non-existing file: {name}")

    ok = len(issues) == 0
    result = {
        "ok": ok,
        "issues": issues,
        "warnings": warnings,
        "priority_count": len(priority),
        "exclude_count": len(exclude),
    }

    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Module Order Report", "", f"- OK: {ok}", f"- Priority entries: {len(priority)}", f"- Exclude entries: {len(exclude)}", ""]
    lines.append("## Issues")
    if issues:
        lines.extend([f"- {x}" for x in issues])
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Warnings")
    if warnings:
        lines.extend([f"- {x}" for x in warnings])
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Rebuild with: `python Scripts/ValidateModuleOrder.py`")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Updated: {OUT_MD}")
    print(f"Updated: {OUT_JSON}")
    print(f"OK: {ok}")

    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
