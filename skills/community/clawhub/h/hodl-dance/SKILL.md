# HODL.DANCE Agent Skill

Trade memecoins on the [HODL.DANCE](https://hodl.dance) bonding curve launchpad on BSC (BNB Chain).

## Overview

HODL.DANCE is a memecoin launchpad on BSC using a CPMM bonding curve (r × t = k).
Tokens trade on the curve until 19 BNB is raised, then liquidity auto-migrates to PancakeSwap V3.

- **Network:** BSC Mainnet (Chain ID: 56)
- **Native currency:** BNB
- **Fee:** 1% per trade (buy and sell)
- **API:** [https://hodl.dance/api](https://hodl.dance/api) (public, no API key required)
- **Docs:** [https://docs.hodl.dance](https://docs.hodl.dance)

## Installation

```bash
npm install -g @hodl-dance/skill
# or without installing:
npx @hodl-dance/skill <command>
```

## Credentials

Required only for `create-token`, `buy-token` and `sell-token`:

```bash
export HODL_PRIVATE_KEY=0xyour_private_key
export HODL_RPC_URL=https://bsc-dataseed.binance.org/  # optional
```

> ⚠️ The private key is used locally only to sign transactions. Never share it.

---

## Commands

### `get-tokens`

List tokens with filtering and sorting. Returns full token objects including `bonding_curve_address`.

```bash
hodl-skill get-tokens
hodl-skill get-tokens --sort=market_cap --limit=10
hodl-skill get-tokens --sort=volume --verified=true
hodl-skill get-tokens --sort=progress --finalized=false
hodl-skill get-tokens --search=pepe --limit=5
```

**Options:** `--sort=newest|market_cap|progress|volume` · `--limit=N` (max 100) · `--offset=N` · `--verified=true|false` · `--finalized=true|false` · `--search=<text>`

**Key output fields per token:**
- `address` — token contract address
- `bonding_curve_address` — ⭐ use this in quote/buy-token/sell-token
- `market_cap_usd`, `progress_percent` (0–100 toward PancakeSwap migration)
- `finalized` — if true, bonding curve is closed, token is on PancakeSwap V3
- `price_change_24h`, `trades_24h`, `volume_24h_bnb`

---

### `get-token <tokenAddress>`

Full token details + 20 most recent trades.

```bash
hodl-skill get-token 0x1a2b3c...
```

Returns same fields as `get-tokens` plus `recent_trades[]`.

---

### `get-trades <tokenAddress>`

Trade history for a specific token.

```bash
hodl-skill get-trades 0x1a2b3c...
hodl-skill get-trades 0x1a2b3c... --type=buy --limit=20
```

**Options:** `--type=all|buy|sell` · `--limit=N` (max 500) · `--offset=N`

---

### `quote <bondingCurveAddress> buy|sell <amount>`

**Simulate** trade output using live on-chain state. No transaction sent, no gas used.

```bash
# How many tokens will I get for 0.1 BNB?
hodl-skill quote 0xbc1234... buy 0.1

# How much BNB will I get for selling 500000 tokens?
hodl-skill quote 0xbc1234... sell 500000
```

> Always run `quote` before `buy-token` or `sell-token` to verify expected amounts.

---

### `create-token`

Deploy a new token + bonding curve on HODL.DANCE. Uploads logo to IPFS, then sends on-chain transaction.

```bash
hodl-skill create-token --name="Moon Cat" --symbol=MCAT --logo=./logo.png

hodl-skill create-token \
  --name="Moon Cat" \
  --symbol=MCAT \
  --logo=./logo.png \
  --category=meme \
  --description="The cat that dances on the moon" \
  --twitter="https://x.com/mooncat" \
  --telegram="https://t.me/mooncat" \
  --website="https://mooncat.io" \
  --initial-buy=0.1
```

**Requires:** `HODL_PRIVATE_KEY`

**Options:**
- `--name` — token name, 3–40 characters *(required)*
- `--symbol` — token symbol, 1–10 characters *(required)*
- `--logo` — path to local image file PNG/JPG/WEBP, max 5MB *(required)*
- `--category` — `meme|ai|games|social|other` (default: `meme`)
- `--description` — token description, max 500 characters
- `--website` — `https://...`
- `--twitter` — `https://x.com/...`
- `--telegram` — `https://t.me/...`
- `--initial-buy` — BNB amount to buy in the same transaction (default: `0`)

> Deploy fee: **0.0001 BNB**. If `--initial-buy` is set, total value = `0.0001 + initial-buy`.

**Output:** `tx_hash`, `block_number`, `gas_used`, `token_address`, `bonding_curve_address`, `name`, `symbol`, `category`, `logo_ipfs`, `initial_buy_bnb`

---

### `buy-token <bondingCurveAddress> <bnbAmount> [--recipient=0x...]`

Buy tokens using BNB. Sends transaction on-chain.

```bash
hodl-skill buy-token 0xbc1234... 0.1
hodl-skill buy-token 0xbc1234... 0.5 --recipient=0xfriend...
```

**Requires:** `HODL_PRIVATE_KEY`

**Output:** `tx_hash`, `bnb_spent`, `tokens_received`, `tokens_estimated`, `fee_bnb`, `block_number`, `gas_used`

---

### `sell-token <bondingCurveAddress> <tokenAmount>`

Sell tokens, receive BNB.

```bash
hodl-skill sell-token 0xbc1234... 1000000
```

**Requires:** `HODL_PRIVATE_KEY`

> ⚠️ **Selling requires ERC20 `approve` before `sellTokens`.**
> This skill handles it automatically in two steps:
> 1. Checks current `allowance` — if insufficient, sends `approve()` transaction first
> 2. Sends `sellTokens()` transaction
>
> The output field `approve_was_needed: true/false` tells you whether approve was sent.
> If approve was needed, `approve_tx_hash` contains its transaction hash.
> Total gas cost may cover 2 transactions if approve was required.

**Output:** `tx_hash`, `tokens_sold`, `bnb_received`, `bnb_estimated`, `fee_bnb`, `approve_tx_hash`, `approve_was_needed`, `block_number`, `gas_used`

---

## Response Format

All commands output JSON to stdout:

```json
{ "success": true, "data": { ... } }
```

Errors:

```json
{ "success": false, "error": { "code": "TOKEN_FINALIZED", "message": "..." } }
```

Exit code `0` = success, `1` = error.

### Error Codes

| Code | Meaning |
|---|---|
| `MISSING_ARG` | Required argument not provided |
| `INVALID_ARG` | Invalid argument value (e.g. logo file not found) |
| `TOKEN_FINALIZED` | Token migrated to PancakeSwap V3, bonding curve closed |
| `INSUFFICIENT_BALANCE` | Not enough tokens to sell |
| `ERROR` | General error (message contains details) |

---

## Typical Agent Workflow

```
1. get-tokens --sort=volume --limit=10
   → find tokens with activity, note bonding_curve_address

2. get-token <tokenAddress>
   → check progress_percent, finalized, recent_trades

3. quote <bondingCurveAddress> buy 0.1
   → verify tokens_out before committing

4. buy-token <bondingCurveAddress> 0.1
   → execute, save tx_hash and tokens_received

5. [later] quote <bondingCurveAddress> sell <tokens_received>
   → check exit value

6. sell-token <bondingCurveAddress> <tokens_received>
   → approve sent automatically if needed, then sell
   → check approve_was_needed in output
```

### Token Launch Workflow

```
1. create-token --name="..." --symbol=... --logo=./logo.png --initial-buy=0.1
   → deploys token + bonding curve, returns token_address and bonding_curve_address

2. quote <bonding_curve_address> buy 0.5
   → verify expected tokens before buying more

3. buy-token <bonding_curve_address> 0.5
   → accumulate position
```

---

## Contract Addresses (BSC Mainnet, Chain ID 56)

| Contract | Address |
|---|---|
| Token Factory | `0x99A1F02f56E8356e6E90A880DBb1be6EC7485737` |
| Bonding Curve Template | `0xea508aD6B550E94aC45831F265B2bD5346d06700` |

> Each token has its own unique Bonding Curve instance.
> Always fetch `bonding_curve_address` from `get-token`, `get-tokens` or `create-token` — do not use the template address.