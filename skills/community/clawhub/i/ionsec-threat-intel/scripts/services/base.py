#!/usr/bin/env python3
"""
Base service class for threat intelligence APIs.
Provides rate limiting, caching, and retry logic.
"""

import json
import hashlib
import time
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from typing import Dict, Optional
from pathlib import Path


class BaseService(ABC):
    """Abstract base class for threat intelligence services."""
    
    # Service metadata
    NAME: str = "base"
    SUPPORTED_TYPES: list = []
    REQUIRES_API_KEY: bool = False
    
    # Rate limit: requests per minute (None = no limit)
    RATE_LIMIT: int = None
    
    # Cache TTL in seconds (0 = no cache)
    CACHE_TTL: int = 1800  # 30 minutes default
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.timeout = kwargs.get("timeout", 30)
        self._last_request_time = 0
        self._cache_dir = Path(__file__).parent.parent.parent / ".cache"
        self._cache_dir.mkdir(exist_ok=True)
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests."""
        if self.RATE_LIMIT is None or self.RATE_LIMIT <= 0:
            return
        
        min_interval = 60.0 / self.RATE_LIMIT
        elapsed = time.time() - self._last_request_time
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self._last_request_time = time.time()
    
    def _get_cache_key(self, observable: str, obs_type: str) -> str:
        """Generate cache key for a query."""
        return f"{self.NAME}:{obs_type}:{observable.lower()}"
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get filesystem path for cache key."""
        safe_key = cache_key.replace('/', '_').replace(':', '_')
        return self._cache_dir / f"{safe_key}.json"
    
    def _get_cached(self, observable: str, obs_type: str) -> Optional[Dict]:
        """Get cached response if available and not expired."""
        if self.CACHE_TTL == 0:
            return None
        
        cache_key = self._get_cache_key(observable, obs_type)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path) as f:
                cached = json.load(f)
            
            if time.time() - cached.get("timestamp", 0) < self.CACHE_TTL:
                return cached.get("data")
        except:
            pass
        
        return None
    
    def _cache_response(self, observable: str, obs_type: str, data: Dict):
        """Cache a response."""
        if self.CACHE_TTL == 0:
            return
        
        cache_key = self._get_cache_key(observable, obs_type)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump({
                    "timestamp": time.time(),
                    "data": data
                }, f)
        except:
            pass
    
    @abstractmethod
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query the service for the observable.
        
        Args:
            observable: The IOC to query (IP, domain, hash, URL)
            obs_type: Type of observable ('ip', 'domain', 'hash', 'url')
        
        Returns:
            Dict with service name, status, classification, summary, and raw data
        """
        pass
    
    def _make_request(
        self,
        url: str,
        headers: Optional[Dict] = None,
        method: str = "GET",
        data: Optional[bytes] = None,
        max_retries: int = 3
    ) -> Dict:
        """Make an HTTP request with rate limiting, caching, and retry logic.
        
        Args:
            url: Request URL
            headers: Optional headers dict
            method: HTTP method (GET, POST)
            data: Optional request body
            max_retries: Number of retry attempts
        
        Returns:
            Parsed JSON response
        
        Raises:
            Exception on HTTP errors or JSON parse errors
        """
        # Check cache for GET requests
        if method == "GET":
            cache_key = f"{self.NAME}:url:{url}"
            cached = self._get_cached(url, "url")
            if cached:
                return cached
        
        request_headers = headers or {}
        request_headers.setdefault("User-Agent", "OpenClaw-ThreatIntel/1.0")
        
        # Add API key if available
        if self.api_key:
            if "virustotal" in url.lower():
                request_headers["x-apikey"] = self.api_key
            elif "greynoise" in url.lower():
                request_headers["key"] = self.api_key
            elif "abuseipdb" in url.lower():
                request_headers["Key"] = self.api_key
            elif "urlscan" in url.lower():
                request_headers["API-Key"] = self.api_key
            else:
                request_headers.setdefault("Authorization", f"Bearer {self.api_key}")
                request_headers.setdefault("X-API-Key", self.api_key)
        
        # Enforce rate limit before request
        self._enforce_rate_limit()
        
        last_error = None
        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(
                    url,
                    headers=request_headers,
                    method=method,
                    data=data
                )
                
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    
                    # Cache successful GET responses
                    if method == "GET":
                        self._cache_response(url, "url", result)
                    
                    return result
                    
            except urllib.error.HTTPError as e:
                last_error = e
                
                # Handle rate limiting (429)
                if e.code == 429:
                    retry_after = e.headers.get('Retry-After')
                    if retry_after:
                        sleep_time = min(int(retry_after), 300)  # Max 5 min
                    else:
                        sleep_time = 2 ** attempt  # Exponential backoff
                    
                    if attempt < max_retries - 1:
                        time.sleep(sleep_time)
                        continue
                    else:
                        raise Exception(f"Rate limited. Retry after {retry_after or 'unknown'}s")
                
                # Server errors (502, 503, 504) - retry
                elif e.code in (502, 503, 504):
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise Exception(f"HTTP {e.code}: {e.read().decode('utf-8') if e.fp else 'Server error'}")
                
                # Other HTTP errors
                else:
                    error_body = e.read().decode("utf-8") if e.fp else ""
                    raise Exception(f"HTTP {e.code}: {error_body}")
            
            except urllib.error.URLError as e:
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception(f"Connection error: {e.reason}")
            
            except json.JSONDecodeError as e:
                raise Exception(f"Invalid JSON response: {e}")
        
        raise last_error if last_error else Exception("Max retries exceeded")
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify the result as malicious, suspicious, benign, or unknown.
        
        Override this method in subclasses to implement service-specific logic.
        
        Returns:
            Tuple of (classification: str, summary: str)
        """
        return ("unknown", "No classification available")
    
    def _success_response(self, data: Dict) -> Dict:
        """Build a successful response."""
        classification, summary = self._classify_result(data)
        return {
            "service": self.NAME,
            "status": "success",
            "classification": classification,
            "summary": summary,
            "data": data
        }
    
    def _error_response(self, error: str) -> Dict:
        """Build an error response."""
        return {
            "service": self.NAME,
            "status": "error",
            "error": error,
            "classification": "error",
            "summary": error
        }
    
    @staticmethod
    def calculate_hash(observable: str, algorithm: str = "md5") -> str:
        """Calculate hash for URL encoding."""
        if algorithm == "md5":
            return hashlib.md5(observable.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(observable.encode()).hexdigest()
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def encode_url(url: str) -> str:
        """Encode URL for API queries (base64 or similar)."""
        import base64
        return base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
