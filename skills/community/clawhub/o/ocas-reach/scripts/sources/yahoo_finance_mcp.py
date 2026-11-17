"""Yahoo Finance MCP connector for Reach.

Invokes yahoo-finance-mcp via stdio JSON-RPC to get comprehensive financial data
from Yahoo Finance. No API key required.

MCP server: yahoo-finance-mcp (GitHub)
Install:   uvx --from git+https://github.com/Alex2Yang97/yahoo-finance-mcp yahoo-finance-mcp
"""
from __future__ import annotations

import json
import subprocess
import threading
from typing import Any, Dict, Optional

from ._mcp_client import MCPClient


class _MCPClient(MCPClient):
    """Yahoo Finance-specific MCP client (uses uvx git+https launcher)."""
    pass


# ── Module-level client cache ──────────────────────────────────────────────
_client: Optional[_MCPClient] = None


def _get_client(auth: dict) -> _MCPClient:
    global _client
    if _client is None or _client._proc is None or _client._proc.poll() is not None:
        _client = _MCPClient([
            "uvx", "--from",
            "git+https://github.com/Alex2Yang97/yahoo-finance-mcp",
            "yahoo-finance-mcp"
        ])
        _client.start()
    return _client


def _close_client():
    global _client
    if _client:
        _client.close()
        _client = None


# ── Reach query interface ──────────────────────────────────────────────────

def query(action: str, params: dict, auth: dict) -> dict:
    """
    Reach-facing query entry point.

    Actions:
      historical_prices — Get OHLCV data. Params: symbol, period, interval
      stock_info        — Get comprehensive metrics. Params: symbol
      news              — Get news. Params: symbol, count
      financial_statement — Get financials. Params: symbol, statement_type, period
      holder_info       — Get holder data. Params: symbol, holder_type
      recommendations   — Get analyst recs. Params: symbol
      options_chain     — Get options. Params: symbol, expiration, option_type
      stock_actions     — Get dividends/splits. Params: symbol
    """
    client = _get_client(auth)

    try:
        symbol = params.get("symbol", "").upper()
        if not symbol and action != "recommendations":
            return {"error": f"{action} requires 'symbol'"}

        action_map = {
            "historical_prices": ("get_historical_stock_prices", _args_historical),
            "stock_info": ("get_stock_info", _args_symbol),
            "news": ("get_yahoo_finance_news", _args_news),
            "financial_statement": ("get_financial_statement", _args_financial),
            "holder_info": ("get_holder_info", _args_holder),
            "recommendations": ("get_recommendations", _args_symbol),
            "options_chain": ("get_option_chain", _args_options),
            "stock_actions": ("get_stock_actions", _args_symbol),
        }

        entry = action_map.get(action)
        if entry is None:
            return {"error": f"Unknown action: {action}", "valid_actions": list(action_map.keys())}

        tool_name, args_fn = entry
        args = args_fn(symbol, params)
        if isinstance(args, dict) and "error" in args:
            return args

        return client.call_tool(tool_name, args)
    except Exception as e:
        _close_client()
        return {"error": str(e), "action": action}


def _args_symbol(symbol: str, params: dict) -> dict:
    return {"symbol": symbol}


def _args_historical(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("period"):
        args["period"] = params["period"]
    if params.get("interval"):
        args["interval"] = params["interval"]
    return args


def _args_news(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("count"):
        args["count"] = int(params["count"])
    return args


def _args_financial(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("statement_type"):
        args["statement_type"] = params["statement_type"]
    if params.get("period"):
        args["period"] = params["period"]
    return args


def _args_holder(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("holder_type"):
        args["holder_type"] = params["holder_type"]
    return args


def _args_options(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("expiration"):
        args["expiration"] = params["expiration"]
    if params.get("option_type"):
        args["option_type"] = params["option_type"]
    return args
