#!/usr/bin/env python3
"""
GreyNoise API client for IP reputation and classification.
"""

from typing import Dict, Optional
from .base import BaseService


class GreyNoise(BaseService):
    """GreyNoise API client for IP reputation.
    
    Classifies IPs as malicious, benign (business internet), or unknown.
    Tracks botnets, scanners, and compromised devices.
    """
    
    NAME = "greynoise"
    SUPPORTED_TYPES = ["ip"]
    REQUIRES_API_KEY = True
    RATE_LIMIT = 1  # Free tier: 1 request/minute
    CACHE_TTL = 1800  # 30 minutes cache
    
    BASE_URL = "https://api.greynoise.io/v3/noise"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        # GreyNoise community tier works without key for basic queries
        # but has severe rate limits
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query GreyNoise for an IP address."""
        if obs_type != "ip":
            return self._error_response(f"Unsupported type: {obs_type}")
        
        try:
            data = self._query_context(observable)
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str, use_key: bool = True) -> Dict:
        """Make request to GreyNoise API."""
        headers = {"Accept": "application/json"}
        
        # GreyNoise community API uses 'key' query param for free tier
        # Enterprise uses Authorization header
        if use_key and self.api_key:
            headers["key"] = self.api_key
        
        return super()._make_request(url, headers=headers)
    
    def _query_context(self, ip: str) -> Dict:
        """Get full context for an IP."""
        url = f"{self.BASE_URL}/context/{ip}"
        return self._make_request(url)
    
    def _query_quick(self, ip: str) -> Dict:
        """Quick check if IP is in GreyNoise."""
        url = f"{self.BASE_URL}/quick/{ip}"
        return self._make_request(url)
    
    def _query_riot(self, ip: str) -> Dict:
        """Check if IP is a RIOT (known benign business service)."""
        url = f"https://api.greynoise.io/v3/riot/{ip}"
        return self._make_request(url)
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on GreyNoise classification."""
        # The response structure varies based on endpoint
        result = data.get("data", data)
        
        classification = result.get("classification", "unknown")
        
        if classification == "benign":
            name = result.get("name", "Unknown")
            return ("benign", f"Known benign: {name}")
        
        elif classification == "malicious":
            tags = result.get("tags", [])
            actor = result.get("actor", "Unknown")
            return ("malicious", f"Malicious actor: {actor}. Tags: {', '.join(tags[:5])}")
        
        elif classification == "unknown":
            return ("unknown", "Not in GreyNoise database")
        
        else:
            # RIOT response
            is_riot = result.get("riot", False)
            if is_riot:
                name = result.get("name", "Business service")
                return ("benign", f"RIOT (known benign): {name}")
            
            return ("unknown", "Classification unknown")