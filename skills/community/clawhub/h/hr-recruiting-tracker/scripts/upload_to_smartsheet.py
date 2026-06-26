#!/usr/bin/env python3
"""将简历包中的确定性候选人草稿上传到腾讯文档智能表格。

依赖：mcporter CLI + tencent-docs MCP server 已配置和授权。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import table_models

# ─── 智能表格字段定义 ───────────────────────────────────────────
#
# tencent-docs 1.0.33 的 smartsheet.add_fields 对 singleSelect/select 字段
# 会返回 22020: "Smartsheet invalid select field"。为保证 OpenClaw 首次运行
# 能真实落表，默认将枚举类字段建成 text；HR 后续可在腾讯文档 UI 中转换为单选。

CANDIDATE_FIELDS = table_models.get_field_definitions("candidates")
SENSITIVE_FIELDS = {"姓名", "电话", "邮箱", "简历来源", "简历包路径", "记录ID"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def mcporter_call(tool: str, args: dict) -> dict:
    """调用 tencent-docs MCP 工具。"""
    payload = json.dumps(args, ensure_ascii=False)
    proc = subprocess.run(
        ["mcporter", "call", "tencent-docs", tool, "--args", payload],
        text=True, capture_output=True, timeout=60, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"mcporter call '{tool}' 失败 (exit={proc.returncode}): {proc.stderr.strip()[:500]}"
        )
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"mcporter 返回非 JSON: {proc.stdout[:500]}")
    if result.get("error"):
        raise RuntimeError(f"MCP 错误: {result['error'][:500]}")
    return result


def list_tables(file_id: str) -> list[dict]:
    """获取智能表格的所有工作表。"""
    result = mcporter_call("smartsheet.list_tables", {"file_id": file_id})
    return result.get("sheets", [])


def list_fields(file_id: str, sheet_id: str) -> list[dict]:
    """获取工作表的所有字段。"""
    result = mcporter_call("smartsheet.list_fields", {
        "file_id": file_id, "sheet_id": sheet_id,
    })
    return result.get("fields", [])


def add_fields(file_id: str, sheet_id: str, fields: list[dict]) -> list[dict]:
    """批量添加字段到工作表。"""
    result = mcporter_call("smartsheet.add_fields", {
        "file_id": file_id, "sheet_id": sheet_id, "fields": fields,
    })
    return result.get("fields", [])


def add_records(file_id: str, sheet_id: str, records: list[dict]) -> list[dict]:
    """批量添加记录。"""
    result = mcporter_call("smartsheet.add_records", {
        "file_id": file_id, "sheet_id": sheet_id, "records": records,
    })
    return result.get("records", [])


def list_records(file_id: str, sheet_id: str) -> list[dict]:
    """列出工作表所有记录。"""
    all_records = []
    offset = 0
    while True:
        result = mcporter_call("smartsheet.list_records", {
            "file_id": file_id, "sheet_id": sheet_id,
            "offset": offset, "limit": 100,
        })
        records = result.get("records", [])
        all_records.extend(records)
        if not result.get("has_more"):
            break
        offset = result.get("next", offset + len(records))
    return all_records


def delete_records(file_id: str, sheet_id: str, record_ids: list[str]):
    """删除默认空行。"""
    if not record_ids:
        return
    mcporter_call("smartsheet.delete_records", {
        "file_id": file_id, "sheet_id": sheet_id,
        "record_ids": record_ids,
    })


def delete_fields(file_id: str, sheet_id: str, field_ids: list[str]):
    """删除默认列。"""
    if not field_ids:
        return
    mcporter_call("smartsheet.delete_fields", {
        "file_id": file_id, "sheet_id": sheet_id,
        "field_ids": field_ids,
    })


def create_smartsheet(title: str, space_id: str | None = None) -> str:
    """创建新的智能表格文档，返回 file_id。"""
    args = {"title": title, "file_type": "smartsheet"}
    if space_id:
        args["space_id"] = space_id
    result = mcporter_call("manage.create_file", args)
    file_id = result.get("file_id", "")
    if not file_id:
        raise RuntimeError(f"创建智能表格失败: {result}")
    return file_id


def find_smartsheets_by_title(title: str) -> list[dict[str, str]]:
    """按固定标题查找腾讯文档智能表格。"""
    result = mcporter_call("manage.search_file", {"search_key": title})
    matches = []
    for item in result.get("list", []):
        if item.get("title") == title and item.get("file_id"):
            matches.append(item)
    return matches


def find_smartsheet_by_title(title: str) -> dict[str, str] | None:
    matches = find_smartsheets_by_title(title)
    return matches[0] if matches else None


def resolve_smartsheet_target(
    file_id: str | None,
    sheet_title: str,
    space_id: str | None,
    create_new: bool,
    dry_run: bool = False,
    probe_remote: bool = False,
) -> tuple[str | None, bool, str]:
    """解析候选人库目标。默认复用固定表名，找不到才创建。"""
    if file_id:
        return file_id, False, "use_explicit_file_id"

    if dry_run and not probe_remote:
        return None, False, "dry_run_offline"

    if not create_new:
        matches = find_smartsheets_by_title(sheet_title)
        if matches:
            if len(matches) > 1:
                print(f"  注意：找到 {len(matches)} 个同名候选人库，将使用搜索结果中的第一个。需要指定时传 --file-id。")
            return matches[0]["file_id"], False, "reuse_existing_title"

    if dry_run:
        return None, True, "would_create"

    return create_smartsheet(sheet_title, space_id), True, "created_new"


def mask_name(name: str | None) -> str | None:
    if not name:
        return name
    if len(name) <= 1:
        return "*"
    return name[0] + "*" * (len(name) - 1)


def mask_phone(phone: str | None) -> str | None:
    if not phone:
        return phone
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 7:
        return "***"
    return f"{digits[:3]}****{digits[-4:]}"


def mask_email(email: str | None) -> str | None:
    if not email or "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if not local:
        return "***@" + domain
    return local[:1] + "***@" + domain


def mask_path(path: str | None) -> str | None:
    if not path:
        return path
    return "file://<redacted-bundle>"


def mask_record_id(record_id: str | None) -> str | None:
    if not record_id:
        return record_id
    if "-" not in record_id:
        return "***"
    _, suffix = record_id.rsplit("-", 1)
    return f"***-{suffix[:6]}..."


def redact_string_field(field: str, value: str | None) -> str | None:
    if field == "姓名":
        return mask_name(value)
    if field == "电话":
        return mask_phone(value)
    if field == "邮箱":
        return mask_email(value)
    if field == "简历包路径":
        return mask_path(value)
    if field == "记录ID":
        return mask_record_id(value)
    if field == "简历来源":
        return Path(value).suffix and f"***{Path(value).suffix}" or "***"
    return value


def redact_record(record: dict[str, Any]) -> dict[str, Any]:
    redacted = {"field_values": []}
    for field_value in record.get("field_values", []):
        copied = json.loads(json.dumps(field_value, ensure_ascii=False))
        field = copied.get("field")
        if field not in SENSITIVE_FIELDS:
            redacted["field_values"].append(copied)
            continue

        if "string_value" in copied:
            copied["string_value"] = redact_string_field(field, copied.get("string_value"))
        text_value = copied.get("text_value")
        if text_value:
            for item in text_value.get("items", []):
                item["text"] = redact_string_field(field, item.get("text"))
        redacted["field_values"].append(copied)
    return redacted


def should_block_unreviewed_upload(report: dict[str, Any]) -> bool:
    quality = report.get("quality", "unknown")
    return bool(report.get("review_required", quality != "high"))


def ensure_candidate_fields(file_id: str, sheet_id: str) -> list[dict]:
    """确保工作表有候选人字段，返回完整字段映射。"""
    existing_fields = list_fields(file_id, sheet_id)
    existing_titles = {f["field_title"] for f in existing_fields}
    expected_types = {f["field_title"]: f["field_type"] for f in CANDIDATE_FIELDS}

    conflicts = [
        f"{field['field_title']}({field.get('field_type')} != {expected_types[field['field_title']]})"
        for field in existing_fields
        if field.get("field_title") in expected_types
        and field.get("field_type") != expected_types[field["field_title"]]
    ]
    if conflicts:
        raise RuntimeError("智能表格字段类型冲突，请手动处理后重试: " + ", ".join(conflicts))

    needed = [f for f in CANDIDATE_FIELDS if f["field_title"] not in existing_titles]
    if needed:
        print(f"  添加 {len(needed)} 个新字段...")
        add_fields(file_id, sheet_id, needed)
        # 重新获取完整字段列表
        existing_fields = list_fields(file_id, sheet_id)

    return existing_fields


def clean_default_rows_and_cols(file_id: str, sheet_id: str, defined_fields: list[dict] | None = None):
    """删除智能表格创建时的默认空行和默认列。"""
    defined_titles = {f["field_title"] for f in (defined_fields or CANDIDATE_FIELDS)}

    # 清理默认列（不在候选人字段定义中的）
    fields = list_fields(file_id, sheet_id)
    default_field_ids = [
        f["field_id"] for f in fields
        if f["field_title"] not in defined_titles
    ]
    if default_field_ids:
        print(f"  删除 {len(default_field_ids)} 个默认列...")
        delete_fields(file_id, sheet_id, default_field_ids)

    # 清理默认空行（所有字段值均为空的记录）
    records = list_records(file_id, sheet_id)
    empty_record_ids = []
    for rec in records:
        field_values = rec.get("field_values", [])
        has_value = any(
            fv.get("text_value") or fv.get("string_value") or fv.get("number_value")
            or fv.get("bool_value") or fv.get("option_value")
            for fv in field_values
        )
        if not has_value:
            empty_record_ids.append(rec["record_id"])

    if empty_record_ids:
        print(f"  删除 {len(empty_record_ids)} 条默认空行...")
        delete_records(file_id, sheet_id, empty_record_ids)


def read_candidate_data(bundle_dir: Path) -> dict:
    """从简历包中读取候选人草稿和解析报告。"""
    draft_path = bundle_dir / "candidate_draft.json"
    report_path = bundle_dir / "extraction_report.json"

    if not draft_path.exists():
        raise FileNotFoundError(f"找不到 candidate_draft.json: {draft_path}")
    if not report_path.exists():
        raise FileNotFoundError(f"找不到 extraction_report.json: {report_path}")

    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    return {"draft": draft, "report": report}


DEGREE_ORDER = {"博士": 5, "硕士": 4, "研究生": 4, "本科": 3, "学士": 3, "大专": 2, "专科": 2, "高中": 1}
INSTITUTION_SUFFIXES = (
    "职业技术学院",
    "科技学院",
    "工程学院",
    "医学院",
    "音乐学院",
    "美术学院",
    "学院",
    "大学",
    "学校",
)


def normalize_cjk_spacing(text: str) -> str:
    """修复 PDF 文本层常见的中文字符被空格拆开问题。"""
    normalized = re.sub(r"\s+", " ", text.strip())
    for suffix in INSTITUTION_SUFFIXES:
        normalized_suffix = "".join(f"{char}\\s*" for char in suffix)
        normalized = re.sub(normalized_suffix, suffix, normalized)
    for degree in DEGREE_ORDER:
        normalized_degree = "".join(f"{char}\\s*" for char in degree)
        normalized = re.sub(normalized_degree, degree, normalized)
    common_majors = [
        "人工智能",
        "计算机科学与技术",
        "计算机科学",
        "软件工程",
        "数据科学与大数据技术",
        "信息安全",
        "电子信息工程",
    ]
    for major in common_majors:
        normalized_major = "".join(f"{char}\\s*" for char in major)
        normalized = re.sub(normalized_major, major, normalized)
    normalized = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def clean_education_part(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = value.strip(" \t-—–:：,，;；()（）[]【】")
    cleaned = re.sub(r"\s+", "", cleaned)
    return cleaned or None


def extract_graduation_year(line: str) -> str | None:
    years = re.findall(r"(?:19|20)\d{2}", line)
    return years[-1] if years else None


def parse_education_line(line: str) -> dict[str, str | int | None]:
    """将一条教育经历拆成学校、专业、学历、毕业年份。"""
    normalized = normalize_cjk_spacing(line)
    degree_match = re.search("|".join(map(re.escape, DEGREE_ORDER.keys())), normalized)
    degree = degree_match.group(0) if degree_match else None
    if degree == "研究生":
        degree = "硕士"

    school = None
    major = None
    for suffix in INSTITUTION_SUFFIXES:
        match = re.search(rf"(?P<school>[\u4e00-\u9fffA-Za-z0-9·（）()]+?{re.escape(suffix)})", normalized)
        if match:
            school = clean_education_part(match.group("school"))
            rest_start = match.end()
            rest_end = degree_match.start() if degree_match else len(normalized)
            if rest_end > rest_start:
                major = clean_education_part(normalized[rest_start:rest_end])
            break

    if major:
        major = re.sub("|".join(map(re.escape, DEGREE_ORDER.keys())), "", major)
        major = clean_education_part(major)

    return {
        "degree": degree,
        "school": school,
        "major": major,
        "graduation_year": extract_graduation_year(normalized),
        "degree_level": DEGREE_ORDER.get(degree or "", 0),
        "normalized": normalized,
    }


def extract_education_highest(education_evidence: list[str]) -> tuple[str | None, str | None, str | None, str | None]:
    """从教育证据中提取最高学历对应的学校、专业和毕业年份。"""
    parsed = [parse_education_line(line) for line in education_evidence]
    usable = [item for item in parsed if item["school"] or item["degree"] or item["major"]]
    if not usable:
        return None, None, None, None

    def sort_key(item: dict[str, str | int | None]) -> tuple[int, int]:
        year = int(item["graduation_year"]) if item.get("graduation_year") else 0
        return int(item.get("degree_level") or 0), year

    best = max(usable, key=sort_key)
    return (
        best.get("degree") if isinstance(best.get("degree"), str) else None,
        best.get("school") if isinstance(best.get("school"), str) else None,
        best.get("major") if isinstance(best.get("major"), str) else None,
        best.get("graduation_year") if isinstance(best.get("graduation_year"), str) else None,
    )


def map_candidate_to_record(draft: dict, report: dict, bundle_dir: str) -> dict:
    """将候选人草稿映射为 SmartSheet 记录格式。"""
    identity = draft.get("identity", {})
    profile = draft.get("profile", {})

    # 姓名
    name = identity.get("name")

    # 电话 - 脱敏处理
    phone_raw = identity.get("phone")
    phone = phone_raw if phone_raw else None

    # 邮箱
    email = identity.get("email")

    # 公司/工作年限
    company = profile.get("current_company")
    years = profile.get("years_of_experience")

    # 教育
    edu_evidence = profile.get("education_evidence", [])
    degree, school, major, grad_year = extract_education_highest(edu_evidence)

    # 技能
    skills = profile.get("skill_mentions", [])
    skill_text = "、".join(skills[:8]) if skills else None

    # 简历来源
    source = draft.get("source", {})
    resume_file = source.get("file_name", "")

    # 解析质量
    quality = report.get("quality", "unknown")
    quality_map = {"high": "高保真", "fallback": "回退解析", "text-only": "纯文本", "source": "纯文本"}
    quality_label = quality_map.get(quality, "回退解析")

    # HR 审核标记
    review_required = report.get("review_required", quality != "high")

    # 简历包路径
    bundle_uri = f"file://{bundle_dir}"

    now_ms = str(int(time.time() * 1000))

    field_values = []

    def add_text(field: str, value: str | None):
        if value:
            field_values.append({
                "field": field,
                "text_value": {"items": [{"text": str(value), "type": "text"}]}
            })

    def add_number(field: str, value: float | None):
        if value is not None:
            field_values.append({"field": field, "number_value": value})

    def add_bool(field: str, value: bool):
        field_values.append({"field": field, "bool_value": value})

    def add_string(field: str, value: str | None):
        if value:
            field_values.append({"field": field, "string_value": str(value)})

    # 映射所有字段
    add_text("姓名", name)
    add_string("电话", phone)
    add_string("邮箱", email)
    add_text("当前公司", company)
    add_number("工作年限", years)
    add_text("最高学历", degree)
    add_text("毕业院校", school)
    add_text("专业", major)
    add_number("毕业年份", int(grad_year) if grad_year and grad_year.isdigit() else None)
    add_text("技能标签", skill_text)
    add_text("求职意向", None)  # 从候选人草稿中提取
    add_text("招聘阶段", "简历筛选")
    add_text("简历来源", resume_file)
    add_text("解析质量", quality_label)
    add_bool("需HR审核", review_required)
    add_text("简历包路径", bundle_uri)
    add_string("录入时间", now_ms)
    sha = source.get("sha256", "")
    short_sha = sha[:12] if sha else resume_file[:20]
    add_text("记录ID", f"{name or 'unknown'}-{short_sha}")

    return {"field_values": field_values}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_dir", help="简历包目录路径")
    parser.add_argument("--file-id", help="已有候选人库 file_id；不填时先搜索固定表名，找不到才创建。")
    parser.add_argument("--space-id", help="知识库空间 ID（创建新表时使用）")
    parser.add_argument(
        "--sheet-title",
        default=table_models.get_fixed_sheet_title("candidates"),
        help=f"新建智能表格文档标题（默认：{table_models.get_fixed_sheet_title('candidates')}）",
    )
    parser.add_argument("--create-new", action="store_true", help="忽略固定表名搜索结果，强制创建新候选人库。")
    parser.add_argument("--no-cleanup", action="store_true", help="不清理默认空行和默认列")
    parser.add_argument("--dry-run", action="store_true", help="仅展示将写入的数据，不实际调用 API；默认不联网且输出脱敏。")
    parser.add_argument("--probe-remote", action="store_true", help="dry-run 时也探测腾讯文档目标表。未传入时 dry-run 保持离线。")
    parser.add_argument("--show-sensitive", action="store_true", help="在终端输出中显示姓名、电话、邮箱、路径等敏感值。默认脱敏。")
    parser.add_argument("--confirmed-reviewed", action="store_true", help="确认 HR 已审核 review_required=true 的候选人后，允许实际上传。")
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir).expanduser().resolve()
    if not bundle_dir.is_dir():
        print(f"简历包目录不存在: {bundle_dir}", file=sys.stderr)
        return 2

    # 1. 读取候选人草稿
    print("📖 读取候选人草稿...")
    data = read_candidate_data(bundle_dir)
    draft = data["draft"]
    report = data["report"]

    name = draft.get("identity", {}).get("name", "未知")
    display_name = name if args.show_sensitive else mask_name(name)
    quality = report.get("quality", "unknown")
    print(f"  候选人: {display_name}")
    print(f"  解析质量: {quality}")

    # 2. 映射为 SmartSheet 记录
    record = map_candidate_to_record(draft, report, str(bundle_dir))

    if should_block_unreviewed_upload(report) and not args.confirmed_reviewed and not args.dry_run:
        reasons = report.get("review_reasons") or ["解析结果标记为需要 HR 审核。"]
        print("候选人记录尚未确认审核，已阻止上传。", file=sys.stderr)
        for reason in reasons:
            print(f"- {reason}", file=sys.stderr)
        print("HR 审核后请添加 --confirmed-reviewed 再上传。", file=sys.stderr)
        return 3

    # 3. 获取或创建智能表格
    print("\n🎯 解析候选人库目标...")
    file_id, created_new, target_action = resolve_smartsheet_target(
        args.file_id,
        args.sheet_title,
        args.space_id,
        args.create_new,
        dry_run=args.dry_run,
        probe_remote=args.probe_remote,
    )

    if target_action == "reuse_existing_title":
        print(f"  复用固定候选人库: {args.sheet_title} ({file_id})")
    elif target_action == "use_explicit_file_id":
        print(f"  使用显式指定候选人库: {file_id}")
    elif target_action == "dry_run_offline":
        print(f"  dry-run 离线预览：实际运行时会先搜索或创建候选人库: {args.sheet_title}")
    elif target_action == "would_create":
        print(f"  未找到候选人库，dry-run 不创建；实际运行会创建: {args.sheet_title}")
    else:
        print(f"  创建新的候选人库: {args.sheet_title} ({file_id})")

    if args.dry_run:
        print("\n📋 将写入的数据（dry-run）:")
        output_record = record if args.show_sensitive else redact_record(record)
        print(json.dumps({
            "target": {
                "file_id": file_id,
                "sheet_title": args.sheet_title,
                "action": target_action,
                "remote_probe": args.probe_remote,
            },
            "review_required": should_block_unreviewed_upload(report),
            "sensitive_values_redacted": not args.show_sensitive,
            "record": output_record,
        }, ensure_ascii=False, indent=2))
        return 0

    if not file_id:
        raise RuntimeError("未能解析候选人库 file_id")

    # 4. 获取工作表
    print("📋 获取工作表...")
    tables = list_tables(file_id)
    if not tables:
        raise RuntimeError("智能表格中没有工作表")
    sheet_id = tables[0]["sheet_id"]
    print(f"  sheet_id: {sheet_id} (标题: {tables[0].get('title', '')})")

    # 5. 确保字段存在
    print("🔧 检查字段...")
    ensure_candidate_fields(file_id, sheet_id)

    # 6. 清理默认行和列（仅新建表时）
    if created_new and not args.no_cleanup:
        print("🧹 清理默认行和列...")
        clean_default_rows_and_cols(file_id, sheet_id)

    # 7. 上传记录
    print("📤 上传候选人记录...")
    result = add_records(file_id, sheet_id, [record])

    record_ids = [r["record_id"] for r in result]
    print(f"\n✅ 候选人「{display_name}」已录入智能表格")
    print(f"   file_id: {file_id}")
    print(f"   sheet_id: {sheet_id}")
    print(f"   record_id: {record_ids[0] if record_ids else 'N/A'}")
    print(f"   腾讯文档链接: https://docs.qq.com/smartsheet/{file_id}")

    # 输出 JSON 供程序化使用
    output = {
        "status": "success",
        "file_id": file_id,
        "sheet_id": sheet_id,
        "record_ids": record_ids,
        "candidate_name": display_name,
        "sensitive_values_redacted": not args.show_sensitive,
        "url": f"https://docs.qq.com/smartsheet/{file_id}",
    }
    print("\n" + json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
