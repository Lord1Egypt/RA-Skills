#!/usr/bin/env python3
"""
IP address checker - quick utility for IP reputation.
"""

import sys
import argparse
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))

from threat_intel import load_config, query_all_services


def main():
    parser = argparse.ArgumentParser(description="Check IP reputation across multiple services")
    parser.add_argument("ip", help="IP address to check")
    parser.add_argument("--services", "-s", default="abuseipdb,pulsedive",
                        help="Comma-separated services (default: abuseipdb,pulsedive)")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    config = load_config()
    services = [s.strip() for s in args.services.split(",")]
    
    results = query_all_services(args.ip, "ip", services, config)
    
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        from threat_intel import print_table
        print_table(results)


if __name__ == "__main__":
    main()
