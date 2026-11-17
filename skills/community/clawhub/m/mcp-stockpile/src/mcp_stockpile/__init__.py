"""
Official Model Context Protocol (MCP) server for Stockpile Market.
https://stockpile.market
"""

__version__ = "2.0.1"
__author__ = "Stockpile Market"

from .client import StockpileClient
from .server import create_server, run_stdio_server

__all__ = ["__version__", "StockpileClient", "create_server", "run_stdio_server"]
