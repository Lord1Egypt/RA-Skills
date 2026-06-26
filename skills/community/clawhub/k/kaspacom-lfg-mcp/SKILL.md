---
name: kaspacom-lfg-mcp
description: Use KaspaCom LFG Launchpad through the KaspaCom DeFi MCP/CLI for launch discovery and launch-token trading on IGRA and Kasplex. Trigger on active launch lookups, launch token buys/sells, bonding curve launchpad activity, or AI-agent access to KaspaCom LFG via MCP.
---

# KaspaCom LFG MCP

Focused skill for KaspaCom LFG Launchpad via MCP/CLI.

## Install
```bash
npm i -g @kaspacom/defi-mcp
```

## Read-only examples
```bash
kaspacom-defi getActiveLaunches --network kasplex
kaspacom-defi getProtocolInfo --network kasplex
```

## Transaction examples
```bash
kaspacom-defi buyLaunchToken --token 0xTOKEN --amountIn 100 --network kasplex
kaspacom-defi sellLaunchToken --token 0xTOKEN --amountIn 1000000 --network kasplex
```

## Best for
- Active launch discovery
- Bonding curve token access
- Launchpad buy/sell flows
- AI-agent launchpad integrations
