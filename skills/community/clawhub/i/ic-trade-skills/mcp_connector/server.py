"""
mcp_connector/server.py
────────────────────────
MCP (Model Context Protocol) server — client-side connector.

Exposes three tools to MCP-compatible agents (Claude Desktop, etc.):

  quote_part          — fetch a market quote from the remote engine
  read_erp_inventory  — read local ERP for a part number (stock + status only)
  get_combined_view   — merge remote quote + local ERP and display

Transport: stdio (standard MCP default)

Run:
    python -m mcp_connector.server

Or register in Claude Desktop's mcp_servers config:
    {
      "ic-quote": {
        "command": "python",
        "args": ["-m", "mcp_connector.server"],
        "env": {
          "QUOTE_ENGINE_URL":     "https://quote.example.com",
          "QUOTE_ENGINE_API_KEY": "<your-key>",
          "ERP_EXCEL_PATH":       "C:/Users/You/Desktop/ERP內容.xlsx"
        }
      }
    }

Dependencies:
    pip install mcp httpx openpyxl
"""
from __future__ import annotations

import json
import logging
import sys

# ── MCP SDK import (graceful degradation if not installed) ────────────────────
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolRequest,
        CallToolResult,
        ListToolsRequest,
        ListToolsResult,
        TextContent,
        Tool,
    )
    _MCP_AVAILABLE = True
except ImportError:
    _MCP_AVAILABLE = False

from mcp_connector.api_client import QuoteApiError, fetch_quote
from mcp_connector.config import config
from mcp_connector.erp_reader import read_erp
from mcp_connector.merger import format_as_text, merge

log = logging.getLogger("mcp_connector.server")
logging.basicConfig(level="INFO", format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")

# ── Tool definitions ──────────────────────────────────────────────────────────

_TOOLS = [
    {
        "name": "quote_part",
        "description": (
            "Fetch a market quote for an IC component from the remote engine. "
            "Returns the quoted price (USD), quote action, and availability signal. "
            "No local ERP data is included — use get_combined_view for a merged view."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "part_number": {
                    "type": "string",
                    "description": "IC part number, e.g. STM32L412CBU6",
                },
                "qty": {
                    "type": "integer",
                    "description": "Requested quantity (0 = unspecified)",
                    "default": 0,
                },
                "customer_id": {
                    "type": "string",
                    "description": "Optional opaque customer identifier",
                    "default": "",
                },
            },
            "required": ["part_number"],
        },
    },
    {
        "name": "read_erp_inventory",
        "description": (
            "Read local ERP inventory for an IC part number. "
            "Returns ONLY stock quantity and supply status from your local ERP file. "
            "Pricing data (floor price, sale price) is never extracted or returned. "
            "Data stays on your machine — nothing is sent to the server."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "part_number": {
                    "type": "string",
                    "description": "IC part number, e.g. STM32L412CBU6",
                },
            },
            "required": ["part_number"],
        },
    },
    {
        "name": "get_combined_view",
        "description": (
            "Get a combined view of remote market quote and local ERP inventory. "
            "Fetches the market quote from the engine, reads local ERP stock, "
            "merges both on the client side, and returns a formatted summary table. "
            "Includes a recommendation based on quote action and local stock."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "part_number": {
                    "type": "string",
                    "description": "IC part number, e.g. STM32L412CBU6",
                },
                "qty": {
                    "type": "integer",
                    "description": "Requested quantity",
                    "default": 0,
                },
                "customer_id": {
                    "type": "string",
                    "description": "Optional customer identifier",
                    "default": "",
                },
                "format": {
                    "type": "string",
                    "enum": ["text", "json"],
                    "description": "Output format: 'text' (markdown table) or 'json'",
                    "default": "text",
                },
            },
            "required": ["part_number"],
        },
    },
]


# ── Tool handlers ─────────────────────────────────────────────────────────────

def _handle_quote_part(args: dict) -> str:
    part   = str(args.get("part_number", "")).strip().upper()
    qty    = int(args.get("qty", 0))
    cid    = str(args.get("customer_id", "")).strip()

    if not part:
        return "❌ Error: part_number is required."

    try:
        q = fetch_quote(part, qty=qty, customer_id=cid)
    except QuoteApiError as exc:
        return f"❌ Quote API error: {exc}"
    except ImportError as exc:
        return f"❌ Missing dependency: {exc}"

    if not q.ok:
        return f"❌ Part not found or unavailable: {q.error}"

    price_str = f"USD {q.quoted_price:.4f}" if q.quoted_price is not None else "N/A (pending review)"
    action_map = {"auto_quote": "✅ Auto-quote ready", "pending": "🔄 Pending review", "clarify": "⚠️ Clarify request"}

    lines = [
        f"**{q.part_number}** — Remote Market Quote",
        f"- Quoted price:   {price_str}",
        f"- Quote action:   {action_map.get(q.quote_action, q.quote_action)}",
        f"- Market in stock: {'Yes' if q.stock_available else 'No'}",
        f"- Supply status:  {q.supply_status or '—'}",
        f"- Data source:    {q.data_source}",
    ]
    return "\n".join(lines)


def _handle_read_erp(args: dict) -> str:
    part = str(args.get("part_number", "")).strip().upper()
    if not part:
        return "❌ Error: part_number is required."

    record = read_erp(
        part_number=part,
        excel_path=config.erp_excel_path or None,
        sqlite_path=config.erp_sqlite_path or None,
    )

    if record.source == "unavailable":
        return (
            f"⚠️ No local ERP source configured or accessible.\n"
            f"Set ERP_EXCEL_PATH or ERP_SQLITE_PATH in your environment."
        )

    qty_str = f"{int(record.stock_qty):,} units" if record.stock_qty is not None else "No data"
    return (
        f"**{record.part_number}** — Local ERP Inventory\n"
        f"- Stock qty:     {qty_str}\n"
        f"- Supply status: {record.supply_status or '—'}\n"
        f"- ERP source:    {record.source}\n"
        f"*(Pricing data is excluded — stays on your machine.)*"
    )


def _handle_combined_view(args: dict) -> str:
    from mcp_connector.merger import format_as_dict

    part   = str(args.get("part_number", "")).strip().upper()
    qty    = int(args.get("qty", 0))
    cid    = str(args.get("customer_id", "")).strip()
    fmt    = str(args.get("format", "text")).strip().lower()

    if not part:
        return "❌ Error: part_number is required."

    # 1. Remote quote
    try:
        remote = fetch_quote(part, qty=qty, customer_id=cid)
    except QuoteApiError as exc:
        return f"❌ Quote API error: {exc}"
    except ImportError as exc:
        return f"❌ Missing dependency: {exc}"

    # 2. Local ERP
    local = read_erp(
        part_number=part,
        excel_path=config.erp_excel_path or None,
        sqlite_path=config.erp_sqlite_path or None,
    )

    # 3. Merge on client side
    view = merge(remote, local, requested_qty=qty)

    if fmt == "json":
        return json.dumps(format_as_dict(view), ensure_ascii=False, indent=2)
    return format_as_text(view)


# ── MCP server bootstrap ──────────────────────────────────────────────────────

def _run_mcp_server() -> None:
    """Run the MCP server using the official SDK (stdio transport)."""
    server = Server("ic-quote-connector")

    @server.list_tools()
    async def list_tools(request: ListToolsRequest) -> ListToolsResult:
        return ListToolsResult(
            tools=[
                Tool(
                    name=t["name"],
                    description=t["description"],
                    inputSchema=t["inputSchema"],
                )
                for t in _TOOLS
            ]
        )

    @server.call_tool()
    async def call_tool(request: CallToolRequest) -> CallToolResult:
        name = request.params.name
        args = dict(request.params.arguments or {})

        dispatch = {
            "quote_part":         _handle_quote_part,
            "read_erp_inventory": _handle_read_erp,
            "get_combined_view":  _handle_combined_view,
        }

        handler = dispatch.get(name)
        if handler is None:
            result_text = f"❌ Unknown tool: {name}"
        else:
            try:
                result_text = handler(args)
            except Exception as exc:
                log.exception("Tool %s raised unexpected error", name)
                result_text = f"❌ Internal error in {name}: {exc}"

        return CallToolResult(content=[TextContent(type="text", text=result_text)])

    import asyncio
    asyncio.run(stdio_server(server))


def _run_cli_fallback() -> None:
    """
    Minimal CLI fallback when the MCP SDK is not installed.
    Useful for testing tools from the command line.
    """
    import argparse

    parser = argparse.ArgumentParser(description="IC Quote MCP Connector (CLI fallback)")
    sub = parser.add_subparsers(dest="tool")

    p_quote = sub.add_parser("quote_part")
    p_quote.add_argument("part_number")
    p_quote.add_argument("--qty", type=int, default=0)

    p_erp = sub.add_parser("read_erp_inventory")
    p_erp.add_argument("part_number")

    p_combo = sub.add_parser("get_combined_view")
    p_combo.add_argument("part_number")
    p_combo.add_argument("--qty", type=int, default=0)
    p_combo.add_argument("--format", default="text", choices=["text", "json"])

    args = parser.parse_args()
    if not args.tool:
        parser.print_help()
        sys.exit(0)

    if args.tool == "quote_part":
        print(_handle_quote_part({"part_number": args.part_number, "qty": args.qty}))
    elif args.tool == "read_erp_inventory":
        print(_handle_read_erp({"part_number": args.part_number}))
    elif args.tool == "get_combined_view":
        print(_handle_combined_view({"part_number": args.part_number, "qty": args.qty, "format": args.format}))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Print config warnings on startup
    for warning in config.validate():
        log.warning(warning)

    if _MCP_AVAILABLE:
        log.info("Starting IC Quote MCP server (stdio transport)...")
        _run_mcp_server()
    else:
        log.warning(
            "MCP SDK not installed (pip install mcp). "
            "Falling back to CLI mode for testing."
        )
        _run_cli_fallback()
