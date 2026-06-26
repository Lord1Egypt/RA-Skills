# Weather High-Temp Sniper 🌡️

**OpenClaw Skill** | Polymarket Weather Trading via Simmer SDK

Automated trading bot for Polymarket weather "highest temperature" markets. Uses Simmer's `/markets/importable` endpoint for discovery and executes trades during the local 9-10 AM window when YES price exceeds your configured threshold.

**Skill Slug**: `polymarket-weather-high-temp-sniper`  
**Version**: 1.0.4  
**Strategy**: Sniper-style entry on high-probability weather markets

---

## Quick Start

### 1. Install Dependencies

```bash
cd polymarket-weather-high-temp-sniper-1
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in this folder:

```env
# Required: Get from simmer.markets/dashboard → SDK tab
SIMMER_API_KEY=your_api_key_here

# Optional: Telegram notifications
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789
TELEGRAM_ENABLED=true
```

Or set environment variables in your shell or OpenClaw automaton config.

### 3. Test Telegram (Optional)

```bash
python scripts/sniper.py --test-telegram
```

### 4. Dry Run First

```bash
python scripts/sniper.py
```

Observe logs and signals. No real trades are executed.

### 5. Go Live

```bash
python scripts/sniper.py --live
```

---

## Configuration

All parameters are tunable. See [SKILL.md](SKILL.md#configuration) for full details.

| Parameter | Env Var | Default | Description |
|-----------|----------|---------|-------------|
| `entry_price_threshold` | `SIMMER_SNIPER2_ENTRY_PRICE_THRESHOLD` | `0.35` | Min YES price to buy (35%) |
| `max_position_usd` | `SIMMER_SNIPER2_MAX_POSITION_USD` | `2.50` | Max USD per trade |
| `shares_per_order` | `SIMMER_SNIPER2_SHARES` | `5` | Shares per order (min 5) |
| `scan_interval_seconds` | `SIMMER_SNIPER2_SCAN_INTERVAL` | `300` | Scan every 5 minutes |
| `fallback_at_local_10` | `SIMMER_SNIPER2_FALLBACK_10AM` | `true` | Enable 10:00-10:05 fallback |
| `telegram_enabled` | `SIMMER_SNIPER2_TELEGRAM_ENABLED` | `false` | Enable Telegram |
| `report_interval_seconds` | `SIMMER_SNIPER2_REPORT_INTERVAL` | `240` | Periodic report interval |

### Change Config at Runtime

```bash
python scripts/sniper.py --set entry_price_threshold=0.40
python scripts/sniper.py --set max_position_usd=5.00
```

Changes are saved to `config.json` (if using skill framework) or environment.

---

## Commands

| Command | Description |
|---------|-------------|
| `python scripts/sniper.py` | Run in dry-run mode (no trades) |
| `python scripts/sniper.py --live` | Execute real trades |
| `python scripts/sniper.py --positions` | Show current open positions |
| `python scripts/sniper.py --config` | Display active configuration |
| `python scripts/sniper.py --test-telegram` | Verify Telegram setup |
| `python scripts/sniper.py --set KEY=VALUE` | Set config parameter |
| `python scripts/sniper.py --quiet` | Suppress info logs (errors only) |

---

## How It Works

1. **Discovery Phase** (every 6 hours)
   - Fetches remaining import quota from Simmer
   - Queries importable Polymarket markets with "highest temperature"
   - Filters to weather-related markets
   - Checks for duplicates via `/markets/check`
   - Imports new markets using `/markets/import`

2. **Scanning Phase** (every `scan_interval_seconds`)
   - Fetches active weather markets from Simmer (`import_source='polymarket'`)
   - For each market:
     - Detect timezone from city name in question
     - Check if local time is 9:00-9:59 AM (or fallback 10:00-10:05)
     - Get current YES price
     - If price ≥ `entry_price_threshold` and position cost ≤ `max_position_usd` → BUY
   - Records trade in state and marks market as "traded today"

3. **Reporting**
   - Sends Telegram notifications on trades and errors
   - Emits periodic summary report
   - JSON report for automaton integration

---

## State File

`config.json` (if using framework) or environment variables persist your config.

`state/sniper.state.json` (runtime state):
- `date`: Current UTC date (reset daily)
- `traded_today`: List of market IDs already traded
- `last_report_ts`: Timestamp of last report
- `last_discovery_ts`: Timestamp of last discovery

---

## Telegram Integration

1. Create a bot via [@BotFather](https://t.me/BotFather) → get token
2. Start a chat with your bot → send any message
3. Get your chat ID: Visit `https://api.telegram.org/bot<token>/getUpdates`
4. Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
5. Set `TELEGRAM_ENABLED=true`

Notifications include:
- Startup message (dry-run/live status)
- Trade confirmations
- Errors (with alerts)
- Periodic reports
- Shutdown notice

---

## Troubleshooting

**"SIMMER_API_KEY not set"** → Set it in `.env` or environment.

**No trades happening** → Check: time window (local 9-10 AM), price ≥ threshold, position cost within limit.

**Telegram not working** → Run `--test-telegram`, check bot token, chat ID, and that bot is started.

**Quota exhausted** → Daily import limit reached (~10/day). Wait for UTC midnight or request increase.

**Markets skipped** → Watch logs for skip reasons (`already hold`, `price < entry`, `outside 9am-4pm`, etc.)

---

## Files

- `scripts/sniper.py` — Main trading logic
- `SKILL.md` — Full documentation (AgentSkills format)
- `clawhub.json` — Skill metadata for OpenClaw
- `requirements.txt` — Python dependencies
- `.env.sample` — Environment template
- `state/sniper.state.json` — Runtime persistence
- `config.json` — User overrides (auto-created)

---

## License & Support

Part of the OpenClaw ecosystem. See OpenClaw documentation for integration details.
