"""
Technical indicators API client for OlaXBT Nexus Data API.
Provides access to technical analysis indicators and trading signals.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class TechnicalClient:
    """Client for Technical Indicators API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_indicators(
        self,
        symbol: str,
        timeframe: str = "1h",
        indicators: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get technical indicators for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for indicators
            indicators: Specific indicators to include
            
        Returns:
            Technical indicators data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["1m", "5m", "15m", "1h", "4h", "1d", "1w"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        if indicators:
            params["indicators"] = ",".join(indicators)
        
        try:
            response = self.api.get("technical/indicators", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get technical indicators for {symbol}: {str(e)}")
            raise
    
    def get_signals(
        self,
        symbol: str,
        timeframe: str = "1h",
        signal_types: Optional[List[str]] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get trading signals for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for signals
            signal_types: Types of signals to include
            limit: Maximum number of signals
            
        Returns:
            List of trading signals
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "limit": limit,
        }
        
        if signal_types:
            params["signal_types"] = ",".join(signal_types)
        
        try:
            response = self.api.get("technical/signals", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get trading signals for {symbol}: {str(e)}")
            raise
    
    def get_support_resistance(
        self,
        symbol: str,
        timeframe: str = "1d",
        levels: int = 5,
    ) -> Dict[str, Any]:
        """
        Get support and resistance levels.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for analysis
            levels: Number of levels to return
            
        Returns:
            Support and resistance data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        if not 1 <= levels <= 10:
            raise ValidationError("Levels must be between 1 and 10")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "levels": levels,
        }
        
        try:
            response = self.api.get("technical/support-resistance", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get support/resistance for {symbol}: {str(e)}")
            raise
    
    def get_trend_analysis(
        self,
        symbol: str,
        timeframe: str = "1d",
    ) -> Dict[str, Any]:
        """
        Get trend analysis for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for trend analysis
            
        Returns:
            Trend analysis data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("technical/trend", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get trend analysis for {symbol}: {str(e)}")
            raise
    
    def get_volume_analysis(
        self,
        symbol: str,
        timeframe: str = "1h",
    ) -> Dict[str, Any]:
        """
        Get volume analysis for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for volume analysis
            
        Returns:
            Volume analysis data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("technical/volume", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get volume analysis for {symbol}: {str(e)}")
            raise
    
    def get_momentum_indicators(
        self,
        symbol: str,
        timeframe: str = "1h",
    ) -> Dict[str, Any]:
        """
        Get momentum indicators for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for indicators
            
        Returns:
            Momentum indicators data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("technical/momentum", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get momentum indicators for {symbol}: {str(e)}")
            raise