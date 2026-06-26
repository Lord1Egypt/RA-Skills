---
name: openalgo-executor
description: |
  Skill to interact with the OpenAlgo API for trading operations.
  Allows placing market/limit orders, retrieving current positions, and fetching symbol quotes.
  Supports connecting to OpenAlgo via a specified URL (defaulting to http://localhost:5000 or ngrok URL).

  Use when you need to perform trading actions or query market/position data via the OpenAlgo API.

  Supported commands:
  - Order placement: buy/sell market or limit orders.
  - Position retrieval: get current open positions.
  - Quote retrieval: get real-time price quotes for symbols.

  Example Usage:
  - Place a market buy order for 10 SOL: `openalgo-executor.run_command("order --symbol SOLUSD --action buy --quantity 10")`
  - Place a limit sell order for 5 BTC at $50000: `openalgo-executor.run_command("order --symbol BTCUSD --action sell --quantity 5 --type limit --price 50000")`
  - Get current positions: `openalgo-executor.run_command("positions")`
  - Get quote for ETHUSD: `openalgo-executor.run_command("quote --symbol ETHUSD")`
  - Use a specific OpenAlgo URL: `openalgo-executor.run_command("order --symbol SOLUSD --action buy --quantity 10 --url http://your-ngrok-url.io")`
  
  Requires: openalgo_client.py script in scripts/ directory.
---

# OpenAlgo Executor Skill

This skill provides an interface to the OpenAlgo trading platform.

## Capabilities

*   Place Market/Limit Orders
*   Retrieve Current Positions
*   Obtain Symbol Quotes

## Configuration

The skill uses a Python client script (`scripts/openalgo_client.py`) to interact with the OpenAlgo API. The default API endpoint is `http://localhost:5000`. If your OpenAlgo service is accessible via a different URL or an ngrok tunnel, you can specify it using the `--url` argument when running commands.

## Usage

To use this skill, you can execute commands via the `run_command` function, passing the desired arguments for the `openalgo_client.py` script.

### Placing Orders

**Market Order:**
To place a market order, specify the symbol, action (buy/sell), and quantity.

*Example:* Place a market buy order for 10 SOL:
```bash
openalgo-executor.run_command("order --symbol SOLUSD --action buy --quantity 10")
```

**Limit Order:**
To place a limit order, specify the symbol, action, quantity, order type (`limit`), and the desired price.

*Example:* Place a limit sell order for 5 BTC at $50000:
```bash
openalgo-executor.run_command("order --symbol BTCUSD --action sell --quantity 5 --type limit --price 50000")
```

### Retrieving Positions

To get a list of your current open positions, use the `positions` command.

*Example:*
```bash
openalgo-executor.run_command("positions")
```

### Retrieving Quotes

To get the current quote for a specific symbol, use the `quote` command with the symbol.

*Example:* Get the quote for ETHUSD:
```bash
openalgo-executor.run_command("quote --symbol ETHUSD")
```

### Custom URL

If your OpenAlgo API is hosted at a different URL (e.g., via ngrok), append the `--url` argument to your command.

*Example:* Using an ngrok URL:
```bash
openalgo-executor.run_command("order --symbol SOLUSD --action buy --quantity 10 --url http://your-ngrok-url.io")
```
