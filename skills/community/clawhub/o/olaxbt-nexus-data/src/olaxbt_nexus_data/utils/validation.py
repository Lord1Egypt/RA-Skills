"""
Validation utilities for OlaXBT Nexus Data API client.
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..core.exceptions import ValidationError


def validate_symbol(symbol: str) -> str:
    """
    Validate cryptocurrency symbol.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., "BTC")
        
    Returns:
        Uppercase validated symbol
        
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError(f"Symbol must be a non-empty string: {symbol}")
    
    # Basic symbol validation (2-10 alphanumeric characters)
    if not re.match(r'^[A-Z0-9]{2,10}$', symbol.upper()):
        raise ValidationError(f"Invalid symbol format: {symbol}")
    
    return symbol.upper()


def validate_timeframe(timeframe: str, allowed: Optional[List[str]] = None) -> str:
    """
    Validate timeframe parameter.
    
    Args:
        timeframe: Timeframe string (e.g., "1h", "24h", "7d")
        allowed: List of allowed timeframes
        
    Returns:
        Validated timeframe
        
    Raises:
        ValidationError: If timeframe is invalid
    """
    if not timeframe or not isinstance(timeframe, str):
        raise ValidationError(f"Timeframe must be a non-empty string: {timeframe}")
    
    # Common timeframe patterns
    pattern = r'^(\d+)([hmd])$'
    match = re.match(pattern, timeframe.lower())
    
    if not match:
        raise ValidationError(f"Invalid timeframe format: {timeframe}")
    
    value, unit = match.groups()
    
    if allowed and timeframe not in allowed:
        raise ValidationError(
            f"Timeframe {timeframe} not allowed. Allowed: {allowed}"
        )
    
    return timeframe


def validate_limit(limit: int, min_val: int = 1, max_val: int = 100) -> int:
    """
    Validate limit parameter.
    
    Args:
        limit: Limit value
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Validated limit
        
    Raises:
        ValidationError: If limit is invalid
    """
    if not isinstance(limit, int):
        raise ValidationError(f"Limit must be an integer: {limit}")
    
    if not min_val <= limit <= max_val:
        raise ValidationError(f"Limit must be between {min_val} and {max_val}: {limit}")
    
    return limit


def validate_offset(offset: int) -> int:
    """
    Validate offset parameter.
    
    Args:
        offset: Offset value
        
    Returns:
        Validated offset
        
    Raises:
        ValidationError: If offset is invalid
    """
    if not isinstance(offset, int):
        raise ValidationError(f"Offset must be an integer: {offset}")
    
    if offset < 0:
        raise ValidationError(f"Offset cannot be negative: {offset}")
    
    return offset


def validate_date(date_str: str, format: str = "%Y-%m-%d") -> str:
    """
    Validate date string.
    
    Args:
        date_str: Date string
        format: Expected date format
        
    Returns:
        Validated date string
        
    Raises:
        ValidationError: If date is invalid
    """
    try:
        datetime.strptime(date_str, format)
        return date_str
    except ValueError:
        raise ValidationError(f"Invalid date format. Expected {format}: {date_str}")


def validate_parameters(params: Dict[str, Any], required: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Validate multiple parameters at once.
    
    Args:
        params: Parameters dictionary
        required: List of required parameter names
        
    Returns:
        Validated parameters
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    # Check required parameters
    if required:
        missing = [p for p in required if p not in params]
        if missing:
            raise ValidationError(f"Missing required parameters: {missing}")
    
    # Validate each parameter based on type
    validated = {}
    
    for key, value in params.items():
        if value is None:
            continue
        
        # Basic type validation
        if key.endswith("_limit") or key == "limit":
            if isinstance(value, int):
                validated[key] = validate_limit(value)
            else:
                raise ValidationError(f"{key} must be an integer: {value}")
        
        elif key.endswith("_offset") or key == "offset":
            if isinstance(value, int):
                validated[key] = validate_offset(value)
            else:
                raise ValidationError(f"{key} must be an integer: {value}")
        
        elif key == "symbol" or key.endswith("_symbol"):
            if isinstance(value, str):
                validated[key] = validate_symbol(value)
            else:
                raise ValidationError(f"{key} must be a string: {value}")
        
        elif key == "timeframe" or key.endswith("_timeframe"):
            if isinstance(value, str):
                validated[key] = validate_timeframe(value)
            else:
                raise ValidationError(f"{key} must be a string: {value}")
        
        else:
            validated[key] = value
    
    return validated


def validate_wallet_credentials(wallet_address: str, private_key: str) -> None:
    """
    Validate wallet credentials.
    
    Args:
        wallet_address: Ethereum wallet address
        private_key: Ethereum private key
        
    Raises:
        ValidationError: If credentials are invalid
    """
    # Wallet address validation (basic format)
    if not re.match(r'^0x[a-fA-F0-9]{40}$', wallet_address):
        raise ValidationError(f"Invalid wallet address format: {wallet_address[:20]}...")
    
    # Private key validation (basic format)
    if not re.match(r'^0x[a-fA-F0-9]{64}$', private_key):
        raise ValidationError("Invalid private key format. Should be 0x + 64 hex characters")
    
    # Additional checks
    if wallet_address.lower() == private_key.lower():
        raise ValidationError("Wallet address and private key cannot be the same")
    
    if "0x0" * 20 in wallet_address.lower():
        raise ValidationError("Wallet address appears to be zero address")


def sanitize_input(input_str: str, max_length: int = 1000) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        input_str: Input string
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
        
    Raises:
        ValidationError: If input is too long or contains dangerous characters
    """
    if not isinstance(input_str, str):
        raise ValidationError(f"Input must be a string: {type(input_str)}")
    
    # Check length
    if len(input_str) > max_length:
        raise ValidationError(f"Input too long (max {max_length} chars): {len(input_str)}")
    
    # Remove potentially dangerous characters
    dangerous_patterns = [
        r'<script.*?>.*?</script>',  # Script tags
        r'on\w+\s*=',  # Event handlers
        r'javascript:',  # JavaScript protocol
        r'data:',  # Data protocol
        r'vbscript:',  # VBScript protocol
    ]
    
    sanitized = input_str
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    # Remove excessive whitespace
    sanitized = ' '.join(sanitized.split())
    
    return sanitized.strip()