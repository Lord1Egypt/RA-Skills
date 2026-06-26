#!/usr/bin/env python3
"""
Data Transformer - Pandas数据转换工具
数据格式转换、聚合、透视表等操作
"""

import pandas as pd
import argparse
import sys
from pathlib import Path


def load_data(file_path: str) -> pd.DataFrame:
    """加载数据文件"""
    file_path = Path(file_path)
    
    if file_path.suffix == '.csv':
        return pd.read_csv(file_path)
    elif file_path.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    elif file_path.suffix == '.json':
        return pd.read_json(file_path)
    elif file_path.suffix == '.parquet':
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {file_path.suffix}")


def save_data(df: pd.DataFrame, output_path: str):
    """保存数据"""
    output_path = Path(output_path)
    
    if output_path.suffix == '.csv':
        df.to_csv(output_path, index=False)
    elif output_path.suffix in ['.xlsx', '.xls']:
        df.to_excel(output_path, index=False)
    elif output_path.suffix == '.json':
        df.to_json(output_path, orient='records', indent=2)
    elif output_path.suffix == '.parquet':
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == '.html':
        df.to_html(output_path, index=False)
    else:
        raise ValueError(f"不支持的输出格式: {output_path.suffix}")
    
    print(f"数据已保存到: {output_path}")


def convert_format(input_path: str, output_path: str):
    """格式转换"""
    df = load_data(input_path)
    print(f"转换: {Path(input_path).suffix} → {Path(output_path).suffix}")
    print(f"数据: {len(df)} 行, {len(df.columns)} 列")
    save_data(df, output_path)


def aggregate_data(df: pd.DataFrame, group_by: list, agg_dict: dict) -> pd.DataFrame:
    """聚合数据"""
    return df.groupby(group_by).agg(agg_dict).reset_index()


def pivot_table(df: pd.DataFrame, values: str, index: str, columns: str, aggfunc: str = 'sum') -> pd.DataFrame:
    """创建透视表"""
    return pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc=aggfunc, fill_value=0)


def merge_files(file_paths: list, how: str = 'outer', on: str = None) -> pd.DataFrame:
    """合并多个文件"""
    dfs = [load_data(path) for path in file_paths]
    
    if on:
        result = dfs[0]
        for df in dfs[1:]:
            result = pd.merge(result, df, how=how, on=on)
    else:
        # 按行拼接
        result = pd.concat(dfs, ignore_index=True)
    
    return result


def filter_data(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """使用query过滤数据"""
    return df.query(query)


def sort_data(df: pd.DataFrame, by: list, ascending: bool = True) -> pd.DataFrame:
    """排序数据"""
    return df.sort_values(by=by, ascending=ascending)


def select_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """选择指定列"""
    return df[columns]


def main():
    parser = argparse.ArgumentParser(description='Pandas数据转换工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 格式转换
    convert_parser = subparsers.add_parser('convert', help='格式转换')
    convert_parser.add_argument('input', help='输入文件')
    convert_parser.add_argument('output', help='输出文件')
    
    # 合并文件
    merge_parser = subparsers.add_parser('merge', help='合并文件')
    merge_parser.add_argument('files', nargs='+', help='要合并的文件列表')
    merge_parser.add_argument('--output', '-o', required=True, help='输出文件')
    merge_parser.add_argument('--how', choices=['inner', 'outer', 'left', 'right'], default='outer')
    merge_parser.add_argument('--on', help='合并键列名')
    
    # 过滤数据
    filter_parser = subparsers.add_parser('filter', help='过滤数据')
    filter_parser.add_argument('input', help='输入文件')
    filter_parser.add_argument('--query', '-q', required=True, help='过滤条件(pandas query语法)')
    filter_parser.add_argument('--output', '-o', required=True, help='输出文件')
    
    # 排序数据
    sort_parser = subparsers.add_parser('sort', help='排序数据')
    sort_parser.add_argument('input', help='输入文件')
    sort_parser.add_argument('--by', '-b', required=True, nargs='+', help='排序列名')
    sort_parser.add_argument('--descending', action='store_true', help='降序排序')
    sort_parser.add_argument('--output', '-o', required=True, help='输出文件')
    
    # 选择列
    select_parser = subparsers.add_parser('select', help='选择列')
    select_parser.add_argument('input', help='输入文件')
    select_parser.add_argument('--columns', '-c', required=True, nargs='+', help='要选择的列名')
    select_parser.add_argument('--output', '-o', required=True, help='输出文件')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'convert':
            convert_format(args.input, args.output)
        
        elif args.command == 'merge':
            print(f"合并 {len(args.files)} 个文件...")
            df = merge_files(args.files, how=args.how, on=args.on)
            print(f"合并后: {len(df)} 行, {len(df.columns)} 列")
            save_data(df, args.output)
        
        elif args.command == 'filter':
            df = load_data(args.input)
            print(f"原始数据: {len(df)} 行")
            df = filter_data(df, args.query)
            print(f"过滤后: {len(df)} 行")
            save_data(df, args.output)
        
        elif args.command == 'sort':
            df = load_data(args.input)
            df = sort_data(df, by=args.by, ascending=not args.descending)
            print(f"按 {', '.join(args.by)} {'降序' if args.descending else '升序'}排序")
            save_data(df, args.output)
        
        elif args.command == 'select':
            df = load_data(args.input)
            print(f"原始列: {len(df.columns)} 列")
            df = select_columns(df, args.columns)
            print(f"选择列: {len(df.columns)} 列")
            save_data(df, args.output)
        
        else:
            parser.print_help()
            sys.exit(1)
        
        print("\n✓ 数据转换完成!")
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
