#!/usr/bin/env python3
"""
Validin API client for DNS and infrastructure intelligence.

Validin provides:
- Passive DNS (historical and current)
- Subdomain enumeration
- WHOIS data
- Certificate transparency logs
- Infrastructure correlation
"""

from typing import Dict, Optional, List
from .base import BaseService


class Validin(BaseService):
    """Validin API client for DNS and infrastructure intelligence.
    
    Provides passive DNS, subdomain data, and infrastructure mapping.
    Free tier available with generous limits.
    """
    
    NAME = "validin"
    SUPPORTED_TYPES = ["ip", "domain", "hash"]
    REQUIRES_API_KEY = True
    RATE_LIMIT = 60  # requests per minute
    CACHE_TTL = 3600  # 1 hour cache
    
    BASE_URL = "https://app.validin.com/api/v1"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        if not self.api_key:
            raise ValueError("Validin requires an API key (VALIDIN_API_KEY)")
    
    def query(self, observable: str, obs_type: str) -> Dict:
        """Query Validin for an observable."""
        try:
            if obs_type == "ip":
                data = self._query_ip(observable)
            elif obs_type == "domain":
                data = self._query_domain(observable)
            elif obs_type == "hash":
                data = self._query_hash(observable)
            else:
                return self._error_response(f"Unsupported type: {obs_type}")
            
            return self._success_response(data)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Dict:
        """Make authenticated request to Validin."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": "OpenClaw-ThreatIntel/1.0"
        }
        return super()._make_request(url, headers=headers)
    
    def _query_ip(self, ip: str) -> Dict:
        """Query IP for passive DNS and infrastructure data."""
        # Get DNS records pointing to this IP (reverse DNS)
        url = f"{self.BASE_URL}/dns/ip/{ip}"
        dns_data = self._make_request(url)
        
        # Get WHOIS data for the IP
        whois_url = f"{self.BASE_URL}/whois/ip/{ip}"
        try:
            whois_data = self._make_request(whois_url)
        except:
            whois_data = {}
        
        return {
            "dns": dns_data,
            "whois": whois_data
        }
    
    def _query_domain(self, domain: str) -> Dict:
        """Query domain for DNS history and subdomains."""
        # Get current DNS records
        dns_url = f"{self.BASE_URL}/dns/domain/{domain}"
        dns_data = self._make_request(dns_url)
        
        # Get historical DNS (passive DNS)
        history_url = f"{self.BASE_URL}/dns/history/{domain}"
        try:
            history_data = self._make_request(history_url)
        except:
            history_data = {}
        
        # Get subdomains
        subdomains_url = f"{self.BASE_URL}/subdomains/{domain}"
        try:
            subdomains_data = self._make_request(subdomains_url)
        except:
            subdomains_data = {}
        
        # Get WHOIS
        whois_url = f"{self.BASE_URL}/whois/domain/{domain}"
        try:
            whois_data = self._make_request(whois_url)
        except:
            whois_data = {}
        
        return {
            "dns": dns_data,
            "history": history_data,
            "subdomains": subdomains_data,
            "whois": whois_data
        }
    
    def _query_hash(self, hash_value: str) -> Dict:
        """Query hash for infrastructure correlations."""
        # Validin may not support hash lookups directly
        # Return error for now, can be extended later
        return {"error": "Hash lookups not supported by Validin"}
    
    def _classify_result(self, data: Dict) -> tuple:
        """Classify based on Validin infrastructure data."""
        if "error" in data:
            return ("error", data["error"])
        
        # Check for DNS data
        dns_data = data.get("dns", {})
        history = data.get("history", {})
        subdomains = data.get("subdomains", {})
        
        # Count records
        total_records = 0
        if isinstance(dns_data, dict):
            total_records += len(dns_data.get("records", []))
        
        # Check historical data
        historical_records = 0
        if isinstance(history, dict):
            historical_records = len(history.get("changes", []))
        
        # Subdomain count
        subdomain_count = 0
        if isinstance(subdomains, dict):
            subdomain_list = subdomains.get("subdomains", subdomains.get("domains", []))
            subdomain_count = len(subdomain_list) if isinstance(subdomain_list, list) else 0
        
        # Build summary
        parts = []
        if total_records > 0:
            parts.append(f"{total_records} current DNS records")
        if historical_records > 0:
            parts.append(f"{historical_records} historical changes")
        if subdomain_count > 0:
            parts.append(f"{subdomain_count} subdomains")
        
        summary = "; ".join(parts) if parts else "Infrastructure data found"
        
        # Check for suspicious patterns
        suspicious_tlds = [
            ".tk", ".ml", ".ga", ".cf", ".gq",  # Free domains often abused
            ".top", ".xyz", ".click", ".download"
        ]
        
        # Look at domain for suspicious patterns
        domain = None
        if isinstance(dns_data, dict) and "domain" in dns_data:
            domain = dns_data["domain"]
        elif isinstance(subdomains, dict) and "domain" in subdomains:
            domain = subdomains["domain"]
        
        if domain and any(domain.endswith(tld) for tld in suspicious_tlds):
            return ("suspicious", f"Suspicious TLD. {summary}")
        
        # Many subdomains can indicate suspicious activity
        if subdomain_count > 100:
            return ("suspicious", f"Large subdomain count ({subdomain_count}). {summary}")
        
        if subdomain_count > 10:
            return ("benign", f"Active domain with subdomains. {summary}")
        
        if total_records > 0 or historical_records > 0:
            return ("benign", summary)
        
        return ("unknown", "No DNS infrastructure data found")
