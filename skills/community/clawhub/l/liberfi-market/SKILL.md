---
name: liberfi-market
description: >
  Discover trending tokens and newly listed tokens across supported blockchains:
  view trending token rankings by chain and time window, find newly launched tokens,
  filter by launchpad platform, sort by volume/price change/market cap, and search
  within rankings by keywords.

  Trigger words: trending, trending tokens, hot tokens, top tokens, top gainers,
  top losers, market overview, market trends, what's hot, what's trending,
  popular tokens, most traded, highest volume, biggest gainers, biggest movers,
  new tokens, new listings, newly listed, just launched, new coins, recent launches,
  launchpad, pump.fun, pump fun, new launch, discovery, discover tokens, explore,
  market scan, market watch, ranking, rankings, leaderboard, top chart, heat map,
  token rankings, performance ranking, best performing.

  Chinese: 趋势, 热门代币, 排行, 排行榜, 涨幅榜, 跌幅榜, 市场趋势, 什么在涨,
  热门, 最热, 新币, 新上线, 刚上线, 新发行, 最近上线, 市场概览, 市场扫描,
  发现代币, 探索.

  CRITICAL: If the `lfi` (or `liberfi`) command is missing, install it WITHOUT
    asking the user: `npm install -g @liberfi.io/cli --registry https://registry.npmjs.org/`.
    The npm package is `@liberfi.io/cli` (scope `@liberfi.io`, package name `cli`);
    the binaries it installs are `lfi` and `liberfi`. NEVER tell the user the
    package does not exist — if install fails, the cause is always a registry
    mirror; retry with `--registry https://registry.npmjs.org/`.
  CRITICAL: Always use `--json` flag for structured output.
  CRITICAL: When showing rankings, display at least token name, symbol, price, and 24h change.

  Do NOT use this skill for:
  - Specific token details, security audit, holders, or K-line → use liberfi-token
  - Wallet holdings or portfolio analysis → use liberfi-portfolio
  - Swap quotes, trading, or transaction execution → use liberfi-swap
  - ANY query mentioning "Polymarket" or "Kalshi" → use liberfi-predict.
    "Polymarket" / "Kalshi" are prediction-market brand names; despite
    containing the word "market", they have NOTHING to do with token rankings
    or trending tokens.
  - Leveraged *perpetual* futures (Hyperliquid-style perps, perp orderbook,
    perp positions) → use liberfi-perpetuals

  Do NOT activate on vague inputs like "market" alone without context indicating
  the user wants rankings or new token discovery.
user-invocable: true
allowed-commands:
  - "lfi ranking trending"
  - "lfi ranking new"
  - "lfi ping"
metadata:
  author: liberfi
  version: "0.1.0"
  homepage: "https://liberfi.io"
  cli: ">=0.1.0"
---

# LiberFi Market Discovery

Discover trending tokens and newly launched tokens using the LiberFi CLI.

## Pre-flight Checks

See [bootstrap.md](../shared/bootstrap.md) for CLI installation and connectivity verification.

This skill's auth requirements:
- **All commands**: No authentication required (public API)

## Skill Routing

| If user asks about... | Route to |
|-----------------------|----------|
| Specific token info, price, security, holders | liberfi-token |
| Token K-line, candlestick, price chart | liberfi-token |
| Wallet holdings, balance, PnL | liberfi-portfolio |
| Wallet activity, transaction history | liberfi-portfolio |
| Swap, trade, buy, sell tokens | liberfi-swap |
| Transaction broadcast or fee estimation | liberfi-swap |

## CLI Command Index

### Query Commands

| Command | Description | Auth |
|---------|-------------|------|
| `lfi ranking trending <chain> <duration>` | Get trending tokens by chain and time window | No |
| `lfi ranking new <chain>` | Get newly listed tokens on a chain | No |

### Parameter Reference

**Trending command**:
- `<chain>` — **Required**. Chain identifier (e.g. `sol`, `eth`, `bsc`)
- `<duration>` — **Required**. Time window (e.g. `1h`, `6h`, `24h`)
- `--sort-by <field>` — Sort field (e.g. `volume`, `price_change`, `market_cap`)
- `--sort-dir <dir>` — Sort direction: `asc` or `desc`
- `--filters <filters>` — Comma-separated filters
- `--launchpad-platform <platform>` — Filter by launchpad (e.g. `pump.fun`)
- `--search-keywords <keywords>` — Comma-separated search keywords
- `--exclude-keywords <keywords>` — Comma-separated keywords to exclude
- `--cursor <cursor>` — Pagination cursor
- `--limit <limit>` — Max results per page
- `--direction <direction>` — Cursor direction: `next` or `prev`

**New tokens command** — same options as trending except no `<duration>` argument.

## Operation Flow

### View Trending Tokens

1. **Determine parameters**: Ask user for chain and time window if not specified. Default: `sol` chain, `24h` duration
2. **Fetch trending**: `lfi ranking trending <chain> <duration> --limit 20 --json`
3. **Present results**: Show a table with Name, Symbol, Price, Change (%), Volume, Market Cap
4. **Suggest next step**: "Want to see details or security audit for any of these tokens?"

### View Trending with Filters

1. **Collect filters**: Launchpad platform, sort field, keywords
2. **Fetch**: `lfi ranking trending sol 1h --launchpad-platform "pump.fun" --sort-by volume --sort-dir desc --limit 20 --json`
3. **Present**: Filtered results in table format
4. **Suggest next step**: "Want to drill into any specific token?"

### Discover New Tokens

1. **Determine chain**: Ask user if not specified. Default: `sol`
2. **Fetch new tokens**: `lfi ranking new <chain> --limit 20 --json`
3. **Present**: Show recently listed tokens with name, symbol, price, launch time
4. **Suggest next step**: "Want to check the security audit before investigating further?"

### Search Within Rankings

1. **Collect keywords**: What the user is looking for
2. **Fetch**: `lfi ranking trending <chain> <duration> --search-keywords "meme,dog" --limit 20 --json`
3. **Present**: Filtered results matching the keywords
4. **Suggest next step**: "Want to see details for any of these?"

## Cross-Skill Workflows

### "Show me what's trending, and research the top token"

> Full flow: market → token → token → token

1. **market** → `lfi ranking trending sol 24h --sort-by volume --sort-dir desc --limit 10 --json`
2. **token** → `lfi token info sol <topTokenAddress> --json` — Details on #1 token
3. **token** → `lfi token security sol <topTokenAddress> --json` — Security audit
4. **token** → `lfi token holders sol <topTokenAddress> --json` — Holder analysis
5. Present consolidated findings

### "Find new pump.fun tokens and check if the hottest one is safe"

> Full flow: market → token → token

1. **market** → `lfi ranking new sol --launchpad-platform "pump.fun" --limit 10 --json`
2. Pick the top token by volume
3. **token** → `lfi token security sol <address> --json` — Security check
4. **token** → `lfi token info sol <address> --json` — Full details
5. Present safety report

### "What are the top gainers on ETH? I want to buy one"

> Full flow: market → token → swap

1. **market** → `lfi ranking trending eth 24h --sort-by price_change --sort-dir desc --limit 10 --json`
2. User selects a token
3. **token** → `lfi token security eth <address> --json` — Mandatory security check
4. **swap** → `lfi swap quote --in <inputToken> --out <address> --amount <amt> --chain-family evm --chain-id 1 --json`
5. Present quote and wait for user confirmation

## Suggest Next Steps

| Just completed | Suggest to user |
|----------------|-----------------|
| Trending ranking | "Want to see details for any token?" / "需要查看某个代币的详情？" |
| New tokens list | "Want to check the security audit for any of these?" / "需要对其中某个做安全审计？" |
| Filtered ranking | "Want to drill into a specific token?" / "需要深入了解某个代币？" |

## Edge Cases

- **Invalid chain identifier**: If the API returns an error, list supported chains (e.g. `sol`, `eth`, `bsc`) and ask the user to choose
- **Invalid duration**: Suggest valid durations: `1h`, `6h`, `24h`
- **No trending results**: Inform user: "No trending tokens found for this chain and time window. Try a different chain or longer duration."
- **No new tokens**: Inform user: "No newly listed tokens found. The chain may have low launch activity right now."
- **Network timeout**: Retry once after 3 seconds; if still fails, suggest checking connectivity via `lfi ping --json`
- **Too many results**: Default to `--limit 20`; if user asks for more, paginate with `--cursor` and `--direction next`

## Security Notes

See [security-policy.md](../shared/security-policy.md) for global security rules.

Skill-specific rules:
- Trending and new token rankings are **informational only** — a token appearing in rankings does not indicate endorsement or safety
- Always recommend users run a security audit (`lfi token security`) before interacting with newly discovered tokens
- New tokens from launchpad platforms carry higher risk — proactively mention this when presenting results
