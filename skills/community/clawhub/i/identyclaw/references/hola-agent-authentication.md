# HOLA Protocol - Inter-Agent Authentication

Complete guide to the HOLA protocol for proving your identity to other agents using cryptographic signatures.

## Table of Contents

- [Quick Start: HOLA Generation Pattern](#quick-start-hola-generation-pattern)
- [Overview](#overview)
- [When is a HOLA validated?](#when-is-a-hola-validated)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Vocabulary (HOLA)](#vocabulary-hola)
- [HOLA Message Format](#hola-message-format)
- [Canonical form vs on-the-wire appearance](#canonical-form-vs-on-the-wire-appearance)
- [Authentication Flow](#authentication-flow)
- [Step 1: Get JWT Token](#step-1-get-jwt-token)
- [Step 2: Request Nonce](#step-2-request-nonce)
- [Step 3: Construct HOLA Message](#step-3-construct-hola-message)
- [Step 3.5: Canonicalization (CRITICAL)](#step-35-canonicalization-critical)
- [Step 3.6: Sign the Canonical Message](#step-36-sign-the-canonical-message)
- [Step 3.7: Checksum Calculation](#step-37-checksum-calculation)
- [Complete Pattern Example](#complete-pattern-example)
- [Step 4: Send HOLA to Peer](#step-4-send-hola-to-peer)
- [Step 5: Verify HOLA (Peer Agent) — HTTP API path](#step-5-verify-hola-peer-agent--http-api-path)
- [Verify Your HOLA Works](#verify-your-hola-works)
- [Common Pitfalls](#common-pitfalls)
- [Debugging HOLA Failures](#debugging-hola-failures)
- [Next Steps](#next-steps)

## Quick Start: HOLA Generation Pattern

**Reference (IdentyClaw)** — API `https://api.identyclaw.com`. Login and nonce retrieval use curl + Bearer JWT (no client-side NEAR RPC for server validation). HOLA line signing below is the proven wire format from this deployment.

**⚠️ CRITICAL:** HOLA messages are time-sensitive — generate fresh timestamps and nonces for each message.

### Complete Flow Pattern

```javascript
// Reference (IdentyClaw) wire format — your values will differ each run
const nacl = require('tweetnacl');
const base32 = require('hi-base32');
const bs58 = require('bs58');
// 1. Get fresh JWT token (see Step 1 for details)
const jwt = await getJWT(); // Bearer token (see Step 1);
// 2. Request a fresh nonce for this HOLA message
const nonceResponse = await fetch('https://api.identyclaw.com/api/holanonce16ts', {
  headers: { 'Authorization': `Bearer ${jwt}` }
});
const { noncetsHex, timestamp } = await nonceResponse.json();
// Example response: { noncetsHex: "A1B2C3D4E5F6...", timestamp: "2026-05-04T10:09:00.000Z" }
// 3. Build message (everything before signature)
const recipient = 'MUNDO';
const tokenId = 'bjbvcjzqbdsj'; // Your 12-letter passport ID;
const message = `HOLA/${recipient}/${tokenId}/${timestamp}/${noncetsHex}/API.IDENTYCLAW.COM/`;
// 4. Canonicalize (UPPERCASE everything)
const canonicalMessage = message.toUpperCase();
// Result: "HOLA/MUNDO/BJBVCJZQBDSJ/2026-05-04T10:09:00.000Z/A1B2C3D4E5F6.../API.IDENTYCLAW.COM/"
// 5. Sign the canonical message
const messageBytes = new TextEncoder().encode(canonicalMessage);
const signature = nacl.sign.detached(messageBytes, yourSecretKey);
const signatureB32 = base32.encode(Buffer.from(signature)).replace(/=+$/, '').toUpperCase();
// Example: "MFRGG2LTMVZXGZLSN5XWC3TBNRQW4ZDJMQFA..."
// 6. Calculate checksum
const checksumPrefix = `${canonicalMessage}${signatureB32}/`;
const sum = 0;
sum += checksumPrefix.charCodeAt(i);
const holaChecksumAlphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ';
const checksum = holaChecksumAlphabet[sum % 23];
// Example: sum=12543, checksum='J' (index 8 in alphabet; omits I, L, O)
// 7. Build final HOLA
const hola = `${canonicalMessage}${signatureB32}/${checksum}`;
// Example result: "HOLA/MUNDO/BJBVCJZQBDSJ/2026-05-04T10:09:00.000Z/A1B2.../API.IDENTYCLAW.COM/MFRGG.../J"
```

**Key Points**:
- ✓ Generate **fresh nonce** for each HOLA (5-minute validity)
- ✓ Use **current timestamp** from nonce response
- ✓ **Uppercase** entire message before signing
- ✓ Sign with **Ed25519 private key** of passport owner
- ✓ Encode signature as **base32** (not base64)
- ✓ Calculate **checksum** on canonical message + signature + `/`
- ✓ **Wire presentation**: You do **not** need to send the line in all capitals; verifiers normalize casing. You still sign the uppercase canonical prefix ([Canonical form vs on-the-wire appearance](#canonical-form-vs-on-the-wire-appearance))

## Overview

HOLA (Hello Authentication) is a peer-to-peer protocol: agents prove Passport identity to each other with signed **HOLA lines**.

### When is a HOLA validated?

Verifying the checksum locally, or checking that an Ed25519 signature verifies against a public key you fetched yourself, is **not** sufficient to treat a received HOLA as authenticated for trust or authorization. Those checks only show that the string is well-formed and that *some* key signed *something* matching that payload.

**Full validation** means applying the complete proof bar: on-chain Passport state (exists, active, not expired), signature and checksum validity, fresh timestamp, nonce replay safety, and recipient binding. You can reach that bar in two ways:

| Path | When to use |
| --- | --- |
| **Direct (peer-to-peer)** | Peers verify on-chain state and cryptography locally (for example with `@rodit/rodit-auth-be` and NEAR RPC). No IdentyClaw API participates in the interaction. |
| **Via IdentyClaw HTTP API** | Call `POST /api/identity/verify` — this server's packaged implementation of the same checks. Documented in detail below. |

**This guide documents the HTTP API path** because it is what IdentyClaw implements. It does **not** mean Passport holders must route peer trust through this API.

**When using the HTTP API path:** treat an inbound HOLA as validated only after `POST /api/identity/verify` completes successfully with an outcome that confirms verification—for example `verified: true` with passing checks and no blocking failures (see [Step 5](#step-5-verify-hola-peer-agent--http-api-path)). Until then, do not grant access, secrets, tools, or elevated behavior based on checksum or bare signature checks alone.

`POST /api/testhola` is for diagnosing **your own** HOLA generation. It is **not** a substitute for full validation when deciding whether to trust **another agent's** HOLA.

**Trust the API, not just TLS (HTTP path only):** `/api/identity/verify` only protects you if the JWT session came from the real IdentyClaw API. **Default:** curl login against a pinned hostname plus impersonation checks ([finding-agents.md](finding-agents.md)). **Optional:** `@rodit/rodit-auth-be` `RoditClient.login_server()` validates the server Passport via NEAR RPC—see [Verify the API server (MITM protection)](login-authentication.md#verify-the-api-server-mitm-protection).

Conceptual background: [`public/policies/why-identyclaw.md`](../public/policies/why-identyclaw.md) §3.1 and §8.1.

### Envelope vs HOLA line

Handle your own messaging or routing outside this protocol however you need. Put Passport proof only in the **HOLA line**—not inside unrelated envelope or routing fields.

### HOLA Format Boundaries

- Send HOLA as one slash-separated string in the request payload: `{"hola": "<single HOLA string>"}`.
- Build HOLA signatures from the **HOLA canonical prefix** using **base32** only (RFC 4648 on the signed prefix).
- Use the ISO 8601 timestamp returned by `GET /api/holanonce16ts` for HOLA.
- **Capitalization on the wire is optional**: nothing requires an all-uppercase transmitted line. **Stylistic choices that fit your agent’s identity are welcome** (for example a lowercase `hola/` greeting), as long as the cryptographic steps use the canonical uppercase signed payload ([Canonical form vs on-the-wire appearance](#canonical-form-vs-on-the-wire-appearance)).

**Self-diagnostic loop:** Use `POST /api/testhola` to troubleshoot HOLA format and signature issues. Each error response includes `details.documentation.see` (paths into `references/`) and `details.example` (a corrected value for the failing field), so you can iterate without leaving the endpoint. It does **not** replace `POST /api/identity/verify` when you must decide whether another agent’s HOLA is trustworthy ([When is a HOLA validated?](#when-is-a-hola-validated)).

## When to Use

Use HOLA Protocol when you need to:

- Prove your identity to another agent
- Establish trust with a peer agent
- Implement agent-to-agent communication
- Enable decentralized verification — peers apply the full proof bar directly or via a verification service (see [When is a HOLA validated?](#when-is-a-hola-validated))
- **You ALREADY have a bearer token** for IdentyClaw HTTP calls (see [Prerequisites](#prerequisites))

## Prerequisites

Before using HOLA, you must:

1. **Have a valid JWT token** - Complete [API Login](login-authentication.md) first
2. **Know your Passport ID** - Your 12-letter identity (e.g., `bkbvehbdcrgm`)
3. **Have access to your NEAR private key** - From the account that owns your Passport

## Vocabulary (HOLA)

This guide uses the following terms consistently. **HTTP fields stay as defined in OpenAPI** (for example the JSON property `hola`, responses from `GET /api/holanonce16ts`).

| Term | Meaning |
| --- | --- |
| **HOLA line** | Full slash-separated wire string (for example the JSON `hola` field on verify/test endpoints) |
| **HOLA canonical prefix** | UTF-8 bytes from `HOLA/` through `API.IDENTYCLAW.COM/`, uppercased for signing |
| **HOLA nonce** | JSON field `noncetsHex` from `GET /api/holanonce16ts` (32 uppercase hex characters in the line) |
| **HOLA timestamp** | JSON field `timestamp` from the same response (ISO-8601; not login `timestamp_iso`) |
| **base32 line signature** | Ed25519 signature over the canonical prefix, base32-encoded for the line |
| **Bearer token** | Credential in `Authorization: Bearer …` for IdentyClaw endpoints that require a session (nonce fetch, verification, etc.); **not** a substitute for sending a **HOLA line** to a peer |

## HOLA Message Format

**Structure**:
```
HOLA/<recipient>/<tokenId>/<ISO8601-timestamp>/<noncets-hex>/API.IDENTYCLAW.COM/<base32-signature>/<checksum>
```

**Components**:

| Field | Description | Example |
|-------|-------------|---------|
| `HOLA/` | Protocol identifier | `HOLA/` |
| `recipient` | Intended recipient (default: MUNDO) | `MUNDO` or `abcdefghijkl` |
| `tokenId` | Sender's Passport ID (12 lowercase letters) | `bkbvehbdcrgm` |
| `timestamp` | ISO 8601 timestamp | `2026-04-19T10:47:00.000Z` |
| `noncets-hex` | 32 uppercase hex characters (16 bytes) from `/api/holanonce16ts` | `4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE` |
| `API.IDENTYCLAW.COM` | Domain identifier | `API.IDENTYCLAW.COM` |
| `signature` | base32-encoded Ed25519 signature (RFC 4648, A-Z2-7, uppercase, no padding) | `N3FZ5KQ8LH2BSM1XY` |
| `checksum` | Single letter from `ABCDEFGHJKMNPQRSTUVWXYZ` (23 letters; omits **I**, **L**, **O**) | `J` |

**Example HOLA Message**:
```
HOLA/MUNDO/bkbvehbdcrgm/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/dGVzdHNpZ25hdHVyZQ/M
```

## Canonical form vs on-the-wire appearance

HOLA distinguishes two ideas: **what must be signed and checksummed**, and **what characters may appear when you transmit the line**.

### Cryptographic canonical form

Verification always uses a single deterministic UTF-8 string: the segment from `HOLA/` through `API.IDENTYCLAW.COM/` with **that entire prefix uppercased** (see [Step 3.5](#step-35-canonicalization-critical)). You sign those octets with Ed25519, encode the signature as base32 (RFC 4648, uppercase A–Z and 2–7, no padding), then compute the checksum over the canonical uppercase prefix plus the base32 signature and a trailing `/`. If any of those steps use a different casing for the signed payload, the signature or checksum will not match.

### Presentation on the wire (optional)

**Sending an all-uppercase line is not required.** The protocol does not prescribe “official-looking” caps on the wire. Many examples use uppercase because the signing step uses an uppercase canonical prefix and copying that same string is convenient—not because peers must shout `HOLA`.

**Creative or distinctive presentation that reflects your agent’s identity is welcome**: tone in logs or UI, a lowercase `hola/` if that fits your persona, or any harmless stylistic choice—provided you still produce a valid signature and checksum over the **canonical uppercase** signed bytes above. IdentyClaw HTTP validators normalize letter casing when parsing and reconstruct that canonical payload for verification. **`POST /api/testhola` uses the same normalization** and does not reject a message solely because the prefix was sent as `hola/` instead of `HOLA/`.

### Signature field (base32)

The signature itself is base32 (RFC 4648) with an uppercase alphabet by specification. That is separate from how you choose to spell the protocol keyword on the wire.

## Authentication Flow

```
Agent A (Initiator):
1. POST /api/login → Get JWT
2. GET /api/holanonce16ts → Get nonce
3. Construct HOLA message with signature
4. Send HOLA to Agent B

Agent B (Verifier):
5. POST /api/login → Get JWT (if not already authenticated)
6. POST /api/identity/verify → Full server validation of Agent A's HOLA (required before trusting)
7. Trust established only after verify succeeds (see When is a HOLA validated? above)
```

**Note:** Steps 5–6 describe the IdentyClaw HTTP API path. Peers may instead validate on-chain and cryptographically without calling this API ([When is a HOLA validated?](#when-is-a-hola-validated)).

## Step 1: Get JWT Token

You must have a valid JWT token before requesting nonces. See [API Login Authentication](login-authentication.md) for complete instructions.

**Quick summary**:
```bash
# 1. Get fresh one-time timestamp challenge
curl https://api.identyclaw.com/api/login/timestamp
# 2. Sign message: accountid + timestamp_iso
# 3. POST to login
curl -X POST https://api.identyclaw.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"accountid": "43d3c5b5e77a46b52933bc7a8b79b06f16dd4ca3cfbacd0e6fede0e7e01782ac", "timestamp": 1776622758, "base64url_signature": "..."}'
```

Use each login timestamp pair once. If login fails, fetch a new pair and retry.

## Step 2: Request Nonce

⚠️ **CRITICAL: Which Key Pair to Use**

You must use the private key of the NEAR account that **currently owns** your IdentyClaw Passport.

**Key Requirements:**
1. Use the private key of the **current owner account** of your Passport
2. Private key location: `~/.near-credentials/mainnet/<account_id>.json`
3. If you've transferred your Passport to a different account, use that account's credentials (see [Key rotation](key-rotation.md))

---

**Endpoint**: `GET /api/holanonce16ts` (requires JWT)

```bash
curl https://api.identyclaw.com/api/holanonce16ts \
  -H "Authorization: Bearer YOUR_JWT"
```

**Response Pattern** (values shown are illustrative only):
```json
{
  "noncetsHex": "4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE",
  "timestamp": "2026-04-19T10:47:00.000Z",
  "length": 16,
  "algorithm": "randomBytes(16)_hex",
  "requestId": "01HQXYZ..."
}
```

**Do not confuse with login:** `GET /api/login/timestamp` returns `timestamp` + `timestamp_iso` for API login only. HOLA uses **`GET /api/holanonce16ts`** with JSON keys **`noncetsHex`** and **`timestamp`** only (not `timestamp_iso`, `nonceHex`, or `noncets`). Canonical reference: [holanonce-api.md](holanonce-api.md).

**⚠️ CRITICAL - Nonce Freshness**:
- Nonces are valid for approximately **5 minutes**
- Generate a **NEW nonce** for each HOLA message
- Treat documentation nonces as examples only; request and use fresh runtime nonce values
- Use the `noncetsHex` and `timestamp` values **immediately** after receiving them

**Extract nonce hex from response**: Use the `noncetsHex` field directly (already uppercase): `4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE`

## Step 3: Construct HOLA Message

**Message to sign** (everything before the signature field):
```
HOLA/<recipient>/<tokenId>/<timestamp>/<noncets-hex>/API.IDENTYCLAW.COM/
```

**Reference (IdentyClaw) — wire format** (your values will differ):
```
HOLA/MUNDO/bkbvehbdcrgm/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/
```

⚠️ Use the **fresh timestamp and nonce** from Step 2, not values from this example.

## Step 3.5: Canonicalization (CRITICAL)

The signed payload is always the **uppercase canonical prefix** through `API.IDENTYCLAW.COM/`. How you **transmit** that line is up to you; verifiers normalize casing (see [Canonical form vs on-the-wire appearance](#canonical-form-vs-on-the-wire-appearance)).

**Before signing, convert ALL components to UPPERCASE:**

⚠️ **This is the most common source of HOLA signature failures.**

**Components to uppercase:**
1. **recipient** → `MUNDO` (already uppercase)
2. **tokenId** → `BKBVEHBDCRGM` (even though stored as lowercase in database)
3. **timestamp** → `2026-04-19T10:47:00.000Z` (verify 'Z' is uppercase)
4. **noncetsHex** → `4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE` (already uppercase from API)
5. **domain** → `API.IDENTYCLAW.COM` (already uppercase)

**Reference (IdentyClaw) — wire format** (use your fresh values from Step 2):
```javascript
// Original message components (use YOUR fresh values)
const recipient = 'MUNDO';
const tokenId = 'bkbvehbdcrgm';  // Your 12-letter passport ID (lowercase from storage);
const timestamp = '2026-04-19T10:47:00.000Z';  // From Step 2 nonce response;
const noncetsHex = '4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE';  // From Step 2 nonce response;
// Build message
const message = `HOLA/${recipient}/${tokenId}/${timestamp}/${noncetsHex}/API.IDENTYCLAW.COM/`;
// Canonicalize: UPPERCASE EVERYTHING
const canonicalMessage = message.toUpperCase();
// Result: "HOLA/MUNDO/BKBVEHBDCRGM/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/"
// Sign the canonical message
const messageBytes = new TextEncoder().encode(canonicalMessage);
const signature = nacl.sign.detached(messageBytes, secretKey);
```

⚠️ **Critical**: Sign the **canonicalized (uppercase) message**, not the original case.

## Step 3.6: Sign the Canonical Message

**Signing:** Ed25519 detached over UTF-8 bytes of the **HOLA canonical prefix**; encode the result as **base32** for the HOLA line (not base64url).

1. Convert **canonical (uppercase)** prefix to UTF-8 bytes
2. Sign with Ed25519 secret key
3. Encode signature as **base32** (RFC 4648, A-Z2-7, uppercase, no padding)

**Reference (IdentyClaw) — JavaScript wire format** (use your fresh values):
```javascript
const nacl = require('tweetnacl');
const base32 = require('hi-base32');
const bs58 = require('bs58');
const fs = require('fs');
// 1. Load credentials
const creds = JSON.parse(fs.readFileSync('~/.near-credentials/mainnet/your-account.json'));
const privateKeyBase58 = creds.private_key.replace('ed25519:', '');
// 2. Decode keypair
const keypair = bs58.decode(privateKeyBase58);
const secretKey = keypair.slice(0, 32);
// 3. Build and canonicalize message (use YOUR fresh timestamp and nonce from Step 2)
const message = `HOLA/MUNDO/bkbvehbdcrgm/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/`;
const canonicalMessage = message.toUpperCase();
// 4. Sign the canonical message
const messageBytes = new TextEncoder().encode(canonicalMessage);
const signature = nacl.sign.detached(messageBytes, secretKey);
// 5. Encode as base32 (RFC 4648: A-Z2-7, uppercase, no padding)
const signatureB32 = base32.encode(Buffer.from(signature)).replace(/=+$/, '').toUpperCase();
// Example result: "MFRGG2LTMVZXGZLSN5XWC3TBNRQW4ZDJMQFA..." (yours will differ)
```

**Reference (IdentyClaw) — Python wire format** (use your fresh values):
```python
from nacl.signing import SigningKey
import base58
import json
import base64
# 1. Load credentials
creds = json.load(f)
private_key_base58 = creds['private_key'].replace('ed25519:', '')
# 2. Decode keypair
keypair = base58.b58decode(private_key_base58)
secret_key = keypair[:32]
# 3. Build and canonicalize message (use YOUR fresh timestamp and nonce from Step 2)
message = 'HOLA/MUNDO/bkbvehbdcrgm/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/'
canonical_message = message.upper()
# 4. Sign the canonical message
signing_key = SigningKey(secret_key)
signature = signing_key.sign(canonical_message.encode('utf-8')).signature
# 5. Encode as base32 (RFC 4648)
import base64
signature_b32 = base64.b32encode(signature).decode('utf-8').rstrip('=').upper()
# Example result: "MFRGG2LTMVZXGZLSN5XWC3TBNRQW4ZDJMQFA..." (yours will differ)
```

## Step 3.7: Checksum Calculation

**Alphabet (fixed order, length 23):** `ABCDEFGHJKMNPQRSTUVWXYZ` (uppercase Latin letters **without** **I**, **L**, **O**).

**Algorithm**: Let `checksumPrefix` be the canonical uppercase signed payload through `API.IDENTYCLAW.COM/`, plus the base32 signature, plus a trailing `/`. Sum **UTF-16 code units** (same as JavaScript `charCodeAt` over that string—ASCII-only HOLA components match byte sums). Then `checksum = alphabet[sum % 23]`.

The checksum is calculated on the **canonicalized (uppercase) message + signature + trailing slash**.

### Canonical string (signing and checksum)

Use **one** uppercase prefix for both Ed25519 signing and the checksum (the signature is appended only for the checksum step):

1. Build the signed prefix (field order and slashes matter):

```
HOLA/<recipient>/<tokenId>/<ISO-8601-timestamp>/<noncets-hex>/API.IDENTYCLAW.COM/
```

| Field | Meaning |
|-------|---------|
| `recipient` | Intended recipient (often `MUNDO`; may be another agent's 12-letter Passport ID when addressing them directly) |
| `tokenId` | **Sender's** Passport id (12 letters; often stored lowercase, uppercased in canonical form) |
| `noncets-hex` | 32 hex characters from `GET /api/holanonce16ts` (16 random bytes as hex — not 16 hex chars) |

2. **Canonicalize:** `canonicalMessage = message.toUpperCase()` on the **entire** prefix string.
3. **Sign:** Ed25519 detached signature over UTF-8 bytes of `canonicalMessage`.
4. **Encode:** RFC 4648 base32, uppercase `A–Z2–7`, no `=` padding → `signatureB32` (always **103 characters** for Ed25519).
5. **Checksum input:** `checksumPrefix = canonicalMessage + signatureB32 + "/"` — include the trailing `/`; do **not** include the checksum letter.

**Self-test:** After assembling your HOLA, call `POST /api/testhola` while building as the sender. When validating a peer's HOLA, use `POST /api/identity/verify`. A checksum mismatch returns `expected` vs `got` in the error message — use that to diff your `checksumPrefix`.

```javascript
// Step 1: Build canonical message (already uppercase)
const canonicalMessage = message.toUpperCase();
// Example: "HOLA/MUNDO/BKBVEHBDCRGM/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/"
// Step 2: Add signature and trailing slash
const checksumPrefix = `${canonicalMessage}${signatureB32}/`;
// Example: "HOLA/MUNDO/.../API.IDENTYCLAW.COM/MFRGG2LTMVZXGZLSN5XWC3TBNRQW4ZDJMQFA.../"
// Step 3: Sum UTF-16 code units (charCodeAt)
const sum = 0;
sum += checksumPrefix.charCodeAt(i);
// Example: sum = 12543
// Step 4: Modulo 23 and pick letter from fixed alphabet
const holaChecksumAlphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ';
const checksum = holaChecksumAlphabet[sum % 23];
// Example: 12543 % 23 = 8 → alphabet[8] = 'J'
```

**Full checksum input example** (one continuous line; signature is illustrative — yours will differ):

```
HOLA/MUNDO/BKBVEHBDCRGM/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/FCHWM6BHKU43A4GB2HO4J455TH3AHAV4WCJJOWBS3VLWSZDRFKR6PYCV7RTPLYABEUY75BOQ4ONOOJ3N4U5JAHB2YECVNDMISI3DUDI/
```

Sum of UTF-16 code units over that string: 13807 → `13807 % 23 = 7` → checksum **`H`** (index 7 in `ABCDEFGHJKMNPQRSTUVWXYZ`).

**Critical Notes**:
- Checksum is calculated on the **uppercase canonical message**
- Include the **trailing slash** after the signature: `"...SIGNATURE/"`
- Use `charCodeAt()` (JavaScript) or equivalent UTF-16 code units over `checksumPrefix`
- Result is always **one uppercase letter** from `ABCDEFGHJKMNPQRSTUVWXYZ`
- This is **NOT** a cryptographic hash (it's a simple integrity check)

**Final HOLA Pattern** (same values as the checksum example above; signature is illustrative):

```
HOLA/MUNDO/BKBVEHBDCRGM/2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/FCHWM6BHKU43A4GB2HO4J455TH3AHAV4WCJJOWBS3VLWSZDRFKR6PYCV7RTPLYABEUY75BOQ4ONOOJ3N4U5JAHB2YECVNDMISI3DUDI/H
```

## Complete Pattern Example

**⚠️ Complete working code pattern - generate fresh values each time**

### JavaScript Complete Implementation

```javascript
const nacl = require('tweetnacl');
const base32 = require('hi-base32');
const bs58 = require('bs58');
const fs = require('fs');
async function generateHOLA(tokenId, jwtToken) {
// 1. Get fresh nonce for this run
const nonceResponse = await fetch('https://api.identyclaw.com/api/holanonce16ts', {
  headers: { 'Authorization': `Bearer ${jwtToken}` }
});
  throw new Error(`Failed to fetch nonce: ${nonceResponse.status}`)
const { noncetsHex, timestamp } = await nonceResponse.json();
// Example: { noncetsHex: "A1B2C3D4E5F6...", timestamp: "2026-05-04T10:09:00.000Z" }
// 2. Load your NEAR credentials
const creds = JSON.parse(fs.readFileSync(;
`~/.near-credentials/mainnet/${tokenId}.near.json`;
));
const privateKeyBase58 = creds.private_key.replace('ed25519:', '');
const keypair = bs58.decode(privateKeyBase58);
const secretKey = keypair.slice(0, 32);
// 3. Build message
const recipient = 'MUNDO';
const message = `HOLA/${recipient}/${tokenId}/${timestamp}/${noncetsHex}/API.IDENTYCLAW.COM/`;
// 4. Canonicalize (UPPERCASE)
const canonicalMessage = message.toUpperCase();
// 5. Sign
const messageBytes = new TextEncoder().encode(canonicalMessage);
const signature = nacl.sign.detached(messageBytes, secretKey);
const signatureB32 = base32.encode(Buffer.from(signature)).replace(/=+$/, '').toUpperCase();
// 6. Calculate checksum
const checksumPrefix = `${canonicalMessage}${signatureB32}/`;
const sum = 0;
sum += checksumPrefix.charCodeAt(i);
const holaChecksumAlphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ';
const checksum = holaChecksumAlphabet[sum % 23];
// 7. Build final HOLA
const hola = `${canonicalMessage}${signatureB32}/${checksum}`;
return {
  hola,
  tokenId,
  recipient,
  timestamp,
  noncetsHex,
  signatureB32,
  checksum
};
// Usage:
// const result = await generateHOLA('bjbvcjzqbdsj', yourJWT);
// console.log('HOLA:', result.hola);
```

### Python Complete Implementation

```python
import requests
import json
from nacl.signing import SigningKey
import base58
import base64
# 1. Get fresh nonce for this run
nonce_response = requests.get(
headers = {'Authorization': f'Bearer {jwt_token}'}
)
nonce_data = nonce_response.json()
noncets_hex = nonce_data['noncetsHex']
timestamp = nonce_data['timestamp']
# Example: { "noncetsHex": "A1B2C3D4E5F6...", "timestamp": "2026-05-04T10:09:00.000Z" }
# 2. Load your NEAR credentials
creds = json.load(f)
private_key_base58 = creds['private_key'].replace('ed25519:', '')
keypair = base58.b58decode(private_key_base58)
secret_key = keypair[:32]
# 3. Build message
recipient = 'MUNDO'
message = f'HOLA/{recipient}/{token_id}/{timestamp}/{noncets_hex}/API.IDENTYCLAW.COM/'
# 4. Canonicalize (UPPERCASE)
canonical_message = message.upper()
# 5. Sign
signing_key = SigningKey(secret_key)
signature = signing_key.sign(canonical_message.encode('utf-8')).signature
signature_b32 = base64.b32encode(signature).decode('utf-8').rstrip('=').upper()
# 6. Calculate checksum
checksum_prefix = f'{canonical_message}{signature_b32}/'
char_sum = sum(ord(c) for c in checksum_prefix)
hola_checksum_alphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ'
checksum = hola_checksum_alphabet[char_sum % 23]
# 7. Build final HOLA
hola = f'{canonical_message}{signature_b32}/{checksum}'
# Usage:
# result = generate_hola('bjbvcjzqbdsj', your_jwt)
# print('HOLA:', result['hola'])
```

**Key Points**:
- ✓ Fetches **fresh nonce** from API (not hardcoded)
- ✓ Uses **current timestamp** from nonce response
- ✓ **Uppercases** entire message before signing
- ✓ Returns complete HOLA ready to send
- ✓ All values are **generated fresh** each time

## Step 4: Send HOLA to Peer

Transmit the HOLA message to the peer agent via your communication channel (HTTP, WebSocket, etc.).

The peer must apply **full validation** before treating your HOLA as authenticated — either directly (on-chain + local crypto) or via `POST /api/identity/verify` when using the IdentyClaw HTTP path ([When is a HOLA validated?](#when-is-a-hola-validated)).

## Step 5: Verify HOLA (Peer Agent) — HTTP API path

This section documents **`POST /api/identity/verify`**, IdentyClaw's convenience implementation of full HOLA validation. If you verify peer-to-peer without the API, you must still apply the same substantive checks ([When is a HOLA validated?](#when-is-a-hola-validated)).

When using this endpoint: if you only parse the string, recompute the checksum, or verify the Ed25519 signature locally without completing the full proof bar, you have **not** finished validation. **Treat a received HOLA as unvalidated until `POST /api/identity/verify` returns a successful verification outcome** (or until equivalent direct verification succeeds).

**Endpoint**: `POST /api/identity/verify` (requires JWT)

```bash
# Use YOUR freshly generated HOLA, not this example
curl -X POST https://api.identyclaw.com/api/identity/verify \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  "hola": "HOLA/MUNDO/BJBVCJZQBDSJ/2026-05-04T10:09:00.000Z/A1B2C3D4.../API.IDENTYCLAW.COM/MFRGG.../J"
```

**Success Response Pattern**:
```json
{
  "verified": true,
  "peerTokenId": "bjbvcjzqbdsj",
  "destinatary": "MUNDO",
  "checks": {
    "tokenExists": true,
    "tokenActive": true,
    "timestampFresh": true,
    "nonceReplaySafe": true,
    "signatureValid": true,
    "checksumValid": true
  },
  "failureReasons": [],
  "signatureVerificationImplemented": true,
  "requestId": "01HX..."
}
```

## Verify Your HOLA Works

**Test Endpoint**: `POST /api/testhola` (requires JWT)

Use this endpoint to validate **your own** HOLA generation and iterate on mistakes before sending to peers. **Do not treat another agent’s HOLA as trusted because you ran equivalent local checks**—or because `/api/testhola` passed for your copy of their message—without completing [`POST /api/identity/verify`](#step-5-verify-hola-peer-agent--http-api-path) in the peer's trust workflow ([When is a HOLA validated?](#when-is-a-hola-validated)).

```bash
# Generate fresh HOLA using the pattern above, then test it:
curl -X POST https://api.identyclaw.com/api/testhola \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  "hola": "YOUR_FRESHLY_GENERATED_HOLA"
```

**Success Response** (200 OK):
```json
{
  "valid": true,
  "peerTokenId": "bjbvcjzqbdsj",
  "destinatary": "MUNDO",
  "peerVerified": true,
  "hola": "HOLA/MUNDO/...",
  "serverTokenId": "...",
  "checks": {
    "formatValid": true,
    "checksumValid": true,
    "timestampValid": true,
    "timestampFresh": true,
    "noncetsValid": true,
    "nonceReplaySafe": true,
    "tokenExists": true,
    "tokenActive": true,
    "signatureValid": true
  }
}
```

✓ **If you see `"valid": true` and all checks passing, your HOLA generation is working correctly!**

**Important**:
- Must use `Content-Type: application/json` header
- Must include valid JWT in Authorization header
- HOLA must be freshly generated (not from documentation examples)
- Server responds with its own HOLA in the `hola` field
- `/api/testhola` is JWT-protected as an API endpoint, but validation is based on the HOLA payload and cryptographic checks (not caller-token equality).
- A successful response here means **your** build of the HOLA is sound; it does **not** replace `POST /api/identity/verify` when deciding whether to trust **another agent’s** HOLA ([When is a HOLA validated?](#when-is-a-hola-validated))

## Common Pitfalls

❌ **Treating checksum / signature as “good enough” without `/api/identity/verify`**
- **Problem**: Accepting a peer’s HOLA for authorization after local checksum or Ed25519 verification only
- **Solution**: Treat inbound HOLAs as **unvalidated** until `POST /api/identity/verify` succeeds; local crypto checks are at most a development aid ([When is a HOLA validated?](#when-is-a-hola-validated))

❌ **Missing recipient field**
- **Problem**: Signing `HOLA/<tokenId>/...` without recipient
- **Solution**: Include recipient (default: `MUNDO`): `HOLA/MUNDO/<tokenId>/...`

❌ **Using wrong nonce**
- **Problem**: Using nonce from `/api/login/timestamp` (32 bytes) instead of `/api/holanonce16ts` (16 bytes)
- **Solution**: Always use `/api/holanonce16ts` for HOLA messages

❌ **Wrong checksum calculation**
- **Problem**: Using cryptographic hash instead of simple sum
- **Solution**: Sum UTF-16 code units (JavaScript `charCodeAt`) over `canonicalMessage + signature + "/"`, modulo 23, index into `ABCDEFGHJKMNPQRSTUVWXYZ`

❌ **Not uppercasing before signing**
- **Problem**: Signing the original mixed-case message instead of canonical uppercase
- **Solution**: Call `.toUpperCase()` on the entire message before signing

❌ **Missing trailing slash in checksum**
- **Problem**: Checksumming `canonicalMessage + signature` without the trailing `/`
- **Solution**: Include trailing slash: `checksumPrefix = canonicalMessage + signature + "/"`

❌ **Wrong signature encoding**
- **Problem**: Using base64url instead of **base32** for the HOLA line signature
- **Solution**: Use base32 (RFC 4648, A-Z2-7) for HOLA signatures

❌ **Expired nonce**
- **Problem**: Using nonce that's too old
- **Solution**: Request fresh nonce from `/api/holanonce16ts` before each HOLA

## Debugging HOLA Failures

### Step-by-Step Debugging Process

**1. Verify Canonicalization**
```json
console.log('Original:', message),
console.log('Canonical:', canonicalMessage),
console.log('Match:', message === canonicalMessage),
```

**2. Verify Signature Encoding**
```json
console.log('Signature length:', signatureB32.length),
console.log('Signature format valid:', /^[A-Z2-7]+$/.test(signatureB32)),
```

**3. Verify Checksum Calculation**
```javascript
const checksumPrefix = `${canonicalMessage}${signatureB32}/`;
const sum = 0;
sum += checksumPrefix.charCodeAt(i);
const holaChecksumAlphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ';
const expectedChecksum = holaChecksumAlphabet[sum % 23];
  console.log('Checksum prefix:', checksumPrefix)
  console.log('Sum:', sum)
  console.log('Expected:', expectedChecksum, 'Got:', checksum)
// Should match
```

### Common Error Patterns

| Error Code | Root Cause | Fix |
|------------|------------|-----|
| `HOLA_VALIDATION_FAILED` | Invalid format/payload/checksum | Check `error.details.stage` + `error.details.reasonCode` |
| `HOLA_VALIDATION_FAILED` + `nonce_replay` | Nonce reused within validity window | Request fresh nonce from `/api/holanonce16ts` for each HOLA |
| `HOLA_TIMESTAMP_INVALID` | HOLA line timestamp not valid ISO, or outside freshness window on `/api/testhola` | Use ISO from `GET /api/holanonce16ts` for that line; regenerate HOLA after a fresh nonce |
| `HOLA_SIGNATURE_INVALID` + `public_key_unavailable` | Public key unavailable from blockchain | Verify token owner key availability / RPC health |
| `HOLA_SIGNATURE_INVALID` + `signature_mismatch` | Wrong key pair or canonicalization/signing bug | Sign canonical uppercase message with correct owner key |
| `HOLA_SIGNATURE_INVALID` + `token_expired` | Passport expired (`not_after`) | Renew/reissue passport |
| `payload_is_json_object` | `hola` sent as JSON object instead of one string | Use `{"hola":"HOLA/MUNDO/..."}` only; keep envelope fields outside `hola` |
| `unix_millis_timestamp` | Timestamp field is raw Unix ms | Use ISO 8601 from `/api/holanonce16ts` |
| `signature_not_base32` | Signature uses base64url or other alphabet | HOLA line signature must be **base32** (not base64url) |
| `placeholder_signature` | Brackets or prose in signature slot | Sign canonical uppercase prefix; emit real base32 |

### Structured Failure Diagnostics (`/api/testhola`)

`/api/testhola` rejects with machine-readable details in `error.details`:

- `stage`: failing validation stage
- `reasonCode`: stable classifier for tests/automation

Typical values:
- `format_checksum_and_payload_validation` + `invalid_format` / `checksum_invalid`
- `timestamp_freshness_validation` + `timestamp_stale_or_future`
- `nonce_replay_validation` + `nonce_replay`
- `signature_verification` + `token_not_found` / `token_expired` / `public_key_unavailable` / `signature_mismatch` / `blockchain_unavailable_or_validation_error`

### Verification Result Diagnostics (`/api/identity/verify`)

`/api/identity/verify` always returns a verification outcome payload (HTTP 200 when request is well-formed), with:

- `verified`: overall decision
- `checks`: boolean stage results
- `failureReasons`: machine-readable reasons (e.g. `checksum_invalid`, `timestamp_stale_or_future`, `nonce_replay`, `token_missing`, `token_expired`, `signature_invalid`, `public_key_unavailable`, `public_key_error`)

## Next Steps

- [API Login Authentication](login-authentication.md)
- [Test with /api/testhola](https://api.identyclaw.com/docs)
- [Understand Passport metadata](token-metadata.md)
- [Explore API endpoints](api-reference.md)
- [View JSON-LD integration](jsonld-metadata.md)
