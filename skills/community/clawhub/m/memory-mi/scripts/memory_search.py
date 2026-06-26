#!/usr/bin/env python3
"""
记忆搜索脚本 - 调用外部 API 服务检索用户对话记忆
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


def search(
    user_id: str,
    query: str,
    timezone: str = DEFAULT_TIMEZONE,
    limit: int = 3
) -> Dict[str, Any]:
    """
    主搜索接口：
    - 调用外部 API 服务搜索记忆
    - 返回按层级（L0/L1/L2）组织的记忆
    """
    # 构建请求体
    payload = {
        "user_id": user_id,
        "query": query,
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
        with request.urlopen(req, timeout=15) as resp:
            response_body = resp.read().decode('utf-8')
            try:
                api_result = json.loads(response_body)
            except json.JSONDecodeError:
                api_result = {"raw_response": response_body}

            # 解析 API 返回的记忆结果（处理中文 key）
            # API 返回格式: {"l0记忆": "...", "l1记忆": "...", "l2记忆": "...", ...}
            l0_content = api_result.get("l0记忆", "")
            l1_content = api_result.get("l1记忆", "")
            l2_content = api_result.get("l2记忆", "")
            session_content = api_result.get("session_memories_raw", "")

            # 保持与原接口兼容的输出格式
            result = {
                "l0": l0_content,
                "l1": l1_content,
                "l2": l2_content,
                "session": session_content,
                "api_response": api_result,
                "status_code": resp.status
            }

            return result

    except error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            "l0": "",
            "l1": "",
            "l2": "",
            "session": "",
            "error": f"HTTP {e.code}: {error_body}",
            "status_code": e.code
        }

    except error.URLError as e:
        return {
            "l0": "",
            "l1": "",
            "l2": "",
            "session": "",
            "error": f"URL Error: {e.reason}"
        }

    except TimeoutError:
        return {
            "l0": "",
            "l1": "",
            "l2": "",
            "session": "",
            "error": "Request timeout: API took too long to respond"
        }

    except Exception as e:
        return {
            "l0": "",
            "l1": "",
            "l2": "",
            "session": "",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Search memories via external API service')
    parser.add_argument('--user-id', required=True, help='User unique identifier')
    parser.add_argument('--query', required=True, help='Search query (keywords)')
    parser.add_argument('--timezone', default=DEFAULT_TIMEZONE, help='User timezone')
    parser.add_argument('--limit', type=int, default=3, help='Max results per level (kept for compatibility)')

    args = parser.parse_args()

    try:
        # 执行搜索
        result = search(
            user_id=args.user_id,
            query=args.query,
            timezone=args.timezone,
            limit=args.limit
        )

        # 检查是否有错误
        if result.get("error"):
            output = {
                "success": False,
                "error": result["error"],
                "user_id": args.user_id,
                "query": args.query,
                "memories": {"l0": "", "l1": "", "l2": "", "session": ""},
                "found": False,
                "count": 0
            }
            print(json.dumps(output, ensure_ascii=False, indent=2), file=sys.stderr)
            return 1

        # 检查是否有任何记忆
        has_memories = any(result[level] for level in ["l0", "l1", "l2", "session"] if level in result)

        # 构建输出
        output = {
            "success": True,
            "user_id": args.user_id,
            "query": args.query,
            "memories": {
                "l0": result.get("l0", ""),
                "l1": result.get("l1", ""),
                "l2": result.get("l2", ""),
                "session": result.get("session", "")
            },
            "found": has_memories,
            "count": sum(1 for level in ["l0", "l1", "l2", "session"] if result.get(level)),
            "api_response": result.get("api_response")
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "user_id": args.user_id,
            "query": args.query,
            "memories": {"l0": "", "l1": "", "l2": "", "session": ""},
            "found": False,
            "count": 0
        }
        print(json.dumps(error_result, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
