#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw MCP Client - 通过 Model Context Protocol 连接外部服务
原创实现，使用 Anthropic 官方 MCP Python SDK
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json
import asyncio
import argparse
from pathlib import Path


def check_sdk():
    """检查 MCP SDK 是否安装"""
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        return True
    except ImportError:
        print("❌ MCP Python SDK 未安装")
        print("   安装: pip install mcp")
        return False


async def list_tools(server_cmd, server_args):
    """列出 MCP Server 可用的工具"""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=server_cmd,
        args=server_args
    )

    print(f"\n🔌 连接 MCP Server: {server_cmd} {' '.join(server_args)}")
    print(f"{'='*50}")

    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()

                if not tools.tools:
                    print("  该 Server 没有暴露任何工具")
                    return

                print(f"\n📦 可用工具 ({len(tools.tools)}):")
                for t in tools.tools:
                    print(f"\n  🛠️  {t.name}")
                    if t.description:
                        print(f"     📝 {t.description[:100]}")
                    if t.inputSchema:
                        props = t.inputSchema.get('properties', {})
                        if props:
                            print(f"     参数: {', '.join(props.keys())}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")


async def call_tool(server_cmd, server_args, tool_name, args_dict):
    """调用 MCP 工具"""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=server_cmd,
        args=server_args
    )

    print(f"\n🔌 调用: {tool_name}")
    print(f"{'='*50}")
    print(f"参数: {json.dumps(args_dict, ensure_ascii=False, indent=2)}")

    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments=args_dict)

                print(f"\n📤 结果:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(f"\n{content.text}")
                    else:
                        print(f"\n{content}")
    except Exception as e:
        print(f"❌ 调用失败: {e}")


async def main():
    parser = argparse.ArgumentParser(description="OpenClaw MCP Client")
    parser.add_argument('action', choices=['tools', 'call'], help='操作')
    parser.add_argument('--server', required=True, help='MCP Server 命令 (如 node, python)')
    parser.add_argument('--args', default='', help='Server 参数 (如 "server.js")')
    parser.add_argument('--tool', help='要调用的工具名称')
    parser.add_argument('--params', help='工具参数 (JSON 格式)')

    args = parser.parse_args()

    if not check_sdk():
        sys.exit(1)

    server_args = args.args.split() if args.args else []

    if args.action == 'tools':
        await list_tools(args.server, server_args)
    elif args.action == 'call':
        if not args.tool:
            print("❌ 调用工具需要 --tool 参数")
            sys.exit(1)
        params = json.loads(args.params) if args.params else {}
        await call_tool(args.server, server_args, args.tool, params)


if __name__ == '__main__':
    asyncio.run(main())
