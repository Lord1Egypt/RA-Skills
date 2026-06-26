---
name: openbroker
description: Hyperliquid trading plugin with background position monitoring and custom automations. Execute market orders, limit orders, manage positions, view funding rates, run trading strategies, and write event-driven automation scripts with automatic alerts for PnL changes and liquidation risk.
license: MIT
compatibility: Requires Node.js 22+, network access to api.hyperliquid.xyz
homepage: https://www.npmjs.com/package/openbroker-plugin
metadata: {"author": "monemetrics", "version": "1.2.0", "openclaw": {"requires": {"bins": ["openbroker"], "env": ["HYPERLIQUID_PRIVATE_KEY"]}, "primaryEnv": "HYPERLIQUID_PRIVATE_KEY", "install": [{"id": "node", "kind": "node", "package": "openbroker-plugin", "bins": ["openbroker"], "label": "Install openbroker-plugin (npm)"}]}}
allowed-tools: ob_account ob_positions ob_funding ob_markets ob_search ob_spot ob_outcomes ob_fills ob_orders ob_order_status ob_fees ob_candles ob_funding_history ob_trades ob_rate_limit ob_funding_scan ob_buy ob_sell ob_limit ob_trigger ob_tpsl ob_cancel ob_spot_buy ob_spot_sell ob_outcome_buy ob_outcome_sell ob_twap ob_twap_cancel ob_twap_status ob_bracket ob_chase ob_watcher_status ob_auto_run ob_auto_stop ob_auto_list Bash(openbroker:*)
---

# Open Broker - Hyperliquid Trading CLI

Execute trading operations on Hyperliquid DEX with builder fee support.

## Installation

```bash
npm install -g openbroker
```

## Quick Start

```bash
# 1. Setup (generates wallet, creates config, approves builder fee)
openbroker setup

# 2. Fund your wallet with USDC on Arbitrum, then deposit at https://app.hyperliquid.xyz/

# 3. Start trading
openbroker account
openbroker buy --coin ETH --size 0.1
```

## Important: Finding Assets Before Trading

**Always search before trading an unfamiliar asset.** Hyperliquid has main perps (ETH, BTC, SOL...), HIP-3 perps (xyz:CL, xyz:GOLD, km:USOIL...), spot markets, and HIP-4 outcome markets. Use search to discover the correct ticker:

```bash
openbroker search --query GOLD              # Find all GOLD markets across all providers
openbroker search --query oil               # Find oil-related assets (CL, BRENTOIL, USOIL...)
openbroker search --query BTC --type perp   # BTC perps only
openbroker search --query NATGAS --type hip3  # HIP-3 only
openbroker search --query BTC --type outcome  # HIP-4 only
openbroker outcomes --query BTC             # Outcome-specific details
```

Or with the `ob_search` plugin tool: `{ "query": "gold" }` or `{ "query": "oil", "type": "hip3" }`

**HIP-3 assets use `dex:COIN` format** — e.g., `xyz:CL` not just `CL`. If you get an error like "No market data found", search for the asset to find the correct prefixed ticker. Common HIP-3 dexes: `xyz`, `flx`, `km`, `hyna`, `vntl`, `cash`.

### Asset IDs (disambiguation)

Every info JSON output includes an `assetId` field — the canonical Hyperliquid asset index. Prefer it over the coin name when persisting references, because the same ticker can exist on multiple providers (e.g. `HYPE` perp, `hyna:HYPE` HIP-3, and `HYPE/USDC` spot all coexist).

| Scope | Formula | Example |
|-------|---------|---------|
| Main perps | universe index | `HYPE` → `159` |
| HIP-3 perps | `100000 + dexIdx * 10000 + assetIdx` | `hyna:HYPE` → `140002` |
| Spot | `10000 + pair.index` | `HYPE/USDC` → `10107` |
| HIP-4 outcomes | `100000000 + (10 * outcomeId + side)` | outcome `123` YES → `100001230` |

```bash
openbroker search HYPE --json | jq '.[] | {coin, assetId, type, provider}'
```

Trading commands still take `--coin <name>` for perps/spot (including HIP-3 `dex:COIN`) — `assetId` is for queries, comparisons, and agent state, not order placement. HIP-4 outcome commands take `--outcome <id|#encoding|+encoding>` plus `--outcome-side yes|no` when using a plain id.

## Troubleshooting: CLI Fallback

If an `ob_*` plugin tool returns unexpected errors, empty results, or crashes, **fall back to the equivalent CLI command** via Bash. The CLI and plugin tools share the same core code, but the CLI has more mature error handling and output.

**Every info command supports `--json`** for structured output. The table below covers the commands with dedicated plugin tools; any other info command (e.g. `spot`, `trades`, `fees`, `order-status`, `rate-limit`, `funding-history`, `all-markets`) can be run as `openbroker <command> --json` for the same effect.

| Plugin Tool | CLI Equivalent |
|-------------|---------------|
| `ob_account` | `openbroker account --json` |
| `ob_positions` | `openbroker positions --json` |
| `ob_funding` | `openbroker funding --json --include-hip3` |
| `ob_markets` | `openbroker markets --json --include-hip3` |
| `ob_search` | `openbroker search --query <QUERY> --json` |
| `ob_spot` | `openbroker spot --json` (or `--balances --json`) |
| `ob_outcomes` | `openbroker outcomes --json` (or `--query <QUERY> --json`) |
| `ob_fills` | `openbroker fills --json` |
| `ob_orders` | `openbroker orders --json` |
| `ob_order_status` | `openbroker order-status --oid <OID> --json` |
| `ob_fees` | `openbroker fees --json` |
| `ob_candles` | `openbroker candles --coin <COIN> --json` |
| `ob_funding_history` | `openbroker funding-history --coin <COIN> --json` |
| `ob_trades` | `openbroker trades --coin <COIN> --json` |
| `ob_rate_limit` | `openbroker rate-limit --json` |
| `ob_funding_scan` | `openbroker funding-scan --json` |
| `ob_buy` | `openbroker buy --coin <COIN> --size <SIZE>` |
| `ob_sell` | `openbroker sell --coin <COIN> --size <SIZE>` |
| `ob_limit` | `openbroker limit --coin <COIN> --side <SIDE> --size <SIZE> --price <PRICE>` |
| `ob_tpsl` | `openbroker tpsl --coin <COIN> --tp <PRICE> --sl <PRICE>` |
| `ob_cancel` | `openbroker cancel --all` or `--coin <COIN>` |
| `ob_outcome_buy` | `openbroker outcome-buy --outcome <ID> --outcome-side yes --size <SIZE>` |
| `ob_outcome_sell` | `openbroker outcome-sell --outcome <ID> --outcome-side yes --size <SIZE>` |
| `ob_auto_run` | `openbroker auto run <script> [--dry]` |
| `ob_auto_stop` | `openbroker auto stop <id>` (or SIGINT if run in foreground) |
| `ob_auto_list` | `openbroker auto list` |

**When to use CLI fallback:**
- Plugin tool returns `null`, empty data, or throws an error
- You need data the plugin tool doesn't expose (e.g., `--verbose` debug output)
- Long-running operations (strategies) — the CLI handles timeouts and progress better

Add `--dry` to any trading CLI command to preview without executing. Add `--json` to info commands for structured output.

## Command Reference

### Setup
```bash
openbroker setup              # One-command setup (wallet + config + builder approval)
openbroker approve-builder --check  # Check builder fee status (for troubleshooting)
```

The `setup` command offers three modes:
1. **Generate fresh wallet** (recommended for agents) — creates a dedicated trading wallet with builder fee auto-approved. No browser steps needed — just fund with USDC and start trading.
2. **Import existing key** — use a private key you already have
3. **Generate API wallet** — creates a restricted wallet that can trade but cannot withdraw. Requires browser approval from a master wallet.

For options 1 and 2, setup saves config and approves the builder fee automatically.
For option 3 (API wallet), see the API Wallet Setup section below.

### Fresh Wallet Setup (Recommended for Agents)

The simplest setup for agents. A fresh wallet is generated, the builder fee is auto-approved, and the agent is ready to trade immediately after funding.

**Flow:**
1. Run `openbroker setup` and choose option 1 ("Generate a fresh wallet")
2. The CLI generates a wallet, saves the config, and approves the builder fee automatically
3. Fund the wallet by sending USDC from your Hyperliquid account to the agent's wallet address using the **Send** feature on https://app.hyperliquid.xyz/. **Funding should be done on Hyperliquid L1 only.**
4. Start trading

### API Wallet Setup (Alternative)

API wallets can place trades on behalf of a master account but **cannot withdraw funds**. Use this if you prefer to keep funds in your existing wallet and only delegate trading access.

**Flow:**
1. Run `openbroker setup` and choose option 3 ("Generate API wallet")
2. The CLI generates a keypair and prints an approval URL (e.g. `https://openbroker.dev/approve?agent=0xABC...`)
3. The agent owner opens the URL in a browser and connects their master wallet (MetaMask etc.)
4. The master wallet signs two transactions: `ApproveAgent` (authorizes the API wallet) and `ApproveBuilderFee` (approves the 1 bps fee)
5. The CLI detects the approval automatically and saves the config

**After setup, the config will contain:**
```
HYPERLIQUID_PRIVATE_KEY=0x...        # API wallet private key
HYPERLIQUID_ACCOUNT_ADDRESS=0x...    # Master account address
HYPERLIQUID_NETWORK=mainnet
```

**Important for agents:** When using an API wallet, pass the approval URL to the agent owner (the human who controls the master wallet). The owner must approve in a browser before the agent can trade. The CLI waits up to 10 minutes for the approval. If it times out, re-run `openbroker setup`.

### Account Info
```bash
openbroker account            # Balance, equity, margin
openbroker account --orders   # Include open orders
openbroker account --address 0xabc...  # Look up another account
openbroker positions          # Open positions with PnL
openbroker positions --coin ETH  # Specific coin
openbroker positions --address 0xabc...  # Another account's positions
```

### Funding Rates
```bash
openbroker funding --top 20   # Top 20 by funding rate
openbroker funding --coin ETH # Specific coin
openbroker funding --top 20 --json  # JSON (includes assetId)
```

### Markets
```bash
openbroker markets --top 30   # Top 30 main perps
openbroker markets --coin BTC # Specific coin
openbroker markets --coin BTC --json  # JSON (includes assetId)
```

### All Markets (Perps + Spot + HIP-3 + HIP-4)
```bash
openbroker all-markets                 # Show all markets
openbroker all-markets --type perp     # Main perps only
openbroker all-markets --type hip3     # HIP-3 perps only
openbroker all-markets --type spot     # Spot markets only
openbroker all-markets --type outcome  # HIP-4 outcome markets only
openbroker all-markets --top 20        # Top 20 by volume
openbroker all-markets --json          # JSON (includes assetId)
```

### Search Markets (Find assets across providers)
```bash
openbroker search --query GOLD    # Find all GOLD markets
openbroker search --query BTC     # Find BTC across all providers
openbroker search --query ETH --type perp  # ETH perps only
openbroker search --query BTC --type outcome  # HIP-4 outcome markets only
openbroker search HYPE --json     # JSON with assetId per result
```

### Spot Markets
```bash
openbroker spot                   # Show all spot markets
openbroker spot --coin PURR       # Show PURR market info
openbroker spot --balances        # Show your spot balances
openbroker spot --balances --address 0xabc...  # Another account's spot balances
openbroker spot --top 20          # Top 20 by volume
openbroker spot --json            # JSON (includes assetId, base, quote)
```

### Trade Fills
```bash
openbroker fills                          # Recent fills
openbroker fills --coin ETH               # ETH fills only
openbroker fills --coin BTC --side buy --top 50
openbroker fills --address 0xabc...       # Another account's fills
```

### Order History
```bash
openbroker orders                         # Recent orders (all statuses)
openbroker orders --open                  # Currently open orders only
openbroker orders --open --coin ETH       # Open orders for a specific coin
openbroker orders --coin ETH --status filled
openbroker orders --top 50
openbroker orders --address 0xabc... --open  # Another account's open orders
```

### Order Status
```bash
openbroker order-status --oid 123456789   # Check specific order
openbroker order-status --oid 0x1234...   # By client order ID
openbroker order-status --oid 123456789 --address 0xabc...  # On another account
openbroker order-status --oid 123456789 --json
```

### Fee Schedule
```bash
openbroker fees                           # Fee tier, rates, and volume
openbroker fees --address 0xabc...        # Another account's fees
openbroker fees --json
```

### Candle Data (OHLCV)
```bash
openbroker candles --coin ETH                           # 24 hourly candles
openbroker candles --coin BTC --interval 4h --bars 48   # 48 four-hour bars
openbroker candles --coin SOL --interval 1d --bars 30   # 30 daily bars
openbroker candles --coin ETH --json                    # JSON (coin, assetId, interval, candles)
```

### Funding History
```bash
openbroker funding-history --coin ETH              # Last 24h
openbroker funding-history --coin BTC --hours 168  # Last 7 days
openbroker funding-history --coin ETH --json       # JSON (coin, assetId, history)
```

### Recent Trades (Tape)
```bash
openbroker trades --coin ETH              # Last 30 trades
openbroker trades --coin BTC --top 50     # Last 50 trades
openbroker trades --coin ETH --json       # JSON (coin, assetId, trades)
```

### Rate Limit
```bash
openbroker rate-limit                     # API usage and capacity
openbroker rate-limit --json
```

### Funding Rate Scanner (Cross-Dex)
```bash
openbroker funding-scan                          # Scan all dexes, >25% threshold
openbroker funding-scan --threshold 50 --pairs   # Show opposing funding pairs
openbroker funding-scan --hip3-only --top 20     # HIP-3 only
openbroker funding-scan --watch --interval 120   # Re-scan every 2 minutes
openbroker funding-scan --json                   # JSON (includes assetId per result)
```

## Trading Commands

### HIP-3 Perp Trading
All trading commands support HIP-3 assets using `dex:COIN` syntax:
```bash
openbroker buy --coin xyz:CL --size 1              # Buy crude oil on xyz dex
openbroker sell --coin xyz:BRENTOIL --size 1        # Sell brent oil
openbroker limit --coin xyz:GOLD --side buy --size 0.1 --price 2500
```

### Market Orders (Quick)
```bash
openbroker buy --coin ETH --size 0.1
openbroker sell --coin BTC --size 0.01
openbroker buy --coin SOL --size 5 --slippage 100  # Custom slippage (bps)
```

### Market Orders (Full)
```bash
openbroker market --coin ETH --side buy --size 0.1
openbroker market --coin BTC --side sell --size 0.01 --slippage 100
```

### Limit Orders
```bash
openbroker limit --coin ETH --side buy --size 1 --price 3000
openbroker limit --coin SOL --side sell --size 10 --price 200 --tif ALO
```

### Set TP/SL on Existing Position
```bash
# Set take profit at $40, stop loss at $30
openbroker tpsl --coin HYPE --tp 40 --sl 30

# Set TP at +10% from entry, SL at entry (breakeven)
openbroker tpsl --coin HYPE --tp +10% --sl entry

# Set only stop loss at -5% from entry
openbroker tpsl --coin ETH --sl -5%

# Partial position TP/SL
openbroker tpsl --coin ETH --tp 4000 --sl 3500 --size 0.5
```

### Trigger Orders (Standalone TP/SL)
```bash
# Take profit: sell when price rises to $40
openbroker trigger --coin HYPE --side sell --size 0.5 --trigger 40 --type tp

# Stop loss: sell when price drops to $30
openbroker trigger --coin HYPE --side sell --size 0.5 --trigger 30 --type sl
```

### Cancel Orders
```bash
openbroker cancel --all           # Cancel all orders
openbroker cancel --coin ETH      # Cancel ETH orders only
openbroker cancel --oid 123456    # Cancel specific order
```

### Spot Orders
Spot trading uses a separate order path with its own asset indices (see Asset IDs section). Pass the base token symbol as `--coin` — quote is always USDC.

```bash
# Market orders (shortcuts)
openbroker spot-buy --coin PURR --size 1000
openbroker spot-sell --coin HYPE --size 5

# Full form (specify --side)
openbroker spot-order --coin PURR --side buy --size 1000

# Limit orders (add --price)
openbroker spot-order --coin HYPE --side sell --size 50 --price 25.50
openbroker spot-order --coin PURR --side buy --size 500 --price 0.20 --tif Alo

# Preview without executing
openbroker spot-buy --coin PURR --size 500 --dry
```

**Spot flags:** `--coin`, `--side`, `--size`, `--price` (omit → market order), `--tif` (`Gtc`/`Ioc`/`Alo`, default `Gtc`), `--slippage` (bps, market orders only), `--dry`, `--verbose`.

### HIP-4 Outcome Trading
Outcome markets are prediction-style YES/NO tokens. The outcome spot coin is `#<encoding>`, the token name is `+<encoding>`, and `encoding = 10 * outcomeId + side` where side `0` is usually YES and side `1` is usually NO.

```bash
openbroker outcomes --query BTC
openbroker outcomes --outcome 123 --side yes --json
openbroker outcomes --balances

openbroker outcome-buy --outcome 123 --outcome-side yes --size 10 --dry
openbroker outcome-buy --outcome 123 --outcome-side no --size 5 --price 0.42
openbroker outcome-sell --outcome #1230 --size 10
openbroker outcome-order --outcome 123 --outcome-side yes --side buy --size 10
```

**Outcome flags:** `--outcome`, `--outcome-side`, `--side`, `--size`, `--price` (omit → market IOC), `--tif` (`Gtc`/`Ioc`/`Alo`, default `Gtc`), `--slippage`, `--sz-decimals`, `--dry`, `--verbose`.

## Advanced Execution

### TWAP (Native Exchange Order)
```bash
# Buy 1 ETH over 30 minutes (exchange handles slicing)
openbroker twap --coin ETH --side buy --size 1 --duration 30

# Sell 0.5 BTC over 2 hours without randomized timing
openbroker twap --coin BTC --side sell --size 0.5 --duration 120 --randomize false

# Reduce-only (close position with TWAP). Note: TWAP uses `--reduce-only`, not `--reduce`
openbroker twap --coin ETH --side sell --size 1 --duration 30 --reduce-only

# Cancel a running TWAP
openbroker twap-cancel --coin ETH --twap-id 77738308

# Check TWAP status
openbroker twap-status --active
```

### Scale In/Out (Grid Orders)
```bash
# Place 5 buy orders ranging 2% below current price
openbroker scale --coin ETH --side buy --size 1 --levels 5 --range 2

# Scale out with exponential distribution
openbroker scale --coin BTC --side sell --size 0.5 --levels 4 --range 3 --distribution exponential --reduce
```

### Bracket Order (Entry + TP + SL)
```bash
# Long ETH with 3% take profit and 1.5% stop loss
openbroker bracket --coin ETH --side buy --size 0.5 --tp 3 --sl 1.5

# Short with limit entry
openbroker bracket --coin BTC --side sell --size 0.1 --entry limit --price 100000 --tp 5 --sl 2
```

### Chase Order (Follow Price)
```bash
# Chase buy with ALO orders until filled
openbroker chase --coin ETH --side buy --size 0.5 --timeout 300

# Aggressive chase with tight offset
openbroker chase --coin SOL --side buy --size 10 --offset 2 --timeout 60
```

## Order Types

### Limit Orders vs Trigger Orders

**Limit Orders** (`openbroker limit`):
- Execute immediately if price is met
- Rest on the order book until filled or cancelled
- A limit sell BELOW current price fills immediately (taker)
- NOT suitable for stop losses

**Trigger Orders** (`openbroker trigger`, `openbroker tpsl`):
- Stay dormant until trigger price is reached
- Only activate when price hits the trigger level
- Proper way to set stop losses and take profits
- Won't fill prematurely

### When to Use Each

| Scenario | Command |
|----------|---------|
| Buy at specific price below market | `openbroker limit` |
| Sell at specific price above market | `openbroker limit` |
| Stop loss (exit if price drops) | `openbroker trigger --type sl` |
| Take profit (exit at target) | `openbroker trigger --type tp` |
| Add TP/SL to existing position | `openbroker tpsl` |

## Common Arguments

All commands support `--dry` for dry run (preview without executing).

| Argument | Description |
|----------|-------------|
| `--coin` | Asset symbol (ETH, BTC, SOL, HYPE, etc.) |
| `--side` | Order direction: `buy` or `sell` |
| `--size` | Order size in base asset |
| `--price` | Limit price |
| `--dry` | Preview without executing |
| `--help` | Show command help |

### Order Arguments
| Argument | Description |
|----------|-------------|
| `--trigger` | Trigger price (for trigger orders) |
| `--type` | Trigger type: `tp` or `sl` |
| `--slippage` | Slippage tolerance in bps (for market orders) |
| `--tif` | Time in force: GTC, IOC, ALO |
| `--reduce` | Reduce-only order |

### TP/SL Price Formats
| Format | Example | Description |
|--------|---------|-------------|
| Absolute | `--tp 40` | Price of $40 |
| Percentage up | `--tp +10%` | 10% above entry |
| Percentage down | `--sl -5%` | 5% below entry |
| Entry price | `--sl entry` | Breakeven stop |

## Configuration

Config is loaded from (in priority order):
1. Environment variables
2. `.env` in current directory
3. `~/.openbroker/.env` (global config)

Run `openbroker setup` to create the global config interactively.

| Variable | Required | Description |
|----------|----------|-------------|
| `HYPERLIQUID_PRIVATE_KEY` | Yes | Wallet private key (0x...) |
| `HYPERLIQUID_NETWORK` | No | `mainnet` (default) or `testnet` |
| `HYPERLIQUID_ACCOUNT_ADDRESS` | No | Master account address (required for API wallets) |
| `OB_DASHBOARD_URL` | No | Dashboard API URL for forwarding audit notes, metrics, and agent actions (e.g. `http://localhost:3001`) |

The builder fee (1 bps / 0.01%) is hardcoded and not configurable.

## OpenClaw Plugin (Optional)

This skill works standalone via Bash — every command above runs through the `openbroker` CLI. For enhanced features, the same `openbroker` npm package also ships as an **OpenClaw plugin** that you can enable alongside this skill.

### What the plugin adds

- **Structured agent tools** (`ob_account`, `ob_buy`, `ob_limit`, etc.) — typed tool calls with proper input schemas instead of Bash strings. The agent gets structured JSON responses.
- **Background position watcher** — polls your Hyperliquid account every 30s and sends webhook alerts when positions open/close, PnL moves significantly, or margin usage gets dangerous.
- **Automation tools** (`ob_auto_run`, `ob_auto_stop`, `ob_auto_list`) — start, stop, and manage custom trading automations from within the agent.
- **CLI commands** — `openclaw ob status` and `openclaw ob watch` for inspecting the watcher.

### Enable the plugin

The plugin is bundled in the same `openbroker` npm package. To enable it in your OpenClaw config:

```yaml
plugins:
  entries:
    openbroker:
      enabled: true
      config:
        hooksToken: "your-hooks-secret"   # Required for watcher alerts
        watcher:
          enabled: true
          pollIntervalMs: 30000
          pnlChangeThresholdPct: 5
          marginUsageWarningPct: 80
```

The plugin reads wallet credentials from `~/.openbroker/.env` (set up by `openbroker setup`), so you don't need to duplicate `privateKey` in the plugin config unless you want to override.

### Webhook setup for watcher alerts

For the position watcher and automations to send alerts to the agent, you must enable webhooks in your OpenClaw gateway config and add a hook mapping. This is a manual configuration step — plugins cannot auto-configure gateway settings.

**1. Generate a hook token** — any secure random string:
```bash
openssl rand -hex 32
```

**2. Enable hooks and add a mapping** in your `openclaw.json` (or `openclaw.yaml`) deployment config:
```json
"hooks": {
  "enabled": true,
  "path": "/hooks",
  "token": "<your-generated-token>",
  "allowedAgentIds": ["hooks", "main", "openbroker"],
  "mappings": [
    {
      "id": "main",
      "match": {
        "path": "openbroker"
      },
      "action": "agent",
      "wakeMode": "now",
      "name": "Openbroker",
      "agentId": "main",
      "deliver": true,
      "channel": "last",
      "model": "anthropic/claude-sonnet-4-6"
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `token` | Shared secret — must match `hooksToken` in the plugin config |
| `allowedAgentIds` | Agent IDs allowed to receive webhook requests |
| `mappings[].match.path` | Matches the webhook path sent by the plugin (always `"openbroker"`) |
| `mappings[].wakeMode` | `"now"` triggers an immediate agent turn. `"next-heartbeat"` queues for the next scheduled heartbeat |
| `mappings[].deliver` | If `true`, the agent's response is delivered to the user via the configured channel |
| `mappings[].channel` | Delivery channel: `"last"` (most recent), `"slack"`, `"telegram"`, `"discord"`, `"whatsapp"`, etc. |
| `mappings[].model` | Model override for webhook-triggered turns. Optional — uses deployment default if omitted |

**3. Set the same token in your plugin config:**
```yaml
plugins:
  entries:
    openbroker:
      enabled: true
      config:
        hooksToken: "<your-generated-token>"   # Same token as hooks.token
        watcher:
          enabled: true
```

**4. Restart the gateway** and verify:
```bash
openclaw ob status
```

The watcher sends alerts to `POST /hooks/agent` with `Authorization: Bearer <token>`. The gateway matches the request against the mapping and triggers an agent turn. Without hooks enabled, the watcher still tracks state (accessible via `ob_watcher_status`), but it can't wake the agent.

### Using with or without the plugin

- **Skill only (no plugin):** Use Bash commands (`openbroker buy --coin ETH --size 0.1`). No background monitoring.
- **Skill + plugin:** The agent prefers the `ob_*` tools when available (structured data), falls back to Bash for commands not covered by tools (strategies, scale). Background watcher sends alerts automatically.

## Trading Automations

Automations let you write custom event-driven trading logic as TypeScript scripts. Write exactly the logic you need and OpenBroker handles the polling, event detection, and SDK access.

### IMPORTANT: Bundled Examples Are References, Not Ready-Made Strategies

OpenBroker ships bundled automation examples (`dca`, `grid`, `funding-arb`, `mm-spread`, `mm-maker`) that demonstrate common patterns. **These examples are meant to be read and learned from — not run directly as production strategies.** When the user asks for a strategy (e.g. "run a DCA on HYPE"), you should:

1. Read the relevant bundled example source code to understand the automation API patterns
2. Write a **custom automation** tailored to the user's specific requirements (coin, size, thresholds, risk parameters, TP/SL logic, etc.)
3. Save it to `~/.openbroker/automations/` and run it with `openbroker auto run`

Do NOT simply run `openbroker auto run --example dca --set coin=HYPE`. The examples use generic defaults and lack the nuanced risk management, position sizing, and TP/SL logic that a real strategy needs. Always write a purpose-built automation.

To view bundled examples and their config schemas:
```bash
openbroker auto examples    # List examples with config fields
```

Available examples: `dca`, `grid`, `funding-arb`, `mm-spread`, `mm-maker`, `price-alert`

### How Automations Work

An automation is a `.ts` file that exports a default function. The function receives an `AutomationAPI` with the full Hyperliquid client, typed event subscriptions, persistent state, and a logger. The runtime connects a WebSocket for real-time price and order events, with REST polling every 30s as a heartbeat for position/margin data. Use `--no-ws` to disable WebSocket and fall back to pure REST polling (every 10s).

### Writing an Automation

Create a `.ts` file in `~/.openbroker/automations/` (or any path):

```typescript
// ~/.openbroker/automations/funding-scalp.ts
export default function(api) {
  const COIN = 'ETH';

  api.on('funding_update', async ({ coin, annualized }) => {
    if (coin !== COIN) return;

    if (annualized > 0.5 && !api.state.get('isShort')) {
      api.log.info('High positive funding — going short');
      await api.client.marketOrder(COIN, false, 0.1);
      api.state.set('isShort', true);
    } else if (annualized < -0.1 && api.state.get('isShort')) {
      api.log.info('Funding normalized — closing short');
      await api.client.marketOrder(COIN, true, 0.1);
      api.state.set('isShort', false);
    }
  });

  api.onStop(async () => {
    if (api.state.get('isShort')) {
      api.log.warn('Closing short on shutdown');
      await api.client.marketOrder('ETH', true, 0.1);
      api.state.set('isShort', false);
    }
  });
}
```

### AutomationAPI Reference

| Property / Method | Description |
|-------------------|-------------|
| `api.client` | Full HyperliquidClient — `marketOrder()`, `limitOrder()`, `triggerOrder()`, `cancelAll()`, `getUserStateAll()`, `getAllMids()`, `updateLeverage()`, and 35+ more methods |
| `api.on(event, handler)` | Subscribe to a market/account event (see Events below) |
| `api.every(ms, handler)` | Run a handler on a recurring interval (aligned to poll loop) |
| `api.onStart(handler)` | Called after all handlers are registered, before first poll |
| `api.onStop(handler)` | Called on shutdown (SIGINT). Use for cleanup — close positions, cancel orders |
| `api.onError(handler)` | Called when a handler throws. Error is already logged — use for recovery logic |
| `api.state.get(key)` | Get a persisted value (survives restarts, stored in `~/.openbroker/state/`) |
| `api.state.set(key, value)` | Set a persisted value |
| `api.state.delete(key)` | Delete a persisted value |
| `api.state.clear()` | Clear all state |
| `api.publish(message, options?)` | Send a message to the OpenClaw agent via webhook. Triggers an agent turn — the agent receives the message and can notify the user, take action, etc. Returns `true` if delivered. Options: `{ name?, wakeMode?, deliver?, channel? }` |
| `api.log.info/warn/error/debug(msg)` | Structured logger |
| `api.audit.record(kind, payload?)` | Add a custom audit note to the local SQLite trail for later reporting |
| `api.audit.metric(name, value, tags?)` | Add a numeric metric to the local SQLite trail |
| `api.utils` | `roundPrice`, `roundSize`, `sleep`, `normalizeCoin`, `formatUsd`, `annualizeFundingRate` |
| `api.id` | Automation ID (filename or `--id` flag) |
| `api.dryRun` | `true` if running with `--dry` (write methods are intercepted) |

Automations now write a local audit trail automatically to `~/.openbroker/automation-audit.sqlite`. The runtime records run config, logs, state changes, write actions, order updates, fills, user events, and per-poll account snapshots so you can generate performance reports later.

**Dashboard Forwarding:** When `OB_DASHBOARD_URL` is set (e.g. `http://localhost:3001`), audit notes, metrics, and trade actions are automatically forwarded to the OpenBroker Vaults dashboard API in real time. The vault address is read from `HYPERSTABLE_VAULT_ADDRESS` or `VAULT`. Forwarding is fire-and-forget — it never blocks the automation or causes errors if the dashboard is unreachable.

### Events

| Event | Payload | When |
|-------|---------|------|
| `tick` | `{ timestamp, pollCount }` | Every poll cycle (default: 10s) |
| `price_change` | `{ coin, oldPrice, newPrice, changePct }` | Mid price moved > 0.01% between polls |
| `funding_update` | `{ coin, fundingRate, annualized, premium }` | Every poll for all assets |
| `position_opened` | `{ coin, side, size, entryPrice }` | New position detected |
| `position_closed` | `{ coin, previousSize, entryPrice }` | Position no longer present |
| `position_changed` | `{ coin, oldSize, newSize, entryPrice }` | Position size changed |
| `pnl_threshold` | `{ coin, unrealizedPnl, changePct, positionValue }` | PnL moved > 5% of position value |
| `margin_warning` | `{ marginUsedPct, equity, marginUsed }` | Margin usage > 80% |

### Event Details — Choosing the Right Event

#### `tick` — The universal heartbeat
Fires **every single poll cycle** (default: 10s) regardless of market conditions. Use this when you need to check something on every poll — absolute price thresholds, custom conditions, periodic account checks. This is the most reliable event because it always fires.

**Payload:** `{ timestamp: number, pollCount: number }`

**When to use:**
- Checking if a price is above/below an absolute threshold (e.g. "alert me when ETH < $3000")
- Custom conditions that don't fit other events (e.g. "if I have no positions and funding is high, enter")
- Periodic tasks that need to run every poll (though `api.every()` is better for longer intervals)

**Example — absolute price alert:**
```typescript
api.on('tick', async () => {
  const mids = await api.client.getAllMids();
  const price = parseFloat(mids['HYPE']);
  if (price < 38 && !api.state.get('alerted')) {
    api.state.set('alerted', true);
    await api.publish(`HYPE dropped below $38 — now at $${price.toFixed(3)}`);
  }
});
```

**Note:** `tick` does not include price data in its payload — you must fetch it yourself via `api.client.getAllMids()`. This is because tick fires before any other event processing. If you only care about price movements, use `price_change` instead.

#### `price_change` — Relative price movements
Fires when a coin's mid price moves **≥ 0.01%** compared to the previous poll. This filters out rounding noise while catching virtually any real price movement. The comparison is between consecutive polls (not from a fixed baseline), so it detects incremental changes.

**Payload:** `{ coin: string, oldPrice: number, newPrice: number, changePct: number }`

**When to use:**
- Reacting to price movements (breakouts, momentum, mean reversion)
- Monitoring specific coins for volatility
- Building price-triggered entry/exit logic

**When NOT to use:**
- Checking if price is above/below a fixed threshold — use `tick` instead, because `price_change` only fires on relative movement between polls. During slow drifts (e.g. price slowly declining $0.001/s), the change between any two 10s polls may be < 0.01%, so the event won't fire even though the price has crossed your threshold.

**Example — momentum detector:**
```typescript
api.on('price_change', async ({ coin, changePct, newPrice }) => {
  if (coin !== 'ETH') return;
  if (changePct > 0.5) {
    api.log.info(`ETH surging +${changePct.toFixed(2)}% — price $${newPrice}`);
    // Enter long on strong upward momentum
  }
});
```

#### `funding_update` — Funding rate data
Fires **every poll** for **every asset** that has funding rate data. This is high-frequency — if there are 150 perp assets, this fires 150 times per poll. Filter by coin in your handler.

**Payload:** `{ coin: string, fundingRate: number, annualized: number, premium: number }`
- `fundingRate` — the raw hourly funding rate (e.g. 0.0001 = 0.01%/hr)
- `annualized` — annualized rate (fundingRate × 8760 × 100, as a percentage)
- `premium` — the premium component

**When to use:**
- Funding rate arbitrage strategies
- Monitoring for extreme funding (entry/exit signals)
- Scanning for highest/lowest funding across all assets

**Example — funding scalp:**
```typescript
api.on('funding_update', async ({ coin, annualized }) => {
  if (coin !== 'ETH') return;
  if (annualized > 50 && !api.state.get('isShort')) {
    api.log.info(`ETH funding at ${annualized.toFixed(1)}% annualized — shorting`);
    await api.client.marketOrder('ETH', false, 0.1);
    api.state.set('isShort', true);
  }
});
```

#### `position_opened` — New position detected
Fires when a position appears that wasn't present in the previous poll. Useful for tracking entries made by other systems or confirming your own orders filled.

**Payload:** `{ coin: string, side: 'long' | 'short', size: number, entryPrice: number }`

**When to use:**
- Setting TP/SL on new positions automatically
- Logging/alerting when positions are opened (by you or another system)
- Starting position-specific monitoring

**Example — auto TP/SL on new positions:**
```typescript
api.on('position_opened', async ({ coin, side, size, entryPrice }) => {
  const tpPrice = side === 'long' ? entryPrice * 1.05 : entryPrice * 0.95;
  const slPrice = side === 'long' ? entryPrice * 0.97 : entryPrice * 1.03;
  await api.client.takeProfit(coin, side !== 'long', size, tpPrice);
  await api.client.stopLoss(coin, side !== 'long', size, slPrice);
  api.log.info(`Set TP at ${tpPrice} / SL at ${slPrice} for ${coin}`);
});
```

#### `position_closed` — Position gone
Fires when a position that existed in the previous poll is no longer present. The position was either closed by you, liquidated, or filled by TP/SL.

**Payload:** `{ coin: string, previousSize: number, entryPrice: number }`

**When to use:**
- Logging/alerting when positions close
- Cleaning up related orders or state
- Re-entry logic after a position closes

**Example:**
```typescript
api.on('position_closed', async ({ coin, previousSize, entryPrice }) => {
  api.log.info(`${coin} position closed (was ${previousSize} @ ${entryPrice})`);
  api.state.delete(`${coin}_tp`);
  await api.publish(`Position closed: ${coin} (entry: $${entryPrice})`);
});
```

#### `position_changed` — Size or direction changed
Fires when an existing position's size changes (partial close, add to position, or flip direction). Does NOT fire when a new position opens or an existing one fully closes — use `position_opened` and `position_closed` for those.

**Payload:** `{ coin: string, oldSize: number, newSize: number, entryPrice: number }`
- `oldSize`/`newSize` are signed: positive = long, negative = short

**When to use:**
- Detecting partial closes or position scaling
- Adjusting TP/SL when position size changes
- Tracking DCA entries

**Example:**
```typescript
api.on('position_changed', async ({ coin, oldSize, newSize }) => {
  if (Math.abs(newSize) > Math.abs(oldSize)) {
    api.log.info(`${coin} position increased: ${oldSize} → ${newSize}`);
  } else {
    api.log.info(`${coin} position reduced: ${oldSize} → ${newSize}`);
  }
});
```

#### `pnl_threshold` — Significant PnL movement
Fires when unrealized PnL changes by **≥ 5% of position value** between consecutive polls. This is a large move detector — useful for risk management alerts rather than routine monitoring.

**Payload:** `{ coin: string, unrealizedPnl: number, changePct: number, positionValue: number }`
- `changePct` — the PnL change as a percentage of total position value (not % of PnL itself)

**When to use:**
- Risk alerts for large PnL swings
- Auto-close or reduce positions on sudden adverse moves
- Escalating alerts to the user via `api.publish()`

**Example:**
```typescript
api.on('pnl_threshold', async ({ coin, unrealizedPnl, changePct }) => {
  if (unrealizedPnl < 0) {
    await api.publish(
      `⚠️ ${coin} PnL dropped sharply: $${unrealizedPnl.toFixed(2)} (${changePct.toFixed(1)}% of position)`,
      { name: 'pnl-alert' },
    );
  }
});
```

#### `margin_warning` — High margin usage
Fires when margin usage exceeds **80%** of equity. After the first trigger, it only fires again if margin usage increases by another 5 percentage points (prevents spam). Resets when margin drops back below 80%.

**Payload:** `{ marginUsedPct: number, equity: number, marginUsed: number }`

**When to use:**
- Automated risk reduction (close smallest position to free margin)
- Alerting the user before liquidation risk
- Pausing new entries when margin is high

**Example:**
```typescript
api.on('margin_warning', async ({ marginUsedPct, equity }) => {
  await api.publish(
    `🚨 Margin at ${marginUsedPct.toFixed(1)}% — equity: $${equity.toFixed(2)}. Consider reducing exposure.`,
    { name: 'margin-alert' },
  );
});
```

#### `order_update` — Real-time order lifecycle (WebSocket)
Fires instantly when any order changes status: `open`, `filled`, `canceled`, `triggered`, `rejected`, `marginCanceled`, `liquidatedCanceled`, `badAloPxRejected`, and 20+ other statuses. Requires WebSocket (enabled by default).

**Payload:** `{ coin: string, oid: number, side: 'buy' | 'sell', size: number, price: number, origSize: number, status: string, statusTimestamp: number }`

**Example:**
```typescript
api.on('order_update', async ({ coin, oid, status, side, size, price }) => {
  if (status === 'filled') {
    api.log.info(`Order ${oid} filled: ${side} ${size} ${coin} @ $${price}`);
  } else if (status === 'canceled' || status.includes('Rejected')) {
    api.log.warn(`Order ${oid} ${status}: ${coin}`);
  }
});
```

#### `liquidation` — Liquidation alert (WebSocket only)
Fires when the account is liquidated. This event is **only available via WebSocket** — there is no REST polling equivalent.

**Payload:** `{ lid: number, liquidator: string, liquidatedUser: string, liquidatedNtlPos: number, liquidatedAccountValue: number }`

**Example:**
```typescript
api.on('liquidation', async ({ liquidatedNtlPos, liquidatedAccountValue }) => {
  await api.publish(
    `LIQUIDATED: $${liquidatedNtlPos.toFixed(2)} notional, account value: $${liquidatedAccountValue.toFixed(2)}`,
    { name: 'liquidation-alert' },
  );
});
```

### WebSocket Real-Time Data

Automations use **WebSocket by default** for real-time market and account events. The runtime subscribes to:
- **allMids** — price updates for all assets (drives `price_change` events in real-time)
- **orderUpdates** — order lifecycle events (drives `order_update` and `order_filled`)
- **userFills** — trade fill details with PnL and fees
- **userEvents** — liquidation alerts, funding payments, system cancellations

REST polling continues as a **heartbeat** (every 60s by default) for position/margin/funding events that aren't covered by WebSocket. If the WebSocket connection fails, the runtime falls back to full REST polling (every 10s) automatically.

To disable WebSocket (pure REST polling):
```bash
openbroker auto run my-strategy.ts --no-ws
```

### Choosing the Right Event — Quick Guide

| Use case | Best event | Why |
|----------|-----------|-----|
| Alert when price crosses a fixed level | `tick` | Fires every poll — no minimum change threshold |
| React to price momentum/volatility | `price_change` | Real-time via WebSocket, provides relative change data |
| Funding rate strategy | `funding_update` | Gives annualized rate directly |
| Auto TP/SL on new positions | `position_opened` | Fires exactly when a new position appears |
| Log when positions close | `position_closed` | Fires when position disappears |
| Track position scaling | `position_changed` | Fires on size changes only |
| Risk management — PnL spikes | `pnl_threshold` | Only fires on large moves (≥5% of position value) |
| Risk management — margin | `margin_warning` | Fires at 80%+ margin usage |
| React instantly to order fills/rejects | `order_update` | Real-time via WebSocket — sub-second latency |
| Liquidation alerts | `liquidation` | WebSocket only — no REST equivalent |
| Periodic task (DCA, rebalance) | `api.every(ms, fn)` | Better than tick for longer intervals |

### Client Methods Available

The `api.client` object exposes the full `HyperliquidClient`. All `coin` params accept HIP-3 prefixed tickers (e.g. `xyz:CL`). Optional `user` params default to the configured wallet address.

#### Trading

| Method | Description |
|--------|-------------|
| `marketOrder(coin, isBuy, size, slippageBps?, leverage?)` | Market order via IOC limit at mid ± slippage. Returns `OrderResponse` |
| `limitOrder(coin, isBuy, size, price, tif?, reduceOnly?, leverage?)` | Limit order. `tif`: `'Gtc'` (default), `'Ioc'`, `'Alo'`. Returns `OrderResponse` |
| `triggerOrder(coin, isBuy, size, triggerPrice, limitPrice, tpsl, reduceOnly?, leverage?)` | Trigger (conditional) order. `tpsl`: `'tp'` or `'sl'`. Activates when price hits `triggerPrice`, then fills as limit at `limitPrice`. Returns `OrderResponse` |
| `stopLoss(coin, isBuy, size, triggerPrice, slippageBps?)` | Stop loss shortcut. Sets limit price with slippage buffer (default 100 bps / 1%) to ensure fill. `reduceOnly` is always true. Returns `OrderResponse` |
| `takeProfit(coin, isBuy, size, triggerPrice)` | Take profit shortcut. Limit price = trigger price (favorable direction). `reduceOnly` is always true. Returns `OrderResponse` |
| `cancel(coin, oid)` | Cancel a single order by numeric OID. Returns `CancelResponse` |
| `cancelAll(coin?)` | Cancel all open orders. If `coin` is provided, only cancels orders for that asset. Returns `CancelResponse[]` |
| `order(coin, isBuy, size, price, orderType, reduceOnly?, includeBuilder?, leverage?)` | Low-level order placement. `orderType`: `{ limit: { tif: 'Gtc' | 'Ioc' | 'Alo' } }`. Automatically injects builder fee, rounds price/size, and handles HIP-3 margin setup. Returns `OrderResponse` |
| `outcomeMarketOrder(outcomeRef, outcomeSide, isBuy, size, slippageBps?, szDecimalsOverride?)` | HIP-4 outcome market order via IOC limit. `outcomeRef` can be an outcome id, `#encoding`, or `+encoding`. Returns `OrderResponse` |
| `outcomeLimitOrder(outcomeRef, outcomeSide, isBuy, size, price, tif?, szDecimalsOverride?)` | HIP-4 outcome limit order. `outcomeSide`: `yes`/`no` or `0`/`1` for plain ids. Returns `OrderResponse` |

#### Market Data

| Method | Returns |
|--------|---------|
| `getAllMids()` | `Record<string, string>` — mid prices for assets. HIP-4 outcomes use `#<encoding>` keys when available |
| `getMetaAndAssetCtxs()` | `MetaAndAssetCtxs` — market metadata (universe of assets with `szDecimals`, `maxLeverage`) and asset contexts (funding, open interest, volume, mark/oracle prices) |
| `getL2Book(coin)` | `{ bids, asks, bestBid, bestAsk, midPrice, spread, spreadBps }` — L2 order book with computed spread |
| `getRecentTrades(coin)` | `Array<{ coin, side, px, sz, time, hash, tid }>` — recent trade tape. `side`: `'B'` (buy) or `'A'` (sell) |
| `getCandleSnapshot(coin, interval, startTime, endTime?)` | `Array<{ t, T, s, i, o, c, h, l, v, n }>` — OHLCV candles. `interval`: `'1m'`, `'5m'`, `'15m'`, `'1h'`, `'4h'`, `'1d'`. Times are Unix ms |
| `getFundingHistory(coin, startTime, endTime?)` | `Array<{ coin, fundingRate, premium, time }>` — historical hourly funding rates |
| `getPredictedFundings()` | `Array<[coin, Array<[venue, { fundingRate, nextFundingTime }]>]>` — predicted funding rates across all venues |
| `getPerpDexs()` | `Array<{ name, fullName, deployer } | null>` — list of perp DEXs. Index 0 is `null` (main), rest are HIP-3 |
| `getAllPerpMetas()` | `Array<{ dexName, meta, assetCtxs }>` — metadata + contexts for every perp DEX (main + all HIP-3) |
| `getSpotMeta()` | `{ tokens, universe }` — spot market metadata (token info, trading pairs) |
| `getSpotMetaAndAssetCtxs()` | `{ meta, assetCtxs }` — spot metadata + price/volume contexts |
| `getOutcomeMeta()` | HIP-4 raw outcome metadata (`outcomes`, `questions`) |
| `getOutcomeMarkets()` | Normalized HIP-4 markets with parsed descriptions, side encodings, asset ids, token decimals, and price context |
| `resolveOutcomeRef(ref, side?)` | Convert outcome id / `#encoding` / `+encoding` into `{ outcome, side, encoding, coin, tokenName, assetId }` |
| `getTokenDetails(tokenId)` | Token details: supply, deployer, prices. Returns `null` if not found |

#### Account

| Method | Returns |
|--------|---------|
| `getUserStateAll(user?)` | `ClearinghouseState` — full account state across all dexes: `marginSummary` (accountValue, totalMarginUsed, withdrawable), `crossMarginSummary`, and `assetPositions[]` (each with `position.coin`, `.szi`, `.entryPx`, `.unrealizedPnl`, `.positionValue`, `.leverage`, `.marginUsed`, `.liquidationPx`) |
| `getUserState(user?, dex?)` | `ClearinghouseState` — account state for a single dex (omit `dex` for main perps) |
| `getOpenOrders(user?)` | `OpenOrder[]` — all open orders across all dexes. Each: `{ coin, side, limitPx, sz, oid, timestamp, orderType }` |
| `getUserFills(user?, aggregateByTime?)` | `Array<{ coin, px, sz, side, time, closedPnl, fee, oid, tid, crossed, builderFee }>` — trade fill history. `side`: `'B'` (buy) or `'A'` (sell) |
| `getHistoricalOrders(user?)` | `Array<{ order: { coin, side, limitPx, sz, origSz, oid, timestamp, orderType, tif, triggerCondition, triggerPx, isTrigger, isPositionTpsl, reduceOnly }, status, statusTimestamp }>` — all orders (filled, cancelled, etc.) |
| `getOrderStatus(oid, user?)` | `{ status, order? }` — status of a specific order by numeric OID or string CLOID |
| `getUserFunding(user?, startTime?, endTime?)` | `Array<{ time, hash, delta: { coin, usdc, szi, fundingRate } }>` — funding payments received/paid |
| `getUserFees(user?)` | `{ dailyUserVlm, feeSchedule, userCrossRate, userAddRate, activeReferralDiscount, activeStakingDiscount }` — fee tier, rates, and volume |
| `getUserRateLimit(user?)` | `{ cumVlm, nRequestsUsed, nRequestsCap, nRequestsSurplus }` — API rate limit status |
| `getSpotBalances(user?)` | `{ balances: Array<{ coin, token, hold, total, entryNtl }> }` — spot token balances |
| `getSubAccounts(user?)` | `Array<{ subAccountUser, name }>` — sub-accounts for a master wallet |
| `getAccountMode(user?)` | `string` — account abstraction mode: `'standard'`, `'unified'`, `'portfolio'`, or `'dexAbstraction'` |
| `isUnifiedAccount(user?)` | `boolean` — `true` if unified or portfolio margin (shared USDC across dexes) |

#### Leverage & Config

| Method | Description |
|--------|-------------|
| `updateLeverage(coin, leverage, isCross?)` | Set leverage. `isCross` defaults to `true` (cross margin). HIP-3 assets are forced to isolated and clamped to their max leverage |
| `approveBuilderFee(maxFeeRate?, builder?)` | Approve builder fee (must be called from main wallet, not API wallet). Default rate: `'0.1%'` |
| `getMaxBuilderFee(user?, builder?)` | Check approved builder fee. Returns fee string (e.g. `'0.01%'`) or `null` if not approved |

#### Utility Properties

| Property / Method | Description |
|-------------------|-------------|
| `getAssetIndex(coin)` | Get numeric asset index for a coin (used internally for order wire) |
| `getSzDecimals(coin)` | Get size decimal precision for a coin |
| `isHip3(coin)` | Check if a coin is a HIP-3 asset |
| `getCoinDex(coin)` | Get dex name for a coin (`null` for main perps) |
| `getAllAssetNames()` | Get all known asset names (main + HIP-3) |
| `getHip3AssetNames()` | Get only HIP-3 asset names |
| `invalidateMetaCache()` | Force refresh of market metadata on next call |

#### Utility Functions (`api.utils`)

| Function | Description |
|----------|-------------|
| `roundPrice(price, szDecimals, isSpot?)` | Round price to 5 significant figures (max 6 decimals perp, 8 spot) |
| `roundSize(size, szDecimals)` | Round size to asset-specific decimal precision |
| `sleep(ms)` | Promise-based delay |
| `normalizeCoin(coin)` | Normalize coin name (uppercase, trim whitespace) |
| `formatUsd(amount)` | Format number as USD string (e.g. `$1,234.56`) |
| `annualizeFundingRate(hourlyRate)` | Convert hourly funding rate to annualized percentage |

### Example: Price Breakout

```typescript
// ~/.openbroker/automations/breakout.ts
export default function(api) {
  const COIN = 'ETH';
  const BREAKOUT_PCT = 2;  // 2% move triggers entry
  const SIZE = 0.5;
  let basePrice = null;

  api.onStart(async () => {
    const mids = await api.client.getAllMids();
    basePrice = parseFloat(mids[COIN]);
    api.log.info(`Watching ${COIN} from $${basePrice} for ${BREAKOUT_PCT}% breakout`);
  });

  api.on('price_change', async ({ coin, newPrice }) => {
    if (coin !== COIN || !basePrice) return;
    const totalChange = ((newPrice - basePrice) / basePrice) * 100;

    if (Math.abs(totalChange) >= BREAKOUT_PCT && !api.state.get('inPosition')) {
      const side = totalChange > 0;  // true = long, false = short
      api.log.info(`Breakout! ${totalChange.toFixed(2)}% — entering ${side ? 'long' : 'short'}`);
      await api.client.marketOrder(COIN, side, SIZE);
      api.state.set('inPosition', true);
    }
  });
}
```

### Example: Scheduled DCA

```typescript
// ~/.openbroker/automations/hourly-dca.ts
export default function(api) {
  const COIN = 'ETH';
  const USD_PER_BUY = 100;

  // Buy $100 of ETH every hour
  api.every(60 * 60 * 1000, async () => {
    const mids = await api.client.getAllMids();
    const price = parseFloat(mids[COIN]);
    const size = parseFloat(api.utils.roundSize(USD_PER_BUY / price, 4));
    await api.client.marketOrder(COIN, true, size);
    const count = (api.state.get('buyCount') || 0) + 1;
    api.state.set('buyCount', count);
    api.log.info(`DCA #${count}: bought ${size} ${COIN} at $${price}`);
  });
}
```

### Example: Margin Guardian

```typescript
// ~/.openbroker/automations/margin-guard.ts
export default function(api) {
  api.on('margin_warning', async ({ marginUsedPct, equity }) => {
    api.log.warn(`Margin at ${marginUsedPct.toFixed(1)}% — reducing positions`);

    // Close the smallest position to free margin
    const state = await api.client.getUserStateAll();
    const positions = state.assetPositions
      .filter(p => parseFloat(p.position.szi) !== 0)
      .sort((a, b) => Math.abs(parseFloat(a.position.positionValue)) - Math.abs(parseFloat(b.position.positionValue)));

    if (positions.length > 0) {
      const pos = positions[0].position;
      const size = Math.abs(parseFloat(pos.szi));
      const isBuy = parseFloat(pos.szi) < 0; // Close short = buy, close long = sell
      api.log.info(`Closing smallest position: ${pos.coin} (${pos.szi})`);
      await api.client.marketOrder(pos.coin, isBuy, size);
    }
  });
}
```

### Publishing to the Agent (Webhooks)

Use `api.publish()` to send messages back to the OpenClaw agent. This triggers an agent turn — the agent receives the message and can notify the user via their preferred channel, take trading actions, or log the event.

```typescript
// Simple notification
await api.publish(`ETH broke above $4000 — current price: $${price}`);

// With options
await api.publish(`Margin at ${pct}% — positions at risk`, {
  name: 'margin-alert',           // appears in logs
  wakeMode: 'now',                // 'now' (default) or 'next-heartbeat'
  channel: 'slack',               // target channel (optional)
});
```

`api.publish()` returns `true` if delivered, `false` if webhooks are not configured (no hooks token). It requires `OPENCLAW_HOOKS_TOKEN` to be set (automatically configured when running as an OpenClaw plugin).

**Example: Price alert automation with publish**
```typescript
// ~/.openbroker/automations/price-alert.ts
export default function(api) {
  const COIN = 'ETH';
  const THRESHOLD = 4000;

  api.on('price_change', async ({ coin, newPrice, changePct }) => {
    if (coin !== COIN) return;

    const crossed = api.state.get<boolean>('crossed', false);
    if (!crossed && newPrice >= THRESHOLD) {
      api.state.set('crossed', true);
      await api.publish(
        `${COIN} crossed above $${THRESHOLD}! Price: $${newPrice.toFixed(2)} (+${changePct.toFixed(2)}%)`,
      );
    } else if (crossed && newPrice < THRESHOLD) {
      api.state.set('crossed', false);
    }
  });
}
```

### Running Automations

**CLI:**
```bash
openbroker auto run my-strategy --dry       # Test without trading
openbroker auto run ./funding-scalp.ts      # Run from path
openbroker auto run my-strategy --poll 5000 # Poll every 5s
openbroker auto run my-strategy --no-ws     # Disable WebSocket, pure REST polling
openbroker auto run --example dca --set coin=HYPE --set amount=50 --dry  # Run bundled example
openbroker auto examples                    # List bundled examples with config
openbroker auto list                        # Show available scripts
openbroker auto status                      # Show running automations
openbroker auto stop <id>                   # Unregister an automation (won't auto-restart)
openbroker auto report <id>                 # Read the local audit report (logs, trades, metrics) for an automation
openbroker auto clean                       # Remove stale entries from the registry
```

**Plugin tools (for OpenClaw agents):**
- `ob_auto_run` — `{ "script": "funding-scalp", "dry": true }` — start an automation
- `ob_auto_run` — `{ "example": "dca", "config": { "coin": "HYPE", "amount": 50 }, "dry": true }` — run a bundled example
- `ob_auto_stop` — `{ "id": "funding-scalp" }` — stop a running automation
- `ob_auto_list` — `{}` — list available automations, bundled examples with config schemas, and running automations

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--dry` | Intercept write methods — no real trades | false |
| `--verbose` | Show debug output | false |
| `--id <name>` | Custom automation ID | filename |
| `--poll <ms>` | Poll interval in milliseconds | 10000 |
| `--no-ws` | Disable WebSocket; fall back to REST-only polling | WebSocket on |
| `--example <name>` | Run a bundled example automation | - |
| `--set key=value` | Set config values (repeatable) | - |

**Inspecting automations after they run:**
- `openbroker auto report <id>` — reads the local SQLite audit trail at `~/.openbroker/automation-audit.sqlite` and prints a summary of logs, write actions, fills, PnL, and custom metrics recorded via `api.audit.record()` / `api.audit.metric()`. Use this to review what a strategy actually did.
- `openbroker auto clean` — prunes registry entries for automations that are no longer running or whose script file is gone. Safe to run anytime.

**Guidelines for agents writing automations:**

**Risk & Safety (mandatory):**
- Always attach a liquidation monitoring automation to every open position. Subscribe to `margin_warning` and `pnl_threshold` events so the user is never blindsided by liquidation risk. If no margin/liquidation automation is already running, create one before placing trades.
- Use `api.publish()` to notify the user of important events — position opens/closes, TP/SL triggers, large PnL swings, margin warnings, errors, and any situation that requires human attention. Do NOT silently handle critical events.
- Always register an `api.onStop()` handler to clean up — cancel open orders and close positions (or at minimum alert the user) on shutdown. Never leave orphaned orders or unmanaged positions.
- Do NOT use `--dry` unless the user explicitly asks for it. Automations should run live by default.
- Never place trades without validating that sufficient margin is available. Check account state before sizing orders.
- Cap position sizes relative to account equity. Do not risk more than a reasonable percentage of equity on a single trade unless the user explicitly specifies the size.
- Always set TP/SL on new positions — either within the automation or by confirming the user has them set. Unprotected positions are a liability.

**State & Reliability:**
- Use `api.state` to track position state, entry prices, and flags across restarts. Never rely on in-memory variables alone — automations persist across gateway restarts and are automatically restarted.
- Use idempotency guards (`api.state.get`/`set`) to prevent duplicate orders. Events can fire multiple times for the same condition across polls — always check state before placing orders.
- The runtime catches errors per handler — one failing handler won't crash others, but always handle expected errors (e.g. order rejection, insufficient margin) gracefully within handlers.

**Communication:**
- Use `api.publish()` to send alerts/events back to the OpenClaw agent — do NOT manually construct webhook requests.
- Publish on: position opened/closed, TP/SL triggered, PnL threshold exceeded, margin warning, automation errors, and any automated trade execution. The user should always know what the automation did and why.
- Include actionable context in publish messages — coin, price, size, PnL, and what happened — so the user can make informed decisions without checking the terminal.

**General:**
- Scripts are loaded from `~/.openbroker/automations/` by name, or from any absolute path.
- All trading commands support HIP-3 assets (`api.client.marketOrder('xyz:CL', true, 1)`).
- Automations persist across gateway restarts — they are automatically restarted when the gateway comes back up.
- Prefer `api.every(ms, fn)` over `tick` for periodic tasks with intervals longer than the poll cycle.

## Risk Warning

- Always use `--dry` first to preview orders
- Start with small sizes on testnet (`HYPERLIQUID_NETWORK=testnet`)
- Monitor positions and liquidation prices
- Use `--reduce` for closing positions only
