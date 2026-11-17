#!/usr/bin/env python3
"""Build, query, calculate, and validate local insurance evidence caches."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evidence_pipeline.cache import (
    CACHE_DIRNAME,
    SCHEMA_VERSION,
    TOOL_VERSION,
    build_cache_manifest,
    compare_manifest,
    source_files,
)
from scripts.evidence_pipeline.calculations import break_even_metrics, calculate_xirr
from scripts.evidence_pipeline.inventory import build_inventory, classify_document
from scripts.evidence_pipeline.pdf_extract import extract_pdf_pages
from scripts.evidence_pipeline.search import build_evidence, compact_evidence, query_evidence
from scripts.evidence_pipeline.validator import validate_report
from scripts.evidence_pipeline.workbook_extract import extract_workbook
from scripts.generate_report_input import generate_report_input
from scripts.checks import check_build, check_report, check_report_output, run_all_checks

FIELD_SYNONYMS = {
    "减保": ["减保", "减少基本保险金额", "基本保险金额减少", "合同变更"],
    "保单贷款": ["保单贷款", "保险合同贷款", "借款", "贷款"],
    "第二投保人": ["第二投保人", "第二投保"],
    "宽限期": ["宽限期", "宽限"],
    "复效": ["复效", "效力恢复", "合同效力"],
    "犹豫期": ["犹豫期", "犹豫"],
    "等待期": ["等待期", "责任起算", "保险责任开始", "合同生效后"],
    "增值服务": ["增值服务", "健康管理权益", "客户服务", "就医服务", "绿通", "陪诊"],
    "年金": ["年金", "养老年金", "生存金", "生存保险金"],
    "身故保险金": ["身故保险金", "身故金", "身故"],
    "满期保险金": ["满期保险金", "满期金", "满期"],
    "红利": ["红利", "分红"],
    "责任免除": ["责任免除", "免责条款", "免责"],
    "减额交清": ["减额交清", "交清保险"],
    "自动垫交": ["自动垫交", "垫交", "保险费自动垫交"],
    "健康告知": ["健康告知", "如实告知"],
    "投保年龄": ["投保年龄", "承保年龄", "投保范围"],
    "缴费期间": ["缴费期间", "交费期间", "保险费的支付"],
    "保险期间": ["保险期间", "保障期间"],
    "最低保费": ["最低保费", "最低保险费", "最低年交保费"],
}


def cache_dir(product_dir: Path) -> Path:
    path = product_dir / CACHE_DIRNAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(product_dir: Path, name: str, default=None):
    path = product_dir / CACHE_DIRNAME / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def workbook_search_text(workbook: dict) -> str:
    values: list[str] = []
    for sheet in workbook.get("sheets", []):
        values.append(sheet.get("name", ""))
        values.extend(sheet.get("unit_hints", []))
        for path in sheet.get("header_paths", {}).values():
            values.extend(str(item) for item in path)
        for row in sheet.get("rows", [])[:50]:
            values.extend(str(value) for value in row if isinstance(value, str) and value.strip())
    return "\n".join(values)


def build(product_dir: Path) -> dict:
    product_dir = product_dir.resolve()
    cache = cache_dir(product_dir)
    old_manifest = load_json(product_dir, "cache-manifest.json")
    new_manifest = build_cache_manifest(product_dir)
    difference = compare_manifest(old_manifest, new_manifest)

    required = [
        "inventory.json",
        "evidence.json",
        "evidence.compact.json",
        "scenario-options.json",
        "validation.json",
    ]
    if (
        old_manifest
        and not difference.get("changed")
        and not difference.get("removed")
        and not difference.get("full_rebuild")
        and all((cache / name).exists() for name in required)
    ):
        compact = load_json(product_dir, "evidence.compact.json", {})
        return {
            "cache_hit": True,
            "processed_files": 0,
            "total_records": compact.get("total_records", 0),
            "evidence_fields": len(compact.get("facts", [])),
        }

    text_by_relative: dict[str, str] = {}
    page_records_by_relative: dict[str, list[dict]] = {}
    workbook_by_relative: dict[str, dict] = {}

    for path in source_files(product_dir):
        relative = path.relative_to(product_dir).as_posix()
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".csv"}:
            text_by_relative[relative] = path.read_text(encoding="utf-8", errors="replace")
        elif suffix == ".pdf":
            pages = extract_pdf_pages(path)
            page_records_by_relative[relative] = pages
            text_by_relative[relative] = "\n".join(page.get("text", "") for page in pages)
            save_json(cache / "extracted" / f"{path.stem}.json", pages)
        elif suffix in {".xls", ".xlsx"}:
            workbook = extract_workbook(path)
            workbook_by_relative[relative] = workbook
            text_by_relative[relative] = workbook_search_text(workbook)
            save_json(cache / "tables" / f"{path.stem}.json", workbook)

    inventory = build_inventory(product_dir, extracted_text=text_by_relative)
    save_json(cache / "inventory.json", inventory)

    records: list[dict] = []
    datasets: list[dict] = []
    for item in inventory:
        relative = item["relative_path"]
        if item.get("duplicate_of"):
            continue
        pages = page_records_by_relative.get(relative)
        if pages:
            for page in pages:
                records.append({
                    "source_id": item["source_id"],
                    "authority_rank": item["authority_rank"],
                    "page": page["page"],
                    "method": page["method"],
                    "text": page["text"],
                })
        elif relative in text_by_relative:
            records.append({
                "source_id": item["source_id"],
                "authority_rank": item["authority_rank"],
                "page": None,
                "method": "workbook" if relative in workbook_by_relative else "text",
                "text": text_by_relative[relative],
            })

        workbook = workbook_by_relative.get(relative)
        if workbook:
            for sheet in workbook.get("sheets", []):
                datasets.append({
                    "dataset_id": f"dataset-{len(datasets) + 1:03d}",
                    "source_id": item["source_id"],
                    "sheet": sheet["name"],
                    "hidden": sheet["hidden"],
                    "max_row": sheet["max_row"],
                    "max_column": sheet["max_column"],
                    "header_paths": sheet["header_paths"],
                    "unit_hints": sheet["unit_hints"],
                })

    field_hits = build_evidence(records, FIELD_SYNONYMS)
    full_evidence = {
        "schema_version": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "product": {
            "source_directory_name": product_dir.name,
            "canonical_name": product_dir.name,
            "aliases": [],
        },
        "source_inventory": inventory,
        "field_hits": field_hits,
        "tabular_datasets": datasets,
    }
    save_json(cache / "evidence.json", full_evidence)

    compact_hits = compact_evidence(field_hits, limit_per_field=3)
    facts = []
    for field, hits in compact_hits.items():
        if not hits:
            continue
        citations = []
        for hit in hits[:2]:
            locator = {"type": "pdf" if hit.get("page") else "text"}
            if hit.get("page"):
                locator["page"] = hit["page"]
            citations.append({
                "source_id": hit["source_id"],
                "locator": locator,
                "quote": hit["quote"],
                "toc_score": hit.get("toc_score", 0),
                "quality_score": hit.get("quality_score", 0),
            })
        facts.append({
            "fact_id": f"fact-{len(facts) + 1:03d}",
            "subject": field,
            "certainty": "explicit",
            "citations": citations,
        })

    compact = {
        "schema_version": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "product": full_evidence["product"],
        "source_inventory": [
            {
                "source_id": item["source_id"],
                "relative_path": item["relative_path"],
                "document_type": item["document_type"],
                "authority_rank": item["authority_rank"],
            }
            for item in inventory
        ],
        "facts": facts,
        "tabular_datasets": datasets,
        "quality_checks": [],
        "total_records": len(records),
    }
    save_json(cache / "evidence.compact.json", compact)
    save_json(cache / "scenario-options.json", {
        "datasets": datasets,
        "required_dimensions": ["age", "sex", "premium_term", "coverage_term"],
    })
    save_json(cache / "validation.json", {"ok": True, "stage": "evidence-build"})
    save_json(cache / "cache-manifest.json", new_manifest)

    return {
        "cache_hit": False,
        "processed_files": len(inventory),
        "total_records": len(records),
        "evidence_fields": len(facts),
    }


def query(product_dir: Path, field: str, limit: int) -> dict:
    evidence = load_json(product_dir, "evidence.json", {})
    return query_evidence(evidence.get("field_hits", {}), field, limit=limit)


def calculate(product_dir: Path, scenario_path: Path) -> dict:
    cache = cache_dir(product_dir)
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    existing = load_json(product_dir, "calculations.json", {"calculations": []})
    xirr = calculate_xirr(scenario.get("events", []))
    output = {
        "calculation_id": f"calc-{len(existing['calculations']) + 1:03d}",
        "scenario_id": scenario.get("scenario_id"),
        "guarantee_class": scenario.get(
            "guarantee_class", "derived_from_guaranteed_inputs"
        ),
        "input_fact_ids": scenario.get("input_fact_ids", []),
        "xirr": round(xirr, 12) if xirr is not None else None,
        "break_even": break_even_metrics(scenario.get("yearly_records", [])),
        "events": scenario.get("events", []),
        "assumptions": scenario.get("assumptions", []),
    }
    existing["calculations"].append(output)
    save_json(cache / "calculations.json", existing)
    return output


def validate(product_dir: Path, report_path: Path) -> dict:
    cache = cache_dir(product_dir)
    compact = load_json(product_dir, "evidence.compact.json", {})
    manifest = {
        "source_inventory": load_json(product_dir, "inventory.json", []),
        "facts": compact.get("facts", []),
        "calculation_scenarios": load_json(
            product_dir, "calculations.json", {"calculations": []}
        ).get("calculations", []),
    }
    result = validate_report(
        report_path.read_text(encoding="utf-8"), manifest, source_dir=product_dir
    )
    output = {"ok": result.ok, "errors": result.errors, "warnings": result.warnings}
    save_json(cache / "validation.json", output)
    return output


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    build_parser = commands.add_parser("build")
    build_parser.add_argument("product_dir", type=Path)

    query_parser = commands.add_parser("query")
    query_parser.add_argument("product_dir", type=Path)
    query_parser.add_argument("field")
    query_parser.add_argument("--limit", type=int, default=20)

    calculate_parser = commands.add_parser("calculate")
    calculate_parser.add_argument("product_dir", type=Path)
    calculate_parser.add_argument("--scenario", type=Path, required=True)

    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("product_dir", type=Path)
    validate_parser.add_argument("--report", type=Path, required=True)

    report_parser = commands.add_parser("report")
    report_parser.add_argument("product_dir", type=Path)

    check_parser = commands.add_parser("check")
    check_parser.add_argument("product_dir", type=Path)
    check_parser.add_argument("step", nargs="?", default="all", choices=["all", "build", "report", "output"])
    return root


def main() -> None:
    args = parser().parse_args()
    if not args.product_dir.is_dir():
        raise SystemExit(f"Not a directory: {args.product_dir}")
    if args.command == "build":
        output = build(args.product_dir)
        # Auto-check after build
        check = check_build(args.product_dir)
        output["check"] = check
    elif args.command == "query":
        output = query(args.product_dir, args.field, args.limit)
    elif args.command == "calculate":
        output = calculate(args.product_dir, args.scenario)
    elif args.command == "report":
        output = generate_report_input(args.product_dir)
        cache = args.product_dir / CACHE_DIRNAME
        cache.mkdir(parents=True, exist_ok=True)
        save_json(cache / "report-input.json", output)
        # Auto-check after report
        check = check_report(args.product_dir)
        output = {"status": "ok", "output": str(cache / "report-input.json"), "check": check}
    elif args.command == "check":
        step = getattr(args, "step", "all")
        if step == "all":
            output = run_all_checks(args.product_dir)
        elif step == "build":
            output = check_build(args.product_dir)
        elif step == "report":
            output = check_report(args.product_dir)
        elif step == "output":
            output = check_report_output(args.product_dir)
        else:
            output = run_all_checks(args.product_dir)
    else:
        output = validate(args.product_dir, args.report)
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    print()
    if args.command == "validate" and not output["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
