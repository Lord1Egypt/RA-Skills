# API Login Authentication

Complete guide to authenticating with the IdentyClaw API server to obtain JWT tokens.

## Table of Contents

- [Quick Start: Login Pattern](#quick-start-login-pattern)
- [Overview](#overview)
- [Vocabulary (API login)](#vocabulary-api-login)
- [When to Use](#when-to-use)
- [Understanding ID vs Account](#understanding-id-vs-account)
- [Key Rotation](#key-rotation)
- [Authentication Flow](#authentication-flow)
- [Verify the API server (MITM protection)](#verify-the-api-server-mitm-protection)
- [Step 1: Get Consistent Timestamp](#step-1-get-consistent-timestamp)
- [Step 2: Sign the Message](#step-2-sign-the-message)
- [Step 3: POST /api/login](#step-3-post-apilogin)
- [Complete Pattern Example](#complete-pattern-example)
- [Step 4: Use JWT Token](#step-4-use-jwt-token)
- [Agent harnesses (OpenClaw, Cursor, shell agents)](#agent-harnesses-openclaw-cursor-shell-agents)
- [Verify Your Login Works](#verify-your-login-works)
- [Machine-readable login errors](#machine-readable-login-errors)
- [Common Pitfalls](#common-pitfalls)
- [Next Steps](#next-steps)

## Quick Start: Login Pattern

**Reference (IdentyClaw)** — API `https://api.identyclaw.com`. Proven wire format (also exercised by the deployment test suite in **clienttest-idc** via direct `fetch`/`curl`): challenge → sign locally → `POST /api/login` → Bearer JWT on protected routes. **No client-side NEAR RPC is required** for this path—you only sign with your NEAR/Passport key and call HTTP.

### Complete Flow Pattern (curl)

```bash
# 1. One-time challenge (use both fields from the same response)
curl -sS https://api.identyclaw.com/api/login/timestamp

# 2. Sign UTF-8 bytes of: <accountid or roditid> + <timestamp_iso> (no separator)
#    → base64url_signature (see Steps 1–2 below)

# 3. Exchange signature for JWT (send exactly one timestamp field)
curl -sS -X POST https://api.identyclaw.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"accountid":"<64-char-hex>","timestamp":1776622758,"base64url_signature":"<sig>"}'

# 4. Protected call
JWT="<jwt_token from step 3>"
curl -sS https://api.identyclaw.com/api/me/identity \
  -H "Authorization: Bearer ${JWT}"
```

**⚠️ CRITICAL:** Fetch a fresh `GET /api/login/timestamp` pair immediately before each login attempt; use it once, then discard.

**Optional — `@rodit/rodit-auth-be`:** `RoditClient.login_server()` also validates the **API server's** on-chain Passport before returning a JWT. That adds **NEAR RPC** load and dependency on RPC bandwidth/latency on the agent host. Use it when MITM protection outweighs that cost; otherwise curl login above is sufficient for most agents. See [Verify the API server (MITM protection)](#verify-the-api-server-mitm-protection).

**Key Points**:
- ✓ Fetch **fresh timestamp** from API for each login attempt
- ✓ Sign with **timestamp_iso** (ISO string from the API response)
- ✓ Send exactly one timestamp field in POST payload: **timestamp** (Unix seconds) or **timestamp_iso**
- ✓ Concatenate **accountid + timestamp_iso** with no separator for signing
- ✓ Encode signature as **base64url** (not standard base64)
- ✓ Response field is **jwt_token** (not `token`)
- ✓ JWT expires in 1 hour - request new token when needed
- ✓ Treat each timestamp pair as **single-use** for one login attempt only

**Note on Login Methods**: The API supports two login identifiers:
- **accountid**: 64-character lowercase hex NEAR implicit account ID (for enrollment)
- **roditid**: 12-letter on-chain token_id (for direct IdentyClaw Passport login)
Choose the appropriate identifier based on your use case.

## Timestamp Handling Checklist

**Do**:
- Fetch `GET /api/login/timestamp` immediately before signing
- Use `timestamp_iso` for **signing** the message
- Send exactly one timestamp field in the POST payload: `timestamp` (Unix seconds) or `timestamp_iso`
- On any failed `POST /api/login`, fetch a **new** timestamp pair before retry

**Implementation checklist**:
- Fetch a new timestamp pair immediately before signing each attempt
- Keep timestamp pairs in request-local scope and discard them after the attempt
- Use `timestamp` and `timestamp_iso` from the same response object
- Send `timestamp` in the POST payload (or omit it and use server default)

## Overview

API Login is the authentication mechanism for accessing protected IdentyClaw API endpoints. It provides a JWT token that authorizes your requests to the server.

## Vocabulary (API login)

This guide uses the following terms consistently. **HTTP request and response fields are unchanged** — see [API Reference](api-reference.md) and OpenAPI (for example `accountid`, `timestamp`, `base64url_signature`, `jwt_token` on `POST /api/login`).

| Term | Meaning |
| --- | --- |
| **Login challenge pair** | `timestamp` and `timestamp_iso` from `GET /api/login/timestamp`, used together once per login attempt |
| **Login signing payload** | Concatenation `accountid` + `timestamp_iso` (no separator), UTF-8 bytes you sign for login |
| **base64url login signature** | Ed25519 signature over the login signing payload, encoded for `base64url_signature` |
| **JWT** / **API bearer token** | Session credential returned by `POST /api/login` (`jwt_token`) |
| **API error code (login lane)** | Machine-readable classifier for JWT login failures — see [Machine-readable login errors](#machine-readable-login-errors) (`error.code`; legacy shape may use top-level string `error`) |

## When to Use

Use API Login when you need to:

- Access protected API endpoints
- Get your own identity (`/api/me/identity`)
- Request nonces for HOLA protocol (`GET /api/holanonce16ts` → JSON `noncetsHex`, `timestamp` — see [holanonce-api.md](holanonce-api.md); not `timestamp_iso`)
- Verify HOLA messages from other agents
- **This is your FIRST step** - you need a JWT before doing anything else

For inter-agent HOLA lines and tooling, see [HOLA Protocol](hola-agent-authentication.md).

## Understanding ID vs Account

Think of your **IdentyClaw Passport as your passport** and your **NEAR account as your wallet**:

- **Your Passport (Passport ID)**: Your unique 12-letter identity (e.g., `bkbvehbdcrgm`) that proves who you are. This is what you show to others. IdentyClaw Passports are implemented as on-chain credentials on the NEAR blockchain.
- **Your Wallet (NEAR Account)**: The account that owns and controls your passport (e.g., `alice.near`). This is what holds your private keys and signs on your behalf.

When you authenticate, you're using your wallet's private key to prove you own your passport.

## Key Rotation

Key rotation is seamless and requires **no coordination between clients and servers**. IdentyClaw does not maintain a separate key registry — ownership is determined on-chain. **You choose the rotation frequency**; there is no platform-mandated schedule.

**To rotate signing keys:**

1. Create a new NEAR wallet.
2. Fund the new wallet on-chain.
3. Transfer your IdentyClaw Passport with **`near-cli-rs`**, calling the contract method **`rodit_transfer`** (this is not a standard NEAR `nft_transfer`).
4. Point login and HOLA tooling at the new wallet credentials.

Your Passport ID (12-letter token id) is unchanged. After the transfer, the API and peers accept the new key automatically because they verify current on-chain ownership.

See [key-rotation.md](key-rotation.md) for the full security guidance, `near-cli-rs` command, and contract interface.

## Authentication Flow

```
1. GET /api/login/timestamp → {timestamp, timestamp_iso}
2. Sign message: accountid + timestamp_iso
3. POST /api/login → {jwt_token: "eyJhbGc..."}
4. Use JWT in Authorization header for protected endpoints
```

## Verify the API Server (MITM Protection)

### The threat

TLS protects the channel, but it does **not** by itself prove that responses came from the **real** IdentyClaw API. An attacker could:

- **Man-in-the-middle** your connection and return forged JWTs or API payloads
- Run a **look-alike server** at a similar hostname that accepts valid login signatures but serves untrustworthy results (for example on `POST /api/identity/verify`)

If you log in with raw `fetch` or `curl` and accept any `jwt_token` from the response, you have proved **your** Passport to whatever endpoint answered—you have **not** proved that endpoint **is** IdentyClaw.

### Default for agents: curl / HTTP login

Most agents should use the [Quick Start](#quick-start-login-pattern) curl flow:

- You authenticate **to** the server (login signature).
- You do **not** need a working NEAR RPC on the agent machine for login.
- Mitigations without RPC: pin the API hostname (`https://api.identyclaw.com` or your deployment URL), use TLS, and cross-check high-value results (canonical `tokenId` on official channels—see [finding-agents.md](finding-agents.md)).

This matches how **clienttest-idc** exercises public and many authenticated endpoints with direct HTTP (`fetch`/`curl`); the SDK is used there mainly where the test constitution requires it, not for every agent integration.

### Optional: client-side server Passport validation (`@rodit/rodit-auth-be`)

Login can be **mutual**: after `POST /api/login`, a client may validate the returned JWT against the **server's** on-chain Passport before trusting it.

| Direction | Who is verified | curl login | SDK `login_server()` |
| --- | --- | --- | --- |
| **Server → client** | Your Passport | ✓ (server validates your signature) | ✓ |
| **Client → server** | The API server's Passport | ✗ (you trust TLS + hostname) | ✓ (loads server Passport via **NEAR RPC**) |

**Tradeoff:** `RoditClient.login_server()` (and `client.request()`) call NEAR RPC to load and validate the server Passport. Agents on constrained networks, rate-limited RPC, or minimal shells may find that **slower or less reliable than curl alone**. Use the SDK when you explicitly need client→server Passport validation and can provision RPC with enough bandwidth.

```javascript
const { RoditClient } = require("@rodit/rodit-auth-be");

const client = await RoditClient.create("client");
const { jwt_token } = await client.login_server();
// Throws if server JWT / on-chain Passport validation fails
```

`RoditClient.login_server()` POSTs your signed credentials, then **before returning a session**:

1. Decodes the JWT to read the server's on-chain Passport id (`rodit_id` claim)
2. Loads that server Passport from NEAR (**RPC required**)
3. Validates the JWT cryptographically against that Passport (signature, expiry, session state, family, and trust rules)

If the endpoint is an impostor or misconfigured proxy, validation fails with explicit **`[SERVER REJECTED]`** errors, including:

| Error code | Meaning |
| --- | --- |
| `SERVER_RODIT_FAMILY_MISMATCH` | Server Passport is not in the expected IdentyClaw family |
| `SERVER_RODIT_NOT_LIVE` | Server Passport is expired or not yet active |
| `SERVER_RODIT_REVOKED` | Server Passport has been revoked |
| `SERVER_SMART_CONTRACT_NOT_TRUSTED` | Server Passport was not issued by a trusted contract |
| `SERVER_TOKEN_IDENTITY_MISMATCH` | JWT server identity does not match the on-chain record |

For outbound webhooks from IdentyClaw to your agent, webhook signature verification (SDK `verifyWebhookSignature()` / `getWebhookHandler()`) is separate from login—only needed if you accept server-pushed events.

Install (optional): `npm install @rodit/rodit-auth-be@9.10.6`. Wire-format login in this guide does **not** require the package.

## Step 1: Get Consistent Timestamp

**Endpoint**: `GET /api/login/timestamp` (public, no auth required)

```bash
curl https://api.identyclaw.com/api/login/timestamp
```

**Response Pattern** (values shown are illustrative only):
```json
{
  "timestamp": 1776622758,
  "timestamp_iso": "2026-04-19T18:19:18.000Z",
  "requestId": "01HQXYZ..."
}
```

**⚠️ CRITICAL - Timestamp Consistency**:
- `timestamp` and `timestamp_iso` are generated from the **same moment**
- Use **timestamp_iso** when signing your message (Step 2)
- Send exactly one timestamp field in the login payload (Step 3): `timestamp` or `timestamp_iso`
- Fetch the timestamp pair from this endpoint and sign exactly what the endpoint returns
- Timestamps are valid for a short window (~5 minutes)
- Treat each pair as a one-time challenge for one login attempt

## Step 2: Sign the Message

**Message to sign** (UTF-8 bytes):
```
accountid + timestamp_iso
```

**Reference (IdentyClaw) — wire format** (use your fresh values from Step 1):
- Account ID: `43d3c5b5e77a46b52933bc7a8b79b06f16dd4ca3cfbacd0e6fede0e7e01782ac`
- timestamp_iso: `2026-04-19T18:19:18.000Z` (from Step 1 response)
- **Message**: `43d3c5b5e77a46b52933bc7a8b79b06f16dd4ca3cfbacd0e6fede0e7e01782ac2026-04-19T18:19:18.000Z` (no separators, literal concatenation)

⚠️ Use the **fresh timestamp_iso** from Step 1, not values from this example.

**Signing Steps**:

1. Extract your NEAR private key from credentials file
2. Decode from base58 to get 64-byte keypair
3. Extract first 32 bytes (secret key)
4. Sign message with Ed25519
5. Encode signature as base64url (URL-safe base64: `-` and `_` instead of `+` and `/`, no padding `=`)

**Reference (IdentyClaw) — JavaScript wire format** (use your fresh values):

```javascript
const nacl = require('tweetnacl');
const bs58 = require('bs58');
const fs = require('fs');
// 1. Load credentials
const creds = JSON.parse(fs.readFileSync('~/.near-credentials/mainnet/your-account.json'));
const privateKeyBase58 = creds.private_key.replace('ed25519:', '');
// 2. Decode keypair
const keypair = bs58.decode(privateKeyBase58);
const secretKey = keypair.slice(0, 32);
// 3. Sign message (use YOUR fresh timestamp_iso from Step 1)
const message = '43d3c5b5e77a46b52933bc7a8b79b06f16dd4ca3cfbacd0e6fede0e7e01782ac2026-04-19T18:19:18.000Z';
const messageBytes = Buffer.from(message, 'utf8');
const signature = nacl.sign.detached(messageBytes, secretKey);
// 4. Encode as base64url (URL-safe: - and _ instead of + and /)
const base64url = Buffer.from(signature).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
// Example result: "xK7vR3mN9pQ2wL8hF5jT6cY1sD4eU0iO..." (yours will differ)
console.log(base64url);
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
# 3. Sign message (use YOUR fresh timestamp_iso from Step 1)
signing_key = SigningKey(secret_key)
message = b'43d3c5b5e77a46b52933bc7a8b79b06f16dd4ca3cfbacd0e6fede0e7e01782ac2026-04-19T18:19:18.000Z'
signature = signing_key.sign(message).signature
# 4. Encode as base64url (URL-safe: - and _ instead of + and /)
base64url = base64.b64encode(signature).decode('utf-8').replace('+', '-').replace('/', '_').replace('=', '')
# Example result: "xK7vR3mN9pQ2wL8hF5jT6cY1sD4eU0iO..." (yours will differ)
print(base64url)
```

## Step 3: POST /api/login

**Endpoint**: `POST /api/login` (public, no auth required)

**Request Pattern** (use your fresh values):
```bash
curl -sS -X POST https://api.identyclaw.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"accountid":"43d3c5b5e77a46b52933bc7a8b79b06f16dd4ca3cfbacd0e6fede0e7e01782ac","timestamp":1776622758,"base64url_signature":"YOUR_BASE64URL_SIGNATURE"}'
```

For **roditid** login (12-letter Passport ID), use `roditid` and `roditid_base64url_signature` instead—same signing rule: `roditid + timestamp_iso` (see **clienttest-idc** `security.js` and `authentication-comprehensive.js` for `fetch` examples).

**Note**: `POST /api/login` requires timestamp information from the same `GET /api/login/timestamp` challenge pair used for signing. Send exactly one of `timestamp` (Unix seconds) or `timestamp_iso` (canonical ISO string). Do not send both fields.

**Success Response Pattern**:
```json
{
  "jwt_token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
  "requestId": "01HQXYZ..."
}
```

**Important**:
- `accountid`: Your 64-character lowercase hex NEAR implicit account ID (or use `roditid` for 12-letter token_id)
- `timestamp`: Unix seconds from Step 1 (or provide `timestamp_iso` instead, but not both)
- `base64url_signature`: URL-safe base64 from Step 2
- Response field is `jwt_token` (not `token`)
- JWT expires in 3600 seconds (1 hour)
- If login fails, discard this timestamp pair and start again from Step 1

### Retry Pattern (Correct)

**Reference (IdentyClaw)** — fetch a new timestamp pair on each failed attempt; do not reuse a consumed challenge.

```javascript
async function loginWithFreshTimestampRetry(accountId, signAndLogin, maxAttempts = 2) {
  let lastError;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const tsResp = await fetch("https://api.identyclaw.com/api/login/timestamp");
    const { timestamp, timestamp_iso } = await tsResp.json();
    const base64url_signature = await signAndLogin(accountId, timestamp_iso);
    const loginResp = await fetch("https://api.identyclaw.com/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ accountid: accountId, timestamp, base64url_signature }),
    });
    if (loginResp.ok) {
      return loginResp.json();
    }
    lastError = await loginResp.text();
  }
  throw new Error(`Login failed after retries: ${lastError}`);
}
```

## Complete Pattern Example

**Reference (IdentyClaw)** — end-to-end curl (no client-side NEAR RPC):

```bash
TS_JSON="$(curl -sS https://api.identyclaw.com/api/login/timestamp)"
TIMESTAMP="$(printf '%s' "$TS_JSON" | jq -r .timestamp)"
TIMESTAMP_ISO="$(printf '%s' "$TS_JSON" | jq -r .timestamp_iso)"
# SIG="$(sign_accountid_timestamp_iso "$ACCOUNTID" "$TIMESTAMP_ISO")"  # your local signer

LOGIN_JSON="$(curl -sS -X POST https://api.identyclaw.com/api/login \
  -H "Content-Type: application/json" \
  -d "{\"accountid\":\"${ACCOUNTID}\",\"timestamp\":${TIMESTAMP},\"base64url_signature\":\"${SIG}\"}")"
JWT="$(printf '%s' "$LOGIN_JSON" | jq -r .jwt_token)"

curl -sS https://api.identyclaw.com/api/me/identity \
  -H "Authorization: Bearer ${JWT}"
```

Signing (Step 2) is local Ed25519 over `accountid + timestamp_iso`; see [Step 2](#step-2-sign-the-message). Optional SDK path: [Optional: client-side server Passport validation](#optional-client-side-server-passport-validation-roditrodit-auth-be).

**Key Points**:
- ✓ Fetches **fresh timestamp** from API (not generated locally)
- ✓ Uses **timestamp_iso** from the response for signing
- ✓ Signs with **timestamp_iso** (ISO string)
- ✓ Sends exactly one timestamp field in payload (`timestamp` or `timestamp_iso`)
- ✓ Returns JWT ready to use
- ✓ All values are **generated fresh** each time

## Step 4: Use JWT Token

Include JWT in `Authorization` header for protected endpoints:

```bash
# Use YOUR freshly obtained JWT token
curl https://api.identyclaw.com/api/me/identity \
  -H "Authorization: Bearer eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9..."
```

**Common Protected Endpoints**:
- `GET /api/me/identity` - Get your passport information
- `GET /api/holanonce16ts` - HOLA nonce; response JSON: `noncetsHex`, `timestamp`, `length`, `algorithm`, `requestId` ([holanonce-api.md](holanonce-api.md))
- `POST /api/identity/verify` - Verify HOLA messages from peers
- `POST /api/testhola` - Test your HOLA generation

## Agent harnesses (OpenClaw, Cursor, shell agents)

AI agent runtimes often **redact** `jwt_token` in tool output (for example `eyJhbG…ISDw`). Using that fragment in a later `Authorization: Bearer …` header produces `401 INVALIDATED_TOKEN` with `details.reason: invalid_jwt_format` even when `POST /api/login` returned **200**.

Before debugging server session state, verify the bearer token on the client: length ~1500–2000 characters, three dot-separated segments, field name **`jwt_token`**.

Store and reuse the full JWT on the **agent machine** (SDK, local plugin, or file)—not inline in chat or curl the model can see. Complete client-side patterns: [`mcp-auth-tools.md`](mcp-auth-tools.md) (`doc:reference:mcp-auth-tools`). Machine-readable diagnosis: `guide:troubleshooting`.

## Verify Your Login Works

**Test Endpoint**: `GET /api/me/identity` (requires JWT)

Use this endpoint to validate your login was successful.

```bash
# Use YOUR freshly obtained JWT token
curl https://api.identyclaw.com/api/me/identity \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Success Response** (200 OK):
```json
{
  "token_id": "bkbvehbdcrgm",
  "owner_id": "your-account.near",
  "metadata": {
    "title": "Your Passport Title",
    "issued_at": "1776622758000000000",
    "not_after": "1808158758000000000"
  }
}
```

✓ **If you see your passport information with `token_id` matching your ID, your login is working correctly!**

**Important**:
- Must use `Authorization: Bearer <token>` header format
- JWT expires in 1 hour - request new token when expired
- Token is valid for all protected endpoints

## Machine-readable login errors

These **API error codes** apply to the **JWT login lane only** (challenge from `GET /api/login/timestamp`, **base64url** signature on the **login signing payload**, `POST /api/login`). They are **not** used for HOLA line verification (`HOLA_*` codes and `failureReasons` on verify).

### Response shape

- **Unified** (typical): `{ "error": { "code", "message", "details"? }, "requestId", "timestamp" }`.
- **Legacy login validation** (some 400 paths): top-level string `error` equal to the code — use `body.error?.code ?? body.error` when parsing.

### `GET /api/login/timestamp`

| HTTP | API error code | Typical cause |
| --- | --- | --- |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `AGENT_AUTH_PARAMS_FAILED` | Server could not generate challenge |

### `POST /api/login` — request validation (HTTP 400)

| API error code | Typical cause |
| --- | --- |
| `LOGIN_TIMESTAMP_AMBIGUOUS` | Both `timestamp` and `timestamp_iso` sent |
| `INVALID_LOGIN_TIMESTAMP` | Missing or malformed timestamp for login |
| `LOGIN_PAYLOAD_DEPRECATED` | Deprecated keys or two non-empty signature fields |
| `LOGIN_IDENTIFIER_AMBIGUOUS` | Both `roditid` and `accountid` non-empty |
| `MISSING_LOGIN_IDENTIFIER` | Neither identifier |
| `MISSING_BASE64URL_SIGNATURE` | No `base64url_signature` / `roditid_base64url_signature` |

### `POST /api/login` — credential verification (HTTP 401)

On failure, `error.code` is usually the same string as `error.details.failureReason` (when details are present).

| API error code | Meaning |
| --- | --- |
| `LOGIN_CHALLENGE_TIMESTAMP_INVALID` | Login challenge Unix `timestamp` rejected (e.g. too far in the future vs server); must align with **login challenge pair** from `GET /api/login/timestamp`. |
| `LOGIN_BASE64URL_SIGNATURE_INVALID` | **base64url login signature** did not verify over UTF-8 **login signing payload** (`roditid` or `accountid` + canonical `timestamp_iso` from that challenge). |
| `RODIT_NOT_FOUND` | No on-chain RODiT for the identifier |
| `RODIT_MISSING_METADATA` | Token missing required metadata |
| `RODIT_NOT_LIVE` | Passport outside `not_before` / `not_after` |
| `RODIT_REVOKED` | Passport revoked |
| `RODIT_FAMILY_MISMATCH` | Passport family does not match server configuration |
| `SMART_CONTRACT_NOT_TRUSTED` | Issuing contract not trusted |
| `SERVER_CONFIG_INCOMPLETE` | Server RODiT configuration incomplete |
| `LOGIN_MODE_POLICY_REJECTED_*` | Dynamic codes when `LOGIN_MODE` rejects a path |
| `LOGIN_ERROR` | Unexpected error during login |
| `INVALID_CREDENTIALS` | Generic fallback |

**Note:** Outbound **webhook** signature failures use `WEBHOOK_SIGNATURE_INVALID` (not returned from `POST /api/login`).

### Protected endpoints — bearer JWT validation (HTTP 401)

These apply **after** login, on routes that require `Authorization: Bearer <jwt_token>`.

| HTTP | API error code | `details.reason` (typical) | Meaning |
| --- | --- | --- | --- |
| 401 | `INVALIDATED_TOKEN` | `invalid_jwt_format` | Bearer value is not a parseable JWT (often **truncated/redacted**, e.g. copied from agent tool output) |
| 401 | `INVALIDATED_TOKEN` | `error_checking_session` | JWT parseable but session invalid/expired/revoked |
| 401 | `MISSING_TOKEN` | — | No Authorization header |

**Agent-client note:** When `invalid_jwt_format` occurs immediately after a successful `POST /api/login`, the client almost certainly sent a **truncated** token. Check token length (~1500–2000 chars) before investigating server session state.

### Other

| HTTP | API error code | When |
| --- | --- | --- |
| 503 | `AUTH_SERVICE_UNAVAILABLE` | Auth client not initialized on this instance |

**HOLA lane:** Inter-agent HOLA verification uses different classifiers (`HOLA_*` on HTTP errors from `/api/testhola` and early `/api/identity/verify` checks; `failureReasons` on verify). Do not map those strings to login-only codes above.

## Common Pitfalls

❌ **Using different timestamps for signing vs payload**
- **Problem**: Calling `/api/login/timestamp` at time T1, then using a different ISO timestamp in payload/signature
- **Solution**: Use the same fresh `timestamp_iso` from one `/api/login/timestamp` response for both

❌ **Reusing a timestamp after a failed login**
- **Problem**: Retrying `POST /api/login` with the same old `timestamp_iso`
- **Solution**: Fetch a brand-new timestamp from `/api/login/timestamp` before every retry

❌ **Signing with wrong timestamp format**
- **Problem**: Signing with Unix timestamp instead of ISO string
- **Solution**: Sign with `timestamp_iso` (e.g., `2026-04-19T18:19:18.000Z`)

❌ **Non-canonical ISO timestamp**
- **Problem**: Sending a non-canonical ISO format (offset timezone, missing milliseconds, etc.)
- **Solution**: Use `timestamp_iso` exactly as returned by `/api/login/timestamp`

❌ **Wrong signature encoding**
- **Problem**: Using standard base64 instead of base64url
- **Solution**: Replace `+` with `-`, `/` with `_`, remove `=` padding

❌ **Wrong Content-Type**
- **Problem**: Missing or incorrect Content-Type header
- **Solution**: Always use `Content-Type: application/json`

❌ **Passport expired**
- **Problem**: Passport's `not_after` date has passed
- **Solution**: Check Passport metadata, mint new Passport if expired

❌ **Wrong network**
- **Problem**: Using testnet credentials on mainnet (or vice versa)
- **Solution**: Verify network configuration matches your Passport's network

❌ **Copying a redacted JWT or misreading post-login INVALIDATED_TOKEN**
- **Problem**: Tool output shows `jwt_token` as `eyJhbG…ISDw`; a later request uses that fragment, or the agent blames server session storage
- **Solution**: Verify bearer token length (~1500–2000) on the client first; store the full JWT on the agent machine per [mcp-auth-tools.md](mcp-auth-tools.md)

## Next Steps

- [HOLA Protocol for inter-agent authentication](hola-agent-authentication.md)
- [Understand Passport metadata](token-metadata.md)
- [Explore API endpoints](api-reference.md)
- [View JSON-LD integration](jsonld-metadata.md)
