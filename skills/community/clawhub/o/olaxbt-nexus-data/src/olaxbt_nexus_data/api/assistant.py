"""
AIO Assistant API client for OlaXBT Nexus Data API.
Provides market analysis and trading signals.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class AssistantClient:
    """Client for AIO Assistant API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_analysis(
        self,
        symbol: str,
        timeframe: str = "1h",
        include_signals: bool = True,
        include_risk: bool = True,
    ) -> Dict[str, Any]:
        """
        Get AI analysis for a cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Analysis timeframe (1h, 4h, 1d, 1w)
            include_signals: Include trading signals
            include_risk: Include risk assessment
            
        Returns:
            AI analysis data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_timeframes = ["1h", "4h", "1d", "1w"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "include_signals": str(include_signals).lower(),
            "include_risk": str(include_risk).lower(),
        }
        
        try:
            response = self.api.get("assistant/analysis", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get AI analysis for {symbol}: {str(e)}")
            raise
    
    def get_signals(
        self,
        symbols: Optional[List[str]] = None,
        timeframe: str = "1h",
        limit: int = 10,
        min_confidence: float = 0.6,
    ) -> List[Dict[str, Any]]:
        """
        Get trading signals from AI assistant.
        
        Args:
            symbols: List of symbols to analyze (None for all)
            timeframe: Signal timeframe (1h, 4h, 1d)
            limit: Maximum number of signals
            min_confidence: Minimum confidence threshold (0.0-1.0)
            
        Returns:
            List of trading signals
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not 1 <= limit <= 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        if not 0.0 <= min_confidence <= 1.0:
            raise ValidationError("Min confidence must be between 0.0 and 1.0")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
            "min_confidence": min_confidence,
        }
        
        if symbols:
            params["symbols"] = ",".join([s.upper() for s in symbols])
        
        try:
            response = self.api.get("assistant/signals", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get trading signals: {str(e)}")
            raise
    
    def get_market_insights(
        self,
        timeframe: str = "24h",
        include_topics: bool = True,
        include_sentiment: bool = True,
    ) -> Dict[str, Any]:
        """
        Get market insights from AI assistant.
        
        Args:
            timeframe: Insights timeframe (1h, 24h, 7d)
            include_topics: Include trending topics
            include_sentiment: Include sentiment analysis
            
        Returns:
            Market insights data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "timeframe": timeframe,
            "include_topics": str(include_topics).lower(),
            "include_sentiment": str(include_sentiment).lower(),
        }
        
        try:
            response = self.api.get("assistant/insights", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get market insights: {str(e)}")
            raise
    
    def ask_question(
        self,
        question: str,
        context: Optional[str] = None,
        max_tokens: int = 500,
    ) -> Dict[str, Any]:
        """
        Ask a question to the AI assistant.
        
        Args:
            question: Question to ask
            context: Additional context for the question
            max_tokens: Maximum response length
            
        Returns:
            AI assistant response
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not question or not question.strip():
            raise ValidationError("Question cannot be empty")
        
        if not 10 <= max_tokens <= 2000:
            raise ValidationError("Max tokens must be between 10 and 2000")
        
        data = {
            "question": question.strip(),
            "max_tokens": max_tokens,
        }
        
        if context:
            data["context"] = context.strip()
        
        try:
            response = self.api.post("assistant/ask", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to ask question: {str(e)}")
            raise