#!/usr/bin/env python3
"""
MCP Server — 将 multi-agent-orchestrator 包装为 MCP 工具。
支持 stdio JSON-RPC 传输，暴露 pipeline_run/pipeline_status/pipeline_approve 三个工具。
其他 Agent 框架可直接调用整条流水线作为单个工具。
"""

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from datetime import datetime

MCP_VERSION = "2024-11-05"

# MCP 工具定义
TOOLS = [
    {
        "name": "pipeline_run",
        "description": "运行一条多智能体流水线。参数：pipeline_file（YAML/JSON 文件路径），inputs（可选，输入参数 dict）。返回：run_id, status。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pipeline_file": {
                    "type": "string",
                    "description": "流水线文件路径（.yaml 或 .json）"
                },
                "inputs": {
                    "type": "object",
                    "description": "可选输入参数",
                    "additionalProperties": True
                }
            },
            "required": ["pipeline_file"]
        }
    },
    {
        "name": "pipeline_status",
        "description": "查询流水线运行状态。参数：run_id（由 pipeline_run 返回）。返回：完整状态（节点状态、耗时、成本、日志）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "string",
                    "description": "流水线运行 ID"
                }
            },
            "required": ["run_id"]
        }
    },
    {
        "name": "pipeline_approve",
        "description": "人工审批/拒绝流水线中的审批节点。参数：run_id, node_id, approved（True=通过，False= False=拒绝），comment（可选，审批意见）。返回：审批结果。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string", "description": "流水线运行 ID"},
                "node_id": {"type": "string", "description": "审批节点 ID"},
                "approved": {"type": "boolean", "description": "True=通过，False=拒绝"},
                "comment": {"type": "string", "description": "审批意见（可选）"}
            },
            "required": ["run_id", "node_id", "approved"]
        }
    }
]


def _send(obj):
    """发送 JSON-RPC 消息到 stdout"""
    line = json.dumps(obj, ensure_ascii=False)
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def _send_result(id_, result):
    _send({"jsonrpc": "2.0", "id": id_, "result": result})


def _send_error(id_, code, message, data=None):
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    _send({"jsonrpc": "2.0", "id": id_, "error": err})


def _read_line():
    """从 stdin 读取一行 JSON-RPC 请求"""
    line = sys.stdin.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def _find_orchestrator():
    """找到 orchestrator.py 的路径"""
    # 与 mcp_server.py 同目录
    script_dir = Path(__file__).parent.resolve()
    orch = script_dir / "orchestrator.py"
    if orch.exists():
        return str(orch)
    return None


def _run_orchestrator(args, timeout=None):
    """运行 orchestrator.py 子进程，返回 (stdout, stderr, returncode)"""
    orch = _find_orchestrator()
    if not orch:
        return "", "orchestrator.py not found", 1
    cmd = [sys.executable, orch] + args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=str(Path(orch).parent.parent)
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "orchestrator.py timed out", 1
    except Exception as e:
        return "", str(e), 1


def _get_state_path(run_id):
    """从 run_id 推断状态文件路径"""
    # run_id 格式通常为 <pipeline_name>_<timestamp>
    # 搜索最近匹配的状态文件
    orch = _find_orchestrator()
    if not orch:
        return None
    base_dir = Path(orch).parent.parent
    states_dir = base_dir / "states"
    if not states_dir.exists():
        return None
    # 搜索 *.json
    for f in sorted(states_dir.glob("*.json"), reverse=True):
        if run_id in f.stem:
            return str(f)
    return None


def handle_tools_list(id_):
    _send_result(id_, {"tools": TOOLS})


def handle_tools_call(id_, params):
    name = params.get("name", "")
    arguments = params.get("arguments", {})

    if name == "pipeline_run":
        _handle_pipeline_run(id_, arguments)
    elif name == "pipeline_status":
        _handle_pipeline_status(id_, arguments)
    elif name == "pipeline_approve":
        _handle_pipeline_approve(id_, arguments)
    else:
        _send_error(id_, -32601, f"Unknown tool: {name}")


def _handle_pipeline_run(id_, arguments):
    pipeline_file = arguments.get("pipeline_file", "")
    inputs = arguments.get("inputs", {})

    if not pipeline_file:
        _send_error(id_, -32602, "pipeline_file is required")
        return

    if not os.path.exists(pipeline_file):
        _send_error(id_, -32602, f"pipeline_file not found: {pipeline_file}")
        return

    args = ["run", pipeline_file]
    if inputs:
        # 序列化 inputs 为 JSON 字符串传给 orchestrator
        args.extend(["--inputs", json.dumps(inputs, ensure_ascii=False)])

    stdout, stderr, rc = _run_orchestrator(args, timeout=120)

    if rc != 0:
        _send_result(id_, {
            "content": [{"type": "text", "text": f"流水线执行失败 (exit {rc}):\n{stderr or stdout}"}],
            "isError": True
        })
        return

    # 解析 run_id（从输出中提取）
    run_id = None
    for line in (stdout + "\n" + stderr).split("\n"):
        if "run_id" in line.lower() or "runid" in line.lower():
            # 简单提取
            parts = line.split()
            for p in parts:
                if "_" in p and any(c.isdigit() for c in p):
                    run_id = p.strip()
                    break

    result_text = stdout or "流水线已提交"
    _send_result(id_, {
        "content": [{"type": "text", f"text": f"{result_text}\nrun_id: {run_id or 'unknown'}"}],
        "isError": False
    })


def _handle_pipeline_status(id_, arguments):
    run_id = arguments.get("run_id", "")
    if not run_id:
        _send_error(id_, -32602, "run_id is required")
        return

    state_path = _get_state_path(run_id)
    if not state_path:
        _send_result(id_, {
            "content": [{"type": "text", f"text": f"未找到 run_id={run_id} 的状态文件"}],
            "isError": True
        })
        return

    # 用 orchestrator status 获取状态
    stdout, stderr, rc = _run_orchestrator(["status", state_path])
    if rc != 0:
        _send_result(id_, {
            "content": [{"type": "text", f"text": f"状态查询失败: {stderr}"}],
            "isError": True
        })
        return

    _send_result(id_, {
        "content": [{"type": "text", "text": stdout}],
        "isError": False
    })


def _handle_pipeline_approve(id_, arguments):
    run_id = arguments.get("run_id", "")
    node_id = arguments.get("node_id", "")
    approved = arguments.get("approved", True)
    comment = arguments.get("comment", "")

    if not run_id or not node_id:
        _send_error(id_, -32602, "run_id and node_id are required")
        return

    state_path = _get_state_path(run_id)
    if not state_path:
        _send_result(id_, {
            "content": [{"type": "text", "text": f"未找到 run_id={run_id} 的状态文件"}],
            "isError": True
        })
        return

    args = ["resume", state_path, "--approve", node_id, "true" if approved else "false"]
    if comment:
        args.extend(["--comment", comment])

    stdout, stderr, rc = _run_orchestrator(args, timeout=60)
    action = "通过" if approved else "拒绝"
    if rc != 0:
        _send_result(id_, {
            "content": [{"type": "text", f"text": f"审批{action}失败: {stderr}"}],
            "isError": True
        })
        return

    _send_result(id_, {
        "content": [{"type": "text", "text": f"审批{action}成功\n{stdout}"}],
        "isError": False
    })


def main():
    """MCP Server 主循环 — stdio JSON-RPC"""
    while True:
        req = _read_line()
        if req is None:
            break

        # 处理通知（无 id）
        if "id" not in req:
            method = req.get("method", "")
            params = req.get("params", {})
            if method == "notifications/initialized":
                pass  # 客户端已初始化，无需响应
            continue

        id_ = req["id"]
        method = req.get("method", "")
        params = req.get("params", {})

        if method == "initialize":
            _send_result(id_, {
                "protocolVersion": MCP_VERSION,
                "serverInfo": {
                    "name": "multi-agent-orchestrator-mcp",
                    "version": "5.4.0"
                },
                "capabilities": {"tools": {}}
            })
        elif method == "tools/list":
            handle_tools_list(id_)
        elif method == "tools/call":
            handle_tools_call(id_, params)
        elif method == "notifications/initialized":
            pass  # 忽略通知
        else:
            _send_error(id_, -32601, f"Method not found: {method}")


if __name__ == "__main__":
    main()
