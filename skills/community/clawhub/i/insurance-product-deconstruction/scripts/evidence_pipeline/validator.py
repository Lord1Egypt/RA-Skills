"""Validate evidence manifests and generated insurance deconstruction reports."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

MODULES = [
    "## 一、产品基础信息",
    "## 二、核心保障责任拆解",
    "## 三、现金价值与收益分析",
    "## 四、免责条款与重要提示",
    "## 五、投保规则与权益",
    "## 六、增值服务清单",
    "## 七、优缺点与适合人群",
    "## 八、对比模板预留字段",
]
REQUIRED_YAML = {"产品名称", "承保公司", "产品类型", "场景ID"}
FORBIDDEN_TERMS = (
    "未提供",
    "未载明",
    "无法判断",
    "市场领先",
    "行业平均",
    "头部保司",
    "不如同类产品",
)
EVIDENCE_PATTERN = re.compile(r"<!--\s*evidence:\s*([^>]+?)\s*-->")


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    parsed = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip().strip('"\'')
    return parsed


def _is_within(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


def validate_report(text: str, manifest: dict, *, source_dir: Path) -> ValidationResult:
    result = ValidationResult()

    positions = [text.find(module) for module in MODULES]
    if any(position < 0 for position in positions):
        missing = [module for module, position in zip(MODULES, positions) if position < 0]
        result.error(f"Missing required module(s): {missing}")
    elif positions != sorted(positions) or len(set(positions)) != len(positions):
        result.error("Module order is invalid")

    yaml_values = _frontmatter(text)
    missing_yaml = sorted(key for key in REQUIRED_YAML if not yaml_values.get(key))
    if missing_yaml:
        result.error(f"Missing required YAML field(s): {missing_yaml}")

    found_forbidden = sorted(term for term in FORBIDDEN_TERMS if term in text)
    if found_forbidden:
        result.error(f"Forbidden unsupported or placeholder term(s): {found_forbidden}")

    source_ids = set()
    for source in manifest.get("source_inventory", []):
        source_id = source.get("source_id")
        if source_id:
            source_ids.add(source_id)
        source_path = source.get("path")
        if source_path and not _is_within(Path(source_path), Path(source_dir)):
            result.error(f"Source outside product directory: {source_path}")

    fact_ids = set()
    for fact in manifest.get("facts", []):
        fact_id = fact.get("fact_id")
        if fact_id:
            fact_ids.add(fact_id)
        citations = fact.get("citations") or []
        if not citations:
            result.error(f"Fact {fact_id or '?'} has no citations")
        for citation in citations:
            if citation.get("source_id") not in source_ids:
                result.error(f"Fact {fact_id or '?'} references unknown source {citation.get('source_id')}")
            locator = citation.get("locator") or {}
            if locator.get("type") == "pdf" and not locator.get("page"):
                result.error(f"Fact {fact_id or '?'} PDF citation lacks page")
            if not citation.get("quote"):
                result.error(f"Fact {fact_id or '?'} citation lacks quote")

    calculation_ids = set()
    for calculation in manifest.get("calculation_scenarios", []):
        calculation_id = calculation.get("calculation_id")
        if calculation_id:
            calculation_ids.add(calculation_id)
        if not calculation.get("scenario_id"):
            result.error(f"Calculation {calculation_id or '?'} lacks scenario_id")
        if not calculation.get("guarantee_class"):
            result.error(f"Calculation {calculation_id or '?'} lacks guarantee_class")
        unknown_inputs = set(calculation.get("input_fact_ids", [])) - fact_ids
        if unknown_inputs:
            result.error(f"Calculation {calculation_id or '?'} references unknown fact(s): {sorted(unknown_inputs)}")

    known_evidence = fact_ids | calculation_ids
    comments = EVIDENCE_PATTERN.findall(text)
    referenced = {
        token.strip()
        for comment in comments
        for token in comment.split(",")
        if token.strip()
    }
    unknown = referenced - known_evidence
    if unknown:
        result.error(f"Report references unknown evidence id(s): {sorted(unknown)}")

    for module in MODULES:
        start = text.find(module)
        if start < 0:
            continue
        later = [text.find(other, start + len(module)) for other in MODULES]
        later = [position for position in later if position > start]
        end = min(later) if later else len(text)
        if not EVIDENCE_PATTERN.search(text[start:end]):
            result.error(f"Module lacks evidence citation: {module}")

    return result
