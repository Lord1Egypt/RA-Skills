#!/usr/bin/env python3
"""
mcp_server.py - MCP Server for mu-pdf-converter
Zero external dependencies. Communicates via stdin/stdout JSON-RPC 2.0.

Each line on stdin is one JSON-RPC 2.0 request; each line on stdout is one response.
Subprocess timeout: 120 seconds per conversion call.
"""
import json
import sys
import subprocess
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# ─── Tool definitions ────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "pdf_to_pptx",
        "description": "将PDF转换为可编辑的PowerPoint文件（四层叠加：位图+SVG+表格+文本框）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "输入PDF文件的绝对路径"},
                "outfile": {"type": "string", "description": "输出PPTX路径（可选，默认同目录同名）"},
                "slide_size": {
                    "type": "string",
                    "enum": ["pdf", "16:9", "4:3", "A4", "A4v"],
                    "default": "pdf",
                    "description": "幻灯片尺寸",
                },
                "no_translate": {
                    "type": "boolean",
                    "default": False,
                    "description": "禁用外文自动翻译",
                },
            },
            "required": ["pdf_path"],
        },
    },
    {
        "name": "pdf_to_docx",
        "description": "将PDF转换为可编辑的Word文档（保留标题/段落/表格/字体）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "输入PDF文件的绝对路径"},
                "outfile": {"type": "string", "description": "输出DOCX路径（可选）"},
            },
            "required": ["pdf_path"],
        },
    },
    {
        "name": "pdf_to_xlsx",
        "description": "提取PDF中的表格并写入Excel（三引擎：XY-Cut→MarkItDown→pdfplumber）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "输入PDF文件的绝对路径"},
                "outfile": {"type": "string", "description": "输出XLSX路径（可选）"},
                "pages": {
                    "type": "string",
                    "default": "all",
                    "description": "页面范围，如 1-3 或 all",
                },
                "batch_dir": {
                    "type": "string",
                    "description": "批量模式：扫描此目录下所有PDF（与pdf_path二选一）",
                },
            },
            "required": [],
        },
    },
    {
        "name": "pdf_to_images",
        "description": "将PDF每页渲染为高质量图片",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "输入PDF文件的绝对路径"},
                "outdir": {"type": "string", "description": "输出目录（可选）"},
                "dpi": {"type": "integer", "default": 150, "description": "渲染DPI"},
                "format": {
                    "type": "string",
                    "enum": ["png", "jpg"],
                    "default": "png",
                },
            },
            "required": ["pdf_path"],
        },
    },
    {
        "name": "pdf_fill_form",
        "description": "PDF表单填写（支持可填字段和坐标注释两种路径）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "输入PDF文件的绝对路径"},
                "detect": {
                    "type": "boolean",
                    "default": False,
                    "description": "检测可填字段",
                },
                "fill_json": {"type": "string", "description": "填写值JSON文件路径"},
                "outfile": {"type": "string", "description": "输出PDF路径"},
            },
            "required": ["pdf_path"],
        },
    },
    {
        "name": "pdf_remove_watermark",
        "description": "PDF去水印（4种策略：XObject/Alpha/文字/跨页图片）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "输入PDF文件的绝对路径"},
                "outfile": {"type": "string", "description": "输出PDF路径（可选）"},
                "method": {
                    "type": "string",
                    "enum": ["auto", "text", "image", "xobject"],
                    "default": "auto",
                    "description": "水印类型",
                },
                "detect_only": {
                    "type": "boolean",
                    "default": False,
                    "description": "仅检测不修改",
                },
                "aggressive": {
                    "type": "boolean",
                    "default": False,
                    "description": "激进模式",
                },
            },
            "required": ["pdf_path"],
        },
    },
]

# ─── Script-name mapping ─────────────────────────────────────────────────────

TOOL_SCRIPT_MAP = {
    "pdf_to_pptx": "pdf_to_pptx.py",
    "pdf_to_docx": "pdf_to_docx.py",
    "pdf_to_xlsx": "pdf_to_xlsx.py",
    "pdf_to_images": "pdf_to_images.py",
    "pdf_fill_form": "pdf_fill_form.py",
    "pdf_remove_watermark": "pdf_remove_watermark.py",
}


# ─── MCP protocol handlers ───────────────────────────────────────────────────

def handle_initialize(params):
    """Handle the 'initialize' MCP handshake."""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "mu-pdf-converter", "version": "1.7"},
    }


def handle_tools_list(params):
    """Handle 'tools/list' — return all tool definitions."""
    return {"tools": TOOLS}


def _build_command(name, arguments):
    """
    Build the subprocess command list for a given tool invocation.

    Returns:
        list[str] — the command suitable for subprocess.run()
    """
    script = str(SCRIPT_DIR / TOOL_SCRIPT_MAP[name])
    cmd = ["python3", script]

    if name == "pdf_to_pptx":
        cmd.append(arguments["pdf_path"])
        if arguments.get("outfile"):
            cmd.extend(["--outfile", arguments["outfile"]])
        if arguments.get("slide_size"):
            cmd.extend(["--slide-size", arguments["slide_size"]])
        if arguments.get("no_translate"):
            cmd.append("--no-translate")

    elif name == "pdf_to_docx":
        cmd.append(arguments["pdf_path"])
        if arguments.get("outfile"):
            cmd.extend(["--outfile", arguments["outfile"]])

    elif name == "pdf_to_xlsx":
        # Mutually exclusive: batch_dir OR pdf_path
        if arguments.get("batch_dir"):
            cmd.extend(["--batch", arguments["batch_dir"]])
        elif arguments.get("pdf_path"):
            cmd.append(arguments["pdf_path"])
        else:
            raise ValueError("pdf_to_xlsx requires either 'pdf_path' or 'batch_dir'")
        if arguments.get("outfile"):
            cmd.extend(["--outfile", arguments["outfile"]])
        if arguments.get("pages") and not arguments.get("batch_dir"):
            cmd.extend(["--pages", arguments["pages"]])

    elif name == "pdf_to_images":
        cmd.append(arguments["pdf_path"])
        if arguments.get("outdir"):
            cmd.extend(["--outdir", arguments["outdir"]])
        if arguments.get("dpi") is not None:
            cmd.extend(["--dpi", str(arguments["dpi"])])
        if arguments.get("format"):
            cmd.extend(["--format", arguments["format"]])

    elif name == "pdf_fill_form":
        cmd.append(arguments["pdf_path"])
        if arguments.get("detect"):
            cmd.append("--detect")
        if arguments.get("fill_json"):
            cmd.extend(["--fill-json", arguments["fill_json"]])
        if arguments.get("outfile"):
            cmd.extend(["--outfile", arguments["outfile"]])

    elif name == "pdf_remove_watermark":
        cmd.append(arguments["pdf_path"])
        if arguments.get("outfile"):
            cmd.extend(["--outfile", arguments["outfile"]])
        method = arguments.get("method", "auto")
        # The underlying script uses "all" where the tool exposes "auto"
        if method == "auto":
            method = "all"
        cmd.extend(["--method", method])
        if arguments.get("detect_only"):
            cmd.append("--detect-only")
        if arguments.get("aggressive"):
            cmd.append("--aggressive")

    else:
        raise ValueError(f"Unknown tool: {name}")

    return cmd


def handle_tools_call(params):
    """
    Handle 'tools/call' — execute the requested tool via subprocess.

    Returns MCP-compliant content array on success, or isError content on failure.
    """
    name = params.get("name", "")
    arguments = params.get("arguments", {})

    if name not in TOOL_SCRIPT_MAP:
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": f"Unknown tool: {name}"}
            ],
        }

    try:
        cmd = _build_command(name, arguments)
    except (ValueError, KeyError) as exc:
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": f"Invalid arguments: {exc}"}
            ],
        }

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": "Conversion timed out after 120 seconds."}
            ],
        }
    except Exception as exc:
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": f"Failed to run subprocess: {exc}"}
            ],
        }

    if result.returncode != 0:
        error_text = result.stderr.strip() or result.stdout.strip() or "Process exited with non-zero status."
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": error_text}
            ],
        }

    output_text = result.stdout.strip()
    if not output_text:
        output_text = "Conversion completed successfully (no stdout output)."

    return {
        "content": [
            {"type": "text", "text": output_text}
        ],
    }


# ─── Main loop ────────────────────────────────────────────────────────────────

def main():
    """Main loop: read JSON-RPC from stdin, write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        # Notifications (no id) that we acknowledge silently
        if method == "notifications/initialized":
            continue

        # Route to handler
        if method == "initialize":
            result = handle_initialize(params)
        elif method == "tools/list":
            result = handle_tools_list(params)
        elif method == "tools/call":
            result = handle_tools_call(params)
        else:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}",
                },
            }
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
            continue

        response = {"jsonrpc": "2.0", "id": req_id, "result": result}
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
