"""
Example: How to connect to Polymarket APIs

This example shows basic connection methods to Polymarket.

Author: Calvin Lam
"""

import requests

# Method 1: Gamma API (Public, no auth required)
def get_all_markets():
    """Get all active markets"""
    response = requests.get(
        "https://gamma-api.polymarket.com/markets",
        params={"active": "true", "limit": 10}
    )
    return response.json()


# Method 2: Get specific market
def get_market_by_id(market_id):
    """Get market by ID"""
    response = requests.get(
        f"https://gamma-api.polymarket.com/markets/{market_id}"
    )
    return response.json()


# Method 3: Search markets
def search_markets(keyword):
    """Search markets by keyword"""
    response = requests.get(
        "https://gamma-api.polymarket.com/markets",
        params={"_s": keyword}
    )
    return response.json()


# Method 4: Get market prices
def get_market_prices(market_id):
    """Get current prices for a market"""
    response = requests.get(
        f"https://gamma-api.polymarket.com/markets/{market_id}/price"
    )
    return response.json()


# Example usage
if __name__ == "__main__":
    # Get some markets
    markets = get_all_markets()
    
    print("="*80)
    print(f"Found {len(markets)} active markets")
    print("="*80)
    
    for market in markets[:5]:
        print(f"\nQuestion: {market['question']}")
        print(f"ID: {market['id']}")
        print(f"Outcomes: {market['outcomes']}")
        print(f"Prices: {market.get('outcomePrices', [])}")
    
    # Search example
    print("\n" + "="*80)
    print("Searching for 'bitcoin' markets...")
    print("="*80)
    
    bitcoin_markets = search_markets("bitcoin")
    for market in bitcoin_markets[:3]:
        print(f"- {market['question']}")
