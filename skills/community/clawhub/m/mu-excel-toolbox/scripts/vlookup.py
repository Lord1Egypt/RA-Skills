#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vlookup.py — 多表关联
跨文件/跨 Sheet 按关键列匹配合并数据，类似 Excel 的 VLOOKUP 功能。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="跨文件/跨 Sheet 按关键列匹配合并（类似 VLOOKUP）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 用工号关联花名册和考勤表，拉取"出勤天数"列
  python vlookup.py --main 花名册.xlsx --lookup 考勤表.xlsx --key 工号 --columns 出勤天数 -o result.xlsx

  # 多列关联，inner join
  python vlookup.py --main main.xlsx --lookup ref.xlsx --key 工号 --columns 部门 职级 --how inner -o result.xlsx

  # 指定 Sheet
  python vlookup.py --main data.xlsx --lookup data.xlsx --key ID --columns 分数 --main-sheet 学生 --lookup-sheet 成绩 -o result.xlsx
        """
    )
    parser.add_argument("--main", required=True, help="主表文件路径")
    parser.add_argument("--lookup", required=True, help="查找表文件路径")
    parser.add_argument("--key", required=True, help="关联列名（两张表中必须同名）")
    parser.add_argument(
        "--columns",
        nargs="+",
        required=True,
        help="要从查找表匹配过来的列名（一个或多个）"
    )
    parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    parser.add_argument(
        "--how",
        choices=["left", "inner", "outer"],
        default="left",
        help="关联方式: left=保留主表全部, inner=仅匹配行, outer=保留全部（默认: left）"
    )
    parser.add_argument("--main-sheet", help="主表的 Sheet 名称")
    parser.add_argument("--lookup-sheet", help="查找表的 Sheet 名称")
    return parser.parse_args()


def check_key_duplicates(df, key, table_name):
    """检查关联列是否有重复值，给出提示"""
    dup_count = df[key].duplicated().sum()
    if dup_count > 0:
        total = len(df)
        unique = df[key].nunique()
        print(f"  ⚠️ {table_name}中关联列 '{key}' 存在重复值:")
        print(f"     总行数={total}, 唯一值={unique}, 重复行={dup_count}")
        # 展示前几个重复值
        dup_values = df[df[key].duplicated(keep=False)][key].value_counts().head(5)
        for val, count in dup_values.items():
            print(f"     '{val}' 出现 {count} 次")
        return True
    return False


def main():
    args = parse_args()

    # 检查文件
    if not os.path.exists(args.main):
        print(f"✗ 主表文件不存在: {args.main}")
        sys.exit(1)
    if not os.path.exists(args.lookup):
        print(f"✗ 查找表文件不存在: {args.lookup}")
        sys.exit(1)

    # 读取数据
    print("📖 读取数据...")
    main_df, _err1 = safe_read(args.main, sheet_name=args.main_sheet)
    lookup_df, _err2 = safe_read(args.lookup, sheet_name=args.lookup_sheet)

    print(f"  主表: {len(main_df)} 行 × {len(main_df.columns)} 列")
    print(f"  查找表: {len(lookup_df)} 行 × {len(lookup_df.columns)} 列")
    print()

    # 检查关联列是否存在
    if args.key not in main_df.columns:
        available = ", ".join(main_df.columns.tolist())
        print(f"✗ 主表中不存在列 '{args.key}'。可用列: {available}")
        sys.exit(1)
    if args.key not in lookup_df.columns:
        available = ", ".join(lookup_df.columns.tolist())
        print(f"✗ 查找表中不存在列 '{args.key}'。可用列: {available}")
        sys.exit(1)

    # 检查要匹配的列是否存在于查找表
    missing_cols = [c for c in args.columns if c not in lookup_df.columns]
    if missing_cols:
        available = ", ".join(lookup_df.columns.tolist())
        print(f"✗ 查找表中不存在以下列: {missing_cols}")
        print(f"  可用列: {available}")
        sys.exit(1)

    # 检查重复值情况
    print("🔍 检查关联列...")
    main_has_dup = check_key_duplicates(main_df, args.key, "主表")
    lookup_has_dup = check_key_duplicates(lookup_df, args.key, "查找表")

    if main_has_dup and lookup_has_dup:
        print("  ⚠️ 两张表的关联列都有重复值，结果可能出现多对多笛卡尔积，请注意核查")
    elif lookup_has_dup:
        print("  ⚠️ 查找表关联列有重复值，主表每行可能匹配多行（一对多）")
    print()

    # 准备查找表：只保留关联列和要匹配的列
    lookup_cols = [args.key] + args.columns
    lookup_subset = lookup_df[lookup_cols]

    # 执行关联
    print(f"🔗 执行关联 (how={args.how})...")
    result = main_df.merge(lookup_subset, on=args.key, how=args.how, suffixes=('', '_lookup'))

    # 统计匹配情况
    if args.how == "left":
        # 检查有多少行没匹配到
        matched = result[args.columns[0]].notna().sum()
        unmatched = len(result) - matched
        print(f"  匹配成功: {matched} 行")
        if unmatched > 0:
            print(f"  未匹配（空值）: {unmatched} 行")

    # 输出结果
    result.to_excel(args.output, index=False)
    print(f"\n✅ 关联完成: {len(result)} 行 × {len(result.columns)} 列 → {args.output}")

    # 行数变化提示
    if len(result) > len(main_df):
        print(f"  ℹ️ 结果行数({len(result)}) > 主表行数({len(main_df)})，"
              f"可能因为查找表中有重复的关联键")
    elif len(result) < len(main_df):
        print(f"  ℹ️ 结果行数({len(result)}) < 主表行数({len(main_df)})，"
              f"inner join 过滤了未匹配的行")


if __name__ == "__main__":
    main()
