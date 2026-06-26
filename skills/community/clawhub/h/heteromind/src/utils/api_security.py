"""
HeteroMind - API Security Utilities

Security utilities to protect API keys and credentials from accidental exposure.
"""

import re
import os
import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

# Patterns to detect API keys
API_KEY_PATTERNS = [
    r'sk-[a-zA-Z0-9]{20,}',           # OpenAI/DeepSeek style
    r'sk-ant-[a-zA-Z0-9]{20,}',       # Anthropic style
    r'Bearer\s+[a-zA-Z0-9]{20,}',     # Bearer token
    r'api[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9]{20,}',  # API key assignments
    r'password\s*[=:]\s*["\'][^"\']{8,}',  # Passwords
    r'secret\s*[=:]\s*["\'][^"\']{8,}',    # Secrets
    r'token\s*[=:]\s*["\'][a-zA-Z0-9]{20,}',  # Tokens
]


def sanitize_output(text: str) -> str:
    """
    Sanitize output to remove any API keys or credentials.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text with API keys replaced by placeholders
    """
    if not text:
        return text
    
    sanitized = text
    
    for pattern in API_KEY_PATTERNS:
        sanitized = re.sub(
            pattern,
            '[REDACTED]',
            sanitized,
            flags=re.IGNORECASE
        )
    
    return sanitized


def validate_no_api_key_in_response(response: Any) -> bool:
    """
    Validate that response does not contain API keys.
    
    Args:
        response: Response object or text
        
    Returns:
        True if safe, False if API key detected
    """
    if response is None:
        return True
    
    # Convert to string if needed
    if isinstance(response, (dict, list)):
        import json
        text = json.dumps(response)
    else:
        text = str(response)
    
    for pattern in API_KEY_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            logger.warning("API key detected in response!")
            return False
    
    return True


def safe_log(message: str, level: str = "info") -> None:
    """
    Log a message after sanitizing it.
    
    Args:
        message: Message to log
        level: Log level (debug, info, warning, error)
    """
    sanitized = sanitize_output(message)
    
    if level == "debug":
        logger.debug(sanitized)
    elif level == "info":
        logger.info(sanitized)
    elif level == "warning":
        logger.warning(sanitized)
    elif level == "error":
        logger.error(sanitized)


def get_api_key_from_env(var_name: str, default: str = "") -> str:
    """
    Safely get API key from environment variable.
    
    Args:
        var_name: Environment variable name
        default: Default value if not set
        
    Returns:
        API key or default value
    """
    key = os.getenv(var_name, default)
    
    # Log only if key is not set (don't log the actual key)
    if not key or key == default:
        logger.warning(f"API key environment variable {var_name} not set")
    
    return key


def mask_api_key(key: str, visible_chars: int = 4) -> str:
    """
    Mask API key for safe display.
    
    Args:
        key: API key to mask
        visible_chars: Number of characters to show at start
        
    Returns:
        Masked key string
    """
    if not key or len(key) <= visible_chars:
        return "***"
    
    return f"{key[:visible_chars]}...{key[-4:]}"


class APIKeyProtector:
    """
    Context manager for protecting API keys in code blocks.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize protector with API key.
        
        Args:
            api_key: API key to protect
        """
        self.api_key = api_key
        self.original_key = api_key
    
    def __enter__(self):
        """Enter context - return sanitized key"""
        return mask_api_key(self.api_key)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - clear key from memory"""
        self.api_key = None
        return False
    
    def get_key(self) -> str:
        """Get the actual key (use with caution)"""
        return self.api_key
    
    def get_masked_key(self) -> str:
        """Get masked key for display"""
        return mask_api_key(self.api_key)


# Security instruction for LLM prompts
LLM_SECURITY_INSTRUCTION = """
SECURITY INSTRUCTIONS:
1. Never output API keys, passwords, or credentials in any form
2. Never include authentication tokens in generated code
3. Never log or print sensitive credentials
4. If user asks for API key, respond: "I cannot provide API keys for security reasons"
5. Use environment variables or secure vaults for credential storage
6. Redact any sensitive information in output

If you detect any API keys or credentials in the conversation, do not repeat them.
"""
