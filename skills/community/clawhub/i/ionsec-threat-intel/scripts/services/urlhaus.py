#!/usr/bin/env python3
"""
Abuse.ch URLhaus API client.
"""

import urllib.request
import urllib.parse
import json
from typing import Dict, Optional
from .base import BaseService


class URLhaus(BaseService):
    """URLhaus API client for malicious URL lookups.
    
    Free service from Abuse.ch for querying malicious URLs.
    """
    
    NAME = "urlhaus"
    SUPPORTED_TYPES = ["url", "domain", "hash"]
    REQUIRES_API_KEY = False
    RATE_LIMIT = 60  # requests per minute
    CACHE_TTL = 3600  # 1 hour cache
    
    BASE_URL = "https://urlhaus-api.abuse.ch/v1/"
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query URLhaus for URL, domain, or hash."""
        try:
            if obs_type == "url":
                data = self._query_url(observable)
            elif obs_type == "domain":
                data = self._query_domain(observable)
            elif obs_type == "hash":
                data = self._query_hash(observable)
            else:
                return self._error_response(f"Unsupported type: {obs_type}")
            
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make POST request to URLhaus."""
        encoded_data = urllib.parse.urlencode(params).encode()
        url = f"{self.BASE_URL}{endpoint}/"
        
        req = urllib.request.Request(
            url,
            data=encoded_data,
            headers={"User-Agent": "OpenClaw-ThreatIntel/1.0"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    
    def _query_url(self, url: str) -> Dict:
        """Query by URL."""
        return self._make_request("url", {"url": url})
    
    def _query_domain(self, domain: str) -> Dict:
        """Query by domain."""
        return self._make_request("host", {"host": domain})
    
    def _query_hash(self, hash_value: str) -> Dict:
        """Query by payload hash."""
        return self._make_request("payload", {"hash": hash_value})
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on URLhaus data."""
        query_status = data.get("query_status", "unknown")
        
        if query_status == "ok":
            # Check threat type
            threat = data.get("threat", "")
            url_status = data.get("url_status", "")
            
            if threat:
                return ("malicious", f"Threat type: {threat}. Status: {url_status}")
            
            # Check if online
            if url_status == "online":
                return ("suspicious", "URL marked as malicious, currently online")
            
            return ("suspicious", f"Malicious URL (status: {url_status})")
        
        if query_status == "no_results":
            return ("benign", "Not found in URLhaus database")
        
        return ("unknown", f"Query status: {query_status}")