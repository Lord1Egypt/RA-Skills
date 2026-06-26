#!/usr/bin/env python3
"""
Basic usage example for OlaXBT Nexus Data API client.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for local testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.olaxbt_nexus_data import NexusClient


def main():
    """Main demonstration function."""
    print("=== OlaXBT Nexus Data API Basic Usage Example ===\n")
    
    # Check environment variable (obtain JWT via Nexus auth flow — see skills/nexus/SKILL.md)
    jwt = os.getenv("NEXUS_JWT")
    if not jwt or not jwt.strip():
        print("❌ Error: NEXUS_JWT not set.")
        print("Obtain a JWT using the Nexus auth flow (see https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md), then:")
        print('export NEXUS_JWT="<your-jwt>"')
        return
    
    print("Using NEXUS_JWT from environment.")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Initialize client
        print("1. Initializing Nexus client...")
        client = NexusClient()
        print("   ✅ Client initialized\n")
        
        # Authenticate
        print("2. Authenticating with API...")
        jwt_token = client.authenticate()
        print(f"   ✅ Authentication successful")
        print(f"   JWT Token: {jwt_token[:50]}...\n")
        
        # Get credits balance
        print("3. Checking credits balance...")
        credits = client.get_credits_balance()
        print(f"   ✅ Credits: {credits.get('balance', 0)}")
        print(f"   Expires: {credits.get('expires_at', 'N/A')}\n")
        
        # Get latest news
        print("4. Getting latest cryptocurrency news...")
        news = client.news.get_latest(limit=5)
        print(f"   ✅ Retrieved {len(news)} news items")
        
        for i, item in enumerate(news[:3], 1):
            title = item.get('title', 'No title')[:60]
            print(f"   {i}. {title}...")
        print()
        
        # Get market overview
        print("5. Getting market overview...")
        market = client.market.get_overview()
        total_market_cap = market.get('global_metrics', {}).get('total_market_cap_usd', 0)
        print(f"   ✅ Total Market Cap: ${total_market_cap:,.0f}")
        
        # Get KOL heatmap for Bitcoin
        print("6. Getting KOL heatmap for BTC...")
        kol_data = client.kol.get_heatmap(symbol="BTC", limit=5)
        print(f"   ✅ Retrieved {len(kol_data)} KOL entries")
        
        # Health check
        print("7. Performing health check...")
        health = client.health_check()
        print(f"   ✅ API Status: {'Healthy' if health else 'Unhealthy'}\n")
        
        # Get metrics
        print("8. Request metrics:")
        metrics = client.api_client.get_metrics()
        print(f"   Total Requests: {metrics['total_requests']}")
        print(f"   Success Rate: {metrics['success_rate']}")
        print(f"   Avg Response Time: {metrics['average_response_time']}")
        print(f"   Rate Limit Remaining: {metrics['rate_limit_remaining']}/{metrics['rate_limit_total']}\n")
        
        print("=== Example completed successfully ===")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure NEXUS_JWT is set (obtain via Nexus auth flow)")
        print("2. Ensure you have sufficient credits")
        print("3. Verify network connectivity")
        print("4. Check API status at https://olaxbt.xyz")


if __name__ == "__main__":
    main()