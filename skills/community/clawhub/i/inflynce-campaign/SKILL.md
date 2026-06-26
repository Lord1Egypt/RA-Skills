---
name: inflynce-create-campaign
description: Create and launch Inflynce Boost campaigns to promote any https:// link (tweet, website, Farcaster cast, etc.) by paying USDC rewards to real users on Base. Use this skill when: boosting any content, creating a marketing campaign, promoting a link for visibility. Each campaign requires a 0.25 USDC payment on Base before creation. Your campaign budget is distributed as rewards to users who explore the promoted link. Inflynce increases visibility by paying real creators based on their social influence score.
requires:
  env:
    - GRAPHQL_URL    # Required: must be https://boost.inflynce.com/api/graphql (enforced at runtime)
    - PRIVATE_KEY    # Optional: only for pay_fee.js and top_up.js — treat as highly sensitive
homepage: https://boost.inflynce.com
---

# Inflynce Create Campaign

## What is Inflynce?

**Inflynce Marketing** lets anyone boost a link using USDC and reward real users based on measurable social influence (Mindshare). You set a budget and eligible users (Farcaster for now, expanding to X) engage with your link to earn rewards instantly. You can BOOST any link on internet — tweets, project websites, Youtube videos, Farcaster casts — to get visibility. Inflynce runs on Base and does not custody user funds.

This skill creates boost campaigns on [Inflynce](https://boost.inflynce.com) via the `postBoostWeb` GraphQL mutation.

## Project Structure

```
inflynce-create-campaign/
├── scripts/
│   ├── create_campaign.js   # Create a boost campaign (main script)
│   ├── pay_fee.js           # Pay 0.25 USDC platform fee (requires PRIVATE_KEY)
│   └── top_up.js            # Approve USDC budget for boosts contract (requires PRIVATE_KEY)
├── test/
│   └── create_campaign.test.js
├── package.json
├── clawhub.json
└── SKILL.md
```

## Prerequisites

1. **Install dependencies**: Run `npm install` once before using any script.
2. **Platform fee**: Each campaign requires **0.25 USDC**. The creator wallet MUST have already sent exactly 0.25 USDC to Inflynce on Base. See "How to Pay 0.25 USDC" below.
3. **Config**: Set `GRAPHQL_URL` to `https://boost.inflynce.com/api/graphql`. For programmatic pay/top-up, also set `PRIVATE_KEY` (creator wallet private key).
4. **Gas**: The wallet running `pay_fee.js` or `top_up.js` needs Base ETH for gas, in addition to USDC.

### Environment variables

```env
GRAPHQL_URL=https://boost.inflynce.com/api/graphql
PRIVATE_KEY=0x...   # optional — only needed for pay_fee.js and top_up.js

# Optional: supply your own Base RPC to avoid public endpoint rate limits
RPC_URL=https://mainnet.base.org
```

> **Note on RPC:** `pay_fee.js` and `top_up.js` use viem's default public Base RPC if no `RPC_URL` is provided. This may be rate-limited under heavy load. For production use, supply a dedicated RPC URL from a provider such as Alchemy, Infura, or QuickNode.

## Security

**`GRAPHQL_URL` is enforced at runtime.** The script validates that the URL host is exactly `boost.inflynce.com` and that the protocol is `https`. Any other value causes an immediate error before any data is sent. You cannot override this to a different endpoint.

**`PRIVATE_KEY` is highly sensitive.** It signs real Base transactions. Only supply it if you understand the risk. Prefer doing the 0.25 USDC payment and top-ups manually via [boost.inflynce.com](https://boost.inflynce.com) to avoid storing a private key in the agent.

**Hardcoded addresses (verify at [boost.inflynce.com](https://boost.inflynce.com) or Inflynce docs):**

| Purpose | Address | Chain |
|---------|---------|-------|
| 0.25 USDC fee recipient | `0xA61529732F4E71ef1586252dDC97202Ce198A38A` | Base |
| USDC contract | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | Base (Circle) |
| Boosts contract (approve spender) | `0x6e6A6128bB0c175989066eb0e2bf54F06688207b` | Base |

## Usage

### Live campaign

```bash
npm install && node scripts/create_campaign.js \
  --cast-url "https://..." \
  --payment-hash "0x<TX_HASH_OF_0.25_USDC_PAYMENT>" \
  --creator-wallet "0x..." \
  --budget "50" \
  [--multiplier 1] \
  [--graphql-url "https://boost.inflynce.com/api/graphql"]
```

### Dry run (no API call, no payment required)

Use `--dry-run` to validate inputs and inspect what would be sent without creating a real campaign. Any valid-format payment hash works for testing.

```bash
node scripts/create_campaign.js \
  --dry-run \
  --cast-url "https://x.com/user/status/123" \
  --payment-hash "0x$(python3 -c 'print("ab"*32)')" \
  --creator-wallet "0x..." \
  --budget "10"
```

Or use `run_script` with the script path. Required args:

- `--cast-url`: **Any https URL** — tweet, project website, Farcaster cast, etc.
- `--payment-hash`: On-chain tx hash proving 0.25 USDC payment
- `--creator-wallet`: Ethereum address (validated against payment sender)
- `--budget`: Campaign budget in USDC (minimum 5 USDC)

Optional args:

- `--multiplier`: Integer 1–10, default 1. Scales the reward cost per engagement. Use a higher multiplier to attract higher-influence users; use 1 for broad, cost-efficient reach.
- `--graphql-url`: Override the GraphQL endpoint (must still be `https://boost.inflynce.com`). Useful when `GRAPHQL_URL` env var is not set.
- `--dry-run`: Validate inputs and print the payload without calling the API.

### Example output

A successful campaign creation returns:

```json
{
  "id": "cm9abc123def456",
  "boostStatus": "ACTIVE",
  "creatorWallet": "0x000...0001"
}
```

Use `id` to track or reference the campaign. `boostStatus` will be `ACTIVE` immediately after creation.

## Supported URLs

- **Tweets**: `https://x.com/...` or `https://twitter.com/...`
- **Project websites**: `https://example.com`
- **Farcaster casts**: `https://warpcast.com/~/casts/0x...`
- **Any https link**

## API Reference

- **Endpoint**: `POST https://boost.inflynce.com/api/graphql`
- **Mutation**: `postBoostWeb(input: PostBoostWebInput!)`
- **Auth**: None (payment hash proves authorization)
- **Returns**: `{ id, boostStatus, creatorWallet }`
- **appType**: This skill sends `appType: 2` (Agent). Web UI uses `appType: 1`. Filter `mindshare_boosts` by `app_type = 2` to find agent-created campaigns.

## Flow

1. **Top up** — Approve USDC for the boosts contract (min 5 USDC). See "How to Top Up" below.
2. **Pay 0.25 USDC** — Platform fee per campaign. See "How to Pay 0.25 USDC" below.
3. Run this skill with the payment tx hash; campaign is created and returns boost ID.
4. Top up again anytime to increase budget.

## How to Pay 0.25 USDC

Each campaign requires a 0.25 USDC transfer to Inflynce on Base. The tx hash is the proof.

### Agent (programmatic)

> ⚠️ **No dry-run available.** This script broadcasts a real transaction immediately. Ensure the wallet has USDC and Base ETH for gas before running.

```bash
npm install && node scripts/pay_fee.js
# Pass PRIVATE_KEY via env:
PRIVATE_KEY=0x... node scripts/pay_fee.js
# Or pass inline as a flag:
node scripts/pay_fee.js --private-key 0x...
```

Sends `USDC.transfer(0xA61529732F4E71ef1586252dDC97202Ce198A38A, 0.25)` on Base.

**Output:**
```json
{ "txHash": "0xabc...def", "amount": 0.25, "chain": "base" }
```

Extract `txHash` from stdout and pass it as `--payment-hash` to `create_campaign.js`.

### Human (wallet)

1. Ensure wallet has USDC on Base
2. Send **exactly 0.25 USDC** to `0xA61529732F4E71ef1586252dDC97202Ce198A38A`
3. Use the transaction hash as `--payment-hash`

## How to Top Up

### Option A: Agent (programmatic)

> ⚠️ **No dry-run available.** This script broadcasts a real transaction immediately. Ensure the wallet has USDC and Base ETH for gas before running.

```bash
npm install && node scripts/top_up.js --amount 50
# Pass PRIVATE_KEY via env:
PRIVATE_KEY=0x... node scripts/top_up.js --amount 50
# Or pass inline as a flag:
node scripts/top_up.js --private-key 0x... --amount 50
```

`--amount` defaults to `50` if omitted. Minimum is `5` USDC.

This sends an ERC-20 approve tx: `USDC.approve(BOOSTS_CONTRACT, amount)` on Base. The agent's wallet must hold USDC and Base ETH for gas.

**Output:**
```json
{ "txHash": "0xabc...def", "amount": 50, "chain": "base" }
```

### Option B: Human (web UI)

1. Go to [boost.inflynce.com](https://boost.inflynce.com)
2. Connect the creator wallet
3. Click **Top Up Your Spending** or **Approve USDC**
4. Enter amount (minimum 5 USDC), confirm in wallet

## Errors & Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `GRAPHQL_URL required` | Env var not set and `--graphql-url` not passed | Set `GRAPHQL_URL` in env or pass `--graphql-url` |
| `Untrusted GRAPHQL_URL host` | URL points to a host other than `boost.inflynce.com` | Use the correct endpoint |
| `must use HTTPS` | `GRAPHQL_URL` uses `http://` | Switch to `https://` |
| `payment-hash must be a valid tx hash` | Hash is not 0x + 64 hex chars | Use the exact on-chain tx hash |
| `Minimum budget is 5 USDC` | `--budget` is below 5 | Set budget to 5 or higher |
| `Invalid URL` | `--cast-url` is not https or a raw 0x hash | Use a full `https://` URL |
| `Private key required` | `PRIVATE_KEY` not set for pay_fee/top_up | Set `PRIVATE_KEY` env var or pass `--private-key 0x...` |
| `Amount must be at least 5 USDC` | top_up amount below minimum | Use `--amount 5` or higher |
| API: payment hash already used | Same tx hash submitted twice | Pay a new 0.25 USDC fee; get a fresh tx hash |
| API: budget below minimum | Server-side budget validation | Increase `--budget` |

## FAQ

**What URL formats are supported?**
Any valid `https://` URL can be used in an Inflynce Boost campaign. This includes tweets from `x.com` or `twitter.com`, project websites, YouTube links, and Farcaster casts from `base.app` or `farcaster.xyz`. For Farcaster casts, the system extracts the cast hash directly from the URL path. For all other URLs, the system generates a unique identifier using `keccak256(URL)`.

**What is the minimum budget?**
The minimum campaign budget is 5 USDC. Before creating a campaign, you must set a spending limit using `top_up.js` or the web interface at [boost.inflynce.com](https://boost.inflynce.com).

**Does Inflynce custody my funds?**
No. Inflynce does not custody user funds. When creating a campaign, you approve USDC to the boost contract, and rewards are paid directly from your wallet to users when they engage with the campaign.

**How do I get USDC on Base?**
You can obtain USDC on Base by bridging funds from Ethereum or another supported network, swapping tokens on Base for USDC, or withdrawing USDC from an exchange that supports the Base network such as Coinbase. You will need USDC on Base for campaign fees and budgets, and ETH on Base to pay gas fees.

**Can I reuse a payment hash for multiple campaigns?**
No. Each campaign requires its own 0.25 USDC payment. You must run `pay_fee.js` or send a 0.25 USDC payment manually once for every new campaign that you create.

**How do I know if a campaign was created by an AI agent?**
Campaigns created through this skill include the parameter `appType: 2`. You can identify them by filtering the `mindshare_boosts` table where `app_type = 2`. Campaigns created through the web interface use `appType: 1`.

**What is Mindshare?**
Mindshare is Inflynce's metric for measuring a user's social influence on the Farcaster network for now. It is calculated from meaningful engagement signals such as likes, replies, recasts, and follows. Users with higher Mindshare receive higher rewards when participating in campaigns because payouts are pegged to Mindshare.

**What is minMindshare?**
For this skill, the `minMindshare` value is fixed at `0.003`. This threshold ensures that only users with a minimum level of influence can participate in campaigns, which protects campaign budgets from bots, scripted accounts, and low-quality engagement.

**What is the cost multiplier?**
The `--multiplier` parameter controls the reward cost per engagement. It accepts values from 1 to 10, and the default value is 1. Increasing the multiplier attracts users with higher Mindshare but will consume the campaign budget faster. For most campaigns, starting with a multiplier of 1 is recommended.

**Which chain is used for payments?**
All payments are executed on Base mainnet. Testnet networks are not supported for `pay_fee` or `top_up` operations.
