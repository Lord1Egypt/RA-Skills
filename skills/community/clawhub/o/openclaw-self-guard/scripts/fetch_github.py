#!/usr/bin/env python3
"""
OpenClaw Self Guard - Fetch from GitHub Security Advisories
Checks GitHub Advisory Database for OpenClaw-related vulnerabilities
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

GITHUB_GHSA_API = "https://api.github.com/advisories"


def fetch_github_advisories(ecosystem: str = "npm", severity: str = None) -> List[Dict]:
    """Fetch advisories from GitHub Advisory Database"""
    advisories = []
    
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "OpenClaw-SelfGuard/1.0"
    }
    
    params = {
        "type": "reviewed",
        "ecosystem": ecosystem,
        "severity": severity if severity else undefined,
        "per_page": 100
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        response = requests.get(
            GITHUB_GHSA_API,
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            for advisory in data:
                ghsa_id = advisory.get("ghsa_id", "")
                cve_id = advisory.get("cve_id", "")
                description = advisory.get("description", "")
                severity = advisory.get("severity", "UNKNOWN")
                published = advisory.get("published_at", "")[:10]
                updated = advisory.get("updated_at", "")[:10]
                
                # Get affected ranges
                vulnerabilities = advisory.get("vulnerabilities", [])
                affected = []
                for vuln in vulnerabilities:
                    pkg = vuln.get("package", {}).get("name", "")
                    range_info = vuln.get("vulnerable_version_range", "")
                    first_fixed = vuln.get("first_patched_version", {}).get("identifier", "")
                    affected.append({
                        "package": pkg,
                        "range": range_info,
                        "fixed": first_fixed if first_fixed else "No fix available"
                    })
                
                advisories.append({
                    "ghsa_id": ghsa_id,
                    "cve_id": cve_id,
                    "description": description[:300],
                    "severity": severity.upper(),
                    "published": published,
                    "updated": updated,
                    "affected": affected,
                    "source": "GitHub"
                })
                
    except Exception as e:
        print(f"Error fetching GitHub advisories: {e}", file=sys.stderr)
    
    return advisories


def check_openclaw_advisories() -> List[Dict]:
    """Check for OpenClaw-specific advisories"""
    all_advisories = []
    
    # Check NPM ecosystem for OpenClaw
    advisories = fetch_github_advisories(ecosystem="npm")
    for adv in advisories:
        desc_lower = adv.get("description", "").lower()
        pkg_name = ""
        for aff in adv.get("affected", []):
            pkg_name += aff.get("package", "").lower() + " "
        
        # Check if related to OpenClaw
        if "openclaw" in desc_lower or "openclaw" in pkg_name or "claw" in desc_lower:
            all_advisories.append(adv)
    
    return all_advisories


def get_recent_advisories(days: int = 30) -> List[Dict]:
    """Get recent advisories from all ecosystems"""
    all_advisories = []
    cutoff = datetime.now() - timedelta(days=days)
    
    for ecosystem in ["npm", "pip", "go", "rubygems", "maven", "nuget", "composer"]:
        advisories = fetch_github_advisories(ecosystem=ecosystem)
        
        for adv in advisories:
            try:
                pub_date = datetime.strptime(adv.get("published", "")[:10], "%Y-%m-%d")
                if pub_date >= cutoff:
                    adv["ecosystem"] = ecosystem
                    all_advisories.append(adv)
            except (ValueError, TypeError):
                pass
    
    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}
    all_advisories.sort(key=lambda x: severity_order.get(x.get("severity", "UNKNOWN"), 5))
    
    return all_advisories


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    severity = sys.argv[2] if len(sys.argv) > 2 else None
    
    if "--openclaw" in sys.argv:
        advisories = check_openclaw_advisories()
        print(json.dumps({
            "count": len(advisories),
            "type": "openclaw_specific",
            "advisories": advisories
        }, indent=2))
    else:
        advisories = get_recent_advisories(days)
        print(json.dumps({
            "count": len(advisories),
            "type": "recent",
            "days": days,
            "advisories": advisories[:30]  # Limit to top 30
        }, indent=2))
