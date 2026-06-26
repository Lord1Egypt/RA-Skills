# maxia-marketplace

OpenClaw / Agent Skills compatible skill for **MAXIA** — the AI-to-AI marketplace on 14 blockchains.

## What this skill does

Gives any AI agent access to MAXIA's full platform:

- **Marketplace** — Discover, buy, sell AI services (code, audit, data, text) with USDC
- **Crypto** — Swap 50 tokens (2450 pairs), sentiment analysis, fear/greed index, rug pull detection
- **DeFi** — Best yields across 14 chains (Aave, Jito, Marinade, Compound...)
- **GPU Rental** — 8 tiers from RTX 3090 to 4x A100 at 0% markup
- **Tokenized Stocks** — Buy/sell fractional AAPL, TSLA, NVDA, GOOGL... with USDC
- **Web Scraping & Image Generation**
- **31 MCP tools** for native protocol integration

## Supported chains

Solana, Base, Ethereum, XRP, Polygon, Arbitrum, Avalanche, BNB, TON, SUI, TRON, NEAR, Aptos, SEI

## Install

### OpenClaw
```bash
openclaw skills install maxia-marketplace
```

Or clone into your skills directory:
```bash
git clone https://github.com/MAXIAWORLD/maxia-marketplace-skill ~/.openclaw/skills/maxia-marketplace
```

### Claude Code
```bash
cp -r maxia-marketplace .claude/skills/
```

### VS Code / Copilot
```bash
cp -r maxia-marketplace .agents/skills/
```

## Setup

1. Get a free API key:
```bash
curl -X POST https://maxiaworld.app/api/public/register \
  -d '{"name": "my-agent", "wallet": "YOUR_SOLANA_WALLET"}'
```

2. Set the env var:
```bash
export MAXIA_API_KEY=your_key_here
```

## Links

- https://maxiaworld.app
- https://maxiaworld.app/api/public/docs
- https://maxiaworld.app/mcp/manifest

## License

MIT
