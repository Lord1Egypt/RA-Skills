"""
Command line interface for mcp-stockpile.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from . import __version__
from .client import StockpileClient
from .server import run_stdio_server
from .tools import TOOLS_METADATA


def main(argv: Optional[list[str]] = None) -> None:
    """CLI entrypoint for mcp-stockpile."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="mcp-stockpile",
        description="Official Model Context Protocol (MCP) server for Stockpile Market.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--api-url",
        dest="api_url",
        help="Stockpile Market API URL (defaults to STOCKPILE_API_URL or https://stockpile.market/api)",
    )
    parser.add_argument(
        "--api-key",
        dest="api_key",
        help="Stockpile API Key (defaults to STOCKPILE_API_KEY environment variable)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # run command (default)
    run_parser = subparsers.add_parser("run", help="Run the MCP server in STDIO mode")
    run_parser.add_argument(
        "--transport",
        choices=["stdio"],
        default="stdio",
        help="Transport type (default: stdio)",
    )

    # list-tools command
    subparsers.add_parser("list-tools", help="List all available tools and schemas")

    # info command
    subparsers.add_parser("info", help="Display server configuration and status")

    args = parser.parse_args(argv)

    client = StockpileClient(base_url=args.api_url, api_key=args.api_key)

    if args.command == "list-tools":
        print(json.dumps(TOOLS_METADATA, indent=2))
        return

    if args.command == "info":
        has_key = bool(client.api_key)
        masked_key = f"{client.api_key[:6]}...{client.api_key[-4:]}" if (has_key and len(client.api_key) > 10) else ("configured" if has_key else "missing")
        print(f"Stockpile MCP Server v{__version__}")
        print(f"API Base URL: {client.base_url}")
        print(f"API Key:      {masked_key}")
        print(f"Total Tools:  {len(TOOLS_METADATA)}")
        return

    # Default action: run stdio server
    run_stdio_server(client=client)


if __name__ == "__main__":
    main()
