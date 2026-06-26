# Perp Deposit Flow (Canonical)

This is the canonical end-to-end workflow the agent must follow when the
user wants to **fund their Hyperliquid perp account from Solana**.

The recommended path is the **TEE one-click flow** (`deposit-place`): the
LiberFi server quotes the deposit, signs the Solana transaction with the
user's Privy TEE wallet, broadcasts it, and submits the intent in a single
HTTP call. The user never sees keys, signatures, or RPC endpoints.

The atomic flow (`deposit-quote` → user signs/broadcasts → `deposit-submit`)
is an escape hatch for advanced clients: external SOL wallets, custom RPCs,
or recovery after a partial failure.

## Decision tree

```
User says "fund my perp account / deposit X SOL to Hyperliquid"
        │
        ├─ User has a LiberFi TEE wallet and is willing to delegate signing
        │   ──→ TEE one-click flow (deposit-place) — RECOMMENDED
        │
        ├─ User explicitly insists on signing the SOL tx themselves
        │   (external wallet, hardware key, custom RPC)
        │   ──→ Escape-hatch flow (deposit-quote → sign → deposit-submit)
        │
        └─ User reports "I broadcasted the SOL tx but the system has no record"
            (deposit-place returned `submit_failed_after_broadcast`, or the
            user signed manually after deposit-quote and the network dropped
            the submit call)
            ──→ Recovery flow (deposit-submit only, with the existing tx hash)
```

If the user did not specify an amount, **ask before doing anything else**.
Never guess deposit sizes.

## Architecture

```
┌────────┐  POST /v1/perpetuals/deposits/place        ┌──────────────┐
│  CLI   │ ───────────────────────────────────────►   │ openapi-     │
│ (lfi)  │                                            │ server       │
└────────┘                                            └──────┬───────┘
     ▲                                                       │ ① quote
     │                                                       ▼
     │                                                ┌──────────────┐
     │                                                │ perpetuals-  │
     │                                                │ server       │
     │                                                └──────┬───────┘
     │                                                       │ unsigned SOL tx
     │                                                       ▼
     │                                                ┌──────────────┐
     │                                                │ Privy TEE    │
     │                                                │ (SignSOL)    │
     │                                                └──────┬───────┘
     │                                                       │ signed tx
     │                                                       ▼
     │                                                ┌──────────────┐
     │                                                │ Solana RPC   │
     │                                                │ (broadcast)  │
     │                                                └──────┬───────┘
     │                                                       │ tx hash
     │                                                       ▼
     │                                                ┌──────────────┐
     │             ④ {intentId, txHash}              │ perpetuals-  │
     │ ◄──────────────────────────────────────────── │ server       │
     │                                                │ /submit      │
     │             then poll deposit-status           └──────────────┘
```

Steps ① quote, ② TEE sign, ③ broadcast, ④ submit happen server-side
inside `openapi-server` for `deposit-place`. For the escape-hatch flow,
the client orchestrates the same steps locally.

## TEE one-click flow (recommended)

### Step 1 — Authentication gate

```bash
lfi status --json
```

If `authenticated: false`, run `lfi login key --json` (agent mode) or the
appropriate email-OTP flow (human mode). Do not proceed without a session.

### Step 2 — Confirm intent with the user

Always confirm the **deposit amount** in human units (SOL), and the
**recipient** if the user passes one explicitly. Default recipient is the
user's TEE EVM address (`lfi whoami --json` → `evmAddress`), which is the
account Hyperliquid binds to.

### Step 3 — Place

```bash
lfi perpetuals deposit-place \
  --gross-lamports <lamports> \
  [--hyperliquid-recipient 0x…] \
  --json
```

Conversion: `lamports = SOL × 1_000_000_000` (1 SOL = 1e9 lamports).
Examples:

| Human amount | Lamports |
|--------------|----------|
| 0.01 SOL     | `10000000` |
| 0.1 SOL      | `100000000` |
| 1 SOL        | `1000000000` |

Capture the response:

```jsonc
{
  "intentId": "intent-abc123",
  "solanaTxHash": "5vGj…",
  "status": "broadcasted",
  "breakdown": { /* gross / fee / relay split, treasury, currencies */ },
  "issuedAt": "2026-04-28T12:00:00Z"
}
```

### Step 4 — Poll status

```bash
lfi perpetuals deposit-status <intentId> --json
```

Repeat every ~5 seconds until `status` is one of:

| Status | Meaning | Next action |
|--------|---------|-------------|
| `broadcasted` | tx is on Solana, server is observing it | continue polling |
| `relay_waiting` | server has confirmed the SOL tx, queued to Relay | continue polling |
| `relay_pending` | Relay is bridging SOL→Hyperliquid | continue polling |
| `settled` | deposit credited to Hyperliquid perp account ✓ | success — show breakdown + USDC delta |
| `failed_quote_expired` | submit happened too late (quote TTL exceeded) | start over with `deposit-place` |
| `failed_relay_rejected` | Relay rejected the deposit (e.g. amount below floor) | inspect `lastError`; recommend smaller amount |
| `failed_relay_dropped` | Relay request dropped after retries | inspect `lastError`; user may need manual recovery |

If the user wants a fresh server-side fetch (bypassing any Redis cache),
add `--refresh`:

```bash
lfi perpetuals deposit-status <intentId> --refresh --json
```

> Today the `--refresh` and the cache-friendly endpoints behave
> identically (caching is not yet enabled). The flag exists so client UX
> stays stable when caching is later turned on.

## Escape-hatch atomic flow

Use only when the user has a Solana key outside the TEE.

### Step A — Quote

```bash
lfi perpetuals deposit-quote \
  --user-solana-address <sol_pubkey> \
  --hyperliquid-recipient 0x… \
  --gross-lamports <lamports> \
  --json
```

Response includes `serializedTxBase64` (base64 unsigned tx),
`issuedAt` (UTC ISO-8601), `expiresAt` (~30 s after `issuedAt`),
and the same `breakdown`.

### Step B — Sign + broadcast (off-CLI)

The user (or their wallet) base64-decodes the tx, signs it with the
matching Solana private key, and broadcasts it via `sendRawTransaction`
to a Solana RPC endpoint. The CLI does NOT help here.

### Step C — Submit

Within ~30 seconds of `issuedAt`, post the broadcasted tx hash:

```bash
lfi perpetuals deposit-submit --body '{
  "userSolanaAddress": "<sol_pubkey>",
  "hyperliquidRecipient": "0x…",
  "solanaTxHash": "<5vGj…>",
  "breakdown": { /* echoed verbatim from quote */ },
  "userId": "<your user id, e.g. lfi whoami → userId>",
  "quoteIssuedAt": "<issuedAt from quote>"
}' --json
```

The CLI auto-injects `source: "default"` if you omit it. Submit is
idempotent on `solanaTxHash` — safe to retry.

Then continue with `deposit-status` polling.

## Recovery flow (after a partial failure)

If `deposit-place` returns `submit_failed_after_broadcast`, the response
includes the SOL tx hash and the breakdown:

```jsonc
{
  "error": "submit_failed_after_broadcast",
  "message": "transaction broadcasted but perpetuals-server submit failed; retry deposit-submit manually",
  "solana_tx_hash": "5vGj…",
  "breakdown": { … },
  "quote_issued_at": "2026-04-28T12:00:00Z"
}
```

Replay submit by feeding those values back into `deposit-submit`:

```bash
lfi perpetuals deposit-submit --body '{
  "userSolanaAddress": "<lfi whoami → solAddress>",
  "hyperliquidRecipient": "<lfi whoami → evmAddress, OR the explicit recipient>",
  "solanaTxHash": "5vGj…",
  "breakdown": { /* from the failed deposit-place response */ },
  "userId": "<lfi whoami → userId>",
  "quoteIssuedAt": "2026-04-28T12:00:00Z"
}' --json
```

This is the same code path as the escape-hatch step C.

## Common pitfalls

- **Wrong unit** — `--gross-lamports` is **lamports**, not SOL. Always
  multiply by 1e9 before passing.
- **Skipping authentication** — `deposit-place` returns 401 if the
  caller has no LiberFi JWT. Run `lfi status` first.
- **Missing TEE EVM wallet** — if the user's TEE has no EVM wallet
  provisioned (rare, only for legacy accounts), `deposit-place` returns
  400 unless the user supplies `--hyperliquid-recipient` explicitly.
- **Using a Safe / smart-wallet address as `--hyperliquid-recipient`** —
  Hyperliquid binds to the EOA, not a Safe. Always pass the EOA.
- **Not polling `deposit-status`** — `deposit-place` returns the moment
  the SOL tx is broadcasted; settlement to Hyperliquid takes 30–120 s.
  Without polling, the user has no way to know the deposit landed.
- **Confusing `--refresh` with `--force`** — `--refresh` only bypasses
  server-side caching; it does not retry the underlying Relay request
  or replay the SOL tx. There is no force-replay knob today.
