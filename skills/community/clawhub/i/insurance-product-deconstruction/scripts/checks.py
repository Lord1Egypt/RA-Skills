"""Lightweight step-level checks (supervisors) for the pipeline.

Each check runs in <0.1s and catches errors at the source,
before they propagate to the next step.
"""

from __future__ import annotations

import json
from pathlib import Path

CACHE_DIR = ".product-cache"


def _load(product_dir: Path, name: str, default=None):
    path = product_dir / CACHE_DIR / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def check_build(product_dir: Path) -> dict:
    """Check 1: After build — verify extraction quality."""
    errors = []
    warnings = []

    inventory = _load(product_dir, "inventory.json", [])
    compact = _load(product_dir, "evidence.compact.json", {})
    cache_manifest = _load(product_dir, "cache-manifest.json", {})

    # No files processed
    if not inventory:
        errors.append("inventory.json is empty — no files were processed")
        return {"ok": False, "errors": errors, "warnings": warnings}

    # Check each file has extracted text
    extracted_dir = product_dir / CACHE_DIR / "extracted"
    for item in inventory:
        if item.get("duplicate_of"):
            continue
        if item["extension"] == ".pdf":
            json_file = extracted_dir / f"{Path(item['filename']).stem}.json"
            if not json_file.exists():
                errors.append(f"PDF {item['filename']} has no extracted text")
                continue
            pages = json.loads(json_file.read_text(encoding="utf-8"))
            total_chars = sum(len(p.get("text", "")) for p in pages)
            if total_chars < 100:
                warnings.append(f"PDF {item['filename']} has very little text ({total_chars} chars) — may be scanned")

    # Check evidence quality
    facts = compact.get("facts", [])
    if len(facts) < 5:
        errors.append(f"Only {len(facts)} evidence fields found — expected at least 5")

    # Check for TOC contamination
    toc_contaminated = 0
    for fact in facts:
        for c in fact.get("citations", []):
            if c.get("toc_score", 0) > 0.5:
                toc_contaminated += 1
                break
    if toc_contaminated > 0:
        warnings.append(f"{toc_contaminated} fields have TOC-contaminated citations")

    # Check for low-quality citations
    low_quality = 0
    for fact in facts:
        for c in fact.get("citations", []):
            if c.get("quality_score", 1) < 0.5:
                low_quality += 1
                break
    if low_quality > 0:
        warnings.append(f"{low_quality} fields have low-quality citations (score < 0.5)")

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "files": len(inventory),
            "non_duplicate": sum(1 for i in inventory if not i.get("duplicate_of")),
            "evidence_fields": len(facts),
            "toc_contaminated": toc_contaminated,
            "low_quality": low_quality,
        },
    }


def check_report(product_dir: Path) -> dict:
    """Check 2: After report — verify content completeness."""
    errors = []
    warnings = []

    report_input = _load(product_dir, "report-input.json")
    if not report_input:
        errors.append("report-input.json not found — run 'report' command first")
        return {"ok": False, "errors": errors, "warnings": warnings}

    clauses = report_input.get("clauses", {})
    manual = report_input.get("manual_content", {})
    underwriting = report_input.get("underwriting_rules", "")
    surrender = report_input.get("surrender_rules", "")

    # Critical clauses must be present
    critical_clauses = ["保险责任", "犹豫期", "宽限期", "保单贷款", "减保"]
    for name in critical_clauses:
        if name not in clauses or not clauses[name]:
            errors.append(f"Missing critical clause: {name}")

    # Underwriting rules
    if not underwriting:
        errors.append("Underwriting rules (投保规则) is empty")

    # At least some manual content
    if len(manual) < 2:
        warnings.append(f"Only {len(manual)} manual sections extracted — may be incomplete")

    # Check clause lengths
    for name, text_list in clauses.items():
        text = text_list[0] if isinstance(text_list, list) else str(text_list)
        if len(text) < 50:
            warnings.append(f"Clause '{name}' is very short ({len(text)} chars) — may be incomplete")

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "clauses": len(clauses),
            "manual_sections": len(manual),
            "has_underwriting": bool(underwriting),
            "has_surrender": bool(surrender),
        },
    }


def check_report_output(product_dir: Path) -> dict:
    """Check 3: After generate_report — verify report structure."""
    errors = []
    warnings = []

    # Check Obsidian output
    try:
        from scripts.config import get_obsidian_output
        obsidian_base = get_obsidian_output()
    except ImportError:
        obsidian_base = Path.home() / "Documents"
    report_path = obsidian_base / f"{product_dir.name}.md"
    if not report_path.exists():
        # Try review path
        report_path = product_dir / "report-draft.md"
    if not report_path.exists():
        errors.append("No report file found")
        return {"ok": False, "errors": errors, "warnings": warnings}

    text = report_path.read_text(encoding="utf-8")

    # Check 8 modules
    required_modules = [
        "## 一、产品基础信息",
        "## 二、核心保障责任拆解",
        "## 三、现金价值与收益分析",
        "## 四、免责条款与重要提示",
        "## 五、投保规则与权益",
        "## 六、增值服务清单",
        "## 七、优缺点与适合人群",
        "## 八、对比模板预留字段",
    ]
    for module in required_modules:
        if module not in text:
            errors.append(f"Missing module: {module}")

    # Check YAML frontmatter
    if not text.startswith("---"):
        errors.append("Missing YAML frontmatter")
    else:
        end = text.find("\n---", 4)
        if end < 0:
            errors.append("YAML frontmatter not closed")
        else:
            yaml_text = text[4:end]
            required_yaml = ["产品名称", "承保公司", "产品类型"]
            for field in required_yaml:
                if field not in yaml_text:
                    errors.append(f"Missing YAML field: {field}")

    # Check for forbidden terms
    forbidden = ["请审查", "待基于", "未提供", "未载明", "无法判断"]
    for term in forbidden:
        if term in text:
            errors.append(f"Forbidden term found: '{term}'")

    # Check for external comparison claims
    external_claims = ["市场领先", "行业平均", "头部保司", "同类较少", "不如同类"]
    for claim in external_claims:
        if claim in text:
            warnings.append(f"External comparison claim found: '{claim}'")

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "report_length": len(text),
            "modules_found": sum(1 for m in required_modules if m in text),
        },
    }


def run_all_checks(product_dir: Path) -> dict:
    """Run all three checks and return combined result."""
    results = {
        "build": check_build(product_dir),
        "report_input": check_report(product_dir),
        "report_output": check_report_output(product_dir),
    }

    all_ok = all(r["ok"] for r in results.values())
    all_errors = []
    all_warnings = []
    for step, result in results.items():
        for e in result.get("errors", []):
            all_errors.append(f"[{step}] {e}")
        for w in result.get("warnings", []):
            all_warnings.append(f"[{step}] {w}")

    return {
        "ok": all_ok,
        "errors": all_errors,
        "warnings": all_warnings,
        "steps": results,
    }
