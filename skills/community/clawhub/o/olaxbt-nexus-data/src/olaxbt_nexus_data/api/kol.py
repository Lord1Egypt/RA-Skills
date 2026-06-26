"""
KOL (Key Opinion Leader) API client for OlaXBT Nexus Data API.
Provides access to KOL tracking, tweet analysis, and symbol heatmaps.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class KOLClient:
    """Client for KOL API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        """
        Initialize KOL client.
        
        Args:
            api_client: Base API client instance
        """
        self.api = api_client
    
    def get_heatmap(
        self,
        symbol: Optional[str] = None,
        timeframe: str = "24h",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get KOL heatmap for symbols.
        
        Args:
            symbol: Filter by specific symbol (e.g., "BTC")
            timeframe: Timeframe for analysis (1h, 24h, 7d, 30d)
            limit: Maximum number of KOLs to return
            
        Returns:
            List of KOL heatmap data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d", "30d"]
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
            response = self.api.get("kol/heatmap", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get KOL heatmap: {str(e)}")
            raise
    
    def get_top_kols(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        min_followers: Optional[int] = None,
        min_engagement: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get top KOLs by influence.
        
        Args:
            timeframe: Timeframe for analysis (24h, 7d, 30d)
            limit: Maximum number of KOLs to return
            min_followers: Minimum follower count filter
            min_engagement: Minimum engagement rate filter
            
        Returns:
            List of top KOLs
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        if min_followers is not None:
            if min_followers < 0:
                raise ValidationError("Min followers cannot be negative")
            params["min_followers"] = min_followers
        
        if min_engagement is not None:
            if not 0 <= min_engagement <= 1:
                raise ValidationError("Min engagement must be between 0 and 1")
            params["min_engagement"] = min_engagement
        
        try:
            response = self.api.get("kol/top", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get top KOLs: {str(e)}")
            raise
    
    def get_kol_details(
        self,
        kol_id: str,
        include_tweets: bool = True,
        tweet_limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Get detailed information for a specific KOL.
        
        Args:
            kol_id: KOL identifier (username or ID)
            include_tweets: Whether to include recent tweets
            tweet_limit: Maximum number of tweets to include
            
        Returns:
            KOL details
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not kol_id:
            raise ValidationError("KOL ID is required")
        
        if not 1 <= tweet_limit <= 50:
            raise ValidationError("Tweet limit must be between 1 and 50")
        
        params = {
            "include_tweets": str(include_tweets).lower(),
            "tweet_limit": tweet_limit,
        }
        
        try:
            response = self.api.get(f"kol/{kol_id}", params=params)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get KOL details for {kol_id}: {str(e)}")
            raise
    
    def get_symbol_mentions(
        self,
        symbol: str,
        timeframe: str = "24h",
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get KOL mentions for a specific symbol.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., "BTC")
            timeframe: Timeframe for analysis (1h, 24h, 7d, 30d)
            limit: Maximum number of mentions to return
            
        Returns:
            List of KOL mentions
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["1h", "24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 200:
            raise ValidationError("Limit must be between 1 and 200")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "limit": limit,
        }
        
        try:
            response = self.api.get("kol/mentions", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get symbol mentions for {symbol}: {str(e)}")
            raise
    
    def get_tweet_analysis(
        self,
        tweet_id: str,
    ) -> Dict[str, Any]:
        """
        Get analysis for a specific tweet.
        
        Args:
            tweet_id: Twitter tweet ID
            
        Returns:
            Tweet analysis data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not tweet_id:
            raise ValidationError("Tweet ID is required")
        
        try:
            response = self.api.get(f"kol/tweet/{tweet_id}")
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get tweet analysis for {tweet_id}: {str(e)}")
            raise
    
    def get_sentiment_trend(
        self,
        symbol: str,
        timeframe: str = "7d",
        interval: str = "1h",
    ) -> List[Dict[str, Any]]:
        """
        Get sentiment trend for a symbol over time.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Overall timeframe (24h, 7d, 30d)
            interval: Time interval for data points (1h, 4h, 12h, 1d)
            
        Returns:
            List of sentiment data points
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        valid_intervals = ["1h", "4h", "12h", "1d"]
        if interval not in valid_intervals:
            raise ValidationError(f"Interval must be one of: {valid_intervals}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "interval": interval,
        }
        
        try:
            response = self.api.get("kol/sentiment/trend", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get sentiment trend for {symbol}: {str(e)}")
            raise
    
    def search_kols(
        self,
        query: str,
        limit: int = 20,
        min_followers: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for KOLs by name or description.
        
        Args:
            query: Search query string
            limit: Maximum results to return
            min_followers: Minimum follower count filter
            
        Returns:
            List of matching KOLs
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not query.strip():
            raise ValidationError("Search query cannot be empty")
        
        if not 1 <= limit <= 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        params = {
            "q": query,
            "limit": limit,
        }
        
        if min_followers is not None:
            if min_followers < 0:
                raise ValidationError("Min followers cannot be negative")
            params["min_followers"] = min_followers
        
        try:
            response = self.api.get("kol/search", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to search KOLs: {str(e)}")
            raise