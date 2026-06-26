"""
Example: Accessing Order Book Data on Polymarket

This example shows how to get and analyze order book data
from Polymarket markets.

Order books show:
- Current bids (buy orders)
- Current asks (sell orders)
- Market depth and liquidity
- Price spread

Author: Calvin Lam
"""

import requests
from typing import Dict, List, Optional


# =============================================================================
# Basic Order Book Access
# =============================================================================

def get_orderbook(market_id: str) -> Optional[Dict]:
    """
    Get order book for a market.
    
    Args:
        market_id: The market ID
    
    Returns:
        Order book data or None if error
    """
    url = f"https://data-api.polymarket.com/orderbook/{market_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching orderbook: {e}")
        return None


def get_orderbook_simple(market_id: str) -> Dict:
    """
    Get simplified order book with just bids and asks.
    
    Args:
        market_id: The market ID
    
    Returns:
        Dict with 'bids' and 'asks' lists
    """
    data = get_orderbook(market_id)
    
    if not data:
        return {'bids': [], 'asks': []}
    
    return {
        'bids': data.get('bids', []),
        'asks': data.get('asks', [])
    }


# =============================================================================
# Order Book Analysis
# =============================================================================

def analyze_orderbook(orderbook: Dict) -> Dict:
    """
    Analyze order book and return key metrics.
    
    Args:
        orderbook: Order book data
    
    Returns:
        Dict with analysis metrics
    """
    bids = orderbook.get('bids', [])
    asks = orderbook.get('asks', [])
    
    if not bids or not asks:
        return {
            'error': 'Empty bids or asks',
            'bid_count': 0,
            'ask_count': 0
        }
    
    # Calculate totals
    total_bid_volume = sum(float(bid.get('size', 0)) for bid in bids)
    total_ask_volume = sum(float(ask.get('size', 0)) for ask in asks)
    
    # Best prices
    best_bid = float(bids[0].get('price', 0)) if bids else 0
    best_ask = float(asks[0].get('price', 0)) if asks else 0
    
    # Spread
    spread = best_ask - best_bid
    spread_pct = (spread / best_ask * 100) if best_ask > 0 else 0
    
    # Mid price
    mid_price = (best_bid + best_ask) / 2 if best_bid and best_ask else 0
    
    # Imbalance
    total_volume = total_bid_volume + total_ask_volume
    bid_imbalance = (total_bid_volume / total_volume * 100) if total_volume > 0 else 50
    
    return {
        'bid_count': len(bids),
        'ask_count': len(asks),
        'total_bid_volume': total_bid_volume,
        'total_ask_volume': total_ask_volume,
        'best_bid': best_bid,
        'best_ask': best_ask,
        'spread': spread,
        'spread_pct': spread_pct,
        'mid_price': mid_price,
        'bid_imbalance': bid_imbalance
    }


def print_orderbook_summary(market_id: str):
    """
    Print a formatted summary of an order book.
    
    Args:
        market_id: Market to analyze
    """
    print(f"\n{'='*70}")
    print(f"ORDER BOOK: {market_id}")
    print(f"{'='*70}")
    
    orderbook = get_orderbook(market_id)
    
    if not orderbook:
        print("❌ Could not fetch order book")
        return
    
    analysis = analyze_orderbook(orderbook)
    
    if 'error' in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Orders: {analysis['bid_count']} bids | {analysis['ask_count']} asks")
    print(f"   Volume: {analysis['total_bid_volume']:.0f} bid | {analysis['total_ask_volume']:.0f} ask")
    print(f"\n💰 Prices:")
    print(f"   Best Bid: {analysis['best_bid']:.4f}")
    print(f"   Best Ask: {analysis['best_ask']:.4f}")
    print(f"   Spread:   {analysis['spread']:.4f} ({analysis['spread_pct']:.2f}%)")
    print(f"   Mid:      {analysis['mid_price']:.4f}")
    print(f"\n⚖️ Imbalance:")
    print(f"   Bid side: {analysis['bid_imbalance']:.1f}%")
    print(f"   Ask side: {100 - analysis['bid_imbalance']:.1f}%")
    
    # Interpretation
    if analysis['bid_imbalance'] > 60:
        print(f"   → Bullish pressure (more buyers)")
    elif analysis['bid_imbalance'] < 40:
        print(f"   → Bearish pressure (more sellers)")
    else:
        print(f"   → Balanced market")
    
    print(f"{'='*70}\n")


# =============================================================================
# Order Book Depth Visualization
# =============================================================================

def visualize_depth(orderbook: Dict, levels: int = 5):
    """
    Print a simple text visualization of order book depth.
    
    Args:
        orderbook: Order book data
        levels: Number of price levels to show
    """
    bids = orderbook.get('bids', [])[:levels]
    asks = orderbook.get('asks', [])[:levels]
    
    print(f"\n{'='*70}")
    print("ORDER BOOK DEPTH")
    print(f"{'='*70}")
    print(f"{'ASKS (Sell)':^35}|{'BIDS (Buy)':^35}")
    print(f"{'-'*70}")
    
    # Print asks in reverse order (highest at top)
    for ask in reversed(asks):
        price = float(ask.get('price', 0))
        size = float(ask.get('size', 0))
        bar = '█' * int(size / 100)
        print(f"{price:>10.4f} | {size:>10.0f} {bar:<13}|")
    
    print(f"{'-'*70}")
    
    # Print bids (highest at top)
    for bid in bids:
        price = float(bid.get('price', 0))
        size = float(bid.get('size', 0))
        bar = '█' * int(size / 100)
        print(f"{' '*35}| {bar:>13} {size:<10.0f} | {price:<10.4f}")
    
    print(f"{'='*70}\n")


# =============================================================================
# Liquidity Analysis
# =============================================================================

def check_liquidity(market_id: str, min_volume: float = 10000) -> Dict:
    """
    Check if a market has sufficient liquidity.
    
    Args:
        market_id: Market to check
        min_volume: Minimum total volume required
    
    Returns:
        Dict with liquidity analysis
    """
    orderbook = get_orderbook(market_id)
    
    if not orderbook:
        return {
            'sufficient': False,
            'reason': 'Could not fetch order book'
        }
    
    analysis = analyze_orderbook(orderbook)
    
    total_liquidity = analysis['total_bid_volume'] + analysis['total_ask_volume']
    sufficient = total_liquidity >= min_volume
    
    return {
        'sufficient': sufficient,
        'total_liquidity': total_liquidity,
        'min_required': min_volume,
        'bid_volume': analysis['total_bid_volume'],
        'ask_volume': analysis['total_ask_volume'],
        'spread': analysis['spread'],
        'spread_pct': analysis['spread_pct']
    }


# =============================================================================
# Price Impact Calculator
# =============================================================================

def calculate_price_impact(market_id: str, order_size: float, side: str = 'buy') -> Dict:
    """
    Calculate the price impact of an order.
    
    Args:
        market_id: Market ID
        order_size: Size of order in dollars
        side: 'buy' or 'sell'
    
    Returns:
        Dict with impact analysis
    """
    orderbook = get_orderbook(market_id)
    
    if not orderbook:
        return {'error': 'Could not fetch order book'}
    
    # Use asks for buys, bids for sells
    orders = orderbook.get('asks' if side == 'buy' else 'bids', [])
    
    if not orders:
        return {'error': 'No orders available'}
    
    remaining_size = order_size
    total_cost = 0
    weighted_price = 0
    levels_used = 0
    
    for order in orders:
        price = float(order.get('price', 0))
        size = float(order.get('size', 0))
        cost_at_level = price * size
        
        if remaining_size <= size:
            # Order fits in this level
            total_cost += price * remaining_size
            weighted_price = total_cost / order_size
            levels_used += 1
            break
        else:
            # Use entire level
            total_cost += cost_at_level
            remaining_size -= size
            levels_used += 1
    
    best_price = float(orders[0].get('price', 0))
    worst_price = price
    price_impact = abs(worst_price - best_price) / best_price * 100
    
    return {
        'order_size': order_size,
        'side': side,
        'best_price': best_price,
        'worst_price': worst_price,
        'weighted_price': weighted_price,
        'price_impact_pct': price_impact,
        'levels_used': levels_used,
        'total_cost': total_cost
    }


# =============================================================================
# Order Book Monitoring
# =============================================================================

def monitor_orderbook(market_id: str, interval: int = 5, duration: int = 60):
    """
    Monitor order book changes over time.
    
    Args:
        market_id: Market to monitor
        interval: Seconds between checks
        duration: Total monitoring duration in seconds
    """
    import time
    
    print(f"\n{'='*70}")
    print(f"MONITORING ORDER BOOK: {market_id}")
    print(f"Interval: {interval}s | Duration: {duration}s")
    print(f"{'='*70}\n")
    
    iterations = duration // interval
    previous_analysis = None
    
    for i in range(iterations):
        orderbook = get_orderbook(market_id)
        
        if orderbook:
            analysis = analyze_orderbook(orderbook)
            
            # Calculate changes
            if previous_analysis:
                bid_change = analysis['total_bid_volume'] - previous_analysis['total_bid_volume']
                ask_change = analysis['total_ask_volume'] - previous_analysis['total_ask_volume']
                spread_change = analysis['spread'] - previous_analysis['spread']
            else:
                bid_change = 0
                ask_change = 0
                spread_change = 0
            
            print(f"[{i+1}/{iterations}] "
                  f"Spread: {analysis['spread']:.4f} ({spread_change:+.4f}) | "
                  f"Bids: {analysis['total_bid_volume']:.0f} ({bid_change:+.0f}) | "
                  f"Asks: {analysis['total_ask_volume']:.0f} ({ask_change:+.0f})")
            
            previous_analysis = analysis
        else:
            print(f"[{i+1}/{iterations}] ❌ Error fetching order book")
        
        time.sleep(interval)
    
    print(f"\n{'='*70}")
    print("MONITORING COMPLETE")
    print(f"{'='*70}\n")


# =============================================================================
# Example Usage
# =============================================================================

def example_basic():
    """Basic order book example"""
    print("\n" + "="*70)
    print("Example 1: Basic Order Book Access")
    print("="*70)
    
    market_id = "your_market_id_here"  # Replace with actual market ID
    
    # Get order book
    orderbook = get_orderbook(market_id)
    
    if orderbook:
        print(f"\n✅ Order book fetched successfully")
        print(f"   Bids: {len(orderbook.get('bids', []))}")
        print(f"   Asks: {len(orderbook.get('asks', []))}")


def example_analysis():
    """Order book analysis example"""
    print("\n" + "="*70)
    print("Example 2: Order Book Analysis")
    print("="*70)
    
    market_id = "your_market_id_here"  # Replace with actual market ID
    
    # Print full summary
    print_orderbook_summary(market_id)


def example_liquidity():
    """Liquidity check example"""
    print("\n" + "="*70)
    print("Example 3: Liquidity Check")
    print("="*70)
    
    market_id = "your_market_id_here"  # Replace with actual market ID
    
    liquidity = check_liquidity(market_id, min_volume=10000)
    
    print(f"\nMarket: {market_id}")
    print(f"Sufficient Liquidity: {'✅ Yes' if liquidity.get('sufficient') else '❌ No'}")
    print(f"Total Liquidity: ${liquidity.get('total_liquidity', 0):,.0f}")
    print(f"Spread: {liquidity.get('spread', 0):.4f} ({liquidity.get('spread_pct', 0):.2f}%)")


def example_impact():
    """Price impact example"""
    print("\n" + "="*70)
    print("Example 4: Price Impact Calculator")
    print("="*70)
    
    market_id = "your_market_id_here"  # Replace with actual market ID
    order_size = 1000  # $1000 order
    
    impact = calculate_price_impact(market_id, order_size, side='buy')
    
    if 'error' not in impact:
        print(f"\nOrder: ${order_size} BUY")
        print(f"Best Price: {impact['best_price']:.4f}")
        print(f"Worst Price: {impact['worst_price']:.4f}")
        print(f"Price Impact: {impact['price_impact_pct']:.2f}%")
        print(f"Levels Used: {impact['levels_used']}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("POLYMARKET ORDER BOOK EXAMPLES")
    print("="*70)
    print("\nThis example shows how to access and analyze order book data.")
    print("\n💡 Tip: Replace 'your_market_id_here' with actual market IDs")
    print("   Market IDs can be found via the Gamma API or Polymarket website")
    
    print("\n" + "="*70)
    print("Available Functions")
    print("="*70)
    print("  • get_orderbook(market_id) - Get raw order book")
    print("  • analyze_orderbook(orderbook) - Analyze metrics")
    print("  • print_orderbook_summary(market_id) - Formatted summary")
    print("  • visualize_depth(orderbook) - Text visualization")
    print("  • check_liquidity(market_id) - Liquidity analysis")
    print("  • calculate_price_impact(market_id, size) - Impact calculator")
    print("  • monitor_orderbook(market_id) - Live monitoring")
    
    # Uncomment to run examples:
    # example_basic()
    # example_analysis()
    # example_liquidity()
    # example_impact()
    
    print("\n✅ Examples ready! Uncomment the code you want to try.")
    print("="*70 + "\n")
