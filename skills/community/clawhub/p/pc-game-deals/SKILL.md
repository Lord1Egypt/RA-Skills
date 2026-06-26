---
name: game-deals
description: "Track PC game discounts across Steam, Epic Games, GOG, Humble Store and 30+ stores via CheapShark API. Use when user asks: 'any deals on [game]', 'game discounts', 'steam sale', 'lowest price for [game]', 'set price alert', or mentions game prices/savings. NOT for console games (PS5/Xbox/Switch) or mobile games - CheapShark is PC only. No API key required."
metadata: { "openclaw": { "emoji": "🎮", "requires": { "bins": ["curl", "jq"] } } }
---

# Game Deals

Track game discounts across PC game stores.

## Store IDs

| ID | Store |
|----|-------|
| 1 | Steam |
| 7 | GOG |
| 11 | Humble Store |
| 25 | Epic Games Store |
| 31 | Blizzard Shop |

Full list: `curl -s "https://www.cheapshark.com/api/1.0/stores" | jq '.[] | "\(.storeID): \(.storeName)"'`

---

## Commands

### Search Game

```bash
curl -s "https://www.cheapshark.com/api/1.0/games?title=GAME_NAME&limit=5" | jq -r '.[] | "🎯 \(.external) - 最低价: $\(.cheapest)"'
```

### Hot Deals

```bash
# Steam deals under $15
curl -s "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15&pageSize=10" | jq -r '.[] | "🔥 \(.title) - $\(.salePrice) (原价 $\(.normalPrice), -\(.savings | tonumber | floor)%%)"'
```

### Filter Options

- `storeID=1` — Steam only
- `upperPrice=10` — Max price $10
- `sortBy=Savings&desc=1` — Sort by discount
- `onSale=1` — Only items on sale

### Price History

```bash
# Get gameID from search first
curl -s "https://www.cheapshark.com/api/1.0/games?id=GAME_ID" | jq '{cheapest: .cheapestPriceEver.price, current: .deals | map({store: .storeID, price: .price})}'
```

---

## Price Alerts

Web-based only: https://www.cheapshark.com → Search game → "Set Alert" → Enter email + target price
