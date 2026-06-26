#!/usr/bin/env python3
"""
Nango Connection Tester
Validates API connections and tests basic operations.
"""

import os
import sys
import json
from pathlib import Path

def test_nango_connection():
    """Test basic Nango connectivity."""
    try:
        from nango import Nango
        
        # Check environment
        secret_key = os.environ.get("NANGO_SECRET_KEY")
        if not secret_key:
            print("ERROR: NANGO_SECRET_KEY not set")
            print("Set it with: export NANGO_SECRET_KEY=your-key")
            return False
        
        nango = Nango()
        
        # Test connection
        providers = nango.list_providers()
        print(f"✓ Connected to Nango")
        print(f"✓ {len(providers)} providers available")
        
        return True
        
    except ImportError:
        print("ERROR: nango package not installed")
        print("Install with: pip install nango")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def list_providers():
    """List all available providers."""
    try:
        from nango import Nango
        nango = Nango()
        
        providers = nango.list_providers()
        
        print("\n=== Available Providers ===")
        for p in providers[:20]:  # Show first 20
            name = p.get("name", p.get("provider", "?"))
            auth_type = p.get("auth_type", "?")
            print(f"  {name}: {auth_type}")
        
        if len(providers) > 20:
            print(f"\n  ... and {len(providers) - 20} more")
        
        print(f"\nTotal: {len(providers)} providers")
        return providers
        
    except Exception as e:
        print(f"ERROR: {e}")
        return []

def get_provider_info(provider: str):
    """Get detailed info for a provider."""
    try:
        from nango import Nango
        nango = Nango()
        
        info = nango.get_provider(provider)
        
        print(f"\n=== {provider} ===")
        print(f"Auth Type: {info.get('auth_type', '?')}")
        print(f"Scopes: {', '.join(info.get('scopes', []))}")
        
        print("\nAvailable Actions:")
        for action in info.get('actions', [])[:10]:
            name = action.get('name', '?')
            endpoint = action.get('endpoint', '?')
            method = action.get('method', '?')
            print(f"  {method} {endpoint} - {name}")
        
        return info
        
    except Exception as e:
        print(f"ERROR getting provider info: {e}")
        return None

def test_oauth_flow(provider: str, redirect_uri: str):
    """Generate OAuth URL for testing."""
    try:
        from nango import Nango
        nango = Nango()
        
        auth_url = nango.get_auth_url(
            provider=provider,
            redirect_uri=redirect_uri
        )
        
        print(f"\n=== OAuth Flow for {provider} ===")
        print(f"1. Visit this URL to authorize:")
        print(f"   {auth_url}")
        print(f"\n2. After authorization, you'll receive a code in the redirect URL")
        print(f"3. Use that code to create a connection")
        
        return auth_url
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Nango Connection Tester")
    parser.add_argument("--test", action="store_true", help="Test connection")
    parser.add_argument("--list", action="store_true", help="List providers")
    parser.add_argument("--info", type=str, help="Get info for provider")
    parser.add_argument("--oauth", nargs=2, metavar=("PROVIDER", "REDIRECT_URI"),
                       help="Generate OAuth URL")
    
    args = parser.parse_args()
    
    if args.test:
        success = test_nango_connection()
        sys.exit(0 if success else 1)
    
    elif args.list:
        list_providers()
    
    elif args.info:
        get_provider_info(args.info)
    
    elif args.oauth:
        provider, redirect_uri = args.oauth
        test_oauth_flow(provider, redirect_uri)
    
    else:
        # Default: run all tests
        print("=== Nango Connection Tester ===\n")
        
        if not test_nango_connection():
            sys.exit(1)
        
        print("\n")
        list_providers()
        
        print("\n=== Usage ===")
        print("  python test_connection.py --test         # Test connection")
        print("  python test_connection.py --list         # List all providers")
        print("  python test_connection.py --info github  # Get provider details")
        print("  python test_connection.py --oauth github https://your-app.com/callback")

if __name__ == "__main__":
    main()