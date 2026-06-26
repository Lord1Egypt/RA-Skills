---
name: opensea
description: DEPRECATED — moved to opensea/opensea-marketplace. Install that skill instead. This slug is no longer maintained.
---

# DEPRECATED

This skill has moved to **[`opensea/opensea-marketplace`](https://clawhub.ai/opensea/opensea-marketplace)** — the official OpenSea publication on ClawHub. All future updates ship there.

## Migration

Replace `opensea-skill` with `opensea/opensea-marketplace` in your agent manifest:

```json
{
  "skills": [
    { "clawhub_slug": "opensea/opensea-marketplace", "name": "OpenSea" }
  ]
}
```

Or via CLI:

```bash
clawhub install opensea/opensea-marketplace
```

## What changed

This skill (`opensea-skill`) was the original location, originally published by @dfinzer and transferred to @ryanio. The OpenSea team subsequently created an `@opensea` ClawHub org and published the skill fresh under it as `opensea-marketplace` — that's now the canonical home.

Same skill, same functionality (OpenSea MCP wrapper for NFT data, marketplace listings, Seaport trades, ERC20 swaps across Ethereum/Base/Arbitrum/Polygon/etc.). Only the publisher changed.
