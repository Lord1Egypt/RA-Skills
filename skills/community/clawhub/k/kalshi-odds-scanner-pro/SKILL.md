# Kalshi Odds Scanner Pro

Compare Kalshi prediction market prices vs 6 major sportsbooks in real-time. Fires automatically on 8%+ edge. Kelly-sized execution. The exact scanner used to deploy capital daily on Kalshi sports markets.

> 💰 **Used to generate consistent returns on Kalshi sports markets.** $79 value.

## What It Does

- Fetches live odds from The Odds API (6+ sportsbooks: DraftKings, FanDuel, BetMGM, Caesars, etc.)
- Compares sportsbook-implied probabilities vs Kalshi ask prices
- Fires on 8%+ edge (YES side) or 5%+ edge (NO side heavy favorites)
- Kelly criterion position sizing (25% fractional Kelly, capped at $60)
- NCAAB heavy-favorite NO-side insight: ~74% historical win rate when fav > 80%
- Deduplicates — ONE side per game only

## Setup

1. Copy `odds_scanner.py` to your polymarket/trading directory
2. Get a free API key at [the-odds-api.com](https://the-odds-api.com)
3. Set your Kalshi API credentials:
   - `KALSHI_KEY_ID` — your Kalshi API key ID
   - `~/.config/kalshi/private_key.pem` — your Kalshi private key

Edit constants at the top of the script:
```python
ODDS_API_KEY = "your_key_here"
KALSHI_KEY_ID = "your_kalshi_key_id"
```

## Usage

```bash
# Scan YES plays (default NBA)
python3 odds_scanner.py

# Scan NO plays (heavy favorites, 74% win rate)
python3 odds_scanner.py --side no

# Scan both YES and NO
python3 odds_scanner.py --side both

# Scan NCAAB (college basketball)
python3 odds_scanner.py --sport ncaab --side both

# Execute found plays on Kalshi
python3 odds_scanner.py --buy --sport nba --side both

# Set custom edge threshold
python3 odds_scanner.py --min-edge 0.10
```

## Supported Sports

| Key | League |
|-----|--------|
| `nba` | NBA Basketball |
| `ncaab` | NCAA Basketball |
| `nhl` | NHL Hockey |
| `mlb` | MLB Baseball |

## Edge Logic

**YES side:** `sportsbook_prob - kalshi_yes_ask > 8%`
- Example: Sportsbooks say Lakers win 72%, Kalshi YES at 62% → +10% edge → BUY

**NO side:** `(1 - sportsbook_prob) - kalshi_no_ask > 5%`
- Example: Sportsbooks say team wins 85%, Kalshi NO at 8% → true NO worth 15% → +7% edge → BUY NO

## Kelly Sizing

```
f = (b*p - q) / b  × 0.25 (quarter Kelly)
```
- `MIN_BET = $10`, `MAX_BET = $60`
- `RESERVE = $50` kept aside always

## Integration

Works with `ensemble.py` and `momentum.py` in the same directory for multi-model consensus gating.

## Requirements

- Python 3.9+
- `cryptography` library: `pip install cryptography`
- The Odds API key (free tier: 500 requests/month)
- Kalshi account with API access
