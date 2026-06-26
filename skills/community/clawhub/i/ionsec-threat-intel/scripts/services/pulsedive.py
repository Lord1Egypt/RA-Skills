#!/usr/bin/env python3
"""
Pulsedive API client (free tier).
"""

import json
from typing import Dict, Optional
from .base import BaseService


class Pulsedive(BaseService):
    """Pulsedive API client for IP, domain, and URL lookups.
    
    Free service with rate limits (30 requests/minute).
    Provides threat intelligence from multiple feeds.
    """
    
    NAME = "pulsedive"
    SUPPORTED_TYPES = ["ip", "domain", "url"]
    REQUIRES_API_KEY = False  # Free tier works without key
    RATE_LIMIT = 30  # requests per minute
    CACHE_TTL = 1800  # 30 minutes cache
    
    BASE_URL = "https://pulsedive.com/api"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        # API key increases rate limits but not required
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query Pulsedive for an observable."""
        try:
            data = self._query_indicator(observable)
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Dict:
        """Make request to Pulsedive."""
        import urllib.request
        
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    
    def _query_indicator(self, value: str) -> Dict:
        """Query indicator by value."""
        # First get indicator info
        import urllib.parse
        encoded = urllib.parse.quote(value)
        url = f"{self.BASE_URL}/info.php?indicator={encoded}"
        return self._make_request(url)
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on Pulsedive risk."""
        if "error" in data:
            return ("error", data["error"])
        
        # Check if we got results
        indicators = data.get("results", [data])
        
        if isinstance(data, dict) and "indicator" in data:
            # Single indicator response
            risk = data.get("risk", "unknown")
            threat = data.get("threat", [])
            
            risk_map = {
                "critical": "critical",
                "high": "malicious",
                "medium": "suspicious",
                "low": "suspicious",
                "none": "benign",
                "unknown": "unknown"
            }
            
            classification = risk_map.get(risk, "unknown")
            threat_names = [t.get("name", "") for t in threat] if threat else []
            
            if classification == "malicious" or classification == "critical":
                return ("malicious", f"Risk: {risk}. Threats: {', '.join(threat_names[:3])}")
            
            if classification == "suspicious":
                return ("suspicious", f"Risk: {risk}")
            
            return ("benign", f"No threats detected. Risk: {risk}")
        
        return ("unknown", "No indicator data returned")