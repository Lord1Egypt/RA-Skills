# predictfun-mcp

<a href="https://glama.ai/mcp/servers/PaulieB14/predictfun-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/PaulieB14/predictfun-mcp/badge" />
</a>

MCP (Model Context Protocol) server that gives AI agents structured access to [Predict.fun](https://predict.fun) — a prediction market protocol on BNB Chain with $1.7B+ volume and yield-bearing mechanics via Venus Protocol.

Indexes data from three subgraphs on [The Graph](https://thegraph.com): orderbook activity, position lifecycle, and yield mechanics.

## Install

### Claude Code

```bash
claude mcp add predictfun -- npx predictfun-mcp
```

Then set your Graph API key:

```bash
export GRAPH_API_KEY=your-key-here
```

### Claude Desktop / Manual Config

Add to your MCP config (`~/.claude/settings.json` or Claude Desktop settings):

```json
{
  "mcpServers": {
    "predictfun": {
      "command": "npx",
      "args": ["predictfun-mcp"],
      "env": {
        "GRAPH_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### OpenClaw / Remote Agents (SSE)

Start the server with the HTTP transport:

```bash
# Dual transport — stdio + SSE on port 3850
npx predictfun-mcp --http

# SSE only (for remote/server deployments)
npx predictfun-mcp --http-only

# Custom port
MCP_HTTP_PORT=4000 npx predictfun-mcp --http
```

Then point your agent at the SSE endpoint:

```json
{
  "mcpServers": {
    "predictfun": {
      "url": "http://localhost:3850/sse"
    }
  }
}
```

### Docker

```bash
docker build -t predictfun-mcp .
docker run -e GRAPH_API_KEY=your-key-here predictfun-mcp
```

### Transport Modes

| Invocation | Transports | Use case |
|---|---|---|
| `npx predictfun-mcp` | stdio | Claude Desktop, Cursor, Claude Code |
| `npx predictfun-mcp --http` | stdio + SSE :3850 | Dual — local + remote agents |
| `npx predictfun-mcp --http-only` | SSE :3850 | OpenClaw, remote deployments |

A `/health` endpoint is available at `http://localhost:3850/health` when HTTP transport is active.

## Requirements

- **Graph API Key** — Get one free at [Subgraph Studio](https://thegraph.com/studio/) ([docs](https://thegraph.com/docs/en/subgraphs/querying/managing-api-keys/))

That's it — subgraph IDs are built in. Queries go through [The Graph Gateway](https://thegraph.com/docs/en/querying/graphql-api/) and are billed to your API key.

## Tools (14)

### Data Tools

| Tool | Description |
|---|---|
| `get_platform_stats` | Full platform overview — volume, OI, yield, sync status |
| `get_top_markets` | Rank markets by volume, open interest, or trade count |
| `get_market_details` | Deep dive: OI, resolution, top holders, orderbook stats |
| `get_trader_profile` | Full P&L: trades, positions, payouts, yield rewards |
| `get_recent_activity` | Latest trades, splits, merges, redemptions, or yield claims |
| `get_yield_overview` | Venus Protocol deposits, redemptions, yield stats |
| `get_whale_positions` | Largest holders with % of market OI |
| `get_leaderboard` | Top traders by volume, payouts, or trade count |
| `get_resolved_markets` | Recently settled markets with outcomes |
| `query_subgraph` | Custom GraphQL against any subgraph |

### Meta-Tools (agent reasoning layer)

These tools let agents reason about **trader behavior** and **market quality** — not just raw data.

| Tool | Description |
|---|---|
| `find_trader_persona` | Classify a trader into archetypes: whale accumulator, yield farmer, arbitrageur, early mover, resolution sniper |
| `scan_trader_personas` | Find traders matching a specific behavioral archetype across the platform |
| `tag_market_structure` | Tag a market by resolution latency, liquidity profile, oracle type, and tail-risk indicators |
| `scan_markets_by_structure` | Find markets by structural filter: resolution speed, liquidity depth, oracle type, OI concentration, tail risk |

**Trader Personas:** whale_accumulator, yield_farmer, arbitrageur, early_mover, resolution_sniper

**Market Structural Filters:** fast_resolution, slow_resolution, stale, deep_liquidity, thin_liquidity, dormant, uma_oracle, concentrated_oi, high_tail_risk

All meta-tools return structured JSON for programmatic agent consumption.

## Prompts (9)

Pre-built workflows for common analysis:

| Prompt | Description |
|---|---|
| `platform_overview` | Full platform stats, top markets, whales, yield |
| `analyze_trader` | Deep dive on a specific trader's P&L and strategy |
| `market_deep_dive` | Full analysis of a specific prediction market |
| `yield_analysis` | Venus Protocol yield mechanics and APY |
| `whale_alert` | Find biggest players and their positions |
| `market_scanner` | Scan for interesting markets across all rankings |
| `custom_query_examples` | Example GraphQL queries for each subgraph |
| `trader_persona_analysis` | Classify traders by behavioral archetypes and find similar traders |
| `market_quality_scan` | Scan markets by structural quality indicators to find opportunities or risks |

## Architecture

```
User → AI Agent (Claude) → MCP Server → The Graph Gateway → Subgraphs → BNB Chain
```

Three subgraphs power the data:

- **predictfun-orderbook** — trades, orderbooks, market names (NegRisk + CTF)
- **predictfun-positions** — splits, merges, redemptions, open interest
- **predictfun-yield** — Venus Protocol deposits, vToken minting, yield claims

All markets include human-readable names decoded from UMA oracle ancillary data.

## Examples

Ask your AI agent:

- "What are the hottest prediction markets right now?"
- "Show me the top 10 traders by volume"
- "Who are the whales betting on the FIFA World Cup?"
- "What's the yield being generated through Venus?"
- "Find recently resolved markets and their outcomes"
- "What type of trader is 0x1234...? Are they a whale, arbitrageur, or sniper?"
- "Find all resolution snipers on the platform"
- "Which markets have concentrated OI or tail risk?"
- "Run a full market quality scan — what's deep liquidity vs dormant?"

## License

MIT
