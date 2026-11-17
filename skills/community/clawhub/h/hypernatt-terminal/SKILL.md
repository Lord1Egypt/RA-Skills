---
name: hypernatt-terminal
description: >-
  Onboarding skill for HyperNatt Terminal remote MCP (exactly 6 tools v2.8.0):
  get_agent_manifest, get_liq_radar, swap_via_nattswap, get_execution_quote,
  compare_execution_context, reconcile_execution. Docs + call order only -
  no local exec/shell/files. Read-only market microstructure for crypto trading
  agents (any venue). Not trade advice. get_liq_radar = $0.001 USDC via x402.
version: 1.6.1
author: DIALLOUBE-RESEARCH
license: MIT
homepage: https://hypernatt.com
permissions:
  exec: false
  filesystem: false
  network:
    - hypernatt.com
    - docs.cdp.coinbase.com
  env: []
  tools:
    - mcp
metadata:
  openclaw:
    requires:
      bins: []
    envVars: []
    primaryEnv: null
  hermes:
    tags:
      [
        MCP,
        x402,
        crypto,
        trading,
        perpetual,
        liquidation,
        microstructure,
        market-data,
        swap,
      ]
    related_skills: [native-mcp, mcporter, hypernatt-liq-radar]
---

# HyperNatt Terminal MCP

**What this skill is:** onboarding text for a **remote** MCP server.

**What this skill is NOT:** a local bot, vault control, or a 14-tool terminal.
Live surface = **exactly 6 tools - v2.8.0**.

## Declared capabilities (honest)

| Capability | Declared |
|------------|----------|
| Local exec / shell | **No** |
| Local filesystem | **No** |
| Env vars required | **None** |
| Outbound network | `https://hypernatt.com` ; optional Coinbase Agentic Wallet docs |
| Tools | Remote MCP connector only |

## Connect

| Resource | URL |
|----------|-----|
| Platform | https://hypernatt.com |
| MCP | https://hypernatt.com/mcp/protocol |
| Server card | https://hypernatt.com/.well-known/mcp/server-card.json |
| Source | https://github.com/DIALLOUBE-RESEARCH/hypernatt-terminal |
| Security | https://github.com/DIALLOUBE-RESEARCH/hypernatt-terminal/blob/main/SECURITY.md |
| Trading-first skill | https://github.com/DIALLOUBE-RESEARCH/hypernatt-terminal/blob/main/skills/hypernatt-liq-radar/SKILL.md |

## Tool surface (6 only)

1. **get_agent_manifest** - Free - Catalog + journeys
2. **get_liq_radar** - $0.001 x402 - Forced-order / liquidation map
3. **swap_via_nattswap** - Free at MCP (you sign) - Li.Fi route
4. **get_execution_quote** - $0.001 - Depth, VWAP, spread and fees for an order size
5. **compare_execution_context** - $0.001 - Changes since a saved baseline
6. **reconcile_execution** - $0.001 - Compare supplied fills with that baseline

Symbols: BTC ETH SOL BNB XRP HYPE ZEC. Radar defaults to BTC; execution quotes require symbol.

Daily MCP trial: one free call per paid tool and per token per client each UTC day. Four tools x seven tokens = up to 28 independent trials; then 0.001 USDC per call. Read trial_policy_v2 and free_tier_status_v1 on the same MCP connection for current availability. A zero daily_cap is the separate credit pool, not the intro allowance.

## Example

Use the connected remote MCP tool interface (no shell command):

```json
{"name":"get_agent_manifest","arguments":{}}
```

Then, if liquidation terrain is the requested task:

```json
{"name":"get_liq_radar","arguments":{"symbol":"ETH"}}
```

## Execution-context workflow

For a Hyperliquid order, call `get_execution_quote` and save the returned baseline. Reuse it in `compare_execution_context`; after your own execution, send fills to `reconcile_execution`. These tools never submit orders. All seven symbols are supported; quantity must be a decimal string in token units. Read `delivery` and quality flags. See [execution-context.md](../../docs/execution-context.md).

## Trading-agent loop

1. Connect and call `get_agent_manifest` (free); choose `journeys_v1` by intent.
2. For liquidation terrain, use `get_liq_radar`. For Hyperliquid order costs, use `get_execution_quote` with `symbol`, `side`, `quantity_base`. Neither path requires buying the other.
3. Keep the returned `baseline` unchanged. Compare against it when another check is useful; keep the next baseline. Freeze a separate `pre_order_baseline` before your own execution.
4. After your own execution, call `reconcile_execution` with that pre-order baseline and `fills_dataset` for one order. Read quality and delivery flags throughout.
5. Use `swap_via_nattswap` separately for a Li.Fi route. You sign your own transaction. No mandatory paid polling.

## Wallet / x402

Paid calls need a USDC buyer wallet. **Base** = EIP-3009 (`@x402/evm`). **Solana** = SVM exact (`@x402/svm`) — live rail; an EVM signer cannot pay it. A Base HTTP 200 is not a Solana payment. See [docs/x402-pay.md](../../docs/x402-pay.md). Use the buyer wallet already configured in the host application and its payment authorization rules. If no wallet is configured, explain the available free trials and let the user choose whether to set up payments separately.

Optional wallet setup documentation for the user: https://docs.cdp.coinbase.com/agentic-wallet/mcp/welcome

This remote-only onboarding skill does not install or launch local software, create wallets, or change the host configuration.

This skill never asks for private keys or scrapes env secrets.

## Honest claims

- Not trade advice - no custody - no performance promise
- Do not advertise more than 6 MCP tools
- Vault/platform pages are not Terminal MCP P&L
