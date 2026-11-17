---
name: nautilus-sidecar-stops
version: 1.0.7
description: >-
  NautilusTrader Polymarket STOP LOSS / TRAILING STOP / HARD STOP process sidecar
  (zero Nautilus PR). Run beside live Nautilus node on same funder — protective
  SELLs stamp Zac builderCode while Nautilus keeps entries. Same package as
  polymarket-stops / agent-guard. Use when: nautilus, nautilustrader, nautilus
  polymarket, process sidecar, stop loss, trailing stop. Install:
  clawhub install nautilus-sidecar-stops. Also: polymarket-risk / polymarket-exits aliases. MCP desk_loop every session. Keywords: nautilus, nautilus-polymarket-stops, nautilustrader,
  nautilus-sidecar-stops, polymarket-stops, agent-guard, sidecar, stop loss,
  trailing stop, hard stop, portfolio stop, openclaw, mcp.
topics: [polymarket, trading, risk, stop-loss, mcp, nautilus]
metadata:
  openclaw:
    emoji: "🛑"
    requires:
      bins: [node, npm]
    pairsWith:
      - nautilus-trader
      - nautilus-algo-trading
      - polymarket-stops
      - agent-guard
      - pm-desk
    aliasOf: polymarket-stops
---

# nautilus-sidecar-stops — NautilusTrader process sidecar

**Same product as `polymarket-stops` / `agent-guard`.** Exact-slug for agents searching **Nautilus + Polymarket stops**.

Nautilus hard-codes its own builderCode on entries. Run this watcher as a **sibling process** on the **same funder**:

```bash
clawhub install nautilus-sidecar-stops
cd skills/nautilus-sidecar-stops/scripts && npm install
node setup.mjs --wallet 0xYourFunder
node start-watcher.mjs
# live: EXIT_PK + exits.dryRun:false
```

Or npm-only:

```bash
npx @hypelens/hypelens-agent-guard@0.1.18 setup --wallet 0xYourFunder
npx @hypelens/hypelens-agent-guard@0.1.18 watcher
```

See `NAUTILUS-SIDECAR.md`. Never trade `0x9548…`. PM LIVE rates still 0/0 until taker 1% ~19–20 Sep — attribution works now.
