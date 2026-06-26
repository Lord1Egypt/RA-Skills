#!/usr/bin/env python3
"""初始化和维护腾讯文档岗位信息智能表格。"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import table_models
import upload_to_smartsheet as smartsheet


JOB_TABLE = "jobs"
JOB_FIELDS = table_models.get_field_definitions(JOB_TABLE)
JOB_KEY_TO_TITLE = table_models.get_field_key_to_title(JOB_TABLE)
JOB_FIXED_TITLE = table_models.get_fixed_sheet_title(JOB_TABLE)


def now_ms() -> str:
    return str(int(time.time() * 1000))


def find_smartsheet_by_title(title: str) -> dict[str, str] | None:
    """在腾讯文档中按固定标题查找岗位库。"""
    result = smartsheet.mcporter_call("manage.search_file", {"search_key": title})
    for item in result.get("list", []):
        if item.get("title") == title and item.get("file_id"):
            return item
    return None


def ensure_fields(file_id: str, sheet_id: str, fields: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing_fields = smartsheet.list_fields(file_id, sheet_id)
    existing_titles = {field["field_title"] for field in existing_fields}
    expected_types = {field["field_title"]: field["field_type"] for field in fields}

    conflicts = [
        f"{field['field_title']}({field.get('field_type')} != {expected_types[field['field_title']]})"
        for field in existing_fields
        if field.get("field_title") in expected_types
        and field.get("field_type") != expected_types[field["field_title"]]
    ]
    if conflicts:
        raise RuntimeError("岗位表字段类型冲突，请手动处理后重试: " + ", ".join(conflicts))

    missing = [field for field in fields if field["field_title"] not in existing_titles]
    if missing:
        print(f"  添加 {len(missing)} 个岗位字段...")
        smartsheet.add_fields(file_id, sheet_id, missing)
        existing_fields = smartsheet.list_fields(file_id, sheet_id)

    return existing_fields


def add_text(field_values: list[dict[str, Any]], field: str, value: Any) -> None:
    if value is None or value == "":
        return
    field_values.append({
        "field": field,
        "text_value": {"items": [{"text": str(value), "type": "text"}]},
    })


def add_datetime(field_values: list[dict[str, Any]], field: str, value: Any) -> None:
    if value is None or value == "":
        value = now_ms()
    field_values.append({"field": field, "string_value": str(value)})


def map_job_to_record(job: dict[str, Any]) -> dict[str, Any]:
    """将岗位字典映射为 SmartSheet add_records 输入。"""
    field_values: list[dict[str, Any]] = []
    field_types = {field["field_title"]: field["field_type"] for field in JOB_FIELDS}

    for key, title in JOB_KEY_TO_TITLE.items():
        field_type = field_types[title]
        value = job.get(key)
        if key == "updated_at":
            add_datetime(field_values, title, value)
        elif field_type == "text":
            add_text(field_values, title, value)
        elif field_type == "dateTime":
            add_datetime(field_values, title, value)
        else:
            raise RuntimeError(f"岗位表暂不支持字段类型: {title}={field_type}")

    return {"field_values": field_values}


def field_value_as_text(field_value: dict[str, Any]) -> str | None:
    if "string_value" in field_value:
        return str(field_value["string_value"])
    text_value = field_value.get("text_value")
    if text_value:
        return "".join(item.get("text", "") for item in text_value.get("items", []))
    if "number_value" in field_value:
        return str(field_value["number_value"])
    if "bool_value" in field_value:
        return str(field_value["bool_value"])
    return None


def existing_job_ids(file_id: str, sheet_id: str) -> set[str]:
    ids = set()
    for record in smartsheet.list_records(file_id, sheet_id):
        for field_value in record.get("field_values", []):
            if field_value.get("field") == "job_id":
                value = field_value_as_text(field_value)
                if value:
                    ids.add(value)
    return ids


def validate_job(job: dict[str, Any]) -> None:
    required = [
        "job_id",
        "job_title",
        "department",
        "hiring_manager",
        "must_have",
        "nice_to_have",
        "responsibilities",
        "level",
        "location",
        "salary_range",
        "interview_process",
        "status",
    ]
    missing = [key for key in required if not job.get(key)]
    if missing:
        raise ValueError(f"岗位记录缺少必填字段: {', '.join(missing)}")
    if job["status"] not in {"开放", "暂停", "关闭"}:
        raise ValueError(f"岗位 status 必须是 开放/暂停/关闭: {job['status']}")


def load_job_records(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return []
    records_path = Path(path).expanduser().resolve()
    data = json.loads(records_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("jobs"), list):
        data = data["jobs"]
    if not isinstance(data, list):
        raise ValueError("岗位记录文件必须是数组，或包含 jobs 数组的对象。")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("岗位记录文件中的每一项都必须是对象。")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file-id", help="已有岗位智能表格 file_id；不填时按固定表名查找或创建。")
    parser.add_argument("--sheet-title", default=JOB_FIXED_TITLE, help=f"固定岗位智能表格名（默认：{JOB_FIXED_TITLE}）")
    parser.add_argument("--space-id", help="知识库空间 ID（创建新表时使用）")
    parser.add_argument("--create-new", action="store_true", help="忽略同名搜索结果，强制创建新岗位表。")
    parser.add_argument("--no-cleanup", action="store_true", help="新建表时不清理默认空行和默认列。")
    parser.add_argument("--records-json", help="可选：导入真实岗位记录 JSON 文件。未传入时只初始化岗位表结构。")
    parser.add_argument("--dry-run", action="store_true", help="仅展示将执行的操作，不实际调用腾讯文档写入。")
    args = parser.parse_args()

    jobs = load_job_records(args.records_json)
    for job in jobs:
        validate_job(job)

    if args.dry_run:
        print(json.dumps({
            "status": "dry-run",
            "fixed_sheet_title": args.sheet_title,
            "fields": JOB_FIELDS,
            "records_to_import": jobs,
        }, ensure_ascii=False, indent=2))
        return 0

    file_id = args.file_id
    created_new = False
    found = None

    if not file_id and not args.create_new:
        found = find_smartsheet_by_title(args.sheet_title)
        if found:
            file_id = found["file_id"]
            print(f"🔎 使用已存在岗位表: {args.sheet_title} ({file_id})")

    if not file_id:
        print(f"🆕 创建岗位智能表格: {args.sheet_title}")
        file_id = smartsheet.create_smartsheet(args.sheet_title, args.space_id)
        created_new = True
        print(f"  file_id: {file_id}")

    print("📋 获取工作表...")
    tables = smartsheet.list_tables(file_id)
    if not tables:
        raise RuntimeError("岗位智能表格中没有工作表")
    sheet_id = tables[0]["sheet_id"]
    print(f"  sheet_id: {sheet_id} (标题: {tables[0].get('title', '')})")

    print("🔧 检查岗位字段...")
    ensure_fields(file_id, sheet_id, JOB_FIELDS)

    if created_new and not args.no_cleanup:
        print("🧹 清理默认行和列...")
        smartsheet.clean_default_rows_and_cols(file_id, sheet_id, JOB_FIELDS)

    record_ids: list[str] = []
    skipped_job_ids: list[str] = []

    if jobs:
        existing_ids = existing_job_ids(file_id, sheet_id)
        to_insert = []
        for job in jobs:
            if job["job_id"] in existing_ids:
                skipped_job_ids.append(job["job_id"])
            else:
                to_insert.append(map_job_to_record(job))

        if to_insert:
            print(f"📤 写入 {len(to_insert)} 条岗位记录...")
            result = smartsheet.add_records(file_id, sheet_id, to_insert)
            record_ids = [record["record_id"] for record in result]
        elif skipped_job_ids:
            print("  岗位记录已存在，跳过重复写入。")
    else:
        print("  未提供 --records-json，仅初始化/校验岗位表结构。")

    url = f"https://docs.qq.com/smartsheet/{file_id}"
    output = {
        "status": "success",
        "file_id": file_id,
        "sheet_id": sheet_id,
        "record_ids": record_ids,
        "skipped_job_ids": skipped_job_ids,
        "fixed_sheet_title": args.sheet_title,
        "url": url,
    }

    print(f"\n✅ 岗位信息库已就绪: {args.sheet_title}")
    print(f"   file_id: {file_id}")
    print(f"   sheet_id: {sheet_id}")
    print(f"   腾讯文档链接: {url}")
    print("\n" + json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
