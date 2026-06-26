"""Infoway Financial Data MCP Server.

Provides 17 tools for accessing real-time and fundamental financial data
through the Infoway API. Designed for use with Claude Desktop and other
MCP-compatible clients.
"""

import json
import os

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from infoway import InfowayClient

app = Server("infoway-mcp-server")

# ---------------------------------------------------------------------------
# Market-type dispatch helper
# ---------------------------------------------------------------------------

_MARKET_CLIENTS = {"stock", "crypto", "common", "japan", "india"}


def _get_client() -> InfowayClient:
    return InfowayClient(api_key=os.environ.get("INFOWAY_API_KEY", ""))


def _market_sub_client(client: InfowayClient, market_type: str):
    """Return the appropriate sub-client for the given market type."""
    mt = market_type.lower()
    if mt not in _MARKET_CLIENTS:
        raise ValueError(
            f"Invalid market_type '{market_type}'. "
            f"Must be one of: {', '.join(sorted(_MARKET_CLIENTS))}"
        )
    return getattr(client, mt)


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    Tool(
        name="get_realtime_trade",
        description=(
            "Get real-time trade data for stocks, crypto, or forex. "
            "Returns latest price, volume, change, and timestamp for each symbol. "
            "Example codes: 'AAPL.US', 'BTCUSDT', '700.HK', 'USDJPY'."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "codes": {
                    "type": "string",
                    "description": (
                        "Comma-separated symbol codes. "
                        "Examples: 'AAPL.US' (US stock), '700.HK' (HK stock), "
                        "'BTCUSDT' (crypto), 'USDJPY' (forex)."
                    ),
                },
                "market_type": {
                    "type": "string",
                    "enum": ["stock", "crypto", "common", "japan", "india"],
                    "description": (
                        "Market type to query. 'stock' for HK/US/CN equities, "
                        "'crypto' for digital currencies, 'common' for forex & commodities, "
                        "'japan' for Japan equities, 'india' for India equities."
                    ),
                    "default": "stock",
                },
            },
            "required": ["codes"],
        },
    ),
    Tool(
        name="get_market_depth",
        description=(
            "Get real-time order book / market depth (bid/ask levels) for given symbols. "
            "Returns arrays of bid and ask prices with their quantities."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "codes": {
                    "type": "string",
                    "description": "Comma-separated symbol codes (e.g. 'AAPL.US,MSFT.US').",
                },
                "market_type": {
                    "type": "string",
                    "enum": ["stock", "crypto", "common", "japan", "india"],
                    "description": "Market type to query.",
                    "default": "stock",
                },
            },
            "required": ["codes"],
        },
    ),
    Tool(
        name="get_kline",
        description=(
            "Get candlestick / K-line (OHLCV) data for given symbols. "
            "Supports multiple intervals: 1m, 5m, 15m, 30m, 1h, 2h, 4h, "
            "daily, weekly, monthly, quarterly, yearly."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "codes": {
                    "type": "string",
                    "description": "Comma-separated symbol codes.",
                },
                "market_type": {
                    "type": "string",
                    "enum": ["stock", "crypto", "common", "japan", "india"],
                    "description": "Market type to query.",
                    "default": "stock",
                },
                "kline_type": {
                    "type": "integer",
                    "enum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    "description": (
                        "K-line interval: 1=1min, 2=5min, 3=15min, 4=30min, "
                        "5=1hour, 6=2hour, 7=4hour, 8=daily, 9=weekly, "
                        "10=monthly, 11=quarterly, 12=yearly."
                    ),
                    "default": 8,
                },
                "count": {
                    "type": "integer",
                    "description": "Number of candles to return (max varies by interval).",
                    "default": 100,
                },
            },
            "required": ["codes"],
        },
    ),
    Tool(
        name="get_market_temperature",
        description=(
            "Get market temperature / sentiment overview for specified markets. "
            "Shows overall market heat, advance-decline ratios, and sentiment indicators. "
            "Useful for gauging whether the market is bullish or bearish."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": (
                        "Comma-separated market codes. Available: HK, US, CN, SG. "
                        "Example: 'HK,US' for Hong Kong and US markets."
                    ),
                    "default": "HK,US,CN,SG",
                },
            },
        },
    ),
    Tool(
        name="get_market_breadth",
        description=(
            "Get market breadth data showing advance/decline statistics. "
            "Includes number of advancing, declining, and unchanged stocks."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": "Market code (e.g. 'HK', 'US', 'CN', 'SG').",
                },
            },
            "required": ["market"],
        },
    ),
    Tool(
        name="get_global_indexes",
        description=(
            "Get real-time data for major global stock market indexes. "
            "Includes Dow Jones, S&P 500, Nasdaq, Hang Seng, SSE Composite, Nikkei, etc."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="get_leading_industries",
        description=(
            "Get top-performing industry sectors for a market, ranked by performance. "
            "Useful for identifying sector rotation and market leaders."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": "Market code (e.g. 'HK', 'US', 'CN').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of top industries to return.",
                    "default": 10,
                },
            },
            "required": ["market"],
        },
    ),
    Tool(
        name="get_industry_list",
        description=(
            "Get the full list of industry sectors for a market with their "
            "performance data. Includes change percentage, member count, and leader stocks."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": "Market code (e.g. 'HK', 'US', 'CN').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of industries to return.",
                    "default": 200,
                },
            },
            "required": ["market"],
        },
    ),
    Tool(
        name="get_concept_list",
        description=(
            "Get the list of concept/thematic sectors for a market. "
            "Concepts are thematic groupings like 'AI', 'EV', 'Metaverse', etc."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": "Market code (e.g. 'HK', 'US', 'CN').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of concepts to return.",
                    "default": 100,
                },
            },
            "required": ["market"],
        },
    ),
    Tool(
        name="get_plate_members",
        description=(
            "Get all stock members of a specific industry or concept plate/sector. "
            "Returns individual stocks with their price and change data."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "plate_symbol": {
                    "type": "string",
                    "description": "The plate/sector symbol identifier.",
                },
            },
            "required": ["plate_symbol"],
        },
    ),
    Tool(
        name="get_plate_heatmap",
        description=(
            "Get sector heatmap data for a market showing plate/sector performance. "
            "Useful for visualizing which sectors are hot or cold."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": "Market code (e.g. 'HK', 'US', 'CN').",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of plates to return.",
                    "default": 50,
                },
            },
            "required": ["market"],
        },
    ),
    Tool(
        name="get_company_overview",
        description=(
            "Get company profile and overview including business description, "
            "CEO, employee count, founding date, headquarters, and key metrics."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g. 'AAPL.US', '700.HK', '600519.SH').",
                },
            },
            "required": ["symbol"],
        },
    ),
    Tool(
        name="get_stock_valuation",
        description=(
            "Get stock valuation metrics including P/E ratio, P/B ratio, "
            "market cap, EV/EBITDA, dividend yield, and other fundamental ratios."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g. 'AAPL.US', '700.HK').",
                },
            },
            "required": ["symbol"],
        },
    ),
    Tool(
        name="get_stock_ratings",
        description=(
            "Get analyst ratings and consensus for a stock. "
            "Includes buy/sell/hold counts, target price, and rating distribution."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g. 'AAPL.US', '700.HK').",
                },
            },
            "required": ["symbol"],
        },
    ),
    Tool(
        name="get_stock_panorama",
        description=(
            "Get a panoramic summary of a stock including key financial data, "
            "performance metrics, and comprehensive stock overview."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g. 'AAPL.US', '700.HK').",
                },
            },
            "required": ["symbol"],
        },
    ),
    Tool(
        name="get_stock_drivers",
        description=(
            "Get the key price drivers and catalysts for a stock. "
            "Shows factors that are influencing the stock price movement."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g. 'AAPL.US', '700.HK').",
                },
            },
            "required": ["symbol"],
        },
    ),
    Tool(
        name="search_symbols",
        description=(
            "Search and list available trading symbols. "
            "Returns symbols with their names, market, and type information. "
            "Optionally filter by market."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": (
                        "Filter by market code (e.g. 'HK', 'US', 'CN', 'SG', 'JP', 'IN'). "
                        "Leave empty to get all markets."
                    ),
                },
            },
        },
    ),
]


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@app.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    client = _get_client()
    try:
        result = _dispatch(client, name, arguments)
        return [
            TextContent(
                type="text",
                text=json.dumps(result, ensure_ascii=False, indent=2),
            )
        ]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]
    finally:
        client.close()


def _dispatch(client: InfowayClient, name: str, args: dict):
    """Route a tool call to the appropriate SDK method."""

    # --- Real-time market data (trade / depth / kline) ---
    if name == "get_realtime_trade":
        sub = _market_sub_client(client, args.get("market_type", "stock"))
        return sub.get_trade(args["codes"])

    if name == "get_market_depth":
        sub = _market_sub_client(client, args.get("market_type", "stock"))
        return sub.get_depth(args["codes"])

    if name == "get_kline":
        sub = _market_sub_client(client, args.get("market_type", "stock"))
        return sub.get_kline(
            codes=args["codes"],
            kline_type=args.get("kline_type", 8),
            count=args.get("count", 100),
        )

    # --- Market overview ---
    if name == "get_market_temperature":
        return client.market.get_temperature(market=args.get("market", "HK,US,CN,SG"))

    if name == "get_market_breadth":
        return client.market.get_breadth(market=args["market"])

    if name == "get_global_indexes":
        return client.market.get_indexes()

    if name == "get_leading_industries":
        return client.market.get_leaders(
            market=args["market"], limit=args.get("limit", 10)
        )

    # --- Plate / sector ---
    if name == "get_industry_list":
        return client.plate.get_industry(
            market=args["market"], limit=args.get("limit", 200)
        )

    if name == "get_concept_list":
        return client.plate.get_concept(
            market=args["market"], limit=args.get("limit", 100)
        )

    if name == "get_plate_members":
        return client.plate.get_members(plate_symbol=args["plate_symbol"])

    if name == "get_plate_heatmap":
        return client.plate.get_chart(
            market=args["market"], limit=args.get("limit", 50)
        )

    # --- Stock fundamentals ---
    if name == "get_company_overview":
        return client.stock_info.get_company(symbol=args["symbol"])

    if name == "get_stock_valuation":
        return client.stock_info.get_valuation(symbol=args["symbol"])

    if name == "get_stock_ratings":
        return client.stock_info.get_ratings(symbol=args["symbol"])

    if name == "get_stock_panorama":
        return client.stock_info.get_panorama(symbol=args["symbol"])

    if name == "get_stock_drivers":
        return client.stock_info.get_drivers(symbol=args["symbol"])

    # --- Basic ---
    if name == "search_symbols":
        return client.basic.get_symbols(market=args.get("market"))

    raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    import asyncio

    asyncio.run(_run())


async def _run():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    main()
