"""
Custom exceptions for the OlaXBT Nexus Data API client.
"""

from typing import Optional, Dict, Any


class NexusError(Exception):
    """Base exception for all Nexus API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message


class AuthenticationError(NexusError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(f"Authentication failed: {message}", status_code)


class APIError(NexusError):
    """Raised when API requests fail."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        self.response_data = response_data or {}
        super().__init__(f"API error: {message}", status_code)


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429,
        reset_in: Optional[int] = None,
        limit: Optional[int] = None,
        remaining: Optional[int] = None,
    ):
        self.reset_in = reset_in
        self.limit = limit
        self.remaining = remaining
        super().__init__(message, status_code)
    
    def __str__(self) -> str:
        base = super().__str__()
        details = []
        if self.reset_in:
            details.append(f"Reset in: {self.reset_in} seconds")
        if self.limit:
            details.append(f"Limit: {self.limit}/hour")
        if self.remaining is not None:
            details.append(f"Remaining: {self.remaining}")
        
        if details:
            return f"{base} [{', '.join(details)}]"
        return base


class ValidationError(NexusError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        if field:
            super().__init__(f"Validation error for field '{field}': {message}")
        else:
            super().__init__(f"Validation error: {message}")


class ConfigurationError(NexusError):
    """Raised when client configuration is invalid."""
    
    def __init__(self, message: str):
        super().__init__(f"Configuration error: {message}")


class WalletError(NexusError):
    """Raised when wallet operations fail."""
    
    def __init__(self, message: str):
        super().__init__(f"Wallet error: {message}")


class TokenError(NexusError):
    """Raised when JWT token operations fail."""
    
    def __init__(self, message: str):
        super().__init__(f"Token error: {message}")