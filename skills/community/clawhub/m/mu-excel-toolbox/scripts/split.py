#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split.py — 拆分文件
按 Sheet 拆分或按列值拆分 Excel 文件为多个独立文件。
"""

import argparse
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="按 Sheet 或按列值拆分 Excel 文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 按 Sheet 拆分
  python split.py data.xlsx --output-dir ./output --mode by-sheet

  # 按"部门"列拆分
  python split.py data.xlsx --output-dir ./output --mode by-column --column 部门

  # 自定义输出文件命名
  python split.py data.xlsx --output-dir ./output --mode by-column --column 部门 --naming "{value}_数据"
        """
    )
    parser.add_argument("input_file", help="输入文件路径")
    parser.add_argument("--output-dir", required=True, help="输出目录路径")
    parser.add_argument(
        "--mode",
        choices=["by-sheet", "by-column"],
        default="by-sheet",
        help="拆分模式: by-sheet=按Sheet拆分, by-column=按列值拆分（默认: by-sheet）"
    )
    parser.add_argument("--column", help="按哪列拆分（by-column 模式必需）")
    parser.add_argument(
        "--naming",
        default="{value}",
        help="输出文件命名规则，{value}会被替换为列值或Sheet名（默认: {value}）"
    )
    parser.add_argument("--sheet", help="指定读取的 Sheet（by-column 模式可用）")
    return parser.parse_args()


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    name = str(name).strip()
    # 替换文件名非法字符
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    # 去除前后空格和点
    name = name.strip('. ')
    return name if name else "未命名"


def split_by_sheet(input_file, output_dir, naming):
    """按 Sheet 拆分文件"""
    file_type = detect_file_type(input_file)
    if file_type == "csv":
        print("✗ CSV 文件不支持按 Sheet 拆分（只有一个数据表）")
        sys.exit(1)

    xls = pd.ExcelFile(input_file)
    sheet_names = xls.sheet_names
    print(f"📋 文件包含 {len(sheet_names)} 个 Sheet: {sheet_names}")
    print()

    created_files = []
    for sn in sheet_names:
        df = pd.read_excel(xls, sheet_name=sn)
        filename = sanitize_filename(naming.format(value=sn))
        output_path = os.path.join(output_dir, f"{filename}.xlsx")
        df.to_excel(output_path, index=False)
        created_files.append(output_path)
        print(f"  ✓ Sheet '{sn}' → {output_path} ({len(df)} 行)")

    return created_files


def split_by_column(input_file, output_dir, column, naming, sheet_name):
    """按列值拆分文件"""
    df, _errors = safe_read(input_file, sheet_name=sheet_name if sheet_name else None)

    if column not in df.columns:
        available = ", ".join(df.columns.tolist())
        print(f"✗ 列 '{column}' 不存在。可用列: {available}")
        sys.exit(1)

    # 获取唯一值
    unique_values = df[column].dropna().unique()
    # 检查是否有空值行
    null_rows = df[df[column].isna()]

    print(f"📊 按列 '{column}' 拆分，共 {len(unique_values)} 个唯一值")
    if len(null_rows) > 0:
        print(f"  ⚠️ 有 {len(null_rows)} 行该列为空值，将合并到 '未分类' 文件中")
    print()

    created_files = []

    for value in sorted(unique_values, key=str):
        subset = df[df[column] == value]
        filename = sanitize_filename(naming.format(value=value))
        output_path = os.path.join(output_dir, f"{filename}.xlsx")
        subset.to_excel(output_path, index=False)
        created_files.append(output_path)
        print(f"  ✓ {column}='{value}' → {output_path} ({len(subset)} 行)")

    # 处理空值行
    if len(null_rows) > 0:
        filename = sanitize_filename(naming.format(value="未分类"))
        output_path = os.path.join(output_dir, f"{filename}.xlsx")
        null_rows.to_excel(output_path, index=False)
        created_files.append(output_path)
        print(f"  ✓ {column}=空值 → {output_path} ({len(null_rows)} 行)")

    return created_files


def main():
    args = parse_args()

    # 检查输入文件
    if not os.path.exists(args.input_file):
        print(f"✗ 文件不存在: {args.input_file}")
        sys.exit(1)

    # by-column 模式必须指定列
    if args.mode == "by-column" and not args.column:
        print("✗ by-column 模式必须指定 --column 参数")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"📁 拆分模式: {args.mode}")
    print(f"📄 输入文件: {args.input_file}")
    print(f"📂 输出目录: {args.output_dir}")
    print()

    if args.mode == "by-sheet":
        created_files = split_by_sheet(args.input_file, args.output_dir, args.naming)
    elif args.mode == "by-column":
        created_files = split_by_column(
            args.input_file, args.output_dir, args.column, args.naming, args.sheet
        )

    print(f"\n✅ 拆分完成，共生成 {len(created_files)} 个文件")


if __name__ == "__main__":
    main()
