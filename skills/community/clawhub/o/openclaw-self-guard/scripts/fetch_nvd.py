#!/usr/bin/env python3
"""
OpenClaw Self Guard - Fetch CVEs from NVD
Searches NVD for OpenClaw-related and other critical CVEs
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Keywords to search for OpenClaw and similar platforms
SEARCH_KEYWORDS = [
    "openclaw",
    "claw",
    "agent framework",
    "open source agent",
]

# Critical software packages often used
CRITICAL_PACKAGES = [
    "node.js",
    "nodejs",
    "npm",
    "python",
    "linux kernel",
]


def fetch_cves_for_keyword(keyword: str, days: int = 7) -> List[Dict]:
    """Fetch CVEs matching a keyword"""
    cves = []
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    params = {
        "pubStartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": 50,
        "keywordSearch": keyword
    }
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "OpenClaw-SelfGuard/1.0"
    }
    
    try:
        response = requests.get(NVD_API_BASE, params=params, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            for vuln in data.get("vulnerabilities", []):
                cve = vuln.get("cve", {})
                cve_id = cve.get("id", "N/A")
                
                # Get English description
                descriptions = cve.get("descriptions", [])
                description = ""
                for desc in descriptions:
                    if desc.get("lang") == "en":
                        description = desc.get("value", "")
                        break
                
                # Get CVSS score
                metrics = cve.get("metrics", {})
                cvss_score = "N/A"
                cvss_severity = "UNKNOWN"
                
                if "cvssMetricV31" in metrics and metrics["cvssMetricV31"]:
                    cvss_data = metrics["cvssMetricV31"][0].get("cvssData", {})
                    cvss_score = cvss_data.get("baseScore", "N/A")
                    cvss_severity = cvss_data.get("baseSeverity", "UNKNOWN")
                elif "cvssMetricV30" in metrics and metrics["cvssMetricV30"]:
                    cvss_data = metrics["cvssMetricV30"][0].get("cvssData", {})
                    cvss_score = cvss_data.get("baseScore", "N/A")
                    cvss_severity = cvss_data.get("baseSeverity", "UNKNOWN")
                elif "cvssMetricV2" in metrics and metrics["cvssMetricV2"]:
                    cvss_data = metrics["cvssMetricV2"][0].get("cvssData", {})
                    cvss_score = cvss_data.get("baseScore", "N/A")
                
                published = cve.get("published", "")[:10]
                
                cves.append({
                    "cve_id": cve_id,
                    "description": description[:300],
                    "cvss_score": cvss_score,
                    "cvss_severity": cvss_severity,
                    "published": published,
                    "source": "NVD"
                })
                
    except Exception as e:
        print(f"Error fetching CVEs for {keyword}: {e}", file=sys.stderr)
    
    return cves


def fetch_recent_cves(days: int = 7, min_cvss: float = 7.0) -> List[Dict]:
    """Fetch all recent high-severity CVEs"""
    all_cves = []
    seen_ids = set()
    
    # Fetch for each keyword
    for keyword in SEARCH_KEYWORDS + CRITICAL_PACKAGES:
        cves = fetch_cves_for_keyword(keyword, days)
        for cve in cves:
            if cve["cve_id"] not in seen_ids:
                seen_ids.add(cve["cve_id"])
                # Filter by CVSS if we have a score
                try:
                    score = float(cve["cvss_score"])
                    if score >= min_cvss:
                        all_cves.append(cve)
                except (ValueError, TypeError):
                    # Include if no CVSS score (might be new)
                    all_cves.append(cve)
    
    # Sort by CVSS score descending
    all_cves.sort(key=lambda x: float(x["cvss_score"]) if x["cvss_score"] != "N/A" else 0, reverse=True)
    
    return all_cves


def fetch_openclaw_specific_cves() -> List[Dict]:
    """Fetch CVEs specifically mentioning OpenClaw"""
    return fetch_cves_for_keyword("OpenClaw", days=365)  # Check last year for OpenClaw specifically


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    min_cvss = float(sys.argv[2]) if len(sys.argv) > 2 else 7.0
    
    if "--openclaw-only" in sys.argv:
        cves = fetch_openclaw_specific_cves()
    else:
        cves = fetch_recent_cves(days, min_cvss)
    
    print(json.dumps({
        "count": len(cves),
        "cves": cves[:20]  # Limit to top 20
    }, indent=2))
