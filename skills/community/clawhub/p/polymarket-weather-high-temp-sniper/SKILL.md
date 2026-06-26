---
name: polymarket-weather-high-temp-sniper
description: Automated trader for Polymarket weather highest temperature markets. Uses Simmer SDK's importable endpoint for market discovery and trades only during local 9-10 AM window when YES price exceeds threshold. Supports Telegram notifications.
metadata:
  author: "OpenClaw"
  version: "1.0.4"
  displayName: "Weather High-Temp Sniper"
  difficulty: "intermediate"
  tags: ["weather", "polymarket", "simmer", "sniper"]
---

# Weather High-Temp Sniper

Automated trading bot for Polymarket weather markets focusing on "highest temperature" predictions. Uses Simmer SDK's modern market discovery workflow to find and import new weather markets, then executes trades during a specific time window.

## Features

- **Market Discovery**: Uses `/markets/importable` endpoint to find new Polymarket weather markets
- **Duplicate Prevention**: Checks `/markets/check` before importing to avoid duplicates
- **Active Market Fetching**: Retrieves active weather markets via `get_markets(import_source='polymarket', tags=['weather'])`
- **Time-Window Trading**: Only trades during local 9-10 AM based on market location's timezone
- **Fallback Window**: Optional 10:00-10:05 fallback if configured
- **Telegram Notifications**: Real-time alerts for trades, errors, and daily reports
- **Configurable Parameters**: All trading parameters tunable via environment or automaton

## How It Works

### 1. Market Discovery & Import

The bot runs a discovery phase every 6 hours to find new weather markets:

1. Fetches daily import quota from Simmer
2. Queries `list_importable_markets(venue="polymarket", q="highest temperature")`
3. Filters markets using `is_weather_market_question()` heuristics
4. For each candidate, checks if it already exists via `check_market_exists()`
5. Imports new markets using `import_market()` until quota is exhausted

### 2. Active Market Scanning

After discovery, the bot fetches active weather markets:

```python
markets = client.get_markets(
    import_source="polymarket",
    status="active",
    max_hours_to_resolution=48
)
```

It then locally filters to only weather-related markets using the same heuristics.

### 3. Trading Logic

For each weather market:

1. **Extract location** from the question string and detect timezone (via `CITY_TZ_MAP`)
2. **Check time window**: Only trade if local time is 9:00-9:59 AM (or fallback 10:00-10:05)
3. **Get current price** (YES probability)
4. **Check threshold**: Price must be ≥ `ENTRY_PRICE_THRESHOLD`
5. **Validate position size**: Cost (shares × price) must be ≤ `MAX_POSITION_USD`
6. **Execute trade**: `place_order(market_id, "buy", shares, price, slippage)`
7. **Record state**: Mark market as traded today to avoid re-entry

### 4. Position Management

- No position in the same market on the same day
- All trades tracked in `sniper.state.json`
- State persists across restarts

## Configuration

All parameters are configurable via environment variables or via the OpenClaw automaton (`--set` flag):

| Parameter | Environment Variable | Default | Description |
|-----------|---------------------|---------|-------------|
| `entry_price_threshold` | `SIMMER_SNIPER2_ENTRY_PRICE_THRESHOLD` | `0.35` (35%) | Minimum YES price to trigger a buy |
| `max_position_usd` | `SIMMER_SNIPER2_MAX_POSITION_USD` | `2.50` | Maximum USD risk per trade |
| `shares_per_order` | `SIMMER_SNIPER2_SHARES` | `5` | Number of YES shares per order (min 5 on Polymarket) |
| `slippage_tolerance` | `SIMMER_SNIPER2_SLIPPAGE` | `0.15` (15%) | Maximum acceptable slippage |
| `scan_interval_seconds` | `SIMMER_SNIPER2_SCAN_INTERVAL` | `300` (5 min) | How often to scan for opportunities |
| `fallback_at_local_10` | `SIMMER_SNIPER2_FALLBACK_10AM` | `true` | Enable 10:00-10:05 fallback window |
| `telegram_enabled` | `SIMMER_SNIPER2_TELEGRAM_ENABLED` | `false` | Enable Telegram notifications |
| `telegram_chat_id` | `SIMMER_SNIPER2_TELEGRAM_CHAT_ID` | `""` | Your Telegram chat ID |
| `report_interval_seconds` | `SIMMER_SNIPER2_REPORT_INTERVAL` | `240` (4 min) | How often to send periodic reports |

### Setting Configuration

**Via environment variable**:
```bash
export SIMMER_SNIPER2_ENTRY_PRICE_THRESHOLD=0.40
export SIMMER_SNIPER2_MAX_POSITION_USD=5.00
```

**Via command line** (overrides config.json):
```bash
python sniper.py --set entry_price_threshold=0.40
python sniper.py --set max_position_usd=5.00
```

**Via OpenClaw automaton** (persistent tuning):
The skill integrates with the Simmer Automaton — configuration changes via automaton are automatically persisted and synced.

## Installation & Setup

### Prerequisites

- Python 3.8+
- Simmer API key (from [simmer.markets/dashboard](https://simmer.markets/dashboard))
- Polymarket linked wallet (bot will auto-link on first run)
- Telegram bot token and chat ID (optional, for notifications)

### Install Dependencies

```bash
cd polymarket-weather-high-temp-sniper-1
pip install -r requirements.txt
```

### Configure Environment

Create `.env` file in the skill folder:

```bash
# Required
SIMMER_API_KEY=your_simmer_api_key_here

# Optional (Telegram)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789  # Your Telegram user ID
TELEGRAM_ENABLED=true
```

Or set environment variables directly in your shell/automaton config.

### Test Telegram

```bash
python sniper.py --test-telegram
```

This verifies bot token and sends a test message.

## Usage

### Dry Run (Default)

See what would be traded without executing:

```bash
python scripts/sniper.py
```

### Live Trading

Execute real trades:

```bash
python scripts/sniper.py --live
```

The daemon will:
- Run discovery phase every 6 hours
- Scan every 5 minutes (configurable via `scan_interval_seconds`)
- Send Telegram notifications on trades and errors
- Print periodic reports every 4 minutes

### Show Current Positions

```bash
python scripts/sniper.py --positions
```

### Show Active Configuration

```bash
python scripts/sniper.py --config
```

### Adjust Parameters On-The-Fly

```bash
python scripts/sniper.py --set entry_price_threshold=0.40
python scripts/sniper.py --set max_position_usd=5.00
python scripts/sniper.py --set scan_interval_seconds=180
```

### Stop the Bot

Press `Ctrl+C` in the terminal where it's running. A shutdown notification will be sent via Telegram if enabled.

## State Persistence

The skill stores its runtime state in `sniper.state.json`:

```json
{
  "date": "2025-01-15",
  "traded_today": ["market_id_1", "market_id_2"],
  "last_report_ts": 1705312345,
  "last_discovery_ts": 1705312000
}
```

- `traded_today`: List of markets already traded today (reset at midnight UTC)
- `last_report_ts`: Timestamp of last periodic report
- `last_discovery_ts`: Timestamp of last market discovery phase

## Important Notes

### Timezone Detection

The bot auto-detects timezone from city names in the market question. It recognizes major cities worldwide (see `CITY_TZ_MAP` in the code). If a city is not recognized, the market is skipped.

### Price Source

The bot reads `current_probability` or `external_price_yes` from the Simmer market object. Prices are expressed as probabilities (0.0 - 1.0).

### Market Question Filtering

Only markets meeting these criteria are considered:

- Must contain "temperature", "temp", "°c", or "°f"
- Must contain "highest" or "high"
- Must NOT contain "lowest", "minimum", "low", "below", "fall below"
- Must NOT contain noise keywords: crypto, bitcoin, election, president, sports, etc.

### Import Quota

Simmer imposes daily import limits (typically ~10/day). The bot respects remaining quota and will skip discovery when exhausted.

### Position Sizing

Each trade costs: `shares_per_order × price`. The bot checks this ≤ `max_position_usd` before buying. Example: With `max_position_usd=2.50`, `shares=5`, and price `0.35`, cost = `5 × 0.35 = $1.75` ✅.

### Minimum Shares

Polymarket requires a minimum of 5 shares per order. The default `shares_per_order=5` satisfies this constraint.

## Troubleshooting

### "SIMMER_API_KEY not set"

Set your API key in `.env` or environment. Get it from [simmer.markets/dashboard](https://simmer.markets/dashboard) → SDK tab.

### "Telegram: bot token invalid"

Test with `--test-telegram`. Verify:
- `TELEGRAM_BOT_TOKEN` is correct (format: `123456:ABC-DEF...`)
- Bot has been started (send `/start` to your bot in Telegram)
- `TELEGRAM_CHAT_ID` is your numeric user ID (not username)

### Markets Not Being Traded

- Check if current time is within 9-10 AM local time for the market location
- Verify price is ≥ `entry_price_threshold` (default 35%)
- Ensure cost (`shares × price`) ≤ `max_position_usd`
- Check logs for skipped markets and reasons

### Quota Exhausted

The bot will log when daily import quota (10/day) is exhausted. Wait for the next UTC day or request quota increase from Simmer.

### No Positions Showing

Use `--positions` to fetch current positions. Ensure wallet is linked (bot attempts auto-link on first run).

## Support

For issues or feature requests, refer to the OpenClaw documentation or contact the skill author.
