"""
Sentiment API client for OlaXBT Nexus Data API.
Provides access to market sentiment analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class SentimentClient:
    """Client for Sentiment API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_sentiment(
        self,
        symbol: Optional[str] = None,
        timeframe: str = "24h",
        sources: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get sentiment analysis.
        
        Args:
            symbol: Filter by cryptocurrency symbol
            timeframe: Timeframe for sentiment analysis
            sources: Data sources to include
            
        Returns:
            Sentiment analysis data
            
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
        
        if symbol:
            params["symbol"] = symbol.upper()
        
        if sources:
            params["sources"] = ",".join(sources)
        
        try:
            response = self.api.get("sentiment", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get sentiment analysis: {str(e)}")
            raise
    
    def get_sentiment_trend(
        self,
        symbol: str,
        timeframe: str = "7d",
        interval: str = "1h",
    ) -> List[Dict[str, Any]]:
        """
        Get sentiment trend over time.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Overall timeframe
            interval: Data point interval
            
        Returns:
            Sentiment trend data
            
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
            response = self.api.get("sentiment/trend", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get sentiment trend for {symbol}: {str(e)}")
            raise
    
    def get_social_sentiment(
        self,
        symbol: str,
        platform: str = "twitter",
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get social media sentiment.
        
        Args:
            symbol: Cryptocurrency symbol
            platform: Social media platform
            timeframe: Timeframe for analysis
            
        Returns:
            Social sentiment data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_platforms = ["twitter", "reddit", "telegram", "all"]
        if platform not in valid_platforms:
            raise ValidationError(f"Platform must be one of: {valid_platforms}")
        
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "symbol": symbol.upper(),
            "platform": platform,
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("sentiment/social", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get social sentiment for {symbol}: {str(e)}")
            raise
    
    def get_fear_greed_index(
        self,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get fear and greed index.
        
        Args:
            timeframe: Timeframe for index
            
        Returns:
            Fear and greed index data
            
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
            response = self.api.get("sentiment/fear-greed", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get fear greed index: {str(e)}")
            raise
    
    def get_sentiment_indicators(
        self,
        symbol: Optional[str] = None,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get sentiment indicators.
        
        Args:
            symbol: Filter by cryptocurrency symbol
            timeframe: Timeframe for indicators
            
        Returns:
            Sentiment indicators data
            
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
        
        if symbol:
            params["symbol"] = symbol.upper()
        
        try:
            response = self.api.get("sentiment/indicators", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get sentiment indicators: {str(e)}")
            raise