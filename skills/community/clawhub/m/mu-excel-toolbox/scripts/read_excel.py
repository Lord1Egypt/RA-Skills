#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 工具箱 — 读取 Excel
灵活读取 Excel 数据，支持范围选取、条件筛选、多种输出格式。
"""

import argparse
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    detect_file_type,
    ensure_dependencies,
    safe_read,
    format_output,
    is_large_file,
    ErrorCollector,
)


def parse_range(range_str):
    """解析 Excel 范围字符串（如 A1:D100）。

    Args:
        range_str: Excel 范围表达式

    Returns:
        tuple: (start_col, start_row, end_col, end_row)，列为0-based索引，行为1-based
    """
    match = re.match(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", range_str.upper())
    if not match:
        raise ValueError(f"无效的范围格式: {range_str}，应为如 A1:D100")

    start_col = _col_to_idx(match.group(1))
    start_row = int(match.group(2))
    end_col = _col_to_idx(match.group(3))
    end_row = int(match.group(4))

    return start_col, start_row, end_col, end_row


def _col_to_idx(col_str):
    """将列字母转为 0-based 索引（A=0, B=1, ..., Z=25, AA=26）。"""
    result = 0
    for char in col_str:
        result = result * 26 + (ord(char) - ord("A") + 1)
    return result - 1


def parse_filter(filter_str):
    """解析筛选条件字符串。

    支持的操作符: ==, !=, >, <, >=, <=, contains, startswith, endswith

    Args:
        filter_str: 如 "年龄 > 30" 或 "姓名 contains 张"

    Returns:
        tuple: (column_name, operator, value)
    """
    # 支持的操作符（按长度排序避免前缀匹配错误）
    operators = [">=", "<=", "!=", "==", ">", "<", "contains", "startswith", "endswith"]

    for op in operators:
        # 使用空格分割
        parts = filter_str.split(f" {op} ", 1)
        if len(parts) == 2:
            col_name = parts[0].strip()
            value = parts[1].strip()
            # 尝试转为数字
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    # 去除引号
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
            return col_name, op, value

    raise ValueError(f"无法解析筛选条件: {filter_str}\n支持的操作符: {', '.join(operators)}")


def apply_filter(df, col_name, operator, value):
    """对 DataFrame 应用筛选条件。

    Args:
        df: pandas DataFrame
        col_name: 列名
        operator: 操作符
        value: 比较值

    Returns:
        DataFrame: 筛选后的数据
    """
    if col_name not in df.columns:
        raise ValueError(f"列 '{col_name}' 不存在。可用列: {', '.join(df.columns)}")

    col = df[col_name]

    if operator == "==":
        mask = col == value
    elif operator == "!=":
        mask = col != value
    elif operator == ">":
        mask = col > value
    elif operator == "<":
        mask = col < value
    elif operator == ">=":
        mask = col >= value
    elif operator == "<=":
        mask = col <= value
    elif operator == "contains":
        mask = col.astype(str).str.contains(str(value), na=False)
    elif operator == "startswith":
        mask = col.astype(str).str.startswith(str(value), na=False)
    elif operator == "endswith":
        mask = col.astype(str).str.endswith(str(value), na=False)
    else:
        raise ValueError(f"不支持的操作符: {operator}")

    return df[mask]


def read_with_range(path, sheet_name=None, range_str=None, columns=None,
                    row_range=None, header_row=0, filters=None, nrows=None):
    """读取 Excel 文件，支持范围选取和条件筛选。

    Args:
        path: 文件路径
        sheet_name: Sheet 名称或索引
        range_str: Excel 范围（如 A1:D100）
        columns: 列名列表
        row_range: 行范围字符串（如 "1-100"）
        header_row: 表头行号（0-based）
        filters: 筛选条件列表
        nrows: 最大读取行数

    Returns:
        tuple: (DataFrame, ErrorCollector)
    """
    import pandas as pd

    errors = ErrorCollector()

    # 构建读取参数
    read_kwargs = {}
    if sheet_name is not None:
        # 尝试将 sheet_name 解析为数字索引
        try:
            read_kwargs["sheet_name"] = int(sheet_name)
        except (ValueError, TypeError):
            read_kwargs["sheet_name"] = sheet_name

    if header_row is not None:
        read_kwargs["header"] = header_row

    if nrows is not None:
        read_kwargs["nrows"] = nrows

    # 如果指定了范围，解析列
    usecols = None
    skiprows = None
    if range_str:
        start_col, start_row, end_col, end_row = parse_range(range_str)
        usecols = list(range(start_col, end_col + 1))
        read_kwargs["usecols"] = usecols
        # 调整 skiprows 和 nrows
        if start_row > 1:
            # skiprows 跳过前面的行（但保留表头）
            actual_skip = start_row - 1 - header_row
            if actual_skip > 0:
                read_kwargs["skiprows"] = list(range(header_row + 1, start_row))
        read_kwargs["nrows"] = end_row - start_row + 1

    # 安全读取
    df, read_errors = safe_read(path, **read_kwargs)
    errors._errors.extend(read_errors._errors)
    errors._warnings.extend(read_errors._warnings)

    # 选择指定列
    if columns:
        available_cols = list(df.columns)
        valid_cols = []
        for col in columns:
            if col in available_cols:
                valid_cols.append(col)
            else:
                errors.add_warning(f"列 '{col}' 不存在，已跳过")
        if valid_cols:
            df = df[valid_cols]

    # 行范围筛选
    if row_range:
        try:
            parts = row_range.split("-")
            start = int(parts[0]) - 1  # 转为 0-based
            end = int(parts[1]) if len(parts) > 1 else start + 1
            df = df.iloc[start:end]
        except (ValueError, IndexError):
            errors.add_warning(f"行范围 '{row_range}' 格式错误，已忽略")

    # 应用筛选条件
    if filters:
        for filter_str in filters:
            try:
                col_name, op, value = parse_filter(filter_str)
                df = apply_filter(df, col_name, op, value)
            except ValueError as e:
                errors.add_error(str(e))

    return df, errors


def main():
    parser = argparse.ArgumentParser(
        description="灵活读取 Excel/CSV 数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python read_excel.py data.xlsx
  python read_excel.py data.xlsx --sheet "销售数据" --format json
  python read_excel.py data.xlsx --range A1:D100
  python read_excel.py data.xlsx --columns 姓名 年龄 部门
  python read_excel.py data.xlsx --filter "年龄 > 30"
  python read_excel.py data.xlsx --filter "部门 contains 技术" --format csv
        """,
    )
    parser.add_argument("input_file", help="要读取的文件路径")
    parser.add_argument("--sheet", "-s", help="Sheet 名称或索引（默认第一个）")
    parser.add_argument("--range", "-r", help="读取范围（如 A1:D100）")
    parser.add_argument("--columns", "-c", nargs="+", help="要读取的列名列表")
    parser.add_argument("--rows", help="行范围（如 1-100）")
    parser.add_argument("--format", "-f", choices=["json", "csv", "markdown", "table", "tsv"],
                        default="table", help="输出格式（默认: table）")
    parser.add_argument("--header-row", type=int, default=0, help="表头行号，0-based（默认: 0）")
    parser.add_argument("--filter", dest="filters", action="append",
                        help="筛选条件（可多次使用），如 \"年龄 > 30\"")
    parser.add_argument("--nrows", "-n", type=int, help="最大读取行数")

    args = parser.parse_args()

    # 检查依赖
    missing = ensure_dependencies()
    if missing:
        sys.exit(1)

    # 检查文件
    path = Path(args.input_file)
    if not path.exists():
        print(f"❌ 文件不存在: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        df, errors = read_with_range(
            path,
            sheet_name=args.sheet,
            range_str=args.range,
            columns=args.columns,
            row_range=args.rows,
            header_row=args.header_row,
            filters=args.filters,
            nrows=args.nrows,
        )

        # 输出结果
        output = format_output(df, args.format)
        print(output)

        # 输出统计信息
        print(f"\n📊 共 {len(df)} 行 × {len(df.columns)} 列", file=sys.stderr)

        # 输出错误/警告
        if errors.has_issues():
            print(f"\n{errors.report()}", file=sys.stderr)

    except Exception as e:
        print(f"❌ 读取失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
