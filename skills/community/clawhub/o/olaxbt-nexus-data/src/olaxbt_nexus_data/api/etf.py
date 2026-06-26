"""
ETF API client for OlaXBT Nexus Data API.
Provides ETF inflow/outflow tracking and analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class ETFClient:
    """Client for ETF API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_flows(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        flow_type: str = "all",
    ) -> List[Dict[str, Any]]:
        """
        Get ETF flows data.
        
        Args:
            timeframe: Timeframe for flow analysis
            limit: Maximum number of flows to return
            flow_type: Type of flows (inflow, outflow, all)
            
        Returns:
            ETF flows data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        valid_types = ["all", "inflow", "outflow", "net"]
        if flow_type not in valid_types:
            raise ValidationError(f"Flow type must be one of: {valid_types}")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
            "type": flow_type,
        }
        
        try:
            response = self.api.get("etf/flows", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get ETF flows: {str(e)}")
            raise
    
    def get_etf_details(
        self,
        etf_symbol: str,
        include_holdings: bool = True,
        include_performance: bool = True,
    ) -> Dict[str, Any]:
        """
        Get details for specific ETF.
        
        Args:
            etf_symbol: ETF symbol (e.g., "GBTC", "IBIT")
            include_holdings: Include holdings data
            include_performance: Include performance data
            
        Returns:
            ETF details
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not etf_symbol:
            raise ValidationError("ETF symbol is required")
        
        params = {
            "include_holdings": str(include_holdings).lower(),
            "include_performance": str(include_performance).lower(),
        }
        
        try:
            response = self.api.get(f"etf/{etf_symbol}", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get ETF details for {etf_symbol}: {str(e)}")
            raise
    
    def get_holdings(
        self,
        etf_symbol: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get ETF holdings.
        
        Args:
            etf_symbol: ETF symbol
            limit: Maximum number of holdings
            
        Returns:
            ETF holdings
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not etf_symbol:
            raise ValidationError("ETF symbol is required")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "limit": limit,
        }
        
        try:
            response = self.api.get(f"etf/{etf_symbol}/holdings", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get ETF holdings for {etf_symbol}: {str(e)}")
            raise
    
    def get_performance(
        self,
        etf_symbol: str,
        timeframe: str = "7d",
    ) -> Dict[str, Any]:
        """
        Get ETF performance.
        
        Args:
            etf_symbol: ETF symbol
            timeframe: Performance timeframe
            
        Returns:
            ETF performance data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not etf_symbol:
            raise ValidationError("ETF symbol is required")
        
        valid_timeframes = ["1h", "4h", "24h", "7d", "30d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        params = {
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get(f"etf/{etf_symbol}/performance", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get ETF performance for {etf_symbol}: {str(e)}")
            raise
    
    def get_etf_list(
        self,
        limit: int = 50,
        sort_by: str = "aum",
    ) -> List[Dict[str, Any]]:
        """
        Get list of available ETFs.
        
        Args:
            limit: Maximum number of ETFs
            sort_by: Sort criteria
            
        Returns:
            List of ETFs
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not 1 <= limit <= 200:
            raise ValidationError("Limit must be between 1 and 200")
        
        valid_sorts = ["aum", "inflow", "outflow", "net_flow", "name"]
        if sort_by not in valid_sorts:
            raise ValidationError(f"Sort by must be one of: {valid_sorts}")
        
        params = {
            "limit": limit,
            "sort_by": sort_by,
        }
        
        try:
            response = self.api.get("etf/list", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get ETF list: {str(e)}")
            raise