#!/usr/bin/env python3
"""
Data Analyzer - Pandas数据分析工具
生成数据摘要、统计信息和基础分析报告
"""

import pandas as pd
import numpy as np
import argparse
import sys
import json
from pathlib import Path
from typing import Dict, Any


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


def basic_info(df: pd.DataFrame) -> Dict[str, Any]:
    """基础信息"""
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
        'duplicates': df.duplicated().sum(),
        'column_names': df.columns.tolist()
    }


def data_types_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """数据类型汇总"""
    dtype_counts = df.dtypes.value_counts().to_dict()
    return {
        'dtype_counts': {str(k): int(v) for k, v in dtype_counts.items()},
        'column_dtypes': df.dtypes.astype(str).to_dict()
    }


def missing_values_report(df: pd.DataFrame) -> Dict[str, Any]:
    """缺失值报告"""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    missing_data = pd.DataFrame({
        'missing_count': missing,
        'missing_percentage': missing_pct
    })
    
    missing_data = missing_data[missing_data['missing_count'] > 0].sort_values(
        'missing_count', ascending=False
    )
    
    return {
        'total_missing': int(df.isnull().sum().sum()),
        'columns_with_missing': len(missing_data),
        'details': missing_data.to_dict('index') if not missing_data.empty else {}
    }


def numeric_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """数值型列统计"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        return {'message': '没有数值型列'}
    
    stats = df[numeric_cols].describe().T
    stats['variance'] = df[numeric_cols].var()
    stats['skewness'] = df[numeric_cols].skew()
    stats['kurtosis'] = df[numeric_cols].kurtosis()
    
    return {
        'numeric_columns': numeric_cols,
        'statistics': stats.to_dict('index')
    }


def categorical_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """分类型列统计"""
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not categorical_cols:
        return {'message': '没有分类型列'}
    
    result = {}
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        result[col] = {
            'unique_values': int(df[col].nunique()),
            'most_common': value_counts.head(10).to_dict(),
            'least_common': value_counts.tail(5).to_dict()
        }
    
    return {
        'categorical_columns': categorical_cols,
        'details': result
    }


def correlation_analysis(df: pd.DataFrame, threshold: float = 0.5) -> Dict[str, Any]:
    """相关性分析"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        return {'message': '数值列不足，无法进行相关性分析'}
    
    corr_matrix = df[numeric_cols].corr()
    
    # 找出高相关性对
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) >= threshold:
                high_corr.append({
                    'column1': corr_matrix.columns[i],
                    'column2': corr_matrix.columns[j],
                    'correlation': round(corr_matrix.iloc[i, j], 4)
                })
    
    return {
        'correlation_matrix': corr_matrix.to_dict(),
        'high_correlations': high_corr
    }


def outlier_detection(df: pd.DataFrame, method: str = 'iqr') -> Dict[str, Any]:
    """异常值检测"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        return {'message': '没有数值型列'}
    
    outliers = {}
    
    for col in numeric_cols:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': round(outlier_count / len(df) * 100, 2),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound)
                }
    
    return {
        'method': method,
        'outliers': outliers
    }


def generate_report(df: pd.DataFrame, output_format: str = 'json') -> str:
    """生成完整分析报告"""
    report = {
        'basic_info': basic_info(df),
        'data_types': data_types_summary(df),
        'missing_values': missing_values_report(df),
        'numeric_statistics': numeric_statistics(df),
        'categorical_statistics': categorical_statistics(df),
        'correlation_analysis': correlation_analysis(df),
        'outlier_detection': outlier_detection(df)
    }
    
    if output_format == 'json':
        return json.dumps(report, indent=2, ensure_ascii=False)
    else:
        # 文本格式
        lines = []
        lines.append("=" * 80)
        lines.append("数据分析报告")
        lines.append("=" * 80)
        lines.append(f"\n基础信息:")
        for k, v in report['basic_info'].items():
            lines.append(f"  {k}: {v}")
        
        lines.append(f"\n缺失值分析:")
        lines.append(f"  总缺失值: {report['missing_values']['total_missing']}")
        lines.append(f"  有缺失值的列数: {report['missing_values']['columns_with_missing']}")
        
        lines.append(f"\n数值型统计:")
        if 'numeric_columns' in report['numeric_statistics']:
            lines.append(f"  数值列: {', '.join(report['numeric_statistics']['numeric_columns'])}")
        
        lines.append(f"\n分类型统计:")
        if 'categorical_columns' in report['categorical_statistics']:
            lines.append(f"  分类列: {', '.join(report['categorical_statistics']['categorical_columns'])}")
        
        lines.append("=" * 80)
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Pandas数据分析工具')
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('--output', '-o', help='输出报告路径')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='报告格式')
    
    args = parser.parse_args()
    
    try:
        # 加载数据
        print(f"加载数据: {args.input}")
        df = load_data(args.input)
        
        # 生成报告
        report = generate_report(df, args.format)
        
        # 输出报告
        if args.output:
            Path(args.output).write_text(report, encoding='utf-8')
            print(f"\n报告已保存到: {args.output}")
        else:
            print("\n" + report)
        
        print("\n✓ 数据分析完成!")
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
