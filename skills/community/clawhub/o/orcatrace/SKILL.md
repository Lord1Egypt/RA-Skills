---
name: orcatrace
version: 1.0.0
description: >-
  Polymarket intelligence for AI agents — track smart money, see what others miss. Real-time
  prediction-market signals across 42K markets: quality-gated repricings with order-book
  microstructure, tracked-whale entries annotated with each wallet's hold-to-resolution
  calibration (follow/fade), and AI-detected predetermined-outcome markets — one unified feed.
  Plus the 4-hourly Intelligence Digest, markets resolving soon, whale calibration tables, and
  $1 single-market deep research. Pay-per-call via x402 (USDC on Base only); no accounts, no API
  keys. Free /v1/index, /v1/pulse, /v1/digest/brief, /v1/sample, and /v1/track-record (a
  verifiable whale scorecard) expose the funnel and every paid shape before you pay.
homepage: https://orcatrace.dev
metadata:
  openclaw:
    emoji: "🐋"
    requires:
      bins: ["node"]
---

# OrcaTrace — Polymarket Intelligence for AI Agents

API at `https://api.orcatrace.dev` (website `https://orcatrace.dev`). **Track smart money, see what others miss.** OrcaTrace serves real-time Polymarket signals across 42K markets in one unified, index-polled feed: quality-gated **movers** (genuine repricings, noise-filtered, vol >= $10k & depth >= $2.5k, with order-book microstructure), tracked-**whale entries** (each annotated with that wallet's hold-to-resolution calibration — a follow/fade/neutral label from resolved, on-chain-auditable positions), and AI-detected **predetermined** markets (outcome already exists in definitive form). On top of the feed it produces the 4-hourly **Intelligence Digest**, lists **markets resolving soon**, publishes a **whale calibration table**, and runs on-demand **$1 single-market deep research**. Strictly pay-per-call via x402 — no accounts, no API keys, no bundles.

> OrcaTrace is the Polymarket-intelligence product spun out of moltalyzer. The old paths `/api/polymarket/*` on `api.moltalyzer.xyz` **308-redirect** here — point new integrations at `api.orcatrace.dev`.

## Free endpoints (no auth, no payment)

Poll the free feeds to detect new items and learn every paid response shape before paying. `/v1/sample` returns static samples of every paid shape, explicitly labelled, so it is safe for shape-testing without implying live data. `/v1/track-record` is the **verifiable free proof** behind paid `/v1/whales` — it publishes full public wallet addresses so you can cross-check every claim on Polymarket before paying. All free endpoints are rate-limited **5/min per IP**.

| Method | Path | Rate limit | Description |
|--------|------|-----------|-------------|
| GET | `/v1/index` | 5/min | Poll target — current feed index, `totalToday`, `todayByType`, and latest digest pointer (~10min cadence), so agents detect new items without paying |
| GET | `/v1/pulse` | 5/min | Top-3 Polymarket repricings (24h, noise-filtered) plus a digest teaser — the hook |
| GET | `/v1/digest/brief` | 5/min | Intelligence Digest teaser: title + summary, no analysis. Full digest at GET `/v1/digest` ($0.10) |
| GET | `/v1/sample` | 5/min | Static samples of every paid response shape (signal, whales, digest), explicitly labelled. Learn the contract before paying |
| GET | `/v1/track-record` | 5/min | Verifiable whale-calibration scorecard — the free proof behind paid `/v1/whales`: aggregate hold-to-resolution win rate, follow/fade ROI, per-odds-band breakdown, and top wallets with **full public addresses**. Cross-check any wallet on-chain before paying |

```bash
curl https://api.orcatrace.dev/v1/track-record
```

## Paid endpoints (x402 V2, USDC on Base only, per-call)

Each paid call is a flat price per call, settled per call via x402. Networks: **Base Mainnet only** (`eip155:8453`). Two settlement patterns apply (see notes below the table).

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | `/v1/latest` | **$0.01** | Most recent Polymarket feed item — mover, whale entry (with calibration), or predetermined signal. Same shape as `/v1/signal` without `?index` |
| GET | `/v1/signal?index=N` | **$0.01** | One feed item: quality-gated mover (+order-book microstructure), whale entry (named whale, +calibration), or predetermined signal. `?index=N` for a specific item, omit for latest |
| GET | `/v1/signals?since=N&type=mover` | **$0.03** | Batch feed items (up to 20). Poll GET `/v1/index` (free), then `?since=N` for new items; filter with `&type=mover\|whale_entry\|predetermined` |
| GET | `/v1/resolving?withinHours=24` | **$0.02** | Markets resolving within `?withinHours` (1-72): odds, contested-vs-converged, liquidity, and order-book microstructure. Mechanical short-interval markets excluded by default (`?includeNoise=1`) |
| GET | `/v1/whales` | **$0.05** | Whale calibration table: per-wallet hold-to-resolution win rates by odds band, mirror/fade ROI, and follow/fade labels (min 30 resolved entries). Free proof: GET `/v1/track-record` |
| GET | `/v1/digest` | **$0.10** | Full 4-hourly Intelligence Digest: what repriced and why across 42K markets — moves, whale positioning through calibration, predetermined signals, international news context. Synthesized analysis, not raw data |
| GET | `/v1/digest/history?hours=24&limit=6` | **$0.05** | Historical Intelligence Digests (up to 7 days, 4h cadence) — track how prediction-market narratives evolved |
| GET | `/v1/research?market=<slug>` | **$1.00** | Single-market deep-dive: 7-day price action + live order book + tracked-whale positioning with calibration + related news, synthesized into a thesis with risks and an actionable bottom line. Generated on demand (10-60s), cached 30 min |

**Params.** `/v1/signal`: `index` (integer, omit for latest). `/v1/signals`: `since` (integer, poll cursor), `count` (integer 1-20, default 10), `type` (`mover`, `whale_entry`, or `predetermined`). `/v1/resolving`: `withinHours` (integer 1-72, default 24), `minLiquidity` (number >=1000, default 5000), `includeNoise` (set to `1` to include mechanical short-interval markets). `/v1/digest/history`: `hours` (integer 1-168, default 24), `limit` (integer 1-42, default 6). `/v1/research`: `market` (Polymarket market slug, **required** — from `polymarket.com/market/<slug>` or our feed items). All prices are USD, settled as USDC (6 decimals) on Base.

### Settlement patterns — never charged for nothing

- **Compute-first / settle-after** (DB reads: `latest`, `signal`, `signals`, `digest`, `digest/history`) — computed first, settled after; you are **never charged for an error**.
- **`/v1/digest` never serves stale data** — a digest older than 6 hours is not sold: the route returns **503 (no charge)** rather than serving stale paid intelligence.
- **Settle-early with a GUARANTEED refund** (proxied compute: `resolving`, `whales`, `research`) — these settle early to dispatch the compute, but are guaranteed: if OrcaTrace charges you and cannot deliver a 2xx result, the payment is **automatically refunded** (a rail-tagged RefundRequest is queued and issued off the public edge).

## Paying (x402)

Paid routes settle per call via **x402 V2**. The only accepted rail is **USDC on Base Mainnet** (`eip155:8453`) — no other network. No account, no signup, no API key.

Pay flow:
1. Call the paid route with no payment → receive **HTTP 402**. The x402 V2 `PaymentRequirements` ride in the base64 `PAYMENT-REQUIRED` header; the JSON body mirrors the price + `accepts`.
2. Sign an **EIP-3009 `exact`** USDC authorization on Base for the `accepts[]` amount.
3. Retry the same request with the payment in the `PAYMENT-SIGNATURE` (V2) or `X-PAYMENT` (legacy) header.

```bash
# 1. Probe for the 402 challenge (price + accepts):
curl -i "https://api.orcatrace.dev/v1/whales"
# → HTTP/1.1 402 Payment Required, PAYMENT-REQUIRED header (base64 requirements)

# 2. Sign + retry with a stock x402 client (handles the whole flow):
```

```typescript
import { wrapFetchWithPayment } from "@x402/fetch";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const wallet = createWalletClient({ account, chain: base, transport: http() });
const fetchWithPay = wrapFetchWithPayment(fetch, wallet); // signs EIP-3009 on 402, retries

// $0.05 — whale calibration table (free proof: /v1/track-record):
const whales = await fetchWithPay(
  "https://api.orcatrace.dev/v1/whales",
).then((r) => r.json());
// whales.data.wallets[] (pseudonym, wallet, resolved, winRate, fadeRoi, label)

// $1.00 — single-market deep research (guaranteed refund on non-delivery):
const research = await fetchWithPay(
  "https://api.orcatrace.dev/v1/research?market=next-us-iran-meeting-switzerland",
).then((r) => r.json());
```

Stock x402 clients (`@x402/fetch`, `@x402/axios`, python `x402`) do the 402 → sign → retry automatically. Discover the machine-readable route + price catalog at `/.well-known/x402`.

## Free funnel

Try the whole product for free before you pay. Poll `/v1/index` (5/min) to detect new feed items on their ~10min cadence; read `/v1/pulse` (5/min) for the top-3 24h movers + digest teaser, `/v1/digest/brief` (5/min) for the digest title + summary; hit `/v1/sample` (5/min) for static samples of every paid response shape to learn the exact contract before spending. `/v1/track-record` (5/min) is the verifiable whale scorecard with **full public wallet addresses** — the free proof behind paid `/v1/whales`, so you can audit every calibration claim on Polymarket before paying a cent. Feed items and digests carry `createdAt` provenance so you always know how fresh the data is.

## Machine discovery

| Path | What |
|------|------|
| `/llms.txt` | This doc (concise) |
| `/llms-full.txt` | Extended agent doc |
| `/openapi.json` | OpenAPI 3.1 spec |
| `/discovery` | Discovery JSON (free/paid endpoint listing + terms pointer) |
| `/.well-known/x402` | x402 payment manifest (route + price catalog) |
| `/.well-known/agent-card.json` | A2A agent card |
| `/terms.txt` | Terms of Service |

**Terms:** https://api.orcatrace.dev/terms.txt

**Disclaimer:** Polymarket intelligence aggregated from public prediction-market data and LLM-synthesized; informational only, provided as-is without warranty. Whale calibration measures **entries held to resolution, not trader P&L** (exits are not tracked) — not financial advice. Digest and research analysis is model-generated and may be imperfect — every response carries `createdAt` provenance so you can judge freshness.
