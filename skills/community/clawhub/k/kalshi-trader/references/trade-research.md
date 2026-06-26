# Trade Research Workflow

## Finding Good Trades

### Step 1: Scan markets
Get markets closing within 7 days with real prices:
```python
close_ts = int(time.time()) + (7 * 24 * 3600)
r = signed_request("GET", f"/trade-api/v2/markets?limit=200&status=open&max_close_ts={close_ts}")
markets = r.json().get("markets", [])
```

Filter for tradeable candidates:
```python
candidates = []
for m in markets:
    ya = float(m.get("yes_ask_dollars","0") or "0")
    yb = float(m.get("yes_bid_dollars","0") or "0")
    vol = float(m.get("volume_fp","0") or "0")
    # Sweet spot: 65-90¢, liquid, tight spread
    if 0.65 <= ya <= 0.90 and yb > 0 and vol > 200 and (ya-yb) < 0.10:
        candidates.append(m)
```

### Step 2: Research each candidate
Always use web_search before placing. Match the market's resolution rules:

| Market type | What to search |
|-------------|----------------|
| Weather | "city rainfall/snowfall March 2026 total inches" |
| Political actions | "Trump executive orders/actions this week count" |
| Economic data | "AAA gas prices today" / "10Y treasury yield today" |
| Sports | Check schedule + standings |
| Crypto | Check current price vs threshold |

### Step 3: Evaluate edge
Only trade if you can verify the outcome is likely:
- **High confidence (>80%)**: Real-world data clearly supports YES/NO
- **Medium (65-80%)**: Data leans one way but uncertain
- **Skip (<65%)**: Not enough edge to justify risk

### Step 4: Size the position
- Suggested max per trade: 10-15% of total balance
- Never go 100% deployed — keep 5-10% cash buffer
- Higher confidence = can use larger size

## Best Market Categories

### High edge (verifiable data)
- **Weather** — rainfall/snowfall totals trackable daily
- **Economic indicators** — gas prices, treasury yields, Fed decisions
- **Presidential actions** — countable from whitehouse.gov
- **Sports game results** — clear outcomes

### Medium edge (research-dependent)  
- **Crypto prices** — volatile, check current price vs threshold
- **Corporate events** — earnings, launches, announcements
- **Political events** — bills passing, votes

### Avoid
- **Long-shot YES (<15¢)** — buying lottery tickets
- **Near-certain NO (YES >95¢)** — tiny profit, not worth fees
- **Zero volume** — can't exit if needed
- **Wide spreads (>15¢)** — market maker takes too much

## Monitoring Positions

Check hourly. Exit if:
- YES price drops >10¢ from entry (market turning against you)
- New information changes your confidence significantly
- Better opportunity found and capital needed

To exit (sell your YES position):
```python
order = {
    "ticker": ticker,
    "action": "sell",
    "side": "yes",
    "type": "limit",
    "count": contracts_owned,
    "yes_price_dollars": str(current_bid),  # use yes_bid_dollars
    "client_order_id": f"exit-{int(time.time())}"
}
```
