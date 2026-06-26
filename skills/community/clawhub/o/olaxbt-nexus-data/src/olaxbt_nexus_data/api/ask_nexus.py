"""
Ask Nexus API client for OlaXBT Nexus Data API.
Provides AI-powered cryptocurrency chat and analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class AskNexusClient:
    """Client for Ask Nexus API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Chat with Ask Nexus AI.
        
        Args:
            message: User message
            conversation_id: Conversation ID for context
            context: Additional context data
            max_tokens: Maximum response tokens
            
        Returns:
            Chat response with credits usage
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")
        
        if not 10 <= max_tokens <= 4000:
            raise ValidationError("Max tokens must be between 10 and 4000")
        
        data = {
            "message": message.strip(),
            "max_tokens": max_tokens,
        }
        
        if conversation_id:
            data["conversation_id"] = conversation_id
        
        if context:
            data["context"] = context
        
        try:
            response = self.api.post("ask-nexus/chat", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to chat with Ask Nexus: {str(e)}")
            raise
    
    def analyze_market(
        self,
        query: str,
        symbols: Optional[List[str]] = None,
        timeframe: str = "24h",
        include_charts: bool = False,
    ) -> Dict[str, Any]:
        """
        Get market analysis from Ask Nexus.
        
        Args:
            query: Analysis query
            symbols: List of symbols to analyze
            timeframe: Analysis timeframe
            include_charts: Include chart data
            
        Returns:
            Market analysis with credits usage
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not query or not query.strip():
            raise ValidationError("Query cannot be empty")
        
        data = {
            "query": query.strip(),
            "timeframe": timeframe,
            "include_charts": include_charts,
        }
        
        if symbols:
            data["symbols"] = symbols
        
        try:
            response = self.api.post("ask-nexus/analyze", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get market analysis: {str(e)}")
            raise
    
    def get_coin_analysis(
        self,
        symbol: str,
        analysis_type: str = "comprehensive",
        include_forecast: bool = False,
    ) -> Dict[str, Any]:
        """
        Get comprehensive coin analysis.
        
        Args:
            symbol: Cryptocurrency symbol
            analysis_type: Type of analysis
            include_forecast: Include price forecast
            
        Returns:
            Coin analysis with credits usage
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")
        
        valid_types = ["quick", "comprehensive", "technical", "fundamental"]
        if analysis_type not in valid_types:
            raise ValidationError(f"Analysis type must be one of: {valid_types}")
        
        data = {
            "symbol": symbol.upper(),
            "analysis_type": analysis_type,
            "include_forecast": include_forecast,
        }
        
        try:
            response = self.api.post("ask-nexus/coin-analysis", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get coin analysis for {symbol}: {str(e)}")
            raise
    
    def summarize_news(
        self,
        news_ids: List[str],
        summary_type: str = "brief",
        max_length: int = 500,
    ) -> Dict[str, Any]:
        """
        Summarize news articles.
        
        Args:
            news_ids: List of news article IDs
            summary_type: Type of summary
            max_length: Maximum summary length
            
        Returns:
            News summary with credits usage
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not news_ids:
            raise ValidationError("At least one news ID is required")
        
        valid_types = ["brief", "detailed", "bulletpoints"]
        if summary_type not in valid_types:
            raise ValidationError(f"Summary type must be one of: {valid_types}")
        
        if not 100 <= max_length <= 2000:
            raise ValidationError("Max length must be between 100 and 2000")
        
        data = {
            "news_ids": news_ids,
            "summary_type": summary_type,
            "max_length": max_length,
        }
        
        try:
            response = self.api.post("ask-nexus/summarize-news", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to summarize news: {str(e)}")
            raise
    
    def get_credits_estimate(
        self,
        operation: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get credits estimate for an operation.
        
        Args:
            operation: Operation type
            parameters: Operation parameters
            
        Returns:
            Credits estimate
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not operation:
            raise ValidationError("Operation is required")
        
        data = {
            "operation": operation,
            "parameters": parameters,
        }
        
        try:
            response = self.api.post("ask-nexus/credits-estimate", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get credits estimate: {str(e)}")
            raise