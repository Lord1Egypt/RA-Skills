#!/usr/bin/env python3
"""
Spur.us API client for VPN/proxy/hosting detection.

Spur.us identifies if an IP is associated with:
- VPN services
- Proxies (SOCKS, HTTP)
- Cloud/hosting providers
- Residential proxies
- TOR exit nodes
"""

from typing import Dict, Optional
from .base import BaseService


class SpurUs(BaseService):
    """Spur.us API client for infrastructure detection.
    
    Detects VPNs, proxies, hosting providers, and residential IPs.
    Particularly useful for fraud detection and user verification.
    """
    
    NAME = "spur"
    SUPPORTED_TYPES = ["ip"]
    REQUIRES_API_KEY = True
    RATE_LIMIT = 60  # requests per minute
    CACHE_TTL = 3600  # 1 hour cache
    
    BASE_URL = "https://api.spur.us/v2"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        if not self.api_key:
            raise ValueError("Spur.us requires an API key (SPUR_API_KEY)")
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query Spur.us for an IP address."""
        if obs_type != "ip":
            return self._error_response(f"Unsupported type: {obs_type}")
        
        try:
            data = self._query_context(observable)
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Dict:
        """Make authenticated request to Spur.us."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        return super()._make_request(url, headers=headers)
    
    def _query_context(self, ip: str) -> Dict:
        """Get full context for an IP."""
        url = f"{self.BASE_URL}/context/{ip}"
        return self._make_request(url)
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on Spur.us infrastructure detection."""
        if "error" in data:
            return ("error", data["error"])
        
        # Extract key fields
        vpn = data.get("vpn", False)
        proxy = data.get("proxy", False)
        tor = data.get("tor", False)
        hosting = data.get("hosting", False)
        residential = data.get("residential", False)
        
        # Build classification
        risks = []
        if vpn:
            risks.append("VPN")
        if proxy:
            risks.append("Proxy")
        if tor:
            risks.append("TOR")
        if hosting:
            risks.append("Hosting")
        if residential:
            risks.append("Residential Proxy")
        
        # Get organization and location
        org = data.get("organization", "Unknown")
        location = data.get("location", {})
        country = location.get("country", "Unknown")
        
        if risks:
            risk_str = ", ".join(risks)
            if tor:
                return ("malicious", f"TOR exit node detected. Org: {org}")
            if vpn or proxy:
                return ("suspicious", f"{risk_str} detected. Org: {org}, Country: {country}")
            return ("suspicious", f"{risk_str}. Org: {org}, Country: {country}")
        
        # Clean result
        asn = data.get("asn", "Unknown")
        return ("benign", f"No VPN/proxy detected. ASN: {asn}, Org: {org}")
