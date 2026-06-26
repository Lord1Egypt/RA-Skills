# Kalshi API Reference

## Base URL
```
https://api.elections.kalshi.com
```

## Authentication
Every request needs three headers:
- `KALSHI-ACCESS-KEY` — your API Key ID
- `KALSHI-ACCESS-TIMESTAMP` — current time in milliseconds
- `KALSHI-ACCESS-SIGNATURE` — RSA-PSS SHA256 signature of `timestamp + METHOD + path`

## Python Auth Template
```python
import requests, time, base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open("/root/.kalshi/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("/root/.kalshi/key_id.txt") as f:
    key_id = f.read().strip()

BASE = "https://api.elections.kalshi.com"

def signed_request(method, path, body=None):
    timestamp = str(int(time.time() * 1000))
    msg = (timestamp + method + path.split("?")[0]).encode()
    sig = private_key.sign(
        msg,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
        hashes.SHA256()
    )
    headers = {
        "KALSHI-ACCESS-KEY": key_id,
        "KALSHI-ACCESS-TIMESTAMP": timestamp,
        "KALSHI-ACCESS-SIGNATURE": base64.b64encode(sig).decode(),
        "Content-Type": "application/json"
    }
    if body:
        return requests.request(method, BASE + path, headers=headers, json=body)
    return requests.request(method, BASE + path, headers=headers)
```

## Key Endpoints

### Balance
```
GET /trade-api/v2/portfolio/balance
→ { "balance": 2419 }  # in cents, divide by 100
```

### Markets
```
GET /trade-api/v2/markets?limit=200&status=open&max_close_ts=<unix_timestamp>
→ { "markets": [...], "cursor": "..." }
```

Market fields:
- `ticker` — unique ID
- `title` — description
- `yes_ask_dollars` — cost to buy YES
- `yes_bid_dollars` — what you'd get selling YES
- `no_ask_dollars` — cost to buy NO
- `volume_fp` — total volume traded
- `close_time` — when market closes

### Single Market
```
GET /trade-api/v2/markets/<ticker>
→ { "market": { ...full details including rules_primary... } }
```

### Place Order
```
POST /trade-api/v2/portfolio/orders
{
  "ticker": "KXEXAMPLE-26MAR31",
  "action": "buy",
  "side": "yes",          # "yes" or "no"
  "type": "limit",
  "count": 10,            # number of contracts
  "yes_price_dollars": "0.7500",  # or no_price_dollars
  "client_order_id": "unique-id"
}
→ { "order": { "status": "executed", "fill_count_fp": "10.00", ... } }
```

### Positions
```
GET /trade-api/v2/portfolio/positions?count_filter=position&limit=50
→ { "market_positions": [...] }
```

### Cancel Order
```
DELETE /trade-api/v2/portfolio/orders/<order_id>
```

## Price Notes
- Prices are in dollars (0.00 to 1.00)
- YES price + NO price ≈ $1.00 (minus spread)
- Buying YES at $0.70 = paying 70¢ to win $1.00 if YES resolves
- Volume is in number of contracts
