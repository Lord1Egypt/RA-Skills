#!/usr/bin/env python3
"""infoseek_archive_server.py — Infoseek 写操作 server（版本随 SKILL_VERSION 单源）
与 infoseek_mcp_server.py (search server) 拆分，实现最小权限原则

工具:
  - save_archive（写归档）
  - dedup_stats（读任务报告，但与归档操作紧密绑定，保留在此 server）

启动:
  python scripts/infoseek_archive_server.py                              # stdio
  python scripts/infoseek_archive_server.py --transport sse --port 8081 # SSE
"""
import argparse
import json
import os
import sys
from pathlib import Path

# 复用 search server 的核心实现（PROTOCOL_VERSION、handlers、tools、auth）
from infoseek_mcp_server import (
    PROTOCOL_VERSION,
    SERVER_NAME,
    SERVER_VERSION,
    TOOLS,
    handle_initialize,
    handle_tools_list,
    handle_tools_call,
    check_auth,
    run_stdio_server,
    run_sse_server,
    INFOSEEK_ROOT,
    WORKSPACE,
)

# archive server 只暴露 2 个写操作工具
ARCHIVE_TOOLS = [t for t in TOOLS if t['name'] in ('save_archive', 'dedup_stats')]

# 临时覆盖 TOOLS（archive server 只暴露 2 工具）
TOOLS.clear()
TOOLS.extend(ARCHIVE_TOOLS)

# v1.8.1 版本单源化：移除本地 SERVER_VERSION = "1.7.0" 覆盖（曾致对外版本倒挂）；
# 沿用 mcp_tools_common.SKILL_VERSION（经 infoseek_mcp_server import 转手）。
SERVER_NAME = "infoseek-archive"


def main():
    parser = argparse.ArgumentParser(description=f'Infoseek Archive Server v{SERVER_VERSION} (写操作)')
    parser.add_argument('--transport', default='stdio', choices=['stdio', 'sse'])
    parser.add_argument('--port', type=int, default=8081, help='SSE 端口（默认 8081，与 search 错开）')
    parser.add_argument('--require-token', action='store_true')
    parser.add_argument('--token', default=None)
    parser.add_argument('--list-tools', action='store_true')
    args = parser.parse_args()

    if args.list_tools:
        print(json.dumps(ARCHIVE_TOOLS, ensure_ascii=False, indent=2))
        return

    print(f"[infoseek-archive] server v{SERVER_VERSION} starting (写操作 server)", file=sys.stderr)

    if args.transport == 'stdio':
        run_stdio_server()
    elif args.transport == 'sse':
        run_sse_server(
            port=args.port,
            require_token=args.require_token,
            fixed_token=args.token
        )


if __name__ == '__main__':
    main()