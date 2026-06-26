"""
GStable API Client
"""

import os
from typing import Any

import httpx


def _get_api_base_url() -> str:
    """Get API base URL from environment or use default"""
    return os.environ.get("GSTABLE_API_BASE_URL", "https://aipay.gstable.io/api/v1")


async def _api_request(endpoint: str, method: str = "GET", json_data: dict | None = None) -> dict[str, Any]:
    """
    Make an API request to GStable
    
    Args:
        endpoint: API endpoint
        method: HTTP method
        json_data: JSON body data
        
    Returns:
        dict: API response data
        
    Raises:
        Exception: If API returns error
    """
    url = f"{_get_api_base_url()}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url, headers={"Content-Type": "application/json"})
        else:
            response = await client.post(url, json=json_data, headers={"Content-Type": "application/json"})
        
        data = response.json()
        
        if data.get("code") != 0:
            raise Exception(f"API Error: {data.get('message')} (code: {data.get('code')})")
        
        return data


def _api_request_sync(endpoint: str, method: str = "GET", json_data: dict | None = None) -> dict[str, Any]:
    """
    Make a synchronous API request to GStable
    
    Args:
        endpoint: API endpoint
        method: HTTP method
        json_data: JSON body data
        
    Returns:
        dict: API response data
        
    Raises:
        Exception: If API returns error
    """
    url = f"{_get_api_base_url()}{endpoint}"
    
    with httpx.Client() as client:
        if method == "GET":
            response = client.get(url, headers={"Content-Type": "application/json"})
        else:
            response = client.post(url, json=json_data, headers={"Content-Type": "application/json"})
        
        data = response.json()
        
        if data.get("code") != 0:
            raise Exception(f"API Error: {data.get('message')} (code: {data.get('code')})")
        
        return data


async def get_payment_link(link_id: str) -> dict[str, Any]:
    """
    Get payment link details
    GET /payment/link/:linkId
    
    Args:
        link_id: Payment link ID
        
    Returns:
        dict: Payment link data
    """
    response = await _api_request(f"/payment/link/{link_id}")
    return response.get("data", response)


def get_payment_link_sync(link_id: str) -> dict[str, Any]:
    """
    Get payment link details (sync)
    GET /payment/link/:linkId
    
    Args:
        link_id: Payment link ID
        
    Returns:
        dict: Payment link data
    """
    response = _api_request_sync(f"/payment/link/{link_id}")
    return response.get("data", response)


async def create_payment_session(message: dict[str, Any], signature: str) -> dict[str, Any]:
    """
    Create a payment session
    POST /payment/session/create
    
    Args:
        message: EIP-712 message
        signature: Signature
        
    Returns:
        dict: Session data
    """
    response = await _api_request(
        "/payment/session/create",
        method="POST",
        json_data={"message": message, "signature": signature}
    )
    return response.get("data", response)


def create_payment_session_sync(message: dict[str, Any], signature: str) -> dict[str, Any]:
    """
    Create a payment session (sync)
    POST /payment/session/create
    
    Args:
        message: EIP-712 message
        signature: Signature
        
    Returns:
        dict: Session data
    """
    response = _api_request_sync(
        "/payment/session/create",
        method="POST",
        json_data={"message": message, "signature": signature}
    )
    return response.get("data", response)


async def get_payment_session(session_id: str) -> dict[str, Any]:
    """
    Get payment session details
    GET /session/:sessionId
    
    Args:
        session_id: Session ID
        
    Returns:
        dict: Session data
    """
    response = await _api_request(f"/session/{session_id}")
    return response.get("data", response)


def get_payment_session_sync(session_id: str) -> dict[str, Any]:
    """
    Get payment session details (sync)
    GET /session/:sessionId
    
    Args:
        session_id: Session ID
        
    Returns:
        dict: Session data
    """
    response = _api_request_sync(f"/session/{session_id}")
    return response.get("data", response)


async def prepare_payment(message: dict[str, Any], signature: str) -> dict[str, Any]:
    """
    Prepare payment and get calldata
    POST /payment/prepare
    
    Args:
        message: EIP-712 message
        signature: Signature
        
    Returns:
        dict: Prepare payment data with calldata
    """
    response = await _api_request(
        "/payment/prepare",
        method="POST",
        json_data={"message": message, "signature": signature}
    )
    return response.get("data", response)


def prepare_payment_sync(message: dict[str, Any], signature: str) -> dict[str, Any]:
    """
    Prepare payment and get calldata (sync)
    POST /payment/prepare
    
    Args:
        message: EIP-712 message
        signature: Signature
        
    Returns:
        dict: Prepare payment data with calldata
    """
    response = _api_request_sync(
        "/payment/prepare",
        method="POST",
        json_data={"message": message, "signature": signature}
    )
    return response.get("data", response)
