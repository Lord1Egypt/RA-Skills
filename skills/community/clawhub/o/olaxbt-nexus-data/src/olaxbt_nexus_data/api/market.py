"""
Market data API client for OlaXBT Nexus Data API.
Provides access to comprehensive market overview and analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class MarketClient:
    """Client for Market API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        """
        Initialize Market client.
        
        Args:
            api_client: Base API client instance
        """
        self.api = api_client
    
    def get_overview(
        self,
        include_global: bool = True,
        include_top_coins: bool = True,
        include_fear_greed: bool = True,
    ) -> Dict[str, Any]:
        """
        Get comprehensive market overview.
        
        Args:
            include_global: Include global market metrics
            include_top_coins: Include top cryptocurrency data
            include_fear_greed: Include fear & greed index
            
        Returns:
            Market overview data
            
        Raises:
            APIError: If API request fails
        """
        params = {
            "include_global": str(include_global).lower(),
            "include_top_coins": str(include_top_coins).lower(),
            "include_fear_greed": str(include_fear_greed).lower(),
        }
        
        try:
            response = self.api.get("market/overview", params=params)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get market overview: {str(e)}")
            raise
    
    def get_top_movers(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        min_volume: Optional[float] = None,
        direction: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get top gaining and losing cryptocurrencies.
        
        Args:
            timeframe: Timeframe for price change (1h, 24h, 7d, 30d)
            limit: Maximum number of coins to return
            min_volume: Minimum trading volume filter (in USD)
            direction: Filter by direction ("gainers" or "losers")
            
        Returns:
            List of top movers
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        valid_directions = [None, "gainers", "losers"]
        if direction not in valid_directions:
            raise ValidationError("Direction must be 'gainers' or 'losers'")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        if min_volume is not None:
            if min_volume < 0:
                raise ValidationError("Min volume cannot be negative")
            params["min_volume"] = min_volume
        
        if direction:
            params["direction"] = direction
        
        try:
            response = self.api.get("market/top-movers", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get top movers: {str(e)}")
            raise
    
    def get_volume_leaders(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        exchange: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get cryptocurrencies with highest trading volume.
        
        Args:
            timeframe: Timeframe for volume calculation (1h, 24h, 7d)
            limit: Maximum number of coins to return
            exchange: Filter by specific exchange
            
        Returns:
            List of volume leaders
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        if exchange:
            params["exchange"] = exchange
        
        try:
            response = self.api.get("market/volume-leaders", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get volume leaders: {str(e)}")
            raise
    
    def get_market_cap_ranking(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get cryptocurrency market cap ranking.
        
        Args:
            limit: Maximum number of coins to return (1-500)
            offset: Pagination offset
            
        Returns:
            List of cryptocurrencies ranked by market cap
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not 1 <= limit <= 500:
            raise ValidationError("Limit must be between 1 and 500")
        
        if offset < 0:
            raise ValidationError("Offset cannot be negative")
        
        params = {
            "limit": limit,
            "offset": offset,
        }
        
        try:
            response = self.api.get("market/cap-ranking", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get market cap ranking: {str(e)}")
            raise
    
    def get_fear_greed_index(
        self,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get cryptocurrency fear and greed index.
        
        Args:
            timeframe: Timeframe for index calculation (24h, 7d, 30d)
            
        Returns:
            Fear and greed index data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("market/fear-greed", params=params)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get fear greed index: {str(e)}")
            raise
    
    def get_market_dominance(
        self,
        symbols: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get market dominance for major cryptocurrencies.
        
        Args:
            symbols: List of symbols to include (default: major coins)
            
        Returns:
            Market dominance data
            
        Raises:
            APIError: If API request fails
        """
        params = {}
        
        if symbols:
            params["symbols"] = ",".join([s.upper() for s in symbols])
        
        try:
            response = self.api.get("market/dominance", params=params)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get market dominance: {str(e)}")
            raise
    
    def get_exchange_flows(
        self,
        timeframe: str = "24h",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get exchange inflow/outflow data.
        
        Args:
            timeframe: Timeframe for flow calculation (1h, 24h, 7d)
            limit: Maximum number of exchanges to return
            
        Returns:
            List of exchange flow data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        try:
            response = self.api.get("market/exchange-flows", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get exchange flows: {str(e)}")
            raise
    
    def get_volatility_index(
        self,
        timeframe: str = "24h",
        symbols: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get market volatility index.
        
        Args:
            timeframe: Timeframe for volatility calculation (1h, 24h, 7d)
            symbols: List of symbols to include in index
            
        Returns:
            Volatility index data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "timeframe": timeframe,
        }
        
        if symbols:
            params["symbols"] = ",".join([s.upper() for s in symbols])
        
        try:
            response = self.api.get("market/volatility", params=params)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get volatility index: {str(e)}")
            raise
    
    def get_market_sentiment(
        self,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get overall market sentiment.
        
        Args:
            timeframe: Timeframe for sentiment analysis (1h, 24h, 7d)
            
        Returns:
            Market sentiment data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("market/sentiment", params=params)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get market sentiment: {str(e)}")
            raise