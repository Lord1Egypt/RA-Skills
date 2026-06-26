---
name: identyclaw
description: >-
  IdentyClaw API workflows — API session login (JWT), HOLA peer handshake lines,
  DID resolution, and Passport lookup. Requires an IdentyClaw Passport on the Gateway.
  Use when creating or verifying HOLA lines, obtaining an API session, resolving
  Passport IDs, enrolling on NEAR, or reading agent discovery metadata.
version: 1.4.0
metadata:
  openclaw:
    envVars:
      - name: IDENTYCLAW_BASE_URL
        required: false
        description: API base URL (default https://api.identyclaw.com)
      - name: IDENTYCLAW_ACCOUNT_ID
        required: false
        description: NEAR implicit account id (64-char hex) for API login
      - name: IDENTYCLAW_NEAR_PRIVATE_KEY
        required: false
        description: Passport Ed25519 key (ed25519:...) — API login signature + HOLA line signing (Gateway only)
      - name: IDENTYCLAW_JWT
        required: false
        description: Optional API bearer token (jwt_token from POST /api/login) — not a HOLA line
    homepage: https://api.identyclaw.com/docs
---

# IdentyClaw

**Base URL:** `https://api.identyclaw.com`

IdentyClaw is an HTTP API for IdentyClaw Passport holders and the **HOLA** mutual authentication protocol. This skill is the **runnable cheat sheet**; deep specs live in bundled `references/` and MCP `doc:*` resources.

**Live docs:** MCP `doc:discovery` · `doc:skills` · `curl https://api.identyclaw.com/api/mcp/resource/doc:skills`

**ClawHub:** [identyclaw/identyclaw](https://clawhub.ai/identyclaw/identyclaw) · [OpenClaw plugin](https://clawhub.ai/plugins/@identyclaw/openclaw-identyclaw-plugin) · [Source (skill + plugin)](https://github.com/discernible-io/openclaw-identyclaw-plugin)

---

## Two lanes — do not mix them

| Lane | Artifact | Typical TTL | Signing | Docs |
| --- | --- | --- | --- | --- |
| **API login** | Bearer **JWT** (`jwt_token`) | ~1 hour | `accountid` + `timestamp_iso` → **base64url** | [`references/login-authentication.md`](references/login-authentication.md) |
| **HOLA protocol** | **HOLA line** (slash-separated string) | ~5 min (nonce) | Canonical prefix → **base32** + checksum | [`references/hola-howto.md`](references/hola-howto.md), [`references/hola-agent-authentication.md`](references/hola-agent-authentication.md) |

**Two clocks:**

| Clock | Source | Used for |
| --- | --- | --- |
| JWT **session** | `POST /api/login` | `Authorization: Bearer …` on protected routes |
| HOLA **nonce** | `GET /api/holanonce16ts` | `noncetsHex` + `timestamp` in each HOLA line — **not** login `timestamp_iso` |

| Endpoint | JSON fields | Purpose |
| --- | --- | --- |
| `GET /api/login/timestamp` | `timestamp`, `timestamp_iso` | API login only |
| `GET /api/holanonce16ts` | `noncetsHex`, `timestamp` | HOLA line only — [`references/holanonce-api.md`](references/holanonce-api.md) |

A JWT is **not** a HOLA line. HOLA tools need an API session to call protected routes; the handshake payload is the **HOLA wire string**.

---

## Credentials (ClawHub “API key required” badge)

ClawHub’s badge means your **IdentyClaw Passport** — not a separate vendor API key.

| What you configure | Role |
| --- | --- |
| **Passport signing key** (`accountid` + `nearPrivateKey`) | Long-lived secret on the Gateway (like an API key) |
| **JWT** (`jwt_token`) | Short-lived **API session**; plugin auto-login usually supplies this |
| **Public routes** | No Passport needed |

**`nearPrivateKey` on the Gateway** — same NEAR key, **two signatures**:

1. **API login** — base64url over `accountid` + `timestamp_iso`
2. **HOLA create** — base32 over uppercase canonical HOLA prefix (`identyclaw_create_hola` / `@rodit/hola-client`)

`identyclaw_verify_hola` needs only API session + peer HOLA line (no `nearPrivateKey`).

```json5
{
  plugins: {
    entries: {
      "identyclaw-tools": {
        enabled: true,
        config: {
          baseUrl: "https://api.identyclaw.com",
          accountid: "<64-char-hex-near-implicit-account>",
          nearPrivateKey: "ed25519:..."
        }
      }
    }
  }
}
```

Enroll first if needed: [`references/login-authentication.md`](references/login-authentication.md). Never paste keys into chat.

---

## Install and entry points

```text
Skill (workflows):     openclaw skills install clawhub:identyclaw
Plugin (tools):        openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
MCP (docs):            https://api.identyclaw.com/mcp
Discovery index:       doc:discovery
Cheat sheet:           doc:skills
```

---

## Agent cheat sheet

| # | Goal | Method | Lane |
|---|------|--------|------|
| 1 | API session (JWT) | `GET /api/login/timestamp` → sign → `POST /api/login` | API login |
| 2 | **Create outbound HOLA line** | `identyclaw_create_hola` or `@rodit/hola-client` | HOLA (+ API session) |
| 3 | **Verify peer HOLA line** | `POST /api/identity/verify` or `identyclaw_verify_hola` | HOLA (+ API session) |
| 4 | Resolve Passport → full DN | `GET /api/identity/token/{tokenId}/full` | API session |
| 5 | List public agents | `GET /api/agents?limit=20` | Public |
| 6 | Resolve DID | `GET /.well-known/did/resolve?did=did:rodit:{tokenId}` | API session |

### 1. API login (get JWT)

```bash
BASE=https://api.identyclaw.com

TS_JSON=$(curl -sS "$BASE/api/login/timestamp")
TIMESTAMP=$(echo "$TS_JSON" | jq -r '.timestamp')
TIMESTAMP_ISO=$(echo "$TS_JSON" | jq -r '.timestamp_iso')

# Sign UTF-8: <accountid> + <timestamp_iso> (no separator) → base64url_signature

JWT=$(curl -sS -X POST "$BASE/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"accountid\":\"<64-char-hex>\",\"timestamp\":$TIMESTAMP,\"base64url_signature\":\"<sig>\"}" \
  | jq -r '.jwt_token')
```

Full steps: [`references/login-authentication.md`](references/login-authentication.md#quick-start-login-pattern).

### 2. Create outbound HOLA line

**Recommended:** `identyclaw_create_hola` (plugin **v1.4.0+**) or **`@rodit/hola-client`** — API session fetches nonce; **private key signs HOLA locally**.

```text
HOLA/<recipient>/<tokenId>/<timestamp>/<noncetsHex>/API.IDENTYCLAW.COM/<base32-signature>/<checksum>
```

Walkthrough: [`references/hola-howto.md`](references/hola-howto.md). Self-test: `POST /api/testhola`.

### 3. Verify an incoming HOLA line

The **payload** is the HOLA string; your **JWT** only authorizes the API call.

```bash
curl -sS -X POST https://api.identyclaw.com/api/identity/verify \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"hola":"HOLA/MUNDO/<peerTokenId>/...","expectedRecipient":"MUNDO"}'
```

Trust only when `verified: true`. Diagnostics: [`references/hola-agent-authentication.md`](references/hola-agent-authentication.md#verification-result-diagnostics-apidentityverify).

### 4–6. Identity, discovery, DID

```bash
curl -sS "$BASE/api/identity/token/<tokenId>/full" -H "Authorization: Bearer $JWT"
curl -sS "$BASE/api/agents?limit=20"
curl -sS "$BASE/.well-known/did/resolve?did=did:rodit:<tokenId>" -H "Authorization: Bearer $JWT"
```

---

## First contact from an unknown agent

1. **API login** — your JWT (cheat sheet §1).
2. **Verify HOLA line** — `POST /api/identity/verify` with the exact string received (not a JWT).
3. **If `verified: true`** — note `peerTokenId`.
4. **Lookup** — `GET /api/identity/token/{peerTokenId}/full`.
5. **Impersonation guard** — compare `peerTokenId` to officially published Passport ID. [`references/finding-agents.md`](references/finding-agents.md#5-guard-against-impersonation).
6. **Subagent** — `POST /api/isauthorizedsigner` when delegation fields present. [`references/hola-subagent-authentication.md`](references/hola-subagent-authentication.md).

---

## OpenClaw plugin (recommended for Gateways)

```bash
openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
```

Plugin **v1.4.0+** · tool reference: [README.md](https://github.com/discernible-io/openclaw-identyclaw-plugin/blob/main/README.md)

### Public (no API session)

| Tool | Endpoint |
| --- | --- |
| `identyclaw_list_agents` | `GET /api/agents` |
| `identyclaw_list_resources` | `GET /api/mcp/resources` |
| `identyclaw_get_resource` | `GET /api/mcp/resource/{uri}` |

### API session only

| Tool | Endpoint |
| --- | --- |
| `identyclaw_get_my_identity` | `GET /api/me/identity` |
| `identyclaw_get_agent_identity` | `GET /api/identity/token/{tokenId}/full` |
| `identyclaw_check_subagent_signer` | `POST /api/isauthorizedsigner` |
| `identyclaw_resolve_did` | `GET /.well-known/did/resolve` |

### HOLA protocol

| Tool | Notes |
| --- | --- |
| `identyclaw_get_nonce` | `GET /api/holanonce16ts` — HOLA nonce fields |
| `identyclaw_create_hola` | API session + local HOLA sign (`nearPrivateKey`) |
| `identyclaw_verify_hola` | API session + peer HOLA line → `POST /api/identity/verify` |

Allowlist optional tools in `tools.allow` when credentials are configured.

**ClawHub skill (this bundle):** `openclaw skills install clawhub:identyclaw`

---

## Bundled references

| Topic | File |
|-------|------|
| Endpoint catalog | [`references/api-reference.md`](references/api-reference.md) |
| API login / JWT | [`references/login-authentication.md`](references/login-authentication.md) |
| HOLA quick path | [`references/hola-howto.md`](references/hola-howto.md) |
| HOLA full spec | [`references/hola-agent-authentication.md`](references/hola-agent-authentication.md) |
| HOLA nonce JSON | [`references/holanonce-api.md`](references/holanonce-api.md) |
| Subagent delegation | [`references/hola-subagent-authentication.md`](references/hola-subagent-authentication.md) |
| Agent discovery | [`references/finding-agents.md`](references/finding-agents.md) |
| Collaboration envelope | [`references/collaboration-envelope.md`](references/collaboration-envelope.md) |
| OpenClaw webhooks | [`references/openclaw-integration-guide.md`](references/openclaw-integration-guide.md) |
| Client-side auth | [`references/mcp-auth-tools.md`](references/mcp-auth-tools.md) |
| Enrollment | [`references/enrollment.md`](references/enrollment.md) |

---

## Conventions

**Terminology:** User-facing copy says **IdentyClaw Passport** (12-letter ID). **RODiT** is protocol technology only — do not say "RODiT Passport."

**Skill vs plugin vs MCP:** This **skill** teaches workflows. The **plugin** runs API calls and local HOLA signing. **MCP** serves documentation only (`list_resources`, `get_resource`).
