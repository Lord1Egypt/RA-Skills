#!/usr/bin/env python3
"""
URLScan API client for URL analysis.
"""

import base64
from typing import Dict, Optional
from .base import BaseService


class URLScan(BaseService):
    """URLScan API client for URL scanning and screenshots.
    
    Provides live URL scanning, screenshot capture, and
    technology detection.
    """
    
    NAME = "urlscan"
    SUPPORTED_TYPES = ["url"]
    REQUIRES_API_KEY = False  # Public API works with rate limits
    RATE_LIMIT = 60  # requests per minute
    CACHE_TTL = 3600  # 1 hour cache
    
    BASE_URL = "https://urlscan.io/api/v1"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        # API key optional, increases rate limits
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query URLScan for a URL."""
        if obs_type != "url":
            return self._error_response(f"Unsupported type: {obs_type}")
        
        try:
            # First check if already scanned
            data = self._search_url(observable)
            if data.get("results"):
                return self._success_response(data)
            
            # If not, need to scan (requires API key for private scans)
            if self.api_key:
                data = self._submit_scan(observable)
                return self._success_response(data)
            
            return self._error_response("URL not previously scanned. Submit scan requires API key.")
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str, method: str = "GET", data: Optional[bytes] = None) -> Dict:
        """Make request to URLScan."""
        headers = {"Accept": "application/json"}
        
        if self.api_key:
            headers["API-Key"] = self.api_key
        
        return super()._make_request(url, headers=headers, method=method, data=data)
    
    def _search_url(self, url: str) -> Dict:
        """Search for existing scan results."""
        import urllib.parse
        encoded = urllib.parse.quote(url)
        search_url = f"{self.BASE_URL}/search/?q=page.url:\"{encoded}\""
        return self._make_request(search_url)
    
    def _submit_scan(self, url: str) -> Dict:
        """Submit URL for scanning (requires API key)."""
        import json
        payload = json.dumps({
            "url": url,
            "public": "on"  # Public scan
        }).encode()
        
        submit_url = f"{self.BASE_URL}/scan/"
        result = self._make_request(submit_url, method="POST", data=payload)
        return result
    
    def _get_result(self, uuid: str) -> Dict:
        """Get scan result by UUID."""
        result_url = f"{self.BASE_URL}/result/{uuid}/"
        return self._make_request(result_url)
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on URLScan verdicts."""
        # Check if this is a search result
        results = data.get("results", [])
        
        if results:
            latest = results[0] if results else {}
            page = latest.get("page", {})
            verdicts = latest.get("verdicts", {})
            
            # Check verdicts
            malicious = verdicts.get("malicious", 0)
            suspicious = verdicts.get("suspicious", 0)
            
            if malicious > 0:
                url = page.get("url", "")
                return ("malicious", f"Flagged malicious. URL: {url}")
            
            if suspicious > 0:
                return ("suspicious", f"Flagged suspicious")
            
            # Check for malicious redirects or technologies
            stats = latest.get("stats", {})
            malicious_stats = stats.get("malicious", 0)
            
            if malicious_stats > 0:
                return ("suspicious", f"{malicious_stats} malicious indicators")
            
            return ("benign", f"Clean scan. {page.get('title', 'No title')}")
        
        # Direct result (from scan submission)
        if "task" in data:
            status = data.get("status", "unknown")
            if status == "pending":
                return ("unknown", "Scan in progress. Check result URL later.")
            
            verdicts = data.get("verdicts", {}).get("overall", {})
            malicious = verdicts.get("malicious", 0)
            
            if malicious > 0:
                return ("malicious", f"Malicious: {malicious} detections")
            
            return ("benign", "Scan completed, no malicious indicators")
        
        return ("unknown", "No scan data available")