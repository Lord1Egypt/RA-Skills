#!/usr/bin/env python3
"""
DetectRuleConflicts.py
Scan markdown modules for potential rule conflicts based on opposite keyword patterns.
Outputs:
- References/ConflictReport.md
- References/ConflictReport.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from itertools import combinations

REF_DIR = Path(__file__).resolve().parents[1] / "References"
OUT_MD = REF_DIR / "ConflictReport.md"
OUT_JSON = REF_DIR / "ConflictReport.json"

PATTERNS = [
    (r"\b必须\b", r"\b可选\b"),
    (r"\b必须\b", r"\b禁止\b"),
    (r"\b允许\b", r"\b禁止\b"),
    (r"\b仅\b", r"\b任意\b"),
    (r"\bonly\b", r"\bany\b"),
    (r"\bmust\b", r"\boptional\b"),
    (r"\ballow\b", r"\bforbid\b"),
]


def load_modules() -> dict[str, str]:
    mods = {}
    for p in sorted(REF_DIR.glob("*.md")):
        if p.name in {"ReferenceMap.md", "ModuleGraph.md", "ConflictReport.md"}:
            continue
        mods[p.name] = p.read_text(encoding="utf-8", errors="ignore")
    return mods


def detect_conflicts(mods: dict[str, str]) -> list[dict]:
    results = []
    for a, b in combinations(mods.keys(), 2):
        ta, tb = mods[a], mods[b]
        found = []
        for p1, p2 in PATTERNS:
            c1a = len(re.findall(p1, ta, flags=re.IGNORECASE))
            c2a = len(re.findall(p2, ta, flags=re.IGNORECASE))
            c1b = len(re.findall(p1, tb, flags=re.IGNORECASE))
            c2b = len(re.findall(p2, tb, flags=re.IGNORECASE))
            # heuristic: one file dominated by p1 and another by p2
            if (c1a > 0 and c2b > 0) or (c2a > 0 and c1b > 0):
                found.append({"pair": [p1, p2], "counts": {a: [c1a, c2a], b: [c1b, c2b]}})
        if found:
            results.append({"modules": [a, b], "signals": found})
    return results


def write_outputs(conflicts: list[dict], module_count: int) -> None:
    OUT_JSON.write_text(json.dumps({"module_count": module_count, "conflict_groups": conflicts, "count": len(conflicts)}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Conflict Report",
        "",
        "Auto-generated potential rule conflict report (keyword heuristic).",
        "",
        f"- Modules scanned: {module_count}",
        f"- Potential conflict groups: {len(conflicts)}",
        "",
        "## Results",
    ]

    if not conflicts:
        lines.append("- No potential conflicts detected by heuristic patterns.")
    else:
        for i, c in enumerate(conflicts, 1):
            m1, m2 = c["modules"]
            lines.append(f"### {i}. `{m1}` vs `{m2}`")
            for s in c["signals"]:
                p1, p2 = s["pair"]
                lines.append(f"- Pattern: `{p1}` <-> `{p2}`")
            lines.append("")

    lines += [
        "## Notes",
        "- This report is heuristic and may include false positives.",
        "- Review flagged module pairs manually before changing rules.",
        "- Rebuild with: `python Scripts/DetectRuleConflicts.py`",
        "",
    ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    mods = load_modules()
    conflicts = detect_conflicts(mods)
    write_outputs(conflicts, len(mods))
    print(f"Updated: {OUT_MD}")
    print(f"Updated: {OUT_JSON}")
    print(f"Modules: {len(mods)}")
    print(f"Potential Conflicts: {len(conflicts)}")


if __name__ == "__main__":
    main()
