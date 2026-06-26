#!/usr/bin/env python3
"""
AlienVault OTX API client.
"""

from typing import Dict, Optional
from .base import BaseService


class AlienVaultOTX(BaseService):
    """AlienVault OTX API client for IP, domain, URL, and hash lookups.
    
    Provides threat intel from OTX community including pulses,
    malware families, and related indicators.
    """
    
    NAME = "otx"
    SUPPORTED_TYPES = ["ip", "domain", "hash", "url"]
    REQUIRES_API_KEY = True
    RATE_LIMIT = 60  # requests per minute
    CACHE_TTL = 3600  # 1 hour cache
    
    BASE_URL = "https://otx.alienvault.com/api/v1/indicators"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        if not self.api_key:
            raise ValueError("OTX requires an API key (OTX_API_KEY)")
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query OTX for the observable."""
        type_map = {
            "ip": "IPv4",
            "domain": "domain",
            "hash": "file",
            "url": "url"
        }
        
        otx_type = type_map.get(obs_type)
        if not otx_type:
            return self._error_response(f"Unsupported type: {obs_type}")
        
        try:
            data = self._query_observable(observable, otx_type)
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Dict:
        """Make authenticated request to OTX."""
        headers = {
            "X-OTX-API-KEY": self.api_key,
            "Accept": "application/json"
        }
        return super()._make_request(url, headers=headers)
    
    def _query_observable(self, value: str, otx_type: str) -> Dict:
        """Query observable by type."""
        # Get general info
        general_url = f"{self.BASE_URL}/{otx_type}/{value}/general"
        general = self._make_request(general_url)
        
        # Get reputation for IPs
        if otx_type == "IPv4":
            rep_url = f"{self.BASE_URL}/{otx_type}/{value}/reputation"
            rep = self._make_request(rep_url)
            general["reputation"] = rep
        
        return general
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on OTX pulse count and reputation."""
        # Check pulse count
        pulses = data.get("general", data).get("pulse_info", {}).get("pulses", [])
        pulse_count = len(pulses)
        
        # High pulse count suggests malicious
        if pulse_count > 5:
            tags = []
            for pulse in pulses[:3]:
                tags.extend(pulse.get("tags", [])[:3])
            return ("malicious", f"Found in {pulse_count} pulses. Tags: {', '.join(tags[:5])}")
        
        if pulse_count > 0:
            names = [p.get("name", "") for p in pulses[:3]]
            return ("suspicious", f"Found in {pulse_count} pulse(s): {', '.join(names)}")
        
        # Check reputation for IPs
        reputation = data.get("reputation", {})
        if reputation:
            threat_score = reputation.get("threat_score", 0)
            if threat_score > 2:
                return ("malicious", f"Threat score: {threat_score}")
        
        return ("benign", "No threat intelligence found")