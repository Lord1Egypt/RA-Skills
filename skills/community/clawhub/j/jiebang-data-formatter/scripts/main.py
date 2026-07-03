#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
捷帮数据格式化工具 - 提供多种数据格式转换功能
API基础URL: https://www.jiebang.site
"""

import os
import json
from coze_workload_identity import requests


# API基础配置
BASE_URL = "https://www.jiebang.site"


def get_admin_key():
    """从环境变量获取Admin Key"""
    admin_key = os.getenv("COZE_JIEBANG_ADMIN_KEY_7647541396387201070")
    if not admin_key:
        raise ValueError("缺少凭证配置，请检查环境变量 COZE_JIEBANG_ADMIN_KEY")
    return admin_key


def get_headers():
    """构建请求头，包含鉴权信息"""
    return {
        "Content-Type": "application/json",
        "X-Admin-Key": get_admin_key()
    }


def json_yaml_convert(data: str, direction: str, indent: int = 2) -> dict:
    """
    JSON/YAML互转
    
    Args:
        data: 要转换的数据
        direction: 转换方向 (json_to_yaml / yaml_to_json)
        indent: 缩进空格数
        
    Returns:
        转换结果
    """
    api_url = f"{BASE_URL}/api/json-yaml"
    
    payload = {
        "data": data,
        "direction": direction,
        "indent": indent
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def xml_format(data: str, action: str = "format") -> dict:
    """
    XML格式化
    
    Args:
        data: XML内容
        action: 操作 (format / minify / validate)
        
    Returns:
        格式化结果
    """
    api_url = f"{BASE_URL}/api/xml-format"
    
    payload = {
        "data": data,
        "action": action
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def sql_format(sql: str, keyword_upper: bool = True, indent: int = 2) -> dict:
    """
    SQL格式化
    
    Args:
        sql: SQL语句
        keyword_upper: 关键字大写
        indent: 缩进空格数
        
    Returns:
        格式化结果
    """
    api_url = f"{BASE_URL}/api/sql-format"
    
    payload = {
        "sql": sql,
        "keyword_upper": keyword_upper,
        "indent": indent
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def base_convert(value: str, from_base: int, to_base: int) -> dict:
    """
    进制转换
    
    Args:
        value: 要转换的数值
        from_base: 源进制
        to_base: 目标进制
        
    Returns:
        转换结果
    """
    api_url = f"{BASE_URL}/api/base-convert"
    
    payload = {
        "value": value,
        "from_base": from_base,
        "to_base": to_base
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def html_entity(data: str, action: str) -> dict:
    """
    HTML实体编解码
    
    Args:
        data: 要处理的内容
        action: 操作 (encode / decode)
        
    Returns:
        处理结果
    """
    api_url = f"{BASE_URL}/api/html-entity"
    
    payload = {
        "data": data,
        "action": action
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def cron_parse(expression: str, next_runs: int = 5) -> dict:
    """
    Cron表达式解析
    
    Args:
        expression: Cron表达式
        next_runs: 返回下次执行次数
        
    Returns:
        解析结果
    """
    api_url = f"{BASE_URL}/api/cron-parse"
    
    payload = {
        "expression": expression,
        "next_runs": next_runs
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def main():
    """主函数，处理命令行参数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="捷帮数据格式化工具")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")
    
    # JSON/YAML转换
    json_yaml_parser = subparsers.add_parser("json-yaml", help="JSON/YAML互转")
    json_yaml_parser.add_argument("--data", required=True, help="要转换的数据")
    json_yaml_parser.add_argument("--direction", required=True, 
                                  choices=["json_to_yaml", "yaml_to_json"],
                                  help="转换方向")
    json_yaml_parser.add_argument("--indent", type=int, default=2, help="缩进")
    
    # XML格式化
    xml_parser = subparsers.add_parser("xml", help="XML格式化")
    xml_parser.add_argument("--data", required=True, help="XML内容")
    xml_parser.add_argument("--action", default="format", 
                           choices=["format", "minify", "validate"],
                           help="操作")
    
    # SQL格式化
    sql_parser = subparsers.add_parser("sql", help="SQL格式化")
    sql_parser.add_argument("--sql", required=True, help="SQL语句")
    sql_parser.add_argument("--keyword-upper", type=bool, default=True, help="关键字大写")
    sql_parser.add_argument("--indent", type=int, default=2, help="缩进")
    
    # 进制转换
    base_parser = subparsers.add_parser("base", help="进制转换")
    base_parser.add_argument("--value", required=True, help="要转换的值")
    base_parser.add_argument("--from-base", type=int, required=True, help="源进制")
    base_parser.add_argument("--to-base", type=int, required=True, help="目标进制")
    
    # HTML实体
    html_parser = subparsers.add_parser("html-entity", help="HTML实体编解码")
    html_parser.add_argument("--data", required=True, help="要处理的内容")
    html_parser.add_argument("--action", required=True, choices=["encode", "decode"],
                            help="操作")
    
    # Cron解析
    cron_parser = subparsers.add_parser("cron", help="Cron表达式解析")
    cron_parser.add_argument("--expression", required=True, help="Cron表达式")
    cron_parser.add_argument("--next-runs", type=int, default=5, help="下次执行次数")
    
    args = parser.parse_args()
    
    if args.action == "json-yaml":
        result = json_yaml_convert(args.data, args.direction, args.indent)
    elif args.action == "xml":
        result = xml_format(args.data, args.action)
    elif args.action == "sql":
        result = sql_format(args.sql, args.keyword_upper, args.indent)
    elif args.action == "base":
        result = base_convert(args.value, args.from_base, args.to_base)
    elif args.action == "html-entity":
        result = html_entity(args.data, args.action)
    elif args.action == "cron":
        result = cron_parse(args.expression, args.next_runs)
    else:
        print("请指定操作类型")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
