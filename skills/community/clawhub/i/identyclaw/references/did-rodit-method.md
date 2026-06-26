# The `did:rodit` Method

**Status:** Experimental — OpenAPI marks DID resolution endpoints as experimental and they may change. There is **no separate method version** (not on-chain; not in [`api-docs/swagger.json`](../api-docs/swagger.json)). See [versioning.md](versioning.md).  
**Normative references:** [W3C DID Core 1.0](https://www.w3.org/TR/did-core/), [did:web Method Specification](https://w3c-ccg.github.io/did-method-web/)

This document is the IdentyClaw **DID method specification** for Rich Online Digital Identity Tokens (RODiT / IdentyClaw Passports) served by IDClawserver.

---

## 1. Method name

| Property | Value |
|----------|--------|
| **Method** | `rodit` |
| **DID syntax** | `did:rodit:<passport-id>` |

The method name uses only lowercase ASCII letters (`r`, `o`, `d`, `i`, `t`), which satisfies the DID Core `method-name` production.

**Do not use** NEAR contract account IDs (e.g. `rodit.near`, `genaaaa-identyclaw-com.near`) in the DID string. Contract deployment is configuration and on-chain metadata (`serviceprovider_id`), not part of the DID identifier.

---

## 2. Method-specific identifier (`passport-id`)

| Rule | Requirement |
|------|-------------|
| Length | Exactly **12** characters |
| Charset | Lowercase ASCII letters **`a`–`z`** only |
| Semantics | On-chain RODiT `token_id` (facial encoding); unique within a given NEAR contract deployment |
| Examples | `bkbvehbdcrgm`, `saaddbbadbbf` |

Passport IDs are case-normalized to lowercase for blockchain lookup. Other encodings (facial categories) are documented in [token-metadata.md](token-metadata.md#facial-token-id-encoding).

---

## 3. Blockchain and contract context (resolution prerequisites)

`did:rodit` resolution is **not** a neutral global resolver. Each IDClawserver instance resolves tokens against:

| Setting | Source | Purpose |
|---------|--------|---------|
| **`NEAR_CONTRACT_ID`** | `config/main.json`, `config/development.json`, or host `NEAR_CONTRACT_ID` env | NEAR account of the RODiT smart contract |
| **`NEAR_RPC_URL`** | Same config / env | NEAR RPC endpoint used for on-chain reads |
| **Network** | **NEAR mainnet** (implicit via RPC and contract deployment) | Production and development configs both target mainnet contract accounts |

**Contract naming (operator reference only):**

- Production: `gen****-identyclaw-com.near` (e.g. `genaaaa-identyclaw-com.near`)
- Development: `YYYYYvN-identyclaw-com.near` (e.g. `2026v2-identyclaw-com.near`)

Documentation examples use the **production/main** contract. The DID string does not encode which contract is used; resolvers must know the API host (or trust that host’s `NEAR_CONTRACT_ID`).

If the same `passport-id` existed on two contracts (unlikely in practice), `did:rodit:<passport-id>` would be ambiguous across resolvers pointing at different contracts.

---

## 4. Resolution

### 4.1 Authentication

All HTTP resolution endpoints require a **valid JWT** (Bearer), same as other authenticated IdentyClaw API routes. Unauthenticated callers receive an error from the authentication middleware.

### 4.2 Resolution URLs

Let `{base}` be the IdentyClaw API origin (e.g. `https://api.identyclaw.com`).

| Operation | HTTP | URL |
|-----------|------|-----|
| Resolve by passport id (primary) | `GET` | `{base}/.well-known/did/rodit/{passport-id}` |
| Resolve by DID string | `GET` | `{base}/.well-known/did/resolve?did={url-encoded-did}` |
| Resolve as `did:web` (alias primary) | `GET` | `{base}/.well-known/did/web/token/{passport-id}` |
| Same, `did.json` suffix | `GET` | `{base}/.well-known/did/web/token/{passport-id}/did.json` |

**Examples:**

```http
GET /.well-known/did/rodit/bkbvehbdcrgm
Authorization: Bearer <jwt>
```

```http
GET /.well-known/did/resolve?did=did%3Arodit%3Abkbvehbdcrgm
Authorization: Bearer <jwt>
```

### 4.3 MCP discovery

| MCP resource URI | Description |
|------------------|-------------|
| `did:resolve:{passport-id}` | DID document JSON (12-letter id) |
| `doc:reference:did-rodit-method` | This specification (Markdown) |

### 4.4 Resolution algorithm (normative for IdentyClaw)

1. Parse `did:rodit:<passport-id>` or accept `passport-id` from the path parameter.
2. Load the Passport on-chain via `NEAR_CONTRACT_ID` / RPC (`token_id` = `passport-id`).
3. If no token → **404** `DID_NOT_FOUND`.
4. Fetch the current owner’s Ed25519 public key from NEAR.
5. Build a DID document (see §5).
6. If the request used `did:web`, set `id` to the `did:web` form and include `did:rodit:…` in `alsoKnownAs` (and vice versa for `did:rodit` primary).

---

## 5. DID document

### 5.1 `did:rodit` primary form

| Field | Value |
|-------|--------|
| `id` | `did:rodit:<passport-id>` |
| `alsoKnownAs` | `did:web:<host>:token:<passport-id>` when host is known (`:` in host percent-encoded as `%3A`) |
| `controller` | NEAR account id of the current token owner (not the DID string) |
| `verificationMethod[]` | One entry: `id` = `{did}#controller`, `type` = `Ed25519VerificationKey2020`, `controller` = `{did}`, `publicKeyBase58` = owner key |
| `authentication` / `assertionMethod` | `[ "{did}#controller" ]` |
| `service[]` | `RoditTokenMetadata` (embedded metadata) and `MCPDiscoveryService` (`{base}/api/mcp/resources`) |

`@context` includes `https://www.w3.org/ns/did/v1` and the IdentyClaw RODiT vocabulary (`https://identyclaw.com/ns/rodit#`).

### 5.2 Example (illustrative)

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    {
      "rodit": "https://identyclaw.com/ns/rodit#",
      "RoditTokenMetadata": "https://identyclaw.com/ns/services#RoditTokenMetadata",
      "MCPDiscoveryService": "https://identyclaw.com/ns/services#MCPDiscoveryService"
    }
  ],
  "id": "did:rodit:bkbvehbdcrgm",
  "alsoKnownAs": [
    "did:web:api.identyclaw.com:token:bkbvehbdcrgm"
  ],
  "controller": "abc123def4567890123456789012345678901234567890123456789012345678",
  "verificationMethod": [
    {
      "id": "did:rodit:bkbvehbdcrgm#controller",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:rodit:bkbvehbdcrgm",
      "publicKeyBase58": "..."
    }
  ],
  "authentication": ["did:rodit:bkbvehbdcrgm#controller"],
  "assertionMethod": ["did:rodit:bkbvehbdcrgm#controller"],
  "service": [
    {
      "id": "did:rodit:bkbvehbdcrgm#metadata",
      "type": "RoditTokenMetadata",
      "serviceEndpoint": { "type": "RODiTMetadataDocument", "tokenId": "bkbvehbdcrgm", "metadata": {} }
    },
    {
      "id": "did:rodit:bkbvehbdcrgm#mcp-discovery",
      "type": "MCPDiscoveryService",
      "serviceEndpoint": "https://api.identyclaw.com/api/mcp/resources"
    }
  ]
}
```

---

## 6. Relationship to `did:web`

| Aspect | `did:rodit` | `did:web` (alias) |
|--------|-------------|-------------------|
| **Purpose** | Stable, contract-host-agnostic passport identifier | HTTPS-oriented identifier tied to the serving API host |
| **Form** | `did:rodit:<passport-id>` | `did:web:<host>:token:<passport-id>` |
| **Primary in API** | Default for `/.well-known/did/rodit/...` and `did:resolve` when method is `rodit` | Primary when resolving via `/.well-known/did/web/token/...` |
| **Document** | Same logical document; `id` and `alsoKnownAs` swap roles | Same |
| **Generic did:web resolvers** | N/A | May work only if the host exposes unauthenticated well-known DID URLs; IdentyClaw currently requires JWT on these paths |

Integrators should treat **`did:rodit`** as the portable passport DID and **`did:web`** as the deployment-scoped alias for the same passport on a given API hostname.

---

## 7. Supported DID methods on IdentyClaw resolvers

| Method | Supported | Notes |
|--------|-----------|--------|
| `rodit` | Yes | This specification |
| `web` | Yes | Path must include `:token:<passport-id>` after host segments |
| `wba`, others | No | Rejected with `INVALID_DID` |

Legacy documentation that referred to `did:wba:rodit.near:…` is withdrawn. JSON-LD views may still use on-chain `did_wba_jsonld`; HTTP DID resolution uses `did:rodit` / `did:web` only.

---

## 8. Experimental status and stability

- OpenAPI `/.well-known/did/*` operations are labeled **EXPERIMENTAL** and may change when [`api-docs/swagger.json`](../api-docs/swagger.json) `info.version` bumps.
- This file describes server behavior for RFC alignment; it is not a W3C-registered method and carries no standalone revision number.
- Breaking changes (e.g. new verification method type, public unauthenticated resolution) require updates to this document, `did.protected.routes.js`, and OpenAPI as needed.

---

## 9. Security considerations

- Resolution reveals passport metadata and owner NEAR account id to authenticated callers.
- Trust the API instance’s `NEAR_CONTRACT_ID` when verifying that a DID refers to a genuine IdentyClaw Passport.
- Verify signatures via HOLA or JWT login flows; DID resolution alone does not prove live possession of a private key.
- Impersonation: compare attested `token_id` with out-of-band publication ([finding-agents.md](finding-agents.md)).

---

## 10. Related documentation

- [versioning.md](versioning.md) — HTTP API release (swagger) vs on-chain JSON-LD (MCP)
- [api-reference.md](api-reference.md#did-resolution) — HTTP endpoints
- [jsonld-metadata.md](jsonld-metadata.md) — Semantic mappings
- [token-metadata.md](token-metadata.md) — Passport fields and facial encoding
- [security-compliance-improvements.md](../security-compliance-improvements.md) — Compliance backlog (item 18)
