---
name: pumpmarket
version: 1.0.0
description: Predict pump.fun token graduations (YES/NO) on Solana mainnet via PumpMarket parimutuel betting markets.
homepage: https://pumpmarket.fun
metadata: {"openclaw":{"emoji":"🎰","category":"defi","homepage":"https://pumpmarket.fun","requires":{"bins":["curl"],"npm":["@coral-xyz/anchor","@solana/web3.js"]}}}
---

# PumpMarket Agent Skill

Trade SOL on pump.fun token graduation outcomes. Predict which tokens will graduate to PumpSwap within 1 hour.

**Network:** Solana **mainnet-beta**
**API:** `https://pumpbet-mainnet.up.railway.app`
**WebSocket:** `wss://pumpbet-mainnet.up.railway.app`
**Program ID:** `3mNbBV3Xc3rNJ4E87pSFzW7VhUZySHQDQVyd4MP2VFG6`
**IDL:** [`https://pumpmarket.fun/skill.json`](https://pumpmarket.fun/skill.json)
**Treasury:** `4iFYGzxKGH2SAeVaR5AxPiCfLCSQD9fdPK8tsDBbmx3f`
**Naming:** Brand is PumpMarket. On-chain program name is `pumpbets` (legacy). API host `pumpbet-*` retains the original name.

> **This is mainnet. Bets use real SOL.** The program is deployed (100 markets, 290 bets on-chain), the treasury is funded (9.29 SOL), and the keeper authority is operational (0.12 SOL). All addresses, API URLs, and code examples target Solana mainnet-beta.

---

## Table of Contents

1. [What Is PumpMarket](#1-what-is-pumpmarket)
2. [First-Run Setup](#2-first-run-setup)
3. [On-Chain Parameters](#3-on-chain-parameters)
4. [API Reference](#4-api-reference)
5. [WebSocket Reference](#5-websocket-reference)
6. [Transaction Construction](#6-transaction-construction)
7. [Transaction Flows](#7-transaction-flows)
8. [Signal Evaluation & Strategy](#8-signal-evaluation--strategy)
9. [Resolution Logic](#9-resolution-logic)
10. [Error Handling](#10-error-handling)
11. [Rate Limits & Best Practices](#11-rate-limits--best-practices)
12. [FAQ & Gotchas](#12-faq--gotchas)
13. [Appendix: Account Data Layout](#13-appendix-account-data-layout)
14. [Appendix: On-Chain Events](#14-appendix-on-chain-events)
15. [Appendix: Dry-Run Simulation](#15-appendix-dry-run-simulation)

---

## 1. What Is PumpMarket

PumpMarket is a parimutuel prediction market for pump.fun token graduations on Solana. Users bet SOL on whether a pump.fun token will "graduate" (complete its bonding curve and migrate to PumpSwap DEX) within approximately 1 hour.

**How it works:**
1. A user creates a market for a pump.fun token, choosing YES or NO and staking SOL
2. Other users bet YES (token will graduate) or NO (it won't) within the ~1-hour window
3. An automated keeper resolves the market based on on-chain data
4. Winners split the total pool proportionally (minus 4.5% fees)

**Market outcomes:**
- **YES wins** — token graduated (bonding curve hit 100%, migrated to PumpSwap)
- **NO wins** — token did not graduate within the deadline (timeout or rug)
- **VOIDED** — one-sided pool (all bets on the same side) or oracle void — full refunds, zero fees

---

## 2. First-Run Setup

Before an agent can trade, it needs:

### Wallet
- A Solana wallet with a keypair (e.g., `Keypair.fromSecretKey(...)`)
- **Connected to mainnet-beta** RPC (e.g., `https://api.mainnet-beta.solana.com` or a Helius/Quicknode endpoint)
- Funded with SOL for bets and transaction fees

### RPC Endpoint
The public `https://api.mainnet-beta.solana.com` is rate-limited. For production agents, use a dedicated RPC provider (Helius, Quicknode, Triton, etc.).

### Terms Acceptance (Required Once)
PumpMarket requires users to accept terms before their activity is fully tracked. This is a one-time operation:

1. **Get the message to sign:**
   ```
   GET https://pumpbet-mainnet.up.railway.app/api/users/{wallet}/terms/message
   ```
   Response:
   ```json
   { "message": "PumpMarket Terms of Service\nI agree to the terms at https://pumpmarket.fun/terms\nWallet: ...\nTimestamp: ...", "timestamp": 1772413074485, "wallet": "..." }
   ```
2. **Sign the `message` string with your wallet and encode as base58:**
   ```typescript
   import nacl from 'tweetnacl';
   import bs58 from 'bs58';
   const sig = nacl.sign.detached(new TextEncoder().encode(message), keypair.secretKey);
   const signatureBase58 = bs58.encode(sig);
   ```
3. **Submit the signed acceptance:**
   ```
   POST https://pumpbet-mainnet.up.railway.app/api/users/{wallet}/terms
   Body: { "signature": "<base58 signature>", "timestamp": <timestamp from step 1> }
   ```
4. **Verify acceptance:**
   ```
   GET https://pumpbet-mainnet.up.railway.app/api/users/{wallet}/terms
   → { "wallet": "...", "termsAccepted": true }
   ```

### Dependencies
```bash
npm install @coral-xyz/anchor @solana/web3.js
```

The `@pumpmarket/sdk` npm package is **not published** (internal monorepo only). All code examples in this document use raw `@coral-xyz/anchor` and `@solana/web3.js`. You need the program IDL, which is provided in [Section 6](#6-transaction-construction).

### Keypair Security

> **Never hardcode private keys in source code or commit them to repositories.**

**Loading a keypair from file:**
```typescript
import { Keypair } from '@solana/web3.js';
import fs from 'fs';

// Ensure keyfile permissions: chmod 600 ~/.config/solana/id.json
const secret = JSON.parse(fs.readFileSync(process.env.KEYPAIR_PATH!, 'utf-8'));
const keypair = Keypair.fromSecretKey(Uint8Array.from(secret));
```

**Loading from environment variable:**
```typescript
import bs58 from 'bs58';
const keypair = Keypair.fromSecretKey(bs58.decode(process.env.PRIVATE_KEY!));
```

**Best practices:**
- Store keys in environment variables or encrypted keyfiles — never in source code
- Set keyfile permissions to `600` (`chmod 600 keyfile.json`)
- Add `*.json` keypair paths to `.gitignore`
- Use a dedicated betting wallet with limited funds — not your main wallet
- For production agents, consider a secrets manager (e.g. AWS Secrets Manager, Doppler)

### Testing Without Real SOL

This skill targets **mainnet-beta** where bets use real SOL. To test transaction construction without spending:

- **Dry-run simulation:** See [Appendix: Dry-Run Simulation](#15-appendix-dry-run-simulation) — builds and simulates transactions on-chain without submitting them.
- **Devnet:** PumpMarket has a devnet deployment (`beta.pumpmarket.fun`) used for internal testing. The devnet program ID is `3mNbBV3Xc3rNJ4E87pSFzW7VhUZySHQDQVyd4MP2VFG6` (same binary, different state). Devnet is not guaranteed to be stable or have active markets.
- **Start small:** If testing on mainnet, budget at least 0.2 SOL per bet (0.1 SOL bet + 0.1 SOL market creation fee). Bets below 0.1 SOL are likely unprofitable after fees.

---

## 3. On-Chain Parameters

All values verified against the Anchor smart contract at `packages/contracts/programs/pumpbets/src/constants.rs`.

| Parameter | Value | Lamports | On-Chain Enforcement |
|-----------|-------|----------|---------------------|
| **Market Creation Fee** | 0.1 SOL | 100,000,000 | `createMarket` — transferred to treasury |
| **Min Bet** | 0.01 SOL | 10,000,000 | `createMarket` + `placeBet` |
| **Max Bet** | 10 SOL | 10,000,000,000 | `createMarket` + `placeBet` |
| **Platform Fee** | 3.5% | 350 BPS | `resolveMarket` — from total pool to treasury |
| **Creator Fee** | 1.0% | 100 BPS | `resolveMarket` — from total pool to creator |
| **Total Fee** | 4.5% | 450 BPS | Combined (platform + creator) |
| **Market Duration** | ~1 hour | 9,000 slots | `createMarket` — `resolution_slot = current + 9000` |
| **Max Bonding Progress** | < 95 | — | Strict `<` check: 0–94 accepted, **95+ rejected** |
| **Rug Threshold** | $4,500 USD | — | Off-chain keeper checks (constants defined on-chain) |
| **Rug Duration** | ~5 minutes | 750 slots | Must sustain below threshold continuously |
| **Claim Period** | ~7 days | 1,512,000 slots | Vault can be closed (rent reclaimed) after this |
| **Emergency Delay** | ~1 day | 216,000 slots | Only treasury can emergency withdraw after this |

### Mainnet Activity (Indexer snapshot — 2026-03-02)

| Metric | Value |
|--------|-------|
| Program accounts | 490 (100 markets, 290 bets, 100 vaults) |
| Markets resolved | 53 (47 voided) |
| Total volume | 76.14 SOL |
| Treasury balance | 9.29 SOL |
| Keeper balance | 0.12 SOL |

> These values are from PumpMarket's internal indexer at the timestamp above and may differ from current on-chain state.

### Verify Mainnet Deployment

```bash
# Verify API is healthy
curl -s https://pumpbet-mainnet.up.railway.app/api/health | python3 -m json.tool

# Verify program on-chain (requires solana CLI)
solana program show 3mNbBV3Xc3rNJ4E87pSFzW7VhUZySHQDQVyd4MP2VFG6 --url mainnet-beta

# Verify treasury is funded
solana balance 4iFYGzxKGH2SAeVaR5AxPiCfLCSQD9fdPK8tsDBbmx3f --url mainnet-beta

# Verify active markets exist
curl -s https://pumpbet-mainnet.up.railway.app/api/stats | python3 -m json.tool
```

### Reproduce Account Counts via RPC

Estimate on-chain account counts by querying program-owned accounts by data size. Account sizes: BettingMarket = 123 bytes, UserBet = 91 bytes, Vault = 41 bytes.

> Some public RPCs rate-limit `getProgramAccounts`. Use a paid RPC if needed.

```bash
RPC=https://api.mainnet-beta.solana.com
PID=3mNbBV3Xc3rNJ4E87pSFzW7VhUZySHQDQVyd4MP2VFG6

count_by_size () {
  curl -s $RPC -X POST -H 'Content-Type: application/json' -d "{
    \"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getProgramAccounts\",
    \"params\":[\"$PID\",{
      \"encoding\":\"base64\",
      \"dataSlice\":{\"offset\":0,\"length\":0},
      \"filters\":[{\"dataSize\":$1}]
    }]
  }" | jq '.result | length'
}

echo "BettingMarket (123): $(count_by_size 123)"
echo "UserBet (91):         $(count_by_size 91)"
echo "Vault (41):           $(count_by_size 41)"
```

### Mainnet Addresses

| Address | Purpose |
|---------|---------|
| `3mNbBV3Xc3rNJ4E87pSFzW7VhUZySHQDQVyd4MP2VFG6` | PumpBets Program ID |
| `4iFYGzxKGH2SAeVaR5AxPiCfLCSQD9fdPK8tsDBbmx3f` | Treasury |
| `3cHDNTUqsqV4XSDdzuinvzaENKaUTKmud9m8enWFMfTh` | Keeper Authority |

### PDA Seeds

| Account | Seeds | Constraint |
|---------|-------|-----------|
| Market | `["market", token_mint]` | One market per token mint |
| User Bet | `["bet", market, user, bet_index_u32_le]` | Seed is `"bet"` (not `"user_bet"`) |
| Vault | `["vault", market]` | Holds all SOL for a market |

---

## 4. API Reference

**Base URL:** `https://pumpbet-mainnet.up.railway.app`

All endpoints are **public with no authentication** — no API keys, no wallet signatures, no headers required. The only exception is `POST /api/users/:wallet/terms` which requires a wallet signature (one-time terms acceptance).

### Health & Stats

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check — DB/Redis status, uptime, version |
| GET | `/api/stats` | Platform stats — `marketsResolved`, `activeMarkets`, `totalVolumeSol` |

### Tokens

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tokens` | List tokens (paginated, filterable) |
| GET | `/api/tokens/featured` | Top 5 tokens nearest graduation with active markets |
| GET | `/api/tokens/trending` | Trending tokens by volume |
| GET | `/api/tokens/graduated` | Recently graduated tokens |
| GET | `/api/tokens/prices/live?mints=mint1,mint2` | Birdeye prices (max 20 mints via GET) |
| GET | `/api/tokens/top-trades` | Biggest trades in last 15 minutes |
| GET | `/api/tokens/:mint` | Single token details |
| POST | `/api/tokens/:mint/validate-bonding` | Fresh bonding validation (anti-stale-data) (**no request body**) |
| POST | `/api/tokens/:mint/refresh` | Force refresh bonding data from chain |

**GET `/api/tokens` Query Parameters:**

| Param | Values | Default |
|-------|--------|---------|
| `sort` | `volume_desc`, `created_desc`, `bonding_desc`, `pool_desc`, `bonding_active_desc` | `created_desc` |
| `has_market` | `true`, `false` | — |
| `user` | wallet address | — |
| `creator` | wallet address | — |
| `cursor` | string (from `nextCursor`) | — |
| `limit` | 1–100 | 20 |

**Response:**
```json
{
  "tokens": [{
    "id": 64934529,
    "mintAddress": "7QMT...pump",
    "name": "Dodger",
    "symbol": "DRAFT",
    "imageUrl": "https://ipfs.io/...",
    "bondingProgress": 3.65,
    "marketCapUsd": 2443.34,
    "solReserves": 0.834,
    "createdAt": "2026-03-01T23:50:41.654Z",
    "updatedAt": "2026-03-01T23:50:41.654Z",
    "graduatedAt": null,
    "isGraduated": false
  }],
  "nextCursor": "2026-03-01T23:50:36.703Z:64934477",
  "cached": false
}
```

**GET `/api/tokens/:mint` Response — verified live (includes nested market if one exists):**
```json
{
  "id": 53217785,
  "mintAddress": "2XPS...pump",
  "name": "Kuzya",
  "symbol": "KUZYA",
  "imageUrl": "https://...",
  "bondingProgress": 0,
  "marketCapUsd": 1692.45,
  "solReserves": 0,
  "createdAt": "2026-02-22T14:47:48.437Z",
  "graduatedAt": "2026-02-22T14:57:46.634Z",
  "isGraduated": true,
  "market": {
    "marketAddress": "8ydD...zfKs",
    "yesPool": 0, "noPool": 1,
    "status": "voided",
    "creationSlot": 443918000,
    "resolutionSlot": 443927000,
    "totalBets": 1
  }
}
```

**POST `/api/tokens/:mint/validate-bonding`** — no request body required. The server fetches fresh data from Bitquery, bypassing all caches.

Response:
```json
{ "valid": true, "bondingProgress": 42, "isGraduated": false, "priceUsd": 0.001, "verifiedAt": "..." }
```
or:
```json
{ "valid": false, "bondingProgress": 97, "reason": "Token is at 97% bonding progress..." }
```

### Markets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/markets` | **Active (unresolved) markets only** |
| GET | `/api/markets/resolved` | Resolved/voided/pending markets (filterable) |
| GET | `/api/markets/graduated` | Alias for resolved with `filter=resolved` |
| GET | `/api/markets/:address` | Single market — full details, odds, delta |
| GET | `/api/markets/:address/bets` | Paginated bets for a market |
| GET | `/api/markets/:address/can-bet` | Check if market accepts bets |
| POST | `/api/markets/:address/check-graduation` | Trigger manual graduation check |
| GET | `/api/markets/by-creator/:wallet` | Markets created by a wallet |

**`GET /api/markets` returns active/unresolved markets only.** No pagination — returns all active markets at once. No status filter. For historical data, use `/api/markets/resolved`.

**GET `/api/markets` Response — verified from source (`routes/markets.ts:119-147`):**
```json
{
  "markets": [{
    "address": "AJAi...4kDZ",
    "tokenMint": "DPMo...pump",
    "token": { "name": "WASM AI", "symbol": "WASM", "image": "https://...", "bondingProgress": "45.20", "marketCapUsd": 8525.77, "priceUsd": 0.001 },
    "creator": "Ax7R...UZMg",
    "deadlineSlot": "403565031",
    "pools": { "yes": 0.5, "no": 1, "total": 1.5 },
    "odds": { "yes": 3, "no": 1.5, "yesImplied": 33.33, "noImplied": 66.67 },
    "delta": 0,
    "totalVolume": 1.5,
    "createdAt": "2026-02-21T18:56:32.279Z"
  }]
}
```

**Note:** The active list uses `address` (same as single market). `creator` is truncated. Includes live `bondingProgress`, `marketCapUsd`, `priceUsd` in the `token` object, and computed `odds`/`delta`. No `nextCursor` — all active markets returned in one response.

> **Type caveat:** `bondingProgress` inside the `token` object on market endpoints is a **string** (e.g. `"45.20"`). On `/api/tokens` it's a number. Always `parseFloat()` before arithmetic (e.g. `delta = parseFloat(token.bondingProgress) - yesImplied`).

**GET `/api/markets/resolved` Response — verified live:**
```json
{
  "markets": [{
    "id": 473,
    "marketAddress": "CJyX...EkhZ",
    "tokenMint": "2yok...pump",
    "token": { "name": "Oil coin", "symbol": "Oilcoin", "image": "https://..." },
    "status": "voided",
    "outcome": null,
    "voided": true,
    "resolutionReason": null,
    "pools": { "yes": 0.1, "no": 0 },
    "totalVolume": 0.1,
    "totalBets": 1,
    "resolvedAt": null,
    "graduatedAt": "2026-03-01T18:53:57.484Z",
    "minutesSinceGraduation": 406,
    "deadlineSlot": "403565031",
    "slotsUntilResolution": null,
    "estimatedResolutionMinutes": null,
    "marketCapUsd": "8525.77",
    "creatorWallet": "9F89...wCZT",
    "holderCount": null
  }],
  "nextCursor": null,
  "_meta": { "currentSlot": 403621384, "pendingMarketsIncluded": true }
}
```

**Beware:** The resolved list uses `marketAddress` (not `address` like the active list and single market endpoints). It also uses `creatorWallet` instead of `creator`. No `odds`/`delta` fields — those are only on active markets and the single market endpoint.

**GET `/api/markets/resolved` Query Parameters:**

| Param | Values | Default |
|-------|--------|---------|
| `filter` | `all`, `resolved`, `pending`, `voided` | `all` |
| `cursor` | string | — |
| `limit` | 1–100 | 20 |
| `includeHolders` | `true` | — |

**Single Market Response (`/api/markets/:address`) — verified live:**
```json
{
  "address": "AJAi1rndzVCZ4SroBnaHv8LDrYsPMteFCwkTun8B4kDZ",
  "tokenMint": "DPMo...pump",
  "creator": "Ax7RXZZSr8eZPDJdeazeZpn9EgnpnEHVzhhYwik5UZMg",
  "token": { "name": "WASM AI", "symbol": "WASM", "image": "https://...", "bondingProgress": "0.00" },
  "status": "resolved",
  "outcome": true,
  "voided": false,
  "pools": { "yes": 0.5, "no": 1, "total": 1.5 },
  "odds": { "yes": 3, "no": 1.5, "yesImplied": 33.33, "noImplied": 66.67 },
  "delta": 0,
  "totalVolume": 1.5,
  "deadlineSlot": "443738815",
  "resolvedAt": null,
  "createdAt": "2026-02-21T18:56:32.279Z",
  "summary": { "yesCount": 1, "noCount": 2, "yesTotal": 0.5, "noTotal": 1, "uniqueBettors": 2 }
}
```

**Note:** The single market endpoint uses `address` (not `marketAddress`), and `odds` uses `yes`/`no` (decimal odds, not `yesOdds`/`noOdds`). Includes a `summary` field with bet counts. Full wallet addresses only appear here — list endpoints truncate to `"Xxxx...xxxx"`.

**`GET /api/markets/:address/can-bet` Response — verified live:**
```json
{ "canBet": false, "reason": "Market is already voided", "marketStatus": "voided", "tokenGraduated": true }
```

**`GET /api/markets/:address/bets` Response — verified live:**
```json
{
  "bets": [{
    "id": 3963,
    "betAddress": "5V9x...oZS",
    "user": "7oQJ...GmKT",
    "amount": 0.5,
    "prediction": "NO",
    "potentialPayout": 0,
    "claimed": false,
    "claimedAmount": null,
    "createdAt": "2026-02-21T18:59:42.249Z"
  }],
  "nextCursor": "2026-02-21T18:59:42.249Z"
}
```

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/:wallet/stats` | User statistics (**volume/profit in lamport strings, not SOL**) |
| GET | `/api/users/:wallet/bets` | Bet history (filterable) |
| GET | `/api/users/:wallet/bets/counts` | Bet counts by status |
| GET | `/api/users/:wallet/claimable` | Count of claimable bets |
| GET | `/api/users/:wallet/claimable/details` | **Claimable bets with estimated payouts** |
| GET | `/api/users/:wallet/terms` | Check terms acceptance |
| POST | `/api/users/:wallet/terms` | Accept terms (**requires wallet signature**) |
| GET | `/api/users/:wallet/terms/message` | Get terms message to sign |

**GET `/api/users/:wallet/bets` Query Parameters:**

| Param | Values | Default |
|-------|--------|---------|
| `status` | `active`, `won`, `lost`, `refunded`, `all` | `all` |
| `cursor` | string | — |
| `limit` | 1–100 | 20 |

**GET `/api/users/:wallet/stats` Response — verified live:**
```json
{
  "wallet": "GVEt...RZW4",
  "totalBets": 57,
  "totalWins": 5,
  "totalVolume": "43100000000",
  "totalProfit": "805083332",
  "marketsCreated": 51,
  "creatorEarnings": "0",
  "termsAccepted": false,
  "termsAcceptedAt": null
}
```
**Important:** `totalVolume` and `totalProfit` are **lamport strings** (not SOL floats). Divide by 1e9 to get SOL. This differs from leaderboard endpoints which return SOL floats.

**GET `/api/users/:wallet/bets` Response — verified live:**
```json
{
  "bets": [{
    "id": 4173,
    "betAddress": "7szH...eyP",
    "market": {
      "marketAddress": "74p2...9nk",
      "tokenMint": "BPba...pump",
      "resolved": true, "voided": false, "outcome": false,
      "deadlineSlot": 443736779,
      "yesPool": 0.1, "noPool": 1
    },
    "token": { "mint": "BPba...pump", "name": "...", "symbol": "...", "imageUrl": "..." },
    "amount": 1,
    "prediction": false,
    "odds": 1.1,
    "status": "won",
    "payout": 1.0505,
    "claimed": false,
    "createdAt": "2026-02-21T19:09:28.382Z"
  }],
  "nextCursor": "2026-02-21T19:09:28.382Z"
}
```

**GET `/api/users/:wallet/bets/counts` Response — verified live:**
```json
{ "active": 0, "won": 15, "lost": 12, "refunded": 11, "all": 38 }
```

**GET `/api/users/:wallet/claimable/details` Response:**
```json
{
  "wallet": "Ax7R...UZMg",
  "count": 3,
  "bets": [{
    "betAddress": "...",
    "marketAddress": "...",
    "amount": 0.5,
    "prediction": true,
    "outcome": true,
    "isRefund": false,
    "estimatedPayout": 0.85,
    "token": { "name": "...", "symbol": "...", "imageUrl": "..." }
  }],
  "totalEstimatedPayout": 2.55
}
```

### Bets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bets/:betAddress` | Single bet by on-chain address |
| POST | `/api/bets/sync` | Sync bet from chain to DB (**optional** — background service catches up) |
| POST | `/api/bets/sync-market` | Sync all bets for a market (**optional**) |
| POST | `/api/bets/sync-user` | Sync all bets for a user (**optional**) |
| POST | `/api/bets/claim/:betAddress` | Record on-chain claim in DB (**optional**) |

**There is no `GET /api/bets` list endpoint.** Use `/api/users/:wallet/bets` or `/api/markets/:address/bets`.

All sync/claim POST endpoints are **optional DB convenience calls**. Bets exist on-chain regardless. A background sync service runs continuously and will pick up unsynced bets within minutes. Calling sync immediately after a transaction makes the bet visible in the API/UI sooner.

**POST `/api/bets/sync`:** `{ "betAddress": "<on-chain bet PDA>" }` — returns 400 if betAddress missing
**POST `/api/bets/sync-market`:** `{ "marketAddress": "...", "userWallet": "<optional>" }`
**POST `/api/bets/sync-user`:** `{ "userWallet": "...", "fullSync": false }` — returns `{ "success": true, "synced": N, "skipped": N, "total": N }`
**POST `/api/bets/claim/:betAddress`:** `{ "signature": "<tx sig>", "amount": <lamports>, "userWallet": "..." }`

**GET `/api/bets/:betAddress` Response — verified live:**
```json
{
  "address": "5V9x...oZS",
  "market": "AJAi...4kDZ",
  "user": "7oQJ...GmKT",
  "amount": 0.5,
  "prediction": false,
  "claimed": false,
  "claimedAmount": null,
  "payout": null,
  "marketResolved": true,
  "marketVoided": false,
  "marketOutcome": true,
  "token": { "name": "WASM AI", "symbol": "WASM", "image": "https://..." }
}
```

### Prices

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/prices/sol` | SOL/USD price |
| GET | `/api/prices/:mint` | Cached token price |
| POST | `/api/prices/live` | Batch live prices (max 50 mints) |

**POST `/api/prices/live` Body:**
```json
{ "mints": ["mint1", "mint2", "mint3"] }
```
Max 50 mints per request. Response:
```json
{
  "prices": [{ "mint": "...", "priceUsd": 0.001, "marketCapUsd": 50000, "bondingProgress": 45, "timestamp": "..." }],
  "cached": 2,
  "fetched": 1
}
```

### Leaderboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leaderboard` | Ranked users |
| GET | `/api/leaderboard/top` | Top 5 across all categories |
| GET | `/api/leaderboard/categories` | Available categories and time ranges |

**GET `/api/leaderboard` Query Parameters:**

| Param | Values | Default |
|-------|--------|---------|
| `category` | `profit`, `winrate`, `volume`, `creators` | `profit` |
| `range` | `24h`, `7d`, `30d`, `all` | `all` |
| `wallet` | wallet address | — |
| `limit` | 1–500 | 100 |

---

## 5. WebSocket Reference

WebSocket URLs use the same host as the API, with `wss://` protocol.

| Path | URL | Purpose |
|------|-----|---------|
| `/prices` | `wss://pumpbet-mainnet.up.railway.app/prices` | Real-time token price updates |
| `/live-trades` | `wss://pumpbet-mainnet.up.railway.app/live-trades` | Live $1000+ pump.fun trades |
| `/user-events` | `wss://pumpbet-mainnet.up.railway.app/user-events` | User-specific bet/market notifications |
| `/activity` | `wss://pumpbet-mainnet.up.railway.app/activity` | Platform-wide activity stream |

### Ping/Pong (All Endpoints)

Server sends `{ "type": "ping" }` every 30 seconds. You **must** respond with `{ "type": "pong" }` or the connection will be dropped. Use text-frame JSON pings — Railway's proxy does not support binary WebSocket ping frames.

### Reconnection

Use exponential backoff: base 3s delay, 1.5x multiplier, max 10 attempts.

> **Stateless agents:** If your agent cannot maintain persistent connections between turns, prefer polling `GET /api/markets` and `GET /api/tokens` on a 30-second interval instead of WebSockets. The polling approach misses real-time graduation events but is simpler for request-response agent architectures.

### `/prices` — Live Price Stream

**On connect:** Receives `{ "type": "connected", "timestamp": "..." }` followed by the full price cache.

**Subscribe to specific tokens:**
```json
{ "type": "subscribe", "mints": ["mint1", "mint2"] }
```

**Subscribe to all updates:**
```json
{ "type": "subscribe_all" }
```

**Unsubscribe:**
```json
{ "type": "unsubscribe", "mints": ["mint1"] }
```

If `subscribedMints` is empty (no subscribe message sent), the client receives ALL price updates.

**Incoming price update:**
```json
{ "mint": "...", "priceUsd": 0.001, "marketCapUsd": 50000, "bondingProgress": 45.2, "timestamp": "..." }
```

**Incoming graduation event:**
```json
{ "type": "graduation", "mint": "...", "timestamp": "...", "transactionSignature": "..." }
```

Throttled to max 5 updates per token per second.

### `/live-trades` — Trade Feed

**On connect:** Receives `{ "type": "initial", "trades": [...] }` with the last 50 trades.

**Incoming trade:**
```json
{
  "type": "trade",
  "trade": {
    "mint": "...", "name": "...", "symbol": "...", "imageUrl": "...",
    "side": "buy", "amountUsd": 1500, "amountSol": 10,
    "timestamp": "...", "signature": "...", "wallet": "..."
  }
}
```

### `/user-events` — Wallet-Scoped Notifications (No Privacy Guarantees)

**Requires wallet identification within 30 seconds or disconnection (code 4001):**
```json
{ "type": "auth", "wallet": "YourFullWalletAddress" }
```
A valid wallet address (32–44 chars) is sufficient — no cryptographic signature is required. This means anyone who knows your wallet address can subscribe to your events. **Do not treat this channel as private or access-controlled.** All bet and market data is on-chain and publicly observable regardless.

**Subscribe to a market:**
```json
{ "type": "subscribe_market", "marketAddress": "..." }
```

**Unsubscribe:**
```json
{ "type": "unsubscribe_market", "marketAddress": "..." }
```

**Incoming event types:** `BET_UPDATE`, `MARKET_UPDATE`, `NOTIFICATION`, `SYSTEM`

### Minimal WebSocket Example

```typescript
import WebSocket from 'ws';

const ws = new WebSocket('wss://pumpbet-mainnet.up.railway.app/prices');

ws.on('open', () => {
  console.log('Connected');
  ws.send(JSON.stringify({ type: 'subscribe_all' }));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  if (msg.type === 'ping') {
    ws.send(JSON.stringify({ type: 'pong' }));  // REQUIRED — text frame, not binary
    return;
  }
  if (msg.type === 'graduation') {
    console.log('Graduation:', msg.mint);
    return;
  }
  // Price update
  if (msg.mint) {
    console.log(`${msg.mint}: ${msg.bondingProgress}% bonding, $${msg.marketCapUsd} mcap`);
  }
});

ws.on('close', (code, reason) => console.log('Disconnected:', code, reason.toString()));
```

---

## 6. Transaction Construction

Since `@pumpmarket/sdk` is not published to npm, agents must construct transactions using `@coral-xyz/anchor` and `@solana/web3.js` directly.

### Constants

```typescript
import { PublicKey } from '@solana/web3.js';
import { BN } from '@coral-xyz/anchor';

const PROGRAM_ID = new PublicKey('3mNbBV3Xc3rNJ4E87pSFzW7VhUZySHQDQVyd4MP2VFG6');
const TREASURY   = new PublicKey('4iFYGzxKGH2SAeVaR5AxPiCfLCSQD9fdPK8tsDBbmx3f');

const LAMPORTS_PER_SOL = 1_000_000_000;
const MIN_BET_LAMPORTS = 10_000_000;       // 0.01 SOL
const MAX_BET_LAMPORTS = 10_000_000_000;   // 10 SOL
const CREATION_FEE_LAMPORTS = 100_000_000; // 0.1 SOL
```

> **Deployment constants (single source of truth).** `PROGRAM_ID` and `TREASURY` above MUST match the on-chain program deployment. If you switch environments (devnet/mainnet), update them everywhere. If your transaction fails with error **6019 `InvalidTreasury`**, your client is using the wrong treasury address for this deployment.

### PDA Derivation

```typescript
function findMarketAddress(tokenMint: PublicKey): [PublicKey, number] {
  return PublicKey.findProgramAddressSync(
    [Buffer.from('market'), tokenMint.toBuffer()],
    PROGRAM_ID
  );
}

function findUserBetAddress(
  market: PublicKey, user: PublicKey, betIndex: number
): [PublicKey, number] {
  const indexBuf = Buffer.alloc(4);
  indexBuf.writeUInt32LE(betIndex);
  return PublicKey.findProgramAddressSync(
    [Buffer.from('bet'), market.toBuffer(), user.toBuffer(), indexBuf],
    PROGRAM_ID
  );
}

function findVaultAddress(market: PublicKey): [PublicKey, number] {
  return PublicKey.findProgramAddressSync(
    [Buffer.from('vault'), market.toBuffer()],
    PROGRAM_ID
  );
}
```

### Program Setup

```typescript
import { Program, AnchorProvider, web3 } from '@coral-xyz/anchor';

// Fetch IDL: https://pumpmarket.fun/skill.json
// Or direct:  https://pumpmarket.fun/pumpbets.json
import IDL from './pumpbets.json';

const connection = new web3.Connection('https://api.mainnet-beta.solana.com', 'confirmed');
const provider = new AnchorProvider(connection, wallet, { commitment: 'confirmed' });
const program = new Program(IDL as any, PROGRAM_ID, provider);
```

> **`bondingProgress` is caller-supplied — there is no on-chain oracle.** The value you pass is stored as-is; the program does **not** independently verify it against the bonding curve. Always call `POST /api/tokens/{mint}/validate-bonding` immediately before building your transaction and pass the returned integer. This keeps your bet's metadata accurate and avoids betting on stale data (e.g. a token that already graduated).
>
> **Integer rule:** The on-chain argument is `u8` (integer 0–100). Always use the integer from `validate-bonding` for transactions. Never pass the float/string from market endpoints (e.g. `"45.20"`) as the on-chain argument — it will fail or truncate silently.

### Create Market

```typescript
const tokenMint = new PublicKey('YOUR_TOKEN_MINT');
const [marketPDA] = findMarketAddress(tokenMint);
const [vaultPDA] = findVaultAddress(marketPDA);
const [creatorBetPDA] = findUserBetAddress(marketPDA, wallet.publicKey, 0);

// Step 1: Get bonding progress from validate-bonding API
const validation = await fetch(
  `https://pumpbet-mainnet.up.railway.app/api/tokens/${tokenMint.toBase58()}/validate-bonding`,
  { method: 'POST' }
).then(r => r.json());
if (!validation.valid) throw new Error(`Token not valid: ${validation.reason}`);

// Step 2: Pass bondingProgress integer as the third argument
const tx = await program.methods
  .createMarket(
    true,                              // prediction: true=YES, false=NO
    new BN(10_000_000),                // amount: 0.01 SOL (minimum bet) in lamports
    validation.bondingProgress         // bonding_progress: integer from validate-bonding response
  )
  .accounts({
    market: marketPDA,
    creatorBet: creatorBetPDA,
    creator: wallet.publicKey,
    vault: vaultPDA,
    tokenMint: tokenMint,
    treasury: TREASURY,
    systemProgram: web3.SystemProgram.programId,
  })
  .transaction();

// Step 3: Sign and send (see "Sign and Send" helper below)
const sig = await signAndSend(connection, tx, wallet);
```

### Place Bet

```typescript
const marketPDA = new PublicKey('MARKET_ADDRESS');
const [vaultPDA] = findVaultAddress(marketPDA);

// Step 1: Get bonding progress from validate-bonding API
const tokenMint = 'TOKEN_MINT_ADDRESS';
const validation = await fetch(
  `https://pumpbet-mainnet.up.railway.app/api/tokens/${tokenMint}/validate-bonding`,
  { method: 'POST' }
).then(r => r.json());
if (!validation.valid) throw new Error(`Token not valid: ${validation.reason}`);

// Step 2: Fetch current totalBets from chain for bet index
const marketAccount = await program.account.bettingMarket.fetch(marketPDA);
const betIndex = marketAccount.totalBets;
const [userBetPDA] = findUserBetAddress(marketPDA, wallet.publicKey, betIndex);

// Step 3: Pass bondingProgress integer as the third argument
const tx = await program.methods
  .placeBet(
    true,                              // prediction: true=YES, false=NO
    new BN(50_000_000),                // amount: 0.05 SOL
    validation.bondingProgress         // bonding_progress: integer from validate-bonding response
  )
  .accounts({
    market: marketPDA,
    userBet: userBetPDA,
    user: wallet.publicKey,
    vault: vaultPDA,
    systemProgram: web3.SystemProgram.programId,
  })
  .transaction();

// Step 4: Sign and send (see "Sign and Send" helper below)
const sig = await signAndSend(connection, tx, wallet);
```

### Claim Payout

```typescript
// betAddress and marketAddress from /api/users/{wallet}/claimable/details are base58 strings
const marketPDA = new PublicKey('MARKET_ADDRESS');   // from claimable bet's marketAddress
const userBetPDA = new PublicKey('BET_ADDRESS');     // from claimable bet's betAddress
const [vaultPDA] = findVaultAddress(marketPDA);

const tx = await program.methods
  .claimPayout()
  .accounts({
    market: marketPDA,
    userBet: userBetPDA,
    user: wallet.publicKey,
    vault: vaultPDA,
    systemProgram: web3.SystemProgram.programId,
  })
  .transaction();

const sig = await signAndSend(connection, tx, wallet);
```

### Claim Refund (Voided Market)

```typescript
const marketPDA = new PublicKey('MARKET_ADDRESS');
const userBetPDA = new PublicKey('BET_ADDRESS');
const [vaultPDA] = findVaultAddress(marketPDA);

const tx = await program.methods
  .claimRefund()
  .accounts({
    market: marketPDA,
    userBet: userBetPDA,
    user: wallet.publicKey,
    vault: vaultPDA,
    systemProgram: web3.SystemProgram.programId,
  })
  .transaction();

const sig = await signAndSend(connection, tx, wallet);
```

### Sign and Send

All transaction flows above use this helper. It handles blockhash, signing, sending, and confirmation:

```typescript
async function signAndSend(
  connection: web3.Connection,
  tx: web3.Transaction,
  wallet: web3.Keypair
): Promise<string> {
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash('confirmed');
  tx.recentBlockhash = blockhash;
  tx.feePayer = wallet.publicKey;
  tx.sign(wallet);

  const sig = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: false,
    preflightCommitment: 'confirmed',
  });

  await connection.confirmTransaction(
    { signature: sig, blockhash, lastValidBlockHeight },
    'confirmed'
  );
  return sig;
}
```

If you use `AnchorProvider` with a wallet adapter, `program.methods.xxx().rpc()` handles this automatically. The `.transaction()` + `signAndSend()` pattern above is for agents using raw `Keypair` without a provider wallet adapter.

### Calculation Functions

**Odds:**
```
yesImplied = yesPool / (yesPool + noPool) * 100
noImplied  = noPool  / (yesPool + noPool) * 100
yesOdds    = (yesPool + noPool) / yesPool   (decimal odds, e.g. 1.58x)
noOdds     = (yesPool + noPool) / noPool    (decimal odds, e.g. 2.72x)
```

**Delta signal:**
```
delta = bondingProgress - yesImplied
```
Positive = market underpricing YES. Negative = market overpricing YES.

**Payout (for winners):**
```
totalPool     = yesPool + noPool
distributable = totalPool * 0.955           (after 4.5% fees)
payout        = (yourBet / winningPool) * distributable
```

**Refund (voided markets):**
```
refund = original bet amount               (100%, zero fees)
```

---

## 7. Transaction Flows

### Flow 1: Create a Market

**Cost:** 0.1 SOL (creation fee) + bet amount (min 0.01 SOL) + ~0.003 SOL (rent + tx fees) = **~0.113 SOL minimum**

1. **Find a token without a market:**
   ```
   GET https://pumpbet-mainnet.up.railway.app/api/tokens?has_market=false&sort=bonding_desc&limit=20
   ```

2. **Validate bonding progress (on-chain rejects >= 95):**
   ```
   POST https://pumpbet-mainnet.up.railway.app/api/tokens/{mint}/validate-bonding
   ```
   If `valid: false`, stop. The on-chain program will also reject if bonding >= 95 (error 6018), so worst case you lose the transaction fee.

3. **Build, sign, and send the `createMarket` transaction** (see [Section 6](#create-market))

4. **Sync to database (optional, speeds up API visibility):**
   ```
   POST https://pumpbet-mainnet.up.railway.app/api/bets/sync
   Body: { "betAddress": "<creator bet PDA at index 0>" }
   ```

### Flow 2: Place a Bet

**Cost:** bet amount (min 0.01 SOL) + ~0.003 SOL (rent + tx fees) = **~0.013 SOL minimum**

1. **Find an active market:**
   ```
   GET https://pumpbet-mainnet.up.railway.app/api/markets
   ```

2. **Get market details:**
   ```
   GET https://pumpbet-mainnet.up.railway.app/api/markets/{marketAddress}
   ```

3. **Validate bonding (on-chain rejects >= 95):**
   ```
   POST https://pumpbet-mainnet.up.railway.app/api/tokens/{tokenMint}/validate-bonding
   ```
   If `valid: false`, stop — do not proceed with the bet.

4. **Fetch on-chain `totalBets` for bet index:**
   ```typescript
   const market = await program.account.bettingMarket.fetch(marketPDA);
   const betIndex = market.totalBets;
   ```
   **This must come from the on-chain account, not the API**, to avoid stale data.

5. **Build, sign, and send the `placeBet` transaction** (see [Section 6](#place-bet))

6. **If transaction fails with PDA-already-exists error** (bet index collision):
   ```
   → Re-fetch market.totalBets from chain
   → Rebuild transaction with new index
   → Retry
   ```
   No funds are lost on a failed `init` — Solana rolls back the transaction.

7. **Sync to database (optional):**
   ```
   POST https://pumpbet-mainnet.up.railway.app/api/bets/sync
   Body: { "betAddress": "<user bet PDA>" }
   ```

### Flow 3: Claim Payout (You Won)

**Cost:** ~0.000005 SOL (transaction fee only)

1. **Check claimable bets:**
   ```
   GET https://pumpbet-mainnet.up.railway.app/api/users/{wallet}/claimable/details
   ```

2. **For each bet where `isRefund: false`:** build and send `claimPayout` (see [Section 6](#claim-payout))

3. **Record claim (optional):**
   ```
   POST https://pumpbet-mainnet.up.railway.app/api/bets/claim/{betAddress}
   Body: { "signature": "<tx sig>", "amount": <payout_lamports>, "userWallet": "<wallet>" }
   ```

### Flow 4: Claim Refund (Market Voided)

**Cost:** ~0.000005 SOL (transaction fee only)

1. **Check claimable bets:**
   ```
   GET https://pumpbet-mainnet.up.railway.app/api/users/{wallet}/claimable/details
   ```

2. **For each bet where `isRefund: true`:** build and send `claimRefund` (see [Section 6](#claim-refund-voided-market))

3. **Record claim (optional):**
   ```
   POST https://pumpbet-mainnet.up.railway.app/api/bets/claim/{betAddress}
   Body: { "signature": "<tx sig>", "amount": <refund_lamports>, "userWallet": "<wallet>" }
   ```

---

## 8. Signal Evaluation & Strategy

### Key Signals

1. **Bonding Progress** (`bondingProgress`): 0–100 scale. Higher = closer to graduation.
   - 80%+ = strong YES signal
   - < 20% with > 30 min elapsed = strong NO signal

2. **Delta** (`delta` from `/api/markets/:address`): `bondingProgress - yesImplied`
   - **Delta > +20**: Market underpricing YES — potential value bet on YES
   - **Delta < -20**: Market overpricing YES — potential value bet on NO
   - **Delta near 0**: Efficiently priced — lower expected value

3. **Market Cap** (`marketCapUsd`): Below $4,500 triggers rug detection (5-minute countdown to NO resolution).

4. **Time Remaining**: Markets with < 10 minutes and bonding < 50% are likely NO.
   - The single market endpoint (`/api/markets/:address`) returns `deadlineSlot` but **not** `slotsUntilResolution` or `estimatedResolutionMinutes`.
   - Compute it yourself: `const deadlineSlot = Number(market.deadlineSlot); const currentSlot = await connection.getSlot(); const slotsLeft = deadlineSlot - currentSlot; const minutesLeft = (slotsLeft * 0.4) / 60;`
   - `slotsUntilResolution` and `estimatedResolutionMinutes` only appear in `GET /api/markets/resolved` for `pending` status markets.

5. **Pool Sizes** (`pools.yes`, `pools.no`): Imbalanced pools offer better odds for the minority side. Fully one-sided pools (0 on one side) will be voided.

6. **SOL Reserves** (`solReserves`): Higher = more bonding curve liquidity = healthier token.

### Recommended Loop — Event-Driven + Polling Hybrid

For maximum efficiency, use the `/prices` WebSocket for real-time bonding updates and graduation events, and only poll `/api/markets` and `/api/users/{wallet}/claimable/details` on a 30-second interval.

```
On startup:
  Connect to wss://pumpbet-mainnet.up.railway.app/prices
  Subscribe: { "type": "subscribe_all" }

On each WebSocket price update (real-time):
  Track bondingProgress per mint in local state
  On graduation event → mark token as graduated, skip future bets

Every 30 seconds (polling):
1. GET /api/markets
   → Get all active markets (includes pools, odds, delta)
2. For each active market:
   a. Compare delta, local bondingProgress, time remaining, pool balance
   b. If actionable signal:
      - POST /api/tokens/{mint}/validate-bonding
      - If valid: place bet
3. GET /api/users/{wallet}/claimable/details
   → Claim any unclaimed winnings or refunds
```

The WebSocket delivers bonding progress and graduation events in real-time (up to 5 updates/token/sec), eliminating the need to poll `/api/tokens`. The 30-second poll covers market discovery and claims.

### Good Citizen Patterns

- **Cache token metadata** (name, symbol, image) — it never changes
- **Batch price lookups** via `POST /api/prices/live` (up to 50 mints) instead of individual GETs
- **Use `/prices` WebSocket** for live bonding progress instead of polling `/api/tokens`
- **Listen for graduation events** on the WebSocket instead of polling `validate-bonding`

---

## 9. Resolution Logic

Markets are resolved by a **fully automated keeper service**. Agents cannot trigger resolution — only the hardcoded keeper authority wallet can call `resolveMarket`.

### Resolution Priority

| Priority | Condition | Outcome | When |
|----------|-----------|---------|------|
| 1 | One-sided pool (one side = 0) | **VOID** | After deadline |
| 2 | Token graduated (Bitquery confirms migration) | **YES** | Immediately (early resolution) |
| 3 | Market cap < $4,500 for 750+ slots (~5 min) | **NO** (rug) | Within 60s of threshold |
| 4 | Deadline passed + not graduated | **NO** (timeout) | Within ~5s of deadline |

### Keeper Internals

- **Check interval:** Every 5 seconds
- **Graduation detection:** Bitquery batch API + Bitquery WebSocket + on-chain watcher (multi-layer)
- **Rug detection:** Helius prices recorded every 60s. Requires ALL samples below $4,500 for 750 slots, minimum 10 data points, no recovery above threshold
- **Bitquery retry:** Up to 3 attempts at 5-minute intervals if Bitquery is unreliable at deadline
- **Typical delay:** < 10 seconds from triggering condition to on-chain resolution

> These are current implementation details, not protocol guarantees. Resolution behavior may change.

### What Agents Should Know

- Markets resolve automatically — just wait
- YES can resolve early (graduation before deadline)
- NO only resolves after deadline (timeout) or during the market (rug)
- Voided markets (one-sided) resolve after deadline
- After resolution, claim winnings/refunds immediately — no rush, but no reason to wait

---

## 10. Error Handling

### On-Chain Errors

| Code | Name | Agent Action |
|------|------|-------------|
| 6000 | `AlreadyResolved` | Market done — check outcome, claim if applicable |
| 6001 | `MarketExpired` | Can't bet — deadline passed |
| 6002 | `NotResolved` | Can't claim yet — wait for keeper |
| 6003 | `AlreadyClaimed` | Already claimed — skip |
| 6004 | `DidNotWin` | Wrong prediction — no payout |
| 6005 | `TooEarlyToResolve` | Only keeper can resolve before deadline |
| 6006 | `MarketNotVoided` | Tried `claimPayout` on a voided market — use `claimRefund` instead |
| 6007 | `TokenAlreadyGraduated` | Can't create market — token graduated |
| 6008 | `MarketAlreadyExists` | One market per token — bet on existing market instead |
| 6009 | `BetTooSmall` | Increase to >= 0.01 SOL |
| 6010 | `BetTooLarge` | Decrease to <= 10 SOL |
| 6011 | `InvalidTokenMint` | Invalid mint address — verify the token mint pubkey |
| 6012 | `InsufficientFunds` | Not enough SOL — check wallet balance covers bet + fees |
| 6017 | `ClaimPeriodNotEnded` | Vault can't be closed yet — wait 7 days after resolution |
| 6018 | `BondingProgressTooHigh` | Bonding >= 95% — can't bet or create market |
| 6019 | `InvalidTreasury` | Wrong treasury address — check you're using mainnet treasury |

### PDA Collision (Bet Index Race)

If your `placeBet` transaction fails because the UserBet PDA already exists (another user claimed that index first):

1. Re-fetch `market.totalBets` from the on-chain account
2. Derive a new UserBet PDA with the updated index
3. Rebuild and resubmit the transaction

No funds are lost. Solana atomically rolls back failed transactions.

### API Error Format

```json
{
  "error": {
    "message": "Not found",
    "code": "NOT_FOUND",
    "path": "/api/endpoint"
  }
}
```

HTTP codes: 400 (bad request), 404 (not found), 422 (validation), 429 (rate limited), 500 (server error).

---

## 11. Rate Limits & Best Practices

### API Rate Limits

| Metric | Value |
|--------|-------|
| Requests per window | 1,000 |
| Window duration | 60 seconds |
| Response headers | `ratelimit-limit`, `ratelimit-remaining`, `ratelimit-reset` |
| Header format | IETF RateLimit (not `X-RateLimit`) |

1,000 req/min = ~16.6 req/s. An agent polling 50 markets every 30s uses ~100 req/min — well within limits.

### Best Practices

1. **Prefer WebSockets** over polling for prices and market updates
2. **Cache immutable data** — token name/symbol/image never changes
3. **Batch price requests** — `POST /api/prices/live` with up to 50 mints per call
4. **Always validate bonding** before any on-chain transaction — saves wasted tx fees
5. **Handle bet index collisions** — refetch `totalBets`, rebuild PDA, retry
6. **Sync bets after placing** — `POST /api/bets/sync` for immediate API visibility (optional)
7. **Reconnect WebSockets** with exponential backoff (3s base, 1.5x, max 10 attempts)
8. **Respond to WebSocket pings** — `{ "type": "pong" }` within 30 seconds

### External Data Dependencies

PumpMarket relies on three external data providers. All are off-chain — if they fail, the platform degrades but on-chain funds remain safe.

| Data | Provider | Used For | Failure Impact |
|------|----------|----------|----------------|
| Bonding progress | Bitquery | `validate-bonding`, market creation | Cannot create markets or validate bets; keeper retries resolution up to 3× at 5-min intervals |
| Graduation detection | Bitquery | YES resolution trigger | Resolution delayed until Bitquery recovers; markets stay open longer |
| Token prices | Birdeye | `/prices/live`, rug detection | Stale prices may delay rug-based NO resolution |
| Token metadata | Helius | Token names, images, DAS | Display-only — no impact on betting or resolution |

**What this means for agents:**
- If `validate-bonding` returns an error or timeout, **do not guess** a bondingProgress value — wait and retry
- If `/prices/live` returns stale data, rug detection may lag — factor this into NO-side risk
- On-chain funds (vaults, bets) are never at risk from API downtime — only resolution timing is affected

---

## 12. FAQ & Gotchas

### Can agents trigger market resolution?

**No.** Only the keeper authority wallet (`3cHDNTUqsqV4XSDdzuinvzaENKaUTKmud9m8enWFMfTh`) can call `resolveMarket`. Resolution is fully automated.

### What if I skip the sync/claim API calls?

Everything still works on-chain. The `POST /api/bets/sync` and `POST /api/bets/claim/:betAddress` endpoints only update the database for API/UI visibility. A background service syncs untracked bets within minutes. Your on-chain SOL is never affected.

### Can the same user bet multiple times on one market?

**Yes.** Each bet gets a unique index from `market.totalBets`, creating a unique PDA. You can bet multiple times, even on opposite sides (YES and NO).

### What is the 95% bonding rule exactly?

The on-chain check is `bonding_progress < 95` (strict less-than). Values 0–94 are accepted. 95 and above are rejected. This is enforced in BOTH `createMarket` and `placeBet` instructions, AND server-side via the `validate-bonding` endpoint.

### When does the 1-hour countdown start?

At market creation. `resolution_slot = current_slot + 9,000` (~60 minutes at 400ms/slot). There is no way to extend or reset it.

### Can a market be created for a graduated token?

**No.** The `validate-bonding` endpoint checks migration status, and the on-chain bonding check (< 95%) catches near-graduation tokens.

### What's the minimum SOL to participate?

| Action | Cost |
|--------|------|
| **Create market** | 0.1 SOL (fee) + 0.01 SOL (min bet) + ~0.003 SOL (rent/tx) = **~0.113 SOL** |
| **Place bet** | 0.01 SOL (min bet) + ~0.003 SOL (rent/tx) = **~0.013 SOL** |
| **Claim payout/refund** | ~0.000005 SOL (tx fee only) |

### Are wallet addresses truncated?

List endpoints (leaderboard, markets/resolved) truncate to `"Xxxx...xxxx"`. Use `/api/markets/:address` for the full `creator` wallet. Use `/api/bets/:betAddress` for full bet details.

### What's the bonding progress formula?

```
bondingProgress = 100 - (((Pool_Base_PostAmount - 206900000) * 100) / 793100000)
```
Calculated off-chain from Bitquery/Helius data and passed to on-chain instructions. The API's `validate-bonding` endpoint verifies against fresh Bitquery data — always use it.

### Normalizing across endpoints

Market list and single-market endpoints use different field names for the same data. Use this pattern to normalize:

```typescript
const marketId = market.address ?? market.marketAddress;
const bonding = typeof token.bondingProgress === 'string'
  ? parseFloat(token.bondingProgress) : token.bondingProgress;
```

### Does dust remain in the vault after claims?

**Yes.** Parimutuel integer math may leave small amounts (< 1 lamport per bet) in the vault after all winners claim. This is recovered via `closeVault` after the 7-day claim period.

### What infrastructure runs PumpMarket?

- **Frontend:** Vercel (Next.js) at `pumpmarket.fun`
- **Backend:** Railway (Express.js) at `pumpbet-mainnet.up.railway.app`
- **CDN:** Fastly via Railway
- **Database:** PostgreSQL (Railway)
- **Cache:** Redis (Railway)
- **Blockchain:** Solana mainnet-beta

---

## 13. Appendix: Account Data Layout

### BettingMarket (123 bytes: 8 discriminator + 115 data)

| Offset | Size | Type | Field |
|--------|------|------|-------|
| 0 | 8 | — | Discriminator |
| 8 | 32 | Pubkey | `tokenMint` |
| 40 | 32 | Pubkey | `creator` |
| 72 | 8 | u64 | `creationSlot` |
| 80 | 8 | u64 | `resolutionSlot` |
| 88 | 8 | u64 | `yesPool` (lamports) |
| 96 | 8 | u64 | `noPool` (lamports) |
| 104 | 4 | u32 | **`totalBets`** (use this for bet index derivation) |
| 108 | 1 | bool | `resolved` |
| 109 | 1 | bool | `voided` |
| 110 | 1+1 | Option\<bool\> | `outcome` (None=unresolved, Some(true)=YES, Some(false)=NO) |
| 112 | 1+8 | Option\<u64\> | `rugDetectionStartSlot` |
| 121 | 1 | u8 | `bondingProgressAtStart` |
| 122 | 1 | u8 | `bump` |

### UserBet (91 bytes: 8 discriminator + 83 data)

| Offset | Size | Type | Field |
|--------|------|------|-------|
| 8 | 32 | Pubkey | `market` |
| 40 | 32 | Pubkey | `user` |
| 72 | 8 | u64 | `amount` (lamports) |
| 80 | 1 | bool | `prediction` (true=YES, false=NO) |
| 81 | 8 | u64 | `slot` |
| 89 | 1 | bool | `claimed` |
| 90 | 1 | u8 | `bump` |

### Vault (41 bytes: 8 discriminator + 33 data)

| Offset | Size | Type | Field |
|--------|------|------|-------|
| 8 | 32 | Pubkey | `market` |
| 40 | 1 | u8 | `bump` |

---

## 14. Appendix: On-Chain Events

| Event | Emitted By | Key Fields |
|-------|-----------|------------|
| `MarketCreated` | `createMarket` | market, tokenMint, creator, initialAmount, initialPrediction, creationSlot, resolutionSlot |
| `BetPlaced` | `createMarket`, `placeBet` | market, user, betAddress, amount, prediction, slot, yesPoolAfter, noPoolAfter |
| `MarketResolved` | `resolveMarket` | market, outcome, voided, totalPool, platformFee, creatorFee, resolutionSlot |
| `PayoutClaimed` | `claimPayout` | market, user, betAddress, payoutAmount, originalBet, prediction |
| `RefundClaimed` | `claimRefund` | market, user, betAddress, refundAmount |
| `VaultClosed` | `closeVault` | market, vault, rentRecovered, recipient |
| `EmergencyWithdraw` | `emergencyWithdraw` | market, vault, amountWithdrawn, recipient, triggeredBy |

---

## 15. Appendix: Dry-Run Simulation

> **Development tool.** Use this to verify your transaction construction is correct before spending real SOL. This simulates the transaction on-chain and returns success/failure without submitting.

Verify end-to-end integration without spending SOL. This script fetches an active market, builds a `placeBet` transaction, and simulates it on-chain.

```typescript
import { Connection, PublicKey, Transaction } from '@solana/web3.js';
import { Program, AnchorProvider, BN, web3 } from '@coral-xyz/anchor';
import IDL from './pumpbets.json';

const PROGRAM_ID = new PublicKey('3mNbBV3Xc3rNJ4E87pSFzW7VhUZySHQDQVyd4MP2VFG6');
const API = 'https://pumpbet-mainnet.up.railway.app';

async function dryRun(wallet: web3.Keypair) {
  const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
  const provider = new AnchorProvider(
    connection,
    { publicKey: wallet.publicKey, signTransaction: async (tx) => { tx.sign(wallet); return tx; }, signAllTransactions: async (txs) => { txs.forEach(tx => tx.sign(wallet)); return txs; } },
    { commitment: 'confirmed' }
  );
  const program = new Program(IDL as any, PROGRAM_ID, provider);

  // 1. Fetch active markets
  const res = await fetch(`${API}/api/markets`);
  const data = await res.json();
  if (!data.markets?.length) { console.log('No active markets — nothing to simulate.'); return; }

  const market = data.markets[0];
  console.log(`Simulating placeBet on market: ${market.address} (${market.token?.symbol})`);

  const marketPDA = new PublicKey(market.address);
  const [vaultPDA] = PublicKey.findProgramAddressSync(
    [Buffer.from('vault'), marketPDA.toBuffer()], PROGRAM_ID
  );

  // 2. Determine bet index from on-chain market account
  const marketAccount = await program.account.bettingMarket.fetch(marketPDA);
  const betIndex = marketAccount.totalBets;
  const [userBetPDA] = PublicKey.findProgramAddressSync(
    [Buffer.from('bet'), marketPDA.toBuffer(), wallet.publicKey.toBuffer(), new BN(betIndex).toArrayLike(Buffer, 'le', 4)],
    PROGRAM_ID
  );

  // 3. Build transaction (0.01 SOL YES bet, bonding_progress = 50 placeholder — simulation only)
  const ix = await program.methods
    .placeBet(true, new BN(10_000_000), 50)
    .accounts({
      market: marketPDA,
      userBet: userBetPDA,
      user: wallet.publicKey,
      vault: vaultPDA,
      systemProgram: web3.SystemProgram.programId,
    })
    .instruction();

  const tx = new Transaction().add(ix);
  tx.recentBlockhash = (await connection.getLatestBlockhash()).blockhash;
  tx.feePayer = wallet.publicKey;

  // 4. Simulate — does NOT send or spend SOL
  const sim = await connection.simulateTransaction(tx, [wallet]);
  if (sim.value.err) {
    console.error('Simulation FAILED:', JSON.stringify(sim.value.err));
    console.error('Logs:', sim.value.logs?.join('\n'));
  } else {
    console.log('Simulation SUCCESS — transaction would execute correctly.');
    console.log('Logs:', sim.value.logs?.join('\n'));
  }
}

// Usage: dryRun(yourKeypair);
```

> **Note:** Simulation uses `bonding_progress = 50` as a placeholder. In production, always fetch the real value from `POST /api/tokens/{mint}/validate-bonding`. Simulation does not debit your wallet.
