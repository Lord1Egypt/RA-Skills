# Subagent HOLA Protocol

Complete guide to the HOLA protocol for subagents using delegated authorization from parent agents.

## Table of Contents

- [Overview](#overview)
- [When is subagent HOLA validated?](#when-is-subagent-hola-validated)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Subagent HOLA Message Format](#subagent-hola-message-format)
- [Two-Signature Model](#two-signature-model)
- [Delegation Authorization](#delegation-authorization)
- [Step 1: Generate NEAR Account](#step-1-generate-near-account)
- [Step 2: Get JWT Token](#step-2-get-jwt-token)
- [Step 3: Parent Creates Delegation Authorization](#step-3-parent-creates-delegation-authorization)
- [Step 4: Request Nonce](#step-4-request-nonce)
- [Step 5: Construct Subagent HOLA](#step-5-construct-subagent-hola)
- [Step 6: Send HOLA to Peer](#step-6-send-hola-to-peer)
- [Step 7: Verify Subagent HOLA (Peer Agent)](#step-7-verify-subagent-hola-peer-agent)
- [Test Your Subagent HOLA](#test-your-subagent-hola)
- [Critical Encoding Notes](#critical-encoding-notes)
- [Common Pitfalls](#common-pitfalls)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Overview

Subagent HOLA is an extension of the standard HOLA protocol that includes delegation information. Unlike standard agents who sign HOLA messages with their own IdentyClaw Passport, subagents use a two-signature model:
1. **Delegation Authorization Signature** - Parent authorizes the subagent
2. **HOLA Message Signature** - Subagent signs the HOLA with their own key

This enables parent agents to delegate authentication authority to subagents while maintaining a verifiable trust chain.

### When is subagent HOLA validated?

Follow the same rule as [standard HOLA](hola-agent-authentication.md#when-is-a-hola-validated): **checksum or local signature verification alone does not mean the HOLA is validated.** For subagents you must also complete **delegation** checks.

**Full subagent validation** requires:

1. **HOLA proof bar** — same as standard HOLA (direct or via `POST /api/identity/verify`)
2. **Delegation authorization** — parent signed `{tokenId}:{delegateId}:{timestamp}:{publicKey}`; verify via direct cryptography against the parent's on-chain key **or** via `POST /api/isauthorizedsigner` (HTTP convenience path)

**When using the IdentyClaw HTTP path:** treat an inbound subagent HOLA as unvalidated until **both** HTTP checks succeed:

1. `POST /api/identity/verify` — full HOLA verification on the server  
2. `POST /api/isauthorizedsigner` — delegation authorization (see [Step 7](#step-7-verify-subagent-hola-peer-agent))

Until full validation succeeds (by either path), do not grant trust, access, or elevated behavior. `POST /api/testhola` does not verify delegation authorization and must not be treated as full validation of another agent's subagent HOLA.

Conceptual background: [`public/policies/why-identyclaw.md`](../public/policies/why-identyclaw.md) §8.1 and §11.

## When to Use

Use Subagent HOLA Protocol when you need to:
- Act as a subagent delegated by a parent agent
- Prove your identity with delegated authorization
- Implement hierarchical agent systems with controlled delegation
- Enable subagent-to-agent communication with parent vouching
- **You have delegation authorization from a parent agent**

## Prerequisites

Before using Subagent HOLA, you must:

1. **Have delegation authorization** - Parent agent must authorize your public key
2. **Generate your NEAR account** - Use `gennearaccount` (same as standard agents)
3. **Have a valid JWT token** - Complete API Login with your subagent account
4. **Know your delegateID** - From parent's delegation authorization
5. **Know parent's tokenId** - The parent's IdentyClaw Passport ID

## Subagent HOLA Message Format

**Structure**:
```
HOLA/<recipient>/<delegateID>/<issuer_tokenId>/<publicKey>/<ISO8601-timestamp>/<noncets-hex>/API.IDENTYCLAW.COM/<base32-signature>/<checksum>
```

**Components**:

| Field | Description | Example |
|-------|-------------|---------|
| `HOLA/` | Protocol identifier | `HOLA/` |
| `recipient` | Intended recipient (default: MUNDO) | `MUNDO` or `abcdefghijkl` |
| `delegateID` | Subagent ID from authorization (base64url hash or DID) | `aBcDeFgHiJkLmNoPqRsTuVwXyZ` |
| `issuer_tokenId` | Parent's Passport ID (12 lowercase letters) | `bkbvehbdcrgm` |
| `publicKey` | Subagent's Ed25519 public key (base32-encoded) | `N3FZ5KQ8LH2BSM1XY...` |
| `timestamp` | ISO 8601 timestamp | `2026-04-19T10:47:00.000Z` |
| `noncets-hex` | 32 uppercase hex characters (16 bytes) from `/api/holanonce16ts` | `4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE` |
| `API.IDENTYCLAW.COM` | Domain identifier | `API.IDENTYCLAW.COM` |
| `signature` | base32-encoded Ed25519 signature (RFC 4648, A-Z2-7, uppercase, no padding) | `MFRGG2LTMVZXGZLSN5XWC3TBNRQW4ZDJMQFA...` |
| `checksum` | Single letter from `ABCDEFGHJKMNPQRSTUVWXYZ` (23 letters; omits **I**, **L**, **O**) | `J` |

**Example Subagent HOLA Message**:
```
HOLA/MUNDO/aBcDeFgHiJkLmNoPqRsTuVwXyZ/bkbvehbdcrgm/N3FZ5KQ8LH2BSM1XY.../2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/dGVzdHNpZ25hdHVyZQ/a
```

Subagent HOLA uses the **same uppercase canonical signed payload and verifier normalization** as standard HOLA: sign and checksum the UTF-8 bytes of the prefix uppercased through `API.IDENTYCLAW.COM/`. **You do not need to transmit an all-uppercase line**; presentation on the wire is optional and stylistic choices that match your agent’s identity are welcome, as in standard HOLA. See [Canonical form vs on-the-wire appearance](hola-agent-authentication.md#canonical-form-vs-on-the-wire-appearance).

## Two-Signature Model

Subagents require two separate signatures for complete authentication:

### 1. Delegation Authorization Signature
- **Signed by**: Parent agent (Passport signing key)
- **Message**: `{tokenId}:{delegateID}:{unixTimestamp}:{publicKey}`
- **Verified via**: `POST /api/isauthorizedsigner`
- **Purpose**: Proves parent authorized this subagent

### 2. HOLA Message Signature
- **Signed by**: Subagent (using own private key from `~/.near-credentials`)
- **Message**: `HOLA/<recipient>/<delegateID>/<issuer_tokenId>/<publicKey>/<timestamp>/<noncets>/API.IDENTYCLAW.COM/`
- **Verified via**: `POST /api/identity/verify`
- **Purpose**: Proves subagent controls the authorized keypair

**Requirement**: Both signatures must be valid for complete subagent authentication.

## Delegation Authorization

Before generating HOLA messages, the parent must authorize the subagent.

### Authorization Message Format

```
{tokenId}:{delegateID}:{unixTimestamp}:{publicKey}
```

**Components**:
- `tokenId`: Parent's Passport ID (12 letters)
- `delegateID`: Subagent ID (DID, name, or BLAKE3 hash of metadata)
- `unixTimestamp`: When authorization was granted (Unix seconds)
- `publicKey`: Subagent Ed25519 public key (base64url-encoded)

### Subagent Metadata Template (for BLAKE3 hash)

When using BLAKE3 hash for `delegateID`, use this metadata structure:

```json
{
  "schema": "openclaw.identity_meta.v1",
  "context": "urn:openclaw:identity:2026",
  "id": "did:openclaw:subagent123:session456:msg789",
  "agent": {
    "did": "did:openclaw:subagent123",
    "publicKey": "base64url-encoded-subagent-public-key",
    "type": "subagent"
  },
  "metadata": {
    "expiresAt": "2027-12-31T23:59:59Z",
    "permissions": [
      "sign_hola",
      "read_data"
    ],
    "scope": "customer-service"
  }
}
```

### BLAKE3 Hash Function

```javascript
const { createHash } = require("blake3");

function toBase64Url(buffer) {
  return Buffer.from(buffer)
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

function canonicalize(value) {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return "[" + value.map(canonicalize).join(",") + "]";
  }
  const keys = Object.keys(value).sort();
  const entries = keys.map((key) => JSON.stringify(key) + ":" + canonicalize(value[key]));
  return "{" + entries.join(",") + "}";
}

function canonicalizeAndHash(metadataJson) {
  const canonicalJson = canonicalize(metadataJson);
  const hashBuffer = createHash().update(canonicalJson).digest();
  const hashOrDelegateId = toBase64Url(hashBuffer);
  return { canonicalJson, hashOrDelegateId };
}
```

**Notes**:
- Keep field names and value casing stable - any change produces a new hash
- Include stable identity fields in signed metadata so the delegation hash remains consistent across runs
- Parent signs: `{tokenId}:{hashOrDelegateId}:{unixTimestamp}:{publicKey}`

## Step 1: Generate NEAR Account

Subagent generates their own NEAR account using the same mechanism as standard agents. Store the resulting JSON on **non-volatile storage** with other secrets (see [`references/enrollment.md#near-credentials-storage-required`](enrollment.md#near-credentials-storage-required)).

```javascript
mkdir -p <credentials-dir> && chmod 700 <credentials-dir>;
gennearaccount <credentials-dir>;
// Back up credentials JSON to encrypted operator storage
```

This creates:
- 64-character hex account ID
- Ed25519 keypair stored at `<credentials-dir>/<accountid>.json` (default on persistent `$HOME`: `~/.near-credentials/mainnet/<accountid>.json`)

## Step 2: Get JWT Token

Authenticate with your subagent account to get a JWT token.

```bash
# 1. Get fresh one-time timestamp challenge
curl https://api.identyclaw.com/api/login/timestamp
# 2. Sign message: accountid + timestamp_iso
# 3. POST to login
curl -X POST https://api.identyclaw.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"accountid": "YOUR_SUBAGENT_ACCOUNTID", "timestamp": 1776622758, "base64url_signature": "..."}'
```

**Response**:
```json
{
  "jwt_token": "eyJhbGc...",
  "requestId": "01HQXYZ..."
}
```

## Step 3: Parent Creates Delegation Authorization

Parent agent creates the delegation signature offline (no API call required).

**Message to sign**:
```
{parentTokenId}:{delegateID}:{unixTimestamp}:{subagentPublicKey}
```

**Example**:
```javascript
const nacl = require('tweetnacl');
const bs58 = require('bs58');
// Parent's credentials
const parentPrivateKey = /* parent's Passport signing key */;
// Subagent's public key (base64url-encoded)
const subagentPublicKey = 'base64url-encoded-subagent-public-key';
// Authorization message
const message = `${parentTokenId}:${delegateID}:${unixTimestamp}:${subagentPublicKey}`;
// Sign with parent's key
const messageBytes = new TextEncoder().encode(message);
const signature = nacl.sign.detached(messageBytes, parentPrivateKey);
const signatureBase64url = Buffer.from(signature).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
// Store for subagent
const authorization = {
  tokenId: parentTokenId,
  delegateID: delegateID,
  unixTimestamp: unixTimestamp,
  publicKey: subagentPublicKey,
  signature: signatureBase64url
};
```

Parent provides this authorization to the subagent.

## Step 4: Request Nonce

⚠️ **CRITICAL: Which Key Pair to Use**

You must use the private key of the **subagent's NEAR account** (not the parent's key).

**Key Requirements**:
1. Use the private key of the **subagent's NEAR account**
2. Private key location: `~/.near-credentials/mainnet/<subagent_accountid>.json`
3. The parent's key is only used for delegation authorization

---

**Endpoint**: `GET /api/holanonce16ts` (requires JWT)

```bash
curl https://api.identyclaw.com/api/holanonce16ts \
  -H "Authorization: Bearer YOUR_SUBAGENT_JWT"
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

## Step 5: Construct Subagent HOLA

**Message to sign** (everything before the signature field):
```
HOLA/<recipient>/<delegateID>/<issuer_tokenId>/<publicKey>/<timestamp>/<noncets-hex>/API.IDENTYCLAW.COM/
```

**Reference (IdentyClaw) — wire format** (your values will differ):
```
HOLA/MUNDO/aBcDeFgHiJkLmNoPqRsTuVwXyZ/bkbvehbdcrgm/N3FZ5KQ8LH2BSM1XY.../2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/
```

### Step 5.1: Canonicalization (CRITICAL)

**Before signing, convert ALL components to UPPERCASE:**

⚠️ **This is the most common source of HOLA signature failures.**

**Components to uppercase**:
1. **recipient** → `MUNDO` (already uppercase)
2. **delegateID** → `ABCDEF...` (uppercase the base64url string)
3. **issuer_tokenId** → `BKBVEHBDCRGM` (even though stored as lowercase)
4. **publicKey** → `N3FZ5KQ8LH2BSM1XY...` (uppercase the base32 string)
5. **timestamp** → `2026-04-19T10:47:00.000Z` (verify 'Z' is uppercase)
6. **noncetsHex** → `4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE` (already uppercase from API)
7. **domain** → `API.IDENTYCLAW.COM` (already uppercase)

**Reference (IdentyClaw) — wire format**:
```javascript
// Original message components (use YOUR fresh values)
const recipient = 'MUNDO';
const delegateID = 'aBcDeFgHiJkLmNoPqRsTuVwXyZ';  // From authorization;
const issuerTokenId = 'bkbvehbdcrgm';  // Parent's passport ID;
const publicKey = 'n3fz5kq8lh2bsm1xy...';  // Your public key (base32);
const timestamp = '2026-04-19T10:47:00.000Z';  // From Step 4;
const noncetsHex = '4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE';  // From Step 4;
// Build message
const message = `HOLA/${recipient}/${delegateID}/${issuerTokenId}/${publicKey}/${timestamp}/${noncetsHex}/API.IDENTYCLAW.COM/`;
// Canonicalize: UPPERCASE EVERYTHING
const canonicalMessage = message.toUpperCase();
// Sign the canonical message
const messageBytes = new TextEncoder().encode(canonicalMessage);
const signature = nacl.sign.detached(messageBytes, subagentSecretKey);
```

### Step 5.2: Sign the Canonical Message

**Signing**:
1. Convert **canonical (uppercase)** message to UTF-8 bytes
2. Sign with **subagent's** Ed25519 secret key (from `~/.near-credentials`)
3. Encode signature as **base32** (RFC 4648, A-Z2-7, uppercase, no padding)

**Reference (IdentyClaw) — JavaScript wire format**:
```javascript
const nacl = require('tweetnacl');
const base32 = require('hi-base32');
const bs58 = require('bs58');
const fs = require('fs');
// 1. Load subagent credentials
const creds = JSON.parse(fs.readFileSync('~/.near-credentials/mainnet/subagent-account.json'));
const privateKeyBase58 = creds.private_key.replace('ed25519:', '');
// 2. Decode keypair
const keypair = bs58.decode(privateKeyBase58);
const secretKey = keypair.slice(0, 32);
// 3. Build and canonicalize message (use YOUR fresh values)
const message = `HOLA/MUNDO/aBcDeFgHiJkLmNoPqRsTuVwXyZ/bkbvehbdcrgm/N3FZ5KQ8LH2BSM1XY.../2026-04-19T10:47:00.000Z/4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE/API.IDENTYCLAW.COM/`;
const canonicalMessage = message.toUpperCase();
// 4. Sign the canonical message
const messageBytes = new TextEncoder().encode(canonicalMessage);
const signature = nacl.sign.detached(messageBytes, secretKey);
// 5. Encode as base32 (RFC 4648: A-Z2-7, uppercase, no padding)
const signatureB32 = base32.encode(Buffer.from(signature)).replace(/=+$/, '').toUpperCase();
```

### Step 5.3: Checksum Calculation

**Algorithm**: `checksumPrefix = canonicalUppercaseThroughApiDotCom + base32Signature + '/'`; `checksum = ABCDEFGHJKMNPQRSTUVWXYZ[(sum of UTF-16 code units over checksumPrefix) % 23]`.

The checksum is calculated on the **canonicalized (uppercase) message + signature + trailing slash**.

```javascript
// Step 1: Build canonical message (already uppercase)
const canonicalMessage = message.toUpperCase();
// Step 2: Add signature and trailing slash
const checksumPrefix = `${canonicalMessage}${signatureB32}/`;
// Step 3: Sum ASCII character codes
const sum = 0;
sum += checksumPrefix.charCodeAt(i);
// Step 4: Modulo 16 and convert to hex
const holaChecksumAlphabet = 'ABCDEFGHJKMNPQRSTUVWXYZ';
const checksum = holaChecksumAlphabet[sum % 23];
```

**Final Subagent HOLA Pattern**:
```
HOLA/MUNDO/ABCDEF.../BKBVEHBDCRGM/N3FZ5KQ8LH2BSM1XY.../2026-04-19T10:47:00.000Z/4F9A3C7E.../API.IDENTYCLAW.COM/MFRGG2LTMVZXGZLSN5XWC3TBNRQW4ZDJMQFA.../F
```

## Step 6: Send HOLA to Peer

Transmit the subagent HOLA message to the peer agent via your communication channel (HTTP, WebSocket, etc.).

The peer agent will verify your HOLA using both `/api/identity/verify` and `/api/isauthorizedsigner`. **Neither you nor the peer should treat the message as validated until those server calls succeed** ([When is subagent HOLA validated?](#when-is-subagent-hola-validated)).

## Step 7: Verify Subagent HOLA (Peer Agent)

Peer agent must verify both signatures to establish trust. **Local checksum or HOLA signature checks are not sufficient**—full validation requires the API steps below ([When is subagent HOLA validated?](#when-is-subagent-hola-validated)).

### Step 7.1: Verify HOLA Signature

**Endpoint**: `POST /api/identity/verify` (requires JWT)

```bash
curl -X POST https://api.identyclaw.com/api/identity/verify \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  "hola": "HOLA/MUNDO/ABCDEF.../BKBVEHBDCRGM/N3FZ5KQ8LH2BSM1XY.../2026-04-19T10:47:00.000Z/4F9A3C7E.../API.IDENTYCLAW.COM/MFRGG.../F"
```

**Success Response Pattern**:
```json
{
  "verified": true,
  "peerTokenId": "delegateID",
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
  "requestId": "01HX..."
}
```

### Step 7.2: Verify Delegation Authorization

**Endpoint**: `POST /api/isauthorizedsigner` (requires JWT)

```bash
curl -X POST https://api.identyclaw.com/api/isauthorizedsigner \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  "tokenId": "bkbvehbdcrgm", \
  "hashOrDelegateId": "aBcDeFgHiJkLmNoPqRsTuVwXyZ", \
  "unixTimestamp": 1714143000, \
  "publicKey": "base64url-encoded-subagent-public-key", \
  "signature": "parent-authorization-signature"
```

**Success Response Pattern**:
```json
{
  "authorized": true,
  "checks": {
    "signatureValid": true,
    "timestampValid": true,
    "publicKeyMatch": true
  },
  "requestId": "01HX..."
}
```

Both verifications must pass for complete subagent authentication.

## Test Your Subagent HOLA

**Test Endpoint**: `POST /api/testhola` (requires JWT)

Use this endpoint to validate **your own** subagent HOLA generation before sending to peers. It does **not** check delegation authorization and does **not** replace `POST /api/identity/verify` plus `POST /api/isauthorizedsigner` when deciding whether to trust **another agent’s** subagent HOLA ([When is subagent HOLA validated?](#when-is-subagent-hola-validated)).

```bash
# Generate fresh subagent HOLA using the pattern above, then test it:
curl -X POST https://api.identyclaw.com/api/testhola \
  -H "Authorization: Bearer YOUR_SUBAGENT_JWT" \
  -H "Content-Type: application/json" \
  "hola": "YOUR_FRESHLY_GENERATED_SUBAGENT_HOLA"
```

**Note**: Authenticate with a valid JWT to call `/api/testhola`. Validation outcomes are based on HOLA fields and cryptographic checks, not enforced JWT sender-token matching.

**Success Response** (200 OK):
```json
{
  "valid": true,
  "peerTokenId": "delegateID",
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

**Note**: `/api/testhola` validates format, signature, and checksum but does NOT verify delegation authorization - use `/api/isauthorizedsigner` separately for that.

## Critical Encoding Notes

**Canonical vs wire (case):** Subagent HOLA follows the same rules as standard HOLA: verifiers normalize casing when reconstructing the signed prefix. Capitalization on the wire is **not** required; creative presentation is welcome. Cryptography must still use the uppercase canonical body through `API.IDENTYCLAW.COM/`. Details: [Canonical form vs on-the-wire appearance](hola-agent-authentication.md#canonical-form-vs-on-the-wire-appearance).

Different endpoints use different encodings:

- **HOLA signatures**: Always **base32** (RFC 4648 Base32: A-Z2-7, uppercase, no padding)
- **Subagent public key in HOLA**: **base32** (52 characters, no padding)
- **Delegation public key in authorization**: **base64url** (for `/api/isauthorizedsigner` endpoint)
- **Login signatures**: **base64url** (for `/api/login` endpoint)

**Encoding Summary**:
| Context | Encoding | Purpose |
|---------|----------|---------|
| HOLA message signature | base32 | Ed25519 signature in HOLA protocol |
| Public key in HOLA | base32 | Subagent public key in HOLA message |
| Delegation signature | base64url | Parent signature for authorization |
| Public key in authorization | base64url | Subagent public key for `/api/isauthorizedsigner` |
| API login signature | base64url | Signature for `/api/login` |

## Common Pitfalls

❌ **Trusting checksum / local signature without `/api/identity/verify` (and delegation)**
- **Problem**: Accepting a subagent HOLA after offline checks only
- **Solution**: Treat as **unvalidated** until `POST /api/identity/verify` **and** `POST /api/isauthorizedsigner` both succeed ([When is subagent HOLA validated?](#when-is-subagent-hola-validated))

❌ **Wrong signature key**
- **Problem**: Subagent signs HOLA with parent's key instead of own key
- **Solution**: Use subagent's private key from `~/.near-credentials/mainnet/<subagent-account>.json`

❌ **Wrong HOLA format**
- **Problem**: Using standard agent HOLA format (8 fields) instead of subagent format (11 fields)
- **Solution**: Subagent format has 3 extra fields: `delegateID`, `issuer_tokenId`, `publicKey`

❌ **Encoding confusion**
- **Problem**: Using base64url instead of base32 for HOLA signature
- **Solution**: HOLA signatures always use base32 (A-Z2-7, uppercase, no padding)

❌ **Missing delegation verification**
- **Problem**: Only verifying HOLA signature, not delegation authorization
- **Solution**: Peer must call both `/api/identity/verify` and `/api/isauthorizedsigner`

❌ **Reused nonce**
- **Problem**: Using stale nonce from previous HOLA
- **Solution**: Request fresh nonce from `/api/holanonce16ts` for each HOLA

## Troubleshooting

### signature_invalid (subagent HOLA)
**Cause**: Subagent signed with wrong key (parent's instead of own)

**Solutions**:
- Verify subagent uses its OWN private key for HOLA signature
- Parent's key is only used for delegation signature (`/api/isauthorizedsigner`)
- Check signed message format matches subagent format exactly

### HOLA_VALIDATION_FAILED (wrong field count / format)
**Cause**: Wrong number of fields in HOLA message (`error.details.reasonCode` often reflects format parsing)

**Solutions**:
- Subagent format: 11 fields total (3 extra: delegateID, issuer_tokenId, publicKey)
- Count separators `/` - should be 10 for subagent
- Verify field order matches specification exactly

### HOLA_VALIDATION_FAILED (delegate id)
**Cause**: delegateID is missing or wrong length

**Solutions**:
- delegateID must be 1-128 characters
- Use descriptive IDs: `'researcher-sub-001'` not `'abc'`
- delegateID must match what was used in `/api/isauthorizedsigner`

### subagent_public_key_invalid_length
**Cause**: Public key in HOLA is not 32 bytes when decoded

**Solutions**:
- Public key must be base32-encoded Ed25519 key (32 bytes)
- Encoded length should be 52 characters (no padding)
- Verify decoded length is exactly 32 bytes

### publicKeyAuthorizationFailed (/api/isauthorizedsigner)
**Cause**: Parent signature is invalid or timestamp mismatch

**Solutions**:
- Verify parent signed correct message: `tokenId:delegateId:timestamp:publicKey`
- Ensure timestamp matches delegation record exactly
- Check parent's private key is correct
- Verify signature is base64url-encoded (no padding)

## Next Steps

- [Standard Agent HOLA](hola-agent-authentication.md) - For non-delegated agent authentication
- [Subagent HOLA guide](hola-subagent-authentication.md) and [holanonce API](holanonce-api.md) — delegation + nonce response
- [API Login Authentication](login-authentication.md) - How to get JWT tokens
- [Test with /api/testhola](https://api.identyclaw.com/docs) - Interactive API testing
- [Explore API endpoints](api-reference.md) - Complete API reference
