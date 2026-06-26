#!/usr/bin/env python3
"""
验证导出的Excel文件
检查数据完整性和准确性
"""

import sys
import argparse
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("[FAIL] 需要安装pandas: pip install pandas")
    sys.exit(1)


def verify_excel(file_path: str):
    """验证Excel文件"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"[FAIL] 文件不存在: {file_path}")
        return False
    
    print("=" * 60)
    print("Excel文件验证报告")
    print("=" * 60)
    print(f"文件: {file_path}")
    print("-" * 60)
    
    try:
        # 读取Excel
        xls = pd.ExcelFile(file_path)
        
        print(f"\n工作表数量: {len(xls.sheet_names)}")
        print(f"工作表: {', '.join(xls.sheet_names)}")
        
        # 验证主表
        if "发票信息" in xls.sheet_names:
            df_main = pd.read_excel(file_path, sheet_name="发票信息")
            
            print(f"\n【发票信息表】")
            print(f"  记录数: {len(df_main)}")
            
            # 检查关键字段
            required_fields = ["发票号码", "开票日期", "销售方名称", "价税合计"]
            print(f"\n  字段完整性:")
            for field in required_fields:
                if field in df_main.columns:
                    non_null = df_main[field].notna().sum()
                    print(f"    {field}: {non_null}/{len(df_main)} ({non_null/len(df_main)*100:.1f}%)")
                else:
                    print(f"    {field}: [缺失]")
            
            # 统计金额
            if "价税合计" in df_main.columns:
                total = df_main["价税合计"].sum()
                print(f"\n  金额统计:")
                print(f"    发票总额: {total:,.2f}")
                print(f"    平均金额: {df_main['价税合计'].mean():,.2f}")
                print(f"    最大金额: {df_main['价税合计'].max():,.2f}")
                print(f"    最小金额: {df_main['价税合计'].min():,.2f}")
            
            # 日期范围
            if "开票日期" in df_main.columns:
                dates = pd.to_datetime(df_main["开票日期"], errors='coerce')
                valid_dates = dates.dropna()
                if len(valid_dates) > 0:
                    print(f"\n  日期范围:")
                    print(f"    最早: {valid_dates.min().strftime('%Y-%m-%d')}")
                    print(f"    最晚: {valid_dates.max().strftime('%Y-%m-%d')}")
        
        # 验证明细表
        if "商品明细" in xls.sheet_names:
            df_items = pd.read_excel(file_path, sheet_name="商品明细")
            
            print(f"\n【商品明细表】")
            print(f"  记录数: {len(df_items)}")
            
            if "发票号码" in df_items.columns:
                unique_invoices = df_items["发票号码"].nunique()
                print(f"  涉及发票: {unique_invoices} 张")
        
        print("\n" + "=" * 60)
        print("[OK] 验证完成")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"[FAIL] 验证失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='验证导出的Excel文件',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'file',
        help='Excel文件路径'
    )
    
    args = parser.parse_args()
    
    success = verify_excel(args.file)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
