---
name: kryptone-escrow-agent
description: Register as buyer or seller, create and manage USDC escrow trades on Kryptone/PrivacyEscrow via HTTP API using agent API key or human JWT auth.
requirements: >-
  Node.js 18+. Server must have optional AGENT_API_KEY and AGENT_SOLANA_ADDRESS set for x-api-key auth.
  Client needs KRYPTONE_API_BASE_URL and AGENT_API_KEY matching the server. Treasury and Privacy Cash env must be configured on the server for settle.
keywords:
  - kryptone
  - privacyescrow
  - solana
  - usdc
  - escrow
  - api
---

# Kryptone escrow agent skill

Use this skill when an agent should drive **buy/sell escrow flows** against a running **Kryptone/PrivacyEscrow** API. Pricing and deposits are **USDC (SPL)** only.

## Authentication (two modes)

Same JSON bodies and paths; choose one auth style per request.

| Mode | Headers | When |
|------|---------|------|
| Human / web app | `Authorization: Bearer <JWT>` | After wallet signs `/api/auth/login`. Do **not** put an API key in the Bearer field. |
| Agent / automation | `x-api-key: <AGENT_API_KEY>` | Server maps the key to `AGENT_SOLANA_ADDRESS`. Requires operator to set `AGENT_API_KEY` and `AGENT_SOLANA_ADDRESS` in server `.env`. |

If the server does **not** set `AGENT_API_KEY`, only JWT (or legacy Solana signature headers) work.

## Environment

**Server (`.env`):**

- `AGENT_API_KEY` – shared secret; clients send it in `x-api-key`.
- `AGENT_SOLANA_ADDRESS` – Solana public key the agent acts as (register as Buyer or Seller for that wallet).
- Usual escrow vars: `TREASURY_WALLET`, `TREASURY_PRIVATE_KEY`, `SOLANA_RPC_URL`, `USDC_MINT`, `JWT_SECRET`, etc.

**Client (scripts or agent runtime):**

- `KRYPTONE_API_BASE_URL` – e.g. `http://localhost:5001` (no trailing slash required).
- `AGENT_API_KEY` – must equal server `AGENT_API_KEY`.

## Core endpoints (authenticated)

| Method | Path | Role / notes |
|--------|------|----------------|
| GET | `/api/user/info` | Current wallet and user type |
| POST | `/api/user/register` | Body `{ "userType": "Buyer" \| "Seller" }` |
| GET | `/api/trades` | List trades for authenticated wallet |
| POST | `/api/trades` | Seller creates trade: `{ "itemName", "priceInUsdc", "buyerWallet", optional "description", optional "adId" }` |
| GET | `/api/trades/:tradeId` | Trade detail + payment flags |
| POST | `/api/trades/:tradeId/accept` | **Buyer** – returns base64 unsigned USDC deposit tx |
| POST | `/api/trades/:tradeId/deposit-signature` | **Buyer** – body `{ "txSignature" }` after signing/sending deposit |
| POST | `/api/trades/:tradeId/reject` | **Buyer** |
| POST | `/api/trades/:tradeId/settle` | **Buyer** – triggers server Privacy Cash settle (needs treasury config) |
| POST | `/api/trades/:tradeId/disputes` | Open dispute |
| POST | `/api/ads` | **Buyer** – create ad |
| GET | `/api/ads` | Buyers: own ads; Sellers: open ads |

Admin routes (`/api/admin/...`) use separate admin wallet checks; do not assume agent key grants admin access.

## Flow A – Agent wallet is the **buyer**

1. Register: `POST /api/user/register` with `userType: "Buyer"` (once).
2. Seller (another wallet or platform) creates a trade with `buyerWallet` = your `AGENT_SOLANA_ADDRESS`.
3. `POST /api/trades/:tradeId/accept` → response includes `transaction` (base64). **Sign and submit** that transaction with the buyer’s Solana keypair (human-in-the-loop wallet, or a separate high-risk signing process—never embed private keys in prompts).
4. `POST /api/trades/:tradeId/deposit-signature` with on-chain `txSignature`.
5. When status allows, `POST /api/trades/:tradeId/settle` (buyer-only; server uses treasury).

Optional: `POST /api/ads` to publish a buyer ad; a seller can attach `adId` when creating a trade.

## Flow B – Agent wallet is the **seller**

1. Register: `userType: "Seller"`.
2. `POST /api/trades` with `buyerWallet`, `itemName`, `priceInUsdc` (and optional `adId` / `description`).
3. Buyer (human or other automation) accepts, signs deposit, submits signature, and settles—or coordinate out of band.

## CLI helpers (this folder)

From `skill/kryptone-escrow-agent/`:

```bash
export KRYPTONE_API_BASE_URL=http://localhost:5001
export AGENT_API_KEY=your-server-agent-key

npm run register -- Seller
npm run create-trade -- <buyerWallet> "Item" 12.5 "optional description"
npm run accept-deposit -- <tradeId>
npm run submit-deposit-sig -- <tradeId> <onChainSignature>
npm run settle -- <tradeId>
```

Scripts send `x-api-key` only. For JWT-based testing, use `curl` or the Postman collection at repo root.

## Operational notes

- Wrong `x-api-key` returns **401**; the server does not fall through to JWT for that request.
- One API key maps to **one** Solana identity; rotate `AGENT_API_KEY` if exposed.
- Deposit settlement on-chain is still **buyer-signed**; the API key cannot replace the buyer’s signature for the SPL transfer.
