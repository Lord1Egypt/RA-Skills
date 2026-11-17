#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean.py — 数据清洗
批量执行清洗规则，支持多种内置规则类型，输出清洗报告。
"""

import argparse
import json
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector

import pandas as pd
import numpy as np


SUPPORTED_RULES = [
    "remove_empty_rows",
    "trim_spaces",
    "normalize_phone",
    "normalize_date",
    "normalize_case",
    "fill_empty",
    "remove_duplicates",
    "type_convert",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="批量清洗 Excel 数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的规则类型:
  remove_empty_rows  - 删除全空行
  trim_spaces        - 去除前后空格（可指定列）
  normalize_phone    - 手机号统一 11 位格式（可指定列）
  normalize_date     - 日期统一格式（可指定列和目标格式）
  normalize_case     - 大小写统一（可指定列和目标 upper/lower/title）
  fill_empty         - 填充空值（可指定默认值或 ffill/bfill）
  remove_duplicates  - 简单去重（可指定列）
  type_convert       - 类型转换（可指定列和目标类型 int/float/str）

规则 JSON 格式示例:
  [
    {"type": "remove_empty_rows"},
    {"type": "trim_spaces", "columns": ["姓名", "部门"]},
    {"type": "normalize_phone", "columns": ["手机号"]},
    {"type": "normalize_date", "columns": ["入职日期"], "format": "%Y-%m-%d"},
    {"type": "fill_empty", "columns": ["部门"], "value": "未分配"},
    {"type": "fill_empty", "columns": ["数量"], "method": "ffill"}
  ]

示例:
  # 使用规则文件
  python clean.py data.xlsx -o cleaned.xlsx --rules rules.json

  # 使用内联 JSON 规则
  python clean.py data.xlsx -o cleaned.xlsx --rules '[{"type":"remove_empty_rows"},{"type":"trim_spaces"}]'
        """
    )
    parser.add_argument("input_file", help="输入文件路径")
    parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    parser.add_argument(
        "--rules",
        required=True,
        help="清洗规则 JSON（文件路径或 JSON 字符串）"
    )
    parser.add_argument("--sheet", help="指定读取的 Sheet 名称")
    return parser.parse_args()


def load_rules(rules_arg):
    """加载清洗规则：支持文件路径或内联 JSON"""
    # 尝试作为文件路径
    if os.path.exists(rules_arg):
        with open(rules_arg, "r", encoding="utf-8") as f:
            rules = json.load(f)
    else:
        # 尝试作为 JSON 字符串解析
        try:
            rules = json.loads(rules_arg)
        except json.JSONDecodeError as e:
            print(f"✗ 规则解析失败: {e}")
            print("  请传入有效的 JSON 文件路径或 JSON 字符串")
            sys.exit(1)

    if not isinstance(rules, list):
        print("✗ 规则必须是 JSON 数组格式")
        sys.exit(1)

    # 验证规则类型
    for i, rule in enumerate(rules):
        if "type" not in rule:
            print(f"✗ 第 {i+1} 条规则缺少 'type' 字段")
            sys.exit(1)
        if rule["type"] not in SUPPORTED_RULES:
            print(f"✗ 不支持的规则类型: '{rule['type']}'")
            print(f"  支持的类型: {SUPPORTED_RULES}")
            sys.exit(1)

    return rules


def rule_remove_empty_rows(df, rule):
    """删除全空行"""
    before = len(df)
    df = df.dropna(how="all").reset_index(drop=True)
    affected = before - len(df)
    return df, affected


def rule_trim_spaces(df, rule):
    """去除前后空格"""
    columns = rule.get("columns", None)
    affected = 0

    target_cols = columns if columns else df.select_dtypes(include=["object"]).columns.tolist()

    for col in target_cols:
        if col in df.columns and df[col].dtype == "object":
            original = df[col].copy()
            df[col] = df[col].str.strip()
            changed = (original != df[col]) & original.notna()
            affected += changed.sum()

    return df, affected


def rule_normalize_phone(df, rule):
    """手机号统一 11 位格式"""
    columns = rule.get("columns", None)
    affected = 0

    if not columns:
        # 尝试自动识别手机号列
        columns = [c for c in df.columns if "手机" in c or "电话" in c or "phone" in c.lower()]

    for col in columns:
        if col not in df.columns:
            continue

        original = df[col].copy()

        def normalize_phone_value(val):
            if pd.isna(val):
                return val
            # 转字符串并去除空格、横线、括号
            s = str(val).strip()
            s = re.sub(r'[\s\-\(\)\+]', '', s)
            # 去除国际区号前缀 86
            if s.startswith('86') and len(s) == 13:
                s = s[2:]
            # 去除前缀 0（座机转手机场景）
            if s.startswith('0') and len(s) == 12:
                s = s[1:]
            # 只保留纯数字 11 位的
            if re.match(r'^\d{11}$', s):
                return s
            return str(val)  # 无法规范化的保持原样

        df[col] = df[col].apply(normalize_phone_value)
        changed = (original.astype(str) != df[col].astype(str)) & original.notna()
        affected += changed.sum()

    return df, affected


def rule_normalize_date(df, rule):
    """日期统一格式"""
    columns = rule.get("columns", None)
    target_format = rule.get("format", "%Y-%m-%d")
    affected = 0

    if not columns:
        # 尝试自动识别日期列
        columns = [c for c in df.columns if "日期" in c or "时间" in c or "date" in c.lower()]

    for col in columns:
        if col not in df.columns:
            continue

        original = df[col].copy()
        try:
            # 尝试解析为日期
            parsed = pd.to_datetime(df[col], errors="coerce")
            # 格式化为目标格式
            df[col] = parsed.dt.strftime(target_format)
            # 将 NaT 转换回的 'NaT' 字符串恢复为 NaN
            df[col] = df[col].replace('NaT', np.nan)
            changed = (original.astype(str) != df[col].astype(str)) & original.notna()
            affected += changed.sum()
        except Exception:
            pass

    return df, affected


def rule_normalize_case(df, rule):
    """大小写统一"""
    columns = rule.get("columns", None)
    target = rule.get("target", "lower")  # upper/lower/title
    affected = 0

    if not columns:
        columns = df.select_dtypes(include=["object"]).columns.tolist()

    for col in columns:
        if col not in df.columns or df[col].dtype != "object":
            continue

        original = df[col].copy()
        if target == "upper":
            df[col] = df[col].str.upper()
        elif target == "lower":
            df[col] = df[col].str.lower()
        elif target == "title":
            df[col] = df[col].str.title()

        changed = (original != df[col]) & original.notna()
        affected += changed.sum()

    return df, affected


def rule_fill_empty(df, rule):
    """填充空值"""
    columns = rule.get("columns", None)
    value = rule.get("value", None)
    method = rule.get("method", None)  # ffill/bfill
    affected = 0

    target_cols = columns if columns else df.columns.tolist()

    for col in target_cols:
        if col not in df.columns:
            continue

        empty_count = df[col].isna().sum()
        if empty_count == 0:
            continue

        if method == "ffill":
            df[col] = df[col].ffill()
        elif method == "bfill":
            df[col] = df[col].bfill()
        elif value is not None:
            df[col] = df[col].fillna(value)
        else:
            continue

        # 计算实际填充的数量（某些行可能 ffill/bfill 仍为空）
        new_empty = df[col].isna().sum()
        affected += empty_count - new_empty

    return df, affected


def rule_remove_duplicates(df, rule):
    """简单去重"""
    columns = rule.get("columns", None)
    keep = rule.get("keep", "first")
    before = len(df)

    if columns:
        df = df.drop_duplicates(subset=columns, keep=keep).reset_index(drop=True)
    else:
        df = df.drop_duplicates(keep=keep).reset_index(drop=True)

    affected = before - len(df)
    return df, affected


def rule_type_convert(df, rule):
    """类型转换"""
    columns = rule.get("columns", [])
    target_type = rule.get("target_type", "str")  # int/float/str
    affected = 0

    for col in columns:
        if col not in df.columns:
            continue

        try:
            before_type = df[col].dtype
            if target_type == "int":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            elif target_type == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")
            elif target_type == "str":
                df[col] = df[col].astype(str).replace("nan", np.nan)

            if str(before_type) != str(df[col].dtype):
                affected += len(df[col].dropna())
        except Exception as e:
            print(f"  ⚠️ 列 '{col}' 类型转换失败: {e}")

    return df, affected


# 规则处理器映射
RULE_HANDLERS = {
    "remove_empty_rows": rule_remove_empty_rows,
    "trim_spaces": rule_trim_spaces,
    "normalize_phone": rule_normalize_phone,
    "normalize_date": rule_normalize_date,
    "normalize_case": rule_normalize_case,
    "fill_empty": rule_fill_empty,
    "remove_duplicates": rule_remove_duplicates,
    "type_convert": rule_type_convert,
}


def main():
    args = parse_args()

    # 检查输入文件
    if not os.path.exists(args.input_file):
        print(f"✗ 文件不存在: {args.input_file}")
        sys.exit(1)

    # 加载规则
    rules = load_rules(args.rules)
    print(f"📖 读取文件: {args.input_file}")
    df, _errors = safe_read(args.input_file, sheet_name=args.sheet)
    original_count = len(df)
    print(f"  行数: {original_count}, 列数: {len(df.columns)}")
    print(f"\n🧹 开始清洗（共 {len(rules)} 条规则）...")
    print()

    # 清洗报告
    report = []

    for i, rule in enumerate(rules, 1):
        rule_type = rule["type"]
        handler = RULE_HANDLERS[rule_type]

        before_rows = len(df)
        df, affected = handler(df, rule)
        after_rows = len(df)

        # 构建规则描述
        desc_parts = [rule_type]
        if "columns" in rule:
            desc_parts.append(f"列={rule['columns']}")
        if "format" in rule:
            desc_parts.append(f"格式={rule['format']}")
        if "target" in rule:
            desc_parts.append(f"目标={rule['target']}")
        if "value" in rule:
            desc_parts.append(f"填充值={rule['value']}")
        if "method" in rule:
            desc_parts.append(f"方法={rule['method']}")

        desc = " | ".join(desc_parts)
        row_change = f"（行数: {before_rows} → {after_rows}）" if before_rows != after_rows else ""

        print(f"  [{i}/{len(rules)}] {desc}")
        print(f"         影响: {affected} 处 {row_change}")

        report.append({
            "序号": i,
            "规则": rule_type,
            "详情": desc,
            "影响处数": affected,
            "处理前行数": before_rows,
            "处理后行数": after_rows,
        })

    # 输出结果
    df.to_excel(args.output, index=False)

    # 汇总报告
    print(f"\n{'='*50}")
    print(f"📊 清洗报告汇总:")
    print(f"  原始行数: {original_count}")
    print(f"  清洗后行数: {len(df)}")
    print(f"  删除行数: {original_count - len(df)}")
    total_affected = sum(r["影响处数"] for r in report)
    print(f"  总影响处数: {total_affected}")
    print(f"\n✅ 清洗完成 → {args.output}")


if __name__ == "__main__":
    main()
