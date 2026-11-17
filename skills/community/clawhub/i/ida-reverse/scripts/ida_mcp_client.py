#!/usr/bin/env python3
"""
ida_mcp_client.py — OpenClaw 会话内直连 ida-pro-mcp 的 HTTP 客户端。

用途：绕过 mcporter CLI 的每调用冷启动（fork+node+配置加载 1~2s），
一次 Python 进程内可连续执行多步分析，批量操作（decompile → rename →
set_comments）时节省大量等待时间。

用法：
  # 单工具调用（等价 mcporter call ida-pro-mcp decompile --args '{...}'）
  python3 ida_mcp_client.py decompile '{"addr":"0x18005a8bc"}'

  # 批量调用（JSON Lines：每行 {"tool":..., "args":...}，按序执行）
  echo '{"tool":"decompile","args":{"addr":"0x18005a8bc"}}
  {"tool":"set_comments","args":{"items":[{"addr":"0x18005a8e6","comment":"crash here"}]}}' \
    | python3 ida_mcp_client.py --batch

  # 自省（列出服务端全部工具及参数 schema）
  python3 ida_mcp_client.py --list-tools

配置：默认 http://127.0.0.1:13337/mcp，可用环境变量 IDA_MCP_URL 覆盖。
依赖：仅 Python 3 标准库（urllib），无需 pip 安装。
"""

import json
import os
import sys
import urllib.request

URL = os.environ.get("IDA_MCP_URL", "http://127.0.0.1:13337/mcp")
_session_id = None
_req_id = 0


def _rpc(method, params=None):
    """发一条 JSON-RPC，返回 (result, error)。自动处理 session 头。"""
    global _session_id, _req_id
    _req_id += 1
    payload = {"jsonrpc": "2.0", "id": _req_id, "method": method}
    if params is not None:
        payload["params"] = params
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if _session_id:
        headers["Mcp-Session-Id"] = _session_id
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        sid = resp.headers.get("Mcp-Session-Id")
        if sid:
            _session_id = sid
        body = resp.read().decode("utf-8", "replace")

    # 兼容 SSE 帧（data: {...}）与纯 JSON
    if body.lstrip().startswith("{"):
        data = json.loads(body)
    else:
        for line in body.splitlines():
            if line.startswith("data:"):
                data = json.loads(line[5:].strip())
                break
        else:
            raise RuntimeError(f"unparseable response: {body[:200]}")

    if "error" in data and data["error"]:
        raise RuntimeError(f"RPC error: {data['error']}")
    return data.get("result"), None


def initialize():
    """MCP 握手；部分服务端要求 initialized 通知后才接受 tools/call。"""
    _rpc("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "openclaw-ida-client", "version": "1.0.0"},
    })
    try:
        # initialized 是通知：无 id、无响应体
        payload = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream"}
        if _session_id:
            headers["Mcp-Session-Id"] = _session_id
        req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                     headers=headers, method="POST")
        urllib.request.urlopen(req, timeout=30)
    except Exception:
        pass


def call_tool(name, args):
    result, _ = _rpc("tools/call", {"name": name, "arguments": args or {}})
    return result


def main():
    argv = sys.argv[1:]
    if "--list-tools" in argv:
        initialize()
        result, _ = _rpc("tools/list")
        tools = result.get("tools", [])
        for t in tools:
            props = t.get("inputSchema", {}).get("properties", {})
            req = t.get("inputSchema", {}).get("required", [])
            sig = ", ".join(
                k + ("*" if k in req else "") for k in props
            )
            print(f"{t['name']}({sig})")
        return 0

    batch_mode = "--batch" in argv
    if batch_mode:
        lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
        if not lines:
            print("no input lines", file=sys.stderr)
            return 2
        initialize()
        for line in lines:
            job = json.loads(line)
            name, args = job["tool"], job.get("args", {})
            try:
                print(json.dumps({"tool": name, "result": call_tool(name, args)},
                                 ensure_ascii=False))
            except Exception as e:
                print(json.dumps({"tool": name, "error": str(e)},
                                 ensure_ascii=False))
        return 0

    if len(argv) < 1:
        print(__doc__)
        return 2
    tool = argv[0]
    args = json.loads(argv[1]) if len(argv) > 1 else {}
    initialize()
    print(json.dumps(call_tool(tool, args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
