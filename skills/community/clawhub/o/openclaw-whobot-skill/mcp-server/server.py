#!/usr/bin/env python3
"""
OpenClaw WhoBot MCP Server
提供 WhoBot (呼波特) AI电话数字员工知识查询工具。

支持两种传输方式：
  - stdio: 本地使用，通过标准输入输出通信
  - http:  远程使用，通过 Streamable HTTP 通信（OpenClaw 插件模式）

用法：
  # stdio 模式（默认，适合本地 Claude Code / OpenClaw）
  python3 server.py

  # HTTP 模式（适合远程 OpenClaw 插件）
  python3 server.py --http --port 18080
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------- 知识库加载 ----------

KNOWLEDGE_PATH = Path(__file__).parent.parent / "references" / "knowledge.md"


def load_knowledge() -> str:
    """加载知识库内容"""
    if KNOWLEDGE_PATH.exists():
        return KNOWLEDGE_PATH.read_text(encoding="utf-8")
    return ""


def search_knowledge(query: str, knowledge: str) -> str:
    """在知识库中搜索相关段落"""
    query_lower = query.lower()
    sections = re.split(r"\n(?=##\s)", knowledge)
    matched = []
    for section in sections:
        if any(
            keyword in section.lower()
            for keyword in query_lower.split()
            if len(keyword) > 1
        ):
            matched.append(section.strip())
    if not matched:
        return knowledge[:3000] + "\n\n...(更多内容请使用更具体的关键词查询)"
    return "\n\n---\n\n".join(matched)


# ---------- 工具定义 ----------

TOOLS = [
    {
        "name": "whobot_knowledge",
        "description": (
            "查询 WhoBot (呼波特) AI电话数字员工的知识库。"
            "支持按关键词搜索公司信息、产品能力、核心技术、行业方案、客户案例等。"
            "Query WhoBot knowledge base by keywords."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，如：拟人化、行业方案、融资、团队、技术架构等",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "whobot_faq",
        "description": (
            "获取 WhoBot 常见问题的回答。"
            "涵盖：什么是 WhoBot、核心能力、与竞品区别、成本、行业覆盖等。"
            "Get answers to frequently asked questions about WhoBot."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "要回答的问题",
                }
            },
            "required": ["question"],
        },
    },
    {
        "name": "whobot_overview",
        "description": (
            "获取 WhoBot (呼波特) 公司和产品的完整概览。"
            "Get a complete overview of WhoBot company and products."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]

# ---------- FAQ 数据 ----------

FAQ = {
    "什么是whobot": "WhoBot（呼波特）是顶级AI电话数字员工平台，像真人一样帮企业接打电话。98% 的通话对象分不清电话那头是真人还是 AI。",
    "核心能力": "两大核心能力：1. 拟人化引擎 — 自然停顿、语气词、情绪感知，像人但比人稳定；2. 拟角色飞轮 — 30+ 行业深耕，数据飞轮驱动，每一通更好。",
    "和竞品区别": "WhoBot 不是传统语音机器人/IVR。核心差异：自研端到端语音系统、98% 拟人识别率、边说边做实时 OS、1000+ 行业知识沉淀。",
    "成本": "成本降低 10 倍。通信 SP 场景：1000 次转化 ¥30,000 vs 人工 ¥300,000，降本 90%。",
    "行业": "覆盖 30+ 行业：医疗、汽车、餐饮连锁、教育、通信 & BPO、零售、家装等。",
    "团队": "CEO 董连平（前作业帮/百度）、CTO 梁斌（前阿里云P8/百度T7）、COO 黄天文（《引爆用户增长》作者）、AI 合伙人 云中江树（LangGPT 创始人）。",
    "融资": "金沙江创投 A 轮数千万人民币。金沙江创投曾投资滴滴、饿了么等头部公司。",
    "合规": "等保三级 · ICP 京ICP备2025110070号 · 京B2-20260448。",
}


def answer_faq(question: str) -> str:
    """匹配并回答常见问题"""
    q_lower = question.lower()
    for key, answer in FAQ.items():
        if any(word in q_lower for word in key.split()):
            return answer
    # 未匹配到 FAQ，搜索知识库
    knowledge = load_knowledge()
    return search_knowledge(question, knowledge)


# ---------- 工具执行 ----------


def handle_tool_call(name: str, arguments: dict) -> str:
    """执行工具调用"""
    knowledge = load_knowledge()

    if name == "whobot_knowledge":
        query = arguments.get("query", "")
        return search_knowledge(query, knowledge)

    elif name == "whobot_faq":
        question = arguments.get("question", "")
        return answer_faq(question)

    elif name == "whobot_overview":
        # 返回公司概览 + 产品概览
        sections = re.split(r"\n(?=##\s)", knowledge)
        overview_parts = []
        for section in sections:
            if any(
                kw in section
                for kw in ["Company Overview", "Product Platform", "Competitive"]
            ):
                overview_parts.append(section.strip())
        return "\n\n---\n\n".join(overview_parts) if overview_parts else knowledge[:5000]

    return f"Unknown tool: {name}"


# ========== STDIO 传输 ==========


def run_stdio():
    """以 stdio 模式运行 MCP Server"""

    def send(msg: dict):
        sys.stdout.write(json.dumps(msg) + "\n")
        sys.stdout.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = request.get("method", "")
        req_id = request.get("id")

        if method == "initialize":
            send(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": {
                            "name": "openclaw-whobot-mcp",
                            "version": "1.0.0",
                        },
                    },
                }
            )

        elif method == "notifications/initialized":
            pass  # No response needed

        elif method == "tools/list":
            send({"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}})

        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            result_text = handle_tool_call(tool_name, arguments)
            send(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": result_text}],
                        "isError": False,
                    },
                }
            )

        elif method == "ping":
            send({"jsonrpc": "2.0", "id": req_id, "result": {}})

        else:
            if req_id is not None:
                send(
                    {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}",
                        },
                    }
                )


# ========== HTTP 传输 (Streamable HTTP / SSE) ==========


def run_http(host: str = "0.0.0.0", port: int = 18080):
    """以 HTTP 模式运行 MCP Server（OpenClaw 插件模式）"""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
    except ImportError:
        print("HTTP server requires Python 3.7+", file=sys.stderr)
        sys.exit(1)

    class MCPHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                request = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
                return

            method = request.get("method", "")
            req_id = request.get("id")
            response = None

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": {
                            "name": "openclaw-whobot-mcp",
                            "version": "1.0.0",
                        },
                    },
                }
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS},
                }
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                result_text = handle_tool_call(tool_name, arguments)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": result_text}],
                        "isError": False,
                    },
                }
            elif method == "ping":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}",
                    },
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        def log_message(self, format, *args):
            print(f"[MCP] {args[0]}", file=sys.stderr)

    server = HTTPServer((host, port), MCPHandler)
    print(f"🦞 OpenClaw WhoBot MCP Server running on http://{host}:{port}", file=sys.stderr)
    print(f"   Transport: Streamable HTTP", file=sys.stderr)
    print(f"   Tools: {', '.join(t['name'] for t in TOOLS)}", file=sys.stderr)
    server.serve_forever()


# ========== 入口 ==========

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenClaw WhoBot MCP Server")
    parser.add_argument("--http", action="store_true", help="以 HTTP 模式运行（OpenClaw 插件模式）")
    parser.add_argument("--host", default="0.0.0.0", help="HTTP 监听地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=18080, help="HTTP 监听端口 (默认: 18080)")
    args = parser.parse_args()

    if args.http:
        run_http(args.host, args.port)
    else:
        run_stdio()
