#!/usr/bin/env python3
"""Stdio MCP adapter for One Person Company OS.

This server intentionally wraps the canonical repository scripts instead of
duplicating business logic. It supports a small tool surface that is useful
across Hermes, Claude Desktop, Cursor, VS Code, and other MCP clients.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


def run_script(script: str, args: List[str]) -> str:
    command = [sys.executable, str(SCRIPTS / script)] + args
    completed = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    output = []
    if completed.stdout:
        output.append(completed.stdout.strip())
    if completed.stderr:
        output.append(completed.stderr.strip())
    if completed.returncode != 0:
        raise RuntimeError("\n".join(output) or f"{script} failed with exit code {completed.returncode}")
    return "\n\n".join(output)


def text_result(text: str) -> Dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "preflight_check",
        "description": "Check runtime and workspace readiness for One Person Company OS.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "default": "create-company"},
                "company_dir": {"type": "string"},
            },
        },
    },
    {
        "name": "init_business",
        "description": "Create a founder-approved local operating cockpit workspace.",
        "inputSchema": {
            "type": "object",
            "required": ["company_name", "path", "product_name", "target_user", "core_problem", "product_pitch"],
            "properties": {
                "company_name": {"type": "string"},
                "path": {"type": "string"},
                "product_name": {"type": "string"},
                "target_user": {"type": "string"},
                "core_problem": {"type": "string"},
                "product_pitch": {"type": "string"},
                "language": {"type": "string", "enum": ["zh-CN", "en-US"], "default": "zh-CN"},
            },
        },
    },
    {
        "name": "update_focus",
        "description": "Update current goal, bottleneck, primary arena, and shortest action.",
        "inputSchema": {
            "type": "object",
            "required": ["company_dir", "primary_goal", "primary_bottleneck", "primary_arena", "today_action"],
            "properties": {
                "company_dir": {"type": "string"},
                "primary_goal": {"type": "string"},
                "primary_bottleneck": {"type": "string"},
                "primary_arena": {"type": "string", "enum": ["sales", "product", "delivery", "cash", "asset"]},
                "today_action": {"type": "string"},
                "week_outcome": {"type": "string"},
            },
        },
    },
    {
        "name": "generate_artifact_document",
        "description": "Generate a numbered formal DOCX artifact inside the approved workspace.",
        "inputSchema": {
            "type": "object",
            "required": ["company_dir", "title", "category", "summary"],
            "properties": {
                "company_dir": {"type": "string"},
                "title": {"type": "string"},
                "category": {"type": "string", "enum": ["business", "delivery", "product", "operations"]},
                "summary": {"type": "string"},
                "evidence": {"type": "string"},
            },
        },
    },
    {
        "name": "validate_release",
        "description": "Run the local release validation suite.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "preflight_check":
        args = ["--mode", str(arguments.get("mode") or "create-company")]
        if arguments.get("company_dir"):
            args.extend(["--company-dir", str(arguments["company_dir"])])
        return text_result(run_script("preflight_check.py", args))

    if name == "init_business":
        args = [
            str(arguments["company_name"]),
            "--path",
            str(arguments["path"]),
            "--product-name",
            str(arguments["product_name"]),
            "--target-user",
            str(arguments["target_user"]),
            "--core-problem",
            str(arguments["core_problem"]),
            "--product-pitch",
            str(arguments["product_pitch"]),
            "--language",
            str(arguments.get("language") or "zh-CN"),
            "--confirmed",
        ]
        return text_result(run_script("init_business.py", args))

    if name == "update_focus":
        args = [
            str(arguments["company_dir"]),
            "--primary-goal",
            str(arguments["primary_goal"]),
            "--primary-bottleneck",
            str(arguments["primary_bottleneck"]),
            "--primary-arena",
            str(arguments["primary_arena"]),
            "--today-action",
            str(arguments["today_action"]),
        ]
        if arguments.get("week_outcome"):
            args.extend(["--week-outcome", str(arguments["week_outcome"])])
        return text_result(run_script("update_focus.py", args))

    if name == "generate_artifact_document":
        args = [
            str(arguments["company_dir"]),
            "--title",
            str(arguments["title"]),
            "--category",
            str(arguments["category"]),
            "--summary",
            str(arguments["summary"]),
        ]
        if arguments.get("evidence"):
            args.extend(["--evidence", str(arguments["evidence"])])
        return text_result(run_script("generate_artifact_document.py", args))

    if name == "validate_release":
        return text_result(run_script("validate_release.py", []))

    raise ValueError(f"unknown tool: {name}")


def read_message() -> Optional[Dict[str, Any]]:
    headers: Dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, _, value = line.decode("ascii").partition(":")
        headers[key.lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    payload = sys.stdin.buffer.read(length)
    return json.loads(payload.decode("utf-8"))


def write_message(message: Dict[str, Any]) -> None:
    payload = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()


def response(request_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def handle(message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params") or {}

    try:
        if method == "initialize":
            return response(
                request_id,
                {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "one-person-company-os", "version": "1.0.3"},
                },
            )
        if method == "tools/list":
            return response(request_id, {"tools": TOOLS})
        if method == "tools/call":
            return response(request_id, call_tool(str(params.get("name")), params.get("arguments") or {}))
        if method == "ping":
            return response(request_id, {})
        if method and method.startswith("notifications/"):
            return None
        return error_response(request_id, -32601, f"method not found: {method}")
    except Exception as exc:  # MCP servers should return structured failures.
        return error_response(request_id, -32000, str(exc))


def main() -> int:
    while True:
        message = read_message()
        if message is None:
            return 0
        reply = handle(message)
        if reply is not None:
            write_message(reply)


if __name__ == "__main__":
    raise SystemExit(main())
