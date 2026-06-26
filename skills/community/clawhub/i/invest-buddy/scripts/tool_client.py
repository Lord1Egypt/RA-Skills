#!/usr/bin/env python3
"""
Investment Research Tools - HTTP API Client

调用 投资研究工具的 HTTP API 客户端脚本。
通过环境变量或命令行参数配置 API URL 和 Token。

使用示例:
    python tool_client.py --tool extract_assets --text "分析下茅台"
    python tool_client.py --tool get_asset_overview --symbol 600519.SH
    python tool_client.py --tool analyze_technical --symbol 600519.SH
"""

import argparse
import json
import os
import sys
from typing import Any

try:
    import requests
except ImportError:
    print("Error: requests is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


# 支持的工具列表
AVAILABLE_TOOLS = [
    "extract_assets",
    "investment_search_pro",
    "get_asset_overview",
    "analyze_fundamentals_financial",
    "analyze_fundamentals_valuation",
    "analyze_technical",
    "analyze_capital_flow",
    "analyze_market_sentiment",
]


def get_api_config() -> tuple[str, str]:
    """获取 API 配置"""
    # 优先使用新的环境变量名
    api_url = os.getenv("TOOL_API_URL", 'https://api.facaidazi.com/api/tools/call')
    api_token = os.getenv("TOOL_API_TOKEN")

    if not api_token:
        raise ValueError(
            "TOOL_API_TOKEN is required. "
            "Set it via environment variable or in .env file"
        )

    return api_url, api_token


def call_tool(
    tool_name: str,
    parameters: dict[str, Any],
    api_url: str,
    api_token: str,
    timeout: float = 300.0,
) -> dict[str, Any]:
    """
    调用工具

    Args:
        tool_name: 工具名称
        parameters: 工具参数
        api_url: API 端点
        api_token: Bearer Token
        timeout: 请求超时时间（秒）

    Returns:
        API 响应结果

    Raises:
        requests.RequestException: 请求失败
        ValueError: 响应格式错误
    """
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    data = {"tool_name": tool_name, "parameters": parameters}

    try:
        response = requests.post(api_url, json=data, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"Request failed: {e}") from e


def main():
    parser = argparse.ArgumentParser(
        description="Call Investment Research Tools via HTTP API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available tools:
  extract_assets                    从文本提取资产
  investment_search_pro             检索专业投资信息
  get_asset_overview               获取资产快速概览
  analyze_fundamentals_financial   分析基本面-财务
  analyze_fundamentals_valuation   分析基本面-估值
  analyze_technical                分析技术面
  analyze_capital_flow             分析资金面
  analyze_market_sentiment         分析市场观点

Examples:
  # Extract assets from text
  python tool_client.py --tool extract_assets --text "分析下茅台"

  # Search for investment information
  python tool_client.py --tool investment_search_pro --query "宁德时代 2025年业绩"

  # Get asset overview
  python tool_client.py --tool get_asset_overview --symbol 600519.SH

  # Analyze technical indicators
  python tool_client.py --tool analyze_technical --symbol 600519.SH

  # Full deep analysis (bash)
  for tool in analyze_fundamentals_financial analyze_fundamentals_valuation analyze_technical analyze_capital_flow analyze_market_sentiment; do
    python tool_client.py --tool $tool --symbol 600519.SH
  done
        """,
    )

    parser.add_argument("--tool", required=True, choices=AVAILABLE_TOOLS, help="Tool name")
    parser.add_argument("--symbol", help="Stock symbol (e.g., 600519.SH,务必带上symbol后缀)")
    parser.add_argument("--text", help="Text input for extract_assets")
    parser.add_argument("--query", help="Query text for investment_search_pro")
    parser.add_argument("--timeout", type=float, default=300.0, help="Request timeout in seconds")
    parser.add_argument("--output", default="text", choices=["text", "json"], help="Output format")
    parser.add_argument("--indent", type=int, default=2, help="JSON indent level")

    args = parser.parse_args()

    try:
        api_url, api_token = get_api_config()
    except ValueError:
        parser.error("TOOL_API_TOKEN is required. Set via environment variable or in .env file")

    # 构建参数
    params = {}
    if args.tool == "extract_assets":
        if not args.text:
            parser.error("--text is required for extract_assets tool")
        params["text"] = args.text
    elif args.tool == "investment_search_pro":
        if not args.query:
            parser.error("--query is required for investment_search_pro tool")
        params["query"] = args.query
    else:
        if not args.symbol:
            parser.error("--symbol is required for analysis tools")
        params["symbol"] = args.symbol

    try:
        result = call_tool(args.tool, params, api_url, api_token, args.timeout)

        if args.output == "json":
            print(json.dumps(result, indent=args.indent, ensure_ascii=False))
        else:
            print(result.get("result", json.dumps(result)))

    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
