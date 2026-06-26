# Security model

This skill manages **on-chain hot wallets** to pay for Mobula's pay-as-you-go API. Read this before deploying it on a machine that handles real funds.

## What the skill does with private keys

1. **Generates** a fresh secp256k1 wallet via `viem/accounts` (no entropy is sourced from the network).
2. **Stores** the private key encrypted at rest using AES-256-GCM.
3. **Decrypts in memory** only when signing a Tempo `transferWithMemo` transaction in response to a 402 challenge from `mpp.mobula.io`.
4. **Never transmits** the private key anywhere. It does not touch any network egress.

The plaintext key only exists inside the running Node/Bun process — it is not written to logs, not exported, not sent over RPC.

## Storage layout

| Wallet kind | Path | Encryption key |
|---|---|---|
| CLI hot wallet (single user) | `~/.mpp-skill/wallet.json` | 32-byte random secret at `~/.mpp-skill/.secret` (`chmod 600`), generated on first run |
| Per-user agent wallet (multi-tenant) | `.claude/claudeclaw/wallets/{userId}.json` | `HMAC-SHA256(WALLET_SECRET, userId)` where `WALLET_SECRET` is at `.claude/claudeclaw/wallet.secret` (`chmod 600`) |

Different agents on the same host with separate working directories cannot decrypt each other's wallets because each working dir gets its own `wallet.secret`. Different Telegram users on the same agent cannot decrypt each other's wallets because the per-user key derivation includes the user ID.

## Threat model

**In scope:**
- Casual local file inspection (`cat wallet.json`) → ciphertext only, useless without `.secret`.
- Cross-user inspection on a multi-tenant Telegram bot → ciphertext only, no decryption path.
- A misconfigured or compromised Mobula payment server returning an inflated 402 challenge → blocked by the **per-call amount cap** (`MAX_CHALLENGE_AMOUNT_ATOMS = $0.01`); a malicious server cannot drain more than $0.01 per call before the skill refuses to sign.
- A wrong chain id in the 402 challenge → blocked, only chainId 4217 (Tempo) is accepted.
- An off-prefix recipient or non-Tempo currency → on-chain rejection (memo layout enforced server-side by `mppx`).

**Out of scope (acceptable risks):**
- Local-machine compromise (root, malware reading `~/.mpp-skill/.secret`) → **the wallet is compromised**. This is a hot wallet for ≤ a few dollars; treat it as such.
- A compromised host bridging the wallet's full balance via your own bridge UI → same as above.
- A compromised npm dependency exfiltrating the private key → same as for any wallet library; pin versions, audit `bun.lock`.

## Spending limits (built-in)

```ts
// src/mpp/tempo-client.ts
export const MAX_CHALLENGE_AMOUNT_ATOMS = 10_000n;  // $0.01 per call
```

This is a hard refusal at the skill layer. The skill checks the requested amount **before** signing, so a 402 with `amount: 50000000` ($50, what `/agent/mpp/subscribe` would charge) is rejected with an error rather than silently signed away. Subscription flows are intentionally not handled by this skill — only per-call data endpoints under `/api/2/*` (~$0.0004 each).

To raise this cap (e.g. to enable subscription via this skill), edit the constant explicitly. There is no env var override, on purpose.

## Network egress

The skill's allowlist (declared in `package.json` under `clawhub.permissions.network`):

- `https://mpp.mobula.io` — paid Mobula API endpoints + 402 challenge issuer
- `https://rpc.tempo.xyz` — Tempo public RPC for sending the payment tx and checking balance
- `https://relay.link` — bridge UI link printed to the user (no secrets sent here, just a URL)

No telemetry, no analytics, no third-party crash reporting.

## Code paths that touch the private key

Static-analysis-friendly summary of where the plaintext key appears:

| File | Function | What it does with the key |
|---|---|---|
| `src/cli-wallet.ts` | `createCliWallet` | Generates with `viem.generatePrivateKey`, encrypts, writes ciphertext to disk. Plaintext is returned to the in-process caller for the same session only. |
| `src/cli-wallet.ts` | `loadCliWallet` | Reads ciphertext from disk, decrypts in memory, returns. |
| `src/wallet.ts` | `createUserWallet` | Same as above but for per-user wallets. |
| `src/wallet.ts` | `getUserPrivateKey` | Decrypts and returns the private key for the calling agent process. |
| `src/mpp/tempo-client.ts` | `tempoFetch` | Receives the key as an argument, passes it to `viem`'s `privateKeyToAccount` to sign one `transferWithMemo` transaction, then drops the reference. |

The key never leaves these call paths. There is no `console.log(privateKey)`, no fetch with the key in headers/body, no file write of the plaintext.

## Reporting issues

Open an issue at <https://github.com/Flotapponnier/mpp-skill/issues>. For security-sensitive reports, please use email rather than a public issue.
