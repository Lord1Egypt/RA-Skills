#!/usr/bin/env python3
"""
记忆添加脚本 - 调用外部 API 服务保存记忆
"""

import argparse
import json
import sys
import os
from typing import Dict, Any
from urllib import request, error


# API 配置
API_URL = ""
API_TOKEN = ""
DEFAULT_TIMEZONE = "Asia/Shanghai"


def add(
    user_id: str,
    query: str,
    response: str,
    timezone: str = DEFAULT_TIMEZONE
) -> Dict[str, Any]:
    """
    记忆处理接口：
    - 调用外部 API 服务保存记忆
    - 返回成功/失败标识
    """
    # 构建请求体
    payload = {
        "user_id": user_id,
        "query": query,
        "response": response,
        "history": [],
        "timezone": timezone
    }
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    # 发送 POST 请求
    req = request.Request(
        API_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with request.urlopen(req, timeout=10) as resp:
            response_body = resp.read().decode('utf-8')
            try:
                api_result = json.loads(response_body)
            except json.JSONDecodeError:
                api_result = {"raw_response": response_body}
            
            return {
                "success": True,
                "api_response": api_result,
                "status_code": resp.status
            }
            
    except error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            "success": False,
            "error": f"HTTP {e.code}: {error_body}",
            "status_code": e.code
        }
        
    except error.URLError as e:
        return {
            "success": False,
            "error": f"URL Error: {e.reason}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Add memories via external API service')
    parser.add_argument('--user-id', required=True, help='User unique identifier')
    parser.add_argument('--query', required=True, help='User query text')
    parser.add_argument('--response', required=True, help='AI response text')
    parser.add_argument('--timezone', default=DEFAULT_TIMEZONE, help='User timezone (default: Asia/Shanghai)')
    
    args = parser.parse_args()
    
    try:
        # 调用 add 函数
        result = add(
            user_id=args.user_id,
            query=args.query,
            response=args.response,
            timezone=args.timezone
        )
        
        output = {
            "success": result.get("success", False),
            "user_id": args.user_id,
            "memory_saved": result.get("success", False),
            "api_response": result.get("api_response")
        }
        
        if not result.get("success"):
            output["error"] = result.get("error")
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if result.get("success") else 1
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_result, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
