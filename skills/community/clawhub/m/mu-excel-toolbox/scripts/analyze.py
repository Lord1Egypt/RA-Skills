#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析 & 统计摘要工具 - 一键生成数据分析报告

场景：快速了解数据概况、分布、异常值
输出：基础统计/数值统计/文本统计/日期统计/相关性/异常值检测
"""

import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import detect_file_type, safe_read, format_output, ErrorCollector


def analyze_basic(df: pd.DataFrame) -> dict:
    """基础统计"""
    total_cells = df.shape[0] * df.shape[1]
    null_cells = df.isna().sum().sum()
    duplicate_rows = df.duplicated().sum()

    return {
        'rows': df.shape[0],
        'columns': df.shape[1],
        'total_cells': total_cells,
        'null_cells': int(null_cells),
        'null_rate': f"{null_cells / max(total_cells, 1) * 100:.2f}%",
        'duplicate_rows': int(duplicate_rows),
        'duplicate_rate': f"{duplicate_rows / max(df.shape[0], 1) * 100:.2f}%",
        'column_names': list(df.columns),
    }


def analyze_numeric(df: pd.DataFrame, columns: list = None) -> dict:
    """数值列分析"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if columns:
        numeric_cols = [c for c in columns if c in numeric_cols]

    if not numeric_cols:
        return {}

    result = {}
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue

        stats = {
            'count': int(series.count()),
            'null_count': int(df[col].isna().sum()),
            'mean': round(float(series.mean()), 4),
            'median': round(float(series.median()), 4),
            'std': round(float(series.std()), 4),
            'min': round(float(series.min()), 4),
            'max': round(float(series.max()), 4),
            'q25': round(float(series.quantile(0.25)), 4),
            'q75': round(float(series.quantile(0.75)), 4),
            'q90': round(float(series.quantile(0.90)), 4),
        }
        result[col] = stats

    return result


def analyze_text(df: pd.DataFrame, columns: list = None) -> dict:
    """文本列分析"""
    text_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    if columns:
        text_cols = [c for c in columns if c in text_cols]

    if not text_cols:
        return {}

    result = {}
    for col in text_cols:
        series = df[col].dropna().astype(str)
        if len(series) == 0:
            continue

        # 频率 TOP5
        top5 = series.value_counts().head(5)

        stats = {
            'count': int(series.count()),
            'null_count': int(df[col].isna().sum()),
            'unique_count': int(series.nunique()),
            'avg_length': round(float(series.str.len().mean()), 1),
            'max_length': int(series.str.len().max()),
            'min_length': int(series.str.len().min()),
            'top5': [{'value': str(k), 'count': int(v)} for k, v in top5.items()],
        }
        result[col] = stats

    return result


def analyze_datetime(df: pd.DataFrame, columns: list = None) -> dict:
    """日期列分析"""
    # 尝试识别日期列
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

    # 额外尝试解析可能是日期的文本列
    for col in df.select_dtypes(include=['object', 'string']).columns:
        if columns and col not in columns:
            continue
        sample = df[col].dropna().head(20)
        if len(sample) == 0:
            continue
        try:
            parsed = pd.to_datetime(sample, errors='coerce')
            if parsed.notna().sum() >= len(sample) * 0.8:  # 80%以上能解析为日期
                date_cols.append(col)
        except Exception:
            continue

    if columns:
        date_cols = [c for c in columns if c in date_cols]

    if not date_cols:
        return {}

    result = {}
    for col in date_cols:
        try:
            series = pd.to_datetime(df[col], errors='coerce').dropna()
            if len(series) == 0:
                continue

            stats = {
                'count': int(series.count()),
                'null_count': int(df[col].isna().sum()),
                'earliest': str(series.min()),
                'latest': str(series.max()),
                'range_days': int((series.max() - series.min()).days),
            }

            # 按月分布
            monthly = series.dt.to_period('M').value_counts().sort_index()
            stats['monthly_distribution'] = {str(k): int(v) for k, v in monthly.head(12).items()}

            result[col] = stats
        except Exception:
            continue

    return result


def analyze_correlation(df: pd.DataFrame, columns: list = None) -> dict:
    """相关性矩阵（数值列之间）"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if columns:
        numeric_cols = [c for c in columns if c in numeric_cols]

    if len(numeric_cols) < 2:
        return {}

    corr_matrix = df[numeric_cols].corr()
    result = {}
    for col in corr_matrix.columns:
        result[col] = {k: round(float(v), 4) for k, v in corr_matrix[col].items() if k != col}

    return result


def detect_outliers(df: pd.DataFrame, columns: list = None) -> dict:
    """异常值检测（IQR 法）"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if columns:
        numeric_cols = [c for c in columns if c in numeric_cols]

    if not numeric_cols:
        return {}

    result = {}
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = series[(series < lower_bound) | (series > upper_bound)]
        if len(outliers) > 0:
            result[col] = {
                'outlier_count': int(len(outliers)),
                'outlier_rate': f"{len(outliers) / len(series) * 100:.2f}%",
                'lower_bound': round(float(lower_bound), 4),
                'upper_bound': round(float(upper_bound), 4),
                'outlier_rows': [int(idx + 2) for idx in outliers.index[:20]],  # 最多显示20行
            }

    return result


def format_text_report(analysis: dict, detail: bool = True) -> str:
    """格式化为文本报告"""
    lines = []
    lines.append("=" * 70)
    lines.append("📊 数据分析报告")
    lines.append("=" * 70)

    # 基础统计
    basic = analysis.get('basic', {})
    lines.append("\n📋 基础统计")
    lines.append("-" * 40)
    lines.append(f"  行数: {basic.get('rows', 0)}")
    lines.append(f"  列数: {basic.get('columns', 0)}")
    lines.append(f"  空值率: {basic.get('null_rate', '0%')}")
    lines.append(f"  重复行: {basic.get('duplicate_rows', 0)} ({basic.get('duplicate_rate', '0%')})")
    lines.append(f"  列名: {', '.join(basic.get('column_names', []))}")

    # 数值列
    numeric = analysis.get('numeric', {})
    if numeric:
        lines.append("\n📈 数值列统计")
        lines.append("-" * 40)
        for col, stats in numeric.items():
            lines.append(f"\n  【{col}】")
            lines.append(f"    有效值: {stats['count']} | 空值: {stats['null_count']}")
            lines.append(f"    均值: {stats['mean']} | 中位数: {stats['median']} | 标准差: {stats['std']}")
            lines.append(f"    最小: {stats['min']} | 最大: {stats['max']}")
            if detail:
                lines.append(f"    Q25: {stats['q25']} | Q75: {stats['q75']} | Q90: {stats['q90']}")

    # 文本列
    text = analysis.get('text', {})
    if text:
        lines.append("\n📝 文本列统计")
        lines.append("-" * 40)
        for col, stats in text.items():
            lines.append(f"\n  【{col}】")
            lines.append(f"    有效值: {stats['count']} | 唯一值: {stats['unique_count']}")
            lines.append(f"    平均长度: {stats['avg_length']} | 最长: {stats['max_length']}")
            if detail and stats.get('top5'):
                top_str = ', '.join([f"{t['value']}({t['count']})" for t in stats['top5']])
                lines.append(f"    TOP5: {top_str}")

    # 日期列
    date_info = analysis.get('datetime', {})
    if date_info:
        lines.append("\n📅 日期列统计")
        lines.append("-" * 40)
        for col, stats in date_info.items():
            lines.append(f"\n  【{col}】")
            lines.append(f"    范围: {stats['earliest']} ~ {stats['latest']} ({stats['range_days']}天)")
            if detail and stats.get('monthly_distribution'):
                dist_str = ', '.join([f"{k}:{v}" for k, v in list(stats['monthly_distribution'].items())[:6]])
                lines.append(f"    月分布: {dist_str}")

    # 相关性
    correlation = analysis.get('correlation', {})
    if correlation and detail:
        lines.append("\n🔗 相关性矩阵（>0.5 的显著相关）")
        lines.append("-" * 40)
        shown = set()
        for col, corrs in correlation.items():
            for other_col, val in corrs.items():
                pair = tuple(sorted([col, other_col]))
                if abs(val) > 0.5 and pair not in shown:
                    shown.add(pair)
                    lines.append(f"  {col} ↔ {other_col}: {val}")

    # 异常值
    outliers = analysis.get('outliers', {})
    if outliers:
        lines.append("\n⚠️ 异常值检测（IQR 法）")
        lines.append("-" * 40)
        for col, info in outliers.items():
            lines.append(f"  【{col}】{info['outlier_count']} 个异常值 ({info['outlier_rate']})")
            lines.append(f"    正常范围: [{info['lower_bound']}, {info['upper_bound']}]")
            if detail:
                rows_str = ', '.join([str(r) for r in info['outlier_rows'][:10]])
                lines.append(f"    异常行号: {rows_str}")

    lines.append("\n" + "=" * 70)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Excel 数据分析工具 - 一键生成统计摘要报告'
    )
    parser.add_argument('input_file', help='输入文件路径（Excel/CSV）')
    parser.add_argument('--output', help='分析报告输出路径（不指定则打印到终端）')
    parser.add_argument('--columns', help='分析指定列（逗号分隔）')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='输出格式（默认 text）')
    parser.add_argument('--detail', action='store_true', default=True,
                        help='详细模式（默认开启）')
    parser.add_argument('--brief', action='store_true',
                        help='简要模式（关闭详细信息）')
    parser.add_argument('--sheet', help='指定 Sheet 名称')

    args = parser.parse_args()

    if args.brief:
        args.detail = False

    # 校验输入
    if not os.path.exists(args.input_file):
        print(f"❌ 输入文件不存在: {args.input_file}")
        sys.exit(1)

    # 加载数据
    try:
        df, _errors = safe_read(args.input_file, sheet_name=args.sheet)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        sys.exit(1)

    # 解析目标列
    target_columns = None
    if args.columns:
        target_columns = [c.strip() for c in args.columns.split(',')]
        # 验证列名存在
        missing = [c for c in target_columns if c not in df.columns]
        if missing:
            print(f"⚠️ 以下列不存在: {', '.join(missing)}")

    print(f"📊 分析文件: {args.input_file}")
    print(f"📝 数据规模: {df.shape[0]} 行 × {df.shape[1]} 列\n")

    # 执行分析
    analysis = {
        'basic': analyze_basic(df),
        'numeric': analyze_numeric(df, target_columns),
        'text': analyze_text(df, target_columns),
        'datetime': analyze_datetime(df, target_columns),
        'correlation': analyze_correlation(df, target_columns),
        'outliers': detect_outliers(df, target_columns),
    }

    # 输出报告
    if args.format == 'json':
        report_text = json.dumps(analysis, ensure_ascii=False, indent=2)
    else:
        report_text = format_text_report(analysis, detail=args.detail)

    if args.output:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"✅ 分析报告已保存: {args.output}")
    else:
        print(report_text)


if __name__ == "__main__":
    main()
