# Configuration Guide — Polymarket Executor v2.0.0

---

## Overview

The executor runs in two modes:

| Mode | Credentials needed | Capital | Risk |
|---|---|---|---|
| **Paper** (default) | None | $100 simulated | ZERO |
| **Live** | Polymarket API + Wallet | Your USDC | Real |

**Start with paper mode. Always.**

---

## Step 1: Environment Variables

Add to Wesley's `.env` file (`/docker/openclaw-yyvg/.env`):

```bash
# ── PAPER MODE (default: true) ──────────────
PAPER_MODE=true

# ── POLYMARKET CREDENTIALS (live mode only) ──
POLYMARKET_API_KEY=your_api_key
POLYMARKET_SECRET=your_secret
POLYMARKET_PASSPHRASE=your_passphrase
POLYMARKET_WALLET_ADDRESS=your_polygon_wallet_address

# ── CAPITAL (live mode only) ─────────────────
POLYMARKET_CAPITAL=50.0     # Start small — $50 USDC recommended

# ── TELEGRAM (already configured in Wesley) ──
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=1584210176

# ── WORKSPACE (already set in Wesley) ────────
WORKSPACE=/data/.openclaw/workspace
```

---

## Step 2: Generate Polymarket API Keys (Live Mode Only)

**IMPORTANT: Do this on your LOCAL machine, not the VPS.**

Your wallet private key is needed ONCE to generate API credentials. It must NEVER be stored on the server.

```bash
# On your LOCAL machine
pip install py-clob-client

python3 << 'EOF'
from py_clob_client.client import ClobClient

client = ClobClient(
    host="https://clob.polymarket.com",
    key="YOUR_WALLET_PRIVATE_KEY",  # Used ONCE, never stored on server
    chain_id=137  # Polygon
)

creds = client.create_api_key()

print("=== SAVE THESE — ADD TO WESLEY .env ===")
print(f"POLYMARKET_API_KEY={creds['apiKey']}")
print(f"POLYMARKET_SECRET={creds['secret']}")
print(f"POLYMARKET_PASSPHRASE={creds['passphrase']}")
print("========================================")
EOF
```

Copy the 3 values to Wesley's `.env`. Your private key stays on your local machine.

---

## Step 3: Fund Wallet (Live Mode Only)

1. Buy USDC on Binance or Coinbase
2. Withdraw to Polygon network (not Ethereum — Polygon is cheap)
3. Your wallet address = `POLYMARKET_WALLET_ADDRESS`
4. Minimum recommended: $50 USDC to start

Check balance:
```
https://polygonscan.com/address/YOUR_WALLET_ADDRESS
```

---

## Step 4: Install in Wesley Workspace

```bash
# On VPS as root
docker exec openclaw-yyvg-openclaw-1 bash -c "
mkdir -p /data/.openclaw/workspace/skills/polymarket-executor
"

# Copy script to container
docker cp polymarket_executor.py openclaw-yyvg-openclaw-1:/data/.openclaw/workspace/skills/polymarket-executor/
docker cp SKILL.md openclaw-yyvg-openclaw-1:/data/.openclaw/workspace/skills/polymarket-executor/
```

---

## Step 5: Test Paper Mode

```bash
docker exec openclaw-yyvg-openclaw-1 bash -c "
cd /data/.openclaw/workspace/skills/polymarket-executor
python3 polymarket_executor.py
"
```

Expected:
```
[MODE] 📄 PAPER TRADING (simulated capital: $100.00)
[GAMMA] Fetched 2,341 markets
[SCAN] Found 8 opportunities
```

---

## Configuration Parameters

All parameters live in `learned_config.json` (auto-created on first run, adjusted by optimizer).

### Thresholds

| Parameter | Default | Description |
|---|---|---|
| `min_edge_pct` | 2% | Minimum edge to trade |
| `min_parity_profit` | 2% | Minimum parity arbitrage profit |
| `min_tail_end_certainty` | 95% | Minimum certainty for tail-end |
| `min_logical_edge` | 5% | Minimum edge for logical arb |

### Position Sizing

| Parameter | Default | Description |
|---|---|---|
| `kelly_fraction` | 0.25 | Conservative Kelly multiplier |
| `max_position_pct` | 10% | Max % of capital per trade |
| `max_concurrent_trades` | 3 | Max open positions at once |

### Risk Controls

| Parameter | Default | Description |
|---|---|---|
| `circuit_breaker_pct` | -15% | Daily loss → halt trading |
| `stop_loss_pct` | -50% | Per-position stop-loss |
| `max_daily_trades` | 20 | Hard cap per day |

### Scan Settings

| Parameter | Default | Description |
|---|---|---|
| `scan_interval_seconds` | 300 | 5 min between scans |
| `max_markets_to_scan` | 500 | Markets per cycle |
| `scan_workers` | 50 | Parallel scan threads |

---

## Risk Profiles

### Conservative (Paper mode — start here)
```json
{
  "min_parity_profit": 0.025,
  "min_tail_end_certainty": 0.97,
  "kelly_fraction": 0.20,
  "max_position_pct": 0.05
}
```
Target: 8–12% monthly, 95%+ win rate

### Balanced (After 30+ paper trades validated)
```json
{
  "min_parity_profit": 0.02,
  "min_tail_end_certainty": 0.95,
  "kelly_fraction": 0.25,
  "max_position_pct": 0.10
}
```
Target: 12–20% monthly, 88–92% win rate

---

## Proxy Setup (Live Mode on VPS Only)

Polymarket CLOB API blocks datacenter IPs for POST /order.

**Paper mode:** No proxy needed ✅
**Live mode on VPS:** Residential proxy required

```bash
# Add to .env for live mode
PROXY_URL=http://user:pass@proxy.ipro.yal.com:12321
```

Recommended providers: IPRoyal, BrightData, Oxylabs

---

## Monitoring

```bash
# Live logs
docker exec openclaw-yyvg-openclaw-1 bash -c "
tail -f /data/.openclaw/workspace/paper_trades.json
"

# Portfolio status
docker exec openclaw-yyvg-openclaw-1 bash -c "
cat /data/.openclaw/workspace/portfolio.json | python3 -m json.tool
"

# Strategy performance
docker exec openclaw-yyvg-openclaw-1 bash -c "
cat /data/.openclaw/workspace/performance_metrics.json | python3 -m json.tool
"
```

---

## Troubleshooting

**"Failed to fetch markets"**
→ Gamma API timeout. Normal. Script auto-retries.

**"API error: Unauthorized"**
→ Wrong credentials or expired. Regenerate API keys.

**"Found 0 opportunities"**
→ Normal during low-activity periods. Markets are efficient. Optimizer will lower thresholds if sustained.

**"Circuit breaker active"**
→ Daily loss exceeded -15%. Trading halted until next day. Check Telegram for details.

**POST order rejected on VPS**
→ Configure residential proxy. Expected behavior — datacenter IPs blocked by Cloudflare.

---

**Version:** 2.0.0 | **Author:** Georges Andronescu (Wesley Armando)
