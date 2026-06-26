#!/usr/bin/env python3
"""
Shodan API client for IP intelligence.
"""

from typing import Dict, Optional
from .base import BaseService


class Shodan(BaseService):
    """Shodan API client for IP analysis.
    
    Provides open ports, services, vulnerabilities, and general
    internet exposure data for IP addresses.
    """
    
    NAME = "shodan"
    SUPPORTED_TYPES = ["ip"]
    REQUIRES_API_KEY = True
    RATE_LIMIT = 60  # requests per minute
    CACHE_TTL = 3600  # 1 hour cache
    
    BASE_URL = "https://api.shodan.io"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        if not self.api_key:
            raise ValueError("Shodan requires an API key (SHODAN_API_KEY)")
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query Shodan for an IP address."""
        if obs_type != "ip":
            return self._error_response(f"Unsupported type: {obs_type}")
        
        try:
            data = self._query_host(observable)
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Dict:
        """Make authenticated request to Shodan."""
        # Shodan uses ?key= query param
        full_url = f"{url}?key={self.api_key}" if "?" not in url else f"{url}&key={self.api_key}"
        return super()._make_request(full_url)
    
    def _query_host(self, ip: str) -> Dict:
        """Get host information."""
        url = f"{self.BASE_URL}/shodan/host/{ip}"
        return self._make_request(url)
    
    def _query_honeyscore(self, ip: str) -> Dict:
        """Check if IP is a honeypot."""
        url = f"{self.BASE_URL}/labs/honeyscore/{ip}"
        return self._make_request(url)
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on Shodan data."""
        if "error" in data:
            return ("unknown", data["error"])
        
        # No data found
        if not data.get("data") and not data.get("ports"):
            return ("unknown", "No data found for this IP")
        
        ports = data.get("ports", [])
        hostnames = data.get("hostnames", [])
        org = data.get("org", "Unknown")
        isp = data.get("isp", "Unknown")
        vulns = data.get("vulns", [])
        
        # Check for common malicious patterns
        tags = data.get("tags", [])
        if any(t in ["malware", "compromised", "attacker"] for t in tags):
            return ("malicious", f"Tagged as malicious. Ports: {ports}")
        
        # Has known vulnerabilities
        if vulns and len(vulns) > 0:
            return ("suspicious", f"Vulnerable ({len(vulns)} CVEs). Ports: {ports}")
        
        # Standard exposure
        open_ports = len(ports)
        if open_ports > 0:
            port_list = ", ".join(str(p) for p in ports[:10])
            return ("exposed", f"{open_ports} open ports: {port_list}. Org: {org}")
        
        return ("benign", f"No exposure detected. Org: {org}")