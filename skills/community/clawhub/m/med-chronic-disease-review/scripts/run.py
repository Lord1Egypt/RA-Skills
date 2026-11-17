#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_ROOT = SCRIPT_DIR.parents[3]
_preprocess_dir = SKILLS_ROOT / "_shared" / "doc-preprocess" / "scripts"
if str(_preprocess_dir) not in sys.path:
    sys.path.insert(0, str(_preprocess_dir))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from preprocess import (
    PreprocessError,
    SUPPORTED_FILE_TYPES,
    detect_input_type,
    normalize_header,
    load_input_artifact,
)
from chronic_disease_review import (
    DEFAULT_LLM_BASE,
    DEFAULT_LLM_MODEL,
    _infer_label,
    _resolve_disease_code,
    dry_run_response,
    review_chronic_disease,
    validate_ocr_data,
)
from format_review_nl import build_natural_language

DOC_TYPE_RULES = [
    ("住院病案首页", ("住院病案首页", "病案首页")),
    ("出院记录", ("出院记录",)),
    ("入院记录", ("入院记录",)),
    ("诊断证明", ("诊断证明", "诊断证明书")),
    ("检验记录", ("检验报告", "检验记录")),
    ("检查记录", ("检查记录", "检查报告", "心电图报告")),
    ("长期医嘱", ("长期医嘱", "长期医嘱单")),
    ("体温记录", ("体温记录",)),
    ("身份证", ("居民身份证", "身份证")),
    ("社会保障卡", ("社会保障卡", "医保卡")),
    ("客户截图", ("审核结果", "认定材料", "门诊慢特病购药信息")),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preprocess pdf/doc/docx/xls/xlsx/csv/txt/json input into OCR-array JSON, then run chronic disease review."
    )
    parser.add_argument("--input", required=True, help="Input file path.")
    parser.add_argument(
        "--input-type",
        default="auto",
        choices=["auto", *sorted(SUPPORTED_FILE_TYPES)],
        help="Explicit input type. Default: auto.",
    )
    parser.add_argument("--sheet", default="", help="Optional sheet name for xlsx/xls inputs.")
    parser.add_argument("--encoding", default="utf-8", help="Text encoding for txt/csv inputs. Default: utf-8.")
    parser.add_argument(
        "--disease-code",
        required=True,
        help="糖尿病/高血压 or aliases diabetes/hypertension/dm/htn. Also supports auto.",
    )
    parser.add_argument("--review-type", default="慢病审核", help="review_type (default: 慢病审核)")
    parser.add_argument(
        "--appkey",
        default="",
        help="内部医疗大模型鉴权 key（--dry-run 时可选）。",
    )
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"LLM base URL (default: {DEFAULT_LLM_BASE})")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"LLM model (default: {DEFAULT_LLM_MODEL})")
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout seconds (default: 120).")
    parser.add_argument("--dry-run", action="store_true", help="Skip LLM call; emit placeholder response.")
    parser.add_argument("--output-json", default="", help="Path to save raw response JSON.")
    parser.add_argument("--output-text", default="", help="Path to save natural language summary.")
    parser.add_argument(
        "--save-prepared",
        action="store_true",
        help="Save the normalized OCR array next to the outputs for debugging.",
    )
    return parser.parse_args()


def infer_doc_type(text: str, fallback: str = "未分类文书") -> str:
    content = text or ""
    for doc_type, keywords in DOC_TYPE_RULES:
        if any(keyword in content for keyword in keywords):
            return doc_type
    return fallback


def normalize_to_int(value: Any, default: int) -> int:
    try:
        if value is None or str(value).strip() == "":
            return default
        return int(float(str(value).strip()))
    except Exception:
        return default


def build_ocr_item(*, file_name: str, page: int, doc_type: str, text: str) -> Optional[Dict[str, Any]]:
    content = (text or "").strip()
    if not content:
        return None
    return {
        "fileName": file_name,
        "page": page,
        "docType": doc_type or infer_doc_type(content),
        "ocrText": content,
    }


def first_matching_index(header_map: Dict[str, int], aliases: Sequence[str]) -> Optional[int]:
    for alias in aliases:
        idx = header_map.get(normalize_header(alias))
        if idx is not None:
            return idx
    return None


def coerce_ocr_items(items: List[Any], source_name: str) -> List[Dict[str, Any]]:
    ocr_items: List[Dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        text = item.get("ocrText") or item.get("text") or item.get("content") or item.get("format_page_text")
        if not isinstance(text, str) or not text.strip():
            continue
        file_name = str(item.get("fileName") or item.get("file") or item.get("name") or source_name)
        page = normalize_to_int(item.get("page") or item.get("pageNo") or item.get("page_num"), idx)
        doc_type = str(item.get("docType") or item.get("type") or item.get("documentType") or infer_doc_type(text))
        built = build_ocr_item(file_name=file_name, page=page, doc_type=doc_type, text=text)
        if built:
            ocr_items.append(built)
    if not ocr_items:
        raise PreprocessError("JSON array did not contain recognizable OCR items.")
    return validate_ocr_data(ocr_items)


def docs_to_ocr_items(docs: List[Any], source_name: str) -> List[Dict[str, Any]]:
    ocr_items: List[Dict[str, Any]] = []
    for idx, doc in enumerate(docs, start=1):
        if not isinstance(doc, dict):
            continue
        text = doc.get("format_page_text") or doc.get("text") or doc.get("content")
        if not isinstance(text, str) or not text.strip():
            continue
        doc_type = str(doc.get("docType") or doc.get("doc_name") or doc.get("docName") or infer_doc_type(text))
        built = build_ocr_item(file_name=source_name, page=idx, doc_type=doc_type, text=text)
        if built:
            ocr_items.append(built)
    if not ocr_items:
        raise PreprocessError("medicalRecord/docs JSON did not contain recognizable document text.")
    return validate_ocr_data(ocr_items)


def ocr_array_from_json(data: Any, source_name: str) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return coerce_ocr_items(data, source_name)
    if isinstance(data, dict):
        for key in ("ocr_data", "items", "pages", "results"):
            if isinstance(data.get(key), list):
                return coerce_ocr_items(list(data[key]), source_name)
        if isinstance(data.get("medicalRecord"), dict):
            docs = data["medicalRecord"].get("docs")
            if isinstance(docs, list):
                return docs_to_ocr_items(docs, source_name)
        if isinstance(data.get("docs"), list):
            return docs_to_ocr_items(list(data["docs"]), source_name)
        if isinstance(data.get("text"), str):
            item = build_ocr_item(file_name=source_name, page=1, doc_type=infer_doc_type(data["text"]), text=data["text"])
            if item:
                return validate_ocr_data([item])
    raise PreprocessError("Unsupported JSON schema for chronic disease review.")


def ocr_array_from_tables(tables: List[Dict[str, Any]], source_name: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for table in tables:
        rows = table.get("rows") or []
        if not rows:
            continue
        header_map = {normalize_header(cell): idx for idx, cell in enumerate(rows[0]) if cell.strip()}
        text_idx = first_matching_index(header_map, ("ocrtext", "text", "content", "内容", "文本"))
        page_idx = first_matching_index(header_map, ("page", "页码", "pageno"))
        file_idx = first_matching_index(header_map, ("filename", "file", "name", "文件名"))
        doc_type_idx = first_matching_index(header_map, ("doctype", "type", "文书类型", "文档类型"))
        data_rows = rows[1:] if text_idx is not None else rows

        if text_idx is not None:
            for row_idx, row in enumerate(data_rows, start=1):
                if text_idx >= len(row):
                    continue
                text = row[text_idx].strip()
                if not text:
                    continue
                file_name = (
                    row[file_idx].strip()
                    if file_idx is not None and file_idx < len(row) and row[file_idx].strip()
                    else source_name
                )
                page = normalize_to_int(
                    row[page_idx] if page_idx is not None and page_idx < len(row) else None, row_idx
                )
                doc_type_value = (
                    row[doc_type_idx].strip()
                    if doc_type_idx is not None and doc_type_idx < len(row)
                    else infer_doc_type(text, table["name"])
                )
                built = build_ocr_item(file_name=file_name, page=page, doc_type=doc_type_value, text=text)
                if built:
                    items.append(built)
            continue

        merged_lines = [" | ".join(cell for cell in row if cell) for row in rows if any(cell for cell in row)]
        merged_text = "\n".join(line for line in merged_lines if line.strip()).strip()
        if merged_text:
            built = build_ocr_item(
                file_name=source_name,
                page=len(items) + 1,
                doc_type=infer_doc_type(merged_text, table["name"]),
                text=merged_text,
            )
            if built:
                items.append(built)

    if not items:
        raise PreprocessError("Could not derive OCR text rows from the table input.")
    return validate_ocr_data(items)


def ocr_array_from_pages(pages: List[str], source_name: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for idx, page_text in enumerate(pages, start=1):
        built = build_ocr_item(
            file_name=source_name,
            page=idx,
            doc_type=infer_doc_type(page_text),
            text=page_text,
        )
        if built:
            items.append(built)
    if not items:
        raise PreprocessError("No non-empty text pages were extracted from the input.")
    return validate_ocr_data(items)


def preprocess_to_ocr_array(path: Path, input_type: str, encoding: str, sheet_name: str) -> List[Dict[str, Any]]:
    artifact = load_input_artifact(path, input_type, encoding, sheet_name, pdf_as_single_text=False)
    kind = artifact["kind"]
    if kind == "pages":
        return ocr_array_from_pages(artifact["pages"], path.name)
    if kind == "text":
        return ocr_array_from_pages([artifact["text"]], path.name)
    if kind == "json":
        return ocr_array_from_json(artifact["data"], path.name)
    if kind == "tables":
        return ocr_array_from_tables(artifact["tables"], path.name)
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def resolve_or_infer_disease_code(raw: str, ocr_data: List[Dict[str, Any]]) -> str:
    value = (raw or "").strip()
    if value and value.lower() != "auto":
        resolved = _resolve_disease_code(value)
        if resolved is None:
            raise PreprocessError("Unable to resolve --disease-code.")
        return resolved
    content = "\n".join(item.get("ocrText", "") for item in ocr_data)
    if "糖尿病" in content:
        return "糖尿病"
    if "高血压" in content:
        return "高血压"
    raise PreprocessError("Could not infer disease code from OCR text; please pass --disease-code explicitly.")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"✗ Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        input_type = detect_input_type(input_path, args.input_type)
        ocr_data = preprocess_to_ocr_array(input_path, input_type, args.encoding, args.sheet)
        disease_code = resolve_or_infer_disease_code(args.disease_code, ocr_data)
    except Exception as exc:
        print(f"✗ Preprocess Error: {exc}", file=sys.stderr)
        return 1

    try:
        if args.dry_run:
            resp = dry_run_response(disease_code=disease_code, review_type=args.review_type)
        else:
            if not (args.appkey or "").strip():
                print("✗ Error: --appkey is required unless --dry-run is set.", file=sys.stderr)
                return 1
            resp = review_chronic_disease(
                ocr_data,
                disease_code=disease_code,
                review_type=args.review_type or "慢病审核",
                appkey=args.appkey.strip(),
                base=args.base,
                model=args.model,
                timeout=args.timeout,
            )
    except Exception as exc:
        print(f"✗ Error: {exc}", file=sys.stderr)
        return 1

    label = _infer_label(disease_code)
    default_base = Path("../runs/med-chronic-disease-review")
    out_json = Path(args.output_json) if args.output_json else (default_base / f"{label}_resp.json")
    out_text = Path(args.output_text) if args.output_text else (default_base / f"{label}_resp.txt")

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")

    text = build_natural_language(resp)
    out_text.parent.mkdir(parents=True, exist_ok=True)
    out_text.write_text(text, encoding="utf-8")

    if args.save_prepared:
        prepared_path = out_json.with_name(f"{out_json.stem}.prepared.json")
        prepared_path.write_text(json.dumps(ocr_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✓ Prepared OCR array saved to: {prepared_path}")

    print(f"✓ Saved raw JSON to: {out_json}")
    print(f"✓ Saved natural language to: {out_text}")
    print("\n--- Natural language preview ---")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
