#!/usr/bin/env python3
"""
招投标数据查询脚本

功能：查询招投标数据，支持自然语言查询和时间范围筛选
授权方式：Token 通过 HTTP Header 传递
凭证文件：references/api_key.md

时间限制：默认查询近3个自然年的数据，超过3个自然年的请求会被拒绝
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({"error": "缺少依赖包：requests。请执行 pip install requests"}, ensure_ascii=False))
    sys.exit(1)


def get_api_key():
    """
    从配置文件获取API Key
    
    Returns:
        str: API Key
    
    Raises:
        Exception: 凭证文件不存在或为空
    """
    # 配置文件路径
    script_dir = Path(__file__).parent.parent
    api_key_file = script_dir / "references" / "api_key.md"
    
    # 检查文件是否存在
    if not api_key_file.exists():
        raise Exception("API Key 配置文件不存在。请先配置 API Key。")
    
    # 读取文件内容
    api_key = api_key_file.read_text(encoding="utf-8").strip()
    
    # 检查内容是否为空
    if not api_key:
        raise Exception("API Key 配置文件为空。请先配置 API Key。")
    
    return api_key


def save_api_key(api_key):
    """
    保存API Key到配置文件
    
    Args:
        api_key: API Key 字符串
    
    Raises:
        Exception: API Key 为空或文件写入失败
    """
    if not api_key or not api_key.strip():
        raise Exception("API Key 不能为空")
    
    # 配置文件路径
    script_dir = Path(__file__).parent.parent
    api_key_file = script_dir / "references" / "api_key.md"
    
    # 确保目录存在
    api_key_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存 API Key
    try:
        api_key_file.write_text(api_key.strip(), encoding="utf-8")
    except Exception as e:
        raise Exception(f"保存 API Key 失败: {str(e)}")


def get_three_years_ago_timestamp():
    """
    获取3个自然年前1月1日的时间戳（毫秒）
    
    说明：3个自然年指当前年份及前两年
    例如：当前是2026年，则包含2024、2025、2026年，开始时间为2024年1月1日
    
    Returns:
        int: 3个自然年前1月1日 00:00:00 的时间戳（毫秒）
    """
    current_date = datetime.now()
    current_year = current_date.year
    start_year = current_year - 2  # 当前年份减2年，包含3个自然年
    
    # 创建3个自然年前1月1日 00:00:00的时间对象
    date_obj = datetime(start_year, 1, 1, 0, 0, 0)
    
    # 转换为时间戳（毫秒）
    return int(date_obj.timestamp() * 1000)


def get_current_timestamp():
    """
    获取当前时间戳（毫秒）
    
    Returns:
        int: 当前时间戳（毫秒）
    """
    return int(datetime.now().timestamp() * 1000)


def query_bidding(query, start_time=None, end_time=None, top_k=10):
    """
    查询招投标数据
    
    时间限制：只能查询近3个自然年的数据
    
    Args:
        query: 用户提问的文本内容（必填）
        start_time: 开始时间戳（毫秒），默认近3个自然年
        end_time: 结束时间戳（毫秒），默认当前时间
        top_k: 召回条数，默认10
    
    Returns:
        list: API返回的数据列表
    
    Raises:
        Exception: 参数验证失败、凭证缺失、时间范围超过3个自然年或API调用失败
    """
    # 1. 获取凭证
    api_key = get_api_key()
    
    # 2. 参数验证
    if not query or not query.strip():
        raise Exception("query参数不能为空")
    
    # 3. 时间范围处理
    three_years_ago_timestamp = get_three_years_ago_timestamp()
    
    # 如果用户未提供开始时间，使用3年前1月1日
    actual_start_time = start_time if start_time is not None else three_years_ago_timestamp
    
    # 如果用户未提供结束时间，使用当前时间
    actual_end_time = end_time if end_time is not None else get_current_timestamp()
    
    # 验证时间范围是否超过3个自然年
    if actual_start_time < three_years_ago_timestamp:
        raise Exception("对不起，无法查询超过3个自然年之前的招投标信息。请调整查询时间范围。")
    
    # 4. 构建请求参数
    url = "https://mcp.mysteel.com/mcp/info/vector/rag-search"
    headers = {
        "Content-Type": "application/json",
        "token": api_key
    }
    
    payload = {
        "query": query,
        "startTime": actual_start_time,
        "endTime": actual_end_time,
        "topK": top_k,
        "innerType": 18,
        "onlyOriginData": True
    }
    
    # 5. 发起请求
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
        
        data = response.json()
    except requests.exceptions.Timeout:
        raise Exception("请求超时（30秒）")
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")
    
    # 6. 错误处理
    if data.get("code") == "400":
        raise Exception("Token校验失败，请重新配置API Key")
    
    if data.get("code") == "401":
        raise Exception("接口异常，请稍后重试")
    
    if data.get("code") != "200":
        raise Exception(f"接口错误: {data.get('message', '未知错误')}")
    
    # 7. 返回数据
    return data.get("data", [])


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="招投标数据查询脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python bidding_api.py --query "查询钢材招标项目"
  python bidding_api.py --query "招标项目" --start_time 1704038400000 --end_time 1735660799999
  python bidding_api.py --save_api_key "your_api_key"
        """
    )
    
    parser.add_argument("--query", "-q", type=str, help="查询文本")
    parser.add_argument("--start_time", type=int, help="开始时间戳（毫秒）")
    parser.add_argument("--end_time", type=int, help="结束时间戳（毫秒）")
    parser.add_argument("--top_k", type=int, default=10, help="召回条数，默认10")
    parser.add_argument("--save_api_key", type=str, help="保存 API Key 到配置文件")
    
    args = parser.parse_args()
    
    # 如果提供了保存 API Key 参数，则保存 API Key
    if args.save_api_key:
        try:
            save_api_key(args.save_api_key)
            print(json.dumps({"success": True, "message": "API Key 已保存"}, ensure_ascii=False, indent=2))
            sys.exit(0)
        except Exception as error:
            print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
            sys.exit(1)
    
    # 查询招投标数据
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    try:
        result = query_bidding(
            query=args.query,
            start_time=args.start_time,
            end_time=args.end_time,
            top_k=args.top_k
        )
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    except Exception as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
