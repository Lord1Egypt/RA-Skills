#!/usr/bin/env python3
"""
Sensitive Information Handler

Handles sensitive information (tokens, credentials) securely with 
automatic redaction and safe error messaging.
"""

import re
from typing import List, Tuple


class SensitiveInfoHandler:
    """
    Handles sensitive information (tokens, credentials) securely.
    
    Features:
    - Redacts sensitive data from strings
    - Masks tokens in logs
    - Safe error messages
    """
    
    # Patterns to detect sensitive information
    SENSITIVE_PATTERNS: List[Tuple[str, str]] = [
        (r'(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}', '<GITHUB_TOKEN>'),
        (r'xox[baprs]-[A-Za-z0-9]{10,}', '<SLACK_TOKEN>'),
        (r'AIza[A-Za-z0-9_-]{35}', '<GOOGLE_API_KEY>'),
        (r'SK[A-Za-z0-9_-]{20,}', '<STRIPE_KEY>'),
        (r'Bearer\s+[A-Za-z0-9._-]+', r'Bearer <TOKEN>'),
        (r'password["\']?\s*[:=]\s*["\']?[^\s"\']+', 'password=<REDACTED>'),
    ]
    
    @classmethod
    def redact(cls, text: str) -> str:
        """
        Redact sensitive information from text.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Text with sensitive information redacted
        """
        if not text:
            return text
        
        result = text
        for pattern, replacement in cls.SENSITIVE_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    @classmethod
    def redact_url(cls, url: str) -> str:
        """
        Remove credentials from URL.
        
        Args:
            url: URL potentially containing credentials
            
        Returns:
            URL with credentials removed
        """
        if not url:
            return url
        
        # Remove user:pass@ from URLs
        result = re.sub(r'://[^@]+@', '://', url)
        return result
    
    @classmethod
    def safe_error_message(cls, error: Exception, include_details: bool = False) -> str:
        """
        Create a safe error message that doesn't leak sensitive info.
        
        Args:
            error: The exception
            include_details: Whether to include error details (for debugging)
            
        Returns:
            Safe error message string
        """
        error_str = str(error)
        redacted = cls.redact(error_str)
        
        if include_details:
            return f"Error: {redacted}"
        else:
            # Generic message for production
            return "Operation failed. Please check your configuration and try again."


class SecureLogger:
    """
    Logger that automatically redacts sensitive information.
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def _safe_print(self, *args, **kwargs):
        """Print with sensitive data redacted."""
        safe_args = tuple(
            SensitiveInfoHandler.redact(str(arg)) if isinstance(arg, str) else arg
            for arg in args
        )
        print(*safe_args, **kwargs)
    
    def info(self, *args, **kwargs):
        """Log info message."""
        self._safe_print(*args, **kwargs)
    
    def warning(self, *args, **kwargs):
        """Log warning message."""
        self._safe_print(f"⚠️  ", *args, **kwargs)
    
    def error(self, *args, **kwargs):
        """Log error message."""
        self._safe_print(f"❌ ", *args, **kwargs)
    
    def debug(self, *args, **kwargs):
        """Log debug message (only if verbose mode)."""
        if self.verbose:
            self._safe_print(f"🔍 ", *args, **kwargs)
