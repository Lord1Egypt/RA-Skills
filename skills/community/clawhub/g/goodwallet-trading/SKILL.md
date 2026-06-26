---
name: goodwallet-trading
description: >
  Blockchain trading tools extending GoodWallet MPC agentic wallets. Adds ERC20 transfers,
  token approvals, DEX swaps (Uniswap V2), arbitrary contract calls, balance checking, and
  token info queries — all MPC-signed via Sodot threshold ECDSA.
  Trigger when the user mentions "trade", "swap tokens", "send ERC20", "approve tokens",
  "token balance", "contract call", "DEX", "Uniswap", or wants to interact with DeFi
  using their GoodWallet.
---

# GoodWallet Trading

Extends the `goodwallet` skill with blockchain trading capabilities. All transactions are MPC-signed via the same Sodot threshold ECDSA signing service.

**Prerequisite:** The user must first authorize via the `goodwallet` skill (`auth` + `pair`). Credentials are shared via `~/.config/goodwallet/config.json`.

All commands are run via `npx goodwallet-trading@0.2.0`.

**Important:** Do not share technical details (key types, signature formats, internal paths). Run commands and report outcomes in plain language.

## Setup

If the user hasn't authorized yet, run the goodwallet auth flow first:

```bash
npx goodwallet@0.2.0 auth
# Show the URL to the user, then immediately:
npx goodwallet@0.2.0 pair
```

Once paired, all goodwallet-trading commands will work automatically.

## Commands

### balance — Check ETH and ERC20 balances

```bash
npx goodwallet-trading@0.2.0 balance
npx goodwallet-trading@0.2.0 balance --token <erc20-address>
```

### erc20-send — Send ERC20 tokens

```bash
npx goodwallet-trading@0.2.0 erc20-send --to <address> --amount <amount> --token <erc20-address>
```

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--to <address>` | `-t` | Yes | Recipient address |
| `--amount <amount>` | `-a` | Yes | Amount (human-readable, e.g. `10.5`) |
| `--token <address>` | | Yes | ERC20 token contract |

### approve — Approve token spending

```bash
npx goodwallet-trading@0.2.0 approve --token <erc20-address> --spender <address>
npx goodwallet-trading@0.2.0 approve --token <erc20-address> --spender <address> --amount 100
```

Without `--amount`, approves unlimited spending.

### contract-call — Call any smart contract

The most powerful command — execute arbitrary contract calls with MPC signing.

```bash
npx goodwallet-trading@0.2.0 contract-call --to <contract> --data <calldata-hex>
npx goodwallet-trading@0.2.0 contract-call --to <contract> --data <calldata-hex> --value 0.1
```

| Flag | Required | Description |
|------|----------|-------------|
| `--to <address>` | Yes | Contract address |
| `--data <hex>` | Yes | Calldata (hex with 0x prefix) |
| `--value <ether>` | No | ETH to send with call (default: 0) |

### swap — Uniswap V2 DEX swap

```bash
npx goodwallet-trading@0.2.0 swap --router <router-address> --from-token ETH --to-token <token-address> --amount 0.1
npx goodwallet-trading@0.2.0 swap --router <router-address> --from-token <token-a> --to-token <token-b> --amount 100
```

| Flag | Required | Description |
|------|----------|-------------|
| `--router <address>` | Yes | Uniswap V2 router address |
| `--from-token <address\|ETH>` | Yes | Token to sell (or "ETH") |
| `--to-token <address\|ETH>` | Yes | Token to buy (or "ETH") |
| `--amount <amount>` | Yes | Amount to swap |
| `--slippage <percent>` | No | Slippage tolerance (default: 1%) |

### token-info — Get ERC20 token details

```bash
npx goodwallet-trading@0.2.0 token-info --token <erc20-address>
```

Returns: name, symbol, decimals, total supply, your balance.

### allowance — Check approved spending

```bash
npx goodwallet-trading@0.2.0 allowance --token <erc20-address> --spender <address>
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SIGN_URL` | `sign.goodwallet.dev` | Signing service endpoint |
| `RPC_URL` | Alchemy Hoodi endpoint | Override RPC URL |

## Network

Currently configured for **Hoodi testnet** (chain ID 560048). Explorer: https://hoodi.etherscan.io/

## File Locations

| File | Purpose |
|------|---------|
| `~/.config/goodwallet/config.json` | Shared credentials from goodwallet auth |

## Typical Workflow

```bash
# 1. Auth (if not already done)
npx goodwallet@0.2.0 auth
npx goodwallet@0.2.0 pair

# 2. Check balance
npx goodwallet-trading@0.2.0 balance

# 3. Send ERC20 tokens
npx goodwallet-trading@0.2.0 erc20-send --to 0x... --amount 10 --token 0x...

# 4. Approve DEX router
npx goodwallet-trading@0.2.0 approve --token 0x... --spender 0x...

# 5. Swap on DEX
npx goodwallet-trading@0.2.0 swap --router 0x... --from-token ETH --to-token 0x... --amount 0.1

# 6. Arbitrary contract call
npx goodwallet-trading@0.2.0 contract-call --to 0x... --data 0xabcdef... --value 0.05
```
