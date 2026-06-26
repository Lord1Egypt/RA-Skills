#!/usr/bin/env python3
"""
麦当劳 MCP 工具调用脚本
Usage: python3 mcp_call.py <tool_name> [json_arguments]
"""

import json
import os
import sys
import urllib.request
import urllib.error

MCP_URL = "https://mcp.mcd.cn"
MCP_TOKEN = os.environ.get("MCD_MCP_TOKEN", "")

def call_mcp_tool(tool_name: str, arguments: dict = None) -> dict:
    """调用麦当劳 MCP 工具"""
    if not MCP_TOKEN:
        raise ValueError("MCD_MCP_TOKEN 环境变量未设置")

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }

    headers = {
        "Authorization": f"Bearer {MCP_TOKEN}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8')}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 mcp_call.py <tool_name> [json_arguments]")
        print("\n可用工具:")
        print("  available-coupons     - 查询可领优惠券")
        print("  query-my-coupons      - 查询我的优惠券")
        print("  auto-bind-coupons     - 自动领取优惠券")
        print("  query-my-account      - 查询积分账户")
        print("  mall-points-products  - 查询积分商品")
        print("  delivery-query-addresses - 查询配送地址")
        print("  query-meals           - 查询餐品菜单")
        print("  campaign-calendar     - 营销活动日历")
        print("  list-nutrition-foods  - 营养成分数据")
        sys.exit(1)

    tool_name = sys.argv[1]
    arguments = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    result = call_mcp_tool(tool_name, arguments)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
