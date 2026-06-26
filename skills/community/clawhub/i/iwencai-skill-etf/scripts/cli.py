#!/usr/bin/env python3
"""
同花顺智能选ETF - ETF数据查询CLI
使用Python标准库实现，无第三方依赖
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error


DEFAULT_API_URL = "https://openapi.iwencai.com/v1/query2data"
DEFAULT_PAGE = "1"
DEFAULT_LIMIT = "10"
DEFAULT_IS_CACHE = "1"
DEFAULT_SOURCE = "test"
DEFAULT_EXPAND_INDEX = "true"


class ETFSelectorAPIError(Exception):
    """API错误异常类"""
    def __init__(self, message: str, status_code: int = None, response: str = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="同花顺智能选ETF - ETF数据查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python scripts/cli.py --query "沪深300ETF有哪些？"
  python scripts/cli.py --query "规模最大的ETF" --page "1" --limit "20"
  python scripts/cli.py --query "创业板ETF" --api-key "your-key"

环境变量:
  IWENCAI_API_KEY   API密钥
  IWENCAI_API_URL   API地址（默认使用环境变量IWENCAI_API_URL的值）
        """
    )

    parser.add_argument(
        "--query", "-q",
        type=str,
        required=True,
        help="查询字符串（必填）"
    )

    parser.add_argument(
        "--page",
        type=str,
        default=DEFAULT_PAGE,
        help=f"分页参数（默认: {DEFAULT_PAGE}）"
    )

    parser.add_argument(
        "--limit",
        type=str,
        default=DEFAULT_LIMIT,
        help=f"每页条数（默认: {DEFAULT_LIMIT}）"
    )

    parser.add_argument(
        "--is-cache",
        type=str,
        default=DEFAULT_IS_CACHE,
        help=f"缓存参数（默认: {DEFAULT_IS_CACHE}）"
    )

    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API密钥（默认从环境变量IWENCAI_API_KEY读取）"
    )

    return parser.parse_args()


def query_etf(query: str, page: str, limit: str,
             is_cache: str, api_key: str) -> list:
    """
    调用ETF数据查询接口

    Args:
        query: 查询字符串
        page: 分页参数
        limit: 每页条数
        is_cache: 缓存参数
        api_key: API密钥

    Returns:
        datas数组

    Raises:
        ETFSelectorAPIError: API调用失败时抛出
    """
    # 获取API密钥
    if not api_key:
        api_key = os.environ.get("IWENCAI_API_KEY", "")
    if not api_key:
        raise ETFSelectorAPIError("API密钥未设置，请通过参数或环境变量IWENCAI_API_KEY指定")

    # 构造请求数据
    payload = {
        "query": query,
        "source": DEFAULT_SOURCE,
        "page": DEFAULT_PAGE,
        "limit": DEFAULT_LIMIT,
        "is_cache": DEFAULT_IS_CACHE,
        "expand_index": DEFAULT_EXPAND_INDEX
    }

    # 构造请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 创建请求对象
    api_url = DEFAULT_API_URL
    request = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        # 发送请求
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body)

            # 检查响应是否包含错误
            if isinstance(result, dict):
                # 返回datas字段
                if "datas" in result:
                    return result["datas"]
                # 检查是否有错误信息
                if "code" in result and result["code"] != 0:
                    message = result.get("message", "未知错误")
                    raise ETFSelectorAPIError(f"API返回错误: {message}")
                return result if result else []
            return result if result else []

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise ETFSelectorAPIError(
            f"HTTP错误 {e.code}: {e.reason}",
            status_code=e.code,
            response=error_body
        )
    except urllib.error.URLError as e:
        raise ETFSelectorAPIError(f"网络错误: {e.reason}")
    except json.JSONDecodeError as e:
        raise ETFSelectorAPIError(f"响应解析失败: {e}")


def main():
    """主函数"""
    args = parse_args()

    try:
        datas = query_etf(
            query=args.query,
            page=args.page,
            limit=args.limit,
            is_cache=args.is_cache,
            api_key=args.api_key
        )

        # 输出结果（JSON格式）
        output = {
            "success": True,
            "query": args.query,
            "count": len(datas),
            "datas": datas
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    except ETFSelectorAPIError as e:
        error_output = {
            "success": False,
            "error": e.message
        }
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        error_output = {
            "success": False,
            "error": f"发生错误: {str(e)}"
        }
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
