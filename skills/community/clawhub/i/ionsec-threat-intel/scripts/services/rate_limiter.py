#!/usr/bin/env python3
"""
Rate limiting and caching system for threat intelligence services.
Handles rate limit tracking, automatic retries, and response caching.
"""

import json
import time
from pathlib import Path
from typing import Dict, Optional, Tuple
from functools import wraps


class RateLimiter:
    """Rate limit tracker and manager for TI services."""
    
    # Default rate limits per service (requests per minute)
    DEFAULT_LIMITS = {
        "virustotal": 4,      # Free tier: 4/min
        "greynoise": 1,     # Free tier: 1/min
        "shodan": 1,        # Free tier: 1/min (100/month)
        "otx": 60,          # OTX: generous limits
        "abuseipdb": 5,     # Free tier: 5/min
        "urlscan": 1,       # Free tier: 1/min
        "spur": 60,         # Paid: 60/min
        "validin": 30,      # Free tier: 30/min
        "pulsedive": 30,    # Free tier: 30/min
        "malwarebazaar": 10,
        "urlhaus": 10,
        "dns": 100,         # DNS services are generous
    }
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path(__file__).parent.parent / ".cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        # Rate limit state file
        self.state_file = self.cache_dir / "rate_limits.json"
        self.state = self._load_state()
        
        # Response cache
        self.response_cache = {}
        self.cache_ttl = {
            "virustotal": 3600,      # 1 hour
            "greynoise": 1800,       # 30 min
            "shodan": 86400,         # 24 hours (infrastructure doesn't change often)
            "otx": 3600,
            "abuseipdb": 1800,
            "urlscan": 86400,        # Scan results don't change
            "spur": 3600,
            "validin": 3600,
            "pulsedive": 1800,
            "malwarebazaar": 86400,
            "urlhaus": 3600,
        }
    
    def _load_state(self) -> Dict:
        """Load rate limit state from disk."""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_state(self):
        """Save rate limit state to disk."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def get_wait_time(self, service: str) -> float:
        """Get seconds to wait before next request."""
        service = service.lower()
        now = time.time()
        
        if service not in self.state:
            return 0
        
        last_request = self.state[service].get("last_request", 0)
        limit = self.DEFAULT_LIMITS.get(service, 60)
        min_interval = 60.0 / limit
        
        elapsed = now - last_request
        if elapsed < min_interval:
            return min_interval - elapsed
        
        return 0
    
    def record_request(self, service: str):
        """Record that a request was made."""
        service = service.lower()
        now = time.time()
        
        if service not in self.state:
            self.state[service] = {}
        
        self.state[service]["last_request"] = now
        self.state[service]["request_count"] = self.state[service].get("request_count", 0) + 1
        self._save_state()
    
    def record_rate_limit_hit(self, service: str, retry_after: Optional[int] = None):
        """Record that we hit a rate limit."""
        service = service.lower()
        now = time.time()
        
        if service not in self.state:
            self.state[service] = {}
        
        self.state[service]["rate_limited_until"] = now + (retry_after or 60)
        self.state[service]["rate_limit_hits"] = self.state[service].get("rate_limit_hits", 0) + 1
        self._save_state()
    
    def is_rate_limited(self, service: str) -> bool:
        """Check if service is currently rate limited."""
        service = service.lower()
        now = time.time()
        
        if service in self.state:
            limited_until = self.state[service].get("rate_limited_until", 0)
            if limited_until > now:
                return True
        
        return False
    
    def get_cache_key(self, service: str, observable: str, obs_type: str) -> str:
        """Generate cache key for a query."""
        return f"{service}:{obs_type}:{observable.lower()}"
    
    def get_cached_response(self, service: str, observable: str, obs_type: str) -> Optional[Dict]:
        """Get cached response if available and not expired."""
        cache_key = self.get_cache_key(service, observable, obs_type)
        cache_file = self.cache_dir / f"{cache_key.replace('/', '_')}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file) as f:
                cached = json.load(f)
            
            # Check if cache is still valid
            ttl = self.cache_ttl.get(service, 1800)
            if time.time() - cached.get("timestamp", 0) < ttl:
                return cached.get("data")
        except:
            pass
        
        return None
    
    def cache_response(self, service: str, observable: str, obs_type: str, data: Dict):
        """Cache a response."""
        cache_key = self.get_cache_key(service, observable, obs_type)
        cache_file = self.cache_dir / f"{cache_key.replace('/', '_')}.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    "timestamp": time.time(),
                    "data": data
                }, f)
        except:
            pass
    
    def get_status(self) -> Dict:
        """Get current rate limit status for all services."""
        now = time.time()
        status = {}
        
        for service in self.DEFAULT_LIMITS:
            svc_state = self.state.get(service, {})
            limited_until = svc_state.get("rate_limited_until", 0)
            
            status[service] = {
                "limit": self.DEFAULT_LIMITS[service],
                "requests": svc_state.get("request_count", 0),
                "rate_limited": limited_until > now,
                "retry_after": max(0, limited_until - now) if limited_until > now else 0
            }
        
        return status


class RateLimitedClient:
    """HTTP client wrapper with rate limiting support."""
    
    def __init__(self, service_name: str, rate_limiter: Optional[RateLimiter] = None):
        self.service_name = service_name.lower()
        self.rate_limiter = rate_limiter or RateLimiter()
    
    def make_request(self, url: str, headers: Optional[Dict] = None, 
                     max_retries: int = 3, backoff_factor: float = 2.0) -> Tuple[Dict, bool]:
        """
        Make HTTP request with automatic rate limit handling.
        
        Returns: (response_data, from_cache)
        """
        import urllib.request
        import urllib.error
        
        # Check cache first
        # Extract observable from URL for caching
        cache_key = url.split('/')[-1] if '/' in url else url
        cached = self.rate_limiter.get_cached_response(self.service_name, cache_key, "auto")
        if cached:
            return cached, True
        
        # Check if rate limited
        if self.rate_limiter.is_rate_limited(self.service_name):
            wait = self.rate_limiter.get_wait_time(self.service_name)
            if wait > 0:
                time.sleep(min(wait, 5))  # Wait max 5 seconds
        
        # Wait for rate limit if needed
        wait_time = self.rate_limiter.get_wait_time(self.service_name)
        if wait_time > 0:
            time.sleep(wait_time)
        
        # Make request with retries
        for attempt in range(max_retries):
            try:
                self.rate_limiter.record_request(self.service_name)
                
                req = urllib.request.Request(url, headers=headers or {})
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    # Cache successful response
                    self.rate_limiter.cache_response(self.service_name, cache_key, "auto", data)
                    
                    return data, False
                    
            except urllib.error.HTTPError as e:
                if e.code == 429:  # Too Many Requests
                    retry_after = None
                    try:
                        retry_after = int(e.headers.get('Retry-After', 60))
                    except:
                        retry_after = 60
                    
                    self.rate_limiter.record_rate_limit_hit(self.service_name, retry_after)
                    
                    if attempt < max_retries - 1:
                        sleep_time = min(retry_after, backoff_factor ** attempt)
                        time.sleep(sleep_time)
                        continue
                    else:
                        raise Exception(f"Rate limited. Retry after {retry_after}s")
                
                elif e.code in (502, 503, 504):  # Server errors, retry
                    if attempt < max_retries - 1:
                        time.sleep(backoff_factor ** attempt)
                        continue
                    raise
                
                else:
                    raise
            
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(backoff_factor ** attempt)
                    continue
                raise
        
        raise Exception("Max retries exceeded")


def rate_limited_query(service_name: str):
    """Decorator for adding rate limiting to service query methods."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get or create rate limiter
            if not hasattr(self, '_rate_limiter'):
                self._rate_limiter = RateLimiter()
            
            client = RateLimitedClient(service_name, self._rate_limiter)
            
            # Store client reference for use in the method
            self._http_client = client
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def with_retry(max_retries: int = 3, backoff_factor: float = 2.0):
    """Decorator for adding retry logic to methods."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(backoff_factor ** attempt)
                        continue
                    raise
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator
