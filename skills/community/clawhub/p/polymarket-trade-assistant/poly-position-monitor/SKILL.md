---
name: poly-position-monitor
version: 1.0.2
description: Monitor Polymarket positions and open orders for specific wallet addresses. Detects price anomalies, volume spikes, whale activity, and position changes across held markets, with alerts via terminal, Telegram, and email. Use when the user wants to monitor their Polymarket positions, track wallet activity, set up position alerts, or watch for market anomalies on held markets.
metadata: {"openclaw": {"emoji": "👁️", "requires": {"bins": ["python3"]}, "envVars": [{"name": "POLY_API_KEY", "required": false, "description": "CLOB API key for order monitoring (optional, can use config file)"}, {"name": "POLY_SECRET", "required": false, "description": "CLOB API secret"}, {"name": "POLY_PASSPHRASE", "required": false, "description": "CLOB API passphrase"}]}}
---

# Polymarket Position Monitor

Monitor wallet positions on Polymarket in real time. Detects 5 types of anomalies across all held markets and delivers alerts through console, Telegram, and email.

## Anomaly Types

1. **Price volatility** — relative price change exceeds threshold on 5/15/60/240 min windows
2. **Volume anomaly** — trading volume spikes or drops vs rolling average
3. **Large inflows** — new positions or significant size changes
4. **Whale activity** — watched addresses trade on the user's held markets
5. **Order changes** — open orders filled, partially filled, or cancelled

## Workflow

Execute the following 6 steps in order.

### Step 1: Configure

Copy the example config and fill in credentials:

```bash
cp scripts/config.example.json ~/polymarket-monitoring/config.json
```

Edit `~/polymarket-monitoring/config.json`:

1. **user_addresses**: Add the user's Polymarket wallet address(es)
2. **watched_addresses**: Add whale/notable addresses to monitor (with labels)
3. **clob_auth**: Add API credentials for order monitoring (see below)
4. **thresholds**: Adjust alert thresholds if needed (see [references/alert-thresholds.md](references/alert-thresholds.md))
5. **notifications**: Enable Telegram and/or email

**Getting CLOB API credentials:**

```python
from py_clob_client.client import ClobClient
client = ClobClient("https://clob.polymarket.com", chain_id=137, key="YOUR_PRIVATE_KEY")
creds = client.create_or_derive_api_creds()
print(creds)  # {"apiKey": "...", "secret": "...", "passphrase": "..."}
```

**Setting up Telegram Bot:**
1. Message @BotFather on Telegram, create a bot, get the token
2. Send a message to your bot, then call `https://api.telegram.org/bot<TOKEN>/getUpdates` to find your chat_id
3. Set `telegram.enabled: true`, fill in `bot_token` and `chat_id`

### Step 2: Install Dependencies

```bash
pip install py-clob-client
```

Only required for open order monitoring. Position tracking, price analysis, volume tracking, and whale detection use standard library only.

### Step 3: Initial Snapshot

Run the position fetcher to verify connectivity and see current holdings:

```bash
python scripts/fetch_positions.py <wallet_address>
```

This shows all active positions, their markets, current values, and PnL. Confirm the output looks correct before starting the monitor.

### Step 4: Verify Connections

Test each component individually:

```bash
# Test price history (use an asset_id from Step 3 output)
python scripts/fetch_price_history.py <token_id>

# Test market trades (use a condition_id from Step 3 output)
python scripts/fetch_market_activity.py trades --market <condition_id>

# Test order fetching (requires auth)
python scripts/fetch_orders.py --config ~/polymarket-monitoring/config.json
```

If Telegram is configured, the monitor will send a test alert on first run.

### Step 5: Start Monitor

```bash
python scripts/monitor.py --config ~/polymarket-monitoring/config.json
```

The monitor runs continuously, checking every `interval_seconds` (default: 60s).

**Options:**
- `--once` — Run a single cycle and exit (useful for cron jobs)
- `--interval 30` — Override check interval to 30 seconds

**Cron setup** (alternative to continuous mode):
```bash
# Check every 2 minutes
*/2 * * * * cd {baseDir} && python scripts/monitor.py --config ~/polymarket-monitoring/config.json --once >> ~/polymarket-monitoring/cron.log 2>&1
```

**Graceful shutdown:** Ctrl-C saves final state and exits cleanly.

### Step 6: Manage

**View alert history:**
```bash
# Recent alerts (JSON lines)
tail -20 ~/polymarket-monitoring/alerts.jsonl

# Filter by type
grep '"CRITICAL"' ~/polymarket-monitoring/alerts.jsonl
grep '"whale"' ~/polymarket-monitoring/alerts.jsonl
```

**View state snapshots:**
```bash
ls ~/polymarket-monitoring/snapshot-*.json
cat ~/polymarket-monitoring/monitor-state.json
```

**Add/remove watched addresses:** Edit `watched_addresses` in config.json. Changes take effect on next cycle.

**Adjust thresholds:** Edit `thresholds` in config.json. See [references/alert-thresholds.md](references/alert-thresholds.md) for tuning guide.

## Troubleshooting

- **No positions found**: Verify the wallet address is correct and has active (non-redeemed) positions on Polymarket
- **Price history empty**: The token_id (asset_id) might be invalid. Check that the position's asset_id matches a valid CLOB token
- **Order fetch fails**: Verify API credentials. Re-derive with `create_or_derive_api_creds()` if needed
- **Telegram not sending**: Check bot token and chat_id. Ensure the bot has received at least one message from the user first
- **Too many alerts**: Increase thresholds in config.json. Set notification `min_level` to "ALERT" or "CRITICAL"
- **Rate limiting**: Increase `interval_seconds`. The monitor makes ~3 API calls per market per cycle

## Reference Files

- [references/polymarket-api.md](references/polymarket-api.md) — API endpoint documentation
- [references/alert-thresholds.md](references/alert-thresholds.md) — Threshold tuning guide
- [references/output-template.md](references/output-template.md) — Alert format specifications
