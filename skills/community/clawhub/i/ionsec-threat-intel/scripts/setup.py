#!/usr/bin/env python3
"""
Interactive setup for Threat Intel skill.
Configures API keys and saves to config.json.
"""

import json
import os
from pathlib import Path


def get_config_path() -> Path:
    """Get path to config file."""
    script_dir = Path(__file__).parent.parent
    config_path = script_dir / "config.json"
    return config_path


def load_existing_config() -> dict:
    """Load existing config if present."""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    """Save config to file."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"\n✅ Config saved to: {config_path}")


def prompt_api_key(name: str, description: str, existing: str = "") -> str:
    """Prompt user for an API key."""
    print(f"\n{name}")
    print("-" * len(name))
    print(description)
    
    if existing:
        print(f"Current: {'*' * 8}{existing[-4:] if len(existing) > 4 else ''}")
        print("Press Enter to keep existing, or type new key:")
    else:
        print("Enter API key (leave empty to skip):")
    
    value = input("> ").strip()
    return value if value else existing


def main():
    print("=" * 60)
    print("  Threat Intel - API Key Configuration")
    print("=" * 60)
    print("\nThis wizard will help you configure API keys for threat")
    print("intelligence services. Keys are stored locally in config.json.")
    print("\nFree services work without keys but have lower rate limits.")
    print("Get your keys at the URLs listed for each service.")
    
    config = load_existing_config()
    
    # Service definitions
    services = [
        {
            "key": "vt_api_key",
            "name": "VirusTotal",
            "desc": "Free tier: 500 requests/day\nGet key: https://www.virustotal.com/gui/my-apikey",
            "required": False
        },
        {
            "key": "greynoise_api_key",
            "name": "GreyNoise",
            "desc": "Community tier: 50 requests/day (optional)\nSign up: https://viz.greynoise.io/sign-up",
            "required": False
        },
        {
            "key": "shodan_api_key",
            "name": "Shodan",
            "desc": "Free: 100 queries/month\nGet key: https://account.shodan.io/",
            "required": False
        },
        {
            "key": "otx_api_key",
            "name": "AlienVault OTX",
            "desc": "Unlimited queries (registration required)\nGet key: https://otx.alienvault.com/settings",
            "required": False
        },
        {
            "key": "abuseipdb_api_key",
            "name": "AbuseIPDB",
            "desc": "Free: 1000 checks/month\nGet key: https://www.abuseipdb.com/account/api",
            "required": False
        },
        {
            "key": "urlscan_api_key",
            "name": "URLscan",
            "desc": "Optional - increases rate limits\nGet key: https://urlscan.io/user/signup",
            "required": False
        },
    ]
    
    for svc in services:
        existing = config.get(svc["key"], "")
        value = prompt_api_key(
            svc["name"],
            svc["desc"],
            existing
        )
        if value:
            config[svc["key"]] = value
    
    # Save configuration
    print("\n" + "=" * 60)
    print("  Configuration Summary")
    print("=" * 60)
    
    configured = sum(1 for k, v in config.items() if v)
    total = len(services)
    
    print(f"\nConfigured {configured}/{total} services.")
    
    save_config(config)
    
    print("\nEnvironment variables also work:")
    print("  export VT_API_KEY=your_key_here")
    print("  export GREYNOISE_API_KEY=your_key_here")
    print("  export SHODAN_API_KEY=your_key_here")
    print("  export OTX_API_KEY=your_key_here")
    print("  export ABUSEIPDB_API_KEY=your_key_here")
    print("  export URLSCAN_API_KEY=your_key_here")
    
    print("\n🎉 Setup complete! Try: openclaw threat-intel ip 8.8.8.8 --services all")


if __name__ == "__main__":
    main()
