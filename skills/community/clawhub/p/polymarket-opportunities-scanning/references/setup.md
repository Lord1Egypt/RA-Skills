# Setup Guide

## Requirements

- Node.js v18+ (uses native `fetch` — no npm install needed)
- macOS (for email via Apple Mail + osascript)
- Telegram chat ID (for Telegram delivery)

## Directory Structure

```
your-project/
├── scanner.js        — Scans Polymarket API, saves opportunities.json
├── send-report.js    — Runs scanner, formats report, sends Telegram + email
├── opportunities.json — Auto-generated scan output (gitignore this)
└── .env              — Your config (gitignore this)
```

## .env Configuration

```env
# Email recipient (Apple Mail sends from your default account)
SMTP_TO=you@example.com

# Optional: override sender display name
# SMTP_FROM=Polymarket Scanner
```

## Telegram Delivery

The `send-report.js` script uses OpenClaw's `message` tool for Telegram.

To configure your Telegram chat ID:
1. Send a message to your OpenClaw bot
2. Your chat ID appears in OpenClaw's message logs
3. Update the `TELEGRAM_CHAT_ID` constant in `send-report.js`

## Customising Scan Parameters

Edit the `CONFIG` object at the top of `scanner.js`:

```js
const CONFIG = {
  minVolume: 10000,     // Min market volume ($) — raise to filter noise
  minThreshold: 0.03,   // Min deviation (3%) — lower = more results
  maxThreshold: 0.50,   // Max deviation (50%) — above = likely false signal
  minPrice: 0.03,       // Min valid outcome price
  maxPrice: 0.97,       // Max valid outcome price
  minHealthyMarkets: 2, // Min outcomes in valid range
  pageSize: 100,        // Markets fetched per API call
};
```

**Recommended starting point:**
- `minVolume: 10000` — filters out illiquid markets
- `minThreshold: 0.03` — 3% deviation is meaningful after fees
- Focus on NegRisk markets first — they have the cleanest structure

## Excluded Market Types

The scanner automatically excludes non-mutually-exclusive markets:
- Over/under lines
- Spread bets
- Handicap markets
- Moneyline with multi-outcome structure

These are filtered via keyword matching in `EXCLUDE_KEYWORDS` (editable in scanner.js).

## Understanding the Output

**OVERBOOK (sum > 1.0):**
The market is pricing outcomes at more than 100% combined. Buying all NO outcomes guarantees a profit if held to resolution (minus fees).

**UNDERBOOK (sum < 1.0):**
The market is under-pricing all outcomes. Buying all YES outcomes guarantees a profit if held to resolution (minus fees).

**NegRisk markets:**
Polymarket's NegRisk contracts are structurally guaranteed to be mutually exclusive. These are the highest-quality opportunities with the least false-positive risk.

## Fees

Polymarket charges a maker/taker fee (typically 1–2%). Factor this into your minimum threshold — a 3% deviation leaves ~1–2% net after fees.
