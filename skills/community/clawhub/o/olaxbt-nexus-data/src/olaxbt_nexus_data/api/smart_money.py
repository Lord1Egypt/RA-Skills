"""
Smart Money API client for OlaXBT Nexus Data API.
Provides access to institutional money tracking and analysis.
"""

import logging
from typing import Optional, Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class SmartMoneyClient:
    """Client for Smart Money API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_flows(
        self,
        timeframe: str = "24h",
        limit: int = 20,
        min_volume: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get smart money flows.
        
        Args:
            timeframe: Timeframe for flow analysis
            limit: Maximum number of flows to return
            min_volume: Minimum volume filter
            
        Returns:
            List of smart money flows
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        if min_volume is not None:
            if min_volume < 0:
                raise ValidationError("Min volume cannot be negative")
            params["min_volume"] = min_volume
        
        try:
            response = self.api.get("smart-money/flows", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get smart money flows: {str(e)}")
            raise
    
    def get_positions(
        self,
        symbol: Optional[str] = None,
        wallet_type: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get smart money positions.
        
        Args:
            symbol: Filter by cryptocurrency symbol
            wallet_type: Filter by wallet type (institution, whale, etc.)
            limit: Maximum number of positions to return
            
        Returns:
            List of smart money positions
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        params = {
            "limit": limit,
        }
        
        if symbol:
            params["symbol"] = symbol.upper()
        
        if wallet_type:
            valid_types = ["institution", "whale", "exchange", "fund"]
            if wallet_type not in valid_types:
                raise ValidationError(f"Wallet type must be one of: {valid_types}")
            params["wallet_type"] = wallet_type
        
        try:
            response = self.api.get("smart-money/positions", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get smart money positions: {str(e)}")
            raise
    
    def get_wallet_analysis(
        self,
        wallet_address: str,
        include_transactions: bool = True,
        transaction_limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Get analysis for a specific smart money wallet.
        
        Args:
            wallet_address: Ethereum wallet address
            include_transactions: Include recent transactions
            transaction_limit: Maximum transactions to include
            
        Returns:
            Wallet analysis data
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not wallet_address:
            raise ValidationError("Wallet address is required")
        
        if not 1 <= transaction_limit <= 50:
            raise ValidationError("Transaction limit must be between 1 and 50")
        
        params = {
            "include_transactions": str(include_transactions).lower(),
            "transaction_limit": transaction_limit,
        }
        
        try:
            response = self.api.get(f"smart-money/wallet/{wallet_address}", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get wallet analysis: {str(e)}")
            raise
    
    def get_token_analysis(
        self,
        symbol: str,
        timeframe: str = "24h",
    ) -> Dict[str, Any]:
        """
        Get smart money analysis for a token.
        
        Args:
            symbol: Cryptocurrency symbol
            timeframe: Timeframe for analysis
            
        Returns:
            Token smart money analysis
            
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
            "symbol": symbol.upper(),
            "timeframe": timeframe,
        }
        
        try:
            response = self.api.get("smart-money/token-analysis", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get token analysis for {symbol}: {str(e)}")
            raise
    
    def get_divergence_signals(
        self,
        timeframe: str = "24h",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get smart money divergence signals.
        
        Args:
            timeframe: Timeframe for divergence analysis
            limit: Maximum number of signals
            
        Returns:
            List of divergence signals
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        valid_timeframes = ["1h", "4h", "24h", "7d"]
        if timeframe not in valid_timeframes:
            raise ValidationError(f"Timeframe must be one of: {valid_timeframes}")
        
        if not 1 <= limit <= 50:
            raise ValidationError("Limit must be between 1 and 50")
        
        params = {
            "timeframe": timeframe,
            "limit": limit,
        }
        
        try:
            response = self.api.get("smart-money/divergence", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get divergence signals: {str(e)}")
            raise