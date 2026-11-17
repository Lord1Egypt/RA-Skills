#!/usr/bin/env python3
"""
美兰中心知识库同步脚本
从腾讯文档读取4个数据表并保存为本地JSON文件
"""
import json
import os
from datetime import datetime, timezone, timedelta

# 腾讯文档文件ID和sheet_id
TABLES = {
    "房源销控表": {
        "file_id": "LfrpttqlgMBR",
        "sheet_id": "t00i2h",
        "output": "房源销控表.json"
    },
    "客户跟进记录": {
        "file_id": "LvhKHMhJdlfY",
        "sheet_id": "t00i2h",
        "output": "客户跟进记录.json"
    },
    "租金报价表": {
        "file_id": "LFwHUDhfyHKP",
        "sheet_id": "t00i2h",
        "output": "租金报价表.json"
    },
    "配套资源表": {
        "file_id": "LCGvNpxtrBaY",
        "sheet_id": "t00i2h",
        "output": "配套资源表.json"
    }
}

def convert_record(record):
    """将API返回的field_values转换为友好的字段格式"""
    fields = {}
    for fv in record.get("field_values", []):
        field_name = fv.get("field", "")
        # 提取字段值（根据不同类型的字段）
        if "text_value" in fv:
            items = fv["text_value"].get("items", [])
            if items and items[0].get("text"):
                fields[field_name] = items[0]["text"]
            else:
                fields[field_name] = ""
        elif "number_value" in fv:
            fields[field_name] = fv["number_value"]
        elif "string_value" in fv:
            fields[field_name] = fv["string_value"]
        elif "option_value" in fv:
            items = fv["option_value"].get("items", [])
            if items and items[0].get("text"):
                fields[field_name] = items[0]["text"]
            else:
                fields[field_name] = ""
        else:
            fields[field_name] = ""
    return {
        "record_id": record.get("record_id", ""),
        "fields": fields
    }

def main():
    import subprocess
    import sys
    
    # 获取当前脚本的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant/projects/meilan-center/data")
    cache_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant/projects/meilan-center/cache")
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)
    
    # 获取当前时间（带时区）
    now = datetime.now(timezone(timedelta(hours=8))).isoformat()
    
    print(f"开始同步美兰中心知识库...")
    print(f"输出目录: {output_dir}")
    print(f"缓存目录: {cache_dir}")
    print()
    
    results = {}
    
    for table_name, config in TABLES.items():
        print(f"正在同步: {table_name}")
        print(f"  file_id: {config['file_id']}")
        
        # 注意：此脚本需要通过MCP工具调用腾讯文档API
        # 由于认证限制，此脚本应该通过WorkBuddy的MCP环境运行
        # 这里只是定义数据转换逻辑
        
        print(f"  数据转换逻辑已定义")
        results[table_name] = {
            "status": "pending",
            "message": "需要通过MCP环境运行"
        }
    
    print()
    print("注意：此脚本需要通过WorkBuddy的MCP环境运行。")
    print("请使用WorkBuddy内置的MCP工具来执行数据同步。")

if __name__ == "__main__":
    main()
