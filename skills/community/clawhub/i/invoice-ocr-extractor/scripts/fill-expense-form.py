#!/usr/bin/env python3
"""
报销单填写脚本 - invoice-ocr-extractor skill
将识别结果写入飞书报销系统或生成报销单草稿
"""

import argparse
import json
import os
import sys
from pathlib import Path


def load_results(source: str) -> list:
    """加载识别结果（JSON 文件）"""
    path = Path(source)
    if not path.exists():
        print(f"[ERROR] 文件不存在: {source}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def fill_feishu_expense(results: list, applicant_id: str = "") -> dict:
    """
    生成飞书报销单数据结构
    实际提交需要飞书报销 API（需单独配置）
    """
    items = []
    total = 0.0

    for r in results:
        if r.get("_duplicate"):
            continue
        amount = float(r.get("total_amount") or 0)
        total += amount
        items.append({
            "expense_date":     r.get("invoice_date", ""),
            "expense_type":     r.get("expense_category", "其他"),
            "amount":           amount,
            "currency":         "CNY",
            "merchant":         r.get("seller_name", ""),
            "invoice_code":     r.get("invoice_code", ""),
            "invoice_number":   r.get("invoice_number", ""),
            "remark":           f"发票识别 | 置信度: {r.get('confidence', 'unknown')}",
        })

    form = {
        "applicant_open_id": applicant_id,
        "total_amount":      round(total, 2),
        "currency":          "CNY",
        "expense_items":     items,
        "status":            "draft",
    }

    return form


def generate_summary(results: list) -> str:
    """生成费用汇总文本"""
    valid = [r for r in results if not r.get("_duplicate")]
    total = sum(float(r.get("total_amount") or 0) for r in valid)

    # 按费用类型汇总
    by_category = {}
    for r in valid:
        cat = r.get("expense_category", "其他")
        by_category[cat] = by_category.get(cat, 0) + float(r.get("total_amount") or 0)

    lines = [
        f"📋 报销汇总",
        f"共 {len(valid)} 张发票，合计 ¥{total:.2f}",
        "",
        "按费用类型：",
    ]
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        lines.append(f"  • {cat}：¥{amt:.2f}")

    # 校验问题汇总
    issues = []
    for r in valid:
        v = r.get("validation", {})
        if not v.get("passed"):
            for issue in v.get("issues", []):
                issues.append(f"  ⚠️ {r.get('file', '')} — {issue}")

    if issues:
        lines.append("")
        lines.append("需关注：")
        lines.extend(issues)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="报销单填写工具")
    sub = parser.add_subparsers(dest="cmd")

    # fill
    p_fill = sub.add_parser("fill", help="生成报销单")
    p_fill.add_argument("--source", required=True, help="识别结果 JSON 文件")
    p_fill.add_argument("--target", default="feishu-expense", help="目标系统")
    p_fill.add_argument("--applicant", default="", help="申请人 open_id")
    p_fill.add_argument("--output", default="expense-form.json", help="输出文件")

    # summary
    p_sum = sub.add_parser("summary", help="生成费用汇总")
    p_sum.add_argument("--source", required=True, help="识别结果 JSON 文件")

    args = parser.parse_args()

    if args.cmd == "fill":
        results = load_results(args.source)
        form = fill_feishu_expense(results, args.applicant)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(form, f, ensure_ascii=False, indent=2)
        print(f"[OK] 报销单已生成: {args.output}")
        print(f"     共 {len(form['expense_items'])} 条，合计 ¥{form['total_amount']:.2f}")
        print(f"\n{generate_summary(results)}")

    elif args.cmd == "summary":
        results = load_results(args.source)
        print(generate_summary(results))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
