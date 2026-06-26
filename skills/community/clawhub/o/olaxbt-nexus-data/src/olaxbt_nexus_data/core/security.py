"""
Security configuration and utilities for the Nexus API client.
"""

import os
import time
import hashlib
import hmac
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from cryptography.fernet import Fernet
import base64

from .exceptions import ValidationError


@dataclass
class SecurityConfig:
    """Security configuration for the Nexus client."""
    
    # JWT settings
    encrypt_jwt: bool = True
    jwt_ttl: int = 3600  # 1 hour in seconds
    
    # Rate limiting
    rate_limit: int = 1000  # requests per hour
    rate_limit_window: int = 3600  # 1 hour in seconds
    
    # Request settings
    timeout: int = 30  # seconds
    max_retries: int = 3
    
    # Encryption
    encryption_key: Optional[str] = None
    
    def __post_init__(self):
        """Initialize encryption key if not provided."""
        if self.encrypt_jwt and not self.encryption_key:
            # Generate a secure encryption key
            key = os.urandom(32)
            self.encryption_key = base64.urlsafe_b64encode(key).decode()
    
    def validate(self) -> None:
        """Validate security configuration."""
        if self.rate_limit <= 0:
            raise ValidationError("Rate limit must be positive")
        
        if self.timeout <= 0:
            raise ValidationError("Timeout must be positive")
        
        if self.max_retries < 0:
            raise ValidationError("Max retries cannot be negative")
        
        if self.jwt_ttl <= 0:
            raise ValidationError("JWT TTL must be positive")


class TokenEncryptor:
    """Encrypt and decrypt JWT tokens."""
    
    def __init__(self, encryption_key: str):
        """
        Initialize encryptor with encryption key.
        
        Args:
            encryption_key: Base64-encoded encryption key
            
        Raises:
            ValidationError: If encryption key is invalid
        """
        try:
            self.fernet = Fernet(encryption_key.encode())
        except Exception as e:
            raise ValidationError(f"Invalid encryption key: {str(e)}")
    
    def encrypt(self, token: str) -> str:
        """
        Encrypt a JWT token.
        
        Args:
            token: Plain JWT token
            
        Returns:
            Encrypted token
        """
        return self.fernet.encrypt(token.encode()).decode()
    
    def decrypt(self, encrypted_token: str) -> str:
        """
        Decrypt a JWT token.
        
        Args:
            encrypted_token: Encrypted JWT token
            
        Returns:
            Decrypted token
            
        Raises:
            TokenError: If decryption fails
        """
        try:
            return self.fernet.decrypt(encrypted_token.encode()).decode()
        except Exception as e:
            from .exceptions import TokenError
            raise TokenError(f"Failed to decrypt token: {str(e)}")


class RateLimiter:
    """Rate limiting implementation."""
    
    def __init__(self, limit: int, window: int):
        """
        Initialize rate limiter.
        
        Args:
            limit: Maximum requests per window
            window: Time window in seconds
        """
        self.limit = limit
        self.window = window
        self.requests: Dict[str, list] = {}  # key -> [timestamps]
    
    def check(self, key: str) -> bool:
        """
        Check if request is allowed.
        
        Args:
            key: Rate limit key (e.g., wallet address)
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        
        # Clean old requests
        if key in self.requests:
            self.requests[key] = [
                ts for ts in self.requests[key]
                if now - ts < self.window
            ]
        
        # Check limit
        if key not in self.requests:
            self.requests[key] = []
        
        if len(self.requests[key]) >= self.limit:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True
    
    def get_remaining(self, key: str) -> int:
        """
        Get remaining requests for a key.
        
        Args:
            key: Rate limit key
            
        Returns:
            Number of remaining requests
        """
        now = time.time()
        
        if key not in self.requests:
            return self.limit
        
        # Count requests within window
        valid_requests = [
            ts for ts in self.requests[key]
            if now - ts < self.window
        ]
        
        return max(0, self.limit - len(valid_requests))
    
    def get_reset_time(self, key: str) -> Optional[float]:
        """
        Get reset time for a key.
        
        Args:
            key: Rate limit key
            
        Returns:
            Unix timestamp when limit resets, or None if no requests
        """
        if key not in self.requests or not self.requests[key]:
            return None
        
        now = time.time()
        oldest_request = min(self.requests[key])
        return oldest_request + self.window


def validate_wallet_address(address: str) -> bool:
    """
    Validate Ethereum wallet address.
    
    Args:
        address: Wallet address to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    
    # Basic Ethereum address validation
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))


def validate_private_key(private_key: str) -> bool:
    """
    Validate Ethereum private key.
    
    Args:
        private_key: Private key to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    
    # Private key should be 64 hex characters (32 bytes) with 0x prefix
    pattern = r'^0x[a-fA-F0-9]{64}$'
    return bool(re.match(pattern, private_key))


def sanitize_error_message(message: str) -> str:
    """
    Sanitize error messages to prevent information leakage.
    
    Args:
        message: Original error message
        
    Returns:
        Sanitized error message
    """
    # Remove potential sensitive information
    sensitive_patterns = [
        r'0x[a-fA-F0-9]{40}',  # Wallet addresses
        r'0x[a-fA-F0-9]{64}',  # Private keys
        r'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',  # JWT tokens
        r'password', r'secret', r'key', r'token',  # Sensitive keywords
    ]
    
    sanitized = message
    for pattern in sensitive_patterns:
        import re
        sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)
    
    return sanitized


def generate_request_id() -> str:
    """
    Generate a unique request ID.
    
    Returns:
        Unique request ID string
    """
    import uuid
    return str(uuid.uuid4())