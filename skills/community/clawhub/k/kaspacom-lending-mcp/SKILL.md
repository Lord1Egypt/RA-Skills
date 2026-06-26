---
name: kaspacom-lending-mcp
description: Use KaspaCom Lending through the KaspaCom DeFi MCP/CLI for market discovery, position checks, and lending actions like supply, borrow, and repay on IGRA and Kasplex environments. Trigger on lending market, health factor, collateral, borrow, repay, or Aave-style KaspaCom requests through MCP.
---

# KaspaCom Lending MCP

Focused skill for KaspaCom lending via MCP/CLI.

## Install
```bash
npm i -g @kaspacom/defi-mcp
```

## Read-only examples
```bash
kaspacom-defi getMarkets --network igra
kaspacom-defi getPosition --address 0xYOUR_WALLET --network igra
```

## Transaction examples
```bash
kaspacom-defi supply --token USDC --amount 500 --network igra
kaspacom-defi borrow --token WKAS --amount 50 --network igra
kaspacom-defi repay --token WKAS --amount max --network igra
```

## Best for
- Market snapshots
- Wallet lending positions
- Health factor checks
- Collateral and borrowing flows
- AI-agent access to KaspaCom lending
