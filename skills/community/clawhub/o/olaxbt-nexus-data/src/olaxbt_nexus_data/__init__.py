"""
OlaXBT Nexus Data API Client

Official Python client for the OlaXBT Nexus Data API.
Uses a JWT (obtained via the Nexus auth flow); no private key in the skill.
news, KOL tracking, technical indicators, and comprehensive market analysis.
"""

__version__ = "1.0.0"
__author__ = "OlaXBT Team"
__email__ = "contact@olaxbt.xyz"
__license__ = "MIT"

import os
import logging
from typing import Optional, Dict, Any

from .core.auth import NexusAuth, NexusAuthJWT
from .core.client import NexusAPIClient
from .core.security import SecurityConfig
from .api.news import NewsClient
from .api.kol import KOLClient
from .api.market import MarketClient
from .api.technical import TechnicalClient
from .api.smart_money import SmartMoneyClient
from .api.liquidations import LiquidationsClient
from .api.sentiment import SentimentClient
from .api.etf import ETFClient
from .api.oi import OIClient
from .api.coin import CoinClient
from .api.assistant import AssistantClient
from .api.ask_nexus import AskNexusClient
from .api.divergences import DivergencesClient
from .api.credits import CreditsClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NexusClient:
    """Main client for OlaXBT Nexus Data API. Uses NEXUS_JWT only (no private key in skill)."""

    def __init__(
        self,
        jwt_token: Optional[str] = None,
        auth_url: Optional[str] = None,
        data_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit: int = 1000,
    ):
        """
        Initialize the Nexus client with a JWT. The skill does not use private keys.

        Obtain the JWT using the [Nexus Skills API auth flow](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md):
        POST /auth/message with your wallet address, sign the message with your wallet
        (e.g. via OpenClaw or a one-time sign-in), then POST /auth/wallet to get the token.

        Args:
            jwt_token: Nexus JWT (optional, uses NEXUS_JWT env var)
            auth_url: Authentication API URL (optional)
            data_url: Data API URL (optional)
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            rate_limit: Maximum requests per hour

        Raises:
            ValueError: If NEXUS_JWT is not set
        """
        jwt = jwt_token or os.getenv("NEXUS_JWT")
        if not jwt or not jwt.strip():
            raise ValueError(
                "NEXUS_JWT is required. Obtain a JWT using the Nexus auth flow "
                "(see https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md): "
                "POST /auth/message, sign the message with your wallet, POST /auth/wallet, then set NEXUS_JWT."
            )

        self.auth_url = auth_url or os.getenv("NEXUS_AUTH_URL", "https://api.olaxbt.xyz/api")
        self.data_url = data_url or os.getenv("NEXUS_DATA_URL", "https://api-data.olaxbt.xyz/api/v1")

        self.security_config = SecurityConfig(
            encrypt_jwt=False,
            rate_limit=rate_limit,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.auth = NexusAuthJWT(
            jwt_token=jwt.strip(),
            auth_url=self.auth_url,
            security_config=self.security_config,
        )
        self.wallet_address = self.auth.wallet_address
        
        # Initialize API client
        self.api_client = NexusAPIClient(
            auth_client=self.auth,
            data_url=self.data_url,
            security_config=self.security_config,
        )
        
        # Initialize API clients
        self.news = NewsClient(self.api_client)
        self.kol = KOLClient(self.api_client)
        self.market = MarketClient(self.api_client)
        self.technical = TechnicalClient(self.api_client)
        self.smart_money = SmartMoneyClient(self.api_client)
        self.liquidations = LiquidationsClient(self.api_client)
        self.sentiment = SentimentClient(self.api_client)
        self.etf = ETFClient(self.api_client)
        self.oi = OIClient(self.api_client)
        self.coin = CoinClient(self.api_client)
        self.assistant = AssistantClient(self.api_client)
        self.ask_nexus = AskNexusClient(self.api_client)
        self.divergences = DivergencesClient(self.api_client)
        self.credits = CreditsClient(self.api_client)
        
        logger.info("Nexus client initialized with JWT.")
    
    def authenticate(self) -> str:
        """
        Authenticate with the Nexus API and get JWT token.
        
        Returns:
            JWT token string
            
        Raises:
            AuthenticationError: If authentication fails
        """
        return self.auth.authenticate()
    
    def get_credits_balance(self) -> Dict[str, Any]:
        """
        Get current credits balance.
        
        Returns:
            Dictionary with credits information
            
        Raises:
            APIError: If API request fails
        """
        return self.api_client.get_credits_balance()
    
    def health_check(self) -> bool:
        """
        Check if the API is healthy and accessible.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = self.api_client._request("GET", "health")
            return response.get("status") == "healthy"
        except Exception:
            return False
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"NexusClient(url={self.data_url})"


# Export main classes
__all__ = [
    "NexusClient",
    "NexusAuth",
    "NexusAuthJWT",
    "NexusAPIClient",
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

# Export exceptions
from .core.exceptions import (
    NexusError,
    AuthenticationError,
    APIError,
    RateLimitError,
    ValidationError,
)

__all__.extend([
    "NexusError",
    "AuthenticationError",
    "APIError",
    "RateLimitError",
    "ValidationError",
])