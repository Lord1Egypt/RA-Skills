#!/usr/bin/env python3
"""Check paper-code joint analysis outputs for reader compatibility."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FIXED_FILES = [
    "analysis_bundle.json",
    "paper_reading_report.md",
    "paper_questions_for_code.md",
    "paper_code_crosswalk.md",
    "experiment_joint_reading.md",
    "implementation_omissions.md",
    "diagrams.md",
    "modify_method_guide.md",
    "validation_report.md",
]

REPORT_REQUIRED_TERMS = [
    ["问题", "problem"],
    ["假设", "assumption"],
    ["符号", "symbol"],
    ["公式", "equation", "loss"],
    ["方法", "method"],
    ["算法", "流程", "control flow"],
    ["实验", "Table", "Figure"],
    ["局限", "limitation", "gap"],
]

OTHER_REQUIRED_TERMS = {
    "paper_questions_for_code.md": ["疑问", "不清楚", "代码", "证据", "落地"],
    "paper_code_crosswalk.md": ["代码", "formula", "公式", "line", "行"],
    "experiment_joint_reading.md": ["Table", "Figure", "命令", "command", "代码"],
    "implementation_omissions.md": ["论文", "代码", "影响"],
    "diagrams.md": ["```mermaid", "sequenceDiagram", "classDiagram"],
    "modify_method_guide.md": ["文件", "函数", "方法", "模型", "算法", "smoke", "测试"],
    "validation_report.md": ["验证", "检查", "pass", "unresolved"],
}

MOJIBAKE_MARKERS = [
    "鎬", "绮捐", "鐞", "瀹", "楠", "璁", "婧", "鍥", "鍏",
    "闂", "妫", "骞", "乣", "銆", "€", "�", "Ã", "Â",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def mojibake_hits(text: str) -> list[str]:
    return [marker for marker in MOJIBAKE_MARKERS if marker in text]


def check_analysis_dir(root: Path, min_report_chars: int) -> tuple[list[str], dict]:
    errors: list[str] = []
    info: dict = {"root": str(root), "files": {}}

    for name in FIXED_FILES:
        path = root / name
        if not path.exists():
            errors.append(f"missing fixed artifact: {name}")
            continue
        text = read_text(path)
        hits = mojibake_hits(text)
        if hits:
            errors.append(f"{name} contains possible mojibake markers: {', '.join(hits[:8])}")
        info["files"][name] = {"bytes": path.stat().st_size}

    bundle_path = root / "analysis_bundle.json"
    if bundle_path.exists():
        try:
            data = json.loads(read_text(bundle_path))
            info["schema_version"] = data.get("schema_version")
            if data.get("schema_version") != "paper-code-joint-analysis.v1":
                errors.append("analysis_bundle.json schema_version must be paper-code-joint-analysis.v1")
            for key in [
                "intake",
                "paper_questions",
                "domain_critical_execution",
                "mechanisms",
                "experiments",
                "implementation_omissions",
                "diagrams",
                "modify_guide",
                "validation",
            ]:
                if key not in data:
                    errors.append(f"analysis_bundle.json missing key: {key}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"analysis_bundle.json cannot be parsed: {exc}")

    report_path = root / "paper_reading_report.md"
    if report_path.exists():
        report = read_text(report_path)
        char_count = len(report)
        info["report_chars"] = char_count
        if char_count < min_report_chars:
            errors.append(f"paper_reading_report.md too short: {char_count} chars < {min_report_chars}")
        for terms in REPORT_REQUIRED_TERMS:
            if not has_any(report, terms):
                errors.append("paper_reading_report.md missing topic group: " + "/".join(terms))
        if report.count("```math") == 0:
            errors.append("paper_reading_report.md should contain fenced math blocks for formulas")
        headings = re.findall(r"^#{1,4}\s+(.+)$", report, flags=re.MULTILINE)
        info["report_headings"] = headings[:50]

    for name, terms in OTHER_REQUIRED_TERMS.items():
        path = root / name
        if not path.exists():
            continue
        text = read_text(path)
        if not has_any(text, terms):
            errors.append(f"{name} missing expected terms: {terms}")

    return errors, info


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("analysis_dir", help="Directory containing analysis_bundle.json and fixed Markdown artifacts")
    parser.add_argument("--min-report-chars", type=int, default=12000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.analysis_dir).resolve()
    errors, info = check_analysis_dir(root, args.min_report_chars)
    report = {"valid": not errors, "errors": errors, "info": info}
    if args.json:
      print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if errors:
            print(f"INVALID outputs {root}")
            for err in errors:
                print(f"- {err}")
        else:
            print(f"VALID outputs {root}")
            print(f"- report chars: {info.get('report_chars')}")
            print(f"- schema: {info.get('schema_version')}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
