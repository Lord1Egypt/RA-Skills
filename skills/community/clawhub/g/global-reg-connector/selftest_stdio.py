#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球法规连接器 · stdio 协议层自检（可重跑）
=====================================================
通过 FastMCP 官方 Client 走真实 stdio 协议调用 4 个工具，验证 MCP 链路。
退出码 0 = 全部通过。

运行: python selftest_stdio.py
"""
import asyncio
import json
import sys
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

PY = sys.executable
CWD = Path(__file__).parent


async def main() -> int:
    t = StdioTransport(command=PY, args=["reg_connector_server.py"], cwd=str(CWD))
    async with Client(t) as client:
        tools = await client.list_tools()
        names = [x.name for x in tools]
        expected = ["list_hubs", "search_regulation", "get_hub", "ask_classification"]
        assert names == expected, f"工具列表不符: {names}"
        print("✅ 工具列表:", names)

        r = await client.call_tool("list_hubs", {})
        data = json.loads(r.data)
        print(f"✅ list_hubs -> {len(data)} 个枢纽")

        r = await client.call_tool("search_regulation", {"query": "ISO 10993 生物相容性", "top_k": 3})
        data = json.loads(r.data)
        print(f"✅ search_regulation -> {data['count']} 条, top1: {data['results'][0]['hub_title']}")

        r = await client.call_tool("get_hub", {"hub_key": "风险管理枢纽"})
        data = json.loads(r.data)
        print(f"✅ get_hub -> {data['title']}")

        r = await client.call_tool("ask_classification", {"product": "一次性使用输液器"})
        data = json.loads(r.data)
        print(f"✅ ask_classification -> matches {len(data['matches'])} 条")

        print("\n✅ MCP stdio 协议层自检全部通过")
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
