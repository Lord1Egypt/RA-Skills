#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
捷帮时区转换工具 - 提供全球时区查询和时间转换功能
API基础URL: https://www.jiebang.site
"""

import os
import json
from coze_workload_identity import requests


# API基础配置
BASE_URL = "https://www.jiebang.site"

# 占位skill_id，创建草稿后需替换
def get_admin_key():
    """从环境变量获取Admin Key"""
    admin_key = os.getenv("COZE_JIEBANG_ADMIN_KEY_7647547445039104038")
    if not admin_key:
        raise ValueError("缺少凭证配置，请检查环境变量 COZE_JIEBANG_ADMIN_KEY")
    return admin_key


def get_headers():
    """构建请求头，包含鉴权信息"""
    return {
        "Content-Type": "application/json",
        "X-Admin-Key": get_admin_key()
    }


def timezone_convert(time_str: str, from_tz: str, to_tz: str) -> dict:
    """
    时区转换
    
    Args:
        time_str: 要转换的时间
        from_tz: 源时区
        to_tz: 目标时区
        
    Returns:
        转换结果
    """
    api_url = f"{BASE_URL}/api/timezone-convert"
    
    payload = {
        "time": time_str,
        "from": from_tz,
        "to": to_tz
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


def timezone_query(timezone: str) -> dict:
    """
    查询时区当前时间
    
    Args:
        timezone: 时区名称
        
    Returns:
        查询结果
    """
    api_url = f"{BASE_URL}/api/timezone-query"
    
    try:
        params = {"timezone": timezone}
        response = requests.get(
            api_url,
            headers=get_headers(),
            params=params,
            timeout=30
        )
        
        if response.status_code >= 400:
            # 尝试POST
            response = requests.post(
                api_url,
                headers=get_headers(),
                json={"timezone": timezone},
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
    
    parser = argparse.ArgumentParser(description="捷帮时区转换工具")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")
    
    # 时区转换
    convert_parser = subparsers.add_parser("convert", help="时区转换")
    convert_parser.add_argument("--time", required=True, help="要转换的时间")
    convert_parser.add_argument("--from-tz", required=True, help="源时区")
    convert_parser.add_argument("--to-tz", required=True, help="目标时区")
    
    # 时区查询
    query_parser = subparsers.add_parser("query", help="查询时区当前时间")
    query_parser.add_argument("--timezone", required=True, help="时区名称")
    
    args = parser.parse_args()
    
    if args.action == "convert":
        result = timezone_convert(args.time, args.from_tz, args.to_tz)
    elif args.action == "query":
        result = timezone_query(args.timezone)
    else:
        print("请指定操作类型: convert / query")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
