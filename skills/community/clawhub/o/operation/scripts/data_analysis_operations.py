#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析和操作工具箱
提供全面的 Excel/CSV 文件数据分析、对比、清洗和报告功能
支持多种数据格式和编码
"""

import pandas as pd
import numpy as np
import os
import sys
import argparse
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """打印彩色标题"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """打印信息"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def resolve_column(df, column_ref):
    """解析列引用（支持列名、字母、索引）"""
    if isinstance(column_ref, str):
        column_ref = column_ref.strip()
        # 检查是否是列名
        if column_ref in df.columns:
            return column_ref
        # 检查是否是字母（如 'A', 'B'）
        if column_ref.isalpha() and len(column_ref) <= 3:
            try:
                col_idx = 0
                for char in column_ref.upper():
                    col_idx = col_idx * 26 + (ord(char) - ord('A') + 1)
                col_idx -= 1  # 转换为0索引
                if 0 <= col_idx < len(df.columns):
                    return df.columns[col_idx]
            except:
                pass
        # 检查是否是数字索引
        try:
            col_idx = int(column_ref)
            if 0 <= col_idx < len(df.columns):
                return df.columns[col_idx]
        except:
            pass
    return None

def read_file_with_encoding(file_path):
    """智能读取文件，自动检测编码"""
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin1', 'cp936']
    
    for encoding in encodings:
        try:
            if file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
                return pd.read_excel(file_path), encoding
            else:
                return pd.read_csv(file_path, encoding=encoding), encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            continue
    
    # 如果所有编码都失败，尝试使用 Python 引擎
    try:
        if file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
            return pd.read_excel(file_path), 'auto'
        else:
            return pd.read_csv(file_path, engine='python', encoding='latin1'), 'latin1 (fallback)'
    except Exception as e:
        raise ValueError(f"无法读取文件 '{file_path}': {str(e)}")

def analyze_data(file_path, focus_columns=None, output_file=None):
    """
    综合分析 Excel/CSV 文件
    """
    print_header(f"数据分析: {os.path.basename(file_path)}")
    
    try:
        # 读取文件
        df, encoding = read_file_with_encoding(file_path)
        print_success(f"成功读取文件 (编码: {encoding})")
        print_info(f"数据维度: {df.shape[0]} 行 × {df.shape[1]} 列")
        
        # 确定分析的列
        if focus_columns:
            analyze_cols = []
            for ref in focus_columns.split(','):
                col = resolve_column(df, ref.strip())
                if col:
                    analyze_cols.append(col)
                else:
                    print_warning(f"列 '{ref}' 未找到")
            
            if not analyze_cols:
                print_error("没有找到有效的分析列")
                return
        else:
            analyze_cols = list(df.columns)
        
        # 生成报告文件
        if output_file is None:
            base_name = os.path.splitext(file_path)[0]
            output_file = f"{base_name}_analysis_report.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 1. 数据概览
            print_header("数据概览")
            print_info(f"列名: {', '.join(df.columns.tolist())}")
            
            summary_data = {
                '指标': ['总行数', '总列数', '文件大小(MB)', '读取时间', '编码'],
                '数值': [len(df), len(df.columns), 
                        os.path.getsize(file_path) / 1024 / 1024,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        encoding]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='数据概览', index=False)
            
            # 2. 列信息
            print_header("列信息")
            col_info = pd.DataFrame({
                '列名': df.columns,
                '数据类型': df.dtypes.astype(str),
                '空值数量': df.isnull().sum().values,
                '空值比例(%)': (df.isnull().sum() / len(df) * 100).round(2).values,
                '唯一值数量': df.nunique().values
            })
            col_info.to_excel(writer, sheet_name='列信息', index=False)
            
            # 显示空值统计
            missing_info = col_info[col_info['空值数量'] > 0]
            if len(missing_info) > 0:
                print_warning("发现空值列:")
                for _, row in missing_info.iterrows():
                    print(f"  {row['列名']}: {row['空值数量']} ({row['空值比例(%)']}%)")
            else:
                print_success("没有发现空值")
            
            # 3. 数值列统计
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                print_header("数值列分析")
                print_info(f"发现 {len(numeric_cols)} 个数值列")
                
                numeric_stats = df[numeric_cols].describe().round(2)
                numeric_stats.to_excel(writer, sheet_name='数值统计')
                
                # 打印关键统计
                for col in numeric_cols:
                    print(f"\n  {col}:")
                    print(f"    最小值: {df[col].min()}")
                    print(f"    最大值: {df[col].max()}")
                    print(f"    平均值: {df[col].mean():.2f}")
                    print(f"    中位数: {df[col].median()}")
            
            # 4. 分类列分析
            object_cols = df.select_dtypes(include=['object']).columns.tolist()
            if object_cols:
                print_header("分类列分析")
                print_info(f"发现 {len(object_cols)} 个分类列")
                
                cat_stats_data = []
                for col in object_cols:
                    unique_count = df[col].nunique()
                    cat_stats_data.append({
                        '列名': col,
                        '数据类型': '分类',
                        '唯一值数量': unique_count,
                        '最高频值': df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A',
                        '最高频计数': df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
                    })
                
                cat_stats_df = pd.DataFrame(cat_stats_data)
                cat_stats_df.to_excel(writer, sheet_name='分类统计', index=False)
                
                # 显示高频值
                for col in object_cols[:3]:  # 只显示前3列
                    if df[col].nunique() < 20:
                        print(f"\n  {col} 值分布:")
                        value_counts = df[col].value_counts().head(5)
                        for val, count in value_counts.items():
                            percent = count / len(df) * 100
                            print(f"    {val[:30]}: {count} ({percent:.1f}%)")
            
            # 5. 业务洞察
            print_header("业务洞察")
            insights = []
            
            # 数据质量洞察
            if len(missing_info) > 0:
                high_missing = missing_info[missing_info['空值比例(%)'] > 20]
                if len(high_missing) > 0:
                    insights.append(f"⚠️ 以下列空值超过20%: {', '.join(high_missing['列名'].tolist())}")
            
            # 重复数据检查
            duplicate_rows = df.duplicated().sum()
            if duplicate_rows > 0:
                insights.append(f"⚠️ 发现 {duplicate_rows} 行重复数据 ({duplicate_rows/len(df)*100:.1f}%)")
            else:
                insights.append("✓ 没有发现重复数据")
            
            # 异常值检测（针对数值列）
            for col in numeric_cols:
                if len(df[col].dropna()) > 10:  # 至少有10个有效值
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
                    if len(outliers) > 0:
                        insights.append(f"⚠️ {col} 中发现 {len(outliers)} 个异常值")
            
            # 保存洞察
            if insights:
                insights_df = pd.DataFrame({'洞察': insights})
                insights_df.to_excel(writer, sheet_name='业务洞察', index=False)
                
                for insight in insights:
                    if insight.startswith('✓'):
                        print_success(insight[1:].strip())
                    elif insight.startswith('⚠️'):
                        print_warning(insight[2:].strip())
                    else:
                        print_info(insight)
        
        print_success(f"分析报告已保存到: {output_file}")
        return output_file
        
    except Exception as e:
        print_error(f"分析过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def compare_columns(file_path, col_a, col_b, mode='full', output_file=None):
    """
    对比两列数据
    """
    print_header(f"列对比: {col_a} vs {col_b}")
    
    try:
        # 读取文件
        df, encoding = read_file_with_encoding(file_path)
        print_success(f"成功读取文件 (编码: {encoding})")
        
        # 解析列引用
        col_a_name = resolve_column(df, col_a)
        col_b_name = resolve_column(df, col_b)
        
        if not col_a_name:
            print_error(f"无法解析列 '{col_a}'")
            return None
        if not col_b_name:
            print_error(f"无法解析列 '{col_b}'")
            return None
        
        print_info(f"对比列: {col_a_name} ↔ {col_b_name}")
        
        # 提取数据并去重
        series_a = df[col_a_name].dropna().astype(str).str.strip()
        series_b = df[col_b_name].dropna().astype(str).str.strip()
        
        set_a = set(series_a)
        set_b = set(series_b)
        
        # 计算对比结果
        only_in_a = sorted(set_a - set_b)
        only_in_b = sorted(set_b - set_a)
        common_values = sorted(set_a & set_b)
        
        print_header("对比结果")
        print_info(f"A列唯一值数量: {len(set_a)}")
        print_info(f"B列唯一值数量: {len(set_b)}")
        print_info(f"共有的值: {len(common_values)}")
        print_info(f"仅在A列的值: {len(only_in_a)}")
        print_info(f"仅在B列的值: {len(only_in_b)}")
        
        # 生成输出文件
        if output_file is None:
            base_name = os.path.splitext(file_path)[0]
            output_file = f"{base_name}_对比_{col_a_name}_vs_{col_b_name}.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 汇总表
            summary_data = {
                '指标': ['A列', 'B列', 'A列唯一值', 'B列唯一值', '共有值', '仅A列', '仅B列'],
                '数值': [col_a_name, col_b_name, len(set_a), len(set_b), 
                        len(common_values), len(only_in_a), len(only_in_b)]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='汇总', index=False)
            
            # 仅A列
            if only_in_a:
                pd.DataFrame({'仅在A列的值': only_in_a}).to_excel(writer, sheet_name='仅A列', index=False)
            
            # 仅B列
            if only_in_b:
                pd.DataFrame({'仅在B列的值': only_in_b}).to_excel(writer, sheet_name='仅B列', index=False)
            
            # 共有的值
            if common_values:
                pd.DataFrame({'共有的值': common_values}).to_excel(writer, sheet_name='共有值', index=False)
        
        print_success(f"对比报告已保存到: {output_file}")
        
        # 根据模式显示结果
        if mode == 'diff':
            print_header("差异值")
            if only_in_a:
                print(f"\n仅在 {col_a_name} 中的值:")
                for val in only_in_a[:10]:  # 只显示前10个
                    print(f"  - {val}")
                if len(only_in_a) > 10:
                    print(f"  ... 还有 {len(only_in_a)-10} 个值")
            
            if only_in_b:
                print(f"\n仅在 {col_b_name} 中的值:")
                for val in only_in_b[:10]:
                    print(f"  - {val}")
                if len(only_in_b) > 10:
                    print(f"  ... 还有 {len(only_in_b)-10} 个值")
        
        return output_file
        
    except Exception as e:
        print_error(f"对比过程中出错: {str(e)}")
        return None

def clean_data(file_path, output_file=None, remove_duplicates=True, fill_missing='none'):
    """
    数据清洗功能
    """
    print_header(f"数据清洗: {os.path.basename(file_path)}")
    
    try:
        # 读取文件
        df, encoding = read_file_with_encoding(file_path)
        print_success(f"成功读取文件 (编码: {encoding})")
        original_shape = df.shape
        
        # 记录清洗步骤
        steps = []
        
        # 1. 删除完全为空的列
        empty_cols = df.columns[df.isnull().all()].tolist()
        if empty_cols:
            df = df.drop(columns=empty_cols)
            steps.append(f"删除 {len(empty_cols)} 个空列: {', '.join(empty_cols)}")
        
        # 2. 删除重复行
        if remove_duplicates:
            duplicate_count = df.duplicated().sum()
            if duplicate_count > 0:
                df = df.drop_duplicates()
                steps.append(f"删除 {duplicate_count} 行重复数据")
        
        # 3. 处理缺失值
        if fill_missing != 'none':
            if fill_missing == 'zero':
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = df[numeric_cols].fillna(0)
                steps.append("数值列空值填充为 0")
            elif fill_missing == 'mean':
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if df[col].isnull().any():
                        mean_val = df[col].mean()
                        df[col] = df[col].fillna(mean_val)
                        steps.append(f"{col} 空值填充为平均值 {mean_val:.2f}")
            elif fill_missing == 'mode':
                for col in df.columns:
                    if df[col].dtype == 'object' and df[col].isnull().any():
                        mode_val = df[col].mode()
                        if not mode_val.empty:
                            df[col] = df[col].fillna(mode_val.iloc[0])
                            steps.append(f"{col} 空值填充为最高频值")
        
        # 4. 去除字符串列的前后空格
        str_cols = df.select_dtypes(include=['object']).columns
        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()
        if str_cols.any():
            steps.append("清理字符串列的空格")
        
        # 生成输出文件
        if output_file is None:
            base_name = os.path.splitext(file_path)[0]
            output_file = f"{base_name}_cleaned.xlsx"
        
        # 保存清洗后的数据
        if file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
            df.to_excel(output_file, index=False)
        else:
            df.to_csv(output_file, index=False, encoding='utf-8')
        
        # 打印清洗报告
        print_header("清洗报告")
        for step in steps:
            print_success(step)
        
        print_info(f"原始数据: {original_shape[0]} 行 × {original_shape[1]} 列")
        print_info(f"清洗后: {df.shape[0]} 行 × {df.shape[1]} 列")
        
        if original_shape[0] > df.shape[0]:
            removed = original_shape[0] - df.shape[0]
            print_info(f"删除了 {removed} 行数据 ({removed/original_shape[0]*100:.1f}%)")
        
        if original_shape[1] > df.shape[1]:
            removed_cols = original_shape[1] - df.shape[1]
            print_info(f"删除了 {removed_cols} 个空列")
        
        print_success(f"清洗后的数据已保存到: {output_file}")
        return output_file
        
    except Exception as e:
        print_error(f"清洗过程中出错: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Excel 数据分析与操作工具箱')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 分析命令
    analyze_parser = subparsers.add_parser('analyze', help='分析 Excel/CSV 文件')
    analyze_parser.add_argument('file', help='要分析的 Excel/CSV 文件')
    analyze_parser.add_argument('--focus', help='指定要分析的列（逗号分隔）')
    analyze_parser.add_argument('--output', help='输出文件路径')
    
    # 对比命令
    compare_parser = subparsers.add_parser('compare', help='对比两列数据')
    compare_parser.add_argument('file', help='要对比的 Excel/CSV 文件')
    compare_parser.add_argument('col_a', help='第一列（列名、字母或索引）')
    compare_parser.add_argument('col_b', help='第二列（列名、字母或索引）')
    compare_parser.add_argument('--mode', choices=['full', 'diff', 'unique_a', 'unique_b', 'common'], 
                               default='full', help='对比模式')
    compare_parser.add_argument('--output', help='输出文件路径')
    
    # 清洗命令
    clean_parser = subparsers.add_parser('clean', help='清洗数据')
    clean_parser.add_argument('file', help='要清洗的 Excel/CSV 文件')
    clean_parser.add_argument('--output', help='输出文件路径')
    clean_parser.add_argument('--no-dedup', action='store_true', help='不删除重复行')
    clean_parser.add_argument('--fill', choices=['none', 'zero', 'mean', 'mode'], 
                             default='none', help='缺失值填充方式')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'analyze':
            analyze_data(args.file, args.focus, args.output)
        elif args.command == 'compare':
            compare_columns(args.file, args.col_a, args.col_b, args.mode, args.output)
        elif args.command == 'clean':
            clean_data(args.file, args.output, not args.no_dedup, args.fill)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print_error(f"执行出错: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()