---
name: Portfolio Drift Monitor
description: "Real-time Kalshi portfolio drift alerts — monitors positions and fires when any moves beyond your configured threshold since last check. Snapshot comparison, rate-limited checking, directional emoji indicators. Schedule hourly to catch position swings between morning and evening briefs. Part of the OpenClaw Prediction Market Trading Stack — risk management layer that pairs with Kalshi Command Center and Market Morning Brief."
---

# Portfolio Drift Monitor

Real-time monitoring of Kalshi portfolio positions with configurable alerts when positions move significantly. Ideal for active traders tracking exposure, P&L swings, and position concentration.

## Overview

The Portfolio Drift Monitor tracks your Kalshi positions and alerts when any position moves beyond your configured threshold percentage since the last check. It:

- **Compares snapshots**: Current positions vs. last recorded snapshot
- **Detects drift**: Flags positions that moved ≥ threshold (default 5%)
- **Rate-limits checks**: Prevents excessive API calls (configurable, default 60min interval)
- **Formats alerts**: Emoji indicators (📈/📉), directional arrows, price changes
- **Persistent state**: Stores snapshots locally at `~/.openclaw/state/portfolio_snapshot.json`

## When to Use This Skill

- You hold Kalshi positions overnight and want alerts if something moves sharply
- You want hourly drift checks between your morning and evening briefs
- You manage multiple positions and need to catch concentration risk early
- You want a lightweight risk monitoring layer that runs on a schedule without manual checking

## Prerequisites

- **kalshi_python SDK**: Install via `pip install kalshi-python`
- **Kalshi API credentials**: `KALSHI_KEY_ID` and `KALSHI_KEY_PATH` environment variables
- **API key file**: Located at path specified by `KALSHI_KEY_PATH` (typically `~/.kalshi/key.pem`)

## Configuration

Set these environment variables or edit defaults in your environment:

| Variable | Default | Purpose |
|----------|---------|---------|
| `KALSHI_KEY_ID` | (required) | Your Kalshi API key ID from dev.kalshi.com |
| `KALSHI_KEY_PATH` | (required) | Path to your Kalshi private key file (ES256 PEM) |
| `PORTFOLIO_DRIFT_THRESHOLD` | `5.0` | Percentage change to trigger alert (e.g., 5 = 5%) |
| `PORTFOLIO_DRIFT_INTERVAL` | `60` | Minutes between checks (rate limiting, prevents API spam) |

## How to Trigger

Use any of these phrases in conversation:

- "check portfolio drift"
- "portfolio alert"
- "position monitor"
- "drift check"
- "kalshi positions"

## How It Works

### Step 1: Fetch Current Portfolio

The skill calls Kalshi's API to get your current open positions:

```bash
python scripts/portfolio_drift.py
```

This reads `KALSHI_KEY_ID` and `KALSHI_KEY_PATH` from environment, authenticates with Kalshi, and retrieves all open positions.

### Step 2: Load Previous Snapshot

On first run, creates baseline snapshot. On subsequent runs, compares current positions with the last recorded snapshot stored at `~/.openclaw/state/portfolio_snapshot.json`.

### Step 3: Detect Drift

For each position, calculates percent change in:
- **Holdings** (share count)
- **Unrealized P&L** (USD value)
- **Price** (avg entry price vs. current)

If any metric ≥ threshold, flags that position.

### Step 4: Format and Output

Outputs drift alerts with:
- Directional emoji: 📈 (up) or 📉 (down)
- Position symbol and side (YES/NO contract)
- Percentage change with sign (e.g., "+12.5%")
- Time since last check

### Step 5: Update Snapshot

Saves current portfolio as new baseline for next check.

## Output Format

Example output for a position that drifted:

```
📈 YES/TRUMP.25DEC → +12.5% (↑$1,250 P&L, ↑350 shares)
   Last check: 47 minutes ago

📉 NO/ELEX.HOUSEGOV → -8.3% (↓$425 unrealized P&L)
   Last check: 42 minutes ago

No significant drift: KALSHI.USD, CRYPTO.BTC
```

### Error Handling

- **First run**: Creates baseline snapshot, no alerts
- **API failure**: Logs error, doesn't update snapshot
- **Rate limit hit**: Skips check if interval not elapsed
- **No positions**: Outputs "Portfolio is empty"

## Command Examples

### Check portfolio now (bypassing rate limit)

```bash
PORTFOLIO_DRIFT_THRESHOLD=3.0 python scripts/portfolio_drift.py
```

### Check with custom threshold

```bash
PORTFOLIO_DRIFT_THRESHOLD=10.0 python scripts/portfolio_drift.py
```

### Check and see full state file

```bash
python scripts/portfolio_drift.py && cat ~/.openclaw/state/portfolio_snapshot.json | python -m json.tool
```

## Threshold Tuning

| Profile | Threshold | Interval | Use Case |
|---------|-----------|----------|----------|
| **Tight** | 3% | 30 min | Active day trading, many positions |
| **Standard** | 5% | 60 min | Default — balanced signal-to-noise |
| **Loose** | 10% | 120 min | Long-term positions, fewer alerts |
| **News-reactive** | 2% | 15 min | Event-driven trading (FOMC, elections) |

## OpenClaw Ecosystem Integration

Risk management layer for the Prediction Market Trading Stack. Schedule hourly checks to catch position swings between Morning Briefs.

**Scheduling:**
```yaml
skills:
  portfolio-drift-monitor:
    enabled: true
    schedule: "0 * * * *"  # Every hour
    timeout_seconds: 30
```

| Connected Skill | How It Connects |
|----------------|-----------------|
| **Market Morning Brief** | Morning/evening briefs bookend your day; drift alerts fill the gaps |
| **Kalshi Command Center** | Monitors positions opened through the command center |
| **Kalshalyst** | Tracks exposure on positions flagged by contrarian analysis |

**Install the complete stack:**
```bash
clawhub install kalshalyst kalshi-command-center polymarket-command-center prediction-market-arbiter xpulse portfolio-drift-monitor market-morning-brief personality-engine
```

## Performance & Cost

- **Runtime:** <5 seconds per check
- **API calls:** 1 (Kalshi portfolio read)
- **Cost:** $0 (Kalshi free tier)
- **State file:** ~2KB (`portfolio_snapshot.json`)

### Scaling

24 checks/day (hourly) = 24 Kalshi API calls. Well within free tier limits.

## Debugging

Check logs and state:

```bash
# View current snapshot
cat ~/.openclaw/state/portfolio_snapshot.json | python -m json.tool

# Run manually with debug output
python -u scripts/portfolio_drift.py 2>&1 | head -50

# Verify credentials
echo $KALSHI_KEY_ID
ls -la $KALSHI_KEY_PATH
```

## Agent Bug-Fix Protocol

**CRITICAL**: When you (the agent) discover and fix a bug in any script during a conversation, you MUST write the fix to the source file on disk using file editing tools. Showing the fix in chat is NOT sufficient — the next scheduled run starts a fresh session and will not have your conversational fix.

Checklist after finding a bug:
1. Edit the actual `.py` file on disk (e.g., `~/skills/portfolio-drift-monitor/scripts/portfolio_drift.py`)
2. Also update the installed copy at `~/.openclaw/skills/portfolio-drift-monitor/scripts/portfolio_drift.py`
3. Confirm both files are written before telling the user the fix is done
4. If the fix is significant, stage a git commit in `~/skills/`

Never say "fixed" if you only demonstrated the fix in conversation output.

## Known Limitations

- **Kalshi-only:** Currently monitors Kalshi positions only. Polymarket positions require separate tracking.
- **Price-based drift:** Drift is calculated on mid-market price changes, not on volume or open interest shifts.
- **No alerting transport:** Outputs to stdout. Your OpenClaw agent or a wrapper script handles delivery (iMessage, Slack, etc.).

## Additional Resources

- For complete configuration reference, see [drift-config.md](references/drift-config.md)
- For API details, consult [kalshi_python SDK docs](https://docs.kalshi.com)


---

## Feedback & Issues

Found a bug? Have a feature request? Want to share results?

- **GitHub Issues**: [github.com/kingmadellc/openclaw-prediction-stack/issues](https://github.com/kingmadellc/openclaw-prediction-stack/issues)
- **X/Twitter**: [@KingMadeLLC](https://x.com/KingMadeLLC)

Part of the **OpenClaw Prediction Stack** — the first prediction market skill suite on ClawHub.
