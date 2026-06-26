#!/usr/bin/env python3
"""
行业/概念选股结果Excel生成脚本
用法: python generate_stock_excel.py <输出文件名> <sheet名称> <字段1,字段2,字段3,...> <数据行1|数据行2|...>
"""

import sys
import os
from datetime import datetime

def generate_excel(output_file, sheets_data):
    """
    生成Excel文件
    sheets_data: list of dict, each dict contains:
        - 'name': sheet name
        - 'headers': list of column headers
        - 'rows': list of lists, each inner list is a row
    """
    try:
        import pandas as pd
    except ImportError:
        print("pandas not installed, will save as CSV")
        # Fallback to CSV
        for sheet in sheets_data:
            df = pd.DataFrame(sheet['rows'], columns=sheet['headers'])
            csv_file = output_file.replace('.xlsx', f"_{sheet['name']}.csv")
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        return
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet in sheets_data:
            df = pd.DataFrame(sheet['rows'], columns=sheet['headers'])
            # Excel sheet name max 31 chars
            sheet_name = sheet['name'][:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Excel file created: {output_file}")

def parse_arguments():
    """解析命令行参数"""
    if len(sys.argv) < 2:
        # Demo mode - generate sample file
        output_file = f"/Users/tututu/.openclaw/workspace/选股结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        sheets_data = [
            {
                'name': '新能源',
                'headers': ['代码', '名称', '现价', '涨跌幅', '换手率', '市值', '市盈率'],
                'rows': [
                    ['600150', '中国船舶', '25.80', '5.23%', '3.21%', '500亿', '28.5'],
                    ['601865', '莱特光电', '18.92', '3.45%', '2.11%', '120亿', '35.2'],
                ]
            },
            {
                'name': 'AI概念',
                'headers': ['代码', '名称', '现价', '涨跌幅', '换手率', '市值', '市盈率'],
                'rows': [
                    ['300750', '宁德时代', '180.50', '-1.23%', '1.85%', '8500亿', '45.6'],
                    ['002594', '比亚迪', '245.80', '0.89%', '2.10%', '7200亿', '52.3'],
                ]
            }
        ]
        generate_excel(output_file, sheets_data)
        return output_file
    
    output_file = sys.argv[1]
    
    # Parse subsequent arguments as sheets
    # Format: sheet_name|header1,header2,header3|row1col1,row1col2|row2col1,row2col2
    sheets_data = []
    i = 2
    while i < len(sys.argv):
        parts = sys.argv[i].split('|')
        if len(parts) >= 3:
            sheet = {
                'name': parts[0],
                'headers': parts[1].split(','),
                'rows': []
            }
            for row_data in parts[2:]:
                sheet['rows'].append(row_data.split(','))
            sheets_data.append(sheet)
        i += 1
    
    if sheets_data:
        generate_excel(output_file, sheets_data)
    
    return output_file

if __name__ == "__main__":
    result = parse_arguments()
    print(f"Done: {result}")
