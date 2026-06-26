---
name: kaspacom-defi-mcp
description: Use KaspaCom DeFi MCP or CLI to query and transact across KaspaCom DEX, Lending, and LFG Launchpad on IGRA and Kasplex mainnet/testnet. Trigger when the user wants AI-agent access to KaspaCom DeFi, asks to use MCP with Claude/Cursor/Codex, or wants unified CLI/MCP interaction with swaps, lending positions, launchpad buys, prices, pairs, or protocol info.
---

# KaspaCom DeFi MCP

KaspaCom DeFi MCP exposes KaspaCom DeFi through a single MCP server and CLI.

## Supports
- DEX: pairs, prices, swaps, add/remove liquidity
- Lending: markets, positions, supply, borrow, repay
- LFG Launchpad: active launches, buy/sell launch tokens
- Networks: `igra`, `igra-testnet`, `kasplex`, `kasplex-testnet`

## Install
```bash
npm i -g @kaspacom/defi-mcp
```

## Start MCP server
```bash
MCP_NETWORK=igra node dist/mcp/index.js
```

With wallet:
```bash
MCP_WALLET_KEY="0x..." MCP_NETWORK=igra node dist/mcp/index.js
```

## CLI
```bash
kaspacom-defi --help
```

## Good use cases
- "Show me all KaspaCom DEX pairs on Kasplex"
- "Get my lending health factor on IGRA"
- "List active LFG launches"
- "Buy a launch token with 100 KAS"
- "Get protocol info across networks"

## Notes
- Read-only tools work without a wallet.
- Write actions require `MCP_WALLET_KEY`.
- Use `igra-testnet` or `kasplex-testnet` for safe testing first.
