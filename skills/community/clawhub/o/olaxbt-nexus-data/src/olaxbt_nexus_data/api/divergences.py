"""
Market Divergence API client for OlaXBT Nexus Data API.
Provides market divergence detection and analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class DivergencesClient:
    """Client for Market Divergence API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_divergences(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        divergence_type: str = "all",
        min_confidence: float = 0.6,
    ) -> List[Dict[str, Any]]:
        """
        Get market divergences.
        
        Args:
            timeframe: Timeframe for divergence detection
            limit: Maximum number of divergences
            divergence_type: Type of divergences
            min_confidence: Minimum confidence threshold
            
        Returns:
            Market divergences
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        valid_types = ["all", "price_oi", "price_funding", "price_smart_money", "oi_funding"]
        if divergence_type not in valid_types:
            raise ValidationError(f"Divergence type must be one of: {valid_types}")
        
        if not 0.0 <= min_confidence <= 1.0:
            raise ValidationError("Min confidence must be between 0.0 and 1.0")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
            "type": divergence_type,
            "min_confidence": min_confidence,
        }
        
        try:
            response = self.api.get("divergences", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get divergences: {str(e)}")
            raise
    
    def get_symbol_divergences(
        self,
        symbol: str,
        timeframe: str = "24h",
        include_details: bool = True,
    ) -> Dict[str, Any]:
        """
        Get divergences for specific symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for analysis
            include_details: Include detailed divergence data
            
        Returns:
            Symbol divergences
            
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
            "timeframe": timeframe,
            "include_details": str(include_details).lower(),
        }
        
        try:
            response = self.api.get(f"divergences/{symbol.upper()}", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get divergences for {symbol}: {str(e)}")
            raise
    
    def get_divergence_types(self) -> List[Dict[str, Any]]:
        """
        Get available divergence types.
        
        Returns:
            Divergence types
            
        Raises:
            APIError: If API request fails
        """
        try:
            response = self.api.get("divergences/types")
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get divergence types: {str(e)}")
            raise
    
    def get_divergence_history(
        self,
        symbol: str,
        divergence_type: str,
        timeframe: str = "7d",
        interval: str = "1h",
    ) -> List[Dict[str, Any]]:
        """
        Get divergence history for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol
            divergence_type: Type of divergence
            timeframe: Overall timeframe
            interval: Data point interval
            
        Returns:
            Divergence history
            
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
            "divergence_type": divergence_type,
            "timeframe": timeframe,
            "interval": interval,
        }
        
        try:
            response = self.api.get("divergences/history", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get divergence history for {symbol}: {str(e)}")
            raise
    
    def analyze_divergence_pattern(
        self,
        symbol: str,
        start_time: str,
        end_time: str,
        divergence_type: str,
    ) -> Dict[str, Any]:
        """
        Analyze divergence pattern for a specific period.
        
        Args:
            symbol: Cryptocurrency symbol
            start_time: Start time (ISO format)
            end_time: End time (ISO format)
            divergence_type: Type of divergence
            
        Returns:
            Divergence pattern analysis
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        if not start_time or not end_time:
            raise ValidationError("Start time and end time are required")
        
        data = {
            "symbol": symbol.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "divergence_type": divergence_type,
        }
        
        try:
            response = self.api.post("divergences/analyze-pattern", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to analyze divergence pattern for {symbol}: {str(e)}")
            raise
    
    def get_divergence_alerts(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        alert_level: str = "medium",
    ) -> List[Dict[str, Any]]:
        """
        Get divergence alerts.
        
        Args:
            timeframe: Timeframe for alerts
            limit: Maximum number of alerts
            alert_level: Alert level (low, medium, high, critical)
            
        Returns:
            Divergence alerts
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        valid_levels = ["low", "medium", "high", "critical"]
        if alert_level not in valid_levels:
            raise ValidationError(f"Alert level must be one of: {valid_levels}")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
            "alert_level": alert_level,
        }
        
        try:
            response = self.api.get("divergences/alerts", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get divergence alerts: {str(e)}")
            raise