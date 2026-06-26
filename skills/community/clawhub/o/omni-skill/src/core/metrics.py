import time
import threading
import logging
from typing import Callable, Any, Dict
from .interfaces import OmniErrorCode

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.settings as settings

class CircuitBreaker:
    def __init__(self, failure_threshold: int = settings.CIRCUIT_BREAKER_FAILURE_THRESHOLD, recovery_timeout: float = settings.CIRCUIT_BREAKER_RECOVERY_TIMEOUT):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self._lock = threading.Lock()

    def allow_request(self) -> bool:
        with self._lock:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                    return True
                return False
            return True

    def record_success(self):
        with self._lock:
            self.failure_count = 0
            self.state = "CLOSED"

    def record_failure(self):
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logging.warning("Circuit breaker opened due to repeated failures.")

class RateLimiter:
    def __init__(self, max_requests: int = settings.RATE_LIMIT_MAX_REQUESTS, time_window: float = settings.RATE_LIMIT_TIME_WINDOW):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = threading.Lock()

    def allow_request(self) -> bool:
        with self._lock:
            current_time = time.time()
            # Clean up old requests
            self.requests = [req_time for req_time in self.requests if current_time - req_time <= self.time_window]
            
            if len(self.requests) < self.max_requests:
                self.requests.append(current_time)
                return True
            return False

def with_timeout(func: Callable, timeout: float, *args, **kwargs) -> Any:
    result_container = {}
    exception_container = {}

    def worker():
        try:
            result_container["result"] = func(*args, **kwargs)
        except Exception as e:
            exception_container["exception"] = e

    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutError(f"Execution timed out after {timeout} seconds")
    if "exception" in exception_container:
        raise exception_container["exception"]
    
    return result_container.get("result")
