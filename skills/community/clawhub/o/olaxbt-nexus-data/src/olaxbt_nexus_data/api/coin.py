"""
Coin data API client for OlaXBT Nexus Data API.
Provides access to per-coin data and metrics.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class CoinClient:
    """Client for Coin Data API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_coin_data(
        self,
        symbol: str,
        include_metrics: bool = True,
        include_social: bool = True,
        include_technical: bool = False,
    ) -> Dict[str, Any]:
        """
        Get comprehensive data for a specific coin.
        
        Args:
            symbol: Cryptocurrency symbol
            include_metrics: Include price and market metrics
            include_social: Include social data
            include_technical: Include technical indicators
            
        Returns:
            Coin data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        params = {
            "include_metrics": str(include_metrics).lower(),
            "include_social": str(include_social).lower(),
            "include_technical": str(include_technical).lower(),
        }
        
        try:
            response = self.api.get(f"coin/{symbol.upper()}", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get coin data for {symbol}: {str(e)}")
            raise
    
    def get_price_history(
        self,
        symbol: str,
        timeframe: str = "7d",
        interval: str = "1h",
    ) -> List[Dict[str, Any]]:
        """
        Get price history for a coin.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Overall timeframe
            interval: Data point interval
            
        Returns:
            Price history data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["1h", "4h", "24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        valid_intervals = ["1m", "5m", "15m", "1h", "4h", "1d"]
        if interval not in valid_intervals:
            raise ValidationError(f"Interval must be one of: {valid_intervals}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "interval": interval,
        }
        
        try:
            response = self.api.get("coin/price-history", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get price history for {symbol}: {str(e)}")
            raise
    
    def get_coin_metrics(
        self,
        symbol: str,
    ) -> Dict[str, Any]:
        """
        Get detailed metrics for a coin.
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Coin metrics
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        try:
            response = self.api.get(f"coin/{symbol.upper()}/metrics")
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get coin metrics for {symbol}: {str(e)}")
            raise
    
    def get_coin_social(
        self,
        symbol: str,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get social data for a coin.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for social data
            
        Returns:
            Social data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("coin/social", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get social data for {symbol}: {str(e)}")
            raise
    
    def get_coin_development(
        self,
        symbol: str,
        include_github: bool = True,
        include_community: bool = True,
    ) -> Dict[str, Any]:
        """
        Get development and community data for a coin.
        
        Args:
            symbol: Cryptocurrency symbol
            include_github: Include GitHub metrics
            include_community: Include community metrics
            
        Returns:
            Development data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        params = {
            "include_github": str(include_github).lower(),
            "include_community": str(include_community).lower(),
        }
        
        try:
            response = self.api.get(f"coin/{symbol.upper()}/development", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get development data for {symbol}: {str(e)}")
            raise
    
    def compare_coins(
        self,
        symbols: List[str],
        metrics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Compare multiple coins.
        
        Args:
            symbols: List of cryptocurrency symbols
            metrics: Specific metrics to compare
            
        Returns:
            Comparison data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbols or len(symbols) < 2:
            raise ValidationError("At least 2 symbols are required")
        
        if len(symbols) > 10:
            raise ValidationError("Maximum 10 symbols allowed")
        
        data = {
            "symbols": [s.upper() for s in symbols],
        }
        
        if metrics:
            data["metrics"] = metrics
        
        try:
            response = self.api.post("coin/compare", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to compare coins: {str(e)}")
            raise