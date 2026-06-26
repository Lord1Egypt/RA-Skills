# Meteora Liquidity Analyst

OpenClaw skill that turns your AI agent into a real-time Meteora liquidity analyst on Solana.

## What It Does

Ask natural language questions about Meteora pools and get actionable data:

- **Pool rankings** by APR, TVL, volume, or fees
- **Token search** — find all pools for any token
- **Pool details** by address with full metrics
- **Cross-AMM comparison** — DLMM vs DAMM v1 vs DAMM v2
- **Protocol metrics** — global TVL, volume, fees
- **OHLCV data** and volume history
- **Pool groups** — same pair, different configurations

## Quick Install

```bash
clawhub install meteora-analyst
```

Or with the OpenClaw CLI:

```bash
openclaw skills install meteora-analyst
```

Or manually: copy the `meteora-analyst/` folder into your project's `.agents/skills/` directory.

## Requirements

- No API key needed
- No wallet needed
- No configuration needed

All data comes from Meteora's public REST APIs.

## Supported APIs

| Product | Base URL | Rate Limit |
|---------|----------|------------|
| DLMM | `https://dlmm.datapi.meteora.ag` | 30 RPS |
| DAMM v1 | `https://amm-v2.meteora.ag` | -- |
| DAMM v2 | `https://damm-v2.datapi.meteora.ag` | 10 RPS |

## Example Questions

- "What are the top 10 pools by fees on Meteora?"
- "Find all SOL-USDC pools and compare them"
- "What's the APR for this pool? [address]"
- "Show me the global metrics for Meteora"
- "Compare DLMM vs DAMM v2 for the SOL-USDC pair"
- "Which pools have the best fee/TVL ratio?"

## Target Users

| Profile | Use Case |
|---------|----------|
| Solana Trader | Find the best pool for LP before depositing |
| DeFi Researcher | Compare pool metrics across AMM types |
| Dev / Builder | Explore pools for a newly launched token |
| Token Holder | Check if liquidity exists for a token on Meteora |

## Files

```
meteora-analyst/
  SKILL.md                        # Main skill instructions
  references/
    api-endpoints.md              # Complete API endpoint reference
  README.md                       # This file
```

## Version

1.0.0

## License

MIT
