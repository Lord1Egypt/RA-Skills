---
name: nostr-auth
description: "Authenticate to Nostr sign-in challenges (NIP-07 style) without a wallet or browser extension. Signs kind-22242 AUTH challenge events with a secp256k1 (BIP-340) key derived from a local master secret and optionally submits them to the service callback. Use when a site or API asks for a signed Nostr event to prove key ownership. More methods coming: NIP-98 HTTP Auth, NIP-42 relay AUTH, NIP-05."
version: 1.0.0
homepage: https://github.com/dyegolara/nostr-auth-agents
metadata:
  openclaw:
    requires:
      bins: [node]
    envVars:
      - name: NOSTR_AUTH_KEYFILE
        required: false
        description: Optional path for the persistent 32-byte master secret.
---

# Nostr sign-in (NIP-07)

Use this skill for authentication only — signing sign-in events that prove
ownership of a Nostr identity. It never publishes notes, connects to relays
beyond the configured callback, or requires a wallet or browser extension.

## Inputs

- A sign-in challenge from a "Sign in with Nostr" page or API — either an
  event template (`kind`, `tags`, `content`) or a challenge string.
- Optional `--domain` for the service host (used for deterministic key
  derivation), `--callback` URL to submit the signed event to.
- Optional `--dry-run` when the signed event must be inspected before
  submission.

Do not invent or alter challenges. Ask for a fresh challenge when the service
reports it was already used.

## Run

The bundled helper uses only Node.js built-ins and lives at:

```text
<skill_dir>/scripts/nostr_auth.js
```

Inspect the identity and signature without authenticating:

```bash
node <skill_dir>/scripts/nostr_auth.js pubkey --domain example.com
node <skill_dir>/scripts/nostr_auth.js --challenge "<hex>" --relay "wss://..." --dry-run --json
```

After confirming the service and callback are expected, submit:

```bash
node <skill_dir>/scripts/nostr_auth.js --challenge "<hex>" --relay "wss://..." --callback "https://example.com/verify" --json
```

Or sign a full event template:

```bash
node <skill_dir>/scripts/nostr_auth.js sign '{"kind":22242,"tags":[["challenge","<hex>"]],"content":""}' --domain example.com --callback https://example.com/verify --json
```

The helper requires Node.js 20.19 or newer. The only network request is the
final callback POST.

## Protocol

1. Derive a per-service secp256k1 private key: `HMAC-SHA256(master, domain)`,
   from the persisted master secret (`~/.config/nostr-auth/master.key`, mode
   `0600`).
2. Build the event (kind 22242 for challenges by default), compute the NIP-01
   id `sha256(JSON.stringify([0, pubkey, created_at, kind, tags, content]))`.
3. Sign the raw 32-byte id with BIP-340 schnorr; store the 64-byte signature
   as hex in `event.sig`.
4. POST `{"event": <signed>}` to the callback. Interpret `{"status":"OK"}` as
   accepted; a fresh challenge is needed after `{"status":"ERROR"}`.

## Identity and safety

- Keep the master secret local (`0600`); expose the nsec to nobody.
- Per-domain derivation keeps unrelated services from correlating identity.
- Inspect the callback URL and signed event in `--dry-run` before submitting.
- The `npub` derived here is an agent identity — it is not the same key as a
  user's browser extension unless the master secret comes from it.

## Failure handling

- `Invalid hex` / `odd length` — malformed key or challenge input.
- `Callback returned non-JSON or HTTP <n>` — the service is down or the URL is
  wrong; verify `--callback`.
- `{"status":"ERROR"}` — challenge may already be used; request a fresh one.

## Self-test (offline, cost-free)

```bash
cd <skill_dir>
npm test
```

The local mock service validates the full sign → submit → verify roundtrip.