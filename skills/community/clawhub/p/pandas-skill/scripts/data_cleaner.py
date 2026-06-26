#!/usr/bin/env python3
"""
Data Cleaner - Pandas数据清洗工具
处理常见的数据清洗任务：缺失值、重复值、异常值等
"""

import pandas as pd
import numpy as np
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


def remove_duplicates(df: pd.DataFrame, subset=None, keep='first') -> pd.DataFrame:
    """删除重复行"""
    before_count = len(df)
    df = df.drop_duplicates(subset=subset, keep=keep)
    after_count = len(df)
    print(f"删除了 {before_count - after_count} 行重复数据")
    return df


def handle_missing_values(df: pd.DataFrame, strategy='drop', fill_value=None) -> pd.DataFrame:
    """处理缺失值
    
    Args:
        strategy: 'drop', 'fill', 'forward', 'backward', 'mean', 'median'
        fill_value: 当strategy='fill'时使用的填充值
    """
    if strategy == 'drop':
        df = df.dropna()
    elif strategy == 'fill':
        df = df.fillna(fill_value)
    elif strategy == 'forward':
        df = df.fillna(method='ffill')
    elif strategy == 'backward':
        df = df.fillna(method='bfill')
    elif strategy == 'mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == 'median':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    return df


def remove_outliers(df: pd.DataFrame, columns=None, method='iqr', threshold=1.5) -> pd.DataFrame:
    """移除异常值
    
    Args:
        columns: 要检查的列名列表，None表示所有数值列
        method: 'iqr' (四分位距法) 或 'zscore' (标准分数法)
        threshold: IQR方法的倍数(默认1.5)或Z-score的阈值(默认3)
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    before_count = len(df)
    
    if method == 'iqr':
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    elif method == 'zscore':
        for col in columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            df = df[z_scores < threshold]
    
    after_count = len(df)
    print(f"移除了 {before_count - after_count} 行异常值")
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """标准化列名：小写、去空格、下划线分隔"""
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
    return df


def convert_dtypes(df: pd.DataFrame, conversions: dict) -> pd.DataFrame:
    """转换数据类型
    
    Args:
        conversions: {column_name: dtype} 字典
    """
    for col, dtype in conversions.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)
    return df


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
    else:
        raise ValueError(f"不支持的输出格式: {output_path.suffix}")
    
    print(f"数据已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Pandas数据清洗工具')
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('output', help='输出文件路径')
    parser.add_argument('--remove-duplicates', action='store_true', help='删除重复行')
    parser.add_argument('--handle-missing', choices=['drop', 'fill', 'forward', 'backward', 'mean', 'median'],
                        help='缺失值处理策略')
    parser.add_argument('--fill-value', help='缺失值填充值')
    parser.add_argument('--remove-outliers', action='store_true', help='移除异常值')
    parser.add_argument('--outlier-method', choices=['iqr', 'zscore'], default='iqr', help='异常值检测方法')
    parser.add_argument('--standardize-columns', action='store_true', help='标准化列名')
    
    args = parser.parse_args()
    
    try:
        # 加载数据
        print(f"加载数据: {args.input}")
        df = load_data(args.input)
        print(f"原始数据: {len(df)} 行, {len(df.columns)} 列")
        
        # 应用清洗操作
        if args.standardize_columns:
            df = standardize_columns(df)
            print("列名已标准化")
        
        if args.remove_duplicates:
            df = remove_duplicates(df)
        
        if args.handle_missing:
            df = handle_missing_values(df, strategy=args.handle_missing, fill_value=args.fill_value)
            print(f"缺失值处理完成 ({args.handle_missing})")
        
        if args.remove_outliers:
            df = remove_outliers(df, method=args.outlier_method)
        
        # 保存结果
        print(f"清洗后数据: {len(df)} 行, {len(df.columns)} 列")
        save_data(df, args.output)
        
        print("\n✓ 数据清洗完成!")
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
