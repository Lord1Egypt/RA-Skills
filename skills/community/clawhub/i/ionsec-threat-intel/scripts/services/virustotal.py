#!/usr/bin/env python3
"""
VirusTotal v3 API client.
"""

from typing import Dict, Optional
from .base import BaseService


class VirusTotal(BaseService):
    """VirusTotal v3 API client for IP, domain, URL, and hash lookups."""
    
    NAME = "virustotal"
    SUPPORTED_TYPES = ["ip", "domain", "hash", "url"]
    REQUIRES_API_KEY = True
    RATE_LIMIT = 4  # Free tier: 4 requests/minute
    CACHE_TTL = 3600  # 1 hour cache
    
    BASE_URL = "https://www.virustotal.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        if not self.api_key:
            raise ValueError("VirusTotal requires an API key (VT_API_KEY)")
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query VirusTotal for the observable."""
        try:
            if obs_type == "ip":
                data = self._query_ip(observable)
            elif obs_type == "domain":
                data = self._query_domain(observable)
            elif obs_type == "hash":
                data = self._query_file(observable)
            elif obs_type == "url":
                data = self._query_url(observable)
            else:
                return self._error_response(f"Unsupported type: {obs_type}")
            
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Dict:
        """Make authenticated request to VirusTotal."""
        headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }
        return super()._make_request(url, headers=headers)
    
    def _query_ip(self, ip: str) -> Dict:
        """Query IP address."""
        url = f"{self.BASE_URL}/ip_addresses/{ip}"
        return self._make_request(url)
    
    def _query_domain(self, domain: str) -> Dict:
        """Query domain."""
        url = f"{self.BASE_URL}/domains/{domain}"
        return self._make_request(url)
    
    def _query_file(self, hash_value: str) -> Dict:
        """Query file hash."""
        url = f"{self.BASE_URL}/files/{hash_value}"
        return self._make_request(url)
    
    def _query_url(self, url: str) -> Dict:
        """Query URL using URL identifier."""
        import base64
        import hashlib
        
        # VT uses URL identifier: base64(url) without padding
        url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
        api_url = f"{self.BASE_URL}/urls/{url_id}"
        return self._make_request(api_url)
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on VT last_analysis_stats."""
        attributes = data.get("data", {}).get("attributes", {})
        stats = attributes.get("last_analysis_stats", {})
        
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        total = sum(stats.values()) if stats else 0
        
        if total == 0:
            return ("unknown", "No analysis data available")
        
        ratio = f"{malicious}/{total}"
        
        if malicious > 10:
            return ("malicious", f"Detected by {ratio} vendors")
        elif malicious > 0:
            return ("suspicious", f"Detected by {ratio} vendors")
        elif suspicious > 0:
            return ("suspicious", f"Suspicious by {suspicious} vendors")
        else:
            reputation = attributes.get("reputation", 0)
            if reputation < -10:
                return ("suspicious", f"Reputation: {reputation}")
            return ("benign", f"Clean ({ratio} detections)")