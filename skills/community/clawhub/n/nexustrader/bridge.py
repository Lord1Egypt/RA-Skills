#!/usr/bin/env python3
"""
OpenClaw <-> NexusTrader MCP 桥接脚本。

当 AI 调用工具时，本脚本连接到常驻的 MCP Server (SSE)，
获取 JSON 数据并转换成 AI 易读的 Markdown 表格。

Usage:
    # 检查服务器状态
    python bridge.py status

    # 查询所有持仓
    python bridge.py get_all_positions

    # 查询指定交易所持仓
    python bridge.py get_all_positions --exchange=binance

    # 查询余额
    python bridge.py get_balance --exchange=binance --account_type=USD_M_FUTURE_TESTNET

    # 查询行情
    python bridge.py get_ticker --symbol=BTCUSDT-PERP.BINANCE

    # 下单 (⚠️ 真实交易)
    python bridge.py create_order --symbol=BTCUSDT-PERP.BINANCE --side=BUY --order_type=MARKET --amount=0.001

    # 原始 JSON 输出
    python bridge.py get_all_balances --raw

    # 列出所有可用工具
    python bridge.py list_tools
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

def _load_skill_env() -> None:
    """Auto-load .env from skill directory (placed there by `nexustrader-mcp setup`)."""
    env_file = Path(__file__).resolve().parent / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip("'\""))


_load_skill_env()

DEFAULT_SERVER_URL = os.environ.get(
    "NEXUSTRADER_MCP_URL", "http://127.0.0.1:18765/sse"
)


# ── Markdown Formatting ──────────────────────────────────────────────


def _fmt_value(v) -> str:
    """Format a single value for display in markdown."""
    if v is None:
        return "—"
    if isinstance(v, float):
        if abs(v) >= 1:
            return f"{v:,.4f}"
        return f"{v:.8g}"
    if isinstance(v, list):
        return ", ".join(str(i) for i in v) if len(v) <= 5 else f"[{len(v)} items]"
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _dict_to_markdown_list(data: dict) -> str:
    lines = []
    for k, v in data.items():
        lines.append(f"- **{k}**: {_fmt_value(v)}")
    return "\n".join(lines)


def _list_to_markdown_table(rows: list[dict]) -> str:
    if not rows:
        return "_（无数据）_"

    all_keys: list[str] = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                all_keys.append(k)
                seen.add(k)

    header = "| " + " | ".join(all_keys) + " |"
    sep = "| " + " | ".join("---" for _ in all_keys) + " |"
    body_lines = []
    for row in rows:
        vals = [_fmt_value(row.get(k)) for k in all_keys]
        body_lines.append("| " + " | ".join(vals) + " |")

    return "\n".join([header, sep, *body_lines])


def format_result(tool_name: str, data) -> str:
    """Convert tool result to human-readable markdown."""
    if isinstance(data, dict):
        if "error" in data:
            return f"**❌ Error** (`{tool_name}`): {data['error']}"
        return f"### {tool_name}\n\n{_dict_to_markdown_list(data)}"

    if isinstance(data, list):
        if not data:
            return f"### {tool_name}\n\n_（无数据）_"
        if isinstance(data[0], dict):
            return f"### {tool_name}\n\n{_list_to_markdown_table(data)}"
        return f"### {tool_name}\n\n" + "\n".join(f"- {_fmt_value(v)}" for v in data)

    return f"### {tool_name}\n\n{data}"


# ── Daemon Auto-Start ────────────────────────────────────────────────

_DAEMON_SH = Path(__file__).resolve().parent / "nexustrader_daemon.sh"
_AUTOSTART_TIMEOUT = 90  # seconds to wait for daemon after auto-start


def _daemon_start() -> bool:
    """Attempt to start the daemon in the background. Returns True if command succeeded."""
    if not _DAEMON_SH.is_file():
        return False
    result = subprocess.run(
        ["bash", str(_DAEMON_SH), "start"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


async def _wait_for_server(server_url: str, timeout: int = _AUTOSTART_TIMEOUT) -> bool:
    """Poll until server is reachable or timeout expires. Returns True if online."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        info = await _check_status_raw(server_url)
        if info["status"] == "online":
            return True
        await asyncio.sleep(3)
    return False


async def _check_status_raw(server_url: str) -> dict:
    """Low-level status check — does not attempt auto-start."""
    from fastmcp import Client

    try:
        async with Client(server_url) as client:
            tools = await client.list_tools()
        return {"status": "online", "tools": len(tools), "url": server_url}
    except Exception as e:
        return {"status": "offline", "error": str(e), "url": server_url}


async def _ensure_server(server_url: str) -> None:
    """Ensure server is online, optionally auto-starting the daemon.

    Auto-start is DISABLED by default. To enable, set NEXUSTRADER_NO_AUTOSTART=0
    in the skill's .env file (~/.openclaw/skills/nexustrader/.env).
    """
    info = await _check_status_raw(server_url)
    if info["status"] == "online":
        return

    _proj = os.environ.get("NEXUSTRADER_PROJECT_DIR", "~/NexusTrader-mcp")

    # Auto-start is opt-in: only when explicitly set to "0"
    if os.environ.get("NEXUSTRADER_NO_AUTOSTART", "1") != "0":
        raise RuntimeError(
            "NexusTrader MCP 服务器未运行。请手动启动：\n"
            f"  cd {_proj} && uv run nexustrader-mcp start\n\n"
            "如需允许自动启动，在 ~/.openclaw/skills/nexustrader/.env 中设置：\n"
            "  NEXUSTRADER_NO_AUTOSTART=0"
        )

    print(
        "⚠️  NexusTrader MCP server offline — auto-start enabled, starting daemon...\n"
        "    Command: uv run nexustrader-mcp start (background process)\n"
        "    API keys in use: "
        f"{_proj}/.keys/.secrets.toml\n"
        "    To disable auto-start: set NEXUSTRADER_NO_AUTOSTART=1 in skill .env",
        file=sys.stderr,
    )

    started = _daemon_start()
    _proj = os.environ.get("NEXUSTRADER_PROJECT_DIR", "~/NexusTrader-mcp")
    if not started:
        raise RuntimeError(
            "NexusTrader MCP 服务器启动失败。请手动运行：\n"
            f"  uv --directory {_proj} run nexustrader-mcp start"
        )

    print(
        f"⏳ Waiting for server to initialize (up to {_AUTOSTART_TIMEOUT}s)...",
        file=sys.stderr,
    )
    online = await _wait_for_server(server_url, timeout=_AUTOSTART_TIMEOUT)
    if not online:
        raise RuntimeError(
            "服务器未在超时时间内上线。查看日志：\n"
            f"  uv --directory {_proj} run nexustrader-mcp logs"
        )
    print("✅ Server is now online.", file=sys.stderr)


# ── MCP Client Operations ────────────────────────────────────────────


async def _call_tool(server_url: str, tool_name: str, arguments: dict) -> str:
    """Connect to MCP server and call a tool, auto-starting daemon if offline."""
    from fastmcp import Client

    await _ensure_server(server_url)

    async with Client(server_url) as client:
        result = await client.call_tool(tool_name, arguments)

    # fastmcp ≥ 2.x returns CallToolResult(content=[...])
    content = result.content if hasattr(result, "content") else result
    parts = []
    for item in content:
        if hasattr(item, "text"):
            parts.append(item.text)
        else:
            parts.append(str(item))
    return "\n".join(parts)


async def _list_tools(server_url: str) -> list[dict]:
    """List all available tools from the MCP server, auto-starting daemon if offline."""
    from fastmcp import Client

    await _ensure_server(server_url)

    async with Client(server_url) as client:
        tools = await client.list_tools()

    return [
        {
            "name": t.name,
            "description": (t.description or "")[:80],
        }
        for t in tools
    ]


async def _check_status(server_url: str) -> dict:
    """Check server status (no auto-start — status command is for diagnostics)."""
    return await _check_status_raw(server_url)


# ── CLI Argument Parser ──────────────────────────────────────────────


def _parse_tool_args(argv: list[str]) -> tuple[str, dict, str, bool]:
    """
    Parse command-line arguments.

    Returns:
        (tool_name, tool_arguments, server_url, raw_mode)
    """
    server_url = DEFAULT_SERVER_URL
    raw_mode = False
    tool_name = ""
    tool_args: dict = {}
    positional_done = False

    i = 0
    while i < len(argv):
        arg = argv[i]

        if arg in ("--server", "-s") and i + 1 < len(argv):
            server_url = argv[i + 1]
            i += 2
            continue

        if arg == "--raw":
            raw_mode = True
            i += 1
            continue

        if arg.startswith("--") and "=" in arg:
            key, _, val = arg[2:].partition("=")
            tool_args[key] = _coerce_value(val)
            i += 1
            continue

        if arg.startswith("--") and i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            key = arg[2:]
            val = argv[i + 1]
            tool_args[key] = _coerce_value(val)
            i += 2
            continue

        if not positional_done and not arg.startswith("-"):
            tool_name = arg
            positional_done = True
            i += 1
            continue

        i += 1

    return tool_name, tool_args, server_url, raw_mode


def _coerce_value(val: str):
    """Try to convert string to int/float/bool for JSON-friendliness."""
    if val.lower() in ("true", "false"):
        return val.lower() == "true"
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


# ── Main ─────────────────────────────────────────────────────────────


USAGE = textwrap.dedent("""\
    NexusTrader MCP Bridge for OpenClaw

    Usage:
      python bridge.py <tool_name> [--arg1=value1] [--arg2 value2] [--raw]
      python bridge.py status
      python bridge.py list_tools

    Options:
      --server, -s URL    MCP server URL (default: $NEXUSTRADER_MCP_URL or http://127.0.0.1:18765/sse)
      --raw               Output raw JSON instead of markdown

    Examples:
      python bridge.py get_all_positions
      python bridge.py get_balance --exchange=binance --account_type=USD_M_FUTURE_TESTNET
      python bridge.py get_ticker --symbol=BTCUSDT-PERP.BINANCE
""")


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)

    tool_name, tool_args, server_url, raw_mode = _parse_tool_args(argv)

    if not tool_name:
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    # ── Special commands ──
    if tool_name == "status":
        info = asyncio.run(_check_status(server_url))
        print(json.dumps(info, ensure_ascii=False))
        sys.exit(0 if info["status"] == "online" else 1)

    if tool_name == "list_tools":
        tools = asyncio.run(_list_tools(server_url))
        print(json.dumps({"tools": tools}, ensure_ascii=False))
        sys.exit(0)

    # ── Tool call ──
    try:
        raw_text = asyncio.run(_call_tool(server_url, tool_name, tool_args))
    except Exception as e:
        print(json.dumps({"error": str(e), "tool": tool_name}, ensure_ascii=False))
        sys.exit(1)

    # Always output raw JSON so OpenClaw AI can interpret it directly
    print(raw_text)


if __name__ == "__main__":
    main()
