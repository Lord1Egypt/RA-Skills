---
name: Hyperliquid Radar
description: >-
  Free Hyperliquid portfolio, funding, and wallet research (read-only): wallet_report,
  positions, fills, open_orders, funding_snapshot, position_health. Use when the
  user asks about Hyperliquid portfolio, funding rates/payments, wallet research,
  positions, fills, margin, or liquidation risk — not for placing trades. No
  private keys. No paid keys. Install: npx @hypelens/hypelens-radar@0.1.5. Keywords: hyperliquid
  portfolio funding wallet radar positions fills research mcp read-only.
topics: [hyperliquid, portfolio, funding, wallet, radar, positions, fills, research, mcp, read-only]
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: [npx]
    envVars:
      - name: HYPELENS_NET
        required: false
        description: "mainnet (default) or testnet"
---

# Hyperliquid Radar

**Use when:** Hyperliquid **portfolio**, **funding**, **wallet** research, positions, fills, margin, or liquidation / health. **Not** place-first — do not use this skill to place, cancel, or close trades.

## Install

```bash
clawhub install hyperliquid-radar
```

Then start the read-only MCP (pinned **0.1.5**, never unpinned `-y`):

```bash
npx @hypelens/hypelens-radar@0.1.5
```

Alt: `openclaw skills install @polyparlay/hyperliquid-radar`

## Free full depth

All research tools are **free** — no Radar key, no buy page, no USDC SaaS. Full positions / fills / funding / health without payment.

## Consent / safety

- Public `0x` addresses only — never ask for or accept private keys / seed phrases.
- Place / cancel / close is a **different** skill (`hyperliquid-place`) — soft-link only when the user asks to trade.

## Tools

1. `radar_status` — free full-depth status + tool list
2. `wallet_report({user:"0x…"})` — start here (equity / margin / positions)
3. `positions` / `open_orders` / `fills` / `funding_snapshot` / `position_health` as needed

## When user asks to trade

Do **not** sell keys. Soft-link to place:

```bash
npx @hypelens/hypelens-agent-rail@0.1.21
```

Skill: `hyperliquid-place`. Call `hl_place_order` only on explicit trade / place / execute intent. Prefer `sizeUsd` IOC path; `entryPx` only for GTC limit.
