"""
Example: Finding markets on Polymarket

This example shows different ways to find and filter markets.

Author: Calvin Lam
"""

import requests

def get_all_markets(limit=100):
    """Get all active markets"""
    response = requests.get(
        "https://gamma-api.polymarket.com/markets",
        params={"active": "true", "limit": limit}
    )
    return response.json()


def search_markets(keyword):
    """Search markets by keyword"""
    response = requests.get(
        "https://gamma-api.polymarket.com/markets",
        params={"_s": keyword}
    )
    return response.json()


def get_market_by_slug(slug):
    """Get market by URL slug"""
    response = requests.get(
        "https://gamma-api.polymarket.com/markets",
        params={"slug": slug}
    )
    markets = response.json()
    return markets[0] if markets else None


def filter_high_volume_markets(min_volume=100000):
    """Find markets with high trading volume"""
    markets = get_all_markets(limit=500)
    
    high_volume = []
    for market in markets:
        volume = float(market.get('volume', 0))
        if volume >= min_volume:
            high_volume.append({
                'question': market['question'],
                'volume': volume,
                'prices': market.get('outcomePrices', [])
            })
    
    # Sort by volume
    high_volume.sort(key=lambda x: x['volume'], reverse=True)
    return high_volume


def find_closing_soon_markets(hours=24):
    """Find markets closing within specified hours"""
    from datetime import datetime, timedelta
    
    markets = get_all_markets(limit=500)
    now = datetime.now()
    threshold = now + timedelta(hours=hours)
    
    closing_soon = []
    for market in markets:
        if 'expirationDate' in market:
            expiry = datetime.fromisoformat(market['expirationDate'].replace('Z', '+00:00'))
            if now < expiry <= threshold:
                closing_soon.append({
                    'question': market['question'],
                    'expires': market['expirationDate'],
                    'prices': market.get('outcomePrices', [])
                })
    
    return closing_soon


# Example usage
if __name__ == "__main__":
    print("="*80)
    print("1. Search Markets by Keyword")
    print("="*80)
    
    bitcoin_markets = search_markets("bitcoin")
    print(f"\nFound {len(bitcoin_markets)} Bitcoin markets:")
    for market in bitcoin_markets[:5]:
        print(f"- {market['question']}")
    
    print("\n" + "="*80)
    print("2. High Volume Markets")
    print("="*80)
    
    high_vol = filter_high_volume_markets(min_volume=500000)
    print(f"\nFound {len(high_vol)} markets with >$500K volume:")
    for market in high_vol[:5]:
        print(f"- {market['question']}: ${market['volume']:,.0f}")
    
    print("\n" + "="*80)
    print("3. Markets Closing Soon")
    print("="*80)
    
    closing = find_closing_soon_markets(hours=48)
    print(f"\nFound {len(closing)} markets closing in 48 hours:")
    for market in closing[:5]:
        print(f"- {market['question']}")
