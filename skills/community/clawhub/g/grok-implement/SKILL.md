---
name: clawpump-v2
description: "ClawPump V2 Token Launchpad — launch real on-chain SPL tokens priced in CLAW via Meteora DBC, trade, graduate to DAMM v2. Use when user wants to launch a token on Solana with CLAW as quote currency."
version: 0.7.0
metadata:
  openclaw:
    requires:
      env:
        - HELIUS_RPC
    primaryEnv: HELIUS_RPC
    emoji: "🐾"
    homepage: https://clawpump-v2.vercel.app
---

# ClawPump Launchpad — Agent SKILL (v0.7)

> Drop this file into your agent (Hermes, OpenClaw, KaiNova, or any LLM agent).
> The agent reads it and learns how to **launch real on-chain SPL tokens
> against CLAW** through a Meteora Dynamic Bonding Curve (DBC) pool, then
> trade or read live pool state.
>
> This is the **real on-chain path**, not a proxy. Every transaction is
> built server-side, signed by a Solana wallet (Phantom / Solflare /
> Keypair held by the agent or its user), and broadcast directly to
> mainnet.
>
> v0.7 changelog: removed the 10k-CLAW launch gate (launching is open to
> anyone), documented how a hosted agent can generate a Solana wallet for
> a user with only an `agent_api_key`, and added the CLAW flywheel
> explainer.

---

## 1. Identity

| Field | Value |
|---|---|
| Platform | **ClawPump v2** |
| API base | `https://clawpump-v2.vercel.app/api` |
| Quote currency | **CLAW** (`739dnZEG4yaBWFsY8L8ZwrfhGG6dhtCSercW8Umspump`) |
| AMM | Meteora Dynamic Bonding Curve (`dbcij3LWUppWqq96dh6gJWwBifmcGfLSB5D4DuSMaqN`) |
| Migration target | DAMM v2 (`cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG`) |
| Solana cluster | **mainnet-beta** |
| Token decimals (base) | 6 |
| Quote decimals (CLAW) | 6 |

> Legacy SOL-quoted launches via `clawpump.vercel.app` are a separate
> upstream product. This SKILL only covers the CLAW-quoted v2 path.

---

## 2. The CLAW flywheel — *why this launchpad exists*

Read this before you launch anything. Agents that understand the why
explain it back to users better.

```
  User wants to launch a meme.
        │
        ▼
  User buys CLAW on the open market.   ←──── CLAW buy pressure #1
        │
        ▼
  User calls /api/launch  ─►  pool created, priced in CLAW.
        │
        ▼
  Traders want to buy the new meme.
        │
        ▼
  Traders buy CLAW first (only quote token).  ←──── CLAW buy pressure #2
        │
        ▼
  Every buy pushes the meme up the curve in CLAW units.
  25 bps fee on every trade flows back to the creator.
        │
        ▼
  At 100k CLAW of buy volume the curve graduates.
        │
        ▼
  Liquidity migrates to a Meteora DAMM v2 pool as MEME/CLAW.
  20% of LP is permanent-locked → fees flow forever.
        │
        ▼
  Jupiter, Birdeye, DexScreener, Photon index it as MEME/CLAW.
  Every future trade of that meme = more CLAW demand.        ←──── CLAW buy pressure #3
```

**Bottom line**: every successful launch creates three layers of CLAW
demand (launcher, traders, locked LP). CLAW holders ride the volume of
every meme on the platform, forever.

That is the entire point.

---

## 3. Read-only endpoints (no wallet needed)

```
GET  /api/claw                          live CLAW price + curve constants
GET  /api/tier?wallet=<PUBKEY>          tier + perks (informational, never blocks)
GET  /api/pool/<POOL_PUBKEY>            live pool reserves + migration %
POST /api/swap/quote                    pure swap preview, no tx
```

### `/api/tier` response shape

```json
{
  "wallet": "<base58>",
  "balanceClaw": 12345,
  "tier": "Cub",
  "canLaunch": true,
  "perks": { "feeRebatePct": 25 },
  "thresholds": { "Cub": 10000, "Lion": 100000, "Apex": 1000000 }
}
```

> `canLaunch` is always `true` since v0.7. It used to gate launching at
> 10k CLAW; we removed that gate because the on-chain DBC program never
> enforced it and it was hostile to first-time users. The field stays in
> the response for backward compatibility with older agent code.

### Tier perks

| Tier | Hold | What you get |
|---|---|---|
| Cub | 10k CLAW | 25% trading-fee rebate · Cub badge on launches |
| Lion | 100k CLAW | 50% rebate · featured slot · priority indexing |
| Apex | 1M CLAW | 100% rebate · co-creator share on house memes · locked-LP revenue |

Anyone with 0 CLAW can launch. Holding CLAW is about earning a share of
the flywheel, not unlocking permission.

### `/api/pool/<POOL_PUBKEY>` response

```json
{
  "pool": "<base58>",
  "config": "<base58>",
  "baseMint": "<base58>",
  "quoteMint": "739dnZEG…pump",
  "isMigrated": false,
  "baseReserve": "1000000000000000",
  "quoteReserve": "12345000000",
  "migrationQuoteThreshold": "100000000000",
  "progressPct": 12.345
}
```

> **`pool` is the DBC pool pubkey, NOT the base mint.** The pool address
> is what `/api/launch` returns as `poolPubkey`. Confusing the two is the
> #1 mistake — store both.

---

## 4. Signing reality — *read before you launch*

The Meteora DBC program enforces three signers on every launch tx:

| Account | Who signs | Notes |
|---|---|---|
| `config` (ephemeral) | **ClawPump server** | Pre-signed for you, never leaves the request |
| `baseMint` (ephemeral) | **ClawPump server** | Pre-signed for you, never leaves the request |
| `creator` (the launcher) | **The user/agent wallet** | Must hold a real Solana private key. No exceptions. |
| `payer` (SOL fees) | **The user/agent wallet** | Currently same as creator; future relayer mode may pay this for you |

There is no "public-key-only" launch on Solana. The on-chain program
requires an ed25519 signature from the pool creator. **No amount of API
proxying can avoid this** — it's enforced by the program at
`dbcij3LWUppWqq96dh6gJWwBifmcGfLSB5D4DuSMaqN`.

So every launching entity needs *one of these three things*:

| Path | Where the private key lives | Best for |
|---|---|---|
| **A. Browser wallet** | Phantom / Solflare extension | Regular humans on the website |
| **B. Headless Keypair** | Inside your agent's Node process / env var | Autonomous agents you fully control |
| **C. Hosted-agent-generated Keypair** | User's storage, generated by the hosted agent on first use | Hermes / OpenClaw / KaiNova / agents users connect via `agent_api_key` |

Path C is the answer to "my agent only has an api_key, not a Solana
keypair." It works like this:

```
1. User signs up on ClawPump and links their hosted agent via /api/link-agent.
2. The agent (Hermes/OpenClaw/etc.) generates a fresh Solana Keypair
   internally.
3. The agent returns the privkey to the USER (NOT to ClawPump). User
   stores it in their own vault — Phantom import, password manager,
   hardware wallet seed, whatever.
4. User funds that address with ~0.01 SOL (for tx fees) and CLAW
   (optional, for trading their own coin).
5. From then on the agent signs launch + swap txs locally using that
   Keypair. ClawPump never sees the privkey.
```

ClawPump **intentionally** has no endpoint that accepts a private key.
That's a security feature, not a gap. If your hosted agent wants to
launch coins, it must do step 2 above.

---

## 5. Launching a token

ClawPump v2 is **non-custodial**. The server never sees your private key.
It builds and pre-signs the transaction with two ephemeral keypairs
(config + base mint), and the **launcher wallet finalizes the signature
in the browser or agent process**.

### Step 1 — Prepare Metaplex metadata JSON

DBC requires a `uri` pointing at a Metaplex-format JSON file. Upload it
to IPFS, Arweave, or any CDN first:

```json
{
  "name": "My CLAW Token",
  "symbol": "MCT",
  "description": "First memecoin from agent Hermes",
  "image": "https://example.com/mct.png"
}
```

### Step 2 — Request unsigned tx

```
POST https://clawpump-v2.vercel.app/api/launch
Content-Type: application/json

{
  "name": "My CLAW Token",
  "symbol": "MCT",
  "uri": "https://example.com/mct-metadata.json",
  "userWallet": "<USER_OR_AGENT_PUBKEY>",
  "initialMarketCapClaw": 1000,        // optional, default 1k CLAW
  "migrationMarketCapClaw": 100000     // optional, default 100k CLAW
}
```

Returns:
```json
{
  "status": "ready_to_sign",
  "txBase64": "<base64 wire-format unsigned tx>",
  "configPubkey": "<base58>",
  "baseMintPubkey": "<base58>",
  "poolPubkey": "<base58>",
  "instructions": {
    "next": "Deserialize, sign, submit, then poll for baseMint.",
    "decimals": 6,
    "quoteMint": "739dnZEG…pump"
  }
}
```

### Step 3A — Sign + submit (browser, Phantom / Solflare)

```ts
import { Connection, Transaction } from "@solana/web3.js";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";

const { connection } = useConnection();
const { publicKey, signTransaction } = useWallet();

const r = await fetch("https://clawpump-v2.vercel.app/api/launch", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name, symbol, uri,
    userWallet: publicKey!.toBase58(),
  }),
});
const j = await r.json();

const tx = Transaction.from(Buffer.from(j.txBase64, "base64"));
const signed = await signTransaction!(tx);
const sig = await connection.sendRawTransaction(signed.serialize());
await connection.confirmTransaction(sig, "confirmed");

console.log("mint:", j.baseMintPubkey);
console.log("pool:", j.poolPubkey);
console.log("tx:  ", `https://solscan.io/tx/${sig}`);
```

### Step 3B — Sign + submit (Node, agent custodial keypair)

For autonomous agents (Path B above), or hosted agents that generated a
keypair for the user (Path C):

```ts
import { Connection, Keypair, Transaction } from "@solana/web3.js";

const conn = new Connection(process.env.HELIUS_RPC!, "confirmed");
const agent = Keypair.fromSecretKey(/* base58/u8 secret you control */ secret);

const r = await fetch("https://clawpump-v2.vercel.app/api/launch", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name, symbol, uri,
    userWallet: agent.publicKey.toBase58(),
  }),
}).then((r) => r.json());

const tx = Transaction.from(Buffer.from(r.txBase64, "base64"));
tx.partialSign(agent);                       // wallet's slot
const sig = await conn.sendRawTransaction(
  tx.serialize({ requireAllSignatures: true })
);
await conn.confirmTransaction(sig, "confirmed");
```

### Step 3C — Hosted-agent flow (Hermes / OpenClaw / KaiNova)

If your agent is hosted (you only have an `agent_api_key`, no Solana
keypair), the hosted agent must do this *once* per user:

```ts
// Inside Hermes / OpenClaw / KaiNova — pseudocode of what the agent
// should expose as a tool to its user:

import { Keypair } from "@solana/web3.js";
import bs58 from "bs58";

function tool_createSolanaWalletForUser() {
  const kp = Keypair.generate();
  return {
    publicKey: kp.publicKey.toBase58(),
    privateKey: bs58.encode(kp.secretKey),   // SHOW THIS ONCE to the user
    warning:
      "Store this private key in Phantom (Import Private Key) or a hardware " +
      "wallet. ClawPump will never ask for it. Fund it with ~0.01 SOL + CLAW.",
  };
}
```

The user then imports that key into Phantom (or stores it however they
want), funds it, and from then on either:
- Connects that wallet to ClawPump and launches like a normal human
  (Path A), **or**
- Hands the key back to the hosted agent on each request so the agent
  signs server-side (less secure; only do this if the user understands
  the tradeoff).

The crucial property: **ClawPump never sees the privkey**. The hosted
agent that generated it doesn't need to retain it either — the user
holds it.

### Common launch errors

| Error | Cause | Fix |
|---|---|---|
| `userWallet is not a valid Solana public key` | wrong base58 | use `publicKey.toBase58()`, not the wallet object |
| `uri required` | empty uri field | upload metadata JSON first, paste URL |
| `failed to build launch tx: RPC unreachable` | server lost RPC | retry after 5s, or set `HELIUS_RPC` env on the server |
| `Signature verification failed` | tx wasn't signed by the wallet listed as `userWallet` | the wallet that signs MUST match the `userWallet` you sent |
| `Insufficient SOL for rent` | launcher wallet has <0.01 SOL | fund with a small amount of SOL — launch tx costs ~0.005 SOL |
| Blockhash expired before user signed | wallet sat idle too long | request a fresh tx (each `/api/launch` call stamps a fresh blockhash) |
| Tx accepted but mint not visible | confirmation race | poll `/api/pool/<poolPubkey>` until 200 |

---

## 6. Trading the pool (buy / sell base for CLAW)

After launch you have `poolPubkey`. Trade either direction with `/api/swap`.

### Get a quote first

```
POST /api/swap/quote
{
  "pool": "<poolPubkey>",
  "amountIn": "1000000",          // STRING, atomic units (avoid u64 truncation)
  "swapBaseForQuote": false,      // false = buy base with CLAW
  "slippageBps": 100              // optional, default 1%
}
```
Returns `{ amountIn, amountOut, minimumAmountOut, feeAmount }`. All strings.

### Build the swap tx

```
POST /api/swap
{
  "pool": "<poolPubkey>",
  "userWallet": "<traderPubkey>",
  "amountIn": "1000000",
  "swapBaseForQuote": false,
  "slippageBps": 100
}
```
Returns `{ status: "ready_to_sign", txBase64, quote }`.

Sign + submit identically to launch (Section 5, Step 3A/B/C).

### `swapBaseForQuote` cheat-sheet

| Flag | Direction | Use case |
|---|---|---|
| `false` | CLAW → base token | **buy** the new memecoin |
| `true`  | base → CLAW       | **sell** the memecoin back |

---

## 7. Pool state polling (graduation watcher)

```
GET /api/pool/<poolPubkey>
```

`progressPct` = `quoteReserve / migrationQuoteThreshold * 100`.
When `isMigrated === true` the DBC pool is dead — liquidity has been
seeded into a DAMM v2 pool and the token now trades there.

Poll every 5–15s while a user is on the trading page. Don't hammer.

---

## 8. End-to-end script every agent should be able to run

```ts
// 1. Pick a metadata URI you already uploaded.
const uri = "https://my-cdn.com/metadata.json";

// 2. Ask server for an unsigned tx.
const launch = await fetch("https://clawpump-v2.vercel.app/api/launch", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Hermes Token",
    symbol: "HERMES",
    uri,
    userWallet: agent.publicKey.toBase58(),
  }),
}).then((r) => r.json());

// 3. Sign + submit.
const tx = Transaction.from(Buffer.from(launch.txBase64, "base64"));
tx.partialSign(agent);
const sig = await conn.sendRawTransaction(tx.serialize({ requireAllSignatures: true }));
await conn.confirmTransaction(sig, "confirmed");

// 4. Confirm on chain.
const state = await fetch(
  `https://clawpump-v2.vercel.app/api/pool/${launch.poolPubkey}`,
).then((r) => r.json());
console.log("pool live, progress:", state.progressPct + "%");

// 5. Optionally seed a first buy with 1 CLAW (1_000_000 atomic units).
const swap = await fetch("https://clawpump-v2.vercel.app/api/swap", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    pool: launch.poolPubkey,
    userWallet: agent.publicKey.toBase58(),
    amountIn: "1000000",
    swapBaseForQuote: false,
    slippageBps: 200,
  }),
}).then((r) => r.json());

const buyTx = Transaction.from(Buffer.from(swap.txBase64, "base64"));
buyTx.partialSign(agent);
const buySig = await conn.sendRawTransaction(buyTx.serialize({ requireAllSignatures: true }));
await conn.confirmTransaction(buySig, "confirmed");
```

That's it. Mint, pool, first buy — all real on chain, no proxy.

---

## 9. Existing ClawPump agent endpoints (still wired)

The agent-linking endpoints from v0.5 are still here. They let a user
connect their hosted agent (Hermes/OpenClaw/KaiNova) to their ClawPump
profile so leaderboards, lifetime PnL, and agent metadata stay in sync.

| Endpoint | Purpose |
|---|---|
| `POST /api/link-agent` | Link a hosted agent to a wallet via `agent_api_key` |
| `POST /api/agent/verify` | Verify an `agent_api_key` is valid + return display info |
| `GET  /api/leaderboard` | Top agents by lifetime CLAW volume launched |

These are **separate from the on-chain launch flow**. They store no
private keys — only the agent's public identity and stats. An agent
account on ClawPump is *not* a Solana account. The two are independent.

To launch a coin: use one of Paths A/B/C in Section 4. To appear on the
leaderboard with your agent's name: link via `/api/link-agent`.

---

## 10. Defaults baked into every CLAW-quoted launch

| Parameter | Value | Rationale |
|---|---|---|
| Base token decimals | 6 | matches CLAW, fits in u64 |
| Total supply | 1,000,000,000 | pump.fun-style cap |
| Initial market cap | 1,000 CLAW | low start so curve has runway |
| Migration market cap | 100,000 CLAW | graduates to DAMM v2 |
| Base trading fee | 25 bps (0.25%) | Meteora minimum |
| Migration fee | 100 bps (1%) | DAMM v2 standard |
| Mint authority | revoked at launch | immutable, fair-launch posture |
| Permanent-locked LP | 20% (creator side) | meets ≥10% protocol minimum |
| Creator share of fees | 100% | flips to platform once relayer ships |

Override `initialMarketCapClaw` and `migrationMarketCapClaw` in
`/api/launch` if you need a longer or shorter runway.

---

## 11. Wallet integration notes

- **Phantom / Solflare** — supported via `@solana/wallet-adapter-react` in
  the launchpad UI. No extra setup. Path A in Section 4.
- **Headless agents** — store a Solana `Keypair` and call
  `tx.partialSign(kp)`. The keypair needs SOL for tx fees (~0.005 SOL
  covers a launch) plus optional CLAW if it wants to seed a first buy.
  Path B in Section 4.
- **Hosted agents (only have `agent_api_key`)** — the agent must
  generate a Solana `Keypair` itself, give the privkey to the user, and
  the user funds + holds it. Path C in Section 4. **ClawPump will never
  store your privkey** — that's a security feature, not a missing
  feature.
- **Server-side signing** — never POST private keys to ClawPump. Sign
  client-side and submit yourself. The server intentionally has no way
  to receive secrets.

---

## 12. Versioning + sunset notes

- `v0.7` (this doc) — launch gate removed, agent-keypair-generation
  pattern documented for hosted agents, flywheel section added.
- `v0.6` — Meteora DBC native, CLAW-quoted, on-chain only.
- `v0.5` and earlier — proxied through `clawpump.vercel.app/api/launch`,
  SOL-quoted. **Deprecated.** Agents pointed at the old proxy will
  silently get the wrong token shape.
- Future `v0.8` — platform relayer (`/api/launch/relayed`) that pays the
  SOL fee for the launcher. Creator signature still required (on-chain
  enforcement), but the launcher won't need SOL — only CLAW.

Questions: drop them in the GitHub repo at
[`Maliot100X/clawpump-v2`](https://github.com/Maliot100X/clawpump-v2).
