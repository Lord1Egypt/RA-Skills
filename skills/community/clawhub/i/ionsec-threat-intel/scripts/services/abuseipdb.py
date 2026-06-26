#!/usr/bin/env python3
"""
AbuseIPDB API client for IP reputation.
"""

import urllib.parse
from typing import Dict, Optional
from .base import BaseService


class AbuseIPDB(BaseService):
    """AbuseIPDB API client for IP abuse reports.
    
    Provides confidence scores and abuse report counts for IP addresses.
    """
    
    NAME = "abuseipdb"
    SUPPORTED_TYPES = ["ip"]
    REQUIRES_API_KEY = True
    RATE_LIMIT = 5  # Free tier: 5 requests/minute
    CACHE_TTL = 1800  # 30 minutes cache
    
    BASE_URL = "https://api.abuseipdb.com/api/v2/check"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        if not self.api_key:
            raise ValueError("AbuseIPDB requires an API key (ABUSEIPDB_API_KEY)")
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query AbuseIPDB for an IP address."""
        if obs_type != "ip":
            return self._error_response(f"Unsupported type: {obs_type}")
        
        try:
            data = self._check_ip(observable)
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Dict:
        """Make authenticated request to AbuseIPDB."""
        headers = {
            "Key": self.api_key,
            "Accept": "application/json"
        }
        return super()._make_request(url, headers=headers)
    
    def _check_ip(self, ip: str) -> Dict:
        """Check IP address reputation."""
        params = {
            "ipAddress": ip,
            "maxAgeInDays": 90,
            "verbose": True
        }
        url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
        return self._make_request(url)
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on AbuseIPDB confidence score."""
        result = data.get("data", data)
        
        abuse_score = result.get("abuseConfidenceScore", 0)
        total_reports = result.get("totalReports", 0)
        num_distinct_users = result.get("numDistinctUsers", 0)
        
        # High confidence score
        if abuse_score >= 75:
            return ("malicious", f"Abuse score: {abuseScore}%, {totalReports} reports from {num_distinct_users} users")
        
        # Moderate confidence
        if abuse_score >= 50:
            return ("suspicious", f"Abuse score: {abuse_score}%, {total_reports} reports")
        
        # Low confidence but has reports
        if total_reports > 0:
            return ("suspicious", f"Low abuse score ({abuse_score}%), but {total_reports} reports")
        
        # Clean
        return ("benign", f"No abuse reports. Country: {result.get('countryCode', 'Unknown')}")