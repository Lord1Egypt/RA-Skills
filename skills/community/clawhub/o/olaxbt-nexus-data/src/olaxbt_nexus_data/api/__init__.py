"""
API endpoint clients for OlaXBT Nexus Data API.

This package contains client classes for each API endpoint:
- News API
- KOL API
- Market data
- Technical indicators
- Smart money tracking
- And more...
"""

from .news import NewsClient
from .kol import KOLClient
from .market import MarketClient
from .technical import TechnicalClient
from .smart_money import SmartMoneyClient
from .liquidations import LiquidationsClient
from .sentiment import SentimentClient
from .etf import ETFClient
from .oi import OIClient
from .coin import CoinClient
from .assistant import AssistantClient
from .ask_nexus import AskNexusClient
from .divergences import DivergencesClient
from .credits import CreditsClient

__all__ = [
    "NewsClient",
    "KOLClient",
    "MarketClient",
    "TechnicalClient",
    "SmartMoneyClient",
    "LiquidationsClient",
    "SentimentClient",
    "ETFClient",
    "OIClient",
    "CoinClient",
    "AssistantClient",
    "AskNexusClient",
    "DivergencesClient",
    "CreditsClient",
]