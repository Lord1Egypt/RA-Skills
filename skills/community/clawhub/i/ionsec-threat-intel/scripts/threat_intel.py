#!/usr/bin/env python3
"""
Threat Intelligence Service Aggregator
Queries multiple external threat intel services for IOC enrichment.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from services import (
    AbuseIPDB,
    AlienVaultOTX,
    GreyNoise,
    MalwareBazaar,
    Pulsedive,
    Shodan,
    URLhaus,
    URLScan,
    VirusTotal,
    DNSResolver,
    SpurUs,
    Validin,
)

# Service registry - maps names to classes
SERVICE_REGISTRY = {
    # API Key required
    "virustotal": VirusTotal,
    "greynoise": GreyNoise,
    "shodan": Shodan,
    "otx": AlienVaultOTX,
    "abuseipdb": AbuseIPDB,
    "urlscan": URLScan,
    "spur": SpurUs,
    "validin": Validin,
    
    # Free services (no key)
    "malwarebazaar": MalwareBazaar,
    "urlhaus": URLhaus,
    "pulsedive": Pulsedive,
    "dns0": DNSResolver,
    "google_dns": DNSResolver,
    "cloudflare_dns": DNSResolver,
}

# Observable type to supported services mapping
OBSERVABLE_SERVICES = {
    "ip": ["virustotal", "greynoise", "shodan", "otx", "abuseipdb", "pulsedive", "spur", "validin"],
    "domain": ["virustotal", "otx", "pulsedive", "dns0", "google_dns", "cloudflare_dns", "validin"],
    "hash": ["virustotal", "otx", "malwarebazaar", "pulsedive", "validin"],
    "url": ["virustotal", "otx", "urlscan", "urlhaus", "pulsedive"],
}


def get_rate_limit_status():
    """Display current rate limit status for all services."""
    print("\n" + "=" * 70)
    print("🚦 Rate Limit Status")
    print("=" * 70)
    print(f"\n{'Service':<20} {'Rate (req/min)':<15} {'Cache TTL':<12} {'Status'}")
    print("-" * 70)
    
    for name, service_class in SERVICE_REGISTRY.items():
        limit = service_class.RATE_LIMIT if hasattr(service_class, 'RATE_LIMIT') and service_class.RATE_LIMIT else "Unlimited"
        ttl = service_class.CACHE_TTL if hasattr(service_class, 'CACHE_TTL') and service_class.CACHE_TTL else "No cache"
        
        if isinstance(ttl, int):
            ttl_str = f"{ttl // 60}m" if ttl >= 60 else f"{ttl}s"
        else:
            ttl_str = str(ttl)
        
        status = "🟢 Ready"
        if hasattr(service_class, 'REQUIRES_API_KEY') and service_class.REQUIRES_API_KEY:
            status = "🔴 Needs API key"
        
        limit_str = str(limit) if limit else "N/A"
        print(f"{name:<20} {limit_str:<15} {ttl_str:<12} {status}")
    
    print("\n" + "=" * 70)
    print("💡 Tip: Caching reduces API calls for repeated queries")
    print("=" * 70 + "\n")


def load_config() -> Dict:
    """Load configuration from config.json or environment variables."""
    config = {}
    
    # Try to load from config file
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    
    # Environment variables take precedence
    env_mapping = {
        "VT_API_KEY": "vt_api_key",
        "GREYNOISE_API_KEY": "greynoise_api_key",
        "SHODAN_API_KEY": "shodan_api_key",
        "OTX_API_KEY": "otx_api_key",
        "ABUSEIPDB_API_KEY": "abuseipdb_api_key",
        "URLSCAN_API_KEY": "urlscan_api_key",
        "SPUR_API_KEY": "spur_api_key",
        "VALIDIN_API_KEY": "validin_api_key",
    }
    
    for env_var, config_key in env_mapping.items():
        if os.getenv(env_var):
            config[config_key] = os.getenv(env_var)
    
    return config


def is_first_run() -> bool:
    """Check if this is the first time running the skill."""
    config_path = Path(__file__).parent.parent / "config.json"
    
    # If config doesn't exist, it's first run
    if not config_path.exists():
        return True
    
    # If config exists but is empty or has no keys, treat as first run
    try:
        with open(config_path) as f:
            config = json.load(f)
        # Check if any API keys are set
        has_keys = any(v for v in config.values() if v)
        return not has_keys
    except:
        return True


def run_setup_wizard():
    """Launch the interactive setup wizard only when explicitly requested."""
    setup_script = Path(__file__).parent / "setup.py"
    if not setup_script.exists():
        print("Setup script not found.", file=sys.stderr)
        return False

    os.execv(sys.executable, [sys.executable, str(setup_script)])
    return True


def get_service_instance(service_name: str, config: Dict):
    """Get initialized service instance."""
    service_class = SERVICE_REGISTRY.get(service_name)
    if not service_class:
        raise ValueError(f"Unknown service: {service_name}")
    
    # Initialize with relevant config
    service_config = {}
    if service_name == "virustotal":
        service_config["api_key"] = config.get("vt_api_key")
    elif service_name == "greynoise":
        service_config["api_key"] = config.get("greynoise_api_key")
    elif service_name == "shodan":
        service_config["api_key"] = config.get("shodan_api_key")
    elif service_name == "otx":
        service_config["api_key"] = config.get("otx_api_key")
    elif service_name == "abuseipdb":
        service_config["api_key"] = config.get("abuseipdb_api_key")
    elif service_name == "urlscan":
        service_config["api_key"] = config.get("urlscan_api_key")
    elif service_name == "spur":
        service_config["api_key"] = config.get("spur_api_key")
    elif service_name == "validin":
        service_config["api_key"] = config.get("validin_api_key")
    
    return service_class(**service_config)


def query_service(service_name: str, observable: str, obs_type: str, config: Dict) -> Dict:
    """Query a single service for an observable."""
    try:
        service = get_service_instance(service_name, config)
        return service.query(observable, obs_type)
    except Exception as e:
        return {
            "service": service_name,
            "error": str(e),
            "status": "failed"
        }


def query_all_services(observable: str, obs_type: str, services: List[str], config: Dict) -> List[Dict]:
    """Query multiple services and return aggregated results."""
    results = []
    
    for service_name in services:
        result = query_service(service_name, observable, obs_type, config)
        results.append(result)
    
    return results


def print_table(results: List[Dict]):
    """Print results in table format."""
    print(f"\n{'Service':<20} | {'Status':<12} | {'Result':<15} | {'Details'}")
    print("-" * 80)
    
    for r in results:
        service = r.get("service", "unknown")
        status = r.get("status", "unknown")
        
        if "error" in r:
            result = "❌ Error"
            details = r["error"][:40]
        else:
            result = r.get("classification", "unknown")
            details = r.get("summary", "")[:40]
        
        print(f"{service:<20} | {status:<12} | {result:<15} | {details}")


def print_json(results: List[Dict]):
    """Print results as JSON."""
    print(json.dumps(results, indent=2))


def print_markdown(results: List[Dict], observable: str, obs_type: str):
    """Print results in markdown format."""
    print(f"# Threat Intel Report: {obs_type.upper()} = `{observable}`\n")
    
    print("## Summary\n")
    
    for r in results:
        service = r.get("service", "unknown").upper()
        print(f"### {service}\n")
        
        if "error" in r:
            print(f"- **Status:** ❌ Failed")
            print(f"- **Error:** {r['error']}")
        else:
            print(f"- **Status:** ✅ Success")
            print(f"- **Classification:** {r.get('classification', 'unknown')}")
            print(f"- **Summary:** {r.get('summary', 'N/A')}")
            
            if "data" in r:
                print("\n**Details:**")
                print(f"```json")
                print(json.dumps(r["data"], indent=2)[:500] + "...")
                print(f"```")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Query threat intelligence services for IOC enrichment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ip 8.8.8.8 --services virustotal,greynoise
  %(prog)s domain evil.com --services all
  %(prog)s hash a3b2c1d4 --services virustotal
  %(prog)s url http://example.com --services urlscan
        """
    )
    
    # Do not auto-launch interactive setup in agent or automation contexts.
    
    parser.add_argument("type", nargs='?', choices=["ip", "domain", "hash", "url", "setup"],
                        help="Type of observable to query (or 'setup' to configure)")
    parser.add_argument("observable", nargs="?", help="The IOC to query")
    parser.add_argument("--services", "-s", default="all",
                        help="Comma-separated list of services (default: all)")
    parser.add_argument("--format", "-f", choices=["table", "json", "markdown"],
                        default="table", help="Output format")
    parser.add_argument("--config", "-c", help="Path to config.json")
    parser.add_argument("--rate-limits", action="store_true",
                        help="Show rate limit status for all services")
    
    # Parse args
    args = parser.parse_args()
    
    # Handle rate-limits flag
    if args.rate_limits:
        get_rate_limit_status()
        return
    
    # Show a non-blocking first-run notice.
    if is_first_run() and args.type not in (None, "setup"):
        print("\n" + "=" * 60)
        print("🔧 Welcome to IONSEC Threat Intel!")
        print("=" * 60)
        print("\nNo API keys are configured yet.")
        print("Free services will work immediately.")
        print("To add premium services later, run: openclaw threat-intel setup")
        print("Or set environment variables as documented in README.md")
        print("=" * 60 + "\n")
    
    if args.type is None:
        parser.print_help()
        return

    # Load configuration
    config = load_config()
    if args.config:
        with open(args.config) as f:
            config.update(json.load(f))
    
    # Determine which services to query
    available_services = OBSERVABLE_SERVICES.get(args.type, [])
    
    if args.services == "all":
        services = available_services
    else:
        requested = [s.strip() for s in args.services.split(",")]
        services = [s for s in requested if s in available_services]
        if not services:
            print(f"Error: No valid services specified for {args.type}", file=sys.stderr)
            print(f"Available: {', '.join(available_services)}", file=sys.stderr)
            sys.exit(1)
    
    # Query services
    print(f"Querying {len(services)} service(s) for {args.type}: {args.observable}...\n")
    results = query_all_services(args.observable, args.type, services, config)
    
    # Output results
    if args.format == "table":
        print_table(results)
    elif args.format == "json":
        print_json(results)
    elif args.format == "markdown":
        print_markdown(results, args.observable, args.type)


if __name__ == "__main__":
    main()
