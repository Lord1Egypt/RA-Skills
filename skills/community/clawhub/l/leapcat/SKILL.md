---
name: leapcat
description: Trade stocks, subscribe to IPOs, manage wallet, complete KYC, and access real-time market data via AI agent. 7 skills for the Leapcat platform.
homepage: https://leapcat.ai
---

# Leapcat Skills

A comprehensive set of 7 AI agent skills for the [Leapcat](https://leapcat.ai) platform. All commands use `npx leapcat@0.1.1` — no global install needed, just Node.js 18+.

## Available Skills

### leapcat-auth
Login, logout, session management, token refresh, re-authentication, and trade password operations.

### leapcat-kyc
KYC identity verification including document upload, personal info submission, agreements, and status polling.

### leapcat-ipo
Browse IPO projects, estimate costs, subscribe, cancel, and monitor subscription status.

### leapcat-trading
Place buy/sell stock orders (limit/market), monitor order status, and cancel pending orders.

### leapcat-wallet
Check balance, get deposit address, initiate withdrawals, view debt status, and fund activity history.

### leapcat-portfolio
View portfolio overview and individual stock positions with unrealized P&L.

### leapcat-market
Real-time stock quotes, K-line charts, market indices, stock search, exchange rates, and fee schedules. No authentication required.

## Quick Start

Check market data (no login needed):

```bash
npx leapcat@0.1.1 market quote --symbol 00700.HK --json
npx leapcat@0.1.1 market indices --json
```

Login to access authenticated features:

```bash
npx leapcat@0.1.1 auth login --email your@email.com --send-only --json
npx leapcat@0.1.1 auth login --email your@email.com --otp-id <id> --otp-code <code> --json
```

Then use any skill:

```bash
npx leapcat@0.1.1 wallet balance --json
npx leapcat@0.1.1 portfolio positions --json
npx leapcat@0.1.1 ipo projects --json
```

## Notes

- All commands output JSON when using the `--json` flag
- Session tokens are stored locally at `~/.config/leapcat/tokens.json`
- Access tokens auto-refresh; re-login only needed after 30 days of inactivity
- For sensitive operations (withdrawals), run `npx leapcat@0.1.1 auth reauth --json` first

## Security & Provenance

- **Source code**: [github.com/leapcat-ai/leapcat-skills](https://github.com/leapcat-ai/leapcat-skills)
- **npm package**: [npmjs.com/package/leapcat](https://www.npmjs.com/package/leapcat)
- **Version pinned**: All commands use `npx leapcat@0.1.1` (pinned, not @latest) to prevent supply-chain drift
- **Token storage**: `~/.config/leapcat/tokens.json` is created automatically after login; contains JWT access/refresh tokens, not user credentials
- **KYC documents**: Only uploaded when the user explicitly provides file paths; the CLI does not scan or access local files automatically
- **No env vars required**: Authentication is handled via email OTP, no API keys needed
