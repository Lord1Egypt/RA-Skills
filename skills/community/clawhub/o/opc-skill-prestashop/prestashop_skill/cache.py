import time
import threading
from typing import Any, Optional, Dict, Tuple

class SimpleMemoryCache:
    """
    Lightweight, thread-safe in-memory cache with TTL support.
    Used for storing categories, product details, and frequently queried product IDs.
    """
    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.Lock()
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Retrieve item from cache if not expired."""
        with self._lock:
            if key not in self._cache:
                return None
            
            val, expiry = self._cache[key]
            if time.time() > expiry:
                del self._cache[key]
                return None
            
            return val

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store item in cache with TTL (in seconds)."""
        ttl_val = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + ttl_val
        with self._lock:
            self._cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """Delete specific key from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Clear all cached items."""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """Removes expired entries and returns count of removed items."""
        now = time.time()
        removed = 0
        with self._lock:
            keys_to_remove = [k for k, (_, exp) in self._cache.items() if now > exp]
            for k in keys_to_remove:
                del self._cache[k]
                removed += 1
        return removed
