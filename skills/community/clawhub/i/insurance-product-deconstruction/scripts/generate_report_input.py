#!/usr/bin/env python3
"""Generate report-input.json from evidence cache — the bridge between
evidence extraction and Claude report generation.

Claude reads ONLY this file to write the Obsidian markdown.
No PDF re-reading required.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evidence_pipeline.search import _line_is_toc, _TOC_DOTS, _TOC_PAGE_REFS

CACHE_DIR = ".product-cache"


def _load(product_dir: Path, name: str, default=None):
    path = product_dir / CACHE_DIR / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_full_clauses(product_dir: Path) -> dict[str, list[str]]:
    """Extract full clause text grouped by section header pattern.
    Only extracts from main policy terms, not additional insurance documents.
    """
    extracted_dir = product_dir / CACHE_DIR / "extracted"
    if not extracted_dir.exists():
        return {}

    # Load inventory to find main policy terms
    inventory = _load(product_dir, "inventory.json", [])
    main_policy_files = set()
    for item in inventory:
        if item.get("duplicate_of"):
            continue
        filename = item.get("filename", "")
        doc_type = item.get("document_type", "")
        # Identify main policy terms by checking if filename contains product name
        # and is NOT an additional insurance document
        if doc_type == "policy_terms":
            # Check if it's an additional insurance document
            stem = Path(filename).stem
            json_file = extracted_dir / f"{stem}.json"
            if json_file.exists():
                pages = json.loads(json_file.read_text(encoding="utf-8"))
                first_page = pages[0].get("text", "") if pages else ""
                # Additional insurance documents contain "附加" in their title
                if "附加" not in first_page[:200]:
                    main_policy_files.add(stem)

    # If no main policy found, use all policy_terms files (fallback)
    if not main_policy_files:
        for item in inventory:
            if item.get("duplicate_of"):
                continue
            if item.get("document_type") == "policy_terms":
                main_policy_files.add(Path(item["filename"]).stem)

    # Also include product manual files (they contain detailed clauses like 减保)
    for item in inventory:
        if item.get("duplicate_of"):
            continue
        if item.get("document_type") == "product_manual":
            stem = Path(item["filename"]).stem
            # Skip additional insurance manuals
            json_file = extracted_dir / f"{stem}.json"
            if json_file.exists():
                pages = json.loads(json_file.read_text(encoding="utf-8"))
                first_page = pages[0].get("text", "") if pages else ""
                if "附加" not in first_page[:200]:
                    main_policy_files.add(stem)

    all_text = []
    for json_file in sorted(extracted_dir.glob("*.json")):
        stem = json_file.stem
        # Only process main policy terms files
        if stem not in main_policy_files:
            continue
        pages = json.loads(json_file.read_text(encoding="utf-8"))
        for page in pages:
            text = page.get("text", "")
            if not text:
                continue
            # Skip TOC pages
            lines = text.split("\n")
            toc_lines = sum(1 for line in lines if _line_is_toc(line))
            if toc_lines >= max(3, len(lines) * 0.15):
                continue
            all_text.append(text)

    full_text = "\n".join(all_text)

    # Flexible section extraction with closing patterns
    sections = {}
    CLOSING_PATTERNS = [
        r"发生上述.*?情形",
        r"本合同终止",
        r"退还.*?现金价值",
        r"退还.*?保险费",
        r"合同即被解除",
        r"不承担.*?责任",
        r"我们不承担",
    ]

    def _find_end(text: str, start: int, end_patterns: list[str]) -> int:
        end = len(text)
        for cp in CLOSING_PATTERNS:
            for m in re.finditer(cp, text[start:]):
                candidate = start + m.end()
                if candidate - start > 100:
                    end = min(end, candidate)
                    break
        for ep in end_patterns:
            m = re.search(ep, text[start + 50:])
            if m:
                candidate = start + 50 + m.start()
                if candidate > start + 50:
                    end = min(end, candidate)
        return end

    section_defs = [
        ("保险责任", r"\d*\.?\s*保险责任\s", [r"\n\d*\.?\s*责任免除", r"\n\d+\.\s*[^\d]"]),
        ("责任免除", r"\d*\.?\s*责任免除\s", [r"\n\d*\.?\s*其他免责", r"\n\d+\.\s*保单红利", r"\n\d+\.\s*[^\d]"]),
        ("犹豫期", r"\d*\.?\s*犹豫期\s", [r"\n\d+\.\s*保险期间", r"\n\d+\.\s*[^\d]"]),
        ("宽限期", r"\d*\.?\s*宽限期\s", [r"\n\d+\.\s*现金价值", r"\n\d+\.\s*[^\d]"]),
        ("现金价值", r"\d*\.?\s*现金价值\s", [r"\n\d*\.?\s*保单贷款", r"\n\d+\.\s*[^\d]"]),
        ("保单贷款", r"\d*\.?\s*保单贷款\s", [r"\n\d*\.?\s*自动垫交", r"\n\d+\.\s*[^\d]"]),
        ("自动垫交", r"\d*\.?\s*自动垫交\s", [r"\n\d*\.?\s*减少基本保险金额", r"\n\d+\.\s*[^\d]"]),
        ("减保", r"\d*\.?\s*减少基本保险金额", [r"\n\d*\.?\s*减额交清", r"\n\d+\.\s*[^\d]"]),
        ("减额交清", r"\d*\.?\s*减额交清\s", [r"\n\d+\.\s*效力中止", r"\n\d+\.\s*[^\d]"]),
        ("第二投保人", r"\d*\.?\s*保单第二投保人权益", [r"\n\d+\.\s*合同解除", r"\n\d+\.\s*[^\d]"]),
        ("保单红利", r"\d*\.?\s*保单红利\s", [r"\n\d+\.\s*保险费", r"\n\d+\.\s*[^\d]"]),
        ("效力中止与恢复", r"\d*\.?\s*效力中止与恢复", [r"\n\d+\.\s*[^\d]"]),
        ("投保范围", r"\d*\.?\s*投保范围\s", [r"\n\d*\.?\s*犹豫期", r"\n\d+\.\s*[^\d]"]),
    ]
    for name, start_pattern, end_patterns in section_defs:
        match = re.search(start_pattern, full_text)
        if not match:
            continue
        start = match.start()
        end = _find_end(full_text, start, end_patterns)
        section_text = full_text[start:end].strip()
        if len(section_text) > 50:
            sections[name] = [clean_clause(section_text)]

    return sections


def clean_clause(text: str) -> str:
    """Clean extracted clause text: remove TOC lines, footers, normalize whitespace."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if _line_is_toc(stripped):
            continue
        if _TOC_DOTS.search(stripped):
            continue
        if _TOC_PAGE_REFS.search(stripped):
            continue
        if re.match(r"^本条款第\s*\d+\s*页\s*共\s*\d+\s*页$", stripped):
            continue
        cleaned.append(stripped)
    return "\n".join(cleaned)


def _extract_manual_content(product_dir: Path) -> dict[str, str]:
    """Extract key content from product manual (main product only)."""
    extracted_dir = product_dir / CACHE_DIR / "extracted"
    if not extracted_dir.exists():
        return {}

    content = {}
    for json_file in sorted(extracted_dir.glob("*.json")):
        pages = json.loads(json_file.read_text(encoding="utf-8"))
        # Skip附加险 files
        first_page = pages[0].get("text", "") if pages else ""
        if "附加" in first_page[:200]:
            continue
        # Skip TOC pages
        real_pages = []
        for p in pages:
            text = p.get("text", "")
            if not text:
                continue
            lines = text.split("\n")
            toc_lines = sum(1 for line in lines if _line_is_toc(line))
            if toc_lines >= max(3, len(lines) * 0.15):
                continue
            real_pages.append(text)
        full_text = "\n".join(real_pages)

        if "产品说明书" in full_text or "产品摘要" in full_text:
            # Company name from first page
            m = re.search(r"(\S+人寿)\S*股份\w*公司", full_text)
            if m:
                content["承保公司"] = m.group(0).replace(" ", "")

            # 投保须知
            match = re.search(r"(投保须知.*?)(?=保险责任|$)", full_text, re.DOTALL)
            if match:
                content["投保须知"] = clean_clause(match.group(1))

            # 保险责任
            match = re.search(r"(保险责任.*?)(?=责任免除|$)", full_text, re.DOTALL)
            if match:
                content["保险责任摘要"] = clean_clause(match.group(1))

            # 分红说明
            match = re.search(r"(关于分红.*?)(?=投保须知|$)", full_text, re.DOTALL)
            if match:
                content["分红说明"] = clean_clause(match.group(1))

            # 投保示例
            match = re.search(r"(投保示例.*?)(?=备注|$)", full_text, re.DOTALL)
            if match:
                content["投保示例"] = clean_clause(match.group(1))

            # 犹豫期
            match = re.search(r"(犹豫期.*?)(?=红利|$)", full_text, re.DOTALL)
            if match:
                content["犹豫期说明"] = clean_clause(match.group(1))

            # 红利分配
            match = re.search(r"(红利及红利分配.*?)(?=投保示例|$)", full_text, re.DOTALL)
            if match:
                content["红利分配"] = clean_clause(match.group(1))

    return content


def _extract_underwriting(product_dir: Path) -> str:
    """Extract underwriting rules content from main product only."""
    extracted_dir = product_dir / CACHE_DIR / "extracted"
    if not extracted_dir.exists():
        return ""

    # Load inventory to find main product underwriting
    inventory = _load(product_dir, "inventory.json", [])
    product_name = product_dir.name

    # Find best underwriting file (main product, not附加险)
    best_text = ""
    best_score = -1
    for item in inventory:
        if item.get("duplicate_of"):
            continue
        if item.get("document_type") not in ("underwriting_rules",):
            continue
        stem = Path(item["filename"]).stem
        json_file = extracted_dir / f"{stem}.json"
        if not json_file.exists():
            continue
        pages = json.loads(json_file.read_text(encoding="utf-8"))
        first_page = pages[0].get("text", "") if pages else ""
        full_text = "\n".join(p.get("text", "") for p in pages)

        # Skip附加险 files
        if "附加" in first_page[:200]:
            continue

        # Score: prefer files matching product name
        score = 0
        if any(kw in full_text[:300] for kw in ["投保规则", "体检规则"]):
            score += 1
        if product_name[:4] in full_text[:300]:
            score += 2
        if score > best_score:
            best_score = score
            best_text = full_text

    return clean_clause(best_text) if best_text else ""


def _extract_surrender_rules(product_dir: Path) -> str:
    """Extract保全规则 content."""
    extracted_dir = product_dir / CACHE_DIR / "extracted"
    if not extracted_dir.exists():
        return ""

    for json_file in sorted(extracted_dir.glob("*.json")):
        pages = json.loads(json_file.read_text(encoding="utf-8"))
        full_text = "\n".join(p.get("text", "") for p in pages)
        if "保全规则" in full_text or "减少基本保险金额" in full_text:
            if "投保规则" not in full_text:  # avoid underwriting rules
                return clean_clause(full_text)
    return ""


def _extract_table_data(product_dir: Path) -> dict:
    """Extract key data from Excel tables."""
    tables_dir = product_dir / CACHE_DIR / "tables"
    if not tables_dir.exists():
        return {}

    result = {}
    for json_file in sorted(tables_dir.glob("*.json")):
        workbook = json.loads(json_file.read_text(encoding="utf-8"))
        for sheet in workbook.get("sheets", []):
            name = sheet.get("name", "")
            rows = sheet.get("rows", [])
            header_paths = sheet.get("header_paths", {})
            unit_hints = sheet.get("unit_hints", [])

            if not rows:
                continue

            # Get column headers
            headers = {}
            for col_letter, path_list in header_paths.items():
                if path_list:
                    headers[col_letter] = " > ".join(str(p) for p in path_list)

            result[name] = {
                "total_rows": sheet.get("max_row", len(rows)),
                "total_cols": sheet.get("max_column", 0),
                "rows_sampled": len(rows),
                "headers": headers,
                "unit_hints": unit_hints,
                "sample_rows": rows[:10],  # first 10 rows for reference
            }

    return result


def generate_report_input(product_dir: Path) -> dict:
    """Generate the complete report input JSON."""
    product_dir = product_dir.resolve()

    # Load existing evidence
    inventory = _load(product_dir, "inventory.json", [])
    compact = _load(product_dir, "evidence.compact.json", {})

    # Extract structured content
    clauses = _extract_full_clauses(product_dir)
    manual = _extract_manual_content(product_dir)
    underwriting = _extract_underwriting(product_dir)
    surrender = _extract_surrender_rules(product_dir)
    tables = _extract_table_data(product_dir)

    # Build source inventory summary
    source_summary = []
    for item in inventory:
        if item.get("duplicate_of"):
            continue
        source_summary.append({
            "source_id": item["source_id"],
            "filename": item["filename"],
            "document_type": item["document_type"],
            "authority_rank": item["authority_rank"],
        })

    # Build facts lookup
    facts = {}
    for fact in compact.get("facts", []):
        citations = []
        for c in fact.get("citations", []):
            citations.append({
                "source_id": c["source_id"],
                "page": c.get("locator", {}).get("page"),
                "quote": c["quote"],
            })
        facts[fact["subject"]] = {
            "fact_id": fact["fact_id"],
            "citations": citations,
        }

    return {
        "product_name": product_dir.name,
        "source_files": source_summary,
        "facts": facts,
        "clauses": clauses,
        "manual_content": manual,
        "underwriting_rules": underwriting,
        "surrender_rules": surrender,
        "table_data": tables,
    }


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <product_dir>", file=sys.stderr)
        sys.exit(1)

    product_dir = Path(sys.argv[1])
    if not product_dir.is_dir():
        print(f"Not a directory: {product_dir}", file=sys.stderr)
        sys.exit(1)

    result = generate_report_input(product_dir)
    output_path = product_dir / CACHE_DIR / "report-input.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # Summary
    print(json.dumps({
        "output": str(output_path),
        "clauses_extracted": len(result["clauses"]),
        "manual_sections": len(result["manual_content"]),
        "facts_count": len(result["facts"]),
        "tables_count": len(result["table_data"]),
        "has_underwriting": bool(result["underwriting_rules"]),
        "has_surrender": bool(result["surrender_rules"]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
