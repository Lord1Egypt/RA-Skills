"""
Open Interest API client for OlaXBT Nexus Data API.
Provides open interest analysis and rankings.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class OIClient:
    """Client for Open Interest API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_oi_ranking(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        sort_by: str = "oi_value",
    ) -> List[Dict[str, Any]]:
        """
        Get open interest ranking.
        
        Args:
            timeframe: Timeframe for ranking
            limit: Maximum number of rankings
            sort_by: Sort criteria
            
        Returns:
            Open interest ranking
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        valid_sorts = ["oi_value", "oi_change", "volume", "symbol"]
        if sort_by not in valid_sorts:
            raise ValidationError(f"Sort by must be one of: {valid_sorts}")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
            "sort_by": sort_by,
        }
        
        try:
            response = self.api.get("oi/ranking", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get OI ranking: {str(e)}")
            raise
    
    def get_oi_changes(
        self,
        symbol: Optional[str] = None,
        timeframe: str = "24h",
        change_type: str = "absolute",
    ) -> Dict[str, Any]:
        """
        Get open interest changes.
        
        Args:
            symbol: Filter by cryptocurrency symbol
            timeframe: Timeframe for changes
            change_type: Type of change (absolute, percentage)
            
        Returns:
            Open interest changes
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        valid_types = ["absolute", "percentage"]
        if change_type not in valid_types:
            raise ValidationError(f"Change type must be one of: {valid_types}")
        
        params = {
            "timeframe": timeframe,
            "change_type": change_type,
        }
        
        if symbol:
            params["symbol"] = symbol.upper()
        
        try:
            response = self.api.get("oi/changes", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get OI changes: {str(e)}")
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
            response = self.api.get("oi/history", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get OI history for {symbol}: {str(e)}")
            raise
    
    def get_oi_heatmap(
        self,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get open interest heatmap.
        
        Args:
            timeframe: Timeframe for heatmap
            
        Returns:
            Open interest heatmap
            
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
            response = self.api.get("oi/heatmap", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get OI heatmap: {str(e)}")
            raise
    
    def get_funding_correlation(
        self,
        symbol: str,
        timeframe: str = "7d",
    ) -> Dict[str, Any]:
        """
        Get correlation between OI and funding rates.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for analysis
            
        Returns:
            Funding correlation data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("oi/funding-correlation", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get funding correlation for {symbol}: {str(e)}")
            raise
    
    def get_oi_concentration(
        self,
        symbol: str,
    ) -> Dict[str, Any]:
        """
        Get open interest concentration analysis.
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            OI concentration data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        try:
            response = self.api.get(f"oi/{symbol.upper()}/concentration")
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get OI concentration for {symbol}: {str(e)}")
            raise