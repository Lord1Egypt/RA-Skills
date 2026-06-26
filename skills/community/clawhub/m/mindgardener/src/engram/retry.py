"""
Retry with exponential backoff for LLM API calls.

Handles 429 (rate limit), 500/502/503 (server errors), and timeouts.
"""

from __future__ import annotations

import time
import sys
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar('T')

# HTTP errors worth retrying
RETRYABLE_ERRORS = {429, 500, 502, 503, 504}


def with_retry(max_retries: int = 3, base_delay: float = 2.0,
               max_delay: float = 60.0, verbose: bool = False):
    """
    Decorator: retry a function with exponential backoff.
    
    Usage:
        @with_retry(max_retries=3)
        def call_api(prompt):
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    error_str = str(e)
                    
                    # Check if retryable
                    is_retryable = any(
                        str(code) in error_str 
                        for code in RETRYABLE_ERRORS
                    ) or "timeout" in error_str.lower()
                    
                    if not is_retryable or attempt == max_retries:
                        raise
                    
                    # Exponential backoff with jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    
                    if verbose:
                        print(f"  ⏳ Retry {attempt + 1}/{max_retries} "
                              f"after {delay:.1f}s ({error_str[:60]})",
                              file=sys.stderr)
                    
                    time.sleep(delay)
            
            raise last_error
        
        return wrapper
    return decorator


def retry_call(func: Callable[..., T], *args, 
               max_retries: int = 3, verbose: bool = False, 
               **kwargs) -> T:
    """
    Functional retry: call a function with retry logic.
    
    Usage:
        result = retry_call(provider.generate, prompt, max_retries=3)
    """
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            error_str = str(e)
            
            is_retryable = any(
                str(code) in error_str 
                for code in RETRYABLE_ERRORS
            ) or "timeout" in error_str.lower()
            
            if not is_retryable or attempt == max_retries:
                raise
            
            delay = min(2.0 * (2 ** attempt), 60.0)
            
            if verbose:
                print(f"  ⏳ Retry {attempt + 1}/{max_retries} "
                      f"after {delay:.1f}s ({error_str[:60]})",
                      file=sys.stderr)
            
            time.sleep(delay)
    
    raise last_error
