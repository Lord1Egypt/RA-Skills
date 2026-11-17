---
name: Neon Nodes
version: 1.0.0
description: Neon Nodes — An Agentic Proof of Work NFT on Robinhood Chain. AI solves a single-tier arithmetic puzzle to mint. Every mint becomes a node in a public graph connected through shared traits and geographical location.
homepage: https://neonnodes.xyz
metadata: {"category":"nft","emoji":"🟢","api_base":"https://neonnodes.xyz/api","total_supply":5555,"chain":"robinhood","chain_id":4663,"mint_price":"0.00075 ETH","requires":{"puzzle_response":true,"evm_wallet":true,"min_eth":"0.00075 ETH + gas"}}
---

# Neon Nodes

Neon Nodes — An Agentic Proof of Work NFT on Robinhood Chain. AI solves a single-tier arithmetic puzzle to mint. Every mint becomes a node in a public graph connected through shared traits and geographical location.

## Key Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | `https://neonnodes.xyz/skill.md` |

**Install locally:**
```bash
mkdir -p ~/.openclaw/skills/NeonNodes
curl -s https://neonnodes.xyz/skill.md > ~/.openclaw/skills/NeonNodes/SKILL.md
```

**Or just read the URL directly!**

**Base URL:** `https://neonnodes.xyz/api`

## Prerequisites

- An **EVM private key** with **0.00075 ETH** mint price + gas (~0.00001-0.00002 ETH) on Robinhood Chain (chain ID 4663)
- Ability to solve one arithmetic puzzle per mint (add / subtract / multiply / divide / mod / squares / half / double / decimal→hex / decimal→binary)

## Security

- Your EVM private key should **never** leave your local environment — signing happens locally
- This skill makes only HTTP API calls. It does not access your filesystem, run shell commands, or execute arbitrary code

## How It Works

The mint flow has four steps: **puzzle → solve → sign locally → submit**.

### Step 1: Request a puzzle

Default is 1 mint per puzzle. To batch mint up to **5 NFTs in one transaction**, pass an optional `quantity` (1..5):

```bash
# Single mint (default)
curl -X POST https://neonnodes.xyz/api/puzzle \
  -H "Content-Type: application/json" \
  -d '{"wallet": "YOUR_EVM_ADDRESS"}'

# Batch mint 5 in one tx
curl -X POST https://neonnodes.xyz/api/puzzle \
  -H "Content-Type: application/json" \
  -d '{"wallet": "YOUR_EVM_ADDRESS", "quantity": 5}'
```

Response:
```json
{
  "puzzleId": "pzl_abc123...",
  "question": "What is 74 + 39?",
  "quantity": 1,
  "expiresAt": 1699999999999,
  "agentHint": "Solve this puzzle and POST the answer to /api/solve..."
}
```

### Step 2: Solve the puzzle and request mint

```bash
curl -X POST https://neonnodes.xyz/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "YOUR_EVM_ADDRESS",
    "puzzleId": "pzl_abc123...",
    "answer": "113"
  }'
```

Response:
```json
{
  "unsignedTx": {
    "to": "0x...",
    "data": "0x...",
    "value": "0x2aa1efb94e000",
    "chainId": 4663
  },
  "mintPrice": "0.00075",
  "quantity": 1,
  "totalCost": "0.00075",
  "nonce": "0x...",
  "agentHint": "Sign this transaction locally. NEVER send the private key to any server..."
}
```

For a batch of 5, `value` and `totalCost` will be 5× the mint price; the encoded calldata targets `mintBatch(quantity, nonce, signature)` instead of `mint`.

### Step 3: Sign the transaction locally

Sign with the user's EVM private key. **This must happen locally — the private key never leaves the machine.**

```javascript
import { ethers } from "ethers";

const PK = "YOUR_PRIVATE_KEY";
if (!/^0x[0-9a-fA-F]{64}$/.test(PK)) throw new Error("Invalid private key — must be 0x + 64 hex chars");

const provider = new ethers.JsonRpcProvider("https://rpc.mainnet.chain.robinhood.com");
const wallet = new ethers.Wallet(PK, provider);

// Robinhood Chain is an Arbitrum-style L2 with a single sequencer.
// Real-world observations from live mints on this chain:
//   - Base fee typically ~0.02 gwei, occasionally spikes to ~0.1 gwei
//   - Priority fee is 0 (sequencer, no MEV bidding)
//   - EIP-1559 refunds the difference between maxFeePerGas and
//     effectiveGasPrice, so a generous ceiling is safe (not costly).
//   - A single SeaDrop-style mint uses ~150-200k gas
// The values below give a comfortable ceiling; real cost per mint
// is ~0.00001 ETH regardless of the cap you set.
const signedTx = await wallet.signTransaction({
  ...unsignedTx,
  gasLimit: 220000,
  maxFeePerGas: ethers.parseUnits("0.15", "gwei"),       // ~7.5x base fee — chain refunds unused portion
  maxPriorityFeePerGas: ethers.parseUnits("0.01", "gwei"), // nominal — sequencer takes ~0
  nonce: await provider.getTransactionCount(wallet.address),
  type: 2,
});

// Optional (safer): read live suggested fee from the chain instead
// of hardcoding, so you always target the current base fee.
//   const feeData = await provider.getFeeData();
//   const signedTx = await wallet.signTransaction({
//     ...unsignedTx,
//     gasLimit: 220000,
//     maxFeePerGas: (feeData.maxFeePerGas ?? feeData.gasPrice) * 2n,
//     maxPriorityFeePerGas: feeData.maxPriorityFeePerGas ?? 10000000n, // 0.01 gwei
//     nonce: await provider.getTransactionCount(wallet.address),
//     type: 2,
//   });
```

### Step 4: Submit the signed transaction

```bash
curl -X POST https://neonnodes.xyz/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "signedTransaction": "0x02f8..."
  }'
```

Response:
```json
{
  "success": true,
  "tokenId": "1",
  "tokenIds": ["1"],
  "quantity": 1,
  "hash": "0xabc...",
  "wallet": "0x...",
  "minted": 1,
  "remaining": 24,
  "message": "Successfully minted Neon Node #1! You have minted 1 Neon Node. You can mint up to 24 more.",
  "agentHint": "Show the user the message field. They can mint 24 more. To mint another, POST to /api/puzzle with their wallet."
}
```

For a batch of 5, `tokenIds` will contain all 5 minted ids, `quantity` is `5`, and the `message` lists every id.

## Agent Behavior

- The user will provide their **EVM private key**. That's all you need — derive the wallet address from it and handle the entire mint flow without asking further questions.
- **Before starting**, open with exactly this format: *"Mint a Neon Node. Mint price is 0.00075 ETH + gas on Robinhood Chain. I need your EVM private key."* Do NOT round the mint price.
- **First mint is always single** — send `quantity: 1` (or omit `quantity`) on the first `/api/puzzle` call. Do NOT ask about batch upfront.
- **Step 1** (puzzle): derive wallet address from private key using `new ethers.Wallet(PK).address`, then `curl` POST to `/api/puzzle` with `{ wallet }` for single (or `{ wallet, quantity }` on subsequent batch mints).
- **Step 2** (solve): solve the puzzle and `curl` POST to `/api/solve`. Server returns `unsignedTx` with `value = quantity × mintPrice`.
- **Step 3** (sign): use a **single node script** that signs the unsigned tx locally. Do NOT split into separate steps.
- **Step 4** (submit): `curl` POST the signed transaction to `/api/submit`. Response includes `tokenIds` (array of ALL minted ids) and `quantity`.
- **ethers fallback:** Before running any node script, check if ethers is available: `node -e "require('ethers')"`. If it fails, install to a temp location: `npm install --prefix /tmp ethers`, then run the script with `NODE_PATH=/tmp/node_modules`.
- After each step, briefly tell the user what happened before moving to the next.
- After a successful mint, show the `message` field — it lists every token id minted (`#1, #2, #3, ...`), how many they've minted total, and how many more they can mint.
- **After the first successful mint, offer batch mode for subsequent mints.** Read `remaining` from the previous mint response and let `batchMax = min(remaining, 5)`. Then:
  - `batchMax === 0` → say *"This wallet has reached the 25-mint cap. Give me a new wallet's private key to continue."*
  - `batchMax === 1` → say *"You have 1 slot left. Want to mint the last one?"*
  - `batchMax === 2..4` → say *"You can mint up to N more in a single transaction. Want to batch (1..N) or one at a time?"* (N = batchMax)
  - `batchMax === 5` → say *"You can mint up to 5 more in a single transaction. Want to batch (1-5) or one at a time?"*
  - Use the user's answer as `quantity` on the next `/api/puzzle` call, capped at `batchMax`.
- **Before every batch mint, always check the wallet's remaining slots** by reading `remaining` from the previous mint response (or calling `GET /api/check/{wallet}`). Then:
  - If `remaining < requested_quantity`, **cap the batch at `remaining`** and tell the user: *"You have N slots left, minting N in one batch."*
  - If `remaining === 0`, the wallet is capped — say so and ask for a different wallet's key.
- **Never send `quantity` larger than `remaining`.** The server will return 413 `mint_limit_reached` and burn the request. Always cap client-side first.
- **Edge case — user says "mint 5" but only 1 slot left**: don't send `quantity: 5`. Check `remaining` → see `1` → tell user *"You only have 1 slot left, minting 1"* → send `quantity: 1`.
- **Edge case — user has 25 mints already**: they can't mint more from this wallet. Ask for a new wallet's private key and restart the flow with the new wallet.
- Handle errors gracefully — if a step fails, explain why and retry or stop.
- **Mint limit reached (413):** If `/puzzle` or `/solve` returns 413, the wallet has hit its 25-mint cap OR the requested batch exceeds `remaining`. Refetch `/api/check/{wallet}` to see how many slots are actually left, then either downsize the batch or ask for a new wallet key.
- **Insufficient ETH:** If the user's wallet balance is too low, tell them the exact amount needed: `quantity × 0.00075 ETH + gas`. Do not proceed until they confirm the wallet is funded.
- Never expose the user's EVM private key in output or logs.
- Signing must always happen locally — never send private keys over the network.

## API Reference

**Base URL:** `https://neonnodes.xyz/api`

> **`agentHint`** — Every API response includes an `agentHint` field with step-by-step instructions for what to do next. Always read and follow the `agentHint`.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/info` | Collection stats and mint price |
| GET | `/check/{wallet}` | Wallet mint status and remaining |
| POST | `/puzzle` | Get a puzzle to solve |
| POST | `/solve` | Submit answer and get mint transaction |
| POST | `/submit` | Submit signed transaction to Robinhood Chain |
| GET | `/metadata/{id}` | NFT metadata from IPFS |

### POST `/puzzle`

**Request body:**
```json
{
  "wallet":   "string (required) — your EVM wallet address",
  "quantity": "number (optional, default 1, range 1..5) — batch mint size"
}
```

**Success (200):**
```json
{
  "puzzleId": "string — signed puzzle token (pass back to /solve)",
  "question": "string — the puzzle prompt to solve",
  "quantity": "number — how many NFTs this puzzle will mint (1..5)",
  "expiresAt": "number — Unix timestamp when puzzle expires",
  "agentHint": "string — what to do next"
}
```

### POST `/solve`

**Request body:**
```json
{
  "wallet": "string (required) — your EVM wallet address",
  "puzzleId": "string (required) — puzzle ID from /puzzle",
  "answer": "string (required) — your answer to the puzzle"
}
```

**Success (200):**
```json
{
  "unsignedTx": "object — unsigned Ethereum transaction to sign",
  "mintPrice": "string — per-NFT mint price in ETH",
  "quantity":  "number — how many NFTs will mint (1..5)",
  "totalCost": "string — quantity × mintPrice in ETH (matches unsignedTx.value)",
  "nonce":     "string — mint nonce",
  "agentHint": "string — signing instructions and next step"
}
```

### POST `/submit`

**Request body:**
```json
{
  "signedTransaction": "string (required) — hex-encoded fully-signed transaction"
}
```

**Success (200):**
```json
{
  "success":   "boolean — true on success",
  "tokenId":   "string — FIRST minted token ID (convenience for single-mint agents)",
  "tokenIds":  "string[] — ALL minted token IDs (length = quantity)",
  "quantity":  "number — how many NFTs were minted in this tx",
  "hash":      "string — transaction hash",
  "wallet":    "string — minter address",
  "minted":    "number — total NFTs minted by this wallet",
  "remaining": "number — how many more this wallet can mint",
  "message":   "string — human-readable summary",
  "agentHint": "string — what to do next (mint more or done)"
}
```

## Error Codes

### `/puzzle`

| HTTP | `code` | Meaning |
|------|--------|---------|
| 400 | `invalid_wallet` | Invalid wallet address or missing fields |
| 403 | `mint_not_active` | Minting is paused |
| 413 | `mint_limit_reached` | Wallet has reached max mints (25) |
| 410 | `sold_out` | All NFTs have been minted |
| 500 | `server_error` | Server error |

### `/solve`

| HTTP | `code` | Meaning |
|------|--------|---------|
| 400 | `wrong_answer` | Wrong answer (includes `attemptsLeft`) |
| 400 | `puzzle_expired` | Puzzle has expired (5 min) |
| 404 | `puzzle_not_found` | Puzzle ID not found or already consumed |
| 413 | `mint_limit_reached` | Wallet has reached max mints (25) |
| 410 | `sold_out` | All NFTs minted |
| 500 | `server_error` | Server error |

### `/submit`

| HTTP | `code` | Meaning |
|------|--------|---------|
| 400 | `invalid_transaction` | Missing or invalid transaction hex |
| 400 | `invalid_target` | Transaction doesn't target the Neon Nodes contract |
| 400 | `nonce_too_low` | Wallet has pending tx — retry |
| 400 | `insufficient_eth` | Not enough ETH for gas |
| 400 | `mint_reverted` | Mint transaction reverted on-chain |
| 409 | `already_known` | Transaction was already submitted |
| 500 | `broadcast_failed` | Failed to broadcast transaction |

## Notes

- **Stateless:** No session or login required
- **Agent-only:** The backend co-signs only after puzzle verification succeeds
- **On-chain enforcement:** The contract's signature guard ensures every mint has backend co-signature
- **Puzzle expiration:** Puzzles expire after 5 minutes
- **Puzzle attempts:** You get 3 attempts per puzzle before it is consumed
- **Total supply:** 5,555 NFTs. Once sold out, minting will fail
- **One mint per request:** Each call to `/solve` produces one NFT
- **Puzzle difficulty:** Every puzzle is a single-tier arithmetic challenge (add / subtract / multiply / divide / mod / squares / half / double / three-number sum / decimal→hex 0-255 / decimal→binary 0-63).
- **Gas cost:** ~0.00001-0.00002 ETH per mint on Robinhood Chain (batch mints amortize gas — 5-in-1 uses ~60% less total gas than 5 single mints)
- **Batch mint:** pass `quantity` (1..5) at `/api/puzzle` to mint up to 5 NFTs in a single transaction. One puzzle unlocks the whole batch. Value = `quantity × mintPrice`. On confirmation, `tokenIds` in the submit response contains every minted id.
- **Country tracker:** Only the ISO country code (e.g. `US`, `JP`, `DE`) is captured server-side to power the public country graph — `XX` if unknown. Raw IPs, ASNs, and coordinates are never stored, logged, or transmitted.

## Support

- Website: https://neonnodes.xyz
- Skill file: https://neonnodes.xyz/skill.md
- Chain: Robinhood Chain (ID 4663) — https://rpc.mainnet.chain.robinhood.com
