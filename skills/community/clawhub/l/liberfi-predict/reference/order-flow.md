# Predict TEE Order Flow (Canonical)

This is the canonical end-to-end workflow the agent must follow when the
user asks to place a prediction market order via the **TEE auto flow**.
The user never sees POLY_* HMAC credentials, EIP-712 typed data, or
Solana transaction signatures — the LiberFi server signs everything via
the user's Privy TEE wallet.

> If the user explicitly asks to use their own Polymarket CLOB
> credentials or pre-signed Kalshi transactions, fall back to the legacy
> commands (`polymarket-order`, `kalshi-quote`, `kalshi-submit`) and
> warn that they are deprecated.

## Decision Tree

```
User says "I want to bet/buy/sell on <event>"
        │
        ├─ source = polymarket  →  see "Polymarket Flow" below
        └─ source = kalshi      →  see "Kalshi Flow" below
```

If the user did not specify a source, ask before doing anything else.

## Polymarket Flow

### Step 1 — Authentication gate

```bash
lfi status --json
```

If `authenticated: false`, run `lfi login key --json` (agent mode) or
prompt the user for `lfi login <email>` + `lfi verify <otpId> <code>`
(human mode). Do not proceed without a valid session.

### Step 2 — Setup check (idempotent)

```bash
lfi predict polymarket-setup-status --json
```

Inspect the response:

- `safe_deployed` (bool)
- `safe_address` (string, present when deployed)
- `usdc_approved` / `negrisk_approved` / `ctf_approved` (bools)

If **any** of those is `false`, run setup:

```bash
lfi predict polymarket-setup --json
```

This deploys the user's Safe wallet (Polygon) and approves all required
tokens via the Polymarket Builder Relayer. It is **gasless** (the relayer
pays) and idempotent — safe to call repeatedly. After it returns,
re-fetch `polymarket-setup-status` and confirm everything is `true`.

### Step 3 — Funding check

First resolve the user's TEE EOA (skip if you already have it):

```bash
lfi whoami --json   # → evmAddress = TEE EOA
```

Then query the balance — **pass the TEE EOA, NOT the Safe address**:

```bash
lfi predict balance --source polymarket --user <tee_eoa> --json
```

> **Why EOA, not Safe?** The prediction-server's Polymarket balance /
> positions / trades handlers expect the user's EOA and internally derive
> the corresponding Safe via CREATE2 before querying Polygon RPC and the
> Polymarket Data API. If you pass the Safe address here, the server
> derives a Safe *from a Safe* → a non-existent "double-Safe" → balance /
> positions / trades return EMPTY. This is the #1 cause of "balance is
> always 0". The Safe address is ONLY used in Step 3b below
> (`polymarket-deposit-addresses`), where the Polymarket Bridge needs
> the actual Safe as its bridge key.

This returns the actual USDC balance held by the Safe on Polygon and used
by the CLOB. **Recommend a minimum of $2 USDC.** If sufficient, skip the
deposit step and go to Step 4.

### Step 3b — Bridge deposit addresses (only if balance insufficient)

If insufficient, fetch the **bridge deposit addresses**. This is the ONLY
call where you pass the Safe address (the bridge keys its multi-chain
deposit accounts by Safe):

```bash
lfi predict polymarket-deposit-addresses --safe-address <safe_address> --json
```

Response shape (multi-chain bridge addresses provided by the Polymarket
Bridge API — each address is unique per Safe and routes funds to the
Safe automatically):

```json
{
  "evm":  "0x...",   // EVM bridge address — accepts USDC/USDT on Ethereum, Polygon, Base, Arbitrum, Optimism, etc.
  "svm":  "...",     // Solana bridge address — accepts USDC on Solana
  "btc":  "...",     // Bitcoin bridge address
  "tron": "..."      // Tron bridge address (optional, may be omitted)
}
```

**CRITICAL: NEVER tell the user to send funds to the Safe address.**
The Safe address from `polymarket-setup-status` is Polymarket's internal
custody contract — it is NOT a deposit address from the user's
perspective. The user MUST send to one of the bridge addresses returned
by `polymarket-deposit-addresses` so the Polymarket Bridge service can
detect the inbound transfer and credit the Safe.

Pick the right address based on what the user has:

| User's funds live on | Use this field | Example asset |
|---|---|---|
| Any EVM chain (Ethereum, Polygon, Base, Arbitrum, Optimism, BNB, etc.) | `evm` | USDC, USDT |
| Solana | `svm` | USDC |
| Bitcoin | `btc` | BTC |
| Tron | `tron` | USDT-TRC20 |

If the user did not say where their funds are, default to `evm` (most
common) and ask: "你的 USDC 在哪条链上?(Ethereum / Polygon / Base /
Solana / ...)EVM 链系都用同一个地址。"

Tell the user (substituting the actual values):

> 充值地址(EVM,可在 Ethereum / Polygon / Base / Arbitrum / Optimism /
> BNB Chain 等任意 EVM 链上转账):
>
>     <evm>
>
> 请转入至少 $2 USDC(或等值 USDT)。Polymarket Bridge 会自动把资金转到
> 你的 Safe 钱包。到账后我会自动重新检查余额。

Then loop on `lfi predict balance --source polymarket --user <tee_eoa> --json`
(EOA, not Safe — see Step 3 note) until the balance reflects the deposit,
before proceeding to Step 4.

> Note for already-on-Polygon power users: technically, sending Polygon
> USDC.e directly to the Safe address works because the Safe owns it.
> But this is NOT the documented path — for any user without specific
> Polygon USDC.e, ALWAYS use the bridge addresses above. Do not suggest
> the Safe address as a deposit target unless the user explicitly asks.

### Step 4 — Discover the token

If the user gave you an event slug or market URL but not a CLOB token
ID, fetch it:

```bash
lfi predict event <slug> --source polymarket --json
```

The response includes the markets with their YES/NO `clob_token_id`
values. Pick the one matching the user's intended outcome.

### Step 5 — Order parameters

Ask the user (one round trip if the intent is ambiguous):

| Question | Why |
|---|---|
| Market or limit order? | Drives `--order-type` |
| If limit: price + size + GTC vs GTD? | Required flags |
| If GTD: expiration time? | Required `--expiration` (epoch seconds) |
| If market BUY: USDC spend? | `--size` is the USDC amount |
| If market SELL: share count? | `--size` is the share count |

Optional (skip unless the user specifies): `--neg-risk`, `--fee-rate-bps`,
`--tick-size`, `--taker-address`. The server auto-resolves tick size and
fee rate via the existing PS endpoints.

### Step 6 — Confirm

Summarize the final order in plain language:

> You're about to BUY 10 shares of "Will BTC > $100k by EOY 2026 — YES"
> at $0.55/share (limit, Good-Til-Cancelled). Total cost ≈ $5.50 USDC
> plus tiny rounding. **Confirm? (yes/no)**

Wait for explicit `yes` (or Chinese equivalent). Never assume.

### Step 7 — Place

```bash
lfi predict polymarket-place \
  --token-id <id> --side BUY \
  --order-type GTC --price 0.55 --size 10 --json
```

The server:

1. Calls PS `POST /orders/polymarket/prepare` — resolves tick/fee/salt,
   builds the canonical order message, returns EIP-712 typed-data + digest.
2. Calls Privy `eth_signTypedData_v4` against the user's TEE EVM wallet.
3. Derives Polymarket L2 HMAC credentials (signed L1 ClobAuth message)
   on first use and caches them per signer.
4. Calls PS `POST /orders/polymarket/execute` — PS posts the order to
   the Polymarket CLOB on the user's behalf.

The response includes the CLOB raw response (order ID, status, etc.).

### Step 8 — Verify

```bash
lfi predict orders --source polymarket --json
```

Show the user their open orders. If they want to cancel:

```bash
lfi predict cancel <orderId> --source polymarket --json
```

L2 HMAC headers are derived automatically from the caller's TEE wallet.

## Kalshi Flow

Kalshi orders are placed via the DFlow swap pipeline, so the flow is a
single command (no Safe deployment, no approval step):

### Step 1 — Authentication gate

Same as Polymarket. Require a valid `lfi status` session.

### Step 2 — Discover the mints

```bash
lfi predict event <slug> --source kalshi --json
```

The response gives you the `input_mint` (USDC) and `output_mint` (Kalshi
outcome token mint) for the chosen market.

### Step 3 — Confirm

Summarize and wait for explicit user confirmation.

### Step 4 — Place

```bash
lfi predict kalshi-place \
  --input-mint <usdcMint> --output-mint <outcomeMint> \
  --amount 500000 --slippage-bps 100 --json
```

`--amount` is in the input token's **smallest unit** (USDC = 6 decimals,
so `500000` = $0.50). The server:

1. Calls PS `POST /orders/kalshi/quote` with `userPublicKey` taken from
   the caller's JWT.
2. Calls Privy `signTransaction` (Solana) against the user's TEE SOL
   wallet.
3. Calls PS `POST /orders/kalshi/submit` with the signed transaction.

### Step 5 — Verify

```bash
lfi predict orders --source kalshi --wallet-address <userSolAddr> --json
lfi predict trades --wallet <userSolAddr> --source kalshi --json
```

## Common Pitfalls

| Pitfall | Correct approach |
|---|---|
| Calling `polymarket-place` without setup | Always run `polymarket-setup-status` first; auto-run `polymarket-setup` if not ready |
| **Passing the Safe address to `balance` / `positions` / `trades`** | NEVER. Pass the TEE EOA (`evmAddress` from `lfi whoami`) — the prediction-server derives the Safe via CREATE2 internally. Passing the Safe directly causes the server to derive a "Safe of a Safe" and the query returns EMPTY (balance always 0, positions empty, trades empty). |
| **Telling the user to send funds to the Safe address** | NEVER. The Safe is Polymarket's internal custody contract, not a deposit target. Always call `polymarket-deposit-addresses --safe-address <safe>` (Safe is correct here — it's the bridge key) and surface one of its bridge addresses (`evm`/`svm`/`btc`/`tron`). |
| Ignoring the funding check | Tell the user to deposit ≥ $2 USDC to the **bridge address** (NOT the Safe) before placing the first order |
| Skipping confirmation | NEVER call any `*-place` command without explicit user confirmation |
| Mixing TEE flow with `--poly-*` flags | The TEE `polymarket-place` does not accept POLY_* — those are only for the deprecated `polymarket-order` |
| Passing `--user-public-key` to `kalshi-place` | The TEE flow auto-fills it from JWT — flag does not exist on `kalshi-place` |
| Cancelling polymarket orders by hand-rolling POLY_* | Just use `lfi predict cancel <id> --source polymarket` — server derives L2 auth |

## Error Recovery

| Error | Likely cause | Fix |
|---|---|---|
| `EVM TEE wallet not provisioned` | Caller is anonymous or session is for a SOL-only account | Run `lfi login key` to create/refresh credentials |
| `setup_required` from PS | Safe not deployed or token approval missing | Run `lfi predict polymarket-setup --json` |
| `insufficient_balance` from CLOB | Safe USDC balance too low | Show deposit address and pause flow |
| `tick_size_invalid` | Price not a multiple of tick size | Re-fetch tick size and ask user to round price |
| `signature_invalid` from CLOB | Order message changed between prepare/execute (caller bug) | Re-run `polymarket-place`; do not modify intermediate fields |
| `cancel: order_not_found` | Already filled or already cancelled | Refresh `lfi predict orders` and inform user |
