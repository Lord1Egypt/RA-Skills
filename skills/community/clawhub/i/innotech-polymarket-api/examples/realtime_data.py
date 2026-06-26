"""
Example: Real-time Data with WebSocket and Socket.IO

This example shows how to get real-time market data from Polymarket
using WebSocket and Socket.IO connections.

Author: Calvin Lam
"""

import json
import time

# =============================================================================
# Method 1: Native WebSocket (Recommended)
# =============================================================================

def websocket_example():
    """
    Connect to Polymarket using native WebSocket.
    
    This is the fastest and most reliable method for real-time data.
    Requires: pip install websocket-client
    """
    try:
        import websocket
    except ImportError:
        print("❌ websocket-client not installed")
        print("   Install with: pip install websocket-client")
        return
    
    market_id = "your_market_id_here"  # Replace with actual market ID
    
    def on_message(ws, message):
        """Handle incoming messages"""
        data = json.loads(message)
        print(f"📥 Received: {json.dumps(data, indent=2)}")
    
    def on_error(ws, error):
        """Handle errors"""
        print(f"❌ Error: {error}")
    
    def on_close(ws, close_status_code, close_msg):
        """Handle connection close"""
        print("🔌 Connection closed")
    
    def on_open(ws):
        """Handle connection open"""
        print("✅ Connected to Polymarket WebSocket")
        
        # Subscribe to market updates
        subscribe_msg = {
            "type": "subscribe",
            "market": market_id
        }
        ws.send(json.dumps(subscribe_msg))
        print(f"📡 Subscribed to market: {market_id}")
    
    # Create WebSocket connection
    ws_url = "wss://ws-subscriptions.polymarket.com"
    
    print("\n" + "="*80)
    print("Method 1: Native WebSocket")
    print("="*80)
    
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # Run for 30 seconds then close
    import threading
    def close_after_timeout():
        time.sleep(30)
        ws.close()
    
    threading.Thread(target=close_after_timeout, daemon=True).start()
    ws.run_forever()


# =============================================================================
# Method 2: Socket.IO (Good Fallback)
# =============================================================================

def socketio_example():
    """
    Connect to Polymarket using Socket.IO client.
    
    This is a good fallback if native WebSocket doesn't work.
    Requires: pip install python-socketio
    """
    try:
        import socketio
    except ImportError:
        print("❌ python-socketio not installed")
        print("   Install with: pip install python-socketio")
        return
    
    market_ids = ["market_id_1", "market_id_2"]  # Replace with actual IDs
    
    sio = socketio.Client()
    
    @sio.event
    def connect():
        """Handle connection"""
        print("✅ Connected via Socket.IO")
        
        # Subscribe to multiple markets
        sio.emit('subscribe', {'markets': market_ids})
        print(f"📡 Subscribed to {len(market_ids)} markets")
    
    @sio.event
    def price_change(data):
        """Handle price updates"""
        print(f"💰 Price Update: {data}")
    
    @sio.event
    def order_book_update(data):
        """Handle order book changes"""
        print(f"📊 Order Book Update: {data}")
    
    @sio.event
    def disconnect():
        """Handle disconnection"""
        print("🔌 Disconnected from Socket.IO")
    
    print("\n" + "="*80)
    print("Method 2: Socket.IO")
    print("="*80)
    
    try:
        sio.connect('wss://ws-subscriptions.polymarket.com')
        
        # Run for 30 seconds
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ Socket.IO Error: {e}")
    finally:
        sio.disconnect()


# =============================================================================
# Method 3: Async WebSocket (For Async Applications)
# =============================================================================

async def async_websocket_example():
    """
    Async WebSocket connection using websockets library.
    
    Best for applications already using asyncio.
    Requires: pip install websockets
    """
    try:
        import websockets
    except ImportError:
        print("❌ websockets not installed")
        print("   Install with: pip install websockets")
        return
    
    market_id = "your_market_id_here"
    ws_url = "wss://ws-subscriptions.polymarket.com"
    
    print("\n" + "="*80)
    print("Method 3: Async WebSocket")
    print("="*80)
    
    try:
        async with websockets.connect(ws_url) as ws:
            print("✅ Connected via Async WebSocket")
            
            # Subscribe
            subscribe_msg = {
                "type": "subscribe",
                "market": market_id
            }
            await ws.send(json.dumps(subscribe_msg))
            print(f"📡 Subscribed to market: {market_id}")
            
            # Listen for messages for 30 seconds
            start_time = time.time()
            while time.time() - start_time < 30:
                try:
                    message = await asyncio.wait_for(
                        ws.recv(),
                        timeout=5.0
                    )
                    data = json.loads(message)
                    print(f"📥 Received: {data}")
                except asyncio.TimeoutError:
                    continue
                    
    except Exception as e:
        print(f"❌ Async WebSocket Error: {e}")


# =============================================================================
# Common Events to Subscribe To
# =============================================================================

EVENT_TYPES = {
    "price_change": "Real-time price updates for outcomes",
    "order_book_update": "Changes to the order book",
    "trade": "New trade execution notifications",
    "market_update": "General market status changes"
}

def print_available_events():
    """Print available event types"""
    print("\n" + "="*80)
    print("Available Event Types")
    print("="*80)
    
    for event, description in EVENT_TYPES.items():
        print(f"  • {event}: {description}")


# =============================================================================
# Connection Best Practices
# =============================================================================

BEST_PRACTICES = """
Connection Best Practices:

1. ✅ Always implement reconnection logic
   - Networks can drop unexpectedly
   - Use exponential backoff

2. ✅ Handle multiple message types
   - Different events have different structures
   - Parse dynamically

3. ✅ Use connection pooling for multiple markets
   - Don't create new connection per market
   - Subscribe to multiple markets on one connection

4. ✅ Implement heartbeat/ping-pong
   - Detect dead connections early
   - Most WebSocket libraries handle this automatically

5. ✅ Rate limit subscriptions
   - Don't subscribe to thousands of markets instantly
   - Batch subscriptions if needed
"""


def print_best_practices():
    """Print connection best practices"""
    print("\n" + "="*80)
    print("Connection Best Practices")
    print("="*80)
    print(BEST_PRACTICES)


# =============================================================================
# Example with Reconnection Logic
# =============================================================================

class RobustWebSocket:
    """
    WebSocket client with automatic reconnection.
    
    This is a production-ready pattern for maintaining
    persistent WebSocket connections.
    """
    
    def __init__(self, url, market_ids):
        self.url = url
        self.market_ids = market_ids
        self.reconnect_delay = 1
        self.max_reconnect_delay = 60
    
    def connect(self):
        """Connect with auto-reconnect"""
        import websocket
        
        def on_open(ws):
            print("✅ Connected")
            self.reconnect_delay = 1  # Reset on successful connect
            
            # Subscribe to markets
            for market_id in self.market_ids:
                ws.send(json.dumps({
                    "type": "subscribe",
                    "market": market_id
                }))
        
        def on_message(ws, message):
            data = json.loads(message)
            self.handle_message(data)
        
        def on_error(ws, error):
            print(f"❌ Error: {error}")
        
        def on_close(ws, *args):
            print(f"🔌 Disconnected. Reconnecting in {self.reconnect_delay}s...")
            time.sleep(self.reconnect_delay)
            
            # Exponential backoff
            self.reconnect_delay = min(
                self.reconnect_delay * 2,
                self.max_reconnect_delay
            )
            
            self.connect()  # Reconnect
        
        ws = websocket.WebSocketApp(
            self.url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever()
    
    def handle_message(self, data):
        """Override this to handle messages"""
        print(f"📥 {data}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("POLYMARKET REAL-TIME DATA EXAMPLES")
    print("="*80)
    print("\nThis example demonstrates how to get real-time data from Polymarket")
    print("using different WebSocket connection methods.\n")
    
    # Show available events
    print_available_events()
    
    # Show best practices
    print_best_practices()
    
    print("\n" + "="*80)
    print("Running Examples (30 seconds each)")
    print("="*80)
    print("\n💡 Note: Replace 'your_market_id_here' with actual market IDs")
    print("   Market IDs can be found via the Gamma API or Polymarket website\n")
    
    # Run examples
    # Uncomment the method you want to try:
    
    # Method 1: Native WebSocket (recommended)
    # websocket_example()
    
    # Method 2: Socket.IO (fallback)
    # socketio_example()
    
    # Method 3: Async WebSocket
    # import asyncio
    # asyncio.run(async_websocket_example())
    
    print("\n✅ Examples ready! Uncomment the method you want to try.")
    print("="*80 + "\n")
