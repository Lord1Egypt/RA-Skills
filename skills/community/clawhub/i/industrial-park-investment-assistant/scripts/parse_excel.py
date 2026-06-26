#!/usr/bin/env python3
"""
Excel/CSV 自动解析脚本 v1.0
支持多种表头格式自动识别，输出结构化数据
"""

import os
import sys
import json
import csv
import re
from pathlib import Path
from datetime import datetime

def detect_file_type(file_path):
    """检测文件类型（Excel/CSV）"""
    ext = Path(file_path).suffix.lower()
    if ext in ['.xlsx', '.xls']:
        return 'excel'
    elif ext == '.csv':
        return 'csv'
    else:
        return None

def read_excel(file_path):
    """读取Excel文件（需要openpyxl库）"""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        
        # 读取所有行
        rows = []
        for row in ws.iter_rows(values_only=True):
            rows.append([str(cell) if cell is not None else '' for cell in row])
        
        return rows
    except ImportError:
        print("❌ 缺少 openpyxl 库，请运行：pip install openpyxl")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 读取Excel失败：{e}")
        sys.exit(1)

def read_csv(file_path):
    """读取CSV文件"""
    rows = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows
    except UnicodeDecodeError:
        # 尝试GBK编码
        with open(file_path, 'r', encoding='gbk') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows
    except Exception as e:
        print(f"❌ 读取CSV失败：{e}")
        sys.exit(1)

def normalize_header(header):
    """规范化表头（去除空格、特殊字符，统一格式）"""
    if not header:
        return ''
    
    # 去除空格和特殊字符
    normalized = re.sub(r'[\s\-_()（）【】]+', '', str(header))
    
    # 统一常见变体
    mappings = {
        '房间号': ['房间号', '房号', '编号', '单元号'],
        '楼层': ['楼层', '层'],
        '面积': ['面积', '建筑面积', '使用面积', '㎡', '平方米'],
        '状态': ['状态', '出租状态', '招商状态'],
        '业态': ['业态', '用途', '类型'],
        '底价': ['底价', '租金', '单价', '租金单价', '价格'],
        '企业名称': ['企业名称', '公司名称', '客户名称', '租户名'],
        '联系人': ['联系人', '负责人', '对接人'],
        '电话': ['电话', '手机号', '联系方式', '联系电话'],
        '意向等级': ['意向等级', '意向度', '优先级', '重要程度'],
        '最后跟进日期': ['最后跟进日期', '最近跟进', '最后联系时间'],
    }
    
    for standard, variants in mappings.items():
        if any(v in normalized for v in variants):
            return standard
    
    return normalized

def identify_table_type(headers):
    """根据表头判断表格类型（房源销控表/客户跟进记录/渠道跟进表）"""
    header_str = '|'.join([str(h) for h in headers]).lower()
    
    # 房源销控表关键词
    if any(kw in header_str for kw in ['房间号', '房号', '面积', '底价', '租金']):
        return '房源销控表'
    
    # 客户跟进记录关键词
    if any(kw in header_str for kw in ['企业名称', '公司名称', '客户名称', '联系人', '意向']):
        return '客户跟进记录'
    
    # 渠道跟进表关键词
    if any(kw in header_str for kw in ['渠道名称', '渠道', '对接人', '推荐客户', '成交数']):
        return '渠道跟进记录'
    
    return '未知'

def parse_room_list(rows):
    """解析房源销控表"""
    if not rows or len(rows) < 2:
        return []
    
    # 第一行作为表头
    raw_headers = rows[0]
    headers = [normalize_header(h) for h in raw_headers]
    
    # 构建列索引映射
    col_map = {}
    for idx, h in enumerate(headers):
        if h:
            col_map[h] = idx
    
    # 解析数据行
    records = []
    for row in rows[1:]:
        if not any(row):  # 跳过空行
            continue
            
        record = {}
        for col_name, col_idx in col_map.items():
            if col_idx < len(row):
                record[col_name] = row[col_idx]
        
        records.append(record)
    
    return records

def parse_customer_list(rows):
    """解析客户跟进记录"""
    if not rows or len(rows) < 2:
        return []
    
    # 第一行作为表头
    raw_headers = rows[0]
    headers = [normalize_header(h) for h in raw_headers]
    
    # 构建列索引映射
    col_map = {}
    for idx, h in enumerate(headers):
        if h:
            col_map[h] = idx
    
    # 解析数据行
    records = []
    for row in rows[1:]:
        if not any(row):  # 跳过空行
            continue
            
        record = {}
        for col_name, col_idx in col_map.items():
            if col_idx < len(row):
                record[col_name] = row[col_idx]
        
        records.append(record)
    
    return records

def parse_channel_list(rows):
    """解析渠道跟进表"""
    if not rows or len(rows) < 2:
        return []
    
    # 第一行作为表头
    raw_headers = rows[0]
    headers = [normalize_header(h) for h in raw_headers]
    
    # 构建列索引映射
    col_map = {}
    for idx, h in enumerate(headers):
        if h:
            col_map[h] = idx
    
    # 解析数据行
    records = []
    for row in rows[1:]:
        if not any(row):  # 跳过空行
            continue
            
        record = {}
        for col_name, col_idx in col_map.items():
            if col_idx < len(row):
                record[col_name] = row[col_idx]
        
        records.append(record)
    
    return records

def preview_records(records, table_type, max_rows=5):
    """预览解析结果（前N条）"""
    if not records:
        print("⚠️  没有解析到数据")
        return
    
    print(f"\n📊 已解析 {table_type}，共 {len(records)} 条记录，预览前 {min(max_rows, len(records))} 条：\n")
    
    # 根据表格类型显示不同的列
    if table_type == '房源销控表':
        headers = ['房间号', '楼层', '面积(㎡)', '状态', '业态', '底价(元/㎡/天)']
    elif table_type == '客户跟进记录':
        headers = ['企业名称', '联系人', '电话', '意向等级', '最后跟进日期']
    elif table_type == '渠道跟进记录':
        headers = ['渠道名称', '对接人', '电话', '推荐客户数', '成交数']
    else:
        headers = list(records[0].keys())
    
    # 打印表头
    header_line = '| '
    for h in headers:
        header_line += str(h)[:10].ljust(12)
    header_line += ' |'
    print(header_line)
    print('|' + '-' * (len(header_line) - 2) + '|')
    
    # 打印数据行
    for i, record in enumerate(records[:max_rows]):
        row_line = '| '
        for h in headers:
            val = str(record.get(h, ''))[:10]
            row_line += val.ljust(12)
        row_line += ' |'
        print(row_line)
    
    if len(records) > max_rows:
        print(f"\n... 还有 {len(records) - max_rows} 条记录未显示")
    
    print("\n确认无误请输入『确认入库』，有错误请告诉我哪条。")

def save_to_json(records, table_type, output_path):
    """保存解析结果到JSON文件"""
    output = {
        'table_type': table_type,
        'total': len(records),
        'parsed_at': datetime.now().isoformat(),
        'records': records
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 解析结果已保存到：{output_path}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 parse_excel.py <Excel/CSV文件路径> [--preview] [--output output.json]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在：{file_path}")
        sys.exit(1)
    
    # 检测文件类型
    file_type = detect_file_type(file_path)
    if not file_type:
        print(f"❌ 不支持的文件格式：{file_path}")
        sys.exit(1)
    
    print(f"📂 读取文件：{file_path}（{file_type.upper()}格式）")
    
    # 读取文件
    if file_type == 'excel':
        rows = read_excel(file_path)
    else:
        rows = read_csv(file_path)
    
    if not rows:
        print("❌ 文件内容为空")
        sys.exit(1)
    
    print(f"📥 共读取 {len(rows)} 行")
    
    # 识别表格类型
    table_type = identify_table_type(rows[0])
    print(f"🔍 识别为：{table_type}")
    
    # 解析数据
    if table_type == '房源销控表':
        records = parse_room_list(rows)
    elif table_type == '客户跟进记录':
        records = parse_customer_list(rows)
    elif table_type == '渠道跟进记录':
        records = parse_channel_list(rows)
    else:
        print("⚠️  无法识别表格类型，将按客户跟进记录解析")
        records = parse_customer_list(rows)
    
    # 预览
    preview_records(records, table_type)
    
    # 保存结果
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
            save_to_json(records, table_type, output_path)
    
    return records, table_type

if __name__ == '__main__':
    main()
