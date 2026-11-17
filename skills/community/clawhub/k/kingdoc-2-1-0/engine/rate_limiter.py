"""KingDoc Rate Limiter — exponential backoff with random jitter"""
import time
import random
from typing import Callable


def exponential_backoff(retry_count: int, max_retries: int = 5) -> float:
    """Calculate delay for exponential backoff
    
    Args:
        retry_count: Current retry attempt (0-indexed)
        max_retries: Maximum number of retries allowed
    
    Returns:
        Delay in seconds
    """
    if retry_count >= max_retries:
        return -1  # Signal to stop retrying
    
    delay = min(2 ** retry_count + random.uniform(0, 1), 300)
    return delay


def with_retry(func: Callable, max_retries: int = 5):
    """Decorator: retry function on failure with exponential backoff"""
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries:
                    raise
                delay = exponential_backoff(attempt, max_retries)
                if delay < 0:
                    raise
                time.sleep(delay)
    return wrapper
