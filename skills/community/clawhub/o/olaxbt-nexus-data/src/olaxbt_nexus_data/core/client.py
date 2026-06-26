"""
Base API client for OlaXBT Nexus Data API.
Handles HTTP requests, retries, error handling, and rate limiting.
"""

import time
import json
import logging
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    APIError,
    RateLimitError,
    AuthenticationError,
    ValidationError,
)
from .security import RateLimiter, sanitize_error_message, generate_request_id
from .auth import NexusAuth

logger = logging.getLogger(__name__)


@dataclass
class RequestMetrics:
    """Track request metrics for monitoring."""
    
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0
    last_request_time: Optional[float] = None


class NexusAPIClient:
    """Base client for all Nexus API requests."""
    
    def __init__(
        self,
        auth_client: NexusAuth,
        data_url: str,
        security_config,
    ):
        """
        Initialize API client.
        
        Args:
            auth_client: Authenticated NexusAuth instance
            data_url: Data API base URL
            security_config: Security configuration
        """
        self.auth = auth_client
        self.base_url = data_url.rstrip("/")
        self.security_config = security_config
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            limit=security_config.rate_limit,
            window=security_config.rate_limit_window,
        )
        
        # Initialize metrics
        self.metrics = RequestMetrics()
        
        # Configure HTTP session with retries
        self.session = self._create_session()
        
        logger.info(f"API client initialized for {self.base_url}")
    
    def _create_session(self) -> requests.Session:
        """Create configured HTTP session."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.security_config.max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default timeout
        session.request = lambda method, url, **kwargs: requests.Session.request(
            self.session,
            method,
            url,
            timeout=self.security_config.timeout,
            **kwargs,
        )
        
        return session
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        require_auth: bool = True,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Form data
            json_data: JSON request body
            headers: Additional headers
            require_auth: Whether authentication is required
            
        Returns:
            API response as dictionary
            
        Raises:
            RateLimitError: If rate limit is exceeded
            AuthenticationError: If authentication fails
            APIError: If API request fails
        """
        # Build URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Prepare headers
        request_headers = {
            "Content-Type": "application/json",
            "User-Agent": f"OlaXBT-Nexus-Client/{self.auth.wallet_address[:10]}...",
            "X-Request-ID": generate_request_id(),
        }
        
        if require_auth:
            try:
                auth_headers = self.auth.get_auth_headers()
                request_headers.update(auth_headers)
            except AuthenticationError as e:
                logger.error(f"Authentication failed: {str(e)}")
                raise
        
        if headers:
            request_headers.update(headers)
        
        # Check rate limit
        rate_limit_key = self.auth.wallet_address
        if not self.rate_limiter.check(rate_limit_key):
            reset_time = self.rate_limiter.get_reset_time(rate_limit_key)
            remaining = self.rate_limiter.get_remaining(rate_limit_key)
            
            raise RateLimitError(
                message="Rate limit exceeded",
                reset_in=int(reset_time - time.time()) if reset_time else None,
                limit=self.security_config.rate_limit,
                remaining=remaining,
            )
        
        # Make request
        start_time = time.time()
        self.metrics.total_requests += 1
        
        try:
            logger.debug(f"Making {method} request to {url}")
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
            )
            
            # Update metrics
            response_time = time.time() - start_time
            self.metrics.total_response_time += response_time
            self.metrics.last_request_time = time.time()
            
            # Handle rate limit headers
            if "X-RateLimit-Limit" in response.headers:
                try:
                    limit = int(response.headers["X-RateLimit-Limit"])
                    remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
                    reset = int(response.headers.get("X-RateLimit-Reset", 0))
                    
                    # Update rate limiter with server info
                    logger.debug(f"Rate limit: {remaining}/{limit}, resets in {reset}s")
                except (ValueError, TypeError):
                    pass
            
            # Handle errors
            if response.status_code == 429:
                reset_in = int(response.headers.get("Retry-After", 60))
                raise RateLimitError(
                    message="Rate limit exceeded",
                    reset_in=reset_in,
                    limit=self.security_config.rate_limit,
                    remaining=self.rate_limiter.get_remaining(rate_limit_key),
                )
            
            if response.status_code == 401:
                # Clear token and retry once
                self.auth.clear_token()
                raise AuthenticationError("Authentication expired, token cleared")
            
            if response.status_code == 403:
                raise AuthenticationError("Access forbidden, check permissions")
            
            response.raise_for_status()
            
            # Parse response
            try:
                result = response.json()
            except json.JSONDecodeError:
                result = {"raw_response": response.text}
            
            # Check for API-level errors
            if isinstance(result, dict) and not result.get("success", True):
                error_msg = result.get("message", "Unknown API error")
                raise APIError(
                    message=error_msg,
                    status_code=response.status_code,
                    response_data=result,
                )
            
            self.metrics.successful_requests += 1
            logger.debug(f"Request successful in {response_time:.2f}s")
            
            return result
            
        except RateLimitError:
            self.metrics.failed_requests += 1
            raise
        
        except AuthenticationError:
            self.metrics.failed_requests += 1
            raise
        
        except requests.exceptions.RequestException as e:
            self.metrics.failed_requests += 1
            
            # Sanitize error message
            error_msg = sanitize_error_message(str(e))
            
            # Extract status code if available
            status_code = None
            if hasattr(e, "response") and e.response is not None:
                status_code = e.response.status_code
            
            logger.error(f"Request failed: {error_msg}")
            raise APIError(
                message=f"Request failed: {error_msg}",
                status_code=status_code,
            )
        
        except Exception as e:
            self.metrics.failed_requests += 1
            error_msg = sanitize_error_message(str(e))
            logger.error(f"Unexpected error: {error_msg}")
            raise APIError(f"Unexpected error: {error_msg}")
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        require_auth: bool = True,
    ) -> Dict[str, Any]:
        """
        Make GET request.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers
            require_auth: Whether authentication is required
            
        Returns:
            API response
        """
        return self._request(
            method="GET",
            endpoint=endpoint,
            params=params,
            headers=headers,
            require_auth=require_auth,
        )
    
    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        require_auth: bool = True,
    ) -> Dict[str, Any]:
        """
        Make POST request.
        
        Args:
            endpoint: API endpoint path
            json_data: JSON request body
            data: Form data
            headers: Additional headers
            require_auth: Whether authentication is required
            
        Returns:
            API response
        """
        return self._request(
            method="POST",
            endpoint=endpoint,
            json_data=json_data,
            data=data,
            headers=headers,
            require_auth=require_auth,
        )
    
    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        require_auth: bool = True,
    ) -> Dict[str, Any]:
        """
        Make PUT request.
        
        Args:
            endpoint: API endpoint path
            json_data: JSON request body
            headers: Additional headers
            require_auth: Whether authentication is required
            
        Returns:
            API response
        """
        return self._request(
            method="PUT",
            endpoint=endpoint,
            json_data=json_data,
            headers=headers,
            require_auth=require_auth,
        )
    
    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        require_auth: bool = True,
    ) -> Dict[str, Any]:
        """
        Make DELETE request.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers
            require_auth: Whether authentication is required
            
        Returns:
            API response
        """
        return self._request(
            method="DELETE",
            endpoint=endpoint,
            params=params,
            headers=headers,
            require_auth=require_auth,
        )
    
    def get_credits_balance(self) -> Dict[str, Any]:
        """
        Get current credits balance.
        
        Returns:
            Credits balance information
            
        Raises:
            APIError: If request fails
        """
        return self.get("credits/balance")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get request metrics.
        
        Returns:
            Dictionary with request metrics
        """
        avg_response_time = 0.0
        if self.metrics.total_requests > 0:
            avg_response_time = self.metrics.total_response_time / self.metrics.total_requests
        
        success_rate = 0.0
        if self.metrics.total_requests > 0:
            success_rate = (self.metrics.successful_requests / self.metrics.total_requests) * 100
        
        return {
            "total_requests": self.metrics.total_requests,
            "successful_requests": self.metrics.successful_requests,
            "failed_requests": self.metrics.failed_requests,
            "success_rate": f"{success_rate:.1f}%",
            "average_response_time": f"{avg_response_time:.3f}s",
            "total_response_time": f"{self.metrics.total_response_time:.3f}s",
            "last_request_time": self.metrics.last_request_time,
            "rate_limit_remaining": self.rate_limiter.get_remaining(self.auth.wallet_address),
            "rate_limit_total": self.security_config.rate_limit,
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health.
        
        Returns:
            Health check results
        """
        try:
            response = self.get("health", require_auth=False)
            return {
                "status": "healthy",
                "response": response,
                "timestamp": time.time(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time(),
            }