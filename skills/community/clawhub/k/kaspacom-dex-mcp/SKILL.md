---
name: kaspacom-dex-mcp
description: Use KaspaCom DEX through the KaspaCom DeFi MCP/CLI for pair discovery, token pricing, swaps, and liquidity management on IGRA and Kasplex. Trigger on requests about KaspaCom swaps, LPs, token prices, DEX pair data, or liquidity actions through MCP.
---

# KaspaCom DEX MCP

Focused skill for KaspaCom DEX via MCP/CLI.

## Install
```bash
npm i -g @kaspacom/defi-mcp
```

## Read-only examples
```bash
kaspacom-defi getPairs --network igra
kaspacom-defi getTokenPrice --token WKAS --quoteToken USDC --network kasplex
```

## Transaction examples
```bash
kaspacom-defi swap --tokenIn USDC --tokenOut WKAS --amountIn 100 --network igra
kaspacom-defi addLiquidity --tokenA WKAS --tokenB USDC --amountA 100 --amountB 42 --network igra
kaspacom-defi removeLiquidity --tokenA WKAS --tokenB USDC --lpAmount 10 --network igra
```

## Best for
- Pair lookup
- Price checks
- Swaps
- LP management
- Agent-driven DEX access on Kaspa L2s
