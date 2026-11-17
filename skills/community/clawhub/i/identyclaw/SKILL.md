---
name: identyclaw
description: >-
  IdentyClaw API workflows — multi-API JWT sessions (auto-login), HOLA peer
  handshake lines, DID resolution, and Passport lookup. Requires an IdentyClaw
  Passport on the Gateway. Use when calling home or federated APIs, creating or
  verifying HOLA lines, resolving Passport IDs, or reading agent discovery
  metadata. For agent-to-agent A2A messaging use the separate identyclaw-a2a plugin.
version: 1.9.6
metadata:
  openclaw:
    envVars:
      - name: IDENTYCLAW_BASE_URL
        required: false
        description: Home API base URL (default https://api.identyclaw.com)
      - name: IDENTYCLAW_API_ENDPOINTS
        required: false
        description: Comma-separated federated API URLs for concurrent sessions (e.g. https://api-b.example.com)
      - name: IDENTYCLAW_ACCOUNT_ID
        required: false
        description: NEAR implicit account id (64-char hex) for API login
      - name: IDENTYCLAW_NEAR_PRIVATE_KEY
        required: false
        description: Passport Ed25519 key (ed25519:...) — API login signature + HOLA line signing (Gateway only)
    homepage: https://api.identyclaw.com/docs
---

# IdentyClaw

**Home API (default):** `https://api.identyclaw.com`  
**Federated example:** `https://api-b.example.com` (same Rodit login family; configure via `apiEndpoints`)

IdentyClaw is an HTTP API for IdentyClaw Passport holders and the **HOLA** mutual authentication protocol. This skill is a **convenience cheat sheet** for agents; tool catalog and install steps live in the plugin [README](https://github.com/discernible-io/openclaw-identyclaw-plugin/blob/main/README.md). Deep specs live in bundled `references/` and MCP `doc:*` resources.

> **Convenience document:** Change the plugin README and MCP `doc:*` resources first; update this skill only to keep the walkthrough accurate.

**Live docs:** MCP `doc:discovery` · `doc:skills` · `curl https://api.identyclaw.com/api/mcp/resource/doc:skills`

**ClawHub:** [identyclaw/identyclaw](https://clawhub.ai/identyclaw/identyclaw) · [OpenClaw plugin](https://clawhub.ai/plugins/@identyclaw/openclaw-identyclaw-plugin) · [Source (skill + plugin)](https://github.com/discernible-io/openclaw-identyclaw-plugin)

---

## Home vs federated — do not assume shared routes

Federation shares **Rodit login** only (`GET /api/login/timestamp` → sign → `POST /api/login` → JWT cached per URL). A federated peer may expose **any** product routes. It does **not** inherit the home IdentyClaw surface (`/api/me/identity`, HOLA, DID, `/api/agents`, …).

| Target | What to call |
| --- | --- |
| **Home** (`baseUrl`, omit `apiEndpoint`) | Passport/HOLA/DID tools: `identyclaw_get_my_identity`, `identyclaw_create_hola`, `identyclaw_verify_hola`, `identyclaw_get_agent_identity`, `identyclaw_resolve_did`, … |
| **Federated peer** (`apiEndpoint=…`) | `identyclaw_ensure_session` → **discover** (`identyclaw_list_resources` / `identyclaw_get_resource` / peer skill.md / OpenAPI) → **product calls** via `identyclaw_request({ method, path, apiEndpoint })` |

**Never** probe home-only tools against a federated host “to see if they work.” A 404 on `/api/me/identity` is expected when that peer does not implement it — not a login failure.

---

## Agent rule — do not hand-roll login

When the **OpenClaw plugin** is installed (`identyclaw-tools`):

1. **Never** curl `GET /api/login/timestamp` or `POST /api/login`, and never invent Ed25519 signatures in chat.
2. Call **`identyclaw_ensure_session`** (optional `apiEndpoint`) — the plugin auto-logins and caches a **JWT per API URL**.
3. **Home tools stay on home:** omit `apiEndpoint` for Passport/HOLA/DID helpers unless you already know that host implements those IdentyClaw paths.
4. **Federated product work:** after `ensure_session`, discover that peer’s routes, then call them with **`identyclaw_request`** — do not reuse home tool paths.
5. Use **`identyclaw_list_sessions`** to see which APIs already have a live session.
6. **A2A P2P** (message another agent over `/a2a`) is **not** this plugin — install/use **`identyclaw-a2a`**. That plugin owns per-peer JWTs.

Manual curl login below is for **operators / non-plugin clients only**.

---

## Two lanes — do not mix them

| Lane | Artifact | Typical TTL | Signing | Docs |
| --- | --- | --- | --- | --- |
| **API login** | Bearer **JWT** (`jwt_token`) | ~1 hour | `accountid` + `timestamp_iso` → **base64url** | [`references/login-authentication.md`](references/login-authentication.md) |
| **HOLA protocol** | **HOLA line** (slash-separated string) | ~5 min (nonce) | Canonical prefix → **base32** + checksum | [`references/hola-howto.md`](references/hola-howto.md), [`references/hola-agent-authentication.md`](references/hola-agent-authentication.md) |

**Two clocks:**

| Clock | Source | Used for |
| --- | --- | --- |
| JWT **session** | `POST /api/login` (plugin auto) | `Authorization: Bearer …` on protected routes |
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
| **JWT** (`jwt_token`) | Short-lived **API session**; plugin auto-login supplies this (never paste into chat) |
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
          apiEndpoints: ["https://api-b.example.com"],
          accountid: "<64-char-hex-near-implicit-account>",
          nearPrivateKey: "ed25519:..."
        }
      }
    }
  }
}
```

Env alternative: `IDENTYCLAW_API_ENDPOINTS=https://api-b.example.com`.

Enroll first if needed: [`references/login-authentication.md`](references/login-authentication.md). Never paste keys or JWTs into chat.

**Security notes (operators):**
- Prefer the OpenClaw plugin for login/HOLA so private keys and JWTs stay on the Gateway.
- Passport metadata (DN, ContactURI, geo, facial fields) is sensitive — minimize logging and collection.
- Agent-to-agent A2A is **not** this skill — use `identyclaw-a2a` / the A2A trust skill. Do not enable autonomous email from this skill’s docs.

---

## Install and entry points

```text
Skill (workflows):     openclaw skills install clawhub:identyclaw
Plugin (API + HOLA):   openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
Plugin (A2A P2P):      openclaw plugins install clawhub:@identyclaw/openclaw-a2a-plugin
MCP (docs):            https://api.identyclaw.com/mcp
Discovery index:       doc:discovery
Cheat sheet:           doc:skills
```

---

## Agent cheat sheet

| # | Goal | Method | Lane |
|---|------|--------|------|
| 1 | API session (home or federated) | `identyclaw_ensure_session` ± `apiEndpoint` | API login |
| 2 | List live sessions | `identyclaw_list_sessions` | API login |
| 3 | Discover federated peer routes | `identyclaw_list_resources` / `get_resource` / peer skill + `identyclaw_request` | Federated product |
| 4 | **Create outbound HOLA line** | `identyclaw_create_hola` (home) | HOLA (+ home session) |
| 5 | **Verify peer HOLA line** | `identyclaw_verify_hola` (home) | HOLA (+ home session) |
| 6 | Resolve Passport → full DN | `identyclaw_get_agent_identity` (home) | Home API session |
| 7 | List public agents | `identyclaw_list_agents` (home) | Public |
| 8 | Resolve DID | `identyclaw_resolve_did` (home) | Home API session |
| 9 | Message another agent (A2A) | **`identyclaw-a2a` plugin** (not this skill’s HTTP tools) | A2A P2P |
| 10 | List / transfer RODiT on-chain | **`idcp`** (`list`, `transfer`, `rotate`, …) | NEAR / RODiT |

### 1. API session (plugin — preferred)

```text
# Home identity / HOLA / DID
identyclaw_ensure_session
identyclaw_get_my_identity
identyclaw_list_sessions

# Federated peer — login + discover + product routes (arbitrary paths)
identyclaw_ensure_session   apiEndpoint=https://api-b.example.com
identyclaw_list_resources   apiEndpoint=https://api-b.example.com
identyclaw_get_resource     uri=doc:discovery  apiEndpoint=https://api-b.example.com
identyclaw_request          method=GET path=/…  apiEndpoint=https://api-b.example.com
```

Sessions are **cached per URL**. You can be logged into home and federated APIs **at the same time**. Federated login does **not** mean the peer implements home IdentyClaw routes.

### 1b. Manual API login (operators / non-plugin only)

```bash
BASE=https://api.identyclaw.com   # or federated peer URL

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

**Recommended:** `identyclaw_create_hola` (plugin **v1.4.0+**) — API session fetches nonce; **private key signs HOLA locally**.

```text
HOLA/<recipient>/<tokenId>/<timestamp>/<noncetsHex>/API.IDENTYCLAW.COM/<base32-signature>/<checksum>
```

**Outbound HOLA rules (agents):**

- **Signer / origin** is always **this agent's Passport ID** — resolved from `GET /api/me/identity`.
- Call **`identyclaw_create_hola`** without `tokenId`, or call **`identyclaw_get_my_identity`** first if you need your ID for other steps.
- **Never ask the user for your own Passport ID** to create an outbound HOLA line.
- **Only `recipient`** may be user-supplied: peer **12-letter Passport ID** (letters only, **no spaces** — e.g. `BKBVEHBDCRGM`) or `MUNDO` for broadcast intros. Do not pass display names or space-separated strings; invalid recipients are rejected before signing.
- **Subagent delegation** uses a different HOLA wire format — see [`references/hola-subagent-authentication.md`](references/hola-subagent-authentication.md); do not substitute another agent's ID in standard outbound HOLA.

Walkthrough: [`references/hola-howto.md`](references/hola-howto.md). Self-test: `POST /api/testhola`.

### 3. Verify an incoming HOLA line

Use **`identyclaw_verify_hola`** with the exact HOLA string. The JWT only authorizes the API call.

Trust only when `verified: true`. Diagnostics: [`references/hola-agent-authentication.md`](references/hola-agent-authentication.md#verification-result-diagnostics-apidentityverify).

### 4–8. Identity, discovery, DID (home API)

Prefer plugin tools on the **home** `baseUrl` (`identyclaw_get_agent_identity`, `identyclaw_list_agents`, `identyclaw_resolve_did`). Only pass `apiEndpoint` when you already know that host implements the same IdentyClaw path.

---

## First contact from an unknown agent

1. **Home API session** — `identyclaw_ensure_session` (do not curl login).
2. **Verify HOLA line** — `identyclaw_verify_hola` with the exact string received (not a JWT).
3. **If `verified: true`** — note `peerTokenId`.
4. **Lookup** — `identyclaw_get_agent_identity` (home).
5. **Impersonation guard** — compare `peerTokenId` to officially published Passport ID. [`references/finding-agents.md`](references/finding-agents.md#5-guard-against-impersonation).
6. **Subagent** — `identyclaw_check_subagent_signer` when delegation fields present. [`references/hola-subagent-authentication.md`](references/hola-subagent-authentication.md).
7. **Ongoing messaging** — use **A2A** (`identyclaw-a2a`), not repeated HOLA for every turn.

---

## OpenClaw plugin (recommended for Gateways)

```bash
openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
```

Plugin **v1.6.0+** · tool reference: [README.md](https://github.com/discernible-io/openclaw-identyclaw-plugin/blob/main/README.md)

### Session tools

| Tool | Role |
| --- | --- |
| `identyclaw_ensure_session` | Open/refresh session for home or `apiEndpoint` (no JWT returned). Federated responses include a discover-then-`identyclaw_request` hint. |
| `identyclaw_list_sessions` | List cached multi-API sessions |

### Discovery / generic HTTP (safe on federated peers)

| Tool | Role |
| --- | --- |
| `identyclaw_list_resources` | `GET /api/mcp/resources` — if the peer exposes MCP docs |
| `identyclaw_get_resource` | `GET /api/mcp/resource/{uri}` |
| `identyclaw_request` | Arbitrary `method` + `path` on home or federated host |
| `identyclaw_game_tick` | SLC only: ensure session + submit one required message-report/action (safe defaults). Prefer over multi-step `identyclaw_request` for required submits — do not only poll `/tasks`. Pass `apiEndpoint` for the game host. |
| `idcp` | On-chain RODiT / Passport wallet (near-cli-rs). Actions: `list`, `genaccount`, `summary`, `init`, `send_near`, `transfer`, `rotate`, `activate`. **Off by default** — add `"idcp"` to `tools.allow` and install `near` (near-cli-rs) on the gateway PATH, then restart. Never returns private keys. Native `identyclaw_generate_near_account` does not need this. |

### Home IdentyClaw surface (default: omit `apiEndpoint`)

| Tool | Endpoint |
| --- | --- |
| `identyclaw_list_agents` | `GET /api/agents` |
| `identyclaw_get_my_identity` | `GET /api/me/identity` |
| `identyclaw_get_agent_identity` | `GET /api/identity/token/{tokenId}/full` |
| `identyclaw_check_subagent_signer` | `POST /api/isauthorizedsigner` |
| `identyclaw_resolve_did` | `GET /.well-known/did/resolve` |
| `identyclaw_get_nonce` | `GET /api/holanonce16ts` |
| `identyclaw_create_hola` | local HOLA sign; signer from `/api/me/identity` |
| `identyclaw_verify_hola` | `POST /api/identity/verify` |

These home-surface tools still accept `apiEndpoint` for rare full IdentyClaw replicas — **do not** pass a federated product host unless you know it implements that path. Allowlist optional tools in `tools.allow` when credentials are configured. Enable `idcp` only when on-chain wallet actions are required (`near` on PATH).

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

**Skill vs plugin vs MCP vs A2A:** This **skill** teaches workflows. The **identyclaw-tools** plugin runs multi-API login, HOLA, and identity. **MCP** serves documentation. **identyclaw-a2a** owns agent-to-agent P2P JWTs.
