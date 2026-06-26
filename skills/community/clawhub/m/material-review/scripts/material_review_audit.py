#!/usr/bin/env python3
"""Material review script for data-sharing submission docs.

This script extracts structured fields from a filled `.docx` material based on
the shared-template shape, then audits the content according to review rules.
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET


W_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


BASIC_FIELD_ALIASES: Dict[str, List[str]] = {
    "unit_department": ["单位及科室"],
    "contact_person": ["联系人"],
    "contact_phone": ["联系电话", "联系号码"],
    "system_name": ["系统名称"],
    "system_intro": ["系统简介"],
    "go_live_time": ["上线时间", "系统上线时间"],
    "dev_company_contact": ["开发公司及联系人", "开发公司"],
    "database_type": ["系统采用的数据库", "数据库类型"],
    "data_provide_mode": ["数据提供方式"],
    "database_ip": ["连接IP", "数据库IP"],
    "database_port": ["端口"],
    "database_name": ["数据库名", "库名"],
    "readonly_account": ["只读账号"],
    "database_password_note": ["密码"],
}

RESOURCE_FIELD_ALIASES: Dict[str, List[str]] = {
    "resource_name_cn": ["中文表名", "数据资源名称（中文", "数据资源名称(中文", "数据资源名称"],
    "resource_name_en": ["英文表名", "数据资源名称（英文", "数据资源名称(英文"],
    "summary": ["数据资源摘要"],
    "current_volume": ["目前数据量"],
    "data_increment": ["数据增量"],
    "primary_key": ["主键字段"],
    "incremental_fields": ["增量字段"],
    "update_frequency": ["数据更新频率"],
    "share_type": ["共享类型"],
    "open_type": ["开放类型"],
    "remark": ["备注"],
}

FREQUENCY_WORDS = ["每年", "每半年", "每季度", "每月", "每周", "每天", "每时", "实时", "不定时"]

REQUIRED_BASIC_FIELDS = [
    "unit_department",
    "contact_person",
    "contact_phone",
    "system_name",
    "system_intro",
    "go_live_time",
    "dev_company_contact",
]

REQUIRED_RESOURCE_FIELDS = [
    "resource_name_cn",
    "resource_name_en",
    "summary",
    "current_volume",
    "update_frequency",
]


@dataclass
class DataField:
    english_name: str = ""
    chinese_name: str = ""
    data_type_length: str = ""
    nullable: str = ""
    share_type: str = ""
    open_type: str = ""
    remark: str = ""


@dataclass
class DataResource:
    index: int
    resource_name_cn: str = ""
    resource_name_en: str = ""
    summary: str = ""
    current_volume: str = ""
    data_increment: str = ""
    primary_key: str = ""
    incremental_fields: str = ""
    update_frequency: str = ""
    share_type: str = ""
    open_type: str = ""
    remark: str = ""
    fields: List[DataField] = field(default_factory=list)
    raw_lines: List[str] = field(default_factory=list)


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _text_of(node: ET.Element) -> str:
    parts = []
    for t in node.findall(".//w:t", W_NS):
        if t.text:
            parts.append(t.text)
    return normalize_text("".join(parts))


def normalize_text(text: str) -> str:
    t = text.replace("\u3000", " ").replace("\xa0", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _extract_docx(path: Path) -> Tuple[List[str], List[List[List[str]]]]:
    with zipfile.ZipFile(path, "r") as zf:
        xml_bytes = zf.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    body = root.find(".//w:body", W_NS)
    if body is None:
        return [], []

    lines: List[str] = []
    tables: List[List[List[str]]] = []

    for child in body:
        name = _local_name(child.tag)
        if name == "p":
            line = _text_of(child)
            if line:
                lines.append(line)
        elif name == "tbl":
            table_rows: List[List[str]] = []
            for tr in child.findall(".//w:tr", W_NS):
                row = []
                for tc in tr.findall("./w:tc", W_NS):
                    cell_text = _text_of(tc)
                    row.append(cell_text)
                if any(cell for cell in row):
                    table_rows.append(row)
                    lines.extend([c for c in row if c])
            if table_rows:
                tables.append(table_rows)
    return lines, tables


def _value_after_colon(line: str) -> str:
    m = re.search(r"[：:]\s*(.+)$", line)
    return normalize_text(m.group(1)) if m else ""


def _looks_like_label(text: str) -> bool:
    merged = text.replace(" ", "")
    all_keywords = []
    for values in BASIC_FIELD_ALIASES.values():
        all_keywords.extend(values)
    for values in RESOURCE_FIELD_ALIASES.values():
        all_keywords.extend(values)
    return any(k.replace(" ", "") in merged for k in all_keywords)


def _match_alias(text: str, aliases: Dict[str, List[str]]) -> Optional[str]:
    merged = text.replace(" ", "")
    for key, keys in aliases.items():
        for k in keys:
            if k.replace(" ", "") in merged:
                return key
    return None


def _extract_kv_from_tables(tables: List[List[List[str]]]) -> Dict[str, str]:
    kv: Dict[str, str] = {}
    for table in tables:
        for row in table:
            # Parse row by pairs: [label, value, label, value...]
            col = 0
            while col + 1 < len(row):
                label = normalize_text(row[col])
                value = normalize_text(row[col + 1])
                if label and value:
                    kv[label] = value
                col += 2
    return kv


def _extract_basic_info(lines: List[str], tables: List[List[List[str]]]) -> Dict[str, str]:
    result: Dict[str, str] = {}

    # First pass: from table key-value pairs.
    kv = _extract_kv_from_tables(tables)
    for raw_label, raw_value in kv.items():
        k = _match_alias(raw_label, BASIC_FIELD_ALIASES)
        if k and raw_value:
            result[k] = raw_value

    # Second pass: line-based fallback.
    for idx, line in enumerate(lines):
        key = _match_alias(line, BASIC_FIELD_ALIASES)
        if not key:
            continue
        value = _value_after_colon(line)
        if not value and idx + 1 < len(lines):
            nxt = lines[idx + 1]
            if not _looks_like_label(nxt):
                value = normalize_text(nxt)
        if value:
            result[key] = value
    return result


def _resource_index_from_line(line: str) -> Optional[int]:
    m = re.search(r"数据资源\s*([0-9]+)", line.replace(" ", ""))
    if m:
        return int(m.group(1))
    return None


def _find_field_table_candidates(tables: List[List[List[str]]]) -> List[List[List[str]]]:
    candidates: List[List[List[str]]] = []
    for table in tables:
        has_header = False
        for row in table[:3]:
            joined = " ".join(row)
            if "英文字段" in joined and "中文描述" in joined:
                has_header = True
                break
        if has_header:
            candidates.append(table)
    return candidates


def _parse_fields_from_table(table: List[List[str]]) -> List[DataField]:
    fields: List[DataField] = []
    header_idx = -1
    for i, row in enumerate(table):
        joined = " ".join(row)
        if "英文字段" in joined and "中文描述" in joined:
            header_idx = i
            break
    if header_idx < 0:
        return fields

    for row in table[header_idx + 1 :]:
        cleaned = [normalize_text(c) for c in row if normalize_text(c)]
        if len(cleaned) < 2:
            continue
        # Skip repeated header/footer rows.
        test_join = " ".join(cleaned)
        if "英文字段" in test_join and "中文描述" in test_join:
            continue
        fields.append(
            DataField(
                english_name=cleaned[0] if len(cleaned) > 0 else "",
                chinese_name=cleaned[1] if len(cleaned) > 1 else "",
                data_type_length=cleaned[2] if len(cleaned) > 2 else "",
                nullable=cleaned[3] if len(cleaned) > 3 else "",
                share_type=cleaned[4] if len(cleaned) > 4 else "",
                open_type=cleaned[5] if len(cleaned) > 5 else "",
                remark=cleaned[6] if len(cleaned) > 6 else "",
            )
        )
    return fields


def _extract_resources(lines: List[str], tables: List[List[List[str]]]) -> List[DataResource]:
    resources: List[DataResource] = []
    current: Optional[DataResource] = None

    for line in lines:
        idx = _resource_index_from_line(line)
        if idx is not None:
            current = DataResource(index=idx)
            resources.append(current)
            continue

        if current is None:
            continue
        current.raw_lines.append(line)
        key = _match_alias(line, RESOURCE_FIELD_ALIASES)
        if not key:
            continue
        value = _value_after_colon(line)
        if value:
            setattr(current, key, value)
        else:
            # If frequency is given as standalone value in following lines.
            if key == "update_frequency":
                for freq in FREQUENCY_WORDS:
                    if freq in line:
                        current.update_frequency = freq
                        break

    # If no explicit "数据资源X", create one synthetic block so script can still audit.
    if not resources:
        resources = [DataResource(index=1, raw_lines=list(lines))]

    # Fill resource values from table key-value extraction as fallback.
    kv = _extract_kv_from_tables(tables)
    for raw_label, raw_value in kv.items():
        k = _match_alias(raw_label, RESOURCE_FIELD_ALIASES)
        if not k:
            continue
        # Put fallback values into first resource unless already present.
        target = resources[0]
        if not getattr(target, k, "") and raw_value:
            setattr(target, k, raw_value)

    # Parse field definition tables and attach by order.
    field_tables = _find_field_table_candidates(tables)
    for i, ft in enumerate(field_tables):
        parsed = _parse_fields_from_table(ft)
        if not parsed:
            continue
        target = resources[i] if i < len(resources) else resources[-1]
        target.fields.extend(parsed)

    return resources


def _extract_num(value: str) -> Optional[int]:
    if not value:
        return None
    m = re.search(r"\d+", value.replace(",", ""))
    if not m:
        return None
    return int(m.group(0))


def _contains_legal_basis(text: str) -> bool:
    if not text:
        return False
    keys = ["法律", "法规", "条例", "办法", "依据", "制度", "规定"]
    return any(k in text for k in keys)


def audit(structured: Dict[str, object]) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []

    basic = structured.get("basic_info", {})
    resources = structured.get("data_resources", [])
    assert isinstance(basic, dict)
    assert isinstance(resources, list)

    for field_name in REQUIRED_BASIC_FIELDS:
        if not normalize_text(str(basic.get(field_name, ""))):
            issues.append(
                {
                    "category": "必填缺失",
                    "location": f"基础信息.{field_name}",
                    "rule": "除备注外均需完整填写",
                    "message": f"缺少必填字段：{field_name}",
                    "suggestion": "补充该字段后重新提交。",
                    "severity": "high",
                }
            )

    go_live = normalize_text(str(basic.get("go_live_time", "")))
    if go_live in {"/", "-", "--"}:
        issues.append(
            {
                "category": "规则不符",
                "location": "基础信息.go_live_time",
                "rule": "上线时间需填写有效值",
                "message": f"系统上线时间无效：{go_live}",
                "suggestion": "改为真实上线日期（如 YYYY-MM-DD）。",
                "severity": "high",
            }
        )

    for idx, resource_obj in enumerate(resources, start=1):
        if isinstance(resource_obj, dict):
            normalized = dict(resource_obj)
            normalized.setdefault("index", idx)
            res = DataResource(**normalized)
        else:
            res = resource_obj
        assert isinstance(res, DataResource)
        loc_prefix = f"数据资源{res.index}"

        for field_name in REQUIRED_RESOURCE_FIELDS:
            value = normalize_text(getattr(res, field_name, ""))
            if not value:
                issues.append(
                    {
                        "category": "必填缺失",
                        "location": f"{loc_prefix}.{field_name}",
                        "rule": "数据资源关键字段需完整",
                        "message": f"{loc_prefix} 缺少字段：{field_name}",
                        "suggestion": "补充字段值并核对模板一致性。",
                        "severity": "high",
                    }
                )

        # Rule: data increment frequently written as pure number.
        inc = normalize_text(res.data_increment)
        if inc and re.fullmatch(r"\d+", inc):
            issues.append(
                {
                    "category": "规则不符",
                    "location": f"{loc_prefix}.data_increment",
                    "rule": "数据增量不应仅填数字",
                    "message": f"数据增量当前为纯数字：{inc}",
                    "suggestion": "填写增量字段策略，或明确全量更新。",
                    "severity": "high",
                }
            )

        # Rule: large volume should provide increment strategy.
        vol = _extract_num(res.current_volume)
        if vol is not None and vol > 10000:
            has_increment = bool(inc) or bool(normalize_text(res.incremental_fields))
            is_full_update = "全量更新" in (inc + " " + res.incremental_fields + " " + res.remark)
            if not has_increment and not is_full_update:
                issues.append(
                    {
                        "category": "规则不符",
                        "location": f"{loc_prefix}.data_increment",
                        "rule": "大数据量需填写增量策略",
                        "message": f"{loc_prefix} 当前数据量约 {vol}，但缺少增量策略。",
                        "suggestion": "补充增量字段（如 createtime/updatetime）或标注全量更新。",
                        "severity": "high",
                    }
                )

        # Rule: volume=0 tables should be confirmed.
        if vol == 0:
            issues.append(
                {
                    "category": "待确认",
                    "location": f"{loc_prefix}.current_volume",
                    "rule": "数据量为0需确认是否保留",
                    "message": f"{loc_prefix} 当前数据量为 0。",
                    "suggestion": "请业务方确认是否保留；无用则删除该表。",
                    "severity": "medium",
                }
            )

        # Rule: share type "不予共享" requires legal basis.
        share = normalize_text(res.share_type)
        if share == "不予共享" and not _contains_legal_basis(res.remark):
            issues.append(
                {
                    "category": "规则不符",
                    "location": f"{loc_prefix}.share_type",
                    "rule": "不予共享需提供法律依据",
                    "message": f"{loc_prefix} 标注“不予共享”但未给出依据。",
                    "suggestion": "补充法规依据，或改为有条件共享。",
                    "severity": "high",
                }
            )

        # Soft heuristic: likely non-business tables.
        names = f"{res.resource_name_cn} {res.resource_name_en}".lower()
        if any(x in names for x in ["log", "日志", "config", "配置", "sys_", "tmp"]):
            issues.append(
                {
                    "category": "待确认",
                    "location": f"{loc_prefix}.resource_name",
                    "rule": "业务无关表通常不纳入共享",
                    "message": f"{loc_prefix} 可能为配置/日志类表。",
                    "suggestion": "确认是否业务相关；若无关请移出共享清单。",
                    "severity": "low",
                }
            )

        # Rule: every field should have Chinese description and not same as English.
        for f_idx, fd in enumerate(res.fields, start=1):
            en = normalize_text(fd.english_name)
            cn = normalize_text(fd.chinese_name)
            if not en and not cn:
                continue
            if not cn:
                issues.append(
                    {
                        "category": "必填缺失",
                        "location": f"{loc_prefix}.fields[{f_idx}].chinese_name",
                        "rule": "每个数据项中文描述必填",
                        "message": f"字段 {en or '(未命名)'} 缺少中文描述。",
                        "suggestion": "补充准确中文业务含义。",
                        "severity": "high",
                    }
                )
            elif en and cn.lower() == en.lower():
                issues.append(
                    {
                        "category": "规则不符",
                        "location": f"{loc_prefix}.fields[{f_idx}].chinese_name",
                        "rule": "中文描述不能与英文字段完全一致",
                        "message": f"字段 {en} 中文描述与英文同名。",
                        "suggestion": "改为可读中文业务描述。",
                        "severity": "high",
                    }
                )
            if cn == "默认信息" and en.upper() != "TIMEFLAG":
                issues.append(
                    {
                        "category": "平台不一致",
                        "location": f"{loc_prefix}.fields[{f_idx}].chinese_name",
                        "rule": "中文名为默认信息需标注",
                        "message": f"字段 {en or '(未命名)'} 中文名为“默认信息”。",
                        "suggestion": "确认真实中文含义并修正。",
                        "severity": "medium",
                    }
                )

    return issues


def build_structured_data(
    submission_path: Path, template_path: Path, rule_path: Path
) -> Dict[str, object]:
    sub_lines, sub_tables = _extract_docx(submission_path)
    tpl_lines, _ = _extract_docx(template_path)
    rule_lines, _ = _extract_docx(rule_path)

    structured: Dict[str, object] = {
        "source": {
            "submission_docx": str(submission_path),
            "template_docx": str(template_path),
            "review_rule_docx": str(rule_path),
        },
        "template_items": sorted(set([x for x in tpl_lines if len(x) <= 40])),
        "basic_info": _extract_basic_info(sub_lines, sub_tables),
        "data_resources": [r.__dict__ for r in _extract_resources(sub_lines, sub_tables)],
        "rule_points": rule_lines,
    }
    return structured


def _to_markdown_report(issues: List[Dict[str, str]]) -> str:
    lines = [
        "# 材料审核报告",
        "",
        f"- 问题总数: {len(issues)}",
        "",
        "| 序号 | 分类 | 定位 | 规则 | 问题描述 | 修正建议 | 严重级别 |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, issue in enumerate(issues, start=1):
        row = (
            f"| {i} | {issue['category']} | {issue['location']} | {issue['rule']} | "
            f"{issue['message']} | {issue['suggestion']} | {issue['severity']} |"
        )
        lines.append(row)
    if not issues:
        lines.append("| - | - | - | - | 未发现显性问题 | 建议进行平台一致性人工复核 | - |")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Material review automation script")
    parser.add_argument("--submission", required=True, help="Path to filled submission .docx")
    parser.add_argument(
        "--template",
        default="material-review/2附件1-5：数据共享清单（试运行环节）.docx",
        help="Path to template .docx",
    )
    parser.add_argument(
        "--rules",
        default="material-review/文档审查.docx",
        help="Path to review-rules .docx",
    )
    parser.add_argument(
        "--output-dir",
        default="material-review/output",
        help="Directory for generated files",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    submission = Path(args.submission).expanduser().resolve()
    template = Path(args.template).expanduser().resolve()
    rules = Path(args.rules).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not submission.exists():
        raise FileNotFoundError(f"Submission docx not found: {submission}")
    if not template.exists():
        raise FileNotFoundError(f"Template docx not found: {template}")
    if not rules.exists():
        raise FileNotFoundError(f"Rule docx not found: {rules}")

    output_dir.mkdir(parents=True, exist_ok=True)
    structured = build_structured_data(submission, template, rules)
    issues = audit(structured)

    structured_path = output_dir / "structured_data.json"
    issues_path = output_dir / "issues.json"
    report_path = output_dir / "audit_report.md"

    structured_path.write_text(
        json.dumps(structured, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    issues_path.write_text(json.dumps(issues, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(_to_markdown_report(issues), encoding="utf-8")

    print(f"Structured data: {structured_path}")
    print(f"Issues: {issues_path}")
    print(f"Markdown report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
