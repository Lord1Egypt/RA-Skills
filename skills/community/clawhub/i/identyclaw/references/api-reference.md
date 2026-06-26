# API Reference

Complete endpoint listing for IdentyClaw API.

## Table of Contents

- [Public Endpoints](#public-endpoints)
- [Protected Endpoints](#protected-endpoints)
- [Privileged Endpoints](#privileged-endpoints)
- [DID Resolution](#did-resolution)
- [MCP Resources](#mcp-resources)
- [Policy Documents](#policy-documents)

## Public Endpoints

No authentication required.

### Discovery

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API overview with enrollment URL and endpoint listing |
| `/health` | GET | Health check endpoint |
| `/.well-known/enrollment` | GET | Complete enrollment guide with pricing and steps |
| `/.well-known/mcp` | GET | MCP discovery metadata — see [mcp-connection-guide.md](mcp-connection-guide.md) |
| `/docs` | GET | Interactive HTML documentation with Swagger UI |
| `/openapi.json` | GET | OpenAPI 3.0 specification |
| `/swagger.json` | GET | OpenAPI 3.0 specification (alias) |
| `/api/v1/openapi.json` | GET | Versioned OpenAPI specification |

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/login/timestamp` | GET | Get single-use timestamp challenge pair for login |
| `/api/login` | POST | Authenticate with accountid signature and fresh challenge, get JWT |

Login request/response shapes, field constraints, and error semantics are maintained in OpenAPI:

- Canonical contract: [`../api-docs/swagger.json`](../api-docs/swagger.json)
- Runtime endpoints: `GET /openapi.json`, `GET /swagger.json`

For step-by-step API login implementation guidance (challenge retrieval, signing flow, retries, and troubleshooting), use:

- [`login-authentication.md`](login-authentication.md)

### Agent Discovery

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/agents` | GET | List all IdentyClaw Passport holders (cursor-paginated) |

**Query Parameters**:
- `limit` (default: 20, max: 100)
- `cursor` (optional, for pagination)

**Response**:
```json
{
  "agents": [
    {
      "tokenId": "bkbvehbdcrgm",
      "creature": "Legal Specialist",
      "face": {
        "checksumValid": true,
        "categories": [
          "pale-skinned",
          "Nordic",
          "oval-faced"
        ]
      }
    }
  ],
  "nextCursor": "cursor_string_or_null",
  "requestId": "01HQXYZ...",
  "disclaimer": "The creature field and other agent metadata are self-declared by the agent. It is your responsibility to verify the accuracy and authenticity of this information before relying on it."
}
```

### Client Token Signing

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/signclient` | POST | Request server to sign client token metadata |

**Note**: Request non-privileged signing operations through this endpoint. Use permissioned metrics/system/debug/reset endpoints for privileged flows.

---

## Protected Endpoints

Require JWT authentication via `Authorization: Bearer <token>` header.

### Identity

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/me/identity` | GET | Get your own identity information |
| `/api/identity/token/{tokenId}/full` | GET | Get full identity metadata for any token |
| `/api/identity/verify` | POST | Verify HOLA message from peer agent |
| `/api/isauthorizedsigner` | POST | Check if caller is authorized to sign |

**GET /api/identity/token/{tokenId}/full**:

Returns complete identity metadata including DN attributes and facial description.

**Response**:
```json
{
  "tokenId": "bkbvehbdcrgm",
  "dn": {
    "raw": "NNSWF=Alice,Creature=Legal Specialist,Address=123 Main St",
    "nameNotSharedWithFamily": "Alice",
    "nameSharedWithFamily": "Smith",
    "displayName": "Alice Smith",
    "contactUri": "alice@example.com",
    "taxResidence": "US",
    "inceptDateTime": "2026-01-01T00:00:00.000Z",
    "inceptPlace": "New York",
    "taxPayerCode": "12-3456789",
    "address": "123 Main St",
    "creature": "Legal Specialist",
    "avatarUrl": "https://example.com/avatar.jpg",
    "emojiUrl": "https://example.com/emoji.png",
    "allAttributes": {}
  },
  "face": {
    "checksumValid": true,
    "categories": [
      "pale-skinned",
      "Nordic",
      "oval-faced"
    ]
  },
  "requestId": "01HQXYZ...",
  "disclaimer": "The DN metadata including creature, name, contact URI, address, and other attributes are self-declared by the agent. It is your responsibility to verify the accuracy and authenticity of this information before relying on it."
}
```

**POST /api/identity/verify**:

Verify a HOLA message from a peer agent.

**Request**:
```json
{
  "hola": "HOLA/MUNDO/bkbvehbdcrgm/2026-04-19T10:47:00.000Z/4F9A3C7E.../API.IDENTYCLAW.COM/dGVzdA.../M"
}
```

**Response**:
```json
{
  "valid": true,
  "tokenId": "bkbvehbdcrgm",
  "recipient": "MUNDO",
  "timestamp": "2026-04-19T10:47:00.000Z",
  "ageMs": 1234,
  "checksumValid": true,
  "signatureValid": true,
  "nonceValid": true,
  "tokenExists": true
}
```

### Nonces

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/holanonce16ts` | GET | Get nonce for HOLA message (16-byte nonce); requires Bearer JWT |

**Exact response JSON keys** (use verbatim; not login `timestamp_iso` / not `nonceHex`): `noncetsHex`, `timestamp`, `length`, `algorithm`, `requestId`. See [holanonce-api.md](holanonce-api.md).

**Response**:
```json
{
  "noncetsHex": "4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE",
  "timestamp": "2026-04-19T10:47:00.000Z",
  "length": 16,
  "algorithm": "randomBytes(16)_hex",
  "requestId": "01HQXYZ..."
}
```

### Session Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/logout` | POST | Logout and invalidate JWT token |

---

## Privileged Endpoints

Require JWT authentication AND specific permissions in IdentyClaw Passport's `permissioned_routes`.

### Metrics

| Endpoint | Method | Description | Permission Required |
|----------|--------|-------------|---------------------|
| `/api/metrics` | GET | Get performance metrics (admin only) | `metrics` |
| `/api/metrics/system` | GET | Get system metrics (admin only) | `system` |
| `/api/metrics/reset` | POST | Reset metrics | `reset` |
| `/api/metrics/debug` | GET | Get debug information | `debug` |

### Sessions

| Endpoint | Method | Description | Permission Required |
|----------|--------|-------------|---------------------|
| `/api/sessions/list_all` | GET | List all active sessions | `list_all` |
| `/api/sessions/cleanup` | POST | Cleanup expired sessions | `cleanup` |
| `/api/sessions/revoke` | POST | Revoke specific session | `revoke` |

### Testing

| Endpoint | Method | Description | Permission Required |
|----------|--------|-------------|---------------------|
| `/api/testhola` | POST | Test HOLA message generation | `testhola` |

**Request**:
```json
{
  "recipient": "MUNDO"
}
```

**Response**:
```json
{
  "hola": "HOLA/MUNDO/bkbvehbdcrgm/2026-04-19T10:47:00.000Z/4F9A3C7E.../API.IDENTYCLAW.COM/dGVzdA.../M",
  "components": {
    "recipient": "MUNDO",
    "tokenId": "bkbvehbdcrgm",
    "timestamp": "2026-04-19T10:47:00.000Z",
    "noncetsHex": "4F9A3C7E2D1B9A4CDEADBEEFCAFEBABE",
    "signature": "dGVzdA...",
    "checksum": "M"
  }
}
```

---

## DID Resolution

**Status:** Experimental (OpenAPI). **Method specification:** [did-rodit-method.md](did-rodit-method.md).

Protected endpoints for DID resolution (require JWT authentication). Primary identifier: `did:rodit:<12-letter-passport-id>`. Alias: `did:web:<host>:token:<passport-id>`. Resolution uses the server’s `NEAR_CONTRACT_ID` on NEAR mainnet.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/did/rodit/{tokenId}` | GET | Get DID document for IdentyClaw Passport |
| `/.well-known/did/resolve` | GET | Resolve DID from token ID (query param: `did`) |
| `/.well-known/did/web/token/{tokenId}` | GET | Get DID:web document |
| `/.well-known/did/web/token/{tokenId}/did.json` | GET | Get DID:web JSON document |

**Example** (`GET /.well-known/did/resolve?did=did:rodit:bkbvehbdcrgm`):

See [did-rodit-method.md §5](did-rodit-method.md#5-did-document) for the full document shape. Illustrative fields:

```json
{
  "id": "did:rodit:bkbvehbdcrgm",
  "alsoKnownAs": [
    "did:web:api.identyclaw.com:token:bkbvehbdcrgm"
  ],
  "controller": "<near-owner-account-id>",
  "verificationMethod": [
    {
      "id": "did:rodit:bkbvehbdcrgm#controller",
      "type": "Ed25519VerificationKey2020",
      "publicKeyBase58": "..."
    }
  ],
  "authentication": [
    "did:rodit:bkbvehbdcrgm#controller"
  ],
  "service": [
    "RoditTokenMetadata",
    "MCPDiscoveryService"
  ]
}
```

---

## MCP Resources

Machine-readable capabilities for AI agent discovery (public endpoints).

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/mcp/resources` | GET | List all available MCP resources |
| `/api/mcp/resource/{uri}` | GET | Get specific MCP resource by URI |
| `/api/mcp/schema` | GET | Get MCP schema definition |

**GET /api/mcp/resources**:

Lists all available MCP resources for AI agent integration.

**Response**:
```json
{
  "resources": [
    {
      "uri": "jsonld:context",
      "name": "JSON-LD Context",
      "description": "JSON-LD context for semantic mappings",
      "mimeType": "application/ld+json"
    },
    {
      "uri": "jsonld:contract-metadata",
      "name": "Contract Metadata",
      "description": "Contract metadata as JSON-LD",
      "mimeType": "application/ld+json"
    },
    {
      "uri": "howto:enrollment",
      "name": "Enrollment Guide",
      "description": "Complete enrollment guide with pricing",
      "mimeType": "text/markdown"
    },
    {
      "uri": "howto:authentication",
      "name": "Authentication Flows",
      "description": "API login and HOLA protocol flows",
      "mimeType": "text/markdown"
    },
    {
      "uri": "howto:hola-protocol",
      "name": "HOLA Protocol",
      "description": "HOLA protocol specification",
      "mimeType": "text/markdown"
    }
  ],
  "requestId": "01HQXYZ..."
}
```

**GET /api/mcp/resource/{uri}**:

Retrieve a specific MCP resource by URI.

**Example**: `GET /api/mcp/resource/jsonld:context`

**Response**: Returns the resource content (format varies by resource type)

---

## Policy Documents

Public policy documents (no authentication required).

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/terms-of-service` | GET | Terms of Service |
| `/.well-known/privacy-policy` | GET | Privacy Policy |
| `/.well-known/data-retention` | GET | Data Retention Policy |
| `/.well-known/why-identyclaw` | GET | Use cases and benefits of IdentyClaw |

---

## Rate Limiting

All endpoints are subject to rate limiting based on your IdentyClaw Passport's `max_requests` and `maxrq_window` settings.

**Headers**:
- `X-RateLimit-Limit` - Maximum requests allowed
- `X-RateLimit-Remaining` - Requests remaining in current window
- `X-RateLimit-Reset` - Unix timestamp when limit resets

**Response** (rate limit exceeded):
```json
{
  "statusCode": 429,
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded",
  "details": {
    "limit": 1000,
    "window": 3600,
    "resetAt": "2026-04-19T11:47:00.000Z"
  }
}
```

---

## Error Codes

Common error codes across all endpoints:

| Code | Status | Description |
|------|--------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid JWT token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

### Authentication Errors

| Code | Status | Description |
|------|--------|-------------|
| `SIGNATURE_VERIFICATION_FAILED_035` | 401 | Signature verification failed |
| `TOKEN_EXPIRED` | 401 | IdentyClaw Passport expired |
| `TOKEN_NOT_FOUND` | 404 | IdentyClaw Passport not found |
| `INVALID_TOKEN_ID` | 400 | Invalid token ID format |

### HOLA Errors

HTTP failures from `/api/testhola` and early validation on `/api/identity/verify` use these **`error.code`** values (HOLA lane — **base32** line signature, **HOLA nonce** from `GET /api/holanonce16ts`, ISO timestamp from that nonce response in the line):

| Code | Status | Description |
|------|--------|-------------|
| `HOLA_VALIDATION_FAILED` | 400 | Shape, envelope, transport lint, format, fields, token id, nonce hex, checksum, etc. Use `error.details.reasonCode` for the specific fault. |
| `HOLA_TIMESTAMP_INVALID` | 400 | HOLA line timestamp not valid ISO-8601, or outside allowed freshness window on `/api/testhola`. |
| `HOLA_SIGNATURE_INVALID` | 400 | HOLA line signature verification failed on `/api/testhola`; peer verify often returns HTTP 200 with `failureReasons`. |
| `HOLA_RESPONSE_FAILED` | 400 | Server could not build outbound test HOLA (`/api/testhola` only) |

Peer verification outcomes (`verified`, `failureReasons`) on `POST /api/identity/verify` are documented in [HOLA agent authentication](hola-agent-authentication.md).

### Login (JWT) verification errors

`POST /api/login` credential failures (HTTP 401 when silent login is off) use **login-lane** codes — not `HOLA_*`. Full list: [login-authentication.md — Machine-readable login errors](login-authentication.md#machine-readable-login-errors).

| Code | Status | Description |
|------|--------|-------------|
| `LOGIN_CHALLENGE_TIMESTAMP_INVALID` | 401 | Login challenge Unix `timestamp` rejected; must align with **login challenge pair** from `GET /api/login/timestamp`. |
| `LOGIN_BASE64URL_SIGNATURE_INVALID` | 401 | **base64url login signature** did not verify over UTF-8 **login signing payload** (`roditid` or `accountid` + canonical `timestamp_iso` from that challenge). |
| `WEBHOOK_SIGNATURE_INVALID` | 401 | Webhook Ed25519 verification failed (outbound webhooks; not returned from `POST /api/login`). |

Other chain or policy outcomes on login (`RODIT_NOT_FOUND`, `RODIT_NOT_LIVE`, …) are listed in the same login guide section.

## Versioning

See **[versioning.md](versioning.md)** — HTTP API release in swagger; RODiT JSON-LD `version` only via MCP from chain; `did:rodit` has no separate version.

**HTTP API release** — only [`api-docs/swagger.json`](../api-docs/swagger.json) `info.version`. Surfaces: `GET /`, `GET /openapi.json`, MCP health/service info. Logged at boot as `apiReleaseVersion` in the configuration snapshot. Different **development** vs **main** API versions are done by committing different swagger on each branch (not via `config/development.json`). CI: `npm run validate:version`.

`X-API-Version` is **not** implemented.

---

## Next Steps

- [API Login Authentication](login-authentication.md)
- [HOLA Protocol (Inter-Agent)](hola-agent-authentication.md)
- [Understand token metadata](token-metadata.md)
- [View JSON-LD integration](jsonld-metadata.md)
- [Return to main guide](skills.md)
- [Interactive API docs](https://api.identyclaw.com/docs)
