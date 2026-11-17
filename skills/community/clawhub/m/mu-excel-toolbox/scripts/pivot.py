#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 数据透视表生成工具
功能：基于 pandas pivot_table 生成数据透视表
支持多行字段、多列字段、多值字段、多聚合函数
输出格式：Excel / Markdown / JSON
"""

import argparse
import os
import sys
import json
from typing import Optional, List

# 添加脚本所在目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("❌ 缺少 pandas/numpy 库，请运行: pip install pandas numpy")
    sys.exit(1)


# 聚合函数映射
AGGFUNC_MAP = {
    'sum': 'sum',
    'mean': 'mean',
    'count': 'count',
    'max': 'max',
    'min': 'min',
    'median': 'median',
    'std': 'std',
    'first': 'first',
    'last': 'last',
}


def parse_aggfunc(aggfunc_str: str):
    """
    解析聚合函数参数
    支持单个函数或多个函数（逗号分隔）
    返回字符串或列表
    """
    funcs = [f.strip().lower() for f in aggfunc_str.split(',')]

    resolved = []
    for f in funcs:
        if f in AGGFUNC_MAP:
            resolved.append(AGGFUNC_MAP[f])
        else:
            raise ValueError(f"不支持的聚合函数: {f}。可用: {list(AGGFUNC_MAP.keys())}")

    if len(resolved) == 1:
        return resolved[0]
    return resolved


def create_pivot(args, collector: ErrorCollector) -> pd.DataFrame:
    """创建数据透视表"""
    # 读取数据
    df, _errors = safe_read(args.input_file)

    if df.empty:
        collector.add_error("输入文件无数据")
        collector.raise_if_errors()

    all_columns = list(df.columns)

    # 解析行字段
    row_fields = [r.strip() for r in args.rows.split(',')] if args.rows else None
    if row_fields:
        for field in row_fields:
            if field not in all_columns:
                collector.add_error(f"行字段 '{field}' 不存在。可用列: {all_columns}")

    # 解析列字段
    col_fields = [c.strip() for c in args.columns.split(',')] if args.columns else None
    if col_fields:
        for field in col_fields:
            if field not in all_columns:
                collector.add_error(f"列字段 '{field}' 不存在。可用列: {all_columns}")

    # 解析值字段
    value_fields = [v.strip() for v in args.values.split(',')] if args.values else None
    if value_fields:
        for field in value_fields:
            if field not in all_columns:
                collector.add_error(f"值字段 '{field}' 不存在。可用列: {all_columns}")

    if collector.has_errors():
        collector.raise_if_errors()

    # 解析聚合函数
    try:
        aggfunc = parse_aggfunc(args.aggfunc) if args.aggfunc else 'mean'
    except ValueError as e:
        collector.add_error(str(e))
        collector.raise_if_errors()

    # 构建 pivot_table 参数
    pivot_kwargs = {
        'data': df,
        'aggfunc': aggfunc,
    }

    if row_fields:
        pivot_kwargs['index'] = row_fields if len(row_fields) > 1 else row_fields[0]
    if col_fields:
        pivot_kwargs['columns'] = col_fields if len(col_fields) > 1 else col_fields[0]
    if value_fields:
        pivot_kwargs['values'] = value_fields if len(value_fields) > 1 else value_fields[0]

    # 填充空值
    if args.fill_value is not None:
        try:
            pivot_kwargs['fill_value'] = float(args.fill_value)
        except ValueError:
            pivot_kwargs['fill_value'] = args.fill_value

    # 汇总行列
    if args.margins:
        pivot_kwargs['margins'] = True
        pivot_kwargs['margins_name'] = '合计'

    # 生成透视表
    try:
        pivot_df = pd.pivot_table(**pivot_kwargs)
    except Exception as e:
        collector.add_error(f"生成透视表失败: {e}")
        collector.raise_if_errors()

    # 排序
    if args.sort_by:
        try:
            if args.sort_by in pivot_df.columns:
                pivot_df = pivot_df.sort_values(by=args.sort_by, ascending=False)
            elif args.sort_by == 'index':
                pivot_df = pivot_df.sort_index()
            else:
                collector.add_warning(f"排序字段 '{args.sort_by}' 不在透视表列中，已跳过排序")
        except Exception as e:
            collector.add_warning(f"排序失败: {e}")

    return pivot_df


def save_output(pivot_df: pd.DataFrame, args, collector: ErrorCollector) -> str:
    """保存透视表输出"""
    output_format = args.format or 'excel'
    output_path = args.output

    if output_format == 'excel':
        if not output_path:
            base = os.path.splitext(args.input_file)[0]
            output_path = f"{base}_pivot.xlsx"
        if not output_path.endswith('.xlsx'):
            output_path += '.xlsx'

        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                pivot_df.to_excel(writer, sheet_name='透视表')

                # 自适应列宽
                ws = writer.sheets['透视表']
                for col_cells in ws.columns:
                    max_length = 0
                    for cell in col_cells:
                        try:
                            val = str(cell.value) if cell.value else ""
                            length = sum(2 if ord(c) > 127 else 1 for c in val)
                            if length > max_length:
                                max_length = length
                        except Exception:
                            pass
                    from openpyxl.utils import get_column_letter
                    col_letter = get_column_letter(col_cells[0].column)
                    ws.column_dimensions[col_letter].width = min(max_length + 2, 40)

        except Exception as e:
            collector.add_error(f"保存 Excel 失败: {e}")
            collector.raise_if_errors()

        return output_path

    elif output_format == 'markdown':
        result = format_output(pivot_df, 'markdown')
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            return output_path
        else:
            print("\n📊 数据透视表:\n")
            print(result)
            return "(标准输出)"

    elif output_format == 'json':
        result = format_output(pivot_df.reset_index(), 'json')
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            return output_path
        else:
            print("\n📊 数据透视表 (JSON):\n")
            print(result)
            return "(标准输出)"

    else:
        collector.add_error(f"不支持的输出格式: {output_format}")
        collector.raise_if_errors()


def main():
    parser = argparse.ArgumentParser(
        description='Excel 数据透视表生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 按部门汇总销售额
  python pivot.py sales.xlsx --rows 部门 --values 销售额 --aggfunc sum

  # 按部门和月份交叉汇总
  python pivot.py sales.xlsx --rows 部门 --columns 月份 --values 销售额 --aggfunc sum

  # 多值字段 + 多聚合函数
  python pivot.py data.xlsx --rows 部门 --values "销售额,利润" --aggfunc "sum,mean"

  # 输出为 Markdown 格式
  python pivot.py data.xlsx --rows 部门 --values 销售额 --aggfunc sum --format markdown

  # 添加汇总行列 + 排序
  python pivot.py data.xlsx --rows 部门 --values 销售额 --aggfunc sum --margins --sort-by 销售额

  # 输出为 JSON
  python pivot.py data.xlsx --rows 部门 --columns 月份 --values 销售额 --format json -o result.json
"""
    )

    parser.add_argument('input_file', help='输入 Excel/CSV 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--rows', help='行字段（逗号分隔支持多字段）')
    parser.add_argument('--columns', help='列字段（逗号分隔支持多字段）')
    parser.add_argument('--values', help='值字段（逗号分隔支持多字段）')
    parser.add_argument('--aggfunc', default='sum',
                        help='聚合函数（sum/mean/count/max/min/median/std，逗号分隔支持多个）')
    parser.add_argument('--fill-value', help='填充空值（默认 NaN）')
    parser.add_argument('--margins', action='store_true', help='添加汇总行列')
    parser.add_argument('--sort-by', help='排序依据（列名或 "index"）')
    parser.add_argument('--format', '-f', choices=['excel', 'markdown', 'json'],
                        default='excel', help='输出格式（默认 excel）')

    args = parser.parse_args()

    # 验证输入
    if not os.path.exists(args.input_file):
        print(f"❌ 文件不存在: {args.input_file}")
        sys.exit(1)

    if not args.rows and not args.columns:
        print("❌ 请至少指定 --rows 或 --columns 参数")
        sys.exit(1)

    if not args.values:
        print("❌ 请指定 --values 参数（值字段）")
        sys.exit(1)

    collector = ErrorCollector()

    try:
        pivot_df = create_pivot(args, collector)
        output_path = save_output(pivot_df, args, collector)
        if output_path != "(标准输出)":
            print(f"✅ 透视表已保存到: {output_path}")
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成透视表失败: {e}")
        sys.exit(1)

    if collector.has_warnings():
        print(collector.report())


if __name__ == "__main__":
    main()
