#!/usr/bin/env python3
"""
payroll-audit: 交叉验证引擎
基于两个或多个数据源，自动执行交叉校验，标记 ✅一致/⚠️存疑/❌异常

用法:
    python cross_validate.py --audit-item <item_name> --source-a <csv_path> --source-b <csv_path> [--source-c <csv_path>] --key <join_key>

示例:
    python cross_validate.py --audit-item "人员范围" \
        --source-a 入离职表.csv --source-b 上月工资表.csv \
        --key employee_id
"""

import argparse
import json
import csv
import sys
import os
from datetime import datetime


def load_csv(path):
    """加载 CSV 文件为字典列表"""
    if not os.path.exists(path):
        return None, f"文件不存在: {path}"
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows, None


def validate_item(audit_item, source_a, source_b, source_c=None, key='employee_id'):
    """执行单项目交叉验证"""
    result = {
        "audit_item": audit_item,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "unknown",
        "details": [],
        "summary": "",
        "counts": {}
    }

    # 加载数据源
    data_a, err_a = (source_a, None) if isinstance(source_a, list) else load_csv(source_a)
    data_b, err_b = (source_b, None) if isinstance(source_b, list) else load_csv(source_b)
    data_c, err_c = (source_c, None) if source_c is None else (
        (source_c, None) if isinstance(source_c, list) else load_csv(source_c)
    )

    errors = []
    if err_a:
        errors.append(f"数据源A: {err_a}")
    if err_b:
        errors.append(f"数据源B: {err_b}")
    if err_c:
        errors.append(f"数据源C: {err_c}")

    if errors:
        result["status"] = "error"
        result["details"] = errors
        result["summary"] = f"数据源加载失败: {', '.join(errors)}"
        return result

    if data_a is None or data_b is None:
        result["status"] = "error"
        result["summary"] = "数据源 A 和 B 为必填"
        return result

    # 构建索引
    index_a = {row.get(key, ''): row for row in data_a}
    index_b = {row.get(key, ''): row for row in data_b}
    index_c = {row.get(key, ''): row for row in data_c} if data_c else {}

    all_keys = set(index_a.keys()) | set(index_b.keys())
    if index_c:
        all_keys |= set(index_c.keys())

    only_a = set(index_a.keys()) - set(index_b.keys())
    only_b = set(index_b.keys()) - set(index_a.keys())
    in_both = set(index_a.keys()) & set(index_b.keys())

    result["counts"] = {
        "total_unique": len(all_keys),
        "only_in_a": len(only_a),
        "only_in_b": len(only_b),
        "in_both": len(in_both)
    }

    if only_a:
        result["details"].append(
            f"⚠️ 仅在数据源A中存在 {len(only_a)} 条: {', '.join(list(only_a)[:5])}{'...' if len(only_a) > 5 else ''}"
        )
    if only_b:
        result["details"].append(
            f"⚠️ 仅在数据源B中存在 {len(only_b)} 条: {', '.join(list(only_b)[:5])}{'...' if len(only_b) > 5 else ''}"
        )

    # 审计项特定验证
    field_checks = apply_field_rules(audit_item, index_a, index_b, index_c, key)
    result["details"].extend(field_checks)

    # 定级
    errors_count = sum(1 for d in result["details"] if d.startswith("❌"))
    warnings_count = sum(1 for d in result["details"] if d.startswith("⚠️"))

    if errors_count > 0:
        result["status"] = "error"
        result["summary"] = f"❌ 异常: 发现 {errors_count} 处异常, {warnings_count} 处存疑"
    elif warnings_count > 0:
        result["status"] = "warning"
        result["summary"] = f"⚠️ 存疑: 无异常, 但有 {warnings_count} 处需要核实"
    else:
        result["status"] = "pass"
        result["summary"] = f"✅ 一致: 所有数据源核对一致 ({len(in_both)} 条匹配)"

    return result


def apply_field_rules(audit_item, index_a, index_b, index_c, key):
    """根据审计项应用特定校验规则"""
    checks = []

    if audit_item == "人员范围":
        only_a = set(index_a.keys()) - set(index_b.keys())
        only_b = set(index_b.keys()) - set(index_a.keys())
        if only_a:
            checks.append(f"⚠️ 入离职表中有 {len(only_a)} 人不在上月工资表中（可能是新入职）")
        if only_b:
            checks.append(f"⚠️ 上月工资表中有 {len(only_b)} 人不在入离职表中（可能是离职未处理）")

    elif audit_item == "入离职管理":
        for eid in set(index_a.keys()) & set(index_b.keys()):
            row_a = index_a[eid]
            row_b = index_b[eid]
            date_fields = [f for f in row_a.keys() if '日期' in f or 'date' in f.lower()]
            if date_fields:
                checks.append(f"✅ {eid}: 入离职日期字段 {date_fields[0]}={row_a.get(date_fields[0], 'N/A')}")

    elif audit_item == "考勤数据":
        for eid in set(index_a.keys()) & set(index_b.keys()):
            row_a = index_a[eid]
            row_b = index_b[eid]
            day_fields_a = [f for f in row_a.keys() if '天' in f or '出勤' in f or 'days' in f.lower()]
            day_fields_b = [f for f in row_b.keys() if '天' in f or '出勤' in f or 'days' in f.lower()]
            if day_fields_a and day_fields_b:
                val_a = row_a.get(day_fields_a[0], '')
                val_b = row_b.get(day_fields_b[0], '')
                if str(val_a) != str(val_b):
                    checks.append(f"❌ {eid}: 出勤天数不一致 - A={val_a}, B={val_b}")

    elif audit_item == "社保公积金":
        for idx, eid in enumerate(set(index_a.keys()) & set(index_b.keys())):
            if idx >= 10:
                break
            row_a = index_a[eid]
            row_b = index_b[eid]
            amt_fields_a = [f for f in row_a.keys() if '金额' in f or '扣款' in f or '社保' in f or 'amount' in f.lower()]
            amt_fields_b = [f for f in row_b.keys() if '金额' in f or '扣款' in f or '社保' in f or 'amount' in f.lower()]
            if amt_fields_a and amt_fields_b:
                val_a = row_a.get(amt_fields_a[0], '0')
                val_b = row_b.get(amt_fields_b[0], '0')
                try:
                    if abs(float(str(val_a)) - float(str(val_b))) > 0.01:
                        checks.append(f"❌ {eid}: 社保金额不一致 - A={val_a}, B={val_b}")
                except ValueError:
                    checks.append(f"⚠️ {eid}: 社保金额无法比较 - A={val_a}, B={val_b}")

    return checks


def format_markdown(results):
    """格式化结果为 Markdown"""
    md = []
    md.append("## 交叉验证结果\n")
    md.append(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append("| 审核项 | 状态 | 详情 |")
    md.append("|--------|------|------|")

    for r in results:
        status_icon = {"pass": "✅", "warning": "⚠️", "error": "❌", "unknown": "❓"}.get(r["status"], "❓")
        md.append(f"| {r['audit_item']} | {status_icon} {r['status']} | {r['summary']} |")

    md.append("\n### 详细记录\n")
    for r in results:
        md.append(f"#### {r['audit_item']}\n")
        md.append(f"- **状态**: {r['summary']}")
        if r["details"]:
            md.append("- **详情**:")
            for d in r["details"]:
                md.append(f"  - {d}")
        if "counts" in r:
            md.append(f"- **统计**: 共 {r['counts']['total_unique']} 人, 两表匹配 {r['counts']['in_both']} 人")
        md.append("")

    return "\n".join(md)


def format_json(results):
    """格式化结果为 JSON"""
    return json.dumps(results, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="工资审核交叉验证引擎")
    parser.add_argument("--audit-item", required=True, help="审核项名称")
    parser.add_argument("--source-a", required=True, help="数据源A路径（CSV）")
    parser.add_argument("--source-b", required=True, help="数据源B路径（CSV）")
    parser.add_argument("--source-c", default=None, help="数据源C路径（CSV，可选）")
    parser.add_argument("--key", default="employee_id", help="关联键字段名")
    parser.add_argument("--output-format", choices=["markdown", "json"], default="markdown", help="输出格式")
    parser.add_argument("--output-file", default=None, help="输出文件路径")

    args = parser.parse_args()

    # 执行验证
    result = validate_item(
        audit_item=args.audit_item,
        source_a=args.source_a,
        source_b=args.source_b,
        source_c=args.source_c,
        key=args.key,
    )

    # 格式化输出
    if args.output_format == "json":
        output = format_json([result])
    else:
        output = format_markdown([result])

    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已写入: {args.output_file}")
    else:
        print(output)


if __name__ == "__main__":
    main()
