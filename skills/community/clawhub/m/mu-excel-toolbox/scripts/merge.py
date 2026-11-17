#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge.py — 合并文件/Sheet
将多个 Excel 文件或 Sheet 合并为一个文件。
支持纵向合并(concat)、横向合并(horizontal)、按Sheet合并(by-sheet)。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="合并多个 Excel 文件或 Sheet 为一个文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 纵向合并多个文件
  python merge.py file1.xlsx file2.xlsx file3.xlsx -o merged.xlsx

  # 横向合并（按列拼接）
  python merge.py file1.xlsx file2.xlsx -o merged.xlsx --mode horizontal

  # 合并同一文件的多个 Sheet
  python merge.py data.xlsx -o merged.xlsx --mode by-sheet

  # 第二个文件起跳过表头
  python merge.py file1.xlsx file2.xlsx -o merged.xlsx --ignore-headers
        """
    )
    parser.add_argument("input_files", nargs="+", help="输入文件路径（一个或多个）")
    parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    parser.add_argument(
        "--mode",
        choices=["concat", "horizontal", "by-sheet"],
        default="concat",
        help="合并模式: concat=纵向合并, horizontal=横向合并, by-sheet=按Sheet合并（默认: concat）"
    )
    parser.add_argument("--sheet", help="指定读取的 Sheet 名称（仅 concat/horizontal 模式有效）")
    parser.add_argument(
        "--ignore-headers",
        action="store_true",
        help="第二个文件起跳过表头（仅 concat 模式有效）"
    )
    return parser.parse_args()


def merge_concat(input_files, sheet_name, ignore_headers):
    """纵向合并：将多个文件的数据上下拼接"""
    frames = []
    errors = ErrorCollector()

    for i, filepath in enumerate(input_files):
        try:
            df, _err = safe_read(filepath, sheet_name=sheet_name)
            if ignore_headers and i > 0 and len(frames) > 0:
                # 用第一个文件的列名覆盖后续文件
                if len(df.columns) == len(frames[0].columns):
                    df.columns = frames[0].columns
                else:
                    # 列数不同时，自动对齐
                    pass
            frames.append(df)
            print(f"  ✓ 读取 {filepath}: {len(df)} 行 × {len(df.columns)} 列")
        except Exception as e:
            errors.add_error(f"{filepath}: {e}")

    if errors.has_errors():
        print(errors.report(), file=sys.stderr)

    if not frames:
        print("✗ 没有成功读取任何文件，无法合并")
        sys.exit(1)

    # 使用 concat 自动对齐不同列数的文件
    result = pd.concat(frames, ignore_index=True, sort=False)
    return result


def merge_horizontal(input_files, sheet_name):
    """横向合并：将多个文件的数据左右拼接"""
    frames = []
    errors = ErrorCollector()

    for filepath in input_files:
        try:
            df, _err = safe_read(filepath, sheet_name=sheet_name)
            frames.append(df)
            print(f"  ✓ 读取 {filepath}: {len(df)} 行 × {len(df.columns)} 列")
        except Exception as e:
            errors.add_error(f"{filepath}: {e}")

    if errors.has_errors():
        print(errors.report(), file=sys.stderr)

    if not frames:
        print("✗ 没有成功读取任何文件，无法合并")
        sys.exit(1)

    result = pd.concat(frames, axis=1, sort=False)
    return result


def merge_by_sheet(input_files):
    """按 Sheet 合并：将同一文件的所有 Sheet 纵向合并"""
    frames = []
    errors = ErrorCollector()

    for filepath in input_files:
        try:
            file_type = detect_file_type(filepath)
            if file_type == "csv":
                df, _err = safe_read(filepath)
                frames.append(df)
                print(f"  ✓ 读取 {filepath} (CSV): {len(df)} 行")
            else:
                xls = pd.ExcelFile(filepath)
                sheet_names = xls.sheet_names
                print(f"  📋 文件 {filepath} 包含 {len(sheet_names)} 个 Sheet: {sheet_names}")
                for sn in sheet_names:
                    df = pd.read_excel(xls, sheet_name=sn)
                    frames.append(df)
                    print(f"    ✓ Sheet '{sn}': {len(df)} 行 × {len(df.columns)} 列")
        except Exception as e:
            errors.add_error(f"{filepath}: {e}")

    if errors.has_errors():
        print(errors.report(), file=sys.stderr)

    if not frames:
        print("✗ 没有成功读取任何 Sheet，无法合并")
        sys.exit(1)

    result = pd.concat(frames, ignore_index=True, sort=False)
    return result


def main():
    args = parse_args()

    # 检查输入文件是否存在
    for f in args.input_files:
        if not os.path.exists(f):
            print(f"✗ 文件不存在: {f}")
            sys.exit(1)

    print(f"📁 合并模式: {args.mode}")
    print(f"📄 输入文件: {len(args.input_files)} 个")
    print()

    if args.mode == "concat":
        result = merge_concat(args.input_files, args.sheet, args.ignore_headers)
    elif args.mode == "horizontal":
        result = merge_horizontal(args.input_files, args.sheet)
    elif args.mode == "by-sheet":
        result = merge_by_sheet(args.input_files)
    else:
        print(f"✗ 不支持的合并模式: {args.mode}")
        sys.exit(1)

    # 输出结果
    result.to_excel(args.output, index=False)
    print(f"\n✅ 合并完成: {len(result)} 行 × {len(result.columns)} 列 → {args.output}")


if __name__ == "__main__":
    main()
