"""
Liquidations API client for OlaXBT Nexus Data API.
Provides access to liquidation data and open interest analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class LiquidationsClient:
    """Client for Liquidations API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_liquidations(
        self,
        symbol: Optional[str] = None,
        timeframe: str = "24h",
        liquidation_type: str = "all",
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Get liquidation data.
        
        Args:
            symbol: Filter by cryptocurrency symbol
            timeframe: Timeframe for liquidation data
            liquidation_type: Type of liquidations (long, short, all)
            limit: Maximum number of liquidations
            
        Returns:
            Liquidation data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        valid_types = ["all", "long", "short"]
        if liquidation_type not in valid_types:
            raise ValidationError(f"Liquidation type must be one of: {valid_types}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "timeframe": timeframe,
            "type": liquidation_type,
            "limit": limit,
        }
        
        if symbol:
            params["symbol"] = symbol.upper()
        
        try:
            response = self.api.get("liquidations", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get liquidations: {str(e)}")
            raise
    
    def get_oi_history(
        self,
        symbol: str,
        timeframe: str = "7d",
        interval: str = "1h",
    ) -> List[Dict[str, Any]]:
        """
        Get open interest history for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Overall timeframe
            interval: Data point interval
            
        Returns:
            Open interest history
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        valid_intervals = ["5m", "15m", "1h", "4h", "1d"]
        if interval not in valid_intervals:
            raise ValidationError(f"Interval must be one of: {valid_intervals}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "interval": interval,
        }
        
        try:
            response = self.api.get("liquidations/oi-history", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get OI history for {symbol}: {str(e)}")
            raise
    
    def get_funding_rates(
        self,
        symbol: Optional[str] = None,
        timeframe: str = "24h",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get funding rates data.
        
        Args:
            symbol: Filter by cryptocurrency symbol
            timeframe: Timeframe for funding rates
            limit: Maximum number of rates
            
        Returns:
            Funding rates data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "8h", "24h"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        if symbol:
            params["symbol"] = symbol.upper()
        
        try:
            response = self.api.get("liquidations/funding-rates", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get funding rates: {str(e)}")
            raise
    
    def get_large_liquidations(
        self,
        min_amount: float = 1000000,  # 1 million USD
        timeframe: str = "24h",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get large liquidation events.
        
        Args:
            min_amount: Minimum liquidation amount in USD
            timeframe: Timeframe for events
            limit: Maximum number of events
            
        Returns:
            Large liquidation events
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if min_amount < 0:
            raise ValidationError("Min amount cannot be negative")
        
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        params = {
            "min_amount": min_amount,
            "timeframe": timeframe,
            "limit": limit,
        }
        
        try:
            response = self.api.get("liquidations/large", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get large liquidations: {str(e)}")
            raise
    
    def get_heatmap(
        self,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get liquidation heatmap.
        
        Args:
            timeframe: Timeframe for heatmap
            
        Returns:
            Liquidation heatmap data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("liquidations/heatmap", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get liquidation heatmap: {str(e)}")
            raise