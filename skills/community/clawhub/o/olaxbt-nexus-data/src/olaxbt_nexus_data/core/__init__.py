"""
Core modules for OlaXBT Nexus Data API client.

This package contains the core functionality for authentication,
API communication, security, and error handling.
"""

from .auth import NexusAuth
from .client import NexusAPIClient
from .security import SecurityConfig
from .exceptions import (
    NexusError,
    AuthenticationError,
    APIError,
    RateLimitError,
    ValidationError,
)

__all__ = [
    "NexusAuth",
    "NexusAPIClient",
    "SecurityConfig",
    "NexusError",
    "AuthenticationError",
    "APIError",
    "RateLimitError",
    "ValidationError",
]