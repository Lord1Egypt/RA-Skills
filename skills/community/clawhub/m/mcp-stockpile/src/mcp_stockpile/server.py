"""
Model Context Protocol (MCP) Server Implementation for Stockpile Market.
Supports both FastMCP (official SDK) and zero-dependency STDIO JSON-RPC 2.0.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, Optional

from .client import StockpileClient
from .tools import TOOLS_METADATA, execute_tool

SERVER_NAME = "stockpile-mcp-server"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"


def run_stdio_server(client: Optional[StockpileClient] = None) -> None:
    """
    Run the MCP server in STDIO mode using JSON-RPC 2.0.
    Standardized for Claude Desktop, Cursor, Cline, Windsurf, and custom agents.
    """
    if client is None:
        client = StockpileClient()

    for line in sys.stdin:
        clean_line = line.strip()
        if not clean_line:
            continue
        try:
            msg = json.loads(clean_line)
        except Exception:
            continue

        msg_id = msg.get("id")
        method = msg.get("method")
        params = msg.get("params", {})

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": SERVER_NAME,
                        "version": SERVER_VERSION
                    }
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": TOOLS_METADATA
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            try:
                res = execute_tool(tool_name, tool_args, client=client)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": res
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "isError": True,
                        "content": [
                            {"type": "text", "text": f"Error executing {tool_name}: {str(e)}"}
                        ]
                    }
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "ping":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {}
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            # Initialization completed notification
            pass

        else:
            if msg_id is not None:
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not found"
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()


def create_server(client: Optional[StockpileClient] = None):
    """
    Create a FastMCP server instance if official `mcp` SDK is available,
    otherwise fallback to returning None.
    """
    try:
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("stockpile-mcp-server")
        if client is None:
            client = StockpileClient()

        # Dynamically attach tools to FastMCP
        for tool_meta in TOOLS_METADATA:
            name = tool_meta["name"]
            desc = tool_meta["description"]

            def make_handler(t_name: str):
                def handler(**kwargs):
                    return execute_tool(t_name, kwargs, client=client)
                return handler

            mcp.add_tool(make_handler(name), name=name, description=desc)

        return mcp
    except ImportError:
        return None
