#!/usr/bin/env python3
"""
园区数据查询脚本
支持查询房源、租金、配套、政策等实时数据
"""

import os
import sys
import json
from pathlib import Path

# 模拟数据源（实际应对接腾讯文档API）
PARK_DATA = {
    "房源": [
        {"楼栋": "T1", "楼层": "8", "房号": "801", "面积": 256, "状态": "空置", "层高": 4.5, "承重": 500},
        {"楼栋": "T1", "楼层": "12", "房号": "1201", "面积": 228, "状态": "空置", "层高": 4.5, "承重": 500},
        {"楼栋": "T2", "楼层": "5", "房号": "502", "面积": 318, "状态": "空置", "层高": 4.2, "承重": 450},
        {"楼栋": "T1", "楼层": "3", "房号": "301", "面积": 545, "状态": "已租", "层高": 4.5, "承重": 500},
    ],
    "租金": [
        {"分区": "低区", "底价": 1.8, "物业费": 0.8, "停车费": 300},
        {"分区": "中区", "底价": 2.2, "物业费": 0.8, "停车费": 300},
        {"分区": "高区", "底价": 2.5, "物业费": 0.8, "停车费": 300},
    ],
    "配套": [
        {"类型": "食堂", "名称": "园区餐厅", "位置": "T1栋1楼", "容量": 500},
        {"类型": "公寓", "名称": "人才公寓", "位置": "园区北侧", "数量": 200},
        {"类型": "交通", "名称": "地铁站", "位置": "距离800米", "线路": "地铁5号线"},
    ],
    "政策": [
        {"类型": "人才补贴", "内容": "本科1万/硕士3万/博士5万", "条件": "园区企业员工"},
        {"类型": "税收返还", "内容": "增值税地方留存部分返还50%", "条件": "年纳税额>100万"},
        {"类型": "专项补贴", "内容": "研发投入补贴最高100万/年", "条件": "高新技术企业"},
    ]
}

def query_data(data_type, filter_key=None, filter_value=None):
    """查询园区数据"""
    if data_type not in PARK_DATA:
        return f"❌ 不支持的数据类型: {data_type}"
    
    data = PARK_DATA[data_type]
    
    # 过滤数据
    if filter_key and filter_value:
        filtered = [item for item in data if str(item.get(filter_key, "")) == str(filter_value)]
        return filtered if filtered else data
    
    return data

def format_output(data, data_type):
    """格式化输出"""
    if isinstance(data, str):
        return data
    
    output = f"📊 {data_type}查询结果（共{len(data)}条）\n\n"
    
    if data_type == "房源":
        output += "| 楼栋 | 楼层 | 房号 | 面积(㎡) | 状态 | 层高(m) | 承重(kg/㎡) |\n"
        output += "|------|------|------|----------|------|---------|-------------|\n"
        for item in data:
            output += f"| {item['楼栋']} | {item['楼层']} | {item['房号']} | {item['面积']} | {item['状态']} | {item['层高']} | {item['承重']} |\n"
    
    elif data_type == "租金":
        output += "| 分区 | 底价(元/㎡/天) | 物业费(元/㎡/月) | 停车费(元/月) |\n"
        output += "|------|----------------|-------------------|----------------|\n"
        for item in data:
            output += f"| {item['分区']} | {item['底价']} | {item['物业费']} | {item['停车费']} |\n"
    
    elif data_type == "配套":
        output += "| 类型 | 名称 | 位置 | 详情 |\n"
        output += "|------|------|------|------|\n"
        for item in data:
            detail = item.get('容量', item.get('数量', item.get('线路', '')))
            output += f"| {item['类型']} | {item['名称']} | {item['位置']} | {detail} |\n"
    
    elif data_type == "政策":
        output += "| 类型 | 内容 | 申请条件 |\n"
        output += "|------|------|----------|\n"
        for item in data:
            output += f"| {item['类型']} | {item['内容']} | {item['条件']} |\n"
    
    return output

def save_to_file(data, data_type, output_dir=None):
    """保存查询结果到文件"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
    
    os.makedirs(output_dir, exist_ok=True)
    
    from datetime import datetime
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"查询结果_{date_str}.md")
    
    formatted = format_output(data, data_type)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# 📊 园区数据查询结果\n\n")
        f.write(f"**查询时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**数据类型：** {data_type}\n\n")
        f.write(formatted)
        f.write(f"\n\n---\n*本报告由招商助手自动生成*")
    
    return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 query_park_data.py <数据类型> [过滤键] [过滤值]")
        print("示例: python3 query_park_data.py 房源 楼栋 T1")
        print("数据类型: 房源/租金/配套/政策")
        sys.exit(1)
    
    data_type = sys.argv[1]
    filter_key = sys.argv[2] if len(sys.argv) > 2 else None
    filter_value = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"🔍 开始查询 {data_type} 数据...")
    
    # 查询数据
    data = query_data(data_type, filter_key, filter_value)
    
    # 格式化输出
    formatted = format_output(data, data_type)
    print(formatted)
    
    # 保存到文件
    output_file = save_to_file(data, data_type)
    print(f"\n✅ 查询结果已保存: {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()
