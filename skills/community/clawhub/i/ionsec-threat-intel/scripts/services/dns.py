#!/usr/bin/env python3
"""
DNS resolver services for domain lookups.
"""

import json
import urllib.request
from typing import Dict, Optional
from .base import BaseService


class DNSResolver(BaseService):
    """DNS resolution via public resolvers.
    
    Supports DNS0.eu, Google DNS, and Cloudflare DNS.
    """
    
    NAME = "dns"
    SUPPORTED_TYPES = ["domain"]
    REQUIRES_API_KEY = False
    RATE_LIMIT = 60  # requests per minute
    CACHE_TTL = 3600  # 1 hour cache
    
    RESOLVERS = {
        "dns0": {
            "url": "https://dns0.eu",
            "malicious_detector": True
        },
        "google_dns": {
            "url": "https://dns.google/resolve",
            "malicious_detector": False
        },
        "cloudflare_dns": {
            "url": "https://cloudflare-dns.com/dns-query",
            "malicious_detector": False
        }
    }
    
    def __init__(self, resolver: str = "dns0", **kwargs):
        super().__init__(**kwargs)
        self.resolver = resolver
        if self.resolver not in self.RESOLVERS:
            raise ValueError(f"Unknown resolver: {self.resolver}. Options: {list(self.RESOLVERS.keys())}")
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query DNS for a domain."""
        if obs_type != "domain":
            return self._error_response(f"Unsupported type: {obs_type}")
        
        try:
            data = self._resolve_domain(observable)
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _resolve_domain(self, domain: str) -> Dict:
        """Resolve domain via configured resolver."""
        resolver_config = self.RESOLVERS[self.resolver]
        base_url = resolver_config["url"]
        
        if self.resolver == "dns0":
            # DNS0 with malicious detection
            return self._query_dns0(domain)
        elif self.resolver == "google_dns":
            return self._query_google_dns(domain)
        elif self.resolver == "cloudflare_dns":
            return self._query_cloudflare_dns(domain)
    
    def _query_dns0(self, domain: str) -> Dict:
        """Query DNS0.eu for resolution and malicious detection."""
        # Check resolution
        import urllib.parse
        encoded = urllib.parse.quote(domain)
        url = f"https://dns0.eu/resolve?name={encoded}&type=A"
        
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            resolution = json.loads(response.read().decode("utf-8"))
        
        # Check malicious detection
        mal_url = f"https://dns0.eu/check/{encoded}"
        try:
            mal_req = urllib.request.Request(mal_url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(mal_req, timeout=self.timeout) as response:
                malicious = json.loads(response.read().decode("utf-8"))
                resolution["malicious"] = malicious
        except:
            resolution["malicious"] = None
        
        return resolution
    
    def _query_google_dns(self, domain: str) -> Dict:
        """Query Google Public DNS."""
        import urllib.parse
        encoded = urllib.parse.quote(domain)
        url = f"https://dns.google/resolve?name={encoded}&type=ANY"
        
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    
    def _query_cloudflare_dns(self, domain: str) -> Dict:
        """Query Cloudflare DNS over HTTPS."""
        import urllib.parse
        encoded = urllib.parse.quote(domain)
        url = f"https://cloudflare-dns.com/dns-query?name={encoded}&type=A"
        
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on DNS resolution and malicious detection."""
        # Check for DNS0 malicious flag
        malicious = data.get("malicious")
        if malicious and isinstance(malicious, dict):
            if malicious.get("malicious", False):
                return ("malicious", "Domain flagged as malicious by DNS0")
        
        # Check resolution status
        status = data.get("Status", 0)
        if status == 3:  # NXDOMAIN
            return ("unknown", "Domain does not exist (NXDOMAIN)")
        
        # Get resolved IPs
        answers = data.get("Answer", [])
        if answers:
            ips = [a.get("data", "") for a in answers if a.get("type") == 1]
            if ips:
                return ("benign", f"Resolves to: {', '.join(ips[:5])}")
            return ("benign", "DNS records found")
        
        return ("unknown", "No DNS records found")