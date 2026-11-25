#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-hub 的最小 stdio MCP 服务器（纯 Python，无第三方依赖）。

暴露给 Agent 的工具：
  - pan_doctor    : 环境检查（JSON）
  - pan_detect    : 识别网盘（JSON）
  - pan_dirs      : 默认下载目录（JSON）
  - pan_get_plan  : 生成 dry-run 下载计划（JSON，不打码省略凭据）

注册到 Codex（$CODEX_HOME/config.toml）示例：
  [mcp_servers.pan-cloud-drive]
  command = "$CODEX_HOME/skills/pan-hub/scripts/pan_mcp.py"
  enabled = true

协议遵循 MCP stdio JSON-RPC：initialize / notifications/initialized / tools/list / tools/call / ping。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

SCRIPT_DIR = Path(__file__).resolve().parent
PAN_PY = SCRIPT_DIR / "pan.py"
SERVER_NAME = "pan-cloud-drive"
SERVER_VERSION = "0.6.1-r3"

TOOLS: Dict[str, Dict[str, Any]] = {
    "pan_doctor": {
        "description": "检查网盘下载环境（Python、curl、系统凭据库、共享引擎、默认目录），返回 JSON。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "pan_detect": {
        "description": "识别分享链接属于哪个网盘，返回 drive/key、显示名与推荐引擎。",
        "inputSchema": {
            "type": "object",
            "properties": {"url": {"type": "string", "description": "网盘分享链接或直链"}},
            "required": ["url"],
        },
    },
    "pan_dirs": {
        "description": "返回默认下载根目录与示例任务目录。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "pan_get_plan": {
        "description": "为一条下载链接生成 dry-run 计划（JSON），只读不下发文件；可带提取码/路径/tier。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "pwd": {"type": "string", "description": "分享提取码（非账号密码）"},
                "path": {"type": "string", "description": "AList 中已挂载路径"},
                "tier": {"type": "string", "enum": ["free", "vip", "auto"]},
            },
            "required": ["url"],
        },
    },
    "pan_test": {
        "description": "测试一条下载链接是否就绪（只读，不下载）：识别网盘、检查依赖/提码、目标目录可写性，返回 JSON。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "pwd": {"type": "string", "description": "分享提取码（非账号密码）"},
                "path": {"type": "string", "description": "AList/WebDAV 已挂载路径"},
                "tier": {"type": "string", "enum": ["free", "vip", "auto"]},
            },
            "required": ["url"],
        },
    },
}


def _env() -> Dict[str, str]:
    env = dict(os.environ)
    env.setdefault("PYTHONPYCACHEPREFIX", "/tmp/pan-mcp-pycache")
    return env


def run_cli(args, timeout=60):
    cmd = [sys.executable or "python3", str(PAN_PY)] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=_env())
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "{\"ok\": false, \"error\": \"%s\"}" % str(exc), True
    text = (proc.stdout or "").strip() or (proc.stderr or "").strip()
    try:
        json.loads(text)
        return text, proc.returncode != 0
    except json.JSONDecodeError:
        return json.dumps({"ok": proc.returncode == 0, "text": text}, ensure_ascii=False), proc.returncode != 0


def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    args = arguments or {}
    if name == "pan_doctor":
        text, is_err = run_cli(["doctor", "--json"])
    elif name == "pan_detect":
        text, is_err = run_cli(["detect", str(args.get("url", ""))])
    elif name == "pan_dirs":
        text, is_err = run_cli(["dirs", "--json"])
    elif name == "pan_get_plan":
        cmd = ["get", str(args.get("url", "")), "--dry-run", "--json"]
        if args.get("pwd"):
            cmd += ["--pwd", str(args["pwd"])]
        if args.get("path"):
            cmd += ["--path", str(args["path"])]
        if args.get("tier"):
            cmd += ["--tier", str(args["tier"])]
        text, is_err = run_cli(cmd)
    elif name == "pan_test":
        cmd = ["test", str(args.get("url", "")), "--json"]
        if args.get("pwd"):
            cmd += ["--pwd", str(args["pwd"])]
        if args.get("path"):
            cmd += ["--path", str(args["path"])]
        if args.get("tier"):
            cmd += ["--tier", str(args["tier"])]
        text, is_err = run_cli(cmd)
    else:
        return {"content": [{"type": "text", "text": "未知工具：%s" % name}], "isError": True}
    return {"content": [{"type": "text", "text": text}], "isError": is_err}


def handle(msg: Dict[str, Any]) -> Dict[str, Any]:
    method = msg.get("method", "")
    params = msg.get("params") or {}
    if method == "initialize":
        return {
            "protocolVersion": params.get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            "instructions": "该 MCP 服务器用于统一网盘下载：识别、目录规划与 dry-run 计划。凭据一律不出口、不打码参数全部隐藏；实际下载请调用本机 pan.py（CLI）。",
        }
    if method == "tools/list":
        return {"tools": [{"name": k, "description": v["description"], "inputSchema": v["inputSchema"]} for k, v in TOOLS.items()]}
    if method == "tools/call":
        name = str(params.get("name", ""))
        return call_tool(name, params.get("arguments") or {})
    if method == "ping":
        return {}
    raise ValueError("unknown method: %s" % method)


def main() -> int:
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("method") == "notifications/initialized":
            continue
        try:
            result = handle(msg)
        except Exception as exc:  # noqa: BLE001
            response = {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32601, "message": str(exc)}}
        else:
            response = {"jsonrpc": "2.0", "id": msg.get("id"), "result": result}
        if msg.get("id") is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
