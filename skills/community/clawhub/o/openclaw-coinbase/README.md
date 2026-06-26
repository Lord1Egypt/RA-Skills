# OpenClaw Coinbase Skill

Coinbase API integration for OpenClaw trading agents.

## Overview

This skill provides Python bindings for the Coinbase trading API, enabling agents to:
- Check account balances
- View trading products
- Place orders (market and limit)
- Access order history

## Installation

### 1. Install Dependencies

```bash
pip install cryptography PyJWT
```

### 2. Configure API Keys

Create a `.coinbase-api-key` file with your API key:
```
your-api-key-here
```

Create a `.coinbase-api-secret` file with your private key (PEM format):
```
-----BEGIN PRIVATE KEY-----
your-private-key-here
-----END PRIVATE KEY-----
```

### 3. Get API Keys

1. Go to [Coinbase Developer Platform](https://portal.cdp.coinbase.com)
2. Create a new App
3. Generate API credentials
4. Copy the key and secret to the files above

## Usage

```python
from scripts.coinbase import get_all_balances, create_order, get_fills

# Check balances
balances = get_all_balances()
print(f"EUR: {balances.get('EUR')}")
print(f"BTC: {balances.get('BTC')}")

# Place an order
order = create_order(
    product_id='BTC-EUR',
    side='BUY',
    size='0.001'
)

# Get trade history
fills = get_fills()
```

## Requirements

- Python 3.7+
- cryptography
- PyJWT

## License

MIT