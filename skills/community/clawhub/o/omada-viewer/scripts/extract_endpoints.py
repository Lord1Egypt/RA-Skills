#!/usr/bin/env python3
"""Extract and organize endpoints from an OpenAPI spec export.

Usage:
  python extract_endpoints.py <path/to/openapi-spec.json> [output.md]
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_endpoints.py <path/to/openapi-spec.json> [output.md]")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    
    paths = spec.get("paths", {})
    
    # Group by category
    categories = defaultdict(list)
    
    for path, methods in sorted(paths.items()):
        # Skip MSP-only paths for now
        if "/msp/" in path:
            continue
            
        # Categorize
        path_lower = path.lower()
        
        if "/sites/{siteid}" not in path_lower:
            category = "Global/Controller"
        elif "/client" in path_lower:
            category = "Clients"
        elif "/ap" in path_lower or "/eap" in path_lower:
            category = "Access Points"
        elif "/switch" in path_lower:
            category = "Switches"
        elif "/gateway" in path_lower or "/osg" in path_lower:
            category = "Gateway"
        elif "/wlan" in path_lower or "/ssid" in path_lower or "/wireless" in path_lower:
            category = "Wireless/WLAN"
        elif "/lan" in path_lower or "/vlan" in path_lower or "/network" in path_lower:
            category = "LAN/Networks"
        elif "/nat" in path_lower or "/firewall" in path_lower or "/port-forward" in path_lower:
            category = "NAT/Firewall"
        elif "/vpn" in path_lower or "/ipsec" in path_lower:
            category = "VPN"
        elif "/dhcp" in path_lower:
            category = "DHCP"
        elif "/device" in path_lower:
            category = "Devices"
        elif "/portal" in path_lower or "/hotspot" in path_lower:
            category = "Portal/Hotspot"
        elif "/log" in path_lower or "/alert" in path_lower:
            category = "Logs/Alerts"
        elif "/dashboard" in path_lower or "/insight" in path_lower or "/stat" in path_lower:
            category = "Dashboard/Stats"
        elif "/setting" in path_lower or "/config" in path_lower:
            category = "Settings"
        else:
            category = "Other"
        
        for method, details in methods.items():
            if method not in ["get", "post", "put", "delete", "patch"]:
                continue
            summary = details.get("summary", "")
            categories[category].append({
                "method": method.upper(),
                "path": path,
                "summary": summary
            })
    
    # Output markdown
    print("# Omada Controller API Endpoints")
    print()
    print("Extracted from OpenAPI spec (v3/api-docs)")
    print()
    print("Base URL: `https://{controller}:8043`")
    print()
    print("Path variables:")
    print("- `{omadacId}` = Controller ID (from /api/info)")
    print("- `{siteId}` = Site ID (from /sites endpoint)")
    print()
    
    for category in sorted(categories.keys()):
        endpoints = categories[category]
        print(f"## {category}")
        print()
        print("| Method | Path | Description |")
        print("|--------|------|-------------|")
        for ep in endpoints:
            # Shorten path for readability
            short_path = ep["path"].replace("/openapi/v1/{omadacId}", "")
            short_path = short_path.replace("/sites/{siteId}", "/sites/{siteId}")
            summary = ep["summary"][:60] + "..." if len(ep["summary"]) > 60 else ep["summary"]
            print(f"| {ep['method']} | `{short_path}` | {summary} |")
        print()

if __name__ == "__main__":
    main()
