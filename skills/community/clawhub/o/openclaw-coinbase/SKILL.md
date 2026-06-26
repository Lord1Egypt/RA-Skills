# Coinbase Skill

This skill provides access to Coinbase trading API for crypto trading agents.

## Features

- Fetch account balances (EUR, BTC, etc.)
- Get trading products (EUR pairs)
- Create market and limit orders
- View order history and fills

## Usage

### Get Balances
```python
from scripts.coinbase import get_euro_balance, get_btc_balance, get_all_balances

eur = get_euro_balance()
btc = get_btc_balance()
all_balances = get_all_balances()
```

### Get Products
```python
from scripts.coinbase import get_eur_products, get_product

# All EUR trading pairs
products = get_eur_products()

# Specific product
btc_eur = get_product('BTC-EUR')
```

### Create Orders
```python
from scripts.coinbase import create_order

# Market buy order
result = create_order(
    product_id='BTC-EUR',
    side='BUY',
    size='0.001'  # Amount in base currency
)

# Limit order
result = create_order(
    product_id='BTC-EUR',
    side='BUY',
    size='0.001',
    price='45000',  # Limit price
    order_type='LIMIT'
)
```

### Order History
```python
from scripts.coinbase import get_fills, get_orders

# Recent trades
fills = get_fills()

# Specific product
fills_btc = get_fills(product_id='BTC-EUR')

# Order history
orders = get_orders()
```

## Installation

### Requirements
- Coinbase API keys (CDP App)
- Python 3 with cryptography package

### Setup
Create these files in the same directory as the script:

```
.coinbase-api-key     # Your API key
.coinbase-api-secret  # Your private key (PEM format)
```

### Get API Keys
1. Go to [Coinbase Developer Platform](https://portal.cdp.coinbase.com)
2. Create a new App
3. Copy API key and private key to the files

## Notes

- All trades are in EUR pairs
- Use `side='BUY'` or `side='SELL'`
- `size` is in base currency (e.g., BTC, not EUR)