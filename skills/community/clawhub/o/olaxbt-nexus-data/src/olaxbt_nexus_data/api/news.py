"""
News API client for OlaXBT Nexus Data API.
Provides access to cryptocurrency news aggregation and analysis.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class NewsClient:
    """Client for News API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        """
        Initialize News client.
        
        Args:
            api_client: Base API client instance
        """
        self.api = api_client
    
    def get_latest(
        self,
        limit: int = 10,
        offset: int = 0,
        symbols: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get latest cryptocurrency news.
        
        Args:
            limit: Maximum number of news items to return (1-100)
            offset: Pagination offset
            symbols: Filter by cryptocurrency symbols (e.g., ["BTC", "ETH"])
            categories: Filter by categories (e.g., ["market", "regulation"])
            sources: Filter by news sources
            
        Returns:
            List of news items
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        # Validate parameters
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValidationError("Offset cannot be negative")
        
        # Build query parameters
        params = {
            "limit": limit,
            "offset": offset,
        }
        
        if symbols:
            params["symbols"] = ",".join(symbols)
        
        if categories:
            params["categories"] = ",".join(categories)
        
        if sources:
            params["sources"] = ",".join(sources)
        
        try:
            response = self.api.get("news/latest", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get latest news: {str(e)}")
            raise
    
    def search(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_sentiment: Optional[float] = None,
        max_sentiment: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search cryptocurrency news.
        
        Args:
            query: Search query string
            limit: Maximum results (1-100)
            offset: Pagination offset
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            min_sentiment: Minimum sentiment score (-1 to 1)
            max_sentiment: Maximum sentiment score (-1 to 1)
            
        Returns:
            List of news items matching search
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        # Validate parameters
        if not query.strip():
            raise ValidationError("Search query cannot be empty")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        if min_sentiment is not None and not -1 <= min_sentiment <= 1:
            raise ValidationError("Min sentiment must be between -1 and 1")
        
        if max_sentiment is not None and not -1 <= max_sentiment <= 1:
            raise ValidationError("Max sentiment must be between -1 and 1")
        
        # Build query parameters
        params = {
            "q": query,
            "limit": limit,
            "offset": offset,
        }
        
        if start_date:
            params["start_date"] = start_date
        
        if end_date:
            params["end_date"] = end_date
        
        if min_sentiment is not None:
            params["min_sentiment"] = min_sentiment
        
        if max_sentiment is not None:
            params["max_sentiment"] = max_sentiment
        
        try:
            response = self.api.get("news/search", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to search news: {str(e)}")
            raise
    
    def get_trending(
        self,
        timeframe: str = "24h",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get trending news topics.
        
        Args:
            timeframe: Timeframe for trending analysis (1h, 24h, 7d, 30d)
            limit: Maximum number of topics to return
            
        Returns:
            List of trending topics
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        try:
            response = self.api.get("news/trending", params=params)
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get trending news: {str(e)}")
            raise
    
    def get_sentiment(
        self,
        symbol: str,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get sentiment analysis for a cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., "BTC")
            timeframe: Timeframe for sentiment analysis (1h, 24h, 7d, 30d)
            
        Returns:
            Sentiment analysis data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["1h", "24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("news/sentiment", params=params)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to get sentiment for {symbol}: {str(e)}")
            raise
    
    def get_sources(self) -> List[Dict[str, Any]]:
        """
        Get available news sources.
        
        Returns:
            List of news sources
            
        Raises:
            APIError: If API request fails
        """
        try:
            response = self.api.get("news/sources")
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get news sources: {str(e)}")
            raise
    
    def get_categories(self) -> List[str]:
        """
        Get available news categories.
        
        Returns:
            List of news categories
            
        Raises:
            APIError: If API request fails
        """
        try:
            response = self.api.get("news/categories")
            return response.get("data", [])
        
        except APIError as e:
            logger.error(f"Failed to get news categories: {str(e)}")
            raise
    
    def summarize(
        self,
        news_ids: List[str],
        max_length: int = 500,
    ) -> Dict[str, Any]:
        """
        Generate summary for multiple news articles.
        
        Args:
            news_ids: List of news article IDs
            max_length: Maximum summary length in characters
            
        Returns:
            Summary data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not news_ids:
            raise ValidationError("At least one news ID is required")
        
        if not 100 <= max_length <= 2000:
            raise ValidationError("Max length must be between 100 and 2000 characters")
        
        data = {
            "news_ids": news_ids,
            "max_length": max_length,
        }
        
        try:
            response = self.api.post("news/summarize", json_data=data)
            return response.get("data", {})
        
        except APIError as e:
            logger.error(f"Failed to generate news summary: {str(e)}")
            raise