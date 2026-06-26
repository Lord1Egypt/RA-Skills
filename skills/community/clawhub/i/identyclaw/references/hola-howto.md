# Send a verifiable HOLA in under 5 minutes

Linear path from **IdentyClaw Passport holder** to **peer-verified HOLA**. For full protocol detail see [hola-agent-authentication.md](hola-agent-authentication.md); for subagent delegation see [hola-subagent-authentication.md](hola-subagent-authentication.md).

## Two clocks (do not confuse them)

| Clock | Typical TTL | Source | Used for |
| --- | --- | --- | --- |
| **JWT session** | ~1 hour | `POST /api/login` | Bearer auth on protected endpoints (`/api/holanonce16ts`, `/api/identity/verify`, …) |
| **HOLA nonce freshness** | ~5 minutes | `GET /api/holanonce16ts` | Timestamp + nonce inside each HOLA line |

“Session broke after a few minutes” usually means the **HOLA timestamp/nonce** expired, not the JWT. Fetch a **new nonce immediately before each HOLA** you sign.

---

## Step 1 — Log in (get a JWT)

Obtain a Bearer JWT so you can call protected endpoints.

- **Default (curl):** `GET /api/login/timestamp` → sign `accountid + timestamp_iso` (or `roditid + timestamp_iso`) → `POST /api/login`. No client-side NEAR RPC. See [login-authentication.md](login-authentication.md#quick-start-login-pattern).
- **Optional SDK:** `@rodit/rodit-auth-be` `RoditClient.login_server()` also validates the API server Passport over NEAR RPC—use only when that tradeoff is acceptable. See [Verify the API server (MITM protection)](login-authentication.md#verify-the-api-server-mitm-protection).

Confirm with:

```bash
curl -sS https://api.identyclaw.com/api/me/identity \
  -H "Authorization: Bearer ${JWT}"
```

Note your 12-letter **`tokenId`** (Passport facial ID) from the response.

---

## Step 2 — Fetch a fresh HOLA nonce

```bash
curl -sS https://api.identyclaw.com/api/holanonce16ts \
  -H "Authorization: Bearer ${JWT}"
```

Response keys (use verbatim): **`noncetsHex`**, **`timestamp`**. Not `timestamp_iso`, `nonceHex`, or `nonce`. See [holanonce-api.md](holanonce-api.md).

Use this pair **once**, immediately — do not cache across HOLA messages.

---

## Step 3 — Build, sign, and checksum the HOLA line

Standard format:

```text
HOLA/<recipient>/<tokenId>/<timestamp>/<noncetsHex>/API.IDENTYCLAW.COM/<base32-signature>/<checksum>
```

1. Build the prefix ending in `API.IDENTYCLAW.COM/` (recipient is often `MUNDO`).
2. **Uppercase** the entire signed prefix before signing.
3. Sign with your Passport owner **Ed25519** secret key; encode signature as **base32** (uppercase, no padding).
4. Checksum: sum `charCodeAt` over `canonicalUppercase + signatureB32 + '/'`, mod 23, index into `ABCDEFGHJKMNPQRSTUVWXYZ`.

Self-test before sending to peers:

```bash
curl -sS -X POST https://api.identyclaw.com/api/testhola \
  -H "Authorization: Bearer ${JWT}" \
  -H "Content-Type: application/json" \
  -d '{"hola":"<your line>"}'
```

Full walkthrough: [hola-agent-authentication.md](hola-agent-authentication.md).

---

## Step 4 — Send the HOLA to your peer

Deliver the complete HOLA string out of band (message, webhook, MCP tool result, etc.). The line is time-sensitive; peers should verify promptly.

---

## Step 5 — Peer verifies via the API

Your peer (with their own JWT) calls:

```bash
curl -sS -X POST https://api.identyclaw.com/api/identity/verify \
  -H "Authorization: Bearer ${PEER_JWT}" \
  -H "Content-Type: application/json" \
  -d '{"hola":"<HOLA line you sent>"}'
```

HTTP **200** with `"verified": true` means format, checksum, freshness, nonce, token, and signature checks passed. On failure, `failureDetails` includes **`hint`** per reason code; `nonce_replay` also returns **`nonceReplayDetails`** (`holaTimestamp`, `maxAgeMs`, optional `firstSeenAt`).

---

## Step 6 — Impersonation guard (compare canonical Passport ID)

Cryptographic verification proves continuity for a **specific** 12-letter `tokenId`. It does **not** prove the passport belongs to a person or brand you trust.

After verify succeeds:

1. Find the entity’s **canonical Passport ID** on channels they control (website, verified social, docs).
2. Compare it to the `tokenId` in the HOLA line.
3. If the verified `tokenId` is not the same ID the entity officially publishes, reject them as that entity, even though HOLA verification succeeded.

See [finding-agents.md § Guard against impersonation](finding-agents.md#5-guard-against-impersonation).

---

## MCP resource

Agents with MCP access: `doc:reference:hola-howto` (this document).

## Related docs

- [login-authentication.md](login-authentication.md) — JWT login
- [holanonce-api.md](holanonce-api.md) — nonce response shape
- [hola-agent-authentication.md](hola-agent-authentication.md) — full HOLA specification
- [finding-agents.md](finding-agents.md) — discovery and impersonation guard
