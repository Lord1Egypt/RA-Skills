# Verification

How to decide whether an OracleNet response is verified, and what to report when
it is not.

## The short version

- Signing algorithm is **ES256K** (ECDSA over secp256k1, SHA-256).
- Public keys live at `https://tooloracle.io/.well-known/jwks.json`.
- **Not every response is signed.** Most are not.
- Verify locally by matching the JWS header `kid` against the JWKS. You never
  need to call a remote verification service, and verification costs nothing.
- If you did not verify a signature, do not say the result is verified.

## The four states

Report exactly one of these in `verification_status`. They are not
interchangeable.

| State | Means | Requires |
|---|---|---|
| `signed-and-verified` | a signature was present and it checked out | you fetched the JWKS and validated the signature |
| `signed-not-verified` | a signature was present, you did not check it | you saw a signature field |
| `unsigned` | the route returned no signature | you looked and found none |
| `unknown` | you did not look | — |

The most common honest answer for a routine data call is **`unsigned`**. That is
not a defect: the free data routes return provenance envelopes (`request_id`,
`product`, `tool`, `timestamp`), not signatures.

## Signature ≠ hash ≠ receipt ≠ provenance

Four different things, routinely conflated:

- **Signature** — an ES256K signature over content, verifiable against a public
  key. Proves *who* produced it and that it has not changed.
- **Content hash** — a SHA-256 digest. Proves the content has not changed *if*
  you obtained the digest through a trusted path. On its own it proves nothing:
  whoever altered the content could recompute the digest.
- **Receipt** — an endpoint-specific record that something happened (for example
  a settlement). Evidence about an event, not an attestation of the payload.
- **Provenance envelope** — `request_id`, `product`, `tool`, `timestamp`. Useful
  for audit trails and debugging, cryptographically worthless.

Only the first supports `signed-and-verified`.

## Where a signature can arrive

`verification-policy.json → signed_response` states that transport varies:
response headers, body metadata, or endpoint-specific receipts. Header names and
field locations are declared per tool in the MCP card.

There is **no global flag that forces signing on every tool**. If you need a
signed result, pick a route whose card declares signing — do not ask for one.

## How to verify

1. Read the JWS header, take `alg` and `kid`.
2. Fetch `https://tooloracle.io/.well-known/jwks.json`.
3. Select the key whose `kid` matches. Do not fall back to "the first key" —
   a `kid` that is absent from the JWKS is a failed verification, not a reason
   to try another key.
4. Rebuild the signing input as `base64url(header) + "." + base64url(payload)`.
5. The JWS signature is raw `r || s`, 32 bytes each. Most crypto libraries want
   DER, so convert before verifying.
6. Verify with ECDSA/SHA-256 over secp256k1.

A worked example that verifies successfully today:
`https://tooloracle.io/.well-known/issuer-statement.json` carries a JWS signed
by `tooloracle-issuer-keys-1`, and that key is in the JWKS.

## The keys you will encounter

`jwks.json` currently publishes several keys. Their roles differ:

- **`tooloracle-issuer-keys-1`** — the dedicated ToolOracle issuer key (EC,
  secp256k1, ES256K). New signatures use this.
- **`fo-ecdsa-v1`** and **`feedoracle-mcp-es256k-1`** — legacy FeedOracle-era
  keys, retained so historically signed material still verifies. A signature
  under one of these is not invalid; it is old.
- **`feedoracle-mldsa65-1`** — an ML-DSA-65 post-quantum key. Present in the
  JWKS. Do not assume any given route uses it.

Read the JWKS at runtime rather than pinning this list — keys rotate.

## A live inconsistency you must know about

Two published surfaces disagree about the issuer state:

| Surface | Says |
|---|---|
| `/.well-known/jwks.json` | contains `tooloracle-issuer-keys-1` |
| `/.well-known/issuer-statement.json` | dedicated key activated 2026-04-28, JWS verifies against that key |
| `/.well-known/agent.json` → `verification` | `issuer_key_state: "dedicated_active"` |
| `/.well-known/verification-policy.json` v1.0.0 | `is_dedicated_to_tooloracle: false`, `migration_status: "planned"`, "not yet deployed" |

Three surfaces say the dedicated key is live; the policy document still
describes the pre-migration state and has not been regenerated since the key was
activated.

**What to do:** trust the JWKS and the signature, not the prose. A signature
verifies or it does not — that question is settled by `jwks.json`, and the
answer does not change because a policy document is out of date.

Do **not** repeat the claim that a dedicated ToolOracle issuer key is "planned
but not yet deployed". Earlier versions of this skill said exactly that, and it
has been false since 2026-04-28.

Treat `verification-policy.json` as authoritative for **policy** — how signing is
requested, what transports are used, what the timestamp rules are. Treat the
JWKS as authoritative for **key material**.

## What to do when a route is unsigned or only `partial`

1. **Do not manufacture confidence.** Set `verification_status: "unsigned"`.
2. **Record what you do have** — `request_id`, `tool`, `timestamp`, endpoint —
   in `provenance`.
3. **Say what is missing** in `limitations`, e.g. "single source, unsigned,
   retrieved 2026-07-31T09:10Z".
4. **Corroborate if it matters.** For a consequential claim, take a second route
   and compare. Two independent unsigned sources that agree is a materially
   stronger position than one — and it is still not an attestation.
5. **Escalate rather than assert.** If the task genuinely requires an attested
   result and no route provides one, say so instead of downgrading the
   requirement quietly.

## Blockchain anchoring

`verification-policy.json` declares anchoring for *defined evidence flows only*,
across polygon, base, xrpl, hedera, and avalanche. Anchoring is **not** applied
to ordinary calls. Do not tell a user their result is "anchored on-chain" unless
that specific flow returned an anchor reference.

## Things never to say

- "All OracleNet responses are signed." — false.
- "The result is verified." — only after you actually verified it.
- "Signed by ToolOracle" for a signature you did not check against the JWKS.
- "Certified" / "regulator-approved" / "audited" — no such claim is supported.
- "Anchored on-chain" for a call that returned no anchor.
