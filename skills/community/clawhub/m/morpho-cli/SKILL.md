---
name: morpho-cli
description: >
  Interact with the Morpho lending protocol using the CLI. Use this skill when the user asks to:
  query vault APYs, TVL, or allocation strategies ("What's the best USDC vault on Base?");
  query market rates, utilization, or LLTV ("Show me ETH/USDC markets on Ethereum");
  check user positions, balances, or health ("What are my Morpho positions?");
  deposit into or withdraw from a vault ("Deposit 1000 USDC into Steakhouse vault");
  supply collateral, borrow, or repay on a market ("Borrow 5000 USDC against my WETH");
  prepare or simulate any Morpho transaction.
---

# morpho-cli

> **Experimental (pre-v1.0)** — Command syntax, response schemas, and available operations may change. Always verify critical outputs independently.

Query Morpho protocol data and build unsigned transactions. All commands output JSON to stdout. No private keys needed.

```bash
npx @morpho-org/cli <command> [options]
```

Supported chains: `base`, `ethereum`. Every command requires `--chain`.

## Response Schemas

- **[Read commands](references/read.md)** — exact JSON shapes for query-vaults, get-vault, query-markets, get-market, get-positions, get-position
- **[Write commands](references/write.md)** — exact JSON shapes for prepare-\*, simulate-transactions

## Quick Reference

```bash
# Read — query protocol state
npx @morpho-org/cli query-vaults    --chain base [--asset-symbol USDC] [--asset-address 0x...] [--sort apy_desc|apy_asc|tvl_desc|tvl_asc] [--limit 5] [--skip 0] [--fields address,name,symbol,apyPct,tvl,tvlUsd,feePct]
npx @morpho-org/cli get-vault       --chain base --address 0x...
npx @morpho-org/cli query-markets   --chain base --loan-asset 0x... --collateral-asset 0x... [--sort-by supplyApy|borrowApy|netSupplyApy|netBorrowApy|supplyAssetsUsd|borrowAssetsUsd|totalLiquidityUsd] [--sort-direction asc|desc] [--limit 10] [--skip 0] [--fields supplyApy,borrowApy,totalSupply,totalBorrow,totalCollateral,totalLiquidity,supplyAssetsUsd,borrowAssetsUsd,collateralAssetsUsd,liquidityAssetsUsd]
npx @morpho-org/cli get-market      --chain base --id 0x...
npx @morpho-org/cli get-positions   --chain base --user-address 0x... [--vault-address 0x...] [--market-id 0x...]
npx @morpho-org/cli get-position    --chain base --user-address 0x... [--vault-address 0x...]

# Write — prepare unsigned transactions (simulation runs by default; add --no-simulate to skip)
npx @morpho-org/cli prepare-deposit              --chain base --vault-address 0x... --user-address 0x... --amount 1000
npx @morpho-org/cli prepare-withdraw             --chain base --vault-address 0x... --user-address 0x... --amount max
npx @morpho-org/cli prepare-supply               --chain base --market-id 0x... --user-address 0x... --amount 5000
npx @morpho-org/cli prepare-borrow               --chain base --market-id 0x... --user-address 0x... --borrow-amount 1
npx @morpho-org/cli prepare-repay                --chain base --market-id 0x... --user-address 0x... --amount max
npx @morpho-org/cli prepare-supply-collateral    --chain base --market-id 0x... --user-address 0x... --amount 5000
npx @morpho-org/cli prepare-withdraw-collateral  --chain base --market-id 0x... --user-address 0x... --amount max

# Simulate — standalone re-simulation or arbitrary transaction simulation
npx @morpho-org/cli simulate-transactions --chain base --from 0x... --transactions '<JSON>' --analysis-context '<JSON>'

# Utility
npx @morpho-org/cli health-check
npx @morpho-org/cli get-supported-chains
```

## Write Workflow: Prepare → Present

Every write operation follows two steps. Simulation runs automatically inside `prepare-*`.

1. **Prepare** — run a `prepare-*` command. The CLI handles token decimals, allowances, approvals, and simulation automatically. Returns `{operation, simulation}` where `operation` has transactions/summary/warnings/preview and `simulation` has execution results, gas, and post-state analysis. Use `--no-simulate` to skip simulation.
2. **Present** — show the summary, list of unsigned transactions, simulation results, and any warnings (low health factor, partial liquidity) in tabular format. If `simulation.allSucceeded` is false — diagnose before presenting.

Use `simulate-transactions` separately only for re-simulating with different parameters or simulating arbitrary transactions.


## Simulation Failures

| Revert | Cause | What to do |
|--------|-------|------------|
| `ERC20: insufficient allowance` | Missing approval | Re-prepare — CLI should include approvals automatically |
| `ERC4626ExceededMaxWithdraw` | Vault liquidity insufficient | Reduce amount (see below) |
| `insufficient balance` | User lacks tokens | Tell the user |
| Custom error hex | Protocol-specific | Query state with `get-market` or `get-vault` to diagnose |

## Partial Withdrawal

If `prepare-withdraw --amount max` returns a liquidity warning:
1. Parse the safe amount from `summary`, apply ~1% buffer (`parsedAmount * 0.99`)
2. Re-call `prepare-withdraw` with the buffered amount, then simulate
3. Tell the user: remaining locked assets free up as borrowers repay

## Safety Rules

1. **Check simulation before presenting** — simulation runs by default; check `simulation.allSucceeded` before presenting
2. **Never sign or broadcast** — unsigned payloads only
3. **Watch health factor** for borrows — warn if below 1.1
4. **Communicate liquidity constraints** clearly for partial withdrawals

## CLI Errors

When a `npx @morpho-org/cli` command fails, **stop and report the error to the user**. Do not:
- Retry with different parameters you invented
- Fall back to alternative tools or APIs
- Attempt to work around missing required options
- Pipe output through `jq` or other filters — use the CLI's built-in flags (`--fields`, `--sort-by`, `--limit`, etc.) to shape the response


## Common Mistakes

- Forgetting `--chain` — every command requires it, there is no default
- Using chain IDs (`1`, `8453`) instead of names (`ethereum`, `base`)
- Displaying raw amounts without dividing by `10^decimals` — `"2000000000"` USDC is `2000`, not 2 billion
- Assuming 18 decimals — USDC/USDT have 6
- Passing raw units as `--amount` — CLI expects human-readable (`1000` not `1000000000`)
- Using `--no-simulate` without reason — simulation is on by default; only skip when debugging or for speed
- Ignoring `simulation.allSucceeded === false` — diagnose before presenting
