---
name: mt5-trading-assistant
description: Comprehensive MetaTrader 5 (MT5) trading automation and monitoring skill. Use when users need to connect to MT5 trading platforms, execute trades, monitor accounts, analyze market data, or automate trading strategies. Triggers: MT5, MetaTrader 5, trading automation, forex trading, gold trading (XAUUSD), automated trading, trading bot, MT5 API, execute trade, buy/sell orders, close positions, stop loss/take profit, account monitoring, real-time quotes, K-line data.
---

# MT5 Trading Assistant

Complete automation suite for MetaTrader 5 trading platforms. Provides tools for account monitoring, trade execution, market analysis, and risk management.

## Quick Start

> **Important**: This skill contains example scripts with hardcoded credentials. You MUST modify the configuration before use.

### Prerequisites

1. **Python 3.7+** with `MetaTrader5` package:
   ```bash
   pip install MetaTrader5
   ```

2. **MT5 Desktop Client** running and logged into your account
3. **AutoTrading enabled** in MT5 (press F7 or click traffic light icon)

### Basic Usage Example

#### Check Account Status
```bash
python scripts/mt5_check.py
```

#### Execute Test Trade
```bash
# IMPORTANT: First modify scripts/mt5_buy.py with your account details
python scripts/mt5_buy.py 0.01
```

### Basic Usage

#### Check Account Status
```bash
python scripts/mt5_check.py
```

#### Get Market Snapshot
```bash
python scripts/mt5_snapshot.py
```

#### Execute Trades
```bash
# Buy 0.01 lots at market price
python scripts/mt5_buy.py 0.01

# Sell 0.02 lots at specified price 5040.00
python scripts/mt5_sell.py 0.02 5040.00

# Buy with stop loss and take profit
python scripts/mt5_buy.py 0.01 0 5030 5050
```

#### Close Positions
```bash
# Close all script-managed positions
python scripts/mt5_close_all.py

# Close all positions for a symbol
python scripts/mt5_close_all.py all

# Close specific position by ticket
python scripts/mt5_close_all.py 12345678
```

#### Test K-line Data
```bash
python scripts/test_mt5_kline.py
```

## Core Features

### 1. Account Monitoring
- Real-time balance and equity tracking
- Position monitoring with P&L calculation
- Margin and leverage information
- Connection status verification

### 2. Trade Execution
- Market orders (BUY/SELL)
- Position closing (full/partial)
- Stop loss and take profit management
- Order modification capabilities

### 3. Market Data
- Real-time bid/ask quotes
- Historical K-line data (M1, M5, H1, D1, etc.)
- Spread monitoring
- Price change calculations

### 4. Risk Management
- Position size calculation
- Stop loss automation
- Risk percentage limits
- Daily loss limits

## Script Reference

### `mt5_buy.py` - Buy Order Execution
```bash
python scripts/mt5_buy.py <volume> [price] [stop_loss] [take_profit]
```
**Parameters**:
- `volume`: Lot size (e.g., 0.01 for micro lot)
- `price`: Optional execution price (0 for market price)
- `stop_loss`: Optional stop loss price
- `take_profit`: Optional take profit price

**Examples**:
```bash
# Market buy 0.01 lot
python scripts/mt5_buy.py 0.01

# Limit buy at 5040.00 with SL 5030, TP 5050
python scripts/mt5_buy.py 0.05 5040.00 5030.00 5050.00
```

### `mt5_sell.py` - Sell Order Execution
```bash
python scripts/mt5_sell.py <volume> [price] [stop_loss] [take_profit]
```
**Usage**: Same as `mt5_buy.py` but for sell orders.

### `mt5_close_all.py` - Position Management
```bash
python scripts/mt5_close_all.py [command]
```
**Commands**:
- No argument: Close script-managed positions (magic 100001/100002)
- `all`: Close all positions for configured symbol
- `<ticket>`: Close specific position by ticket number

### `mt5_check.py` - Account Status
```bash
python scripts/mt5_check.py
```
**Output**: Account information, positions, market data, system status.

### `mt5_snapshot.py` - Market Snapshot
```bash
python scripts/mt5_snapshot.py
```
**Output**: Concise account and market status with trading commands.

### `test_mt5_kline.py` - Data Validation
```bash
python scripts/test_mt5_kline.py
```
**Purpose**: Test MT5 connection and data retrieval capabilities.

## Configuration - MUST MODIFY BEFORE USE

⚠️ **SECURITY WARNING**: The example scripts contain hardcoded demo account credentials. You MUST modify these before using with your real account.

### Configuration Options

#### Option 1: Direct Script Modification (Quick)
Edit the configuration section in each script file:

```python
# In scripts/mt5_buy.py, scripts/mt5_sell.py, etc.
ACCOUNT_CONFIG = {
    "login": YOUR_ACCOUNT_NUMBER,      # CHANGE THIS
    "password": "YOUR_PASSWORD",       # CHANGE THIS  
    "server": "YOUR_SERVER_NAME",      # CHANGE THIS
    "symbol": "YOUR_SYMBOL",           # e.g., "XAUUSD" or "XAUUSDm"
}
```

#### Option 2: Configuration File (Recommended)
1. Create `config.py` from template:
   ```bash
   cp references/config_template.py config.py
   ```

2. Edit `config.py`:
   ```python
   MT5_CONFIG = {
       "login": 12345678,              # YOUR MT5 account number
       "password": "your_password",    # YOUR MT5 password
       "server": "YourServer",         # YOUR MT5 server
       "symbol": "XAUUSD",             # Trading symbol
   }
   ```

3. Uncomment import lines in scripts:
   ```python
   # Uncomment these lines in each script:
   try:
       from config import MT5_CONFIG
       ACCOUNT_CONFIG.update(MT5_CONFIG)
   except ImportError:
       print("NOTE: config.py not found, using default configuration")
   ```

### Broker-Specific Settings

#### Exness
```python
MT5_CONFIG = {
    "login": 277528870,
    "password": "your_password",
    "server": "Exness-MT5Trial5",  # Demo server
    "symbol": "XAUUSDm",           # Gold with 'm' suffix
}
```

#### IC Markets
```python
MT5_CONFIG = {
    "login": 12345678,
    "password": "your_password", 
    "server": "ICMarkets-MT5",
    "symbol": "XAUUSD",            # Standard symbol
}
```

## Common Issues & Solutions

### Connection Problems
**Error**: `Initialize failed` or `Login failed`
**Solution**:
1. Ensure MT5 desktop client is running and logged in
2. Verify account credentials in config.py
3. Check server name matches MT5 client
4. Enable AutoTrading in MT5 (F7 key)

### Trading Issues
**Error**: `AutoTrading disabled by client`
**Solution**: Click the AutoTrading button (traffic light) in MT5 toolbar

**Error**: `Invalid symbol`
**Solution**: Check symbol name in MT5 client, note broker-specific suffixes

### Performance Issues
**Slow execution**: Reduce refresh intervals, close unused charts
**Connection drops**: Check internet stability, restart MT5 client

## Advanced Usage

### Custom Strategies
Create strategy scripts by importing MT5 functions:

```python
import MetaTrader5 as mt5
from config import MT5_CONFIG

def moving_average_strategy():
    """Simple moving average crossover strategy"""
    # Initialize MT5
    mt5.initialize()
    mt5.login(MT5_CONFIG["login"], MT5_CONFIG["password"], server=MT5_CONFIG["server"])
    
    # Get historical data
    rates = mt5.copy_rates_from(MT5_CONFIG["symbol"], mt5.TIMEFRAME_H1, datetime.now(), 100)
    
    # Calculate indicators
    # ... strategy logic ...
    
    # Execute trades
    # ... order execution ...
    
    mt5.shutdown()
```

### Risk Management Integration
```python
from config import MT5_CONFIG

def calculate_position_size(risk_percent=0.02, stop_loss_pips=20):
    """Calculate position size based on risk"""
    account = mt5.account_info()
    risk_amount = account.balance * risk_percent
    
    # Get point value
    symbol_info = mt5.symbol_info(MT5_CONFIG["symbol"])
    point_value = symbol_info.trade_tick_value
    
    # Calculate lot size
    risk_per_pip = risk_amount / stop_loss_pips
    lot_size = risk_per_pip / point_value
    
    return min(lot_size, MT5_CONFIG.get("max_lot_size", 1.0))
```

### Monitoring Dashboard
Create a simple monitoring script:

```python
#!/usr/bin/env python3
"""
MT5 Trading Dashboard
Refreshes every 10 seconds with account status
"""

import time
from datetime import datetime
import MetaTrader5 as mt5
from config import MT5_CONFIG

def dashboard():
    while True:
        # Clear screen
        print("\n" * 50)
        
        # Get current time
        print(f"MT5 Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Get account data
        mt5.initialize()
        mt5.login(MT5_CONFIG["login"], MT5_CONFIG["password"], server=MT5_CONFIG["server"])
        
        # Display data
        account = mt5.account_info()
        if account:
            print(f"Account: {account.login} | Equity: ${account.equity:.2f}")
            print(f"Balance: ${account.balance:.2f} | Margin: ${account.margin:.2f}")
        
        # Get positions
        positions = mt5.positions_get(symbol=MT5_CONFIG["symbol"])
        if positions:
            print(f"\nPositions: {len(positions)}")
            for pos in positions:
                pnl = "+" if pos.profit > 0 else ""
                print(f"  {pos.ticket}: {pos.symbol} {pos.volume} lots | P&L: {pnl}${pos.profit:.2f}")
        
        mt5.shutdown()
        
        print("\n" + "=" * 60)
        print("Next update in 10 seconds (Ctrl+C to stop)")
        
        time.sleep(10)

if __name__ == "__main__":
    try:
        dashboard()
    except KeyboardInterrupt:
        print("\nDashboard stopped")
```

## Security Best Practices

1. **Never hardcode passwords** - Use config.py or environment variables
2. **Use environment variables for production**:
   ```python
   import os
   MT5_CONFIG = {
       "login": os.getenv("MT5_LOGIN"),
       "password": os.getenv("MT5_PASSWORD"),
       "server": os.getenv("MT5_SERVER"),
   }
   ```
3. **Set file permissions**: `chmod 600 config.py`
4. **Add to .gitignore**: `echo "config.py" >> .gitignore`
5. **Regular password rotation**: Change passwords every 30-90 days

## Resources

### Reference Files
- `references/config_template.py` - Configuration template
- `references/setup_guide.md` - Complete setup instructions

### External Resources
- [MetaTrader5 Python Documentation](https://www.mql5.com/en/docs/integration/python_metatrader5)
- [MT5 API Reference](https://www.mql5.com/en/docs/constants/structures)
- [Exness API Guide](https://exness.com/developers/)
- [IC Markets API](https://www.icmarkets.com/development-api/)

## Support

For issues:
1. Check `references/setup_guide.md` for troubleshooting
2. Verify MT5 client is running with AutoTrading enabled
3. Test connection with `python scripts/test_mt5_kline.py`
4. Check account credentials in config.py

Common solutions:
- Restart MT5 client
- Re-enable AutoTrading (F7)
- Verify internet connection
- Check broker server status