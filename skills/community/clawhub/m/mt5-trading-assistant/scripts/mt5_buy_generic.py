#!/usr/bin/env python3
"""
Generic MT5 Buy Order Script

This script demonstrates how to execute buy orders using configuration.
Users should copy this script and modify it for their specific needs.
"""

import MetaTrader5 as mt5
import sys
import time
from datetime import datetime

def buy_order(volume=0.01, price=None, sl=None, tp=None, config=None):
    """
    Execute a buy order with configurable parameters
    
    Args:
        volume: Lot size (e.g., 0.01)
        price: Execution price (None/0 for market price)
        sl: Stop loss price (optional)
        tp: Take profit price (optional)
        config: Dictionary with MT5 configuration
    """
    if config is None:
        # Default configuration - USER MUST MODIFY THIS
        config = {
            "login": 12345678,              # CHANGE: Your MT5 account number
            "password": "your_password",    # CHANGE: Your MT5 password
            "server": "YourServer",         # CHANGE: Your MT5 server
            "symbol": "XAUUSD",             # CHANGE: Your trading symbol
            "deviation": 20,                # Price deviation in points
            "magic": 100001,                # Order magic number
            "comment": "Buy order",
        }
    
    symbol = config["symbol"]
    
    # Initialize MT5
    if not mt5.initialize():
        print("ERROR: MT5 initialization failed")
        return False
    
    # Login
    if not mt5.login(config["login"], config["password"], server=config["server"]):
        print("ERROR: Login failed")
        print(f"  Account: {config['login']}")
        print(f"  Server: {config['server']}")
        mt5.shutdown()
        return False
    
    # Select symbol
    if not mt5.symbol_select(symbol, True):
        print(f"ERROR: Cannot select symbol {symbol}")
        mt5.shutdown()
        return False
    
    # Get current price
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print(f"ERROR: Cannot get tick data for {symbol}")
        mt5.shutdown()
        return False
    
    # Use specified price or market price
    if price is None or price <= 0:
        price = tick.ask  # Buy at ask price
    
    print(f"Buy {symbol} {volume} lots")
    print(f"Current ask: {tick.ask:.3f}")
    print(f"Execution price: {price:.3f}")
    
    if sl:
        print(f"Stop loss: {sl:.3f}")
    if tp:
        print(f"Take profit: {tp:.3f}")
    
    # Build order request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": config.get("deviation", 20),
        "magic": config.get("magic", 100001),
        "comment": config.get("comment", f"Buy {volume} lots"),
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    # Add stop loss and take profit
    if sl:
        request["sl"] = sl
    if tp:
        request["tp"] = tp
    
    # Send order
    result = mt5.order_send(request)
    
    # Check result
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"SUCCESS: Buy order executed")
        print(f"  Order ticket: {result.order}")
        print(f"  Execution price: {result.price:.3f}")
        print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Wait and get position details
        time.sleep(1)
        positions = mt5.positions_get(ticket=result.order)
        if positions:
            pos = positions[0]
            print(f"  Position info:")
            print(f"    Open price: {pos.price_open:.3f}")
            print(f"    Current price: {pos.price_current:.3f}")
            print(f"    Profit/Loss: ${pos.profit:.2f}")
    else:
        print(f"FAILED: Buy order rejected")
        print(f"  Error code: {result.retcode}")
        print(f"  Description: {result.comment}")
    
    # Close connection
    mt5.shutdown()
    return result.retcode == mt5.TRADE_RETCODE_DONE

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python mt5_buy_generic.py <volume> [price] [stop_loss] [take_profit]")
        print("Examples:")
        print("  python mt5_buy_generic.py 0.01                  # Market buy 0.01 lots")
        print("  python mt5_buy_generic.py 0.05 5040.00         # Buy at 5040.00")
        print("  python mt5_buy_generic.py 0.03 0 5030 5050    # Market buy with SL/TP")
        print("  python mt5_buy_generic.py 0.02 5045 5035 5060 # Limit buy with SL/TP")
        print("\nIMPORTANT: Modify the config dictionary in buy_order() function")
        return
    
    try:
        # Parse arguments
        volume = float(sys.argv[1])
        
        price = None
        if len(sys.argv) > 2:
            price_arg = float(sys.argv[2])
            if price_arg > 0:
                price = price_arg
        
        sl = None
        if len(sys.argv) > 3:
            sl_arg = float(sys.argv[3])
            if sl_arg > 0:
                sl = sl_arg
        
        tp = None
        if len(sys.argv) > 4:
            tp_arg = float(sys.argv[4])
            if tp_arg > 0:
                tp = tp_arg
        
        # Execute buy
        success = buy_order(volume, price, sl, tp)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except ValueError as e:
        print(f"Parameter error: {e}")
        print("Please ensure parameters are numeric")
        sys.exit(1)
    except Exception as e:
        print(f"Execution error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()