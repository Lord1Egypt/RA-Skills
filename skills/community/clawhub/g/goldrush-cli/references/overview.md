# GoldRush CLI

## Quick Reference

| Item | Value |
|------|-------|
| **Install** | `npx @covalenthq/goldrush-cli` |
| **Authentication** | `goldrush auth` (stores key in OS keychain) |
| **MCP Setup** | `goldrush install` (registers as tool for Claude) |
| **Commands** | 17 commands across portfolio, market, trading, and utilities |
| **Chains** | 100+ chains (same as Foundational API) |
| **Streaming** | Real-time data via Streaming API for `new_pairs`, `ohlcv_pairs`, `watch` |

---

GoldRush CLI is a terminal-first tool for blockchain data. 17 commands, 100+ chains, real-time streaming, and native MCP support for AI agents. One install, and you've got live onchain data in your terminal or piped directly into Claude.

```bash
npx @covalenthq/goldrush-cli
```

## Two Modes, Same Data

GoldRush CLI serves both humans and AI agents from a single tool:

- **Humans** get a rich terminal experience with live charts, interactive tables, and formatted output.
- **Agents** get MCP tools with structured, streaming data via the [Model Context Protocol](https://modelcontextprotocol.io/).

## What It Does

Seventeen commands across portfolio management, market discovery, trading intelligence, and agent integration.

**Portfolio & Wallets:** Check token balances across 100+ chains, view transfer history, and stream real-time wallet activity.
  

  **Commands: `balances`, `transfers`, `watch`**

**Market Discovery:** Stream new DEX liquidity pairs as they launch and view live OHLCV candlestick charts in ASCII.
  

  **Commands: `new_pairs`, `ohlcv_pairs`**

**Trading Intelligence:** Find top traders for any token, check real-time gas prices, and search tokens by name or address.
  

  **Commands: `traders`, `gas`, `search`**

**Agent Integration:** Register GoldRush as an MCP tool provider for Claude in one command. Agents call GoldRush commands natively.
  

  **Commands: `install`, `auth`, `config`, `status`**

## MCP: Built for Agents

GoldRush CLI is an [MCP server](https://modelcontextprotocol.io/). When you run `goldrush install`, it registers GoldRush as a tool provider for Claude. The agent can then call GoldRush commands the same way it calls any other tool - no wrappers, no glue code.

Three core loops define how agents use blockchain data:

1. **Continuous Market Monitoring** - An agent subscribes to `new_pairs` and receives every new liquidity pair in real time. It evaluates, filters, scores, and decides whether to act.
2. **Wallet Surveillance** - An agent watches specific wallets using `watch`. Whale wallets, smart money, protocol treasuries. Every swap, transfer, and deposit surfaces in real time.
3. **Portfolio Intelligence** - An agent pulls `balances` on a schedule, analyzes composition across chains, evaluates concentration risk, and recommends rebalancing.

These aren't one-shot queries - they're persistent loops. Subscribe, process, act, repeat.

## Get Started

### CLI Quickstart

Three commands to go from zero to streaming blockchain data in your terminal.

---

## Prerequisites

Using GoldRush CLI requires an API key.

### Vibe Coders

$10/mo - Built for solo builders and AI-native workflows.

### Teams

$250/mo - Production-grade with 50 RPS and priority support.

## Install and Authenticate

Run the CLI with `npx` - no global install needed:

```bash
npx @covalenthq/goldrush-cli auth
```

This prompts you for your API key and stores it securely in your OS keychain (not a config file).

After the first run, you can use `goldrush` directly without `npx`.

## Query Wallet Balances

Get a full token portfolio for any address across 100+ chains:

```bash
goldrush balances aave.eth eth-mainnet
```

This returns ERC20s, native tokens, NFTs, USD values, and 24h changes in a formatted table.

## Stream New DEX Pairs

Watch new liquidity pairs launch in real time:

```bash
goldrush new_pairs solana-mainnet raydium
```

Filter by protocol, navigate with arrow keys, and copy addresses to clipboard. Supports 35+ protocol integrations across 9 chains.

## Set Up MCP for AI Agents

Register GoldRush as a native tool provider for Claude:

```bash
goldrush install
```

That's it. Claude can now call GoldRush commands directly - no wrappers or manual JSON configuration needed. This works with both Claude Desktop and Claude Code.

For manual MCP configuration (Cursor, Windsurf, or custom setups), see the **MCP Server docs**.

## What's Next

### Command Reference

Full reference for all 17 CLI commands with usage examples.

### Streaming API

The real-time data layer that powers `new_pairs`, `ohlcv_pairs`, and `watch`.

---

# Command Reference

## Portfolio & Wallets

### `goldrush balances`

Full token portfolio across 100+ chains. ERC20s, native tokens, NFTs, USD values, and 24h changes.

```bash
goldrush balances  
```

```bash
goldrush balances eth-mainnet vitalik.eth
```

### `goldrush transfers`

Transfer history for any wallet - inbound, outbound, and token details.

```bash
goldrush transfers  
```

### `goldrush watch`

Real-time wallet activity streaming. Swaps, transfers, and deposits as they happen.

```bash
goldrush watch  
```

```bash
goldrush watch 0xbaed383ede0e5d9d72430661f3285daa77e9439f base-mainnet
```

This is the command you leave running in a tmux pane. It streams continuously until you stop it.

## Market Discovery

### `goldrush new_pairs`

Live stream of new DEX liquidity pairs as they're created. Supports 35+ protocol integrations across 9 chains: Uniswap V2/V3, PancakeSwap, Raydium, Pump.fun, Moonshot, Meteora, Orca, Shadow, Clanker, Virtuals, nad.fun, and more.

```bash
goldrush new_pairs  [protocols...]
```

```bash
goldrush new_pairs solana-mainnet raydium pump-fun
```

Filter by protocol, navigate with arrow keys, and copy addresses to clipboard.

### `goldrush ohlcv_pairs`

Live OHLCV candlestick charts rendered in ASCII. Configurable intervals from 1 second to 1 day.

```bash
goldrush ohlcv_pairs   [-i interval] [-t timeframe]
```

```bash
goldrush ohlcv_pairs 0x9c087Eb773291e50CF6c6a90ef0F4500e349B903 base-mainnet -i 1m -t 1h
```

## Trading Intelligence

### `goldrush traders`

Top traders for any token, ranked by unrealized PnL. See who's accumulating and who's dumping.

```bash
goldrush traders  
```

### `goldrush gas`

Real-time gas price estimates by transaction type.

```bash
goldrush gas [chain]
```

### `goldrush search`

Find any token by name, symbol, or contract address.

```bash
goldrush search 
```

## Utilities

| Command | Description |
| --- | --- |
| `goldrush chains` | List every supported chain |
| `goldrush auth` | Set your API key (stored in your OS keychain, not a config file) |
| `goldrush install` | Configure Claude Desktop or Claude Code for MCP integration in one command |
| `goldrush config` | View or update settings like proxy port, default chain, and quote currency |
| `goldrush status` | Check API key validity and proxy connectivity |
| `goldrush logout` | Clear API key and session data from your OS keychain |