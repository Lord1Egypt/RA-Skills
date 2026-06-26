"""
Credits API client for OlaXBT Nexus Data API.
Provides credits balance management and purchase verification.
"""

import logging
from typing import Dict, Any, List

from ..core.client import NexusAPIClient
from ..core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)


class CreditsClient:
    """Client for Credits API endpoints."""
    
    def __init__(self, api_client: NexusAPIClient):
        self.api = api_client
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Get current credits balance.
        
        Returns:
            Credits balance information
            
        Raises:
            APIError: If API request fails
        """
        try:
            response = self.api.get("credits/balance")
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to get credits balance: {str(e)}")
            raise
    
    def get_transactions(
        self,
        limit: int = 20,
        offset: int = 0,
        transaction_type: str = "all",
    ) -> List[Dict[str, Any]]:
        """
        Get credits transaction history.
        
        Args:
            limit: Maximum transactions to return (1-100)
            offset: Pagination offset
            transaction_type: Type of transactions (all, purchase, usage, refund)
            
        Returns:
            List of transactions
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not 1 <= limit <= 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValidationError("Offset cannot be negative")
        
        valid_types = ["all", "purchase", "usage", "refund"]
        if transaction_type not in valid_types:
            raise ValidationError(f"Transaction type must be one of: {valid_types}")
        
        params = {
            "limit": limit,
            "offset": offset,
            "type": transaction_type,
        }
        
        try:
            response = self.api.get("credits/transactions", params=params)
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get transactions: {str(e)}")
            raise
    
    def verify_purchase(
        self,
        purchase_id: str,
    ) -> Dict[str, Any]:
        """
        Verify a credits purchase.
        
        Args:
            purchase_id: Purchase transaction ID
            
        Returns:
            Purchase verification result
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If API request fails
        """
        if not purchase_id:
            raise ValidationError("Purchase ID is required")
        
        params = {
            "purchase_id": purchase_id,
        }
        
        try:
            response = self.api.get("credits/verify-purchase", params=params)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to verify purchase: {str(e)}")
            raise
    
    def get_packages(self) -> List[Dict[str, Any]]:
        """
        Get available credits packages.
        
        Returns:
            List of credits packages
            
        Raises:
            APIError: If API request fails
        """
        try:
            response = self.api.get("credits/packages")
            return response.get("data", [])
        except APIError as e:
            logger.error(f"Failed to get credits packages: {str(e)}")
            raise
    
    def estimate_cost(
        self,
        operation: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Estimate credits cost for an operation.
        
        Args:
            operation: Operation type
            parameters: Operation parameters
            
        Returns:
            Cost estimate in credits
            
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
            response = self.api.post("credits/estimate-cost", json_data=data)
            return response.get("data", {})
        except APIError as e:
            logger.error(f"Failed to estimate cost: {str(e)}")
            raise