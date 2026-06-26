#!/usr/bin/env python3
"""
Bulk checker for processing multiple observables from file.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent))

from threat_intel import load_config, query_all_services


def parse_observables(file_path: str) -> List[tuple]:
    """Parse observables from file.
    
    Format: one per line, optionally with type prefix:
        ip:8.8.8.8
        domain:evil.com
        hash:a3b2c1d4
        url:http://example.com
    
    Or just values (auto-detected):
        8.8.8.8
        evil.com
    """
    observables = []
    
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Check for type prefix
            if ":" in line and line.split(":")[0] in ["ip", "domain", "hash", "url"]:
                obs_type, value = line.split(":", 1)
            else:
                # Auto-detect type
                obs_type = detect_type(line)
                value = line
            
            observables.append((value, obs_type))
    
    return observables


def detect_type(value: str) -> str:
    """Auto-detect observable type."""
    import re
    
    # IP address
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value):
        return "ip"
    
    # Hash (MD5, SHA1, SHA256)
    if re.match(r"^[a-fA-F0-9]{32}$", value):
        return "hash"  # MD5
    if re.match(r"^[a-fA-F0-9]{40}$", value):
        return "hash"  # SHA1
    if re.match(r"^[a-fA-F0-9]{64}$", value):
        return "hash"  # SHA256
    
    # URL
    if value.startswith(("http://", "https://")):
        return "url"
    
    # Default to domain
    return "domain"


def main():
    parser = argparse.ArgumentParser(description="Bulk IOC checker from file")
    parser.add_argument("input", help="Input file with observables")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--services", "-s", default="all",
                        help="Comma-separated services (default: all)")
    parser.add_argument("--format", "-f", choices=["json", "markdown"],
                        default="json", help="Output format")
    
    args = parser.parse_args()
    
    # Parse input file
    observables = parse_observables(args.input)
    if not observables:
        print("No observables found in input file", file=sys.stderr)
        sys.exit(1)
    
    print(f"Processing {len(observables)} observables...")
    
    config = load_config()
    all_results = []
    
    for value, obs_type in observables:
        print(f"  Checking {obs_type}: {value}...")
        
        # Determine services
        from threat_intel import OBSERVABLE_SERVICES
        available = OBSERVABLE_SERVICES.get(obs_type, [])
        services = available if args.services == "all" else [s.strip() for s in args.services.split(",")]
        services = [s for s in services if s in available]
        
        results = query_all_services(value, obs_type, services, config)
        all_results.append({
            "observable": value,
            "type": obs_type,
            "results": results
        })
    
    # Output results
    if args.format == "json":
        output = json.dumps(all_results, indent=2)
    else:
        # Markdown
        lines = ["# Bulk Threat Intel Report\n"]
        for item in all_results:
            lines.append(f"## {item['type'].upper()}: `{item['observable']}`\n")
            for r in item['results']:
                svc = r.get('service', 'unknown')
                status = r.get('status', 'unknown')
                classification = r.get('classification', 'unknown')
                lines.append(f"- **{svc}**: {status} ({classification})")
            lines.append("")
        output = "\n".join(lines)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"\n✅ Results saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
