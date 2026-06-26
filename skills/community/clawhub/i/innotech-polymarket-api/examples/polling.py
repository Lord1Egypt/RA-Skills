"""
Example: Polling Methods for Polymarket Data

This example shows how to poll Polymarket APIs when WebSocket
is not available or not needed.

Polling is useful for:
- Simple scripts that don't need real-time updates
- Fallback when WebSocket connections fail
- Reduced complexity for basic use cases
- Batch processing of market data

Author: Calvin Lam
"""

import requests
import time
from datetime import datetime


# =============================================================================
# Basic Polling
# =============================================================================

def poll_market_prices(market_id: str, interval: int = 5):
    """
    Poll market prices at regular intervals.
    
    Args:
        market_id: The market ID to poll
        interval: Seconds between polls (minimum 5 recommended)
    
    Yields:
        dict: Price data for each poll
    """
    url = f"https://gamma-api.polymarket.com/markets/{market_id}/price"
    
    while True:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            yield {
                'timestamp': datetime.now().isoformat(),
                'prices': data.get('outcomePrices', []),
                'volume': data.get('volume', '0')
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Poll error: {e}")
        
        time.sleep(interval)


# =============================================================================
# Smart Polling with Change Detection
# =============================================================================

class SmartPoller:
    """
    Poll markets with change detection.
    
    Only yields data when prices actually change,
    reducing noise and processing overhead.
    """
    
    def __init__(self, market_id: str, interval: int = 5):
        self.market_id = market_id
        self.interval = interval
        self.last_prices = None
    
    def poll(self):
        """
        Poll for price changes.
        
        Yields:
            dict: Price data only when prices change
        """
        url = f"https://gamma-api.polymarket.com/markets/{self.market_id}/price"
        
        while True:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                current_prices = data.get('outcomePrices', [])
                
                # Only yield if prices changed
                if current_prices != self.last_prices:
                    self.last_prices = current_prices
                    
                    yield {
                        'timestamp': datetime.now().isoformat(),
                        'market_id': self.market_id,
                        'prices': current_prices,
                        'volume': data.get('volume', '0'),
                        'change_detected': True
                    }
                else:
                    # No change, but can still yield for monitoring
                    yield {
                        'timestamp': datetime.now().isoformat(),
                        'market_id': self.market_id,
                        'change_detected': False
                    }
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Poll error: {e}")
            
            time.sleep(self.interval)


# =============================================================================
# Exponential Backoff Polling
# =============================================================================

def poll_with_backoff(market_id: str, max_interval: int = 60):
    """
    Poll with exponential backoff on errors.
    
    Increases polling interval when errors occur,
    decreases when successful.
    
    Args:
        market_id: Market to poll
        max_interval: Maximum interval between polls
    """
    url = f"https://gamma-api.polymarket.com/markets/{market_id}/price"
    current_interval = 5
    consecutive_errors = 0
    
    while True:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Success - reset interval
            if consecutive_errors > 0:
                print(f"✅ Connection recovered")
            consecutive_errors = 0
            current_interval = 5
            
            yield {
                'timestamp': datetime.now().isoformat(),
                'prices': data.get('outcomePrices', []),
                'status': 'success'
            }
            
        except requests.exceptions.RequestException as e:
            consecutive_errors += 1
            
            # Exponential backoff
            current_interval = min(
                current_interval * 2,
                max_interval
            )
            
            print(f"❌ Error {consecutive_errors}: {e}")
            print(f"   Retrying in {current_interval}s...")
            
            yield {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'error',
                'next_retry': current_interval
            }
        
        time.sleep(current_interval)


# =============================================================================
# Multi-Market Polling
# =============================================================================

def poll_multiple_markets(market_ids: list, interval: int = 5):
    """
    Poll multiple markets efficiently.
    
    Uses a single request per cycle for all markets,
    rather than separate requests per market.
    
    Args:
        market_ids: List of market IDs to poll
        interval: Seconds between polling cycles
    """
    while True:
        results = {}
        
        for market_id in market_ids:
            try:
                response = requests.get(
                    f"https://gamma-api.polymarket.com/markets/{market_id}",
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                
                results[market_id] = {
                    'question': data.get('question', ''),
                    'prices': data.get('outcomePrices', []),
                    'volume': data.get('volume', '0')
                }
                
            except requests.exceptions.RequestException as e:
                results[market_id] = {'error': str(e)}
            
            # Small delay between requests to be polite
            time.sleep(0.1)
        
        yield {
            'timestamp': datetime.now().isoformat(),
            'markets': results
        }
        
        time.sleep(interval)


# =============================================================================
# Conditional Polling (If-Modified-Since)
# =============================================================================

def poll_with_caching(market_id: str, interval: int = 5):
    """
    Poll using HTTP caching headers.
    
    Uses If-Modified-Since header to avoid transferring
    data that hasn't changed.
    """
    url = f"https://gamma-api.polymarket.com/markets/{market_id}"
    last_modified = None
    
    while True:
        headers = {}
        if last_modified:
            headers['If-Modified-Since'] = last_modified
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 304:
                # Not modified
                yield {
                    'timestamp': datetime.now().isoformat(),
                    'status': 'not_modified'
                }
            else:
                response.raise_for_status()
                
                # Update last modified
                last_modified = response.headers.get('Last-Modified')
                
                data = response.json()
                yield {
                    'timestamp': datetime.now().isoformat(),
                    'data': data,
                    'status': 'modified'
                }
                
        except requests.exceptions.RequestException as e:
            yield {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'error'
            }
        
        time.sleep(interval)


# =============================================================================
# Example: Price Alert System with Polling
# =============================================================================

class PriceAlertPoller:
    """
    Poll-based price alert system.
    
    Monitors a market and triggers alerts when price
    crosses target thresholds.
    """
    
    def __init__(self, market_id: str, target_price: float, outcome_index: int = 0):
        """
        Initialize alert poller.
        
        Args:
            market_id: Market to monitor
            target_price: Target price (0.0 to 1.0)
            outcome_index: 0 for Yes, 1 for No
        """
        self.market_id = market_id
        self.target_price = target_price
        self.outcome_index = outcome_index
        self.triggered = False
    
    def monitor(self, check_above: bool = True, interval: int = 10):
        """
        Monitor for price alert.
        
        Args:
            check_above: If True, alert when price >= target.
                        If False, alert when price <= target.
            interval: Polling interval in seconds
        """
        print(f"\n🎯 Monitoring market: {self.market_id}")
        print(f"   Target: {'>=' if check_above else '<='} {self.target_price}")
        print(f"   Press Ctrl+C to stop\n")
        
        url = f"https://gamma-api.polymarket.com/markets/{self.market_id}/price"
        
        try:
            while not self.triggered:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                prices = data.get('outcomePrices', [])
                if len(prices) > self.outcome_index:
                    current_price = float(prices[self.outcome_index])
                    
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] Current: {current_price:.4f} | Target: {self.target_price}")
                    
                    # Check condition
                    if check_above:
                        if current_price >= self.target_price:
                            self.trigger_alert(current_price)
                    else:
                        if current_price <= self.target_price:
                            self.trigger_alert(current_price)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Monitoring stopped by user")
    
    def trigger_alert(self, current_price: float):
        """Trigger the price alert"""
        self.triggered = True
        
        print("\n" + "="*60)
        print("🚨 PRICE ALERT TRIGGERED!")
        print("="*60)
        print(f"Market: {self.market_id}")
        print(f"Current Price: {current_price}")
        print(f"Target Price: {self.target_price}")
        print(f"Time: {datetime.now().isoformat()}")
        print("="*60 + "\n")


# =============================================================================
# Polling Best Practices
# =============================================================================

POLLING_BEST_PRACTICES = """
Polling Best Practices:

1. ✅ Use reasonable intervals
   - Minimum 5 seconds between polls
   - Longer intervals for less critical data
   - Don't spam the API

2. ✅ Implement error handling
   - Use exponential backoff on errors
   - Don't retry immediately on failure
   - Log errors for debugging

3. ✅ Use caching when possible
   - If-Modified-Since headers
   - ETags if supported
   - Local caching of responses

4. ✅ Be respectful of rate limits
   - Gamma API: ~100 requests/minute
   - Don't exceed limits or you'll be blocked
   - Batch requests when possible

5. ✅ Monitor connection health
   - Track success/failure rates
   - Alert on sustained failures
   - Implement automatic recovery

6. ✅ Consider WebSocket instead
   - For real-time data, WebSocket is better
   - Polling is for fallback or simple scripts
   - WebSocket uses less bandwidth for frequent updates
"""


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("POLYMARKET POLLING EXAMPLES")
    print("="*80)
    print("\nPolling is useful when:")
    print("  • You don't need real-time updates")
    print("  • WebSocket connections aren't available")
    print("  • You want simpler code")
    print("  • You're doing batch processing")
    
    print("\n" + "="*80)
    print("Polling Best Practices")
    print("="*80)
    print(POLLING_BEST_PRACTICES)
    
    print("\n" + "="*80)
    print("Available Polling Methods")
    print("="*80)
    print("  1. Basic polling - poll_market_prices()")
    print("  2. Smart polling with change detection - SmartPoller")
    print("  3. Exponential backoff - poll_with_backoff()")
    print("  4. Multi-market polling - poll_multiple_markets()")
    print("  5. Cached polling - poll_with_caching()")
    print("  6. Price alerts - PriceAlertPoller")
    
    print("\n💡 Tip: Replace 'your_market_id_here' with actual market IDs")
    print("   Market IDs can be found via the Gamma API\n")
    
    # Example usage (uncomment to run):
    
    # Basic polling example
    # for data in poll_market_prices("your_market_id_here", interval=10):
    #     print(f"Prices: {data['prices']}")
    #     break  # Remove to continue polling
    
    # Price alert example
    # alert = PriceAlertPoller(
    #     market_id="your_market_id_here",
    #     target_price=0.50,
    #     outcome_index=0
    # )
    # alert.monitor(check_above=True, interval=10)
    
    print("✅ Examples ready! Uncomment the code you want to try.")
    print("="*80 + "\n")
