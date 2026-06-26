# x402 Payment Reference

Handle `402 Payment Required` HTTP responses by executing payment and fetching the protected resource.

## When to Use

- The user wants to access a resource that returns **HTTP 402 Payment Required** with a `PAYMENT-REQUIRED` header — either known in advance or discovered by a previous attempt.
- Do not pre-fetch the resource yourself to "check" — phase 1 of the script does the fetch.

## Script

### buildX402Payment.js

**Command (phase 1 — discover)**: `node scripts/buildX402Payment.js --resource <url> [--did <did>]`
**Command (phase 2 — execute)**: `node scripts/buildX402Payment.js --paymentRequiredFilePath <path> --paymentHash <hash> [--did <did>]`
**Hint**: **NEVER reuse or cache a previous response from this script.** Every invocation produces unique, time-sensitive output (nonces, signatures, payment tokens). Always execute the script again to get a fresh result — even if the arguments are identical to a prior call.

Executes the x402 payment flow in two strictly separated phases.

- **Phase 1** (`--resource` only): the script fetches the resource, expects a `402` response with a `PAYMENT-REQUIRED` header, caches the decoded challenge to a temp file named by its SHA-256 hash, and returns the available payment options together with the cached file path. It never signs a payment.
- **Phase 2** (`--paymentRequiredFilePath` + `--paymentHash`): the script reads the cached challenge file, looks up the chosen payment option by its `--paymentHash`, signs the payment, sends the `PAYMENT-SIGNATURE` header to the resource, and returns the result.

- `--resource` — (phase 1 only) The URL of the protected resource. The script fetches it and expects HTTP 402 with a `PAYMENT-REQUIRED` header. If the response is any other status, or the header is missing, the script returns status `failed`. Cannot be combined with `--paymentRequiredFilePath` or `--paymentHash`.
- `--paymentRequiredFilePath` — (phase 2 only) Absolute path to the cached payment-required JSON file returned by phase 1. Must be combined with `--paymentHash`. Mutually exclusive with `--resource`.
- `--paymentHash` — (phase 2 only, required) The SHA-256 hash of the chosen payment option from phase 1. Always required on phase 2, even when only one option was offered. Cannot be passed with `--resource`.
- `--did` — (optional) The DID of the signer. Omit unless the user has explicitly asked to pay from a specific DID — the script falls back to the default DID from `getIdentities.js`, which is correct for normal use. Do not prompt the user for a DID on your own.

You **must** pick exactly one phase per invocation. Passing `--resource` together with `--paymentHash` (or with `--paymentRequiredFilePath`) is rejected.

---

## Output

The script always outputs JSON to stdout with a top-level `status` of `success`, `failed`, or `input_required`. See [Handling output](#handling-output) below for the action to take on each.

---

## Workflow

### 1. Trigger

Use this skill whenever the user wants to access a resource you know (or strongly suspect) is gated by `402 Payment Required` with a `PAYMENT-REQUIRED` header.

**Do not fetch the resource yourself first.** `buildX402Payment.js` performs the HTTP request in phase 1, parses the header, and caches the challenge — making your own fetch beforehand is wasted work and may consume a one-shot challenge.

### 2. Ensure identity exists

Run `node scripts/getIdentities.js`. If no identity is configured, create one first (see `reference/identity/SKILL.md`).

### 3. First call — discover payment options (phase 1)

```bash
node scripts/buildX402Payment.js \
  --resource 'https://api.example.com/weather'
```

The script fetches the URL, decodes the `PAYMENT-REQUIRED` header, caches it to a temp file, and **never signs a payment on the first call**. Even when only one option is offered, it returns the list and waits for the user to confirm by selecting a `paymentHash`.

The script outputs `status: "input_required"` with three top-level fields in `data`:

- `resource` — describes the protected resource the user is paying for:
  - `resource.url` — the URL of the protected resource.
  - `resource.description` — a human-readable description of what the resource provides.
- `paymentOptions` — the list of payment options. Each option includes:
  - `hash` — the payment hash (use as `--paymentHash` in the next call)
  - `amount` — the payment amount
  - `asset` — the asset name (e.g., "USDC") or contract address
  - `network` — the network identifier (e.g., "eip155:84532")
  - `requiredAttestations` — informational list of attestation schema IDs that this payment type requires in general; may be non-empty even when the user already holds all of them — **do not use this field to decide whether to block the payment**
  - `hasAllAttestations` — `true` if the user already holds every required attestation and the payment can proceed; `false` if some are missing
  - `attestationLinks` — verification URLs the user must complete to obtain **missing** attestations; empty when `hasAllAttestations` is `true`
- `paymentRequiredFilePath` — absolute path to the cached challenge file. Pass this back via `--paymentRequiredFilePath` on the second call. The file lives in the OS temp directory and is named by the SHA-256 hash of the full challenge content.

**Present the options to the user.** Always start by showing `resource.url` and `resource.description` so the user knows **what** they are paying for. Then show each payment option's amount, asset, network, and whether attestations are required. Ask the user to choose one payment option or decline payment.

If the user declines, do **not** run phase 2. Report that the resource is unavailable without payment and stop.

> **CRITICAL: Formatting `amount` for display (UI only)**
>
> The `amount` field is a raw on-chain integer in the asset's smallest unit. **Never show it to the user as-is** — always convert to a human-readable price by dividing by `10^decimals`, where `decimals` depends on the asset **and the network**.
>
> | Asset       | Network                                          | Decimals | Divisor              |
> | ----------- | ------------------------------------------------ | -------- | -------------------- |
> | USDC / EURC | Ethereum, Polygon, Arbitrum, Optimism, Base      | 6        | 10⁶ = 1 000 000      |
> | USDT        | Ethereum, Polygon, Arbitrum                      | 6        | 10⁶ = 1 000 000      |
> | USDT        | BNB Smart Chain (BEP-20)                         | 18       | 10¹⁸                 |
>
> Examples:
> - `amount: "1000000"` USDC on Base → **$1.00** (or €1.00 for EURC)
> - `amount: "1000000000000000000"` USDT on BNB Smart Chain → **$1.00**
>
> This conversion is **for UI/presentation only**. Always pass the original raw `hash` value back to phase 2 via `--paymentHash` — never round, scale, or modify any field you forward to the script.

> **CRITICAL: Reading attestation status**
>
> Use only `hasAllAttestations` + `attestationLinks` to decide whether a payment is blocked. **Never use `requiredAttestations` alone** — it lists schema IDs informationally and can be non-empty even when the user already holds everything.
>
> | `hasAllAttestations` | `attestationLinks` | What it means                                                       |
> | -------------------- | ------------------ | ------------------------------------------------------------------- |
> | `true`               | empty              | User holds all attestations — payment can proceed immediately.      |
> | `false`              | non-empty          | User is missing attestations — show every link as-is and wait.      |
>
> When `attestationLinks` is non-empty: show every link verbatim, do not open/resolve them yourself, do not complete attestations on the user's behalf, and do not hide options that require attestations.

### 4. Second call — execute chosen payment (phase 2)

This step is **always required** — there is no fast-path that skips it, even when only one payment option was offered. Once the user selects (or confirms) a payment, call the script again with the cached file path and the chosen `--paymentHash`:

```bash
node scripts/buildX402Payment.js \
  --paymentRequiredFilePath '<paymentRequiredFilePath from phase 1>' \
  --paymentHash '<hash of chosen payment>'
```

**Do not pass `--resource` here.** Phase 2 reads the cached challenge from `--paymentRequiredFilePath` and looks up the payment by `--paymentHash`; combining either with `--resource` is rejected. If the server has rotated the challenge in the meantime, the signed payment will be rejected and the script will report `data.newPaymentRequired` — re-run phase 1 to discover the new challenge.

Check the output `status` and follow the rules in [Handling output](#handling-output) below.

---

## Handling output

After **any** invocation (phase 1 or phase 2), branch on `status`:

### `status: "success"`

The resource was fetched. Use `data` as the response body and report it to the user.

### `status: "failed"`

Show `message` to the user and stop. Do not auto-retry. If the user explicitly asks to try again after resolving the issue, you may re-run phase 1 from the top.

### `status: "input_required"`

Do **not** make your own HTTP request to the resource. Inspect `data` and act per the sub-type:

| `data` field                | Action                                                                                                                                                                                                                  |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data.attestationsRequired` | Show every URL in `data.attestationLinks` to the user verbatim. Wait for the user to **explicitly confirm** they completed the attestation, then re-run phase 2 with the same `--paymentRequiredFilePath`/`--paymentHash` — the script will re-check. Do not poll or guess that they are done. |
| `data.maxUseExceeded`       | The chosen payment exceeded its allowed uses. Do not retry the same hash. Go back to step 3's option list, ask the user to pick a different one, and run phase 2 again (reuse the same `--paymentRequiredFilePath`).    |
| `data.newPaymentRequired`   | Server rotated the challenge. Re-enter phase 1 with `--resource <same url>` — a new file path will be cached — then loop back to step 3. Continue until you reach `success` or `failed`.                                |

---

## Examples

### Standard payment flow (user confirmation required)

```
User: "Get me the weather from https://api.example.com/weather — it's a paid endpoint."

Agent: [runs getIdentities.js — confirms identity exists]
Agent: [runs buildX402Payment.js --resource 'https://api.example.com/weather']
       → { "status": "input_required", "data": {
            "resource": { "url": "https://api.example.com/weather", "description": "Weather data" },
            "paymentOptions": [
              { "hash": "a1b2c3...", "amount": "10000", "asset": "USDC", "network": "eip155:84532",
                "requiredAttestations": [], "hasAllAttestations": true, "attestationLinks": [] },
              { "hash": "d4e5f6...", "amount": "6000", "asset": "USDC", "network": "eip155:84532",
                "requiredAttestations": ["0xca35..."], "hasAllAttestations": false,
                "attestationLinks": ["https://wallet.billions.network#request_uri=..."] }
            ],
            "paymentRequiredFilePath": "/tmp/9f3c....json" }}

Agent: "You are about to pay for: Weather data (https://api.example.com/weather).
        There are 2 payment options:
        1) 10000 USDC on eip155:84532 — no attestations required
        2) 6000 USDC on eip155:84532 — requires attestation (missing).
           Complete verification: [link]
        Which would you like?"

User: "Option 1"

Agent: [runs buildX402Payment.js --paymentRequiredFilePath '/tmp/9f3c....json' --paymentHash 'a1b2c3...']
       → { "status": "success", "data": { "temperature": 22, "city": "Kyiv" } }

Agent: "The weather data shows 22°C in Kyiv."
```

### New 402 after payment (loop)

```
Agent: [runs buildX402Payment.js --paymentRequiredFilePath '/tmp/9f3c....json' --paymentHash 'a1b2c3...']
       → { "status": "input_required", "data": { "newPaymentRequired": "eyJ4NDAy..." } }

Agent: [runs buildX402Payment.js --resource 'https://api.example.com/weather']
       → { "status": "input_required", "data": { "resource": {...}, "paymentOptions": [...],
            "paymentRequiredFilePath": "/tmp/b71e....json" }}
…
Agent: [runs buildX402Payment.js --paymentRequiredFilePath '/tmp/b71e....json' --paymentHash '...']
       → { "status": "success", "data": { "temperature": 22, "city": "Kyiv" } }
```

### Attestation required (on chosen payment)

```
Agent: [runs buildX402Payment.js --paymentRequiredFilePath '/tmp/9f3c....json' --paymentHash 'd4e5f6...']
       → { "status": "input_required", "data": { "attestationsRequired": true,
            "message": "The following attestations are required to complete the payment:",
            "attestationLinks": ["https://wallet.billions.network#request_uri=..."] }}

Agent: "You need to complete an attestation before paying. Please open this link: [link]
        Let me know once you've completed it and I'll retry."
User: "Done."
Agent: [retries buildX402Payment.js with same arguments]
```

### Max use exceeded

```
Agent: [runs buildX402Payment.js --paymentRequiredFilePath '/tmp/9f3c....json' --paymentHash 'd4e5f6...']
       → { "status": "input_required", "data": { "maxUseExceeded": true,
            "message": "Payment has exceeded its maximum allowed uses. Choose a different payment or contact the resource provider." }}

Agent: "The selected payment option has reached its maximum number of uses.
        Please choose a different payment option:
        1) 10000 USDC on eip155:84532 — no attestations required
        Which would you like?"

User: "Option 1"

Agent: [runs buildX402Payment.js --paymentRequiredFilePath '/tmp/9f3c....json' --paymentHash 'a1b2c3...']
       → { "status": "success", "data": { "temperature": 22, "city": "Kyiv" } }
```
