#!/usr/bin/env python3
"""Normalize common e-commerce CSV/JSON/XLSX/XLS exports into period metrics.

The adapter is deliberately conservative: it never guesses between multiple
candidate sheets and never invents missing fields. The resulting JSON can be
passed directly to metric_gate.py because it contains a top-level ``rows``
array plus a source manifest for evidence tracing.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

PACKAGE_ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(PACKAGE_ROOT/'scripts'))
from artifact_contract import native_fact_identity

CORE_FIELDS = ("period", "gmv", "visitors", "buyers", "orders")
MAPPING_FILE = Path(__file__).resolve().parents[1] / "references" / "platform-field-mappings.json"
EMPTY_MARKERS = {"", "-", "--", "—", "无", "暂无", "n/a", "na", "null"}


class AdapterError(ValueError):
    """A user-fixable report adapter error."""


def normalize_header(value: Any) -> str:
    text = unicodedata.normalize("NFKC", "" if value is None else str(value))
    text = text.strip().casefold()
    return "".join(
        char for char in text if char.isalnum() or "\u4e00" <= char <= "\u9fff"
    )


def clean_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, float) and math.isnan(value):
        return None
    text = unicodedata.normalize("NFKC", str(value)).strip()
    if text.casefold() in EMPTY_MARKERS:
        return None
    return text.replace("￥", "").replace("¥", "").strip() or None


def load_mapping(path: Path = MAPPING_FILE) -> dict[str, list[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"字段映射文件无法读取: {path}: {exc}") from exc
    expected = {
        "schema_version": "2.0",
        "artifact_type": "platform_field_mapping_registry",
        "contract_name": "omni-ecom.platform-field-mappings",
        "contract_version": "2.0",
        "authenticity_boundary": "package_owned_aliases_not_platform_schema_authentication",
    }
    if not all(payload.get(key) == value for key, value in expected.items()):
        raise AdapterError("字段映射文件身份不是受支持的 2.0 契约")
    if not re.fullmatch(r"2\.\d+\.\d+", str(payload.get("mapping_version") or "")):
        raise AdapterError("字段映射版本无效")
    try:
        date.fromisoformat(str(payload.get("last_reviewed") or ""))
    except ValueError as exc:
        raise AdapterError("字段映射复核日期无效") from exc
    aliases = payload.get("aliases")
    if not isinstance(aliases, dict) or not aliases:
        raise AdapterError("字段映射文件缺少 aliases 对象")
    if not all(isinstance(field, str) and field and isinstance(values, list) and values and
               all(isinstance(alias, str) and alias.strip() for alias in values)
               for field, values in aliases.items()):
        raise AdapterError("字段映射 aliases 结构无效")
    return {field: list(values) for field, values in aliases.items()}


def mapping_index(aliases: dict[str, list[str]]) -> dict[str, str]:
    index: dict[str, str] = {}
    for field, names in aliases.items():
        for name in [field, *names]:
            key = normalize_header(name)
            if not key:
                continue
            if key in index and index[key] != field:
                raise AdapterError(f"字段别名冲突: {name} -> {index[key]} / {field}")
            index[key] = field
    return index


def as_matrix(rows: list[dict[str, Any]]) -> list[list[Any]]:
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    return [headers, *[[row.get(header) for header in headers] for row in rows]]


def read_csv(path: Path) -> list[tuple[str, list[list[Any]]]]:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                return [("CSV", [list(row) for row in csv.reader(handle)])]
        except UnicodeDecodeError as exc:
            last_error = exc
    raise AdapterError(f"CSV 编码无法识别: {path}: {last_error}")


def read_json(path: Path) -> list[tuple[str, list[list[Any]]]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"JSON 无法读取: {path}: {exc}") from exc
    rows = payload if isinstance(payload, list) else payload.get("rows") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise AdapterError("JSON 必须是对象数组，或包含 rows 对象数组")
    return [("JSON", as_matrix(rows))]


def read_xlsx(path: Path) -> list[tuple[str, list[list[Any]]]]:
    try:
        import openpyxl
    except ImportError as exc:
        raise AdapterError("读取 XLSX 需要 openpyxl；请安装或使用工作区内置 Python 依赖") from exc
    try:
        workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception as exc:  # openpyxl exposes several engine-specific exceptions
        raise AdapterError(f"XLSX 无法读取: {path}: {exc}") from exc
    return [
        (sheet.title, [list(row) for row in sheet.iter_rows(values_only=True)])
        for sheet in workbook.worksheets
    ]


def read_xls(path: Path) -> list[tuple[str, list[list[Any]]]]:
    try:
        import pandas as pd
    except ImportError as exc:
        raise AdapterError("读取旧版 XLS 需要 pandas/xlrd；请先另存为 XLSX 或安装读取依赖") from exc
    try:
        frames = pd.read_excel(path, sheet_name=None, header=None)
    except Exception as exc:
        raise AdapterError(f"XLS 无法读取；建议另存为 XLSX: {path}: {exc}") from exc
    return [(str(name), frame.where(frame.notna(), None).values.tolist()) for name, frame in frames.items()]


def read_sheets(path: Path) -> list[tuple[str, list[list[Any]]]]:
    suffix = path.suffix.casefold()
    if suffix == ".csv":
        return read_csv(path)
    if suffix == ".json":
        return read_json(path)
    if suffix == ".xlsx":
        return read_xlsx(path)
    if suffix == ".xls":
        return read_xls(path)
    raise AdapterError("仅支持 CSV、JSON、XLSX 或 XLS")


def find_header(matrix: list[list[Any]], index: dict[str, str]) -> tuple[int, list[Any], dict[str, str], list[str]] | None:
    for row_index, raw_header in enumerate(matrix):
        headers = [clean_value(value) for value in raw_header]
        known = [index.get(normalize_header(value)) for value in headers]
        known_fields = [field for field in known if field]
        if len(set(known_fields)) < 2:
            continue
        mapped: dict[str, str] = {}
        duplicate_headers: list[str] = []
        for position, field in enumerate(known):
            if not field:
                continue
            if field in mapped:
                duplicate_headers.append(str(headers[position]))
            else:
                mapped[field] = str(position)
        return row_index, headers, mapped, duplicate_headers
    return None


def normalize_sheet(
    source_path: Path,
    sheet_name: str,
    matrix: list[list[Any]],
    index: dict[str, str],
) -> dict[str, Any]:
    found = find_header(matrix, index)
    if found is None:
        return {
            "sheet": sheet_name,
            "status": "SKIPPED",
            "rows": [],
            "mapped_fields": [],
            "missing_core_fields": list(CORE_FIELDS),
            "unknown_headers": [],
            "warnings": ["未找到至少两个可识别指标字段的表头"],
        }
    header_row, headers, mapped, duplicate_headers = found
    unknown_headers = [
        str(header) for header in headers if header is not None and normalize_header(header) not in index
    ]
    missing_core = [field for field in CORE_FIELDS if field not in mapped]
    warnings: list[str] = []
    if duplicate_headers:
        warnings.append(f"同一指标出现重复候选列，已保留第一列: {duplicate_headers}")
    if missing_core:
        warnings.append(f"缺少核心字段: {', '.join(missing_core)}")
    rows: list[dict[str, Any]] = []
    if not missing_core:
        for raw_row_index, raw_row in enumerate(matrix[header_row + 1 :], header_row + 2):
            if not any(clean_value(value) is not None for value in raw_row):
                continue
            row: dict[str, Any] = {
                field: clean_value(raw_row[int(position)]) if int(position) < len(raw_row) else None
                for field, position in mapped.items()
            }
            row["_source_sheet"] = sheet_name
            row["_source_row"] = raw_row_index
            rows.append(row)
    return {
        "sheet": sheet_name,
        "status": "READY" if rows else "EMPTY",
        "rows": rows,
        "mapped_fields": sorted(mapped),
        "missing_core_fields": missing_core,
        "unknown_headers": unknown_headers,
        "row_count": len(rows),
        "header_row": header_row + 1,
        "warnings": warnings,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_report(path: Path, platform: str = "", sheet: str = "", all_sheets: bool = False) -> dict[str, Any]:
    if not path.is_file():
        raise AdapterError(f"输入文件不存在: {path}")
    aliases = load_mapping()
    index = mapping_index(aliases)
    candidates = [normalize_sheet(path, name, matrix, index) for name, matrix in read_sheets(path)]
    ready = [item for item in candidates if item["status"] == "READY"]
    if sheet:
        selected = [item for item in ready if item["sheet"] == sheet]
        if not selected:
            available = ", ".join(item["sheet"] for item in candidates)
            raise AdapterError(f"未找到可用工作表 {sheet!r}；可见工作表: {available}")
    elif len(ready) == 1:
        selected = ready
    elif len(ready) > 1 and all_sheets:
        selected = ready
    elif len(ready) > 1:
        names = ", ".join(item["sheet"] for item in ready)
        raise AdapterError(f"发现多个可映射工作表 ({names})；请用 --sheet 明确选择，或显式使用 --all-sheets")
    else:
        missing = sorted({field for item in candidates for field in item["missing_core_fields"]})
        raise AdapterError(f"没有可用于指标闸门的工作表；缺失核心字段: {', '.join(missing)}")

    rows: list[dict[str, Any]] = []
    for item in selected:
        for row in item["rows"]:
            row = dict(row)
            row["_source_file"] = path.name
            rows.append(row)
    warnings = [warning for item in candidates for warning in item.get("warnings", [])]
    sheet_manifest = [
        {key: value for key, value in item.items() if key != "rows"}
        for item in candidates
    ]
    return {
        "normalized_schema": "ecom-period-metrics-2.0",
        "source_manifest": {
            "file_name": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "platform": platform or "unknown",
            "selected_sheets": [item["sheet"] for item in selected],
            "available_sheets": sheet_manifest,
        },
        "rows": rows,
        "warnings": warnings,
    }


def self_test() -> None:
    fixture = Path("fixture.xlsx")
    matrix = [["日期", "成交金额", "商品访客数", "支付买家数", "支付订单数"], ["2026-08", "1,000", 100, 5, 6]]
    aliases = load_mapping()
    item = normalize_sheet(fixture, "Sheet1", matrix, mapping_index(aliases))
    assert item["status"] == "READY"
    assert item["rows"][0]["gmv"] == "1,000"
    assert item["rows"][0]["buyers"] == "5"
    print("normalize_reports self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="把电商原始报表规范化为可复算期间指标")
    parser.add_argument("input", nargs="?", help="CSV、JSON、XLSX 或 XLS 文件")
    parser.add_argument("--platform", default="", help="平台标识，例如 tmall、jd、douyin")
    parser.add_argument("--sheet", default="", help="明确选择一个工作表")
    parser.add_argument("--all-sheets", action="store_true", help="显式合并多个可映射工作表；可能触发重复期间闸门")
    parser.add_argument("--output", help="输出 JSON 路径")
    parser.add_argument("--run-id", help="本次运行编号")
    parser.add_argument("--client-scope", help="本次客户范围")
    parser.add_argument("--team-version", help="本次专家团版本")
    parser.add_argument("--self-test", action="store_true", help="运行内置测试")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.input:
        parser.error("必须提供 input，或使用 --self-test")
    if not all((args.run_id,args.client_scope,args.team_version)):
        parser.error("2.0 输出必须提供 --run-id、--client-scope 和 --team-version")
    input_path=Path(args.input).resolve()
    try:
        result = normalize_report(input_path, args.platform, args.sheet, args.all_sheets)
    except (OSError, AdapterError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    result.update(**native_fact_identity('normalized_report',args.team_version),
                  run_id=args.run_id,client_scope=args.client_scope,team_version=args.team_version)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        if output==input_path or (output.exists() and input_path.exists() and output.samefile(input_path)):
            print("ERROR: normalized_output_overlaps_input",file=sys.stderr); return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
        print(output)
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
