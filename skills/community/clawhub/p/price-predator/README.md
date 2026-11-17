# Price Predator 🦈

Track product prices across time and stores, get alerts on price drops, and predict the best time to buy.

## Features

- **Price tracking** — Add products and record price observations over time
- **ASCII sparkline charts** — Visual price history right in your terminal
- **Drop alerts** — Get notified when prices drop below your threshold (default: 10% below median)
- **Seasonal buying guide** — Know the best month to buy each product category
- **Category-aware predictions** — Depreciation rates and seasonal patterns for 15+ categories
- **Target prices** — Set a buy target and get notified when it's reached
- **Pure Python stdlib** — No dependencies, no pip install, just works

## Quick Start

```bash
# Track a product
python3 scripts/price_predator.py track --name "Sony WH-1000XM5" --price 350.00 --category electronics

# Update with a new price
python3 scripts/price_predator.py update <product-id> --price 299.99

# View price history with sparkline
python3 scripts/price_predator.py history <product-id>

# Check for alerts
python3 scripts/price_predator.py alert

# Best time to buy
python3 scripts/price_predator.py best-time --category electronics

# Full report
python3 scripts/price_predator.py report
```

## Commands

| Command | Description |
|---------|-------------|
| `track` | Add a product to track |
| `update <id> --price N` | Record a new price observation |
| `history <id>` | Show price history with ASCII sparkline |
| `alert [id]` | Check for price drops (all or one product) |
| `best-time --category CAT` | Predict best time to buy by category |
| `report` | Full summary of all tracked products |
| `list` | List all tracked products |
| `remove <id>` | Remove a tracked product |
| `info <id>` | Show detailed product info |

## Categories with Seasonal Data

Electronics, TVs, Laptops, Smartphones, Cameras, Video Games, Mattresses, Appliances, Furniture, Clothing, Toys, Tools, Fitness Equipment, Outdoor Gear, Jewelry.

## Example Session

```bash
$ python3 scripts/price_predator.py track --name "MacBook Air M3" --price 1099 --category laptops --target 999
✅ Tracking product 'MacBook Air M3' (id: a1b2c3d4)
   Initial price: $1099.00
   Category: laptops

$ python3 scripts/price_predator.py update a1b2c3d4 --price 1049 --source amazon
✅ Updated 'MacBook Air M3' → $1049.00
   ↓ -50.00 (-4.5%) from previous $1099.00

$ python3 scripts/price_predator.py update a1b2c3d4 --price 989 --source bestbuy
✅ Updated 'MacBook Air M3' → $989.00
   ↓ -60.00 (-5.7%) from previous $1049.00

$ python3 scripts/price_predator.py alert a1b2c3d4
🔔 ALERT: 'MacBook Air M3' (id: a1b2c3d4)
   Latest: $989.00 | Median: $1049.00
   Drop: 5.7% below median (threshold: 10%)

$ python3 scripts/price_predator.py history a1b2c3d4
📊 Price History: MacBook Air M3 (id: a1b2c3d4)
   Sparkline: █▆▄
```

## License

MIT © Denis Voronin
