# Portfolio Drift Monitor Configuration Reference

Complete configuration guide for the Portfolio Drift Monitor skill.

## Environment Variables

### Required Variables

#### `KALSHI_KEY_ID`
**Type:** String
**Required:** Yes
**Description:** Your Kalshi API key ID from dev.kalshi.com

**Where to find:**
1. Log in to https://dev.kalshi.com
2. Navigate to API keys
3. Copy the "Key ID" value

**Example:**
```bash
export KALSHI_KEY_ID="key_abcd1234"
```

#### `KALSHI_KEY_PATH`
**Type:** Path
**Required:** Yes
**Description:** Absolute path to your Kalshi private key file (ES256 PEM format)

**Where to find:**
1. When creating API key at dev.kalshi.com, download the private key
2. Save securely, typically at `~/.kalshi/key.pem`

**Example:**
```bash
export KALSHI_KEY_PATH="$HOME/.kalshi/key.pem"
```

**Security:** Keep this file private. Never commit to git. Restrict permissions:
```bash
chmod 600 ~/.kalshi/key.pem
```

### Optional Variables

#### `PORTFOLIO_DRIFT_THRESHOLD`
**Type:** Float
**Default:** `5.0`
**Unit:** Percentage (%)
**Description:** Minimum position change percentage to trigger an alert

**Behavior:**
- Position must change ≥ this percentage to generate alert
- Checks changes in: shares held, P&L value, avg entry price
- Uses maximum drift across all metrics

**Examples:**
```bash
# Alert on 3% change (more sensitive)
export PORTFOLIO_DRIFT_THRESHOLD="3.0"

# Alert on 10% change (less sensitive, fewer false alerts)
export PORTFOLIO_DRIFT_THRESHOLD="10.0"

# Alert on any change (very sensitive)
export PORTFOLIO_DRIFT_THRESHOLD="0.5"
```

**Recommended values:**
- Day traders / active monitoring: 2-3%
- Swing traders: 5-7%
- Position traders: 10-15%

#### `PORTFOLIO_DRIFT_INTERVAL`
**Type:** Integer
**Default:** `60`
**Unit:** Minutes
**Description:** Minimum time between checks for rate limiting

**Behavior:**
- If checked within interval, skips check and reports when next check available
- Prevents API spam and excessive polling
- When integrated with proactive agent, set interval on agent, not here

**Examples:**
```bash
# Check every 15 minutes (aggressive monitoring)
export PORTFOLIO_DRIFT_INTERVAL="15"

# Check every 2 hours (light monitoring)
export PORTFOLIO_DRIFT_INTERVAL="120"

# Check every time (no rate limiting, only for manual runs)
export PORTFOLIO_DRIFT_INTERVAL="0"
```

**Recommended values:**
- Proactive agent integration: 15-30 min (agent controls interval)
- Manual checks: 60+ min (prevents accidental spam)

## Configuration Methods

### Method 1: Environment Variables (Recommended for automated)

Set in shell profile or in launchd plist:

```bash
# ~/.zshrc or ~/.bash_profile
export KALSHI_KEY_ID="key_abc123"
export KALSHI_KEY_PATH="$HOME/.kalshi/key.pem"
export PORTFOLIO_DRIFT_THRESHOLD="5.0"
export PORTFOLIO_DRIFT_INTERVAL="60"
```

Reload shell:
```bash
source ~/.zshrc
```

### Method 2: Command line (For ad-hoc runs)

```bash
KALSHI_KEY_ID="key_abc123" \
KALSHI_KEY_PATH="$HOME/.kalshi/key.pem" \
PORTFOLIO_DRIFT_THRESHOLD="3.0" \
python scripts/portfolio_drift.py
```

### Method 3: Launchd plist (For automated scheduled checks)

Example plist for Mac launchd service (`com.portfolio-drift-monitor`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.portfolio-drift-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/portfolio_drift.py</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>KALSHI_KEY_ID</key>
        <string>key_abc123</string>
        <key>KALSHI_KEY_PATH</key>
        <string>/Users/YOUR_USERNAME/.kalshi/key.pem</string>
        <key>PORTFOLIO_DRIFT_THRESHOLD</key>
        <string>5.0</string>
        <key>PORTFOLIO_DRIFT_INTERVAL</key>
        <string>60</string>
    </dict>
    <key>StartInterval</key>
    <integer>900</integer>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/var/log/portfolio-drift.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/portfolio-drift.error</string>
</dict>
</plist>
```

## State File

### Location
`~/.openclaw/state/portfolio_snapshot.json`

### Purpose
Stores the last recorded portfolio state for drift comparison on next run.

### Structure
```json
{
  "timestamp": "2026-03-09T15:30:45.123456",
  "total_positions": 5,
  "positions": {
    "TRUMP.25DEC": {
      "side": "YES",
      "shares": 100,
      "avg_price": 0.65,
      "pnl": 25.00,
      "pnl_percent": 3.8,
      "risk": 35.00,
      "timestamp": "2026-03-09T15:30:45.123456"
    }
  }
}
```

### Auto-management
- Created automatically on first run
- Updated after each successful check
- Never manually edited (script maintains it)
- Safe to delete to reset baseline

## Drift Calculation Details

### What is "Drift"?

A position has drifted when its key metrics change significantly since last check.

### Metrics Checked

For each position, monitor:

1. **Share Count Drift**
   - Formula: `|current_shares - previous_shares| / previous_shares * 100`
   - Detects: Position size changes (scaling up/down, partial exits)

2. **P&L Drift**
   - Formula: `|current_pnl - previous_pnl| / previous_pnl * 100`
   - Detects: USD value changes (market movement, realized gains/losses)

3. **Price Drift**
   - Formula: `|current_avg_price - previous_avg_price| / previous_avg_price * 100`
   - Detects: Average entry price changes (adding at different prices)

### Alert Threshold

A position triggers an alert if **any** metric ≥ threshold percentage.

Example with 5% threshold:
- Position with 3% shares change + 4% P&L change → No alert (below 5%)
- Position with 3% shares change + 6% P&L change → Alert (6% > 5%)

## Output Format

### Drift Detected
```
🚨 Portfolio Drift Alert

📈 YES/TRUMP.25DEC → +12.5% (↑$1,250 P&L, ↑350 shares)
   Last check: 47 minutes ago

📉 NO/ELEX.HOUSEGOV → -8.3% (↓$425 unrealized P&L)
   Last check: 42 minutes ago

---
✓ Stable (3): KALSHI.USD, CRYPTO.BTC, ECON.UNEMP
```

### No Drift
```
✓ No drift detected (5 positions stable)
```

### First Run
```
✅ Baseline established: 5 positions recorded
```

### Rate Limited
```
Rate limited: next check in 47 minutes
```

### Error
```
ERROR: Failed to fetch portfolio from Kalshi: Connection timeout
```

## Troubleshooting

### "KALSHI_KEY_ID and KALSHI_KEY_PATH environment variables required"

**Fix:** Set environment variables before running:
```bash
export KALSHI_KEY_ID="key_abc123"
export KALSHI_KEY_PATH="$HOME/.kalshi/key.pem"
python scripts/portfolio_drift.py
```

### "Kalshi key file not found"

**Fix:** Verify key path exists and is readable:
```bash
ls -la $KALSHI_KEY_PATH
# Expected output: -rw------- YOUR_USER YOUR_USER 1234 ...
```

If file doesn't exist, download from dev.kalshi.com and save to path.

### "Failed to initialize Kalshi client: Authentication failed"

**Fix:** Verify API credentials are correct:
```bash
# Confirm values match what's in dev.kalshi.com
echo $KALSHI_KEY_ID
cat $KALSHI_KEY_PATH | head -1  # Should start with "-----BEGIN PRIVATE KEY-----"
```

### "Rate limited: next check in X minutes"

**Normal behavior** when checking within interval. Either:
- Wait for interval to elapse
- Manually bypass by setting `PORTFOLIO_DRIFT_INTERVAL=0`

### Position shows 0% drift but expected alert

**Possible causes:**
- Position hasn't changed since last check
- Change is below threshold percentage
- Threshold is too high — try lowering it

Check snapshot to debug:
```bash
cat ~/.openclaw/state/portfolio_snapshot.json | python -m json.tool
```

## Integration Examples

### With OpenClaw Scheduled Task

```yaml
skills:
  portfolio-drift-monitor:
    enabled: true
    schedule: "0 * * * *"  # Every hour
    timeout_seconds: 30
    env:
      KALSHI_KEY_ID: "${KALSHI_KEY_ID}"
      KALSHI_KEY_PATH: "${KALSHI_KEY_PATH}"
      PORTFOLIO_DRIFT_THRESHOLD: "5.0"
```

### Manual Monitoring Script

```bash
#!/bin/bash
# Run every hour manually
while true; do
  PORTFOLIO_DRIFT_INTERVAL=0 python scripts/portfolio_drift.py
  sleep 3600  # 1 hour
done
```

### With System Cron (macOS)

Add to `launchd` for recurring checks without daemon:

```bash
# Create plist as shown in Method 3 above
# Install:
launchctl load ~/Library/LaunchAgents/com.portfolio-drift-monitor.plist

# Check status:
launchctl list | grep portfolio

# Uninstall:
launchctl unload ~/Library/LaunchAgents/com.portfolio-drift-monitor.plist
```
