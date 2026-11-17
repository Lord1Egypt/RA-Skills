#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedup.py — 去重
按指定列去重，支持保留策略和去重报告输出。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="按指定列去重",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 按姓名+手机号去重，保留第一条
  python dedup.py data.xlsx --columns 姓名 手机号 --keep first -o deduped.xlsx

  # 去重并输出被删除的重复行报告
  python dedup.py data.xlsx --columns 邮箱 --keep last -o deduped.xlsx --report duplicates.xlsx

  # 删除所有重复行（不保留任何一条）
  python dedup.py data.xlsx --columns ID --keep none -o deduped.xlsx
        """
    )
    parser.add_argument("input_file", help="输入文件路径")
    parser.add_argument(
        "--columns",
        nargs="+",
        required=True,
        help="去重依据列（一个或多个）"
    )
    parser.add_argument(
        "--keep",
        choices=["first", "last", "none"],
        default="first",
        help="保留策略: first=保留首条, last=保留末条, none=全部删除（默认: first）"
    )
    parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    parser.add_argument(
        "--report",
        help="输出去重报告文件路径（被删除的重复行）"
    )
    parser.add_argument("--sheet", help="指定读取的 Sheet 名称")
    return parser.parse_args()


def main():
    args = parse_args()

    # 检查输入文件
    if not os.path.exists(args.input_file):
        print(f"✗ 文件不存在: {args.input_file}")
        sys.exit(1)

    # 读取数据
    print(f"📖 读取文件: {args.input_file}")
    df, _errors = safe_read(args.input_file, sheet_name=args.sheet)
    original_count = len(df)
    print(f"  原始行数: {original_count}")
    print(f"  去重依据列: {args.columns}")
    print(f"  保留策略: {args.keep}")
    print()

    # 检查列是否存在
    missing_cols = [c for c in args.columns if c not in df.columns]
    if missing_cols:
        available = ", ".join(df.columns.tolist())
        print(f"✗ 以下列不存在: {missing_cols}")
        print(f"  可用列: {available}")
        sys.exit(1)

    # 找出重复行
    duplicated_mask = df.duplicated(subset=args.columns, keep=False)
    total_duplicated = duplicated_mask.sum()

    if total_duplicated == 0:
        print("ℹ️ 没有发现重复行，数据已是唯一的")
        df.to_excel(args.output, index=False)
        print(f"\n✅ 输出文件（无变化）: {args.output}")
        return

    # 统计重复组数
    dup_groups = df[duplicated_mask].groupby(args.columns).ngroups
    print(f"🔍 发现 {total_duplicated} 行重复数据，分属 {dup_groups} 组")

    # 执行去重
    if args.keep == "none":
        # 删除所有重复行
        result = df[~duplicated_mask]
        removed = df[duplicated_mask]
    else:
        # 标记要保留的行
        kept_mask = ~df.duplicated(subset=args.columns, keep=args.keep)
        result = df[kept_mask]
        # 被删除的行 = 重复行中未被保留的
        removed = df[~kept_mask & duplicated_mask]

    removed_count = original_count - len(result)

    print(f"\n📊 去重结果:")
    print(f"  原始行数: {original_count}")
    print(f"  去重后行数: {len(result)}")
    print(f"  删除行数: {removed_count}")
    print(f"  去重率: {removed_count / original_count * 100:.1f}%")

    # 输出结果
    result.to_excel(args.output, index=False)
    print(f"\n✅ 去重完成 → {args.output}")

    # 输出去重报告
    if args.report and len(removed) > 0:
        removed.to_excel(args.report, index=False)
        print(f"📋 去重报告（被删除的行）→ {args.report} ({len(removed)} 行)")

        # 打印前几组重复的摘要
        print(f"\n📊 重复数据摘要（前5组）:")
        dup_summary = df[duplicated_mask].groupby(args.columns).size().reset_index(name='重复次数')
        dup_summary = dup_summary.sort_values('重复次数', ascending=False).head(5)
        for _, row in dup_summary.iterrows():
            keys = " | ".join([f"{col}='{row[col]}'" for col in args.columns])
            print(f"  {keys} → 重复 {row['重复次数']} 次")


if __name__ == "__main__":
    main()
