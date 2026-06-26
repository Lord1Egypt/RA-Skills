# Polymarket CLI Examples

## Read-Only (No Wallet Needed)

### Search for markets
```bash
polymarket -o json markets search "trump" --limit 5 | jq '.[] | {question, id}'
polymarket markets search "bitcoin" --limit 10
```

### Get specific market
```bash
polymarket -o json markets get "will-trump-win-2024" | jq '.question, .clobTokenIds'
```

### List active events by tag
```bash
polymarket -o json events list --tag politics --active true --limit 20
polymarket -o json events list --tag crypto --limit 10
```

### Check prices
```bash
# Get token ID from market first
TOKEN_ID="48331043336612883518340892014567954950"
polymarket -o json clob midpoint "$TOKEN_ID"
polymarket -o json clob price "$TOKEN_ID" --side buy
polymarket -o json clob spread "$TOKEN_ID"
```

### View orderbook
```bash
polymarket -o json clob book "$TOKEN_ID" | jq '.bids[:5], .asks[:5]'
```

### Price history
```bash
polymarket -o json clob price-history "$TOKEN_ID" --interval 1d --fidelity 30
```

### Check someone's portfolio (public)
```bash
WALLET="0xf5E642a62cf76FB8DaCc1238c19Ac9c2b7D60e21"
polymarket -o json data positions "$WALLET"
polymarket -o json data value "$WALLET"
polymarket -o json data trades "$WALLET" --limit 20
```

### Leaderboard
```bash
polymarket -o json data leaderboard --period month --order-by pnl --limit 10
```

## Trading (Requires Wallet)

### Setup
```bash
# First time setup
polymarket wallet create
polymarket approve set  # Needs MATIC for gas

# Or import existing wallet
polymarket wallet import 0xYOUR_PRIVATE_KEY
```

### Check balance
```bash
polymarket -o json clob balance --asset-type collateral
```

### Place limit order
```bash
# Buy 10 shares at $0.45
polymarket clob create-order \
  --token "$TOKEN_ID" \
  --side buy \
  --price 0.45 \
  --size 10
```

### Place market order
```bash
# Buy $5 worth
polymarket clob market-order \
  --token "$TOKEN_ID" \
  --side buy \
  --amount 5
```

### View and cancel orders
```bash
polymarket -o json clob orders
polymarket clob cancel ORDER_ID
polymarket clob cancel-all
```

### View trades
```bash
polymarket -o json clob trades | jq '.[] | {market, side, price, size}'
```

## Scripting Patterns

### Find best markets by volume
```bash
polymarket -o json markets list --limit 100 --order volume_num --ascending false \
  | jq '.[] | select(.volume > 1000000) | {question, volume, liquidity}'
```

### Monitor price changes
```bash
while true; do
  PRICE=$(polymarket -o json clob midpoint "$TOKEN_ID" | jq -r '.mid')
  echo "$(date): $PRICE"
  sleep 60
done
```

### Get all active crypto markets
```bash
polymarket -o json events list --tag crypto --active true --limit 50 \
  | jq '.[] | {title, slug, volume}'
```

### Extract token IDs from market
```bash
MARKET_SLUG="bitcoin-above-100k-2024"
polymarket -o json markets get "$MARKET_SLUG" \
  | jq -r '.clobTokenIds | @csv'
```

## Error Handling in Scripts

```bash
if ! result=$(polymarket -o json clob midpoint "$TOKEN_ID" 2>&1); then
  echo "Error: $result" >&2
  exit 1
fi

PRICE=$(echo "$result" | jq -r '.mid')
if [ "$PRICE" = "null" ]; then
  echo "No price data available" >&2
  exit 1
fi

echo "Current price: $PRICE"
```

## Tips

- Always use `-o json` for scripting
- Pipe to `jq` for filtering/formatting
- Token IDs are long numbers, not market IDs
- Prices are 0-1 (52¢ = 0.52)
- Check `polymarket --help` for full command list
- Use `polymarket shell` for interactive mode
