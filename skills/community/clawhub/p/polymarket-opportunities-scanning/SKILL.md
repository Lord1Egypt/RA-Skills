---
name: polymarket-opportunities-scanning
description: Scan Polymarket prediction markets for book arbitrage opportunities (overbooked/underbooked multi-outcome markets), generate a formatted report, and deliver it via Telegram and email. Use when asked to "scan Polymarket", "find betting opportunities", "run Polymarket report", "check Polymarket arb", or set up a daily morning report. No external API keys required — uses Polymarket's public Gamma API.
---

# Polymarket Opportunities Scanning

Scan Polymarket's active multi-outcome markets for book arbitrage opportunities where the sum of all YES prices deviates from 1.0. Generate a ranked report and send to Telegram + email.

## How It Works

In a truly mutually exclusive multi-outcome market, all YES prices should sum to 1.0.

| Deviation | Type | Strategy |
|-----------|------|----------|
| Sum > 1.0 (overbooked) | OVERBOOK | Buy all NO outcomes |
| Sum < 1.0 (underbooked) | UNDERBOOK | Buy all YES outcomes |

**NegRisk markets** are the highest quality — they're structurally guaranteed to be mutually exclusive.

## Setup

1. Copy `scripts/scanner.js` and `scripts/send-report.js` to your project directory
2. Create `.env` in the same directory with email config (see `references/setup.md`)
3. Install dependencies: `npm install` (no external deps — uses built-in `fetch` and Node.js)
4. Test: `node scanner.js && node send-report.js`

## Running a Scan

```bash
# Run scanner → saves opportunities.json
node scanner.js

# Send report (reads opportunities.json → Telegram + email)
node send-report.js
```

Or run both in one cron command:
```bash
node /path/to/send-report.js
```
(send-report.js calls scanner.js internally)

## Scan Parameters (configurable in scanner.js)

| Parameter | Default | Description |
|-----------|---------|-------------|
| minVolume | $10,000 | Skip low-liquidity markets |
| minThreshold | 3% | Minimum deviation worth acting on |
| maxThreshold | 50% | Above this = likely false signal |
| minPrice | 3% | Filter near-zero outcomes |
| maxPrice | 97% | Filter near-certain outcomes |

## Report Format

```
🎯 Polymarket Opportunities Report [timestamp]
Found N opportunities (X NegRisk)

⭐ NegRisk Markets (highest quality)
[OVERBOOK/UNDERBOOK] Event Title
💰 Profit: X%  | Volume: $Xk | 24h: $Xk
📐 Sum: X% (deviation +X%)
🎯 Strategy: Buy all NO / Buy all YES
🔗 https://polymarket.com/event/...
  X%  Outcome A
  X%  Outcome B
  ...

📋 Regular Multi-Outcome Markets
[same format]
```

## Delivery

- **Telegram:** via OpenClaw `message` tool (channel: telegram, to: `<your_telegram_id>`)
- **Email:** via Apple Mail + osascript (macOS only) — set `SMTP_TO` in `.env`

See `references/setup.md` for configuration details.

## Cron Job Setup

Recommended: daily at 08:00 local time.

```json
{
  "name": "Polymarket Morning Scan",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "Europe/Stockholm" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run: exec → node /path/to/send-report.js\nWait for it to complete. If it fails, send a Telegram alert with the error.",
    "timeoutSeconds": 0
  },
  "delivery": { "mode": "none" }
}
```
